# R0.74S boundary-mismatch clock certificate report

## Result

**PASS** — 14/14 exact rational checks, 4/4 finite ledgers, and 38/38 structural checks passed.

## Exact rational and exponent ledger

| Check | Left | Right | Margin |
|---|---:|---:|---:|
| collar_half_width | 1/8 | 1/8 | 0/1 |
| two_collar_total_width | 1/4 | 1/4 | 0/1 |
| minimum_inner_radius | 15/8 | 15/8 | 0/1 |
| annulus_volume_polynomial_m1 | 769/256 | 769/256 | 0/1 |
| holder_conjugacy | 1/1 | 1/1 | 0/1 |
| volume_square_root_shell_power | 1/1 | 1/1 | 0/1 |
| endpoint_shell_power | 2/3 | 2/3 | 0/1 |
| preintegration_gamma_split | 1/2 | 1/2 | 0/1 |
| endpoint_gamma_power | 1/3 | 1/3 | 0/1 |
| endpoint_theta_power | -2/3 | -2/3 | 0/1 |
| coefficient_cube_shell_power | 2/1 | 2/1 | 0/1 |
| coefficient_cube_gamma_power | 1/1 | 1/1 | 0/1 |
| coefficient_cube_theta_power | -2/1 | -2/1 | 0/1 |
| payment_outer_power | 2/3 | 2/3 | 0/1 |

## Finite ledgers

- The exact rational cutoff model checks pointwise \(0\le\beta\le\psi\) and two-collar support on 49 radial samples.
- A nonconsecutive five-shell stopped family checks the maximum-stop
  activation identity against cumulative boundary-clock increments.
- Every subset of six rational exception values with cardinality at
  most three satisfies the squared Cauchy--Schwarz bound.
- All five zero, positive, finite, and infinite branches of the
  composite persistence coefficient satisfy the frozen convention.

## Exponent chain

The certificate checks that a boundary support volume \(2^{2m}R^3\) contributes \(2^m\) after the spatial
square root, then \(2^{2m/3}\gamma_m^{1/3}\) after the
time-persistence step, and finally
\(2^{2m}\gamma_m\Lambda_m^3(\Theta_m^\partial)^{-2}\)
after the shellwise cubic Hölder step.

## Boundary

This finite certificate does not prove the suitable local-energy
identity, periodized support ledger, positivity of the dissipation
measure, or the conditional hypotheses of Theorem 6.1.  It does not
control the root, outer, or weight-drop channels.

**FINITE ONLY. NOT CLAY.**
