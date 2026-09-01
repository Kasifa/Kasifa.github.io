# R0.74J candidate, collision, and evidence matrix

The status labels are `PROVED`, `PUBLISHED`, `FINITE`, `OPEN`,
`REJECTED AS ROUTE`, and `NOT CLAIMED`.

For the exact family, write the common payment as
\(P_j:=P_{R_j}^M=P_{R_j}^F\).

| ID | Candidate or claim | Best current evidence | Status | R0.74J decision / boundary |
|---|---|---|---|---|
| J1 | Admissible mollified trajectories at nearby scales stay within a constant multiple of the larger radius. | J. Yang, *Ann. Inst. H. Poincare Anal. Non Lineaire* 39 (2022), final Lemma 6 / arXiv v2 Lemma 9, DOI `10.4171/AIHPC/20`. | **PUBLISHED** | Strong collision.  Do not claim this geometry as new. |
| J2 | Intersecting admissible skewed cylinders have quantitative spatial containment; a sufficiently admissible large cylinder contains neighboring smaller same-center cylinders. | Yang 2022, final Proposition 7 and proof of final Proposition 11 / arXiv v2 Propositions 10 and 14. | **PUBLISHED** | Factor-\(9\) containment is only during the common lifespan; neighboring-scale \(3/4\)-containment also requires the same centre, stated scale band, and stronger threshold.  A future result would have to derive admissibility from the R0.74 payment rather than assume it. |
| J3 | Skewed cylinders and mollified-flow recentering already enter suitable-weak Navier--Stokes regularity estimates. | A. Vasseur and J. Yang, *Arch. Rational Mech. Anal.* 241 (2021), 683--727, DOI `10.1007/s00205-021-01661-4`. | **PUBLISHED** | Do not claim a first suitable-weak moving-cylinder framework. |
| J4 | Finite total dissipation makes every sufficiently small skewed cylinder admissible at a prescribed point. | Yang final Proposition 11 / arXiv v2 Proposition 14 proves eventual admissibility only for almost every point.  An exceptional set may contain all singular points. | **OPEN** | No fixed-candidate-singular-point implication is available. |
| J5 | Hollow-shell pigeonholing creates small dissipation layers and logarithmically improves partial regularity. | Z. Lei and X. Ren, *Adv. Math.* 445 (2024), 109654, DOI `10.1016/j.aim.2024.109654`. | **PUBLISHED** | A small hollow shell does not by itself control the normalized moving core at a prescribed point. |
| J5A | A velocity-only one-scale exponent-\(3\) epsilon criterion is available for suitable weak solutions. | Y. Wang, G. Wu, and D. Zhou, *J. Differential Equations* 267 (2019), 4673--4704, Theorem 1.1 with \(\delta=1/2\), DOI `10.1016/j.jde.2019.05.003`. | **PUBLISHED** | The theorem concludes regularity on \(Q(1/16)\); it does not force its smallness hypothesis at a prescribed possible singular point. |
| J6 | Finite global energy alone produces one R0.74I-small moving tube at any prescribed possible singular point. | No source or local proof.  Absolute continuity alone does not control the scale-invariant normalization at a fixed exceptional point. | **OPEN** | This remains the global route gap; it is not the R0.74J theorem target. |
| J7 | The R0.74F--H family analysed in R0.74I has a matching lower payment \(P_j\gtrsim B_j^3R_j^3\). | R0.74J Theorem 3.2; inherited R0.74G upper bound; two independent analytic audits. | **PROVED** | Selected theorem target. |
| J8 | The fifth-shell box lies wholly in \(A_5(2R)\), has weight \(e^{-8}\), and the shear is at least \(1/2\) there. | R0.74J Lemmas 2.1 and 3.1; periodic Brownian representation; independent heat audit; 38/38 finite certificate. | **PROVED / FINITE** | The finite certificate checks arithmetic only; the heat argument is analytic. |
| J9 | The complete payment satisfies \(P_j\asymp B_j^3R_j^3\). | R0.74J Theorem 3.3, R0.74G Theorem 1.1, and independent ledger audit. | **PROVED** | Versions M and F coincide only because the explicit family has zero frame acceleration. |
| J10 | The old window \(2/320\le\liminf \log P_j/L_j^2\le\limsup\le3/320\) sharpens to the limit \(3/320\). | R0.74J Corollary 4.1; independent ledger audit; exact exponent certificate. | **PROVED / FINITE** | Exact-family asymptotic only. |
| J11 | The square-root-log endpoint upper bound holds for arbitrary suitable weak solutions. | No theorem.  The explicit family fixes the payment scale on this family but supplies no arbitrary-solution upper estimate. | **OPEN** | R0.74J neither proves nor refutes the universal endpoint. |
| J12 | The explicit family satisfies \(X_j\lesssim B_j^2L_jR_j^2\) or an endpoint upper bound. | No complete inward-tail upper audit. | **OPEN** | Do not infer saturation from the payment equivalence. |
| J13 | The bounded collision search proves novelty or priority. | Two focused literature lanes plus one internal analytic lane, not an exhaustive professional review. | **NOT CLAIMED** | The release states only the verified collision boundary. |
| J14 | R0.74J proves global regularity or resolves the Millennium problem. | No such implication. | **REJECTED AS ROUTE** | **NOT CLAY.** |

## Search stop

The first pass compared three materially different routes: cross-scale
trajectory geometry, singular-point good-scale selection, and exact-family
payment asymptotics.  The focused pass found direct prior results for the
first route and a fixed-point scaling gap in the second.  The third route has
an explicit one-shell lower-bound mechanism and is therefore selected.
Additional broad searching is unlikely to change this internal theorem
target; later source work is limited to claim-level verification and the
release boundary.
