# R0.71Y certificate

This directory archives two independent finite audits for the growing-root
operator-sampling release.

- result.json is produced by research/r071y_exact_audit.py with 90-digit
  Decimal arithmetic. It audits the optimizer, lattice factor, observation-
  coupling envelope, root-separation powers, equal-grid inverse lower bound,
  and R0.71X heat-weighted correction.
- independent-result.json is produced by
  research/r071y_independent_audit.py. It imports neither the producer nor its
  output and constructs finite shift matrices directly to check
  skew-adjointness, dissipativity, contraction, root-coordinate sampling,
  amplitude optimization, separated-root bounds, and determinant
  factorization.

The programs do not replace the analytic proof in
research/r071y_report-source.md. They do not construct a growing exact-root
family, count all nonlinear roots, perform DNS, or prove a universal
Navier--Stokes endpoint or regularity theorem.

R0.71Y also records a corrigendum to the R0.71X open-route matrix: the
observation-layer lower comparison is heat weighted, and that observation
coupling is not the complete launch-to-root IFT certificate.
