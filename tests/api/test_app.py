"""Kiểm thử API web (src/api/app.py) trên CSDL mẫu SQLite."""

import pytest
from fastapi.testclient import TestClient

from examples.vi_du_ngung_nhan_su import tao_csdl_mau
from src.api.app import app, get_db


@pytest.fixture
def client():
    db = tao_csdl_mau()
    app.dependency_overrides[get_db] = lambda: db
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_trang_chu_va_file_tinh(client):
    r = client.get("/")
    assert r.status_code == 200 and "Phân công nhân sự" in r.text
    assert client.get("/static/app.js").status_code == 200
    assert client.get("/static/app.css").status_code == 200


def test_danh_sach_nhan_su(client):
    rows = client.get("/api/nhan-su").json()
    assert [r["Id"] for r in rows] == [1, 2, 3]
    assert rows[1]["HoTen"] == "Trần Thị Bình"


def test_giao_viec_moi(client):
    r = client.post("/api/nhan-su/1/phan-cong", json={"noi_dung": "Khám đoàn tàu SE5"})
    assert r.status_code == 201
    assert [x["NoiDung"] for x in r.json()][-1] == "Khám đoàn tàu SE5"


@pytest.mark.parametrize(
    ("nhan_su_id", "noi_dung", "status"),
    [
        (99, "Khám tàu", 404),  # không tồn tại
        (1, "Khám đoàn tàu SE1 tại ga Đà Nẵng", 409),  # trùng phân công đang hiệu lực
        (1, "   ", 422),  # rỗng
    ],
)
def test_giao_viec_loi(client, nhan_su_id, noi_dung, status):
    r = client.post(f"/api/nhan-su/{nhan_su_id}/phan-cong", json={"noi_dung": noi_dung})
    assert r.status_code == status
    assert isinstance(r.json()["detail"], str)


def test_ngung_roi_kich_hoat_lai(client):
    r = client.post("/api/nhan-su/2/ngung")
    assert r.json() == {"nhan_su_changed": True, "phan_cong_count": 2}
    assert client.get("/api/nhan-su/2/phan-cong").json() == []
    # Đã ngừng thì không giao việc được.
    r = client.post("/api/nhan-su/2/phan-cong", json={"noi_dung": "Khám tàu"})
    assert r.status_code == 409
    assert client.post("/api/nhan-su/2/kich-hoat").json() == {"nhan_su_changed": True}


def test_ngung_ma_khong_ton_tai(client):
    assert client.post("/api/nhan-su/99/ngung").status_code == 404
    assert client.post("/api/nhan-su/99/kich-hoat").status_code == 404
