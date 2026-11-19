"""Set up a new wiki from this template.

usage: python tools/init_wiki.py "<project name>" [--owner "<name>"] [--no-ml]

- writes the project name, owner and today's date into wiki/context.md and handoff.md
- --no-ml removes the optional ML and research module (experiments, literature, theory,
  docs/results.md, docs/claims.md, their templates and index sections)
- logs the setup in wiki/log.md
Run it once, right after creating the repo from the template.
"""
import argparse
import datetime
import os
import re
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ML_DIRS = ['wiki/experiments', 'wiki/literature', 'wiki/theory']
ML_FILES = ['docs/results.md', 'docs/claims.md', 'templates/experiment.md', 'templates/literature.md', 'templates/theory.md']
ML_SECTIONS = ['experiments', 'literature', 'theory']


def edit(rel, fn):
    path = os.path.join(ROOT, rel)
    text = open(path, encoding='utf-8').read()
    open(path, 'w', encoding='utf-8').write(fn(text))


def drop_sections(text, names):
    out, skip = [], False
    for line in text.split('\n'):
        if line.startswith('## '):
            skip = line[3:].strip() in names
        if not skip:
            out.append(line)
    return re.sub(r'\n{3,}', '\n\n', '\n'.join(out)).rstrip('\n') + '\n'


def main():
    ap = argparse.ArgumentParser(description='Set up a new wiki from this template.')
    ap.add_argument('name')
    ap.add_argument('--owner', default=None)
    ap.add_argument('--no-ml', action='store_true', help='remove the optional ML and research module')
    a = ap.parse_args()
    today = datetime.date.today().isoformat()

    def ctx(t):
        t = t.replace('- Name: <project name>', f'- Name: {a.name}')
        t = t.replace('- Started: <YYYY-MM-DD>', f'- Started: {today}')
        t = t.replace('- Status: <planning | active | paused | done>', '- Status: planning')
        if a.owner:
            t = t.replace('- Owner: <person or team>', f'- Owner: {a.owner}')
        return t
    edit('wiki/context.md', ctx)
    edit('handoff.md', lambda t: t.replace('Last updated: YYYY-MM-DD', f'Last updated: {today}'))
    edit('wiki/errors.md', lambda t: t.replace(
        '| E01 | `wiki/context.md` placeholder | "<project name>" | replace with the real name on the first edit | open |',
        f'| E01 | `wiki/context.md` placeholder | the template project name | set to "{a.name}" by tools/init_wiki.py | resolved {today}: init |'))
    if a.owner:
        edit('wiki/decisions/0001-record-decisions.md', lambda t: t.replace('- Deciders: <project owner>', f'- Deciders: {a.owner}'))

    removed = []
    if a.no_ml:
        for d in ML_DIRS:
            if os.path.isdir(os.path.join(ROOT, d)):
                shutil.rmtree(os.path.join(ROOT, d)); removed.append(d + '/')
        for f in ML_FILES:
            if os.path.exists(os.path.join(ROOT, f)):
                os.remove(os.path.join(ROOT, f)); removed.append(f)
        edit('wiki/index.md', lambda t: drop_sections(t, ML_SECTIONS))
        edit('templates/README.md', lambda t: '\n'.join(l for l in t.split('\n') if 'optional ML module' not in l))
        edit('AGENTS.md', lambda t: '\n'.join(l for l in t.split('\n') if not re.search(r'optional, |experiments/|literature/|theory/|templates/(experiment|literature|theory)\.md', l)))

    log_note = f'set the project name to {a.name}' + (f', owner {a.owner}' if a.owner else '') + (f'; removed the ML module: {", ".join(removed)}' if removed else '')
    edit('wiki/log.md', lambda t: t.rstrip('\n') + f'\n\n## {today} - write - wiki set up for {a.name}\n\n- {log_note}\n')
    print(f'set up "{a.name}"' + (f', removed {len(removed)} ML items' if removed else ''))
    print('next: fill the remaining <...> placeholders in wiki/context.md and handoff.md, then run python tools/wikilint.py')
    return 0


if __name__ == '__main__':
    sys.exit(main())
