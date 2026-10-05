# -*- coding: utf-8 -*-
"""Query the Anomaly index without pulling the whole project into context.

  q.py stats
  q.py tree <dir>            directory listing with aggregates
  q.py find <pattern>        files by path/name
  q.py ls <file>             symbols defined in a file
  q.py refs <file|sym>       what this file/symbol points at
  q.py uses <file|sym>       what points at this file/symbol
  q.py chain <sym>           transitive dependencies (depth N)
  q.py rchain <sym>          reverse dependencies
  q.py grep <text>           search ltx params / binary refs / script symbols
  q.py orphans               files nothing references
  q.py levels                per-level rollup
  q.py stats table           meta table
"""
import os, re, sys, sqlite3, argparse

HERE = os.path.dirname(os.path.abspath(__file__))
DBP = os.path.join(HERE, 'anomaly.db')
if not os.path.exists(DBP):
    sys.exit('index not built: %s' % DBP)
C = sqlite3.connect(DBP)
C.row_factory = sqlite3.Row
C.text_factory = lambda b: b.decode('utf-8', 'replace')

SEV = {'0': '30', '1': '31', '2': '32'}


def out(rows, cols, limit=200, trunc=110):
    rows = rows[:limit]
    if not rows:
        print('  (empty)')
        return
    w = [max(len(str(c)), *(len(_fmt(r, c)) for r in rows)) for c in cols]
    w = [min(x, trunc) for x in w]
    print('  ' + '  '.join(str(c)[:trunc].ljust(w[i]) for i, c in enumerate(cols)))
    print('  ' + '  '.join('-' * w[i] for i in range(len(cols))))
    for r in rows:
        print('  ' + '  '.join(_fmt(r, c)[:trunc].ljust(w[i]) for i, c in enumerate(cols)))


def _fmt(r, c):
    v = r[c]
    return '' if v is None else str(v)


def q_file(term):
    """Resolve a path fragment to a file id."""
    t = term.replace('\\', '/')
    row = C.execute("SELECT id,path,size,ext FROM files WHERE path=? OR path LIKE ?",
                    (t, '%' + t + '%')).fetchone()
    if not row:
        row = C.execute("SELECT id,path,size,ext FROM files WHERE lower(name)=lower(?)",
                        (os.path.basename(t),)).fetchone()
    return row


def q_sym(term):
    if term.isdigit():
        return C.execute("SELECT s.*,f.path AS path FROM symbols s JOIN files f ON f.id=s.file_id "
                         "WHERE s.id=?", (int(term),)).fetchone()
    if '::' in term:
        r = C.execute("SELECT s.*,f.path AS path FROM symbols s JOIN files f ON f.id=s.file_id "
                      "WHERE s.qname=? COLLATE NOCASE", (term,)).fetchone()
        return r
    rows = C.execute("SELECT s.*,f.path AS path FROM symbols s JOIN files f ON f.id=s.file_id "
                     "WHERE s.name=? COLLATE NOCASE", (term,)).fetchall()
    if not rows:
        return None
    return rows[0] if len(rows) == 1 else rows


# ------------------------------------------------------------------ commands
def c_stats(a):
    m = dict(C.execute('SELECT k,v FROM meta'))
    if a.what == 'table':
        out([dict(r) for r in C.execute(
            "SELECT type,COUNT(*) n,COUNT(dst_file) to_file,COUNT(dst_sym) to_sym "
            "FROM edges GROUP BY type ORDER BY n DESC")], ['type', 'n', 'to_file', 'to_sym'])
        return
    if a.what == 'ext':
        out([dict(r) for r in C.execute(
            "SELECT ext,COUNT(*) n,ROUND(SUM(size)/1048576.0,1) mb,grp FROM files "
            "GROUP BY grp,ext ORDER BY n DESC")], ['grp', 'ext', 'n', 'mb'])
        return
    if a.what == 'kind':
        out([dict(r) for r in C.execute(
            "SELECT kind,COUNT(*) n FROM symbols GROUP BY kind ORDER BY n DESC")],
            ['kind', 'n'])
        return
    for k in sorted(m):
        if k.startswith('type.'):
            continue
        print('  %-24s %s' % (k, m[k]))


def c_tree(a):
    p = a.path.replace('\\', '/').rstrip('/')
    rows = C.execute("SELECT path,files,bytes FROM dirs WHERE path=? OR path LIKE ? "
                     "ORDER BY path", (p, p + '/%')).fetchall()
    base = len(p) + 1
    for r in rows:
        d = r['path'][base:] if p else r['path']
        if a.maxdepth and d.count('/') >= a.maxdepth:
            continue
        print('  %-58s %7s %10.1f MB' % (d or '.', r['files'], r['bytes'] / 1048576.0))
    tot = C.execute("SELECT COUNT(*) n,SUM(size) s FROM files WHERE path=? OR path LIKE ?",
                    (p, p + '/%')).fetchone()
    print('  %-58s %7d %10.1f MB' % ('TOTAL', tot['n'], (tot['s'] or 0) / 1048576.0))


def c_find(a):
    t = a.pattern.replace('\\', '/')
    sql = "SELECT path,ext,size,grp FROM files WHERE path LIKE ? ORDER BY path"
    out([dict(r) for r in C.execute(sql, ('%' + t + '%',))], ['path', 'ext', 'size', 'grp'],
        a.limit)


def c_ls(a):
    f = q_file(a.file)
    if not f:
        print('  not found:', a.file)
        return
    print('  ==', f['path'], '(%d bytes)' % f['size'])
    out([dict(r) for r in C.execute(
        "SELECT id,kind,name,qname,parent,line FROM symbols WHERE file_id=? ORDER BY line",
        (f['id'],))], ['id', 'kind', 'name', 'qname', 'parent', 'line'], a.limit)


def c_refs(a):
    t = a.target
    f = q_file(t)
    s = q_sym(t) if (a.sym or not f) else None
    if isinstance(s, list):
        print('  %d symbols named %s:' % (len(s), t))
        out([dict(r) for r in s], ['id', 'kind', 'qname', 'path'], a.limit)
        return
    if f and not s:
        where, vals = 'src_file=?', (f['id'],)
    elif s:
        where, vals = 'src_sym=?', (s['id'],)
    else:
        print('  not found:', t)
        return
    sql = ("SELECT e.type,e.key,e.raw,e.line,f.path dfp,g.qname dsq,h.path dsp "
           "FROM edges e LEFT JOIN files f ON f.id=e.dst_file "
           "LEFT JOIN symbols g ON g.id=e.dst_sym "
           "LEFT JOIN files h ON h.id=g.file_id "
           "WHERE e.%s AND e.type<>'param' ORDER BY e.type,e.id" % where)
    out([dict(r) for r in C.execute(sql, vals)], ['type', 'key', 'raw', 'line', 'dfp', 'dsq', 'dsp'],
        a.limit)


def c_uses(a):
    t = a.target
    f = q_file(t)
    s = q_sym(t) if (a.sym or not f) else None
    if isinstance(s, list):
        print('  %d symbols named %s:' % (len(s), t))
        out([dict(r) for r in s], ['id', 'kind', 'qname', 'path'], a.limit)
        return
    cond, vals = [], []
    if f:
        cond.append('e.dst_file=?')
        vals.append(f['id'])
    if s:
        cond.append('e.dst_sym=?')
        vals.append(s['id'])
    if not cond:
        print('  not found:', t)
        return
    sql = ("SELECT e.type,e.key,e.raw,e.line,f.path srcp FROM edges e "
           "JOIN files f ON f.id=e.src_file WHERE (%s) AND e.type<>'param' "
           "ORDER BY f.path,e.type" % ' OR '.join(cond))
    out([dict(r) for r in C.execute(sql, vals)], ['srcp', 'type', 'key', 'raw', 'line'], a.limit)


def _chain(t, depth, rev, limit):
    f = q_file(t)
    seen, frontier = set(), []
    if f:
        frontier = [('file', f['id'])]
    else:
        s = q_sym(t)
        if isinstance(s, list):
            s = s[0]
        if not s:
            return
        frontier = [('sym', s['id'])]
    seen.update(x[1] for x in frontier)
    for d in range(depth):
        nxt = []
        for kind, i in frontier:
            if rev:
                where = 'dst_sym=?' if kind == 'sym' else 'dst_file=?'
            else:
                where = 'src_sym=?' if kind == 'sym' else 'src_file=?'
            rows = C.execute(
                "SELECT DISTINCT src_sym,src_file,dst_sym,dst_file,type,raw FROM edges "
                "WHERE %s AND type<>'param' LIMIT 400" % where, (i,)).fetchall()
            for r in rows:
                tag = '%s=%s %s %s' % (d + 1, kind, r['type'], (r['raw'] or '')[:40])
                print('  %s%s' % ('  ' * (d + 1), tag))
                for nk, ni in (('sym', r['src_sym'] if rev else r['dst_sym']),
                               ('file', r['src_file'] if rev else r['dst_file'])):
                    if ni and ni not in seen:
                        seen.add(ni)
                        nxt.append((nk, ni))
        frontier = nxt
        if not frontier:
            break


def c_chain(a):
    _chain(a.target, a.depth, False, a.limit)


def c_rchain(a):
    _chain(a.target, a.depth, True, a.limit)


def c_grep(a):
    t = a.text
    print('  -- ltx params --')
    out([dict(r) for r in C.execute(
        "SELECT f.path,e.key,e.raw,e.line FROM edges e JOIN files f ON f.id=e.src_file "
        "WHERE e.type='param' AND e.raw LIKE ? LIMIT ?", ('%' + t + '%', a.limit))],
        ['path', 'key', 'raw', 'line'], a.limit)
    print('  -- named refs --')
    out([dict(r) for r in C.execute(
        "SELECT f.path,e.type,e.key,e.raw,e.dst_name FROM edges e JOIN files f ON f.id=e.src_file "
        "WHERE e.type<>'param' AND e.dst_name LIKE ? LIMIT ?", ('%' + t + '%', a.limit))],
        ['path', 'type', 'key', 'raw', 'dst_name'], a.limit)
    print('  -- symbols --')
    out([dict(r) for r in C.execute(
        "SELECT f.path,s.kind,s.name,s.qname FROM symbols s JOIN files f ON f.id=s.file_id "
        "WHERE s.name LIKE ? OR s.qname LIKE ? LIMIT ?",
        ('%' + t + '%', '%' + t + '%', a.limit))], ['path', 'kind', 'name', 'qname'], a.limit)
    print('  -- files --')
    out([dict(r) for r in C.execute(
        "SELECT path,ext,size FROM files WHERE path LIKE ? LIMIT ?",
        ('%' + t + '%', a.limit))], ['path', 'ext', 'size'], a.limit)


def c_orphans(a):
    print('  -- files with no real inbound reference (excluding folder/stem edges) --')
    out([dict(r) for r in C.execute(
        "SELECT f.path,f.ext,f.size,f.grp, "
        "(SELECT COUNT(*) FROM edges e WHERE e.dst_file=f.id) deg FROM files f "
        "WHERE NOT EXISTS (SELECT 1 FROM edges e WHERE e.dst_file=f.id "
        "AND e.type NOT IN ('contain','same_stem')) "
        "ORDER BY f.grp,f.path LIMIT ?", (a.limit,))], ['path', 'ext', 'size', 'grp', 'deg'],
        a.limit)


def c_levels(a):
    out([dict(r) for r in C.execute(
        "SELECT s.name lvl, COUNT(*) files, SUM(f.size) bytes, "
        "(SELECT COUNT(*) FROM edges e2 WHERE e2.dst_sym=s.id AND e2.type='param') cfg_refs "
        "FROM symbols s JOIN edges e ON e.src_sym=s.id "
        "JOIN files f ON f.id=e.dst_file "
        "WHERE s.kind='level' AND e.type='level_contains' "
        "GROUP BY s.id ORDER BY bytes DESC")],
        ['lvl', 'files', 'bytes', 'cfg_refs'], 100)


def c_show(a):
    """Full picture of one config section / script function: body, parents, children, users."""
    s = q_sym(a.target)
    if isinstance(s, list):
        print('  %d symbols named %s -- pick one by id or qname:' % (len(s), a.target))
        out([{'id': r['id'], 'kind': r['kind'], 'qname': r['qname'], 'path': r['path']}
             for r in s], ['id', 'kind', 'qname', 'path'], 40)
        return
    if not s:
        print('  not found:', a.target)
        return
    f = C.execute('SELECT path FROM files WHERE id=?', (s['file_id'],)).fetchone()['path']
    print('  %s  %s   [%s]' % (s['kind'], s['qname'] or s['name'], f))
    if s['line']:
        full = os.path.join(HERE, '..', f)
        try:
            with open(full, 'r', encoding='utf-8', errors='replace') as fh:
                for i, ln in enumerate(fh, 1):
                    if i > s['line'] and i > s['line'] + a.lines:
                        break
                    if i >= s['line'] - a.lines:
                        mark = '>' if i == s['line'] else ' '
                        print('   %s %5d| %s' % (mark, i, ln.rstrip()[:120]))
        except OSError:
            pass
    for title, sql, vals in (
        ('inherits / refs', "SELECT e.key,e.raw,e.line,g.qname,f.path FROM edges e "
         "LEFT JOIN symbols g ON g.id=e.dst_sym LEFT JOIN files f ON f.id=e.src_file "
         "WHERE e.src_sym=? AND e.type<>'param'", (s['id'],)),
        ('params -> file', "SELECT e.key,e.raw,f.path FROM edges e JOIN files f ON f.id=e.dst_file "
         "WHERE e.src_sym=? AND e.type='param'", (s['id'],)),
        ('params -> section', "SELECT e.key,e.raw,g.qname FROM edges e JOIN symbols g ON g.id=e.dst_sym "
         "WHERE e.src_sym=? AND e.type='param'", (s['id'],)),
        ('referenced by', "SELECT f.path,e.key,e.raw,e.type,e.line FROM edges e "
         "JOIN files f ON f.id=e.src_file WHERE e.dst_sym=? LIMIT 300", (s['id'],)),
    ):
        rows = C.execute(sql, vals).fetchall()
        if not rows:
            continue
        print('  -- %s (%d) --' % (title, len(rows)))
        out([dict(r) for r in rows], list(rows[0].keys()), 60)


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='cmd')
    p = sub.add_parser('stats'); p.add_argument('what', nargs='?', default='')
    p = sub.add_parser('tree'); p.add_argument('path'); p.add_argument('--maxdepth', type=int, default=0)
    p = sub.add_parser('find'); p.add_argument('pattern'); p.add_argument('-n', '--limit', type=int, default=60)
    p = sub.add_parser('ls'); p.add_argument('file'); p.add_argument('-n', '--limit', type=int, default=300)
    p = sub.add_parser('refs'); p.add_argument('target'); p.add_argument('--sym', action='store_true')
    p.add_argument('-n', '--limit', type=int, default=200)
    p = sub.add_parser('uses'); p.add_argument('target'); p.add_argument('--sym', action='store_true')
    p.add_argument('-n', '--limit', type=int, default=200)
    p = sub.add_parser('chain'); p.add_argument('target'); p.add_argument('-d', '--depth', type=int, default=2)
    p.add_argument('-n', '--limit', type=int, default=200)
    p = sub.add_parser('rchain'); p.add_argument('target'); p.add_argument('-d', '--depth', type=int, default=2)
    p.add_argument('-n', '--limit', type=int, default=200)
    p = sub.add_parser('grep'); p.add_argument('text'); p.add_argument('-n', '--limit', type=int, default=25)
    p = sub.add_parser('orphans'); p.add_argument('-n', '--limit', type=int, default=100)
    p = sub.add_parser('show'); p.add_argument('target')
    p.add_argument('-L', '--lines', type=int, default=0)
    sub.add_parser('levels')
    a = ap.parse_args()
    if not a.cmd:
        ap.print_help()
        return
    {'stats': c_stats, 'tree': c_tree, 'find': c_find, 'ls': c_ls, 'refs': c_refs,
     'uses': c_uses, 'chain': c_chain, 'rchain': c_rchain, 'grep': c_grep,
     'orphans': c_orphans, 'levels': c_levels, 'show': c_show}[a.cmd](a)


if __name__ == '__main__':
    main()
