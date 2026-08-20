# Figure contract — R0.61 complete quartic target scan

- **Analytical question:** After the exact normalization
  \(A^4G_4/(A^2G_2)=-(\varepsilon^2/L^2)R_{L,M,m}\), does the complete
  quartic target coefficient show growth with the number of coherent outputs
  \(M\) on the archived deterministic scan?
- **Supported claim:** Every one of the 461 distinct archived ratios is
  positive, so every observed quartic target opposes the quadratic target.
  The largest observed ratio is \(1.3286562612067\times10^{-3}\), and the
  edge-target families show no numerical growth with \(M\) up to the scanned
  endpoint \(M=8192\).  These are finite observations, not all-index bounds.
- **Family and variant:** two-panel highlighted multi-series line figure.
  Panel (a) shows four complete target profiles on a logarithmic response
  scale.  Panel (b) shows edge-target scaling over dyadic \(M\) for selected
  fixed \(L\), with the observed maximum highlighted.
- **Data sufficiency:** 416 target-level rows in four complete families and 49
  distinct edge parameter pairs.  The full certificate contains 464
  evaluations, 461 distinct triples, and 7,494,536,238 ordered paths.
- **Renderer and footprint:** reproducible Matplotlib; one double-column
  journal figure at 178 by 105 millimetres; PDF, SVG, and 600 dpi PNG.
- **Palette policy:** restrained blue, gold, rust, and olive roots plus neutral
  ink.  Distinct dash patterns, markers, and direct endpoint labels preserve
  series identity without color.
- **Required QA:** independently validate presentation tables against the
  pinned exploration certificate; inspect color, true grayscale, and
  Poppler-rendered PDF at final size; verify log-scale labeling, the observed
  maximum annotation, embedded fonts, and the explicit finite-evidence scope.

