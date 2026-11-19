"""Create a wiki page from its template, list it in the index and log it.

usage: python tools/new_page.py <type> <name> "<one-line summary>"
types: concept, decision, howto, experiment, literature, theory

examples:
  python tools/new_page.py concept data-split "how train, validation and test are separated"
  python tools/new_page.py decision use-postgres "store results in Postgres instead of CSV"
"""
import datetime
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TYPES = {  # type: (folder under wiki/, index section, numbered prefix)
    'concept': ('concepts', 'concepts', None),
    'decision': ('decisions', 'decisions', 4),
    'howto': ('howto', 'howto', None),
    'experiment': ('experiments', 'experiments', 2),
    'literature': ('literature', 'literature', None),
    'theory': ('theory', 'theory', None),
}


def slug(s):
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')


def next_number(folder, width):
    nums = [int(m.group(1)) for f in os.listdir(folder) if (m := re.match(r'(\d+)-', f))]
    return str(max(nums, default=0) + 1).zfill(width)


def add_to_index(section, line):
    path = os.path.join(ROOT, 'wiki', 'index.md')
    lines = open(path, encoding='utf-8').read().split('\n')
    try:
        start = lines.index(f'## {section}')
    except ValueError:
        lines += ['', f'## {section}', '']
        start = len(lines) - 2
    end = start + 1
    while end < len(lines) and not lines[end].startswith('## '):
        end += 1
    while end > start + 1 and lines[end - 1].strip() == '':
        end -= 1
    lines.insert(end, line)
    open(path, 'w', encoding='utf-8').write('\n'.join(lines))


def append_log(summary, details):
    path = os.path.join(ROOT, 'wiki', 'log.md')
    text = open(path, encoding='utf-8').read().rstrip('\n')
    today = datetime.date.today().isoformat()
    open(path, 'w', encoding='utf-8').write(f'{text}\n\n## {today} - write - {summary}\n\n- {details}\n')


def main(argv):
    if len(argv) != 4 or argv[1] not in TYPES:
        print(__doc__)
        return 2
    kind, name, summary = argv[1], slug(argv[2]), argv[3].strip()
    folder_name, section, width = TYPES[kind]
    folder = os.path.join(ROOT, 'wiki', folder_name)
    if not os.path.isdir(folder):
        print(f'wiki/{folder_name}/ does not exist (optional module removed?)')
        return 1
    num = next_number(folder, width) if width else None
    if num:
        name = f'{num}-{name}'
    path = os.path.join(folder, f'{name}.md')
    if os.path.exists(path):
        print(f'{os.path.relpath(path, ROOT)} already exists')
        return 1
    template = open(os.path.join(ROOT, 'templates', f'{kind}.md'), encoding='utf-8').read()
    heading = f'# {num} - {summary}' if num else f'# {name.replace("-", " ")}'
    template = re.sub(r'^# .*$', heading, template, count=1, flags=re.M)
    if kind == 'decision':
        template = template.replace('- Date: <YYYY-MM-DD>', f'- Date: {datetime.date.today().isoformat()}')
    open(path, 'w', encoding='utf-8').write(template)
    add_to_index(section, f'- [[{name}]] - {summary}')
    append_log(f'new {kind} page {name}', f'created [[{name}]] from `templates/{kind}.md`: {summary}')
    print(f'created {os.path.relpath(path, ROOT)}; added to wiki/index.md and wiki/log.md')
    if os.path.exists(os.path.join(folder, 'README.md')):
        print(f'also add a row for it to wiki/{folder_name}/README.md')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
