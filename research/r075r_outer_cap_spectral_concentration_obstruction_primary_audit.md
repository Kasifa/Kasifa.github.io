# R0.75R primary analytic audit

## Audit object

- Main note: `research/r075r_outer_cap_spectral_concentration_obstruction.md`
- Audit type: geometry, exact PDE, localization, exponent, and claim-boundary audit
- Current verdict: **PASS**
- Mathematical blocker count: **0**
- Release blocker count: **0**

This is an author-side analytic audit, completed after an independent
mathematical reread of the corrected heat-kernel row.  It does not by itself
certify the note and does not authorize publication.

## 1. Radial cross-section audit

For fixed `y=x_2`, polar coordinates in `(x_1,x_3)` give

\[
 \Xi_R(y)=2\pi\int_{|y|}^{\infty}
 \vartheta(\varrho/R-a)\varrho\,d\varrho.
\]

For `y>0`, differentiation gives
`Xi_R'(y)=-2pi y vartheta(y/R-a)`.  For `y<0`, the derivative of `|y|`
changes sign and gives the same formula
`-2pi y vartheta(|y|/R-a)`.  This agrees with direct integration of
`partial_2 xi`.  The identity is odd, integrates to zero, and has the sign
used in the flux lower bound.

The condition `(a+delta)R<pi/2` places every relevant cross-section in one
Euclidean chart.  No periodic copy enters the calculation.

## 2. Outer-cap geometry audit

Because `vartheta=1` through `delta_0` and is continuous, there is a closed
interval strictly to the right of `delta_0` on which `vartheta` has a fixed
positive lower bound.  The constants `s_*` and `h` in R.15--R.16 may
therefore be chosen independently of `L`.

For `y` in `I_+`, `y/R-a` lies in that interval, so
`-D_R(y)>=c_vartheta aR` after increasing the fixed lower threshold for
`a`.  On the other hand, the projection of the plateau shell satisfies
`|y|<=(a+delta_0)R`.  Since `s_*-2h>delta_0`, `I_+` and this projection are
separated by a fixed multiple of `R`.

## 3. Arithmetic and spectral-support audit

The smallest multiple `K` of `16m` above `R^(-3/2)` satisfies

\[
 R^{-3/2}\le K<R^{-3/2}+16m\le2R^{-3/2}
\]

for large `L`.  Both `n=K/(16m)` and `q=3K/2` are integers.  The Fourier
support of `d_n^(2m)` is the Minkowski sum of `2m` copies of `[-n,n]`, hence
is contained in `[-2mn,2mn]=[-K/8,K/8]`.  The two carrier shifts give

\[
 [11K/8,13K/8]\cup[-13K/8,-11K/8],
\]

which is contained in `{K<=|j|<=2K}`.  The packet is real because both
`d_n^(2m)` and the carrier cosine are real.

## 4. Dirichlet concentration audit

The sine quotient in R.21 gives

\[
 |d_n(z)|\le C\min\{1,(n\,\operatorname {dist}
 (z,2\pi\mathbb Z))^{-1}\}.
\]

Raising the square of `G_K` to its envelope and integrating the two-sided
power tail gives

\[
 \|G_K\|_2^2\le C_mA^2n^{-1}.
\]

On a fixed interval `|z|<=c_m/K`, both the normalized Dirichlet kernel and
`cos(qz)` are bounded away from zero.  Its length is comparable to
`K^(-1)`, hence to `n^(-1)` for fixed `m`, which gives the matching lower
bound.

Outside `dist(y,y_0)>=rR`, the pointwise envelope is
`C_mA(nR)^(-2m)`.  Squaring and integrating
`n^(-4m) z^(-4m)` from `rR` to a fixed radius gives

\[
 C_{m,r}A^2n^{-4m}R^{1-4m}
 =C_{m,r}A^2n^{-1}(nR)^{1-4m}.
\]

Since `nR` tends to infinity and `1-4m<0`, the relative tail vanishes.

## 5. Exact-solution audit

Let `H(t,y)=e^(t partial_2^2)G_K(y)`.  Then
`F_K(t,y)=H(t,y-Bt)` satisfies

\[
 \partial_tF_K+B\partial_2F_K-\partial_2^2F_K=0.
\]

For `u_K=(0,B,F_K(x_2))`, the divergence is zero and
`(u_K dot grad)u_K=(0,0,B partial_2F_K)`.  Thus the third component of the
unforced Navier--Stokes equation is exactly the preceding scalar equation;
the first two components are constant.  Constant pressure is admissible.
There is no omitted nonlinear remainder.

On `0<=t<=K^(-2)`, every Fourier multiplier in the support has squared
size at least `e^(-8)`, because `|j|<=2K`.  Translation is unitary.  This
proves the coarse global lower bound R.31.

## 6. Heat-localization audit

The circle heat kernel is the periodization of the one-dimensional Gaussian.
For sets separated by a fixed multiple of `R`, its Gaussian tail and the
Davies--Gaffney `L^2` estimate contribute `exp(-cR^2/t)`.  Since
`t<=K^(-2)`, this is at most `exp(-c(KR)^2)`.  Here
`KR` is comparable to `R^(-1/2)` and tends to infinity.

The drift displacement obeys

\[
 |B|T=bR^{-2}K^{-2}\le bR,
\]

which is smaller than every selected separation by R.27.  Splitting the
initial packet at distance `hR/2` from `y_0` therefore yields

\[
 \|1_{I_+^c}F_K(t)\|_2
 \le C_m\left[(nR)^{(1-4m)/2}
 +e^{-c(KR)^2}\right]A n^{-1/2}.
\]

This is `o(A n^(-1/2))`.  Combining it with R.31 leaves a fixed fraction of
the energy in `I_+`.  The negative cutoff cap is farther from `y_0`, so the
same argument gives R.34.

## 7. Signed-flux audit

With `B<0`, `BD_R>=0` for `y>0` and `BD_R<=0` for `y<0`.  The full positive
half-line may be discarded except for `I_+`.  On `I_+`, R.18 and the local
energy lower bound give `c|B|aR A^2/n` at each time.  The absolute negative
cap contribution is `o(|B|aR A^2/n)` and can be absorbed.  Integration over
`T=K^(-2)` gives R.35 with the stated sign.  No absolute-value upper bound is
being misused as a lower bound.

## 8. Plateau-mass audit

Every plateau fibre projects into `|y|<=(a+delta_0)R`, a fixed distance from
the transported packet center.  Split `G_K` into a central portion and its
far tail.  Gaussian heat leakage bounds the central contribution by
`CA exp(-c(KR)^2)`; `L^infinity` contraction and R.26 bound the far
contribution by `CA(nR)^(-2m)`.  The exponential is smaller than this fixed
power for large `L`.

The plateau shell volume is at most `Ca^2R^3`.  Cubing the pointwise bound
and integrating for `K^(-2)` gives exactly

\[
 M_{K,{\rm plat}}
 \le C_mA^3a^2R^3K^{-2}(nR)^{-6m}.
\]

## 9. Normalization and exponent audit

Taking the two-thirds power of the preceding mass row and dividing R.35 by
it gives

\[
 \frac{\mathcal T_K}{M_{K,{\rm plat}}^{2/3}}
 \ge c_m|B|a^{-1/3}R^{-1}n^{-1}K^{-2/3}(nR)^{4m}.
\]

The quotient of the normalized variables contributes
`R^(1/3)omega^(1/3)`.  Using `|B|=bR^(-2)`, `n asymp K`, and
`K asymp R^(-3/2)` leaves

\[
 c_mba^{-1/3}R^{-2m-1/6}\omega^{1/3}.
\]

At `m=1`, exact arithmetic gives

\[
 \frac{13\rho}{24}-\frac{c_\gamma}{12}
 =\frac{304373}{952560000}>0,
 \qquad
 -\frac{13}{6}+\frac{c_\gamma}{3\rho}
 =-\frac{304373}{214326}.
\]

The amplitude powers are `A^2/A^2`, so `A` cancels.

## 10. Claim-boundary audit

- The result disproves only a uniform payment by the cubic mass on the
  canonical plateau shell for arbitrary high-band packets.
- The full cutoff support includes the outer cap where the packet lives.
- The complete Version-M exterior payment is not identified with the
  plateau-only atom and can also count the constant background component.
- The constant background has not been embedded in the frozen mean-zero,
  inversion-paired Version-M subclass.
- The note does not claim a counterexample to E.24, a failure of all signed
  methods, or a nonlinear instability.
- The example is globally smooth for every `A`, so it has no implication of
  singularity formation.
- Complete-clock extraction, fixed deletion, suitable-weak transfer, and
  regularity remain open.  No novelty or priority claim is made.
  **NOT CLAY.**

## Audit conclusion

The geometry, spectrum, exact Navier--Stokes realization, heat localization,
flux sign, plateau tail, normalization, and frozen exponent are mutually
consistent.  The note is ready for independent analytic review and finite
certificate construction.
