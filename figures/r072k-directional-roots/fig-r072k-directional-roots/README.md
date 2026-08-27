# R0.72K formal figure package

This package visualizes the analytic directional root-sampling theorem and
the inherited common-band finite ledgers.  It performs no new PDE time
evolution: the producer and independent points trace to separately archived
R0.72J evolutions through the R0.72K certificates.

## Masters and publication

- `figure.pdf` -- one-page vector master, 177.8 x 124.0 mm
- `figure.svg` -- editable vector master
- `figure.png` -- 600 dpi raster master

`publish_assets.py` writes byte-identical copies to
`public/figures/r0-72k-directional-roots.{pdf,svg,png}` and verifies every
copy by SHA-256.

## Evidence and QA

- `data.csv` records every plotted value with route, source, and pointer.
- `results.json` records source/output hashes, finite summaries, and the
  no-new-PDE declaration.
- `validation.json` and `qa-report.md` cover certificate status, exact
  sharpness arithmetic, producer-independent agreement, geometry, lineage,
  claim boundaries, and byte-identical publication.
- `qa-final-size.png`, `qa-grayscale.png`, and `qa-pdf.png` are the 180 dpi
  final-size, grayscale, and PDF-raster inspection surfaces.
- `manifest.json` and `SHA256SUMS` provide the formal archive ledger.

Structural QA does not assert that a human inspected the figure.  A formal
manifest therefore requires the explicit
`R072K_VISUAL_QA_INSPECTED=true` declaration after all three QA surfaces have
actually been reviewed.

The plotting environment supplies NumPy, Matplotlib, and Pillow.  The
recorded validation command uses the bundled PDF runtime that supplies
Pillow and pypdf, so the command remains executable without silently relying
on an unrecorded package in the plotting environment.

## Reproduction and provenance

Run `command.txt` from the repository root.  Before building a formal
manifest, set full 40-character `R072K_SOURCE_COMMIT` and
`R072K_CERTIFICATE_COMMIT` values.  The manifest builder rejects shortened or
unresolvable SHAs.  `R072K_DIRTY_AT_CERTIFIED_RUN` may be supplied explicitly
when supported by the certified-run record; if it is omitted, the builder
records the current worktree state from `git status`.  A formal manifest is
refused when that value is true.

The analytic proof is in `research/r072k_report-source.md`.  The finite
points are lineage and implementation checks; they do not enumerate all
complex roots or prove a general Navier--Stokes regularity theorem.
