# Chart contract and source-data specification

## Analytical question

Which temporal and shell-selection quantifiers separate the moving-deletion,
fixed-deletion, simultaneous-clock, and coordinatewise-maximal functionals,
and why can the inherited linear ledger not supply a fixed-budget
\(2/3\)-power bound?

## Supported takeaway

Step 18 proves an exact hierarchy and a payment-shifted target-scale
equivalence between fixed hybrid height and simultaneous completed-clock
height.  Exact disjoint triangular clocks sharply separate moving from fixed
deletion and simultaneous from coordinatewise maxima.  At fixed deletion
budget, the ledger-normalized fixed height grows as \(H^{1/3}\).

## Surface and form

- Surface: standalone double-column paper figure.
- Physical size: 178 mm by 116 mm.
- Exports: vector SVG and PDF, plus 600-dpi PNG.
- Layout: four panels in a two-by-two grid.
- Renderer: Python 3.12.13, NumPy, and Matplotlib with pinned versions.
- Evidence: exact finite formulas and deterministic rendering; no stochastic
  sampling and no PDE simulation.

## Panel contract

- **A:** six exact node records and seven exact edge records, with separate
  visual grammar for literal inequalities and estimates containing known
  payments.
- **B:** 1001 exact samples for each of five disjoint triangular clocks with
  \(N=2,M=5,H=1\).
- **C:** the six exact functional values in (S.490) at that parameter choice.
- **D:** 73 logarithmically spaced heights for fixed \(N=2,M=4\), evaluated
  from the exact formula in (S.492), plus an exact slope audit.

## Palette and non-color distinctions

The palette uses one navy and one burnt-orange root plus charcoal and neutral
grays.  Line style, marker shape, hatch, direct labeling, and panel separation
duplicate every important distinction.  `qa-grayscale.png` is part of the
sealed archive.  The research blossom is locked to the header's top-right
corner.

## Source-data schema

`source-data.csv` is a long-form table with fields:

`panel,record,series,x,y,x_unit,y_unit,evidence_class,formula_source,method`

Numeric values use round-trip-safe decimal formatting.  The validator
regenerates every row from `config.json` and `plot.py` and requires exact
equality.

## Formula authority and claim boundary

The exclusive mathematical source is core commit
`5a9c172e1db8886d49fdf15b8676b4810b002ae3`,
`research/r074s_fixed_deletion_simultaneous_height.md`, equations
(S.477)--(S.492), checked by the bound main certificate and report.  The
figure visualizes already-proved reductions and abstract stress tests.  It
does not prove (S.486), (S.487), global regularity, or the Clay problem.
