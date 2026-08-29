# R0.73C C4 spectral screen and Fourier-tail enclosure route

> **Working-note status (2026-08-30):** this finite spectral route predates
> the validated periodic-ODE certificate.  C4 is now closed by the monodromy
> sign theorem, not by the finite Fourier or sampled-contour calculations in
> this note.  C5 remains open.

**Date:** 2026-08-30  
**Role:** independent finite diagnostic and proof design  
**Decision:** the collision profile has a very strong unstable candidate at
`gamma=1/2`, but `frozenCollisionRayleighInstability=TO_PROVE` until the
Fredholm contour computation below is interval-certified.

## 1. Operator, Fourier matrix, and claim boundary

At `d=0`, put

\[
 W=-\frac12\sin x+\frac14\sin 2x,
 \qquad
 W''=\frac12\sin x-\sin 2x,
 \qquad
 L_\gamma=-\partial_x^2+\gamma^2,
\]

and

\[
 A_\gamma=-i\gamma\left(M_W+M_{W''}L_\gamma^{-1}\right)
 \quad\hbox{on }L^2(\mathbb T).
\]

In the normalized Fourier basis, the exact matrix entries are

\[
 (A_\gamma)_{mn}
 =-i\gamma\left(\widehat W_{m-n}
 +\frac{\widehat {W''}_{m-n}}{n^2+\gamma^2}\right),
 \qquad m,n\in\mathbb Z.                                      \tag{1.1}
\]

Only the shifts `m-n=+-1,+-2` occur.  The source
[`r073c_spectral_screen_agent.py`](r073c_spectral_screen_agent.py) builds
(1.1) independently of the R0.73A/R0.73B experiment sources.  It uses no
randomness and records both ordinary Galerkin matrices and a different
finite-rank approximation having an actual operator-norm tail bound.

Every number in Sections 2--3 is a finite computation.  In particular, a
small embedded eigen-residual and stable cutoff digits do not prove that a
nonnormal infinite-dimensional operator has an eigenvalue.

## 2. Ordinary Fourier screen

For `gamma=1/2`, the rightmost eigenvalue of `P_N A_gamma P_N` is:

| `N` | rightmost eigenvalue | exact embedded residual | projector condition |
|---:|---:|---:|---:|
| 8 | 0.170411082418835 | 3.2791e-3 | 3.90791 |
| 12 | 0.170407928974301 | 8.6166e-4 | 3.90821 |
| 16 | 0.170407977450910 | 2.3015e-4 | 3.90821 |
| 24 | 0.170407976920295 | 1.6680e-5 | 3.90821 |
| 32 | 0.170407976920433 | 1.2184e-6 | 3.90821 |
| 48 | 0.170407976920434 | 6.5522e-9 | 3.90821 |
| 64 | 0.170407976920433 | 3.5374e-11 | 3.90821 |
| 96 | 0.170407976920434 | 2.1021e-15 | 3.90821 |
| 128 | 0.170407976920434 | 1.8431e-15 | 3.90821 |

Here the embedded residual is not the residual inside the matrix.  The
normalized `P_N` eigenvector is extended by zero, the complete banded action
is evaluated through modes `+- (N+2)`, and the resulting `l2` residual is
reported.  Thus the residual includes all omitted output coefficients, but
it is still only pseudospectral evidence without a complement inverse.

The same matrices also suggest a second unstable conjugate pair

\[
 0.040539390616\ \mathbin{\pm}\ 0.176137671494 i.             \tag{2.1}
\]

The proof route below intentionally encloses only the isolated real
candidate; (2.1) is not needed for C4.

At `N=128`, the prescribed row screen gives:

| `gamma` | sampled right edge | interpretation |
|---:|---:|---|
| 1/4 | 0.095519248444876 | stable digits, real candidate |
| 1/2 | 0.170407976920434 | stable digits, real candidate |
| 3/4 | 0.203232470871072 | stable digits, real candidate |
| 1 | 0.174120920035151 | stable eigenvalue digits; tail converges slower |
| `sqrt(7)/2` | 0.00890198 + 0.40575142 i | not the neutral mode; finite-section pollution near the essential spectrum |
| 3/2 | 0.00672409 + 0.48246860 i | right edge decreases with `N`; no unstable eigenvalue claimed |

This last distinction is essential.  The essential spectrum of
`-i gamma M_W` lies on the imaginary axis.  Near or beyond the neutral
threshold, `max Re spectrum(P_N A P_N)` is therefore a poor eigenvalue
selector and visibly drifts toward that axis.

As an independent check of the analytic threshold calculation, selecting
the *real* branch below `gamma_0=sqrt(7)/2` gives

| `gamma` | `eta=sigma/gamma` | `(7/4-gamma^2)/4` | ratio |
|---:|---:|---:|---:|
| 1.300 | 0.0148931901148 | 0.0150000000000 | 0.992879 |
| 1.320 | 0.00189904698062 | 0.00190000000000 | 0.999498 |
| 1.321 | 0.00123945317007 | 0.00123975000000 | 0.999761 |
| 1.322 | 0.00057898730395 | 0.00057900000000 | 0.999978 |

This supports, but does not prove, the local law
`eta ~ (7/4-gamma^2)/4` obtained by projecting the singular neutral mode.
The ordinary Lin/Tollmien criterion still cannot simply be quoted: the
cubic zero makes `-W''/W` singular, and the standard bounded/class-F
hypotheses fail.

## 3. Replace Galerkin convergence by a norm-convergent approximation

Split

\[
 B=-i\gamma M_W,
 \qquad C=-i\gamma M_{W''}L_\gamma^{-1},
 \qquad A_\gamma=B+C.                                        \tag{3.1}
\]

`B` is skew-adjoint and `C` is compact.  For the Fourier projection `P_N`,
define the infinite-dimensional operator

\[
 A_\gamma^{(N)}=B+CP_N.                                     \tag{3.2}
\]

Unlike `P_N A P_N`, (3.2) converges in operator norm.  Indeed,

\[
 \boxed{
 \|A_\gamma-A_\gamma^{(N)}\|
 \le \delta_N
 :=\frac{\gamma\|W''\|_\infty}{(N+1)^2+\gamma^2}.}          \tag{3.3}
\]

The exact maximizer calculation uses

\[
 t_*=\frac{1-\sqrt{129}}{16},
 \qquad
 \|W''\|_\infty
 =\sqrt{(1-t_*^2)(1/2-2t_*)^2}
 =1.36790755203211\ldots .                                  \tag{3.4}
\]

For `gamma=1/2` and `N=48`,

\[
 \boxed{\delta_{48}=2.84832389803667\times10^{-4}.}          \tag{3.5}
\]

A large outer Fourier screen of (3.2), explicitly labelled as a second
finite diagnostic, produces:

| active `N` | rightmost eigenvalue of outer compression of `B+CP_N` |
|---:|---:|
| 8 | 0.170407913958934 |
| 12 | 0.170407977289316 |
| 16 | 0.170407976918968 |
| 24 | 0.170407976920434 |
| 32 | 0.170407976920435 |
| 40 | 0.170407976920434 |
| 48 | 0.170407976920433 |

The outer cutoff was 192.  These digits motivate the contour but play no
role in the future proof once the finite Fredholm matrix is certified.

## 4. Finite Fredholm reduction on a positive-half-plane contour

Choose exact decimal/rational contour data

\[
 \Gamma:\quad |z-0.1704|=0.06,
 \qquad \inf_{z\in\Gamma}\operatorname{Re}z=0.1104.          \tag{4.1}
\]

Since `B` is skew-adjoint and the whole disk lies in `Re z>0`,
`D_z=z-B=z+i gamma W` is invertible throughout the disk.  Put

\[
 M_N(z)=I_{P_N}-P_ND_z^{-1}CP_N.                             \tag{4.2}
\]

The entries of this `(2N+1)`-dimensional analytic matrix are

\[
 (M_N(z))_{mn}
 =\delta_{mn}
 +\frac{i\gamma}{n^2+\gamma^2}
 \widehat{\left(\frac{W''}{z+i\gamma W}\right)}_{m-n}.
                                                                    \tag{4.3}
\]

Zeros of `det M_N` inside `Gamma` are precisely the eigenvalues of
`A_gamma^(N)` there, with algebraic multiplicity.  The Woodbury formula is

\[
 (z-A_\gamma^{(N)})^{-1}
 =D_z^{-1}
 +D_z^{-1}CP_NM_N(z)^{-1}P_ND_z^{-1}.                       \tag{4.4}
\]

For `N=48`, 2,048 contour nodes and 32,768-point periodic quadrature give
the following **sampled** values:

| quantity | finite value |
|---|---:|
| `min_Gamma sigma_min(M_48)` | 0.0569136303558 |
| `max_Gamma ||M_48^-1||` | 17.5704834457 |
| `max_Gamma ||W''/(z+i gamma W)||_2` | 3.59794699811 |
| sampled determinant winding | 1 |
| largest unwrapped phase step | 0.00465431 rad |

The minimum occurred near `theta=1.435806`.  These margins are large enough
to target the interval ceilings

\[
 J:=\sup_\Gamma\left\|\frac{W''}{z+i\gamma W}\right\|_2
 \le3.7,
 \qquad
 \sup_\Gamma\|M_{48}^{-1}\|\le20.                           \tag{4.5}
\]

They are not yet certified inequalities.

## 5. The complete conditional constant chain

With normalized periodic `L2`,

\[
 S_\gamma:=\sum_{n\in\mathbb Z}(n^2+\gamma^2)^{-2}
 =\frac{\pi}{2\gamma^3}\coth(\pi\gamma)
 +\frac{\pi^2}{2\gamma^2}\operatorname{csch}^2(\pi\gamma). \tag{5.1}
\]

At `gamma=1/2`,

\[
 S_{1/2}=17.4287170358769\ldots .                            \tag{5.2}
\]

The first finite-rank factor in (4.4) has a Hilbert--Schmidt bound

\[
 \|D_z^{-1}CP_N\|
 \le \gamma J\sqrt{S_\gamma}.                              \tag{5.3}
\]

Consequently, if (4.5) is interval-certified,

\[
 \|D_z^{-1}CP_{48}\|\le7.72332726585,
\]

\[
 \boxed{
 \sup_{z\in\Gamma}\|(z-A_\gamma^{(48)})^{-1}\|
 \le \frac{1+7.72332726585\times20}{0.1104}
 =1408.21146121.}                                           \tag{5.4}
\]

Combining (3.5) and (5.4) gives

\[
 \boxed{
 \delta_{48}
 \sup_\Gamma\|(z-A_\gamma^{(48)})^{-1}\|
 \le0.401104236<1.}                                        \tag{5.5}
\]

Thus there is already a comfortable, explicit Neumann margin.  Once a
validator proves both (4.5) and winding number one, the homotopy

\[
 A_t=A_\gamma^{(48)}+t(A_\gamma-A_\gamma^{(48)}),
 \qquad0\le t\le1,
\]

has no spectrum on `Gamma`.  Its Riesz projection rank stays one.  The full
operator `A_{1/2}(0)` then has exactly one eigenvalue in the disk (4.1), and
in particular

\[
 \boxed{\operatorname{Re}\sigma_*>0.1104.}                  \tag{5.6}
\]

That would close C4 with a substantially stronger quantitative statement
than mere positivity.

## 6. What the interval validator must still prove

The smallest honest next proof step is one deterministic validator for
`N=48` and (4.1), not a larger floating-point sweep.  It should:

1. enclose the Fourier coefficients in (4.3) with complex balls;
2. prove `J<=3.7` and, for the contour derivative,
   `J_2=sup ||W''/(z+i gamma W)^2||_2<=24`;
3. at sufficiently many contour nodes, prove
   `sigma_min(M_48)>0.05` (or directly `||M_48^-1||<20`);
4. use the derivative bound
   `||M_48'(z)|| <= gamma sqrt(S_gamma) J_2` to cover the arcs between
   nodes;
5. certify that `det M_48` has winding number one, either by interval phase
   tracking or by the argument-principle integral
   `tr(M^-1 M')`;
6. emit the interval precisions, node count, all margins, hashes, and an
   independent recomputation.

A useful quadrature simplification is available.  On `Gamma`,
`Re z>=0.1104`.  For the strip `|Im x|<=0.1`, the Fourier `l1` estimate

\[
 \gamma|W(x+iy)-W(x)|
 \le\frac12\left[\frac12(e^{|y|}-1)
 +\frac14(e^{2|y|}-1)\right]<0.0540
\]

keeps `z+i gamma W(x+iy)` uniformly away from zero.  Analytic trapezoid
aliasing therefore decays exponentially; a ball-arithmetic FFT or direct
residue computation of the associated quartic rational function can make
the Fourier coefficient enclosure cheap.  This analytic-strip error must
be written into the validator rather than inferred from agreement of two
quadrature sizes.

## 7. Decision ledger

| statement | status after this audit |
|---|---|
| exact finite Fourier matrix (1.1) | CHECKED |
| `gamma=1/2` leading candidate `0.170407976920434` | CHECKED AT DECLARED CUTOFFS |
| exact embedded residual through omitted output modes | CHECKED AT DECLARED CUTOFFS |
| norm-convergent finite-rank approximation and tail (3.3) | ANALYTICALLY PROVED |
| Fredholm reduction (4.2)--(4.4) | ANALYTICALLY PROVED |
| sampled contour margins and winding | FINITE DIAGNOSTIC |
| conditional constant chain (5.1)--(5.5) | ANALYTICALLY PROVED GIVEN (4.5) |
| interval Fourier coefficients / inverse / winding | TO PROVE |
| infinite-dimensional unstable eigenvalue C4 | TO PROVE |
| logarithmic fast-time transfer C5 | OPEN; not addressed by frozen spectrum |
| nonlinear Navier--Stokes or Clay implication | OPEN |

The main conclusion is therefore not “cutoff convergence proves
instability.”  It is narrower and more useful: the candidate is strong
enough that an `N=48` finite Fredholm/Riesz certificate has a fully explicit
operator-tail margin of about `0.40`, so C4 appears realistically
certifiable without a large computation.
