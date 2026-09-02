# R0.74O formal figure QA report

Manual status: PASS

The 600-dpi color master, 200-dpi final-size raster, grayscale raster,
independent 300-dpi PDF raster, and macOS Quick Look raster of the
self-contained SVG were inspected on 2026-09-02.  This is internal package
QA, not the independent figure-package audit.

Findings:

- no clipping, overlap, missing glyph, detached label, or broken outline;
- panels A--D and their direct labels remain legible at final size;
- the free `varkappa` multiplier, four payment rows, quadratic observable
  scaling, and exact scalar-frontier conversion remain distinguishable in
  grayscale through position, shape, and solid/dashed outlines;
- the formula `1171/943200`, the exact G ratio, `L^(-3/2)`, `8024/11907`,
  and `86/11907` remain readable on every final-context raster;
- `SCALAR-PAYMENT-ONLY NO-GO` and
  `smooth exact family • scalar-payment-only no-go • NOT CLAY` remain
  prominent without implying a general regularity result;
- the Quick Look raster retains DejaVu Sans regular and bold, without serif
  substitution or missing glyph; and
- the footer states analytic schematic, not to scale, and no
  DNS/simulation/fitted data.

Visual verdict: PASS.
