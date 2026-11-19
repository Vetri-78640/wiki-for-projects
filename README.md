# wiki-for-projects

A template for a project wiki that agents and people maintain together. Sources stay untouched in `raw/`, verified pages live in `wiki/`, and `AGENTS.md` holds the rules every editor follows. A lint check keeps it consistent, and it runs on every push.

It is built for long projects where the reasons behind the work get lost: research and ML projects, course projects, competitions, software with many decisions. The optional ML module adds experiment, literature and theory pages; other projects remove it with one command.

## why

Chat history and scattered notes do not survive a long project. Each new session, by a person or an agent, re-reads everything, repeats old mistakes, and cannot tell a checked fact from a guess. This template keeps one compact, linked, verified record instead:

- **evidence on every claim**: each fact points to a file, log line or URL and carries a tag (`[Certain]`, `[Likely]`, `[Guessing]`, `[User-reported]`)
- **nothing is silently rewritten**: `raw/` is never edited, `wiki/log.md` is append-only, and corrections go in `wiki/errors.md`
- **decisions keep their reasons**: one short record per significant choice, written before acting
- **any session can continue the work**: `handoff.md` says where things stand and what comes next

## the pattern

| layer | what it is | who changes it |
|---|---|---|
| `raw/` | sources exactly as received: logs, exports, papers, notes | added to, never edited |
| `wiki/` | compact pages built from the sources, linked with `[[page]]` | agents and people, by the rules |
| `AGENTS.md` | the schema: layout, rules, templates, workflows | the project owner |

Think of it like a build: `raw/` is the source code, the agent is the compiler, `wiki/` is the output, and the lint check is the test suite. This follows the "LLM wiki" pattern described by Andrej Karpathy, with decision records (Nygard, MADR), the separation of page types from Diataxis, and the cross-tool `AGENTS.md` file.

## quick start

1. On GitHub, click **Use this template** to create your project's wiki repo, then clone it.
2. Set it up (add `--no-ml` if the project has no experiments or papers):
   ```
   python tools/init_wiki.py "My Project" --owner "Your Name"
   ```
3. Fill the `<...>` placeholders in `wiki/context.md` and `handoff.md`.
4. Check it:
   ```
   python tools/wikilint.py
   ```
5. Point your agent at the folder. Claude Code reads `CLAUDE.md`, which loads `AGENTS.md`; Codex, Cursor, Gemini CLI and other tools read `AGENTS.md` directly.

Python 3.9 or newer; no packages needed.

## layout

```
AGENTS.md            rules for agents and people (CLAUDE.md points here)
handoff.md           current state, next steps, open questions
raw/                 sources, never edited
wiki/
  context.md         stable facts, read first
  index.md           catalog of every page
  log.md             append-only operation log
  sources.md         every source, its origin and trust level
  errors.md          corrections register: wrong statements, bugs, tool notes
  glossary.md        project terms
  decisions/         decision records (0001-...)
  concepts/          background ideas
  howto/             step-by-step tasks
  experiments/       optional ML module
  literature/        optional ML module
  theory/            optional ML module, with scripts/ and scripts/out/
docs/                outputs for people (results.md and claims.md in the ML module)
templates/           one template per page type
tools/               wikilint.py, new_page.py, init_wiki.py
```

## page types

| type | answers | template |
|---|---|---|
| concept | what is this idea and why does it matter here? | `templates/concept.md` |
| decision | what did we choose, over what, and why? | `templates/decision.md` |
| how-to | how do I do this task? | `templates/howto.md` |
| experiment | what did we test, what happened, what is the verdict? | `templates/experiment.md` |
| literature | what does this paper claim and how do we use it? | `templates/literature.md` |
| theory | why is this true, and which script checks it? | `templates/theory.md` |

Create pages with the tool, which also lists them in the index and logs them:

```
python tools/new_page.py decision move-to-postgres "store results in Postgres instead of CSV"
python tools/new_page.py experiment ridge-baseline "ridge regression baseline"
```

## workflows

- **ingest**: copy a source into `raw/<area>/`, add a row to `wiki/sources.md`, update the pages it affects, log it.
- **query**: read `wiki/index.md`, open only the pages needed, answer with evidence paths. File reusable answers as pages.
- **write**: create or update a page from its template; keep the index, the log and `handoff.md` current.
- **correct**: fix the page, add a row to `wiki/errors.md`, log it. Never delete history.
- **decide**: write the decision record before acting; supersede, never rewrite.
- **lint**: `python tools/wikilint.py` before every commit.
- **hand off**: update `handoff.md` at the end of every session.

## what the lint check enforces

| check | level |
|---|---|
| every `[[link]]` resolves, every page is in the index | error |
| log headings read `## YYYY-MM-DD - type - summary` | error |
| error ids in `wiki/errors.md` are unique | error |
| no tokens, private keys or signed URLs | error |
| no data or model files (`.npy`, `.pt`, `.safetensors`, ...) and nothing over 5 MB | error |
| no em dashes or emojis in Markdown | error |
| fact pages carry an evidence tag; no `<...>` placeholders left | warning |

`--strict` turns warnings into errors. The same check runs as a GitHub Action on every push and pull request.

## what never goes in

Datasets, model weights, prediction files, credentials, tokens, signed URLs, and anything the data's licence forbids sharing. Keep a pointer instead: a path outside the repo, a dataset name or a URL, with the terms noted in `wiki/sources.md`.

## viewing the wiki

The pages are plain Markdown with `[[wikilinks]]`, so the folder also opens as an Obsidian vault, with backlinks and a graph view.

## further reading

- The LLM wiki pattern: https://blog.starmorph.com/blog/karpathy-llm-wiki-knowledge-base-guide
- Decision record templates (Nygard, MADR): https://adr.github.io/adr-templates/
- Diataxis, the four kinds of documentation: https://diataxis.fr/
- The AGENTS.md format: https://agents.md/

## licence

MIT. See `LICENSE`.
