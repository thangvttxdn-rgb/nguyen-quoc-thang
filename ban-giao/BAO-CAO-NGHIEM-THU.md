# BÁO CÁO NGHIỆM THU – Tích hợp AGENTS.md / CLAUDE.md

**Trạng thái chung: ĐÃ TÍCH HỢP TRÊN REPO THẬT – CHƯA HOÀN THÀNH** (còn 2 mục BLOCKED; chưa commit vì lệnh cấm tác tử tự commit).

Nhãn: **THẬT** = chạy trên repo thật, có bằng chứng · **DEMO** = chạy với dữ liệu mẫu (SQLite) · **BLOCKED** = chưa đủ điều kiện chạy.

| Mã | Kiểm thử | Kết quả | Nhãn | Bằng chứng (`bang-chung.txt`) |
|---|---|---|---|---|
| T1 | Thư mục gốc dự án | PASS | THẬT | `git rev-parse --show-toplevel` = `/home/user/nguyen-quoc-thang`, HEAD `6a57a7f` |
| T2 | Hai tệp đúng vị trí | PASS | THẬT | `AGENTS.md`, `CLAUDE.md` ở gốc repo |
| T3 | Đường dẫn nhập | PASS | THẬT | 3/3 `@AGENTS.md`, `@MEMORY.md`, `@todo.md` trỏ tới tệp tồn tại; không có import lồng |
| T4 | Claude Code nạp hướng dẫn | PASS | THẬT | (1) Đầu phiên: Claude Code nạp `CLAUDE.md` kèm toàn văn 3 tệp (bản trước sửa). (2) Sau khi tiến trình phiên khởi động lại, Claude Code thông báo "Instruction files were re-read… differ from their earlier copies" và nạp **bản AGENTS.md/MEMORY.md/todo.md sau sửa** qua `CLAUDE.md`. Không dùng `/context` (phiên đám mây không tương tác) – đây là cơ chế tương đương. |
| T5 | Trùng lặp / mâu thuẫn | PASS có cảnh báo | THẬT | 1 mâu thuẫn nghiêm trọng ở skill `phat-hanh-ems` – đã ghi nhận, chưa sửa (xem BAO-CAO-DOI-CHIEU) |
| T6 | Kiến trúc ↔ mã nguồn | PASS | THẬT | `app.py:22` FastAPI; `connection.py:117` pyodbc; `py311`; không có `src/utils`, `package.json`, nhánh `develop` |
| T7 | Không đổi mã nghiệp vụ | PASS | THẬT | `git diff --name-only` = chỉ `AGENTS.md`, `MEMORY.md`, `todo.md` (+ thư mục `ban-giao/` chưa theo dõi) |
| T8 | Skills/Agent không bị đổi | PASS | THẬT | SHA-256 `SKILL.md` f2d58765…, `guard.py` e7c14ea7…, `settings.local.json` 9011b8d2…, `CLAUDE.md` b8b779aa… trùng bản sao lưu |
| T9 | Diff, sao lưu, khôi phục | PASS | THẬT | `git diff --stat` 3 tệp (+28/−8); bản sao lưu trùng byte với HEAD → khôi phục được |
| T10a | `ruff check .` | PASS | THẬT | `All checks passed!` |
| T10b | `pytest` ngoài `tests/api/` | PASS 95/95 | DEMO | CSDL SQLite mẫu, không phải SQL Server thật |
| T10c | `pytest -q` toàn bộ | **BLOCKED** | BLOCKED | Thiếu `fastapi` → lỗi thu thập `tests/api/test_app.py`. Cần duyệt `pip install -r requirements-dev.txt` |
| T10d | Thử với SQL Server thật | **BLOCKED** | BLOCKED | Không có SQL Server trong môi trường |

**Bằng chứng hook hoạt động:** `guard.py` đã chặn thật (1) một lệnh `rm -rf` và (2) việc ghi báo cáo ra `/tmp` (ngoài dự án) của chính tác tử trong phiên này → gói bàn giao được đặt trong `ban-giao/`.

## Ngân sách
Không gọi API/dịch vụ ngoài; chỉ kiểm thử tĩnh và pytest cục bộ; không chạy `claude -p`. **Không có số liệu đo chi phí phiên** nên không khẳng định con số.

## Tiêu chí DONE (AGENTS.md mục 5)
1. pytest xanh 100%: **chưa** (BLOCKED T10c).
2. ruff không lỗi mới: **đạt**.
3. Cập nhật `todo.md`, `MEMORY.md`: **đạt**.
