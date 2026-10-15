"""Thao tác bảng PhanCong: giao việc mới cho nhân sự đang hoạt động.

Quy tắc:
- Chỉ giao cho nhân sự tồn tại và đang hoạt động (NhanSu.IsActive = 1).
- Không tạo trùng: cùng nhân sự đã có phân công đang hiệu lực với đúng nội dung đó thì báo lỗi.
- Phân công mới luôn có IsActive = 1. Ngừng phân công đi qua `nhan_su.deactivate`.

GIẢ ĐỊNH CẦN ĐỐI CHIẾU SCHEMA THẬT: PhanCong có các cột `NhanSuId`, `NoiDung`, `IsActive`;
`Id` tự tăng (IDENTITY). Nếu tên cột khác, sửa trực tiếp các câu SQL bên dưới.

Ví dụ:
    with get_connection(DbConfig.from_env(read_only=False)) as conn, transaction(conn):
        add(conn, 42, "Khám đoàn tàu SE3 tại ga Diêu Trì")
"""

from __future__ import annotations

from typing import Any

from src.db.connection import execute_write, fetch_all
from src.db.nhan_su import NhanSuNotFoundError

_SQL_NHAN_SU_STATUS = "SELECT IsActive FROM NhanSu WHERE Id = ?"
_SQL_DUPLICATE = (
    "SELECT Id FROM PhanCong WHERE NhanSuId = ? AND NoiDung = ? AND IsActive = 1"
)
_SQL_INSERT = "INSERT INTO PhanCong (NhanSuId, NoiDung, IsActive) VALUES (?, ?, 1)"
_SQL_LIST_ACTIVE = (
    "SELECT Id, NoiDung FROM PhanCong WHERE NhanSuId = ? AND IsActive = 1 ORDER BY Id"
)

MAX_NOI_DUNG = 500  # khớp với cột NVARCHAR(500) dự kiến; chỉnh theo schema thật


class NhanSuInactiveError(ValueError):
    """Nhân sự đã ngừng hoạt động, không được giao việc."""


class PhanCongDuplicateError(ValueError):
    """Nhân sự đã có phân công đang hiệu lực với cùng nội dung."""


def add(conn: Any, nhan_su_id: int, noi_dung: str) -> None:
    """Giao một phân công mới. Không tự commit - gọi trong khối `transaction(conn)`."""
    noi_dung = " ".join(noi_dung.split())  # bỏ khoảng trắng thừa để kiểm tra trùng chính xác
    if not noi_dung:
        raise ValueError("Nội dung phân công không được để trống.")
    if len(noi_dung) > MAX_NOI_DUNG:
        raise ValueError(f"Nội dung phân công dài quá {MAX_NOI_DUNG} ký tự.")

    rows = fetch_all(conn, _SQL_NHAN_SU_STATUS, (nhan_su_id,))
    if not rows:
        raise NhanSuNotFoundError(f"Không tìm thấy nhân sự Id = {nhan_su_id}")
    if not rows[0]["IsActive"]:
        raise NhanSuInactiveError(f"Nhân sự Id = {nhan_su_id} đã ngừng hoạt động.")
    if fetch_all(conn, _SQL_DUPLICATE, (nhan_su_id, noi_dung)):
        raise PhanCongDuplicateError(
            f"Nhân sự Id = {nhan_su_id} đã có phân công đang hiệu lực: {noi_dung}"
        )

    execute_write(conn, _SQL_INSERT, (nhan_su_id, noi_dung))


def list_active(conn: Any, nhan_su_id: int) -> list[dict[str, Any]]:
    """Các phân công đang hiệu lực của một nhân sự."""
    return fetch_all(conn, _SQL_LIST_ACTIVE, (nhan_su_id,))
