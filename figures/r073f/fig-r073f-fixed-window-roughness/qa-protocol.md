# Visual QA protocol

Inspect all three QA rasters after running `validate.py --qa-status pending`.

1. At final print size (`qa-final-size.png`), verify that all panel titles,
   tick labels, legends, mathematical symbols, and the (d_{diag}) warning are
   legible and do not collide.
2. In `qa-grayscale.png`, verify that marker shapes and line styles distinguish
   every series without colour.
3. In `qa-pdf.png`, verify that the PDF raster agrees with the PNG master and
   that no text, line, or marker is clipped.
4. Cross-check panel A against `moving_gain_rows.csv`, panel B against
   `convergence_rows.csv` and `independent_validation.json`, and panels C--D
   against the two counterexample CSV files.
5. Verify that logarithmic axes, normalized-rate units, the (10^{-17})
   display floor, and the claim boundary are explicit.

Only after this inspection rerun `validate.py --qa-status passed` with a short
inspection note.  A passed visual QA does not upgrade finite data to a
continuum theorem.
