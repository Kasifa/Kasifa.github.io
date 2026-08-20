# R0.69B — A critical transverse-stability gate for the periodic shear packet

## 1. Result

Let \(U_r\) be the exact R0.69A invariant-shear solution with

\[
 M_r=16^r,\qquad H_r=4M_r,\qquad
 A_r=\varepsilon_r\sqrt{H_r},\qquad
 \varepsilon_r^2=\left(\frac{16}{\lambda}\right)^r,
\tag{1.1}
\]

where \(\lambda>25\) is the dominant quartic root certified in R0.66.  Although
the physical Fourier amplitude \(A_r\) grows exponentially, the initial data
become geometrically small in the scale-critical periodic \(BMO^{-1}\) norm:

\[
 \boxed{
 \|U_r(0)\|_{BMO^{-1}_{\rm per}}
 \le (6+4\sqrt{2})\,\varepsilon_r
 \le (6+4\sqrt{2})\rho^r,}
\qquad
 \rho:=\sqrt{\frac{16}{\lambda_-}}<0.797586,
\tag{1.2}
\]

with the exact lower root endpoint

\[
 \lambda_-=\frac{50303178668203}{2000000000000}.
\tag{1.3}
\]

Consequently, if \(\eta_{\rm KT}^{\rm per}>0\) denotes any admissible
small-data threshold for the periodic Koch--Tataru fixed-point theorem, then
for every \(\theta\in(0,1)\) and all sufficiently large \(r\),

\[
 \|U_r(0)\|_{BMO^{-1}_{\rm per}}\le\theta\eta_{\rm KT}^{\rm per}.
\tag{1.4}
\]

Every divergence-free, genuinely three-dimensional perturbation \(w_{0,r}\)
satisfying

\[
 \|w_{0,r}\|_{BMO^{-1}_{\rm per}}
 <(1-\theta)\eta_{\rm KT}^{\rm per}
\tag{1.5}
\]

therefore gives globally regular total data \(U_r(0)+w_{0,r}\).  The allowed
ball has a radius independent of \(r\).  In particular, a transverse
singularity mechanism built on this family cannot remain perturbative in the
same critical topology: it must eventually carry an order-one
\(BMO^{-1}_{\rm per}\) cost.

This is a stability gate, not a resolution of the general three-dimensional
problem.  The universal threshold is not computed here, and data outside the
small critical ball remain uncontrolled.

## 2. Exact perturbation equation

Write the total solution as

\[
 u=U_r+w,\qquad p=P_r+q,
\tag{2.1}
\]

where \(U_r=(0,F_r(x_1,t),G_r(x_1,x_2,t))\) is the exact smooth base
solution.  Subtracting the equation for \(U_r\) from the equation for \(u\)
gives

\[
 \boxed{
 \begin{aligned}
 \partial_tw-\Delta w
 +(U_r\cdot\nabla)w
 +(w\cdot\nabla)U_r
 +(w\cdot\nabla)w+\nabla q&=0,\\
 \nabla\cdot w&=0.
 \end{aligned}}
\tag{2.2}
\]

No term in (2.2) is omitted.  In particular, the term
\((w\cdot\nabla)U_r\) is the transverse coupling that destroys the triangular
scalar reduction used from R0.60 through R0.69A.

For smooth \(w\), incompressibility cancels the base-transport and
self-transport terms in \(L^2\):

\[
 \boxed{
 \frac12\frac{d}{dt}\|w(t)\|_2^2+\|\nabla w(t)\|_2^2
 =-\int_{\mathbb T^3}w_i\,\partial_i(U_r)_j\,w_j\,dx.}
\tag{2.3}
\]

Thus

\[
 \frac12\frac{d}{dt}\|w\|_2^2+\|\nabla w\|_2^2
 \le \|\operatorname{sym}\nabla U_r\|_\infty\|w\|_2^2.
\tag{2.4}
\]

Equation (2.4) is exact but supercritical as a uniform research gate.  It
would require direct control of
\(\int\|\operatorname{sym}\nabla U_r\|_\infty dt\), while the natural
smallness already visible in the packet is the scale-critical heat--Carleson
quantity in (1.2).  R0.69B therefore records (2.3) but does not replace the
critical argument by a Lipschitz Gronwall estimate.

## 3. Source of the critical bound

R0.59 proved for every dyadic \(L,M\), \(H=4LM\), and amplitude \(A\) that
the tensor Rudin--Shapiro packet satisfies

\[
 \|u_0\|_{BMO^{-1}_{\rm per}}
 \le \frac{\sqrt{2}\,C_TA}{\sqrt H},
\qquad
 C_T=(1+\sqrt{2})(2+\sqrt{2})=4+3\sqrt{2}.
\tag{3.1}
\]

The norm is the periodic heat--Carleson norm

\[
 \|f\|_{BMO^{-1}_{\rm per}}
 :=
 \sup_{x,\ 0<R\le1}
 \left(
 \frac1{|B(x,R)|}
 \int_0^{R^2}\int_{B(x,R)}
 |e^{t\Delta}f(y)|^2\,dy\,dt
 \right)^{1/2}.
\tag{3.2}
\]

For the R0.69A family, \(L=1\) and \(A=A_r=\varepsilon_r\sqrt{H_r}\).
Substitution into (3.1) gives

\[
 \sqrt{2}\,C_T
 =\sqrt{2}(4+3\sqrt{2})=6+4\sqrt{2},
\tag{3.3}
\]

which proves the first inequality in (1.2).  R0.66 gives
\(\lambda\ge\lambda_-\), so

\[
 \varepsilon_r
 =\left(\frac{16}{\lambda}\right)^{r/2}
 \le
 \left(\frac{16}{\lambda_-}\right)^{r/2}
 =\rho^r.
\tag{3.4}
\]

The source-bound interval audit gives

\[
 0.7975855452903290<\rho<0.7975855452903292.
\tag{3.5}
\]

For orientation only, the certified upper bound
\((6+4\sqrt{2})\rho^r\) first falls below \(1,10^{-1},10^{-2},10^{-3}\)
at \(r=11,22,32,42\), respectively.  These four numerical thresholds are
not substitutes for the unknown universal
\(\eta_{\rm KT}^{\rm per}\).

## 4. Critical transverse ball

The Koch--Tataru fixed-point theorem has the following form: there is a
universal \(\eta>0\) such that every divergence-free datum with
\(BMO^{-1}\) norm below \(\eta\) generates a unique global mild solution in
the Koch--Tataru solution space.  The periodic version follows from the same
heat and Stokes kernel estimates on the flat torus; equivalently, one applies
the theorem to the mean-zero periodic extension and uses the equivalence of
the periodic and periodic-extension heat--Carleson norms.  Denote an
admissible threshold after this norm equivalence by
\(\eta_{\rm KT}^{\rm per}\).

The triangle inequality and (1.2) give

\[
 \|U_r(0)+w_{0,r}\|_{BMO^{-1}_{\rm per}}
 \le
 (6+4\sqrt{2})\rho^r
 +\|w_{0,r}\|_{BMO^{-1}_{\rm per}}.
\tag{4.1}
\]

Hence the exact sufficient condition is

\[
 \boxed{
 (6+4\sqrt{2})\rho^r
 +\|w_{0,r}\|_{BMO^{-1}_{\rm per}}
 <\eta_{\rm KT}^{\rm per}.}
\tag{4.2}
\]

For a chosen fraction \(\theta\in(0,1)\), the base condition in (1.4) is
guaranteed whenever

\[
 r\ge
 \left\lceil
 \frac{\log((6+4\sqrt{2})/(\theta\eta_{\rm KT}^{\rm per}))}
 {-\log\rho}
 \right\rceil.
\tag{4.3}
\]

This formula is symbolic because the fixed-point literature generally states
the threshold existentially.  No numerical value for
\(\eta_{\rm KT}^{\rm per}\) is asserted.

For smooth periodic data, the mild solution is smooth for positive time.
The higher-regularity results for Koch--Tataru solutions also provide spatial
derivative decay and analyticity.  Thus (4.2) is a genuine global
regularity conclusion for transverse data, not only a formal stability
estimate.

## 5. What this decides

The result is stronger than symmetry-specific smoothness in one direction:

1. the unperturbed R0.69A packet is globally smooth for every \(r\) because
   of its invariant triangular equation;
2. for large \(r\), an entire critical ball of non-invariant,
   three-dimensional data around it is also globally regular;
3. the radius of that ball approaches
   \(\eta_{\rm KT}^{\rm per}\), rather than shrinking with the growing
   Fourier amplitude;
4. therefore a singularity-searching transverse deformation cannot be
   infinitesimal in \(BMO^{-1}_{\rm per}\).

This closes the first transverse gate for the present packet.  It does not
show that every order-one perturbation is singular or unstable.  It only
proves that perturbations below the critical small-data threshold are on the
regular side.

## 6. Next falsifiable problem

The next problem is no longer small-data stability.  It is to locate the
first transverse perturbation family \(w_{0,r}\) satisfying all three
conditions:

\[
 \begin{aligned}
 &\|w_{0,r}\|_{BMO^{-1}_{\rm per}}\not\longrightarrow0,\\
 &\text{\(w_{0,r}\) couples nontrivially through }
 (w\cdot\nabla)U_r,\\
 &\text{the resulting growth reaches a standard critical continuation
 criterion rather than only an \(L^2\) transient.}
 \end{aligned}
\tag{6.1}
\]

A useful first audit is the linearized non-normal propagator

\[
 \partial_tw-\Delta w
 +(U_r\cdot\nabla)w+(w\cdot\nabla)U_r+\nabla q=0,
 \qquad \nabla\cdot w=0,
\tag{6.2}
\]

on one carefully selected three-dimensional Fourier sideband.  The output
must be measured in a scaling-critical norm.  Growth confined to a
supercritical energy estimate will not be treated as evidence for the
Millennium problem.

## References

1. H. Koch and D. Tataru, *Well-posedness for the Navier--Stokes equations*,
   Advances in Mathematics 157 (2001), 22--35.
   <https://doi.org/10.1006/aima.2000.1937>.
2. P. Germain, N. Pavlović, and G. Staffilani, *Regularity of solutions to
   the Navier--Stokes equations evolving from small data in \(BMO^{-1}\)*,
   International Mathematics Research Notices (2007).
   <https://arxiv.org/abs/math/0609781>.
3. P. Auscher, S. Dubois, and P. Tchamitchian, *On the stability of global
   solutions to Navier--Stokes equations in the space \(BMO^{-1}\)*,
   Journal de Mathématiques Pures et Appliquées 83 (2004), 673--697.
   <https://doi.org/10.1016/j.matpur.2004.01.003>.

