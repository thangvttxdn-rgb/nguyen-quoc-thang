"""Tạo manifest SHA-256 cho toàn bộ tệp trong thư mục hồ sơ (trừ chính manifest).

Cách dùng: python3 -I build_manifest.py <thư_mục_hồ_sơ>
"""
import hashlib
import json
import os
import sys

ROOT = sys.argv[1]
entries = []
for dp, dn, fn in os.walk(ROOT):
    for f in sorted(fn):
        p = os.path.join(dp, f)
        rel = os.path.relpath(p, ROOT).replace(os.sep, '/')
        if rel == '12-MANIFEST-SHA256.json':
            continue
        h = hashlib.sha256(open(p, 'rb').read()).hexdigest()
        entries.append({'path': rel, 'sha256': h, 'bytes': os.path.getsize(p)})
entries.sort(key=lambda e: e['path'])
doc = {
    'repo_khao_sat': 'https://github.com/anthropics/knowledge-work-plugins',
    'commit_khao_sat': 'e050c2ec856373787143d7057663a6ebd1277df3',
    'so_tep': len(entries),
    'tep': entries,
}
with open(os.path.join(ROOT, '12-MANIFEST-SHA256.json'), 'w', encoding='utf-8') as f:
    json.dump(doc, f, ensure_ascii=False, indent=1)
print('so_tep', len(entries))
