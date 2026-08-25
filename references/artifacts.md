# Artifact contract

```text
work/<date>-<slug>/
  00-brief.json
  01-script.txt
  02-audio/
    narration.wav
    alignment.json
    captions.srt
  03-sources/
    fact-sheet.md
    source-ledger.md
  04-plan/
    visual-plan.json
    on-screen-copy.json
  05-assets/
  06-composition/
  07-review/
  08-production-status.md
  09-final-qc.md
  final/
```

The status file is the durable source of current truth. It records the current stage, locked files, authorization scope, checks, missing assets, rejected attempts, next action, and rollback path.

`on-screen-copy.json` is a whitelist of approved generated labels. Authentic source media may retain its own text after privacy and rights review; production notes and internal labels never belong on screen.
