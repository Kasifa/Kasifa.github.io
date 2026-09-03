# Chart contract and source-data specification

## Analytical question

Can separating two ordinary \(R^3\)-long packet lobes in time avoid the
Version-M exterior cubic payment, and what normalized dwell would be required
to keep the explicit lobe-floor payment bounded?

## Supported takeaway

Two lobe floors can be scheduled on disjoint admissible windows within one
exact common-shear solution, but scheduling does not enter the one-lobe
Hölder coercivity. Along the inherited adjacent-shell survival path, a
unit-dwell outer lobe has a diverging normalized payment factor; bounded
payment relative to that lobe-floor witness requires an exponentially
collapsing maximal comparable-floor dwell.

## Surface and form

- Surface: standalone double-column journal figure.
- Physical size: 178 mm by 116 mm.
- Exports: vector SVG and one-page PDF, plus 600-dpi PNG.
- Layout: four panels in a two-by-two grid.
- Renderer: Python 3.12.13, NumPy, and Matplotlib with pinned versions.
- Evidence: exact formulas and deterministic derived-analytic evaluations;
  no stochastic sampling, PDE simulation, or fitted model.

## Panel contract

- **A:** exact endpoints and lengths for the two windows in (T.42), with a
  compressed-gap schedule layout and an exact disjointness audit.
- **B:** five atomic factors and their exact product from (T.11)--(T.13), plus
  the resulting monomial exponents.
- **C:** 121 values of `log(Lambda_2)` on the explicit path
  \(d_L=\log L_1\), \(\theta=1\), \(9216\le L_1\le20000\).
- **D:** 121 values of `log10(theta_max)` from (T.28) on the same path with
  the illustrative choice \(C=1\), and the \(\theta=1\) reference.

## Palette and non-color distinctions

The palette uses one navy and one burnt-orange root plus charcoal and neutral
grays. Solid/dashed lines, open/filled markers, hatches, direct labels, and
panel separation duplicate every important distinction. A grayscale export
is sealed. The research blossom is locked to the top-right header corner.

## Source-data schema

`source-data.csv` is a long-form table with fields:

`panel,record,series,x,y,x_unit,y_unit,evidence_class,formula_source,method`

Numeric values use round-trip-safe decimal formatting. Panel A stores actual
dimensionless endpoints \(t/R^2\), not their compressed drawing coordinates.
Panel B stores exact-factor floating representations plus literal formulas in
the method field. Panels C--D store only direct evaluations of the displayed
analytic identities. The validator regenerates every row from `config.json`
and requires exact equality.

## Formula authority and claim boundary

The frozen mathematical authority is core commit
`b120598d36140385676bb4a9922d46abcdff0ba4`, specifically
`research/r074t_schedule_invariant_dwell_coercivity.md`, equations
(T.9)--(T.43), its certificate, and its independent, primary, literature, and
QA audits. All seven Git blobs and SHA-256 digests are locked. The figure
visualizes already-derived statements and does not promote the
one-sided lobe-floor witness to an upper bound for the full
\(\mathfrak L^K\) functional.
