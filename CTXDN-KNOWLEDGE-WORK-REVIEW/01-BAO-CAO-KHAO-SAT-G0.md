# 01 · Báo cáo khảo sát G0

**Nhãn dữ liệu:** THẬT (đo bằng script/đọc tệp) · BLOCKED (không tiếp cận được)

## G0.1 Khảo sát kho GitHub — THẬT

| Mục | Kết quả | Nguồn bằng chứng |
|---|---|---|
| URL | https://github.com/anthropics/knowledge-work-plugins | Lệnh clone |
| Nhánh mặc định | `main` | `git branch --show-current` trong bản clone |
| Commit SHA khảo sát | `e050c2ec856373787143d7057663a6ebd1277df3` | `git rev-parse HEAD` |
| Ngày commit | 2026-11-06 16:55:43 -0800 | `git log -1` |
| Phương thức lấy | `git clone --depth 1` (chỉ đọc), vào thư mục scratchpad, không chạy mã từ kho | — |
| Tổng tệp | 1.285 tệp (không tính `.git`) | đếm `find` |
| Giấy phép gốc | Apache License 2.0 (tệp `LICENSE` ở gốc) | đọc tiêu đề tệp |
| Giấy phép con | Có `LICENSE`/`LICENSE.txt` riêng ở nhiều plugin và skill (ví dụ `partner-built/slack/LICENSE`: Copyright Slack Technologies, LLC) | Glob + đọc tiêu đề |

**Không giả định** toàn bộ kho là Apache-2.0. Cần xác minh từng plugin trước khi đề xuất (xem 07).

**Phân loại nguồn:**
- Do Anthropic duy trì: các plugin ở gốc kho (bio-research, data, engineering, operations, productivity, v.v.).
- Bên thứ ba: thư mục `partner-built/` (apollo, brand-voice, common-room, slack, zoom-plugin).

**Cảnh báo bảo mật đã công bố:** chưa tra cứu được (không có nguồn cấp quyền). Ghi BLOCKED.

## G0.1 Kiểm kê thành phần — THẬT

Số liệu từ `EVIDENCE/inventory/inv.json`, sinh bởi `EVIDENCE/scripts/inventory.py`.

| Loại | Số lượng |
|---|---|
| Skill (`SKILL.md`) | **252** |
| Command (`commands/*.md`) | **15** |
| Agent (`agents/*.md`) | **5** |
| Plugin (`.claude-plugin/plugin.json`) | **22** |
| Tệp cấu hình MCP (`.mcp.json`) | 21 tệp, **186** mục máy chủ |
| Hook riêng | 0 phát hiện |

Phân bố skill theo plugin: partner-built 71 · sales 36 · small-business 44 · data 10 · engineering 10 · human-resources 9 · operations 9 · legal 9 · product-management 8 · marketing 8 · finance 8 · design 7 · bio-research 6 · productivity 4 · customer-support 5 · enterprise-search 5 · cowork-plugin-management 2 · pdf-viewer 1.

Lưu ý: tổng skill theo plugin trong bảng trên là số liệu của script; đối chiếu lại với `02-DANH-MUC-SKILLS.csv`.

**Thành phần có mã thực thi:** 5 thư mục skill chứa `scripts/` với 19 tệp `.py` (bio-research 4 skill, data 1 skill). Ngoài ra `.github/scripts/external-pr-scope.js` là script CI của kho. **Chưa đọc từng tệp; chưa chạy.** Mức: chưa đánh giá.

## Kiểm thử cấu trúc offline — THẬT

| Mã | Kiểm tra | Kết quả |
|---|---|---|
| T-S1 | Có trường `name` | 252/252 đạt |
| T-S2 | Có trường `description` | 252/252 đạt |
| T-S4 | `SKILL.md` đọc được | 252/252 đạt |
| T-S3 | `name` khớp tên thư mục | 211/252 đạt; **41 không khớp** (chủ yếu trong partner-built, ví dụ `zoom-plugin/skills/oauth` có `name: zoom-oauth`) |

T-S3 không phải lỗi chặn; là điểm cần ghi nhận khi cài đặt (tên gọi router có thể khác tên thư mục).

## Trùng tên nội bộ kho — THẬT

6 nhóm trùng `name` giữa các plugin (từ `tom-tat-kiem-thu.json`):
- `start`: bio-research, productivity, partner-built
- `lead-triage`: sales, small-business
- `account-research`: sales, partner-built
- `call-prep`: sales, partner-built
- `competitive-brief`: product-management, marketing
- `prospect`: partner-built (2 mục)

## Quét từ khóa rủi ro — THẬT (chỉ là sàng lọc, chưa phải kết luận)

71 `SKILL.md` chứa ít nhất một từ khóa (curl, https://, token, password, secret, api key, "ignore all", "system prompt", v.v.). Đã rà thủ công 2 mục:
- `product-management/skills/metrics-review` dòng 372 và `small-business/skills/marketing-monday` dòng 66: "ignore all" dùng theo nghĩa thường, **không phải prompt injection**.
- `data/skills/build-dashboard` dòng 140–141: tải Chart.js và chartjs-adapter từ `cdn.jsdelivr.net` kèm SRI. **Mâu thuẫn với yêu cầu không dùng CDN** của HTML xem trước.

**Chưa rà thủ công 69 mục còn lại.** Ghi NOT RUN đối với rà soát prompt injection toàn diện (xem 07).

## G0.2 Registry CTXĐN — BLOCKED

- Repo `thangvttxdn-rgb/nguyen-quoc-thang` (đang mở) **không có file Registry** danh sách Skills, ID, phiên bản hay kết quả kiểm thử cũ. Tìm theo tên `*registry*`: 0 kết quả.
- Có `.claude/skills/phat-hanh-ems/SKILL.md` (quy trình phát hành EMS) và `docs/so-do-agent.html` có mục "Tool Registry" nhưng chỉ mô tả quyền `settings.local.json`, không phải Registry Skills.
- Danh sách Skills hệ thống hiển thị trong phiên (chỉ tên và mô tả, không có nội dung): `tro-ly-22-ky-nang-ctxdn`, `bao-cao-an-toan-van-dung-ctxdn`, `phan-tich-su-co-toa-xe`, `karpathy-guidelines`, `phat-hanh-ems`. Các mục này được dùng làm **tham chiếu tên**, không đối chiếu được nội dung.

**Hệ quả:** không kết luận được trùng lặp chính thức với Registry. Theo G0.2, mọi quyết định phụ thuộc Registry ghi **BLOCKED**. Không dựng Registry giả.

## G0.3 Bảng đối chiếu — xem `02-DANH-MUC-SKILLS.csv` và `03-DOI-CHIEU-REGISTRY.csv`
