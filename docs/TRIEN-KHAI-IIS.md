# Triển khai web app Phân công toa xe lên máy chủ IIS nội bộ

Tài liệu cho người quản trị hệ thống của Chi nhánh. Làm lần lượt từ bước 1 đến bước 9.
Các ô `<điền>` là thông tin riêng của hạ tầng chi nhánh.

## 0. Kiến trúc

```
Điện thoại / máy tính (mạng nội bộ)
        │  HTTPS :443
        ▼
IIS (site "PhanCong") ── HttpPlatformHandler ──► uvicorn 127.0.0.1:<cổng tự cấp>
                                                     │  (Python, src/api/app.py)
                                                     ▼
                                             SQL Server (ODBC Driver 18)
```

IIS nhận HTTPS và tự khởi động, giám sát và khởi động lại tiến trình Python. Ứng dụng chỉ nghe ở `127.0.0.1`, nên máy khác không gọi thẳng vào được.

### Chọn cách chạy

| Cách | Ưu điểm | Nhược điểm |
|---|---|---|
| **A. HttpPlatformHandler** (khuyến nghị) | Một chỗ quản lý (IIS); IIS tự khởi động lại khi tiến trình chết; cấu hình gọn trong `web.config` | Phải cài thêm module; tái chế (recycle) App Pool thì mọi người phải đăng nhập lại |
| B. URL Rewrite + ARR làm reverse proxy, uvicorn chạy như dịch vụ Windows (NSSM/WinSW) | Tách bạch IIS và ứng dụng; khởi động lại IIS không ảnh hưởng ứng dụng | Hai thành phần phải quản lý; cần công cụ ngoài để chạy dịch vụ |

Tài liệu này làm theo **cách A**.

## 1. Chuẩn bị máy chủ (một lần)

Trên Windows Server có IIS:

1. **Python 3.11 trở lên** (bản 64-bit). Khi cài, chọn *Install for all users*; đường dẫn gợi ý `C:\Program Files\Python311`.
2. **Microsoft ODBC Driver 18 for SQL Server**.
3. **HttpPlatformHandler** cho IIS: tải từ trang tải về của Microsoft IIS (tìm "HttpPlatformHandler v1.2"). Cài xong, trong IIS Manager → *Modules* phải thấy `httpPlatformHandler`.
4. **Chứng chỉ HTTPS**: chứng chỉ do CA nội bộ của công ty cấp cho tên máy chủ, ví dụ `phancong.<điền tên miền nội bộ>`.

> Mình chưa kiểm tra được đường dẫn tải chính xác của HttpPlatformHandler; tìm theo tên trên trang chính thức của Microsoft.

## 2. Lấy mã nguồn và cài thư viện

Mở PowerShell **với quyền Administrator**:

```powershell
$App = "D:\Apps\phan-cong"
git clone https://github.com/thangvttxdn-rgb/nguyen-quoc-thang.git $App
# (Nếu máy chủ không có git/Internet: chép thư mục mã nguồn vào $App)

cd $App
& "C:\Program Files\Python311\python.exe" -m venv .venv
.\.venv\Scripts\pip install -r requirements-prod.txt

New-Item -ItemType Directory -Force "$App\logs", "$App\secrets" | Out-Null
```

**Không** đặt mã nguồn trong `C:\inetpub\wwwroot`. Site IIS chỉ trỏ vào `deploy\iis` (chứa đúng một file `web.config`).

## 3. Tạo tài khoản SQL Server

Người quản trị CSDL mở `deploy/sql/tao-tai-khoan.sql` trong SSMS, điền tên CSDL và mật khẩu mạnh, rồi chạy.

- Tài khoản `ems_phan_cong` chỉ được đọc, và INSERT/UPDATE hai bảng `NhanSu`, `PhanCong`. Quyền **DELETE bị chặn**.
- Câu SELECT cuối file in ra quyền đã cấp. Kiểm tra lại: không được có dòng nào là DELETE ở trạng thái GRANT.

## 4. Tạo tài khoản đăng nhập web app

```powershell
cd D:\Apps\phan-cong
.\.venv\Scripts\python -m src.api.auth      # nhập mật khẩu (ẩn), lệnh in ra chuỗi "scrypt$..."
```

Làm lần lượt cho từng người, rồi tạo file `D:\Apps\phan-cong\secrets\users.json`:

```json
{
  "thangnq": {"ten": "Nguyễn Quốc Thắng", "vai_tro": "quan_ly", "bam": "scrypt$..."},
  "kcdt":    {"ten": "Trạm KCTX Diêu Trì", "vai_tro": "xem",     "bam": "scrypt$..."}
}
```

- Vai trò `quan_ly`: được giao việc, ngừng và kích hoạt lại nhân sự. Vai trò `xem`: chỉ xem.
- Tên đăng nhập viết thường, không dấu.
- Lưu file với mã hóa **UTF-8**.

## 5. Cấu hình `web.config`

```powershell
cd D:\Apps\phan-cong\deploy\iis
Copy-Item web.config.mau web.config
notepad web.config
```

Điền `DB_SERVER`, `DB_NAME`, `DB_PASSWORD_APP` (mật khẩu ở bước 3). Nếu không dùng `D:\Apps\phan-cong` thì sửa lại các đường dẫn.

- File `web.config` thật đã nằm trong `.gitignore`. **Không bao giờ commit** file này.
- Không đặt `EMS_DEMO` trên máy chủ thật.

## 6. Phân quyền thư mục (NTFS)

App Pool sẽ chạy dưới danh tính `IIS AppPool\PhanCong`:

```powershell
$App = "D:\Apps\phan-cong"
$Id  = "IIS AppPool\PhanCong"
icacls $App /grant "${Id}:(OI)(CI)RX"                       # đọc + chạy mã nguồn, Python venv
icacls "$App\logs" /grant "${Id}:(OI)(CI)M"                 # ghi log
# secrets: chỉ Administrators và App Pool được đọc
icacls "$App\secrets" /inheritance:r /grant:r "Administrators:(OI)(CI)F" "${Id}:(OI)(CI)R"
icacls "$App\deploy\iis\web.config" /inheritance:r /grant:r "Administrators:F" "${Id}:R" "SYSTEM:F"
```

Nếu Python cài ở `C:\Program Files\Python311`, nhóm `Users` mặc định đã có quyền đọc. Không cần thêm.

Hai lệnh `icacls` cho `secrets` và `web.config` cần chạy **sau khi** đã tạo `users.json` (bước 4) và `web.config` (bước 5).

## 7. Tạo App Pool và Site trong IIS

```powershell
Import-Module WebAdministration
New-WebAppPool -Name "PhanCong"
Set-ItemProperty IIS:\AppPools\PhanCong -Name managedRuntimeVersion -Value ""     # No Managed Code
Set-ItemProperty IIS:\AppPools\PhanCong -Name processModel.idleTimeout -Value "00:00:00"
Set-ItemProperty IIS:\AppPools\PhanCong -Name processModel.maxProcesses -Value 1
# Tái chế định kỳ lúc 03:00 thay vì mỗi 29 giờ (tái chế = mọi người phải đăng nhập lại)
Set-ItemProperty IIS:\AppPools\PhanCong -Name recycling.periodicRestart.time -Value "00:00:00"
Set-ItemProperty IIS:\AppPools\PhanCong -Name recycling.periodicRestart.schedule -Value @{value="03:00:00"}

New-Website -Name "PhanCong" -PhysicalPath "D:\Apps\phan-cong\deploy\iis" `
            -ApplicationPool "PhanCong" -Port 443 -Ssl -HostHeader "phancong.<điền tên miền nội bộ>"
```

Gắn chứng chỉ ở bước 1 cho binding HTTPS: IIS Manager → Sites → PhanCong → *Bindings…* → https → chọn chứng chỉ.

Tường lửa: chỉ mở cổng 443 cho dải IP nội bộ. **Không** mở ra Internet.

## 8. Kiểm tra sau triển khai

| Kiểm tra | Cách làm | Kết quả đúng |
|---|---|---|
| Ứng dụng chạy | Trình duyệt mở `https://phancong.<tên miền>/api/info` | `{"demo":false}` |
| Bắt buộc đăng nhập | Mở `https://phancong.<tên miền>/api/nhan-su` | Lỗi 401 |
| Đăng nhập | Mở trang chủ trên điện thoại, đăng nhập bằng tài khoản `quan_ly` | Hiện danh sách nhân sự thật |
| Phân quyền | Đăng nhập tài khoản `xem` | Không thấy nút giao việc / ngừng |
| Nhật ký | Mở file mới nhất trong `D:\Apps\phan-cong\logs` | Có dòng "Đăng nhập: …" |

## 9. Cập nhật phiên bản mới / quay lại bản cũ

```powershell
cd D:\Apps\phan-cong
git fetch --tags
git checkout <tag hoặc commit mới>
.\.venv\Scripts\pip install -r requirements-prod.txt
Restart-WebAppPool -Name "PhanCong"         # mọi người sẽ phải đăng nhập lại
```

Quay lại bản cũ: `git checkout <tag cũ>`, rồi chạy lại hai lệnh cuối. Nên cập nhật ngoài giờ cao điểm. Ghi lại tag đã chạy trước đó để quay lại khi cần.

## Xử lý sự cố

| Hiện tượng | Nguyên nhân thường gặp | Cách xử lý |
|---|---|---|
| HTTP 502.3 / 502.5 | Python không khởi động được | Xem file trong `logs\`; chạy tay `.\.venv\Scripts\python -m uvicorn src.api.app:app --app-dir D:\Apps\phan-cong` để thấy lỗi |
| 500.19 khi mở site | Chưa cài HttpPlatformHandler hoặc `web.config` sai cú pháp | Cài module; kiểm tra lại XML |
| Đăng nhập xong vẫn quay lại màn đăng nhập | Truy cập bằng `http://` trong khi `EMS_COOKIE_SECURE=1` | Luôn dùng `https://` |
| "Phiên đăng nhập đã hết hạn" hàng loạt | App Pool vừa tái chế hoặc máy chủ khởi động lại | Bình thường; đăng nhập lại. Giữ lịch tái chế 03:00 |
| Lỗi `Data source name not found` / ODBC | Chưa cài ODBC Driver 18, hoặc sai tên driver | Cài driver; hoặc đặt biến `DB_DRIVER` đúng tên driver đã cài |
| Lỗi chứng chỉ khi kết nối SQL | SQL Server dùng chứng chỉ tự ký | Tốt nhất: cấp chứng chỉ CA nội bộ cho SQL Server; tạm thời đặt `DB_TRUST_CERT=1` |
| "Sai quá 5 lần" | Khóa tạm 5 phút sau 5 lần sai | Chờ 5 phút, hoặc tái chế App Pool để mở khóa |
| Không ai đăng nhập được | `users.json` sai đường dẫn, sai JSON, hoặc App Pool không có quyền đọc | Kiểm tra `EMS_USERS_FILE` trong `web.config` và lệnh `icacls` ở bước 6 |

## Giới hạn hiện tại

- **Chỉ chạy 1 tiến trình**, vì phiên đăng nhập lưu trong bộ nhớ. Đủ cho quy mô chi nhánh. Muốn chạy nhiều máy hoặc nhiều tiến trình thì phải chuyển phiên vào CSDL.
- Mật khẩu CSDL nằm trong `web.config`, chỉ được bảo vệ bằng quyền NTFS. Phương án tốt hơn, nếu máy chủ thuộc domain: đăng nhập SQL bằng chính danh tính App Pool (Windows Authentication). Cách này **cần sửa code kết nối**, chưa làm.
- Font chữ tải từ Google Fonts. Máy chủ/điện thoại không ra được Internet thì giao diện dùng font hệ thống, chức năng không đổi.
- Chưa thử với SQL Server thật; tên cột trong `src/db/` vẫn là giả định cần đối chiếu.
