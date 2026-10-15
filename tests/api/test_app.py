"""Kiểm thử API web (src/api/app.py) trên CSDL mẫu SQLite, có đăng nhập."""

import json

import pytest
from fastapi.testclient import TestClient

from examples.vi_du_ngung_nhan_su import tao_csdl_mau
from src.api.app import app, get_auth, get_db
from src.api.auth import Auth, bam_mat_khau

MK_QUAN_LY = "mk-quan-ly-thu"
MK_XEM = "mk-chi-xem-thu"


@pytest.fixture
def users_path(tmp_path):
    path = tmp_path / "users.json"
    path.write_text(json.dumps({
        "ql": {"ten": "Quản lý thử", "vai_tro": "quan_ly", "bam": bam_mat_khau(MK_QUAN_LY)},
        "xem": {"ten": "Người xem thử", "vai_tro": "xem", "bam": bam_mat_khau(MK_XEM)},
    }), encoding="utf-8")
    return path


@pytest.fixture
def client(users_path):
    db = tao_csdl_mau()
    a = Auth(path_fn=lambda: users_path)
    app.dependency_overrides[get_db] = lambda: db
    app.dependency_overrides[get_auth] = lambda: a
    yield TestClient(app)
    app.dependency_overrides.clear()


def login(client, ten, mk):
    return client.post("/api/dang-nhap", json={"ten_dang_nhap": ten, "mat_khau": mk})


@pytest.fixture
def ql(client):
    assert login(client, "ql", MK_QUAN_LY).status_code == 200
    return client


@pytest.fixture
def xem(client):
    assert login(client, "xem", MK_XEM).status_code == 200
    return client


# --- Đăng nhập ----------------------------------------------------------------------


def test_trang_chu_va_file_tinh_khong_can_dang_nhap(client):
    r = client.get("/")
    assert r.status_code == 200 and "Đăng nhập" in r.text
    assert client.get("/static/app.js").status_code == 200
    assert client.get("/api/info").status_code == 200


@pytest.mark.parametrize("url", ["/api/toi", "/api/nhan-su", "/api/nhan-su/1/phan-cong"])
def test_chua_dang_nhap_bi_chan(client, url):
    assert client.get(url).status_code == 401


def test_dang_nhap_dung_dat_cookie_an(client):
    r = login(client, "  QL ", MK_QUAN_LY)  # không phân biệt hoa thường, bỏ khoảng trắng
    assert r.status_code == 200
    assert r.json() == {"ten_dang_nhap": "ql", "ten": "Quản lý thử", "vai_tro": "quan_ly"}
    cookie = r.headers["set-cookie"].lower()
    assert "httponly" in cookie and "samesite=strict" in cookie
    assert client.get("/api/toi").json()["ten_dang_nhap"] == "ql"


@pytest.mark.parametrize(("ten", "mk"), [("ql", "sai-mat-khau"), ("khong-co", MK_QUAN_LY)])
def test_dang_nhap_sai_cung_mot_thong_bao(client, ten, mk):
    r = login(client, ten, mk)
    assert r.status_code == 401
    assert r.json()["detail"] == "Sai tên đăng nhập hoặc mật khẩu."


def test_sai_nhieu_lan_bi_khoa_tam(client):
    for _ in range(5):
        assert login(client, "ql", "sai").status_code == 401
    r = login(client, "ql", MK_QUAN_LY)  # đúng mật khẩu nhưng đang bị khóa
    assert r.status_code == 429 and "phút" in r.json()["detail"]


def test_dang_xuat(ql):
    assert ql.post("/api/dang-xuat").status_code == 200
    assert ql.get("/api/toi").status_code == 401


# --- Phân quyền -----------------------------------------------------------------------


def test_nguoi_xem_doc_duoc_nhung_khong_sua_duoc(xem):
    assert [r["Id"] for r in xem.get("/api/nhan-su").json()] == [1, 2, 3]
    assert xem.post("/api/nhan-su/1/phan-cong", json={"noi_dung": "Khám tàu"}).status_code == 403
    assert xem.post("/api/nhan-su/2/ngung").status_code == 403
    assert xem.post("/api/nhan-su/2/kich-hoat").status_code == 403
    assert len(xem.get("/api/nhan-su/2/phan-cong").json()) == 2  # dữ liệu không đổi


# --- Nghiệp vụ (đăng nhập quản lý) ----------------------------------------------------


def test_giao_viec_moi(ql):
    r = ql.post("/api/nhan-su/1/phan-cong", json={"noi_dung": "Khám đoàn tàu SE5"})
    assert r.status_code == 201
    assert [x["NoiDung"] for x in r.json()][-1] == "Khám đoàn tàu SE5"


@pytest.mark.parametrize(
    ("nhan_su_id", "noi_dung", "status"),
    [
        (99, "Khám tàu", 404),
        (1, "Khám đoàn tàu SE1 tại ga Đà Nẵng", 409),
        (1, "   ", 422),
    ],
)
def test_giao_viec_loi(ql, nhan_su_id, noi_dung, status):
    r = ql.post(f"/api/nhan-su/{nhan_su_id}/phan-cong", json={"noi_dung": noi_dung})
    assert r.status_code == status
    assert isinstance(r.json()["detail"], str)


def test_ngung_roi_kich_hoat_lai(ql):
    r = ql.post("/api/nhan-su/2/ngung")
    assert r.json() == {"nhan_su_changed": True, "phan_cong_count": 2}
    assert ql.get("/api/nhan-su/2/phan-cong").json() == []
    assert ql.post("/api/nhan-su/2/phan-cong", json={"noi_dung": "Khám tàu"}).status_code == 409
    assert ql.post("/api/nhan-su/2/kich-hoat").json() == {"nhan_su_changed": True}


def test_ngung_ma_khong_ton_tai(ql):
    assert ql.post("/api/nhan-su/99/ngung").status_code == 404
    assert ql.post("/api/nhan-su/99/kich-hoat").status_code == 404


def test_ghi_nhat_ky_nguoi_thao_tac(ql, caplog):
    with caplog.at_level("INFO", logger="ems.nhat_ky"):
        ql.post("/api/nhan-su/2/ngung")
    assert any("ql ngừng nhân sự 2" in r.getMessage() for r in caplog.records)
