# R0.74P formal figure — independent promotion audit

## Verdict

**PASS.**  The final candidate package passed independent data, semantic,
geometry, typography, grayscale, SVG, reproducibility, and binding checks.
No blocker remains.

## Data and mathematical claim

- Panel A contains 147 rows: 49 points for each of three distinct decay-rate
  envelopes.
- Panel B contains five exact ledger rows.
- All identifiers are unique and every finite formula recomputes exactly.
- The certificate passes 52/52 checks.
- Panel A now states
  \(\log_{10}(\mathcal C_\sigma/T_*)\le
  \log_{10}C-\beta\log_{10}K_*\) and plots only the decay term
  \(-\beta\log_{10}K_*\).  The unknown additive \(\log_{10}C\) is
  explicitly suppressed; no absolute vertical upper-bound curve is claimed.
- For \(\sigma>1\), the branch is a right-endpoint supremum approached as
  \(x\uparrow1\), not an attained maximum for \(J\Subset I_R\).
- Panel B distinguishes `misses`, `detects`, and `overpays`, and states that
  only the target component is matched while the full
  (Y_2^{\rm sf}) upper bound remains open.

## Geometry and visual QA

- PDF: one page, 178 mm by 100 mm.
- SVG: intrinsic root size explicitly `178mm` by `100mm`.
- PNG: 4205 by 2363 pixels at 600 dpi; the one-pixel height difference is
  valid raster rounding.
- All SVG text is at least 5 pt at final size.
- DejaVu Sans regular and bold font files are embedded in the SVG.
- Color, grayscale, final-size PDF raster, and independent SVG Quick Look
  renders are readable and unclipped.
- Solid/dash/dot line styles, direct labels, exact rate symbols, and verdict
  text preserve meaning without color.

## Reproducibility and bindings

A fresh temporary-directory execution of `plot.py` and `validate.py` passed
20/20 checks and compared byte for byte with the candidate package.  The 24
internal manifest records and 13 external bindings match current bytes and
SHA-256 values; every `SHA256SUMS` entry passes.

Key bindings:

| Artifact | SHA-256 |
|---|---|
| `manifest.json` | `6067d0d10ac596a37cd9814fe3e05077b0802b0f350dd35024a7bd1d7ec9f0d8` |
| `SHA256SUMS` | `0aa1a023e7d090acd64b33c5cdf6f99a7f24f3e4f90c09713467621fc41f9271` |
| `source-data.csv` | `2cd230f4c140454ae95c9dcbf0ebec0985fa066ae94e7747d4d5dcdb4c72fd4b` |
| `figure.pdf` | `e2d0d830eb90f54abf1ea0fffb63d5733bd8f182d4271c0a7d61a1d3ce84aaa7` |
| `figure.svg` | `18a9b8825a1383c6e2546c7da6f3419a630900f290721d1d0707001d2e1ba290` |
| `figure.png` | `1c06af4315f7f0919af1653c482fd358181a9a3dcdf3953d6d38e77fe3a8bfb6` |
| external finite certificate | `c65b38def48b5439f112ab145360c1abb211de5bf6f004eca103271d8d9a204b` |
| external Chinese reader source | `d1602097fce2ae86089ff5dea678be6d5330366ca867886f51488aabf7c435d4` |

The package is an analytic exact-family figure, not simulation or DNS.  It
contains no regularity or Clay conclusion.  **NOT CLAY.**
