---
name: phat-hanh-ems
description: Quy trình phát hành (release) hệ thống EMS của Chi nhánh Toa xe Đà Nẵng - chốt phiên bản, cập nhật CHANGELOG, build/test, gắn tag, triển khai và thông báo. Dùng khi người dùng nói "phát hành EMS", "release EMS", "lên phiên bản EMS", "đóng gói EMS", "deploy EMS", hoặc cần rollback một bản phát hành EMS.
---

# Phát hành EMS

Skill này chuẩn hoá các bước phát hành hệ thống EMS. Luôn làm theo thứ tự, **không bỏ bước**, và dừng lại hỏi người dùng nếu một bước không đạt.

## 0. Cấu hình dự án (điền trước khi dùng lần đầu)

Các giá trị dưới đây là **placeholder** - sửa lại cho đúng dự án EMS thật rồi commit.

| Mục | Giá trị |
|---|---|
| Nhánh phát hành | `main` |
| Nhánh phát triển | `develop` |
| Lệnh build | `cmake -S . -B build -DCMAKE_BUILD_TYPE=Release && cmake --build build -j` |
| Lệnh test | `ctest --test-dir build --output-on-failure` |
| Lệnh đóng gói | `cmake --build build --target package` |
| Thư mục artifact | `build/dist/` |
| Môi trường staging | `<điền>` |
| Môi trường production | `<điền>` |
| Người duyệt phát hành | Phó giám đốc chi nhánh |

> Nếu EMS không dùng CMake/C++, thay bằng lệnh thực tế (ví dụ `npm ci && npm run build`, `dotnet publish -c Release`). Không đoán - hỏi người dùng nếu chưa rõ.

## 1. Kiểm tra trước phát hành

```bash
git status --short          # phải sạch
git rev-parse --abbrev-ref HEAD
git fetch origin && git pull origin <nhánh phát hành>
git log --oneline $(git describe --tags --abbrev=0)..HEAD
```

Điều kiện bắt buộc:
- Working tree sạch, đang ở đúng nhánh phát hành.
- Đã đồng bộ với `origin`.
- Không còn PR/công việc bắt buộc đang mở cho phiên bản này.

Nếu bất kỳ điều kiện nào không đạt → dừng, báo rõ vướng mắc, **không tự ý phát hành**.

## 2. Chốt số phiên bản

Dùng SemVer `vMAJOR.MINOR.PATCH`:
- `MAJOR`: thay đổi phá vỡ tương thích (đổi cấu trúc CSDL, đổi API, buộc thao tác thủ công khi nâng cấp).
- `MINOR`: thêm chức năng, vẫn tương thích ngược.
- `PATCH`: chỉ sửa lỗi.

Đề xuất số phiên bản dựa trên danh sách commit ở bước 1, rồi **xin xác nhận của người dùng** trước khi đi tiếp.

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
- (Bước thủ công, migration CSDL, đổi cấu hình... - ghi "Không có" nếu không có)
```

Viết theo góc nhìn người dùng cuối (nhân viên khám chữa toa xe), không copy nguyên message commit kỹ thuật.

## 4. Build và kiểm thử

Chạy lệnh build và test ở mục 0. **Bắt buộc xanh toàn bộ** mới được đi tiếp.

- Test đỏ → dừng, báo cáo nguyên nhân kèm log. Không được bỏ qua, tắt hay khoanh vùng test để cho qua.
- Build ra artifact → kiểm tra artifact tồn tại trong thư mục đã cấu hình.

## 5. Commit, tag và đẩy lên

```bash
git add CHANGELOG.md <file phiên bản>
git commit -m "chore(release): phát hành vX.Y.Z"
git tag -a vX.Y.Z -m "EMS vX.Y.Z"
git push -u origin <nhánh phát hành>
git push origin vX.Y.Z
```

Nếu push lỗi mạng: thử lại tối đa 4 lần với khoảng chờ 2s, 4s, 8s, 16s.

## 6. Triển khai

1. Triển khai lên **staging** trước, chạy kiểm tra khói (smoke test): đăng nhập, tra cứu toa xe, lập/duyệt phiếu sửa chữa, xuất báo cáo.
2. Sao lưu CSDL và bản đang chạy ở production **trước khi** triển khai.
3. Triển khai production trong khung giờ thấp điểm, sau khi có xác nhận của người duyệt phát hành.
4. Kiểm tra lại sau triển khai: phiên bản hiển thị đúng, log không có lỗi nghiêm trọng trong 15 phút đầu.

## 7. Thông báo phát hành

Soạn thông báo ngắn gọn bằng tiếng Việt gửi các trạm/tổ khám chữa toa xe (Đà Nẵng, Diêu Trì, Nha Trang, Kim Liên, Quảng Ngãi, Tuy Hoà):

```
EMS vX.Y.Z đã phát hành ngày dd/mm/yyyy.
- Chức năng mới: ...
- Lỗi đã sửa: ...
- Việc cần làm phía người dùng: ... (hoặc "Không có")
Liên hệ hỗ trợ: ...
```

## 8. Rollback

Khi bản mới lỗi nghiêm trọng:

```bash
git checkout v<phiên bản trước>          # xác định mã nguồn bản cũ
# triển khai lại artifact bản cũ đã lưu ở bước 6.2
# phục hồi CSDL từ bản sao lưu nếu bản mới có migration
```

Sau khi rollback: ghi lại nguyên nhân vào CHANGELOG hoặc issue, không xoá tag đã đẩy lên remote (chỉ đánh dấu là bản lỗi).

## Danh mục kiểm tra nhanh

- [ ] Working tree sạch, đúng nhánh, đã pull
- [ ] Số phiên bản đã được xác nhận
- [ ] CHANGELOG đã cập nhật
- [ ] Build + test xanh
- [ ] Đã commit, tag, push
- [ ] Staging đạt smoke test
- [ ] Đã sao lưu trước khi lên production
- [ ] Production chạy đúng phiên bản, log sạch
- [ ] Đã gửi thông báo phát hành
