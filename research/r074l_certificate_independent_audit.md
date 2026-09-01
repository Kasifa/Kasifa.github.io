# R0.74L — independent finite-certificate audit

## Status

I independently reconstructed the exact rational arithmetic in
`r074l_main_collar_certificate.json`.  The reconstruction passed all 24
certificate checks.  I found no discrepancy.

This is a **FINITE** result.  It verifies constants, thresholds, signed
margins, and the final scale ledger.  It is not an independent proof of any
stochastic, geometric, or analytic lemma in the R0.74L note.  **NOT CLAY.**

## Independence and binding

The independent implementation is
`scripts/r074l_main_collar_certificate_independent.rb`.  It uses Ruby
`Rational` arithmetic and the formulas displayed in
`r074l_forward_bridge_bv_reduction.md`.  It neither invokes nor imports the
primary Python generator.  I did not use the Python implementation when
constructing the formulas below.

The audited files are bound by these hashes:

- certificate JSON SHA-256:
  `252808d60f90343e3a9d614f0ae11003984498d2362e05f9441d53175bcafd7e`;
- independent Ruby verifier SHA-256:
  `39196aa8741a62863094c34c49f51e7a5c4146a0526d1657cb3482d3f8883619`.

The verifier contains the certificate hash as a required value.  A byte
change to the audited JSON therefore makes this reconstruction fail until a
new independent audit is performed.

## Primitive inputs

The reconstruction begins only from

\[
 \lambda=\frac{63}{32},\qquad
 c_h=\frac{15}{16},\qquad
 \rho=\frac1{320},\qquad
 j_0=14,
\]

and

\[
 \frac1{128}\le BR^2\le\frac1{64}.
\]

The verifier first checks that the JSON input block contains exactly these
values.  Derived fields are not used as inputs.

## Exact reconstruction

### Transition-distance and bad-path exponent

The first scale at the frozen threshold is

\[
 L_{14}=\lambda 2^{14}=32256.
\]

The distance-reserve condition $64\le c_hL/256$ requires

\[
 L\ge \frac{64\cdot256}{c_h}
   =\frac{262144}{15}.
\]

Its exact margin at $L_{14}$ is

\[
 32256-\frac{262144}{15}=\frac{221696}{15}>0.
\]

With total Brownian duration $66R^2$, the reflection exponent is

\[
 A=\frac{(255/256)^2c_h^2}{4\cdot66}
  =\frac{4876875}{1476395008}.
\]

The reserve over $R=e^{-\rho L^2}$ is

\[
 A-\rho
 =\frac{1315703}{7381975040}>0.
\]

### Heat-tail arithmetic

The dimensionless heat-tail argument is

\[
 x=\frac{(32R)^2}{4(65R^2)}=\frac{256}{65}.
\]

Its fourth Taylor partial sum is reconstructed exactly as

\[
 \sum_{k=0}^{4}\frac{x^k}{k!}
 =\frac{587309569}{17850625}
 =32+\frac{16089569}{17850625}>32.
\]

This audit verifies only this finite inequality.  The use of the exponential
series and the heat-tail estimate belongs to the analytic proof.

### Positive-clock support and modulus exponent

The upper calibration gives

\[
 |J|\le65BR^2\le\frac{65}{64}<2,
 \qquad 2-\frac{65}{64}=\frac{63}{64}.
\]

The outer-radius coefficient is $2/\lambda=64/63$.  Adding the stated
padding $1/63$ gives

\[
 C_{\rm pr}=\frac{65}{63},
 \qquad 2C_{\rm pr}=\frac{130}{63}.
\]

Since $B^{-1}\le128R^2$, the physical-duration coefficient is

\[
 \frac43\cdot\frac{130}{63}\cdot128
 =\frac{66560}{189}.
\]

For displacement $R/16$ and generator $\partial_x^2$, the reconstructed
reflection exponent coefficient is

\[
 \frac{1}{16^2\cdot4}\,
 \frac{189}{66560}
 =\frac{189}{68157440}>0.
\]

### Scale ledger

The good-path powers are reconstructed from

\[
 R^6\,R^2\,R^{-1}\,R^{-3}\,(LR)=LR^5.
\]

The bad-path powers are reconstructed from

\[
 R^6\,R^{-1}\,L\,R^{-3}\,R^2\,R=LR^5.
\]

Thus both ledgers have $L$-power $1$ and $R$-power $5$.

## Check-by-check result

| ID | Independently reconstructed relation | Result |
|---|---:|:---:|
| `lambda` | $63/32=63/32$ | PASS |
| `center_height` | $15/16=15/16$ | PASS |
| `radius_exponent` | $1/320=1/320$ | PASS |
| `L14` | $32256=32256$ | PASS |
| `L14_beats_distance_threshold` | $32256\ge262144/15$ | PASS |
| `bad_exponent_A` | $A=4876875/1476395008$ | PASS |
| `bad_exponent_reserve` | $A-\rho=1315703/7381975040$ | PASS |
| `bad_exponent_reserve_positive` | $1315703/7381975040>0$ | PASS |
| `heat_tail_argument` | $x=256/65$ | PASS |
| `taylor4` | $T_4(x)=587309569/17850625$ | PASS |
| `taylor4_beats_32` | $T_4(x)>32$ | PASS |
| `B_R2_lower` | $1/128=1/128$ | PASS |
| `B_R2_upper` | $1/64=1/64$ | PASS |
| `clock_length_upper` | $65/64=65/64$ | PASS |
| `clock_length_below_two` | $65/64<2$ | PASS |
| `projection_radius` | $65/63=65/63$ | PASS |
| `component_length_coefficient` | $130/63=130/63$ | PASS |
| `physical_duration_coefficient` | $66560/189=66560/189$ | PASS |
| `modulus_exponent_coefficient` | $189/68157440=189/68157440$ | PASS |
| `modulus_exponent_positive` | $189/68157440>0$ | PASS |
| `good_R_power` | $5=5$ | PASS |
| `good_L_power` | $1=1$ | PASS |
| `bad_R_power` | $5=5$ | PASS |
| `bad_L_power` | $1=1$ | PASS |

For every row, the verifier also checks the stored relation symbol, exact
signed margin, Boolean `pass` field, and presence of a nonempty note.  It
checks the nine-value `derived` block, the 24/24 summary, the schema, scope,
status flags, and six-item analytic boundary.

## Reproduction

The audit was run locally with Ruby 2.6.10:

```sh
ruby scripts/r074l_main_collar_certificate_independent.rb
```

The command exited with status $0$ and reported

```text
RESULT: PASS (24/24 checks)
ANALYTIC BOUNDARY: finite arithmetic only; no analytic lemma is certified.
```

## Strict analytic boundary

This independent certificate audit does **not** prove:

1. the normalized-bridge reversal identity;
2. any reflection-principle or stopping-time claim;
3. the thickened-slice BV geometry;
4. the short-clock occupation lemma;
5. the nearest inward collar or the full signed packet condition;
6. a universal endpoint estimate, regularity, singularity, or the Clay
   problem.

Those statements require separate analytic review.  Passing this audit means
only that the frozen finite constants and power ledger have been independently
reconstructed without discrepancy.
