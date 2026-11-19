# source entry

<!-- Template: one row in wiki/sources.md, added when a source is ingested into raw/. -->

Copy the row, fill it and add it at the end of the table in `wiki/sources.md`:

```
| S<NN> | `raw/<area>/<file>` | <what it is, one line> | <who made it, how it was obtained, YYYY-MM-DD> | <high | medium | low> | <licence, known errors, what not to trust> |
```

Trust levels:

- **high** - a primary record: logs, API pulls, exports, code exactly as run
- **medium** - written by the team after the fact: reports, READMEs, slides
- **low** - unverified, second-hand, or known to contain errors (link the rows in `wiki/errors.md`)

Example:

```
| S02 | `raw/runs/run-07.log` | training log of run 7 | downloaded from the cluster, 2026-03-02 | high | the last 20 lines are cut off |
```

Then log the ingest in `wiki/log.md`:

```
## YYYY-MM-DD - ingest - <source>

- added S<NN>; updated [[<pages it changed>]]
```
