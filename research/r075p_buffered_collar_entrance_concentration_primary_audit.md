# R0.75P primary analytic audit

## Audit object

- Main note: `research/r075p_buffered_collar_entrance_concentration.md`
- Audit type: geometry, local energy, exponent, and claim-boundary audit
- Verdict: **PASS**
- Mathematical blocker count: **0**
- Release blocker count: **0**

The finite certificate will bind the final main-note SHA-256 after an
independent review. This author-side audit does not authorize publication.

## 1. Canonical geometry audit

The selected R0.75N profile is allowed to contain a fixed plateau
`vartheta=1` on `[-delta_0,delta_0]`. For transverse radius
`q=|y|/R<=a-2delta_0`, the plateau's two `x_1` components have total
length

\[
 2R\left[
 \sqrt{(a+\delta_0)^2-q^2}
 -\sqrt{(a-\delta_0)^2-q^2}\right].
\]

The bracket is increasing for `q>=0` and equals `2delta_0` at zero, so
the fibre length is at least `4delta_0R`. The proof uses this as a lower
bound only.

The entrance cutoff is supported at transverse radius
`(a-3delta_0)R`. A translation of size at most `delta_0R` therefore keeps
its support in the fibre-safe disk of radius `(a-2delta_0)R`. Its area is
at most `pi*a^2*R^2`, and the fixed `R`-scale transition gives
`||Delta phi_0||_infinity<=C_phi R^(-2)`.

## 2. Moving local-energy audit

For

\[
 \partial_tF+B\partial_2F-\Delta_yF=0,
 \qquad
 \phi_t(x_2,x_3)=\phi_0(x_2-Bt,x_3),
\]

one has `partial_t phi_t+B partial_2 phi_t=0`. Direct periodic integration
by parts gives

\[
 \frac d{dt}\int\phi_t|F|^2
 =\int\Delta_y\phi_t|F|^2
 -2\int\phi_t|\nabla_yF|^2.
\]

The finite total-frequency cap `n^2+j^2<=4K^2` is invariant under the
constant-shear heat evolution and implies

\[
 \|\nabla_yF(t)\|_2^2\le4K^2E_0.
\]

Therefore the lower derivative bound is
`E_phi'>=-(8K^2+C_phi R^(-2))E_0`. The frozen
`K>=R^(-3/2)`, `R<=1` gives `R^(-2)<=K^2`, so P.18 follows.

With

\[
 \tau=c_0\mu K^{-2},
 \qquad
 c_0\le[2(8+C_\phi)]^{-1},
\]

the energy loss is at most `mu E_0/2`. The additional choice
`c_0<=delta_0/C_B` and the inequalities
`|B|<=C_BR^(-2)`, `K^(-2)<=R^3` give
`|B|tau<=delta_0R`. Finally `K^2T>=1` implies `tau<=T` because
`c_0*mu<=1`.

## 3. Cubic lower-bound audit

On the transported support,

\[
 \int|F|^3\ge V_\phi^{-1/2}
 \left(\int|F|^2\right)^{3/2}
 \ge(\sqrt\pi aR)^{-1}
 \left(\frac\mu2E_0\right)^{3/2}.
\]

Multiplication by the fibre length `4delta_0R` cancels the remaining
`R^(-1)`. Integration for `tau=c_0mu K^(-2)` gives

\[
 M_{K,\rm col}\ge
 \frac{\sqrt2\,\delta_0c_0}{\sqrt\pi}
 a^{-1}\mu^{5/2}K^{-2}E_0^{3/2}.
\]

Thus `c_*` in P.23 and the inverse powers
`a^(2/3)mu^(-5/3)K^(4/3)` in P.24 are correct. No inverse heat flow or
observability inequality occurs.

## 4. Flux and normalization audit

R0.75O supplies

\[
 |\mathcal T|
 \le\frac{|B|\mathcal W_\infty}{4K^2}E_0,
\]

while R0.75N supplies `mathcal W_infty<=C_vartheta a`. Combining with
P.24 gives exactly

\[
 |\mathcal T|
 \le C|B|a^{5/3}\mu^{-5/3}K^{-2/3}
 M_{K,\rm col}^{2/3}.
\]

For `p_col=R^(-2)omega M_col` and
`X=(omega/R)[T]_+`, the conversion contributes
`R^(1/3)omega^(1/3)`. Paying `|B|<=C_BR^(-2)` and
`K^(-2/3)<=R` leaves

\[
 C L^{5/3}\mu^{-5/3}R^{-2/3}\omega^{1/3}.
\]

If `mu>=c_mu R^sigma`, its exponential rate is

\[
 \frac\rho6-\frac{c_\gamma}{12}
 +\frac{5\sigma\rho}{12}.
\]

The strict negativity threshold is

\[
 \sigma<\frac15\left(\frac{c_\gamma}{\rho}-2\right)
 =\frac{8558}{178605}.
\]

At equality the polynomial `L^(5/3)` remains unbounded. The strict
endpoint in P.5 is therefore necessary for this estimate.

## 5. Payment and boundary audit

- The full flux window and `[0,tau]` are explicitly placed inside the
  frozen `I_(2R)` measurement interval.
- The spatial variables are explicitly the Version-M translated
  coordinates, and inclusion of the plateau shell in the selected
  outer-collar cover is an explicit ledger-alignment hypothesis.
- P.31 separately assumes that `F` is an actual coordinate component of
  the same smooth velocity measured by `P_R^M` on that aligned tube. It is
  not a Littlewood--Paley or Fourier projection of a larger component.
- The plateau shell is then a subset of the canonical outer collar. Its worst
  scale-`2R` weight is `omega`; the inward side has no worse weight.
- Since the total velocity magnitude dominates `|F|`, the nonnegative
  Version-M exterior cubic row gives `p_col<=C P_R^M`.
- This is only a nonnegative-ledger inclusion. The note does not claim that
  every constant-shear packet realizes the frozen inversion-paired
  zero-trajectory solution family.
- No pointwise domination is asserted for a frequency projection of a
  larger field; that route remains open with inter-packet summation.
- The conclusion applies only when the entrance concentration P.5 holds.
  No claim is made that every packet satisfies it.
- The spatially spread example diagnoses failure of the sufficient
  hypothesis, not failure of the signed target.
- Constant shear, one finite total-frequency-capped packet, and the
  canonical cutoff remain essential.
- The low-concentration branch, nonconstant shear, packet summation, low
  differences, arbitrary-field E.24, complete clock, fixed deletion,
  suitable-weak transfer, regularity, and singularity remain open.
- No completeness, novelty, or priority claim is made. **NOT CLAY.**

## Audit conclusion

The geometry, time scale, energy direction, cubic powers, exact
concentration threshold, conditional Version-M ledger inclusion, and
open-claim boundary are internally consistent. The draft is ready for
independent mathematical audit and finite-certificate construction.
