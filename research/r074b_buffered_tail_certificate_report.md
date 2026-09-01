# R0.74B buffered-tail derived finite certificate

**Status:** PASS

**Scope:** `FINITE_DERIVED_EXACT_ARITHMETIC_ONLY`

Every executable actual value below is derived from primitive exponents, interval endpoints, or file bytes before comparison with its declared target. The certificate contains no literal `pass=True` annular/core rows.

## Frozen provenance

- Analytic source SHA256: `bec0a239b3c5d145238c9f06c734661f2e85e8cb339f594e8350c4c111bc87ab`
- Independent audit SHA256: `1af75d494e2b7389adc97836dc3efd1e34a3b95b066e9c4ba54414eaf38b269e`
- Literature audit SHA256: `fe33cc76da4cc5a40b955a0a54b35934da75ad70e346956ff2c7a184ef6dac81`
- Certificate script SHA256: `26c0c6b73253befc6e9f1f6256d92c0847e2eb7c418b7b3e81fee3088612955e`
- External freeze-manifest SHA256: `a6bed470ee1ccaf092e50d28b0c464e830499e6b3de5af7d333acac1039e21e1`
- The external manifest freezes the source, audit, literature-audit, and script hashes. The source SHA embedded in the independent audit must also equal the current analytic source SHA.
- The manifest cannot freeze its own bytes without circularity; its immutability is a version-control and frozen-commit review boundary.

## NSE scaling

| Quantity | Derived exponent |
|---|---:|
| standard_clock | -2 |
| viscosity_clock | -2 |
| U_ext | 0 |
| D_ext | 0 |
| E_endpoint | 0 |
| E_gradient | 0 |
| G_u | 0 |
| G_p | 0 |
| Lambda_R | 2 |
| H_u | 0 |

## Annular and core geometry

The three relative neighbor offsets `-1,0,1` are checked by endpoint equality against the corresponding doubled-radius offsets `-2,-1,0`. Their payment-to-target Gaussian exponent ratios are exactly `1/16,1/4,1`.

The cutoff supports are computed as `[2^m-1/8, 2^(m+1)+1/8]R`. Both `m=1` and `m=2` intersect `B_(4R)` and their exterior portions lie in `A_1(2R) union A_2(2R)`; the `m=3` boundary row is already outside the core.

The finite summability boundary gives delta `6` at `m=4`; the exact truncated exponential lower bound is `1+6+18=25>16`, sufficient for the analytic ratio bound below `1/2`. The infinite-tail quantifier remains analytic.

## Amplitude composition

| Item | Derived degree |
|---|---:|
| E | 2 |
| E^(3/2) | 3 |
| Lambda_R | 2 |
| H_u | 3 |
| G_u | 3 |
| G_p | 3 |
| K_D | 3 |
| A_ext | 3 |
| P | 3 |
| P^(2/3) | 2 |
| (P^(2/3))^(3/2) | 3 |
| P^(3/2) | 9/2 |

## Pressure, clocks, and exact-shear exponent ledger

The Lambda first-shell coefficient and R power are derived as `(1/16,-3)`; every sampled outer Lambda ratio is derived as `1/2`; the Gaussian pressure/velocity normalization is `4`; and the gauge-volume row derives `-2+3=1` before time and pressure scaling return the NSE exponent to zero.

Sparse exact polynomials in the viscosity exponent derive the clock factors from `(kappa+nu) kappa^(-1/3)`: `1+nu` for the standard clock and `2 nu^(2/3)` for the viscosity clock.

The shear ledger derives endpoint, gradient-density, decay-time, dissipation, cubic, and harmonic frequency exponents from `grad u:N^1` and `integral exp(-c nu N^2 t)dt:N^-2`. Exact solvability and positive Riemann-Lebesgue limits remain analytic.

## Result

All 67 derived finite checks pass. The field-level coverage manifest accounts for 89 displayed subject fields plus its own meta-check, and the external hash gates pass.

## Analytic boundary

- periodized suitable test admissibility.
- finite-M to infinite-shell limit.
- uniform-theta infinite summability.
- weighted Holder inequality.
- Calderon-Zygmund and harmonic pressure estimates.
- gauge transfer inequality.
- exact NSE status and Riemann-Lebesgue positive limits for the shear.
- Removal of the `+P` term for large `P` remains OPEN.
- No absorption, epsilon regularity, or global regularity follows.
- NOT CLAY.
