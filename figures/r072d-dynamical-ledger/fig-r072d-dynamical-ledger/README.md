# R0.72D dynamical-ledger figure

This package contains the formal double-column journal figure for R0.72D.
Panel A is a deterministic FFT phase-grid diagnostic of the heat-weighted
shifted Rudin--Shapiro multiplier. Panel B copies the independent finite-ODE
root, atom, and charge rows and adds a deterministic mixed-exposure grid
proxy. The figure is corroborating evidence, not an interval proof or PDE
simulation.

Reproduce from the repository root with the scientific Python environment:

```sh
/Users/kasifa/Documents/Math/.codex-research-venv/bin/python figures/r072d-dynamical-ledger/fig-r072d-dynamical-ledger/build_figure.py --config figures/r072d-dynamical-ledger/fig-r072d-dynamical-ledger/config.json
/Users/kasifa/Documents/Math/.codex-research-venv/bin/python figures/r072d-dynamical-ledger/fig-r072d-dynamical-ledger/qa_images.py
/Users/kasifa/Documents/Math/.codex-research-venv/bin/python figures/r072d-dynamical-ledger/fig-r072d-dynamical-ledger/publish_assets.py
/Users/kasifa/Documents/Math/.codex-research-venv/bin/python figures/r072d-dynamical-ledger/fig-r072d-dynamical-ledger/validate.py
/Users/kasifa/Documents/Math/.codex-research-venv/bin/python figures/r072d-dynamical-ledger/fig-r072d-dynamical-ledger/build_manifest.py
/Users/kasifa/Documents/Math/.codex-research-venv/bin/python figures/r072d-dynamical-ledger/fig-r072d-dynamical-ledger/build_hashes.py
```

Archival outputs are vector PDF/SVG and a 600 dpi PNG at 178 mm width.
Final-size color, grayscale, and PDF-raster QA surfaces are included. Every
plotted row is archived in `data.csv`, while `figure-data-metadata.json`,
`manifest.json`, `validation.json`, and `SHA256SUMS` preserve lineage and QA.
