# BÁO CÁO NGHIỆM THU – Tích hợp AGENTS.md / CLAUDE.md

**Trạng thái chung: HOÀN THÀNH phạm vi tích hợp trên repo thật.** Đã commit, push nhánh `claude/integrate-agents-claude-md-tsvkvq` và mở PR vào `main` (không tự merge, không triển khai production).
Còn 1 mục **BLOCKED ngoài phạm vi**: thử với SQL Server thật (môi trường không có SQL Server).

Nhãn: **THẬT** = chạy trên repo thật, có bằng chứng · **DEMO** = dữ liệu mẫu (SQLite) · **BLOCKED** = chưa đủ điều kiện.

| Mã | Kiểm thử | Kết quả | Nhãn | Bằng chứng (`bang-chung.txt`) |
|---|---|---|---|---|
| T1 | Thư mục gốc dự án | PASS | THẬT | toplevel `/home/user/nguyen-quoc-thang`, HEAD gốc `6a57a7f` |
| T2 | Hai tệp đúng vị trí | PASS | THẬT | `AGENTS.md`, `CLAUDE.md` ở gốc repo |
| T3 | Đường dẫn nhập | PASS | THẬT | 3/3 `@AGENTS.md`, `@MEMORY.md`, `@todo.md` trỏ tới tệp tồn tại; không import lồng |
| T4 | Claude Code nạp hướng dẫn | PASS | THẬT | Sau khi phiên khởi động lại, Claude Code báo "Instruction files were re-read… differ from their earlier copies" và nạp bản AGENTS/MEMORY/todo **sau sửa** qua `CLAUDE.md` (cơ chế tương đương `/context`) |
| T5 | Trùng lặp / mâu thuẫn | PASS | THẬT | Mâu thuẫn skill Node.js ↔ Python đã xử lý bằng mục 9 của skill; các mâu thuẫn nhẹ đã sửa |
| T6 | Kiến trúc ↔ mã nguồn | PASS | THẬT | `app.py:22` FastAPI; `connection.py:117` pyodbc; `py311`; không có `src/utils`, `package.json`, nhánh `develop` |
| T7 | Không đổi mã nghiệp vụ | PASS | THẬT | `git diff 6a57a7f -- src tests examples deploy docs` rỗng |
| T8 | Skills/Agent không đổi ngoài phạm vi | PASS | THẬT | Skill `phat-hanh-ems`: +40/−0 dòng (chỉ thêm mục 9 + ghi chú chọn quy trình, giữ nguyên phần Node.js). `guard.py`, `settings.local.json` trùng SHA-256 bản sao lưu |
| T9 | Diff, sao lưu, khôi phục | PASS | THẬT | `thay-doi.diff`; bản sao lưu trùng byte với `6a57a7f`; khôi phục: `git checkout 6a57a7f -- <tệp>` |
| T10a | `ruff check .` (bản ghim 0.16.8 như CI) | PASS | THẬT | `All checks passed!` |
| T10b | `pytest -q` toàn bộ (trước đây BLOCKED) | **PASS 121/121** | DEMO | Sau khi cài `requirements-dev.txt`; dữ liệu SQLite mẫu |
| T10c | Thử với SQL Server thật | BLOCKED | BLOCKED | Không có SQL Server trong môi trường (việc treo từ trước, ngoài phạm vi tích hợp) |

**Phát hiện khi chạy lại T10b:** `pytest` trong PATH là bản cô lập (uv tool) nên không thấy `fastapi` dù đã cài → phải dùng `python -m pytest`. Đã ghi vào AGENTS.md mục 2 và MEMORY.md.

**Bằng chứng hook hoạt động:** `guard.py` đã chặn thật một lệnh `rm -rf` và việc ghi tệp ra `/tmp` (ngoài dự án) của chính tác tử.

## Ngân sách
Không gọi API/dịch vụ ngoài ngoài phiên này và việc tải gói pip từ kho chính thức. **Không có số liệu đo chi phí phiên** nên không khẳng định con số.

## Tiêu chí DONE (AGENTS.md mục 5)
1. pytest xanh 100%: **đạt** (121/121).
2. ruff không lỗi mới: **đạt**.
3. Cập nhật `todo.md`, `MEMORY.md`: **đạt**.
