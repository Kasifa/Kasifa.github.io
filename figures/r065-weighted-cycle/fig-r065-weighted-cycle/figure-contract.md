# Figure contract — R0.65 heat-weighted periodic target

- **Question:** What happens to the complete heat-integrated quartic scalar
  along the explicit `0100` target cycle through the certified range
  `1 <= r <= 24`?
- **Certified result:** the sign changes at `r=14`; the ten block transitions
  `r=15,...,24` all have absolute growth strictly above `16`; the final
  certified block ratio lies in `(25.29,25.30)`.
- **Boundary:** these are rational enclosures at finitely many named scales.
  The figure does not prove asymptotic growth or failure of a uniform
  quartic bound.
- **Family and variants:** two coordinated ordered-axis diagnostics: signed
  normalized coefficient on a symmetric-log scale, and absolute four-level
  block ratio on a logarithmic scale with exact thresholds.
- **Data sufficiency:** 24 consecutive cycle counts, 23 block ratios, exact
  integer moments through total degree 96, order-48 rational Taylor
  enclosures, and four independent direct-path cross-checks.
- **Palette:** hard two-root cap — blue/open circles for positive values,
  rust/filled squares for negative values, neutral dashed threshold lines.
- **Non-color encoding:** marker shape/fill, zero and threshold rules, direct
  annotations, and a shaded certified run.
- **Output:** double-column `178 mm x 96 mm`, PDF/SVG/600-dpi PNG; inspect
  color, true grayscale, and Poppler-rendered PDF at final size.
