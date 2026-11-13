#!/usr/bin/env python3
"""Hook UserPromptSubmit - Tổng chỉ huy: phân tích yêu cầu và giao việc mỗi lần người dùng gõ chat.

Đọc .claude/tong-chi-huy/registry.json, đối chiếu từ khóa trong yêu cầu với bảng định tuyến,
rồi nạp một kế hoạch ngắn (việc chính, hỗ trợ, cổng kiểm soát, cảnh báo) làm ngữ cảnh cho trợ lý.

- Không chạy với lệnh bắt đầu bằng "/" hoặc yêu cầu chứa "#khong-dieu-phoi".
- Không lặp lại nguyên văn yêu cầu (tránh tiêm lệnh qua ngữ cảnh), chỉ in từ khóa đã khớp.
- Mọi lỗi đều bỏ qua (exit 0) để không chặn người dùng gõ chat.
"""

from __future__ import annotations

import json
import os
import re
import sys
import unicodedata
from pathlib import Path

REGISTRY = Path(__file__).resolve().parents[1] / "tong-chi-huy" / "registry.json"
BO_QUA = "#khong-dieu-phoi"
TOI_DA_TUYEN = 2
KEM_TOI_THIEU = 2  # việc kèm phải khớp ít nhất 2 từ khóa, tránh giao nhầm vì một từ


def bo_dau(text: str) -> str:
    text = unicodedata.normalize("NFD", text.lower())
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    return text.replace("đ", "d")


def go_khong_dau(text: str) -> bool:
    """Người dùng gõ không dấu: không có chữ cái nào ngoài ASCII."""
    return not any(c.isalpha() and not c.isascii() for c in text)


def khop(tu_khoa: list[str], text: str, khong_dau: bool) -> list[str]:
    """Trả về các từ khóa xuất hiện trọn từ trong text.

    Gõ có dấu thì so có dấu ("lời" khác "lỗi"); gõ không dấu thì so sau khi bỏ dấu.
    """
    nguon = bo_dau(text) if khong_dau else unicodedata.normalize("NFC", text.lower())
    ket_qua = []
    for kw in tu_khoa:
        k = bo_dau(kw) if khong_dau else unicodedata.normalize("NFC", kw.lower())
        if re.search(r"(?<!\w)" + re.escape(k) + r"(?!\w)", nguon):
            ket_qua.append(kw)
    return ket_qua


def phan_tich(prompt: str, reg: dict) -> dict | None:
    """Chọn tối đa TOI_DA_TUYEN tuyến có nhiều từ khóa khớp nhất. None nếu không cần điều phối."""
    text = prompt.strip()
    if not text or text.startswith("/") or BO_QUA in text.lower() or len(text) < 4:
        return None
    khong_dau = go_khong_dau(text)
    diem = []
    for thu_tu, tuyen in enumerate(reg["tuyen"]):
        trung = khop(tuyen["tu_khoa"], text, khong_dau)
        if trung:
            diem.append((-len(trung), thu_tu, tuyen, trung))
    diem.sort(key=lambda x: (x[0], x[1]))
    canh_bao = [cb["noi_dung"] for cb in reg.get("canh_bao", [])
                if khop(cb["tu_khoa"], text, khong_dau)]
    chon = [(t, trung) for i, (_, _, t, trung) in enumerate(diem[:TOI_DA_TUYEN])
            if i == 0 or len(trung) >= KEM_TOI_THIEU]
    return {
        "tuyen": chon,
        "canh_bao": canh_bao,
    }


def _ten_muc(muc_id: str, muc: dict) -> str:
    m = muc.get(muc_id)
    if not m:
        return muc_id
    nhan = {"skill": "kỹ năng", "agent": "tác tử", "cmd": "lệnh", "guard": "rào chắn",
            "link": "kết nối"}[m["nhom"]]
    ten = f"{nhan} /{muc_id}" if m["nhom"] == "cmd" else f"{nhan} {muc_id}"
    if m.get("trang_thai") == "thu-nghiem":
        # Chưa kích hoạt: Claude Code không tự nạp, phải đọc file và chỉ chạy trên bản sao.
        ten += f" (THỬ NGHIỆM: đọc {m['duong_dan']}, chỉ làm trên bản sao trong sandbox)"
    return ten


def ke_hoach(kq: dict, reg: dict) -> str:
    muc = {m["id"]: m for m in reg["muc"]}
    dong = ["[TỔNG CHỈ HUY · phân tích tự động - kế hoạch đề xuất, trợ lý tự quyết theo ngữ cảnh]"]
    if not kq["tuyen"]:
        dong.append("Không khớp tuyến nào: trả lời trực tiếp. Nếu là việc nhiều bước, "
                    "áp dụng quy trình tong-chi-huy.")
    for i, (t, trung) in enumerate(kq["tuyen"], 1):
        vai = "Việc chính" if i == 1 else "Việc kèm"
        dong.append(f"{vai}: {t['ten']} (khớp: {', '.join(trung)})")
        dong.append(f"  Giao cho: {_ten_muc(t['chinh'], muc)}")
        ho_tro = [_ten_muc(h, muc) for h in t["ho_tro"]]
        if ho_tro:
            dong.append(f"  Hỗ trợ: {'; '.join(ho_tro)}")
    if kq["tuyen"]:
        dong.append("Cổng: G0 khảo sát đầu vào → G1 thực hiện → G2 kiểm tra → "
                    "G3 phản biện (văn bản/số liệu: to-phan-bien; mã: /code-review) → nghiệm thu "
                    "(AGENTS.md mục 5). Việc nhỏ được bỏ G3.")
        dong.append("Nhãn dữ liệu: THẬT / DEMO / BLOCKED / CẦN CĂN CỨ. "
                    "Không nghiệm thu thay chủ đầu tư.")
    for cb in kq["canh_bao"]:
        dong.append(f"Cảnh báo: {cb}")
    return "\n".join(dong)


def main() -> int:
    try:
        payload = json.load(sys.stdin)
        reg = json.loads(REGISTRY.read_text(encoding="utf-8"))
        kq = phan_tich(str(payload.get("prompt", "")), reg)
        if kq is None:
            return 0
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": ke_hoach(kq, reg),
        }}, ensure_ascii=False))
    except Exception as exc:  # không bao giờ chặn người dùng gõ chat
        if os.environ.get("DIEU_PHOI_DEBUG"):
            print(f"dieu_phoi: {exc}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
