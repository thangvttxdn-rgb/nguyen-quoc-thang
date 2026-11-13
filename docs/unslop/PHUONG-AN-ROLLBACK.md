# Phương án gỡ cài đặt và khôi phục

Toàn bộ thay đổi nằm trong kho, không đụng PATH, registry Windows, cấu hình toàn cục `~/.claude/`,
`.claude/settings.local.json` hay `src/`. Không cần quyền Administrator.

## 1. Danh sách thay đổi

| Loại | Đường dẫn |
|---|---|
| Thêm | `.claude/thu-nghiem/` (bản gốc unslop, `unslop.sha256`, lớp bọc `ctxdn-ui-ux-unslop/`) |
| Thêm | `docs/unslop/` (hồ sơ, `vi-du/`, `kiem-thu/`) |
| Sửa | `.claude/tong-chi-huy/registry.json` (+2 mục, +1 tuyến, `giao diện` chuyển tuyến, +5 trùng lặp, +1 nguồn ngoài) |
| Sửa | `.claude/hooks/dieu_phoi.py` (hàm `_ten_muc`: nhãn thử nghiệm) |
| Sửa | `tests/harness/test_dieu_phoi.py` (trạng thái `thu-nghiem`, +7 test) |
| Sửa | `docs/ai-command-center.html` (nhãn thử nghiệm + dữ liệu registry sinh lại) |
| Sửa | `todo.md`, `MEMORY.md` |

## 2. Gỡ hoàn toàn

Cách 1 - hoàn tác **toàn bộ dải commit** unslop (khuyên dùng, giữ lịch sử). Việc cài gồm nhiều commit
(cài đặt, ghi kết quả gỡ, sửa sau G3); revert một commit lẻ sẽ không về đúng trạng thái cũ:

```bash
git revert --no-edit af0596b..<commit-cuối-của-unslop>   # af0596b = commit ngay trước khi cài
python -m pytest -q          # phải xanh
```

Cách 2 - gỡ bằng tay (khi đã có thay đổi khác chồng lên):

```bash
git rm -r .claude/thu-nghiem docs/unslop
git checkout <mã-commit-trước-unslop> -- .claude/tong-chi-huy/registry.json .claude/hooks/dieu_phoi.py tests/harness/test_dieu_phoi.py docs/ai-command-center.html
python .claude/tong-chi-huy/build_page.py
python -m pytest -q
```

Trên Windows (PowerShell) các lệnh `git` giống hệt; dùng `py -3` nếu không có `python`.
Nếu đã cài Playwright theo hướng dẫn Windows: xóa thư mục `%USERPROFILE%\ctxdn-ui-test`.

Đã thử Cách 1 trên bản sao kho trong sandbox: xem kết quả mục 4.

## 3. Kích hoạt (chỉ khi chủ đầu tư duyệt)

```bash
git mv .claude/thu-nghiem/ctxdn-ui-ux-unslop .claude/skills/ctxdn-ui-ux-unslop
git mv .claude/thu-nghiem/unslop .claude/skills/ctxdn-ui-ux-unslop/unslop
```

Rồi sửa đường dẫn `../unslop/` trong `SKILL.md` thành `unslop/`, sửa `duong_dan` và `trang_thai` trong registry
(bỏ `thu-nghiem`, đổi test `test_muc_thu_nghiem_khong_nam_trong_thu_muc_skills` và `test_ban_goc_unslop_khong_bi_sua`
theo đường dẫn mới), chạy `build_page.py` và pytest. Bản gốc `unslop` vẫn **không** đặt thẳng ở `.claude/skills/unslop`
để không tự kích hoạt ngoài lớp bọc. Kích hoạt chỉ ảnh hưởng phiên Claude Code mở kho này, không phải máy chủ IIS.

Quay lui sau kích hoạt: `git revert` commit kích hoạt.

## 4. Kết quả thử gỡ - THẬT

Lần 1 (trước G3) chỉ revert commit `318f482` - G3 chỉ ra là chưa đủ vì nhánh có thêm commit.
Lần 2 chạy lại với toàn dải - kết quả ở cuối file. Bảng lần 1, để đối chiếu:

| Bước | Kết quả |
|---|---|
| `git clone` kho → `git revert --no-edit 318f482` | Tạo commit hoàn tác, không xung đột |
| `.claude/thu-nghiem/`, `docs/unslop/` | Đã biến mất |
| `git diff af0596b HEAD` (so với trước khi cài) | **Rỗng** - trở về đúng trạng thái cũ |
| `python -m pytest` | 176 passed (183 trừ 7 test của unslop) |
| `build_page.py --check` | Trang Command Center khớp registry |
