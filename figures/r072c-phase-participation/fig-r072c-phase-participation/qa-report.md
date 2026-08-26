# R0.72C-1 visual QA

Reviewed: 2026-08-27, Asia/Shanghai

- final-size color inspection: PASS
- grayscale distinction inspection: PASS
- PDF render inspection: PASS
- title, subtitle, panel labels, legends, axes, annotations, and footer clipping: PASS
- exact-family and boundary interpretation review: PASS

The final render preserves the contract's two-root palette: muted blue and
ochre carry the two exact-launch families, while neutral gray is reserved for
the positive-time tail and the analytic slope references. Filled circles,
open squares, open triangles, and solid, dashed, and dotted lines remain
distinct after grayscale conversion. The two exponent labels sit next to the
correct asymptotic guides without masking exact data marks.

The strict-region curves retain their beta-zero labels and saturation caps.
The footer states the algebraic sharpness and tail-only burn-in limits without
colliding with the figure identifier. The 600 dpi PNG, vector PDF, vector SVG,
final-size color surface, grayscale surface, and Poppler PDF raster were
checked after the final build. No overlap, detached annotation, clipping, or
PDF raster discrepancy was observed.
