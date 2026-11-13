# Báo cáo khảo sát Unslop

- Ngày: 13/11/2026 · Người thực hiện: Tổng chỉ huy (Claude Code, phiên đám mây) · Kết luận chung: **PARTIAL** (xem mục 6).
- Nhãn: **THẬT** (đọc, chạy trực tiếp) · **DEMO** (ví dụ mô phỏng) · **BLOCKED** (không tiếp cận được).

## 1. Môi trường - THẬT, nhưng KHÔNG phải Windows

| Hạng mục | Kết quả | Nhãn |
|---|---|---|
| Hệ điều hành | Linux 6.18 (container đám mây của Claude Code), không phải Windows | THẬT |
| Windows: phiên bản, PATH, PowerShell | Không có máy Windows trong phiên này | **BLOCKED** |
| Node.js / npm | v22.23.4 tại `/opt/node22/bin` | THẬT |
| Python | 3.x tại `/usr/local/bin/python`; dev deps cài theo `requirements-dev.txt` (bản ghim, như CI) | THẬT |
| Git | Có | THẬT |
| Playwright + Chromium | Có sẵn trong môi trường (không cài thêm) | THẬT |
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
| Bản gốc unslop | `.claude/thu-nghiem/unslop/` | Chép nguyên vẹn + `LICENSE`; mã băm ở `.claude/thu-nghiem/unslop.sha256`, có test |
| Lớp bọc CTXĐN | `.claude/thu-nghiem/ctxdn-ui-ux-unslop/SKILL.md` | Bất biến nghiệp vụ, ngoài phạm vi, quy trình tiếng Việt |
| Bộ kiểm thử | `.claude/thu-nghiem/ctxdn-ui-ux-unslop/scripts/kiem_tra_giao_dien.mjs` | 4 cỡ màn hình, so trước/sau |
| Tuyến điều phối | `giao-dien` trong registry | Hook gắn nhãn "THỬ NGHIỆM … chỉ làm trên bản sao" |

Vì sao không chép thẳng vào `.claude/skills/` như README: Claude Code tự nạp mọi thư mục ở đó, tức là
**kích hoạt thật** - trái yêu cầu "chỉ đăng ký Registry thử nghiệm". Kích hoạt: xem `PHUONG-AN-ROLLBACK.md` mục 3.

## 5. Chạy thử - DEMO trên bản sao

Áp dụng lớp bọc lên bản sao `docs/giao-dien-mobile.html` → `docs/unslop/vi-du/sau.html`, chỉ thay khối CSS.
Kết quả kiểm thử: `BAO-CAO-KIEM-THU.md`.

## 6. Kết luận theo tiêu chí XI

| Tiêu chí | Kết quả |
|---|---|
| Repository được xác minh | **ĐẠT** |
| Kiểm tra bảo mật | **ĐẠT có điều kiện** (`BAO-CAO-BAO-MAT.md`) |
| Cài đặt thử | **ĐẠT** ở vùng thử nghiệm; **chưa kích hoạt** trong `.claude/skills/` (chờ duyệt) |
| Registry thử nghiệm không xung đột | **ĐẠT** (pytest 183/183) |
| Hướng dẫn tiếng Việt | **ĐẠT** |
| Kiểm thử có bằng chứng | **PARTIAL** - Chromium mô phỏng; iPhone Safari, Android Chrome, Windows thật: BLOCKED |
| Gỡ cài đặt, rollback | **ĐẠT** (đã thử gỡ trên bản sao kho) |
| HTML xem trước | **ĐẠT** |

→ Tổng: **PARTIAL**. Thiếu: kiểm thử thiết bị thật và máy Windows; 3 dự án ngoài kho chưa thử.
