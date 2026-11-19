# index

Catalog of every wiki page, one line each: `[[page]] - what it holds`. Read [[context]] first, then only the pages the task needs. `tools/new_page.py` adds lines here; `tools/wikilint.py` fails if a page is missing.

## core

- [[context]] - stable facts: goal, owner, where things live, constraints
- [[sources]] - every source in `raw/`, its origin and trust level
- [[errors]] - corrections register: wrong statements, bugs, tool notes
- [[glossary]] - project terms and abbreviations
- [[log]] - append-only record of every wiki operation

## decisions

- [[decisions/README|decisions]] - how decision records work, and their list
- [[0001-record-decisions]] - keep a decision record for every significant choice

## concepts

- [[concepts/README|concepts]] - what a concept page is for
- [[evidence-tags]] - what [Certain], [Likely], [Guessing] and [User-reported] mean, and when to use each

## howto

- [[howto/README|howto]] - what a how-to page is for
- [[lint-the-wiki]] - run the lint check and fix what it reports

## experiments

- [[experiments/README|experiments]] - optional ML module: one page per experiment or approach

## literature

- [[literature/README|literature]] - optional ML module: one page per paper

## theory

- [[theory/README|theory]] - optional ML module: derivations with scripted checks
