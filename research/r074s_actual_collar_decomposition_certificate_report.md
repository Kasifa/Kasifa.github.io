# R0.74S actual-collar decomposition certificate report

## Result

**PASS** — 6/6 exact rational checks, 2/2 exhaustive finite checks, and 23/23 structural checks passed.

## Exact rational ledger

| Check | Left | Right | Margin |
|---|---:|---:|---:|
| collar_width | 1/8 | 1/8 | 0/1 |
| two_collar_widths | 1/4 | 1/4 | 0/1 |
| minimum_boundary_spacing | 2/1 | 2/1 | 0/1 |
| minimum_gap_after_collars | 7/4 | 7/4 | 0/1 |
| derivative_scale | 8/1 | 8/1 | 0/1 |
| weight_gap_constant | 3/35 | 3/35 | 0/1 |

## Exhaustive finite ledgers

- The 24 open radial collars through index 12 have no positive
  length overlap after setting \(R=1\).
- All 64 active-shell masks at \(M=6\) satisfy the exact direct
  shell sum, four-channel block decomposition, and internal
  weight-drop plus bridge-mismatch identity.

## Boundary

The certificate does not prove the analytic cutoff derivative,
unfolding, a uniform PDE collar bridge, or a signed depletion
estimate.  It checks rational geometry, finite algebra, tags,
and fail-closed claim sentinels.

**FINITE ONLY. NOT CLAY.**
