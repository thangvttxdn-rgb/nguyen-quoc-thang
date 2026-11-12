#!/usr/bin/env python3
"""Nhúng registry.json vào docs/ai-command-center.html (giữa hai dấu REGISTRY).

    python .claude/tong-chi-huy/build_page.py          # ghi lại trang
    python .claude/tong-chi-huy/build_page.py --check  # chỉ kiểm tra trang đã khớp registry
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

GOC = Path(__file__).resolve().parents[2]
REGISTRY = GOC / ".claude" / "tong-chi-huy" / "registry.json"
TRANG = GOC / "docs" / "ai-command-center.html"
MO = '<script id="registry" type="application/json">'
DONG = "</script><!-- /REGISTRY -->"


def sinh(trang: str, reg: dict) -> str:
    dau, giua = trang.split(MO, 1)
    _, cuoi = giua.split(DONG, 1)
    # "</" trong JSON sẽ đóng thẻ script sớm - thoát thành "<\/".
    du_lieu = json.dumps(reg, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    return f"{dau}{MO}{du_lieu}{DONG}{cuoi}"


def main(argv: list[str]) -> int:
    reg = json.loads(REGISTRY.read_text(encoding="utf-8"))
    cu = TRANG.read_text(encoding="utf-8")
    moi = sinh(cu, reg)
    if "--check" in argv:
        if moi != cu:
            print("Trang chưa khớp registry. Chạy: python .claude/tong-chi-huy/build_page.py")
            return 1
        return 0
    TRANG.write_text(moi, encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
