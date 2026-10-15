# KẾ HOẠCH TÁC VỤ HIỆN TẠI (todo.md)

## Mục tiêu: Hướng dẫn triển khai web app lên máy chủ IIS nội bộ

### Các bước thực hiện (Think -> Act -> Observe)
- [x] 1. `docs/TRIEN-KHAI-IIS.md`: 9 bước (chuẩn bị máy chủ → mã nguồn → tài khoản SQL → tài khoản đăng nhập → web.config → NTFS → App Pool/Site → kiểm tra → cập nhật/quay lại), bảng xử lý sự cố, giới hạn.
- [x] 2. `deploy/iis/web.config.mau` (HttpPlatformHandler, 1 tiến trình, uvicorn chỉ nghe 127.0.0.1); `web.config` thật và `logs/` vào `.gitignore`.
- [x] 3. `deploy/sql/tao-tai-khoan.sql`: tài khoản `ems_phan_cong` chỉ SELECT/INSERT/UPDATE, DENY DELETE.
- [x] 4. `requirements-prod.txt` (thêm pyodbc 5.3.0).
- [x] 5. Sửa lỗi: nhật ký thao tác (`ems.nhat_ky`) không ra log khi chạy uvicorn - gắn handler riêng; thêm test.
- [x] 6. Nghiệm thu: `pytest -q` 121/121, `ruff` sạch, XML web.config hợp lệ.

### Việc còn treo
- [ ] Làm theo tài liệu trên máy chủ thật (người quản trị).
- [ ] (Tùy chọn) Đăng nhập SQL bằng Windows Authentication thay mật khẩu trong web.config - cần sửa code kết nối.
- [ ] Đối chiếu schema thật; thử với SQL Server thật.
