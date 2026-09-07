"""Check public planning artifacts; this does not render or approve a video."""
import json
from pathlib import Path

root = Path(__file__).resolve().parent
paragraphs = [p for p in (root / "script.txt").read_text().strip().split("\n\n") if p]
sources = json.loads((root / "source-ledger.json").read_text())["sources"]
copy = json.loads((root / "on-screen-copy.json").read_text())
plan = json.loads((root / "visual-plan.json").read_text())
assert len(paragraphs) == 4
assert plan["timing_state"] == "awaiting_accepted_audio"
shots = plan["shots"]
assert len({shot["id"] for shot in shots}) == len(shots)
assert {shot["paragraph"] for shot in shots} == set(range(1, len(paragraphs)+1))
assert {shot["role"] for shot in shots} == {"persona", "evidence", "model"}
source_ids = {source["id"] for source in sources}
for shot in shots:
    assert set(shot["source_ids"]) <= source_ids
    assert set(shot["copy_ids"]) <= set(copy)
    assert "start" not in shot and "end" not in shot
print("PASS: local-first planning artifacts are consistent; audio and visual review remain pending")
