# KẾ HOẠCH TÁC VỤ HIỆN TẠI (todo.md)

## Mục tiêu: Thêm workflow CI chạy pytest và ruff

### Các bước thực hiện (Think -> Act -> Observe)
- [x] 1. `requirements-dev.txt`: ghim `pytest==9.1.1`, `ruff==0.16.8`.
- [x] 2. `.github/workflows/ci.yml`: ruff (gồm luật bảo mật S) + pytest, ma trận Python 3.11 / 3.13, quyền `contents: read`.
- [x] 3. Chạy thử đúng các bước CI trên máy: Python 3.11 và 3.13 đều 78/78 xanh, ruff sạch.
- [ ] 4. Theo dõi lần chạy CI đầu tiên trên PR #4.

### Việc còn treo từ tác vụ trước
- [ ] Đối chiếu schema thật của `NhanSu` (khóa `Id`? cờ `IsActive`?).
- [ ] Nghiệp vụ: ngừng nhân sự có ngừng luôn `PhanCong` liên quan?
