"""Sổ cái nhiệm vụ đội Agent (bản mẫu, chưa nối vào cấu hình thật).

Một file JSON là nguồn sự thật cho: mã việc, người chịu trách nhiệm, tiêu chí hoàn thành, tệp đang
khóa, số lần sửa lỗi, chi phí. Nhật ký chuyển giao ghi riêng dạng JSONL (chỉ thêm, không sửa).

- Ghi nguyên tử (file tạm + os.replace) để phiên bị ngắt vẫn đọc lại được (khôi phục).
- Khóa sổ bằng file .lock tạo độc quyền (O_EXCL) - chạy được trên cả Windows và Linux.
- Một tệp chỉ thuộc một việc đang làm: nhận việc trùng tệp -> XungDot.
- Sửa lỗi quá TOI_DA_LAN_SUA lần -> việc chuyển "dung", phải có người duyệt mới mở lại.
- Ước chi phí vượt trần -> NganSachBlocked, không cho nhận việc.
"""

from __future__ import annotations

import json
import os
import re
import time
from contextlib import contextmanager
from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path, PurePosixPath

TOI_DA_LAN_SUA = 3
TRANG_THAI = ("cho", "dang-lam", "cho-duyet", "xong", "dung", "huy")
# Không để khóa bí mật lọt vào nhật ký.
MAU_BI_MAT = re.compile(
    r"(sk-ant-[\w-]+|gh[pousr]_\w{20,}|(?i:(pwd|password|mat_khau|token|secret)\s*[:=]\s*\S+))"
)


class LoiSoCai(Exception):
    pass


class XungDot(LoiSoCai):
    pass


class NganSachBlocked(LoiSoCai):
    pass


class DaDung(LoiSoCai):
    pass


def _bay_gio() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def chuan_hoa_tep(duong_dan: str) -> str:
    """So khớp tệp không phụ thuộc dấu gạch Windows/Linux và chữ hoa/thường ổ đĩa."""
    return str(PurePosixPath(duong_dan.replace("\\", "/"))).lstrip("./").lower()


def che_bi_mat(text: str) -> str:
    return MAU_BI_MAT.sub("[ĐÃ CHE]", text)


class SoCai:
    def __init__(self, thu_muc: str | Path, tran_usd: Decimal | None = None):
        self.thu_muc = Path(thu_muc)
        self.thu_muc.mkdir(parents=True, exist_ok=True)
        self.file = self.thu_muc / "so-cai.json"
        self.nhat_ky = self.thu_muc / "nhat-ky.jsonl"
        self.tran_usd = tran_usd

    # ---- lưu trữ ----
    @contextmanager
    def _khoa(self, cho_toi_da: float = 5.0):
        lock = self.file.with_suffix(".lock")
        het_han = time.monotonic() + cho_toi_da
        while True:
            try:
                fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                break
            except FileExistsError:
                if time.monotonic() > het_han:
                    raise LoiSoCai("Sổ cái bị khóa quá lâu - phiên treo?") from None
                time.sleep(0.05)
        try:
            os.close(fd)
            yield
        finally:
            lock.unlink(missing_ok=True)

    def doc(self) -> dict:
        if not self.file.exists():
            return {"phien_ban": 1, "dem": 0, "viec": {}}
        return json.loads(self.file.read_text(encoding="utf-8"))

    def _ghi(self, du_lieu: dict) -> None:
        tam = self.file.with_suffix(".tmp")
        tam.write_text(json.dumps(du_lieu, ensure_ascii=False, indent=2), encoding="utf-8")
        os.replace(tam, self.file)

    def ghi_nhat_ky(self, su_kien: str, **chi_tiet) -> None:
        dong = {"luc": _bay_gio(), "su_kien": su_kien}
        dong.update({k: che_bi_mat(v) if isinstance(v, str) else v for k, v in chi_tiet.items()})
        with self.nhat_ky.open("a", encoding="utf-8") as f:
            f.write(json.dumps(dong, ensure_ascii=False) + "\n")

    # ---- nghiệp vụ ----
    def tao_viec(self, tieu_de: str, phu_trach: str, tieu_chi: list[str], tep: list[str],
                 uoc_usd: Decimal = Decimal(0), rui_ro: str = "thap") -> str:
        if not tieu_chi:
            raise LoiSoCai("Việc phải có tiêu chí hoàn thành.")
        with self._khoa():
            du_lieu = self.doc()
            du_lieu["dem"] += 1
            ma = f"NV-{datetime.now(UTC):%Y%m%d}-{du_lieu['dem']:03d}"
            du_lieu["viec"][ma] = {
                "tieu_de": tieu_de, "phu_trach": phu_trach, "tieu_chi": tieu_chi,
                "tep": sorted({chuan_hoa_tep(t) for t in tep}), "trang_thai": "cho",
                "rui_ro": rui_ro, "so_lan_sua": 0, "uoc_usd": str(uoc_usd), "chi_usd": "0",
                "tao_luc": _bay_gio(),
            }
            self._ghi(du_lieu)
        self.ghi_nhat_ky("tao", ma=ma, phu_trach=phu_trach)
        return ma

    def _tong_usd(self, du_lieu: dict, them: Decimal) -> Decimal:
        tong = sum(Decimal(v["chi_usd"]) for v in du_lieu["viec"].values())
        dang_cho = sum(Decimal(v["uoc_usd"]) for v in du_lieu["viec"].values()
                       if v["trang_thai"] == "dang-lam")
        return tong + dang_cho + them

    def nhan_viec(self, ma: str, agent: str) -> None:
        with self._khoa():
            du_lieu = self.doc()
            viec = du_lieu["viec"][ma]
            if viec["trang_thai"] == "dung":
                raise DaDung(f"{ma} đã dừng vì lỗi lặp - cần người duyệt mở lại.")
            if viec["trang_thai"] != "cho":
                raise LoiSoCai(f"{ma} đang ở trạng thái {viec['trang_thai']}.")
            if self.tran_usd is None:
                raise NganSachBlocked("Chưa có trần chi phí được duyệt.")
            if self._tong_usd(du_lieu, Decimal(viec["uoc_usd"])) > self.tran_usd:
                raise NganSachBlocked(f"{ma}: ước chi phí làm vượt trần {self.tran_usd} USD.")
            for ma_khac, khac in du_lieu["viec"].items():
                if khac["trang_thai"] != "dang-lam":
                    continue
                trung = set(khac["tep"]) & set(viec["tep"])
                if trung:
                    self.ghi_nhat_ky("xung-dot", ma=ma, voi=ma_khac, tep=sorted(trung))
                    raise XungDot(f"{ma} trùng tệp {sorted(trung)} với {ma_khac} "
                                  f"({khac['phu_trach']}).")
            viec.update(trang_thai="dang-lam", nguoi_lam=agent, nhan_luc=_bay_gio())
            self._ghi(du_lieu)
        self.ghi_nhat_ky("nhan", ma=ma, agent=agent)

    def chu_tep(self, duong_dan: str) -> tuple[str, str] | None:
        """(mã việc, agent) đang giữ tệp, hoặc None."""
        tep = chuan_hoa_tep(duong_dan)
        for ma, viec in self.doc()["viec"].items():
            if viec["trang_thai"] == "dang-lam" and tep in viec["tep"]:
                return ma, viec.get("nguoi_lam", viec["phu_trach"])
        return None

    def bao_ket_qua(self, ma: str, dat: bool, ghi_chu: str = "",
                    chi_usd: Decimal = Decimal(0)) -> str:
        with self._khoa():
            du_lieu = self.doc()
            viec = du_lieu["viec"][ma]
            viec["chi_usd"] = str(Decimal(viec["chi_usd"]) + chi_usd)
            if dat:
                viec["trang_thai"] = "cho-duyet"  # nghiệm thu là việc của con người (GATE 4)
            else:
                viec["so_lan_sua"] += 1
                viec["trang_thai"] = "dung" if viec["so_lan_sua"] >= TOI_DA_LAN_SUA else "cho"
            self._ghi(du_lieu)
        self.ghi_nhat_ky("ket-qua", ma=ma, dat=dat, lan=viec["so_lan_sua"], ghi_chu=ghi_chu)
        return viec["trang_thai"]

    def duyet(self, ma: str, nguoi_duyet: str, chap_nhan: bool) -> None:
        with self._khoa():
            du_lieu = self.doc()
            viec = du_lieu["viec"][ma]
            if viec["trang_thai"] not in ("cho-duyet", "dung"):
                raise LoiSoCai(f"{ma} chưa đến bước duyệt.")
            if viec["trang_thai"] == "dung":
                viec.update(trang_thai="cho" if chap_nhan else "huy", so_lan_sua=0)
            else:
                viec["trang_thai"] = "xong" if chap_nhan else "cho"
            viec["nguoi_duyet"] = nguoi_duyet
            self._ghi(du_lieu)
        self.ghi_nhat_ky("duyet", ma=ma, nguoi_duyet=nguoi_duyet, chap_nhan=chap_nhan)

    def khoi_phuc(self) -> list[dict]:
        """Sau gián đoạn: việc đang dở trả về hàng chờ (khóa tệp được nhả), báo danh sách."""
        dang_do = []
        with self._khoa():
            du_lieu = self.doc()
            for ma, viec in du_lieu["viec"].items():
                if viec["trang_thai"] == "dang-lam":
                    viec["trang_thai"] = "cho"
                    dang_do.append({"ma": ma, "nguoi_lam": viec.pop("nguoi_lam", None)})
            self._ghi(du_lieu)
        self.ghi_nhat_ky("khoi-phuc", so_viec=len(dang_do))
        return dang_do
