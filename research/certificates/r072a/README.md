# R0.72A certificates

This directory archives two independent finite audits for the local-exposure
strong-coupling theorem and exact one-carrier Bessel family.

- `result.json` is produced by `research/r072a_exact_audit.py`. It recomputes
  the exponent boundary, Bessel moment identity and logarithmic coefficient,
  then solves bilateral finite lattices with complex SciPy DOP853 and roots
  bracketed around the limiting Bessel zeros.
- `independent-result.json` is produced by
  `research/r072a_independent_audit.py`. It imports neither the producer nor
  its output. It evolves the exact invariant real phase with fixed-step RK4,
  discovers roots from unseeded sign changes, and refines them with cubic
  Hermite interpolation.
- `producer-monitor.log` and `independent-monitor.log` are timestamped process
  logs. The producer reports every completed dyadic solve and its independent
  truncation-doubling pass.
- `config.json`, `command.txt`, `seed.txt`, and `environment.txt` record the
  raw configuration and runtime. `SHA256SUMS` is generated only after the
  release package is complete.

The analytic proof is in `research/r072a_report-source.md`; its separate
line-by-line review is in `research/r072a_independent_audit.md`. Finite
truncations corroborate but do not prove the infinite-lattice theorem. These
files do not contain a three-dimensional DNS, interval proof of the continuum
evolution, normalized nonlinear lower bound, or Navier--Stokes regularity
proof.

The calculations are deterministic and use no pseudorandom input. The word
"exact" in the producer name refers to the algebraic model being audited, not
to exact floating-point or interval arithmetic.
