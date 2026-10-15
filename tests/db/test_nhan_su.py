"""Kiểm thử xóa mềm bảng NhanSu (src/db/nhan_su.py)."""

import pytest

from src.db import nhan_su
from src.db.connection import transaction


def test_deactivate_dat_isactive_0_va_ngung_phan_cong(conn):
    conn.will_return(rowcount=1).will_return(rowcount=3)
    assert nhan_su.deactivate(conn, 42) == (True, 3)
    (sql_ns, params_ns), (sql_pc, params_pc) = conn.executed
    assert sql_ns.startswith("UPDATE NhanSu SET IsActive = ?") and params_ns == (0, 42, 1)
    assert sql_pc.startswith("UPDATE PhanCong SET IsActive = 0") and params_pc == (42,)
    assert "IsActive = 1" in sql_pc  # chỉ đụng các phân công đang hoạt động


def test_khong_bao_gio_phat_lenh_delete(conn):
    conn.will_return(rowcount=1).will_return(rowcount=2)
    nhan_su.deactivate(conn, 42)
    assert all("DELETE" not in sql.upper() for sql, _ in conn.executed)


def test_nhan_su_khong_co_phan_cong(conn):
    conn.will_return(rowcount=1).will_return(rowcount=0)
    result = nhan_su.deactivate(conn, 42)
    assert result.nhan_su_changed is True and result.phan_cong_count == 0


def test_nhan_su_da_ngung_van_don_phan_cong_con_sot(conn):
    conn.will_return(rowcount=0).will_return(columns=["IsActive"], rows=[(0,)])
    conn.will_return(rowcount=1)
    result = nhan_su.deactivate(conn, 42)
    assert result == (False, 1)
    assert conn.executed[-1][0].startswith("UPDATE PhanCong")


def test_deactivate_ma_khong_ton_tai_bao_loi_va_khong_dung_phan_cong(conn):
    conn.will_return(rowcount=0).will_return(columns=["IsActive"], rows=[])
    with pytest.raises(nhan_su.NhanSuNotFoundError, match="42"):
        nhan_su.deactivate(conn, 42)
    assert all("PhanCong" not in sql for sql, _ in conn.executed)


def test_reactivate_dat_isactive_1_va_khong_khoi_phuc_phan_cong(conn):
    conn.will_return(rowcount=1)
    assert nhan_su.reactivate(conn, 42) is True
    assert conn.executed == [(nhan_su._SQL_SET_ACTIVE, (1, 42, 0))]


def test_list_active_chi_lay_nhan_su_dang_hoat_dong(conn):
    conn.will_return(columns=["Id", "HoTen"], rows=[(1, "Nguyễn Văn A")])
    assert nhan_su.list_active(conn) == [{"Id": 1, "HoTen": "Nguyễn Văn A"}]
    assert "IsActive = 1" in conn.executed[0][0]


def test_hai_bang_doi_cung_mot_giao_dich(conn):
    conn.will_return(rowcount=1).will_return(rowcount=2)
    with transaction(conn):
        nhan_su.deactivate(conn, 42)
    assert (conn.commits, conn.rollbacks) == (1, 0)
    assert len(conn.executed) == 2


def test_loi_trong_giao_dich_thi_rollback(conn):
    conn.will_return(rowcount=0).will_return(columns=["IsActive"], rows=[])
    with pytest.raises(nhan_su.NhanSuNotFoundError), transaction(conn):
        nhan_su.deactivate(conn, 999)
    assert (conn.commits, conn.rollbacks) == (0, 1)
