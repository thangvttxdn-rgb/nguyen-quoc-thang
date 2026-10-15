"""Web app quản lý nhân sự & phân công, giao diện tối ưu cho điện thoại.

Chạy thử với dữ liệu mẫu (SQLite trong bộ nhớ, không cần SQL Server):
    EMS_DEMO=1 uvicorn src.api.app:app --host 0.0.0.0 --port 8000
rồi mở http://<ip-máy>:8000 trên điện thoại cùng mạng nội bộ.

Chạy với SQL Server: bỏ EMS_DEMO, điền .env (tài khoản ghi DB_USER_APP / DB_PASSWORD_APP).

Đăng nhập: tài khoản trong secrets/users.json (xem src/api/auth.py). Chạy 1 worker vì phiên
lưu trong bộ nhớ. Dùng qua HTTPS thì đặt EMS_COOKIE_SECURE=1.
"""

from __future__ import annotations

import logging
import os
import threading
from collections.abc import Iterator
from pathlib import Path
from typing import Annotated, Any

from fastapi import Cookie, Depends, FastAPI, HTTPException, Response
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from src.api.auth import Auth, LoginLockedError, User
from src.db import nhan_su, phan_cong
from src.db.connection import DbConfig, get_connection, transaction

SRC = Path(__file__).resolve().parents[1]
DEMO = os.environ.get("EMS_DEMO", "").lower() in ("1", "true", "yes")
COOKIE = "ems_phien"
COOKIE_SECURE = os.environ.get("EMS_COOKIE_SECURE", "").lower() in ("1", "true", "yes")

log = logging.getLogger("ems.nhat_ky")
if not log.handlers:
    # uvicorn chỉ cấu hình logger của nó; tự gắn handler để nhật ký thao tác ra stderr
    # (IIS HttpPlatformHandler ghi stderr vào file log).
    _handler = logging.StreamHandler()
    _handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    log.addHandler(_handler)
    log.setLevel(logging.INFO)
app = FastAPI(title="Quản lý phân công toa xe", docs_url=None, redoc_url=None)
app.mount("/static", StaticFiles(directory=SRC / "static"), name="static")
auth = Auth()

_demo_conn: Any = None
_demo_lock = threading.Lock()


def get_db() -> Iterator[Any]:
    """Một kết nối cho mỗi request. Chế độ demo dùng chung một CSDL SQLite có khóa."""
    global _demo_conn
    if DEMO:
        from examples.vi_du_ngung_nhan_su import tao_csdl_mau

        with _demo_lock:
            if _demo_conn is None:
                _demo_conn = tao_csdl_mau()
            yield _demo_conn
        return
    with get_connection(DbConfig.from_env(read_only=False)) as conn:
        yield conn


def get_auth() -> Auth:
    return auth


def current_user(
    a: Annotated[Auth, Depends(get_auth)],
    ems_phien: Annotated[str | None, Cookie()] = None,
) -> User:
    user = a.nguoi_dung(ems_phien)
    if user is None:
        raise HTTPException(401, "Phiên đăng nhập đã hết hạn. Vui lòng đăng nhập lại.")
    return user


def manager(user: Annotated[User, Depends(current_user)]) -> User:
    if not user.la_quan_ly:
        raise HTTPException(403, "Tài khoản của bạn chỉ có quyền xem.")
    return user


Db = Annotated[Any, Depends(get_db)]
Viewer = Annotated[User, Depends(current_user)]
Manager = Annotated[User, Depends(manager)]


class PhanCongIn(BaseModel):
    noi_dung: str


class DangNhapIn(BaseModel):
    ten_dang_nhap: str
    mat_khau: str


def _user_out(user: User) -> dict[str, Any]:
    return {"ten_dang_nhap": user.ten_dang_nhap, "ten": user.ten, "vai_tro": user.vai_tro}


@app.get("/", include_in_schema=False)
def index() -> FileResponse:
    return FileResponse(SRC / "templates" / "index.html")


@app.get("/api/info")
def info() -> dict[str, bool]:
    return {"demo": DEMO}


@app.post("/api/dang-nhap")
def dang_nhap(
    body: DangNhapIn, response: Response, a: Annotated[Auth, Depends(get_auth)]
) -> dict[str, Any]:
    try:
        kq = a.dang_nhap(body.ten_dang_nhap, body.mat_khau)
    except LoginLockedError as e:
        raise HTTPException(429, str(e)) from e
    if kq is None:
        log.warning("Đăng nhập sai: %s", body.ten_dang_nhap.strip().lower())
        raise HTTPException(401, "Sai tên đăng nhập hoặc mật khẩu.")
    token, user = kq
    response.set_cookie(
        COOKIE, token, httponly=True, samesite="strict", secure=COOKIE_SECURE, path="/"
    )
    log.info("Đăng nhập: %s", user.ten_dang_nhap)
    return _user_out(user)


@app.post("/api/dang-xuat")
def dang_xuat(
    response: Response,
    a: Annotated[Auth, Depends(get_auth)],
    ems_phien: Annotated[str | None, Cookie()] = None,
) -> dict[str, bool]:
    a.dang_xuat(ems_phien)
    response.delete_cookie(COOKIE, path="/")
    return {"ok": True}


@app.get("/api/toi")
def toi(user: Viewer) -> dict[str, Any]:
    return _user_out(user)


@app.get("/api/nhan-su")
def list_nhan_su(user: Viewer, conn: Db) -> list[dict[str, Any]]:
    return nhan_su.list_all(conn)


@app.get("/api/nhan-su/{nhan_su_id}/phan-cong")
def list_phan_cong(nhan_su_id: int, user: Viewer, conn: Db) -> list[dict[str, Any]]:
    return phan_cong.list_active(conn, nhan_su_id)


@app.post("/api/nhan-su/{nhan_su_id}/phan-cong", status_code=201)
def add_phan_cong(
    nhan_su_id: int, body: PhanCongIn, user: Manager, conn: Db
) -> list[dict[str, Any]]:
    try:
        with transaction(conn):
            phan_cong.add(conn, nhan_su_id, body.noi_dung)
    except nhan_su.NhanSuNotFoundError as e:
        raise HTTPException(404, str(e)) from e
    except (phan_cong.NhanSuInactiveError, phan_cong.PhanCongDuplicateError) as e:
        raise HTTPException(409, str(e)) from e
    except ValueError as e:
        raise HTTPException(422, str(e)) from e
    log.info("%s giao việc cho nhân sự %s: %s", user.ten_dang_nhap, nhan_su_id, body.noi_dung)
    return phan_cong.list_active(conn, nhan_su_id)


@app.post("/api/nhan-su/{nhan_su_id}/ngung")
def deactivate(nhan_su_id: int, user: Manager, conn: Db) -> dict[str, Any]:
    try:
        with transaction(conn):
            kq = nhan_su.deactivate(conn, nhan_su_id)
    except nhan_su.NhanSuNotFoundError as e:
        raise HTTPException(404, str(e)) from e
    log.info("%s ngừng nhân sự %s: %s", user.ten_dang_nhap, nhan_su_id, kq)
    return kq._asdict()


@app.post("/api/nhan-su/{nhan_su_id}/kich-hoat")
def reactivate(nhan_su_id: int, user: Manager, conn: Db) -> dict[str, Any]:
    try:
        with transaction(conn):
            changed = nhan_su.reactivate(conn, nhan_su_id)
    except nhan_su.NhanSuNotFoundError as e:
        raise HTTPException(404, str(e)) from e
    log.info("%s kích hoạt lại nhân sự %s", user.ten_dang_nhap, nhan_su_id)
    return {"nhan_su_changed": changed}
