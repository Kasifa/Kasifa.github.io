# R0.72O formal figure package

This package builds the 2 x 2 journal figure for the physical-reinsertion
theorem in `research/r072o_report-source.md`.

The figure separates four statements that must not be conflated:

- Panel A compares the old one-carrier window scale
  `R^(2/3) (1+log R)` with the enhanced-dissipation scale
  `R^(4/3) (1+log R)^2`. Unknown theorem constants are suppressed.
- Panel B evaluates the old and enhanced-dissipation normalized algebra at
  fixed `R=64`. The enhanced-dissipation branch is no larger, and is strictly
  smaller for `epsilon>1`, but it eventually rises above the scale-one guide;
  this visualizes the fixed-geometry boundary of the current proof.
- Panel C shows the `p^(4/3)` conditional multi-carrier window at `R=256`.
  The filled blue `N=1, p=1` point is unconditional. The open ochre curve for
  multi-carrier superpositions is conditional on the full integrated
  enhanced-dissipation hypothesis with constants uniform over the plotted
  parameter and geometry family.
- Panel D plots the exact two-carrier common-band profile near its flat
  critical point. Its normalized cubic departure is compared with a Morse
  quadratic reference. This is a theorem-applicability obstruction, not a
  counterexample to the desired multi-carrier estimate.

Producer and independent audit anchors are read from
`research/certificates/r072o/`. Their crosscheck must pass before plotting.
The dense curves are direct evaluations of formulas already proved or stated
conditionally in the report. No PDE solve, regression, fitted exponent, or
interpolation is performed by this package.

`data.csv` stores every plotted row with its panel, route, claim kind, source
file, equation pointer, and boundary note. The archival masters are
`figure.pdf`, `figure.svg`, and a 600 dpi `figure.png`, all at
177.8 x 132.08 mm. Public copies in `public/assets/r072o/` must be
byte-identical to the masters.

`manifest.json`, `SHA256SUMS`, `validation.json`, the three QA surfaces, and
the manual QA report complete the formal archive only after explicit visual
inspection and source/certificate lineage sealing.
