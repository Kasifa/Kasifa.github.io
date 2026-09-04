# R0.75V -- complete signed-flux payment for one dyadic two-harmonic shear

## 0. Result and exact boundary

R0.75T proves sharp collar coercivity for one two-harmonic dyadic pair.
R0.75U uses that coercivity to pay the low difference-frequency row of the
signed flux.  Three coupled rows remain: the two self frequencies `2k,2m`
and the sum frequency `k+m`.  Bounding those rows separately destroys the
cancellation measured by the T defect.  This note keeps their quadratic
combination intact and closes the exact two-harmonic calculation.

Let

\[
 \begin{aligned}
 F(t,x_2)&=A_t\cos(kx_2-\phi_t)
          +C_t\cos(mx_2-\psi_t),\\
 A_t&=Ae^{-k^2t},\qquad C_t=Ce^{-m^2t},\\
 \phi_t&=\phi+kBt,\qquad\psi_t=\psi+mBt,
 \end{aligned}
 \tag{V.1}
\]

where `A,C>=0`, `1<=m<k<=2m`, `d=k-m`, and `maR>=C_0`, with the same
carrier threshold as R0.75T.  Put `n=k+m` and let

\[
 \begin{aligned}
 \mathcal E_{k,m,R}
 &:=\frac B4\int_0^{T_R}\eta_R(t)
 \left[A_t^2J_{2k,R}\sin(2\phi_t)
      +C_t^2J_{2m,R}\sin(2\psi_t)\right]dt\\
 &\quad+\frac B2\int_0^{T_R}\eta_R(t)A_tC_t
 J_{n,R}\sin(\phi_t+\psi_t)\,dt.
 \end{aligned}
 \tag{V.2}
\]

This is exactly the self/sum block left open in U.  There is a constant
depending only on the frozen radial profile, plateau width, carrier
threshold, and time cutoff such that

\[
 \boxed{
 |\mathcal E_{k,m,R}|
 \le Ca^{2/3}R^{-1/3}
 \bigl(M_{k,m,R}^{\rm plat}\bigr)^{2/3}.}
 \tag{V.3}
\]

Combining V.3 with the R0.75U difference-frequency estimate gives the full
exact signed collar flux

\[
 \boxed{
 |\mathcal T_{k,m,R}|
 \le Ca^{2/3}R^{-1/3}
 \bigl(M_{k,m,R}^{\rm plat}\bigr)^{2/3}.}
 \tag{V.4}
\]

With

\[
 p_{k,m,R}^{\rm plat}=R^{-2}\omega M_{k,m,R}^{\rm plat},
 \qquad
 \mathfrak X_{k,m,R}=\frac\omega R[\mathcal T_{k,m,R}]_+,
 \tag{V.5}
\]

equation V.4 becomes

\[
 \boxed{
 \mathfrak X_{k,m,R}
 \le Ca^{2/3}\omega^{1/3}
 \bigl(p_{k,m,R}^{\rm plat}\bigr)^{2/3}.}
 \tag{V.6}
\]

All powers of `R` cancel, and the exact logarithmic `L^2` rate is

\[
 \lim_{L\to\infty}\frac1{L^2}
 \log(a^{2/3}\omega^{1/3})=-\frac2{11907}<0.
 \tag{V.7}
\]

This is a complete flux theorem only for the exact high-carrier dyadic pair
V.1.  It is not an arbitrary two-mode projection theorem and not an
arbitrary-field estimate.

## 1. Frozen inputs and the four-frequency split

Retain

\[
 a=pL,\qquad R=e^{-\rho L^2/4},\qquad T_R=4R^2,
 \qquad \ell=aR,
 \tag{V.8}
\]

and the frozen time cutoff

\[
 0\le\eta_R\le1,\qquad \eta_R(0)=0,
 \qquad |\eta_R'(t)|\le C_\eta R^{-2}.
 \tag{V.9}
\]

The immediately used frozen inputs are

| input | SHA-256 | role |
|---|---|---|
| `research/r075b_bulk_clock_outer_padding_gate.md` | `430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a` | complete clock and cutoff onset |
| `research/r075r_outer_cap_spectral_concentration_obstruction.md` | `e5eba5b262a8e140eaa149b6d914f355f2f3c636ec1e74cf85515f1c38fd32f3` | exact radial cross section |
| `research/r075t_two_harmonic_collar_coercivity.md` | `822059f8a6248143ff3f36938a2333bee9f909b9166db951e227c426c2e8bc66` | two-wave defect and plateau mass |
| `research/r075u_two_harmonic_difference_frequency_payment.md` | `f9fb331cf880b20f3b407fe66453bce71517ac1ef2af4fa0863c00325c1022a4` | difference-frequency payment |

Write

\[
 J_{r,R}=\int_{-\pi}^{\pi}D_R(y)\sin(ry)\,dy,
 \qquad D_R(y)=-2\pi y\vartheta(|y|/R-a).
 \tag{V.10}
\]

The exact expansion from T is

\[
 \begin{aligned}
 \mathcal T_{k,m,R}
 &=\mathcal E_{k,m,R}+\mathcal D_{k,m,R},\\
 \mathcal D_{k,m,R}
 &=\frac B2J_{d,R}\int_0^{T_R}\eta_R A_tC_t
 \sin(\phi_t-\psi_t)\,dt.
 \end{aligned}
 \tag{V.11}
\]

R0.75U already proves V.3 with `mathcal E` replaced by `mathcal D`.
It therefore remains to prove V.3 without taking absolute values inside the
three-row combination V.2.

## 2. Radial quotient and its two-jet

For real `r>0`, define the smooth quotient

\[
 K_R(r):=\frac{J_{r,R}}r.
 \tag{V.12}
\]

The formula in V.10 extends `K_R` smoothly and evenly through `r=0`.
After `y=Rz`, differentiation under the integral and integration by parts in
`z` give, for `j=0,1,2` and every integer `N>=0`,

\[
 \boxed{
 |\partial_r^jK_R(r)|
 \le C_{j,N}a^{j+2}R^{j+3}(1+rR)^{-N}.}
 \tag{V.13}
\]

Indeed, each `r` derivative supplies one factor `Rz`, the support consists
of two fixed-width intervals with `|z|` comparable to `a`, and the frozen
profile is smooth.  For `rR<=1`, the direct moment bound gives V.13.  For
`rR>=1`, arbitrary integration by parts gives the last factor.

Set

\[
 q=nR,\qquad \varepsilon=\min\{1,d\ell\},
 \qquad \Lambda_N=C_Na^2R^3(1+q)^{-N}.
 \tag{V.14}
\]

Since `d<=n/3`, all three arguments `n-d,n,n+d` are comparable to `n`.
Since `n\ell>=2maR>=2C_0`, also

\[
 \frac dn\le C\varepsilon.
 \tag{V.15}
\]

Taylor's theorem, V.13, and the direct bound when `dell>=1` imply

\[
 \begin{aligned}
 |K_R(n)|+\left|\frac{K_R(n+d)+K_R(n-d)}2\right|
 &\le\Lambda_N,\\
 \left|\frac{K_R(n+d)-K_R(n-d)}2\right|
 &\le\Lambda_N\varepsilon,\\
 \left|\frac{K_R(n+d)+K_R(n-d)}2-K_R(n)\right|
 &\le\Lambda_N\varepsilon^2.
 \end{aligned}
 \tag{V.16}
\]

The same statement holds for

\[
 L_R(r):=\frac{r^2}2K_R(r),
 \tag{V.17}
\]

with `Lambda_N` replaced by `C n^2 Lambda_N`.  Terms produced by
differentiating `r^2` carry `d/n` or `(d/n)^2` and are absorbed by V.15.

## 3. The quadratic cancellation lemma

Let

\[
 \Delta_t=\phi_t-\psi_t,
 \qquad
 \delta_t=\operatorname {dist}
 (\Delta_t,\pi+2\pi\mathbb Z),
 \tag{V.18}
\]

and retain the T defect

\[
 H(t)^2=(A_t-C_t)^2+A_tC_t
 \min\{1,(d\ell)^2+\delta_t^2\}.
 \tag{V.19}
\]

Put `u=A_t exp(i Delta_t/2)` and
`v=C_t exp(-i Delta_t/2)`.  Then

\[
 |u+v|^2\le CH(t)^2,
 \qquad \varepsilon(A_t+C_t)\le CH(t).
 \tag{V.20}
\]

Consider any real multiplier triple `G_+,G_0,G_-` satisfying V.16 with
size `Lambda`.  Its quadratic combination can be written exactly as

\[
 \begin{aligned}
 &G_+A_t^2e^{i\Delta_t}+2G_0A_tC_t
  +G_-C_t^2e^{-i\Delta_t}\\
 &\quad=\overline G\,(u+v)^2
 +2A_tC_t(G_0-\overline G)
 +G_\Delta(u^2-v^2),
 \end{aligned}
 \tag{V.21}
\]

where `overline G=(G_++G_-)/2` and
`G_Delta=(G_+-G_-)/2`.  Equations V.16 and V.20 give

\[
 \boxed{
 |G_+A_t^2e^{i\Delta_t}+2G_0A_tC_t
  +G_-C_t^2e^{-i\Delta_t}|
 \le C\Lambda H(t)^2.}
 \tag{V.22}
\]

The last term uses
`|u^2-v^2|<=|u+v|(A_t+C_t)`.  Thus the first multiplier difference is
paired with one factor of the beat defect and the second difference with
two factors.  This is the cancellation lost by three separate absolute
values.

Apply V.22 first to

\[
 G_+=K_R(2k),\qquad G_0=K_R(n),
 \qquad G_-=K_R(2m).
 \tag{V.23}
\]

For the heat row, apply it to `L_R(2k),L_R(n),L_R(2m)`.  The actual cross
coefficient differs from the central one by

\[
 (k^2+m^2)K_R(n)-\frac{n^2}2K_R(n)
 =\frac{d^2}2K_R(n).
 \tag{V.24}
\]

This remainder is also bounded by `C n^2 Lambda_N H(t)^2`, because
`(d/n)^2A_tC_t<=C H(t)^2` by V.15 and V.19.  Consequently the cutoff and
heat quadratic forms obey

\[
 |Q_K(t)|\le C\Lambda_NH(t)^2,
 \qquad
 |Q_L(t)|\le Cn^2\Lambda_NH(t)^2.
 \tag{V.25}
\]

## 4. Exact time integration by parts

For a self phase, direct differentiation gives

\[
 \int_0^{T_R}B g(t)\sin(2\phi+2kBt)\,dt
 =-\left[\frac{g(t)\cos(2\phi+2kBt)}{2k}\right]_0^{T_R}
 +\int_0^{T_R}\frac{g'(t)}{2k}
 \cos(2\phi+2kBt)\,dt.
 \tag{V.26}
\]

The corresponding identity for the sum phase has denominator `n`.
Use V.26 separately on all three rows of V.2.  Because `eta_R(0)=0`, the
initial boundary vanishes.  Factoring the common phase
`Sigma_t=phi_t+psi_t` after, not before, the integrations gives the exact
identity

\[
 \begin{aligned}
 \mathcal E_{k,m,R}
 &=-\frac{\eta_R(T_R)}4
 \operatorname {Re}\!\left(e^{i\Sigma_{T_R}}Q_K(T_R)\right)\\
 &\quad+\frac14\int_0^{T_R}\eta_R'(t)
 \operatorname {Re}\!\left(e^{i\Sigma_t}Q_K(t)\right)dt\\
 &\quad-\frac14\int_0^{T_R}\eta_R(t)
 \operatorname {Re}\!\left(e^{i\Sigma_t}Q_L(t)\right)dt,
 \end{aligned}
 \tag{V.27}
\]

where

\[
 \begin{aligned}
 Q_K(t)&=A_t^2K_R(2k)e^{i\Delta_t}
       +2A_tC_tK_R(n)
       +C_t^2K_R(2m)e^{-i\Delta_t},\\
 Q_L(t)&=2k^2A_t^2K_R(2k)e^{i\Delta_t}
       +2(k^2+m^2)A_tC_tK_R(n)
       +2m^2C_t^2K_R(2m)e^{-i\Delta_t}.
 \end{aligned}
 \tag{V.28}
\]

No derivative of the relative phase occurs in V.27.  Integrating after a
premature common-phase factorization would create an unnecessary `dB`
term and would obscure the exact cancellation.

## 5. Complete-clock trace for the beat defect

Set

\[
 I_H:=\int_0^{T_R}H(t)^3\,dt.
 \tag{V.29}
\]

Holder immediately gives

\[
 \int_0^{T_R}H(t)^2\,dt
 \le T_R^{1/3}I_H^{2/3}
 \le CR^{2/3}I_H^{2/3}.
 \tag{V.30}
\]

The endpoint in V.27 needs one further elementary fact.

**Lemma V.1.**  With `q=nR`,

\[
 \boxed{
 (1+q)^{-8}H(T_R)^2
 \le CR^{-4/3}I_H^{2/3}.}
 \tag{V.31}
\]

To prove it, scale `t=R^2s`, so the clock is `[0,4]`, and write
`x=A_(T_R)`, `y=C_(T_R)`.  Backwards from the terminal time,

\[
 A_{R^2s}\ge x,\qquad C_{R^2s}\ge y.
 \tag{V.32}
\]

For every affine phase and every fixed `epsilon>=0`, direct integration on
the affine pieces of the periodic distance function gives

\[
 \int_0^4\min\{1,\varepsilon^2+
 \operatorname {dist}(\alpha+\sigma s,
 \pi+2\pi\mathbb Z)^2\}^{3/2}ds
 \ge c\min\{1,\varepsilon^2+
 \operatorname {dist}(\alpha+4\sigma,
 \pi+2\pi\mathbb Z)^2\}^{3/2}.
 \tag{V.33}
\]

For `|sigma|<=1`, this is the cubic mean of finitely many affine pieces;
for `|sigma|>=1`, a fixed fraction of a period has distance bounded below.
Equations V.19, V.32, and V.33 pay the terminal product-phase term
`xy min{1,(dell)^2+delta_(T_R)^2}`.

It remains to pay `|x-y|^2`.  Put `epsilon=min{1,dell}`.  If `xy=0`, one
amplitude vanishes on the whole clock and the other is no smaller backwards,
so the required cubic lower bound is immediate.  Suppose `xy>0`.  If
`|x-y|<=4epsilon sqrt(xy)`, that term is already bounded by the
product-phase term.  Otherwise, the backward amplitude ratio is monotone,
and its logarithmic speed is

\[
 (k^2-m^2)R^2=dnR^2.
 \tag{V.34}
\]

On a terminal subinterval of length at least `c(1+q^2)^(-1)` in the
`s` variable, the ratio stays at least a fixed fraction of its terminal
distance from one and the common heat factor changes by at most a fixed
factor.  Indeed, when `dell<=1`, the ratio speed divided by `epsilon` is
`q/a`; when `dell>=1`, V.34 is at most `q^2/3`.  Hence

\[
 \int_0^4|A_{R^2s}-C_{R^2s}|^3ds
 \ge c(1+q^2)^{-1}|x-y|^3.
 \tag{V.35}
\]

The `2/3` power of V.35, together with the product-phase row, proves

\[
 H(T_R)^2
 \le C(1+q^2)^{2/3}
 \left(R^{-2}I_H\right)^{2/3}.
 \tag{V.36}
\]

Multiplication by `(1+q)^(-8)` proves V.31.

## 6. Payment of the self/sum block

Choose `N=8` in V.14--V.25 and abbreviate `w_q=(1+q)^(-8)`.
Equations V.25 and V.27 give

\[
 \begin{aligned}
 |\mathcal E_{k,m,R}|
 &\le Ca^2R^3w_q H(T_R)^2\\
 &\quad+Ca^2R^3w_qR^{-2}\int_0^{T_R}H(t)^2dt\\
 &\quad+Ca^2R^3w_qn^2\int_0^{T_R}H(t)^2dt.
 \end{aligned}
 \tag{V.37}
\]

Use V.30--V.31 and `q^2w_q<=C`.  Every row in V.37 is bounded by

\[
 Ca^2R^{5/3}I_H^{2/3}.
 \tag{V.38}
\]

R0.75T gives

\[
 M_{k,m,R}^{\rm plat}\ge ca^2R^3I_H.
 \tag{V.39}
\]

Substitution of V.39 into V.38 yields

\[
 a^2R^{5/3}
 \left(\frac{M_{k,m,R}^{\rm plat}}{a^2R^3}\right)^{2/3}
 =a^{2/3}R^{-1/3}
 \bigl(M_{k,m,R}^{\rm plat}\bigr)^{2/3},
 \tag{V.40}
\]

which proves V.3.

## 7. Full flux and normalization

Equation V.11 and the triangle inequality applied only after both coupled
blocks have been proved give

\[
 |\mathcal T_{k,m,R}|
 \le|\mathcal E_{k,m,R}|+|\mathcal D_{k,m,R}|.
 \tag{V.41}
\]

R0.75U and V.3 therefore prove V.4.  Substituting
`M=R^2 omega^(-1)p` into `(omega/R)V.4` gives V.6.  With the frozen values
`a=pL` and `omega=exp[-(c_gamma/4)L^2]`, the polynomial factor from `a`
does not affect the `L^2` rate, and `-c_gamma/12=-2/11907`, proving V.7.

## 8. Exact-solution and Version-M boundary

The field V.1 solves

\[
 \partial_tF+B\partial_2F-\partial_2^2F=0
 \tag{V.42}
\]

and embeds in the exact smooth unforced shear `u=(0,B,F(t,x_2))` with
constant pressure.  The nonzero constant background has not been shown to
belong to the frozen mean-zero, inversion-paired Version-M subclass.

If the complete clock and plateau tube belong to the same scale-`2R`
Version-M measurement row of weight at least `omega`, and `F` is an actual
component of that same velocity, then

\[
 p_{k,m,R}^{\rm plat}\le CP_R^M
 \tag{V.43}
\]

and V.6 pays the full exact two-harmonic collar flux by
`C(P_R^M)^(2/3)`.  This is conditional on the realized-subclass and
ledger-alignment hypotheses.  It is not a bound for a Fourier projection of
a larger velocity.

## 9. What is closed and what remains open

**Closed here:** the joint self/sum block; together with U, the complete
signed collar flux of one exact diffusive two-harmonic dyadic pair with
`maR>=C_0`; the scale-free normalization and exact negative coefficient
rate.

**Open:** low-carrier pairs; three or more harmonics; arbitrary dyadic
packets; inter-packet aggregation; nonconstant or vertically dependent
shear; projection from a larger velocity; arbitrary-field E.24; complete
Version-M extraction; fixed deletion; suitable-weak transfer; regularity;
singularity.

R0.75V is a finite-dimensional exact-subfamily theorem.  It does not prove
that the general three-dimensional Navier--Stokes solution is smooth.
**NOT CLAY.**
