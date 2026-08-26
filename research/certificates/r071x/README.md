# R0.71X certificate

This directory archives three separate finite audits for the fixed-small-
coupling one-third endpoint release.

- `result.json` is produced by `research/r071x_exact_audit.py`.  It uses
  90-digit decimal arithmetic for the limiting interpolation, exact normalized
  endpoint algebra, the \(D^\beta\) trichotomy, and the \(\delta^{4/3}\)
  collapse.
- `independent-result.json` is produced by
  `research/r071x_independent_audit.py`.  It imports neither the producer nor
  its output and independently reconstructs the response matrix and power
  ledger in binary64.
- `truncated-coset-result.json` is produced by
  `research/r071x_truncated_coset_audit.py`.  It solves a finite nonlinear
  Fourier-coset system, exact finite root equations, a retained full-coset
  \(\dot H^{-1}\) rotational quadrature, root-exclusion scans, and truncation
  checks.

The programs do not replace the analytic proof.  The uniform infinite-lattice
Dyson bounds, divided-map implicit-function theorem, complete real-time root
set, exact atom normalization, nonlinear enstrophy ratio, and full continuum
projected rotational estimate are proved in
`research/r071x_report-source.md`.

The certificate supports internal \(D^{1/3}\Lambda_1\) saturation for a
globally smooth exact triangular NSE family.  It proves no universal endpoint
estimate, continuation criterion, finite-time singularity, or global
regularity result.  The finite computation uses `atomProxy` wherever the
annular multiplier constants are not numerically locked.  Its fixed
\(\delta=1/128\) is not a validated numerical lower bound for the continuum
IFT radius.
