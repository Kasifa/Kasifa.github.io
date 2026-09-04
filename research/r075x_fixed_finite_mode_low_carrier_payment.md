# R0.75X -- low-carrier signed-flux payment for every fixed finite harmonic family

## 0. Result and exact boundary

R0.75W proves a full-frequency signed collar-flux estimate for one exact
two-harmonic dyadic shear.  Its low-carrier proof uses only two properties of
that pair: a finite-dimensional spatial ODE and a finite-term temporal
exponential polynomial.  The present note proves that this mechanism is not
special to two modes.

Fix an integer `q>=1`.  Let

\[
 1\le n_1<n_2<\cdots<n_q\le2n_1
 \tag{X.1}
\]

and set

\[
 F(t,x_2)=\sum_{j=1}^q
 A_j e^{-n_j^2t}
 \cos\bigl(n_jx_2-\phi_j-n_jBt\bigr),
 \qquad A_j\ge0,\qquad B\in\mathbb R.
 \tag{X.2}
\]

For the frozen radial collar, plateau, and time cutoff, define

\[
 \begin{aligned}
 \mathcal T_{\boldsymbol n,R}
 &:=\frac12\int_0^{4R^2}\!\int_{\mathbb T^3}
 \eta_R(t)B\,\partial_2\xi_{a,R}|F|^2\,dxdt,\\
 M_{\boldsymbol n,R}^{\rm plat}
 &:=\int_0^{4R^2}\!\int_{\mathcal S_{a,R}^{\rm plat}}
 |F|^3\,dxdt.
 \end{aligned}
 \tag{X.3}
\]

Assume the low-carrier condition

\[
 n_1aR<C_0.
 \tag{X.4}
\]

There is a constant `C_q`, depending on `q`, `C_0`, and the frozen collar
and cutoff profiles, but not on `R`, the frequencies, amplitudes, phases, or
`B`, such that

\[
 \boxed{
 |\mathcal T_{\boldsymbol n,R}|
 \le C_q a^{2/3}R^{-1/3}
 \bigl(M_{\boldsymbol n,R}^{\rm plat}\bigr)^{2/3}.}
 \tag{X.5}
\]

With

\[
 p_{\boldsymbol n,R}^{\rm plat}
 =R^{-2}\omega M_{\boldsymbol n,R}^{\rm plat},
 \qquad
 \mathfrak X_{\boldsymbol n,R}
 =\frac\omega R[\mathcal T_{\boldsymbol n,R}]_+,
 \tag{X.6}
\]

equation X.5 becomes

\[
 \boxed{
 \mathfrak X_{\boldsymbol n,R}
 \le C_q a^{2/3}\omega^{1/3}
 \bigl(p_{\boldsymbol n,R}^{\rm plat}\bigr)^{2/3},
 \qquad
 \lim_{L\to\infty}\frac1{L^2}
 \log(a^{2/3}\omega^{1/3})=-\frac2{11907}.}
 \tag{X.7}
\]

For every fixed `q`, the factor `C_q` has zero logarithmic cost on the
frozen `L^2` scale.  No uniform control of `C_q` as `q` grows is proved.
For `q=2`, X.5 is the low-carrier half of R0.75W.  For `q>=3`, the
high-carrier sector remains open.

## 1. Frozen inputs and scaling

Retain

\[
 a=pL,\qquad R=e^{-\rho L^2/4},\qquad
 \omega=e^{-c_\gamma L^2/4},\qquad aR=\ell,
 \tag{X.8}
\]

and

\[
 0\le\eta_R\le1,\qquad \eta_R(0)=0,\qquad
 |\eta_R'(t)|\le C_\eta R^{-2}.
 \tag{X.9}
\]

The immediately used frozen inputs are

| input | SHA-256 | role |
|---|---|---|
| `research/r075b_bulk_clock_outer_padding_gate.md` | `430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a` | complete clock and cutoff onset |
| `research/r075r_outer_cap_spectral_concentration_obstruction.md` | `e5eba5b262a8e140eaa149b6d914f355f2f3c636ec1e74cf85515f1c38fd32f3` | canonical radial cross section and growing-packet obstruction |
| `research/r075w_full_frequency_two_harmonic_flux_payment.md` | `571b8152e3e5f81becec4dd691488fb5889fac23e94ca7c99bd546399dc320d4` | local energy identity and the two-mode case |

In the sector X.4, put

\[
 s=\frac t{R^2},\qquad z=\frac{x_2}{aR},\qquad
 \alpha_j=n_jaR,\qquad v=\frac{BR}{a}.
 \tag{X.10}
\]

Then

\[
 0<\alpha_1<\cdots<\alpha_q\le2C_0
 \tag{X.11}
\]

and

\[
 \begin{aligned}
 G(s,z):=F(R^2s,aRz)
 =\sum_{j=1}^q A_j e^{-\alpha_j^2s/a^2}
 \cos\bigl(\alpha_j(z-vs)-\phi_j\bigr).
 \end{aligned}
 \tag{X.12}
\]

The exact equation is

\[
 \partial_sG+v\partial_zG-a^{-2}\partial_z^2G=0.
 \tag{X.13}
\]

Let

\[
 I=[-1/2,1/2],\qquad
 h(s)=\int_I|G(s,z)|^3\,dz,\qquad
 H=\int_0^4h(s)\,ds.
 \tag{X.14}
\]

## 2. Uniform confluent observation in dimension `2q`

**Lemma X.1.**  Fix `q`, `K<infinity`, and compact intervals `I,J`, with
`I` having nonempty interior.  There is `C=C(q,K,I,J)` such that, for every
parameter vector `boldsymbol alpha in [0,K]^q`, every real or complex
solution of

\[
 \prod_{j=1}^q(\partial_z^2+\alpha_j^2)g=0
 \tag{X.15}
\]

satisfies

\[
 \boxed{
 \|g\|_{L^\infty(J)}+\|g'\|_{L^\infty(J)}
 \le C\|g\|_{L^3(I)}.}
 \tag{X.16}
\]

Repeated parameters and `alpha_1=...=alpha_q=0` are included.  In the
fully confluent zero-frequency limit, X.15 is `partial_z^(2q)g=0`, so its
solution space is the polynomials of degree at most `2q-1`.

To prove the lemma, expand

\[
 \prod_{j=1}^q(\lambda+\alpha_j^2)
 =\lambda^q+\sigma_1\lambda^{q-1}+\cdots+\sigma_q
 \tag{X.17}
\]

and write `X=(g,g',...,g^(2q-1))`.  Equation X.15 is

\[
 X'=\mathbb A_{\boldsymbol\alpha}X,
 \tag{X.18}
\]

where the superdiagonal entries are one and the final row has entries

\[
 (-\sigma_q,0,-\sigma_{q-1},0,\ldots,-\sigma_1,0).
 \tag{X.19}
\]

The matrices form a compact bounded family because every `sigma_j` is a
continuous elementary symmetric polynomial on `[0,K]^q`.  It is enough to
control the initial jet at one point of `I`.  Otherwise there would be
parameters `boldsymbol alpha^(r)` and solutions with unit initial jet and
`L^3(I)` norm tending to zero.  After taking a subsequence, both the
parameters and initial jets converge.  Continuous dependence for X.18
gives a nonzero limiting solution whose first component vanishes on `I`.
Uniqueness for X.18 then forces the whole limiting initial jet to vanish,
a contradiction.  Uniform propagation of the controlled jet from `I` to
`J` proves X.16.

At every fixed time, G satisfies X.15 with `K=2C_0`.  Therefore

\[
 \|G(s)\|_{L^\infty(J)}+\|\partial_zG(s)\|_{L^\infty(J)}
 \le C_q h(s)^{1/3}.
 \tag{X.20}
\]

No inverse frequency gap occurs.

## 3. A `2q`-term terminal trace

**Lemma X.2.**  Fix `q` and `Lambda<infinity`.  If

\[
 Q(s)=\sum_{r=1}^{N}c_re^{\lambda_rs},\qquad
 N\le2q,\qquad |\operatorname {Re}\lambda_r|\le\Lambda,
 \tag{X.21}
\]

then

\[
 \boxed{|Q(4)|^3\le C_{q,\Lambda}
 \int_0^4|Q(s)|^3\,ds.}
 \tag{X.22}
\]

The constant is independent of the imaginary parts and of every exponent
gap.  Nazarov's measurable-set inequality gives

\[
 \sup_{[0,4]}|Q|
 \le e^{4\Lambda}
 \left(\frac{4C}{|E|}\right)^{N-1}\sup_E|Q|.
 \tag{X.23}
\]

If `I_Q=int_0^4|Q|^3`, then
`E={s:|Q(s)|^3<=I_Q/2}` has measure at least two.  Substitution in X.23
proves X.22.  This also displays an at-most-exponential contribution in
`q` from the temporal trace; it does not give a uniform-in-`q` estimate.

For each fixed `z`, X.12 has at most `2q` exponential terms, with exponents

\[
 -\alpha_j^2/a^2\pm i\alpha_jv,\qquad 1\le j\le q.
 \tag{X.24}
\]

Their real parts are bounded by `4C_0^2` once `a>=1`.  Apply X.22 and
integrate over `z in I` to obtain

\[
 \boxed{h(4)\le C_qH.}
 \tag{X.25}
\]

This remains uniform for `B=0`, arbitrarily large `|B|`, and colliding
scaled frequencies.

## 4. Radial primitive and local energy identity

Let the frozen radial profile be `vartheta` and set

\[
 W_a(z)=-2\pi az\,\vartheta\bigl(a(|z|-1)\bigr),
 \qquad
 \Xi_a(z)=\int_{-\infty}^zW_a(r)\,dr.
 \tag{X.26}
\]

Oddness gives `int W_a=0`, so `Xi_a` is compactly supported.  For all
sufficiently large `L`, its support lies in `J=[-3/2,3/2]` and

\[
 \|W_a\|_1+\|\Xi_a\|_1+\|\Xi_a\|_\infty\le C,
 \qquad \|\Xi_a''\|_1\le Ca.
 \tag{X.27}
\]

The exact cross-sectional calculation and `zeta(s)=eta_R(R^2s)` give

\[
 \boxed{
 \mathcal T_{\boldsymbol n,R}
 =\frac{a^2R^3}{2}v
 \int_0^4\!\zeta(s)\int_{\mathbb R}W_a(z)G(s,z)^2\,dzds.}
 \tag{X.28}
\]

For `Q=G^2` and `E(s)=int Xi_aG^2`, equation X.13 yields

\[
 \begin{aligned}
 \partial_sQ+v\partial_zQ-a^{-2}\partial_z^2Q
 &=-2a^{-2}|\partial_zG|^2,\\
 v\int W_aG^2
 &=E'(s)-a^{-2}\int\Xi_a''G^2
 +2a^{-2}\int\Xi_a|\partial_zG|^2.
 \end{aligned}
 \tag{X.29}
\]

After multiplication by `zeta` and integration on `[0,4]`, the right side
is

\[
 \begin{aligned}
 \zeta(4)E(4)-\int_0^4\zeta'E\,ds
 -a^{-2}\int_0^4\zeta\int\Xi_a''G^2
 +2a^{-2}\int_0^4\zeta\int\Xi_a|G_z|^2.
 \end{aligned}
 \tag{X.30}
\]

Use X.20 and X.27 at every time.  Since `a>=1`,

\[
 |E(s)|+a^{-2}\left|\int\Xi_a''G^2\right|
 +a^{-2}\int|\Xi_a||G_z|^2
 \le C_qh(s)^{2/3}.
 \tag{X.31}
\]

For the endpoint, X.20 and X.25 give

\[
 |E(4)|\le C_qh(4)^{2/3}\le C_qH^{2/3}.
 \tag{X.32}
\]

The cutoff satisfies `|zeta'|<=C_eta`.  Holder on the fixed time interval
then bounds every other row of X.30 by `C_qH^(2/3)`.  Consequently

\[
 \boxed{
 \left|v\int_0^4\zeta\int W_aG^2\right|
 \le C_qH^{2/3}.}
 \tag{X.33}
\]

The proof forms the complete energy identity before taking absolute values.
It never divides by `v`, an amplitude, a frequency, or a frequency gap.

## 5. Return to physical scales

The exact plateau-fibre area and X.14 give

\[
 \boxed{
 M_{\boldsymbol n,R}^{\rm plat}
 \ge4\pi\delta_0a^2R^5H.}
 \tag{X.34}
\]

Combining X.28, X.33, and X.34 yields

\[
 \begin{aligned}
 |\mathcal T_{\boldsymbol n,R}|
 &\le C_qa^2R^3H^{2/3}\\
 &\le C_qa^{2/3}R^{-1/3}
 \bigl(M_{\boldsymbol n,R}^{\rm plat}\bigr)^{2/3},
 \end{aligned}
 \tag{X.35}
\]

which proves X.5.  Substitution of X.6 proves X.7.

## 6. Dependence on the number of modes

For fixed `q`, `C_q` is independent of `L`; hence it does not alter the
strict rate `-2/11907`.  The proof deliberately does not hide what happens
when `q` grows:

1. the temporal Turan--Nazarov factor in X.23 grows at most exponentially
   in `q` for the fixed half-measure choice;
2. the compactness proof of Lemma X.1 supplies a finite spatial constant for
   each `q`, but no quantitative uniform bound in `q`;
3. the outer-cap construction of R0.75R shows that a growing high-band
   packet can concentrate away from the plateau, so a uniform arbitrary-
   packet conclusion cannot be inferred from X.35.

Thus X.35 is a fixed-finite-dimensional theorem, not an arbitrary-packet
theorem in disguise.

## 7. Exact-solution and Version-M boundary

Equation X.2 satisfies

\[
 \partial_tF+B\partial_2F-\partial_2^2F=0
 \tag{X.36}
\]

and embeds in the exact smooth unforced shear `u=(0,B,F(t,x_2))` with
constant pressure.  The nonzero constant background has not been shown to
belong to the frozen mean-zero, inversion-paired Version-M subclass.

If the complete clock and plateau tube are in the same scale-`2R`
Version-M measurement row with weight at least `omega`, and F is an actual
component of that same velocity, then X.7 gives the same conditional
`C_q(P_R^M)^(2/3)` consequence as W.  This is not valid merely for a Fourier
projection of a larger field.

## 8. What is closed and what remains open

**Closed here:** the complete low-carrier signed-flux estimate for every
fixed finite real harmonic family in one dyadic band; all frequency
collisions; arbitrary phases, amplitudes, and constant shear speed; and the
scale-free normalization for fixed `q`.

**Open:** a quantitative spatial observation constant suitable for
`q=q(L)`; the high-carrier sector for three or more modes; arbitrary dyadic
packets; inter-packet aggregation; nonconstant or vertically dependent
shear; projection from a larger velocity; arbitrary-field E.24; complete
Version-M extraction; fixed deletion; suitable-weak transfer; regularity;
and singularity.

The proof is analytic.  A plot or finite parameter scan would not certify
the `2q`-dimensional compactness argument or the continuum exponential-
polynomial trace, so no formal scientific figure or simulation is claimed.
No completeness, novelty, or priority claim is made.  **NOT CLAY.**
