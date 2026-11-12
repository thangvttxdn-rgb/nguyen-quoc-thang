# QUY CHUẨN KIẾN TRÚC & VẬN HÀNH AGENT (AGENTS.md)

> **Phạm vi.** Mục 3 (an toàn, xin phép), mục 5 (định nghĩa DONE) và yêu cầu trả lời tiếng Việt là **quy định dùng chung CTXĐN**. Các mục còn lại là **riêng dự án này** (web app EMS phân công nhân sự, Python). Skills dùng chung CTXĐN cài ở cấp tài khoản, không nằm trong repo. Nạp vào Claude Code qua `@AGENTS.md` trong `CLAUDE.md`.

## 1. Tổng quan Kiến trúc & Công nghệ
- **Backend:** Python ≥ 3.11 (`target-version` trong `pyproject.toml`), FastAPI (`src/api/app.py:22`). Không dùng Flask.
- **Cơ sở dữ liệu:** SQL Server qua pyodbc (`src/db/connection.py:117`, import trễ); chế độ demo `EMS_DEMO=1` dùng SQLite có sẵn. Hiện chưa dùng SQLAlchemy.
- **Frontend:** HTML5, CSS3, JavaScript thuần (Vanilla JS)
- **Thư mục chính:**
  - `src/api/`: Các route xử lý nghiệp vụ và API.
  - `src/db/`: Kết nối CSDL, stored procedures và schema.
  - `src/static/` & `src/templates/`: Giao diện người dùng.
  - `tests/`: Toàn bộ bài kiểm thử tự động (pytest), chia `api/`, `db/`, `examples/`, `harness/`.
  - `src/db/migrations/`: script đổi cấu trúc bảng (hiện trống, chỉ có `.gitkeep`).
  - `deploy/` (IIS, SQL tạo tài khoản), `docs/` (hướng dẫn, bản xem trước), `examples/` (ví dụ chạy trên SQLite).
  - `.claude/`: `settings.local.json` (permissions + hook), `hooks/guard.py`, `skills/phat-hanh-ems/`.

## 2. Lệnh Thực thi & Lọc nhiễu (Observe & Trim)
Luôn sử dụng cờ rút gọn (quiet/short) khi chạy lệnh để cắt giảm log thừa, tránh làm tràn cửa sổ ngữ cảnh:
- **Chạy toàn bộ test:** `pytest -q --tb=short`
- **Chạy test theo phân hệ:** `pytest tests/<ten_phan_he>/ -q`
- **Kiểm tra lỗi cú pháp/quy chuẩn (Lint):** `ruff check . --quiet` (cùng phạm vi với CI; `ruff check src/` chỉ là kiểm tra nhanh, bỏ sót `tests/`, `examples/`, `.claude/hooks/`).
- **Cài công cụ:** `pip install -r requirements-dev.txt` (phiên bản ghim, trùng với CI; đã gồm `requirements.txt`).
- **Chạy web app (dữ liệu mẫu):** `EMS_DEMO=1 uvicorn src.api.app:app --host 0.0.0.0 --port 8000` (1 worker). Cần file tài khoản `secrets/users.json`; tạo chuỗi băm mật khẩu bằng `python -m src.api.auth`. Tác tử không được đọc `secrets/`. Sửa giao diện (`src/templates`, `src/static`) thì sinh lại bản xem trước `docs/giao-dien-mobile.html`.
- **Triển khai IIS:** làm theo `docs/TRIEN-KHAI-IIS.md`; máy chủ cài `requirements-prod.txt`. Không bao giờ commit `deploy/iis/web.config` (chỉ commit file `.mau`).
- **CI:** `.github/workflows/ci.yml` chạy `ruff check .` và `pytest` trên Python 3.11 và 3.13 cho mọi PR và push lên `main`.

## 3. Quy tắc An toàn & Phân quyền (Policy Gate)
- **ĐƯỢC PHÉP TỰ ĐỘNG (ALLOW):** Đọc file, tìm kiếm mã nguồn, chạy `pytest`, chạy `ruff`, truy vấn SQL dạng `SELECT`.
- **PHẢI XIN PHÉP CON NGƯỜI (ASK/APPROVE):** Mọi thao tác sửa file cấu hình hệ thống, thay đổi cấu trúc bảng (`ALTER/DROP TABLE`), cài đặt thêm thư viện mới, hoặc đẩy code lên nhánh chính.
- **CẤM TUYỆT ĐỐI (DENY):** Xóa thư mục gốc (`rm -rf`), can thiệp ra ngoài phạm vi thư mục dự án, hardcode mật khẩu/chuỗi kết nối CSDL trực tiếp vào mã nguồn.

### Cưỡng chế kỹ thuật
| Lớp | File | Chặn được |
|---|---|---|
| Permissions | `.claude/settings.local.json` | Lệnh/đường dẫn khớp mẫu chữ |
| Hook PreToolUse | `.claude/hooks/guard.py` | Mọi biến thể `rm -rf`; câu SQL ghi/đổi cấu trúc trong lệnh gọi CSDL (ask), `SHUTDOWN`/`DROP DATABASE` (deny); ghi file ngoài dự án; mật khẩu hardcode |
| Ruff `S` | `pyproject.toml` | Mật khẩu hardcode (S105/S106), SQL ghép chuỗi (S608) |
| Tài khoản CSDL | `.env` | Tác tử chỉ dùng tài khoản `db_datareader` - lớp chắc chắn nhất |

Sửa `guard.py` phải kèm test tại `tests/harness/test_guard.py`.

## 3a. Quy tắc SQL Server
- **Tham số hóa mọi truy vấn** (`cursor.execute("... WHERE Id = ?", ma)` hoặc `text(":ma")` của SQLAlchemy). Cấm ghép chuỗi/f-string vào câu SQL.
- **Cấu hình kết nối** đọc từ biến môi trường (mẫu tại `.env.example`); `.env` không được commit.
- **Thay đổi cấu trúc bảng** chỉ qua script đánh số trong `src/db/migrations/` (vd. `0003_them_cot_ghi_chu.sql`), có kèm script hoàn tác, và phải được người duyệt trước khi chạy.
- **Không xóa cứng** bảng nghiệp vụ: cập nhật `IsActive = 0` (xem `MEMORY.md`).
- **Kiểu dữ liệu**: `DECIMAL` -> `decimal.Decimal`, không ép sang `float` khi tính toán; `DATETIME` lưu và so sánh theo một múi giờ thống nhất.

## 4. Điều phối Tác tử phụ (Subagents)
- Repo chưa định nghĩa subagent riêng (không có `.claude/agents/`); dùng subagent có sẵn của Claude Code.
- Khi cần tìm kiếm vị trí sử dụng của một biến/hàm trên toàn bộ dự án hoặc đọc tài liệu quy chuẩn dài, hãy tách **Subagent** với vùng ngữ cảnh độc lập để rà soát và chỉ trả về bản tóm tắt ngắn gọn cho Agent chính.

## 4a. Skills trong repo
- `.claude/skills/phat-hanh-ems/SKILL.md`: quy trình phát hành EMS. **Lưu ý mâu thuẫn chưa xử lý:** skill mô tả EMS là Node.js (`npm ci`, `npm test`, `package.json`, nhánh `develop`), trong khi repo này là Python/FastAPI, không có `package.json`, không có nhánh `develop`. Chưa dùng skill này cho repo này cho đến khi người duyệt xác nhận và sửa. Tác tử không tự triển khai production.
- Quy trình G0–G1 chỉ áp dụng cho công việc tạo/sửa Skills, không áp dụng cho việc sửa mã nguồn thông thường.

## 5. Tiêu chuẩn Nghiệm thu (Verifier - Định nghĩa "DONE")
Một tác vụ CHỈ được phép đánh dấu hoàn thành khi thỏa mãn đồng thời 3 điều kiện thực tế:
1. Chạy `pytest -q` báo xanh 100% (tests pass). Cần cài `requirements-dev.txt` trước; thiếu `fastapi`/`httpx` thì `tests/api/` lỗi thu thập - khi đó báo BLOCKED, không báo PASS.
2. Chạy `ruff check .` không phát sinh lỗi mới (no new lint errors).
3. Đã cập nhật trạng thái vào `todo.md` và ghi chú phát hiện quan trọng (nếu có) vào `MEMORY.md`.
