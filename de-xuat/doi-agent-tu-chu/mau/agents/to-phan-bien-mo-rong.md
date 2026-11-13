# Agent 4 - Chuyên gia phản biện: MỞ RỘNG tác tử `to-phan-bien` sẵn có, không tạo mới

Đề xuất sửa `.claude/agents/to-phan-bien.md` (chờ duyệt - Phạm vi giai đoạn 1 không sửa thật):

1. Thêm vào frontmatter: `model: opus` và `effort: high` (chỉ gọi khi rủi ro cao, xem ma trận).
2. Thêm mục rà thứ 7 vào phần "Rà theo thứ tự":

   7. **Phương án kỹ thuật rủi ro cao** (khi Tổng chỉ huy gửi kèm báo cáo Agent 1 và kết quả Agent 3):
      phương án có đạt tiêu chí không; có đường quay lại không (worktree bỏ được, migration có script
      hoàn tác); có chạm CSDL thật, quyền, CI, guard.py không; Agent 3 có chạy test THẬT không.

3. Giữ nguyên: chỉ `Read, Grep, Glob`; không sửa tệp; trả PASS | FAIL | BLOCKED.

Lý do không tạo Agent 4 riêng: `to-phan-bien` đã là cổng G3 độc lập, chỉ đọc, đã được kiểm chứng
(bắt được 11 điểm Tổ 1 bỏ sót - MEMORY.md 2026-11-12). Thêm tác tử trùng vai trò là trùng lặp.
