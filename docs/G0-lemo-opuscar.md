# BÁO CÁO G0 – ĐÁNH GIÁ `lemomo-ai/lemo-opuscar` CHO CTXĐN AI VIDEO STUDIO

- Ngày: 16/10/2026 · Vai trò: kiến trúc sư phần mềm / sản xuất video kỹ thuật
- Phạm vi G0: **chỉ kiểm kê, phân tích, phản biện**. Đã đọc mã nguồn (clone nông, chỉ đọc) tại commit `d33bdea` (16/10/2026). **Không** cài đặt, **không** chạy script, **không** gọi API, **không** phát sinh chi phí.
- Ký hiệu độ tin cậy: **[Đ]** đã kiểm chứng trong mã nguồn · **[S]** suy luận/ước lượng, cần kiểm chứng ở G1–G3.

---

## 1. Tóm tắt điều hành

| Hạng mục | Kết luận | Mức |
|---|---|---|
| Bản chất | Thư viện **51 "style" phim + bộ prompt chỉ dẫn** cho tác tử lập trình (Claude Code). Video được **vẽ bằng code** (canvas/WebGL, three.js), chụp từng khung bằng Chrome không giao diện; **không** dùng AI sinh video/ảnh | [Đ] |
| Giấy phép | MIT cho mã; tài nguyên bên thứ ba CC0/CC BY/OFL; lưu ý giọng đọc edge-tts, espeak-ng | Xanh/Vàng |
| Bảo mật | **Vàng**: plugin tự `git reset --hard` theo nhánh `main` mỗi lần chạy, Python không ghim phiên bản, tác tử được dặn "tự cài gói, không hỏi lại" – **xung đột** với Policy Gate của CTXĐN | Vàng |
| Chi phí | Phần mềm 0 đ. Chi phí chính: **token Claude** (repo không công bố số liệu) + **máy có GPU** cho 3D + công chuyên gia duyệt | [S] |
| Chạy từ iPhone | **Điều khiển được**, nhưng phiên đám mây **không có GPU** (4 vCPU, 15 GB RAM [Đ]) → 3D chậm. Tốt nhất: iPhone điều khiển máy trạm có GPU tại cơ quan | Vàng |
| Phù hợp Studio | **Phù hợp có điều kiện**: dựng 3D chi tiết tốt (style *Exploded Teardown*), nhưng **không có nhân vật người 3D**, **không có giọng tiếng Việt offline**, chất lượng phụ thuộc model (tác giả: "tune cho Opus 5.5") | Vàng |
| Khuyến nghị | **Đi tiếp G1 (chuẩn bị đầu vào, 0 đ)**; G2 (cài thử) chỉ sau khi duyệt môi trường cô lập + ghim phiên bản | — |

---

## 2. Kiểm kê repository [Đ]

| Thành phần | Nội dung |
|---|---|
| Kích thước | ~112 MB (chủ yếu ảnh gallery); tài nguyên lớn tải riêng từ GitHub Releases |
| Tài liệu điều phối tác tử | `AGENTS.md`, `DIRECTOR.md` (đạo diễn), `TECHNIQUE.md` (kỹ thuật), `styles/<style>/STYLE.md` (51 style) |
| Plugin Claude Code | `.claude-plugin/marketplace.json`, `plugin/skills/lemo-opuscar/SKILL.md` + `scripts/setup.sh` |
| Lõi `core/` | `render/` (Playwright → Chrome headless → ffmpeg), `three/post.js` (DoF, GTAO), `tts/` (Kokoro, edge-tts, kiểm tra Whisper), `audio/` (sampler, Karplus-Strong, foley tổng hợp), `fonts/` |
| Node | `playwright-core ^1.63.0` (Apache-2.0), `three ^0.170.0` (MIT); có `package-lock.json` |
| Python | `numpy, scipy, soundfile, soxr, pillow` (lõi); `kokoro-onnx, edge-tts, faster-whisper` (giọng); `numba` (nhạc) – **không ghim phiên bản** |
| Tải thêm (`tools/assets.json`, có SHA-256) | voice 354 MB, hdri 12 MB, 5 thư viện nhạc cụ 74–416 MB (~1,4 GB); Whisper ~145 MB từ Hugging Face |
| Yêu cầu hệ thống | Node 20+, ffmpeg, Python 3.11+ (hoặc uv); phát triển trên macOS Apple Silicon; Linux "should work"; Windows → WSL; 3D "cần GPU" |
| Thời gian/1 phim | Tác giả: 30–60 phút tác tử + "khá nhiều token" (không có số) |
| Style liên quan kỹ thuật | **Exploded Teardown** (3D PBR từ CAD/BOM), **Projection on White Model**, **Blueprint** (2D, cấm 3D), **Isometric Infographic** (2.5D, có người tối giản), **Engineering Briefing Board**, **Glass Product** |

---

## 3. Giấy phép

| Thành phần | Giấy phép | Đánh giá |
|---|---|---|
| Mã repo | MIT © 2026 LemoLab [Đ] | Dùng nội bộ, sửa đổi tự do; giữ thông báo bản quyền |
| three.js / playwright-core | MIT / Apache-2.0 [Đ] | OK |
| Font `core/fonts` | OFL [Đ] | **Chưa kiểm tra đủ dấu tiếng Việt** – nên dùng Be Vietnam Pro / Noto Sans (OFL) |
| Nhạc cụ mẫu | CC0; riêng Salamander Piano (CC BY 3.0), MuldjordKit (CC BY 4.0) **bắt buộc ghi công** [Đ] | OK nếu ghi CREDITS |
| HDRI Poly Haven | CC0 [Đ] | OK |
| Kokoro (giọng offline) | Model Apache-2.0 [S]; phụ thuộc espeak-ng (GPL-3.0) [S] | Dùng nội bộ – rủi ro thấp; **không hỗ trợ tiếng Việt** [S] |
| edge-tts | Thư viện LGPL-3.0 [S]; **dịch vụ Microsoft trực tuyến** – chính repo cảnh báo "tự kiểm tra điều khoản khi dùng thương mại" [Đ] | **Vàng**: điều khoản chưa rõ + kịch bản gửi ra ngoài |
| Whisper / faster-whisper | MIT [S] | OK |
| Đầu ra video | Thuộc người dùng, không gắn LemoLab [Đ] | OK |
| Nội dung đưa vào | Bản vẽ, ảnh, logo ĐSVN/Chi nhánh | Đơn vị tự chịu trách nhiệm quyền sử dụng |

---

## 4. Bảo mật – phản biện

### 4.1 Điểm tốt [Đ]
- Server xem trước chỉ nghe `127.0.0.1`; không có cờ `--no-sandbox` / `--disable-web-security` cho Chrome.
- Gói tải về kiểm tra SHA-256; giải nén tar có chống path traversal.
- Không có `curl | sh`; luồng mặc định không cần khóa API.

### 4.2 Rủi ro
| # | Rủi ro | Bằng chứng | Mức | Giảm thiểu |
|---|---|---|---|---|
| R1 | **Chuỗi cung ứng không ghim**: mỗi lần chạy `setup.sh` `fetch` + `reset --hard` về `main`; repo commit **hằng ngày** | `setup.sh`: "match main, whatever happened upstream" | Cao | Fork nội bộ, ghim SHA, đặt `LEMO_OPUSCAR_HOME` trỏ bản clone không "managed" |
| R2 | **Prompt injection / trôi chỉ dẫn**: tác tử đọc `AGENTS.md`, `STYLE.md` upstream và làm theo | `SKILL.md` bước 3 | Cao | Như R1 + duyệt diff mỗi lần nâng cấp |
| R3 | Python không ghim phiên bản; dùng `npm install` (không phải `npm ci`) | `requirements*.txt`, `setup.sh` | TB | Tự lập file ghim phiên bản ở G2 |
| R4 | Tác tử được dặn **tự cài gói, không hỏi lại**, chạy đến khi xong | `AGENTS.md`: "Don't come back with more questions" | Cao (so với quy chuẩn CTXĐN) | Chế độ hỏi quyền; **không** cấp `bypassPermissions` |
| R5 | **Dữ liệu ra ngoài**: edge-tts gửi kịch bản tới Microsoft; Whisper tải từ Hugging Face; Claude nhận toàn bộ nội dung | `tts_zh.py`, `asr_check.py` | TB | Phân loại tài liệu; không đưa tài liệu mật; ưu tiên thu giọng thật |
| R6 | **Xung đột repo EMS**: hook `guard.py` chặn ghi ngoài dự án (`~/lemo-opuscar`); Policy Gate cấm tự cài thư viện | `AGENTS.md` dự án | — | **Không** chạy trong repo EMS; dùng repo/máy riêng cho Studio |
| R7 | Chrome `--ignore-gpu-blocklist` | `core/render/browser.mjs` | Thấp | Máy thử nghiệm riêng, không chứa dữ liệu nhạy cảm |

---

## 5. Chi phí (ước lượng)

| Khoản | Chi phí | Ghi chú |
|---|---|---|
| Phần mềm, tài nguyên | 0 đ | Nguồn mở/CC0 |
| Token Claude | **Chưa có số liệu** [S] | Gói thuê bao tính vào hạn mức; API tính theo token – **đo ở G3** với 1 phim 30–45 s, đặt trần trước |
| Phần cứng | Tận dụng máy có sẵn [S] | Mac Apple Silicon hoặc PC GPU NVIDIA; ghi chú trong code: render phần mềm (SwiftShader) chậm ~6 lần [Đ] |
| Dung lượng | ~1–2,5 GB/máy | Lõi ~350 MB + giọng ~0,55 GB + nhạc cụ tùy chọn |
| Giọng đọc | 0 đ (thu giọng thật) / 0 đ nhưng rủi ro điều khoản (edge-tts) | Khuyến nghị thu giọng cán bộ kỹ thuật |
| Nhân công | 4–8 giờ chuyên gia [S] | Viết kịch bản theo quy trình, duyệt kỹ thuật – **khoản quan trọng nhất** |

---

## 6. Khả năng chạy từ iPhone qua Claude Code

| Phương án | Cách làm | Ưu | Nhược |
|---|---|---|---|
| **A. Claude Code đám mây** (app Claude iOS → Claude Code web) | Clone repo vào phiên, tác tử dựng phim trong container | Không cần máy riêng; điều khiển hoàn toàn từ iPhone | **Không GPU**, 4 vCPU/15 GB [Đ] → 3D chậm, có thể vượt thời gian/dung lượng phiên; chính sách mạng có thể chặn GitHub Releases/HF/edge-tts [S]; lấy MP4 về iPhone phải gửi file/đẩy kho lưu trữ |
| **B. iPhone điều khiển máy trạm tại cơ quan** (Remote Control) | Máy trạm có GPU cài sẵn; iPhone ra lệnh, duyệt quyền | GPU thật, dữ liệu ở lại nội bộ, nhanh | Cần máy trạm chuyên dụng + quản trị |
| C. Chạy trực tiếp trên iPhone | — | — | **Không khả thi**: iOS không chạy Node/ffmpeg/Chrome headless |

**Khuyến nghị:** A cho thử **2D / ảnh tĩnh / storyboard**; **B cho video 3D chính thức**.

---

## 7. Khả năng ứng dụng vào CTXĐN AI Video Studio

### 7.1 Điểm mạnh
- **Không bịa hình ảnh**: chi tiết dựng từ hình học/thông số thật → hợp video kỹ thuật, **truy vết được** (CREDITS, FACTS.md).
- **Tái lập & sửa được**: sửa kịch bản/thông số → render lại; lưu như mã nguồn.
- *Exploded Teardown* đúng nhu cầu: tách lớp, đường chú thích, kích thước vẽ trên vật thể, camera bay quanh.
- QC có sẵn: contact sheet, chuẩn âm lượng −14 LUFS, phát hiện khung đen, kiểm tra giọng bằng Whisper.

### 7.2 Hạn chế – phản biện
| Hạn chế | Ảnh hưởng tới bài toán thay lò xo | Mức |
|---|---|---|
| **Không có nhân vật người 3D có khung xương**; chỉ có rig 2.5D và người tối giản kiểu Isometric | 4 công nhân phải dựng mới → dễ "con rối", sai tư thế thao tác | Cao |
| *Teardown* **loại trừ kiểu "assembly manual (step numbers, arrows, hands)"** | Video quy trình cần thứ tự bước + tay người → phải **tùy biến style** | Cao |
| Cần **hình học thật** (CAD/STEP, bản vẽ có kích thước) | Chỉ có bản vẽ giấy → phải số hóa hoặc mô hình gần đúng | Cao |
| **Không có giọng Việt offline**; `asr_check` chỉ tự nhận en/zh [Đ] | Thu giọng thật hoặc dùng edge-tts trực tuyến; bước kiểm tra giọng phải chỉnh cho tiếng Việt | TB |
| Phụ thuộc model và chất lượng tác tử | Kết quả không đồng đều giữa các lần chạy | TB |
| Repo mới, đổi hằng ngày, 1 tác giả | Rủi ro bảo trì dài hạn | TB |

### 7.3 So sánh phương án
| Phương án | Ưu | Nhược |
|---|---|---|
| **lemo-opuscar** (code → video) | 0 đ phần mềm, chính xác hình học, tái lập | Người 3D yếu, cần GPU, phụ thuộc tác tử |
| Blender + mô hình 3D | Nhân vật, rig, ánh sáng chuyên nghiệp | Cần người dựng 3D, tốn công |
| AI sinh video (text-to-video) | Nhanh, người tự nhiên | **Bịa chi tiết kỹ thuật** → **không đạt** cho huấn luyện an toàn |

---

## 8. Quy trình thử nghiệm: video 3D "Thay một lò xo và một biên chống sàng – 4 công nhân"

> **Giả định cần xác nhận:** "biên chống sàng" là chi tiết chống lắc ngang trên giá chuyển hướng; loại toa xe/giá chuyển hướng **chưa biết** – đơn vị cung cấp.

### 8.1 Cổng phê duyệt
| Cổng | Nội dung | Chi phí | Điều kiện qua cổng |
|---|---|---|---|
| **G0** | Báo cáo này | 0 | Lãnh đạo đồng ý đi tiếp |
| **G1 – Đầu vào** | Kịch bản theo quy trình kỹ thuật hiện hành; bản vẽ + kích thước lò xo, biên chống sàng, giá chuyển hướng; ảnh thực tế; dụng cụ, BHLĐ; phân vai 4 công nhân; phân loại tài liệu (được đưa lên Claude hay không) | 0 đ, ~1–2 ngày công | Tổ kỹ thuật + an toàn ký duyệt kịch bản |
| **G2 – Môi trường** | Máy thử riêng (GPU); fork nội bộ ghim SHA; ghim phiên bản Python/npm; chỉ cài tầng `core`; chế độ hỏi quyền; không secrets | 0 đ phần mềm | Checklist bảo mật đạt; danh sách gói được duyệt |
| **G3 – Pilot** | Phim 30–45 s, 1080p/24 fps, 2 phương án A/B | Token Claude có **trần** | Đo thời gian, token, số lần sửa; SME chấm checklist |
| **G4 – Quyết định** | Nhân rộng / tùy biến style / chuyển Blender | — | Báo cáo so sánh |

### 8.2 Phân cảnh khung (chờ SME hiệu chỉnh)
| # | Thời lượng | Nội dung | Vai |
|---|---|---|---|
| 1 | 4 s | Tổng quan giá chuyển hướng, khoanh vị trí lò xo + biên chống sàng | — |
| 2 | 5 s | Biện pháp an toàn: chèn bánh, biển báo, BHLĐ | CN1 (chỉ huy/an toàn) |
| 3 | 7 s | Kích nâng đúng điểm, kiểm tra cân bằng | CN2, CN3 |
| 4 | 7 s | Tháo lò xo hỏng – tách lớp có chú thích | CN2, CN3; CN4 đưa dụng cụ |
| 5 | 6 s | Lắp lò xo mới, đo kiểm theo tiêu chuẩn | CN4 đo, CN1 xác nhận |
| 6 | 7 s | Tháo – lắp biên chống sàng, đo khe hở | CN2, CN3, CN4 |
| 7 | 5 s | Hạ kích, kiểm tra tổng thể, nghiệm thu | CN1 |
| 8 | 3 s | Thẻ kết: nguồn, "Video minh họa – thực hiện theo quy trình hiện hành" | — |

### 8.3 Hai phương án A/B ở G3
| | A: 3D Teardown tùy biến | B: Isometric Infographic 2.5D |
|---|---|---|
| Hình ảnh | PBR, camera bay, tách lớp | Khối phẳng 3 tông |
| Công nhân | Hình nhân xám đơn giản (dựng mới) | Kiểu người tối giản có sẵn |
| Phần cứng | Cần GPU | Chạy được CPU/đám mây |
| Rủi ro | Cao | Thấp |
| Phù hợp | Giới thiệu kết cấu chi tiết | Huấn luyện trình tự bước |

### 8.4 Checklist duyệt kỹ thuật (SME)
1. Đúng thứ tự bước theo quy trình. 2. Đúng điểm kích, vị trí đứng an toàn. 3. Đúng dụng cụ, BHLĐ. 4. Trị số đo khớp tài liệu. 5. Không minh họa sai thao tác nguy hiểm. 6. Thuật ngữ, phụ đề tiếng Việt chuẩn. 7. Ghi nguồn đầy đủ.

---

## 9. Việc cần phê duyệt trước G2/G3
- [ ] Đồng ý đi tiếp G1 (0 đ).
- [ ] Xác nhận chi tiết "biên chống sàng", loại toa xe/giá chuyển hướng, nguồn bản vẽ.
- [ ] Chọn máy: đám mây (iPhone, không GPU) hay máy trạm có GPU.
- [ ] Chọn giọng: thu giọng thật / edge-tts trực tuyến / chỉ phụ đề.
- [ ] Trần token/chi phí cho G3.
- [ ] Repo/máy riêng cho Studio, tách khỏi repo EMS.

## 10. Điểm chưa chắc chắn
- Chi phí token thực tế cho 1 phim – chưa có số liệu công bố.
- Thời gian render 3D trên CPU container đám mây – cần đo.
- Chính sách mạng môi trường đám mây có cho tải GitHub Releases/Hugging Face – chưa kiểm tra.
- Font `core/fonts` có đủ dấu tiếng Việt – chưa kiểm tra.
- Giấy phép Kokoro/espeak-ng/edge-tts ghi [S] theo hiểu biết, chưa đối chiếu văn bản gốc.
