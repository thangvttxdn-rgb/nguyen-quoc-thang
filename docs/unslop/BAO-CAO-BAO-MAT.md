# Báo cáo bảo mật Unslop

Phạm vi: toàn bộ 23 file ở commit `97daa3e`. Cách làm: đọc hết `SKILL.md`, `README.md`, 5 file `references/*.md`,
2 script, 2 test; dò mẫu nguy hiểm bằng `grep`; dò ký tự ẩn (zero-width, đảo chiều bidi, BOM) bằng Python `-I`.
**Không chạy script nào của kho.** Kết luận: **ĐẠT có điều kiện**.

## 1. Kết quả dò - THẬT

| Nguy cơ | Kết quả |
|---|---|
| Tải và chạy mã từ xa (`curl \| sh`, `npx` không ghim, `eval`, `Function()`) | Không có |
| Gọi mạng trong script | `snapshot.mjs`: chỉ mở URL/file **người dùng đưa vào** và tải CSS/ảnh của chính trang đó. `story.mjs`: máy chủ HTTP cục bộ `127.0.0.1`, cổng ngẫu nhiên, chặn truy cập ra ngoài thư mục gốc (`normalize` + `startsWith(root)`) |
| Chạy chương trình con | `story.mjs` gọi `ffmpeg` qua `execFileSync` (mảng tham số, không qua shell) |
| Xóa file | `story.mjs` `rmSync` chỉ thư mục tạm `.story-frames` cạnh file story |
| Biến môi trường | Chỉ đọc `CHROME_PATH`; không đọc khóa, token, `.env` |
| Đo lường / gửi dữ liệu (telemetry, beacon, feedback) | Không có |
| Prompt injection, ký tự ẩn | Không có ký tự ẩn. Không có câu lệnh bảo tác tử bỏ qua luật, tự cài gói hay gửi dữ liệu |
| Quyền ghi | Sửa file giao diện của dự án (đúng chức năng); script ghi file đầu ra người dùng chỉ định |

## 2. Rủi ro còn lại và cách chặn

| # | Rủi ro | Mức | Xử lý |
|---|---|---|---|
| R1 | `references/visuals.md` gợi ý kết nối dịch vụ **sinh ảnh trả phí** (fal, Replicate, OpenAI images, Higgsfield) qua MCP | Trung bình (chi phí, đưa dữ liệu ra ngoài) | Lớp bọc mục 2 cấm. Bản gốc có dặn "hỏi trước mỗi lần sinh ảnh" |
| R2 | Lượt "Copy" của bản gốc sửa câu chữ, bỏ emoji, dấu chấm than - có thể chạm **nội dung cảnh báo an toàn**, nhãn nghiệp vụ | Cao với phần mềm ngành | Lớp bọc mục 1: chỉ sửa chữ trang trí; bộ kiểm thử so chữ trong DOM trước/sau, khác là FAIL |
| R3 | `snapshot.mjs <URL>` mở trang bất kỳ bằng trình duyệt | Thấp | Lớp bọc: chỉ file cục bộ hoặc địa chỉ nội bộ được giao |
| R4 | Ví dụ `examples/*.html` nạp `cdn.tailwindcss.com` và Google Fonts | Thấp | Không chép `examples/` vào kho |
| R5 | Kho chưa có tag; `main` có thể đổi | Trung bình | Ghim commit trong registry; mã băm từng file + test `test_ban_goc_unslop_khong_bi_sua` |
| R6 | Bản gốc tự kích hoạt khi người dùng nói "polish, clean up, redesign" | Trung bình | Không đặt ở `.claude/skills/`; chỉ gọi qua lớp bọc |
| R7 | README quảng cáo dịch vụ thuê thiết kế ("Hire the unslopper") | Thấp | Lớp bọc ghi bỏ qua |
| R8 | Giấy phép CC BY 4.0 bắt buộc ghi công | Pháp lý | Giữ `LICENSE`, dòng ghi công trong các file; video kể chuyện phải có dòng `unslop by @heydamir` |
| R9 | Kiểm thử Windows: script tìm Chrome theo đường dẫn macOS/Linux | Thấp | Trên Windows Playwright dùng Chromium đi kèm; **chưa thử** (BLOCKED) |

## 3. Quyền cần có khi chạy

| Việc | Quyền |
|---|---|
| Đọc kỹ năng, sửa CSS bản sao | Không cần quyền quản trị |
| `kiem_tra_giao_dien.mjs` | Node.js + Playwright (đã có trong môi trường đám mây; trên Windows cần `npm install -D playwright` - **phải xin phép**, AGENTS.md mục 3) |
| `story.mjs` (video) | Thêm FFmpeg; không cần cho việc giao diện thường ngày |
