# R0.74A localized K_D finite arithmetic certificate

**Status:** `PASS`

**Scope:** `FINITE_ARITHMETIC_CROSS_CHECK_ONLY`

This report checks exact rational exponents with Python `Fraction`. It does not check analytic quantifiers, Gaussian kernel estimates, measurability, or the suitable-weak passage. Those remain the responsibility of the main proof.

## Scaling ledger

| Item | Exponent / degree | Expected |
|---|---:|---:|
| K_D Navier--Stokes scaling | 0 | 0 |
| K_D amplitude degree | 3 | 3 |
| A_c scaling | 0 | 0 |
| B_c scaling | 0 | 0 |
| U_ext scaling | 0 | 0 |
| D_ext scaling | 0 | 0 |
| cc=A_c^(1/2) B_c | 0 | 0 |
| ce=B_c U_ext^(1/2) | 0 | 0 |
| ec=A_c^(1/2) D_ext | 0 | 0 |
| ee=U_ext^(1/2) D_ext | 0 | 0 |

## Scale-integration exponents

| Block | Theta exponent |
|---|---:|
| cc | 1/4 |
| ce | 1 |
| ec | 1/4 |
| ee | 1 |

## Function-level obstruction ledgers

For the spatial packet, the amplitude exponent is fixed by `epsilon=N^(-2/3)`.

| Packet item | N exponent |
|---|---:|
| epsilon | -2/3 |
| K_D | 0 |
| old_L3_tail | -2 |
| gradient_energy | 2/3 |

For the time spike, the amplitude is `delta^(-1/3)`.

| Time-spike item | Delta exponent |
|---|---:|
| amplitude | -1/3 |
| L3_time | 0 |
| Linf_L2 | -2/3 |

## Alias check

`D_ext` is the certificate alias for `G_{nabla,ext}^{1,square}`. Both use the coefficient map `nu^1 R^(-1) dt^1 |grad u|^2`, so the alias is consistent with the analytic definition.

## Result

All 21 finite arithmetic checks pass.

## Boundary

- Analytic quantifiers and inequalities are not machine-certified here.
- This certificate does not establish smallness, absorption, compactness, lower semicontinuity, or regularity.
- `NOT CLAY`.
