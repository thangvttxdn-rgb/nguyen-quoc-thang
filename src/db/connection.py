"""Kết nối SQL Server qua pyodbc theo quy tắc AGENTS.md mục 3a.

- Cấu hình chỉ đọc từ biến môi trường (mẫu tại `.env.example`), không hardcode.
- Mọi truy vấn phải tham số hóa bằng `?`; `fetch_all` chỉ nhận câu SELECT.
- Ghi dữ liệu qua `execute_write` trong khối `transaction`: chỉ INSERT/UPDATE có WHERE,
  cấm DELETE (xóa mềm bằng `IsActive = 0`, xem `src/db/nhan_su.py`).
- Tác tử AI dùng tài khoản chỉ đọc; ứng dụng dùng tài khoản ghi
  (`DbConfig.from_env(read_only=False)`).
- Giữ nguyên `decimal.Decimal` từ cột DECIMAL, không ép sang float.

Ví dụ:
    cfg = DbConfig.from_env()
    with get_connection(cfg) as conn:
        rows = fetch_all(conn, "SELECT Id, HoTen FROM NhanSu WHERE IsActive = ?", (1,))
"""

from __future__ import annotations

import os
import re
from collections.abc import Callable, Iterator, Mapping, Sequence
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Any

# (biến tài khoản, biến mật khẩu) theo vai trò kết nối.
ACCOUNT_ENV = {
    True: ("DB_USER_READONLY", "DB_PASSWORD_READONLY"),
    False: ("DB_USER_APP", "DB_PASSWORD_APP"),
}
DEFAULT_DRIVER = "ODBC Driver 18 for SQL Server"

# Câu đọc: bắt đầu bằng SELECT hoặc WITH (CTE), chỉ một câu lệnh.
_READ_ONLY_SQL = re.compile(r"^\s*(SELECT|WITH)\b", re.IGNORECASE)
_WRITE_KEYWORDS = re.compile(
    r"\b(INSERT|UPDATE|DELETE|MERGE|ALTER|DROP|TRUNCATE|CREATE|EXEC(UTE)?|GRANT|REVOKE|INTO)\b",
    re.IGNORECASE,
)
# Câu ghi: chỉ INSERT hoặc UPDATE; UPDATE bắt buộc có WHERE.
_WRITE_SQL = re.compile(r"^\s*(INSERT|UPDATE)\b", re.IGNORECASE)
_FORBIDDEN_IN_WRITE = re.compile(
    r"\b(DELETE|MERGE|ALTER|DROP|TRUNCATE|CREATE|EXEC(UTE)?|GRANT|REVOKE)\b",
    re.IGNORECASE,
)


class DbConfigError(RuntimeError):
    """Thiếu hoặc sai cấu hình kết nối."""


class UnsafeQueryError(ValueError):
    """Câu truy vấn vi phạm quy tắc an toàn."""


@dataclass(frozen=True)
class DbConfig:
    server: str
    database: str
    user: str
    password: str = field(repr=False)
    driver: str = DEFAULT_DRIVER
    trust_server_certificate: bool = False
    timeout: int = 30
    read_only: bool = True

    @classmethod
    def from_env(
        cls, environ: Mapping[str, str] | None = None, read_only: bool = True
    ) -> DbConfig:
        env = os.environ if environ is None else environ
        user_key, password_key = ACCOUNT_ENV[read_only]
        required = ("DB_SERVER", "DB_NAME", user_key, password_key)
        missing = [k for k in required if not env.get(k)]
        if missing:
            raise DbConfigError(f"Thiếu biến môi trường: {', '.join(missing)} (xem .env.example)")
        placeholders = [k for k in required if env[k].strip().startswith("<")]
        if placeholders:
            raise DbConfigError(f"Biến môi trường còn giá trị mẫu: {', '.join(placeholders)}")
        try:
            timeout = int(env.get("DB_TIMEOUT", "30"))
        except ValueError as exc:
            raise DbConfigError("DB_TIMEOUT phải là số nguyên (giây)") from exc
        return cls(
            server=env["DB_SERVER"],
            database=env["DB_NAME"],
            user=env[user_key],
            password=env[password_key],
            driver=env.get("DB_DRIVER") or DEFAULT_DRIVER,
            trust_server_certificate=env.get("DB_TRUST_CERT", "no").lower() in ("1", "yes", "true"),
            timeout=timeout,
            read_only=read_only,
        )


def _odbc_value(value: str) -> str:
    """Bọc giá trị trong {} khi có ký tự đặc biệt (quy tắc chuỗi kết nối ODBC)."""
    if any(c in value for c in ";{}=") or value != value.strip():
        return "{" + value.replace("}", "}}") + "}"
    return value


def build_connection_string(cfg: DbConfig) -> str:
    parts = {
        "DRIVER": "{" + cfg.driver + "}",
        "SERVER": _odbc_value(cfg.server),
        "DATABASE": _odbc_value(cfg.database),
        "UID": _odbc_value(cfg.user),
        "PWD": _odbc_value(cfg.password),
        "Encrypt": "yes",
        "TrustServerCertificate": "yes" if cfg.trust_server_certificate else "no",
        "ApplicationIntent": "ReadOnly" if cfg.read_only else "ReadWrite",
    }
    return ";".join(f"{k}={v}" for k, v in parts.items()) + ";"


def _default_connect(conn_str: str, timeout: int) -> Any:
    import pyodbc  # Import trễ: test và lint không cần cài driver ODBC.

    return pyodbc.connect(conn_str, timeout=timeout, autocommit=False)


@contextmanager
def get_connection(
    cfg: DbConfig | None = None,
    connect: Callable[[str, int], Any] = _default_connect,
) -> Iterator[Any]:
    """Mở kết nối và luôn đóng khi ra khỏi khối `with`."""
    cfg = cfg or DbConfig.from_env()
    conn = connect(build_connection_string(cfg), cfg.timeout)
    try:
        yield conn
    finally:
        conn.close()


def _single_statement(sql: str) -> str:
    body = sql.strip().rstrip(";")
    if ";" in body:
        raise UnsafeQueryError("Chỉ được một câu lệnh mỗi lần gọi.")
    return body


def _check_params(params: Sequence[Any]) -> None:
    if isinstance(params, (str, bytes)):
        raise UnsafeQueryError("params phải là tuple/list, không phải chuỗi.")


def ensure_read_only(sql: str) -> None:
    """Chỉ cho phép một câu SELECT/WITH; chặn câu ghi và nhiều câu nối bằng `;`."""
    body = _single_statement(sql)
    if not _READ_ONLY_SQL.match(body) or _WRITE_KEYWORDS.search(body):
        raise UnsafeQueryError("fetch_all chỉ nhận câu SELECT (không ghi, không SELECT INTO).")


def fetch_all(conn: Any, sql: str, params: Sequence[Any] = ()) -> list[dict[str, Any]]:
    """Chạy câu SELECT tham số hóa, trả về list dict theo tên cột.

    Truyền giá trị qua `params` với dấu `?`, không ghép chuỗi vào `sql`.
    """
    _check_params(params)
    ensure_read_only(sql)
    cursor = conn.cursor()
    try:
        cursor.execute(sql, *params)
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row, strict=True)) for row in cursor.fetchall()]
    finally:
        cursor.close()


def ensure_safe_write(sql: str) -> None:
    """Chỉ cho phép một câu INSERT hoặc UPDATE có WHERE; cấm DELETE và lệnh đổi cấu trúc."""
    body = _single_statement(sql)
    match = _WRITE_SQL.match(body)
    if not match or _FORBIDDEN_IN_WRITE.search(body):
        raise UnsafeQueryError(
            "execute_write chỉ nhận INSERT/UPDATE. Không xóa cứng: dùng IsActive = 0."
        )
    if match.group(1).upper() == "UPDATE" and not re.search(r"\bWHERE\b", body, re.IGNORECASE):
        raise UnsafeQueryError("UPDATE phải có WHERE (tránh cập nhật cả bảng).")


@contextmanager
def transaction(conn: Any) -> Iterator[Any]:
    """Commit khi khối `with` chạy xong, rollback và ném lại lỗi nếu có ngoại lệ."""
    try:
        yield conn
    except BaseException:
        conn.rollback()
        raise
    conn.commit()


def execute_write(conn: Any, sql: str, params: Sequence[Any] = ()) -> int:
    """Chạy một câu ghi tham số hóa, trả về số dòng bị ảnh hưởng. Không tự commit."""
    _check_params(params)
    ensure_safe_write(sql)
    cursor = conn.cursor()
    try:
        cursor.execute(sql, *params)
        return cursor.rowcount
    finally:
        cursor.close()
