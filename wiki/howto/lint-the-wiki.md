# lint the wiki

Goal: check that the wiki is consistent before a commit or at the end of a session.

## before you start

- Python 3.9 or newer; no packages needed.
- Run from the root of the wiki (the folder with `AGENTS.md`).

## steps

1. Run the check:
   ```
   python tools/wikilint.py
   ```
2. Fix every line marked `ERROR`. The most common ones:
   - `broken link [[x]]` - create the page with `tools/new_page.py` or correct the name
   - `not in index` - add a line for the page to `wiki/index.md`
   - `log heading` - write the entry as `## YYYY-MM-DD - type - summary`
   - `possible secret` or `data file` - remove the file or the token; never commit it
3. Read the `WARN` lines and decide; for example, a fact page with no evidence tag.
4. Run the check again until it prints `0 errors`.
5. Log the pass in `wiki/log.md` as `## YYYY-MM-DD - lint - <what you fixed>`.

## check

The command exits with code 0 and prints `0 errors`. The GitHub Action runs the same check on every push.

## related

- [[evidence-tags]] - what the evidence warning asks for
- `AGENTS.md` - the rules each check enforces
