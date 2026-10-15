# KẾ HOẠCH TÁC VỤ HIỆN TẠI (todo.md)

## Mục tiêu: Thêm đăng nhập cho giao diện điện thoại

### Các bước thực hiện (Think -> Act -> Observe)
- [x] 1. `src/api/auth.py`: tài khoản trong `secrets/users.json` (gitignore), mật khẩu băm scrypt (thư viện chuẩn), phiên 12 giờ lưu trong bộ nhớ, khóa tạm 5 phút sau 5 lần sai, thông báo sai giống nhau cho tên sai/mật khẩu sai, lệnh `python -m src.api.auth` tạo chuỗi băm.
- [x] 2. `src/api/app.py`: `/api/dang-nhap`, `/api/dang-xuat`, `/api/toi`; mọi API dữ liệu cần đăng nhập (401); giao việc/ngừng/kích hoạt cần vai trò `quan_ly` (403); cookie HttpOnly + SameSite=Strict (+ Secure khi `EMS_COOKIE_SECURE=1`); ghi nhật ký ai làm gì.
- [x] 3. Giao diện: màn hình đăng nhập, tên + vai trò + nút đăng xuất ở đầu trang, tài khoản "xem" không thấy nút sửa, hết phiên tự về màn đăng nhập.
- [x] 4. Test: `tests/api/test_auth.py` (9), `tests/api/test_app.py` viết lại có đăng nhập (17). `pytest -q` 120/120, `ruff` sạch.
- [x] 5. Chạy thử trên giả lập iPhone 13: sai mật khẩu, đăng nhập, đăng xuất, tài khoản chỉ xem. Bản xem trước cập nhật.

### Việc còn treo
- [ ] Tạo `secrets/users.json` thật trên máy chủ (anh tự làm, không đưa mật khẩu cho tác tử).
- [ ] Chạy qua HTTPS (IIS reverse proxy) và đặt `EMS_COOKIE_SECURE=1`.
- [ ] Đối chiếu schema thật; thử với SQL Server thật.
