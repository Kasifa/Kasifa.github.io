# R0.71C exact-certificate bundle

This directory archives the finite exact audits for the R0.71C
signed-localization boundary.

## Decision locked by the bundle

The producer and independent checker verify the following facts.

1. For every additive finite partition,

   \[
    E_\Pi=\sum_{B\in\Pi}
    \frac{((\sum_{i\in B}w_i)^+)^2}{\sum_{i\in B}d_i}
   \]

   is monotone under refinement.  On a binary tree the fine ledger is the
   root ledger plus an exact sum of nonnegative refinement defects.
2. A three-mode family converges in every fixed Sobolev space while one
   normalized positive-output term remains (A^2B^2/64) for every positive
   perturbation and becomes zero at the zero output-strain mode.  The R0.71B
   same-output normalization is therefore discontinuous.
3. A pair of disjoint same-output-radius triads has 24 ordered zero-sum
   resonances, selected works (2,-2), and dissipation weights (8,8).
   Stokes damping creates positive parent work from exact initial
   cancellation.
4. For the full-response tensor (Q=\omega\otimes\omega), the true NSE
   initial derivative of that parent work is

   \[
    12\nu\varepsilon^3+\frac{76}{5}\varepsilon^4>0.
   \]

5. A balanced (M=8,64) HHL family has (a_+(0)=0).  For the orthogonal
   radial-sphere Parseval response, its exact true-NSE low-output derivative
   is

   \[
    \frac{2193\delta^3
    (2193\delta+32704\sqrt{1206545}\,\nu)}{19304720}>0.
   \]

6. The shellwise full-nonlinearity injection gives a scale-critical
   conditional continuation reduction, but signed time-box mass bounds the
   required positive square variation in the wrong direction.

These results reject a static or homogeneous-Grönwall propagation mechanism.
They do not exclude an adaptive material localization with explicit PDE
fluxes.

## Files

- `result.json` — canonical sorted JSON emitted by the producer;
- `independent-result.json` — standalone exact reconstruction;
- `command.txt` — exact reproduction commands;
- `environment.txt` — pinned runtime and dependency record;
- `SHA256SUMS` — hashes for every archived payload and source dependency;
- `../../r071c_exact_audit.py` — R0.71C producer;
- `../../r071c_independent_audit.py` — independent checker;
- `../../r071c_report-source.md` — analytic source;
- `../../r071c_literature_audit.md` — primary-source boundary;
- `../../r071c_independent_audit.md` — independent manual audit;
- `../../r071b_exact_audit.py` — inherited R0.71A/R0.71B acceptance checks;
- `../../r071a_exact_audit.py`, `../../r070z_exact_audit.py`, and
  `../../r070x_exact_audit.py` — transitive exact dependencies.

## Analytic boundary

The programs certify finite Fourier identities and symbolic inequalities.
The arbitrary finite-partition theorem, conditional continuation theorem,
smooth-frame small-amplitude argument, and literature comparisons are proved
or bounded analytically in the report.

No estimate deriving (a_+\in L_t^1) or
(A_{\mathrm{sb},+}\in L_t^1) from Leray energy is proved.  The bundle proves
no singularity, global regularity theorem, or solution of the Millennium
problem.

No DNS, stochastic search, GPU, or DGX resource is used.
