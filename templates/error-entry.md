# error entry

<!-- Template: one row in wiki/errors.md. Never delete rows; mark them resolved. -->

Pick the table and the next free id, then add the row at the end of that table in `wiki/errors.md`.

Wrong statement (E):

```
| E<NN> | `<file or page>` | "<the wrong statement, quoted>" | <the correct statement> (<evidence>) | open |
```

Bug (B):

```
| B<NN> | `<path>:<line>` | <what goes wrong and its effect> | <fix or workaround> (<evidence>) | open |
```

Tool note (T):

```
| T<NN> | <tool and version> | <problem> | <workaround> | open |
```

When it is fixed, change `open` to `resolved YYYY-MM-DD: <how>`. Then fix every page that repeated the wrong statement and log it:

```
## YYYY-MM-DD - fix - <short summary>

- E<NN>: corrected [[<pages>]]
```

Example:

```
| E02 | `raw/repo/README.md` | "best score 0.88" | 0.88 is the public score; the final private score is 0.86 (`raw/api/leaderboard.json`) | open |
```
