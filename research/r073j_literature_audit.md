# R0.73J primary-literature audit: periodic Rayleigh--Evans counting

**Search date:** 2026-08-30  
**Audit type:** two-pass targeted research using primary papers and author or
publisher copies  
**Frozen target:** `research/r073j_problem_freeze.md`  
**Public status:** source stage  
**Claim status:** literature boundary only; no R0.73J interval contract is
closed here

## 1. Direct decision

I did not locate a theorem that covers the exact two-harmonic profile

\[
 W_d(x)=-\frac12e^{-d}\sin x+\frac14e^{-4d}\sin2x
\]

and simultaneously gives an explicit positive \(d\)-window, a unique
algebraically simple rightmost eigenvalue, a real-part gap, and a kinetic
left/right overlap bound.

The literature supplies the first three pieces of methodology used by the
present profile-specific theorem:

1. periodic monodromy Evans functions and algebraic multiplicity;
2. an Euler/Rayleigh Hill--Evans realization;
3. interval contour enclosures, Chebyshev interpolation, and winding
   transfer;
The fourth item reviewed below, general Hamiltonian index formulae, is an
alternative route that explains what an index budget of one would imply.  I
do not use it here because its standard Euler hypotheses fail for this
profile.

The missing result is therefore concrete rather than bibliographic: the
full complex contour and parameter-uniform validated calculation for this
profile, together with the exact kinetic-operator multiplicity bridge.

## 2. Periodic Evans zero order and algebraic multiplicity

Kevin Zumbrun, *2-Modified Characteristic Fredholm Determinants, Hill's
Method, and the Periodic Evans Function of Gardner*, Z. Anal. Anwend. 31
(2012), 463--472;
[publisher PDF](https://ems.press/content/serial-article-files/35837),
[DOI](https://doi.org/10.4171/ZAA/1469).

- Proposition 2.3 proves that the 2-modified Fredholm Evans function has
  zeros at the periodic eigenvalues with matching multiplicity.
- Definition 4.1 sets
  \(E(\lambda)=\det(\Psi(X,\lambda)-I)\).
- Proposition 4.2 gives the corresponding location-and-multiplicity result
  for the monodromy Evans function.
- Theorem 5.1 shows that the Fredholm and monodromy functions differ by an
  explicit nonvanishing analytic factor.

This is direct support for the standard fixed periodic second-order class.
It is a method precedent, not a black-box proof for the present Rayleigh
pencil: here the spectral parameter occurs rationally after division by
\(W-c\), while the undivided pencil has a differential spectral weight.
R0.73J therefore includes its own analytic-equivalence proof.

Mathew A. Johnson and Kevin Zumbrun, *Convergence of Hill's Method for
Nonselfadjoint Operators*, SIAM J. Numer. Anal. 50 (2012), 64--78;
[preprint](https://arxiv.org/abs/1009.3908),
[DOI](https://doi.org/10.1137/100809349).

- Theorem 3.4 matches generalized periodic Evans zeros and eigenvalue
  multiplicities.
- Corollary 3.9 gives Hill convergence in location and multiplicity on a
  bounded region whose boundary contains no spectrum.
- The discussion after Theorem 3.10 explicitly warns that determinant
  convergence alone gives no effective convergence rate for its zeros and
  that finite Hill eigenvalues alone do not provide such a rate.

This supports the use of Fourier truncations as diagnostics.  It also rules
out treating a cutoff sweep as the R0.73J certificate.

## 3. The closest periodic Euler construction

Holger R. Dullin and Robert Marangell, *An Evans function for the linearised
2D Euler equations using Hill's determinant*, Physica D 457 (2024), 133954;
[author PDF](https://www.maths.usyd.edu.au/u/marangel/publications/EulerHillEvansFinal3.pdf),
[DOI](https://doi.org/10.1016/j.physd.2023.133954).

- Proposition 2.1 reduces the separated Euler problem to a complex Hill
  equation with periodic or quasi-periodic boundary conditions.
- Theorem 5.1 constructs a class Evans function analytic away from the
  velocity range and states that its zero order is the algebraic
  multiplicity of the separated periodic problem.
- Theorem 6.1 combines finitely many class functions for the special
  single-harmonic cosine equilibrium.

This paper is the closest direct Euler precedent.  Its sharp root count is
specific to the cosine profile and its explicit Hill determinant.  It does
not count roots for the present two-harmonic cubic profile.  Its convention
also identifies Euler multiplicity through the separated periodic problem;
R0.73J separately checks Jordan chains of the original kinetic vorticity
operator.

## 4. Validated Evans computations and parameter interpolation

Blake Barker and Kevin Zumbrun, *Numerical proof of stability of viscous
shock profiles*, Math. Models Methods Appl. Sci. 26 (2016), 2451--2469;
[preprint](https://arxiv.org/abs/1601.00837),
[DOI](https://doi.org/10.1142/S0218202516500585).

The paper combines interval arithmetic, analytic and computer-assisted
error bounds, Chebyshev interpolation, and a contour winding calculation.
Sections 2.2--2.5 describe interval arithmetic, wrapping control, separate
error tracking, and interpolation on Bernstein ellipses.  Lemma 3.5 and the
final proof enclose the Evans image on a complete contour.

The limitation is equally relevant.  Theorem 1.1 verifies seven discrete
shock parameters.  Remark 1.2 says that carrying a parameter interval
naively through the ODE is not computationally useful and that an additional
interpolation layer is needed for a sizeable family.  Section 3.4 obtains
only an unspecified neighborhood of each certified point by continuity.

R0.73J adopts that missing layer explicitly: validated ODE values at
Chebyshev nodes in \(d\), a complex-ellipse remainder bound, a certified
range of the interpolant, and a separate bound for each contour box.

The exact interpolation constants were checked separately.  Kuan Xu,
*The Chebyshev points of the first kind*, Applied Numerical Mathematics 102
(2016), 17--30;
[author manuscript](https://kar.kent.ac.uk/58498/1/firstkind_revision2.pdf),
[DOI](https://doi.org/10.1016/j.apnum.2015.12.002), Theorem 4, gives

\[
 \Lambda_n\le1+\frac2\pi\log(n+1)
\]

for degree-\(n\) interpolation at the \(n+1\) roots of \(T_{n+1}\).
Thus the degrees used here have \(\Lambda_n<4\).  Xu's Theorems 1--2 give
the exact aliasing of higher Chebyshev modes on that root grid.  Combining
this with the coefficient bound in Lloyd N. Trefethen, *Approximation Theory
and Approximation Practice*, Theorem 8.1;
[author sample](https://people.maths.ox.ac.uk/trefethen/trefethen_sample.pdf),
gives the first-kind-root interpolation remainder

\[
 \|f-I_nf\|_\infty
 \le\frac{4M\rho^{-n}}{\rho-1}.
\]

Here \(n\) is the polynomial degree and the node count is \(n+1\).  The
exponent is therefore \(-n\), not minus the node count.

## 5. Degenerate critical layers

Dongfen Bian and Emmanuel Grenier, *Singularities of Rayleigh equation*,
2024; [preprint](https://arxiv.org/abs/2408.00977).

Definition 1.1 and Theorem 1.2 describe local Rayleigh solutions near
critical points of arbitrary degeneracy.  The cubic zero at \(d=0,c=0\) is
an order-three object of that type.  The paper does not provide a periodic
Evans count or a rightmost eigenvalue theorem.

This singular machinery is not needed on the R0.73J contours.  If
\(\operatorname{Re}\lambda\ge11/100\) and \(c=2i\lambda\), then
\(\operatorname{Im}c\ge22/100\); a real \(W_d(x)\) cannot equal \(c\).
It becomes relevant only if a later contour is pushed to the imaginary axis
or through \(c=0\).

## 6. Hamiltonian index route and why its standard Euler application fails

Zhiwu Lin and Chongchun Zeng, *Instability, index theorem, and exponential
trichotomy for Linear Hamiltonian PDEs*, 2021 revision;
[preprint](https://arxiv.org/abs/1703.04016).

Theorem 2.3 proves under (H1)--(H3)

\[
 k_r+2k_c+2k_i^{\le0}+k_0^{\le0}=n^-(L).
\]

Corollary 2.2 states that an index remainder of one yields exactly one
simple stable/unstable real pair.  This explains why a successful index-one
realization would be powerful.

The ready-made two-dimensional Euler application in Section 11.5 assumes
\(-\Delta\psi_0=g(\psi_0)\), \(g'(\psi_0)>0\), and additional kernel
control.  For the present shear,

\[
 g'(\psi_0)=-\frac{W_d''}{W_d}.
\]

At \(d=0\),

\[
 -\frac{W_0''}{W_0}\sim-\frac6{x^2},
\]

so the weight is negative and singular at the cubic zero.  For small
positive \(d\), the exact limit is

\[
 \lim_{x\to0}-\frac{W_d''}{W_d}
 =\frac{e^{-d}-4e^{-4d}}{e^{-d}-e^{-4d}}<0,
 \qquad 0<d<\frac{\log4}{3}.
\]

The standard positive weighted Euler space in Theorem 11.5 therefore does
not apply.  This does
not rule out a new singular Hamiltonian factorization; it only means that
such a theory would be a longer, separate route.

Zhiwu Lin, *Instability of Some Ideal Plane Flows*, SIAM J. Math. Anal. 35
(2003), 318--356; [DOI](https://doi.org/10.1137/S0036141002406266),
likewise assumes for its relevant odd-flow construction that
\(-U''/U\) is bounded.  The same \(-6/x^2\) behavior prevents a direct
application.

## 7. Howard enclosure

The outer spectral disk follows from the classical substitution used in
Louis N. Howard, *Note on a paper of John W. Miles*, J. Fluid Mech. 10
(1961), 509--512;
[author-hosted scan](https://www.math.fsu.edu/~moore/SeminarFiles/Howard61.pdf).

For the periodic unstratified problem the boundary term also vanishes, and
the identity is particularly short.  R0.73J records the proof directly and
uses the sharper profile-specific bound
\(\|W_d\|_\infty\le3\sqrt3/8\).

## 8. Final source boundary

| Claim | Literature status | R0.73J obligation |
|---|---|---|
| monodromy Evans zeros count periodic eigenvalues with multiplicity | established for standard periodic operator classes | prove the analytic equivalence for this rational Rayleigh pencil and kinetic space |
| Euler separation admits a Hill--Evans formulation | established, with a sharp count for a single harmonic | build and validate the two-harmonic monodromy |
| interval Evans winding can be a mathematical proof | established methodology | cover the complete contour and the complete \(d\)-window |
| finite Hill matrices converge in location and multiplicity | established asymptotically | do not replace effective error bounds by a cutoff sweep |
| cubic critical layers have a local singular theory | established locally | avoid them at positive contour real part; do not claim a global count from that theory |
| index budget one implies a simple real unstable pair | established abstractly | standard Euler hypotheses fail here; do not cite them as this theorem |

The literature search is saturated for the present decision: additional
general searches are unlikely to remove the profile-specific interval and
operator-multiplicity work.  Those two items remain the original content of
R0.73J.
