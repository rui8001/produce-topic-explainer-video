"""Check public planning artifacts; this does not render or approve a video."""
import json
from pathlib import Path
import re
from urllib.parse import urlparse


def require(condition, message):
    if not condition:
        raise ValueError(message)


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())

root = Path(__file__).resolve().parent
paragraphs = [p for p in (root / "script.txt").read_text().strip().split("\n\n") if p]
sources = json.loads((root / "source-ledger.json").read_text())["sources"]
copy = json.loads((root / "on-screen-copy.json").read_text())
plan = json.loads((root / "visual-plan.json").read_text())
require(len(paragraphs) == 4, "Expected four spoken paragraphs")
require(plan["timing_state"] == "awaiting_accepted_audio", "Shot timing must await accepted audio")
status = (root / "production-status.md").read_text()
require(re.findall(r"^- Stage: (.+)$", status, re.M) == ["pre_audio_planning"],
        "Production stage must be pre_audio_planning")
shots = plan["shots"]
require(all(nonempty(shot["id"]) for shot in shots), "Shot IDs must be nonempty strings")
require(len({shot["id"] for shot in shots}) == len(shots), "Shot IDs must be unique")
require(all(type(shot["paragraph"]) is int for shot in shots), "Paragraph IDs must be integers")
require({shot["paragraph"] for shot in shots} == set(range(1, len(paragraphs)+1)),
        "Shots must cover every spoken paragraph without unknown paragraph IDs")
require({shot["role"] for shot in shots} == {"persona", "evidence", "model"},
        "Expected persona, evidence and model roles")
for source in sources:
    require(all(nonempty(source.get(field)) for field in ("id", "url", "title", "supports")),
            "Each source needs an ID, URL, title and supported claim")
    url = urlparse(source["url"])
    require(url.scheme in ("http", "https") and bool(url.netloc), "Source URL must be HTTP(S)")
source_ids = {source["id"] for source in sources}
require(len(source_ids) == len(sources), "Source IDs must be unique")
for shot in shots:
    require(isinstance(shot["source_ids"], list), "Source references must be a list")
    require(set(shot["source_ids"]) <= source_ids, "Unknown source reference")
    require(shot["role"] != "evidence" or bool(shot["source_ids"]),
            "Evidence shots must cite a source")
    require(isinstance(shot["copy_ids"], list), "Copy references must be a list")
    require(set(shot["copy_ids"]) <= set(copy), "Unknown on-screen-copy reference")
    require("start" not in shot and "end" not in shot, "Pre-audio shots cannot have locked times")
print("PASS: local-first planning artifacts are consistent; audio and visual review remain pending")
