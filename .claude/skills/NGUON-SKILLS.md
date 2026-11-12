# Nguồn gốc Skills trong `.claude/skills/`

| Skill | Nguồn | Giấy phép |
|---|---|---|
| `phat-hanh-ems` | Tự viết cho Chi nhánh | Nội bộ |
| `frontend-design`, `mcp-builder`, `slack-gif-creator`, `theme-factory`, `web-artifacts-builder`, `webapp-testing` | [anthropics/skills](https://github.com/anthropics/skills) commit `2c5958e` (06/11/2026), chép nguyên bản | Apache 2.0 (`LICENSE.txt` trong từng thư mục) |

Skills chép nguyên bản **không sửa** và được loại khỏi ruff (`pyproject.toml` → `extend-exclude`). Cập nhật: chép lại thư mục từ commit mới hơn rồi ghi lại mã commit ở bảng trên.

## Kiểm tra trùng lặp (12/11/2026) – không thêm

| Skill trong anthropics/skills | Lý do không thêm |
|---|---|
| `algorithmic-art`, `canvas-design`, `docx`, `pdf`, `pptx`, `xlsx`, `skill-creator` | Trùng tên: đã cài ở cấp tài khoản (bản khác) |
| `claude-api` | Trùng tên: có sẵn trong Claude Code |
| `internal-comms` | Trùng chức năng với `tro-ly-22-ky-nang-ctxdn` (truyền thông nội bộ); mẫu theo định dạng công ty Anthropic |
| `brand-guidelines` | Nhận diện thương hiệu Anthropic - không phù hợp văn bản CTXĐN |
| `academy-guide`, `discernment-nudge` | Kích hoạt ở gần như mọi câu trả lời, thêm gợi ý/câu hỏi cuối bài - xung đột yêu cầu trả lời ngắn gọn |
| `doc-coauthoring` | Thư mục không kèm tệp giấy phép - chưa rõ điều kiện, không đoán |

## Lưu ý an toàn
- `webapp-testing/scripts/with_server.py` gọi `subprocess` với `shell=True` để chạy lệnh khởi động server: chỉ truyền lệnh do người dùng cung cấp, không truyền dữ liệu từ bên ngoài.
- `mcp-builder`, `web-artifacts-builder`, `slack-gif-creator` có thể yêu cầu cài thêm thư viện (npm/pip): vẫn phải xin phép theo AGENTS.md mục 3.
