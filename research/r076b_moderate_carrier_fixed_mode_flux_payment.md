# R0.76B -- inverse-radius signed-flux payment for every fixed finite harmonic family

## 0. Result and exact boundary

R0.75X pays every fixed finite dyadic harmonic family when the scaled first
carrier `n_1aR` is bounded.  R0.75Z and R0.76A show why a high-carrier proof
cannot simply estimate or discard the localized envelope current.  The present
note instead restores the carrier and works with the square of the complete
real field before any absolute value is taken.

Fix an integer `q>=1`.  Let

\[
 n_1,\ldots,n_q\in\mathbb N,
 \qquad 1\le n_1<n_2<\cdots<n_q\le2n_1
 \tag{B.1}
\]

and set

\[
 F(t,x_2)=\sum_{j=1}^q A_j e^{-n_j^2t}
 \cos\bigl(n_jx_2-\phi_j-n_jBt\bigr),
 \qquad A_j\ge0,\qquad \phi_j\in\mathbb R,
 \qquad B\in\mathbb R.
 \tag{B.2}
\]

For the frozen radial collar, plateau, and complete-clock cutoff, define

\[
 \begin{aligned}
 \mathcal T_{\boldsymbol n,R}
 &:=\frac12\int_0^{4R^2}\!\int_{\mathbb T^3}
 \eta_R(t)B\,\partial_2\xi_{a,R}|F|^2\,dxdt,\\
 M_{\boldsymbol n,R}^{\rm plat}
 &:=\int_0^{4R^2}\!\int_{\mathcal S_{a,R}^{\rm plat}}
 |F|^3\,dxdt.
 \end{aligned}
 \tag{B.3}
\]

Assume the inverse-radius carrier condition

\[
 n_1R\le1.
 \tag{B.4}
\]

For every fixed `q` and all sufficiently large frozen `L`, there is a constant
`C_q`, depending on `q` and the frozen collar and cutoff profiles but not on
`R`, the frequencies, amplitudes, phases, or `B`, such that

\[
 \boxed{
 |\mathcal T_{\boldsymbol n,R}|
 \le C_q a^{2/3}R^{-1/3}
 \bigl(M_{\boldsymbol n,R}^{\rm plat}\bigr)^{2/3}.}
 \tag{B.5}
\]

With

\[
 p_{\boldsymbol n,R}^{\rm plat}
 =R^{-2}\omega M_{\boldsymbol n,R}^{\rm plat},
 \qquad
 \mathfrak X_{\boldsymbol n,R}
 =\frac\omega R[\mathcal T_{\boldsymbol n,R}]_+,
 \tag{B.6}
\]

equation B.5 becomes

\[
 \boxed{
 \mathfrak X_{\boldsymbol n,R}
 \le C_q a^{2/3}\omega^{1/3}
 \bigl(p_{\boldsymbol n,R}^{\rm plat}\bigr)^{2/3},
 \qquad
 \lim_{L\to\infty}\frac1{L^2}
 \log(a^{2/3}\omega^{1/3})=-\frac2{11907}.}
 \tag{B.7}
\]

For fixed `q`, this closes the entire exact-shear carrier range
`n_1<=R^{-1}`.  It does not give a constant uniform in growing `q`, and it
does not address the ultra-high sector `n_1R>1`.

## 1. Frozen inputs and the remaining branch

Retain

\[
 a=pL,\qquad R=e^{-\rho L^2/4},\qquad
 \omega=e^{-c_\gamma L^2/4},\qquad \ell=aR,
 \tag{B.8}
\]

and

\[
 0\le\eta_R\le1,\qquad \eta_R(0)=0,
 \qquad |\eta_R'(t)|\le C_\eta R^{-2}.
 \tag{B.9}
\]

The immediately used frozen inputs are

| input | SHA-256 | role |
|---|---|---|
| `research/r075b_bulk_clock_outer_padding_gate.md` | `430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a` | complete clock and cutoff onset |
| `research/r075r_outer_cap_spectral_concentration_obstruction.md` | `e5eba5b262a8e140eaa149b6d914f355f2f3c636ec1e74cf85515f1c38fd32f3` | radial cross section and growing-packet obstruction |
| `research/r075w_full_frequency_two_harmonic_flux_payment.md` | `571b8152e3e5f81becec4dd691488fb5889fac23e94ca7c99bd546399dc320d4` | local energy identity and two-mode theorem |
| `research/r075x_fixed_finite_mode_low_carrier_payment.md` | `8e0c412528578c15d807b33b64f0996e62a2dabe2ebd58fa297f67c093929763` | fixed-`q` low-carrier half |
| `research/r075z_unresolved_cluster_carrier_current_gate.md` | `30d2811e8747aa2b40b4787e6f169af19d1381b66fc84610327da221168f3d97` | unresolved carrier-current decomposition |
| `research/r076a_complete_clock_localized_current_sign_obstruction.md` | `d23532f84702be1630daa0b8d56d02242571dd8a1f8024c59a7f71bec30f26eb` | failure of localized current sign-dropping |

Put

\[
 s=\frac t{R^2},\qquad z=\frac{x_2}{aR},\qquad
 \kappa_j=n_jaR,\qquad \alpha=\kappa_1,\qquad
 v=\frac{BR}{a}.
 \tag{B.10}
\]

R0.75X with `C_0=8q` already proves B.5 when `alpha<8q`.  It remains to
consider

\[
 8q\le\alpha\le a,
 \qquad \alpha=\kappa_1<\cdots<\kappa_q\le2\alpha.
 \tag{B.11}
\]

Here the upper bound `alpha<=a` is exactly B.4.  Define

\[
 G(s,z)=F(R^2s,aRz)
 =\sum_{j=1}^q A_j e^{-\kappa_j^2s/a^2}
 \cos\bigl(\kappa_j(z-vs)-\phi_j\bigr).
 \tag{B.12}
\]

Then

\[
 \partial_sG+v\partial_zG-a^{-2}\partial_z^2G=0.
 \tag{B.13}
\]

Let

\[
 I=[-1/2,1/2],\qquad J=[-3/2,3/2],\qquad
 J^+=[-2,2],\qquad
 h(s)=\int_I|G(s,z)|^3\,dz,
 \qquad H=\int_0^4h(s)\,ds.
 \tag{B.14}
\]

## 2. High-carrier spatial observation without a gap loss

**Lemma B.1.**  Fix `q`.  If `alpha>=8q` and
`alpha<=kappa_1<...<kappa_m<=2alpha` with `m<=q`, then every real or complex
sum of the corresponding exponentials satisfies

\[
 \boxed{
 \|g\|_{L^\infty(J)}
 +\alpha^{-1}\|g'\|_{L^\infty(J)}
 \le C_q\|g\|_{L^3(I)}.}
 \tag{B.15}
\]

No frequency separation enters the constant.

Set

\[
 f(x)=g(x/\alpha),\qquad r_j=\kappa_j/\alpha\in[1,2].
 \tag{B.16}
\]

If `h_g=int_I|g|^3=0`, analyticity gives `g=0` and the lemma is immediate.
Otherwise Chebyshev's inequality gives a measurable set

\[
 E=\{x\in\alpha I:|f(x)|^3\le2h_g\},
 \qquad |E|\ge\frac\alpha2.
 \tag{B.17}
\]

Apply the Turan--Nazarov measurable-set inequality on `alpha J^+`.  The
exponents of `f` are among `+-ir_j`, their real parts vanish, there are at
most `2q` terms, and `|alpha J^+|/|E|<=8`.  Hence

\[
 \|f\|_{L^\infty(\alpha J^+)}
 \le (8C)^{2q-1}(2h_g)^{1/3}
 \le C_qh_g^{1/3}.
 \tag{B.18}
\]

It remains to control one derivative locally.  Every such `f` solves

\[
 \prod_{j=1}^m(\partial_x^2+r_j^2)f=0.
 \tag{B.19}
\]

The roots lie in the fixed compact set `+-i[1,2]`.  The companion matrices,
including repeated-root limits, form a compact family.  On a unit interval,
the complete initial jet and the `L^infinity` norm of the first component are
uniformly equivalent: otherwise unit jets would converge to a nonzero
limiting solution vanishing on an interval, contradicting ODE uniqueness.
When `m<q`, multiplying the annihilator by repeated factors embeds the
solution in the same order-`2q` compact family.
Consequently, for every unit window `K` and its concentric double window
`K^+`,

\[
 \|f'\|_{L^\infty(K)}
 \le C_q\|f\|_{L^\infty(K^+)}.
 \tag{B.20}
\]

Because `alpha>=8q>=8`, every point of `alpha J` has such a double window
inside `alpha J^+`.  Combine B.18--B.20 and use `g'=alpha f'(alpha z)` to
prove B.15.  Applied to B.12 at each fixed time, the lemma gives

\[
 \boxed{
 \|G(s)\|_{L^\infty(J)}
 +\alpha^{-1}\|G_z(s)\|_{L^\infty(J)}
 \le C_qh(s)^{1/3}.}
 \tag{B.21}
\]

This is the step unavailable from the bounded-frequency compactness lemma
alone: the value is propagated by Turan--Nazarov after carrier scaling, while
only a compact unit-window ODE estimate is used for the derivative.

## 3. Complete-clock terminal trace

For every fixed `z`, write B.12 as an exponential polynomial

\[
 \mathcal Q_z(s)=\sum_{r=1}^{N_z}c_r(z)e^{\lambda_rs},
 \qquad N_z\le2q.
 \tag{B.22}
\]

If the real parts satisfy `|Re lambda_r|<=4`, the same measurable-set
inequality and the half-measure sublevel set give

\[
 \boxed{|\mathcal Q_z(4)|^3
 \le C_q\int_0^4|\mathcal Q_z(s)|^3\,ds.}
 \tag{B.23}
\]

Indeed, the exponents here are

\[
 \lambda_{j,\pm}=-\kappa_j^2/a^2\pm i\kappa_jv,
 \qquad
 0\le\kappa_j^2/a^2\le4,
 \tag{B.24}
\]

where the last bound follows from `kappa_j<=2alpha<=2a`.  The estimate is
therefore independent of `v` and of all gaps.  Integrating B.23 on `I` gives

\[
 \boxed{h(4)\le C_qH.}
 \tag{B.25}
\]

## 4. Full-field local energy identity

For the frozen radial profile set

\[
 W_a(z)=-2\pi az\,\vartheta\bigl(a(|z|-1)\bigr),
 \qquad
 \Xi_a(z)=\int_{-\infty}^zW_a(r)\,dr.
 \tag{B.26}
\]

For all sufficiently large `L`, `Xi_a` is nonnegative, supported in `J`, and

\[
 \|W_a\|_1+\|\Xi_a\|_1+\|\Xi_a\|_\infty\le C,
 \qquad \|\Xi_a''\|_1\le Ca.
 \tag{B.27}
\]

The exact cross-sectional rescaling and
`zeta(s)=eta_R(R^2s)` give

\[
 \boxed{
 \mathcal T_{\boldsymbol n,R}
 =\frac{a^2R^3}{2}v
 \int_0^4\!\zeta(s)\int_{\mathbb R}W_a(z)G(s,z)^2\,dzds.}
 \tag{B.28}
\]

For `Q=G^2`, equation B.13 gives the exact identity

\[
 \partial_sQ+v\partial_zQ-a^{-2}\partial_z^2Q
 =-2a^{-2}|G_z|^2.
 \tag{B.29}
\]

With `E(s)=int Xi_aG^2` and `W_a=Xi_a'`, spatial integration by parts yields

\[
 v\int W_aG^2
 =E'(s)-a^{-2}\int\Xi_a''G^2
 +2a^{-2}\int\Xi_a|G_z|^2.
 \tag{B.30}
\]

Since `zeta(0)=0`, time integration gives

\[
 \begin{aligned}
 v\int_0^4\!\zeta\int W_aG^2
 &=\zeta(4)E(4)-\int_0^4\zeta'E\,ds\\
 &\quad-a^{-2}\int_0^4\!\zeta\int\Xi_a''G^2
 +2a^{-2}\int_0^4\!\zeta\int\Xi_a|G_z|^2.
 \end{aligned}
 \tag{B.31}
\]

The value part of B.21 and B.27 imply

\[
 |E(s)|+a^{-2}\left|\int\Xi_a''G^2\right|
 \le C_qh(s)^{2/3}.
 \tag{B.32}
\]

For the last row, the derivative part of B.21 and `alpha<=a` give

\[
 a^{-2}\int|\Xi_a||G_z|^2
 \le C_q\left(\frac\alpha a\right)^2h(s)^{2/3}
 \le C_qh(s)^{2/3}.
 \tag{B.33}
\]

The endpoint follows from B.21 and B.25:

\[
 |E(4)|\le C_qh(4)^{2/3}\le C_qH^{2/3}.
 \tag{B.34}
\]

Finally `|zeta'|<=C_eta` and Holder's inequality on `[0,4]` give

\[
 \boxed{
 \left|v\int_0^4\zeta\int W_aG^2\right|
 \le C_qH^{2/3}.}
 \tag{B.35}
\]

The complete square `G^2` is retained through B.29--B.31.  Self terms,
difference frequencies, sum frequencies, and all cross-cluster products are
therefore reassembled before absolute values; no spectral separation and no
localized-current sign are used.

## 5. Physical scales and normalization

The exact plateau-fibre area gives

\[
 \boxed{
 M_{\boldsymbol n,R}^{\rm plat}
 \ge4\pi\delta_0a^2R^5H.}
 \tag{B.36}
\]

Combining B.28, B.35, and B.36 proves

\[
 \begin{aligned}
 |\mathcal T_{\boldsymbol n,R}|
 &\le C_qa^2R^3H^{2/3}\\
 &\le C_qa^{2/3}R^{-1/3}
 \bigl(M_{\boldsymbol n,R}^{\rm plat}\bigr)^{2/3},
 \end{aligned}
 \tag{B.37}
\]

which is B.5 in the branch B.11.  Together with R0.75X for `alpha<8q`,
this proves B.5 under the full condition B.4.  Substitution of B.6 proves
B.7.

## 6. Why restoring the carrier removes the R0.76A obstruction

For one analytic cluster, write its complete complex field as

\[
 \mathcal H(s,z)=e^{-\alpha^2s/a^2}e^{i\alpha(z-vs)}Z(s,z),
 \qquad P=|\mathcal H|^2=e^{-2\alpha^2s/a^2}|Z|^2.
 \tag{B.38}
\]

The complex field obeys the same transport-diffusion equation, so

\[
 P_s+vP_z-a^{-2}P_{zz}
 =-2a^{-2}e^{-2\alpha^2s/a^2}
 |i\alpha Z+Z_z|^2\le0.
 \tag{B.39}
\]

The nonnegative square in B.39 expands as

\[
 |i\alpha Z+Z_z|^2
 =\alpha^2|Z|^2+|Z_z|^2
 +2\alpha\operatorname {Im}(\overline Z Z_z).
 \tag{B.40}
\]

R0.76A makes the last two terms negative after localization for one exact
cluster, but B.40 shows that they are not the complete dissipative density.
The proof above restores the full real field even before this decomposition,
so the omitted positive carrier-density block and every real-field
interaction remain present.

## 7. Exact-solution and Version-M boundary

Equation B.2 satisfies

\[
 \partial_tF+B\partial_2F-\partial_2^2F=0
 \tag{B.41}
\]

and embeds in the exact smooth unforced shear `u=(0,B,F(t,x_2))` with constant
pressure.  The nonzero constant background has not been shown to belong to
the frozen mean-zero, inversion-paired Version-M subclass.

If the complete clock and plateau tube belong to the same scale-`2R`
Version-M measurement row with weight at least `omega`, and `F` is an actual
component of that same velocity, B.7 gives the corresponding conditional
`C_q(P_R^M)^(2/3)` consequence.  It cannot be applied merely to a Fourier
projection of a larger solution.

## 8. What is closed and what remains open

**Closed here:** for every fixed `q`, the complete signed collar-flux estimate
for every exact real dyadic harmonic family with `n_1R<=1`; all coefficient
cancellations and frequency collisions; arbitrary phases and constant shear
speed; the fixed-`q` scale normalization; and the R0.76A localized-current
sign obstruction within this exact-shear range.

**Open:** the ultra-high carrier sector `n_1R>1`; a quantitative constant
usable for `q=q(L)`; arbitrary growing packets; nonconstant or vertically
dependent shear; projection from a larger velocity; arbitrary-field E.24;
complete Version-M extraction; fixed deletion; suitable-weak transfer;
regularity; and singularity.

The R0.75R outer-cap construction still forbids promoting this fixed-`q`
result to arbitrary packets.  The proof is analytic.  Finite fixtures audit
the scaling, compact-window geometry, exponent bounds, energy identity, and
one exact high-carrier family; they are not proof of the continuum observation
lemmas.  No formal scientific figure or simulation is claimed.  No
completeness, novelty, or priority claim is made.  **NOT CLAY.**
