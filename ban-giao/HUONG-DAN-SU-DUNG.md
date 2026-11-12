# HƯỚNG DẪN SỬ DỤNG

## 1. Tệp nằm ở đâu
- Thay đổi đã nằm trong repo (chưa commit): `AGENTS.md`, `MEMORY.md`, `todo.md`. `CLAUDE.md` giữ nguyên (đã có `@AGENTS.md`).
- Gói bàn giao: thư mục `ban-giao/` (chưa commit) và `ban-giao.zip`.

## 2. Việc người duyệt cần làm
1. Mở `XEM-TRUOC-TOAN-BO.html` bằng trình duyệt (Windows hoặc Safari iPhone, không cần mạng).
2. Duyệt cài công cụ rồi chạy lại kiểm thử đầy đủ:
   ```bash
   pip install -r requirements-dev.txt
   pytest -q --tb=short
   ruff check . --quiet
   ```
3. Nếu đồng ý, commit (tác tử không tự commit). Không commit `ban-giao/` nếu không cần:
   ```bash
   git add AGENTS.md MEMORY.md todo.md
   git commit -m "docs(agents): đối chiếu AGENTS.md với mã nguồn, ghi nhận mâu thuẫn skill phat-hanh-ems"
   git push -u origin claude/integrate-agents-claude-md-tsvkvq
   ```
4. Quyết định về skill `phat-hanh-ems` (Node.js ↔ Python): sửa cho đúng dự án, hoặc xác nhận EMS Node.js là hệ thống khác.

## 3. Kiểm tra Claude Code nạp hướng dẫn
Mở phiên Claude Code mới tại gốc repo, gõ `/context` hoặc `/memory`: phải thấy `CLAUDE.md` cùng `AGENTS.md`, `MEMORY.md`, `todo.md`.

## 4. Khôi phục bản cũ
```bash
git checkout -- AGENTS.md MEMORY.md todo.md   # khi chưa commit
```
Hoặc chép đè từ `ban-giao/sao-luu/` (đối chiếu bằng `SHA256SUMS.txt`).
