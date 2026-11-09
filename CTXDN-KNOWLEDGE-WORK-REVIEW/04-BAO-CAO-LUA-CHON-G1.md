# 04 · Báo cáo lựa chọn G1

**Nhãn:** THẬT (dựa trên đọc toàn văn hoặc kiểm kê) · CHƯA CHẤM (chỉ có mô tả, chưa đọc toàn văn) · BLOCKED

## 1. Nguyên tắc phân nhóm A–E

Áp dụng đúng định nghĩa G1.1. **Không có mục nào được xếp B (đề xuất Skill mới) hay A (chỉ bổ sung hướng dẫn) ở mức chắc chắn**, vì mọi xếp loại trùng lặp phụ thuộc Registry (BLOCKED).

## 2. Chấm điểm (G1.2) — chỉ cho 2 ứng viên đã đọc toàn văn

| Tiêu chí (điểm tối đa) | UV-02 process-doc (SOP) | risk-assessment |
|---|---|---|
| Giá trị thực tế CTXĐN (25) | 20 | 18 |
| Năng lực mới, không trùng (20) | 12 — chưa biết trùng SOP có sẵn | 10 — khung chung |
| Tích hợp, tái sử dụng (15) | 12 | 13 |
| An toàn, kiểm soát quyền (15) | 13 — không công cụ, không mạng; cần thêm luật "CẦN CĂN CỨ" | 15 |
| Tiết kiệm token (10) | 7 — mẫu dài, chưa đo | 9 |
| Việt hóa, bảo trì (10) | 7 — đã có bản thử | 8 |
| Tài liệu, giấy phép (5) | 5 — Apache-2.0 (gốc kho) | 5 |
| **Tổng** | **76** | **78** |

Ngưỡng: 70–84 = **xem xét có điều kiện**. Điểm chỉ là công cụ hỗ trợ; **không thay kết luận nghiệm thu**. Cả hai đều **BLOCKED** cho đến khi đối chiếu Registry, vì có điều kiện chưa đáp ứng.

Điểm trên do Tổ 1 chấm; Tổ 2 xem xét tại `09-PHAN-BIEN-DOC-LAP-G3.md`.

## 3. Phân nhóm ưu tiên (G1.3) — mức độ ứng viên

| Nhóm | Ứng viên | Trạng thái |
|---|---|---|
| 1 Vận hành & an toàn | process-doc (SOP), risk-assessment, runbook, change-request, compliance-tracking, incident-response | process-doc, risk-assessment: đã chấm. Các mục còn lại: CHƯA CHẤM. incident-response có nguy cơ trùng chủ đề phân tích sự cố (BLOCKED) |
| 2 Phát triển phần mềm | write-spec (PRD), sprint-planning, testing-strategy, deploy-checklist | CHƯA CHẤM |
| 3 Quản trị & tài chính | variance-analysis, financial-statements, vendor-review, status-report | BLOCKED (tài chính — thiếu căn cứ chuẩn kế toán) |
| 4 Nhân sự & đào tạo | onboarding, interview-prep, performance-review, policy-lookup | CHƯA CHẤM; policy-lookup cần tài liệu chính sách nội bộ — BLOCKED |
| 5 Truyền thông | content-creation, campaign-plan, performance-report (marketing) | CHƯA CHẤM; không có kịch bản video tương đương |

**Không áp dụng nguyên xi** quy trình thương mại (theo G1.3). Ví dụ: marketing và sales dùng KPI thương mại không phù hợp đường sắt.

## 4. Phân loại tổng hợp (A–E)

| Loại | Thành phần | Lý do |
|---|---|---|
| D — Không phù hợp | sales (36), small-business (44) | Ngoài nghiệp vụ CTXĐN |
| D — Không phù hợp | bio-research (6) | Ngoài nghiệp vụ; chứa script chưa đánh giá |
| C — Trùng lặp | productivity: memory-management, task-management | Trùng MEMORY.md / todo.md đã có trong repo |
| E — Chưa đủ điều kiện | finance (8), partner-built (71), mục MCP (186) | Thiếu căn cứ/giấy phép/phê duyệt kết nối |
| E — BLOCKED | build-dashboard | Tải CDN, mâu thuẫn yêu cầu offline |
| E — Chưa đủ điều kiện | process-doc, risk-assessment | Chờ đối chiếu Registry |
| CHƯA XÉT | phần còn lại (~200 skill) | Ngoài phạm vi lượt này; không phải quyết định loại |

## 5. Việt hóa (G1.4)

Đã làm **1 mẫu**: `05-UNG-VIEN-VIET-HOA/UV-02-process-doc-SOP.vi.md`.
- Có bản gốc để đối chiếu (đường dẫn và commit SHA).
- Có ví dụ đầu vào/đầu ra. Ví dụ được gắn nhãn **DEMO**.
- Thay đổi có chủ đích: thêm nhãn `CẦN CĂN CỨ` cho nội dung an toàn/pháp lý, không tự điền.
- **Chưa đối chiếu** thuật ngữ với tài liệu CTXĐN (chưa có tài liệu được cấp quyền).

Không làm Việt hóa cho risk-assessment trong lượt này; có thể làm khi có quyết định.

## 6. Ghi chú về lựa chọn gợi ý

Gợi ý sơ bộ để chủ đầu tư xem xét (không phải kết luận nghiệm thu):
1. Đối chiếu Registry trước; sau đó quyết định UV-02 và UC-02.
2. Đọc toàn văn các mục Nhóm 2 (write-spec, deploy-checklist, testing-strategy) trong lượt sau.
