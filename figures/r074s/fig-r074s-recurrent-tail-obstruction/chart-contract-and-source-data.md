# Chart contract and source-data specification

## Analytical question

How does recurrence on a regular closed Taylor-vortex streamline make absolute temporal flux variation scale like the complete cubic payment while signed positive excursion stays at the quadratic terminal scale?

## Supported takeaway

On the frozen smooth exact family, one orbit has nonconstant periodic
\(g=|W|^2\), with exact range \([1/2,3/4]\) and total variation \(V_1=2\)
per return.  Repeating the circuit therefore accumulates absolute variation
without accumulating signed range.  This explains the proved split
\(\mathfrak H^F_1\asymp A^3\) versus
\(\mathfrak O^{F,+}\asymp A^2\), with \(P_R^M\asymp A^3\).

## Surface and form

- Surface: standalone double-column paper figure.
- Physical size: 178 mm by 116 mm.
- Exports: vector SVG and PDF, plus 600-dpi PNG.
- Layout: four panels in a two-by-two grid.
- Renderer: Python 3.12.13, NumPy, and Matplotlib with pinned versions.
- Evidence: exact formulas plus deterministic quadrature/fixed-step rendering; no stochastic sampling and no PDE simulation.

## Panel contract

- **A:** 1201 analytic level-set samples, four direction arrows, and two exact witness points.
- **B:** 1025 stored samples from an 8192-step one-period RK4 audit, plotted against normalized orbit time.
- **C:** four tiled periods of the signed primitive and cumulative absolute variation; cumulative variation is reconstructed from monotone primitive increments on symmetry-resolving nodes.
- **D:** 81 logarithmically spaced amplitudes for each of five normalized exponent guides.  Curves show exponent classes, not fitted constants.

## Palette and non-color distinctions

The palette uses one navy and one burnt-orange root plus charcoal and neutral grays.  Line style, open/filled markers, and panel separation duplicate every important distinction.  `qa-grayscale.png` is part of the sealed archive.  The research blossom is locked to the header's top-right corner.

## Source-data schema

`source-data.csv` is a long-form table with fields:

`panel,record,series,x,y,x_unit,y_unit,evidence_class,formula_source,method`

Numeric values use round-trip-safe decimal formatting.  The validator regenerates every row from `config.json` and `plot.py` and requires exact equality.

## Formula authority and claim boundary

The exclusive mathematical source is core commit
`7355c01dead23c3524242006318b02a8324447e6`,
`research/r074s_recurrent_streamline_temporal_tail_obstruction.md`, equations
(S.445)--(S.475), checked by the bound main certificate and report.  This
figure illustrates the already-proved obstruction and successor scale.  It
does not prove (S.472), global regularity, or the Clay problem.
