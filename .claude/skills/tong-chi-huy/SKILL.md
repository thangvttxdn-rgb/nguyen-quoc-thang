---
name: tong-chi-huy
description: Quy trình Tổng chỉ huy AI CTXĐN - phân tích yêu cầu, giao việc cho đúng kỹ năng/tác tử/lệnh theo registry, đi qua các cổng G0 khảo sát, G1 thực hiện, G2 kiểm tra, G3 phản biện, nghiệm thu. Dùng khi hook điều phối nạp "[TỔNG CHỈ HUY ...]", khi việc có nhiều bước, khi rà soát hoặc chọn kỹ năng/plugin/tác tử mới, hoặc khi người dùng nói "tổng chỉ huy", "giao việc", "điều phối".
---

# Tổng chỉ huy AI CTXĐN

Mỗi lần người dùng gõ chat, hook `.claude/hooks/dieu_phoi.py` đối chiếu yêu cầu với
`.claude/tong-chi-huy/registry.json` và nạp một **kế hoạch đề xuất**. Kế hoạch là gợi ý
từ khóa, không phải mệnh lệnh: đọc lại yêu cầu thật, giữ phần đúng, bỏ phần khớp nhầm.

## 1. Phân tích (mỗi yêu cầu)

1. Xác định **việc chính** và **việc kèm** (tối đa 2). Nếu kế hoạch hook sai, nói ngắn một câu và chọn lại.
2. Ước **quy mô**:
   - *Nhỏ* - hỏi đáp, sửa một chỗ: làm ngay, bỏ G3.
   - *Vừa/lớn* - văn bản gửi ra ngoài, báo cáo số liệu, thay đổi mã nhiều file, chọn công cụ mới: đi đủ cổng.
3. Đọc **cảnh báo** của hook; mọi thao tác thuộc diện ASK trong `AGENTS.md` mục 3 phải hỏi trước.

## 2. Giao việc

| Giao cho | Cách |
|---|---|
| Kỹ năng | Gọi bằng Skill (`/ten-ky-nang`) |
| Tác tử | Agent với `subagent_type` tương ứng; ngữ cảnh độc lập, chỉ nhận về tóm tắt |
| Lệnh | Gọi `/lenh` |
| Kết nối | Công cụ MCP tương ứng; gửi/đăng ra ngoài chỉ tạo nháp |

Mục có `trang_thai: blocked` trong registry: **không dùng**, nêu `ly_do` nếu người dùng hỏi.

## 3. Các cổng

| Cổng | Việc | Đạt khi |
|---|---|---|
| G0 Khảo sát | Đọc đầu vào, xác định căn cứ (thư, biên bản, số liệu, mã) | Có đủ căn cứ; thiếu thì ghi `BLOCKED` hoặc `CẦN CĂN CỨ` và hỏi **một lần** |
| G1 Thực hiện | Mục chính làm, mục hỗ trợ bổ trợ | Có sản phẩm nháp |
| G2 Kiểm tra | Mã: `python -m pytest -q`, `ruff check .`. Văn bản: thể thức NĐ 30, số liệu khớp nguồn | Không lỗi mới |
| G3 Phản biện | Văn bản, số liệu, quyết định: tác tử `to-phan-bien`. Mã: `/code-review` | PASS, hoặc đã xử lý mọi điểm FAIL |
| Nghiệm thu | Điều kiện DONE của `AGENTS.md` mục 5; cập nhật `todo.md`, `MEMORY.md` | Báo kết quả thật, kèm điểm chưa đạt |

**Không nghiệm thu thay chủ đầu tư.** Báo "đã xong" chỉ khi đạt; còn lại báo đúng trạng thái.

### Tính năng mới: đi theo Spec Kit

| Cổng | Lệnh Spec Kit |
|---|---|
| G0 | `/speckit-specify` rồi `/speckit-clarify` (đặc tả tiếng Việt, tối đa 5 câu hỏi) |
| G1 | `/speckit-plan` → `/speckit-tasks` → `/speckit-implement` |
| G2 | `/speckit-checklist`, `/speckit-converge`, pytest, ruff |
| G3 | `/speckit-analyze` (bộ spec/plan/tasks) + `/code-review` (mã) |

Hiến pháp `.specify/memory/constitution.md` chỉ tóm tắt `AGENTS.md`; sửa `AGENTS.md` trước.
`todo.md` chỉ ghi trạng thái và đường dẫn `specs/NNN-ten/tasks.md`, không chép danh sách việc.
Không tự tạo nhánh git cho tính năng; làm trên nhánh được giao.

### Video: HyperFrames v0.9.37

Kỹ năng `hyperframes` (đọc trước), `hyperframes-registry` (khối dựng sẵn), `hyperframes-cli` (render).
Luôn gọi `npx hyperframes@0.9.37`, không gọi bản không ghim; lần chạy đầu xin phép. Dự án để trong
`video/<ten>/`. Không dùng `media-use`, đăng nhập HeyGen, `locate.mjs auto` khi chưa duyệt (gửi dữ
liệu ra ngoài). G3: `to-phan-bien` rà nội dung kỹ thuật (thao tác, số liệu, an toàn) trước khi phát.

## 4. Nhãn dữ liệu

`THẬT` (đo, đọc từ nguồn) · `DEMO` (ví dụ mô phỏng) · `BLOCKED` (không tiếp cận được) ·
`CẦN CĂN CỨ` (nội dung an toàn/pháp lý chưa có văn bản gốc - không tự điền).

## 5. Thêm kỹ năng, tác tử, lệnh mới

1. Tìm trong `registry.json` mục cùng việc. Trùng thì **gộp hoặc bỏ**, ghi vào `trung_lap` kèm lý do.
2. Không trùng: thêm vào `muc`, gắn vào `tuyen` (từ khóa tiếng Việt có dấu).
3. Sinh lại trang: `python .claude/tong-chi-huy/build_page.py`.
4. Chạy `python -m pytest tests/harness/ -q` (kiểm tra registry nhất quán, trang khớp registry).

## 6. Chi phí

Kế hoạch hook dài khoảng 100-200 token mỗi lượt. Không tự gọi tác tử phụ cho việc nhỏ.
Ngân sách mỗi lượt đánh giá công cụ: theo chủ đầu tư (hồ sơ rà soát ghi 10.000 VNĐ/lượt).
