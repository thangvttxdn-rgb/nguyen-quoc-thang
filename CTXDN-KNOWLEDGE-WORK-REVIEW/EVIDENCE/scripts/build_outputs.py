"""Sinh bảng kê CSV và kiểm thử cấu trúc offline từ tệp kiểm kê inv.json.

Cách dùng: python3 -I build_outputs.py <inv.json> <thư_mục_đầu_ra>
Không gọi mạng, không gọi model, không ghi ngoài thư mục đầu ra.
"""
import csv
import json
import os
import sys
from collections import defaultdict

INV, OUTDIR = sys.argv[1], sys.argv[2]
data = json.load(open(INV, encoding='utf-8'))
skills = data['skills']
others = data['others']

# Quyết định sơ bộ của Tổ 1 cho các ứng viên đã xét (chỉ những mục có bằng chứng đọc toàn văn hoặc rà soát có căn cứ).
DEC = {
    ('operations', 'process-doc'): ('BLOCKED', 'Chờ đối chiếu Registry (G0.2); mẫu Việt hóa UV-02 đã làm'),
    ('operations', 'risk-assessment'): ('BLOCKED', 'Chờ đối chiếu Registry; khung 3x3 chung, không thay thế tiêu chuẩn rủi ro nội bộ'),
    ('productivity', 'memory-management'): ('LOẠI', 'Trùng chức năng với cơ chế MEMORY.md / todo.md đã có trong repo (đã kiểm chứng)'),
    ('productivity', 'task-management'): ('LOẠI', 'Trùng chức năng với todo.md đã có trong repo (đã kiểm chứng)'),
    ('data', 'build-dashboard'): ('BLOCKED', 'Tải Chart.js từ CDN jsdelivr; vi phạm yêu cầu offline nếu dùng nguyên xi'),
    ('finance', 'financial-statements'): ('BLOCKED', 'Chưa có căn cứ chuẩn kế toán áp dụng cho CTXĐN'),
    ('finance', 'audit-support'): ('BLOCKED', 'Chưa có căn cứ kiểm soát nội bộ/SOX áp dụng cho CTXĐN'),
    ('finance', 'sox-testing'): ('BLOCKED', 'Chưa có căn cứ kiểm soát nội bộ/SOX áp dụng cho CTXĐN'),
}

rows = []
for i, r in enumerate(skills, 1):
    key = (r['plugin'], r['name'])
    dec, why = DEC.get(key, ('CHƯA XÉT', 'Chưa đọc toàn văn; chỉ có kiểm kê tĩnh'))
    if r['plugin'] in ('partner-built',):
        dec, why = 'BLOCKED', 'Thành phần bên thứ ba; giấy phép riêng từng plugin chưa xác minh'
    elif r['plugin'] in ('sales', 'small-business'):
        dec, why = 'LOẠI', 'Ngoài phạm vi nghiệp vụ CTXĐN (bán hàng/kinh doanh nhỏ)'
    rows.append(dict(
        ID=f'KWP-{i:03d}', Ten=r['name'], Plugin=r['plugin'], Duong_dan=r['path'],
        Dong=r['lines'], Bytes=r['bytes'], SHA256_16=r['sha256'],
        Co_scripts='Có' if r['has_scripts'] else 'Không', Co_references='Có' if r['has_refs'] else 'Không',
        Co_rui_ro_tu_khoa='; '.join(r['risk_hits']), Mo_ta=r['description'][:160].replace('\n', ' '),
        Quyet_dinh_so_bo=dec, Ly_do=why))

os.makedirs(OUTDIR, exist_ok=True)
with open(os.path.join(OUTDIR, '02-DANH-MUC-SKILLS.csv'), 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader()
    w.writerows(rows)

# Thành phần khác: command, agent, plugin, mcp, hook
oth_rows = []
for j, o in enumerate(others, 1):
    oth_rows.append(dict(ID=f'KWP-O{j:03d}', Loai=o['kind'], Ten=o['name'], Plugin=o['plugin'],
                         Duong_dan=o['path'], Mo_ta=(o.get('description') or '')[:160].replace('\n', ' '),
                         Quyet_dinh_so_bo=('BLOCKED' if o['kind'] == 'mcp' else 'CHƯA XÉT'),
                         Ly_do=('Kết nối SaaS bên ngoài: cần phê duyệt riêng, có nguy cơ gửi dữ liệu ra ngoài' if o['kind'] == 'mcp' else '')))
with open(os.path.join(OUTDIR, 'EVIDENCE', 'inventory', 'thanh-phan-khac.csv') if False else os.path.join(OUTDIR, '02b-THANH-PHAN-KHAC.csv'), 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(oth_rows[0].keys()))
    w.writeheader()
    w.writerows(oth_rows)

# Kiểm thử cấu trúc offline (G2 nhóm 16/17): tên và mô tả có mặt, tên khớp thư mục, không rỗng.
tests = {'T-S1 có trường name': 0, 'T-S2 có trường description': 0, 'T-S3 name khớp tên thư mục': 0, 'T-S4 SKILL.md đọc được (có dòng)': 0}
fails = []
for r in skills:
    if r['name']:
        tests['T-S1 có trường name'] += 1
    else:
        fails.append(('T-S1', r['path']))
    if r['description']:
        tests['T-S2 có trường description'] += 1
    else:
        fails.append(('T-S2', r['path']))
    folder = os.path.basename(os.path.dirname(r['path']))
    if r['name'] == folder:
        tests['T-S3 name khớp tên thư mục'] += 1
    else:
        fails.append(('T-S3', r['path'] + f" (name={r['name']})"))
    if r['lines'] > 0:
        tests['T-S4 SKILL.md đọc được (có dòng)'] += 1
    else:
        fails.append(('T-S4', r['path']))

# Trùng tên giữa các plugin (G0.1/G2.2 nhóm 15: trùng lặp nội bộ)
byname = defaultdict(list)
for r in skills:
    byname[r['name']].append(r['plugin'])
dups = {k: v for k, v in byname.items() if len(v) > 1}

summary = dict(tong_skill=len(skills), tong_command=sum(1 for o in others if o['kind'] == 'command'),
               tong_agent=sum(1 for o in others if o['kind'] == 'agent'),
               tong_plugin=sum(1 for o in others if o['kind'] == 'plugin'),
               tong_mcp_entries=sum(1 for o in others if o['kind'] == 'mcp'),
               tests=tests, so_loi_cau_truc=len(fails), loi=fails[:20],
               trung_ten_noi_bo=dups, so_nhom_trung_ten=len(dups),
               co_scripts=sum(1 for r in skills if r['has_scripts']),
               co_rui_ro_tu_khoa=sum(1 for r in skills if r['risk_hits']))
json.dump(summary, open(os.path.join(OUTDIR, 'EVIDENCE', 'inventory', 'tom-tat-kiem-thu.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(json.dumps({k: v for k, v in summary.items() if k != 'loi'}, ensure_ascii=False, indent=1))
print('loi:', fails[:5])
