# R0.75S -- full-frequency complete-clock collar payment for one real harmonic

## 0. Result and exact boundary

R0.75Q pays one spatially spread real shear harmonic on a physical radial
collar under the high-frequency assumptions `k^2 T>=1`, `kaR>=2pi`, and
`k>=R^(-3/2)`.  R0.75R shows why the same plateau-only argument cannot be
extended to an arbitrary concentrated high-band packet.  The present note
returns to the one-harmonic class and removes all three frequency
restrictions by using the complete frozen time window.

Set

\[
 T_R:=t_2-s_R=4R^2
 \tag{S.1}
\]

and translate `s_R` to time zero.  Let `eta` be the frozen nondecreasing
time cutoff, so `0<=eta<=1`, `eta(0)=0`, and its total variation is at most
one.  For every `A>0`, integer `k>=1`, phase `phi in R`, and constant
`B in R`, define

\[
 F_k(t,x_2)=Ae^{-k^2t}\cos\bigl(k(x_2-Bt)-\phi\bigr),
 \qquad 0\le t\le T_R.
 \tag{S.2}
\]

For the canonical radial cutoff and its plateau shell, put

\[
 \begin{aligned}
 \mathcal T_{k,R}
 &:=\frac12\int_0^{T_R}\!\int_{\mathbb T^3}
       \eta(t)B\,\partial_2\xi_{a,R}|F_k|^2\,dxdt,\\
 M_{k,R}^{\rm plat}
 &:=\int_0^{T_R}\!\int_{\mathcal S_{a,R}^{\rm plat}}
       |F_k|^3\,dxdt .
 \end{aligned}
 \tag{S.3}
\]

There is a constant depending only on the fixed radial profile and plateau
width such that, for all sufficiently large `L`,

\[
 \boxed{
 |\mathcal T_{k,R}|
 \le C a^{2/3}R^{-1/3}
       \bigl(M_{k,R}^{\rm plat}\bigr)^{2/3}}
 \tag{S.4}
\]

simultaneously for every `k`, `B`, `phi`, and `A`.  In particular, no lower
or upper bound on the constant shear is needed for this estimate.

With the frozen normalization

\[
 p_{k,R}^{\rm plat}:=R^{-2}\omega M_{k,R}^{\rm plat},
 \qquad
 \mathfrak X_{k,R}:=\frac\omega R[\mathcal T_{k,R}]_+,
 \tag{S.5}
\]

equation S.4 becomes

\[
 \boxed{
 \mathfrak X_{k,R}
 \le C a^{2/3}\omega^{1/3}
       \bigl(p_{k,R}^{\rm plat}\bigr)^{2/3}.}
 \tag{S.6}
\]

Since `a=pL` and `omega=exp[-(c_gamma/4)L^2]`, its coefficient has the
strict rate

\[
 \lim_{L\to\infty}\frac1{L^2}
 \log\bigl(a^{2/3}\omega^{1/3}\bigr)
 =-\frac{c_\gamma}{12}<0.
 \tag{S.7}
\]

Thus the full frozen clock pays the physical-collar flux of every single
real horizontal harmonic, including all frequencies omitted by Q.  The
proof is not a multimode estimate.  It neither contradicts R nor controls
interference between distinct harmonics, a nonconstant shear, or the
arbitrary-field target E.24.

## 1. Frozen geometry and exact scalar reduction

Retain

\[
 a=pL,\quad p=\frac{32}{63},\quad
 R=e^{-\rho L^2/4},\quad
 \omega=e^{-c_\gamma L^2/4},\quad
 \rho=\frac9{10000},\quad c_\gamma=\frac8{3969}.
 \tag{S.8}
\]

The immediately used frozen inputs are

| input | SHA-256 | role |
|---|---|---|
| `research/r075b_bulk_clock_outer_padding_gate.md` | `430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a` | complete time window and monotone cutoff |
| `research/r075e_horizontal_cross_mode_flux_reduction.md` | `99529b8934412775e19a1b70784cddf3e62190b50c42669ccd34135a134c5049` | physical signed flux and E.24 |
| `research/r075q_spatially_spread_harmonic_collar_payment.md` | `9d7058fd7fbc61136967227507e47b0e866c7a4eeafebae198ab05a23645ed9c` | phase-uniform high-frequency plateau mass |
| `research/r075r_outer_cap_spectral_concentration_obstruction.md` | `e5eba5b262a8e140eaa149b6d914f355f2f3c636ec1e74cf85515f1c38fd32f3` | exact radial cross section and multimode boundary |

Choose fixed `0<delta_0<delta` and a smooth profile `0<=vartheta<=1`
such that

\[
 \xi_{a,R}(x)=\vartheta(|x|/R-a),\qquad
 \vartheta=1\ \hbox{on }[-\delta_0,\delta_0],\qquad
 \operatorname {supp}\vartheta\subset(-\delta,\delta).
 \tag{S.9}
\]

Assume `a>=4delta_0` and `(a+delta)R<pi/2`.  Its plateau shell is

\[
 \mathcal S_{a,R}^{\rm plat}
 :=\{x\in\mathbb T^3:||x|/R-a|\le\delta_0\}.
 \tag{S.10}
\]

The exact cross-sectional derivative from R0.75R is

\[
 D_R(y):=\int_{\mathbb T^2_{x_1,x_3}}
 \partial_2\xi_{a,R}(x_1,y,x_3)\,dx_1dx_3
 =-2\pi y\vartheta(|y|/R-a).
 \tag{S.11}
\]

It is odd.  Define its sine coefficient

\[
 S_{k,R}:=\int_{-\pi}^{\pi}D_R(y)\sin(2ky)\,dy.
 \tag{S.12}
\]

The constant and cosine rows vanish by oddness.  Expanding the square in
S.2 therefore gives the exact one-dimensional identity

\[
 \boxed{
 \mathcal T_{k,R}
 =\frac{A^2B S_{k,R}}4
 \int_0^{T_R}\eta(t)e^{-2k^2t}
 \sin(2\phi+2kBt)\,dt.}
 \tag{S.13}
\]

This preserves both signs until the scalar oscillatory integral has been
identified.

## 2. Three bounds for the radial sine coefficient

Put

\[
 q:=kR,\qquad \varepsilon:=kaR=aq.
 \tag{S.14}
\]

After `y=Rz`, equation S.12 becomes

\[
 S_{k,R}=-2\pi R^2\int
 z\vartheta(|z|-a)\sin(2qz)\,dz.
 \tag{S.15}
\]

The integrand is supported on two intervals of fixed length centered at
`+/-a`.  Consequently

\[
 \|z\vartheta(|z|-a)\|_{L^1}\le C a,
 \qquad
 \|\partial_z^N[z\vartheta(|z|-a)]\|_{L^1}\le C_Na
 \quad(N\ge1).
 \tag{S.16}
\]

The elementary bound `|sin(2qz)|<=2q|z|`, the first inequality in S.16,
and `N` integrations by parts give, respectively,

\[
 \boxed{
 |S_{k,R}|\le C_NaR^2
 \min\{\varepsilon,1,q^{-N}\}.}
 \tag{S.17}
\]

The three entries have different roles: `epsilon` resolves low-frequency
oddness, `1` is the direct cross-sectional `L^1` size, and `q^(-N)` pays
frequencies above the inverse collar thickness.

## 3. Two elementary phase--mass lemmas

Let

\[
 d(\psi):=\operatorname {dist}
 \bigl(\psi,\pi/2+\pi\mathbb Z\bigr),\qquad
 Q_\varepsilon(\psi):=\min\{1,\varepsilon+d(\psi)\}.
 \tag{S.18}
\]

The rectangular subcollar used in Q contains

\[
 |x_2|\le aR/4,\qquad |x_3|\le aR/4,
 \qquad
 |\{x_1:(x_1,x_2,x_3)\in\mathcal S_{a,R}^{\rm plat}\}|
 \ge4\delta_0R.
 \tag{S.19}
\]

For `0<epsilon<=2pi`, a one-dimensional node estimate yields

\[
 \int_{-1/4}^{1/4}
 |\cos(\varepsilon z-\psi)|^3\,dz
 \ge c\,Q_\varepsilon(\psi)^3.
 \tag{S.20}
\]

Indeed, if `epsilon+d(psi)` is small, translate the nearest cosine node and
use `|sin r|>=2|r|/pi` on `|r|<=pi/2`; the integral of
`|epsilon z-r_0|^3` is bounded below by a constant times
`(epsilon+|r_0|)^3`.  If `epsilon+d(psi)` is bounded below, compactness on
one phase period gives a positive lower bound.  Equations S.19--S.20 imply

\[
 \int_{\mathcal S_{a,R}^{\rm plat}}
 |\cos(kx_2-\psi)|^3\,dx
 \ge c\,a^2R^3Q_\varepsilon(\psi)^3.
 \tag{S.21}
\]

The second lemma couples a moving node to the signed time phase.  If
`0<epsilon<=2pi`, `0<=lambda<=1`, `sigma in R`, and
`w(s)=eta(T_Rs)e^{-2lambda s}`, then

\[
 \boxed{
 \left|\sigma\int_0^1w(s)
 \sin(2\phi+2\sigma s)\,ds\right|
 \le C\left[
 \int_0^1Q_\varepsilon(\phi+\sigma s)^3\,ds
 \right]^{2/3}.}
 \tag{S.22}
\]

To verify it, denote the integral inside the brackets by `J`.  For
`|sigma|<=1`, an interval of phase length `|sigma|` has

\[
 J^{1/3}\ge c\min\{1,\varepsilon+|\sigma|\}.
 \tag{S.23}
\]

Moreover `|sin(2psi)|<=2Q_epsilon(psi)`.  Holder then gives

\[
 |\sigma|\int_0^1|\sin(2\phi+2\sigma s)|\,ds
 \le C|\sigma|J^{1/3}\le CJ^{2/3}.
 \tag{S.24}
\]

For `|sigma|>=1`, a phase interval of length at least one gives `J>=c`.
The monotonicity of `eta` gives, in fact for every `lambda>=0`,

\[
 \operatorname {Var}_{[0,1]}w
 \le\int_0^1d\eta(T_Rs)
 +2\lambda\int_0^1\eta(T_Rs)e^{-2\lambda s}\,ds
 \le2.
 \tag{S.25}
\]

One integration by parts against the phase then bounds the left side of
S.22 by an absolute constant.  This proves S.22 in both regimes.  The
estimate is exactly what prevents a harmonic that initially lies near a
cosine node from escaping payment: either the shear is too small to create
flux, or it moves the node through enough plateau mass.

## 4. Low spatial frequency: node motion pays the clock

Assume first

\[
 \varepsilon=kaR\le2\pi.
 \tag{S.26}
\]

For all sufficiently large `L`, `a>=4pi`, and hence

\[
 \lambda:=k^2T_R=4q^2
 \le\frac{16\pi^2}{a^2}\le1.
 \tag{S.27}
\]

Set `sigma=kBT_R`.  Equations S.13 and S.17 give

\[
 |\mathcal T_{k,R}|
 \le CA^2a^2R^3
 \left|\sigma\int_0^1
 \eta(T_Rs)e^{-2\lambda s}
 \sin(2\phi+2\sigma s)\,ds\right|.
 \tag{S.28}
\]

On the other hand, S.21 and `e^(-3lambda s)>=e^(-3)` give

\[
 M_{k,R}^{\rm plat}
 \ge cA^3a^2R^3T_R
 \int_0^1Q_\varepsilon(\phi+\sigma s)^3\,ds.
 \tag{S.29}
\]

Apply S.22 and use `T_R=4R^2`.  The amplitude cancels and yields

\[
 |\mathcal T_{k,R}|
 \le Ca^{2/3}R^{-1/3}
 \bigl(M_{k,R}^{\rm plat}\bigr)^{2/3}.
 \tag{S.30}
\]

Thus the complete low-frequency sector is paid without a lower bound on
`B` and without assuming a phase-uniform spatial lower bound at each time.

## 5. High spatial frequency: phase variation and radial Fourier decay

Now assume

\[
 \varepsilon=kaR\ge2\pi.
 \tag{S.31}
\]

The phase-uniform plateau estimate Q.19 gives

\[
 \int_{\mathcal S_{a,R}^{\rm plat}}
 |\cos(kx_2-\psi)|^3\,dx\ge ca^2R^3
 \quad\hbox{for every }\psi.
 \tag{S.32}
\]

Consequently

\[
 M_{k,R}^{\rm plat}
 \ge cA^3a^2R^3\min\{T_R,k^{-2}\}.
 \tag{S.33}
\]

If `B=0`, the flux vanishes.  Otherwise let
`w(t)=eta(t)e^(-2k^2t)`.  Its total variation is at most two, exactly as in
S.25.  Integration by parts in the phase gives

\[
 \left|B\int_0^{T_R}w(t)
 \sin(2\phi+2kBt)\,dt\right|
 \le\frac Ck.
 \tag{S.34}
\]

Therefore S.13 implies

\[
 |\mathcal T_{k,R}|\le CA^2\frac{|S_{k,R}|}{k}.
 \tag{S.35}
\]

It remains only to compare scales.  If `q<=1`, then S.31 gives
`q>=2pi/a`, and S.17 yields

\[
 \frac{|S_{k,R}|}{k}
 \le CaR^3q^{-1}\le Ca^2R^3.
 \tag{S.36}
\]

In this range `min{T_R,k^(-2)}>=cR^2`.  If `q>=1`, use S.17 with `N=1`:

\[
 \frac{|S_{k,R}|}{k}\le CaR^3q^{-2},
 \qquad
 \min\{T_R,k^{-2}\}=R^2q^{-2}.
 \tag{S.37}
\]

Since `q^(-2)<=q^(-4/3)` and `a<=a^2`, equations S.33--S.37 again give

\[
 |\mathcal T_{k,R}|
 \le Ca^{2/3}R^{-1/3}
 \bigl(M_{k,R}^{\rm plat}\bigr)^{2/3}.
 \tag{S.38}
\]

Equations S.30 and S.38 prove S.4 for every integer frequency.

## 6. Normalization, exact-solution status, and open boundary

Substitution of S.5 into S.4 gives S.6.  If, in addition, the harmonic is
an actual coordinate component of the same smooth velocity measured by the
frozen Version-M ledger throughout the plateau tube, and that tube belongs
to an exterior row of weight at least `omega`, then

\[
 p_{k,R}^{\rm plat}\le CP_R^M,
 \qquad
 \mathfrak X_{k,R}\le C(P_R^M)^{2/3}
 \quad(L\ge L_0).
 \tag{S.39}
\]

This last implication is conditional on the same realized-subclass and
ledger-alignment requirements as R0.75Q: the whole interval `[0,T_R]`
must lie in the same scale-`2R` measurement window, and the entire plateau
spacetime tube must lie in an exterior row of weight at least `omega` for
the same velocity `v_R`.  It is not asserted for a Fourier projection of a
larger velocity component.

The scalar family is also embedded in the exact smooth unforced shear

\[
 u_k(t,x)=(0,B,F_k(t,x_2)),
 \tag{S.40}
\]

because `div u_k=0` and

\[
 \partial_tF_k+B\partial_2F_k-\partial_2^2F_k=0.
 \tag{S.41}
\]

More explicitly,

\[
 (u_k\!\cdot\nabla)u_k=(0,0,B\partial_2F_k),
 \qquad \Delta u_k=(0,0,\partial_2^2F_k),
\]

Thus S.40 solves three-dimensional Navier--Stokes with constant pressure.
Its nonzero constant background has not been shown to belong to the frozen
mean-zero, inversion-paired Version-M subclass.

**Proved:** the exact scalar flux identity S.11--S.13; the three radial
coefficient bounds S.15--S.17; the spatial node and moving-phase lemmas
S.18--S.25; the low-frequency payment S.26--S.30; the high-frequency
payment S.31--S.38; and the full-frequency normalized estimate S.6.

**Open:** two or more harmonics; interference and packet aggregation;
nonconstant `x_3` shear; arbitrary vertical structure; transfer from a
harmonic projection to the actual velocity component; arbitrary-field
E.24; complete Version-M clock extraction; fixed deletion; suitable-weak
transfer; and every regularity or singularity conclusion.  No novelty or
priority claim is made.  \(\mathbf{NOT\ CLAY}.\)
