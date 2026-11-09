# 06 · Kế hoạch và kết quả kiểm thử G2

**Nguyên tắc:** không ghi PASS cho kiểm thử chưa chạy. Các mục chạy được ở đây đều là kiểm thử **offline, cấu trúc, không gọi model**.

## 1. Kiểm thử đã chạy (THẬT)

| Mã | Nội dung | Phạm vi | Kết quả | Bằng chứng |
|---|---|---|---|---|
| T-S1 | Có `name` | 252 skill | **PASS** 252/252 | `EVIDENCE/inventory/tom-tat-kiem-thu.json` |
| T-S2 | Có `description` | 252 skill | **PASS** 252/252 | như trên |
| T-S4 | `SKILL.md` đọc được | 252 skill | **PASS** 252/252 | như trên |
| T-S3 | `name` khớp thư mục | 252 skill | **FAIL 41/252** — ghi nhận, không chặn | danh sách trong JSON |
| T-K1 | Kiểm kê đếm đúng thành phần | toàn kho | **PASS** (chạy lại được bằng `inventory.py`) | `inv.json` |
| T-K2 | Tệp đầu ra CSV tạo được và đủ dòng | 252 + 15 + 5 + 22 + 186 | **PASS** (`02-DANH-MUC-SKILLS.csv`, `02b-THANH-PHAN-KHAC.csv`) | `build_outputs.py` |
| T-R1 | Kiểm thử của repo CTXĐN (`pytest -q --tb=short`) | repo CTXĐN | **BLOCKED** — không có `pytest` trong môi trường; cài thêm cần phê duyệt (AGENTS.md mục 3) | Lỗi: `No module named pytest` |
| T-R2 | `ruff check src/ --quiet` | repo CTXĐN | **NOT RUN** — chưa thử; không cài thêm công cụ | — |

**Thay đổi chỉ có tài liệu mới** trong thư mục `CTXDN-KNOWLEDGE-WORK-REVIEW/`; không sửa mã của `src/` hay `tests/`. Vì vậy T-R1/T-R2 không thể làm kiểm tra hồi quy, nhưng chúng vẫn cần chạy để tuyên bố DONE theo AGENTS.md mục 5.

## 2. Kiểm thử G2.2 (20 nhóm) — trạng thái

| # | Nhóm | Trạng thái | Lý do |
|---|---|---|---|
| 1 | Nhận diện đúng nhiệm vụ | NOT RUN | Cần gọi model |
| 2 | Lựa chọn đúng Skill | NOT RUN | Cần gọi model |
| 3 | Không kích hoạt Skill ngoài phạm vi | NOT RUN | Cần gọi model |
| 4 | Không gọi Agent thừa | NOT RUN | Cần gọi model |
| 5 | Không lặp yêu cầu người dùng | NOT RUN | Cần gọi model |
| 6 | Kết quả tiếng Việt chính xác | DEMO | Chỉ có ví dụ mô phỏng trong UV-02 |
| 7 | Giữ đúng cấu trúc biểu mẫu | DEMO | Đối chiếu tĩnh mẫu UV-02 với bản gốc; chưa kiểm chứng đầu ra thật |
| 8 | Không ghi dữ liệu trái phép | NOT RUN | Cần môi trường có công cụ ghi |
| 9 | Không gửi dữ liệu ra ngoài | BLOCKED | Chưa có sandbox mạng được phép |
| 10 | Phát hiện prompt injection | NOT RUN | Chỉ quét từ khóa (xem 07), chưa rà toàn văn |
| 11 | Kiểm soát truy cập tệp & bí mật | NOT RUN | Cần sandbox |
| 12 | Kiểm soát chi phí token | BLOCKED | Không có số đo đáng tin cậy (xem 08) |
| 13 | Hoạt động khi mất mạng | NOT RUN | Cần sandbox |
| 14 | Lỗi và khả năng phục hồi | NOT RUN | Cần sandbox |
| 15 | So sánh trước–sau | BLOCKED | Không có baseline tương đương để so sánh (G2.3) |
| 16 | Tương thích router hiện hành | BLOCKED | Không tiếp cận được Registry/router |
| 17 | Đầu vào sai hoặc thiếu | NOT RUN | Cần gọi model |
| 18 | Hành vi khi vượt quyền | NOT RUN | Cần sandbox |
| 19 | Tái lập kết quả | PASS (cấu trúc) | Kiểm kê chạy lại được bằng script, SHA cố định; **không** áp dụng cho kết quả model |
| 20 | Giấy phép phù hợp | NOT RUN (một phần) | Đã đọc LICENSE gốc; chưa xác minh từng plugin |

## 3. Kiểm thử trước–sau (G2.3)

**Không có baseline** tương đương (Registry BLOCKED). Vì vậy **không tuyên bố cải thiện**.

Các chỉ số (độ chính xác, số lần gọi model, token, chi phí, thời gian, số công cụ, can thiệp của người) đều **NOT RUN**.

## 4. Mẫu test "DEMO" cho UV-02

Chỉ là đối chiếu tĩnh: đầu ra mẫu có đủ các mục của bản gốc (Mục đích, Phạm vi, RACI, Lưu đồ, Các bước, Ngoại lệ, Chỉ số, Tài liệu liên quan) và có nhãn `CẦN CĂN CỨ` cho nội dung an toàn. **Không đại diện cho năng lực thật.**

## 5. Kế hoạch lượt sau (cần phê duyệt chi phí)

Để chạy nhóm 1–5, 10, 17 cần gọi model trên bộ đầu vào giả lập. Cần: (a) chủ đầu tư phê duyệt ngân sách và mô hình, (b) xác minh đơn giá đã công bố. Chưa đủ điều kiện nên chưa thực hiện.
