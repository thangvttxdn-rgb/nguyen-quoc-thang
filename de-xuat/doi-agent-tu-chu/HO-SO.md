# HỒ SƠ PHƯƠNG ÁN ĐỘI AI AGENT TỰ CHỦ - CTXĐN

*Giai đoạn 1: khảo sát, lập phương án, kiểm chứng trong sandbox. Không phải lệnh triển khai.*
*Lập ngày 2026-11-13 · nhánh `claude/autonomous-agent-team-design-1d1e7h` · Claude Code 2.1.325.*

Nhãn: **THẬT** = đã chạy/đọc và có bằng chứng · **DEMO** = mô phỏng, giả định · **BLOCKED** = chưa đủ
điều kiện · **CẦN CĂN CỨ** = chưa có văn bản gốc, không tự điền.

> **Kết luận chính.** (1) Mở rộng Tổng chỉ huy hiện có bằng **Subagents**, không bật Agent Teams.
> (2) Ngân sách 10.000 đ/lượt **không khả thi** cho đội 4 Agent (ước tính DEMO) và không có cơ chế chặn cứng trong phiên
> tương tác → **BLOCKED**, cần chủ đầu tư quyết tỷ giá, hình thức thanh toán và trần mới.
> (3) Trong 23 thao tác khảo sát, `guard.py` hiện hành để lọt 15 thao tác rủi ro; hook đề xuất chặn 12, hỏi
> người duyệt 3 (THẬT, chạy offline; `bang-chung/rao-chan.json`). Chưa áp dụng vì phải qua GATE 2.

---

## 1. Báo cáo kiểm kê hiện trạng

| # | Hạng mục | Hiện trạng | Nhãn |
|---|---|---|---|
| 1 | Mã nguồn, phiên bản | Kho `nguyen-quoc-thang`, commit `af0596b`; FastAPI + SQL Server; Python 3.13.18 (CI 3.11 & 3.13); git 2.43.0; Claude Code **2.1.325**. Registry `phien_ban 1.0`, cập nhật 2026-11-12. | THẬT |
| 2 | Registry | `.claude/tong-chi-huy/registry.json`: **53 mục** (23 kỹ năng, 17 lệnh, 5 tác tử, 5 kết nối, 3 rào chắn); 15 tuyến; 5 `blocked`, 3 `chua-kiem-thu`. Tác tử: `to-phan-bien` (riêng), `general-purpose`, `Explore`, `Plan`, `claude-code-guide` (có sẵn). Chưa có mục về chi phí hay khóa tệp; có mục chồng chéo một phần với đề xuất (xem bảng trùng lặp mục 2). | THẬT |
| 3 | AGENTS.md / CLAUDE.md / quyền / hook / kỹ năng | CLAUDE.md nạp AGENTS.md, MEMORY.md, todo.md. `settings.local.json`: allow 7, ask 7, deny 16 luật. Hook: `guard.py` (PreToolUse), `dieu_phoi.py` (UserPromptSubmit). 14 kỹ năng trong `.claude/skills`. Không có `.claude/settings.json` dự án. | THẬT |
| 4a | Điều phối | `dieu_phoi.py` so từ khóa → kế hoạch gợi ý; **không** giao việc thật, không có mã việc, không khóa tệp. Ví dụ THẬT: yêu cầu này bị định tuyến chính sang "Sửa mã nguồn EMS" (khớp "test", "code", "giao diện") - lệch, đã tự chọn lại. | THẬT |
| 4b | Kiểm thử | 176 test trên commit gốc `af0596b`, 199 sau (thêm 23), `ruff` sạch (`bang-chung/pytest-kich-ban.txt`, có ngày, commit); CI chạy ruff + pytest. | THẬT |
| 4c | Ghi log | Không có nhật ký Agent/chuyển giao. Có logger nghiệp vụ `ems.nhat_ky` (web app, không liên quan). | THẬT |
| 4d | Tính chi phí | Chưa có. **Phát hiện:** transcript `~/.claude/projects/<dự án>/<phiên>.jsonl` ghi `usage` từng lượt gọi (vào/ra/đọc-ghi cache, model) → đo được **sau** khi chạy (`cong-cu/chi_phi.py`). Hook **không** nhận trường chi phí. Chặn cứng chỉ có `--max-budget-usd`, **chỉ ở chế độ `-p`**. | THẬT |
| 5 | Windows | Hook gọi `python3` - trên Windows có thể không có (đã ghi treo trong todo.md). Hook chạy qua Git Bash, không có thì PowerShell (tài liệu chính thức). Agent Teams dạng chia ô không hỗ trợ Windows Terminal. Công cụ mẫu dùng `pathlib`, `os.replace`, khóa `O_EXCL` - chạy được Windows **theo thiết kế, chưa chạy thử trên máy Windows**. | THẬT (tài liệu) / BLOCKED (chạy thử) |
| 6 | Xem trước iPhone Safari | `docs/*.html` có viewport. Trang mới tự chứa, không tải font ngoài. Đã thử trên Chromium giả lập iPhone 13 (không tràn ngang, 0 lỗi console - `bang-chung/xem-truoc-kiem-tra.txt`); **chưa thử Safari thật**. | THẬT (giả lập) / BLOCKED (Safari thật) |
| 7 | Tái sử dụng được | `guard.py` (mở rộng thêm luật Git/bí mật), `dieu_phoi.py` + registry (thêm tuyến "Đội Agent"), `to-phan-bien` (làm Agent 4), `/code-review`, `/security-review`, `Explore`/`Plan`, mẫu test harness, `build_page.py`, CI. | THẬT |

**Đối chiếu tài liệu chính thức** (code.claude.com, đọc 2026-11-13): tác tử phụ hỗ trợ `tools`,
`disallowedTools`, `model` (`haiku`/`sonnet`/`opus`/`fable`/`inherit`), `permissionMode`, `maxTurns`,
`effort`, `hooks`, `isolation: worktree`; lồng tối đa 3 tầng, chỉnh bằng `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`.
Agent Teams: thử nghiệm, tắt mặc định (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`), không khôi phục khi
`/resume`, không đặt quyền riêng từng thành viên, token "tăng tuyến tính theo số thành viên", khoảng 7×
khi chạy chế độ kế hoạch. Hook có `SubagentStart/Stop`, `TaskCreated/Completed`, `TeammateIdle`,
`WorktreeCreate/Remove` (33 sự kiện).

## 2. So sánh mô hình hiện tại và đề xuất

| Tiêu chí | Hiện tại | Đề xuất A: Subagents (**chọn**) | Phương án B: Agent Teams |
|---|---|---|---|
| Trạng thái tính năng | Đang chạy | Ổn định, có sẵn | Thử nghiệm, phải bật cờ |
| Giao việc | Gợi ý từ khóa | Tổng chỉ huy gọi Agent theo ma trận + sổ cái | Trưởng nhóm tự chia, thành viên tự nhận |
| Mã việc, trách nhiệm | Không | `NV-YYYYMMDD-NNN`, phụ trách, tiêu chí | Danh sách việc chung |
| Tránh sửa trùng tệp | Không | Khóa tệp trong sổ cái + hook chặn + worktree | Chỉ khuyến nghị "chia tệp" |
| Quyền từng Agent | - | `tools`/`disallowedTools` từng tác tử | Không đặt riêng lúc tạo |
| Khôi phục khi ngắt | - | Sổ cái ghi nguyên tử, `khoi_phuc()` | Không khôi phục thành viên |
| Chi phí | 1 phiên | 1 phiên + tác tử ngắn hạn, model riêng | Cao nhất (mỗi thành viên 1 phiên) |
| Windows | Có rủi ro `python3` | Như hiện tại | Chia ô không hỗ trợ Windows Terminal |
| Ưu | Đơn giản | Kiểm soát chặt, rẻ hơn | Trao đổi trực tiếp giữa Agent |
| Nhược | Không phối hợp | Tổng chỉ huy là nút cổ chai | Tốn, chưa ổn định, khó kiểm soát |

### Trùng lặp với registry (đã đối chiếu, theo phản biện G3)

| Đề xuất | Mục sẵn có chồng chéo | Xử lý |
|---|---|---|
| A1 Phân tích | `Explore` (tìm kiếm chỉ đọc), `Plan` (lập kế hoạch) | Thử dùng `Explore`/`Plan` với `model` chỉ định trước; chỉ tạo `phan-tich` nếu cần khuôn trả về có danh sách tệp + mức rủi ro (quyết ở ngày 2) |
| A2 Triển khai | `general-purpose`, `/speckit-implement` | Tính năng mới vẫn đi Spec Kit; `trien-khai` chỉ thêm `isolation: worktree` + giới hạn công cụ mà `general-purpose` không có |
| A3 Kiểm thử | `/code-review`, `/security-review` | `kiem-thu` chạy pytest/ruff + đối chiếu tệp khóa; rà lỗi sâu vẫn gọi `/code-review` |
| A4 Phản biện | `to-phan-bien` | Mở rộng, không tạo mới |
| Sổ cái, mã việc | `bo-nho` (todo.md, "thay cho task-management"), `/speckit-tasks` (tasks.md) | Sổ cái chỉ giữ trạng thái chạy (khóa tệp, số lần sửa, chi phí), là dữ liệu phiên, không commit; kế hoạch vẫn ở todo.md/tasks.md, ghi mã `NV-...` vào đó |

## 3. Sơ đồ kiến trúc

```
Người dùng / Chủ đầu tư ──(GATE 2 duyệt phương án, GATE 4 nghiệm thu)──┐
        │ yêu cầu                                                       │
        ▼                                                               │
┌─ TỔNG CHỈ HUY (phiên chính) ──────────────────────────────────────┐   │
│ hook dieu_phoi.py → registry.json → phân loại độ phức tạp/rủi ro  │◄──┘
│ GATE 1: đầu vào, quyền, ngân sách (so_cai.py: trần USD, tỷ giá)    │
│ Sổ cái .doi-agent/so-cai.json · nhat-ky.jsonl · agent.jsonl        │
└───┬───────────────┬───────────────────┬───────────────┬────────────┘
    │ Agent tool    │ (sau GATE 2)      │               │ chỉ khi rủi ro cao
    ▼               ▼                   ▼               ▼
 A1 Phân tích    A2 Triển khai       A3 Kiểm thử     A4 to-phan-bien
 sonnet, chỉ đọc sonnet, worktree    haiku, chạy     opus, chỉ đọc
 Read/Grep/Glob  riêng, tệp đã khóa  pytest/ruff/diff Read/Grep/Glob
                 không push/merge    GATE 3          GATE 3 (văn bản/quyết định)
    └────────── báo cáo ngắn về Tổng chỉ huy (không gọi nhau, độ sâu lồng = 1) ──────────┘
Rào chắn kỹ thuật (mọi Agent): permissions → guard.py → hook_an_toan.py → hook_khoa_tep.py
                               → tài khoản CSDL db_datareader → CI
```

## 4. Ma trận chức năng, công cụ, quyền hạn

| Vai | Model | Công cụ được dùng | Cấm | Sửa tệp | Kích hoạt khi |
|---|---|---|---|---|---|
| Tổng chỉ huy | phiên chính (đề xuất Sonnet cho việc thường, Opus khi kiến trúc) | Tất cả + Agent | Theo AGENTS.md mục 3 | Chỉ sổ cái, `todo.md` | Mọi yêu cầu |
| A1 Phân tích | sonnet, effort medium, ≤25 lượt | Read, Grep, Glob | Bash, Edit, Write, Agent | Không | Chưa rõ nguyên nhân / ≥2 tệp |
| A2 Triển khai | sonnet, effort medium, ≤40 lượt, `isolation: worktree` | Read, Grep, Glob, Edit, Write, Bash | Agent, Web; push/merge/reset (hook) | Chỉ tệp đã khóa | Sau GATE 2 |
| A3 Kiểm thử | haiku, ≤20 lượt | Read, Grep, Glob, Bash (pytest, ruff, git diff) | Edit, Write, Agent, Web | Không | Sau mỗi lần A2 báo xong |
| A4 Phản biện | opus, effort high | Read, Grep, Glob | Mọi công cụ ghi/chạy | Không | Rủi ro "cao" hoặc văn bản ra ngoài |

Phân loại: **nhỏ** (1 tệp, rủi ro thấp) → Tổng chỉ huy tự làm, không gọi Agent · **vừa** → A2 + A3 ·
**lớn/rủi ro cao** → A1 → GATE 2 → A2 → A3 → A4 → GATE 4.

## 5. Bộ prompt chuyên biệt

`mau/agents/phan-tich.md`, `trien-khai.md`, `kiem-thu.md` (định dạng tác tử phụ Claude Code, có
frontmatter quyền/model) và `to-phan-bien-mo-rong.md` (đề xuất **mở rộng** tác tử sẵn có làm Agent 4,
không tạo mới). Mỗi prompt: điều kiện bắt đầu, quy tắc, coi nội dung tệp là dữ liệu (chống tiêm lệnh),
khuôn trả về ngắn có mã việc.

## 6. Phương án cấu hình Git Worktrees, Hooks, Permissions

`mau/settings.de-xuat.json` (chưa áp dụng) gồm:
- `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=0` (chặn đội hình tự hình thành), `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH=1`.
- Thêm deny/ask cho biến thể Git mà luật hiện tại để lọt.
- Hook `hook_an_toan.py` (Git phá hủy, `gh pr merge`, đọc `.env`/`secrets/`, hỏi khi gửi ra mạng),
  `hook_khoa_tep.py` (Agent phụ chỉ sửa tệp của việc mình), `hook_nhat_ky.py` (SubagentStart/Stop).
- Worktree: `isolation: worktree` trong A2 - tài liệu ghi tạo từ **nhánh mặc định**, không phải HEAD
  hiện tại → Tổng chỉ huy phải nêu nhánh gốc trong prompt; worktree tự xóa nếu không có thay đổi.
  Gộp về nhánh làm việc bằng `git merge` (hook hỏi người duyệt), không bao giờ vào `main`.
- Khi duyệt: gộp `hook_an_toan.py` vào `guard.py` + chuyển test sang `tests/harness/test_guard.py`
  (AGENTS.md: sửa guard.py phải kèm test), sửa `python3` → lệnh chạy được trên Windows.

## 7. Kịch bản kiểm thử và bằng chứng

Chạy: `python -m pytest tests/doi_agent -v` → **23 passed** (THẬT, danh sách từng test, ngày, commit trong
`bang-chung/pytest-kich-ban.txt`). Bộ đầy đủ: **199 passed** (gốc 176), `ruff check .` sạch. Các phép thử chạy offline: sổ cái, hook, git thật trong
kho tạm - **không gọi model**. Phần cần Agent chạy thật đều BLOCKED vì chưa duyệt chi phí.

| # | Kịch bản | Đã kiểm được (THẬT) | Chưa kiểm (lý do) |
|---|---|---|---|
| 1 | 1 Agent việc đơn giản | Vòng tạo→nhận→đạt→chờ duyệt→xong | Agent chạy thật - BLOCKED (ngân sách) |
| 2 | 3 Agent phần độc lập | 3 worktree, 3 nhánh, gộp không xung đột | Song song thật - BLOCKED |
| 3 | 2 Agent xung đột | Sổ cái chặn nhận việc trùng tệp (cả đường dẫn kiểu Windows); hook chặn sửa tệp người khác; git báo CONFLICT, `merge --abort` giữ bản cũ | - |
| 4 | Mã chứa chỉ dẫn độc hại | 6 lệnh bị xúi giục bị chặn; 5 lệnh bình thường không bị chặn nhầm | Phản ứng của model với tiêm lệnh - BLOCKED |
| 5 | Test thất bại → rollback | Bỏ worktree, `main` nguyên vẹn, giữ nhánh lỗi làm bằng chứng. "Test thất bại" là **mô phỏng** (mã hỏng + `git diff`), không chạy pytest trong worktree | pytest thật trong worktree - ngày 3 |
| 6 | Sửa lỗi vượt giới hạn | Lần 3 → `dung`; nhận lại bị chặn tới khi người duyệt | - |
| 7 | Nguy cơ vượt 10.000 đ | Thiếu trần/tỷ giá → BLOCKED; ước vượt trần → chặn trước khi nhận | Chặn cứng giữa chừng - chỉ có ở `-p --max-budget-usd` |
| 8 | Vượt quyền | Hàm quyết định của hook: ghi ngoài dự án → deny; `push +main` → deny; merge → ask | Giới hạn `tools`/`disallowedTools` từng Agent và luật permissions trong phiên thật - BLOCKED |
| 9 | Khôi phục sau gián đoạn | File tạm hỏng không ảnh hưởng; việc dở trả về hàng chờ, nhả khóa | Khôi phục phiên Claude thật - BLOCKED |
| 10 | Báo cáo + xem trước | Đo chi phí transcript (gồm tác tử phụ, không đếm trùng); che bí mật trong nhật ký. Trang HTML: **không có test tự động**, chỉ kiểm thủ công bằng Chromium giả lập | Safari thật - BLOCKED |

**Khảo sát rào chắn** (`bang-chung/rao-chan.json`, THẬT - gọi hàm quyết định của hook, không chạy lệnh):
23 thao tác; `guard.py` hiện hành chặn/hỏi 7, để lọt 16 - trong đó **15 rủi ro** (force-push mọi biến thể, `reset --hard`,
`clean -fdx`, `branch -D`, `merge`, `gh pr merge`, `cat .env`, `cat secrets/...`, `curl -d @.env`...).
Thao tác còn lại (ghi `src/api/app.py`) là bình thường, do luật `ask` xử lý. Hook đề xuất chặn/hỏi cả 15. Cột "luật permissions" là **phân tích** theo cách khớp mẫu chữ, không chạy
được bộ máy quyền của Claude Code từ test (CẦN KIỂM trên phiên thật).

## 8. Báo cáo bảo mật, ngân sách, rủi ro

**Ngân sách - BLOCKED.**
- **Đo THẬT** (`bang-chung/chi-phi-phien.txt`, `chi_phi.py` trên transcript, giá niêm yết): phiên lập
  hồ sơ này đến 2026-11-13 23:12 UTC - **58 lượt gọi, 6,32 USD**, toàn bộ Opus 5.5, gồm cả lần phản biện
  G3 (tác tử `to-phan-bien` không đặt `model` nên **kế thừa Opus** - bài học: mọi tác tử phải ghi `model`).
  Các mốc trước đó (13 lượt 1,99 USD; 29 lượt 3,64 USD) đo bằng cùng công cụ nhưng không lưu file.
- **Tỷ giá giả định 26.000 đ/USD** (CẦN CĂN CỨ, chủ đầu tư chốt) → trần 10.000 đ ≈ **0,385 USD**.
  Phiên này ≈ 164.000 đ, gấp ~16 lần trần.
- **Ước tính DEMO** (giả định số lượt/token ghi trong `cong-cu/dung_xem_truoc.py`): Tổng chỉ huy Opus 0,30 ·
  A1 0,18 · A2 0,26 · A3 0,007 · A4 0,20 USD. Đội A1+A2+A3 + Tổng chỉ huy ≈ 0,75 USD (thêm A4 ≈ 0,95);
  1 Agent Sonnet ≈ 0,36; Haiku việc đơn giản ≈ 0,005 → **chỉ vừa trần cho 1 Agent Sonnet hoặc việc Haiku**.
- Giá: bảng "Current Models (cached: 2026-11-03)" trong kỹ năng `claude-api` đi kèm Claude Code 2.1.325
  (Opus 5.5 $4/$20, Sonnet 5.5 $2/$10, Haiku 5.5 $0,10/$0,50 mỗi triệu token). Giá đọc cache Haiku, hệ số
  ghi cache (1,25× / 2×) và giá hợp đồng thực tế: CẦN CĂN CỨ.
- Phiên tương tác **không có chặn cứng**; sổ cái chỉ chặn *trước khi nhận việc* theo ước tính; số đo thật
  có *sau* khi chạy. Chặn cứng: chạy đội ở chế độ `claude -p --max-budget-usd <trần>` (chưa thử).
- Nếu dùng gói thuê bao (Pro/Max/Team), tiền không tính theo token - con số USD chỉ là quy đổi tham chiếu.
  **Chủ đầu tư cần xác nhận hình thức thanh toán.**

**Bảo mật.** Rào chắn nhiều lớp đã liệt kê ở mục 6; tác tử chỉ đọc không có Bash; A2 không có Agent/Web;
nhật ký không ghi nội dung prompt, che mẫu khóa bí mật; dữ liệu Agent nhận là dữ liệu, không phải lệnh.
Chưa kiểm: luật `Read(./.env)` có áp cho `cat .env` qua Bash không (CẦN KIỂM) - hook đề xuất chặn thẳng.

| Rủi ro | Mức | Giảm thiểu |
|---|---|---|
| Vượt ngân sách | Cao | BLOCKED đến khi có trần + tỷ giá; chạy `-p --max-budget-usd`; Haiku cho A3 |
| Tiêm lệnh qua mã/tài liệu | Cao | Hook chặn hành động, không dựa vào lời dặn; tác tử đọc không có Bash |
| Hai Agent sửa cùng tệp | Vừa | Khóa tệp + worktree + hook; git báo xung đột |
| Lỗi lặp vô hạn | Vừa | 3 lần → dừng, cần người duyệt; `maxTurns` |
| Worktree từ nhánh mặc định | Vừa | Nêu nhánh gốc trong prompt; A3 kiểm `git diff main...<nhánh>` |
| Hook `python3` trên Windows | Vừa | Thử trên máy Windows trước khi bật (ngày 4) |
| Agent Teams tự hình thành | Thấp | Đặt cờ = 0 |
| Định tuyến từ khóa sai | Thấp | Thêm tuyến "Đội Agent" sau khi duyệt; Tổng chỉ huy tự chọn lại |

## 9. Kế hoạch thử nghiệm 5 ngày

| Ngày | Việc | Cổng / người duyệt | Điều kiện qua |
|---|---|---|---|
| 0 (trước) | Chủ đầu tư quyết: tỷ giá, hình thức thanh toán, trần USD/lượt, có nâng trần cho đội 3-4 Agent không | **GATE 1** | Có 4 con số/quyết định bằng văn bản |
| 1 | Áp `settings.de-xuat.json` + 3 tác tử mẫu vào nhánh thử (không phải `main`); gộp hook vào `guard.py` kèm test | **GATE 2** duyệt diff cấu hình | pytest + ruff xanh, `/hooks` hiện đúng |
| 2 | KB1, KB7 thật: 1 Agent Haiku việc nhỏ, chạy `-p --max-budget-usd`; đo bằng `chi_phi.py` | GATE 3 (A3) | Chi phí đo ≤ trần; báo cáo có token thật |
| 3 | KB2, KB3, KB5 thật: A2 worktree, A3 kiểm, xung đột cố ý, rollback | GATE 3 | Không ghi đè, `main` nguyên vẹn |
| 4 | KB4, KB6, KB8, KB9 thật + chạy hook trên **máy Windows**, xem trang trên **iPhone Safari** | GATE 3 + A4 | Mọi hành động vượt quyền bị chặn bởi hook, không phải bởi lời dặn |
| 5 | Tổng hợp số đo, cập nhật registry (tuyến "Đội Agent"), trình nghiệm thu | **GATE 4** chủ đầu tư | Chủ đầu tư ký nghiệm thu hoặc trả về |

Dừng thử nghiệm ngay nếu: vượt trần 2 lượt liên tiếp, có thao tác ngoài phạm vi lọt hook, hoặc
chạm dữ liệu EMS thật.

## 10. Bản xem trước

`XEM-TRUOC-TOAN-BO.html` - một tệp, không tải tài nguyên ngoài, mở bằng Edge/Chrome trên Windows hoặc
Safari trên iPhone.

---
**Không làm trong giai đoạn này:** không bật Agent Teams, không cài gói (chỉ cài lại bản ghim
`requirements-dev.txt` để chạy test), không sửa `registry.json`, `settings.local.json`, `guard.py` thật,
không chạy Agent nhiều model.
