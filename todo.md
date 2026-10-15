# KẾ HOẠCH TÁC VỤ HIỆN TẠI (todo.md)

## Mục tiêu: Ngừng nhân sự thì ngừng luôn PhanCong liên quan

### Các bước thực hiện (Think -> Act -> Observe)
- [x] 1. `src/db/nhan_su.py`: `deactivate` cập nhật thêm `PhanCong SET IsActive = 0 WHERE NhanSuId = ? AND IsActive = 1`, trả về `DeactivateResult(nhan_su_changed, phan_cong_count)`.
- [x] 2. Nhân sự đã ngừng từ trước vẫn dọn PhanCong còn sót; mã không tồn tại thì báo lỗi, không đụng PhanCong.
- [x] 3. `reactivate` không tự khôi phục PhanCong.
- [x] 4. Test: `tests/db/test_nhan_su.py` (9 test). Nghiệm thu: `pytest -q` 80/80 xanh, `ruff check .` sạch.

### Việc còn treo
- [ ] Đối chiếu schema thật: khóa `NhanSu.Id`, cột liên kết `PhanCong.NhanSuId`, cờ `IsActive` ở cả hai bảng.
