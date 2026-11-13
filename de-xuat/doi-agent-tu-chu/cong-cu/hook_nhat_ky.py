#!/usr/bin/env python3
"""Hook SubagentStart / SubagentStop mẫu: ghi ai bắt đầu, ai kết thúc, transcript ở đâu.

Không ghi nội dung prompt hay câu trả lời (tránh lộ bí mật); chỉ ghi siêu dữ liệu.
Chi phí đo sau bằng chi_phi.py trên transcript_path. Luôn exit 0 - không chặn công việc.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import UTC, datetime
from pathlib import Path

TRUONG = ("hook_event_name", "session_id", "agent_id", "agent_type", "transcript_path",
          "agent_transcript_path", "cwd", "permission_mode")


def main() -> int:
    try:
        payload = json.load(sys.stdin)
        goc = os.environ.get("CLAUDE_PROJECT_DIR") or payload.get("cwd") or os.getcwd()
        thu_muc = Path(os.environ.get("DOI_AGENT_SO_CAI") or Path(goc) / ".doi-agent")
        thu_muc.mkdir(parents=True, exist_ok=True)
        dong = {"luc": datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")}
        dong.update({k: payload[k] for k in TRUONG if k in payload})
        with (thu_muc / "agent.jsonl").open("a", encoding="utf-8") as f:
            f.write(json.dumps(dong, ensure_ascii=False) + "\n")
    except Exception as exc:  # noqa: BLE001 - nhật ký không được chặn công việc
        if os.environ.get("DOI_AGENT_DEBUG"):
            print(f"hook_nhat_ky: {exc}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
