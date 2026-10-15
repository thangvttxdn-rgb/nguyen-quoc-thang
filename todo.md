# KẾ HOẠCH TÁC VỤ HIỆN TẠI (todo.md)

## Mục tiêu: [Tên tính năng hoặc lỗi cần sửa - VD: Sửa lỗi tính toán ở phân hệ X]

### Các bước thực hiện (Think -> Act -> Observe)
- [x] 1. Khoanh vùng lỗi: Đọc log và chạy thử test tại phân hệ liên quan.
- [~] 2. Xử lý mã nguồn: Cập nhật logic tại file `src/...` (Đang thực hiện).
- [ ] 3. Viết bổ sung kịch bản kiểm thử (unit test) cho trường hợp biên.
- [ ] 4. Nghiệm thu (Verifier): Chạy lại toàn bộ test và kiểm tra lint.

### Nháp trong lượt (Scratchpad)
- Nguyên nhân gốc nằm ở hàm xử lý làm tròn số dòng 88.
- Cần kiểm tra xem có ảnh hưởng đến báo cáo tổng hợp không.
