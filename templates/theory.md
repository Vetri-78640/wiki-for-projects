# t<N> - <claim in a few words>

<!-- Template: theory. Folder: wiki/theory/ (optional ML module). File name: tN-short-title.md.
A derivation or analysis with a scripted check, so the claim can be re-verified.
Scripts go in wiki/theory/scripts/; scripts that need data take its path as an argument and never store the data.
Required sections: claim, derivation, scripted check, result, what it explains. -->

## claim

<One sentence that this page proves or measures.>

## derivation

<The argument, step by step. Give every symbol a one-line meaning. Say which assumptions it needs.>

## scripted check

- Script: `wiki/theory/scripts/<name>.py`
- Run: `python wiki/theory/scripts/<name>.py <data path>`
- Output saved to: `wiki/theory/scripts/out/<name>.txt`

## result

<What the script printed, the key lines quoted. [Certain]>

## what it explains

- <Which result, decision or source statement this confirms or corrects. Link [[<page>]]; if a source was wrong, add a row to [[errors]].>
