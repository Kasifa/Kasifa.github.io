# R0.72B certificates

This directory archives two independent machine audits for the target-row
coherence refinement and the coherent many-carrier exclusion.

- `result.json` is produced by `research/r072b_exact_audit.py`. It reconstructs
  the constants at 80 decimal digits, checks the equal-carrier geometric
  prefactor, evaluates representative mixed-exposure integrals, and records
  the Bessel short-layer comparison indicators.
- `independent-result.json` is produced by
  `research/r072b_independent_audit.py`. It imports neither the producer nor
  its output. It rebuilds a finite shift matrix from raw parameters, evolves
  it with complex DOP853, and checks the target-row norm and Q payment with
  separate binary64 quadrature.
- `producer-progress.ndjson` and `independent-progress.ndjson` preserve stage
  updates. The corresponding monitor logs preserve the console stream.
- `producer-resource.ndjson` and `independent-resource.ndjson` record elapsed
  time, CPU time, resident-set usage, and logical CPU count.
- `config.json`, `command.txt`, `seed.txt`, and `environment.txt` record the
  declared configuration and runtime. `SHA256SUMS` is generated after the
  package is complete.

The analytic argument is primary. These files use high-precision or binary64
floating-point arithmetic without directed rounding. They are not interval
certificates, an infinite-lattice proof, a three-dimensional DNS, a normalized
lower construction, or a Navier--Stokes regularity result. A positive burn-in
can estimate only the remaining tail ledger; it cannot remove the nonnegative
slope mass accumulated before burn-in.

## Recorded restart

The first run used equal-carrier data only through \(M=4096\). Both programs
rejected a tolerance that required the short finite-tail regression to equal
the asymptotic exponent within \(10^{-3}\). The underlying exact formulas and
all other checks passed. The corroborative dyadic sequence was then extended
to \(M=2^{20}\), without changing the theorem or loosening the exponent gate.
The appended progress, resource, and monitor logs preserve both attempts.
