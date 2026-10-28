#!/usr/bin/env python3
"""Check documentation translation coverage, technical literals and Markdown structure."""
from pathlib import Path
from collections import Counter
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'docs/en/translation-manifest.json'
# Generated/edited entry pages need editorial comparison rather than equal row counts.
EDITORIAL = {'README.md', 'docs/README.md', 'docs/STATUS_RU.md',
             'docs/ROADMAP_RU.md', 'docs/INDEX.md', 'docs/INDEXING_RU.md',
             'docs/CHANGES_RU.md'}
FENCES = re.compile(r'(?ms)^\s*(`{3,}|~{3,})[^\n]*\n.*?^\s*\1[^\n]*(?:\n|$)')


def blocks(text):
    return [m.group(0).strip() for m in FENCES.finditer(text)]


def prose(text):
    return FENCES.sub('', text)


def main():
    manifest = json.loads(MANIFEST.read_text(encoding='utf-8'))
    entries = manifest['documents']
    problems = []
    sources = {x['source'] for x in entries}
    translations = {x['english'] for x in entries}
    if len(entries) != len(sources) or len(entries) != len(translations):
        problems.append('Source/translation mapping is not one-to-one')
    if manifest['source_document_count'] != len(entries):
        problems.append('Manifest document count is incorrect')
    # Check tracked Markdown and prose notes; executable configuration files are excluded.
    for path in ROOT.rglob('*'):
        if not path.is_file() or '.git' in path.parts:
            continue
        p = path.relative_to(ROOT).as_posix()
        if p.startswith('docs/en/'):
            continue
        selected = p.endswith('.md') or (p.startswith('docs/') and p.endswith('.txt'))
        selected |= (p.startswith('CCZMP/Concept/') and p.endswith('.ltx'))
        selected |= p in {'CCZMP/README.ltx', 'CCZMP_полный_файл.ltx'}
        if selected and p not in sources:
            problems.append(f'No translation registered for {p}')
    for entry in entries:
        source, target = entry['source'], entry['english']
        if not (ROOT / source).exists() or not (ROOT / target).exists():
            problems.append(f'Missing source or translation: {source} -> {target}')
            continue
        a = (ROOT / source).read_text(encoding='utf-8-sig')
        b = (ROOT / target).read_text(encoding='utf-8-sig')
        if re.search(r'ZXQ\s*\d+\s*QXZ', b, re.I):
            problems.append(f'Unresolved translation placeholder: {target}')
        if source.endswith('.md') and '[English](' not in a:
            problems.append(f'Missing English language switch: {source}')
        if '[Русский](' not in b:
            problems.append(f'Missing Russian language switch: {target}')
        if source in EDITORIAL or not source.endswith('.md'):
            continue
        if blocks(a) != blocks(b):
            problems.append(f'Executable examples changed: {target}')
        pa, pb = prose(a), prose(b)
        for name, pattern in [('headings', r'(?m)^#{1,6}\s'),
                              ('table rows', r'(?m)^\|')]:
            na, nb = len(re.findall(pattern, pa)), len(re.findall(pattern, pb))
            if name == 'headings' and na == 0 and nb == 1:
                continue  # A title was added to an originally untitled prose note.
            if na != nb:
                problems.append(f'Mismatched {name}: {target}')
        if Counter(re.findall(r'`[^`\n]+`', pa)) != Counter(re.findall(r'`[^`\n]+`', pb)):
            problems.append(f'Inline technical literals changed: {target}')
        ra = re.findall(r'(?m)^\|.*$', pa)
        rb = re.findall(r'(?m)^\|.*$', pb)
        if len(ra) == len(rb):
            for i, (x, y) in enumerate(zip(ra, rb), 1):
                if x.count('|') != y.count('|'):
                    problems.append(f'Table column count changed at row {i}: {target}')
    if problems:
        print('\n'.join(problems), file=sys.stderr)
        return 1
    print(f'OK: {len(entries)} source documents have English counterparts; '
          'language switches, structural parity and technical examples checked')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
