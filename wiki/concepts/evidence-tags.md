# evidence tags

Every claim in the wiki says how well it is supported, so a reader can tell a checked fact from a guess without re-checking it. Put the tag at the end of the sentence or bullet it covers. [Certain]

## the tags

| tag | use it when | example |
|---|---|---|
| [Certain] | you checked it yourself against a primary source: a log, a file, a command output, an API pull, code as run | "The run finished in 51 minutes (`raw/runs/run-07.log`, last line)." |
| [Likely] | strong inference from evidence, not checked directly | "The slowdown is likely the data loader: GPU use stays below 30%." |
| [Guessing] | a hypothesis with little support, written down so it can be tested | "The extra layer may overfit on the small months." |
| [User-reported] | the project owner or a teammate said it; not verified independently | "The admin allowed using the dataset in the paper." |

## rules

- A number always carries [Certain] with its source, or it is written as "unknown".
- When a [Likely] or [Guessing] claim is checked, change the tag and add the evidence; if it was wrong, add a row to [[errors]].
- One tag can cover a short list: put it after the list, as `[Certain for every row]`.
- Do not tag definitions, instructions or headings.

## related

- [[0001-record-decisions]] - decisions keep the evidence known at the time
- [[errors]] - where wrong claims are recorded
