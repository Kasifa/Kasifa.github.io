# R0.75W -- full-frequency signed-flux payment for one dyadic two-harmonic shear

## 0. Result and exact boundary

R0.75V proves the complete signed collar-flux estimate for one exact
two-harmonic dyadic shear under the carrier condition `maR>=C_0`.  The
condition enters only through the pointwise-in-time spatial sampling lemma
of R0.75T.  It is false that the same T defect controls a low-carrier pair:
two slowly varying waves can cancel at the centre of the observed interval
for amplitude and phase combinations not measured by that defect.

This note does not repair the T defect.  Instead it treats the complementary
low-carrier sector by one local energy identity and a uniform four-dimensional
observation lemma.  The exact initial slice with `k=2m`, `C=2A`,
`phi=pi/2`, and `psi=-pi/2` is
`A sin(2my)-2A sin(my)=-A(my)^3+O(A(my)^5)`.  Its T amplitude-mismatch
defect is of order `A`, while its observed low-carrier mass vanishes to
ninth order in `maR`.  This is a counterexample to extending the T
pointwise defect, but not to the complete signed-flux estimate below.  Let

\[
 \begin{aligned}
 F(t,x_2)&=A_t\cos(kx_2-\phi_t)
          +C_t\cos(mx_2-\psi_t),\\
 A_t&=Ae^{-k^2t},\qquad C_t=Ce^{-m^2t},\\
 \phi_t&=\phi+kBt,\qquad \psi_t=\psi+mBt,
 \end{aligned}
 \tag{W.1}
\]

where `A,C>=0`, `1<=m<k<=2m`, and `B` is any real constant.  There is a
constant depending only on the frozen radial profile, plateau width, time
cutoff, and the carrier threshold in R0.75T such that

\[
 \mathcal T_{k,m,R}:=\frac12\int_0^{T_R}\!\int_{\mathbb T^3}
 \eta_R(t)B\,\partial_2\xi_{a,R}|F|^2\,dxdt,
 \qquad
 M_{k,m,R}^{\rm plat}:=\int_0^{T_R}\!\int_{\mathcal S_{a,R}^{\rm plat}}
 |F|^3\,dxdt .
\]

Then

\[
 \boxed{
 |\mathcal T_{k,m,R}|
 \le Ca^{2/3}R^{-1/3}
 \bigl(M_{k,m,R}^{\rm plat}\bigr)^{2/3}}
 \tag{W.2}
\]

for every dyadic pair W.1 and all sufficiently large `L`.  There is no
lower or upper carrier-frequency restriction in W.2.

With

\[
 p_{k,m,R}^{\rm plat}=R^{-2}\omega M_{k,m,R}^{\rm plat},
 \qquad
 \mathfrak X_{k,m,R}=\frac\omega R[\mathcal T_{k,m,R}]_+,
 \tag{W.3}
\]

the normalized estimate is

\[
 \boxed{
 \mathfrak X_{k,m,R}
 \le Ca^{2/3}\omega^{1/3}
 \bigl(p_{k,m,R}^{\rm plat}\bigr)^{2/3},
 \qquad
 \lim_{L\to\infty}\frac1{L^2}
 \log(a^{2/3}\omega^{1/3})=-\frac2{11907}.}
 \tag{W.4}
\]

This is a full-frequency theorem only for the exact pair W.1.  It is not a
three-mode estimate, a packet theorem, or an estimate for a Fourier
projection of a larger velocity.

## 1. Frozen inputs and the carrier split

Retain

\[
 a=pL,\qquad R=e^{-\rho L^2/4},\qquad T_R=4R^2,
 \qquad \ell=aR,
 \tag{W.5}
\]

and the translated time cutoff

\[
 0\le\eta_R\le1,\qquad \eta_R(0)=0,
 \qquad |\eta_R'(t)|\le C_\eta R^{-2}.
 \tag{W.6}
\]

The immediately used frozen inputs are

| input | SHA-256 | role |
|---|---|---|
| `research/r075b_bulk_clock_outer_padding_gate.md` | `430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a` | complete clock and cutoff onset |
| `research/r075r_outer_cap_spectral_concentration_obstruction.md` | `e5eba5b262a8e140eaa149b6d914f355f2f3c636ec1e74cf85515f1c38fd32f3` | exact radial cross section |
| `research/r075t_two_harmonic_collar_coercivity.md` | `822059f8a6248143ff3f36938a2333bee9f909b9166db951e227c426c2e8bc66` | plateau fibre and carrier threshold |
| `research/r075v_complete_two_harmonic_flux_payment.md` | `6917ff77099b6271b005ca90335df589434a38b0a57001893dcae8b02fd34824` | complete high-carrier theorem |

The high-carrier sector

\[
 maR\ge C_0
 \tag{W.7}
\]

is exactly R0.75V.  It remains to prove W.2 when `maR<C_0`.  Since
`k<=2m`, both scaled frequencies in that sector obey a fixed upper bound.

## 2. Low-carrier scaling

For `maR<C_0`, set

\[
 s=\frac t{R^2},\qquad z=\frac{x_2}{aR},\qquad
 \alpha=kaR,\quad\beta=maR,\quad v=\frac{BR}{a}.
 \tag{W.8}
\]

Thus `0<beta<alpha<=2C_0`, the time interval becomes `[0,4]`, and

\[
 \begin{aligned}
 G(s,z):=F(R^2s,aRz)
 &=Ae^{-\alpha^2s/a^2}
   \cos\bigl(\alpha(z-vs)-\phi\bigr)\\
 &\quad+Ce^{-\beta^2s/a^2}
   \cos\bigl(\beta(z-vs)-\psi\bigr).
 \end{aligned}
 \tag{W.9}
\]

The exact scalar equation becomes

\[
 \partial_sG+v\partial_zG-a^{-2}\partial_z^2G=0.
 \tag{W.10}
\]

Put `I=[-1/2,1/2]` and

\[
 h(s)=\int_I|G(s,z)|^3\,dz,
 \qquad H=\int_0^4h(s)\,ds.
 \tag{W.11}
\]

The proof below bounds the dimensionless signed flux by `CH^(2/3)`.

## 3. A confluent spatial observation lemma

**Lemma W.1.**  Fix `K<infinity` and compact intervals `I` and `J`, with
`I` having nonempty interior.  There is `C=C(K,I,J)` such that every real
or complex solution of

\[
 (\partial_z^2+\alpha^2)(\partial_z^2+\beta^2)g=0,
 \qquad 0\le\alpha,\beta\le K,
 \tag{W.12}
\]

obeys

\[
 \boxed{
 \|g\|_{L^\infty(J)}+\|g'\|_{L^\infty(J)}
 \le C\|g\|_{L^3(I)}.}
 \tag{W.13}
\]

This includes `alpha=beta` and `alpha=beta=0`.  In the latter limit the
solution space is the cubic-polynomial space, so the lemma retains the
worst confluent cancellation, including the explicit cubic node above,
rather than assuming separated frequencies.

To prove it, write `X=(g,g',g'',g''')`.  Equation W.12 is the first-order
system

\[
 X'=\mathbb A_{\alpha,\beta}X,
 \qquad
 \mathbb A_{\alpha,\beta}=
 \begin{pmatrix}
 0&1&0&0\\0&0&1&0\\0&0&0&1\\
 -\alpha^2\beta^2&0&-(\alpha^2+\beta^2)&0
 \end{pmatrix}.
 \tag{W.14}
\]

The matrices form a compact bounded family.  Gronwall therefore propagates
the initial jet uniformly from `I` to `J`.  If the initial jet were not
controlled by the `L^3(I)` norm, a normalized countersequence would have
convergent parameters and initial jets.  Continuous dependence for W.14
would give a nonzero limiting solution that vanishes almost everywhere on
`I`, hence vanishes identically, a contradiction.  This proves W.13.

## 4. A frequency-gap-free terminal trace

**Lemma W.2.**  Fix `Lambda<infinity`.  If

\[
 q(s)=\sum_{j=1}^{N}c_je^{\lambda_js},
 \qquad N\le4,\qquad |\operatorname {Re}\lambda_j|\le\Lambda,
 \tag{W.15}
\]

then

\[
 \boxed{|q(4)|^3\le C_\Lambda\int_0^4|q(s)|^3\,ds.}
 \tag{W.16}
\]

The constant is independent of the imaginary parts of the exponents and
of the gaps between them.  This is a direct `L^3` consequence of the
Turan--Nazarov inequality

\[
 \sup_{[0,4]}|q|
 \le e^{4\max_j|\operatorname {Re}\lambda_j|}
 \left(\frac{4C}{|E|}\right)^{N-1}\sup_E|q|
 \tag{W.17}
\]

for a measurable `E` of positive measure.  Take `E` to be the half-measure
sublevel set supplied by Chebyshev's inequality.  Nazarov's original result
allows complex exponents and has no imaginary-frequency or gap factor; an
accessible primary restatement is recorded in the source report.

For each fixed `z`, W.9 is an exponential polynomial in `s` with at most
four terms and exponents

\[
 -\alpha^2/a^2\pm i\alpha v,
 \qquad -\beta^2/a^2\pm i\beta v.
 \tag{W.18}
\]

Their real parts are uniformly bounded in the low-carrier sector.  Applying
W.16 pointwise in `z` and integrating over `I` gives

\[
 \boxed{h(4)\le C H.}
 \tag{W.19}
\]

This is the required right-endpoint trace.  It remains uniform as
`v` tends to zero or infinity and as the two frequencies coalesce.

## 5. Scaled radial primitive

Let the frozen radial profile be `vartheta`, as in R0.75R--V, and define

\[
 W_a(z)=-2\pi a z\vartheta\bigl(a(|z|-1)\bigr),
 \qquad
 \Xi_a(z)=\int_{-\infty}^{z}W_a(r)\,dr.
 \tag{W.20}
\]

Oddness gives `int W_a=0`, so `Xi_a` is compactly supported.  Once
`a>=max(1,2delta)`, its support lies in `J=[-3/2,3/2]`, and direct scaling
of the two fixed-width transition intervals gives

\[
 \|W_a\|_{L^1}+\|\Xi_a\|_{L^1}
 +\|\Xi_a\|_{L^\infty}\le C,
 \qquad
 \|\Xi_a''\|_{L^1}=\|W_a'\|_{L^1}\le Ca.
 \tag{W.21}
\]

The exact cross-sectional derivative satisfies

\[
 \int_{-\pi}^{\pi}D_R(y)F(t,y)^2\,dy
 =aR^2\int_{\mathbb R}W_a(z)G(s,z)^2\,dz.
 \tag{W.22}
\]

With `zeta(s)=eta_R(R^2s)`, equations W.8 and W.22 give the exact flux
scaling

\[
 \boxed{
 \mathcal T_{k,m,R}
 =\frac{a^2R^3}{2}v
 \int_0^4\!\zeta(s)
 \int_{\mathbb R}W_a(z)G(s,z)^2\,dzds.}
 \tag{W.23}
\]

## 6. The low-carrier local energy identity

Set `Q=G^2`.  Equation W.10 gives

\[
 \partial_sQ+v\partial_zQ-a^{-2}\partial_z^2Q
 =-2a^{-2}|\partial_zG|^2.
 \tag{W.24}
\]

Let `E(s)=int Xi_a G^2`.  Since `W_a=Xi_a'`, integration by parts in `z`
and W.24 yield the exact identity

\[
 v\int W_aG^2
 =E'(s)-a^{-2}\int\Xi_a''G^2
 +2a^{-2}\int\Xi_a|\partial_zG|^2.
 \tag{W.25}
\]

Multiplying by `zeta`, integrating on `[0,4]`, and using `zeta(0)=0`
gives

\[
 \begin{aligned}
 v\int_0^4\zeta\int W_aG^2
 &=\zeta(4)E(4)-\int_0^4\zeta'E\,ds\\
 &\quad-a^{-2}\int_0^4\zeta\int\Xi_a''G^2\,dzds\\
 &\quad+2a^{-2}\int_0^4\zeta\int\Xi_a|\partial_zG|^2\,dzds.
 \end{aligned}
 \tag{W.26}
\]

At each time, G satisfies W.12 with `K=2C_0`.  Lemma W.1 and W.21 imply

\[
 |E(s)|+a^{-2}\left|\int\Xi_a''G^2\right|
 +a^{-2}\int|\Xi_a||\partial_zG|^2
 \le Ch(s)^{2/3}.
 \tag{W.27}
\]

For the terminal row, apply Lemma W.1 first and W.19 second:

\[
 |E(4)|\le Ch(4)^{2/3}\le CH^{2/3}.
 \tag{W.28}
\]

The remaining rows in W.26 are bounded by W.27, the cutoff bounds, and
Holder on the fixed time interval.  Therefore

\[
 \boxed{
 \left|v\int_0^4\zeta\int W_aG^2\right|
 \le CH^{2/3}.}
 \tag{W.29}
\]

No division by `v`, `alpha-beta`, or either frequency occurs.  The identity
keeps the endpoint, cutoff, heat, and dissipation rows together, including
the cancellations that are lost by integrating the four Fourier rows
separately.

## 7. Return to physical scales

The exact plateau-fibre area from R0.75T is `4pi a delta_0 R^2` for every
`|x_2|<=ell/2`.  Equations W.8 and W.11 therefore give

\[
 \boxed{
 M_{k,m,R}^{\rm plat}
 \ge4\pi\delta_0a^2R^5H.}
 \tag{W.30}
\]

Combining W.23, W.29, and W.30 proves, throughout `maR<C_0`,

\[
 |\mathcal T_{k,m,R}|
 \le Ca^2R^3H^{2/3}
 \le Ca^{2/3}R^{-1/3}
 \bigl(M_{k,m,R}^{\rm plat}\bigr)^{2/3}.
 \tag{W.31}
\]

R0.75V gives the same estimate when `maR>=C_0`; W.7 and W.31 partition
all possibilities.  This proves W.2.  Substitution of W.3 proves W.4, with
the same exact rate `-c_gamma/12=-2/11907`.

## 8. Exact-solution and Version-M boundary

The pair W.1 satisfies

\[
 \partial_tF+B\partial_2F-\partial_2^2F=0
 \tag{W.32}
\]

and embeds in the exact smooth unforced shear `u=(0,B,F(t,x_2))` with
constant pressure.  The constant background has not been shown to belong
to the frozen mean-zero, inversion-paired Version-M subclass.

If the complete clock and plateau tube belong to the same scale-`2R`
Version-M measurement row of weight at least `omega`, and `F` is an actual
component of that same velocity, then

\[
 p_{k,m,R}^{\rm plat}\le CP_R^M,
 \qquad
 \mathfrak X_{k,m,R}\le C(P_R^M)^{2/3}.
 \tag{W.33}
\]

This last implication remains conditional on the realized-subclass and
ledger-alignment hypotheses.  It is not valid merely because W.1 is a
Fourier projection of a larger field.

## 9. What is closed and what remains open

**Closed here:** the low-carrier sector for one exact diffusive dyadic pair;
the frequency-gap-free spatial and terminal observations needed by the
local energy identity; and, after combining with V, the full-frequency
two-harmonic signed-flux estimate and its scale-free normalization.

**Open:** three or more harmonics; arbitrary dyadic packets; inter-packet
aggregation; nonconstant or vertically dependent shear; projection from a
larger velocity; arbitrary-field E.24; complete Version-M extraction; fixed
deletion; suitable-weak transfer; regularity; and singularity.

The proof is analytic.  A numerical plot would neither certify the compact
ODE lemma nor the Turan--Nazarov trace, so no formal scientific figure or
simulation is claimed for this section.  No novelty or priority claim is
made.  R0.75W is not a proof of global regularity.  **NOT CLAY.**
