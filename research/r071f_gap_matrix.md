# R0.71F working gap matrix — localized projected-Lamb trace

Date: 2026-08-25

Status: working audit matrix; not a theorem and not a publication artifact

R0.71F tests one precise implication: whether standard Leray--Hopf budgets,
combined with mollified-flow skewed-cylinder geometry, control a localized
bottom trace of the positive projected-Lamb work without assuming an already
regularizing norm.  The table fixes the burden of proof before any estimate is
accepted.

| Lane | Available input | Exact missing step | Mandatory stress test | Acceptance rule |
|---|---|---|---|---|
| Geometry | Yang/Vasseur--Yang skewed cylinders and their maximal/covering estimates | Construct cutoffs with stated trajectory, radius, time, and overlap constants; quantify every material-shape residual | Large mollified drift and neighboring cylinders with intersecting collars | Geometry may supply bounded overlap only; it cannot be credited with analytic trace gain |
| Local equation | \((\partial_t-\nu\partial_s)W_{j,s}=\operatorname{curl}(A_{j,s}L)\) | Derive the skewed-cylinder ledger while retaining cutoff--curl and shape terms | Replace \(A_{j,s}L\) by \(A_{j,s}(u\times\omega)-\nabla A_{j,s}B\) and verify exact Bernoulli cancellation | Every term must be an identity before inequalities are applied |
| Positive packing | Pointwise Cauchy estimate for \(B_Q^L=\langle A_{j,s}L,\operatorname{curl}(\phi_QW_{j,s})\rangle\) | Sum over the admissible covering and compare the stabilized local denominator with the original shell palinstrophy | Collar-dominated cutoffs, including blocks whose interior curl is small | Any hidden \(r^{-2}\|W\|_2^2\) cost stays explicit; it may not be renamed dissipation |
| Vertical trace | Energy controls \(\int_0^\infty \Theta_s^2\,ds\), not \(\Theta_0^2\) | Identify a valid caloric trace theorem and list its derivative/Besov boundary hypotheses | Dyadic six-mode global-smooth 2D3C family with \(\Theta_0^2=2K^2\int\Theta_s^2ds\) | Reject every bulk-to-bottom estimate lacking the full frequency-square cost or an independent trace regularity input |
| Local obstruction | The R0.71E witness is exact at the global initial trace | Decide whether a fixed-size or parabolically rescaled local/skewed cylinder evades the witness | Translate the cylinder to a point of nonzero local positive density and take radius comparable to \(K^{-1}\) | A local criterion is new only if its localization changes a quantified term, not merely the notation |
| NSE budget | Leray energy gives \(\mathcal V\in L_t^1\) | Bound the localized concentration factor independently of \(A_{\rm sb,+}\) | Check scaling and test against all smooth high-frequency data | No hypothesis algebraically equivalent to \(\Lambda_L^2\mathcal V\in L_t^1\) is accepted as progress |
| Comparison | Serrin, Koch--Tataru, critical Besov, BKM/dissipation-wavenumber criteria | Prove implication, separation, or explicitly state unknown relation | Track scaling, time exponent, amplitude, and whether the assumption is a priori or posteriori | “Different observable” is not evidence of a weaker criterion |

The branch advances only if at least one of the following closes rigorously:

1. a genuinely weaker localized trace criterion with a proved continuation
   implication and a non-circular hypothesis;
2. an unconditional local packing theorem together with a sharp theorem
   showing why skewed geometry alone cannot produce the bottom trace;
3. a new NSE-specific cancellation that survives the six-mode witness and all
   cutoff/collar terms.

Otherwise R0.71F records a negative route decision and does not claim a new
regularity criterion.
