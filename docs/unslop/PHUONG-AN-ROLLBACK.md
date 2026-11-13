# Phương án gỡ cài đặt và khôi phục

Toàn bộ thay đổi nằm trong kho, không đụng PATH, registry Windows, cấu hình toàn cục `~/.claude/`
hay `.claude/settings.local.json`. Ngoại lệ có duyệt: `src/static/app.css` (chỉ CSS, commit `730dca2`).
Không cần quyền Administrator.

## 1. Danh sách thay đổi (trạng thái hiện hành, sau kích hoạt)

| Loại | Đường dẫn |
|---|---|
| Thêm | `.claude/skills/ctxdn-ui-ux-unslop/` (lớp bọc `SKILL.md`, `scripts/`, bản gốc `unslop/`, `unslop.sha256`) |
| Thêm | `docs/unslop/` (hồ sơ, `vi-du/`, `kiem-thu/`) |
| Sửa | `src/static/app.css` (toast, nút 44 px, mã màu trạng thái, băng dữ liệu mẫu) - commit `730dca2` |
| Sửa | `.claude/tong-chi-huy/registry.json` (+2 mục, +1 tuyến, `giao diện` chuyển tuyến, +5 trùng lặp, +1 nguồn ngoài) |
| Sửa | `.claude/hooks/dieu_phoi.py` (hàm `_ten_muc`: nhãn `chi_qua` và `thu-nghiem`) |
| Sửa | `tests/harness/test_dieu_phoi.py` (+9 test) |
| Sửa | `docs/ai-command-center.html` (dữ liệu registry sinh lại) |
| Sửa | `todo.md`, `MEMORY.md` |
| Commit | `318f482` cài · `60e4150` ghi kết quả gỡ lần 1 · `a3d84ee` sửa /code-review · `de2b2d7` sửa Tổ 2 · `5cab4b4`, `912b967`, `730dca2` (kích hoạt + CSS), `fc1de51` và các commit ghi hồ sơ sau đó |

Các file cũ `.claude/thu-nghiem/` đã được `git mv` sang vị trí mới; không còn thư mục này.

## 2. Gỡ hoàn toàn

Cách 1 - hoàn tác **toàn bộ dải commit** unslop (khuyên dùng, giữ lịch sử). Việc cài gồm nhiều commit
(cài đặt, ghi kết quả gỡ, sửa sau G3); revert một commit lẻ sẽ không về đúng trạng thái cũ:

```bash
git revert --no-edit af0596b..<commit-cuối-của-unslop>   # af0596b = commit ngay trước khi cài
python -m pytest -q          # phải xanh
```

Cách 2 - gỡ bằng tay (khi đã có thay đổi khác chồng lên):

```bash
git rm -r .claude/skills/ctxdn-ui-ux-unslop docs/unslop
git checkout af0596b -- .claude/tong-chi-huy/registry.json .claude/hooks/dieu_phoi.py tests/harness/test_dieu_phoi.py docs/ai-command-center.html src/static/app.css
python .claude/tong-chi-huy/build_page.py
python -m pytest -q
```
Cách 2 chỉ dùng khi không thể revert: nó khôi phục `src/static/app.css` về `af0596b` và cần thêm kiểm tra
`git diff af0596b -- src/` để chắc không còn khác biệt.

Trên Windows (PowerShell) các lệnh `git` giống hệt; dùng `py -3` nếu không có `python`.
Nếu đã cài Playwright theo hướng dẫn Windows: xóa thư mục `%USERPROFILE%\ctxdn-ui-test`.

Đã thử Cách 1 trên bản sao kho trong sandbox: xem kết quả mục 4.

## 3. Kích hoạt (đã thực hiện 13/11/2026, theo duyệt của chủ đầu tư)

Các lệnh đã chạy (mỗi lệnh một lần, không có lệnh xóa):

```bash
git mv .claude/thu-nghiem/ctxdn-ui-ux-unslop .claude/skills/ctxdn-ui-ux-unslop
git mv .claude/thu-nghiem/unslop .claude/skills/ctxdn-ui-ux-unslop/unslop
git mv .claude/thu-nghiem/unslop.sha256 .claude/skills/ctxdn-ui-ux-unslop/unslop.sha256
```

Sau đó: `SKILL.md` đổi `../unslop/` thành `unslop/`; registry bỏ `trang_thai` của hai mục và đổi `duong_dan`;
test trỏ tới `.claude/skills/ctxdn-ui-ux-unslop`; `build_page.py` và pytest chạy lại.
Bản gốc `unslop` nằm lồng ở `.claude/skills/ctxdn-ui-ux-unslop/unslop/` chứ không ở `.claude/skills/unslop/`.
**Chưa kiểm chứng** Claude Code có tự nạp file lồng hai cấp này hay không; chỉ `SKILL.md` cấp một được coi là kỹ năng.

Quay lui sau kích hoạt: `git revert` dải commit kích hoạt (mục 2, Cách 1).

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

### Lần 2 - toàn dải commit (sau G3) - THẬT

| Bước | Kết quả |
|---|---|
| `git revert --no-edit af0596b..de2b2d7` (4 commit: `318f482`, `60e4150`, `a3d84ee`, `de2b2d7`) | 4 commit hoàn tác, không xung đột |
| `.claude/thu-nghiem/`, `docs/unslop/` | Đã biến mất |
| `git diff af0596b HEAD` | **Rỗng** - về đúng trạng thái trước khi cài |
| `python -m pytest` | 176 passed |
| `build_page.py --check` | Khớp |

Commit ghi kết quả này (commit thứ 5) chỉ sửa file này; khi gỡ, đưa nó vào dải: `git revert --no-edit af0596b..HEAD`.

### Lần 3 - gỡ toàn dải trên HEAD sau khi kích hoạt - THẬT

| Bước | Kết quả |
|---|---|
| `git revert --no-edit af0596b..HEAD` trên bản sao kho (gồm cả commit kích hoạt và áp CSS) | Không xung đột |
| `.claude/skills/ctxdn-ui-ux-unslop/`, `docs/unslop/` | Đã biến mất |
| `git diff af0596b HEAD` | **Rỗng** - về đúng trạng thái trước khi cài |
| `python -m pytest` | 176 passed |
| `build_page.py --check` | Khớp |

Đây là bằng chứng gỡ trên HEAD cuối cùng; lần 1 và lần 2 ở trên chỉ là lịch sử.
