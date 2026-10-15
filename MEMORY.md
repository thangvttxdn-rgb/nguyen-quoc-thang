# BỘ NHỚ DÀI HẠN DỰ ÁN (MEMORY.md)

*Chỉ ghi lại các quyết định kiến trúc quan trọng, đặc thù hệ thống và các lỗi hóc búa đã xử lý (Kèm tên file và số dòng).*

## 1. Lỗi điển hình & Bài học xương máu (Bug Patterns)
- `[2026-10-15]` **Lỗi sai lệch số liệu / kiểu dữ liệu**: Khi xử lý dữ liệu từ SQL Server lên Python, các trường `DECIMAL` cần ép kiểu rõ ràng trước khi serialize sang JSON (Xem cách xử lý tại `src/utils/formatter.py:42`).
- `[Mẫu từ sơ đồ]` `"currency bug: tax.py:88"` — Luôn kiểm tra đơn vị tiền tệ trước khi áp thuế.

## 2. Đặc thù Cơ sở dữ liệu & Nghiệp vụ
- Bảng `NhanSu` và `PhanCong` liên kết qua mã định danh nội bộ, tuyệt đối không xóa cứng (hard delete) mà chỉ cập nhật cờ `IsActive = 0`.
- Các truy vấn báo cáo tổng hợp bắt buộc phải có `WITH (NOLOCK)` hoặc tối ưu index để tránh khóa bảng trong giờ cao điểm.
