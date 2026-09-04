# R0.75R -- outer-cap spectral concentration obstructs a plateau-only multimode payment

## 0. Result and exact boundary

R0.75Q pays the signed radial-cutoff flux of one spatially spread shear
harmonic with that harmonic's cubic mass on the physical plateau shell.  The
present note tests whether the same plateau atom can pay an arbitrary
high-frequency packet.  It cannot.

Fix an integer `m>=1` and the canonical radial cutoff from R0.75Q.  For every
sufficiently large frozen parameter `L`, the construction below gives a real
trigonometric polynomial `G_K`, supported in the horizontal frequency band

\[
 \{j\in\mathbb Z:K\le |j|\le2K\},
 \tag{R.1}
\]

and an exact global smooth Navier--Stokes shear solution

\[
 u_K(t,x)=(0,B,F_K(t,x_2)),\qquad
 F_K(t,x_2)=e^{t\partial_2^2}G_K(x_2-Bt).
 \tag{R.2}
\]

Here `B=-bR^(-2)` for a fixed sufficiently small `b>0` and the observation
time is `T=K^(-2)`.  With `eta=1`, define

\[
 \begin{aligned}
 \mathcal T_K
 &:=\frac12\int_0^T\!\int_{\mathbb T^3}
 B\,\partial_2\xi_{a,R}(x)|F_K(t,x_2)|^2\,dxdt,\\
 M_{K,{\rm plat}}
 &:=\int_0^T\!\int_{\mathcal S_{a,R}^{\rm plat}}
 |F_K(t,x_2)|^3\,dxdt .
 \end{aligned}
 \tag{R.3}
\]

There are constants depending only on `m` and the fixed cutoff such that

\[
 \boxed{
 \mathcal T_K\ge
 c_m|B|aR A^2 n^{-1}K^{-2},\qquad
 M_{K,{\rm plat}}\le
 C_mA^3a^2R^3K^{-2}(nR)^{-6m}.}
 \tag{R.4}
\]

After the frozen normalization

\[
 p_{K,{\rm plat}}:=R^{-2}\omega M_{K,{\rm plat}},\qquad
 \mathfrak X_K:=\frac\omega R[\mathcal T_K]_+,
 \tag{R.5}
\]

the quotient grows at least as

\[
 \boxed{
 \frac{\mathfrak X_K}{p_{K,{\rm plat}}^{2/3}}
 \ge c_m bL^{-1/3}R^{-2m-1/6}\omega^{1/3}
 =c_m bL^{-1/3}e^{\kappa_mL^2},}
 \tag{R.6}
\]

where

\[
 \kappa_m:=\frac{(2m+1/6)\rho}{4}-\frac{c_\gamma}{12}>0.
 \tag{R.7}
\]

For the smallest choice `m=1`, the exact rate is

\[
 \kappa_1=\frac{304373}{952560000}>0,
 \qquad
 R^{-13/6}\omega^{1/3}
 =R^{-304373/214326}.
 \tag{R.8}
\]

Consequently there is no constant independent of `L` in the plateau-only
multimode estimate

\[
 \mathfrak X_K\le C p_{K,{\rm plat}}^{2/3}.
 \tag{R.9}
\]

This is a negative result about that specific attempted extension of Q.  The
complete Version-M payment sees exterior rows beyond the plateau and also
sees the background component `B`.  Thus R.9 is not a counterexample to E.24
or to Version-M.  In addition, this note does not prove that its constant
background belongs to the frozen mean-zero, inversion-paired Version-M
subclass.  It does not concern singularity formation.

## 1. Frozen geometry and the exact outer-cap identity

Retain

\[
 a=pL,\quad p=\frac{32}{63},\quad
 R=e^{-\rho L^2/4},\quad
 \omega=e^{-c_\gamma L^2/4},\quad
 \rho=\frac9{10000},\quad c_\gamma=\frac8{3969}.
 \tag{R.10}
\]

The immediately used frozen inputs are

| input | SHA-256 | role |
|---|---|---|
| `research/r075b_bulk_clock_outer_padding_gate.md` | `430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a` | frozen `a,R,omega` scales and shear bound |
| `research/r075e_horizontal_cross_mode_flux_reduction.md` | `99529b8934412775e19a1b70784cddf3e62190b50c42669ccd34135a134c5049` | definition and open status of E.24 |
| `research/r075n_radial_collar_averaged_wiener_row.md` | `ba59a4df399d8580b35d8dbb3f0758f9d2ffcc7f97f1147e5804c428f3740318` | canonical radial cutoff geometry |
| `research/r075q_spatially_spread_harmonic_collar_payment.md` | `9d7058fd7fbc61136967227507e47b0e866c7a4eeafebae198ab05a23645ed9c` | one-harmonic plateau payment being tested |

Let `0<delta_0<delta`, and let

\[
 \xi_{a,R}(x)=\vartheta(|x|/R-a),\qquad
 0\le\vartheta\le1,qquad
 \vartheta=1\ \hbox{on }[-\delta_0,\delta_0],\qquad
 \operatorname {supp}\vartheta\subset(-\delta,\delta).
 \tag{R.11}
\]

As before, assume `a>=4delta_0` and `(a+delta)R<pi/2`, so the support lies in
one Euclidean chart of the torus.  Integrate the cutoff derivative over the
two coordinates that do not occur in `F_K`:

\[
 D_R(y):=\int_{\mathbb T^2_{x_1,x_3}}
 \partial_2\xi_{a,R}(x_1,y,x_3)\,dx_1dx_3.
 \tag{R.12}
\]

The cross-sectional cutoff mass is

\[
 \Xi_R(y)=2\pi\int_{|y|}^{\infty}
 \vartheta(\varrho/R-a)\varrho\,d\varrho.
 \tag{R.13}
\]

Differentiating its moving lower endpoint gives the exact identity

\[
 \boxed{D_R(y)=\Xi_R'(y)
 =-2\pi y\vartheta(|y|/R-a).}
 \tag{R.14}
\]

In particular, `D_R<0` on the positive cap and `D_R>0` on the negative cap.
This identity is stronger than the absolute `L^1` estimate used in Q.

Continuity and `vartheta(delta_0)=1` provide numbers

\[
 s_*\in(\delta_0,\delta),\qquad h>0,qquad c_\vartheta>0
 \tag{R.15}
\]

such that

\[
 \delta_0<s_*-3h<s_*+3h<\delta,qquad
 \vartheta(s)\ge c_\vartheta
 \quad(|s-s_*|\le3h).
 \tag{R.16}
\]

Set `y_0=(a+s_*)R`.  The interval

\[
 I_+:=[y_0-2hR,y_0+2hR]
 \tag{R.17}
\]

lies in the positive cutoff cap but outside the `x_2` projection of the
plateau shell if `h` is decreased once more.  On this interval,

\[
 -D_R(y)\ge c_\vartheta aR.
 \tag{R.18}
\]

## 2. An explicit high-band packet

Let `K` be the smallest multiple of `16m` not below `R^(-3/2)`, and put

\[
 n=\frac{K}{16m},\qquad q=\frac{3K}{2},\qquad T=K^{-2}.
 \tag{R.19}
\]

For all sufficiently large `L`,

\[
 R^{-3/2}\le K\le2R^{-3/2},\qquad
 n\asymp_mR^{-3/2},\qquad nR\longrightarrow\infty.
 \tag{R.20}
\]

Use the normalized Dirichlet kernel

\[
 d_n(z)=\frac1{2n+1}\sum_{r=-n}^{n}e^{irz}
 =\frac{\sin((n+1/2)z)}{(2n+1)\sin(z/2)}
 \tag{R.21}
\]

and define the real packet

\[
 G_K(y)=A\,d_n(y-y_0)^{2m}\cos(q(y-y_0)),\qquad A>0.
 \tag{R.22}
\]

The Fourier support of `d_n^(2m)` lies in `[-2mn,2mn]=[-K/8,K/8]`.
Multiplication by the real carrier shifts this support by `+q` and `-q`.
Therefore

\[
 \operatorname {supp}\widehat G_K
 \subset\left\{j:\frac{11K}{8}\le|j|\le\frac{13K}{8}\right\},
 \tag{R.23}
\]

which proves R.1 without a projection remainder.

The elementary Dirichlet bound

\[
 |d_n(z)|\le C\min\left\{1,
 \frac1{n\operatorname {dist}(z,2\pi\mathbb Z)}\right\}
 \tag{R.24}
\]

and a fixed interval of length comparable to `K^(-1)` on which both factors
in R.22 are bounded below show that

\[
 c_mA^2n^{-1}\le\|G_K\|_{L^2(\mathbb T)}^2
 \le C_mA^2n^{-1}.
 \tag{R.25}
\]

For every fixed `r>0`, R.24 also gives the tail bounds

\[
 \begin{aligned}
 \sup_{\operatorname {dist}(y,y_0)\ge rR}|G_K(y)|
 &\le C_{m,r}A(nR)^{-2m},\\
 \int_{\operatorname {dist}(y,y_0)\ge rR}|G_K(y)|^2dy
 &\le C_{m,r}A^2n^{-1}(nR)^{1-4m}.
 \end{aligned}
 \tag{R.26}
\]

The relative tail in the second line tends to zero for every `m>=1`.

## 3. Exact Navier--Stokes evolution

Choose

\[
 0<b\le b_*:=\min\{C_B,h/8,(s_*-\delta_0)/16\},
 \qquad B=-bR^{-2}.
 \tag{R.27}
\]

Since `K>=R^(-3/2)`, the drift over R.19 satisfies

\[
 |B|T\le bR.
 \tag{R.28}
\]

Define `F_K` and `u_K` by R.2.  Direct differentiation gives

\[
 (\partial_t+B\partial_2-\partial_2^2)F_K=0.
 \tag{R.29}
\]

Moreover `div u_K=0` and

\[
 \nabla\!\cdot u_K=0,\qquad
 (u_K\!\cdot\nabla)u_K=(0,0,B\partial_2F_K).
\]

Consequently

\[
 \partial_tu_K+(u_K\cdot\nabla)u_K-\Delta u_K=0
 \tag{R.30}
\]

with constant pressure.  Thus the example is an exact unforced smooth
three-dimensional Navier--Stokes solution, not a passive-scalar surrogate or
a numerical simulation.

The support row R.23 is preserved by the heat semigroup.  Hence, for
`0<=t<=T`,

\[
 \|F_K(t)\|_2^2\ge e^{-8}\|G_K\|_2^2
 \ge c_mA^2n^{-1}.
 \tag{R.31}
\]

The constant `8` is deliberately coarse; `|j|<=2K` and `t<=K^(-2)` are
sufficient.

## 4. Short-time localization and the positive flux

For two subsets of the circle separated by distance `d`, the one-dimensional
heat semigroup satisfies the elementary Gaussian off-diagonal estimates

\[
 \|1_Ee^{t\partial_2^2}1_H\|_{2\to2}
 \le e^{-d^2/(4t)},\qquad
 \sup_{w\in H}\int_{\operatorname {dist}(z,H)\ge d}
 H_t(z-w)\,dz
 \le Ce^{-d^2/(8t)}.
 \tag{R.32}
\]

They follow directly from the periodized Gaussian heat kernel; only fixed
changes in the numerical constants are used below.

Split `G_K` into the part within distance `hR/2` of `y_0` and its complement.
Equations R.26, R.28, and R.32 imply, uniformly for `0<=t<=T`,

\[
 \int_{I_+}|F_K(t,y)|^2dy
 \ge c_mA^2n^{-1}
 \tag{R.33}
\]

once `L` is large.  Indeed, the square root of the relative initial tail is
`O((nR)^((1-4m)/2))`, while the heat leakage is
`O(exp(-c(KR)^2))`; both tend to zero.  Explicitly,

\[
 \|1_{I_+}F_K(t)\|_2
 \ge\|F_K(t)\|_2-\|1_{I_+^c}F_K(t)\|_2,
\]

so the global lower bound minus the vanishing leakage has the required
direction.  The same argument, with a larger separation, gives

\[
 \int_{\{y<0:\,D_R(y)>0\}}|F_K(t,y)|^2dy
 =o_m(A^2n^{-1}).
 \tag{R.34}
\]

Because `B<0`, the integrand `BD_R|F_K|^2` is nonnegative for `y>0` and
nonpositive for `y<0`.  Use R.18 and R.33 for the positive contribution and
R.34 for the only adverse contribution.  For sufficiently large `L`,

\[
 \begin{aligned}
 \mathcal T_K
 &=\frac B2\int_0^T\!\int_{\mathbb T}D_R(y)|F_K(t,y)|^2dydt\\
 &\ge c_m|B|aR\int_0^TA^2n^{-1}dt
 \ge c_m|B|aRA^2n^{-1}K^{-2}.
 \end{aligned}
 \tag{R.35}
\]

This is the first inequality in R.4.

## 5. What the plateau atom misses

If `(x_1,y,x_3)` belongs to the plateau shell, then

\[
 |y|\le(a+\delta_0)R.
 \tag{R.36}
\]

Its circular distance from `y_0` is therefore at least
`(s_*-delta_0)R`.  R.27 keeps the transported center a fixed multiple of
`R` away from that projection throughout `[0,T]`.

Split the heat convolution into initial points near and far from `y_0`.
The near part is controlled by the Gaussian tail in R.32; the far part is
controlled in `L^infinity` by R.26 and heat-semigroup contraction.  Thus

\[
 \sup_{\substack{0\le t\le T\\|y|\le(a+\delta_0)R}}
 |F_K(t,y)|
 \le C_mA\left[(nR)^{-2m}+e^{-c(KR)^2}\right]
 \le C_mA(nR)^{-2m}
 \tag{R.37}
\]

for large `L`.  The plateau shell has volume at most `C a^2R^3`.
Multiplying R.37 cubed by this volume and by `T=K^(-2)` proves

\[
 M_{K,{\rm plat}}
 \le C_mA^3a^2R^3K^{-2}(nR)^{-6m},
 \tag{R.38}
\]

the second inequality in R.4.

## 6. Frozen exponent and failure of the plateau-only estimate

Equations R.35 and R.38 give

\[
 \frac{\mathcal T_K}{M_{K,{\rm plat}}^{2/3}}
 \ge c_m|B|a^{-1/3}R^{-1}n^{-1}K^{-2/3}(nR)^{4m}.
 \tag{R.39}
\]

The normalization R.5 multiplies this quotient by
`R^(1/3)omega^(1/3)`.  Substituting `|B|=bR^(-2)` and R.20 yields

\[
 \frac{\mathfrak X_K}{p_{K,{\rm plat}}^{2/3}}
 \ge c_mba^{-1/3}R^{-2m-1/6}\omega^{1/3}.
 \tag{R.40}
\]

Since `a=(32/63)L`, its polynomial factor is `C L^(-1/3)`.  Finally,

\[
 R^{-2m-1/6}\omega^{1/3}
 =\exp\left[
 \left(\frac{(2m+1/6)\rho}{4}-\frac{c_\gamma}{12}\right)L^2
 \right].
 \tag{R.41}
\]

At `m=1`, exact rational arithmetic gives R.8.  Because `kappa_1>0` and
`kappa_m` increases with `m`, R.6 diverges for every fixed `m>=1`.  This
proves R.9.

The amplitude `A` cancels from the quotient.  The obstruction is therefore
geometric and spectral, not an artifact of a large-amplitude limit.

## 7. Consequence for the route

The one-harmonic Q argument used phase-uniform spatial spreading across the
plateau fibres.  R shows that band limitation alone does not retain that
property for a multimode field: coherent modes can concentrate at scale
`n^(-1)<<R` in an outer cap and leave only an algebraic tail on the plateau.

Any valid continuation of the route must therefore supply at least one of
the following ingredients:

1. a payment atom covering the full signed-flux cap rather than only the
   plateau;
2. a quantitative spreading or thickness hypothesis that rules out the
   packet R.22;
3. a signed multimode cancellation that is not reduced to the plateau's
   absolute cubic mass; or
4. an independent mechanism that transfers outer-cap mass into an already
   counted Version-M row.

This narrows the next positive target.  It does not show that all localized
or signed methods fail.

## 8. Status boundary

**Proved:** the exact cross-sectional identity R.14; the explicit real
high-band support R.23; the Dirichlet concentration and tail rows
R.25--R.26; exact global smooth Navier--Stokes realization R.29--R.30;
short-time outer-cap persistence R.31--R.34; the positive signed-flux lower
bound R.35; the plateau cubic upper bound R.38; and the divergent normalized
quotient R.40--R.41.

**Ruled out:** a uniform extension of Q to arbitrary high-band packets when
the only payment is the cubic mass of the canonical plateau shell.

**Not ruled out or proved:** a payment using the full cutoff support; the
complete nonnegative exterior rows already present in Version-M; a spectral
or physical spreading hypothesis; arbitrary nonconstant shear; nonlinear
mode transfer; the arbitrary-field estimate E.24; complete-clock extraction;
fixed deletion; suitable-weak transfer; or any regularity or singularity
conclusion.  No novelty or priority claim is made.
\(\mathbf{NOT\ CLAY}.\)
