# R0.72G certificate package

This package contains the two deterministic finite audits used in R0.72G.

- `result.json` and `producer-roots.csv` come from the real invariant
  lattice RK4 producer.
- `independent-result.json` and `independent-roots.csv` come from the
  Fourier-angle Strang split-step audit.
- Each route owns separate progress and resource NDJSON logs.
- The two `attempt1-failed-*` groups preserve the first failed validation
  attempts and the exact evidence that caused the reruns.

Both passing JSON files report `allRequiredChecksPassed: true`.  Their common
root counts agree exactly, and their complete masses agree within
`9.18e-7` relative on `R=8,12,16,24,32`.  The producer extends to `R=64`
and includes largest-radius, step, and horizon pressure.

The finite calculations are not interval arithmetic.  They detect resolved
sign-changing roots on finite lattices and finite windows.  The analytic
complete-root theorem is in `research/r072g_report-source.md`; it does not
come from numerical root enumeration.  Machine-readable scope flags rule
out general triangular, arbitrary NSE, continuation, regularity, and
singularity claims.

Use `command.txt` to reproduce both passing runs.  `config.json` records the
shared model and pressure protocol, `environment.txt` records the runtime,
and `SHA256SUMS` seals every file in this directory except itself.
