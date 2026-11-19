# 0001 - keep a decision record for every significant choice

- Status: accepted
- Date: 2026-11-19
- Deciders: <project owner>

## context

Projects change direction many times, and the reason for each change is the first thing lost. Months later nobody, person or agent, can tell whether a choice was deliberate, forced by a constraint, or an accident, so old mistakes get repeated and good choices get undone. [Certain]

## options

| option | for | against |
|---|---|---|
| no records, rely on commit messages and chat | no extra work | reasons scatter across tools and are hard to find |
| one long design document | everything in one place | gets rewritten, so the history of why is lost |
| one short record per decision | small, dated, searchable, keeps history | needs a habit of writing them |

## decision

Keep one short record per significant decision in `wiki/decisions/`, using `templates/decision.md`. Records are written before acting and are never rewritten once accepted; a later record supersedes an earlier one.

## consequences

- Every "why did we do this?" has a page to point to.
- Writing the options down before choosing makes weak options visible early.
- Records cost a few minutes each, so only significant choices get one.

## evidence

- Michael Nygard, "Documenting Architecture Decisions" (2011), and the MADR format: https://adr.github.io/adr-templates/
