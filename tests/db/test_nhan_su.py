"""Kiểm thử xóa mềm bảng NhanSu (src/db/nhan_su.py)."""

import pytest

from src.db import nhan_su
from src.db.connection import transaction


def test_deactivate_dat_isactive_0(conn):
    conn.will_return(rowcount=1)
    assert nhan_su.deactivate(conn, 42) is True
    sql, params = conn.executed[0]
    assert sql.startswith("UPDATE NhanSu SET IsActive = ?") and params == (0, 42, 1)


def test_khong_bao_gio_phat_lenh_delete(conn):
    conn.will_return(rowcount=1)
    nhan_su.deactivate(conn, 42)
    assert all("DELETE" not in sql.upper() for sql, _ in conn.executed)


def test_deactivate_nhan_su_da_ngung_tra_ve_false(conn):
    conn.will_return(rowcount=0).will_return(columns=["IsActive"], rows=[(0,)])
    assert nhan_su.deactivate(conn, 42) is False


def test_deactivate_ma_khong_ton_tai_bao_loi(conn):
    conn.will_return(rowcount=0).will_return(columns=["IsActive"], rows=[])
    with pytest.raises(nhan_su.NhanSuNotFoundError, match="42"):
        nhan_su.deactivate(conn, 42)


def test_reactivate_dat_isactive_1(conn):
    conn.will_return(rowcount=1)
    assert nhan_su.reactivate(conn, 42) is True
    assert conn.executed[0][1] == (1, 42, 0)


def test_list_active_chi_lay_nhan_su_dang_hoat_dong(conn):
    conn.will_return(columns=["Id", "HoTen"], rows=[(1, "Nguyễn Văn A")])
    assert nhan_su.list_active(conn) == [{"Id": 1, "HoTen": "Nguyễn Văn A"}]
    assert "IsActive = 1" in conn.executed[0][0]


def test_loi_trong_giao_dich_thi_rollback(conn):
    conn.will_return(rowcount=0).will_return(columns=["IsActive"], rows=[])
    with pytest.raises(nhan_su.NhanSuNotFoundError), transaction(conn):
        nhan_su.deactivate(conn, 999)
    assert (conn.commits, conn.rollbacks) == (0, 1)
