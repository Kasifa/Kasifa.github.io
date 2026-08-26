# R0.71W certificate

This directory archives three separate finite audits for the amplitude-doped
complete-first-row release.

- result.json is produced by research/r071w_exact_audit.py. It uses 90-digit
  response interpolation, exact heat/tangent enstrophy, a full-frequency
  rotational upper bound, and exponent algebra.
- independent-result.json is produced by
  research/r071w_independent_audit.py. It imports neither the producer nor
  its output and independently rebuilds the leading ledger in binary64.
- truncated-coset-result.json is produced by
  research/r071w_truncated_coset_audit.py. It solves a nonlinear retained
  Fourier-coset system, exact finite root equations, and a retained-coset
  \(\dot H^{-1}\) rotational quadrature with truncation checks.

The scripts do not replace the analytic proof. The uniform infinite-lattice
Dyson bounds, divided-map implicit-function theorem, exact continuum roots
and slopes, nonlinear enstrophy ratio, and full continuum projected
rotational estimate are proved in research/r071w_report-source.md.

The certificate supports the powers of a globally smooth exact triangular
NSE family for which one fixed-shell atom defeats the complete
data-independent first-row Leray ledger. Initial energy and enstrophy grow
like \(q^{2\alpha+2}\). No arbitrary data-dependent estimate, continuation
criterion, finite-time singularity, global regularity, novelty, or priority
statement is certified.
