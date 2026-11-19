# experiments

Optional ML and research module. One page per experiment or approach family, written with `templates/experiment.md`: question, hypothesis, decision rule (before the run), setup, implementation, result, diagnosis, verdict, next. Delete this folder and its index section if the project has no experiments (`python tools/init_wiki.py --no-ml` does it).

- File names: `NN-short-title.md`, numbered in the order the experiments ran.
- Write the hypothesis and the decision rule before the run, and date them.
- Every score says its split (validation, test, public, private) and its source line.

## pages

| id | experiment | status | verdict |
|---|---|---|---|
