# R0.74M — independent finite-certificate audit

## Status

I independently reconstructed the exact rational arithmetic in
`r074m_nearest_inward_certificate.json`.  The Ruby reconstruction returns

```text
RESULT: PASS (38/38 checks)
PASS 38/38
```

I found no mathematical-arithmetic or schema discrepancy in the finite
certificate.  This is a **FINITE** result: it verifies the frozen constants,
monotone thresholds, signed margins, scale powers, field inventories, status
flags, and analytic boundary.  It is not an independent proof of the
stochastic, heat-kernel, support, or expulsion lemmas.  **NOT CLAY.**

## Independence and binding

The independent verifier is
`scripts/r074m_nearest_inward_certificate_independent.rb`.  It uses Ruby
`Rational` arithmetic.  It does not invoke or import the Python generator.
Only the primitive input block is read before the reconstruction; no value in
the JSON `derived` or `checks` blocks is used as an input to another derived
quantity.

The audited artifacts are bound by these hashes:

- certificate JSON SHA-256:
  `5aed76e6c2aac58c1507784dd014a132560967a1bb89e69080fa0e170f65462f`;
- independent Ruby verifier SHA-256:
  `8a13a8268ed0e8ec1824df10102d48eef2246820594805e8f9e20118b00b2a5f`.

The verifier contains the expected certificate hash and fails closed if any
byte in that JSON changes.

## Primitive inputs

The reconstruction first verifies the exact input-field inventory and then
freezes

\[
 \lambda=\frac{63}{32},\qquad
 c_h=\frac{15}{16},\qquad
 \rho=\frac1{320},\qquad
 G_1=\frac2{1323},
\]

\[
 c_{\rm def}=\frac1{640},\qquad
 a=\frac{49}{14625},\qquad
 j_0=13,\qquad L_0=9216.
\]

These are the only JSON values admitted as primitive mathematical inputs.

## Exact reconstruction

### Discrete scale and inward geometry

The first inherited scale is

\[
 L_{13}=\lambda2^{13}=16128\ge9216.
\]

The unpadded outer coefficient of the nearest inward collar is

\[
 \lambda^{-1}=\frac{32}{63}.
\]

After allowing final-segment Brownian motion of size (LR/16), the exact
room inside the (3LR/5) heat-defect window is

\[
 \frac35-\frac{32}{63}-\frac1{16}
 =\frac{149}{5040}>0.
\]

For a final segment of length (R^2/64), the reconstructed reflection
exponent is

\[
 \frac{(1/16)^2}{4(1/64)}=\frac1{16}.
\]

### Heat-defect threshold

The lower dimensionless heat time is

\[
 61-\frac1{64}=\frac{3903}{64},
 \qquad
 \frac1{4(3903/64)}=\frac{16}{3903}.
\]

The exponent comparison is reconstructed as

\[
 \frac{L^2}{640}
 -\frac{16}{3903}\left(\frac35L+64\right)^2
 =\frac{361}{4163200}L^2
 -\frac{2048}{6505}L-\frac{65536}{3903}.
\]

At (L_0=9216), its value and derivative are

\[
 \frac{433872896}{97575}>0,
 \qquad
 \frac{41744}{32525}>0.
\]

The positive leading coefficient and positive derivative at (L_0) verify
the stored monotone-threshold arithmetic for every (L\ge L_0).  This finite
calculation does not prove the heat-kernel lower bound that motivates it.

### Displacement payments

The two exact exponent gaps are

\[
 a-c_{\rm def}=\frac{3347}{1872000}>0,
 \qquad
 \rho-c_{\rm def}=\frac1{640}>0.
\]

Using only the frozen bounds (BR^2\in[1/128,1/64]), (t\le65R^2), and
the final segment (R^2/64), the negative plateau coefficient is

\[
 4\cdot65\cdot\frac1{64}=\frac{65}{16}.
\]

The retained positive contribution is

\[
 \frac12\cdot\frac1{128}\cdot\frac1{64}
 =\frac1{16384}.
\]

Reserving half after absorption gives

\[
 \Sigma_L=\frac1{32768}e^{-L^2/640},
\]

so the reconstructed absorption coefficient is

\[
 \frac{65}{16}\,32768=133120.
\]

At (L_0), the elementary lower bound (e^z\ge z^2/2) yields the exact
stored comparison

\[
 \frac{30447128153161728}{2640625}>133120.
\]

For (L\ge63/8), the (R/8) padding costs at most (LR/63).  Hence

\[
 \frac{32}{63}+\frac1{63}=\frac{11}{21},
 \qquad 4\frac{11}{21}=\frac{44}{21}.
\]

The second (e^x\ge x^2/2) comparison at (L_0) reconstructs

\[
 \frac{220150628352}{25}
 >\frac{4429185024}{7},
\]

with exact positive margin (1430324772864/175).

### Exponent reserves and scale ledger

The bad-event reserve is

\[
 \frac1{16}-\frac1{320}-\frac2{1323}
 =\frac{24497}{423360}>0.
\]

The good-event super-Gaussian rate and prefactor denominator are

\[
 2(\rho-c_{\rm def})=\frac1{320}>0,
 \qquad 32768^2=1073741824.
\]

The raw bad-path ledger is

\[
 R^6R^2R^{-1}L R^{-3}=LR^4,
\]

before the bad-event exponential pays one additional (R).  The raw
good-path ledger is

\[
 R^6R^2R^{-1}L R^{-4}=LR^3,
\]

before the derivative-kernel tail pays (R^2).  Thus the reconstructed
stored powers are respectively ((L^1,R^4)) and ((L^1,R^3)).

## Check-by-check result

| Group | Check IDs | Result |
|---|---|:---:|
| Primitive constants | `lambda`, `center_height`, `radius_exponent`, `weight_gap_G1` | PASS 4/4 |
| Discrete threshold | `L13`, `L13_beats_heat_threshold` | PASS 2/2 |
| Geometry and final segment | `outer_coefficient`, `geometry_gap`, `geometry_gap_positive`, `final_segment_length`, `reflection_exponent` | PASS 5/5 |
| Heat comparison | `heat_time_lower`, `heat_exponent_multiplier`, `heat_margin_quadratic`, `heat_margin_linear`, `heat_margin_constant`, `heat_margin_at_L0`, `heat_margin_at_L0_positive`, `heat_margin_derivative_at_L0`, `heat_margin_derivative_positive` | PASS 9/9 |
| Displacement gaps | `plateau_gap`, `plateau_gap_positive`, `expulsion_gap`, `expulsion_gap_positive` | PASS 4/4 |
| Finite absorption | `negative_absorption_required`, `plateau_exp_lower`, `radius_coefficient_upper`, `four_radius_coefficient`, `expulsion_exp_lower` | PASS 5/5 |
| Bad/good exponent reserves | `bad_event_gap`, `bad_event_gap_positive`, `super_rate`, `super_rate_positive`, `sigma_square_denominator` | PASS 5/5 |
| Scale powers | `bad_R_power`, `bad_L_power`, `good_R_power`, `good_L_power` | PASS 4/4 |
| **Total** | all distinct checks in frozen order | **PASS 38/38** |

For every row, the verifier also checks the exact seven-field inventory,
ID and order, left and right rational values, relation symbol, signed margin,
Boolean `pass`, and exact note.  It separately checks all 11 `derived` fields,
the 38/38 summary, result, schema, scope, four status flags, six-item analytic
boundary, and the certificate SHA-256.

## Reproduction

The audit was run locally with Ruby 2.6.10:

```sh
ruby scripts/r074m_nearest_inward_certificate_independent.rb
```

The command exited with status (0) and reported `PASS 38/38`.

## Strict analytic boundary

This independent finite audit does **not** prove:

1. the normalized bridge or common-forward-law identity;
2. the Brownian reflection estimate;
3. heat-kernel positivity or the periodic Gaussian tail;
4. the support-conditioned displacement lemma;
5. every shell row or the full R0.74K signed collar condition;
6. a universal endpoint estimate, regularity, singularity, or the Clay
   problem.

Those claims require separate analytic review.  The present result says only
that the frozen finite constants, thresholds, metadata boundaries, and power
ledger have been independently reconstructed without discrepancy.
