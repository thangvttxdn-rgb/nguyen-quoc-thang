# UV-02 · Lập tài liệu quy trình (SOP) — bản Việt hóa thử nghiệm

> **Trạng thái:** ỨNG VIÊN — chưa đưa vào Registry, chưa được phê duyệt cài đặt.
> **Bản gốc:** `operations/skills/process-doc/SKILL.md` trong kho `anthropics/knowledge-work-plugins`, commit `e050c2ec856373787143d7057663a6ebd1277df3` (nhánh `main`, ngày 2026-11-06). Giấy phép: Apache-2.0 (tệp `LICENSE` ở gốc kho; thành phần này không có `LICENSE` riêng).
> **Nhãn:** Bản dịch là sản phẩm của Tổng chỉ huy, không phải của Anthropic.

---

## 1. Mô tả

Lập tài liệu một quy trình nghiệp vụ thành SOP hoàn chỉnh: mục đích, phạm vi, ma trận RACI (Thực hiện – Chịu trách nhiệm – Tham vấn – Thông báo), lưu đồ, các bước chi tiết, ngoại lệ và chỉ số đo lường.

Dùng khi:
- quy trình mới chỉ nằm trong đầu một người và cần ghi thành văn bản;
- cần làm rõ ai phụ trách bước nào (RACI);
- cần soạn SOP cho việc bàn giao hoặc cho đợt kiểm tra;
- cần ghi lại các trường hợp ngoại lệ, tức cách làm việc thực tế.

## 2. Ranh giới an toàn (bắt buộc)

- **Không tự đặt** quy trình an toàn chạy tàu, thông số kỹ thuật toa xe hay điều khoản pháp lý.
- Nếu một bước thuộc an toàn chạy tàu, kỹ thuật hoặc pháp lý, ghi: `CẦN CĂN CỨ: [tên văn bản nội bộ/tiêu chuẩn, số hiệu, điều khoản]` và để trống phần nội dung. Không suy đoán nội dung.
- Chỉ hỏi người dùng khi thiếu thông tin **ảnh hưởng đến việc soạn thảo** (ví dụ: không biết ai là người phê duyệt cuối). Không hỏi lại thông tin người dùng đã cung cấp.

## 3. Đầu vào

`/quy-trinh-sop <tên hoặc mô tả quy trình>`

Người dùng có thể mô tả, dán tài liệu hiện có hoặc chỉ nêu tên; nếu thiếu, hỏi các câu hỏi có ảnh hưởng nhất.

## 4. Mẫu đầu ra

```markdown
## Tài liệu quy trình: [Tên quy trình]
**Đơn vị phụ trách:** [Người/Đơn vị] | **Cập nhật lần cuối:** [Ngày] | **Chu kỳ rà soát:** [Quý/Năm]

### 1. Mục đích
[Quy trình này tồn tại để làm gì]

### 2. Phạm vi
- Bao gồm: …
- Không bao gồm: …

### 3. Ma trận RACI
| Bước | Thực hiện (R) | Chịu trách nhiệm (A) | Tham vấn (C) | Thông báo (I) |
|------|---------------|----------------------|--------------|---------------|

### 4. Lưu đồ
[Sơ đồ ASCII hoặc mô tả từng bước]

### 5. Các bước chi tiết
#### Bước 1: [Tên]
- **Người thực hiện:** …
- **Thời điểm / Kích hoạt:** …
- **Cách làm:** …
- **Kết quả đầu ra:** …

### 6. Ngoại lệ và trường hợp đặc biệt
| Tình huống | Xử lý |
|------------|-------|

### 7. Chỉ số đo lường
| Chỉ số | Mục tiêu | Cách đo |
|--------|----------|---------|

### 8. Tài liệu liên quan
- [CẦN CĂN CỨ nếu chưa có danh mục văn bản]
```

## 5. Ví dụ đầu vào/đầu ra

> **DEMO** — dữ liệu mô phỏng, không phải quy trình thật của CTXĐN.

**Đầu vào (mô phỏng):** "Khi toa xe về xưởng, tổ điều phối ghi sổ rồi giao cho tổ kiểm tra. Đôi khi phải chờ vật tư."

**Đầu ra (mô phỏng, rút gọn):**

```markdown
## Tài liệu quy trình: Tiếp nhận toa xe về xưởng (DEMO)
**Đơn vị phụ trách:** [CẦN CĂN CỨ: đơn vị phụ trách theo quy định nội bộ]

### 1. Mục đích
Ghi nhận toa xe nhập xưởng và chuyển đúng tổ xử lý.

### 4. Các bước chi tiết
#### Bước 1: Ghi sổ tiếp nhận
- Người thực hiện: Tổ điều phối (DEMO)
- Cách làm: [CẦN CĂN CỨ: mẫu sổ và các trường bắt buộc]

### 6. Ngoại lệ
| Tình huống | Xử lý |
|------------|-------|
| Thiếu vật tư, phải chờ | [CẦN CĂN CỨ: quy định xử lý chờ vật tư] |
```

## 6. Ghi chú về thay đổi hành vi

- Giữ nguyên cấu trúc đầu ra (mục, RACI, ngoại lệ, chỉ số).
- Thêm nhãn `CẦN CĂN CỨ` — **thay đổi có chủ đích** so với bản gốc, để không tự điền nội dung an toàn.
- Mẫu gốc là tiếng Anh; bản dịch chưa được đối chiếu với thuật ngữ chính thức của CTXĐN vì chưa có tài liệu cấp quyền.
