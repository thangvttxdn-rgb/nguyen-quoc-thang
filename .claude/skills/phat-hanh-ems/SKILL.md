---
name: phat-hanh-ems
description: Quy trình phát hành (release) hệ thống EMS của Chi nhánh Toa xe Đà Nẵng - ứng dụng web Node.js chạy trên máy chủ Windows/IIS nội bộ. Chốt phiên bản, cập nhật CHANGELOG, build/test, gắn tag, triển khai staging rồi production và thông báo. Dùng khi người dùng nói "phát hành EMS", "release EMS", "lên phiên bản EMS", "đóng gói EMS", "deploy EMS", hoặc cần rollback một bản phát hành EMS.
---

# Phát hành EMS

Skill này chuẩn hoá các bước phát hành hệ thống EMS. Luôn làm theo thứ tự, **không bỏ bước**, và dừng lại hỏi người dùng nếu một bước không đạt.

## 0. Cấu hình dự án

EMS là ứng dụng web **Node.js**, triển khai trên **máy chủ Windows nội bộ chạy IIS**, có môi trường **staging riêng**.

| Mục | Giá trị |
|---|---|
| Nhánh phát hành | `main` |
| Nhánh phát triển | `develop` |
| Cài phụ thuộc | `npm ci` |
| Lệnh build | `npm run build` |
| Lệnh test | `npm test` |
| Lệnh lint | `npm run lint` |
| Thư mục artifact | `<điền: dist/ hoặc build/ - xem cấu hình bundler>` |
| Máy chủ staging | `<điền tên máy / IP>` |
| Máy chủ production | `<điền tên máy / IP>` |
| Đường dẫn site trên IIS | `<điền, ví dụ C:\inetpub\wwwroot\ems>` |
| Tên IIS Application Pool | `<điền>` |
| Thư mục sao lưu | `<điền, ví dụ D:\Backup\EMS>` |
| Người duyệt phát hành | Phó giám đốc chi nhánh |

> Các ô `<điền>` là thông tin riêng của hạ tầng chi nhánh - bổ sung một lần rồi commit. **Không đoán**; nếu chưa rõ thì hỏi người dùng.

## 1. Kiểm tra trước phát hành

```bash
git status --short          # phải sạch
git rev-parse --abbrev-ref HEAD
git fetch origin && git pull origin main
git log --oneline $(git describe --tags --abbrev=0)..HEAD
```

Điều kiện bắt buộc:
- Working tree sạch, đang ở nhánh `main`.
- Đã đồng bộ với `origin`.
- Không còn PR/công việc bắt buộc đang mở cho phiên bản này.
- `npm ci` chạy được, `package-lock.json` đã commit và khớp với `package.json`.

Nếu bất kỳ điều kiện nào không đạt → dừng, báo rõ vướng mắc, **không tự ý phát hành**.

## 2. Chốt số phiên bản

Dùng SemVer `vMAJOR.MINOR.PATCH`:
- `MAJOR`: thay đổi phá vỡ tương thích (đổi cấu trúc CSDL, đổi API, buộc thao tác thủ công khi nâng cấp).
- `MINOR`: thêm chức năng, vẫn tương thích ngược.
- `PATCH`: chỉ sửa lỗi.

Đề xuất số phiên bản dựa trên danh sách commit ở bước 1, **xin xác nhận của người dùng**, rồi ghi vào `package.json`:

```bash
npm version X.Y.Z --no-git-tag-version   # chỉ sửa package.json, tự tag ở bước 5
```

## 3. Cập nhật CHANGELOG

Thêm mục mới lên đầu `CHANGELOG.md`:

```markdown
## [v1.4.0] - 2026-09-06

### Thêm mới
- ...

### Sửa lỗi
- ...

### Thay đổi
- ...

### Lưu ý nâng cấp
- (Bước thủ công, migration CSDL, đổi biến môi trường... - ghi "Không có" nếu không có)
```

Viết theo góc nhìn người dùng cuối (nhân viên khám chữa toa xe), không copy nguyên message commit kỹ thuật.

## 4. Build và kiểm thử

```bash
npm ci          # cài đúng theo package-lock.json, không dùng npm install
npm run lint
npm test
npm run build
```

**Bắt buộc xanh toàn bộ** mới được đi tiếp.

- Test hoặc lint đỏ → dừng, báo cáo nguyên nhân kèm log. Không được bỏ qua, tắt hay khoanh vùng test để cho qua.
- Build xong → kiểm tra thư mục artifact đã sinh ra file mới (đối chiếu thời gian sửa đổi).
- Nếu có phần backend Node chạy dưới IIS (iisnode), chuẩn bị thêm `node_modules` bản production:

```bash
npm ci --omit=dev
```

## 5. Commit, tag và đẩy lên

```bash
git add package.json package-lock.json CHANGELOG.md
git commit -m "chore(release): phát hành vX.Y.Z"
git tag -a vX.Y.Z -m "EMS vX.Y.Z"
git push -u origin main
git push origin vX.Y.Z
```

Nếu push lỗi mạng: thử lại tối đa 4 lần với khoảng chờ 2s, 4s, 8s, 16s.

## 6. Triển khai lên IIS

Làm **staging trước, production sau**. Các lệnh PowerShell chạy trên máy chủ tương ứng.

### 6.1 Staging

```powershell
# 1. Dừng nhận request (IIS trả trang bảo trì thay vì lỗi 500)
Copy-Item app_offline.htm <đường dẫn site>\app_offline.htm

# 2. Chép artifact mới đè lên site
robocopy <thư mục artifact> <đường dẫn site> /MIR /XF web.config .env

# 3. Khởi động lại application pool
Restart-WebAppPool -Name "<tên app pool>"

# 4. Mở lại site
Remove-Item <đường dẫn site>\app_offline.htm
```

Lưu ý: `/XF web.config .env` để **không đè** cấu hình riêng của môi trường. Nếu bản mới đổi cấu hình, sửa tay theo mục "Lưu ý nâng cấp" trong CHANGELOG.

Chạy kiểm tra khói (smoke test) trên staging:
- Đăng nhập
- Tra cứu toa xe
- Lập và duyệt phiếu sửa chữa
- Xuất báo cáo

Smoke test không đạt → dừng, **không lên production**.

### 6.2 Production

1. **Sao lưu trước** (bắt buộc):
   ```powershell
   $ts = Get-Date -Format "yyyyMMdd-HHmmss"
   Compress-Archive -Path <đường dẫn site>\* -DestinationPath <thư mục sao lưu>\ems-$ts.zip
   # sao lưu CSDL theo quy trình của quản trị CSDL
   ```
2. Triển khai trong khung giờ thấp điểm, sau khi có xác nhận của người duyệt phát hành.
3. Lặp lại các lệnh ở mục 6.1 trên máy chủ production.
4. Kiểm tra sau triển khai: phiên bản hiển thị đúng, Event Viewer và log ứng dụng không có lỗi nghiêm trọng trong 15 phút đầu.

## 7. Thông báo phát hành

Soạn thông báo ngắn gọn bằng tiếng Việt gửi các trạm/tổ khám chữa toa xe (Đà Nẵng, Diêu Trì, Nha Trang, Kim Liên, Quảng Ngãi, Tuy Hoà):

```
EMS vX.Y.Z đã phát hành ngày dd/mm/yyyy.
- Chức năng mới: ...
- Lỗi đã sửa: ...
- Việc cần làm phía người dùng: ... (hoặc "Không có")
Lưu ý: xoá bộ nhớ đệm trình duyệt (Ctrl+F5) nếu giao diện hiển thị chưa đúng.
Liên hệ hỗ trợ: ...
```

## 8. Rollback

Khi bản mới lỗi nghiêm trọng, khôi phục từ bản sao lưu ở mục 6.2:

```powershell
Copy-Item app_offline.htm <đường dẫn site>\app_offline.htm
Expand-Archive -Path <thư mục sao lưu>\ems-<mốc thời gian>.zip -DestinationPath <đường dẫn site> -Force
Restart-WebAppPool -Name "<tên app pool>"
Remove-Item <đường dẫn site>\app_offline.htm
```

- Nếu bản mới có migration CSDL: phục hồi CSDL từ bản sao lưu **trước khi** mở lại site.
- Sau khi rollback: ghi lại nguyên nhân vào CHANGELOG hoặc issue, không xoá tag đã đẩy lên remote (chỉ đánh dấu là bản lỗi).

## Danh mục kiểm tra nhanh

- [ ] Working tree sạch, đúng nhánh, đã pull
- [ ] Số phiên bản đã được xác nhận, đã ghi vào `package.json`
- [ ] CHANGELOG đã cập nhật
- [ ] `npm ci` + lint + test + build xanh
- [ ] Đã commit, tag, push
- [ ] Staging đạt smoke test
- [ ] Đã sao lưu site và CSDL production
- [ ] Production chạy đúng phiên bản, log sạch sau 15 phút
- [ ] Đã gửi thông báo phát hành
