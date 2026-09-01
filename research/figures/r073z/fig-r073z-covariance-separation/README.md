# Figure R0.73Z-1: covariance separation and pressure-active kernel tests

This package is source-bound to research commit
`7321e8a2c50817b58edd6e3bf1dd35bb3a24576b`.

It visualizes normalized analytic consequences from the frozen R0.73Z
research source.  The plotted rows are deterministic evaluations of explicit
formulas; they are not simulations, DNS, or numerical evidence for the
universal statements.

The package contains the producer, source data, vector SVG/PDF, 600 dpi PNG,
validation metadata, checksums, progress/resource logs, and visual-QA renders.

## Reproduction

Run from this directory with the repository checkout at the bound commit:

```text
python producer.py --render
python validate.py --write-baseline .determinism-baseline.json
python producer.py --render
python validate.py --determinism-baseline .determinism-baseline.json --consume-baseline --write-metadata --confirm-visual-qa
python validate.py --verify-only --confirm-visual-qa
```

The runtime must expose Python 3.12, NumPy, Pillow, ReportLab, pypdf, and
Poppler's `pdftoppm`.  No network, DGX, time stepping, random sampling, or
external data are used.

## Claim boundary

- Panel A shows the exact frequency factor `n` in the proved lower bound
  `c n`; it does not plot or estimate the geometry-dependent constant `c`.
- Panel B evaluates exact rational partial sums.
- Panel C evaluates closed formulas at the declared normalization.
- The finite rows do not prove the analytic quantifiers and do not establish
  interior suitable-weak finiteness, epsilon regularity, global regularity,
  or any Clay conclusion.

**NOT CLAY.**
