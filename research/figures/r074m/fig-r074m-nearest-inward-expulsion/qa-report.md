# R0.74M formal figure QA report

Manual status: PASS

The 600-dpi color master, 200-dpi final-size raster, grayscale raster,
independent 300-dpi PDF raster, and macOS Quick Look raster of the
self-contained SVG were inspected on 2026-09-02.  This is internal package
QA, not an independent figure-package audit; any such audit is reported
separately.

Findings:

- no clipping, overpainting, overlap, missing glyph, or broken arrow;
- all labels remain readable at final size;
- the endpoint collar, path tube, defect window, and kernel-tail region
  remain distinguishable in grayscale by border, position, and line style;
- the exact final duration (R^2/64), modulus (LR/16), displacement
  (Sigma_L=2^{-15}e^{-L^2/640}), and bad-path exponent (1/16) are legible;
- panel A explicitly marks its curve as a schematic analytic event, not a
  simulated or sampled Brownian path;
- the good and bad estimates are spatially separated and lead to the same
  one-packet target; and
- the Quick Look SVG raster retains DejaVu Sans regular and bold text, with no
  serif substitution or missing glyph; and
- the footer states proved in source, analytic audit PASS, and not Clay.

Visual verdict: PASS.
