#!/usr/bin/env python3
"""Hook PreToolUse (Bash) mẫu: chặn Git phá hủy/phát hành, đọc tệp bí mật, hỏi khi gửi ra mạng.

Luật `Bash(git push --force *)` không khớp `git push origin main --force`; hook này soi từng đoạn
lệnh sau khi tách token. Đề xuất gộp vào .claude/hooks/guard.py sau khi được duyệt (kèm test).
"""

from __future__ import annotations

import json
import re
import shlex
import sys

TACH_DOAN = re.compile(r"&&|\|\||[;|\n]")
NHANH_CHINH = {"main", "master"}


def _token(doan: str) -> list[str]:
    try:
        return shlex.split(doan, posix=True)
    except ValueError:
        return doan.split()


def _bo_tuy_chon_git(tok: list[str]) -> list[str]:
    """Bỏ 'git' và tùy chọn toàn cục (-C dir, -c k=v) để lấy lệnh con."""
    i = 1
    while i < len(tok) and tok[i].startswith("-"):
        i += 2 if tok[i] in ("-C", "-c") else 1
    return tok[i:]


def kiem_git(lenh: str) -> tuple[str, str] | None:
    for doan in TACH_DOAN.split(lenh):
        tok = _token(doan.strip())
        if tok and tok[0] in ("sudo", "env"):
            tok = tok[1:]
        if tok[:2] == ["gh", "pr"] and len(tok) > 2 and tok[2] == "merge":
            return "deny", "Agent không tự merge PR - GATE 4 là của con người."
        if not tok or tok[0] != "git":
            continue
        con = _bo_tuy_chon_git(tok)
        if not con:
            continue
        lenh_con, doi = con[0], con[1:]
        co = {d for d in doi if d.startswith("-")}
        if lenh_con == "push":
            if co & {"--force", "-f", "--force-with-lease", "--force-if-includes", "--mirror",
                     "--delete", "-d"} or any(d.startswith(("--force-with-lease=", "+"))
                                              for d in doi) or any(":+" in d for d in doi):
                return "deny", "Cấm push cưỡng bức/xóa nhánh từ xa."
            dich = [d.split(":")[-1] for d in doi if not d.startswith("-")][1:]
            if NHANH_CHINH & {d.removeprefix("refs/heads/") for d in dich}:
                return "deny", "Cấm push thẳng lên nhánh chính."
        if lenh_con == "reset" and "--hard" in co:
            return "deny", "Cấm git reset --hard (mất thay đổi chưa commit)."
        if lenh_con == "clean" and any("f" in d.lstrip("-") for d in co if not d.startswith("--")):
            return "deny", "Cấm git clean -f (xóa tệp chưa theo dõi)."
        if lenh_con == "branch" and co & {"-D", "--delete", "-d"}:
            return "ask", "Xóa nhánh cần người duyệt."
        if lenh_con in ("checkout", "restore") and "." in doi:
            return "ask", "Ghi đè thay đổi trong cây làm việc cần người duyệt."
        if lenh_con == "worktree" and doi[:1] == ["remove"] and co & {"--force", "-f"}:
            return "ask", "Xóa worktree cưỡng bức có thể mất thay đổi chưa commit."
        if lenh_con in ("merge", "rebase", "tag") and not co & {"--abort", "--continue", "-l",
                                                                 "--list"}:
            return "ask", f"git {lenh_con} thay đổi lịch sử/phát hành - cần người duyệt."
    return None


# Tệp bí mật: .env và .env.<tên> (trừ .env.example), thư mục secrets/, web.config thật.
TEP_BI_MAT = re.compile(
    r"(?:^|[\s\"'=@/\\])(?:\.env(?!\.example\b)(?:\.\w+)?|secrets[/\\]\S*|deploy[/\\]iis[/\\]web\.config)"
    r"(?=$|[\s\"';|&)])",
    re.IGNORECASE,
)
GUI_RA_NGOAI = re.compile(r"(?:^|[\s;&|])(?:curl|wget|invoke-webrequest|iwr|scp|nc)\b",
                          re.IGNORECASE)


def kiem_bi_mat(lenh: str) -> tuple[str, str] | None:
    if TEP_BI_MAT.search(lenh):
        return "deny", "Agent không đọc/xuất tệp bí mật (.env, secrets/, web.config thật)."
    return None


def kiem_an_toan(lenh: str) -> tuple[str, str] | None:
    kq = kiem_bi_mat(lenh) or kiem_git(lenh)
    if kq is None and GUI_RA_NGOAI.search(lenh):
        return "ask", "Lệnh gửi/nhận dữ liệu qua mạng cần người duyệt."
    return kq


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0
    if payload.get("tool_name") != "Bash":
        return 0
    kq = kiem_an_toan((payload.get("tool_input") or {}).get("command", ""))
    if kq is None:
        return 0
    if kq[0] == "deny":
        print(kq[1], file=sys.stderr)
        return 2
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse",
                                             "permissionDecision": "ask",
                                             "permissionDecisionReason": kq[1]}},
                     ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
