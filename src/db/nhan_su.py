"""Thao tác bảng NhanSu - chỉ xóa mềm (IsActive = 0), không bao giờ DELETE.

Quy tắc nghiệp vụ: ngừng nhân sự thì ngừng luôn các bản ghi PhanCong đang hoạt động của
nhân sự đó, trong cùng giao dịch. Kích hoạt lại nhân sự KHÔNG tự khôi phục PhanCong.

GIẢ ĐỊNH CẦN ĐỐI CHIẾU SCHEMA THẬT: NhanSu có khóa `Id`; PhanCong liên kết qua cột `NhanSuId`;
cả hai bảng có cờ `IsActive` (BIT). Nếu tên cột khác, sửa trực tiếp các câu SQL bên dưới
(giữ dạng chuỗi hằng, không ghép chuỗi).

Ví dụ:
    with get_connection(DbConfig.from_env(read_only=False)) as conn, transaction(conn):
        deactivate(conn, 42)
"""

from __future__ import annotations

from typing import Any, NamedTuple

from src.db.connection import execute_write, fetch_all

_SQL_EXISTS = "SELECT IsActive FROM NhanSu WHERE Id = ?"
_SQL_SET_ACTIVE = "UPDATE NhanSu SET IsActive = ? WHERE Id = ? AND IsActive = ?"
_SQL_LIST_ACTIVE = "SELECT * FROM NhanSu WHERE IsActive = 1 ORDER BY Id"
_SQL_DEACTIVATE_PHAN_CONG = "UPDATE PhanCong SET IsActive = 0 WHERE NhanSuId = ? AND IsActive = 1"


class NhanSuNotFoundError(LookupError):
    """Không có nhân sự với mã đã cho."""


class DeactivateResult(NamedTuple):
    nhan_su_changed: bool  # False nếu nhân sự đã ngừng hoạt động từ trước
    phan_cong_count: int  # số bản ghi PhanCong vừa được ngừng


def _set_active(conn: Any, nhan_su_id: int, active: bool) -> bool:
    new, old = (1, 0) if active else (0, 1)
    if execute_write(conn, _SQL_SET_ACTIVE, (new, nhan_su_id, old)) == 1:
        return True
    # Không dòng nào đổi: hoặc đã ở trạng thái đích (bình thường), hoặc mã không tồn tại.
    if not fetch_all(conn, _SQL_EXISTS, (nhan_su_id,)):
        raise NhanSuNotFoundError(f"Không tìm thấy nhân sự Id = {nhan_su_id}")
    return False


def deactivate(conn: Any, nhan_su_id: int) -> DeactivateResult:
    """Xóa mềm nhân sự (IsActive = 0) và ngừng luôn các PhanCong đang hoạt động của họ.

    PhanCong vẫn được dọn kể cả khi nhân sự đã ngừng từ trước, để sửa dữ liệu lệch.
    Không tự commit - gọi trong khối `transaction(conn)` để hai bảng đổi cùng nhau.
    """
    changed = _set_active(conn, nhan_su_id, active=False)
    phan_cong_count = execute_write(conn, _SQL_DEACTIVATE_PHAN_CONG, (nhan_su_id,))
    return DeactivateResult(changed, max(phan_cong_count, 0))


def reactivate(conn: Any, nhan_su_id: int) -> bool:
    """Khôi phục: đặt IsActive = 1. Trả về False nếu đang hoạt động sẵn.

    Không khôi phục PhanCong: phân công cũ có thể đã hết hiệu lực, cần giao lại có chủ đích.
    """
    return _set_active(conn, nhan_su_id, active=True)


def list_active(conn: Any) -> list[dict[str, Any]]:
    """Danh sách nhân sự đang hoạt động (mọi truy vấn nghiệp vụ phải lọc IsActive = 1)."""
    return fetch_all(conn, _SQL_LIST_ACTIVE)
