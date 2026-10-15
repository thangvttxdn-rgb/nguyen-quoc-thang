"""Kiểm thử giao phân công mới (src/db/phan_cong.py)."""

import pytest

from examples.vi_du_ngung_nhan_su import tao_csdl_mau
from src.db import nhan_su, phan_cong
from src.db.connection import transaction

# --- Kết nối giả: kiểm tra đúng câu lệnh và thứ tự --------------------------------


def test_giao_viec_cho_nhan_su_dang_hoat_dong(conn):
    conn.will_return(columns=["IsActive"], rows=[(1,)])
    conn.will_return(columns=["Id"], rows=[])
    conn.will_return(rowcount=1)
    phan_cong.add(conn, 42, "  Khám đoàn tàu   SE3  ")
    sql, params = conn.executed[-1]
    assert sql == phan_cong._SQL_INSERT
    assert params == (42, "Khám đoàn tàu SE3")  # đã gọn khoảng trắng


def test_nhan_su_khong_ton_tai(conn):
    conn.will_return(columns=["IsActive"], rows=[])
    with pytest.raises(nhan_su.NhanSuNotFoundError, match="42"):
        phan_cong.add(conn, 42, "Khám tàu")
    assert len(conn.executed) == 1  # không chạy tới câu INSERT


def test_nhan_su_da_ngung_khong_duoc_giao(conn):
    conn.will_return(columns=["IsActive"], rows=[(0,)])
    with pytest.raises(phan_cong.NhanSuInactiveError):
        phan_cong.add(conn, 42, "Khám tàu")
    assert len(conn.executed) == 1


def test_khong_tao_trung(conn):
    conn.will_return(columns=["IsActive"], rows=[(1,)])
    conn.will_return(columns=["Id"], rows=[(11,)])
    with pytest.raises(phan_cong.PhanCongDuplicateError):
        phan_cong.add(conn, 42, "Khám tàu")
    assert all(not sql.startswith("INSERT") for sql, _ in conn.executed)


@pytest.mark.parametrize("noi_dung", ["", "   ", "x" * (phan_cong.MAX_NOI_DUNG + 1)])
def test_noi_dung_khong_hop_le(conn, noi_dung):
    with pytest.raises(ValueError):
        phan_cong.add(conn, 42, noi_dung)
    assert conn.executed == []


# --- SQLite thật: câu SQL chạy được, dữ liệu đúng ----------------------------------


def test_sqlite_giao_viec_moi_va_liet_ke():
    db = tao_csdl_mau()
    with transaction(db):
        phan_cong.add(db, 1, "Khám đoàn tàu SE5 tại ga Đà Nẵng")
    assert [r["NoiDung"] for r in phan_cong.list_active(db, 1)] == [
        "Khám đoàn tàu SE1 tại ga Đà Nẵng",
        "Khám đoàn tàu SE5 tại ga Đà Nẵng",
    ]


def test_sqlite_giao_lai_viec_cu_sau_khi_kich_hoat_lai():
    db = tao_csdl_mau()
    with transaction(db):
        nhan_su.deactivate(db, 2)
    with pytest.raises(phan_cong.NhanSuInactiveError), transaction(db):
        phan_cong.add(db, 2, "Khám đoàn tàu SE3 tại ga Diêu Trì")
    with transaction(db):
        nhan_su.reactivate(db, 2)
        # Nội dung trùng phân công cũ đã ngừng vẫn được giao lại.
        phan_cong.add(db, 2, "Khám đoàn tàu SE3 tại ga Diêu Trì")
    assert len(phan_cong.list_active(db, 2)) == 1


def test_sqlite_trung_thi_rollback_ca_giao_dich():
    db = tao_csdl_mau()
    with pytest.raises(phan_cong.PhanCongDuplicateError), transaction(db):
        phan_cong.add(db, 3, "Kiểm tra hãm đoàn tàu SE21")
        phan_cong.add(db, 3, "Kiểm tra hãm đoàn tàu SE21")
    # Phân công đầu cũng bị hoàn tác cùng giao dịch.
    assert [r["NoiDung"] for r in phan_cong.list_active(db, 3)] == ["Trưởng ca trạm Nha Trang"]
