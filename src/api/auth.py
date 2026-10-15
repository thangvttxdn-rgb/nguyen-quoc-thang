"""Đăng nhập cho web app: tài khoản trong file JSON, mật khẩu băm scrypt, phiên lưu trong bộ nhớ.

File tài khoản (mặc định `secrets/users.json`, đổi bằng biến EMS_USERS_FILE; thư mục secrets/
đã nằm trong .gitignore):

    {
      "thangnq": {"ten": "Nguyễn Quốc Thắng", "vai_tro": "quan_ly", "bam": "scrypt$..."},
      "kcxv01":  {"ten": "Trạm KCTX Diêu Trì", "vai_tro": "xem",     "bam": "scrypt$..."}
    }

Vai trò: `quan_ly` được giao việc, ngừng và kích hoạt lại nhân sự; `xem` chỉ được xem.

Tạo chuỗi băm cho mật khẩu mới (nhập ẩn, không lưu mật khẩu gốc):
    python -m src.api.auth

Giới hạn: phiên nằm trong bộ nhớ một tiến trình -> chạy uvicorn 1 worker; khởi động lại
máy chủ thì mọi người phải đăng nhập lại.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import os
import secrets
import threading
import time
from dataclasses import dataclass
from pathlib import Path

VAI_TRO = ("quan_ly", "xem")
SESSION_TTL = 12 * 3600  # một ca làm việc dài nhất
MAX_FAILS = 5  # sai liên tiếp bao nhiêu lần thì khóa tạm
LOCK_SECONDS = 300
_SCRYPT = {"n": 2**14, "r": 8, "p": 1, "dklen": 32}


@dataclass(frozen=True)
class User:
    ten_dang_nhap: str
    ten: str
    vai_tro: str

    @property
    def la_quan_ly(self) -> bool:
        return self.vai_tro == "quan_ly"


def bam_mat_khau(mat_khau: str) -> str:
    salt = secrets.token_bytes(16)
    digest = hashlib.scrypt(mat_khau.encode(), salt=salt, **_SCRYPT)
    return f"scrypt${salt.hex()}${digest.hex()}"


def kiem_tra_mat_khau(mat_khau: str, chuoi_bam: str) -> bool:
    try:
        thuat_toan, salt_hex, digest_hex = chuoi_bam.split("$")
        if thuat_toan != "scrypt":
            return False
        digest = hashlib.scrypt(mat_khau.encode(), salt=bytes.fromhex(salt_hex), **_SCRYPT)
    except ValueError:
        return False
    return hmac.compare_digest(digest.hex(), digest_hex)


# Băm giả để người dùng không tồn tại cũng tốn thời gian như người tồn tại (khó dò tên đăng nhập).
_BAM_GIA = bam_mat_khau(secrets.token_hex(8))


def users_file() -> Path:
    return Path(os.environ.get("EMS_USERS_FILE", "secrets/users.json"))


def doc_tai_khoan(path: Path) -> dict[str, dict]:
    if not path.is_file():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return {k: v for k, v in data.items() if v.get("vai_tro") in VAI_TRO and v.get("bam")}


class LoginLockedError(RuntimeError):
    """Sai mật khẩu quá nhiều lần, tạm khóa."""


class Auth:
    """Xác thực và quản lý phiên. Một đối tượng dùng chung cho cả ứng dụng."""

    def __init__(self, path_fn=users_file, clock=time.monotonic) -> None:
        self._path_fn = path_fn
        self._clock = clock
        self._sessions: dict[str, tuple[User, float]] = {}
        self._fails: dict[str, tuple[int, float]] = {}
        self._lock = threading.Lock()

    def dang_nhap(self, ten_dang_nhap: str, mat_khau: str) -> tuple[str, User] | None:
        """Trả về (token phiên, người dùng) nếu đúng; None nếu sai."""
        key = ten_dang_nhap.strip().lower()
        now = self._clock()
        with self._lock:
            so_lan, khoa_den = self._fails.get(key, (0, 0.0))
            if so_lan >= MAX_FAILS and now < khoa_den:
                raise LoginLockedError(
                    f"Sai quá {MAX_FAILS} lần. Thử lại sau {int(khoa_den - now) // 60 + 1} phút."
                )
        info = doc_tai_khoan(self._path_fn()).get(key)
        dung = kiem_tra_mat_khau(mat_khau, info["bam"] if info else _BAM_GIA) and info is not None
        with self._lock:
            if not dung:
                so_lan = self._fails.get(key, (0, 0.0))[0] + 1
                self._fails[key] = (so_lan, now + LOCK_SECONDS)
                return None
            self._fails.pop(key, None)
            user = User(key, info.get("ten") or key, info["vai_tro"])
            token = secrets.token_urlsafe(32)
            self._sessions[token] = (user, now + SESSION_TTL)
            return token, user

    def nguoi_dung(self, token: str | None) -> User | None:
        if not token:
            return None
        with self._lock:
            item = self._sessions.get(token)
            if not item:
                return None
            user, het_han = item
            if self._clock() >= het_han:
                del self._sessions[token]
                return None
            return user

    def dang_xuat(self, token: str | None) -> None:
        with self._lock:
            self._sessions.pop(token or "", None)


def _tao_chuoi_bam() -> None:
    import getpass

    mk = getpass.getpass("Mật khẩu mới: ")
    if len(mk) < 8:
        raise SystemExit("Mật khẩu phải có ít nhất 8 ký tự.")
    if getpass.getpass("Nhập lại: ") != mk:
        raise SystemExit("Hai lần nhập không khớp.")
    print(bam_mat_khau(mk))


if __name__ == "__main__":
    _tao_chuoi_bam()
