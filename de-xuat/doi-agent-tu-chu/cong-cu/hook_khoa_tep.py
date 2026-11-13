#!/usr/bin/env python3
"""Hook PreToolUse (Edit|Write|MultiEdit) mẫu: tác tử phụ chỉ được sửa tệp của việc mình đã nhận.

- Tệp đang thuộc việc của agent khác -> deny (exit 2).
- Tác tử phụ sửa tệp không thuộc việc nào -> deny (phải nhận việc qua sổ cái trước).
- Phiên chính (không có agent_type) -> không can thiệp; guard.py vẫn chạy như cũ.
Sổ cái: biến DOI_AGENT_SO_CAI (thư mục), mặc định <dự án>/.doi-agent.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from so_cai import SoCai, chuan_hoa_tep  # noqa: E402


def tep_tuong_doi(file_path: str, goc: str) -> str:
    p = Path(file_path)
    try:
        return p.resolve().relative_to(Path(goc).resolve()).as_posix()
    except ValueError:
        return p.as_posix()


def quyet_dinh(payload: dict, so_cai: SoCai) -> tuple[str, str] | None:
    agent = payload.get("agent_type")
    if not agent:
        return None
    file_path = (payload.get("tool_input") or {}).get("file_path", "")
    if not file_path:
        return None
    tep = chuan_hoa_tep(tep_tuong_doi(file_path, payload.get("cwd") or os.getcwd()))
    chu = so_cai.chu_tep(tep)
    if chu is None:
        return "deny", f"{agent} sửa {tep} khi chưa nhận việc nào giữ tệp này trong sổ cái."
    ma, nguoi_lam = chu
    if nguoi_lam != agent:
        return "deny", f"{tep} đang thuộc {ma} do {nguoi_lam} làm - tránh hai agent sửa cùng tệp."
    return None


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0
    goc = os.environ.get("CLAUDE_PROJECT_DIR") or payload.get("cwd") or os.getcwd()
    so_cai = SoCai(os.environ.get("DOI_AGENT_SO_CAI") or Path(goc) / ".doi-agent")
    kq = quyet_dinh(payload, so_cai)
    if kq:
        print(kq[1], file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
