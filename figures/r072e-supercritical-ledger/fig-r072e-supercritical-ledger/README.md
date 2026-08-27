# R0.72E supercritical-ledger figure

This package contains the formal double-column journal figure for R0.72E.
It copies every plotted numerical value from the producer and independent
certificate JSON files, adds only declared analytic reference rows, and
preserves exact source pointers in `data.csv`.

The three panels show the selected Bessel mass coefficient, the normalized
negative-Sobolev action, and the selected-ledger lower-bound growth after the
(D^{1/3}) payment. These are finite diagnostics of the analytic report, not
an interval proof or a Navier-Stokes regularity result.

Reproduce from the repository root with the scientific Python environment:

```sh
/Users/kasifa/Documents/Math/.codex-research-venv/bin/python figures/r072e-supercritical-ledger/fig-r072e-supercritical-ledger/build_figure.py --config figures/r072e-supercritical-ledger/fig-r072e-supercritical-ledger/config.json
/Users/kasifa/Documents/Math/.codex-research-venv/bin/python figures/r072e-supercritical-ledger/fig-r072e-supercritical-ledger/qa_images.py
/Users/kasifa/Documents/Math/.codex-research-venv/bin/python figures/r072e-supercritical-ledger/fig-r072e-supercritical-ledger/publish_assets.py
/Users/kasifa/Documents/Math/.codex-research-venv/bin/python figures/r072e-supercritical-ledger/fig-r072e-supercritical-ledger/validate.py
/Users/kasifa/Documents/Math/.codex-research-venv/bin/python figures/r072e-supercritical-ledger/fig-r072e-supercritical-ledger/build_manifest.py
/Users/kasifa/Documents/Math/.codex-research-venv/bin/python figures/r072e-supercritical-ledger/fig-r072e-supercritical-ledger/build_hashes.py
```

Archival outputs are vector PDF/SVG and a 600 dpi PNG at 178 mm width.
Final-size color, grayscale, and PDF-raster QA surfaces are included. The
manifest, validation record, progress/resource logs, environment, source
hashes, and `SHA256SUMS` make the package auditable.
