"""Ví dụ thực tế: một khám xa viên trạm Diêu Trì nghỉ việc, ngừng hồ sơ và phân công của họ.

Chạy được ngay, không cần SQL Server: dùng SQLite trong bộ nhớ qua một lớp chuyển đổi nhỏ,
còn toàn bộ logic chạy đúng code thật trong `src/db/` (cùng câu SQL, cùng kiểm tra an toàn).

    python -m examples.vi_du_ngung_nhan_su      # chạy từ thư mục gốc repo

Dữ liệu dưới đây là dữ liệu mẫu, không phải nhân sự thật.
"""

from __future__ import annotations

import sqlite3
from typing import Any

from src.db import nhan_su
from src.db.connection import UnsafeQueryError, execute_write, fetch_all, transaction

SCHEMA = """
CREATE TABLE NhanSu (
    Id INTEGER PRIMARY KEY, HoTen TEXT, DonVi TEXT, ChucDanh TEXT, IsActive INTEGER NOT NULL
);
CREATE TABLE PhanCong (
    Id INTEGER PRIMARY KEY, NhanSuId INTEGER REFERENCES NhanSu(Id),
    NoiDung TEXT, IsActive INTEGER NOT NULL
);
"""

NHAN_SU_MAU = [
    (1, "Nguyễn Văn An", "Trạm KCTX Đà Nẵng", "Khám xa viên", 1),
    (2, "Trần Thị Bình", "Trạm KCTX Diêu Trì", "Khám xa viên", 1),
    (3, "Lê Văn Cường", "Trạm KCTX Nha Trang", "Trưởng ca", 1),
]
PHAN_CONG_MAU = [
    (10, 1, "Khám đoàn tàu SE1 tại ga Đà Nẵng", 1),
    (11, 2, "Khám đoàn tàu SE3 tại ga Diêu Trì", 1),
    (12, 2, "Trực ca đêm tổ Quảng Ngãi", 1),
    (13, 2, "Kiểm tra hãm tàu SE22 (đã kết thúc)", 0),
    (14, 3, "Trưởng ca trạm Nha Trang", 1),
]


class SqliteConn:
    """Bọc sqlite3 cho giống pyodbc: `cursor.execute(sql, *params)`."""

    class _Cursor:
        def __init__(self, cur: sqlite3.Cursor) -> None:
            self._cur = cur

        def execute(self, sql: str, *params: Any) -> None:
            self._cur.execute(sql, params)

        @property
        def description(self) -> Any:
            return self._cur.description

        @property
        def rowcount(self) -> int:
            return self._cur.rowcount

        def fetchall(self) -> list[tuple]:
            return self._cur.fetchall()

        def close(self) -> None:
            self._cur.close()

    def __init__(self, raw: sqlite3.Connection) -> None:
        self.raw = raw

    def cursor(self) -> SqliteConn._Cursor:
        return self._Cursor(self.raw.cursor())

    def commit(self) -> None:
        self.raw.commit()

    def rollback(self) -> None:
        self.raw.rollback()

    def close(self) -> None:
        self.raw.close()


def tao_csdl_mau() -> SqliteConn:
    raw = sqlite3.connect(":memory:")
    raw.executescript(SCHEMA)
    raw.executemany("INSERT INTO NhanSu VALUES (?, ?, ?, ?, ?)", NHAN_SU_MAU)
    raw.executemany("INSERT INTO PhanCong VALUES (?, ?, ?, ?)", PHAN_CONG_MAU)
    raw.commit()
    return SqliteConn(raw)


def in_bang(conn: SqliteConn, tieu_de: str) -> None:
    print(f"\n--- {tieu_de} ---")
    for r in fetch_all(conn, "SELECT Id, HoTen, DonVi, IsActive FROM NhanSu ORDER BY Id"):
        trang_thai = "đang làm" if r["IsActive"] else "ĐÃ NGỪNG"
        print(f"  NhanSu {r['Id']}: {r['HoTen']:<15} {r['DonVi']:<22} {trang_thai}")
    for r in fetch_all(conn, "SELECT Id, NhanSuId, NoiDung, IsActive FROM PhanCong ORDER BY Id"):
        trang_thai = "hiệu lực" if r["IsActive"] else "ngừng"
        print(f"    PhanCong {r['Id']} (NS {r['NhanSuId']}): {r['NoiDung']:<38} {trang_thai}")


def main() -> None:
    conn = tao_csdl_mau()
    in_bang(conn, "Trước khi xử lý")

    # 1. Chị Bình (Id 2) nghỉ việc: ngừng hồ sơ + phân công, trong một giao dịch.
    with transaction(conn):
        kq = nhan_su.deactivate(conn, 2)
    print(f"\n[1] Ngừng nhân sự 2 -> {kq}")
    in_bang(conn, "Sau khi ngừng nhân sự 2")

    # 2. Gõ nhầm mã không tồn tại: báo lỗi, giao dịch hoàn tác, dữ liệu không đổi.
    try:
        with transaction(conn):
            nhan_su.deactivate(conn, 99)
    except nhan_su.NhanSuNotFoundError as e:
        print(f"\n[2] Mã 99: {e} -> đã rollback")

    # 3. Chị Bình quay lại làm: hồ sơ hoạt động lại, phân công cũ KHÔNG tự khôi phục.
    with transaction(conn):
        nhan_su.reactivate(conn, 2)
    con_hieu_luc = fetch_all(
        conn, "SELECT Id FROM PhanCong WHERE NhanSuId = ? AND IsActive = 1", (2,)
    )
    print(f"\n[3] Kích hoạt lại nhân sự 2 -> phân công còn hiệu lực: {len(con_hieu_luc)}")

    # 4. Cố xóa cứng: bị chặn trước khi tới CSDL.
    try:
        execute_write(conn, "DELETE FROM NhanSu WHERE Id = ?", (2,))
    except UnsafeQueryError as e:
        print(f"\n[4] Thử DELETE -> bị chặn: {e}")

    conn.close()


if __name__ == "__main__":
    main()
