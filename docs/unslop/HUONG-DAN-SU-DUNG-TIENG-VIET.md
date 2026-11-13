# Hướng dẫn sử dụng ctxdn-ui-ux-unslop (tiếng Việt)

Dành cho người vận hành CTXĐN. Tên lệnh, đường dẫn, thuộc tính giữ nguyên tiếng Anh như bản gốc.
Bản gốc: unslop của Damir Sokolovsky (@heydamir), CC BY 4.0, https://github.com/heydamir/unslop.

## 1. Kỹ năng làm gì

Unslop sửa giao diện "kiểu AI làm" (dải màu tím-xanh-hồng, quầng sáng, emoji làm biểu tượng, chữ in hoa giãn
cách, khoảng cách lộn xộn) thành giao diện có chủ đích. Lớp bọc CTXĐN thêm: **chỉ sửa lớp trình bày**, giữ nguyên
nghiệp vụ, kiểm thử 4 cỡ màn hình.

| Bước | Bản gốc (tiếng Anh) | Nghĩa |
|---|---|---|
| 1 | Look at the screen | Mở và chụp màn hình hiện tại |
| 2 | Audit (`references/signs.md`) | Liệt kê từng dấu hiệu kèm vị trí |
| 3 | Decide how much to change | Nặng / nhẹ (polish mode) / không cần. Phần mềm đang chạy thật: mặc định **nhẹ** |
| 4 | Direction (Product, Character, World, Moments, Signature) | Sản phẩm, tính cách, thế giới, điểm nhấn, dấu riêng - **dừng chờ duyệt** |
| 5 | Nine passes | Spacing → Color → Icons → Copy → Type → Layout → Details → Visuals → Motion |
| 6 | Check | Chạy checklist + `kiem_tra_giao_dien.mjs` |
| 7 | Report | Báo cáo từng lượt, ảnh trước/sau |

Giá trị chuẩn (bản gốc, `references/tokens.md`): lưới 4px; chữ trọng lượng 400-500 (tối đa 600); một màu nhấn;
bo góc: nút 8-10px, thẻ 12-16px; biểu tượng 16-18px nét 1.5. CTXĐN thêm: chữ ≥ 12px, vùng bấm ≥ 44px trên điện thoại.

## 2. Trạng thái hiện tại: THỬ NGHIỆM

Kỹ năng **chưa kích hoạt** - không có lệnh `/ctxdn-ui-ux-unslop`. Khi gõ yêu cầu có "giao diện", "unslop",
"làm đẹp"…, Tổng chỉ huy nhắc đọc file `.claude/thu-nghiem/ctxdn-ui-ux-unslop/SKILL.md` và chỉ làm trên bản sao.

## 3. Câu lệnh mẫu cho Claude

```
Dùng ctxdn-ui-ux-unslop rà giao diện docs/giao-dien-mobile.html, chỉ liệt kê dấu hiệu, chưa sửa
Nâng cấp giao diện màn hình phân công EMS ở mức nhẹ, làm trên bản sao trong docs/unslop/vi-du/
Chép src/static/app.css ra bản sao, chuẩn hóa khoảng cách và màu theo unslop, giữ họ màu xanh/đỏ trạng thái
Đề xuất hướng thiết kế 5 dòng cho phần mềm quản lý tài sản, chưa sửa gì
Kiểm tra giao diện trước/sau ở 360, 390, 768, 1366 px và xuất báo cáo
```

Không nên: "làm lại giao diện cho đẹp" (không nói bản sao, không nói mức) - Claude sẽ hỏi lại.

## 4. Chạy kiểm thử trên Windows

Cần Node.js 18+ (khuyên 22) và Playwright. Cài Playwright là **cài thư viện mới → phải xin phép** (AGENTS.md mục 3).
Mở PowerShell (không cần quyền Administrator) tại thư mục kho:

```powershell
# Một lần, sau khi được duyệt - cài vào thư mục riêng, không đụng PATH hệ thống
mkdir $env:USERPROFILE\ctxdn-ui-test; cd $env:USERPROFILE\ctxdn-ui-test
npm init -y
npm install -D playwright@1.63.0
npx playwright@1.63.0 install chromium

# Mỗi phiên PowerShell: BẮT BUỘC chỉ cho Node chỗ có playwright. Script nạp thư viện theo vị trí file script
# (createRequire), không theo thư mục đang đứng, nên thiếu dòng này sẽ báo "Cannot find module 'playwright'".
$env:NODE_PATH = "$env:USERPROFILE\ctxdn-ui-test\node_modules"

# Mỗi lần kiểm thử
node <đường-dẫn-kho>\.claude\thu-nghiem\ctxdn-ui-ux-unslop\scripts\kiem_tra_giao_dien.mjs `
  <đường-dẫn-kho>\docs\unslop\vi-du\truoc.html `
  <đường-dẫn-kho>\docs\unslop\vi-du\sau.html `
  .\ket-qua --kich-ban <đường-dẫn-kho>\docs\unslop\vi-du\kich-ban-ems.json
```

Phiên bản `1.63.0` là bản đã dùng để kiểm thử trong phiên đám mây (THẬT); đổi bản khác phải được người quản trị duyệt.
`$env:NODE_PATH` chỉ có hiệu lực trong phiên PowerShell đó, không sửa PATH hệ thống.
Nếu PowerShell báo `npm.ps1 cannot be loaded because running scripts is disabled` (execution policy): gọi
`npm.cmd` / `npx.cmd` thay cho `npm` / `npx`, không đổi execution policy của máy.
Hướng dẫn Windows này **chưa chạy thử** trên máy Windows (BLOCKED trong phiên đám mây).

Kết quả: `ket-qua\ket-qua.json` (PASS/FAIL, danh sách lỗi) và ảnh `truoc-<cỡ>-<trạng thái>.jpg`, `sau-…jpg`.

### Kịch bản thao tác (`--kich-ban`)

File JSON, mỗi bước một dòng:

| Bước | Ý nghĩa |
|---|---|
| `{"dien": "#l-user", "gia_tri": "thu"}` | Điền ô nhập |
| `{"bam": "#l-btn"}` | Bấm (không ép: nếu nút bị che thì báo lỗi - đó là lỗi giao diện thật) |
| `{"cho": "#list li button"}` / `{"cho_an": "#toast"}` | Chờ hiện / chờ ẩn |
| `{"chup": "2-danh-sach"}` | Chụp và đo trạng thái này |

## 5. Ý nghĩa kết quả

| Lỗi | Nghĩa |
|---|---|
| `Mã <script> bị thay đổi` | Đã đụng JavaScript - vi phạm bất biến, phải hoàn tác |
| `Danh sách nút/ô nhập/biểu mẫu bị thay đổi` | Mất/thêm nút, đổi `id`, `name`, `type` - vi phạm |
| `chữ hiển thị khác bản trước` | Nội dung chữ trong DOM đổi - kiểm có phải chữ nghiệp vụ không |
| `tràn ngang`, `chữ < 12px`, `nút < 44px`, `nút bị che` | Lỗi trình bày cần sửa tiếp |

## 6. Những điều không làm

Không sinh ảnh trả phí; không dùng font CDN; không chạy `snapshot.mjs` với trang ngoài; không sửa `src/` khi chưa
được giao; không đổi cảnh báo an toàn, phân quyền, chức năng nút.
