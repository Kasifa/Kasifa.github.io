# Figure contract -- R0.72E supercritical ledger

## Analytical question

At the fixed carrier (q_0=4), do two numerically independent finite audits
reproduce the three scale mechanisms used in R0.72E: logarithmic selected
Bessel slope mass, negative-Sobolev action of order
((log\delta)/\delta), and the (R^{4/3}) selected-ledger lower-bound
growth left after the (D^{1/3}) payment?

## Intended takeaway

The frozen Bessel calculation and the independently evolved dissipative roots
approach the same logarithmic coefficient. The split-step and independent BDF
actions remain bounded after division by ((\log\delta)/\delta). The selected
root ledger, which is a lower bound for the complete nonnegative ledger, grows
near the (R^{4/3}) power reference after normalization at (R=8).

## Chart family and variants

- Family: three-panel static journal figure.
- Panel A: selected slope mass divided by (log R), with the analytic
  (8/\pi^2) reference.
- Panel B: (Q_X/[(\log\delta)/\delta]) for the split-step producer and the
  independent BDF calculation. The legend declares their different finite
  horizons (X=6) and (X=1).
- Panel C: the producer and independent selected-ledger ratios, each divided
  by its (R=8) value, against the exact power-ledger reference
  ((R/8)^{4/3}).
- Variants: archival color figure and grayscale QA rendering.

## Data sufficiency and grain

- Panel A uses four dyadic values (R=8,16,32,64). These are discrete
  asymptotic checkpoints, not a time trend.
- Panel B uses all six producer couplings and all four independent couplings.
- Panel C uses four dyadic values from each certificate. With only four finite
  points, the analytic exponent is shown as a declared reference rather than
  estimated visually from an unconstrained fit.
- Every plotted point and reference row is preserved in `data.csv` with its
  JSON source pointer. No value is manually transcribed from a report or image.

## Renderer and publication surface

- Renderer: Python/Matplotlib static vector workflow.
- Target: mathematical-analysis journal and project research note.
- Final width: 178 mm double column.
- Exports: vector PDF, SVG, and 600 dpi PNG.
- QA: final-size raster, PDF raster, grayscale, hashes, and exact source-copy
  checks.

## Visual encoding

- Producer rows: solid navy line with filled circles.
- Independent rows: dashed rust line with open squares.
- Analytic references: thin dotted charcoal line.
- Color is duplicated by line style and marker fill.
- Panels A and B use logarithmic base-2 horizontal axes and linear vertical
  axes. Panel C uses logarithmic base-2 axes on both dimensions.
- Titles are neutral and descriptive. There are no gradients, fitted bands,
  3D effects, or decorative data marks.

## Claim boundary

The figure is a deterministic binary64 audit. The Panel C quantity uses only
selected roots, so it is a lower bound mechanism for the complete nonnegative
ledger. The bounded (\Lambda_1) factor and fixed target-multiplier constant
are omitted from the plotted normalization. The figure does not prove the
infinite-lattice root persistence, the negative-Sobolev action theorem, the
Malliavin density estimate, Navier-Stokes regularity, singularity formation,
or the Millennium problem.

## Output and QA criteria

1. No clipped text, collisions, detached annotations, or hidden marks at
   178 mm width.
2. PNG metadata reports approximately 600 dpi.
3. PDF is a one-page vector export and SVG contains vector paths.
4. Producer, independent, and reference rows remain distinct in grayscale.
5. Axis labels state every normalization and the action horizons are visible.
6. CSV copies source values exactly and source hashes match both certificates.
7. Configuration, contract, data, results, environment, commands, logs,
   validation, manifest, QA surfaces, public copies, and checksums are archived.
