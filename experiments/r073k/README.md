# R0.73K finite uniform-viscous-branch diagnostic

This directory contains a reproducible, finite Fourier diagnostic for the
parameter-dependent viscous branch on

\[
 0\le d\le 1/450,\qquad (\beta,\xi,\gamma)=(0,0,1/2).
\]

The primary implementation constructs each matrix from the four-term column
recurrence.  The independent validator does not import that producer: it
reconstructs the matrix from the Fourier coefficients of \(W_d\) and
\(W_d''\).  Both work after the exact kinetic-space isometry, so their
Euclidean projector norms are finite-compression diagnostics in the physical
kinetic norm.

## Frozen design

- Seventeen equally spaced parameter nodes \(d_j=j/7200\),
  \(j=0,\ldots,16\), cover \([0,1/450]\), including both endpoints.
- Five cutoffs \(N=24,48,96,128,160\) expose the low-resolution trend and
  retain three high-resolution comparisons.
- The core viscosities satisfy \(0\le\varepsilon\le10^{-3}\).  At every core
  row and every cutoff, the program requires exactly one eigenvalue in the
  fixed circle \(|z-0.17|<0.003\).  It fails closed instead of replacing a
  missing or multiple circle root by a nearest eigenvalue.
- The values \(3\times10^{-3}\) and \(10^{-2}\) are deliberately outside the
  core claim.  They are stress rows selected only by continuation from the
  preceding viscosity; leaving the fixed circle is expected and is recorded.
- Each row preserves both right and left algebraic and embedded residuals,
  the induced \(\|BP-\lambda P\|\) and \(\|PB-\lambda P\|\) residuals,
  the stable rank-one idempotency residual \(\|P^2-P\|\), normalized
  left/right overlap, projector norm, \(P_\varepsilon-P_0\), the eigenvalue
  difference quotient, its exact finite adjoint identity, and the first-order
  adjoint formula at zero viscosity.
- Adjacent cutoffs are compared after zero-embedding the smaller rank-one
  projector into the larger Fourier space.  This is stronger than comparing
  projector norms alone, but it remains a finite computation.

## Files

- `config.json`: frozen parameter grid, circle, and numerical tolerances;
- `viscous_branch_diagnostic.json`: primary results (generated);
- `progress.ndjson`, `resources.ndjson`: row-level progress and resource
  telemetry from the primary run (generated);
- `environment.json`: interpreter, package, platform, and thread settings
  (generated);
- `independent_validate.py`: independent Fourier-coefficient reconstruction;
- `independent_validation.json`: full comparison report (generated);
- `independent_progress.ndjson`, `independent_resources.ndjson`: independent
  run monitoring (generated);
- `seal_package.py`, `manifest.json`, `SHA256SUMS`: package inventory and
  checksums (the latter two are generated after both runs);
- `validate_package.py`, `package_validation.json`: independent post-seal
  verification of every manifest/checksum entry, bound source/configuration
  hashes, schemas, pass decisions, monitoring logs, and fail-closed claim
  boundaries (the JSON report is generated after sealing);
- `command.txt`: exact local reproduction sequence;
- `requirements.txt`: frozen numerical dependencies.

## Claim boundary

The experiment can expose a discretization or bookkeeping error.  It cannot
prove the common continuum contour, a continuum rank-one Riesz projection,
uniform norm convergence as viscosity vanishes, a complementary semigroup
bound, a nonlinear instability theorem, or the Clay regularity problem.  The
continuum claims, if accepted, come only from the separately audited analytic
proof.
