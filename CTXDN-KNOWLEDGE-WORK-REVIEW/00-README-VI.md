# CTXĐN · Rà soát Anthropic Knowledge Work Plugins

**Trạng thái:** CHƯA PHÊ DUYỆT CÀI ĐẶT HOẶC TRIỂN KHAI. Không nghiệm thu thay chủ đầu tư.

## Nguồn

- Kho: https://github.com/anthropics/knowledge-work-plugins
- Nhánh: `main` · Commit: `e050c2ec856373787143d7057663a6ebd1277df3` (2026-11-06)
- Giấy phép gốc: Apache-2.0; thành phần bên thứ ba có giấy phép riêng.

## Kết quả ngắn

- Kiểm kê: 252 skill, 15 command, 5 agent, 22 plugin, 186 mục MCP.
- Registry CTXĐN: **BLOCKED** (không có file trong repo, không cấp quyền đọc).
- Ứng viên xem xét: process-doc (76 điểm), risk-assessment (78 điểm) — **BLOCKED** chờ Registry.
- Việt hóa mẫu: UV-02 (process-doc).
- Kiểm thử: cấu trúc PASS; hành vi model **NOT RUN**; kiểm thử repo **BLOCKED** (thiếu pytest).
- Chi phí: không có số đo; không tính VNĐ.

## Thứ tự đọc

1. `01-BAO-CAO-KHAO-SAT-G0.md`
2. `02-DANH-MUC-SKILLS.csv` và `02b-THANH-PHAN-KHAC.csv`
3. `03-DOI-CHIEU-REGISTRY.csv`
4. `04-BAO-CAO-LUA-CHON-G1.md`
5. `05-UNG-VIEN-VIET-HOA/`
6. `06-KE-HOACH-VA-KET-QUA-TEST-G2.md`
7. `07-BAO-CAO-BAO-MAT.md`
8. `08-SO-CHI-PHI-TOKEN.csv`
9. `09-PHAN-BIEN-DOC-LAP-G3.md`
10. `10-BAO-CAO-NGHIEM-THU.md`
11. `11-DE-XUAT-CHO-PHEP.md`
12. `12-MANIFEST-SHA256.json`
13. `XEM-TRUOC-TOAN-BO.html`

## Tái lập

Chạy lại:
- `python3 -I EVIDENCE/scripts/inventory.py <bản_clone> EVIDENCE/inventory/inv.json`
- `python3 -I EVIDENCE/scripts/build_outputs.py EVIDENCE/inventory/inv.json .`

`EVIDENCE/` chứa script, dữ liệu kiểm kê và tóm tắt kiểm thử.
