# R0.70Z exact-certificate bundle

This directory archives the finite exact audit for the R0.70Z
principal-eigengap and two-channel response-lift gate.

## Decision locked by the bundle

The producer checks six finite groups:

1. trace-free spectral, anisotropy, and sign-pair identities for \(S:Q\);
2. the exact simple-eigenprojector derivative residuals and Frobenius norm;
3. a six-mode two-radius field with
   \[
   \mathfrak P_Q=\frac{9\sqrt{41}}{164};
   \]
4. a ten-mode sign pair with identical covariance at every Fourier output;
5. the arithmetic supporting
   \[
   \lambda_1-\lambda_2\ge8\Lambda^2,\qquad
   \frac{\lambda_1-\lambda_2}{\lambda_1}\ge\frac23,\qquad
   \frac{\lambda_1-\lambda_2}{\operatorname{tr}Q}\ge\frac12;
   \]
6. the two-channel response traces, the archived R0.70X
   full/principal/defect split, and the sharp common/chord HHL formulas.

The two fields have principal work

\[
 \mathfrak P_Q(\omega_{\Lambda,\pm})
 =\pm\frac{9\sqrt{41}}{164}\Lambda^3
\]

despite having the same pointwise \(Q\).

## Files

- result.json — canonical sorted JSON emitted by the producer;
- command.txt — exact reproduction command;
- environment.txt — pinned runtime and dependency record;
- SHA256SUMS — hashes for every archived payload and producer dependency;
- ../../r070z_exact_audit.py — R0.70Z producer;
- ../../r070x_exact_audit.py — imported thirty-six-mode dependency; and
- ../../r070y_exact_audit.py — prior finite source for the reused 49/197
  filler ledger; and
- ../../r070y_report-source.md — analytic source for the zero-set parity
  lemma and its proof boundary.

## Analytic boundary

The finite producer does not replace the zero-set parity proof, Weyl
inequalities, projector perturbation argument, Littlewood--Paley shell
summation, div--curl Hardy-space theorem, or literature comparison in
../../r070z_report-source.md.

It proves no projector-coherence criterion, enstrophy closure, continuation
theorem, singularity, global regularity, or solution of the Millennium
problem.

No DNS, stochastic search, GPU, or DGX resource is used.
