# R0.76I primary mathematical audit

## Verdict

- Mathematical verdict: **PASS**
- Mathematical blockers: **0**
- Source-range blockers after correction: **0**
- Claim-boundary blockers: **0**
- Scope: the continuum implication in R0.76I, not an independent proof of
  Zhang Proposition 4.2.

The audit treats Zhang's endpoint theorem as a cited **LITERATURE** input.
Because the cited source is an unrefereed July 2026 arXiv v1 preprint, the
composite R0.76I result remains **CONDITIONAL-LITERATURE**.

## Bound objects

| object | SHA-256 | role |
|---|---|---|
| R0.76I main theorem | `6277cb69dfad94cae89088c6a8c007967bdde97aceee7b19954d10ec53f6efce` | Audited proof. |
| R0.76I source report | `0ee0fbd75f9691e2ac898a57921f8a0574ba9af9ea652f85d0199856d7e3d423` | Imported theorem, version, range, and collision boundary. |
| R0.76E modal-entropy window | `1494cb7e3863ef934f87746412f2a64ef98f78deb5ce81be3cece7d5a7571ca4` | Exact energy identity, onset estimate, and physical conversion. |
| R0.76H full-plateau absorption | `11490112a1893400a1099dd9f45b906ce78d7dab1ebcf549eaa7870241dc0ef4` | Exact shell cross-section and plateau geometry. |

## 1. Endpoint geometry and branch count

The observed interval has half-length

\[
 e_a=1-\frac{\delta_0}{a}.
\]

Under `z=e_ax`, the outer right endpoint maps to

\[
 \frac{1+\delta/a}{e_a}
 =1+\frac{\delta+\delta_0}{a-\delta_0}
 =1+\Delta_a.
\]

Reflection gives the same left overshoot.  The condition
`a>=delta+2delta_0` implies `0<=Delta_a<=1`.  A real cosine at positive
frequency produces the two complex frequencies `+-kappa_j`, so the number
of branches is at most `N=2q`.  There is no zero mode in I.2; zero
coefficients or coincident time exponents are removed before invoking an
`N`-term theorem.

Zhang Proposition 4.2, squared and scaled, gives

\[
 \sup_{I_a\setminus E_a}|G|^2
 \le\frac{9A_{\rm fr}}{2e_a}(2q)^2
 \exp\!\left(6\sqrt2(2q)\sqrt{\Delta_a}\right)
 \int_{E_a}|G|^2.
\]

Thus the exact pointwise prefactor is `18 A_fr q^2/e_a` and the exponent is
`12 sqrt(2) q sqrt(Delta_a)`.  Erdelyi Theorem 2.3 controls the interior
with `pi^2N^2/(8e_a)`, which the displayed exterior constant dominates.
Hölder contributes only `(2e_a)^(1/3)`.  Equations I.17--I.19: **PASS**.

## 2. Spatial derivative scaling

Let `ell_a=2(1+delta/a)` be the length of `I_a` and map it to `[0,1]`.
Erdelyi journal Theorem 2.20 gives

\[
 \ell_a^2\|G_z\|_\infty^2
 \le C\left(108N^5+
 \ell_a^2\sum_{\nu=1}^N\mu_\nu^2\right)\|G\|_\infty^2.
\]

The frozen `ell_a` is bounded above and below, `N<=2q`, and

\[
 \sum_{\nu=1}^N\mu_\nu^2
 =2\sum_{j=1}^q\kappa_j^2
 \le8q\alpha^2.
\]

Multiplication by the `q^2` observation factor yields
`q^7+q^3alpha^2`.  No frequency separation is used.  Equations
I.20--I.21: **PASS**.

## 3. Reverse-time terminal trace

For `sigma=+-1`, direct expansion of I.3 gives

\[
 G(4-r,z)=\sum_{j,\sigma}c_{j,\sigma}(z)
 e^{\gamma_{j,\sigma}r},
 \qquad
 \gamma_{j,\sigma}
 =(\kappa_j/a)^2+i\sigma v\kappa_j.
\]

Therefore `Re gamma_(j,sigma)>0` for every nonzero heat mode; arbitrary
drift affects only the imaginary part.  The reversed fibre belongs to
`E_N^+` with `N<=2q`.  Kós's inequality, recorded in Erdelyi equation
(1.2), gives

\[
 |G(4,z)|\le4q
 \left(\int_3^4|G(s,z)|^2ds\right)^{1/2}.
\]

On the unit interval,
`(int abs(G)^2)^(3/2)<=int abs(G)^3`.  Cubing and integrating in `z` gives
exactly

\[
 h(4)\le64q^3H,\qquad h(4)^{2/3}\le16q^2H^{2/3}.
\]

Erdelyi equation (1.5) would improve the numerical constant but is not
needed.  Equations I.22--I.24: **PASS**.

## 4. Four-row energy reconstruction

The exact differentiated energy is

\[
 \mathcal E'
 =v\int W_aG^2
 +a^{-2}\int\Xi_a''G^2
 -2a^{-2}\int\Xi_a|G_z|^2.
\]

Multiplication by `zeta`, integration over `[0,4]`, and `zeta(0)=0` give
I.28 with the stated signs.  No division by `v` occurs, so `v=0` is
included.

The four absolute payments are:

| row | audited cost before the common exponential |
|---|---|
| terminal | `C q^4 H^(2/3)` |
| cutoff derivative | `C q^2 H^(2/3)` |
| `Xi_a''` | `C a^(-1)q^2 H^(2/3)` |
| `Xi_a G_z^2` | `C[q^7+q^3 Lambda(q,lambda)]H^(2/3)` |

For `lambda<=1`, `Lambda` is bounded.  For `lambda>1`, R0.76E's
fibrewise onset estimate gives

\[
 q^3[q\log(q+1)]^{4/3}\lambda^{-1/3}
 \le Cq^{17/3}\le Cq^7.
\]

Every row is therefore bounded by
`C q^7 exp(Phi_a) H^(2/3)`.  Equations I.25--I.34: **PASS**.

## 5. Physical powers and asymptotic rate

R0.76H's exact cross-section equals `4 pi a delta_0` on `E_a`, so

\[
 M^{\rm plat}\ge4\pi\delta_0a^2R^5H.
\]

Together with

\[
 \mathcal T=\frac{a^2R^3}{2}
 v\int\zeta\int W_aG^2,
\]

this produces

\[
 |\mathcal T|
 \le Ca^{2/3}R^{-1/3}q^7e^{\Phi_a}
 (M^{\rm plat})^{2/3}.
\]

For `p^(plat)=R^(-2)omega M^(plat)` and
`mathfrak X=(omega/R)[mathcal T]_+`, the `R^(-1/3)` factor cancels exactly,
leaving `a^(2/3)q^7omega^(1/3)e^(Phi_a)`.  Since

\[
 \frac{\Phi_a}{L^2}
 =O\!\left(\frac{q(L)}{L^{5/2}}\right)
\]

and `log q=o(L^2)` under `q=o(L^(5/2))`, the only quadratic rate is
`log(omega^(1/3))/L^2=-2/11907`.  Equations I.35--I.37 and I.5--I.8:
**PASS**.

## 6. Source and claim boundary

- Zhang Proposition 4.2 is used only as an upper bound and is identified
  as an unrefereed arXiv v1 input.
- Zhang Proposition 8.4's lower-bound range is stated as
  `N^(-2)<=Delta<=1`.  No lower assertion is attributed to it below that
  range.
- The confluent complex lower witnesses are not relabelled as real dyadic
  heat shears.
- The cited Fourier result is not relabelled as a three-dimensional signed
  flux theorem; the latter conversion is local.
- Exact-shear, one-band, Version-M, arbitrary-field, regularity,
  singularity, no-simulation, no-figure, and **NOT CLAY** boundaries are
  explicit.

Source and claim boundary: **PASS**.

## Certificate boundary

Finite certificates may bind hashes, exact rational fixtures, term counts,
equation inventory, power ledgers, rate arithmetic, citations, and boundary
phrases.  They do not prove Zhang Proposition 4.2, Erdelyi's continuum
inequalities, or the continuum integrations above.  This audit is a
mathematical reread, not a peer review of the imported preprint.
