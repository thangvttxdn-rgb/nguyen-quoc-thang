# Báo cáo kiểm thử

- Lần chạy hiện hành: xem `ngay` và `phien_ban` trong `docs/unslop/kiem-thu/ket-qua.json`
  (Playwright 1.63.0, Chromium 153.0.8010.12, Linux, không giao diện).
- **Đây là MÔ PHỎNG trình duyệt**, không phải iPhone Safari / Android Chrome / Windows thật.
- Đối tượng: `docs/unslop/vi-du/truoc.html` (chép từ `docs/giao-dien-mobile.html`, bản xem trước EMS có API giả lập)
  và `docs/unslop/vi-du/sau.html` (**DEMO** - áp dụng ctxdn-ui-ux-unslop).
- Bằng chứng: `ket-qua.json` + 40 ảnh `truoc|sau-<cỡ>-<trạng thái>.jpg` cùng thư mục.
- Lệnh: `node .claude/thu-nghiem/ctxdn-ui-ux-unslop/scripts/kiem_tra_giao_dien.mjs docs/unslop/vi-du/truoc.html docs/unslop/vi-du/sau.html docs/unslop/kiem-thu --kich-ban docs/unslop/vi-du/kich-ban-ems.json`

## 0. Lần chạy đầu bị hủy (G3 phát hiện)

Lần chạy 10:59 UTC báo PASS nhưng **không hợp lệ** ở 360/390/768 px: bản xem trước thiếu
`<meta name="viewport">` (trang Artifact được máy chủ tự chèn), nên Chromium dựng trang ở khổ 980 px rồi thu nhỏ
(`rong_noi_dung: 980`). Đã xử lý:
- Thêm vào **cả hai** bản đúng thẻ viewport của template thật (`src/templates/index.html:5`).
- Script nay FAIL nếu bản sau thiếu viewport, và ghi `rong_bo_cuc` từng lần đo.
- Chạy lại toàn bộ; kết quả dưới đây là lần chạy mới.

## 1. Kịch bản (giống nhau cho cả hai bản)

Đăng nhập (`thu`/`thu`, dữ liệu mẫu) → danh sách nhân sự → mở bảng trượt "Trần Thị Bình" → giao việc
"Khám đoàn tàu SE5 tại ga Đà Nẵng" → bấm "Ngừng nhân sự" → hộp xác nhận. Không bấm "Xác nhận ngừng".

## 2. Bất biến nghiệp vụ - THẬT (so mã nguồn)

| Kiểm | Kết quả |
|---|---|
| Khung HTML (mọi thẻ, mọi thuộc tính trừ `class`/`style`, kể cả mọi `data-*`, `onclick`, `action`) | Trùng khớp |
| Mã `<script>` (2 khối) | Trùng từng byte |
| Nút, ô nhập, biểu mẫu | 13 = 13, cùng `id`/`name`/`type` |
| Phần đầu file | **Có sửa ngoài CSS**: bỏ thẻ `<link>` Google Fonts, đổi một dòng chú thích. Từ `<section class="login">` đến hết file trùng khớp |
| Chữ trong DOM | Giống nhau ở 18/20 trạng thái. 2 trạng thái "xác nhận ngừng" ở 360 và 390 px **không so được** vì bản trước không bấm tới được (mục 4); hai trạng thái này chỉ dựa vào việc khung HTML và `<script>` trùng khớp |
| API, CSDL, `src/` | Không đụng |

## 3. Kết quả theo cỡ màn hình - THẬT (mô phỏng), bố cục dựng đúng khổ

| Cỡ | Thiết bị giả lập | Bản trước | Bản sau |
|---|---|---|---|
| 360 px | Android nhỏ | 4 nút < 44 px; toast đè nút "Ngừng nhân sự" và chặn bấm quá 3 giây | **PASS** |
| 390 px | iPhone | Như 360 px | **PASS** |
| 768 px | Máy tính bảng | 4 nút < 44 px; toast đè nút "Ngừng nhân sự" (bấm được sau khi chờ) | **PASS** |
| 1366 px | Windows | Toast đè nút "Ngừng nhân sự" (bấm được sau khi chờ) | **PASS** |

Bản sau ở cả 4 cỡ: không tràn ngang, không chữ < 12 px, không nút < 44 px, không nút bị che hoặc bị đè,
0 lỗi JavaScript, 0 lỗi tải tài nguyên. Kết luận script: `PASS: 8 lần chạy, 0 lỗi`.

## 4. Lỗi giao diện thật ở bản hiện hành

1. **Toast đè nút "Ngừng nhân sự"** sau khi giao việc, ở cả 4 cỡ (THẬT, `ket-qua.json` trạng thái 4). Ở 360 và
   390 px còn **chặn bấm**: Playwright báo `<div id="toast"> intercepts pointer events`, quá 3 giây vẫn không bấm được.
2. **Toast ở đáy màn hình đè hai nút "Huỷ" / "Xác nhận ngừng"** của hộp xác nhận, ở cả 4 cỡ. Đo trên biến thể
   `vi-du/sau-toast-day.html` (bản sau, toast để ở đáy như bản hiện hành, cho bấm xuyên): `kiem-thu/toast-day/ket-qua.json`,
   ảnh `kiem-thu/toast-day/sau-360-5-xac-nhan-ngung.jpg`. Trên **bản hiện hành** chưa đo trực tiếp được (bấm bị chặn
   trước khi hộp mở) - **CẦN CĂN CỨ**: khả năng cao xảy ra nếu người dùng bấm "Ngừng nhân sự" ngay khi toast vừa tắt.
3. **Nút lọc và nút Đăng xuất cao 38 px**, dưới mức 44 px của màn hình cảm ứng (360/390/768 px).

Bản sau xử lý bằng CSS: toast chuyển lên đầu màn hình và có `pointer-events: none`; nút cao 44 px.
Đây là phát hiện trên bản xem trước; cần đối chiếu `src/static/app.css` thật trước khi sửa (chưa sửa `src/`).

## 5. Thay đổi trình bày (DEMO)

| Lượt unslop | Thay đổi |
|---|---|
| Màu | Bỏ dải xanh-tím-hồng ở đầu trang, trang đăng nhập, nút chính, toast, avatar; bỏ bóng màu. Nền xám trung tính, một màu nhấn xanh `#1f4f9c` |
| Khoảng cách | Lưới 4 px (bỏ 13.5/14.5/12.5 px, 6/10/14 px lẻ) |
| Kiểu chữ | Bỏ chữ in hoa giãn cách ("CHI NHÁNH…", tiêu đề mục); trọng lượng 700 → 500-600; font hệ thống thay Google Fonts |
| Chi tiết | Bo góc 10 px thống nhất; vùng bấm nút lọc, Đăng xuất 38 → 44 px; toast lên đầu màn hình |
| Giữ nguyên | Vạch màu trạm/tổ KCTX, bố cục, thứ tự, mọi chữ, nút ✕ |

**Màu ngữ nghĩa: giữ họ màu, đã đổi mã** (không phải "giữ nguyên"):

| Biến | Bản trước (sáng / tối) | Bản sau (sáng / tối) |
|---|---|---|
| `--on` đang làm | `#047857` / `#34d399` | `#1d6b45` / `#7fcfa3` |
| `--off` đã ngừng, nút Ngừng, hộp xác nhận | `#e11d48` / `#fb7185` | `#b42318` / `#f19a90` |
| Băng "dữ liệu mẫu" | Nền dải cam-hồng | Nền cam phẳng `#fdebd9`, viền trái `#c2410c`; tối: `#3a2414`, viền `#fb923c` (giữ độ nổi) |

Đổi mã màu ngữ nghĩa cần chủ đầu tư duyệt trước khi áp vào EMS thật.

## 6. Chưa kiểm thử - BLOCKED

| Hạng mục | Lý do |
|---|---|
| iPhone Safari thật, Android Chrome thật | Không có thiết bị/dịch vụ thiết bị trong phiên đám mây |
| WebKit (gần Safari) | Không cài thêm trình duyệt (cần xin phép) |
| Máy Windows thật | Phiên chạy trên Linux |
| Chế độ tối | Bản sau có bảng màu tối nhưng chưa chụp kiểm |
| Toast ở đầu màn hình khi bảng trượt đã đóng | Sau "Đã ngừng…" / "Đã kích hoạt lại…" toast có thể đè tiêu đề và nút "Đăng xuất" vài giây (bấm xuyên được, che chữ). Kịch bản chưa có bước chụp trạng thái này |
| CTXĐN AI OS 3.0, Quản lý tài sản, Báo cáo tự động | Không có mã nguồn trong kho |
