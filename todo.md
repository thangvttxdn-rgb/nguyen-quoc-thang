# KẾ HOẠCH TÁC VỤ HIỆN TẠI (todo.md)

## Mục tiêu: Ví dụ thực tế chạy được cho xóa mềm NhanSu + PhanCong

### Các bước thực hiện (Think -> Act -> Observe)
- [x] 1. `examples/vi_du_ngung_nhan_su.py`: dữ liệu mẫu 3 trạm KCTX, SQLite trong bộ nhớ, lớp bọc giống pyodbc, 4 tình huống (ngừng, mã sai → rollback, kích hoạt lại, thử DELETE).
- [x] 2. `tests/examples/test_vi_du_ngung_nhan_su.py`: chạy câu SQL thật trên SQLite (5 test).
- [x] 3. Nghiệm thu: `pytest -q` 85/85 xanh, `ruff check .` sạch.

### Việc còn treo
- [ ] Đối chiếu schema thật: khóa `NhanSu.Id`, cột liên kết `PhanCong.NhanSuId`, cờ `IsActive` ở cả hai bảng.
- [ ] Thử với SQL Server thật (cần `pyodbc` + ODBC Driver 18 + `.env`).
