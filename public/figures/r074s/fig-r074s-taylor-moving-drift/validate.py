#!/usr/bin/env python3
"""Check the sealed Step 16 analytic figure package without regenerating it."""
from __future__ import annotations
import hashlib, json, re
from pathlib import Path
from PIL import Image
ROOT = Path(__file__).resolve().parent
def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()
required = ["figure.svg", "figure.pdf", "figure.png", "source-data.csv", "manifest.json", "validation.json", "results.json", "qa-report.md", "qa-grayscale.png", "qa-final-size.png", "qa-pdf-render.png", "config.json", "SHA256SUMS"]
missing = [name for name in required if not (ROOT / name).is_file()]
if missing:
    raise SystemExit(f"missing figure artifacts: {missing}")
validation = json.loads((ROOT / "validation.json").read_text(encoding="utf-8"))
if validation["summary"]["result"] != "PASS" or not all(validation["checks"].values()):
    raise SystemExit("embedded validation is not PASS")
with Image.open(ROOT / "figure.png") as image:
    if image.size != (4204, 2551) or image.info.get("dpi", (0, 0))[0] < 599:
        raise SystemExit(f"PNG geometry drift: {image.size}, {image.info.get('dpi')}")
svg = (ROOT / "figure.svg").read_text(encoding="utf-8")
for marker in ["S.342 = FALSE", "S.444 = OPEN", "NOT SIMULATION OR DNS", "Taylor 1923"]:
    if marker not in svg:
        raise SystemExit(f"SVG boundary marker missing: {marker}")
if re.search(r"analytic schematic", svg, flags=re.I) is None:
    raise SystemExit("SVG analytic-schematic disclaimer missing")
expected = {}
for line in (ROOT / "SHA256SUMS").read_text(encoding="utf-8").splitlines():
    digest, name = line.split("  ", 1)
    expected[name] = digest
for name, digest in expected.items():
    if sha256(ROOT / name) != digest:
        raise SystemExit(f"hash drift: {name}")
print(json.dumps({"figureId": "fig-r074s-taylor-moving-drift", "result": "PASS", "files": len(required)}))
