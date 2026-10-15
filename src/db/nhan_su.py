"""Thao tác bảng NhanSu - chỉ xóa mềm (IsActive = 0), không bao giờ DELETE.

GIẢ ĐỊNH CẦN ĐỐI CHIẾU SCHEMA THẬT: khóa chính là cột `Id`, cờ trạng thái là `IsActive` (BIT).
Nếu tên cột khác, sửa trực tiếp các câu SQL bên dưới (giữ dạng chuỗi hằng, không ghép chuỗi).

Ví dụ:
    with get_connection(DbConfig.from_env(read_only=False)) as conn, transaction(conn):
        deactivate(conn, 42)
"""

from __future__ import annotations

from typing import Any

from src.db.connection import execute_write, fetch_all

_SQL_EXISTS = "SELECT IsActive FROM NhanSu WHERE Id = ?"
_SQL_SET_ACTIVE = "UPDATE NhanSu SET IsActive = ? WHERE Id = ? AND IsActive = ?"
_SQL_LIST_ACTIVE = "SELECT * FROM NhanSu WHERE IsActive = 1 ORDER BY Id"


class NhanSuNotFoundError(LookupError):
    """Không có nhân sự với mã đã cho."""


def _set_active(conn: Any, nhan_su_id: int, active: bool) -> bool:
    new, old = (1, 0) if active else (0, 1)
    if execute_write(conn, _SQL_SET_ACTIVE, (new, nhan_su_id, old)) == 1:
        return True
    # Không dòng nào đổi: hoặc đã ở trạng thái đích (bình thường), hoặc mã không tồn tại.
    if not fetch_all(conn, _SQL_EXISTS, (nhan_su_id,)):
        raise NhanSuNotFoundError(f"Không tìm thấy nhân sự Id = {nhan_su_id}")
    return False


def deactivate(conn: Any, nhan_su_id: int) -> bool:
    """Xóa mềm: đặt IsActive = 0. Trả về False nếu đã ngừng hoạt động từ trước.

    Không tự commit - gọi trong khối `transaction(conn)`.
    """
    return _set_active(conn, nhan_su_id, active=False)


def reactivate(conn: Any, nhan_su_id: int) -> bool:
    """Khôi phục: đặt IsActive = 1. Trả về False nếu đang hoạt động sẵn."""
    return _set_active(conn, nhan_su_id, active=True)


def list_active(conn: Any) -> list[dict[str, Any]]:
    """Danh sách nhân sự đang hoạt động (mọi truy vấn nghiệp vụ phải lọc IsActive = 1)."""
    return fetch_all(conn, _SQL_LIST_ACTIVE)
