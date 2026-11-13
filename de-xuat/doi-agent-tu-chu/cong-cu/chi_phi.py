"""Đo và ước tính chi phí một lượt nhiệm vụ (bản mẫu, chưa nối vào cấu hình thật).

- `do_transcript`: cộng token THẬT từ transcript .jsonl của Claude Code
  (mỗi requestId tính 1 lần), gồm cả transcript tác tử phụ trong thư mục cùng tên phiên.
- `uoc_tinh`: ước tính trước khi chạy từ số token dự kiến.
- `kiem_ngan_sach`: so với ngân sách VNĐ. Không có tỷ giá -> BLOCKED (không tự đoán tỷ giá).

Giá: bảng của kỹ năng claude-api (bản lưu 2026-11-03), giá niêm yết API, USD / 1 triệu token.
Gói thuê bao (Pro/Max/Team) không tính tiền theo token: con số chỉ là quy đổi tham chiếu.
"""

from __future__ import annotations

import json
import os
import sys
from dataclasses import dataclass, field
from decimal import Decimal
from pathlib import Path

# (đầu vào, đầu ra, đọc cache). None = chưa có căn cứ.
BANG_GIA_USD = {
    "claude-opus-5-5": (Decimal("4"), Decimal("20"), Decimal("0.20")),
    "claude-sonnet-5-5": (Decimal("2"), Decimal("10"), Decimal("0.10")),
    "claude-haiku-5-5": (Decimal("0.10"), Decimal("0.50"), None),
}
# Hệ số ghi cache so với giá đầu vào - CẦN CĂN CỨ (theo quy tắc giá chung, chưa đối chiếu hóa đơn).
HE_SO_GHI_CACHE = {"5m": Decimal("1.25"), "1h": Decimal("2")}
HE_SO_DOC_CACHE_MAC_DINH = Decimal("0.1")  # dùng khi bảng giá thiếu - CẦN CĂN CỨ
TRIEU = Decimal(1_000_000)


@dataclass
class TongHop:
    so_luot_goi: int = 0
    dau_vao: int = 0
    dau_ra: int = 0
    doc_cache: int = 0
    ghi_cache_5m: int = 0
    ghi_cache_1h: int = 0
    usd: Decimal = Decimal(0)
    theo_model: dict = field(default_factory=dict)
    model_chua_co_gia: set = field(default_factory=set)

    def as_dict(self) -> dict:
        return {
            "so_luot_goi": self.so_luot_goi,
            "token_dau_vao": self.dau_vao,
            "token_dau_ra": self.dau_ra,
            "token_doc_cache": self.doc_cache,
            "token_ghi_cache_5m": self.ghi_cache_5m,
            "token_ghi_cache_1h": self.ghi_cache_1h,
            "usd": str(self.usd.quantize(Decimal("0.0001"))),
            "theo_model": {k: str(v.quantize(Decimal("0.0001")))
                           for k, v in self.theo_model.items()},
            "model_chua_co_gia": sorted(self.model_chua_co_gia),
        }


def gia_mot_luot(model: str, usage: dict) -> Decimal | None:
    gia = BANG_GIA_USD.get(model)
    if gia is None:
        return None
    vao, ra, doc = gia
    doc = doc if doc is not None else vao * HE_SO_DOC_CACHE_MAC_DINH
    tao = usage.get("cache_creation") or {}
    ghi_5m = int(tao.get("ephemeral_5m_input_tokens", 0))
    ghi_1h = int(tao.get("ephemeral_1h_input_tokens", 0))
    if not tao:  # bản ghi cũ không tách TTL: coi như 5 phút
        ghi_5m = int(usage.get("cache_creation_input_tokens", 0))
    tien = (
        Decimal(int(usage.get("input_tokens", 0))) * vao
        + Decimal(int(usage.get("output_tokens", 0))) * ra
        + Decimal(int(usage.get("cache_read_input_tokens", 0))) * doc
        + Decimal(ghi_5m) * vao * HE_SO_GHI_CACHE["5m"]
        + Decimal(ghi_1h) * vao * HE_SO_GHI_CACHE["1h"]
    )
    return tien / TRIEU


def _cac_file(duong_dan: Path) -> list[Path]:
    """File transcript chính + transcript tác tử phụ (thư mục cùng tên phiên)."""
    files = [duong_dan]
    thu_muc = duong_dan.with_suffix("")
    if thu_muc.is_dir():
        files += sorted(thu_muc.rglob("*.jsonl"))
    return files


def do_transcript(duong_dan: str | Path) -> TongHop:
    th = TongHop()
    da_tinh: set[str] = set()
    for f in _cac_file(Path(duong_dan)):
        for dong in f.read_text(encoding="utf-8").splitlines():
            try:
                ban_ghi = json.loads(dong)
            except json.JSONDecodeError:
                continue
            msg = ban_ghi.get("message") or {}
            usage = msg.get("usage")
            if not isinstance(usage, dict):
                continue
            khoa = ban_ghi.get("requestId") or msg.get("id") or ban_ghi.get("uuid")
            if khoa in da_tinh:  # một lượt gọi API có thể ghi nhiều dòng
                continue
            da_tinh.add(khoa)
            model = msg.get("model", "?")
            th.so_luot_goi += 1
            th.dau_vao += int(usage.get("input_tokens", 0))
            th.dau_ra += int(usage.get("output_tokens", 0))
            th.doc_cache += int(usage.get("cache_read_input_tokens", 0))
            tao = usage.get("cache_creation") or {}
            th.ghi_cache_5m += int(tao.get("ephemeral_5m_input_tokens", 0))
            th.ghi_cache_1h += int(tao.get("ephemeral_1h_input_tokens", 0))
            tien = gia_mot_luot(model, usage)
            if tien is None:
                th.model_chua_co_gia.add(model)
                continue
            th.usd += tien
            th.theo_model[model] = th.theo_model.get(model, Decimal(0)) + tien
    return th


def uoc_tinh(model: str, dau_vao: int, dau_ra: int, doc_cache: int = 0) -> Decimal:
    tien = gia_mot_luot(model, {"input_tokens": dau_vao, "output_tokens": dau_ra,
                                "cache_read_input_tokens": doc_cache})
    if tien is None:
        raise ValueError(f"Chưa có giá cho model {model}")
    return tien


def ty_gia_tu_moi_truong() -> Decimal | None:
    gia_tri = os.environ.get("DOI_AGENT_TY_GIA_VND_USD", "").strip()
    return Decimal(gia_tri) if gia_tri else None


def kiem_ngan_sach(usd: Decimal, ngan_sach_vnd: Decimal, ty_gia: Decimal | None) -> dict:
    """PASS / VUOT / BLOCKED. Không có tỷ giá do chủ đầu tư duyệt thì không kết luận."""
    if ty_gia is None or ty_gia <= 0:
        return {"ket_luan": "BLOCKED", "ly_do": "Chưa có tỷ giá VNĐ/USD được duyệt."}
    vnd = (usd * ty_gia).quantize(Decimal("1"))
    chenh = vnd - ngan_sach_vnd
    return {
        "ket_luan": "PASS" if chenh <= 0 else "VUOT",
        "vnd": str(vnd),
        "ngan_sach_vnd": str(ngan_sach_vnd),
        "chenh_lech_vnd": str(chenh),
        "tran_usd_tuong_ung": str((ngan_sach_vnd / ty_gia).quantize(Decimal("0.0001"))),
    }


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("Dùng: python chi_phi.py <transcript.jsonl> [ngan_sach_vnd]", file=sys.stderr)
        return 1
    th = do_transcript(argv[1])
    ngan_sach = Decimal(argv[2]) if len(argv) > 2 else Decimal(10_000)
    kq = {"do_duoc": th.as_dict(),
          "ngan_sach": kiem_ngan_sach(th.usd, ngan_sach, ty_gia_tu_moi_truong())}
    print(json.dumps(kq, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
