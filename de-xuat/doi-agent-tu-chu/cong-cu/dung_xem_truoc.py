"""Sinh XEM-TRUOC-TOAN-BO.html từ trang mẫu + bằng chứng (rao-chan.json) + ước tính chi phí.

Bảng rào chắn lấy nguyên từ bang-chung/rao-chan.json (chạy khao_sat_rao_chan.py trước).
Bảng chi phí tính bằng chi_phi.uoc_tinh với giả định ghi trong GIA_DINH (nhãn DEMO trên trang).
"""

from __future__ import annotations

import html
import json
from decimal import Decimal
from pathlib import Path

from chi_phi import uoc_tinh

THU_MUC = Path(__file__).resolve().parents[1]
# (tên, model, số lượt gọi, token vào mới, token đọc cache, token ra) MỖI LƯỢT - giả định DEMO.
GIA_DINH = [
    ("Tổng chỉ huy (Opus)", "claude-opus-5-5", 8, 3000, 50000, 800),
    ("Tổng chỉ huy (Sonnet)", "claude-sonnet-5-5", 8, 3000, 50000, 800),
    ("A1 Phân tích (Sonnet)", "claude-sonnet-5-5", 12, 3000, 20000, 700),
    ("A2 Triển khai (Sonnet)", "claude-sonnet-5-5", 15, 3000, 25000, 900),
    ("A3 Kiểm thử (Haiku)", "claude-haiku-5-5", 10, 3000, 18000, 400),
    ("A4 Phản biện (Opus)", "claude-opus-5-5", 6, 3000, 25000, 800),
    ("1 Agent Sonnet làm hết", "claude-sonnet-5-5", 20, 3000, 30000, 900),
]
NHAN = {"deny": "THAT", "ask": "ASK", "lọt": "BLOCKED"}  # chặn = xanh, lọt = đỏ
CHU = {"deny": "chặn", "ask": "hỏi", "lọt": "lọt", "-": "-"}


def _o(gia_tri: str) -> str:
    if gia_tri not in NHAN:
        return html.escape(gia_tri)
    return f'<span class="nhan {NHAN[gia_tri]}">{CHU[gia_tri]}</span>'


def bang_rao_chan() -> str:
    dong = json.loads((THU_MUC / "bang-chung" / "rao-chan.json").read_text(encoding="utf-8"))
    ra = []
    for d in dong:
        ra.append(
            f"      <tr><td><code>{html.escape(d['thao_tac'])}</code></td>"
            f"<td>{html.escape(d['luat_permissions_phan_tich'])}</td>"
            f"<td>{_o(d['guard_hien_hanh_THAT'])}</td><td>{_o(d['hook_git_de_xuat_THAT'])}</td></tr>")
    return "\n".join(ra)


def thanh_chi_phi() -> str:
    ra = []
    for ten, model, luot, vao, doc, ra_tok in GIA_DINH:
        usd = (uoc_tinh(model, vao, ra_tok, doc) * luot).quantize(Decimal("0.001"))
        phan_tram = min(Decimal(100), usd * 100)
        lop = ' class="vuot"' if usd > Decimal("0.385") else ""
        ra.append(
            f'    <div class="dong-cp"><span class="ten">{html.escape(ten)} · {luot} lượt</span>'
            f'<span class="thanh" role="img" aria-label="{usd} USD"><i{lop} '
            f'style="width:{phan_tram}%"></i></span><span class="so">{usd} $</span></div>')
    return "\n".join(ra)


def main() -> None:
    mau = (THU_MUC / "xem-truoc.mau.html").read_text(encoding="utf-8")
    trang = mau.replace("<!--RAO_CHAN-->", bang_rao_chan())
    trang = trang.replace("<!--CHI_PHI-->", thanh_chi_phi())
    (THU_MUC / "XEM-TRUOC-TOAN-BO.html").write_text(trang, encoding="utf-8")
    print("Đã sinh XEM-TRUOC-TOAN-BO.html")


if __name__ == "__main__":
    main()
