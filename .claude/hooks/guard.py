#!/usr/bin/env python3
"""Hook PreToolUse: chặn những gì luật permissions (khớp mẫu chữ) không bắt được.

- Bash: mọi biến thể `rm` đệ quy + cưỡng bức; câu SQL nguy hiểm trong lệnh gọi CSDL.
- Edit/Write: ghi ra ngoài thư mục dự án; hardcode mật khẩu trong chuỗi kết nối.

Kết quả: deny -> exit 2 (lý do in ra stderr); ask -> JSON trên stdout; còn lại exit 0.
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

# Lệnh có thể chạy SQL: chỉ soi SQL trong các lệnh này để `grep "DROP TABLE"` không bị chặn nhầm.
DB_CLIENT = re.compile(r"\b(sqlcmd|osql|isql|bcp|invoke-sqlcmd|python3?|py)\b", re.IGNORECASE)

SQL_DENY = [
    (re.compile(r"\bSHUTDOWN\b", re.IGNORECASE), "SHUTDOWN máy chủ SQL"),
    (re.compile(r"\bDROP\s+DATABASE\b", re.IGNORECASE), "DROP DATABASE"),
]

# Chính sách: chỉ SELECT được tự động; mọi câu ghi/đổi cấu trúc phải có người duyệt.
SQL_ASK = re.compile(
    r"\b(ALTER|DROP|TRUNCATE|DELETE|UPDATE|INSERT|MERGE|CREATE|EXEC(UTE)?|GRANT|REVOKE)\b",
    re.IGNORECASE,
)

# Mật khẩu hardcode, bỏ qua giá trị lấy từ biến ({...}, $..., %...%) hoặc placeholder <...>.
HARDCODED_PWD = [
    # Trong chuỗi kết nối: "...;UID=sa;PWD=abc123"
    re.compile(r"(?:^|[;\"'])\s*(PWD|Password)=(?![{$%<])[^;\"'{}\s]+", re.IGNORECASE),
    # Gán literal: DB_PASSWORD = "abc123", "password": "abc123", password="abc123"
    re.compile(r"\b\w*(password|passwd|pwd)\w*[\"']?\s*[:=]\s*[\"'](?![{$%<])[^\"']{3,}[\"']",
               re.IGNORECASE),
]

SEGMENT_SPLIT = re.compile(r"&&|\|\||[;|\n]")


def _is_force_recursive_rm(segment: str) -> bool:
    tokens = segment.split()
    if tokens and tokens[0] == "sudo":
        tokens = tokens[1:]
    if not tokens or os.path.basename(tokens[0]) != "rm":
        return False
    flags = set()
    for tok in tokens[1:]:
        if tok == "--":
            break
        if tok == "--recursive":
            flags.add("r")
        elif tok == "--force":
            flags.add("f")
        elif tok.startswith("-") and not tok.startswith("--"):
            flags.update(tok[1:].lower())
    return "r" in flags and "f" in flags


def check_bash(command: str) -> tuple[str, str] | None:
    for segment in SEGMENT_SPLIT.split(command):
        if _is_force_recursive_rm(segment.strip()):
            return "deny", "Cấm xóa đệ quy cưỡng bức (rm -rf và các biến thể)."
    if not DB_CLIENT.search(command):
        return None
    for pattern, label in SQL_DENY:
        if pattern.search(command):
            return "deny", f"Cấm tuyệt đối: {label}."
    match = SQL_ASK.search(command)
    if match:
        return "ask", f"Lệnh CSDL có câu {match.group(1).upper()} - chỉ SELECT được chạy tự động."
    return None


def _inside_project(file_path: str, project_dir: str) -> bool:
    root = Path(project_dir).resolve()
    target = Path(file_path)
    if not target.is_absolute():
        target = root / target
    target = target.resolve()
    return target == root or root in target.parents


def check_write(tool_input: dict, project_dir: str) -> tuple[str, str] | None:
    file_path = tool_input.get("file_path", "")
    if file_path and not _inside_project(file_path, project_dir):
        return "deny", f"Cấm ghi ra ngoài thư mục dự án: {file_path}"
    # .env (không commit) được chứa mật khẩu thật; tài liệu/mẫu chỉ có placeholder.
    name = Path(file_path).name.lower()
    if name.startswith(".env") or name.endswith((".md", ".example")):
        return None
    texts = [tool_input.get("content", ""), tool_input.get("new_string", "")]
    texts += [e.get("new_string", "") for e in tool_input.get("edits", [])]
    for text in texts:
        if text and any(p.search(text) for p in HARDCODED_PWD):
            return "deny", (
                "Phát hiện mật khẩu hardcode trong chuỗi kết nối. "
                "Đọc từ biến môi trường (os.environ) thay vì ghi thẳng vào mã."
            )
    return None


def decide(payload: dict, project_dir: str) -> tuple[str, str] | None:
    tool = payload.get("tool_name", "")
    tool_input = payload.get("tool_input") or {}
    if tool == "Bash":
        return check_bash(tool_input.get("command", ""))
    if tool in ("Edit", "Write", "MultiEdit"):
        return check_write(tool_input, project_dir)
    return None


def main() -> int:
    payload = json.load(sys.stdin)
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR") or payload.get("cwd") or os.getcwd()
    result = decide(payload, project_dir)
    if result is None:
        return 0
    decision, reason = result
    if decision == "deny":
        print(reason, file=sys.stderr)
        return 2
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "ask",
            "permissionDecisionReason": reason,
        }
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
