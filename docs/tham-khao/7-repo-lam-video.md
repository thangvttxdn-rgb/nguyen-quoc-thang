# Tham khảo: 7 repo GitHub làm video

Tóm tắt từ video người dùng gửi ngày 12/11/2026 (Facebook, 99 giây, 360×640). Bản thân video **không lưu vào repo** (nội dung của người khác đăng, 1,8 MB nhị phân). Giấy phép đã kiểm tra trực tiếp trên tệp LICENSE của từng repo ngày 12/11/2026; số sao lấy theo video, chưa kiểm chứng.

| # | Repo | Video giới thiệu | Giấy phép (đã kiểm tra) | Đối chiếu với môi trường hiện có |
|---|---|---|---|---|
| 1 | `heygen-com/hyperframes` | Viết HTML ra video, làm riêng cho AI agent | Apache 2.0 | **Trùng**: tài khoản đã kết nối HyperFrames (HeyGen) MCP. Repo có skill riêng (`.claude/skills/…`) - chưa thêm |
| 2 | `remotion-dev/remotion` | Viết component React ra video | **Remotion License**: miễn phí cho cá nhân, công ty ≤ 3 nhân viên, tổ chức phi lợi nhuận. **Công ty lớn hơn phải mua giấy phép** | **Không dùng** cho Chi nhánh khi chưa mua giấy phép |
| 3 | `mrdoob/three.js` | Cảnh 3D trong trình duyệt | MIT | Không trùng; chưa cần cho EMS |
| 4 | `greensock/GSAP` | Chuyển động, hiệu ứng chữ | Repo không kèm tệp LICENSE; README ghi "100% FREE … even for commercial use" theo giấy phép riêng của GSAP | Không trùng; đọc điều khoản trên gsap.com trước khi dùng |
| 5 | `3b1b/manim` | Hoạt hình toán học | MIT | Không trùng |
| 6 | `ahujasid/blender-mcp` | Nối AI vào Blender | MIT | Không trùng; cần cài Blender trên máy người dùng |
| 7 | `FFmpeg/FFmpeg` | Ghép hình, tiếng, xuất video | LGPL 2.1 / GPL 2–3 | **Có sẵn** trong môi trường (`ffmpeg 6.1.1`) |

Video kết luận "cả 7 đều miễn phí" – **không đúng hoàn toàn**: Remotion cần giấy phép trả phí với công ty trên 3 nhân viên.

## Gợi ý dùng cho Chi nhánh
- Video hướng dẫn nội bộ ngắn (an toàn chạy tàu, quy trình khám chữa): HyperFrames (đã kết nối) + FFmpeg.
- Không đưa các thư viện này vào web app EMS; chúng không thuộc kiến trúc dự án (AGENTS.md mục 1).
