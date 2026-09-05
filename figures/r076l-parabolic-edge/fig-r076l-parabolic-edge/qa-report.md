# Figure R0.76L-1 QA report

**Verdict: PASS.**

The archived PNG and the PDF rendered back to pixels were inspected at the
final double-column footprint.  The review found no clipping, collision, or
detached label.  Panel tags, axis labels, tick labels, data marks, the analytic
reference lines, and the common legend remain distinct at final size.

## Manual visual checks

| Check | Verdict | Observation |
|---|---|---|
| Final-size inspection | PASS | The 178 mm by 72 mm composition remains legible, with adequate panel and margin separation. |
| Grayscale inspection | PASS | The four degree laws remain distinguishable by tone, dash pattern, and marker shape; the analytic limit has a separate dashed reference style. |
| Labels and legends | PASS | No label, legend, panel tag, tick, curve, or marker collision is visible in either the PNG or the PDF rendering. |
| Scales and units | PASS | All quantities are dimensionless; each panel's enlarged vertical range is explicit in the caption, and every analytic limit lies within its displayed range. |
| Data cross-check | PASS | The 16 plotted rows agree with the regenerated CSV and SVG, including the three analytic constants and the unit-coordinate finite difference in panel (c). |
| PDF inspection | PASS | The PDF is a single vector page with embedded Georgia fonts and renders consistently with the PNG. |

## Numerical gates

The deterministic recomputation passed all implemented acceptance gates:

- maximum saddle-equation residual: `2.842170943040e-14`;
- maximum coarse-versus-fine grid delta: `1.881494959832e-12`;
- maximum phase-drop sensitivity delta: `1.165734175856e-15`;
- regenerated `data.csv` and `figure.svg`: byte-identical to the archived files.

## Output checks

- PNG: `4205 x 1701` pixels at `600 x 600 dpi`;
- PDF: one page, `504.96 x 204` points, within the renderer gate for the
  `178 mm x 72 mm` target;
- two consecutive render executions produced identical output hashes:
  - PNG SHA-256: `a5bff2596a6bf9ab0becc41cba0a985744c3b31878c6b11281ca2f4cf891fc75`;
  - PDF SHA-256: `6de47c8df62ae35fc85e5b1ca2010038dd505d2e15b39caaa1f765b30cf4e7ea`.

## Scientific boundary

The `p=0.75` finite-tilt sequence moves slightly away from its analytic limit
over the displayed range.  It has not yet entered its eventual asymptotic
approach; the plotted behavior is therefore recorded as pre-asymptotic rather
than presented as visible convergence.

This figure is a finite binary64 diagnostic of scaling, sign, and constants.
It is not a proof of the Laplace limit, the exact integer-shear transfer, the
signed-flux estimate, or any Navier--Stokes regularity statement.
