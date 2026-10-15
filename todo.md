# KẾ HOẠCH TÁC VỤ HIỆN TẠI (todo.md)

## Mục tiêu: Hàm thêm phân công mới cho nhân sự

### Các bước thực hiện (Think -> Act -> Observe)
- [x] 1. `src/db/phan_cong.py`: `add(conn, nhan_su_id, noi_dung)` - chỉ giao cho nhân sự tồn tại và đang hoạt động, chặn trùng phân công đang hiệu lực, kiểm tra nội dung rỗng/quá dài; `list_active(conn, nhan_su_id)`.
- [x] 2. Test: `tests/db/test_phan_cong.py` (10 test, gồm 3 test chạy SQL thật trên SQLite).
- [x] 3. Ví dụ: thêm tình huống [5] giao việc lại sau khi kích hoạt nhân sự.
- [x] 4. Nghiệm thu: `pytest -q` 95/95 xanh, `ruff check .` sạch.

### Việc còn treo
- [ ] Đối chiếu schema thật: `NhanSu.Id`, `PhanCong.NhanSuId`, `PhanCong.NoiDung` (độ dài?), `IsActive`, `PhanCong.Id` có IDENTITY không.
- [ ] Thử với SQL Server thật (cần `pyodbc` + ODBC Driver 18 + `.env`).
