# G0 · Công cụ làm video ("7 repo GitHub làm video")

- Ngày: 12/11/2026 · Đầu vào: video Facebook do chủ đầu tư gửi (99 giây, 7 kho GitHub).
- Nhãn: **THẬT** (tra/đọc trực tiếp, có nguồn) · **CẦN CĂN CỨ** · **BLOCKED**.
- Quyết định lưu ở `.claude/tong-chi-huy/registry.json` (`muc` nhóm Video, `trung_lap`, `nguon_ngoai`).

## 1. Kiểm chứng 7 kho - THẬT

Nguồn: GitHub Search API (`gh api search/repositories`), tra 12/11/2026. Số sao trong video khớp.

| Kho | Sao | Giấy phép (GitHub) | Tạo | Kết luận |
|---|---|---|---|---|
| heygen-com/hyperframes | 83.062 | Apache-2.0 | 03/2026 | **Cài** 3 kỹ năng lõi, v0.9.37 |
| remotion-dev/remotion | 72.622 | Riêng (NOASSERTION) | 2020 | Không cài - xem mục 2 |
| mrdoob/three.js | 118.212 | MIT | 2010 | Không cài riêng (HyperFrames có khối 3D) |
| greensock/GSAP | 30.501 | Riêng | 2012 | Không cài riêng (HyperFrames dùng GSAP) |
| 3b1b/manim | 96.429 | MIT | 2015 | Không cài (video toán học; cần LaTeX, Cairo) |
| ahujasid/mcp-for-blender | 34.092 | MIT | - | **BLOCKED** - chạy Python tùy ý trong Blender, cần máy trạm GPU |
| FFmpeg/FFmpeg | 67.096 | LGPL/GPL | 2011 | Không cài - đã có `/usr/bin/ffmpeg` |

## 2. Giấy phép Remotion - THẬT

`LICENSE.md` của remotion-dev/remotion, commit `eeb428f` (11/11/2026), mục *Free License*: miễn phí nếu là
"an individual", "a for-profit organization with up to 3 employees", hoặc "a non-profit or not-for-profit
organization". Chi nhánh thuộc công ty cổ phần (vì lợi nhuận, trên 3 người) → cần *Company License*.

## 3. HyperFrames v0.9.37 - THẬT

- Tag `v0.9.37`, commit `e8e1177ad609127edc2de390369ceb9a38fd6ba5` (12/11/2026), Apache-2.0.
- Cài: `hyperframes`, `hyperframes-cli`, `hyperframes-registry` (chép file, **không chạy mã**).
- Không cài: `media-use` (BLOCKED: HeyGen, ElevenLabs, OpenAI, Gemini), `slideshow` (trùng pptx),
  `remotion-to-hyperframes`, `reverse-any-video` (dựng lại video người khác), `figma`, `style-sampling`.
- Số "khoảng 450 khối" của `hyperframes-registry` là lời upstream - **CẦN CĂN CỨ** (chưa đếm).

## 4. Đối chiếu lemo-opuscar

Căn cứ: `docs/G0-lemo-opuscar.md` trên nhánh `docs/g0-lemo-opuscar` (chưa gộp vào nhánh này), mục 4.2:
R1 tự `reset --hard` theo `main`, R4 dặn tác tử tự cài gói không hỏi, R6 không chạy trong kho EMS.
HyperFrames ghim được tag và không có R1/R4, nhưng có đo lường và lệnh đám mây (mục 5).
**Chọn HyperFrames là tạm thời**, chờ G2 render thử.

## 5. Phản biện G3 (Tổ 2) - FAIL, đã xử lý

| Điểm Tổ 2 | Xử lý |
|---|---|
| Kỹ năng vẫn dặn `npx hyperframes` không ghim | `lop_phu_hyperframes.py` ghim 278 chỗ về `@0.9.37`; `guard.py` chặn bản không ghim |
| "Usage beacon", `feedback`, `usage` gửi dữ liệu ra HeyGen | `guard.py` chặn `events, feedback, usage, auth, share, publish, cloud, lambda, cloudrun, capture, telemetry enable`; khối luật đầu mỗi SKILL.md |
| Kỹ năng dẫn sang `/media-use` | Khối luật: media-use BLOCKED, dùng tài nguyên nội bộ |
| `browser ensure`, `doctor`, `upgrade`, `--on-device` tải thêm | `guard.py` hỏi trước |
| `bake-basemap.mjs`, CDN, `locate.mjs auto` (khóa Gemini trong URL) | Cảnh báo registry + khối luật |
| Thiếu nguồn giấy phép, số liệu | Biên bản này |
| Chưa chạy thử mà đã là công cụ chính | `trang_thai: chua-kiem-thu` |
| Từ khóa `render`, `clip`, `npx` quá rộng | Bỏ; thêm câu phản chứng vào test |
| `.gitignore` thiếu | Thêm `.hyperframes/`, `*.mov`, `*.webm`, `frames/`, `snapshots/` |
| Phần ngoài phạm vi (Framey, publish, AWS/GCP) | Khối luật ghi "ngoài phạm vi" |

## 6. Còn BLOCKED

- **G2 render thử**: `npx hyperframes@0.9.37` bị bộ phân loại tự động của phiên đám mây chặn (mã tải từ
  ngoài). Cần chủ đầu tư cho phép, rồi render một clip 10 giây.
- Đề xuất (chưa làm, là sửa cấu hình - phải duyệt): đặt `HYPERFRAMES_NO_TELEMETRY=1` trong `env` của
  `.claude/settings.local.json` để tắt đo lường cho mọi lệnh.
