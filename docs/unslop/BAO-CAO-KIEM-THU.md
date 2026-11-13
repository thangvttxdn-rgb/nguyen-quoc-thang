# Báo cáo kiểm thử

- Ngày: 13/11/2026 (10:59 UTC). Công cụ: Playwright 1.63.0 + Chromium không giao diện, Linux.
- **Đây là MÔ PHỎNG trình duyệt**, không phải iPhone Safari / Android Chrome / Windows thật.
- Đối tượng: `docs/unslop/vi-du/truoc.html` (chép từ `docs/giao-dien-mobile.html`, bản xem trước EMS có API giả lập)
  và `docs/unslop/vi-du/sau.html` (**DEMO** - áp dụng ctxdn-ui-ux-unslop, chỉ thay khối CSS, bỏ font CDN).
- Bằng chứng: `docs/unslop/kiem-thu/ket-qua.json` + 40 ảnh `truoc|sau-<cỡ>-<trạng thái>.jpg`.
- Lệnh: `node .claude/thu-nghiem/ctxdn-ui-ux-unslop/scripts/kiem_tra_giao_dien.mjs docs/unslop/vi-du/truoc.html docs/unslop/vi-du/sau.html docs/unslop/kiem-thu --kich-ban docs/unslop/vi-du/kich-ban-ems.json`

## 1. Kịch bản (giống nhau cho cả hai bản)

Đăng nhập (`thu`/`thu`, dữ liệu mẫu) → danh sách nhân sự → mở bảng trượt "Trần Thị Bình" → giao việc
"Khám đoàn tàu SE5 tại ga Đà Nẵng" → bấm "Ngừng nhân sự" → hộp xác nhận. Không bấm "Xác nhận ngừng".

## 2. Bất biến nghiệp vụ - THẬT (so mã nguồn)

| Kiểm | Kết quả |
|---|---|
| Mã `<script>` (2 khối) trùng từng byte | ĐẠT |
| Nút, ô nhập, biểu mẫu: 13 = 13, cùng `id`/`name`/`type`/`data-f` | ĐẠT |
| Toàn bộ HTML từ `<section class="login">` đến hết file | Trùng khớp (`diff` rỗng) |
| Chữ trong DOM ở từng trạng thái | Giống nhau ở 16/16 trạng thái so được; 4 trạng thái "xác nhận ngừng" không so được vì bản trước không tới được (mục 4) |
| API, CSDL, `src/` | Không đụng |

## 3. Kết quả theo cỡ màn hình - THẬT (mô phỏng)

| Cỡ | Thiết bị giả lập | Bản trước | Bản sau |
|---|---|---|---|
| 360 px | Android nhỏ | 4 nút < 44 px (Đăng xuất, 3 nút lọc 38 px); toast chặn nút "Ngừng nhân sự" | **PASS** |
| 390 px | iPhone | Như trên | **PASS** |
| 768 px | Máy tính bảng | Như trên | **PASS** |
| 1366 px | Windows | Toast chặn nút "Ngừng nhân sự" | **PASS** |

Ở cả 8 lần chạy: không tràn ngang, không chữ < 12 px, **0 lỗi JavaScript**, 0 lỗi mạng.
Kết luận bộ kiểm thử: `PASS: 8 lần chạy, 0 lỗi`.

## 4. Lỗi giao diện thật phát hiện ở bản hiện hành

**Thông báo nổi (toast) chặn nút "Ngừng nhân sự"** sau khi giao việc, ở mọi cỡ màn hình: Playwright báo
`<div id="toast"> intercepts pointer events`, bấm không được tới khi toast tắt. Bản sau sửa bằng một dòng CSS
`pointer-events: none` (không đổi JavaScript). Lưu ý: toast vẫn **hiện đè** lên nút vài giây (bấm xuyên qua được).
Đây là phát hiện trên bản xem trước; cần xác nhận trên `src/static/app.css` thật trước khi sửa (chưa sửa `src/`).

## 5. Thay đổi trình bày (DEMO)

| Lượt unslop | Thay đổi |
|---|---|
| Màu | Bỏ dải xanh-tím-hồng ở đầu trang, trang đăng nhập, nút chính, toast, avatar, băng báo dữ liệu mẫu; bỏ bóng màu. Nền xám trung tính, một màu nhấn xanh đường sắt `#1f4f9c` |
| Khoảng cách | Lưới 4 px (bỏ 13.5/14.5/12.5 px, 6/10/14 px lẻ) |
| Kiểu chữ | Bỏ chữ in hoa giãn cách ("CHI NHÁNH…", tiêu đề mục); trọng lượng 700 → 500-600; font hệ thống thay Google Fonts |
| Chi tiết | Bo góc 10 px thống nhất, bỏ hình viên thuốc; vùng bấm nút lọc, Đăng xuất 38 → 44 px |
| Giữ nguyên | Vạch màu trạm/tổ KCTX (dấu riêng), xanh lá/đỏ trạng thái, màu đỏ nút và hộp "Ngừng nhân sự", bố cục, thứ tự, mọi chữ |
| Không làm | Ảnh minh họa, emoji → biểu tượng (nút ✕ giữ nguyên vì đổi phải sửa HTML) |

## 6. Chưa kiểm thử - BLOCKED

| Hạng mục | Lý do |
|---|---|
| iPhone Safari thật, Android Chrome thật | Không có thiết bị/dịch vụ thiết bị trong phiên đám mây |
| WebKit (gần Safari) | Không cài thêm trình duyệt (cần xin phép) |
| Máy Windows thật | Phiên chạy trên Linux |
| Chế độ tối | Bản sau có bảng màu tối nhưng chưa chụp kiểm |
| CTXĐN AI OS 3.0, Quản lý tài sản, Báo cáo tự động | Không có mã nguồn trong kho |
| Bộ test Python của kho | `python -m pytest -q`: 183 passed; `ruff check .`: sạch - THẬT |
