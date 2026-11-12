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

## Mục tiêu (2026-11-12): Tích hợp & kiểm chứng AGENTS.md / CLAUDE.md
- [x] Kiểm kê: AGENTS.md, CLAUDE.md (`@AGENTS.md @MEMORY.md @todo.md`), `.claude/` (settings, hook, 1 skill); không có CLAUDE.local.md, `.claude/agents/`.
- [x] Đối chiếu với mã nguồn, sửa 8 điểm thiếu/sai trong AGENTS.md; chú thích 2 tham chiếu không tồn tại trong MEMORY.md.
- [x] Không đổi mã nguồn, hook, permissions; skill chỉ được bổ sung (không xóa dòng nào).
- [x] Cài `requirements-dev.txt` (được ủy quyền); `python -m pytest -q` 121/121 xanh, `python -m ruff check .` (0.16.8) sạch.
- [x] Skill `phat-hanh-ems`: giữ phần Node.js, thêm mục 9 cho repo Python/FastAPI (site `PhanCong`).
- [x] Commit, push nhánh `claude/integrate-agents-claude-md-tsvkvq`, mở PR vào `main` (không tự merge, không triển khai).
- [ ] Thử với SQL Server thật: BLOCKED - môi trường không có SQL Server (đã có ở mục treo phía trên).

## Mục tiêu (2026-11-12, đợt 3): Thêm skills từ anthropics/skills + tham khảo video
- [x] Kiểm tra trùng lặp 19 skill: thêm 6, không thêm 13 (8 trùng tên, 1 trùng chức năng, 4 không phù hợp/chưa rõ giấy phép) - `.claude/skills/NGUON-SKILLS.md`.
- [x] Loại 6 skill khỏi ruff; `ruff check .` sạch, `pytest -q` 121/121.
- [x] Video "7 repo làm video": tóm tắt + kiểm tra giấy phép tại `docs/tham-khao/7-repo-lam-video.md`; không lưu tệp video vào repo.
