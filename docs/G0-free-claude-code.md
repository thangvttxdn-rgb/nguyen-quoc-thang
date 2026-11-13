# G0 · Free Claude Code (Alishahryar1/free-claude-code)

- Ngày: 13/11/2026 · Đầu vào: chủ đầu tư gửi link kho, yêu cầu rà mã nguồn + so sánh với cách đang dùng.
- Nhãn: **THẬT** (đọc trực tiếp mã nguồn, có file:dòng) · **CẦN CĂN CỨ** · **BLOCKED**.
- Phạm vi rà: đọc tĩnh, **không cài, không chạy**. Bản sao chỉ đọc tại `/home/user/alishahryar1/free-claude-code`
  (bản sao nông, commit `5662101`, 12/11/2026). Đường dẫn bên dưới tính từ `src/free_claude_code/`.

## 1. Kho là gì - THẬT

- Máy chủ trung gian (proxy) Python, chạy trên máy người dùng, cổng mặc định `8082`. Nhận yêu cầu dạng API
  Anthropic/OpenAI từ Claude Code, Codex, Cline, Aider… rồi chuyển sang nhà cung cấp khác (OpenRouter,
  NVIDIA NIM, DeepSeek, Groq, Gemini, GitHub Copilot, ChatGPT/Codex, LM Studio chạy trên máy…).
  Con số "61 nhà cung cấp" là lời tác giả (`README.md:32`), chưa đếm.
- Giấy phép **AGPL-3.0-only** (`LICENSE`, `pyproject.toml`). Ghi rõ không liên kết với Anthropic.
- Quy mô: ~80.900 dòng Python trong `src/`, 30 thư viện phụ thuộc (`pyproject.toml:13-43`, 2 gói chỉ cho
  Windows/macOS; gồm `python-telegram-bot`, `discord.py`, `github-copilot-sdk`, `nvidia-riva-client`, `grpcio`),
  bắt buộc đúng Python **3.14.10**.
- Có thêm: giao diện quản trị web, bot Telegram/Discord điều khiển tác tử từ điện thoại, nhận giọng nói.

## 2. Phát hiện khi rà mã nguồn

### 2.1 Mức NGHIÊM TRỌNG

| # | Phát hiện | Căn cứ (THẬT) | Hệ quả |
|---|---|---|---|
| N1 | Mặc định nghe **mọi giao diện mạng** và **tắt xác thực** | `config/settings.py:734` `host="0.0.0.0"`; `:737-743` `proxy_auth_enabled=False`, mã mặc định `"freecc"`; `api/dependencies.py:52` tắt thì bỏ qua kiểm tra | Máy nào trong mạng LAN chi nhánh cũng gọi được proxy, dùng khóa API của người cài; bật xác thực mà quên đổi mã thì mã là `freecc` ai cũng biết |
| N2 | Tác tử do bot điều khiển chạy với **`--dangerously-skip-permissions`**; không đặt `ALLOWED_DIR` thì làm việc ngay thư mục khởi chạy FCC, không giới hạn thư mục | `cli/managed/claude.py:141,153`; bot gọi qua `runtime/messaging_service.py:232-242` → `cli/managed/session.py:117` | Mọi lệnh tác tử sinh ra (xóa file, chạy shell) đều thực thi không hỏi. Hook `guard.py` có lẽ vẫn chạy, còn luật deny trong `settings` có còn hiệu lực ở chế độ này không - **CẦN CĂN CỨ** (chưa kiểm) |
| N3 | Bot Telegram **không bắt buộc** danh sách người được phép | `messaging/platforms/telegram_inbound.py:29` (tin thoại: `:95`) chỉ lọc khi `ALLOWED_TELEGRAM_USER_ID` có giá trị; trong `runtime/`, `config/`, `messaging/` không có chỗ chặn khởi động khi để trống (`factory.py:61-68` chỉ bỏ thông báo) | Để trống ô này thì ai nhắn tin cho bot cũng ra lệnh được cho tác tử ở N2 → chạy lệnh từ xa trên máy. Discord: để trống là chặn hết, nhưng lọc theo **kênh** chứ không theo người - mọi thành viên kênh đều ra lệnh được (`discord.py:177`) |
| N4 | Mã nguồn, nội dung chat gửi sang **nhà cung cấp thứ ba** | Thiết kế của công cụ (mục 1) | Mã EMS, schema CSDL, dữ liệu nhân sự trong ngữ cảnh rời khỏi phạm vi đã cam kết; gói miễn phí thường được dùng dữ liệu để huấn luyện (**CẦN CĂN CỨ** theo từng nhà cung cấp) |

### 2.2 Mức CAO

| # | Phát hiện | Căn cứ (THẬT) |
|---|---|---|
| C1 | Cài bằng `curl … main/scripts/install.sh \| sh` (Windows: `irm … \| iex`): bước khởi động lấy từ nhánh `main`, rồi **tự chọn bản phát hành mới nhất** và cài `==<bản đó>` - người dùng không chọn/ghim phiên bản | `README.md:66,72`; `scripts/install.sh:1637-1657,1739-1755` |
| C2 | Bộ cài kéo thêm gói không ghim: `@deepseek-ai/dsh@latest`, OpenCode "latest", `aider-chat@latest`, `npm install -g cline` | `scripts/install.sh:13,948-953,1094,1323` |
| C3 | Phụ thuộc chỉ ràng `>=` (không ghim); `uv.lock` có nhưng cách cài khuyến nghị không dùng nó | `pyproject.toml` |
| C4 | Dùng lại **OAuth client ID của ứng dụng Codex chính hãng** để đăng nhập ChatGPT; có cả nhà cung cấp GitHub Copilot | `providers/openai_codex/login.py:16`; `providers/github_copilot/` |
| C5 | Khóa API lưu **văn bản thường** trong `~/.fcc/.env`, token OAuth ChatGPT trong `~/.fcc/auth/openai.json`. Quyền `0600` đặt ở mỗi lần ghi nhưng **bỏ qua trên Windows** (`os.name != "nt"`) - máy EMS chạy Windows | `config/paths.py:5-6,14-15`; `config/env_migrations.py:337-341` |
| C6 | Thêm một đường chạy lệnh không hỏi: Code sessions chế độ `full_access` đặt `approvalPolicy: never`, `:danger-full-access` (chỉ truy cập từ máy cục bộ) | `runtime/codex_app_server.py:738-746` |

C4: dùng gói thuê bao ChatGPT/Copilot qua công cụ bên thứ ba có thể trái điều khoản của OpenAI/GitHub -
**CẦN CĂN CỨ** (chưa đọc điều khoản; README tự nhận "removes integrations if they stop being allowed").

### 2.3 Điểm làm tốt - THẬT

- Không thấy đo lường/telemetry gửi về tác giả; Copilot SDK tắt telemetry (`providers/github_copilot/sdk.py:210`).
- Kiểm tra cập nhật chỉ **hỏi** GitHub Releases + PyPI, không tự cài (`updater/check.py`).
- Giao diện quản trị và "Code sessions" chỉ cho truy cập từ máy cục bộ, kiểm cả `Host`, `Origin`
  (`api/admin_security.py`, `api/code_sessions_routes.py:34`).
- `web_fetch` có chặn SSRF, ghim địa chỉ DNS (`runtime/web_tools/egress.py`).
- Ghi log nội dung thô mặc định tắt (`config/settings.py:663-678`).
- Có bộ test lớn (`tests/`, 21 nhóm) - **chưa chạy**.

## 3. Đối chiếu quy chuẩn dự án (AGENTS.md)

| Quy chuẩn | FCC | Kết luận |
|---|---|---|
| Mục 3: cài thư viện mới phải xin phép | 31 gói + Python 3.14 riêng + gói npm | Vướng - cần duyệt |
| Mục 3: không đưa chuỗi kết nối/mật khẩu ra ngoài | N4: toàn bộ ngữ cảnh gửi cho bên thứ ba | **Vướng** |
| Mục 3: chặn `rm -rf`, SQL ghi | N2, C6 bỏ hết hỏi quyền | Vướng |
| Bài học lemo-opuscar/HyperFrames: ghim phiên bản | C1-C3 không ghim | Vướng |
| Giấy phép | AGPL: chỉ dùng nội bộ thì không phải công bố mã; sửa rồi cho người khác dùng qua mạng thì phải | Dùng được nếu không sửa |

## 4. So sánh với cách đang dùng

Cách đang dùng (THẬT): Claude Code chạy phiên đám mây/máy trạm với tài khoản Anthropic, kèm hàng rào của dự án
(`guard.py`, `settings.local.json`, tài khoản CSDL chỉ đọc, `to-phan-bien`).

| Tiêu chí | Đang dùng (Claude Code + Anthropic) | Free Claude Code |
|---|---|---|
| Chi phí | Trả theo gói/thuê bao | Có gói miễn phí (README: "1.3B+ token/tháng" - **CẦN CĂN CỨ**), hạn mức nhà cung cấp tự đổi |
| Chất lượng mô hình | Mô hình Claude mà kỹ năng, hook được viết cho | Mô hình khác giả danh "Opus/Sonnet"; kỹ năng tiếng Việt, gọi công cụ có thể kém - **chưa kiểm** |
| Dữ liệu đi đâu | Một nhà cung cấp, theo hợp đồng đã biết | Nhà cung cấp được chọn, mỗi nhà điều khoản riêng; **hoặc mô hình chạy trên máy** (LM Studio - `providers/lmstudio`) thì không rời máy, nhưng cần máy có GPU đủ mạnh và chất lượng thấp hơn - **chưa kiểm** |
| Hàng rào an toàn | Hook + quyền + hỏi trước khi chạy | Hook vẫn chạy phía Claude Code, nhưng chế độ bot bỏ hỏi quyền (N2) |
| Bảo mật mạng | Không mở cổng trên máy | Mở cổng 8082 ra LAN, không xác thực (N1) |
| Cài đặt, bảo trì | Có sẵn | Thêm 1 dịch vụ chạy nền, Python 3.14, cập nhật thủ công |
| Chạy trong phiên đám mây hiện nay | Có | Không thực tế (cần proxy trên máy và đổi `ANTHROPIC_BASE_URL`) |
| Chống gián đoạn | Phụ thuộc 1 nhà | Tự chuyển nhà cung cấp, nhiều khóa dự phòng - **ưu điểm thật** |

**Đánh giá:** FCC hợp cho cá nhân thử mô hình rẻ/miễn phí với mã không nhạy cảm. Với kho EMS (schema SQL Server,
dữ liệu nhân sự, cấu hình IIS) thì rủi ro N1-N4 lớn hơn khoản tiết kiệm.

## 5. Đề xuất (chờ chủ đầu tư quyết)

1. **Không cài vào kho EMS hay máy chủ IIS.** Ghi kết luận vào `registry.json` (`trung_lap`).
2. Nếu muốn thử: dùng máy riêng, kho thử không chứa mã/dữ liệu thật, và bắt buộc
   `HOST=127.0.0.1`, `PROXY_AUTH_ENABLED=true` với mã ngẫu nhiên dài, không bật bot Telegram/Discord, đặt `ALLOWED_DIR`, không dùng chế độ `full_access`;
   cài từ tag cố định bằng `uv.lock`, không dùng `curl | sh`.
3. Nếu mục tiêu là giảm chi phí: so sánh gói Anthropic hiện tại với nhu cầu thực trước (cần số liệu sử dụng -
   **CẦN CĂN CỨ**).

## 6. Phản biện G3 (Tổ 2) - FAIL lần 1, đã sửa

Tổ 2 xác nhận N1-N3 đúng mã nguồn, kết luận "không cài vào EMS" giữ nguyên. 8 điểm đã sửa: số thư viện 30
(không phải 31) và nguồn con số 61; C1 bớt phóng đại (bộ cài tự lấy bản phát hành mới nhất); C2 thêm aider, cline;
C5 thêm token OAuth và Windows không đặt quyền; N2 thêm `ALLOWED_DIR`, gắn CẦN CĂN CỨ cho luật deny; N3 Discord lọc
theo kênh; thêm C6 (`full_access`); mục 4 ghi thêm lựa chọn mô hình chạy trên máy.

## 7. Chưa làm

- **BLOCKED**: chạy thử, chạy bộ test của kho (cần cài Python 3.14 + gói ngoài - phải duyệt).
- Chưa đọc điều khoản dịch vụ của OpenAI/GitHub/nhà cung cấp miễn phí (C4, N4).
- Rà tĩnh có chọn lọc (xác thực, mạng, quyền, cập nhật, cài đặt), chưa đọc hết 80.900 dòng.
