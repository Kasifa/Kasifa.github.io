# Figure contract

## Analytical question and takeaway

**Question.** After restoring the R0.72L physical lift, how far does the
R0.72N square-root cubic gain extend the strong-coupling window, and which
parts survive superposition?

**Supported takeaway.** The lifted exponent is (11/6), not (1/2). It
enlarges the proved one-carrier scale window from
(R^{2/3}L_R) to (R^{4/3}L_R^2), but does not pay arbitrary coupling at
fixed (R). The corresponding p-dependent multi-carrier window is only a
conditional implication because common-band data do not imply
full-superposition enhanced dissipation with constants uniform over the
compared parameter and geometry family.

## Chart map

| Panel | Analytical comparison | Form | Claim status |
|---|---|---|---|
| A | old versus ED one-carrier window scale over (R) | highlighted two-series log-log line with audit anchors | proved scale laws, constants suppressed |
| B | old versus ED normalized direct screen at fixed (R) | two-series log-log line with scale-one reference | algebraic diagnostic of the proved bound; not an absolute threshold |
| C | p-dependent ED window at fixed (R) | conditional line plus proved endpoint marker | (N=1) unconditional; every multi-carrier point conditional |
| D | common-band flat critical point versus Morse reference | exact local log-log comparison | exact obstruction to theorem applicability |

## Sources and sufficiency

- Analytic source: `research/r072o_report-source.md`.
- Gap matrix: `research/r072o_gap_matrix.md`.
- Producer inputs: `producer-window.csv`, `producer-degeneracy.csv`, and
  `producer-exponents.json` under `research/certificates/r072o/`.
- Independent inputs: the correspondingly named independent files.
- Cross-route gate: `crosscheck.json` must have status `passed` and every
  recorded relative difference must be at most `2e-12`.
- Expected finite grid: four R values, two regimes, and three relative
  coupling levels, for 24 rows per route.
- Sparse fallback is forbidden. A missing route, case, or claim-status field
  stops the build.

Dense lines in Panels A--D are formula evaluations, not interpolations of the
finite rows. Each output row records its source equation. Panel B normalizes
the unknown action-floor constant to one only to display the exponent algebra;
its horizontal line is explicitly a scale guide, not a certified threshold.

## Theorem, conditional, and diagnostic distinction

- Proved one-carrier quantities use blue solid lines or filled circles.
- Conditional multi-carrier quantities use ochre dashed lines and open
  squares.
- Neutral theorem/algebra references are dark and marker-free.
- Route anchors use distinct circle/square fills so grayscale does not depend
  on color.
- No regression, fitted exponent, extrapolated coefficient, or arbitrary
  theorem constant appears.

## Surface and QA

The static Matplotlib figure is 177.8 x 132.0 mm, exported as editable-text
SVG, one-page PDF, and 600 dpi PNG. The approved hard two-root palette is blue
and ochre plus warm neutrals. A research blossom is locked to the top-right
header corner.

Final QA includes final-size, grayscale, and PDF-raster inspection at 180 dpi;
formula/data checks; producer-independent crosscheck verification; source and
output hashes; public/master byte identity; and explicit inspection of the
proved/conditional/fixed-R distinctions.

## Claim boundary

The unconditional theorem is only for the declared fixed-background,
phase-aligned, row-aligned, exact-root-corrected one-carrier triangular 2.5D
family. The multi-carrier curve assumes full-superposition integrated enhanced
dissipation with constants uniform over the plotted family. The figure proves
neither an arbitrary-coupling fixed-R closure,
multiscale absorption, a general three-dimensional continuation criterion,
finite-time singularity, nor global Navier--Stokes regularity.
