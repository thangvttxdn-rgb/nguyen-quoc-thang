# Báo cáo khảo sát Unslop

- Ngày: 13/11/2026 · Người thực hiện: Tổng chỉ huy (Claude Code, phiên đám mây) · Kết luận chung: **PARTIAL** (xem mục 6).
- Nhãn: **THẬT** (đọc, chạy trực tiếp) · **DEMO** (ví dụ mô phỏng) · **BLOCKED** (không tiếp cận được).

## 1. Môi trường - THẬT, nhưng KHÔNG phải Windows

| Hạng mục | Kết quả | Nhãn |
|---|---|---|
| Hệ điều hành | Linux 6.18 (container đám mây của Claude Code), không phải Windows | THẬT |
| Windows: phiên bản, PATH, PowerShell | Không có máy Windows trong phiên này | **BLOCKED** |
| Node.js / npm | v22.23.4 tại `/opt/node22/bin` | THẬT |
| Python | 3.13 tại `/usr/local/bin/python`; dev deps cài theo `requirements-dev.txt` (bản ghim, như CI) | THẬT |
| Git | Có | THẬT |
| Playwright + Chromium | 1.63.0 + Chromium 153, có sẵn trong môi trường (không cài thêm) | THẬT |
| FFmpeg | `/usr/bin/ffmpeg` | THẬT |
| Thư mục Command Center | `.claude/tong-chi-huy/registry.json` (53 mục trước khi thêm) + `docs/ai-command-center.html` | THẬT |
| Unslop hoặc kỹ năng tương đương | Chưa có. Gần nhất: `artifact-design` (có sẵn, cho trang Artifact), `frontend-design` (không có trong kho) | THẬT |

Dự án thật tìm được: kho EMS (`src/templates`, `src/static`) và bản xem trước `docs/giao-dien-mobile.html`.
CTXĐN AI OS 3.0, Quản lý tài sản, Báo cáo tự động: **không có trong kho này** - BLOCKED, chưa thử.

## 2. Kho nguồn - THẬT

| Mục | Giá trị |
|---|---|
| URL | https://github.com/heydamir/unslop |
| Commit | `97daa3eb365670ea3f87ed85356cbfcee18105a5` (09/11/2026, merge PR #19). Chưa có tag phiên bản |
| Giấy phép | CC BY 4.0 (file `LICENSE`, `CITATION.cff`) - được dùng, sửa, thương mại; **bắt buộc ghi công** Damir Sokolovsky và dẫn link kho |
| Quy mô | 23 file, 1,6 MB; phần cài: 15 file, 1,5 MB (5 ảnh `.webp` tham khảo) |

## 3. Unslop là gì - THẬT

**Kỹ năng (Agent Skill) dạng Markdown**, không phải plugin hay chương trình độc lập. Thành phần:

| File | Vai trò |
|---|---|
| `SKILL.md` (235 dòng) | Quy trình: nhìn màn hình → rà dấu hiệu → chọn mức sửa → hướng thiết kế 5 dòng (dừng hỏi) → 9 lượt sửa → kiểm → báo cáo |
| `references/signs.md`, `tokens.md`, `visuals.md`, `effects.md`, `refs.md` | Danh mục dấu hiệu "giao diện kiểu AI", thang khoảng cách/màu/chữ, cách làm ảnh minh họa |
| `scripts/snapshot.mjs` | Tùy chọn: lưu trang (URL hoặc file) thành một file HTML, cần Playwright |
| `scripts/story.mjs` | Tùy chọn: dựng video "trước → sau" ~10 giây, cần Playwright + FFmpeg |
| `agents/openai.yaml` | Khai báo cho Codex, Claude Code không dùng |

Cách cài chính thức (README): `git clone` rồi `cp -r unslop/skills/unslop ~/.claude/skills/` (toàn cục) hoặc
`.claude/skills/` (một dự án). Không có bước build, không có `npm install` bắt buộc.

## 4. Cách tích hợp đã chọn

Không tạo hệ thống quản lý thứ hai: đăng ký vào **registry duy nhất** `.claude/tong-chi-huy/registry.json`
với trạng thái mới `thu-nghiem`.

| Thành phần | Vị trí | Ghi chú |
|---|---|---|
| Bản gốc unslop | `.claude/skills/ctxdn-ui-ux-unslop/unslop/` | Chép nguyên vẹn + `LICENSE`; mã băm ở `.claude/skills/ctxdn-ui-ux-unslop/unslop.sha256`, có test |
| Lớp bọc CTXĐN | `.claude/skills/ctxdn-ui-ux-unslop/SKILL.md` | Bất biến nghiệp vụ, ngoài phạm vi, quy trình tiếng Việt |
| Bộ kiểm thử | `.claude/skills/ctxdn-ui-ux-unslop/scripts/kiem_tra_giao_dien.mjs` | 4 cỡ màn hình, so trước/sau |
| Tuyến điều phối | `giao-dien` trong registry | Hook gắn nhãn "THỬ NGHIỆM … chỉ làm trên bản sao" |

Vì sao không chép thẳng vào `.claude/skills/` như README: Claude Code tự nạp mọi thư mục ở đó, tức là
**kích hoạt thật**. Lúc đầu chưa kích hoạt; sau khi chủ đầu tư duyệt, đã chuyển vào `.claude/skills/` (`PHUONG-AN-ROLLBACK.md` mục 3).

## 5. Chạy thử - DEMO trên bản sao

Áp dụng lớp bọc lên bản sao `docs/giao-dien-mobile.html` → `docs/unslop/vi-du/sau.html`: thay khối CSS, bỏ thẻ
font Google; cả bản trước và bản sau được thêm thẻ viewport như template thật để đo đúng khổ điện thoại.
Kết quả kiểm thử: `BAO-CAO-KIEM-THU.md`.

## 6. Kết luận theo tiêu chí XI

| Tiêu chí | Kết quả |
|---|---|
| Repository được xác minh | **ĐẠT** |
| Kiểm tra bảo mật | **ĐẠT có điều kiện** (`BAO-CAO-BAO-MAT.md`) |
| Cài đặt thử | **ĐẠT**; đã kích hoạt trong `.claude/skills/` sau khi chủ đầu tư duyệt (13/11/2026) |
| Registry thử nghiệm không xung đột | **ĐẠT** (`python -m pytest` 185 passed, `ruff` sạch) |
| Hướng dẫn tiếng Việt | **PARTIAL** - phần Windows chưa chạy trên máy Windows |
| Kiểm thử có bằng chứng | **PARTIAL** - Chromium mô phỏng (lần đầu không hợp lệ do thiếu viewport, đã chạy lại); iPhone Safari, Android Chrome, Windows thật: BLOCKED |
| Gỡ cài đặt, rollback | **ĐẠT** (thử `git revert` toàn dải commit trên bản sao kho - `PHUONG-AN-ROLLBACK.md` mục 4) |
| HTML xem trước | **ĐẠT** |

→ Tổng: **PARTIAL**. Thiếu: kiểm thử thiết bị thật và máy Windows; hướng dẫn Windows chưa chạy thử; 3 dự án ngoài kho chưa thử.

## 7. Phản biện G3

- `/code-review`: 10 điểm về script kiểm thử và hook - đã sửa hết.
- Tổ 2 (`to-phan-bien`) lần 1: **FAIL**, 15 điểm. Lần 2: 15 điểm đã sửa đúng, còn 7 lỗi văn bản (số trạng thái so chữ 18/20, nguồn của nhận định toast, số rủi ro, số test, mô tả "chỉ CSS", toast đè đầu trang chưa kiểm, màu tối băng dữ liệu mẫu) - đã sửa hết. Đáng kể nhất ở lần 1:
  - Kiểm thử 360/390 px lần đầu đo sai khổ (thiếu viewport). Đã chạy lại. Toast đè hộp xác nhận chỉ đo được trên biến thể toast-ở-đáy; với bản hiện hành là suy ra, CẦN CĂN CỨ.
  - Lớp bọc bổ sung các ngoại lệ với bản gốc: emoji cảnh báo, màu ngữ nghĩa, dữ liệu mẫu, cột hẹp, công cụ thiết kế, lucide.
  - Bỏ bản gốc khỏi danh sách hỗ trợ của tuyến.
  - Nhãn "giữ nguyên màu" sửa thành bảng mã cũ → mới.
  - Rollback thử lại với toàn dải commit.
  - Hướng dẫn Windows: `NODE_PATH` thành bước bắt buộc.
