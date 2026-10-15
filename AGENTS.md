# QUY CHUẨN KIẾN TRÚC & VẬN HÀNH AGENT (AGENTS.md)

## 1. Tổng quan Kiến trúc & Công nghệ
- **Backend:** Python (FastAPI / Flask)
- **Cơ sở dữ liệu:** SQL Server (truy vấn qua pyodbc / SQLAlchemy)
- **Frontend:** HTML5, CSS3, JavaScript thuần (Vanilla JS)
- **Thư mục chính:**
  - `src/api/`: Các route xử lý nghiệp vụ và API.
  - `src/db/`: Kết nối CSDL, stored procedures và schema.
  - `src/static/` & `src/templates/`: Giao diện người dùng.
  - `tests/`: Toàn bộ bài kiểm thử tự động (pytest).

## 2. Lệnh Thực thi & Lọc nhiễu (Observe & Trim)
Luôn sử dụng cờ rút gọn (quiet/short) khi chạy lệnh để cắt giảm log thừa, tránh làm tràn cửa sổ ngữ cảnh:
- **Chạy toàn bộ test:** `pytest -q --tb=short`
- **Chạy test theo phân hệ:** `pytest tests/<ten_phan_he>/ -q`
- **Kiểm tra lỗi cú pháp/quy chuẩn (Lint):** `ruff check src/ --quiet`

## 3. Quy tắc An toàn & Phân quyền (Policy Gate)
- **ĐƯỢC PHÉP TỰ ĐỘNG (ALLOW):** Đọc file, tìm kiếm mã nguồn, chạy `pytest`, chạy `ruff`, truy vấn SQL dạng `SELECT`.
- **PHẢI XIN PHÉP CON NGƯỜI (ASK/APPROVE):** Mọi thao tác sửa file cấu hình hệ thống, thay đổi cấu trúc bảng (`ALTER/DROP TABLE`), cài đặt thêm thư viện mới, hoặc đẩy code lên nhánh chính.
- **CẤM TUYỆT ĐỐI (DENY):** Xóa thư mục gốc (`rm -rf`), can thiệp ra ngoài phạm vi thư mục dự án, hardcode mật khẩu/chuỗi kết nối CSDL trực tiếp vào mã nguồn.

> Phần lệnh shell được cưỡng chế kỹ thuật tại `.claude/settings.local.json`. Riêng giới hạn `SELECT`/`ALTER`/`DROP` là luật hành vi: tác tử phải tự tuân thủ, nên tốt nhất dùng tài khoản CSDL chỉ có quyền đọc khi làm việc với tác tử.

## 4. Điều phối Tác tử phụ (Subagents)
- Khi cần tìm kiếm vị trí sử dụng của một biến/hàm trên toàn bộ dự án hoặc đọc tài liệu quy chuẩn dài, hãy tách **Subagent** với vùng ngữ cảnh độc lập để rà soát và chỉ trả về bản tóm tắt ngắn gọn cho Agent chính.

## 5. Tiêu chuẩn Nghiệm thu (Verifier - Định nghĩa "DONE")
Một tác vụ CHỈ được phép đánh dấu hoàn thành khi thỏa mãn đồng thời 3 điều kiện thực tế:
1. Chạy `pytest -q` báo xanh 100% (tests pass).
2. Chạy `ruff check` không phát sinh lỗi mới (no new lint errors).
3. Đã cập nhật trạng thái vào `todo.md` và ghi chú phát hiện quan trọng (nếu có) vào `MEMORY.md`.
