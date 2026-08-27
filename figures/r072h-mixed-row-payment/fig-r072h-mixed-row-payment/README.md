# R0.72H formal figure package

This package contains the journal-style figure for the carrier-free
critical-log mixed-row theorem and its all-odd Rudin--Shapiro sharpness
family.

## Masters

- figure.pdf -- one-page vector master, 177.8 x 96.0 mm
- figure.svg -- editable vector master
- figure.png -- 600 dpi raster master

Byte-identical public copies are published under:

- public/figures/r0-72h-mixed-row-payment.pdf
- public/figures/r0-72h-mixed-row-payment.svg
- public/figures/r0-72h-mixed-row-payment.png

## Evidence and lineage

- data.csv records every plotted value and its source pointer.
- figure-data-metadata.json records source certificate hashes.
- results.json records the finite summary and claim boundary.
- validation.json contains 22 required package checks.
- manifest.json and SHA256SUMS provide integrity manifests.

## QA

- qa-final-size.png
- qa-grayscale.png
- qa-pdf.png
- qa-report.md

All three QA surfaces use the final physical aspect ratio at 180 dpi. The
grayscale surface checks that the three analytic/numerical series remain
distinguishable without color.

## Reproduction

Run command.txt from the repository root with the declared research Python
environment. The analytic proof is in research/r072h_report-source.md; this
figure is not a substitute for that proof.
