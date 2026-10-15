"""Chạy ví dụ trên SQLite thật để kiểm tra câu SQL của src/db/nhan_su.py chạy được."""

import pytest

from examples.vi_du_ngung_nhan_su import main, tao_csdl_mau
from src.db import nhan_su
from src.db.connection import UnsafeQueryError, execute_write, fetch_all, transaction


def trang_thai(conn):
    ns = {r["Id"]: r["IsActive"] for r in fetch_all(conn, "SELECT Id, IsActive FROM NhanSu")}
    pc = {r["Id"]: r["IsActive"] for r in fetch_all(conn, "SELECT Id, IsActive FROM PhanCong")}
    return ns, pc


def test_ngung_nhan_su_ngung_dung_phan_cong_cua_ho():
    conn = tao_csdl_mau()
    with transaction(conn):
        kq = nhan_su.deactivate(conn, 2)
    assert kq == (True, 2)  # PhanCong 13 đã ngừng từ trước nên không tính
    ns, pc = trang_thai(conn)
    assert ns == {1: 1, 2: 0, 3: 1}
    assert pc == {10: 1, 11: 0, 12: 0, 13: 0, 14: 1}


def test_ma_khong_ton_tai_khong_doi_du_lieu():
    conn = tao_csdl_mau()
    truoc = trang_thai(conn)
    with pytest.raises(nhan_su.NhanSuNotFoundError), transaction(conn):
        nhan_su.deactivate(conn, 99)
    assert trang_thai(conn) == truoc


def test_kich_hoat_lai_khong_khoi_phuc_phan_cong():
    conn = tao_csdl_mau()
    with transaction(conn):
        nhan_su.deactivate(conn, 2)
    with transaction(conn):
        assert nhan_su.reactivate(conn, 2) is True
    ns, pc = trang_thai(conn)
    assert ns[2] == 1 and pc[11] == 0 and pc[12] == 0


def test_delete_bi_chan_va_du_lieu_con_nguyen():
    conn = tao_csdl_mau()
    with pytest.raises(UnsafeQueryError):
        execute_write(conn, "DELETE FROM NhanSu WHERE Id = ?", (2,))
    assert len(fetch_all(conn, "SELECT Id FROM NhanSu")) == 3


def test_script_chay_tron_ven(capsys):
    main()
    out = capsys.readouterr().out
    assert "DeactivateResult(nhan_su_changed=True, phan_cong_count=2)" in out
    assert "đã rollback" in out and "bị chặn" in out
