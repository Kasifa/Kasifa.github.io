# R0.72F critical-log-window figure

This package contains the formal double-column journal figure for R0.72F.
Every finite numerical value is derived from the producer and independent
certificate JSON files. Analytic boundary rows and exact rational frontier
vertices are labelled separately in `data.csv`.

Panel A shows only the intersection of two necessary screens for the checked
selected family: the selected-ledger scaling threshold and the Leray
energy-payment threshold. Panel B compares the critical-log normalization
from the time-dependent split-step producer and the independent real-lattice
BDF audit. Panel C distinguishes the three exact repair vertices; the
root-atom vertex is visibly marked as changing the left-hand-side observable.

Reproduce from the repository root with the scientific Python environment:

```sh
/Users/kasifa/Documents/Math/.codex-research-venv/bin/python figures/r072f-critical-log-window/fig-r072f-critical-log-window/build_figure.py --config figures/r072f-critical-log-window/fig-r072f-critical-log-window/config.json
/Users/kasifa/Documents/Math/.codex-research-venv/bin/python figures/r072f-critical-log-window/fig-r072f-critical-log-window/qa_images.py
/Users/kasifa/Documents/Math/.codex-research-venv/bin/python figures/r072f-critical-log-window/fig-r072f-critical-log-window/publish_assets.py
/Users/kasifa/Documents/Math/.codex-research-venv/bin/python figures/r072f-critical-log-window/fig-r072f-critical-log-window/validate.py
/Users/kasifa/Documents/Math/.codex-research-venv/bin/python figures/r072f-critical-log-window/fig-r072f-critical-log-window/build_manifest.py
/Users/kasifa/Documents/Math/.codex-research-venv/bin/python figures/r072f-critical-log-window/fig-r072f-critical-log-window/build_hashes.py
```

The archival outputs are vector PDF/SVG and a 600 dpi PNG at 178 mm width.
Final-size color, grayscale, and PDF-raster QA surfaces are included. These
finite diagnostics are not a complete-root theorem or a regularity result.
