# templates

One template per page type. `tools/new_page.py` copies the right one; you can also copy by hand. Each template lists its required sections in a comment at the top and points to a filled example.

| template | creates | goes in |
|---|---|---|
| `concept.md` | a page explaining one idea | `wiki/concepts/` |
| `decision.md` | a decision record | `wiki/decisions/` |
| `howto.md` | step-by-step instructions for one task | `wiki/howto/` |
| `source-entry.md` | a row for a new source | `wiki/sources.md` |
| `error-entry.md` | a row for a correction, bug or tool note | `wiki/errors.md` |

Placeholders are written as `<...>` and `NNNN`. `tools/wikilint.py` warns about placeholders left in a page.
