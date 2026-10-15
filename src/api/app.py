"""Web app quản lý nhân sự & phân công, giao diện tối ưu cho điện thoại.

Chạy thử với dữ liệu mẫu (SQLite trong bộ nhớ, không cần SQL Server):
    EMS_DEMO=1 uvicorn src.api.app:app --host 0.0.0.0 --port 8000
rồi mở http://<ip-máy>:8000 trên điện thoại cùng mạng nội bộ.

Chạy với SQL Server: bỏ EMS_DEMO, điền .env (tài khoản ghi DB_USER_APP / DB_PASSWORD_APP).

CHƯA CÓ ĐĂNG NHẬP: chỉ dùng trong mạng nội bộ để thử; phải thêm xác thực trước khi dùng thật.
"""

from __future__ import annotations

import os
import threading
from collections.abc import Iterator
from pathlib import Path
from typing import Annotated, Any

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from src.db import nhan_su, phan_cong
from src.db.connection import DbConfig, get_connection, transaction

SRC = Path(__file__).resolve().parents[1]
DEMO = os.environ.get("EMS_DEMO", "").lower() in ("1", "true", "yes")

app = FastAPI(title="Quản lý phân công toa xe", docs_url=None, redoc_url=None)
app.mount("/static", StaticFiles(directory=SRC / "static"), name="static")

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


Db = Annotated[Any, Depends(get_db)]


class PhanCongIn(BaseModel):
    noi_dung: str


@app.get("/", include_in_schema=False)
def index() -> FileResponse:
    return FileResponse(SRC / "templates" / "index.html")


@app.get("/api/info")
def info() -> dict[str, bool]:
    return {"demo": DEMO}


@app.get("/api/nhan-su")
def list_nhan_su(conn: Db) -> list[dict[str, Any]]:
    return nhan_su.list_all(conn)


@app.get("/api/nhan-su/{nhan_su_id}/phan-cong")
def list_phan_cong(nhan_su_id: int, conn: Db) -> list[dict[str, Any]]:
    return phan_cong.list_active(conn, nhan_su_id)


@app.post("/api/nhan-su/{nhan_su_id}/phan-cong", status_code=201)
def add_phan_cong(
    nhan_su_id: int, body: PhanCongIn, conn: Db
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
    return phan_cong.list_active(conn, nhan_su_id)


@app.post("/api/nhan-su/{nhan_su_id}/ngung")
def deactivate(nhan_su_id: int, conn: Db) -> dict[str, Any]:
    try:
        with transaction(conn):
            kq = nhan_su.deactivate(conn, nhan_su_id)
    except nhan_su.NhanSuNotFoundError as e:
        raise HTTPException(404, str(e)) from e
    return kq._asdict()


@app.post("/api/nhan-su/{nhan_su_id}/kich-hoat")
def reactivate(nhan_su_id: int, conn: Db) -> dict[str, Any]:
    try:
        with transaction(conn):
            changed = nhan_su.reactivate(conn, nhan_su_id)
    except nhan_su.NhanSuNotFoundError as e:
        raise HTTPException(404, str(e)) from e
    return {"nhan_su_changed": changed}
