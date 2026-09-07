# Example quality record

## Automated checks

Run from the repository root:

```bash
python scripts/validate_repository.py
python examples/local-first/verify.py
```

The second command verifies four script paragraphs, unique shot IDs, valid paragraph/source/copy references, all three visual roles, and the explicitly unlocked audio timing state. Expected result: `PASS: local-first planning artifacts are consistent; audio and visual review remain pending`.

## Content review boundaries

The [source ledger](source-ledger.json) maps factual statements to primary sources and records unsupported claims. The script presents a hypothetical user test, not results from a real product or participant. It does not assert current popularity trends or universal safety.

Frame inspection, subtitle readability, sound quality and sample approval are **not performed** because no video/audio has been generated. Passing JSON checks cannot replace those gates.
