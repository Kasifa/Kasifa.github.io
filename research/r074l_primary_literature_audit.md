# R0.74L — bounded primary-source collision audit

## Verdict

Across three targeted waves for the main analytic question and two
additional waves for a discarded marginal-projection route, no primary
theorem was found which directly proves or contradicts

\[
 \sup_{\tau\in I_{R_j}}\mathscr B_j(\tau)
 \lesssim L_jR_j^5
\]

for the exact \(R_j\)-dependent packet under normalized periodic bridges.
This is a bounded non-hit, not evidence of novelty or priority.

The closest useful neighbors concern autonomous-shear enhanced
dissipation, stochastic characteristic methods, general Markov bridges,
Itô marginal mimicking, and inverse time changes.  None contains the
short-clock thickened-slice BV lemma proved in the R0.74L draft.

## Claim-to-source ledger

| Primary source | Exact supported result | Applicability | Remaining mismatch |
|---|---|---|---|
| Bedrossian--Coti Zelati, [Enhanced dissipation, hypoellipticity, and anomalous small noise inviscid limits in shear flows](https://arxiv.org/abs/1510.08098), Theorem 1.1 | Fourier-mode \(L^2\) decay for a fixed autonomous periodic shear with finite-order critical points | Establishes the quantitative shear-mixing mechanism | No endpoint conditioning, finite signed collar trace, or constants uniform in the \(R_j\)-dependent family |
| Albritton--Beekie--Novack, [Enhanced dissipation and Hörmander's hypoellipticity](https://arxiv.org/abs/2105.12308), Theorems 1.1--1.2 | Autonomous shear \(L^2\) decay and Gevrey smoothing; time-dependent extension appears only as Remark 1.4 | Quantitative bracket/subelliptic neighbor | A remark is not the needed time-dependent theorem; global norms do not give the collar observable |
| Villringer, [Enhanced Dissipation via the Malliavin Calculus](https://arxiv.org/abs/2405.12787), Theorem 1.1 and Lemma 2.1 | Autonomous mode decay through Malliavin determinant estimates for unconditioned Brownian characteristics | Retains shear--Brownian correlation | No normalized endpoint bridge, path-crossing BV, or \(j\)-uniform collar estimate |
| Gardner--Liss--Mattingly, [A pathwise approach to the enhanced dissipation of passive scalars advected by shear flows](https://arxiv.org/abs/2410.05657), Theorem 1 and Propositions 3.1, 3.4 | Controlled coupling and Girsanov give contraction in total-variation distance | Methodological neighbor for typical and exceptional paths | Total variation of laws is not bounded variation of the clock; the setting is autonomous and unconditioned |
| Liss--Luan, [Uniform-in-diffusivity mixing by shear flows: stochastic and dynamical perspectives](https://arxiv.org/abs/2603.09238), Theorem 1.1 and Lemmas 2.1--2.2 | Finite-window good/bad Brownian decomposition and interval covering for low phase derivative under one autonomous shear | Closest finite-window stochastic neighbor | No endpoint-conditioned bridge, signed collar, or exponentially flattening shear family |
| Li--Thompson, [First Order Feynman--Kac Formula](https://arxiv.org/abs/1608.03856), Theorems 2.2, 3.3, 3.4 | First derivative Feynman--Kac and bridge formulas under geometric hypotheses | Supports legitimate bridge derivative representations | No shear-enhanced collar occupation theorem |
| Çetin--Danilova, [Markov bridges: SDE representation](https://arxiv.org/abs/1402.0822), Theorem 2.1 | Markov bridge construction and \(h\)-transform SDE representation | Foundational bridge legality | Representation only; no quantitative crossing or collar estimate |
| Brunick--Shreve, [Mimicking an Itô process by a solution of a stochastic differential equation](https://arxiv.org/abs/1011.0111), Theorem 3.6 and Corollary 3.7 | A weak SDE can match fixed-time marginals of an Itô process with adapted coefficients and a random initial state | Makes the inverse-clock marginal projection legitimate in principle | Does not provide uniqueness, Markov regularity, or the required heat-kernel bound |
| Kobayashi, [Stochastic Calculus for a Time-changed Semimartingale and the Associated Stochastic Differential Equations](https://arxiv.org/abs/0906.5385), Lemma 2.7 and Theorem 3.1 | Continuous strictly increasing adapted time changes have stopping-time inverses and valid semimartingale calculus | Supports the clipped positive inverse clock | Does not provide the clock occupation bound |
| Aronson, [Bounds for the Fundamental Solution of a Parabolic Equation](https://doi.org/10.1090/S0002-9904-1967-11830-5), Theorem 1 | Gaussian bounds for the measurable-coefficient divergence-form equation treated there | Initially appeared to offer a density route | The projected forward equation is \(\partial_s p=\partial_{xx}(ap)\); direct use would require a theorem not supplied by the checked statement |

## Exact literature boundary

The literature search leaves these proof obligations internal to the
R0.74 route:

1. integrate the terminal-time-dependent bridge family into one legitimate
   forward law without differentiating a changing bridge horizon;
2. preserve the short physical-time clock support and transverse slice
   geometry simultaneously; and
3. convert that occupation control back to the exact periodic
   Jensen majorant with \(|\theta|\), all windings, and the endpoint
   supremum retained.

The R0.74L draft addresses these obligations by direct reversibility,
a positive clipped clock, and a stopping-time Brownian modulus estimate.
It does not quote any paper above as the missing lemma.

## Search waves and stop rule

The bounded audit used:

1. exact theorem searches for the principal autonomous-shear and
   stochastic enhanced-dissipation papers;
2. Brownian bridge, Feynman--Kac, shear, local time, crossing, and BV
   combinations;
3. conditioned bridge and enhanced-dissipation collision variants;
4. Gyöngy/Brunick--Shreve marginal mimicking and inverse additive time
   change;
5. one-dimensional measurable-coefficient Gaussian bounds for
   \(\partial_s p=\partial_{xx}(ap)\).

The search stopped at the predeclared caps because later queries converged
to general bridge construction or operator classes not matching the frozen
majorant.  No novelty, priority, or completeness claim follows.
