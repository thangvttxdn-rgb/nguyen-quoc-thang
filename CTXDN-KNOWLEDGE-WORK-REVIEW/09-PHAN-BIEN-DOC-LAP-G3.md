# 09 · Phản biện độc lập G3 (Tổ 2)

**Lưu ý về tính độc lập:** lượt này do một tác tử thực hiện cả hai tổ. Phản biện dưới đây được viết theo tư cách rà soát lại có chủ đích, **không phải** đánh giá của người thứ ba. Chủ đầu tư nên coi đây là kiểm tra bổ sung, không thay cho rà soát độc lập.

## Kết luận: **FAIL / BLOCKED** — chưa đủ bằng chứng để đề xuất sử dụng

## Phản biện theo điểm

1. **Registry không tiếp cận được.** Mọi quyết định "không trùng lặp" và "giữ lại" phụ thuộc Registry. Điều kiện nghiệm thu "không trùng lặp vô ích" **chưa đạt**.
2. **Chỉ đọc toàn văn 2 ứng viên** (process-doc, risk-assessment) trong tổng số 252 skill. Điểm số của các ứng viên khác là **không có** — không được tính.
3. **Điểm số của Tổ 1 (76, 78) có thể bị thổi phồng** ở tiêu chí "năng lực mới" vì chưa có đối chiếu. Đề nghị hạ điểm tiêu chí đó về 0–8 cho đến khi có Registry.
4. **Kiểm thử G2 chủ yếu là cấu trúc.** Không có kiểm thử hành vi model nào được chạy. Không được gọi là "kiểm thử năng lực".
5. **Bảo mật chưa rà đầy đủ.** Quét từ khóa không đủ để kết luận. Mục MCP (186) là rủi ro cao nếu bật.
6. **build-dashboard mâu thuẫn** với yêu cầu offline của HTML xem trước. Tổ 1 đã ghi BLOCKED, Tổ 2 đồng ý.
7. **Thiếu kiểm thử repo CTXĐN** (pytest chưa cài). Không thể xác nhận "không hỏng hệ thống hiện có" bằng test; chỉ xác nhận bằng việc không sửa mã.
8. **Việt hóa UV-02** đã thêm nhãn `CẦN CĂN CỨ` — đúng tinh thần an toàn. Nhưng chưa có thuật ngữ được đối chiếu.
9. **Ngân sách/chi phí:** không có số đo; không được tuyên bố đã trong 10.000 VNĐ.

## Ý kiến bất đồng

Không có bất đồng thực chất với Tổ 1 về số liệu kiểm kê. Chỉ bất đồng về mức độ tin cậy của điểm số (xem điểm 3).

## Điều kiện để Tổ 2 xem xét lại

- Có Registry (danh sách Skill, ID, phiên bản) được cấp quyền đọc.
- Đọc toàn văn ít nhất 5 ứng viên Nhóm 1–2 và rà prompt injection trên các mục đó.
- Chạy `pytest -q --tb=short` và `ruff check src/ --quiet` sau khi cài công cụ được phê duyệt.
