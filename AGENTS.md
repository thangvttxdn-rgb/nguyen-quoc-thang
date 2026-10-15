# AGENTS.md — Luật dự án cho tác tử AI

> Vai trò: **[1] Context Builder** (bối cảnh, kiến trúc) và **[7] Verifier** (tiêu chuẩn nghiệm thu).
> Tác tử đọc file này đầu mỗi phiên. Giữ ngắn, chỉ ghi điều **luôn đúng** với dự án.

## 1. Bối cảnh
- Chủ dự án: Phó Giám đốc Chi nhánh Toa xe Đà Nẵng (sửa chữa toa xe, đảm bảo an toàn chạy tàu Kim Liên – Nha Trang).
- Hệ thống chính: **EMS** — web Node.js, chạy trên máy chủ Windows/IIS nội bộ (xem skill `phat-hanh-ems`).
- Ngôn ngữ giao tiếp, commit, tài liệu: **tiếng Việt**. Tên biến/hàm: tiếng Anh.

## 2. Cấu trúc thư mục
| Đường dẫn | Mục đích |
|---|---|
| `AGENTS.md` | Luật, kiến trúc, tiêu chuẩn nghiệm thu (file này) |
| `MEMORY.md` | Bài học kỹ thuật lâu dài, giữ qua các phiên |
| `todo.md` | Kế hoạch & trạng thái của **tác vụ hiện tại** |
| `.claude/settings.local.json` | Phân quyền công cụ, lệnh shell |
| `.claude/skills/` | Quy trình chuẩn (vd. phát hành EMS) |
| `src/` | Mã nguồn |
| `tests/` | Kiểm thử tự động, cấu trúc soi gương `src/` |

## 3. Luật làm việc
1. **Lập kế hoạch trước**: tác vụ > 3 bước → ghi kế hoạch vào `todo.md` trước khi sửa code.
2. **Sửa đúng phạm vi**: không refactor, đổi tên, định dạng lại ngoài yêu cầu.
3. **Không đoán**: thông tin hạ tầng (IP, đường dẫn, mật khẩu) chưa có → hỏi người dùng.
4. **Không bí mật trong repo**: dùng biến môi trường / `.env` (đã gitignore).
5. **Thao tác khó hoàn tác** (xoá dữ liệu, deploy production, force-push) → xin xác nhận.
6. Kết thúc tác vụ: cập nhật `todo.md`; bài học dùng lại được → ghi vào `MEMORY.md`.

## 4. Tiêu chuẩn nghiệm thu (Verifier)
Một thay đổi chỉ được coi là **XONG** khi đủ cả các mục sau:
- [ ] Lint sạch (`npm run lint` hoặc tương đương).
- [ ] Toàn bộ test xanh (`npm test`); code mới có test đi kèm trong `tests/`.
- [ ] Build thành công (`npm run build` nếu có).
- [ ] Không tắt / bỏ qua / khoanh vùng test để cho qua.
- [ ] Đã tự đọc lại diff: không file thừa, không log debug, không bí mật.
- [ ] `todo.md` phản ánh đúng trạng thái; báo cáo trung thực cả phần **chưa** làm được.

## 5. Quy ước commit
- Dạng: `<loại>(<phạm vi>): <mô tả tiếng Việt>` — loại: `feat`, `fix`, `docs`, `test`, `refactor`, `chore`.
- Mỗi commit một ý; không commit khi test đỏ.
