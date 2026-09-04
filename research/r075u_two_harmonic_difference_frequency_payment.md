# R0.75U -- complete-clock payment of the dyadic-pair difference frequency

## 0. Result and exact boundary

R0.75T converts the local cubic mass of one two-harmonic dyadic pair into a
sharp scalar beat defect.  The open row T.31 asks whether that defect pays the
low difference-frequency part of the signed collar flux uniformly in the
constant shear speed.  This note answers that question affirmatively.

Let

\[
 \begin{aligned}
 F(t,x_2)&=A_t\cos(kx_2-\phi_t)
          +C_t\cos(mx_2-\psi_t),\\
 A_t&=Ae^{-k^2t},\qquad C_t=Ce^{-m^2t},\\
 \phi_t&=\phi+kBt,\qquad\psi_t=\psi+mBt,
 \end{aligned}
 \tag{U.1}
\]

where `A,C>=0`, `1<=m<k<=2m`, `d=k-m`, and `maR>=C_0`, with `C_0`
the carrier threshold in R0.75T.  Set

\[
 \mathcal D_{k,m,R}
 :=\frac B2J_{d,R}\int_0^{T_R}
 \eta_R(t)A_tC_t\sin(\phi_t-\psi_t)\,dt,
 \tag{U.2}
\]

where

\[
 J_{n,R}:=\int_{-\pi}^{\pi}D_R(y)\sin(ny)\,dy,
 \qquad D_R(y)=-2\pi y\vartheta(|y|/R-a).
 \tag{U.3}
\]

Then, uniformly in both frequencies, amplitudes, phases, and `B`,

\[
 \boxed{
 |\mathcal D_{k,m,R}|
 \le Ca^{2/3}R^{-1/3}
 \bigl(M_{k,m,R}^{\rm plat}\bigr)^{2/3}.}
 \tag{U.4}
\]

With

\[
 p_{k,m,R}^{\rm plat}:=R^{-2}\omega M_{k,m,R}^{\rm plat},
 \qquad
 \mathfrak X_{k,m,R}^{\rm diff}
 :=\frac\omega R[\mathcal D_{k,m,R}]_+,
 \tag{U.5}
\]

the normalized bound is

\[
 \boxed{
 \mathfrak X_{k,m,R}^{\rm diff}
 \le Ca^{2/3}\omega^{1/3}
 \bigl(p_{k,m,R}^{\rm plat}\bigr)^{2/3}.}
 \tag{U.6}
\]

All powers of `R` cancel.  The exact logarithmic `L^2` coefficient is again

\[
 \lim_{L\to\infty}\frac1{L^2}
 \log(a^{2/3}\omega^{1/3})=-\frac{c_\gamma}{12}
 =-\frac2{11907}<0.
 \tag{U.7}
\]

This proves the difference-frequency target T.31.  It does not yet pay the
two self frequencies `2k,2m` and the sum frequency `k+m` as a combined
quantity, so it is not a complete two-harmonic flux theorem.

## 1. Frozen inputs and the radial row

Retain `T_R=4R^2`, the frozen nondecreasing cutoff with

\[
 0\le\eta_R\le1,\qquad \eta_R(0)=0,
 \qquad |\eta_R'(t)|\le C_\eta R^{-2},
 \tag{U.8}
\]

after translating the left endpoint of the clock to zero.  The immediately
used frozen inputs are

| input | SHA-256 | role |
|---|---|---|
| `research/r075b_bulk_clock_outer_padding_gate.md` | `430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a` | complete clock and cutoff onset |
| `research/r075r_outer_cap_spectral_concentration_obstruction.md` | `e5eba5b262a8e140eaa149b6d914f355f2f3c636ec1e74cf85515f1c38fd32f3` | exact radial cross section |
| `research/r075s_full_frequency_single_harmonic_clock_payment.md` | `d2736eaa43443048bd620567c4acd72024dc4c662320a8aa58af31ccc6047ccd` | radial sine rows and phase-distance method |
| `research/r075t_two_harmonic_collar_coercivity.md` | `822059f8a6248143ff3f36938a2333bee9f909b9166db951e227c426c2e8bc66` | sharp dyadic-pair beat defect |

Scaling `y=Rz` in U.3 gives, exactly as in the one-harmonic row,

\[
 |J_{n,R}|\le CaR^2\min\{naR,1\}.
 \tag{U.9}
\]

Both entries imply the single bound needed here:

\[
 \boxed{\frac{|J_{n,R}|}{n}\le Ca^2R^3
 \qquad(n\ge1).}
 \tag{U.10}
\]

Indeed, use the first entry when `naR<=1`; otherwise `n^(-1)<=aR`
and use the second.

## 2. A weighted moving-phase lemma

The time estimate is independent of the carrier frequencies after
nondimensionalization.

**Lemma U.1.**  Let `zeta` be absolutely continuous on `[0,4]`, with

\[
 0\le\zeta\le1,\qquad \zeta(0)=0,
 \qquad |\zeta'|\le C_\eta.
 \tag{U.11}
\]

For every `Lambda>=0`, `sigma in R`, and `alpha in R`, define

\[
 h(s):=\min\{1,\operatorname {dist}
 (\alpha+\sigma s,\pi+2\pi\mathbb Z)\}.
 \tag{U.12}
\]

Then

\[
 \boxed{
 \left|\sigma\int_0^4\zeta(s)e^{-\Lambda s}
 \sin(\alpha+\sigma s)\,ds\right|
 \le C
 \left(\int_0^4e^{-3\Lambda s/2}h(s)^3\,ds
 \right)^{2/3}.}
 \tag{U.13}
\]

The constant depends only on `C_eta`.

### 2.1 The phase-distance moment

Put

\[
 \tau:=\begin{cases}
  1,&0\le\Lambda\le1,\\
  \Lambda^{-1},&\Lambda\ge1,
 \end{cases}
 \qquad
 r:=h(0),\qquad
 q:=\min\{1,r+|\sigma|\tau\}.
 \tag{U.14}
\]

On `[0,tau]`, the exponential weight is bounded below by `e^(-3/2)`.
The distance to `pi+2pi Z` is a periodic triangular wave.  Integrating one
affine segment, and splitting only when a corner is crossed, gives

\[
 \int_0^\tau h(s)^3\,ds\ge c\tau q^3.
 \tag{U.15}
\]

The estimate includes intervals that cross the cancelling phase: for an
affine distance decreasing from `r` to zero, its cubic mean is `r^3/4`, so
there is no loss at a phase node.  Consequently

\[
 \left(\int_0^4e^{-3\Lambda s/2}h(s)^3\,ds
 \right)^{2/3}
 \ge c\tau^{2/3}q^2.
 \tag{U.16}
\]

### 2.2 Slow phase on the effective heat interval

Assume `|sigma|tau<=1`.  If `Lambda<=1`, then `tau=1`, and on `[0,4]`

\[
 |\sin(\alpha+\sigma s)|\le Cq.
 \tag{U.17}
\]

Therefore the left side of U.13 is at most `C|sigma|q<=Cq^2`, because
`q>=c|sigma|`.

If `Lambda>=1`, U.11 gives `zeta(s)<=C_eta s`.  The elementary Laplace
moments yield

\[
 \begin{aligned}
 &|\sigma|\int_0^4\zeta(s)e^{-\Lambda s}
 |\sin(\alpha+\sigma s)|\,ds\\
 &\qquad\le C|\sigma|
 \int_0^\infty se^{-\Lambda s}
 \min\{1,r+|\sigma|s\}\,ds\\
 &\qquad\le C|\sigma|\tau^2q
 \le C\tau q^2
 \le C\tau^{2/3}q^2.
 \end{aligned}
 \tag{U.18}
\]

Together with U.16, this proves the slow-phase case.

### 2.3 Fast phase on the effective heat interval

Assume `|sigma|tau>=1`; then `q=1`.  Put
`w(s)=zeta(s)e^(-Lambda s)`.  Since `w(0)=0`, one integration by parts gives

\[
 \left|\sigma\int_0^4w(s)\sin(\alpha+\sigma s)\,ds\right|
 \le |w(4)|+\int_0^4|w'(s)|\,ds.
 \tag{U.19}
\]

If `Lambda<=1`, the right side is bounded by a constant.  If
`Lambda>=1`, use `zeta(s)<=C_eta s` to obtain

\[
 |w(4)|+\int_0^4|w'|
 \le C\left(\Lambda^{-1}
 +\Lambda\int_0^\infty se^{-\Lambda s}\,ds\right)
 \le C\tau.
 \tag{U.20}
\]

Since `0<tau<=1`, both cases are at most `C tau^(2/3)`.  Equation U.16
with `q=1` proves the fast-phase case and completes Lemma U.1.

## 3. Application to the exact dyadic pair

If `AC=0`, the difference-frequency flux U.2 vanishes and U.4 is immediate.
Assume below that `AC>0`.

Scale time by

\[
 t=R^2s,\qquad
 \Lambda=(k^2+m^2)R^2,\qquad
 \sigma=dBR^2,
 \tag{U.21}
\]

and set `zeta(s)=eta_R(R^2s)`.  Equation U.8 gives U.11.  Let

\[
 h(s)=\min\{1,\operatorname {dist}
 (\phi-\psi+\sigma s,\pi+2\pi\mathbb Z)\}.
 \tag{U.22}
\]

The R0.75T defect, evaluated at `t=R^2s`, obeys

\[
 H_{d,aR}(R^2s)^2
 \ge A_{R^2s}C_{R^2s}h(s)^2
 =ACe^{-\Lambda s}h(s)^2.
 \tag{U.23}
\]

Hence Lemma U.1 implies

\[
 \begin{aligned}
 &\left|B\int_0^{T_R}\eta_R(t)A_tC_t
 \sin(\phi-\psi+dBt)\,dt\right|\\
 &\qquad\le\frac C{dR^{4/3}}
 \left(\int_0^{T_R}H_{d,aR}(t)^3\,dt\right)^{2/3}.
 \end{aligned}
 \tag{U.24}
\]

The amplitude product cancels exactly: the left side is `AC/d` times the
left side of U.13, while U.23 contributes `(AC)^(3/2)` inside the cubic
integral.

Multiply U.24 by `|J_(d,R)|/2` and use U.10:

\[
 |\mathcal D_{k,m,R}|
 \le Ca^2R^{5/3}
 \left(\int_0^{T_R}H_{d,aR}(t)^3\,dt\right)^{2/3}.
 \tag{U.25}
\]

R0.75T gives

\[
 M_{k,m,R}^{\rm plat}
 \ge ca^2R^3\int_0^{T_R}H_{d,aR}(t)^3\,dt.
 \tag{U.26}
\]

Substitution of U.26 into U.25 proves U.4.  Substitution of U.5 then proves
U.6, including the exact cancellation of the `R` powers.

## 4. Exact-solution and Version-M boundary

The pair U.1 is a solution of

\[
 \partial_tF+B\partial_2F-\partial_2^2F=0.
 \tag{U.27}
\]

It embeds in the exact smooth unforced shear `u=(0,B,F(t,x_2))` with constant
pressure.  Its nonzero constant background has not been shown to belong to
the frozen mean-zero, inversion-paired Version-M subclass.  If the entire
complete clock and plateau tube lie in the same
scale-`2R` Version-M measurement row of weight at least `omega`, and `F` is
an actual component of that same velocity, then

\[
 p_{k,m,R}^{\rm plat}\le CP_R^M
 \tag{U.28}
\]

and U.6 pays the difference-frequency component by
`C(P_R^M)^(2/3)`.  This is conditional on the same realized-subclass and
ledger-alignment hypotheses as R0.75S.  It is not a statement about a
Fourier projection of a larger field, and it does not pay the remaining
three frequency rows in the total flux.

## 5. Meaning and open boundary

**Proved:** the uniform radial quotient U.10; the weighted complete-clock
moving-phase lemma U.13; its slow/fast proof U.14--U.20; exact scaling and
amplitude cancellation U.21--U.24; the difference-frequency payment U.4;
and the normalized rate U.6--U.7.

**What changes:** the most obviously dangerous term in a dyadic pair is the
low difference frequency, because its radial Fourier coefficient need not
have high-frequency decay.  U shows that this term is nevertheless paid by
the same beat defect that measures destructive interference in the local
cubic mass.  Beyond the automatic integer separation `d>=1`, no additional
lower bound on `d`, `dR`, `d aR`, or `B` is used.

**Open:** joint payment of the self frequencies `2k,2m` and sum frequency
`k+m`; a complete two-harmonic signed-flux theorem; low carriers with
`maR<C_0`; three or more harmonics; arbitrary packets; inter-packet
aggregation; nonconstant or vertically dependent shear; arbitrary-field
E.24; complete Version-M extraction; fixed deletion; suitable-weak transfer;
regularity; and singularity.  No novelty or priority claim is made.
\(\mathbf{NOT\ CLAY}.\)
