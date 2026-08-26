# R0.72C certificates

This directory archives two independent machine audits for the physical-phase
extension, heat-participation theorem, and sharp algebraic carrier scales.

- result.json is produced by research/r072c_exact_audit.py with 90-decimal
  mpmath arithmetic. It reconstructs the naive-complex counterexample,
  conjugate-paired skew identity, joint inequality, three heat regimes, exact
  phase boundaries, and two sharp families.
- independent-result.json is produced by
  research/r072c_independent_audit.py. It imports neither the producer nor its
  output. It uses binary64 finite matrices, direct trigonometric evaluation,
  independent Rudin--Shapiro generation, and separate regressions.
- producer-progress.ndjson and independent-progress.ndjson preserve stage
  updates. The corresponding monitor logs preserve the console stream.
- producer-resource.ndjson and independent-resource.ndjson record elapsed
  time, CPU time, resident-set usage, and logical CPU count.
- config.json, command.txt, seed.txt, and environment.txt record the declared
  configuration and runtime. SHA256SUMS is generated after the package is
  complete.

The analytic report is primary. These programs use high-precision or binary64
floating-point arithmetic without directed rounding. They are not interval
certificates, an infinite-lattice proof, a three-dimensional DNS, a lower
bound on the actual root ledger, or a Navier--Stokes regularity result.

The fixed-positive-time result controls only roots observed after burn-in.
It cannot remove the nonnegative pre-ledger. Rudin--Shapiro sharpness concerns
the algebraic upper-prefactor coefficient, not saturation by a solution.
