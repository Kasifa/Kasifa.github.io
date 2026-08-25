# R0.71N certificate bundle

This bundle certifies the complete fixed-cell derivative identity, the exact
nominal-rate cancellation, the square--residual form, and the cancellation of
the apparent positive square after the local filtered-enstrophy identity is
substituted.

The exact producer checks:

- the \(B_t,d_t,Y_t\) quotient rule;
- the radial/projective \(\nu\kappa^2\) cancellation;
- the square--residual representation;
- the local filtered-enstrophy and second-jet rewrite;
- the formal local Euclidean scaling ledger; and
- the \(Y>0,d_Q>0\), fixed-cutoff domain boundary.

The standalone checker declares two explicit smooth periodic velocity fields
and reconstructs their NSE initial jets without importing the exact producer.
At orders 48, 64, and 80 it verifies five representations of
\(\mathcal J_Q\), the local enstrophy balance, and the square cancellation.
Both witnesses have \(z_Q>0\), while their complete signed sources have
opposite signs.

Claim boundary: the Fourier signs are high-margin binary64 diagnostics, not
outward-rounded sign theorems. The bundle proves no bound for the signed
second jet, denominator faces, continuation criterion, singularity, global
regularity, originality, or Millennium-problem result.

## Files

- result.json - exact symbolic result;
- independent-result.json - standalone three-resolution Fourier diagnostic;
- command.txt - reproduction commands;
- environment.txt - execution environment;
- build_hashes.py and SHA256SUMS - archive integrity;
- ../../r071n_exact_audit.py and ../../r071n_independent_audit.py - producers;
- ../../r071n_report-source.md, ../../r071n_gap_matrix.md,
  ../../r071n_literature_audit.md, and ../../r071n_independent_audit.md -
  analytic evidence;
- ../../../figures/r071n-full-scalar/fig-r071n-square-residual-boundary -
  journal figure package.
