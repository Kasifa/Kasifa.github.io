# Chart contract and source data

## Claim contract

For all sufficiently large \(j\), set
\(P_j:=P_{R_j}^M=P_{R_j}^F\) on the explicit R0.74F--H family analysed in
R0.74I. The proved chain is

\[
8e^{-8}B_j^3R_j^3
\le \mathcal G_u(z_{0,j},2R_j;1)
\le P_j
\le C B_j^3R_j^3.
\]

Consequently,

\[
\frac{\log P_j}{L_j^2}\longrightarrow\frac{3}{320},
\qquad
\log\frac{P_{j+1}}{P_j}
=\frac{9}{320}L_j^2+O(1).
\]

The lower bound is analytic. The finite certificate checks the rational
geometry and exponent ledger but does not prove the heat-semigroup argument
or the inherited upper bound.

## Source binding

Every finite-arithmetic label is byte-bound to:

- `research/r074j_matching_payment_certificate.json`, SHA-256
  `493c9cf6bc1357b36da1b0a13becbc51e62ea26aab95b6af7eaeb085b65be5d5`;
- `scripts/r074j_matching_payment_certificate.py`, SHA-256
  `6dcc03d283612306dc39669f5b6c8b3cf8569e40205e067c4db0c2b6929879ec`.

The renderer refuses source drift and requires producer stdout to be
byte-identical to the 38/38 JSON. `source-data.csv` records every plotted
exact value, formula, evidence class, and interpretation.

The analytic sources are Lemma 2.1 and Theorems 3.2--3.3 of
`research/r074j_matching_payment_law.md`. The inherited upper source is
R0.74G Theorem 1.1. Independent analytic audits are bound to the promoted
source SHA in the final release rebind. None of these analytic claims is
certified by the finite JSON.

## Visual policy

- Canvas: 178 mm x 88 mm, the project default for a double-column figure.
- Palette: hard two-root cap, blue and gold plus neutrals.
- Non-color distinctions: direct labels, hatch, solid/dashed borders,
  numbered implication stages, and distinct line/point geometry.
- The longitudinal \(x_3/R\) locations are exact. The transverse thickness
  is explicitly labelled schematic.
- No unknown PDE constant is assigned a value.
- The visible footer states `EXACT FAMILY`, `NOT DNS`, `NOT SIMULATION`,
  and `NOT CLAY`.

## Analytic boundary

The certificate does not prove the periodic heat-semigroup/Brownian
representation, the circle-distance exit implication, Chebyshev's theorem,
the continuum shear lower bound, the R0.74F family construction, or the
inherited R0.74G payment upper bound. The theorem does not provide a universal
upper bound for \(X_j\) or \(\mathfrak C_j\), exclude singularities, prove
global regularity, or settle the Clay Millennium problem.
