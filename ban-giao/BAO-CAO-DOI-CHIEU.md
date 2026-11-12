# BÁO CÁO ĐỐI CHIẾU – AGENTS.md / CLAUDE.md với mã nguồn

- Repo: `thangvttxdn-rgb/nguyen-quoc-thang`, nhánh `claude/integrate-agents-claude-md-tsvkvq`, HEAD gốc `6a57a7f`
- Ngày: 12/11/2026 – Môi trường: container đám mây Claude Code (máy `vm`), thư mục `/home/user/nguyen-quoc-thang`

## 1. Kiểm kê hiện trạng (THẬT)

| Tệp / thư mục | Có? | Ghi chú |
|---|---|---|
| `AGENTS.md` | Có | Quy chuẩn chính, 53 dòng (trước sửa) |
| `CLAUDE.md` | Có | Đã có `@AGENTS.md`, `@MEMORY.md`, `@todo.md` – **không cần sửa** |
| `CLAUDE.local.md` | Không | – |
| `.claude/settings.local.json` | Có | permissions + hook PreToolUse (đang được commit vào repo) |
| `.claude/hooks/guard.py` | Có | Chặn `rm -rf`, SQL nguy hiểm, ghi ngoài dự án, mật khẩu hardcode |
| `.claude/skills/phat-hanh-ems/` | Có | 1 skill dự án |
| `.claude/agents/` | Không | Không có subagent riêng |
| Skills dùng chung CTXĐN | Cấp tài khoản | `tro-ly-22-ky-nang-ctxdn`, `bao-cao-an-toan-van-dung-ctxdn`, `phan-tich-su-co-toa-xe`… – không nằm trong repo, không đụng tới |

**Bộ tệp ngày 12/11 trước đó:** không có trong repo và không có trong phiên này → **không xác định được danh sách "8 vị trí còn thiếu" gốc**. Thay vào đó đã tự rà AGENTS.md với mã nguồn, tìm được 8 điểm thiếu/sai dưới đây. Nếu danh sách gốc khác, cần đối chiếu lại.

## 2. Tám điểm đã điền/sửa trong AGENTS.md (có bằng chứng)

| # | Trước | Sau | Bằng chứng |
|---|---|---|---|
| 1 | Chưa phân biệt quy định chung / riêng | Thêm khối "Phạm vi" | Skills CTXĐN ở cấp tài khoản; repo chỉ có 1 skill |
| 2 | "FastAPI / Flask" | FastAPI, Python ≥ 3.11 | `src/api/app.py:22`, `pyproject.toml:7`; không có `flask` trong mã |
| 3 | "pyodbc / SQLAlchemy" | pyodbc; demo dùng SQLite; chưa dùng SQLAlchemy | `src/db/connection.py:117`; grep không thấy `sqlalchemy` |
| 4 | Thiếu thư mục | Thêm `migrations/`, `deploy/`, `docs/`, `examples/`, `.claude/`, nhóm test | Cây thư mục thực |
| 5 | Lint `ruff check src/` | `ruff check .` (trùng CI) | `.github/workflows/ci.yml` |
| 6 | Không nói về subagent riêng | Ghi rõ chưa có `.claude/agents/` | `ls .claude` |
| 7 | Không có mục Skills | Thêm mục 4a + cảnh báo mâu thuẫn skill | `.claude/skills/phat-hanh-ems/SKILL.md:15-22` |
| 8 | DONE không nói điều kiện cài đặt | Phải cài `requirements-dev.txt`, thiếu thì BLOCKED | `pytest` lỗi thu thập `tests/api/test_app.py:6` |

## 3. Mâu thuẫn phát hiện

| Mức | Nội dung | Xử lý |
|---|---|---|
| **Nghiêm trọng** | Skill `phat-hanh-ems` mô tả EMS là **Node.js** (`npm ci`, `package.json`, nhánh `develop`), repo thực là **Python/FastAPI**, không có `package.json`, không có nhánh `develop`. Skill có bước triển khai production. | **Không sửa skill** (cần người duyệt). Ghi cảnh báo vào AGENTS.md mục 4a và MEMORY.md. |
| Trung bình | MEMORY.md dẫn `src/utils/formatter.py:42` – tệp không tồn tại | Giữ nguyên dòng cũ, thêm chú thích chỉ sang `src/db/connection.py:9` |
| Nhẹ | MEMORY.md dẫn `tax.py:88` – chỉ là ví dụ | Thêm chú thích |
| Nhẹ | Lint `src/` (AGENTS) ≠ `.` (CI) | Thống nhất `ruff check .` |
| Nhẹ | AGENTS nhắc SQLAlchemy `text(":ma")` nhưng repo chưa dùng | Giữ quy tắc, ghi "hiện chưa dùng" |
| Ghi nhận | `.claude/settings.local.json` thường là tệp cá nhân nhưng ở đây được commit | Giữ nguyên (đang là lớp cưỡng chế chung) |

**Không mâu thuẫn:** quyền hạn (settings hỏi mọi `git push` – chặt hơn AGENTS, hợp lệ); bảo mật (hook + ruff `S` + `.gitignore` khớp AGENTS mục 3); triển khai IIS (AGENTS ↔ `docs/TRIEN-KHAI-IIS.md` ↔ `.gitignore`).

**G0–G1:** repo không có tham chiếu; chỉ ghi chú là áp dụng cho việc tạo/sửa Skills, không áp cho việc này.
