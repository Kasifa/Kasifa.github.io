# R0.74U figure QA protocol

## Mathematical and data checks

1. Verify the frozen theorem-note commit/blob/SHA-256 chain and required
   (U.11)--(U.45) locators.
2. Recompute the exact annular-margin test
   `15232043/1849688064 > 0`, the inner margin `9235/21504 > 0`, and
   `3/8 < A(9216) < 1`.
3. Verify `a_D 9216^2 = 462422016/1625 > 4`, hence the stated crude
   `epsilon_i < 1/4` gate, and audit the speed and room exponent ledgers.
4. Verify the corridor bounds `72/5` and strict `1024/3`, while assigning no
   upper coefficient to the completed-clock superlevel set.
5. Recompute `5c_gamma-a_S=603445/89413632>0` and regenerate all 121 values
   of each Panel D series from the displayed formulas.
6. Require the certified lower logarithm to exceed the illustrative necessary
   upper logarithm throughout the path and verify their exact log-gap identity.

## Rendering checks

1. Confirm the 178 mm by 116 mm canvas, 4204 by 2740 600-dpi PNG, vector SVG,
   and one-page PDF with embedded fonts.
2. Inspect `qa-final-size.png` at 300 dpi for legibility, clipping, collision,
   detached annotations, and truthful set nesting.
3. Inspect `qa-grayscale.png`; no comparison may depend on hue alone.
4. Inspect `qa-pdf.png`, an independent PDF rasterization, and compare it
   against the final-size PNG.
5. Confirm the top-right blossom and every scope label in SVG and extracted
   PDF text.

## Required scope labels

`ANALYTIC SCHEMATIC`, `DERIVED ANALYTIC VALUES`, `NOT PDE DATA`, `NOT DNS`,
and `NOT CLAY` must be embedded in the rendered outputs. Panel A must also
say `SCHEMATIC / NOT TO SCALE`; Panel C must say `NO CONVERSE / NO UPPER
BOUND FOR FULL K-SUPERLEVEL`.

## Preseal and final-seal policy

Preseal QA validates exactly 10 source + 11 raw/result files and writes no
archive metadata. The first commit must contain exactly those 21 files.
Final sealing is forbidden until the actual 21-file figure-source commit is
supplied and verified. The seal then adds only `SHA256SUMS`, `manifest.json`,
`qa-report.md`, and `validation.json`; deterministic-core hashes must survive
a complete second render unchanged.
