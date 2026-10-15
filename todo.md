# KẾ HOẠCH TÁC VỤ HIỆN TẠI (todo.md)

## Mục tiêu: Hàm ghi có xóa mềm cho bảng NhanSu

### Các bước thực hiện (Think -> Act -> Observe)
- [x] 1. `src/db/connection.py`: tài khoản ghi riêng (`read_only=False`), `transaction` (commit/rollback), `execute_write` (chỉ INSERT/UPDATE có WHERE, cấm DELETE).
- [x] 2. `src/db/nhan_su.py`: `deactivate`, `reactivate`, `list_active`, lỗi `NhanSuNotFoundError`.
- [x] 3. Test: `tests/db/test_write.py`, `tests/db/test_nhan_su.py`, kết nối giả `tests/db/conftest.py`.
- [x] 4. Nghiệm thu: `pytest -q` 78/78 xanh, `ruff check .` sạch.
- [x] 5. Đổi luật deny `.env.*` sang tên cụ thể; thêm `DB_USER_APP` / `DB_PASSWORD_APP` vào `.env.example`.
- [ ] 6. Đối chiếu schema thật: tên khóa chính (`Id`?) và cột `IsActive` của `NhanSu`.
- [ ] 7. Hỏi nghiệp vụ: ngừng hoạt động nhân sự có phải ngừng luôn các bản ghi `PhanCong` liên quan?
