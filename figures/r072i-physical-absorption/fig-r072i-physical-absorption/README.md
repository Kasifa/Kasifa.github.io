# R0.72I formal figure package

This package contains the journal-style four-panel figure for the physical
absorption audit of the R0.72H complete-root corollary.  It distinguishes a
growing generic `B_A` upper bound from the much smaller parity-resolved cubic
exposure measured in the all-odd Rudin--Shapiro family.

## Masters

- `figure.pdf` -- one-page vector master, 177.8 x 130.0 mm
- `figure.svg` -- editable vector master
- `figure.png` -- 600 dpi raster master

The included `publish_assets.py` can later create byte-identical public
copies named `r0-72i-physical-absorption.{pdf,svg,png}`.  Package construction
does not write outside this directory.

## Evidence and lineage

- `data.csv` records every plotted value, route, source file, and pointer.
- `figure-data-metadata.json` records hashes of all source certificates.
- `results.json` records the numerical summary and claim boundary.
- `validation.json` contains the required package checks.
- `manifest.json` and `SHA256SUMS` provide integrity manifests.

The producer data are mandatory.  If `independent-data.csv` is present when
the figure is rebuilt, its matching fields are overlaid automatically.

## Reproduction

Run the commands in `command.txt` from the repository root.  The continuum
argument belongs in `research/r072i_report-source.md`; this figure and its
finite fits do not replace that proof.
