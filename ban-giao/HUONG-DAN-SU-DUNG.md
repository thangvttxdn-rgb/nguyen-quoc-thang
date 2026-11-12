# HƯỚNG DẪN SỬ DỤNG

## 1. Tệp nằm ở đâu
- Đã commit trên nhánh `claude/integrate-agents-claude-md-tsvkvq`, có PR vào `main` (chưa merge):
  `AGENTS.md`, `MEMORY.md`, `todo.md`, `.claude/skills/phat-hanh-ems/SKILL.md` (thêm mục 9), thư mục `ban-giao/`, `ban-giao.zip`.
- `CLAUDE.md` giữ nguyên (đã có `@AGENTS.md`).

## 2. Việc người duyệt cần làm
1. Mở `XEM-TRUOC-TOAN-BO.html` bằng trình duyệt (Windows hoặc Safari iPhone, không cần mạng).
2. Xem PR trên GitHub, chờ CI xanh (ruff + pytest trên Python 3.11 và 3.13), rồi tự merge.
3. Điền các ô `<điền>` còn lại trong skill `phat-hanh-ems` mục 9 (máy chủ staging/production, thư mục sao lưu) khi có thông tin hạ tầng.
4. Tùy chọn: xóa `ban-giao/` và `ban-giao.zip` khỏi repo sau khi lưu trữ.

## 3. Chạy kiểm thử trên máy mình
```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q --tb=short     # dùng python -m để chạy đúng môi trường
python -m ruff check . --quiet
```

## 4. Kiểm tra Claude Code nạp hướng dẫn
Mở phiên Claude Code mới tại gốc repo, gõ `/context` hoặc `/memory`: phải thấy `CLAUDE.md` cùng `AGENTS.md`, `MEMORY.md`, `todo.md`.

## 5. Khôi phục bản cũ
```bash
git checkout 6a57a7f -- AGENTS.md MEMORY.md todo.md .claude/skills/phat-hanh-ems/SKILL.md
```
Hoặc chép đè từ `ban-giao/sao-luu/` (đối chiếu bằng `SHA256SUMS.txt`). Nếu đã merge: `git revert <commit>`.
