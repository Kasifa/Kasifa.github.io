# R0.73C frozen Rayleigh experiment package

This directory deliberately contains three evidence classes.

1. `interval_run_a.json` and `interval_run_b.json` are rigorous enclosures of
   the infinite-dimensional periodic Rayleigh ODE.  They use the same pinned
   source but different step partitions, Taylor orders, and precisions.
2. `decimal_interval_validation.json` is a separate implementation using
   Python Decimal directed rounding and a Machin-series enclosure of pi.  It
   imports neither mpmath nor the primary interval producer.
3. `fourier_screen.json` and `independent_fourier_validation.json` are finite
   Fourier/Fredholm diagnostics.  They agree on the candidate location but do
   not prove an infinite-dimensional eigenvalue.

The theorem uses only the certified opposite signs of
`trace(M(eta))-2` at `eta=0.3407` and `eta=0.3410`, together with the exact
determinant-one, real-trace, and periodicity lemmas in
`research/r073c_monodromy_proof.md`.

The package does not prove root uniqueness, algebraic simplicity,
vanishing-viscosity persistence, nonautonomous transfer, a nonlinear
Navier--Stokes estimate, or the Clay problem.

## Reproduction

Create an external dependency directory and install `requirements.txt`.
Then run the commands in `command.txt` from the repository root.  All
production runs are deterministic, use no random numbers, and force the
finite linear-algebra path to one thread.

`progress.ndjson` is the joined deterministic monitor log.  The two primary
interval runs also keep their own per-partition progress logs.  Files prefixed
`canonical_` remove machine-local paths and wall-time presentation fields;
the formal manifest and certificate bind those normalized proof objects.
Original producer JSON and progress logs remain as local audit/telemetry and
are deliberately excluded from the formal `SHA256SUMS` scope.
