# <NN> - <experiment or approach in a few words>

<!-- Template: experiment. Folder: wiki/experiments/ (optional ML module). File name: NN-short-title.md.
One page per experiment or approach family. Write the hypothesis and the decision rule BEFORE the run.
Required sections: question, hypothesis, decision rule, setup, implementation, result, diagnosis, verdict, next.
Every number: [Certain] with the log line or file it comes from. Say which split every score is on. -->

- Status: <planned | running | done | abandoned>
- Dates: <YYYY-MM-DD to YYYY-MM-DD>
- Owner: <who ran it>

## question

<What this experiment should tell us, in one sentence.>

## hypothesis

<What we expect and why: the team's reason, and the literature behind it ([[<paper page>]]).>

## decision rule

<Written before the run: what result counts as better, a tie or worse, for example "better only if validation improves by more than 0.003 and the test score is also higher". Date it.>

## setup

| item | value |
|---|---|
| data and split | <which data, how train/validation/test are split, any gap or leakage control> |
| model | <architecture, size, the changes from the baseline> |
| training | <optimizer, schedule, epochs, batch, seeds> |
| metrics | <each metric and the split it is computed on> |
| compute | <hardware and time per run> |
| baseline | <what this is compared with, and its score on the same split> |

## implementation

- <file:line of each change, a link to the run or notebook. [Certain]>

## result

| run | <metric> (validation) | <metric> (test) | notes |
|---|---|---|---|
| <run id> | <value> | <value> | <seed, anything unusual> |

<Source of every number: log path and line. [Certain]>

## diagnosis

<Why the result came out this way. Quote the log lines; link theory checks ([[<theory page>]]). Separate what was checked [Certain] from what is inferred [Likely].>

## verdict

<Apply the decision rule from above, word for word: better, tie, worse or inconclusive. If the rule was changed, say so and why.>

## next

- <What this result changes; link the decision record it led to ([[<NNNN-decision>]]).>
