# R0.76A -- complete-clock obstruction to localized carrier-current positivity

## 0. Result and exact boundary

R0.75Z leaves one possible cluster route: exploit the nonnegative offset
spectrum to keep the carrier current signed instead of estimating its
absolute value.  The full-period current is nonnegative, but the collar
multiplier is local.  This note tests the sign after inserting the actual
frozen radial primitive and the complete-clock cutoff.

Let the frozen radial profile satisfy

\[
 0\le\vartheta\le1,
 \qquad \vartheta=1\ \hbox{on }[-\delta_0,\delta_0],
 \qquad \operatorname {supp}\vartheta\subset(-\delta,\delta),
 \qquad 0<\delta_0<\delta,
 \tag{A.1}
\]

and define

\[
 W_a(z)=-2\pi az\vartheta\bigl(a(|z|-1)\bigr),
 \qquad
 \Xi_a(z)=\int_{-\infty}^{z}W_a(r)\,dr.
 \tag{A.2}
\]

Assume

\[
 a\ge\max(24,2\delta),
 \qquad 0<\ell=aR\le\frac1{11}.
 \tag{A.3}
\]

Set `q=2` and choose the integer carrier and scaled frequencies

\[
 N=\left\lceil\frac{16}{\ell}\right\rceil,
 \qquad \alpha=N\ell,
 \qquad \beta=\ell.
 \tag{A.4}
\]

Then

\[
 16\le\alpha<16+\beta<17,
 \qquad N\ell\ge8q,
 \qquad ((N+1)-N)\ell=\beta<8q.
 \tag{A.5}
\]

Thus `(N,N+1)` is an actual unresolved high-carrier cluster.  On the
scaled complete clock `0<=s<=4`, take `v=1`, amplitudes `(2,1)`, and phases
`(0,pi)`.  After removal of the first carrier, its exact envelope is

\[
 Z(s,z)=2-r(s)e^{i\beta(z-s)},
 \qquad
 r(s)=e^{-\mu s},
 \qquad
 \mu=\frac{2\alpha\beta+\beta^2}{a^2}.
 \tag{A.6}
\]

Let

\[
 J(s,z)=\operatorname {Im}(\overline Z\,\partial_zZ).
 \tag{A.7}
\]

For every `s in [0,4]` and every `z` in the support of `Xi_a`,

\[
 \boxed{J(s,z)\le-\frac9{16}\beta<0,}
 \tag{A.8}
\]

and, more strongly,

\[
 \boxed{
 |\partial_zZ(s,z)|^2+2\alpha J(s,z)
 \le-\alpha\beta<0.}
 \tag{A.9}
\]

The primitive `Xi_a` is nonnegative, nonzero, and has a uniform mass lower
bound.  Hence every nonnegative complete-clock cutoff `zeta` with
`int_0^4 zeta>0` satisfies

\[
 \boxed{
 \int_0^4\!\zeta(s)e^{-2\alpha^2s/a^2}
 \int_{\mathbb R}\!\Xi_a(z)J(s,z)\,dzds<0.}
 \tag{A.10}
\]

The same strict negativity holds with `J` replaced by the left side of
A.9.  Thus one-sided offset spectrum does not give a nonnegative localized
current, even after the actual collar primitive, common carrier heat
factor, complete time window, and nonnegative cutoff are inserted.

This is not a counterexample to the two-mode collar-flux estimate: R0.75W
already pays that estimate.  It rules out only the strategy of discarding
the localized carrier-current row by sign.  In this fixed-amplitude example
the scaled current contribution is at most `C ell/a^2=C R/a`, so it may
still be perturbative or cancel against the carrier-density rows.  No
cluster-payment or regularity claim is made.

## 1. Frozen inputs

| input | SHA-256 | role |
|---|---|---|
| `research/r075r_outer_cap_spectral_concentration_obstruction.md` | `e5eba5b262a8e140eaa149b6d914f355f2f3c636ec1e74cf85515f1c38fd32f3` | frozen radial profile and exact cross section |
| `research/r075w_full_frequency_two_harmonic_flux_payment.md` | `571b8152e3e5f81becec4dd691488fb5889fac23e94ca7c99bd546399dc320d4` | scaled primitive and already-paid two-mode class |
| `research/r075z_unresolved_cluster_carrier_current_gate.md` | `30d2811e8747aa2b40b4787e6f169af19d1381b66fc84610327da221168f3d97` | exhaustive cluster sector and carrier-current identity |

Retain

\[
 s=\frac t{R^2},
 \qquad z=\frac y{aR},
 \qquad v=\frac{BR}{a},
 \qquad \ell=aR.
 \tag{A.11}
\]

The real cluster field corresponding to A.6 is

\[
 \begin{aligned}
 G(s,z)
 &=2e^{-\alpha^2s/a^2}\cos\bigl(\alpha(z-s)\bigr)\\
 &\quad-e^{-(\alpha+\beta)^2s/a^2}
 \cos\bigl((\alpha+\beta)(z-s)\bigr).
 \end{aligned}
 \tag{A.12}
\]

It is the scaled form of the exact smooth diffusive shear with physical
frequencies `(N,N+1)`, positive amplitudes `(2,1)`, second phase `pi`, and
constant speed `B=a/R`.

## 2. Positivity and mass of the frozen primitive

The function `W_a` is odd.  On the negative half-line it is nonnegative;
on the positive half-line it is nonpositive.  Its total integral vanishes.
Therefore

\[
 \Xi_a(z)\ge0\quad(z\in\mathbb R).
 \tag{A.13}
\]

The support condition in A.1 gives

\[
 \operatorname {supp}\Xi_a
 \subset\left[-1-\frac\delta a,1+\frac\delta a\right]
 \subset\left[-\frac32,\frac32\right].
 \tag{A.14}
\]

On

\[
 I_-=\left[-1-\frac{\delta_0}{a},
                 -1+\frac{\delta_0}{a}\right],
 \tag{A.15}
\]

one has `vartheta=1` and `|z|>=1/2`, so

\[
 W_a(z)\ge\pi a,
 \qquad
 \int_{I_-}W_a(z)\,dz\ge2\pi\delta_0.
 \tag{A.16}
\]

Between the two transition lobes, `Xi_a` equals the full mass of the
negative lobe.  The interval
`[-1+delta/a,1-delta/a]` has length at least one.  Consequently,

\[
 \boxed{
 \int_{\mathbb R}\Xi_a(z)\,dz\ge2\pi\delta_0>0.}
 \tag{A.17}
\]

The earlier frozen estimate also gives

\[
 \|\Xi_a\|_{L^1}+\|\Xi_a\|_{L^\infty}\le C_\vartheta.
 \tag{A.18}
\]

## 3. Uniform phase and damping bounds

From A.3--A.5,

\[
 0<\beta\le\frac1{11},
 \qquad 16\le\alpha<17,
 \qquad
 0\le4\mu
 <\frac{140}{11\cdot24^2}<\frac14.
 \tag{A.19}
\]

Thus, throughout the complete clock,

\[
 \frac34<e^{-1/4}\le r(s)\le1.
 \tag{A.20}
\]

For `z` in the support of `Xi_a`, A.14 gives

\[
 |\beta(z-s)|
 \le\beta\left(\frac32+4\right)
 \le\frac12.
 \tag{A.21}
\]

The elementary inequality `cos x>=1-x^2/2` now yields

\[
 \cos\bigl(\beta(z-s)\bigr)\ge\frac78.
 \tag{A.22}
\]

## 4. Exact negative localized current

Differentiating A.6 gives

\[
 \partial_zZ=-i\beta r e^{i\beta(z-s)}.
 \tag{A.23}
\]

Therefore

\[
 \begin{aligned}
 J
 &=\operatorname {Im}\left[
 (2-re^{-i\beta(z-s)})(-i\beta r e^{i\beta(z-s)})
 \right]\\
 &=\beta r\left(r-2\cos(\beta(z-s))\right).
 \end{aligned}
 \tag{A.24}
\]

Equations A.20 and A.22 imply

\[
 r-2\cos(\beta(z-s))\le1-\frac74=-\frac34,
 \tag{A.25}
\]

and hence

\[
 J\le-\frac34\beta r\le-\frac9{16}\beta.
 \tag{A.26}
\]

This proves A.8.  Also

\[
 |\partial_zZ|^2=\beta^2r^2\le\beta^2
 \le\frac18\alpha\beta.
 \tag{A.27}
\]

Combining A.26 and A.27 gives

\[
 |\partial_zZ|^2+2\alpha J
 \le\frac18\alpha\beta-\frac98\alpha\beta
 =-\alpha\beta,
 \tag{A.28}
\]

which proves A.9.

## 5. Complete-clock insertion

Let

\[
 \zeta:[0,4]\longrightarrow[0,1],
 \qquad \zeta\ge0,
 \qquad \int_0^4\zeta(s)\,ds>0.
 \tag{A.29}
\]

No monotonicity is needed for the sign.  Every nonzero frozen cutoff of
this class is admissible.  Because every remaining factor is nonnegative,
A.8 and A.17 give

\[
 \begin{aligned}
 &\int_0^4\zeta e^{-2\alpha^2s/a^2}
 \int_{\mathbb R}\Xi_aJ\,dzds\\
 &\quad\le-\frac{9\pi\delta_0}{8}\beta
 \int_0^4\zeta(s)e^{-2\alpha^2s/a^2}\,ds<0.
 \end{aligned}
 \tag{A.30}
\]

This proves A.10.  The same calculation using A.9 gives

\[
 \begin{aligned}
 &\int_0^4\zeta e^{-2\alpha^2s/a^2}
 \int_{\mathbb R}\Xi_a
 \left(|\partial_zZ|^2+2\alpha J\right)\,dzds\\
 &\quad\le-2\pi\delta_0\alpha\beta
 \int_0^4\zeta(s)e^{-2\alpha^2s/a^2}\,ds<0.
 \end{aligned}
 \tag{A.31}
\]

There is no conflict with the full gradient identity

\[
 |i\alpha Z+\partial_zZ|^2
 =\alpha^2|Z|^2+|\partial_zZ|^2+2\alpha J\ge0.
 \tag{A.32}
\]

The positive carrier-density term `alpha^2|Z|^2` was not included in
A.31.  It is one of the rows that a joint multiplier argument must retain.

## 6. Size and claim boundary

In scaled variables the envelope density equation contains the current as

\[
 \partial_s|Z|^2+v\partial_z|Z|^2-a^{-2}\partial_z^2|Z|^2
 =-2a^{-2}|\partial_zZ|^2
 -4\frac\alpha{a^2}J.
 \tag{A.33}
\]

For the fixed amplitudes in A.6, A.18 and the direct upper bound
`|J|<=3 beta` give

\[
 \left|
 4\frac\alpha{a^2}
 \int_0^4\zeta e^{-2\alpha^2s/a^2}
 \int\Xi_aJ
 \right|
 \le C\frac{\alpha\beta}{a^2}
 \le C\frac\ell{a^2}=C\frac Ra.
 \tag{A.34}
\]

Thus the example proves a strict sign obstruction but not a large-error
obstruction.  It leaves open a perturbative estimate, an inequality with a
localized boundary error, and cancellation with the carrier block.  The
fact that the same two-mode family is fully paid by R0.75W confirms that a
joint mechanism exists in this test class.

**Closed here:** failure of localized current nonnegativity for an exact
integer-frequency high-carrier cluster, with the actual frozen primitive,
carrier heat factor, complete clock, and every nonnegative nonzero cutoff;
uniform negativity of the current-correction density; and its exact
fixed-amplitude upper scale `C R/a`.

**Open:** a quantitative localized current estimate for arbitrary cluster
coefficients; joint density/carrier-block payment; every full Z-sector
collar-flux estimate; cross-cluster aggregation; growing packets;
nonconstant or vertically dependent shear; projection from a larger
velocity; arbitrary-field E.24; complete Version-M extraction; fixed
deletion; suitable-weak transfer; regularity; and singularity.

The proof is analytic.  No simulation or formal scientific figure is
needed.  No completeness, novelty, or priority claim is made.
**NOT CLAY.**
