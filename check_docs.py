"""Offline Markdown checks. Standard library only; see README for parser limits."""
import argparse
import json
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

SKIP = {'.git', '.venv', 'venv', 'node_modules', 'dist', 'build', '__pycache__'}

def prose_lines(text):
    fence = None
    for number, line in enumerate(text.splitlines(), 1):
        match = re.match(r'^\s*(`{3,}|~{3,})', line)
        if match:
            marker = match[1]
            if fence is None:
                fence = marker
            elif marker[0] == fence[0] and len(marker) >= len(fence):
                fence = None
            continue
        if fence is None:
            yield number, re.sub(r'`[^`]*`', '', line)

def check_file(file, root, metadata=False, terms=None):
    issues = []
    rel = file.relative_to(root).as_posix()
    def add(line, rule, message, severity='error'):
        issues.append(dict(file=rel, line=line, rule=rule, message=message, severity=severity))
    try:
        text = file.read_text(encoding='utf-8-sig')
    except (UnicodeError, OSError):
        add(1, 'read', 'Cannot read this file as UTF-8.')
        return issues
    lines = list(prose_lines(text))
    if not any(re.match(r'^#\s+\S', line) for _, line in lines):
        add(1, 'title', 'Add a level-one heading that identifies the topic.')
    if metadata:
        block = re.match(r'\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)', text, re.S)
        values = dict(re.findall(r'^([a-z_]+):\s*(.*?)\s*$', block[1], re.M)) if block else {}
        for key in ('title', 'audience', 'status'):
            if not values.get(key):
                add(1, 'metadata', f'Add a non-empty {key} field in front matter.')
    for number, line in lines:
        # Inline destinations without nested parentheses, plus reference definitions.
        targets = re.findall(r'\]\(<?([^\s)>]+)>?(?:\s+"[^"]*")?\)', line)
        definition = re.match(r'^\s*\[[^\]]+\]:\s*<?([^\s>]+)>?', line)
        if definition:
            targets.append(definition[1])
        for target in targets:
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            # Root-relative web URLs need a site routing configuration, not disk lookup.
            if parsed.path.startswith('/'):
                continue
            dest = (file.parent / unquote(parsed.path)).resolve()
            if not dest.is_relative_to(root.resolve()):
                add(number, 'link', f'Local link leaves the repository: {target}')
            elif not dest.exists():
                add(number, 'link', f'Local link target does not exist: {target}')
        for term, preferred in (terms or {}).items():
            if re.search(r'(?<!\w)' + re.escape(term) + r'(?!\w)', line, re.I):
                add(number, 'terminology', f'Prefer "{preferred}" to "{term}"; check context.', 'warning')
    return issues

def run(root, metadata=False, terms=None):
    files = sorted(p for p in root.rglob('*.md') if not any(part in SKIP for part in p.relative_to(root).parts))
    issues = [issue for file in files for issue in check_file(file, root, metadata, terms)]
    return files, issues

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', nargs='?', default='.')
    parser.add_argument('--require-metadata', action='store_true')
    parser.add_argument('--terms', type=Path, help='JSON object mapping discouraged terms to preferred terms')
    parser.add_argument('--json', action='store_true', dest='as_json')
    parser.add_argument('--strict', action='store_true', help='Fail on terminology warnings too')
    args = parser.parse_args()
    root = Path(args.root).resolve()
    if not root.is_dir():
        parser.error('root must be an existing directory')
    try:
        terms = json.loads(args.terms.read_text(encoding='utf-8')) if args.terms else {}
        if not isinstance(terms, dict) or not all(isinstance(k, str) and k and isinstance(v, str) and v for k, v in terms.items()):
            raise ValueError('terms must map non-empty strings to non-empty strings')
        files, issues = run(root, args.require_metadata, terms)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    if not files:
        issues.append(dict(file='.', line=1, rule='input', message='No Markdown files found.', severity='error'))
    if args.as_json:
        print(json.dumps(dict(files_checked=len(files), issues=issues), indent=2))
    else:
        for issue in issues:
            print('{file}:{line}: {severity} [{rule}] {message}'.format(**issue))
        print(f'Checked {len(files)} Markdown file(s); found {len(issues)} issue(s).')
    return int(any(i['severity'] == 'error' or args.strict for i in issues))

if __name__ == '__main__':
    raise SystemExit(main())
