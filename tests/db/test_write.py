"""Kiểm thử phần ghi của src/db/connection.py."""

import pytest

from src.db.connection import (
    DbConfig,
    DbConfigError,
    UnsafeQueryError,
    build_connection_string,
    ensure_safe_write,
    execute_write,
    transaction,
)

FAKE_SECRET = "mat-khau-ghi-gia"
APP_ENV = {
    "DB_SERVER": "srv-toaxe",
    "DB_NAME": "EMS",
    "DB_USER_APP": "ems_app",
    "DB_PASSWORD_APP": FAKE_SECRET,
}


# --- Cấu hình tài khoản ghi ------------------------------------------------------

def test_tai_khoan_ghi_doc_bien_rieng_va_cho_phep_ghi():
    cfg = DbConfig.from_env(APP_ENV, read_only=False)
    assert cfg.user == "ems_app" and cfg.read_only is False
    assert "ApplicationIntent=ReadWrite" in build_connection_string(cfg)


def test_mac_dinh_van_la_tai_khoan_chi_doc():
    with pytest.raises(DbConfigError, match="DB_USER_READONLY"):
        DbConfig.from_env(APP_ENV)


# --- ensure_safe_write -----------------------------------------------------------

@pytest.mark.parametrize("sql", [
    "INSERT INTO NhanSu (HoTen, IsActive) VALUES (?, 1)",
    "UPDATE NhanSu SET IsActive = 0 WHERE Id = ?",
    "  update NhanSu set HoTen = ? where Id = ?;",
])
def test_cau_ghi_hop_le(sql):
    ensure_safe_write(sql)


@pytest.mark.parametrize("sql", [
    "DELETE FROM NhanSu WHERE Id = ?",
    "UPDATE NhanSu SET IsActive = 0",
    "UPDATE NhanSu SET IsActive = 0 WHERE Id = ?; DELETE FROM PhanCong",
    "SELECT * FROM NhanSu",
    "TRUNCATE TABLE NhanSu",
    "ALTER TABLE NhanSu ADD GhiChu NVARCHAR(200)",
    "EXEC sp_XoaNhanSu ?",
    "MERGE NhanSu AS t USING src ON t.Id = src.Id WHEN MATCHED THEN DELETE",
])
def test_cau_ghi_nguy_hiem_bi_tu_choi(sql):
    with pytest.raises(UnsafeQueryError):
        ensure_safe_write(sql)


# --- execute_write / transaction -------------------------------------------------

def test_execute_write_tra_ve_so_dong_va_khong_tu_commit(conn):
    conn.will_return(rowcount=1)
    assert execute_write(conn, "UPDATE NhanSu SET IsActive = 0 WHERE Id = ?", (7,)) == 1
    assert conn.executed == [("UPDATE NhanSu SET IsActive = 0 WHERE Id = ?", (7,))]
    assert conn.commits == 0


def test_execute_write_khong_chay_cau_bi_cam(conn):
    with pytest.raises(UnsafeQueryError):
        execute_write(conn, "DELETE FROM NhanSu WHERE Id = ?", (7,))
    assert conn.executed == []


def test_execute_write_tu_choi_params_la_chuoi(conn):
    with pytest.raises(UnsafeQueryError, match="params"):
        execute_write(conn, "UPDATE NhanSu SET HoTen = ? WHERE Id = 1", "A")


def test_transaction_commit_khi_thanh_cong(conn):
    with transaction(conn):
        pass
    assert (conn.commits, conn.rollbacks) == (1, 0)


def test_transaction_rollback_khi_loi(conn):
    with pytest.raises(ValueError), transaction(conn):
        raise ValueError("lỗi nghiệp vụ")
    assert (conn.commits, conn.rollbacks) == (0, 1)
