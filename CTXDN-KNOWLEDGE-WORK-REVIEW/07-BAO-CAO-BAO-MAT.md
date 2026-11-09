# 07 · Báo cáo bảo mật

**Phạm vi:** đọc tĩnh kho `anthropics/knowledge-work-plugins` @ `e050c2ec`. Không chạy mã, không kết nối mạng, không kết nối công cụ nào.

| Hạng mục | Kết quả | Mức | Bằng chứng |
|---|---|---|---|
| Prompt injection (rà toàn kho) | **NOT RUN đầy đủ**. Quét từ khóa: 71 skill có từ khóa; đã rà 2 mục, cả 2 là nghĩa thường | Chưa kết luận | 01 mục "Quét từ khóa" |
| Script thực thi | 19 tệp `.py` trong 5 skill; `.github/scripts/external-pr-scope.js` của CI | **Chưa đọc, chưa chạy** | `Glob` |
| Tải/thực thi mã từ xa | Chưa rà toàn bộ. Có `https://` trong `build-dashboard` tải thư viện từ CDN (có SRI) | Trung bình | `data/skills/build-dashboard/SKILL.md:140-141` |
| Truy xuất dữ liệu nhạy cảm | Chưa rà | NOT RUN | — |
| Lộ token/API key | Từ khóa token/API key xuất hiện trong một số skill (ví dụ `legal/triage-nda`, `customer-support/kb-article`); chưa xác định có giá trị thật không | Chưa kết luận | — |
| Kết nối MCP ra ngoài | **186 mục máy chủ MCP** trong 21 `.mcp.json` (SaaS: Slack, Notion, Asana, Amplitude, v.v.). Nhiều mục đã báo lỗi proxy 403 khi kết nối | **Cao** nếu bật cho CTXĐN | `02b-THANH-PHAN-KHAC.csv` |
| Quyền hệ thống tệp | Các skill có `allowed-tools`: đã thu thập trong CSV | Cần đối chiếu | cột `allowed_tools` (inv.json) |
| Dependency không rõ nguồn | Chưa có lockfile/đánh giá; bio-research và data có script Python | Chưa kết luận | — |
| Giấy phép | Apache-2.0 ở gốc; partner-built có LICENSE riêng (Slack Technologies, LLC) | Cần xác minh từng plugin | 01 mục giấy phép |
| Lỗ hổng/cảnh báo công bố | Chưa tra cứu được nguồn | BLOCKED | — |
| Bí mật trong repo CTXĐN | Không chạy quét; `.env`, `secrets/` được `.gitignore` | Không thay đổi | `.gitignore` |

## Quyết định bảo mật

- **Không cài** MCP/plugin/skill nào. Mục MCP 186 ghi BLOCKED.
- **UV-02 và risk-assessment**: không dùng công cụ, không mạng, không script — rủi ro thấp, nhưng vẫn BLOCKED chờ Registry.
- Lỗi nghiêm trọng chưa xử lý: **không ghi nhận** lỗi nghiêm trọng trong phạm vi đã rà, vì phần lớn chưa được rà. Do đó **không kết luận "an toàn"**.

## Rủi ro lớn nhất (đánh giá của Tổ 1, cần Tổ 2 kiểm tra)

1. Kết nối SaaS (MCP) gửi dữ liệu nội bộ ra ngoài nếu được bật.
2. Script trong `bio-research` và `data` chưa đọc, có thể thực thi mã tùy ý nếu chạy.
3. Thư viện CDN không vendor trong `build-dashboard`.
