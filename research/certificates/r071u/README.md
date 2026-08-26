# R0.71U certificate

This directory archives two separate finite audits for the R0.71U
second-time-jet and exact-recurrence release.

- `result.json` is produced by `research/r071u_exact_audit.py`.  It checks the
  zero-gap kernel, eigenshell atom identity, two-row scaling ledger, exact
  2.5D substitution, forced-path stress test, high-precision response
  matrices, modular isolation, and the corrected full-support R0.71T heat
  derivative.
- `independent-result.json` is produced by
  `research/r071u_independent_audit.py`.  It imports neither the exact producer
  nor its output.  It uses polynomial integration, spectral differentiation,
  SVD, and a fresh direct Fourier-lattice shooting solve with three cutoff
  refinements.

The scripts do not replace the analytic proofs.  In particular, the Hilbert
sampling lemma, the extended-Chebyshev zero count, the finite-dimensional
implicit-function theorem, and the all-shell monotone-convergence step are
proved in `research/r071u_report-source.md`.

The certificate supports a trajectory-wise second-time-jet estimate on
compact classical intervals with a positive enstrophy floor.  It also
supports a separate exact unforced 2.5D NSE construction for each prescribed
finite time set.  It does not produce one trajectory with infinitely many
prescribed returns.  Bounded initial energy and enstrophy rule out a uniform
raw-count bound on that bounded class; the weighted atom may shrink.

No Leray-level payment of the second-time-jet row, weak-solution trace,
continuation criterion, finite-time singularity, global regularity, novelty,
or priority statement is certified.
