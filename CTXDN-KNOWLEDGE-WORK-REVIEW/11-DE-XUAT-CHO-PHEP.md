# 11 · Đề xuất cần chủ đầu tư phê duyệt

Không có mục nào dưới đây đã được thực hiện. Mỗi mục là một đề xuất riêng, có phạm vi, lợi ích, rủi ro, chi phí và phương án rollback.

## Đề xuất 1 — Cấp quyền đọc Registry CTXĐN

- **Phạm vi:** đọc danh sách Skill, ID, phiên bản, kết quả kiểm thử cũ. Chỉ đọc.
- **Lợi ích:** mở khóa đối chiếu trùng lặp chính thức (G0.2) và quyết định cho UV-02, risk-assessment.
- **Rủi ro:** thấp (chỉ đọc).
- **Chi phí:** không.
- **Rollback:** không cần (không ghi).

## Đề xuất 2 — Cài công cụ kiểm thử `pytest` và `ruff` để chạy kiểm thử repo

- **Phạm vi:** `pip install -r requirements-dev.txt` (phiên bản ghim, trùng CI).
- **Lợi ích:** chạy T-R1/T-R2; đủ điều kiện DONE theo AGENTS.md mục 5.
- **Rủi ro:** cài thư viện mới (AGENTS.md yêu cầu phê duyệt).
- **Chi phí:** không (cài đặt cục bộ).
- **Rollback:** `pip uninstall` các gói đã cài.

## Đề xuất 3 — Ngân sách và mô hình cho kiểm thử hành vi (nhóm 1–5, 10, 17)

- **Phạm vi:** chạy bộ đầu vào giả lập trên một mô hình đã được duyệt.
- **Lợi ích:** kiểm chứng định tuyến, không lặp câu hỏi, prompt injection.
- **Rủi ro:** có chi phí; không ước tính được khi chưa có đơn giá đã xác minh.
- **Chi phí:** **chưa xác định** — cần chủ đầu tư cung cấp đơn giá và ngân sách. Giới hạn 10.000 VNĐ/lượt không được vượt.
- **Rollback:** dừng lượt, giữ nguyên kết quả đã có.

## Đề xuất 4 — Đọc toàn văn và rà bảo mật các ứng viên Nhóm 1–2

- **Phạm vi:** process-doc, risk-assessment, incident-response, write-spec, deploy-checklist, testing-strategy, sprint-planning, testing-strategy; và 19 script trong skill có `scripts/` (chỉ đọc, không chạy).
- **Lợi ích:** điểm số có căn cứ; rà prompt injection.
- **Rủi ro:** không.
- **Chi phí:** chỉ thời gian đọc.
- **Rollback:** không cần.

## Đề xuất 5 — Không kích hoạt kết nối MCP/SaaS (186 mục)

- **Khuyến nghị:** **không bật** trong giai đoạn này. Đây là quyết định an toàn, cần người duyệt nếu muốn thay đổi.
- **Lý do:** gửi dữ liệu ra dịch vụ bên ngoài; nhiều mục đã lỗi proxy.

## Đề xuất 6 — Giữ nguyên bản build-dashboard hoặc vendor thư viện

- **Phạm vi:** nếu muốn dùng dashboard, phải tải Chart.js về và đưa vào repo (vendoring) thay vì dùng CDN.
- **Lợi ích:** chạy offline, tuân yêu cầu HTML xem trước.
- **Rủi ro:** giấy phép thư viện cần xác minh.
- **Chi phí:** không.
- **Rollback:** xóa thư viện đã vendor.

## Đề xuất 7 — Quyết định về cấu trúc hồ sơ và commit

- **Hiện trạng:** thư mục `CTXDN-KNOWLEDGE-WORK-REVIEW/` đã tạo trên nhánh `claude/anthropic-knowledge-work-review-em31y1`, chưa merge vào nhánh chính.
- **Cần quyết định:** có giữ hồ sơ trong repo này hay chuyển sang repo khác. Không push vào nhánh chính.
