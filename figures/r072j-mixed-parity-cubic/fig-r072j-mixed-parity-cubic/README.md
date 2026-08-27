# R0.72J formal figure package

This package contains the journal-style four-panel figure for the
mixed-parity cubic audit.  It separates the exact residue-graph
classification from one finite triangle-rich carrier family and its measured
physical scaling.

## Masters

- `figure.pdf` - one-page vector master, 177.8 x 130.0 mm
- `figure.svg` - editable vector master
- `figure.png` - 600 dpi raster master

The public copies are byte-identical and are written by `publish_assets.py`
as `public/figures/r0-72j-mixed-parity-cubic.{pdf,svg,png}`.

## Evidence and lineage

- `data.csv` records every plotted certificate value, exact combinatorial
  value, guide, source file, and JSON pointer.
- `figure-data-metadata.json` records source hashes.
- `results.json` records the finite summary and claim boundary.
- `validation.json`, `qa-report.md`, and the three QA rasters record the
  package checks.
- `manifest.json` and `SHA256SUMS` provide integrity manifests.

The figure reads the sealed R0.72J producer, independent, and cross-check
JSON certificates.  It does not rerun the ODE.

## Reproduction

Run the commands in `command.txt` from the repository root.  Rebuild
`SHA256SUMS` only after all other package files are final.

The finite launch constructs one complex root.  It does not enumerate every
root, and the real Rolle complete-root corollary does not apply.
