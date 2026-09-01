# R0.73Y formal figure QA report

Status: **PASS**

- generated at UTC: `2026-09-01T06:20:51.257937+00:00`
- frozen formula-source commit: `1ecc6fe20a921db9d0876dbd4484a3aa4ca7ec66`
- exact inventory target: 25 files = 10 source + 11 raw/result + 4 metadata
- deterministic-core regeneration: PASS, `18` hashes unchanged
- runtime/source/inventory negative tests: PASS
- formula identity maximum discrepancy: `1.110e-16`
- exact-statistic maximum discrepancy: `5.551e-17`
- minimum audited covariance: `4.5279585030313617e-03`
- PDF-versus-PNG QA mean absolute RGB difference: `5.804056`
- render wall time: `0.739420` seconds
- render CPU time: `0.735928` seconds

## Visual QA

The 178 mm final-size render, exact grayscale conversion, and independent PDF render were inspected. Titles, panel markers, axes, legends, formula, non-DNS label, footer, and research blossom are legible. No clipping or collision was accepted. Line styles remain distinct in grayscale.

## Scope

The package visualizes an analytic exact witness and a production-only coercivity obstruction. It is not DNS, not a turbulence-closure validation, and not a solution of the Navier-Stokes existence-and-smoothness problem.

## Nondeterministic observability

UTC timestamps, process IDs, wall/CPU timing, resource observations, environment observations, sealing records, and checksums that depend on them are explicitly outside the deterministic core. Their values are preserved for audit rather than compared across regenerations.
