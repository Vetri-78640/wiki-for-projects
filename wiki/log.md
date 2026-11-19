# log

Append-only record of every wiki operation, newest last. One entry per operation:

```
## YYYY-MM-DD - type - summary

- what changed, with the pages and files involved
```

Types: `ingest`, `query`, `write`, `fix`, `decide`, `lint`, `handoff`. Find entries with `grep "^## " wiki/log.md`. Never edit or remove an old entry; add a new one that corrects it.

## 2026-11-19 - write - wiki created from the wiki-for-projects template

- Core pages, section folders and templates in place. Replace the placeholders in [[context]] and `handoff.md`.
