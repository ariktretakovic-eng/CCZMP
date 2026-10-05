# -*- coding: utf-8 -*-
"""Generate INDEX.md -- the human-readable map of the project."""
import os, sys, sqlite3, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
DBP = os.path.join(HERE, 'anomaly.db')
C = sqlite3.connect(DBP)
C.row_factory = sqlite3.Row


def one(sql, *a):
    return C.execute(sql, a).fetchone()[0]


def table(sql, *a):
    rows = C.execute(sql, a).fetchall()
    if not rows:
        return '_(empty)_\n'
    cols = list(rows[0].keys())
    w = [max(len(c), *(len(str(r[c])) for r in rows)) for c in cols]
    out = ['| ' + ' | '.join(cols) + ' |', '|' + '|'.join('-' * (x + 2) for x in w) + '|']
    for r in rows:
        out.append('| ' + ' | '.join(str(r[c]) for c in cols) + ' |')
    return '\n'.join(out) + '\n'


def table2(*spec):
    """table2('col', 'col', ..., [[row], ...]) -> markdown table"""
    names, data = spec[:-1], spec[-1]
    if not data:
        return '_(empty)_\n'
    w = [max(len(c), *(len(str(r[i])) for r in data)) for i, c in enumerate(names)]
    out = ['| ' + ' | '.join(n.ljust(w[i]) for i, n in enumerate(names)) + ' |',
           '|' + '|'.join('-' * (x + 2) for x in w) + '|']
    for r in data:
        out.append('| ' + ' | '.join(str(r[i]).ljust(w[i]) for i in range(len(names))) + ' |')
    return '\n'.join(out) + '\n'


L = []
A = L.append

A('# Stalker Anomaly 1.5.1 — project index\n')
A('Generated %s by `_index/report.py`. Rebuild with `python _index/build.py`.\n'
  % datetime.date.today().isoformat())
A('Everything in this project was *not* read into the model context. Instead the whole tree is '
  'walked once, parsed, and stored as a queryable graph in `_index/anomaly.db`; the assistant '
  'queries that database on demand and only ever pulls a few dozen rows.\n')

A('## 1. What is in the install\n')
A('| metric | value |')
A('|---|---|')
for k, lbl in (('files', 'files indexed'), ('dirs', 'directories'),
               ('symbols', 'symbols (config sections, script functions, XML nodes)'),
               ('ltx_sections', '&nbsp;&nbsp;of which LTX config sections'),
               ('script_fns', '&nbsp;&nbsp;of which script functions / methods'),
               ('xml_nodes', '&nbsp;&nbsp;of which XML nodes'),
               ('edges', 'graph edges'),
               ('edges_to_file', 'edges resolved to another file'),
               ('edges_to_symbol', 'edges resolved to another symbol'),
               ('files_referenced', 'files referenced by something else'),
               ('files_referencing', 'files that reference something else'),
               ('files_no_real_link', 'files with no semantic link in either direction')):
    A('| %s | %s |' % (lbl, format(int(one("SELECT v FROM meta WHERE k=?", k)), ',')))
A('')

A('### Size by area\n')
A(table("SELECT grp, COUNT(*) files, ROUND(SUM(size)/1048576.0,1) mb FROM files "
        "GROUP BY grp ORDER BY SUM(size) DESC"))
A('### Size by file type\n')
A(table("SELECT COALESCE(NULLIF(ext,''),'(none)') ext, COUNT(*) files, "
        "ROUND(SUM(size)/1048576.0,1) mb FROM files GROUP BY ext ORDER BY files DESC LIMIT 25"))

A('\n## 2. How the game is laid out\n')
A('The shipped build is packed: `db/*.db*` are X-Ray archives. `tools/converter.exe -unpack` '
  'has already expanded them into `tools/_unpacked/`, which is where the real content lives.\n')
rows = C.execute("SELECT dir, COUNT(*) n, SUM(size) s FROM files "
                 "WHERE dir LIKE 'tools/_unpacked/%' GROUP BY dir").fetchall()


def subtree(prefix, depth):
    agg = {}
    for r in rows:
        d = r['dir']
        if not d.startswith(prefix):
            continue
        rest = d[len(prefix):]
        if not rest:
            continue
        parts = rest.split('/')
        key = prefix + '/'.join(parts[:depth])
        a = agg.setdefault(key, [0, 0])
        a[0] += r['n']
        a[1] += r['s']
    return agg


unp = subtree('tools/_unpacked/', 1)
A(table2('area', 'files', 'mb',
         [[k.replace('tools/_unpacked/', ''), v[0], round(v[1] / 1048576.0, 1)]
          for k, v in sorted(unp.items(), key=lambda x: -x[1][1])]))
A('The semantic core — the part a modder actually edits — is much smaller than the install:\n')
A(table("SELECT ext, COUNT(*) files, ROUND(SUM(size)/1024.0,1) kb FROM files "
        "WHERE grp LIKE 'unpacked/configs%' OR grp LIKE 'unpacked/scripts%' "
        "GROUP BY ext ORDER BY files DESC"))
cfg = subtree('tools/_unpacked/configs/', 1)
A('Breakdown of `tools/_unpacked/configs`, the tree a mod actually edits:\n')
A(table2('subtree', 'files', 'kb',
         [[k.replace('tools/_unpacked/configs/', ''), v[0], round(v[1] / 1024.0, 1)]
          for k, v in sorted(cfg.items(), key=lambda x: -x[1][1])]))

A('\n## 3. Levels\n')
A('Each level folder becomes a graph node, so a level can be traced to its spawn data, AI, '
  'lightmaps, meshes and every config that mentions it.\n')
A(table("SELECT s.name AS level, COUNT(DISTINCT f.id) files, ROUND(SUM(f.size)/1048576.0,1) mb, "
        "(SELECT COUNT(*) FROM edges e2 WHERE e2.dst_sym=s.id AND e2.type='param') cfg_mentions "
        "FROM symbols s JOIN edges e ON e.src_sym=s.id JOIN files f ON f.id=e.dst_file "
        "WHERE s.kind='level' AND e.type='level_contains' GROUP BY s.id "
        "ORDER BY SUM(f.size) DESC"))

A('\n## 4. Relation types\n')
A(table("SELECT type, COUNT(*) edges, COUNT(DISTINCT src_file) from_files, "
        "COUNT(DISTINCT dst_file) to_files, COUNT(DISTINCT dst_sym) to_symbols, "
        "ROUND(100.0*COUNT(CASE WHEN dst_file IS NOT NULL OR dst_sym IS NOT NULL THEN 1 END)"
        "/COUNT(*),1) AS resolved_pct FROM edges GROUP BY type ORDER BY edges DESC"))
A('| type | meaning |')
A('|---|---|')
A('| `include` | `#include` directive in a config |')
A('| `inherit` | LTX `[section]:parent` inheritance |')
A('| `param` | a single `key = value` in a config; resolved to a file or a section when it points at one |')
A('| `call` | script function call resolved to its definition |')
A('| `call_dyn` | method call `:name()` resolved through the global symbol table |')
A('| `binref` | readable string recovered from a binary container (`.spawn`, `.ai`, `.ogf`, ...) |')
A('| `xml_parent` | XML element nested in another |')
A('| `level_contains` | file belongs to a level |')
A('| `contain` | file belongs to a folder |')
A('| `same_stem` | files sharing a base name, e.g. `w_ak74.ltx` / `w_ak74.ogf` / icon atlas |')

A('\n## 5. What the index resolves\n')
A(table("SELECT type, COUNT(*) total, COUNT(dst_file) to_file, COUNT(dst_sym) to_symbol, "
        "COUNT(dst_name) kept_as_text FROM edges WHERE type NOT IN ('contain','same_stem') "
        "GROUP BY type ORDER BY total DESC"))
A('The largest LTX keys by how many of their values resolved to a real file or section '
  '(this is the item/weapon/creature -> asset wiring):\n')
A(table("SELECT key, COUNT(*) occurrences, COUNT(dst_file) to_file, COUNT(dst_sym) to_section "
        "FROM edges WHERE type='param' GROUP BY key "
        "ORDER BY (COUNT(dst_file)+COUNT(dst_sym)) DESC LIMIT 20"))
A('Text that could not be resolved is still stored, so `q.py grep` can find it:\n')
A(table("SELECT raw AS unresolved_value, COUNT(*) n FROM edges "
        "WHERE type='param' AND dst_file IS NULL AND dst_sym IS NULL "
        "GROUP BY raw ORDER BY n DESC LIMIT 15"))

A('\n## 6. Files with no named reference\n')
A('These are real, not a parse failure. The X-Ray sound engine loads whole banks by directory '
  'scan rather than by name — `sounds/ambient/**` is mixed at random by the ambience engine, '
  'and `sounds/characters_voice/scenario/<level>/**` is sampled per level — so no config line '
  'ever mentions an individual file in there. The same holds for LOD chains packed inside a '
  'single `.dds`, and for the vanilla content this heavily modded install no longer ships. '
  'Each such file is still attached to its folder through a `contain` edge, and its folder is '
  'the semantic unit the engine actually loads.\n')
A(table("SELECT ext, COUNT(*) files, ROUND(SUM(size)/1048576.0,1) mb FROM files f "
        "WHERE NOT EXISTS (SELECT 1 FROM edges e WHERE e.dst_file=f.id "
        "AND e.type NOT IN ('contain','same_stem')) "
        "AND NOT EXISTS (SELECT 1 FROM edges e WHERE e.src_file=f.id "
        "AND e.type NOT IN ('contain','same_stem')) GROUP BY ext ORDER BY files DESC LIMIT 12"))
A('Largest unreferenced areas, which is where engine-side directory scanning takes over:\n')
A(table("SELECT substr(dir,20) area, COUNT(*) files, ROUND(SUM(size)/1048576.0,1) mb FROM files f "
        "WHERE NOT EXISTS (SELECT 1 FROM edges e WHERE e.dst_file=f.id "
        "AND e.type NOT IN ('contain','same_stem')) "
        "AND NOT EXISTS (SELECT 1 FROM edges e WHERE e.src_file=f.id "
        "AND e.type NOT IN ('contain','same_stem')) "
        "GROUP BY dir ORDER BY files DESC LIMIT 12"))

A('\n## 7. Querying the index\n')
A('```')
A('cd _index')
A('python q.py stats              # headline numbers')
A('python q.py stats table        # edges per relation type')
A('python q.py tree tools/_unpacked/configs   # directory rollup')
A('python q.py ls    <file>       # sections / functions defined in a file')
A('python q.py show  <section|id> # full picture: body, parents, params, users')
A('python q.py refs  <file>       # what this file points at')
A('python q.py uses  <file>       # what points at this file')
A('python q.py chain <file> -d 3  # transitive dependencies')
A('python q.py rchain <section>   # transitive reverse dependencies')
A('python q.py grep  <text>       # search params, binary refs, symbols, paths')
A('python q.py levels             # per-level rollup')
A('python q.py orphans            # files nothing links to')
A('```')
A('Rebuild a single stage without redoing the whole run:\n')
A('```')
A('python build.py ltx resolve params stats   # e.g. after editing the LTX parser')
A('python build.py scan ltx script xml misc bin name atlas levels resolve params links stats')
A('```')
A('Stages: `scan ltx script xml misc bin name atlas levels resolve params prune links '
  'vacuum stats`.\n')

A('## 8. Schema\n')
A('```sql')
A('files(id, path UNIQUE, dir, name, stem, ext, size, grp, lang, bin, parsed)')
A('dirs(path, parent, depth, files, bytes)')
A('symbols(id, file_id, kind, name, qname, parent, line)')
A('edges(id, src_file, src_sym, type, key, raw, dst_file, dst_sym, dst_name, line)')
A('nameidx(key, file_id)        -- every path/alias a config may refer to an asset by')
A('blobs(id, file_id, key, val) -- raw key/value with no index (UI atlas rectangles, ...)')
A('meta(k, v)                   -- build statistics')
A('```')
A('`kind` prefixes: `ltx_*` (actor/item/env/sound/ui/phys/logic/other), `script_fn`, '
  '`script_method`, `xml_*`, `c_symbol`, `level`.\n')

with open(os.path.join(HERE, 'INDEX.md'), 'w', encoding='utf-8') as fh:
    fh.write('\n'.join(L))
print('written:', os.path.join(HERE, 'INDEX.md'))
