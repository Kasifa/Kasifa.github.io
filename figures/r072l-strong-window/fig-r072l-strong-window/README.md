# R0.72L formal figure package

This package visualizes the analytic moderate strong-coupling window and its
first unresolved boundary.  Panels A and B are generated directly from the
scaling formulae in `research/r072l_report-source.md`.  Panel C integrates the
exact projected three-mode ODE only as a finite diagnostic.  Panel D records
the exact full-lattice leakage identity that prevents that projected orbit
from being an invariant subsystem.

## Masters and publication

- `figure.pdf` -- one-page vector master, 177.8 x 124.0 mm
- `figure.svg` -- editable vector master
- `figure.png` -- 600 dpi raster master

`publish_assets.py` writes byte-identical copies to
`public/assets/r072l/fig-r072l-strong-window.{pdf,svg,png}` and verifies each
copy by SHA-256.

## Evidence and QA

- `data.csv` records every plotted datum, source equation, and claim boundary.
- `results.json` records source and output hashes and the projected-ODE tail
  slopes.
- `validation.json` and `qa-report.md` check formulas, dimensions, public-copy
  identity, finite ODE behaviour, leakage arithmetic, and claim boundaries.
- `qa-final-size.png`, `qa-grayscale.png`, and `qa-pdf.png` are the final-size,
  grayscale, and PDF-raster inspection surfaces at 180 dpi.
- `manifest.json` and `SHA256SUMS` provide the archive ledger.

The finite Galerkin points are not a proof of the analytic theorem, a DNS, an
invariant full-lattice orbit, or a Navier--Stokes regularity result.  A formal
manifest requires an explicit visual-inspection declaration and a clean
certified-run declaration after the package source has been committed.
