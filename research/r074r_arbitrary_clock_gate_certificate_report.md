# R0.74R arbitrary-clock gate certificate report

## Result

**PASS** — 13/13 exact rational checks, 3/3 exponent ledgers, and 25/25 structural checks passed.

## Exact rational checks

| Check | Left | Relation | Right | Margin |
|---|---:|:---:|---:|---:|
| `primary_half_split` | `1/2` | `==` | `1/2` | `0/1` |
| `secondary_half_split` | `1/4` | `==` | `1/4` | `0/1` |
| `triage_fraction_sum` | `1/1` | `==` | `1/1` | `0/1` |
| `holder_conjugacy` | `1/1` | `==` | `1/1` | `0/1` |
| `endpoint_gamma_after_substitution` | `1/3` | `==` | `1/3` | `0/1` |
| `endpoint_R_after_substitution` | `4/3` | `==` | `4/3` | `0/1` |
| `raised_gamma_power` | `1/2` | `==` | `1/2` | `0/1` |
| `raised_R_power` | `2/1` | `==` | `2/1` | `0/1` |
| `cutoff_power_after_raise` | `3/2` | `==` | `3/2` | `0/1` |
| `persistence_theta_power` | `-2/3` | `==` | `-2/3` | `0/1` |
| `coefficient_cube_gamma` | `1/1` | `==` | `1/1` | `0/1` |
| `coefficient_cube_theta` | `-2/1` | `==` | `-2/1` | `0/1` |
| `payment_outer_power` | `2/3` | `==` | `2/3` | `0/1` |

## Power ledger

The JSON checks the complete exponent chain

\[
 e_k^{\eta}(t)
 \lesssim2^kR^{4/3}\gamma_k^{1/3}g_k(t)^{2/3},
\]

\[
 e_k^{\eta}(\tau)
 \lesssim2^k\gamma_k^{1/3}(\Theta_k^{\eta})^{-2/3}(p_k^{\eta})^{2/3},
\]

and the cubed coefficient
\(2^{3k}\gamma_k\Lambda_k^3(\Theta_k^{\eta})^{-2}\).

## Boundary

This finite certificate verifies rational constants, exponent
bookkeeping, tags, and fail-closed claim sentinels.  It does not
prove the local-energy identities, the inherited payment bound,
the conditional hypotheses (R.216)--(R.217), or any PDE extraction
theorem.  The no-go fields are not Navier--Stokes solutions.

**FINITE ONLY. NOT CLAY.**
