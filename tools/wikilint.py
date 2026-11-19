"""Check a project wiki against the rules in AGENTS.md.

usage: python tools/wikilint.py [--root PATH] [--strict]

Errors (exit code 1): broken links, pages missing from the index, bad log headings,
duplicate error ids, possible secrets, data or model files, em dashes, emojis.
Warnings: fact pages without an evidence tag (how-to pages are instructions and need none), placeholders left in a page, log entries out of order.
--strict turns warnings into errors.
"""
import argparse
import os
import re
import sys

LOG_TYPES = ('ingest', 'query', 'write', 'fix', 'decide', 'lint', 'handoff')
TAGS = ('[Certain', '[Likely', '[Guessing', '[User-reported')
NO_TAG_NEEDED = {'index.md', 'log.md', 'glossary.md', 'README.md', 'sources.md', 'errors.md'}
DATA_EXT = {'.npy', '.npz', '.pt', '.pth', '.ckpt', '.safetensors', '.onnx', '.h5', '.hdf5',
            '.parquet', '.feather', '.pkl', '.joblib'}
MAX_BYTES = 5 * 1024 * 1024
SKIP_DIRS = {'.git', '.venv', '__pycache__', 'node_modules', '.obsidian'}
SECRETS = [
    (r'hf_[A-Za-z0-9]{30,}', 'Hugging Face token'),
    (r'ghp_[A-Za-z0-9]{36}', 'GitHub token'),
    (r'github_pat_[A-Za-z0-9_]{40,}', 'GitHub token'),
    (r'sk-[A-Za-z0-9_-]{32,}', 'API key'),
    (r'AKIA[0-9A-Z]{16}', 'AWS key'),
    (r'xox[abprs]-[A-Za-z0-9-]{10,}', 'Slack token'),
    (r'-----BEGIN [A-Z ]*PRIVATE KEY-----', 'private key'),
    (r'X-Amz-Signature=[0-9a-f]{20,}', 'signed URL'),
]
EM_DASH = '—'
EMOJI = re.compile('[\U0001F000-\U0001FAFF☀-➿️]')
LINK = re.compile(r'\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]')
LOG_HEAD = re.compile(r'^## (\d{4}-\d{2}-\d{2}) - (' + '|'.join(LOG_TYPES) + r') - \S.*$')
PLACEHOLDER = re.compile(r'<(?!!--)(?![a-z]+>)(?!/)[A-Za-z][^<>\n]{2,100}>')
ERR_ID = re.compile(r'^\|\s*([EBT]\d+)\s*\|')


class Report:
    def __init__(self):
        self.errors, self.warnings = [], []

    def error(self, path, line, msg):
        self.errors.append(f'ERROR {path}:{line} {msg}')

    def warn(self, path, line, msg):
        self.warnings.append(f'WARN  {path}:{line} {msg}')


def text_lines(path):
    """Lines with fenced code blocks blanked and inline code removed, so examples are not checked."""
    out, fence = [], False
    with open(path, encoding='utf-8', errors='replace') as f:
        for line in f:
            line = line.rstrip('\n')
            if line.lstrip().startswith('```'):
                fence = not fence
                out.append('')
                continue
            out.append('' if fence else re.sub(r'`[^`]*`', '', line))
    return out


def walk(root):
    for d, dirs, files in os.walk(root):
        dirs[:] = [x for x in dirs if x not in SKIP_DIRS]
        for f in files:
            yield os.path.join(d, f)


def main():
    ap = argparse.ArgumentParser(description='Check a project wiki against AGENTS.md.')
    ap.add_argument('--root', default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ap.add_argument('--strict', action='store_true', help='treat warnings as errors')
    a = ap.parse_args()
    root = os.path.abspath(a.root)
    rel = lambda p: os.path.relpath(p, root)
    r = Report()
    wiki = os.path.join(root, 'wiki')
    if not os.path.isdir(wiki):
        print(f'no wiki/ folder under {root}')
        return 2

    # pages: bare name and path (relative to wiki/, no .md) both resolve; bare names must be unique
    pages, by_name = set(), {}
    for p in walk(wiki):
        if p.endswith('.md'):
            key = os.path.relpath(p, wiki)[:-3].replace(os.sep, '/')
            pages.add(key)
            by_name.setdefault(os.path.basename(key), []).append(key)

    def resolve(target):
        t = target.strip().removesuffix('.md')
        if t.startswith('wiki/'):
            t = t[5:]
        if t in pages:
            return t, None
        hits = by_name.get(t, [])
        if len(hits) == 1:
            return hits[0], None
        if len(hits) > 1:
            return None, f'ambiguous link [[{target}]]: use one of {", ".join(sorted(hits))}'
        return None, f'broken link [[{target}]]'

    # 1. links in every markdown file outside templates/
    linked_from_index = set()
    for p in walk(root):
        if not p.endswith('.md') or rel(p).startswith('templates' + os.sep):
            continue
        for n, line in enumerate(text_lines(p), 1):
            for m in LINK.finditer(line):
                target = m.group(1)
                if '<' in target:
                    continue
                key, problem = resolve(target)
                if problem:
                    r.error(rel(p), n, problem)
                elif os.path.abspath(p) == os.path.join(wiki, 'index.md'):
                    linked_from_index.add(key)

    # 2. every page is in the index
    for key in sorted(pages - linked_from_index - {'index'}):
        r.error(f'wiki/{key}.md', 1, 'not in index: add a line to wiki/index.md')

    # 3. log headings and order
    log = os.path.join(wiki, 'log.md')
    if os.path.exists(log):
        last = ''
        for n, line in enumerate(text_lines(log), 1):
            if line.startswith('## '):
                m = LOG_HEAD.match(line)
                if not m:
                    r.error('wiki/log.md', n, f'log heading must be "## YYYY-MM-DD - type - summary" with type in {", ".join(LOG_TYPES)}')
                    continue
                if m.group(1) < last:
                    r.warn('wiki/log.md', n, f'entry dated {m.group(1)} after {last}: append new entries at the end')
                last = max(last, m.group(1))

    # 4. unique ids in the errors register
    errs = os.path.join(wiki, 'errors.md')
    if os.path.exists(errs):
        seen = {}
        for n, line in enumerate(text_lines(errs), 1):
            m = ERR_ID.match(line)
            if m:
                if m.group(1) in seen:
                    r.error('wiki/errors.md', n, f'duplicate id {m.group(1)} (first on line {seen[m.group(1)]})')
                seen.setdefault(m.group(1), n)

    # 5. evidence tags and placeholders on wiki pages
    for key in sorted(pages):
        p = os.path.join(wiki, key + '.md')
        lines = text_lines(p)
        body = '\n'.join(lines)
        if os.path.basename(p) not in NO_TAG_NEEDED and not key.startswith('howto/') and not any(t in body for t in TAGS):
            r.warn(f'wiki/{key}.md', 1, 'no evidence tag ([Certain], [Likely], [Guessing], [User-reported])')
        for n, line in enumerate(lines, 1):
            m = PLACEHOLDER.search(line)
            if m:
                r.warn(f'wiki/{key}.md', n, f'placeholder left: {m.group(0)}')

    # 6. secrets, data files, writing style across the repository
    for p in walk(root):
        rp = rel(p)
        ext = os.path.splitext(p)[1].lower()
        if ext in DATA_EXT:
            r.error(rp, 1, f'data or model file ({ext}): keep it outside the wiki and link to it')
            continue
        try:
            size = os.path.getsize(p)
        except OSError:
            continue
        if size > MAX_BYTES:
            r.error(rp, 1, f'file is {size / 1e6:.1f} MB: large files do not belong in the wiki')
            continue
        try:
            with open(p, encoding='utf-8') as f:
                content = f.read()
        except (UnicodeDecodeError, OSError):
            continue
        if rp == os.path.join('tools', 'wikilint.py'):
            continue
        for n, line in enumerate(content.splitlines(), 1):
            for pat, what in SECRETS:
                if re.search(pat, line):
                    r.error(rp, n, f'possible secret ({what}): remove it and rotate the credential')
            if ext == '.md':
                if EM_DASH in line:
                    r.error(rp, n, 'em dash: use " - " instead')
                if EMOJI.search(line):
                    r.error(rp, n, 'emoji: remove it')

    for line in r.errors + r.warnings:
        print(line)
    n_err = len(r.errors) + (len(r.warnings) if a.strict else 0)
    print(f'{len(pages)} pages, {len(r.errors)} errors, {len(r.warnings)} warnings')
    return 1 if n_err else 0


if __name__ == '__main__':
    sys.exit(main())
