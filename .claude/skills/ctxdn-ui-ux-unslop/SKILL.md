---
name: ctxdn-ui-ux-unslop
description: Nâng cấp giao diện phần mềm nội bộ CTXĐN (EMS, AI OS 3.0, quản lý tài sản, báo cáo tự động) theo phương pháp Unslop - rà dấu hiệu giao diện "kiểu AI", chuẩn hóa khoảng cách, màu, chữ, biểu tượng, tối ưu điện thoại, kiểm thử 360/390/768/1366 px và xuất bản so sánh trước/sau. CHỈ sửa lớp trình bày (CSS, chữ hiển thị không thuộc nghiệp vụ), không đụng API, CSDL, phân quyền, chức năng nút, cảnh báo an toàn. Dùng khi được giao "nâng cấp giao diện", "làm đẹp giao diện", "unslop", "chuẩn hóa UI".
license: CC-BY-4.0 (phần dẫn xuất từ unslop của Damir Sokolovsky, https://github.com/heydamir/unslop)
---

# ctxdn-ui-ux-unslop

Lớp CTXĐN bọc ngoài kỹ năng **unslop** (bản gốc nguyên vẹn tại `unslop/`, commit
`97daa3eb365670ea3f87ed85356cbfcee18105a5`, CC BY 4.0 - giữ ghi công Damir Sokolovsky, @heydamir).
Khi luật dưới đây khác bản gốc, **luật dưới đây thắng**.

Đã kích hoạt ngày 13/11/2026 (`.claude/skills/`). Việc sửa mã vẫn chỉ làm trên **bản sao trong sandbox** (scratchpad hoặc `docs/unslop/vi-du/`),
không sửa thẳng `src/` khi chưa có nhiệm vụ cụ thể được chủ đầu tư giao.

## 1. Bất biến nghiệp vụ (không bao giờ được đổi)

| Không đổi | Cách kiểm |
|---|---|
| API, backend, CSDL, schema, thuật toán, quy trình xử lý toa xe | Chỉ sửa `*.css`, khối `<style>`, thuộc tính `class`/`style` |
| Phân quyền, đăng nhập | Không đổi `id`, `name`, `type`, `autocomplete`, `required` của ô nhập |
| Chức năng nút, cơ chế xuất nhập dữ liệu | Khung HTML (mọi thẻ, thuộc tính trừ `class`/`style`, mọi `<script>`) trùng khớp - script kiểm thử so tự động |
| Nội dung cảnh báo an toàn | Giữ nguyên chữ **và cả emoji** (⚠️, ⛔…), màu đỏ/cam, mức nổi bật. Ngoại lệ với bản gốc `SKILL.md` dòng 96-100 (emoji → biểu tượng màu chữ phụ) và dòng 224 ("No emoji left") |
| Màu ngữ nghĩa (đang làm / đã ngừng / cảnh báo / dữ liệu mẫu) | Giữ họ màu và độ nổi; được chỉnh mã màu cho đủ tương phản, ghi bảng mã cũ → mới trong báo cáo. Ngoại lệ với bản gốc dòng 88 ("toned down") |
| Dữ liệu mẫu, nhãn DEMO | Không thay dữ liệu mẫu bằng dữ liệu "trông thật" (ngoại lệ với bản gốc dòng 112, 212); giữ nguyên nhãn "dữ liệu mẫu" |
| Cấu trúc dữ liệu, JavaScript nghiệp vụ | Mã `<script>` phải trùng khớp từng byte với bản trước |
| Nhận diện phần mềm | Giữ tên phần mềm, logo thật, màu thương hiệu thật (nếu có) |

Bản gốc unslop cho phép sửa câu chữ (pass "Copy"). Ở CTXĐN: mặc định **không sửa chữ** (script so chữ trong
DOM, khác là FAIL). Chỉ sửa chữ trang trí (tiêu đề chào hỏi, dấu chấm than) khi chủ đầu tư duyệt từng câu; không
bao giờ sửa nhãn trường, tên nút, thông báo lỗi, thuật ngữ ngành (toa xe, KCTX, trạm…).

Bố cục: phần mềm nội bộ dùng trên điện thoại được giữ cột hẹp (vd. EMS 640 px) - ngoại lệ với bản gốc dòng 128.

## 2. Ngoài phạm vi (bản gốc có, CTXĐN không dùng)

- **Sinh ảnh, công cụ thiết kế bên ngoài** (fal, Replicate, OpenAI images, Higgsfield, và mọi "design tool" như
  Adobe, Canva, Figma đang kết nối - `references/visuals.md` dòng 54, 60): không gọi trong kỹ năng này. Phần mềm
  nội bộ không cần ảnh minh họa; để trống và ghi đề xuất.
- **Bộ biểu tượng** (bản gốc gợi ý lucide): chỉ dùng biểu tượng đã có trong dự án hoặc SVG viết tay nội tuyến;
  không tải từ CDN, không `npm install` (cài thư viện phải xin phép).
- **Font từ CDN**: máy chủ nội bộ có thể không ra Internet. Dùng font hệ thống hỗ trợ tiếng Việt
  (`"Segoe UI", Roboto, system-ui, sans-serif`); font web chỉ khi đã có sẵn trong dự án.
- **`scripts/snapshot.mjs` với URL ngoài**: chỉ dùng với file cục bộ hoặc địa chỉ nội bộ được giao.
- **Video kể chuyện (`scripts/story.mjs`)**: chỉ khi được yêu cầu; cần Playwright + FFmpeg; dùng
  `video/` theo luật HyperFrames, không commit file render.
- Mục "Hire the unslopper" (quảng cáo dịch vụ trong README): bỏ qua.

## 3. Quy trình (ánh xạ 9 lượt của unslop)

1. **G0 - Nhìn màn hình.** Đọc file giao diện; chụp ảnh ở 4 cỡ (mục 5). Ghi nhãn THẬT/DEMO.
2. **Rà dấu hiệu** theo `unslop/references/signs.md`, mỗi dấu hiệu một dòng kèm vị trí (file:dòng).
   Bổ sung dấu hiệu riêng CTXĐN: chữ < 12px trên điện thoại, nút < 44×44px, tương phản < 4.5:1,
   tràn ngang, ô nhập không có nhãn.
3. **Chọn mức sửa** (nặng / nhẹ / không cần) như bản gốc. Phần mềm đang dùng thật → mặc định **nhẹ**.
4. **Hướng thiết kế 5 dòng** (Product, Character, World, Moments, Signature) bằng tiếng Việt, rút từ
   nghiệp vụ ngành toa xe. **Dừng, trình chủ đầu tư** trước khi sửa (trừ khi đã được bảo "cứ làm").
5. **9 lượt theo thứ tự**: khoảng cách → màu → biểu tượng → chữ trang trí → kiểu chữ → bố cục →
   chi tiết → hình ảnh → chuyển động. Giá trị cụ thể: `unslop/references/tokens.md`.
6. **Kiểm thử** bằng `scripts/kiem_tra_giao_dien.mjs` (mục 5) - phải PASS hết.
7. **Báo cáo**: hướng thiết kế, thay đổi từng lượt, bảng kiểm thử, ảnh trước/sau, danh sách chữ đã đổi.

## 4. Câu lệnh mẫu (tiếng Việt)

```
Dùng ctxdn-ui-ux-unslop rà giao diện docs/giao-dien-mobile.html, chỉ báo dấu hiệu, chưa sửa
Nâng cấp giao diện màn hình phân công EMS ở mức nhẹ, làm trên bản sao trong sandbox
Chép src/static/app.css ra bản sao, chuẩn hóa khoảng cách và màu theo unslop, giữ họ màu xanh/đỏ trạng thái
Kiểm tra giao diện trước/sau ở 360, 390, 768, 1366 px và xuất báo cáo
```

## 5. Kiểm thử bắt buộc

```
node .claude/skills/ctxdn-ui-ux-unslop/scripts/kiem_tra_giao_dien.mjs <truoc.html> <sau.html> <thu-muc-ket-qua>
```

Script dùng Playwright + Chromium có sẵn, mở cả hai bản ở 360/390/768/1366 px, ghi `ket-qua.json` và
ảnh chụp. Kiểm: có `<meta name="viewport" content="width=device-width…">` (thiếu thì số đo điện thoại vô nghĩa),
khung HTML trừ CSS trùng khớp, chữ trong DOM giống bản trước, không tràn ngang, chữ ≥ 12px, nút ≥ 44px trên
điện thoại, không lỗi JavaScript/tải tài nguyên mới, nút không bị che hoặc bị lớp cố định (toast…) đè.
Mã thoát: 0 PASS, 1 FAIL, 2 lỗi công cụ. Biến `UNSLOP_TOI=1` chạy chế độ tối.
Đây là **mô phỏng trình duyệt** (Chromium), không thay kiểm thử trên iPhone Safari / Android Chrome thật.

## 6. Chi phí

Ngân sách 10.000 đ/lượt (theo lệnh giao nhiệm vụ của chủ đầu tư ngày 13/11/2026). Một tác tử là đủ; không gọi tác tử phụ; tối đa 3 lần chụp/so sánh mỗi lượt
(theo bản gốc); dùng lại kết quả kiểm thử. Không đăng ký, không mua dịch vụ.
