# -*- coding: utf-8 -*-
"""Shared helpers: schema, path resolution, LTX/script/XML/binary parsers."""
import os, re, sqlite3, fnmatch

ROOT = r"D:\CCZMP PROJECT"
OUT = os.path.join(ROOT, "_index")
UNP = "tools/_unpacked"

SCHEMA = """
PRAGMA journal_mode=OFF;
PRAGMA synchronous=OFF;
PRAGMA temp_store=MEMORY;

CREATE TABLE IF NOT EXISTS meta(k TEXT PRIMARY KEY, v TEXT);

CREATE TABLE IF NOT EXISTS files(
  id INTEGER PRIMARY KEY,
  path TEXT UNIQUE NOT NULL,
  dir TEXT, name TEXT, stem TEXT, ext TEXT,
  size INTEGER, grp TEXT, lang TEXT, bin INTEGER DEFAULT 0, parsed INTEGER DEFAULT 0
);
CREATE INDEX IF NOT EXISTS ix_f_dir  ON files(dir);
CREATE INDEX IF NOT EXISTS ix_f_ext  ON files(ext);
CREATE INDEX IF NOT EXISTS ix_f_grp  ON files(grp);
CREATE INDEX IF NOT EXISTS ix_f_name ON files(name);
CREATE INDEX IF NOT EXISTS ix_f_stem ON files(stem);

CREATE TABLE IF NOT EXISTS dirs(
  path TEXT PRIMARY KEY, parent TEXT, depth INT, files INT, bytes INT
);

CREATE TABLE IF NOT EXISTS symbols(
  id INTEGER PRIMARY KEY,
  file_id INT NOT NULL,
  kind TEXT NOT NULL,
  name TEXT NOT NULL,
  qname TEXT,
  parent TEXT,
  line INT,
  nchild INT DEFAULT 0
);
CREATE INDEX IF NOT EXISTS ix_s_file ON symbols(file_id);
CREATE INDEX IF NOT EXISTS ix_s_qnam ON symbols(qname);
CREATE INDEX IF NOT EXISTS ix_s_name ON symbols(name);
CREATE INDEX IF NOT EXISTS ix_s_kind ON symbols(kind);

CREATE TABLE IF NOT EXISTS edges(
  id INTEGER PRIMARY KEY,
  src_file INT NOT NULL,
  src_sym INT,
  type TEXT NOT NULL,
  key TEXT,
  raw TEXT,
  dst_file INT,
  dst_sym INT,
  dst_name TEXT,
  line INT
);
CREATE INDEX IF NOT EXISTS ix_e_src    ON edges(src_file, type);
CREATE INDEX IF NOT EXISTS ix_e_srcsym ON edges(src_sym);
CREATE INDEX IF NOT EXISTS ix_e_dst    ON edges(dst_file);
CREATE INDEX IF NOT EXISTS ix_e_dsym   ON edges(dst_sym);
CREATE INDEX IF NOT EXISTS ix_e_dname  ON edges(dst_name);
CREATE INDEX IF NOT EXISTS ix_e_type   ON edges(type);
CREATE INDEX IF NOT EXISTS ix_e_key    ON edges(key);

CREATE TABLE IF NOT EXISTS nameidx(
  key TEXT NOT NULL, file_id INT NOT NULL
);
CREATE INDEX IF NOT EXISTS ix_ni ON nameidx(key);

CREATE TABLE IF NOT EXISTS bstrings(
  id INTEGER PRIMARY KEY, file_id INT NOT NULL, val TEXT, n INT DEFAULT 1
);
CREATE INDEX IF NOT EXISTS ix_bs ON bstrings(file_id);

CREATE TABLE IF NOT EXISTS blobs(
  id INTEGER PRIMARY KEY, file_id INT NOT NULL, sym INT, key TEXT, val TEXT
);
CREATE INDEX IF NOT EXISTS ix_bl ON blobs(file_id);
"""

# ---------------------------------------------------------------- extensions
BIN_EXT = {
    'dds', 'ogg', 'ogf', 'ogm', 'omf', 'thm', 'anm', 'anm1', 'obj', 'tga', 'png', 'jpg',
    'bmp', 'exe', 'dll', 'db0', 'db1', 'db2', 'db3', 'db4', 'phys', 'gct', 'bin', 'pdb',
    'cform', 'geom', 'geomx', 'hom', 'details', 'level', 'ai', 'spawn', 'snd_static',
    'ps_static', 'som', 'ps', 'ppe', 'env_mod', 'fog_vol', 'lights', 'wallmarks',
    'gs', 'seq', 'dm', 'mhr', 'ogx', 'r0', 'wd', 'sv', 'lsx', 'xls', 'fac',
}
TEXT_EXT = {
    'ltx', 'script', 'xml', 'ini', 'txt', 'h', 'vs', 'ps', 's', 'cs', 'xr', 'sqx',
    'cfg', 'hpp', 'cpp', 'bat', 'md', 'fmt', 'dss', 'map', 'sch', 'ltx2', 'tga_desc',
}

ASSET_EXT = {
    'dds', 'ogg', 'ogf', 'ogm', 'omf', 'thm', 'tga', 'png', 'jpg', 'bmp', 'xr', 'ltx',
    'script', 'ini', 'xml', 'sqx', 'obj', 'bik', 'mp3', 'wav', 'ai', 'spawn', 'omx',
    'level', 'details', 'som', 'lights', 'dm', 'ppe', 'env_mod', 'fog_vol', 'wallmarks',
}

# prefixes to try when a config value looks like a path
CAND_PREFIX = [
    '', 'gamedata/', 'configs/', 'meshes/', 'sounds/', 'sound/', 'textures/',
    'levels/', 'scripts/', 'anims/', 'shaders/', 'ai/', 'misc/', 'ui/',
    'models/', 'items/', 'weapons/', 'creatures/', 'zones/', 'text/',
    'gameplay/', 'plugins/', 'presets/', 'mp/', 'environment/', 'scripts\\',
]
# leading folder aliases used inside configs vs. on disk
ALIAS = {
    'sound': 'sounds/', 'snd': 'sounds/', 'mesh': 'meshes/', 'tex': 'textures/',
    'texture': 'textures/', 'model': 'models/', 'anim': 'anims/',
    'level': 'levels/', 'script': 'scripts/', 'cfg': 'configs/',
    'ui': 'ui/', 'gamedata': '',
}
# a sound descriptor's `path` is a prefix; the engine appends these suffixes
SOUND_VARIANTS = (
    '_a', '_b', '_c', '_d', '_1', '_2', '_3', '_1a', '_1b', '_2a', '_2b',
    '_bark', '_howl', '_scream', '_attack', '_hit', '_death', '_die', '_idle',
    '_stand', '_move', '_walk', '_run', '_breath', '_voice', '_say', '_1a_', '_a_',
)

# ------------------------------------------------------------------- helpers
def norm(s):
    return (s or '').strip().replace('/', '\\').lower()

def strip_slash(s):
    return s.replace('\\', '/')

def bucket(path):
    p = strip_slash(path)
    if p.startswith(UNP + '/'):
        rest = p[len(UNP) + 1:].split('/')
        return 'unpacked/' + (rest[0] if rest[0] else '')
    return p.split('/')[0] or '<root>'

def read_text(path, limit=None):
    """Read a text file, tolerating any encoding. Returns str or None."""
    try:
        with open(path, 'rb') as f:
            data = f.read() if limit is None else f.read(limit)
    except OSError:
        return None
    if b'\x00' in data[:4096]:
        return None
    for enc in ('utf-8-sig', 'utf-8', 'cp1251', 'cp1252', 'latin-1'):
        try:
            return data.decode(enc)
        except (UnicodeDecodeError, LookupError):
            continue
    return data.decode('latin-1', 'replace')

# ------------------------------------------------------------- LTX parsing
RE_LTX_COMMENT = re.compile(r';.*$')
RE_LTX_INCLUDE = re.compile(r'^[ \t]*#include[ \t]+"([^"]+)"', re.I)
RE_LTX_SECTION = re.compile(r'^[ \t]*\[([^\]]+)\](.*)$')
RE_LTX_ANYSEC =  re.compile(r'\[[^\]\n]{1,120}\]')
RE_LTX_PARAM =   re.compile(r'^[ \t]*([A-Za-z_$][\w$%.\-]*)[ \t]*=[ \t]*(.*)$')
RE_LTX_FLAG =    re.compile(r'^[ \t]*([A-Za-z_$][\w$%.\-]*)[ \t]*$')

SECTION_KIND = [
    (re.compile(r'^(actor|stalker|monster|dog|wolf|flesh|spider|mutant|bear|boar|alien|poltergeists?|chimer|karakhan|rat|scorpion|turtle|zombie|nightstand|snork|videodog)', re.I), 'actor'),
    (re.compile(r'^(wpn|weapon|hands|wpn_base|grenade|knife|medkit|ammo|artefact|artifact|device|food|drink|drug|explosive|item|attch|box|space|torch|custom|attach)', re.I), 'item'),
    (re.compile(r'^(light|lamps|night|day|sky|sun|moon|weather|tree|grass|bush|flora|env_|fog)', re.I), 'env'),
    (re.compile(r'^(snd|sound|music|ambience|ui_sound|net_sound)', re.I), 'sound'),
    (re.compile(r'^(text|font|ui_|ui$|ctrl|xml|menu|window|game_ui|icon|mark)', re.I), 'ui'),
    (re.compile(r'^(physics|phys|ragdoll|material|shader|psys|pfx|postprocess)', re.I), 'phys'),
    (re.compile(r'^(gulag|smart|log_|logic|job|beh|ai_|base|sect|spawn|task)', re.I), 'logic'),
    (re.compile(r'^(class_|c_?base|base_|game|deleter|release|director)', re.I), 'system'),
]


def ltx_kind(name):
    for rx, k in SECTION_KIND:
        if rx.match(name):
            return k
    return 'other'


def parse_ltx(text, file_id, db, path):
    """Yield symbols and edges for one .ltx file."""
    syms = []          # (name, parent, line)
    for lineno, raw in enumerate(text.splitlines(), 1):
        # strip comments (X-Ray: ';' starts a comment, quotes do not protect it)
        line = RE_LTX_COMMENT.sub('', raw).rstrip()
        if not line.strip():
            continue
        m = RE_LTX_INCLUDE.match(line)
        if m:
            for g in re.findall(r'"([^"]+)"', line):
                db.add_edge(file_id, None, 'include', 'include', g, None, None, None, lineno)
            continue
        m = RE_LTX_SECTION.match(line)
        if m:
            name = m.group(1).strip()
            tail = m.group(2).strip()
            # `[section]:parent_a, parent_b` -- the inheritance list lives outside
            # the brackets, so section names may freely contain ':'
            parents = []
            if tail.startswith(':'):
                p = tail[1:].strip()
                if ':' not in p:
                    parents = [x.strip() for x in re.split(r'[,;]', p) if x.strip()]
            syms.append((name, parents, lineno))
            continue
        m = RE_LTX_PARAM.match(line)
        if m:
            k = m.group(1)
            v = m.group(2).strip().strip('"')
            db.add_blob(file_id, k, v)
            db.add_param(file_id, k, v, lineno)
            continue
        m = RE_LTX_FLAG.match(line)
        if m:
            db.add_blob(file_id, m.group(1), '')
    for name, parents, lineno in syms:
        sid = db.add_sym(file_id, 'ltx_' + ltx_kind(name), name, name, None, lineno)
        for p in parents:
            db.add_edge(file_id, sid, 'inherit', ':', p, None, None, p, lineno)
    return syms

# --------------------------------------------------------- script parsing
RE_S_FUNC = re.compile(r'\bfunction\s+((?:[\w]+\.)?[\w]+::)([\w]+)\s*\(')
RE_S_PLAIN = re.compile(r'\bfunction\s+([A-Za-z_]\w*)\s*\(')
RE_S_METHOD = re.compile(r'\bfunction\s+([A-Za-z_][\w]*)\s*[:.]\s*([A-Za-z_]\w*)\s*\(')
RE_S_ASSIGN = re.compile(r'\b([\w]+)\s*=\s*function\s*\(')
RE_S_CALL = re.compile(r'([A-Za-z_]\w*)\s*\(')
RE_S_MCALL = re.compile(r'[:.]\s*([A-Za-z_]\w*)\s*\(')
RE_S_QREF = re.compile(r'([A-Za-z_][\w]*)\.script\s*::\s*([A-Za-z_]\w*)')
RE_S_DOTTED = re.compile(r'([A-Za-z_][\w]*)\.script\b')
RE_S_STR = re.compile(r'"(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\'')


def strip_lua(text):
    """Blank out comments while keeping offsets and line numbers intact.

    String literals keep their length (inner chars -> '~') so that asset paths
    inside them stay recoverable with correct line numbers.
    """
    out = []
    i, n = 0, len(text)
    while i < n:
        if text.startswith('--[[', i):
            j = text.find(']]', i)
            j = n if j < 0 else j + 2
            out.append(''.join(c if c == '\n' else ' ' for c in text[i:j]))
            i = j
            continue
        if text.startswith('--', i):
            j = text.find('\n', i)
            j = n if j < 0 else j
            out.append(' ' * (j - i))
            i = j
            continue
        c = text[i]
        if c in '"\'':
            j = i + 1
            while j < n and text[j] != c:
                j += 2 if text[j] == '\\' else 1
            j = min(j + 1, n)
            # keep the literal body verbatim: offsets and line numbers survive,
            # and asset paths inside it stay recoverable
            out.append(c + text[i + 1:max(i + 1, j - 1)] + c)
            i = j
            continue
        out.append(c)
        i += 1
    return ''.join(out)


def script_defs(text, stem):
    """Return [(qname, name, kind)] for every function/method defined."""
    res, seen = [], set()
    t = strip_lua(text)

    def push(q, nm, kind):
        if (q, nm) in seen:
            return
        seen.add((q, nm))
        res.append((q, nm, kind))

    for m in RE_S_METHOD.finditer(t):
        cls, meth = m.group(1), m.group(2)
        cls = re.sub(r'\.script$', '', cls)
        push(cls + '::' + meth, meth, 'script_method')
    for m in RE_S_FUNC.finditer(t):
        ns, nm = m.group(1)[:-2], m.group(2)
        ns = re.sub(r'\.script$', '', ns)
        push(ns + '::' + nm, nm, 'script_fn')
    for m in RE_S_PLAIN.finditer(t):
        push(stem + '::' + m.group(1), m.group(1), 'script_fn')
    for m in RE_S_ASSIGN.finditer(t):
        push(stem + '::' + m.group(1), m.group(1), 'script_fn')
    return res


# -------------------------------------------------------------- XML parsing
RE_X_ATTR = re.compile(r'([\w:.\-]+)\s*=\s*"([^"]*)"')
RE_X_TAG = re.compile(r'<\s*(/?)\s*([\w:.\-]+)((?:"[^"]*"|\'[^\']*\'|[^>"\'])*?)(/?)\s*>', re.S)
RE_X_COMMENT = re.compile(r'<!--.*?-->', re.S)
XML_ID_ATTRS = ('id', 'name', 'key', 'file')
XML_REF_ATTRS = ('parent', 'parent_section', 'template', 'spec', 'class',
                 'section', 'object', 'group', 'file', 'texture', 'sounds')
# elements that carry atlas / batch metadata rather than game objects
XML_CONTAINER = ('file', 'texture_descr', 'textures', 'game_data', 'ui', 'list', 'row')


def parse_xml(text, file_id, db, path):
    """Generic X-Ray XML walk: symbols per element, containment + typed refs."""
    t = RE_X_COMMENT.sub('', text)
    stack = []          # (tag, symbol_id)
    for m in RE_X_TAG.finditer(t):
        closing, tag, attrsrc, selfclose = m.group(1), m.group(2), m.group(3), m.group(4)
        if tag.startswith('?') or tag.startswith('!'):
            continue
        lineno = t.count('\n', 0, m.start()) + 1
        if closing:
            if stack:
                stack.pop()
            continue
        attrs = dict(RE_X_ATTR.findall(attrsrc))
        parent_sym = stack[-1][1] if stack else None
        ident = None
        for a in XML_ID_ATTRS:
            if a in attrs and attrs[a]:
                ident = attrs[a]
                break
        if tag in XML_CONTAINER:
            sid = db.add_sym(file_id, 'xml_' + tag, ident or tag, ident or tag, None, lineno)
        elif ident is not None:
            sid = db.add_sym(file_id, 'xml_' + tag, ident, ident, None, lineno)
        else:
            sid = None
        if sid is not None and parent_sym is not None:
            db.add_edge(file_id, sid, 'xml_parent', tag, tag, None, parent_sym, None, lineno)
        for a in XML_REF_ATTRS:
            if a in attrs and attrs[a]:
                db.add_edge(file_id, sid, 'xml_ref', a, attrs[a], None, None, attrs[a], lineno)
        for a in ('x', 'y', 'width', 'height', 'shade', 'complex_mode'):
            if a in attrs:
                db.add_blob(file_id, a, attrs[a])
        if not selfclose:
            stack.append((tag, sid))

# ------------------------------------------------------- binary string scan
RE_U16 = re.compile(rb'(?:[\x20-\x7e]\x00){4,}')
RE_ASC = re.compile(rb'[\x20-\x7e]{6,}')

BIN_SCAN_EXT = {
    'spawn', 'ai', 'level', 'omf', 'ogf', 'snd_static', 'ps_static', 'som',
    'details', 'ogm', 'thm', 'anm', 'fog_vol', 'env_mod', 'dm', 'xr',
    'game', 'lights', 'wallmarks', 'gs', 'seq', 'omf',
}
BIN_SCAN_CAP = {  # bytes to read per file
    'ogf': 6 << 20, 'omf': 6 << 20, 'ogm': 6 << 20, 'thm': 2 << 20,
    'anm': 2 << 20, 'dm': 4 << 20, 'xr': 4 << 20, 'game': 4 << 20,
    'lights': 4 << 20, 'wallmarks': 4 << 20, 'gs': 2 << 20, 'seq': 1 << 20,
    'spawn': 256 << 20, 'ai': 128 << 20, 'level': 128 << 20,
    'snd_static': 32 << 20, 'ps_static': 32 << 20, 'som': 8 << 20,
    'details': 32 << 20, 'fog_vol': 1 << 20, 'env_mod': 1 << 20,
}
SKIP_BIG = {'cform', 'geom', 'geomx', 'db0', 'db1', 'db2', 'db3', 'db4',
            'dds', 'ogg', 'exe', 'dll'}


def bin_strings(data):
    out = set()
    for m in RE_U16.finditer(data):
        out.add(m.group().decode('utf-16-le', 'ignore'))
    for m in RE_ASC.finditer(data):
        s = m.group().decode('ascii', 'ignore')
        if len(s) >= 6 and ' ' not in s:
            out.add(s)
    return out
