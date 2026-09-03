# R0.74S recurrent-tail formal figure QA report

Status: **PASS**

- generated at UTC: `2026-09-02T23:40:42.081698+00:00`
- frozen mathematical core: `7355c01dead23c3524242006318b02a8324447e6`
- figure-source seal: `e70db2c5da131d05500e1399df1299c25c78886c`
- exact inventory: 25 files = 10 source + 11 raw/result + 4 metadata
- deterministic-core regeneration: PASS, `18` hashes unchanged
- validation checks: `42` passed
- orbit period: `8.626062589998575`
- period quadrature discrepancy: `8.882e-15`
- RK4 closure error: `3.454e-14`
- maximum streamline-level residual: `4.052e-15`
- one-period absolute variation: `2.000000000000007`
- signed one-period drift: `5.551e-17`
- PDF-versus-PNG mean absolute RGB difference: `4.019735`
- render wall time: `1.096563` seconds
- render CPU time: `1.018097` seconds

## Visual QA

The 178 mm final-size image, grayscale conversion, and independent PDF render were inspected.  The four panel titles, markers, axes, legends, dual-axis labels, scope badge, footer, and top-right research blossom are legible.  No clipping or collision was accepted.  Line styles and marker shapes preserve the comparisons in grayscale.

## Scope

This package is an analytic-exact construction with deterministic numerical rendering of the orbit-time parametrization.  It is not DNS, not a PDE simulation, not a proof of the open estimate (S.472), and not a solution of the Navier--Stokes Millennium problem.
