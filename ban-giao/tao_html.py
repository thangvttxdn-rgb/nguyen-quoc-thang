"""Sinh XEM-TRUOC-TOAN-BO.html độc lập (không CDN) từ các tệp trong ban-giao/.

Chạy: python ban-giao/tao_html.py
"""

import html
from pathlib import Path

B = Path(__file__).parent
esc = html.escape


def doc(ten):
    return (B / ten).read_text(encoding="utf-8")


THAT, DEMO, BLOCK = "THẬT", "DEMO", "BLOCKED"
TESTS = [
    ("T1", "Thư mục gốc dự án", "PASS", THAT, "toplevel nguyen-quoc-thang, HEAD 6a57a7f"),
    ("T2", "Hai tệp đúng vị trí", "PASS", THAT, "AGENTS.md, CLAUDE.md ở gốc repo"),
    ("T3", "Đường dẫn nhập @", "PASS", THAT, "3/3 import trỏ tới tệp tồn tại"),
    ("T4", "Claude Code nạp hướng dẫn", "PASS", THAT,
     "Phiên khởi động lại đã nạp bản sau sửa qua CLAUDE.md"),
    ("T5", "Trùng lặp / mâu thuẫn", "PASS", THAT, "Skill Node.js ↔ Python: thêm mục 9"),
    ("T6", "Kiến trúc ↔ mã nguồn", "PASS", THAT, "app.py:22 FastAPI; connection.py:117"),
    ("T7", "Không đổi mã nghiệp vụ", "PASS", THAT, "diff src/tests/examples/deploy/docs rỗng"),
    ("T8", "Skills/Agent ngoài phạm vi", "PASS", THAT, "Skill +40/−0; hook, settings không đổi"),
    ("T9", "Diff, sao lưu, khôi phục", "PASS", THAT, "sao lưu == 6a57a7f"),
    ("T10a", "ruff check . (0.16.8)", "PASS", THAT, "All checks passed!"),
    ("T10b", "pytest -q toàn bộ", "PASS 121/121", DEMO, "SQLite mẫu; trước đây BLOCKED"),
    ("T10c", "SQL Server thật", "BLOCKED", BLOCK, "Không có SQL Server (ngoài phạm vi)"),
]
CHANGES = [
    ("AGENTS.md", "Khối Phạm vi (chung CTXĐN / riêng dự án)"),
    ("AGENTS.md", "FastAPI, Python ≥ 3.11; pyodbc, chưa dùng SQLAlchemy"),
    ("AGENTS.md", "Bổ sung thư mục; lint ruff check . trùng CI"),
    ("AGENTS.md", "Ghi chú python -m pytest; mục 4a Skills; DONE cần requirements-dev"),
    ("MEMORY.md", "Chú thích 2 tham chiếu không tồn tại; 2 ghi nhận 12/11"),
    ("todo.md", "Mục tiêu 12/11 và trạng thái"),
    ("SKILL.md", "phat-hanh-ems: ghi chú chọn quy trình + mục 9 Python/IIS PhanCong"),
    ("CLAUDE.md", "Không đổi (đã có @AGENTS.md)"),
    ("ban-giao/", "Báo cáo, hướng dẫn, HTML, sao lưu, bằng chứng, ZIP"),
]


def row(cells):
    return "<tr>" + "".join(f"<td>{c}</td>" for c in cells) + "</tr>"


def badge(t):
    cls = {THAT: "real", DEMO: "demo", BLOCK: "block"}[t]
    return f'<span class="b {cls}">{t}</span>'


def diff_html(text):
    out = []
    for line in text.splitlines():
        c = ""
        if line.startswith("+") and not line.startswith("+++"):
            c = "add"
        elif line.startswith("-") and not line.startswith("---"):
            c = "del"
        out.append(f'<span class="{c}">{esc(line)}</span>')
    return "\n".join(out)


tests = "".join(row([t[0], esc(t[1]), esc(t[2]), badge(t[3]), esc(t[4])]) for t in TESTS)
changes = "".join(row([f"<code>{f}</code>", esc(d)]) for f, d in CHANGES)

CSS = """
:root{--bg:#f7f7f5;--fg:#1d1d1b;--mut:#666;--card:#fff;--line:#ddd;
--real:#1a7f37;--demo:#9a6700;--block:#cf222e;--add:#e6ffec;--del:#ffebe9}
@media (prefers-color-scheme:dark){:root{--bg:#161616;--fg:#eee;--mut:#aaa;--card:#202020;
--line:#3a3a3a;--add:#12361f;--del:#4a1c1c}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);
font:15px/1.5 -apple-system,"Segoe UI",Roboto,Arial,sans-serif;-webkit-text-size-adjust:100%}
main{max-width:960px;margin:0 auto;padding:16px}
h1{font-size:1.4rem;margin:.2em 0} h2{font-size:1.1rem;margin-top:1.6em}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px 14px}
.status{border-left:5px solid var(--real)}
.tw{overflow-x:auto;-webkit-overflow-scrolling:touch}
table{border-collapse:collapse;width:100%;font-size:14px}
td,th{border-bottom:1px solid var(--line);padding:6px 8px;text-align:left;vertical-align:top}
.b{display:inline-block;padding:1px 8px;border-radius:99px;color:#fff;
font-size:12px;font-weight:600}
.real{background:var(--real)} .demo{background:var(--demo)} .block{background:var(--block)}
pre{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:10px;
overflow-x:auto;font-size:12px;line-height:1.4;white-space:pre}
pre .add{background:var(--add);display:block} pre .del{background:var(--del);display:block}
details{margin:.6em 0} summary{cursor:pointer;font-weight:600}
.mut{color:var(--mut);font-size:13px}
"""

page = f"""<!doctype html>
<html lang="vi"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Nghiệm thu AGENTS.md</title>
<style>{CSS}</style></head><body><main>
<h1>Tích hợp AGENTS.md &amp; CLAUDE.md – Nghiệm thu</h1>
<p class="mut">Repo thangvttxdn-rgb/nguyen-quoc-thang ·
nhánh claude/integrate-agents-claude-md-tsvkvq · gốc 6a57a7f · 12/11/2026</p>
<div class="card status"><b>Trạng thái: HOÀN THÀNH phạm vi tích hợp trên repo thật.</b><br>
pytest 121/121, ruff sạch. Đã commit, push, mở PR vào main (chưa merge, không triển khai).
Còn {badge(BLOCK)} thử SQL Server thật – ngoài phạm vi, môi trường không có.</div>
<p>Chú giải: {badge(THAT)} chạy trên repo thật · {badge(DEMO)} dữ liệu mẫu SQLite ·
{badge(BLOCK)} chưa đủ điều kiện.</p>

<h2>Kết quả kiểm thử</h2>
<div class="tw"><table>
<tr><th>Mã</th><th>Kiểm thử</th><th>Kết quả</th><th>Nhãn</th><th>Bằng chứng</th></tr>
{tests}</table></div>

<h2>Mâu thuẫn đã xử lý</h2>
<div class="card">Skill <code>phat-hanh-ems</code> viết cho EMS Node.js; repo là Python/FastAPI.
Giữ nguyên phần Node.js (có thể là hệ khác), thêm mục 9 cho repo này.<br>
Không tìm thấy bộ tệp 12/11 trước đó nên “8 vị trí” được xác định lại từ mã nguồn.</div>

<h2>Danh sách thay đổi</h2>
<div class="tw"><table><tr><th>Tệp</th><th>Thay đổi</th></tr>{changes}</table></div>

<h2>Git diff (so với 6a57a7f)</h2>
<pre>{diff_html(doc("thay-doi.diff"))}</pre>

<h2>Bằng chứng lệnh</h2>
<details><summary>bang-chung.txt</summary><pre>{esc(doc("bang-chung.txt"))}</pre></details>

<h2>Nội dung tệp</h2>
<details><summary>CLAUDE.md</summary><pre>{esc(doc("CLAUDE.md"))}</pre></details>
<details><summary>AGENTS.md</summary><pre>{esc(doc("AGENTS.md"))}</pre></details>
<p class="mut">Tệp độc lập, không dùng CDN hay mạng.</p>
</main></body></html>
"""
(B / "XEM-TRUOC-TOAN-BO.html").write_text(page, encoding="utf-8")
print("ok", len(page))
