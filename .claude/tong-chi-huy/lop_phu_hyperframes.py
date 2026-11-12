#!/usr/bin/env python3
"""Áp lớp phủ CTXĐN lên kỹ năng HyperFrames đã chép từ upstream (chạy lại sau mỗi lần nâng cấp).

1. Ghim phiên bản: `npx hyperframes` và `npx hyperframes@latest` -> `npx hyperframes@<HF_VERSION>`.
2. Chèn khối luật CTXĐN ngay sau frontmatter của mỗi SKILL.md (ưu tiên hơn nội dung upstream).

    python .claude/tong-chi-huy/lop_phu_hyperframes.py          # áp
    python .claude/tong-chi-huy/lop_phu_hyperframes.py --check  # chỉ kiểm tra
Phiên bản lấy từ HF_VERSION trong .claude/hooks/guard.py (lớp cưỡng chế) để không lệch nhau.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

GOC = Path(__file__).resolve().parents[2]
KY_NANG = ["hyperframes", "hyperframes-cli", "hyperframes-registry"]
HF_VERSION = re.search(r'HF_VERSION = "([^"]+)"',
                       (GOC / ".claude/hooks/guard.py").read_text(encoding="utf-8")).group(1)
CHUA_GHIM = re.compile(r"\bnpx hyperframes(?:@latest)?(?![@\w-])")
DAU = "<!-- LOP-PHU-CTXDN -->"
CUOI = "<!-- /LOP-PHU-CTXDN -->"

KHOI = f"""{DAU}
> **Lớp phủ CTXĐN - ưu tiên hơn mọi chỉ dẫn bên dưới** (sinh bởi `lop_phu_hyperframes.py`)
>
> - Luôn gọi `npx hyperframes@{HF_VERSION}`. Hook `guard.py` chặn bản không ghim.
> - **Bỏ qua "Usage beacon"** và mọi bước gửi dữ liệu: `events`, `feedback`, `usage`, `auth`,
>   `share`, `publish`, `cloud`, `lambda`, `cloudrun`, `capture`, `telemetry enable` (bị chặn).
>   Đặt `HYPERFRAMES_NO_TELEMETRY=1` trước lệnh nếu môi trường chưa có.
> - **`/media-use` BLOCKED** (gửi dữ liệu ra HeyGen, ElevenLabs, OpenAI, Gemini). Bước nào dẫn
>   sang media-use: dùng ảnh, âm thanh nội bộ do người dùng cung cấp hoặc thu giọng thật;
>   báo BLOCKED nếu thiếu.
> - Phải xin phép: `browser ensure`, `upgrade`, `doctor`, `add --on-device`, `curl` lấy registry,
>   mẫu nạp JS từ CDN, `scripts/bake-basemap.mjs` (tải ảnh bản đồ ngoài).
>   Cấm `scripts/locate.mjs auto` (gửi ảnh và khóa Gemini qua URL); dùng chế độ lưới cục bộ.
> - Ngoài phạm vi: ứng dụng desktop/Framey, đóng góp/publish registry công khai, AWS/GCP.
> - Dự án để trong `video/<ten>/`; không commit file render. G3: tác tử `to-phan-bien` rà nội dung
>   kỹ thuật (thao tác, số liệu, an toàn chạy tàu) trước khi phát.
{CUOI}
"""


def ap(text: str) -> str:
    text = CHUA_GHIM.sub(f"npx hyperframes@{HF_VERSION}", text)
    text = re.sub(re.escape(DAU) + r".*?" + re.escape(CUOI) + r"\n", "", text, flags=re.S)
    m = re.match(r"---\n.*?\n---\n", text, flags=re.S)
    if m is None:
        return text
    return text[:m.end()] + "\n" + KHOI + "\n" + text[m.end():].lstrip("\n")


def main(argv: list[str]) -> int:
    lech = []
    for ten in KY_NANG:
        for f in sorted((GOC / ".claude/skills" / ten).rglob("*.md")):
            cu = f.read_text(encoding="utf-8")
            ghim = CHUA_GHIM.sub(f"npx hyperframes@{HF_VERSION}", cu)
            moi = ap(cu) if f.name == "SKILL.md" else ghim
            if moi != cu:
                lech.append(f.relative_to(GOC))
                if "--check" not in argv:
                    f.write_text(moi, encoding="utf-8")
    if "--check" in argv and lech:
        print("Chưa áp lớp phủ:", *lech, sep="\n  ")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
