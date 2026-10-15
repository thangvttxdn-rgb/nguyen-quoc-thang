# KẾ HOẠCH TÁC VỤ HIỆN TẠI (todo.md)

## Mục tiêu: Giao diện điện thoại quản lý nhân sự & phân công

### Các bước thực hiện (Think -> Act -> Observe)
- [x] 1. API `src/api/app.py` (FastAPI): danh sách nhân sự, phân công đang hiệu lực, giao việc, ngừng, kích hoạt lại. Lỗi nghiệp vụ → 404/409/422 kèm thông báo tiếng Việt. Chế độ `EMS_DEMO=1` dùng SQLite mẫu.
- [x] 2. Giao diện `src/templates/index.html`, `src/static/app.css`, `app.js` (JS thuần): tìm kiếm không dấu, lọc trạng thái, bảng trượt chi tiết, giao việc, xác nhận ngừng ngay trong trang, sáng/tối theo máy.
- [x] 3. `nhan_su.list_all`; `requirements.txt` (fastapi, uvicorn); `requirements-dev.txt` thêm httpx.
- [x] 4. Test API `tests/api/test_app.py` (9 test). Nghiệm thu: `pytest -q` 103/103 xanh trên Python 3.11 & 3.13, `ruff` sạch.
- [x] 5. Chạy thử trên trình duyệt giả lập iPhone 13: giao việc → ngừng → thông báo đúng, không lỗi JS, không tràn ngang.
- [x] 6. Bản xem trước không cần server: `docs/giao-dien-mobile.html`.

### Việc còn treo
- [ ] **Đăng nhập / phân quyền** trước khi dùng thật (hiện ai vào được mạng nội bộ cũng thao tác được).
- [ ] Đối chiếu schema thật (`NhanSu.Id`, `HoTen`, `DonVi`, `ChucDanh`; `PhanCong.NhanSuId`, `NoiDung`, `IsActive`).
- [ ] Thử với SQL Server thật và chọn cách triển khai (IIS + reverse proxy hoặc dịch vụ Windows).
