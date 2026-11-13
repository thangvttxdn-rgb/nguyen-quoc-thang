# Đối chiếu Registry

Registry duy nhất: `.claude/tong-chi-huy/registry.json` (không tạo registry thứ hai). Sau thay đổi:
55 mục (+2), 16 tuyến (+1), 25 kết luận trùng lặp (+5), 3 nguồn ngoài (+1).

## 1. Mục thêm

| id | Nhóm | Trạng thái | Đường dẫn |
|---|---|---|---|
| `ctxdn-ui-ux-unslop` | Kỹ năng · Giao diện | `thu-nghiem` | `.claude/thu-nghiem/ctxdn-ui-ux-unslop/SKILL.md` |
| `unslop` | Kỹ năng · Giao diện | `thu-nghiem` | `.claude/thu-nghiem/unslop/SKILL.md` |

Trạng thái `thu-nghiem` mới: hook in "THỬ NGHIỆM: đọc <đường dẫn>, chỉ làm trên bản sao trong sandbox";
trang Command Center hiện nhãn "thử nghiệm". Test bắt buộc mục thử nghiệm **không** nằm trong `.claude/skills/`.

## 2. Tuyến mới `giao-dien` - "Nâng cấp giao diện (thử nghiệm)"

- Từ khóa: `giao diện`, `unslop`, `ui`, `ux`, `bố cục`, `css`, `responsive`, `làm đẹp`, `màu sắc`, `typography`.
- Chính: `ctxdn-ui-ux-unslop`. Hỗ trợ: `unslop`, `karpathy-guidelines`, `/code-review`.
- **Thay đổi tuyến cũ:** từ khóa `giao diện` chuyển từ tuyến `ma-nguon` sang `giao-dien` (test cấm trùng từ khóa).
  "Sửa lỗi giao diện…" vẫn về `ma-nguon` vì khớp 2 từ khóa ("sửa lỗi", "lỗi") - có test.

## 3. Kết luận trùng lặp

| A | B | Quyết định | Lý do |
|---|---|---|---|
| unslop (bản gốc) | ctxdn-ui-ux-unslop | Bọc, không gộp | Giữ bản gốc để nâng cấp, giữ ghi công; luật CTXĐN ở lớp bọc |
| ctxdn-ui-ux-unslop | karpathy-guidelines | Chia phạm vi | Giao diện: CSS + chữ trang trí; logic JS, API, CSDL vẫn theo karpathy + /code-review |
| artifact-design (có sẵn) | ctxdn-ui-ux-unslop | Chia phạm vi | artifact-design cho trang Artifact claude.ai; unslop cho phần mềm trong kho |
| frontend-design | ctxdn-ui-ux-unslop | Không cài | Không có trong kho, cùng việc - tránh hai hệ quy tắc thiết kế |
| Canva | ctxdn-ui-ux-unslop | Chia phạm vi | Canva: ấn phẩm; unslop: màn hình phần mềm |

## 4. Xung đột đã kiểm - THẬT

`python -m pytest -q`: **183 passed** (gồm 7 test mới: định tuyến có dấu/không dấu, ưu tiên sửa lỗi,
nhãn thử nghiệm, mã băm bản gốc, vị trí thư mục). `ruff check .`: sạch. `build_page.py --check`: khớp.
