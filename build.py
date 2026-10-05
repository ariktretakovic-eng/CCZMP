# -*- coding: utf-8 -*-
"""Stalker Anomaly project indexer.

Scans every file, parses the text configs (ltx / script / xml / xr / shaders),
extracts readable symbols out of the binary containers and resolves a full
cross-reference graph into SQLite.  Nothing is printed except progress.
"""
import os, re, sys, time, sqlite3, fnmatch, collections

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib
from lib import ROOT, OUT, UNP, SCHEMA, norm, strip_slash, bucket

DB = None
_seen_sym = {}
T0 = time.time()
# param keys whose value names a level rather than an arbitrary string
LEVEL_KEYS = {'level', 'level_name', 'name', 'caption', 'map', 'spawn_level', 'level_id'}


def log(*a):
    print('[%6.1fs]' % (time.time() - T0), *a, flush=True)


class Store:
    def __init__(self, conn):
        self.c = conn
        self.cur = conn.cursor()
        self.fsym = []          # per-file list of symbol ids
        self.pending = []       # deferred resolution tuples

    def add_sym(self, file_id, kind, name, qname, parent, line):
        self.cur.execute(
            'INSERT INTO symbols(file_id,kind,name,qname,parent,line) VALUES(?,?,?,?,?,?)',
            (file_id, kind, name, qname, parent, line))
        return self.cur.lastrowid

    def add_edge(self, sf, ss, typ, key, raw, df, ds, dn, line):
        self.c.execute(
            'INSERT INTO edges(src_file,src_sym,type,key,raw,dst_file,dst_sym,dst_name,line)'
            ' VALUES(?,?,?,?,?,?,?,?,?)', (sf, ss, typ, key, raw, df, ds, dn, line))

    def add_blob(self, sf, k, v):
        self.c.execute('INSERT INTO blobs(file_id,key,val) VALUES(?,?,?)', (sf, k, v))

    def add_param(self, sf, k, v, line):
        self.c.execute('INSERT INTO edges(src_file,type,key,raw,line) VALUES(?,?,?,?,?)',
                       (sf, 'param', k, v, line))
        self.params.append((sf, k, v))

    params = []


# ------------------------------------------------------------------ 1. scan
def scan():
    files, dirs = [], []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames
                       if d not in ('.git', '.vs', '__pycache__', '_index')]
        rel = os.path.relpath(dirpath, ROOT)
        rel = '' if rel == '.' else strip_slash(rel)
        depth = 0 if not rel else rel.count('/') + 1
        parent = rel.rsplit('/', 1)[0] if '/' in rel else ''
        n = 0
        b = 0
        for fn in filenames:
            full = os.path.join(dirpath, fn)
            try:
                sz = os.path.getsize(full)
            except OSError:
                continue
            p = (rel + '/' + fn) if rel else fn
            ext = os.path.splitext(fn)[1].lstrip('.').lower()
            stem = os.path.splitext(fn)[0]
            files.append((p, rel, fn, stem, ext, sz, bucket(p)))
            n += 1
            b += sz
        dirs.append((rel or '<root>', parent, depth, n, b))
    return files, dirs


def detect_lang(p):
    m = re.search(r'/text/([a-z]{2,4})/', '/' + p)
    if m:
        return m.group(1)
    m = re.search(r'[/\\]([a-z]{2,4})[/\\][^/\\]*$', p, re.I)
    if m and m.group(1).lower() in ('eng', 'rus', 'ukr', 'deu', 'fra', 'spa', 'ita',
                                    'pol', 'por', 'ces', 'hun', 'srb', 'cze', 'eng2'):
        return m.group(1).lower()
    return None


# ------------------------------------------------------------- 2. parse ltx
def reset_ltx():
    DB.execute("DELETE FROM edges WHERE src_file IN (SELECT id FROM files WHERE ext='ltx')")
    DB.execute("DELETE FROM symbols WHERE kind LIKE 'ltx%'")
    DB.execute("UPDATE files SET parsed=0 WHERE ext='ltx'")
    DB.commit()


def parse_all_ltx(idmap):
    n = 0
    rows = DB.execute("SELECT id,path FROM files WHERE ext='ltx' AND size>0")
    for fid, p in rows.fetchall():
        full = os.path.join(ROOT, strip_slash(p))
        t = lib.read_text(full)
        if t is None:
            continue
        lib.parse_ltx(t, fid, S, p)
        DB.execute('UPDATE files SET parsed=1 WHERE id=?', (fid,))
        n += 1
        if n % 1000 == 0:
            log('  ltx', n)
    return n


RE_S_QREF = lib.RE_S_QREF
RE_STR_ASSET = re.compile(
    r'"([^"\n]{4,200})"'
    r'|(?<![\w])((?:[\w\-]+[\\/])+[\w\-]+\.(?:ogg|ogf|ogm|omf|dds|ltx|script|thm|omx|obj|bik|mp3|wav))',
    re.I)


def is_asset_path(s):
    if not s or ' ' in s:
        return False
    s = s.replace('/', '\\')
    if '\\' not in s:
        return False
    return s.rsplit('.', 1)[-1].lower() in lib.ASSET_EXT


# ---------------------------------------------------------- 3. parse script
def reset_script():
    DB.execute("DELETE FROM edges WHERE src_file IN (SELECT id FROM files WHERE ext='script')")
    DB.execute("DELETE FROM symbols WHERE kind LIKE 'script%'")
    DB.execute("UPDATE files SET parsed=0 WHERE ext='script'")
    DB.commit()


def parse_all_scripts():
    n = 0
    rows = DB.execute("SELECT id,path,stem FROM files WHERE ext='script' AND size>0")
    texts = []
    for fid, p, stem in rows.fetchall():
        t = lib.read_text(os.path.join(ROOT, strip_slash(p)))
        if t is None:
            continue
        texts.append((fid, p, stem, t))
        for q, nm, kind in lib.script_defs(t, stem):
            S.add_sym(fid, kind, nm, q, q.split('::')[0], 0)
        DB.execute('UPDATE files SET parsed=1 WHERE id=?', (fid,))
        n += 1
    log('  script files', n, 'total bytes', sum(len(t[3]) for t in texts))

    # collect every defined (name) across the project
    by_name = collections.defaultdict(list)
    for sid, nm in DB.execute(
            "SELECT id,name FROM symbols WHERE kind LIKE 'script%'"):
        by_name[nm].append(sid)
    script_sym_ids = collections.defaultdict(set)
    for sid, fid in DB.execute("SELECT id,file_id FROM symbols WHERE kind LIKE 'script%'"):
        script_sym_ids[fid].add(sid)

    for fid, p, stem, t in texts:
        clean = lib.strip_lua(t)
        mine = set(script_sym_ids.get(fid, ()))
        lineno = 0
        for ln in clean.splitlines():
            lineno += 1
            # asset paths written as string literals (sound_play, load_sound, ...)
            for m in RE_STR_ASSET.finditer(ln):
                s = m.group(1) or m.group(2)
                if is_asset_path(s):
                    S.add_edge(fid, None, 'strref', 'literal', s,
                               None, None, s, lineno)
            # explicit script.script::func references
            for m in lib.RE_S_QREF.finditer(ln):
                sf, fn = m.group(1), m.group(2)
                S.add_edge(fid, None, 'script_ref', 'call', sf + '::' + fn,
                           None, None, sf + '::' + fn, lineno)
            for m in lib.RE_S_DOTTED.finditer(ln):
                S.add_edge(fid, None, 'script_ref', 'load', m.group(0),
                           None, None, m.group(1), lineno)
            for m in lib.RE_S_CALL.finditer(ln):
                nm = m.group(1)
                if nm in ('if', 'for', 'while', 'return', 'function', 'and', 'or',
                          'not', 'else', 'repeat', 'until', 'do', 'end', 'local',
                          'table', 'string', 'math', 'os', 'self', 'type', 'print'):
                    continue
                for sid in by_name.get(nm, ()):
                    if sid in mine:
                        continue
                    S.add_edge(fid, None, 'call', nm, nm, None, sid, None, lineno)
            for m in lib.RE_S_MCALL.finditer(ln):
                nm = m.group(1)
                for sid in by_name.get(nm, ())[:8]:
                    S.add_edge(fid, None, 'call_dyn', nm, nm, None, sid, None, lineno)
    return n


# ------------------------------------------------------------ 4. parse xml
def reset_xml():
    DB.execute("DELETE FROM edges WHERE src_file IN (SELECT id FROM files WHERE ext='xml')")
    DB.execute("DELETE FROM symbols WHERE kind LIKE 'xml%'")
    DB.execute("UPDATE files SET parsed=0 WHERE ext='xml'")
    DB.commit()


def parse_all_xml():
    n = 0
    for fid, p in DB.execute("SELECT id,path FROM files WHERE ext='xml' AND size>0").fetchall():
        t = lib.read_text(os.path.join(ROOT, strip_slash(p)))
        if t is None:
            continue
        lib.parse_xml(t, fid, S, p)
        DB.execute('UPDATE files SET parsed=1 WHERE id=?', (fid,))
        n += 1
    return n


# ------------------------------------------------------- 4b. atlases / batches
def build_atlases():
    """<file name="ui\\ui_iconsNpc"> + <texture id="..."> -> alias every id to the atlas file."""
    R = Resolver()
    pairs = []
    for sid, name, fpath in DB.execute(
            "SELECT s.id,s.name,f.path FROM symbols s JOIN files f ON f.id=s.file_id "
            "WHERE s.kind='xml_file'").fetchall():
        fid = R.file(name)
        if fid is None:
            for e in ('.dds', '.ltx', ''):
                fid = R.file(name + e)
                if fid:
                    break
        if fid:
            DB.execute('UPDATE edges SET dst_file=? WHERE src_sym=? AND type=\'xml_ref\'', (fid, sid))
            pairs.append((sid, fid))
    alias = []
    for sid, fid in pairs:
        for tid, tname in DB.execute(
                "SELECT s.id,s.name FROM symbols s JOIN edges e ON e.dst_sym=s.id "
                "WHERE e.dst_sym=? AND e.type='xml_parent' AND e.src_sym IS NOT NULL",
                (sid,)).fetchall():
            if tname and tname.lower() == tname:
                alias.append((tname.lower(), fid))
    DB.executemany('INSERT INTO nameidx(key,file_id) VALUES(?,?)', alias)
    DB.commit()
    return len(pairs), len(alias)


# ------------------------------------------------------- 5. generic text ltx-like
RE_INC_ANY = re.compile(r'^[ \t]*#include[ \t]+"([^"]+)"', re.I | re.M)


def parse_misc_text():
    """ini / xr / shader sources / other text: record includes and defined names."""
    n = 0
    rows = DB.execute("SELECT id,path,ext FROM files WHERE parsed=0 AND size>0").fetchall()
    for fid, p, ext in rows:
        if ext in lib.BIN_EXT:
            continue
        t = lib.read_text(os.path.join(ROOT, strip_slash(p)))
        if t is None or len(t) < 8:
            continue
        found = False
        for m in RE_INC_ANY.finditer(t):
            S.add_edge(fid, None, 'include', 'include', m.group(1), None, None,
                       m.group(1), t.count('\n', 0, m.start()) + 1)
            found = True
        if ext in ('vs', 'ps', 'h', 's', 'dm', 'ini', 'xr', 'sqx', 'cs', 'cfg', 'txt'):
            names = re.findall(r'^[ \t]*(?:function|struct|class|#define|uniform|static)[ \t]+'
                               r'([A-Za-z_]\w*)', t, re.M)
            for nm in dict.fromkeys(names):
                S.add_sym(fid, 'c_symbol', nm, nm, None, 0)
                found = True
        if found:
            DB.execute('UPDATE files SET parsed=1 WHERE id=?', (fid,))
            n += 1
    return n


# ---------------------------------------------------- 6. binary string harvest
def harvest_binary():
    n = 0
    rows = DB.execute("SELECT id,path,ext,size FROM files WHERE parsed=0").fetchall()
    for fid, p, ext, size in rows:
        if ext in lib.SKIP_BIG or ext not in lib.BIN_SCAN_EXT:
            continue
        cap = lib.BIN_SCAN_CAP.get(ext, 8 << 20)
        try:
            with open(os.path.join(ROOT, strip_slash(p)), 'rb') as f:
                data = f.read(cap)
        except OSError:
            continue
        strs = lib.bin_strings(data)
        for s in strs:
            s = s.strip()
            if len(s) < 4 or len(s) > 200:
                continue
            S.add_edge(fid, None, 'binref', ext, s, None, None, s, 0)
        DB.execute('UPDATE files SET parsed=1 WHERE id=?', (fid,))
        n += 1
        if n % 500 == 0:
            log('  binary', n)
    return n


# ------------------------------------------------------------ 7. name index
def build_nameidx():
    rows = DB.execute("SELECT id,path,stem,name FROM files").fetchall()
    ins = []
    for fid, p, stem, name in rows:
        g = p
        if g.startswith(UNP + '/'):
            g = g[len(UNP) + 1:]
        keys = {g.lower(), g.lower() + '.', norm(g)}
        k = g.lower()
        if '.' in os.path.basename(k):
            keys.add(k.rsplit('.', 1)[0])
        keys.add(name.lower())
        keys.add(stem.lower())
        keys.add(p.lower())
        for key in keys:
            if key:
                ins.append((key, fid))
    DB.executemany('INSERT INTO nameidx(key,file_id) VALUES(?,?)', ins)
    DB.commit()
    return len(ins)


# ---------------------------------------------------------- 8. resolution
class Resolver:
    def __init__(self):
        self.by_key = collections.defaultdict(list)
        for key, fid in DB.execute('SELECT key,file_id FROM nameidx'):
            self.by_key[key].append(fid)
        self.cfg = collections.defaultdict(list)   # section / xml node name -> sym ids
        for sid, nm in DB.execute(
                "SELECT id,name FROM symbols WHERE kind LIKE 'ltx%' OR kind LIKE 'xml%' "
                "OR kind='level'"):
            self.cfg[nm.lower()].append(sid)
        self.levels = collections.defaultdict(list)
        for sid, nm in DB.execute("SELECT id,name FROM symbols WHERE kind='level'"):
            self.levels[nm.lower()].append(sid)
        self.cfg_q = {}
        for sid, q in DB.execute(
                "SELECT id,qname FROM symbols WHERE kind LIKE 'script%'"):
            self.cfg_q[q.lower()] = sid
        self.stem_file = {}
        for fid, stem, ext in DB.execute(
                "SELECT id,stem,ext FROM files WHERE ext IN ('script','ltx')"):
            self.stem_file.setdefault(stem.lower(), []).append(fid)
        self.fpath = {}
        for fid, p in DB.execute('SELECT id,path FROM files'):
            self.fpath[fid] = p
        self.sym_by_name = collections.defaultdict(list)
        self.sym_file = {}
        for sid, nm, fid in DB.execute(
                "SELECT id,name,file_id FROM symbols WHERE kind LIKE 'script%' OR kind LIKE 'ltx%'"):
            self.sym_by_name[nm.lower()].append(sid)
            self.sym_file[sid] = fid
        self.cur_file = None

    def sym(self, name, prefer_file=None):
        got = self.sym_by_name.get((name or '').lower())
        if not got:
            return None
        if prefer_file is not None:
            for s in got:
                if self.sym_file.get(s) == prefer_file:
                    return s
        return got[0]

    def file(self, raw, srcdir=''):
        if not raw:
            return None
        v = strip_slash(str(raw)).lower()
        v = v.split('$')[0].strip(' \'"')
        if not v or ' ' in v or len(v) > 300:
            return None
        if '#' in v:
            v = v.split('#')[0]
        v = v.strip('/')
        if not v:
            return None
        cands = [v]
        for pre in lib.CAND_PREFIX:
            if pre:
                cands.append(pre + v)
        head, _, tail = v.partition('/')
        if head in lib.ALIAS:
            cands.append(lib.ALIAS[head] + tail)
        extless = []
        for c in cands:
            e = c.rsplit('.', 1)
            if len(e) == 2 and e[1].rsplit('/', 1)[-1] in lib.ASSET_EXT:
                extless.append(e[0])
        cands += extless
        if srcdir:
            cands.append(srcdir.lower() + '/' + v)
            cands.append(srcdir.lower() + '/' + v.rsplit('.', 1)[0])
        for c in cands:
            got = self.by_key.get(c)
            if got:
                return got[0]
        # sound descriptors name a prefix; the engine appends the variants
        for c in list(cands):
            if '.' in c.rsplit('/', 1)[-1]:
                continue
            for suf in lib.SOUND_VARIANTS:
                got = self.by_key.get(c + suf)
                if got:
                    return got[0]
        if '/' not in v:
            got = self.by_key.get(v.rsplit('.', 1)[0]) or self.by_key.get(v)
            if got:
                return got[0]
        return None

    def include(self, raw, srcfid):
        """Resolve an #include path, X-Ray style (relative, then gamedata roots)."""
        v = norm(raw)
        src = self.fpath.get(srcfid, '')
        srcdir = src.rsplit('/', 1)[0] if '/' in src else ''
        got = self.file(v, srcdir)
        if got:
            return got
        # glob
        if '*' in v or '?' in v:
            pat = v
            roots = [srcdir, 'configs', 'configs/items', 'configs/gameplay', 'configs/scripts']
            for r in roots:
                pre = (r + '/') if r else ''
                for key, fids in self.by_key.items():
                    if fnmatch.fnmatch(key, pre + pat) or fnmatch.fnmatch(key, pat):
                        return fids[0]
        return None

    def section(self, name):
        return self.cfg.get(name.lower())


def resolve():
    R = Resolver()
    log('  resolver ready')
    upd_file, upd_sym, upd_name = [], [], []
    n = 0
    cur = DB.execute("SELECT id,src_file,src_sym,type,key,raw,dst_name FROM edges "
                     "WHERE type IN ('include','script_ref','binref','inherit','xml_ref',"
                     "'call','call_dyn','strref') ORDER BY type, id")
    srcfile = {fid: p for fid, p in DB.execute('SELECT id,path FROM files')}
    while True:
        rows = cur.fetchmany(4000)
        if not rows:
            break
        for eid, sfid, ssym, typ, key, raw, dname in rows:
            n += 1
            df = ds = None
            if typ in ('include',):
                df = R.include(raw, sfid)
            elif typ == 'strref':
                df = R.file(raw)
            elif typ in ('call', 'call_dyn'):
                ds = R.sym(raw, sfid)
            elif typ == 'inherit':
                # Anomaly appends state modifiers to the parent: beh@general
                for cand in (raw, re.split(r'[@+#]', raw or '', maxsplit=1)[0]):
                    got = R.section(cand)
                    if got:
                        ds = got[0]
                        break
            elif typ == 'xml_ref':
                df = R.file(raw)
                if df is None:
                    got = R.section(raw) or R.cfg_q.get((raw or '').lower())
                    if got:
                        ds = got[0]
            elif typ in ('script_ref',):
                q = (raw or '').lower()
                ds = R.cfg_q.get(q)
                if ds is None:
                    sf = q.split('::')[0]
                    got = R.stem_file.get(sf.lower() + '.script') or R.stem_file.get(sf.lower())
                    df = got[0] if got else None
            elif typ == 'binref':
                df = R.file(raw)
                if df is None and re.fullmatch(r'[\w:\.]+', raw or ''):
                    got = R.section(raw.split(':')[-1]) or R.section(raw)
                    if got:
                        ds = got[0]
            if df is not None and ds is None:
                upd_file.append((df, eid))
            if ds is not None:
                upd_sym.append((ds, eid))
        if n % 200000 == 0:
            log('  resolved', n)
            DB.executemany('UPDATE edges SET dst_file=? WHERE id=?', upd_file); upd_file = []
            DB.executemany('UPDATE edges SET dst_sym=? WHERE id=?', upd_sym); upd_sym = []
    DB.executemany('UPDATE edges SET dst_file=? WHERE id=?', upd_file)
    DB.executemany('UPDATE edges SET dst_sym=? WHERE id=?', upd_sym)
    DB.commit()
    return n


def resolve_params():
    """LTX parameter values -> files / config sections (only cross-file refs kept)."""
    R = Resolver()
    upd_f, upd_s, upd_n = [], [], []
    total = 0
    cur = DB.execute("SELECT e.id,e.src_file,e.key,e.raw FROM edges e "
                     "JOIN files f ON f.id=e.src_file "
                     "WHERE e.type='param' AND f.ext='ltx'")
    while True:
        rows = cur.fetchmany(8000)
        if not rows:
            break
        for eid, sfid, key, raw in rows:
            total += 1
            if raw is None:
                continue
            v = raw.strip('"\'').strip()
            if not v or len(v) > 260:
                continue
            if ',' in v or '|' in v or '{' in v or '=' in v:
                v = v.split(',')[0].split('|')[0].split('{')[0].split('=')[0].strip()
            if not v or len(v) < 3:
                continue
            if ' ' in v:
                continue
            ext = v.rsplit('.', 1)[-1].lower() if '.' in v else ''
            ident = bool(re.search(r'[A-Za-z]', v)) and not v.replace('.', '').isdigit()
            if v.lower() in ('true', 'false', 'nil', 'none', 'all', 'default', 'yes', 'no'):
                continue
            looks_path = ('\\' in v or '/' in v) and ident
            df = None
            if looks_path:
                df = R.file(v)
                if df is not None:
                    upd_f.append((df, eid))
                    continue
                base = re.split(r'[\\/@:]', v)[-1]
                got = R.section(base)
                if got:
                    upd_s.append((got[0], eid))
                else:
                    upd_n.append((v, eid))
            elif ident:
                if key in LEVEL_KEYS:
                    g = R.levels.get(v.lower())
                    if g:
                        upd_s.append((g[0], eid))
                        continue
                got = R.section(v)
                if got:
                    upd_s.append((got[0], eid))
                else:
                    upd_n.append((v, eid))
        if total % 200000 == 0:
            log('  params', total)
            for buf, sql in ((upd_f, 'dst_file'), (upd_s, 'dst_sym'), (upd_n, 'dst_name')):
                if buf:
                    DB.executemany('UPDATE edges SET %s=? WHERE id=?' % sql, buf)
                    del buf[:]
    for buf, sql in ((upd_f, 'dst_file'), (upd_s, 'dst_sym'), (upd_n, 'dst_name')):
        if buf:
            DB.executemany('UPDATE edges SET %s=? WHERE id=?' % sql, buf)
    DB.commit()
    return total



# ------------------------------------------------------------- 9. levels
def build_levels():
    """One symbol per level folder, linked to every file that belongs to it."""
    DB.execute("DELETE FROM edges WHERE type IN ('level_contains')")
    DB.execute("DELETE FROM symbols WHERE kind='level'")
    rows = DB.execute(
        "SELECT id,path FROM files WHERE path LIKE '%/levels/%' ORDER BY path").fetchall()
    lv = collections.defaultdict(list)
    for fid, p in rows:
        m = re.search(r'/(?:unpacked/)?levels/([^/]+)/', p)
        if m:
            lv[m.group(1)].append((fid, p))
    n = m = 0
    for name, members in lv.items():
        anchor = None
        for fid, p in members:
            if p.endswith('/level.ltx') or p.endswith('/level.spawn'):
                anchor = (fid, p)
                break
        if anchor is None:
            anchor = members[0]
        sid = S.add_sym(anchor[0], 'level', name, name, None, 0)
        for fid, p in members:
            DB.execute('INSERT INTO edges(src_file,src_sym,type,key,raw,dst_file) '
                       'VALUES(?,?,?,?,?,?)', (anchor[0], sid, 'level_contains', 'file', p, fid))
            m += 1
        n += 1
    DB.commit()
    return n, m


def index_levels():
    levels = collections.Counter()
    for (p,) in DB.execute("SELECT path FROM files WHERE path LIKE '%/levels/%'"):
        m = re.search(r'/(?:unpacked/)?levels/([^/]+)/', p)
        if m:
            levels[m.group(1)] += 1
    return levels


# ------------------------------------------- 10. structural / coverage links
def prune():
    """Drop binary-ASCII noise: unresolved binrefs that carry no path syntax."""
    n = C0 = DB.execute(
        "SELECT COUNT(*) FROM edges WHERE type='binref' AND dst_file IS NULL "
        "AND dst_sym IS NULL AND raw NOT LIKE '%\\%'").fetchone()[0]
    DB.execute("DELETE FROM edges WHERE type='binref' AND dst_file IS NULL "
               "AND dst_sym IS NULL AND raw NOT LIKE '%\\%'")
    DB.execute("UPDATE edges SET dst_name=NULL WHERE type='binref' AND dst_file IS NULL "
               "AND dst_sym IS NULL")
    DB.commit()
    return n


def build_links():
    """Guarantee every file carries relations: folder containment + stem family."""
    DB.execute("DELETE FROM edges WHERE type IN ('contain','same_stem')")
    n = m = 0
    stemmap = collections.defaultdict(list)
    for fid, stem, p in DB.execute("SELECT id,stem,path FROM files").fetchall():
        stemmap[stem.lower()].append(fid)
        d = p.rsplit('/', 1)[0] if '/' in p else ''
        DB.execute('INSERT INTO edges(src_file,type,key,raw,dst_file) VALUES(?,?,?,?,?)',
                   (0, 'contain', 'dir', d or '<root>', fid))
        n += 1
    DB.commit()
    for stem, fids in stemmap.items():
        if len(fids) < 2 or len(fids) > 24:
            continue
        for a in fids:
            for b in fids:
                if a != b:
                    DB.execute('INSERT INTO edges(src_file,type,key,raw,dst_file) '
                               'VALUES(?,?,?,?,?)', (a, 'same_stem', stem, stem, b))
                    m += 1
    DB.commit()
    return n, m


# ----------------------------------------------------------------- main
def open_db(create=False):
    global DB, S
    os.makedirs(OUT, exist_ok=True)
    dbp = os.path.join(OUT, 'anomaly.db')
    if create and os.path.exists(dbp):
        os.remove(dbp)
    DB = sqlite3.connect(dbp)
    if create:
        DB.executescript(SCHEMA)
    S = Store(DB)
    return dbp


def emit_stats():
    stats = {
        'files': DB.execute('SELECT COUNT(*) FROM files').fetchone()[0],
        'dirs': DB.execute('SELECT COUNT(*) FROM dirs').fetchone()[0],
        'symbols': DB.execute('SELECT COUNT(*) FROM symbols').fetchone()[0],
        'ltx_sections': DB.execute("SELECT COUNT(*) FROM symbols WHERE kind LIKE 'ltx%'").fetchone()[0],
        'script_fns': DB.execute("SELECT COUNT(*) FROM symbols WHERE kind LIKE 'script%'").fetchone()[0],
        'xml_nodes': DB.execute("SELECT COUNT(*) FROM symbols WHERE kind LIKE 'xml%'").fetchone()[0],
        'edges': DB.execute('SELECT COUNT(*) FROM edges').fetchone()[0],
        'edges_to_file': DB.execute('SELECT COUNT(*) FROM edges WHERE dst_file IS NOT NULL').fetchone()[0],
        'edges_to_symbol': DB.execute('SELECT COUNT(*) FROM edges WHERE dst_sym IS NOT NULL').fetchone()[0],
        'files_with_inbound': len(DB.execute('SELECT DISTINCT dst_file FROM edges WHERE dst_file IS NOT NULL').fetchall()),
        'files_with_outbound': len(DB.execute('SELECT DISTINCT src_file FROM edges WHERE src_file>0').fetchall()),
        'files_referenced': len(DB.execute(
            'SELECT DISTINCT dst_file FROM edges WHERE dst_file IS NOT NULL '
            "AND type NOT IN ('contain','same_stem')").fetchall()),
        'files_referencing': len(DB.execute(
            'SELECT DISTINCT src_file FROM edges WHERE src_file>0 '
            "AND type NOT IN ('contain','same_stem')").fetchall()),
        'files_unlinked': DB.execute('SELECT COUNT(*) FROM files f WHERE NOT EXISTS '
                                     '(SELECT 1 FROM edges e WHERE e.src_file=f.id) '
                                     'AND NOT EXISTS (SELECT 1 FROM edges e WHERE e.dst_file=f.id)').fetchone()[0],
        'files_no_real_link': DB.execute(
            'SELECT COUNT(*) FROM files f WHERE NOT EXISTS '
            '(SELECT 1 FROM edges e WHERE e.dst_file=f.id AND e.type NOT IN '
            "('contain','same_stem')) AND NOT EXISTS (SELECT 1 FROM edges e WHERE "
            "e.src_file=f.id AND e.type NOT IN ('contain','same_stem'))").fetchone()[0],
    }
    for et, c in DB.execute('SELECT type,COUNT(*) FROM edges GROUP BY type ORDER BY 2 DESC'):
        stats['type.' + et] = c
    for et, c in DB.execute("SELECT type,COUNT(*) FROM edges WHERE type NOT IN ('contain','same_stem') "
                            "AND dst_file IS NOT NULL GROUP BY type ORDER BY 2 DESC"):
        stats['resolved.' + et] = c
    DB.executemany('INSERT OR REPLACE INTO meta(k,v) VALUES(?,?)',
                   [(k, str(v)) for k, v in stats.items()])
    DB.execute("DELETE FROM meta WHERE k IN ('edges_resolved_file','edges_resolved_sym')")
    DB.commit()
    for k in sorted(stats):
        log('  %-24s %s' % (k, stats[k]))


def main():
    stages = sys.argv[1:] or ['all']
    a = stages == ['all']
    dbp = open_db(create=a or 'scan' in stages)
    try:
        if a or 'scan' in stages:
            log('scanning tree...')
            files, dirs = scan()
            log('files', len(files), 'dirs', len(dirs))
            DB.executemany('INSERT INTO files(path,dir,name,stem,ext,size,grp,lang,bin)'
                           ' VALUES(?,?,?,?,?,?,?,?,?)',
                           [(p, d, n, s, e, z, g, detect_lang(p),
                             1 if (e in lib.BIN_EXT or e not in lib.TEXT_EXT) else 0)
                            for p, d, n, s, e, z, g in files])
            DB.executemany('INSERT INTO dirs(path,parent,depth,files,bytes) VALUES(?,?,?,?,?)', dirs)
            DB.commit()
        if a or 'ltx' in stages:
            reset_ltx()
            log('parsing ltx...'); log('   ', parse_all_ltx({})); DB.commit()
        if a or 'script' in stages:
            reset_script()
            log('parsing scripts...'); parse_all_scripts(); DB.commit()
        if a or 'xml' in stages:
            reset_xml()
            log('parsing xml...'); log('   ', parse_all_xml()); DB.commit()
        if a or 'misc' in stages:
            log('parsing misc text...'); log('   ', parse_misc_text()); DB.commit()
        if a or 'bin' in stages:
            log('harvesting binary strings...'); log('   ', harvest_binary()); DB.commit()
        if a or 'name' in stages:
            log('building name index...'); log('   ', build_nameidx())
        if a or 'atlas' in stages:
            log('mapping atlases...'); log('   ', build_atlases())
        if a or 'resolve' in stages:
            DB.execute("UPDATE edges SET dst_file=NULL, dst_sym=NULL WHERE type IN "
                       "('include','script_ref','binref','inherit','xml_ref',"
                       "'call','call_dyn','strref')")
            DB.commit()
            log('resolving edges...'); log('   ', resolve())
        if a or 'params' in stages:
            DB.execute("UPDATE edges SET dst_file=NULL, dst_sym=NULL,dst_name=NULL WHERE type='param'")
            DB.commit()
            log('resolving ltx params...'); log('   ', resolve_params())
        if a or 'prune' in stages:
            log('pruning binary noise...'); log('   ', prune())
        if a or 'links' in stages:
            log('building structural links...')
            log('   files %d, stem edges %d' % build_links())
        if a or 'levels' in stages:
            log('indexing levels...'); log('   ', build_levels())
        if a or 'stats' in stages:
            DB.executescript('ANALYZE;')
            emit_stats()
        if 'vacuum' in stages:
            log('vacuuming...')
            DB.executescript('VACUUM; ANALYZE;')
        DB.commit()
        DB.execute('PRAGMA optimize')
    finally:
        DB.commit()
        DB.close()
    log('done ->', dbp)


if __name__ == '__main__':
    main()