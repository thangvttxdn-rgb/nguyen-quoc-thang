"""Kiểm thử src/db/connection.py - không cần SQL Server hay pyodbc thật."""

from decimal import Decimal

import pytest

from src.db.connection import (
    DbConfig,
    DbConfigError,
    UnsafeQueryError,
    build_connection_string,
    ensure_read_only,
    fetch_all,
    get_connection,
)

FAKE_SECRET = "mat-khau-gia"
SPECIAL_SECRET = "a;b}c"
ENV = {
    "DB_SERVER": "srv-toaxe",
    "DB_NAME": "EMS",
    "DB_USER_READONLY": "agent_ro",
    "DB_PASSWORD_READONLY": FAKE_SECRET,
}


def parse(conn_str):
    """Tách chuỗi kết nối đơn giản (không có giá trị bọc {} chứa ;)."""
    return dict(p.split("=", 1) for p in conn_str.rstrip(";").split(";"))


class FakeCursor:
    def __init__(self, rows, columns):
        self.rows, self.description = rows, [(c,) for c in columns]
        self.executed, self.closed = None, False

    def execute(self, sql, *params):
        self.executed = (sql, params)

    def fetchall(self):
        return self.rows

    def close(self):
        self.closed = True


class FakeConn:
    def __init__(self, cursor=None):
        self._cursor, self.closed = cursor, False

    def cursor(self):
        return self._cursor

    def close(self):
        self.closed = True


# --- DbConfig.from_env ---------------------------------------------------------

def test_doc_cau_hinh_tu_env():
    cfg = DbConfig.from_env(ENV)
    assert (cfg.server, cfg.database, cfg.user) == ("srv-toaxe", "EMS", "agent_ro")
    assert cfg.timeout == 30 and cfg.trust_server_certificate is False


def test_thieu_bien_bao_ro_ten():
    env = {k: v for k, v in ENV.items() if k != "DB_NAME"}
    with pytest.raises(DbConfigError, match="DB_NAME"):
        DbConfig.from_env(env)


def test_con_gia_tri_mau_thi_bao_loi():
    with pytest.raises(DbConfigError, match="DB_SERVER"):
        DbConfig.from_env({**ENV, "DB_SERVER": "<điền tên máy chủ>"})


def test_timeout_sai_kieu():
    with pytest.raises(DbConfigError, match="DB_TIMEOUT"):
        DbConfig.from_env({**ENV, "DB_TIMEOUT": "ba muoi"})


def test_repr_khong_lo_mat_khau():
    assert FAKE_SECRET not in repr(DbConfig.from_env(ENV))


# --- build_connection_string ---------------------------------------------------

def test_chuoi_ket_noi_bat_ma_hoa_va_chi_doc():
    parts = parse(build_connection_string(DbConfig.from_env(ENV)))
    assert parts["DRIVER"] == "{ODBC Driver 18 for SQL Server}"
    assert parts["UID"] == "agent_ro" and parts["PWD"] == FAKE_SECRET
    assert parts["Encrypt"] == "yes" and parts["TrustServerCertificate"] == "no"
    assert parts["ApplicationIntent"] == "ReadOnly"


def test_gia_tri_co_ky_tu_dac_biet_duoc_boc_ngoac():
    cfg = DbConfig.from_env({**ENV, "DB_PASSWORD_READONLY": SPECIAL_SECRET})
    assert "{a;b}}c}" in build_connection_string(cfg)


# --- get_connection ------------------------------------------------------------

def test_ket_noi_luon_duoc_dong_ke_ca_khi_loi():
    conn, seen = FakeConn(), {}

    def fake_connect(conn_str, timeout):
        seen["timeout"] = timeout
        return conn

    with pytest.raises(RuntimeError), get_connection(DbConfig.from_env(ENV), fake_connect):
        raise RuntimeError("lỗi giữa chừng")
    assert conn.closed and seen["timeout"] == 30


# --- ensure_read_only / fetch_all ----------------------------------------------

@pytest.mark.parametrize("sql", [
    "SELECT Id FROM NhanSu WHERE IsActive = ?",
    "  select * from PhanCong with (nolock);",
    "WITH t AS (SELECT Id FROM NhanSu) SELECT * FROM t",
    "SELECT UpdatedAt, DeletedBy FROM NhanSu",
])
def test_cau_doc_hop_le(sql):
    ensure_read_only(sql)


@pytest.mark.parametrize("sql", [
    "UPDATE NhanSu SET IsActive = 0",
    "DELETE FROM NhanSu WHERE Id = ?",
    "SELECT * INTO NhanSu_bak FROM NhanSu",
    "SELECT 1; DROP TABLE NhanSu",
    "EXEC sp_XoaNhanSu ?",
    "WITH t AS (SELECT 1 AS x) DELETE FROM NhanSu",
])
def test_cau_ghi_bi_tu_choi(sql):
    with pytest.raises(UnsafeQueryError):
        ensure_read_only(sql)


def test_fetch_all_tra_ve_dict_va_giu_decimal():
    cursor = FakeCursor([(1, "Nguyễn Văn A", Decimal("12.50"))], ["Id", "HoTen", "HeSo"])
    rows = fetch_all(FakeConn(cursor), "SELECT Id, HoTen, HeSo FROM NhanSu WHERE Id = ?", (1,))
    assert rows == [{"Id": 1, "HoTen": "Nguyễn Văn A", "HeSo": Decimal("12.50")}]
    assert isinstance(rows[0]["HeSo"], Decimal)
    assert cursor.executed == ("SELECT Id, HoTen, HeSo FROM NhanSu WHERE Id = ?", (1,))
    assert cursor.closed


def test_fetch_all_tu_choi_params_la_chuoi():
    with pytest.raises(UnsafeQueryError, match="params"):
        fetch_all(FakeConn(FakeCursor([], [])), "SELECT 1 WHERE ? = 1", "1")


def test_fetch_all_khong_chay_cau_ghi():
    cursor = FakeCursor([], [])
    with pytest.raises(UnsafeQueryError):
        fetch_all(FakeConn(cursor), "DELETE FROM NhanSu")
    assert cursor.executed is None
