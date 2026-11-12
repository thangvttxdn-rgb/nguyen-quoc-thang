# Hiến pháp EMS - Chi nhánh Toa xe Đà Nẵng

> Bản này **chỉ tóm tắt và trỏ về nguồn**. Nội dung đầy đủ, có hiệu lực cao nhất nằm ở
> `AGENTS.md` và `MEMORY.md` (nạp tự động mỗi phiên qua `CLAUDE.md`). Khi hai nơi khác nhau,
> `AGENTS.md` đúng; sửa `AGENTS.md` trước rồi cập nhật bản này.

## Nguyên tắc cốt lõi

### I. An toàn dữ liệu nghiệp vụ (KHÔNG THƯƠNG LƯỢNG)
Không xóa cứng bảng nghiệp vụ, chỉ `IsActive = 0`. Ngừng nhân sự thì ngừng luôn `PhanCong` liên quan
trong cùng giao dịch. Đổi cấu trúc bảng chỉ qua script đánh số trong `src/db/migrations/`, có script
hoàn tác và người duyệt. Xem `AGENTS.md` mục 3a, `MEMORY.md` mục 2.

### II. SQL tham số hóa, không bí mật trong mã (KHÔNG THƯƠNG LƯỢNG)
Mọi truy vấn dùng tham số `?` hoặc `:ten`; cấm ghép chuỗi. Cấu hình kết nối đọc từ biến môi trường.
Không đọc `secrets/`, `.env`. Cưỡng chế bằng `guard.py`, Ruff S105/S106/S608. Xem `AGENTS.md` mục 3, 3a.

### III. Kiểm thử trước khi xong
Mỗi thay đổi có test pytest; `python -m pytest -q` xanh 100% và `ruff check .` không lỗi mới.
Xem `AGENTS.md` mục 5.

### IV. Kiểu dữ liệu chính xác
`DECIMAL` → `decimal.Decimal`, không ép `float`; `DATETIME` theo một múi giờ thống nhất. Báo cáo tổng
hợp dùng `WITH (NOLOCK)` hoặc index phù hợp.

### V. Đơn giản, đúng phạm vi
Không giả định, không sửa lan ngoài yêu cầu (kỹ năng `karpathy-guidelines`). Ưu tiên mở rộng mã có sẵn
trong `src/api`, `src/db` hơn thêm lớp mới.

## Ràng buộc công nghệ

Python (FastAPI) · SQL Server (pyodbc/SQLAlchemy) · HTML/CSS/JS thuần · triển khai IIS nội bộ,
uvicorn **1 worker** (phiên đăng nhập trong bộ nhớ). Thêm thư viện mới phải xin phép.
Xem `AGENTS.md` mục 1, 2 và `docs/TRIEN-KHAI-IIS.md`.

## Quy trình phát triển

Tính năng mới đi theo Spec Kit, gắn với các cổng của Tổng chỉ huy (`.claude/skills/tong-chi-huy`):
G0 `/speckit-specify` + `/speckit-clarify` → G1 `/speckit-plan` + `/speckit-tasks` + `/speckit-implement`
→ G2 `/speckit-checklist`, pytest, ruff → G3 `/speckit-analyze` + `/code-review` → nghiệm thu.
Đặc tả viết tiếng Việt. Không tự tạo nhánh git; làm trên nhánh được giao.

## Quản trị

`AGENTS.md` có hiệu lực cao hơn bản này. Sửa nguyên tắc phải được chủ đầu tư duyệt. Mọi PR kiểm tra
tuân thủ các nguyên tắc I-V.

**Version**: 1.0.0 | **Ratified**: 2026-11-12 | **Last Amended**: 2026-11-12
