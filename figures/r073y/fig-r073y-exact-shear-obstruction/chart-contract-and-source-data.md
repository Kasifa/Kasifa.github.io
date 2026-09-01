# Chart contract and source-data specification

## Analytical question

Can signed heat-scale production observables alone control a positive, amplitude-cubic exterior-size quantity on the exact shear family?

## Supported takeaway

No. On the frozen exact-shear family, $\Pi_s$ and $\mathscr S_s$ vanish pointwise for all $s>0$, while $D_{ii,s}$ is strictly positive and the normalized positive size grows as $|A|^3$.

## Surface and form

- Surface: standalone, double-column, paper-ready static figure.
- Renderer: pinned Python/Matplotlib.
- Width and height: 178 mm by 62 mm.
- Exports: vector PDF and SVG plus 600 dpi PNG.
- Canonical family: three aligned line-chart panels.
- Variant: highlighted multiseries profiles, exact scale statistics, and amplitude homogeneity against a zero reference.

## Panel contract

- Panel A: 721 phase points for each of four heat scales. Four color/line-style pairs encode scale; a dark dashed baseline encodes $\Pi_s=\mathscr S_s=0$.
- Panel B: 401 geometrically spaced heat scales. Three line styles show exact pointwise minimum, spatial mean, and pointwise maximum on common log-log axes.
- Panel C: 281 amplitude points. The normalized positive size $|A|^3$ is shown against the exact zero-production baseline.

The row count is more than sufficient to resolve each analytic curve. No interpolation, fitting, stochastic sampling, or numerical trajectory evolution is used.

## Palette and non-color distinctions

The palette is restricted to navy, gold, orange, olive, charcoal, and neutral grays. Every simultaneous series is also distinguished by line style. The archive includes a grayscale QA render.

## Source-data schema

`source-data.csv` is a long-form table with fields:

`panel, record, series, x, y, x_unit, y_unit, evidence_class, formula_source`

Every numeric row is regenerated from the formula authority identified below. Values use round-trip-safe decimal formatting.

## Formula authority and claim boundary

The sole formula source is frozen commit `1ecc6fe20a921db9d0876dbd4484a3aa4ca7ec66`, `research/r073y_exact_shear_no_go.md`, Theorem 1.1 equation (1.4), corroborated by the exact single-sine certificate. The plot is an analytic obstruction and sanity check. It is not DNS, does not establish a new regularity criterion, and does not solve the Clay problem.
