# KẾ HOẠCH TÁC VỤ HIỆN TẠI (todo.md)

## Mục tiêu: Viết mẫu `src/db/connection.py` (kết nối SQL Server an toàn) kèm test

### Các bước thực hiện (Think -> Act -> Observe)
- [x] 1. Thiết kế: cấu hình từ env, chuỗi kết nối mã hóa + ReadOnly, chỉ cho SELECT tham số hóa.
- [x] 2. Xử lý mã nguồn: `src/db/connection.py`.
- [x] 3. Kiểm thử: `tests/db/test_connection.py` (21 test, dùng kết nối giả, không cần SQL Server).
- [x] 4. Nghiệm thu: `pytest -q` 53/53 xanh, `ruff check .` sạch.
- [ ] 5. Thử với SQL Server thật (cần cài `pyodbc` + ODBC Driver 18 và điền `.env`) - chờ người dùng.

### Nháp trong lượt (Scratchpad)
- `pyodbc` chưa có trong dependency: thêm thư viện mới cần người duyệt (Policy Gate).
- `ApplicationIntent=ReadOnly` chỉ có tác dụng khi dùng Always On read replica; quyền thật vẫn do tài khoản `db_datareader` quyết định.
