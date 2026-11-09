"""Kiểm kê tĩnh kho anthropics/knowledge-work-plugins (chỉ đọc, không chạy mã nguồn từ kho).

Cách dùng: python3 -I inventory.py <thư_mục_kho> <tệp_json_đầu_ra>
"""
import os
import re
import json
import hashlib
import sys
from collections import Counter

ROOT = sys.argv[1]
OUT = sys.argv[2]


def fm(text):
    m = re.match(r'^---\n(.*?)\n---', text, re.S)
    d = {}
    if not m:
        return d
    cur = None
    for line in m.group(1).split('\n'):
        mm = re.match(r'^([A-Za-z_-]+):\s*(.*)$', line)
        if mm:
            cur = mm.group(1)
            d[cur] = mm.group(2).strip().strip('"\'')
        elif cur and line.startswith((' ', '\t')):
            d[cur] = (d[cur] + ' ' + line.strip()).strip()
    return d


RISK = re.compile(r'(curl |wget |Invoke-WebRequest|requests\.|fetch\(|https?://|eval\(|subprocess|os\.system|base64|api[_ ]?key|token|password|secret|ignore (all|previous)|system prompt)', re.I)
rows = []
comps = []
for dp, dn, fn in os.walk(ROOT):
    if os.sep + '.git' in dp or os.sep + '.github' in dp:
        continue
    rel = os.path.relpath(dp, ROOT)
    parts = rel.split(os.sep)
    plugin = parts[0] if parts[0] != '.' else '(root)'
    for f in fn:
        p = os.path.join(dp, f)
        rp = os.path.relpath(p, ROOT)
        slash = '/' + rp.replace(os.sep, '/')
        if f == 'SKILL.md':
            t = open(p, encoding='utf-8', errors='replace').read()
            d = fm(t)
            hits = sorted(set(m.group(0).lower() for m in RISK.finditer(t)))[:8]
            rows.append(dict(kind='skill', plugin=plugin, path=rp,
                             name=d.get('name', os.path.basename(dp)),
                             description=d.get('description', '')[:300],
                             bytes=len(t.encode()), lines=t.count('\n'),
                             sha256=hashlib.sha256(t.encode()).hexdigest()[:16],
                             has_scripts=os.path.isdir(os.path.join(dp, 'scripts')),
                             has_refs=os.path.isdir(os.path.join(dp, 'references')),
                             allowed_tools=d.get('allowed-tools', ''), risk_hits=hits))
        elif '/commands/' in slash and f.endswith('.md'):
            t = open(p, encoding='utf-8', errors='replace').read()
            d = fm(t)
            comps.append(dict(kind='command', plugin=plugin, path=rp, name=f[:-3],
                              description=d.get('description', '')[:200], bytes=len(t.encode())))
        elif '/agents/' in slash and f.endswith('.md'):
            t = open(p, encoding='utf-8', errors='replace').read()
            d = fm(t)
            comps.append(dict(kind='agent', plugin=plugin, path=rp, name=d.get('name', f[:-3]),
                              description=d.get('description', '')[:200], bytes=len(t.encode())))
        elif f == '.mcp.json':
            try:
                j = json.load(open(p))
            except Exception:
                j = {}
            srv = j.get('mcpServers', j)
            if isinstance(srv, dict):
                for sname, sv in srv.items():
                    if not isinstance(sv, dict):
                        continue
                    target = sv.get('url') or (str(sv.get('command', '')) + ' ' + ' '.join(map(str, sv.get('args', []) or [])))
                    comps.append(dict(kind='mcp', plugin=plugin, path=rp, name=sname,
                                      description=str(target)[:200], bytes=0))
        elif f == 'plugin.json' and '.claude-plugin' in rp:
            try:
                j = json.load(open(p))
            except Exception:
                j = {}
            comps.append(dict(kind='plugin', plugin=plugin, path=rp, name=j.get('name', plugin),
                              description=(j.get('description') or '')[:200], bytes=0,
                              version=j.get('version', ''), author=str(j.get('author', ''))[:80]))
        elif '/hooks/' in slash or f == 'hooks.json':
            comps.append(dict(kind='hook', plugin=plugin, path=rp, name=f, description='',
                              bytes=os.path.getsize(p)))

json.dump(dict(skills=rows, others=comps), open(OUT, 'w'), ensure_ascii=False, indent=1)
print('skills', len(rows), 'others', dict(Counter(c['kind'] for c in comps)))
print(dict(Counter(r['plugin'] for r in rows)))
print('with scripts', sum(r['has_scripts'] for r in rows), 'with refs', sum(r['has_refs'] for r in rows))
print('risk-flagged', sum(1 for r in rows if r['risk_hits']))
