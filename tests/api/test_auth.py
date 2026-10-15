"""Kiểm thử src/api/auth.py: băm mật khẩu, phiên, khóa tạm."""

import json

import pytest

from src.api import auth as A

MK = "mat-khau-thu-nghiem"


class Clock:
    def __init__(self):
        self.t = 1000.0

    def __call__(self):
        return self.t


@pytest.fixture
def store(tmp_path):
    path = tmp_path / "users.json"
    path.write_text(json.dumps({
        "ql": {"ten": "Quản lý", "vai_tro": "quan_ly", "bam": A.bam_mat_khau(MK)},
        "la": {"ten": "Vai trò lạ", "vai_tro": "admin", "bam": A.bam_mat_khau(MK)},
    }), encoding="utf-8")
    clock = Clock()
    return A.Auth(path_fn=lambda: path, clock=clock), clock


def test_bam_khong_chua_mat_khau_goc_va_moi_lan_mot_khac():
    h1, h2 = A.bam_mat_khau(MK), A.bam_mat_khau(MK)
    assert MK not in h1 and h1 != h2
    assert A.kiem_tra_mat_khau(MK, h1) and A.kiem_tra_mat_khau(MK, h2)
    assert not A.kiem_tra_mat_khau("sai", h1)


@pytest.mark.parametrize("chuoi", ["", "khong-dung-dinh-dang", "md5$ab$cd", "scrypt$zz$00"])
def test_chuoi_bam_hong_thi_tu_choi(chuoi):
    assert A.kiem_tra_mat_khau(MK, chuoi) is False


def test_phien_het_han_sau_12_gio(store):
    a, clock = store
    token, user = a.dang_nhap("ql", MK)
    assert a.nguoi_dung(token) == user
    clock.t += A.SESSION_TTL
    assert a.nguoi_dung(token) is None


def test_vai_tro_khong_hop_le_bi_bo_qua(store):
    a, _ = store
    assert a.dang_nhap("la", MK) is None


def test_khoa_tam_roi_mo_lai(store):
    a, clock = store
    for _ in range(A.MAX_FAILS):
        assert a.dang_nhap("ql", "sai") is None
    with pytest.raises(A.LoginLockedError):
        a.dang_nhap("ql", MK)
    clock.t += A.LOCK_SECONDS
    assert a.dang_nhap("ql", MK) is not None


def test_khong_co_file_tai_khoan_thi_khong_ai_dang_nhap_duoc(tmp_path):
    a = A.Auth(path_fn=lambda: tmp_path / "khong-co.json")
    assert a.dang_nhap("ql", MK) is None
