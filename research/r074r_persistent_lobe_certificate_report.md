# R0.74R terminal-window lobe certificate report

## Result

**PASS** — 21/21 exact arithmetic checks and 22/22 structural checks passed.

## Exact arithmetic

| Check | Left | Relation | Right | Margin |
|---|---:|:---:|---:|---:|
| `weight_chart_identity` | `1/128` | `==` | `1/128` | `0/1` |
| `previous_shell_weight_exponent` | `1/512` | `==` | `1/512` | `0/1` |
| `kappa_1_exact` | `-769/1905120` | `==` | `-769/1905120` | `0/1` |
| `kappa_1_negative` | `-769/1905120` | `<` | `0/1` | `769/1905120` |
| `kappa_2_exact` | `8831/1905120` | `==` | `8831/1905120` | `0/1` |
| `kappa_2_positive` | `8831/1905120` | `>` | `0/1` | `8831/1905120` |
| `adjacent_reciprocal_weight_rate` | `20/1323` | `==` | `20/1323` | `0/1` |
| `tail_minimum_rate` | `80/1323` | `==` | `80/1323` | `0/1` |
| `j2_base_L` | `63/8` | `==` | `63/8` | `0/1` |
| `j2_tail_exponent` | `15/4` | `==` | `15/4` | `0/1` |
| `exp_linear_ratio_majorant` | `8/19` | `<` | `1/2` | `3/38` |
| `lobe_volume_fraction` | `1/16` | `==` | `1/16` | `0/1` |
| `averaged_energy_mass_factor` | `2/1` | `==` | `2/1` | `0/1` |
| `spacetime_lobe_R_power` | `6/1` | `==` | `6/1` | `0/1` |
| `normalized_payment_prefactor` | `1/4` | `==` | `1/4` | `0/1` |
| `cubic_coefficient_squared` | `8/1` | `==` | `8/1` | `0/1` |
| `cubic_two_thirds_factor` | `8/1` | `==` | `8/1` | `0/1` |
| `tail_prefactor_cubed` | `4/1` | `==` | `4/1` | `0/1` |
| `pointwise_floor_energy_constant` | `1/32` | `==` | `1/32` | `0/1` |
| `pointwise_corollary_constant_squared` | `1/4096` | `==` | `1/4096` | `0/1` |
| `gamma_previous_power` | `1/4` | `==` | `1/4` | `0/1` |

The exponent vector in the JSON separately verifies

\[
 (2R)^{-2}\Gamma^{1/4}
 \frac{(2R^4\Gamma^{-1}E)^{3/2}}
 {(LR^6/16)^{1/2}}
 =2\sqrt2\,R\Gamma^{-5/4}L^{-1/2}E^{3/2}.
\]

The tail-ratio threshold uses only the exact implication
\(e^x\ge1+x\): for \(j\ge2\), the minimal tail exponent
is \(15/4\), hence the adjacent reciprocal-weight ratio is at
most \(2/(1+15/4)=8/19<1/2\).

## Structural boundary

All 22 tag, sentinel, delimiter, and claim-boundary checks pass.
The certificate does not prove lobe placement, window-mass extraction, the
nonnegative payment-row inclusion, or any PDE extraction theorem.
It does not prove signed flux, the full square-function upper bound,
the fixed-scale inequality, regularity, blow-up, or any Clay claim.

**FINITE ONLY. NOT CLAY.**
