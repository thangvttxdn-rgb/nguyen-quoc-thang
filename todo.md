# KẾ HOẠCH TÁC VỤ HIỆN TẠI (todo.md)

## Mục tiêu: Hướng dẫn triển khai web app lên máy chủ IIS nội bộ

### Các bước thực hiện (Think -> Act -> Observe)
- [x] 1. `docs/TRIEN-KHAI-IIS.md`: 9 bước (chuẩn bị máy chủ → mã nguồn → tài khoản SQL → tài khoản đăng nhập → web.config → NTFS → App Pool/Site → kiểm tra → cập nhật/quay lại), bảng xử lý sự cố, giới hạn.
- [x] 2. `deploy/iis/web.config.mau` (HttpPlatformHandler, 1 tiến trình, uvicorn chỉ nghe 127.0.0.1); `web.config` thật và `logs/` vào `.gitignore`.
- [x] 3. `deploy/sql/tao-tai-khoan.sql`: tài khoản `ems_phan_cong` chỉ SELECT/INSERT/UPDATE, DENY DELETE.
- [x] 4. `requirements-prod.txt` (thêm pyodbc 5.3.0).
- [x] 5. Sửa lỗi: nhật ký thao tác (`ems.nhat_ky`) không ra log khi chạy uvicorn - gắn handler riêng; thêm test.
- [x] 6. Nghiệm thu: `pytest -q` 121/121, `ruff` sạch, XML web.config hợp lệ.

## Mục tiêu phụ: Tổng chỉ huy + AI Skills Command Center (hợp nhất)
- [x] Phân tích trùng lặp (7 cặp) - kết quả trong `registry.json` mục `trung_lap` và trên trang.
- [x] `.claude/tong-chi-huy/registry.json`: nguồn duy nhất (39 mục, 14 tuyến, 5 cảnh báo); mở khóa "Registry CTXĐN: BLOCKED" của hồ sơ rà soát.
- [x] Hook `UserPromptSubmit` `.claude/hooks/dieu_phoi.py` - tự phân tích và giao việc mỗi lần gõ chat; đăng ký trong `.claude/settings.local.json`.
- [x] Kỹ năng `.claude/skills/tong-chi-huy`, tác tử `.claude/agents/to-phan-bien.md`.
- [x] Trang `docs/ai-command-center.html` sinh từ registry (`build_page.py`); bảng định tuyến, bảng trùng lặp.
- [x] Nghiệm thu: `python -m pytest -q` 145/145, `ruff check .` sạch.
- [ ] Hồ sơ rà soát Knowledge Work (nhánh `claude/anthropic-knowledge-work-review-em31y1`) chưa gộp vào nhánh này - chờ chủ đầu tư quyết (Đề xuất 7).
- [ ] Chạy thử hook trên máy Windows: lệnh `python3` có thể không có, cần đổi thành `py -3` hoặc `python`.

## Mục tiêu phụ: Thêm GitHub Spec Kit (v1.4.0, MIT)
- [x] G0: khảo sát mã nguồn (commit `0019fa1`), chạy thử `specify init` trên bản sao - chỉ thêm file, không ghi đè; rà script: không gọi mạng, không xóa, không tự tạo nhánh.
- [x] Cài: `.specify/` + 9 kỹ năng `.claude/skills/speckit-*` (script Python để chạy được trên Windows).
- [x] Gỡ trùng: hiến pháp chỉ trỏ về AGENTS.md; tasks.md/todo.md chia cấp; /speckit-plan thay tác tử Plan cho tính năng mới; analyze/to-phan-bien chia phạm vi.
- [x] Registry: 48 mục, 12 kết luận trùng lặp; tuyến "Tính năng mới" giao cho /speckit-specify. `.specify` loại khỏi ruff.
- [x] Sửa hook: "gửi" quá rộng (cảnh báo nhầm khi chia sẻ link); "spec" khớp nhầm URL.
- [x] Nghiệm thu: `python -m pytest -q` 148/148, `ruff check .` sạch.
- [ ] Thử luồng /speckit-specify → /speckit-implement với một tính năng thật (đề xuất: lịch sử phân công theo nhân sự).

## Mục tiêu phụ: Công cụ làm video (video "7 repo GitHub làm video")
- [x] G0: kiểm chứng 7 kho qua GitHub (sao, giấy phép đều THẬT); đối chiếu G0 lemo-opuscar và kết nối HyperFrames sẵn có.
- [x] Chọn HyperFrames v0.9.37 (commit `e8e1177`, tạm thời); cài 3 kỹ năng lõi (chép file, không chạy mã). Biên bản: `docs/G0-cong-cu-video.md`.
- [x] G3 Tổ 2: **FAIL** 11 điểm (chưa ghim trong file kỹ năng, beacon/feedback gửi dữ liệu, dẫn sang media-use, từ khóa "render" quá rộng…) → đã xử lý: `guard.py` chặn lệnh không ghim và lệnh gửi dữ liệu (+19 test), `lop_phu_hyperframes.py` ghim 278 chỗ và chèn khối luật, `trang_thai: chua-kiem-thu`, thu hẹp từ khóa, `.gitignore`.
- [x] Không cài: Remotion (giấy phép thu phí tổ chức >3 người), Manim, GSAP/three.js riêng, FFmpeg (đã có), slideshow (trùng pptx). BLOCKED: media-use, Blender MCP.
- [x] Registry 53 mục, 15 tuyến, 20 kết luận trùng lặp; tuyến "Làm video"; `.gitignore` cho `video/`.
- [ ] Đề xuất (cấu hình, chờ duyệt): `HYPERFRAMES_NO_TELEMETRY=1` trong `env` của `.claude/settings.local.json`.
- [ ] **G2 BLOCKED**: chạy thử `npx hyperframes@0.9.37` bị bộ phân loại tự động chặn (mã tải từ ngoài). Cần chủ đầu tư cho phép lệnh `npx hyperframes@0.9.37` rồi render thử 1 clip 10 giây.

## Mục tiêu phụ: Floorplan (sơ đồ mã nguồn, v0.8.0, MIT)
- [x] G0: rà kho `haydenschmitty/floorplan` commit `5e3eaac`: 0 thư viện phụ thuộc, Node 18+; máy chủ xem chỉ nghe 127.0.0.1 có token; Ask bar gọi `claude -p` chỉ đọc. Gọi ra ngoài duy nhất: waitlist (gửi email khi bấm "Notify me"; ô email tự điền từ tài khoản Claude). Test gốc 287/287 xanh.
- [x] Cài: chép `skills/floorplan` vào `.claude/skills/floorplan` (+LICENSE, bỏ file Codex); `/floorplan/` vào `.gitignore`.
- [x] Registry: mục `floorplan` (`chua-kiem-thu`), tuyến "Sơ đồ mã nguồn", cảnh báo, 2 kết luận trùng lặp (với /speckit-plan, Explore).
- [x] G2: `scan.mjs` chạy trên bản sao kho - nhận 10 route FastAPI, 14 lời gọi frontend→API.
- [x] Đã đặt `FLOORPLAN_NO_PROMPTS=1` trong `env` của `.claude/settings.local.json` (chủ đầu tư duyệt 2026-11-13); có hiệu lực từ phiên Claude Code sau.
- [x] Dựng bản đồ EMS (cách tiết kiệm: bỏ `.claude/skills`, `.specify`, `docs`; tự viết mô tả, không gọi tác tử phụ): 27/27 file, 10/10 API, Health 0 nghiêm trọng, 1 nhẹ (`GET /api/info` không cần đăng nhập - chỉ trả phiên bản, chấp nhận được). Bản đồ nằm ở `floorplan/` (không commit), mất khi container bị thu hồi; chạy lại `/floorplan` trên máy để giữ.

### Việc còn treo
- [ ] Làm theo tài liệu trên máy chủ thật (người quản trị).
- [ ] (Tùy chọn) Đăng nhập SQL bằng Windows Authentication thay mật khẩu trong web.config - cần sửa code kết nối.
- [ ] Đối chiếu schema thật; thử với SQL Server thật.
