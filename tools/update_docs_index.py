#!/usr/bin/env python3
"""Build public documentation indexes from tracked paths; check relative file links.

No game files, SQLite database or network connection are needed.
"""
import argparse
from collections import Counter
from datetime import date
import json
import os
from pathlib import Path
import posixpath
import re
import subprocess
import sys
from urllib.parse import quote, unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
OUTPUTS = {'docs/INDEX.md', 'docs/FILES.json', 'docs/en/docs/INDEX.md'}
TRANSLATIONS = ROOT / 'docs/en/translation-manifest.json'


def tracked_paths(source):
    if source:
        # Optional GitHub recursive-tree export, useful when preparing an API commit.
        data = json.loads(Path(source).read_text(encoding='utf-8'))
        paths = {x['path'] for x in data['tree'] if x['type'] == 'blob'}
    else:
        result = subprocess.run(
            ['git', 'ls-files', '-z'], cwd=ROOT, check=True, capture_output=True)
        paths = set(result.stdout.decode('utf-8').rstrip('\0').split('\0'))
    return sorted((paths | OUTPUTS) - {''})


def category(path):
    if path.startswith('docs/en/'):
        return 'English documentation'
    if path.startswith('docs/archive/'):
        return 'Исторический индекс установки'
    if path.startswith('docs/snapshot-2026-10-28/'):
        return 'Исходные документы и отчёты этапов'
    if path.startswith('docs/') or path in {'README.md', 'INDEX.md', 'CONTRIBUTING.md'}:
        return 'Текущая документация и навигация'
    if path.startswith('modules/'):
        return 'Публичные исходные модули'
    if path.startswith('CCZMP/') or path == 'CCZMP_полный_файл.ltx':
        return 'Ранние концепции и прототипы'
    if path.startswith('gamedata/') or path == 'items.ltx':
        return 'Ранний опубликованный фрагмент gamedata'
    if path.startswith('tools/'):
        return 'Инструменты публичной документации'
    if path in {'build.py', 'lib.py', 'q.py', 'report.py'}:
        return 'Инструменты локального графа Anomaly'
    return 'Прочее'


def title(path):
    f = ROOT / path
    if path == 'docs/INDEX.md':
        return 'Полный индекс опубликованной документации'
    if f.exists() and path.endswith('.md'):
        for line in f.read_text(encoding='utf-8').splitlines():
            if line.startswith('# '):
                return line[2:].strip().replace('|', '\\|')
    return Path(path).name.replace('|', '\\|')


def build(paths, updated):
    translation_data = json.loads(TRANSLATIONS.read_text(encoding='utf-8')) if TRANSLATIONS.exists() else {'documents': []}
    translations = {x['source']: x['english'] for x in translation_data['documents']}
    counts = Counter(p.split('/')[0] if '/' in p else '(корень)' for p in paths)
    records = [{'path': p, 'category': category(p)} for p in paths]
    manifest = {
        'schema_version': 1,
        'updated': updated,
        'scope': 'Tracked public repository files; not the full installed game or dependency graph.',
        'file_count': len(paths),
        'counts_by_root': dict(sorted(counts.items())),
        'files': records,
    }
    lines = [
        '# Полный индекс опубликованной документации', '',
        f'Обновлено {updated}. Состав построен по отслеживаемым файлам Git.', '',
        '**Русский** · [English](en/docs/INDEX.md)', '',
        '[Начать здесь](README.md) · [Статус](STATUS_RU.md) · [80 направлений](SYSTEMS_RU.md) · '
        '[Транспорт](TRANSPORT_RU.md) · [Состав всех файлов](FILES.json) · '
        '[Пересборка](INDEXING_RU.md)', '',
        'Датированные документы сохраняют выводы своего этапа. Текущий реестр учитывает '
        'более позднее ядро жизни 22 жителей и публичный стенд Locks. ТЗ описывает цель, '
        'а не доказательство реализации.', '',
    ]
    docs = [p for p in paths if not p.startswith('docs/en/') and (p.endswith('.md') or
            (p.startswith('docs/') and p.endswith('.txt')) or
            (p.startswith('CCZMP/Concept/') and p.endswith('.ltx')) or
            p in {'CCZMP/README.ltx', 'CCZMP_полный_файл.ltx'})]
    for group in dict.fromkeys(category(p) for p in docs):
        members = [p for p in docs if category(p) == group]
        lines += [f'## {group} ({len(members)})', '', '| Документ | English | Путь |', '|---|---|---|']
        for p in members:
            target = quote(posixpath.relpath(p, 'docs'), safe='/._-')
            english = '[EN](' + quote(posixpath.relpath(translations[p], 'docs'), safe='/._-') + ')' if p in translations else '—'
            lines.append(f'| [{title(p)}]({target}) | {english} | `{p}` |')
        lines.append('')
    lines += ['## Состав репозитория', '',
              f'Всего **{len(paths)} файлов**, включая код, конфиги и архивные материалы; '
              'это не число реализованных систем.', '', '| Область | Файлов |', '|---|---:|']
    lines += [f'| `{key}` | {value} |' for key, value in sorted(counts.items())]
    lines += ['', 'Полные пути, включая не-документные файлы: [FILES.json](FILES.json). '
              'Бинарные модели, сохранения и полная локальная база зависимостей сюда не входят.', '']
    en_base = 'docs/en/docs'
    en_lines = ['# Complete English documentation index', '',
                '[Русский](../../INDEX.md) · **English** · [Project overview](../README.md) · '
                '[Translation notes](../TRANSLATION.md)', '',
                f'Updated {updated}. English counterparts for **{len(translations)} source documents**, '
                'including technical guides, concepts, dated reports and legacy material.', '',
                'Dated reports retain the conclusions and limitations of their original stage. '
                'Specifications describe intended behavior, not evidence of completion. '
                'Identifiers, executable examples and original file paths are preserved.', '',
                '| Document | English | Русский |', '|---|---|---|']
    for source, english in translations.items():
        en_target = quote(posixpath.relpath(english, en_base), safe='/._-')
        ru_target = quote(posixpath.relpath(source, en_base), safe='/._-')
        en_lines.append(f'| {title(english)} | [Read]({en_target}) | [RU]({ru_target}) |')
    en_lines += ['', '## Maintenance', '',
                 '[Rebuild the indexes](INDEXING_EN.md) · [Translation coverage](../translation-manifest.json) · '
                 '[All repository files](../../FILES.json)', '',
                 f'The repository contains **{len(paths)} tracked files**; this includes both languages, '
                 'code and configuration files. It is not the number of implemented systems.', '']
    return {'docs/INDEX.md': '\n'.join(lines),
            'docs/en/docs/INDEX.md': '\n'.join(en_lines),
            'docs/FILES.json': json.dumps(manifest, ensure_ascii=False, indent=2) + '\n'}


def missing_links(paths, outputs):
    known = set(paths)
    directories = {'.'}
    for path in paths:
        parent = posixpath.dirname(path)
        while parent:
            directories.add(parent)
            parent = posixpath.dirname(parent)
    problems = []
    for path in paths:
        if not path.endswith('.md'):
            continue
        f = ROOT / path
        if path in outputs:
            content = outputs[path]
        elif f.exists():
            content = f.read_text(encoding='utf-8')
        else:
            problems.append(f'{path}: Markdown source is not available locally')
            continue
        content = re.sub(r'```.*?```', '', content, flags=re.S)
        for link in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)', content):
            link = link.split(' "', 1)[0].strip('<>')
            url = urlsplit(link)
            if url.scheme or url.netloc or not url.path:
                continue
            target = posixpath.normpath(posixpath.join(
                posixpath.dirname(path), unquote(url.path)))
            if target not in known and target not in directories:
                problems.append(f'{path}: {link} -> {target}')
    return problems


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--date', default=date.today().isoformat())
    parser.add_argument('--paths-json', help='Optional GitHub recursive-tree JSON')
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    date.fromisoformat(args.date)
    paths = tracked_paths(args.paths_json)
    outputs = build(paths, args.date)
    errors = missing_links(paths, outputs)
    for path, content in outputs.items():
        f = ROOT / path
        if args.check:
            if not f.exists() or f.read_text(encoding='utf-8') != content:
                errors.append(f'{path}: generated index is out of date')
        else:
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_text(content, encoding='utf-8', newline='\n')
    if errors:
        print('\n'.join(errors), file=sys.stderr)
        return 1
    print(f'OK: {len(paths)} tracked files; generated indexes and relative file links verified')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
