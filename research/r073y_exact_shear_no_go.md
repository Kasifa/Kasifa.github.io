# R0.73Y-A — exact shear-class no-go theorem for production-only heat payments

**Frozen date:** 2026-09-01

**Status:** `EXACT ANALYTIC THEOREM + DETERMINISTIC CERTIFICATE`

**Claim class:** smooth exact Navier--Stokes trajectory; universal no-go for
production-only coercivity; no epsilon-regularity theorem

**Domain:** the normalized torus
\(\mathbb T^3=(\mathbb R/2\pi\mathbb Z)^3\), viscosity \(\nu>0\)

**Dependencies:** the definitions in `r073x_problem_freeze.md`, the exact
localized ledgers in `r073x_localized_heat_characteristic.md`, and the
exterior functional in `r073x_exterior_tail_freeze.md`

This note closes one R0.73X bridge in the negative.  A signed heat-scale
production, even when it vanishes pointwise at every positive heat scale,
cannot by itself force

\[
 \mathcal E^\square(z_0,4R)^{3/2}
 +\mathcal A_{\rm ext}^\square(z_0,R;\theta)
\]

to be small.  The obstruction is an exact, mean-zero, arbitrarily large,
globally smooth Navier--Stokes shear.  The theorem does **not** refute a
regularity criterion: every member of the family is already smooth.  It
refutes only the missing coercive bridge from production-only smallness to
small positive size.

### Literature boundary

The shear geometry and the vanishing of its exact subgrid production are not
claimed as new.  Plane-parallel exact Navier--Stokes reductions are classical;
on \(\mathbb T^3\), Jeong--Yoneda, *Proc. Amer. Math. Soc.* **150**
(2022), [doi:10.1090/proc/15754](https://doi.org/10.1090/proc/15754),
explicitly use a shear component governed by the one-dimensional heat
equation.  Mazzucato--Taylor, *Analysis & PDE* **1** (2008), 35--93,
[doi:10.2140/apde.2008.1.35](https://doi.org/10.2140/apde.2008.1.35), give
the broader plane-parallel lineage.  More directly, Vreman, *Physics of
Fluids* **16** (2004), 3670--3681,
[doi:10.1063/1.1785131](https://doi.org/10.1063/1.1785131), proves that the
exact subgrid dissipation vanishes for the simple laminar-shear derivative
classes under commuting filters.  Gaussian filtering as a continuous
diffusion-scale coordinate and the exact stress evolution are also established
in Johnson, *Physical Review Letters* **124** (2020), 104501,
[doi:10.1103/PhysRevLett.124.104501](https://doi.org/10.1103/PhysRevLett.124.104501).
Germano, *J. Fluid Mech.* **238** (1992), 325--336,
[doi:10.1017/S0022112092001733](https://doi.org/10.1017/S0022112092001733),
and Eyink--Aluie, *Physics of Fluids* **21** (2009), 115107,
[doi:10.1063/1.3266883](https://doi.org/10.1063/1.3266883), already separate
signed production from nonnegative gradient covariance in exact
coarse-grained energy ledgers.

The auditable increment here is narrower: the classical shear kernel is placed
on an exact periodic Navier--Stokes trajectory; the heat covariance is shown to
be pointwise strictly positive while both tensor and centered-increment
productions vanish; and this separation is tied to the precise R0.73X positive
size to disprove a production-only amplitude-independent modulus.  The bounded
collision search is recorded separately and is not a novelty or priority
claim.

---

## 1. Exact family and theorem

Fix \(n\in\mathbb N\) with \(n\ge1\), \(A\in\mathbb R\), and write

\[
 b_A(t)=A e^{-\nu n^2t},\qquad \xi=nx_2.
\tag{1.1}
\]

Set

\[
 \boxed{
 u^A(t,x)=b_A(t)\sin\xi\,e_1,\qquad p^A(t,x)=0.}
\tag{1.2}
\]

The time origin in (1.1) is immaterial; replacing \(t\) by \(t-t_*\)
gives the same conclusions.  The solution is smooth on every finite time
interval and has zero spatial mean.

### Theorem 1.1 — exact production kernel with positive size

For the family (1.2), every \(t\), \(x\), and \(s>0\) satisfy, pointwise,

\[
 \Pi_s[u^A](t,x)=0,
 \qquad
 \mathscr S_s[u^A](t,x)=0,
 \qquad
 Q_s[u^A,p^A](t,x)=0.
\tag{1.3}
\]

The corresponding suitable-weak local-energy defect satisfies
\(\mu^A\equiv0\) as a measure.

If \(A\ne0\), then the positive gradient covariance is strictly positive:

\[
 \boxed{
 D_{ii,s}[u^A](t,x)
 ={b_A(t)^2n^2\over2}
   (1-e^{-2n^2s})
   (1-e^{-2n^2s}\cos(2nx_2))>0.}
\tag{1.4}
\]

Fix either cylinder clock
\(\square\in\{\mathrm{std},\nu\}\), an admissible
\(z_0,R,\theta\) from `r073x_exterior_tail_freeze.md`, and a time interval
compactly contained in the smooth lifespan.  Then

\[
 \boxed{
 \mathcal E^\square[u^A](z_0,4R)^{3/2}
 +\mathcal A_{\rm ext}^\square[u^A,p^A](z_0,R;\theta)
 =|A|^3 C_{n,\nu,z_0,R,\theta,\square},}
\tag{1.5}
\]

where

\[
 C_{n,\nu,z_0,R,\theta,\square}>0.
\tag{1.6}
\]

Consequently, for fixed admissible geometry there is no
amplitude-independent universal bound of the left side of (1.5) by a
zero-preserving functional built only from signed or unsigned \(\Pi_s\)- or
\(\mathscr S_s\)-production.  The statement remains true after inserting
arbitrary scalar cutoffs or sampling arbitrary heat-scale paths, in the
precise production-only sense of Sections 8--9.

### Theorem 1.2 — structural shear-class extension

Let \(k\in\mathbb Z^3\setminus\{0\}\),
\(a\in\mathbb R^3\setminus\{0\}\), and \(a\cdot k=0\).  Let
\(f_0\in C^\infty(\mathbb T)\) be nonconstant with zero mean, put

\[
 H_\sigma=e^{\sigma\partial_\vartheta^2},\qquad
 F(t,\vartheta)=H_{\nu|k|^2t}f_0(\vartheta),
\tag{1.7}
\]

and define, for \(t>0\),

\[
 u^A(t,x)=A\,a\,F(t,k\cdot x),\qquad p^A(t,x)=0.
\tag{1.8}
\]

Then (1.8) is a smooth mean-zero exact Navier--Stokes solution.  For every
\(t>0\), \(x\in\mathbb T^3\), and \(s>0\), the first three quantities below
vanish pointwise:

\[
 \Pi_s=\mathscr S_s=Q_s=0.
\tag{1.9}
\]

The local-energy defect satisfies \(\mu^A\equiv0\) as a measure.

If \(A\ne0\), its positive gradient covariance is

\[
 \boxed{
 D_{ii,s}=A^2|a|^2|k|^2
 \left\{H_{s|k|^2}\!\left[(\partial_\vartheta F)^2\right]
 -\left(H_{s|k|^2}\partial_\vartheta F\right)^2\right\}>0.}
\tag{1.10}
\]

For every fixed admissible R0.73X geometry whose time interval is compactly
contained in \((0,\infty)\), the positive size in (1.5) again equals
\(|A|^3C\), where

\[
 C=C_{a,k,f_0,\nu,z_0,R,\theta,\square}>0.
\tag{1.11}
\]

Hence the no-go conclusion holds for the whole class (1.8), while the single
Fourier mode (1.2) remains the explicit deterministic certificate witness.
Section 10 gives the proof.

---

## 2. Verification of the Navier--Stokes equation

The only nonzero component of \(u^A\) is \(u_1^A\), and it depends only on
\(x_2\).  Therefore

\[
 \nabla\cdot u^A=\partial_1u_1^A=0,
 \qquad
 (u^A\cdot\nabla)u^A=u_1^A\partial_1u^A=0.
\tag{2.1}
\]

Moreover,

\[
 \partial_tu^A=-\nu n^2u^A,
 \qquad
 \Delta u^A=-n^2u^A.
\tag{2.2}
\]

Hence

\[
 \partial_tu^A+(u^A\cdot\nabla)u^A+\nabla p^A
 -\nu\Delta u^A=0.
\tag{2.3}
\]

Thus (1.2) is an exact Navier--Stokes solution, not a static test field,
linearization, numerical trajectory, or approximate ansatz.

---

## 3. Exact heat filter and stress

Put

\[
 \rho=e^{-n^2s}\in(0,1).
\tag{3.1}
\]

Since \(\sin(nx_2)\) is a Laplace eigenfunction,

\[
 \boxed{v_s=P_su^A=b_A(t)\rho\sin\xi\,e_1.}
\tag{3.2}
\]

Only the \((1,1)\) component of \(u^A\otimes u^A\) is nonzero.  Using
\(\sin^2\xi=(1-\cos2\xi)/2\),

\[
 P_s(u^A\otimes u^A)_{11}
 ={b_A(t)^2\over2}\left(1-\rho^4\cos2\xi\right),
\tag{3.3}
\]

whereas

\[
 (v_s\otimes v_s)_{11}
 ={b_A(t)^2\rho^2\over2}\left(1-\cos2\xi\right).
\tag{3.4}
\]

Therefore \(\tau_s\) has only one nonzero component,

\[
 \boxed{
 \tau_{11,s}
 ={b_A(t)^2\over2}
 \left[(1-\rho^2)+(\rho^2-\rho^4)\cos2\xi\right],}
\tag{3.5}
\]

and

\[
 k_s={1\over2}\operatorname{tr}\tau_s
 ={b_A(t)^2\over4}
 \left[(1-\rho^2)+(\rho^2-\rho^4)\cos2\xi\right].
\tag{3.6}
\]

As a consistency check, \(\tau_{11,s}\ge0\); its minimum is
\(b_A(t)^2(1-\rho^2)^2/2\).

---

## 4. Exact vanishing of \(\Pi_s\) and \(\mathscr S_s\)

With the convention \((\nabla v_s)_{ij}=\partial_jv_{s,i}\), the only
nonzero entry of \(\nabla v_s\) is

\[
 (\nabla v_s)_{12}=b_A(t)n\rho\cos\xi.
\tag{4.1}
\]

The stress has only the \((1,1)\) entry.  The two tensors have no common
nonzero index pair, so

\[
 \boxed{\Pi_s=-\tau_s:\nabla v_s=0.}
\tag{4.2}
\]

For the centered increment, lift the periodic field to \(\mathbb R^3\).
Then

\[
 a_s(x,y)=u^A(x-y)-v_s(x)=\alpha_s(t,x_2,y_2)e_1,
\tag{4.3}
\]

where

\[
 \alpha_s=b_A(t)
 [\sin(n(x_2-y_2))-\rho\sin(nx_2)].
\tag{4.4}
\]

Thus \(y\cdot a_s=y_1\alpha_s\) and
\(|a_s|^2=\alpha_s^2\).  The factor \(\alpha_s^3\) is independent of
\(y_1\), while the Euclidean Gaussian is even in \(y_1\).  Fubini gives

\[
 \begin{aligned}
 \mathscr S_s
 &= {1\over4s}\int_{\mathbb R^3}
    y_1\alpha_s^3g_s(y)\,dy\\
 &= {1\over4s}
    \left(\int_{\mathbb R}y_1g_s^{(1)}(y_1)\,dy_1\right)
    \left(\int_{\mathbb R^2}\alpha_s^3
                  g_s^{(2)}(y_2,y_3)\,dy_2dy_3\right)=0.
 \end{aligned}
\tag{4.5}
\]

The same proof on the torus uses
\(-\frac12\int\partial_{y_1}g_s^{\rm per}\,\alpha_s^3\,dy=0\).
There is no appeal to cancellation across \(x\), \(t\), or \(s\): both
(4.2) and (4.5) are pointwise identities.

The centered flux \(K_s\) has only an \(e_1\) component and depends only on
\(x_2\).  Hence \(\nabla\cdot K_s=\partial_1K_{1,s}=0\), consistently with
\(\Pi_s=\nabla\cdot K_s+\mathscr S_s=0\).  In particular, for every smooth
periodic spatial cutoff \(\eta\),

\[
 -\int_{\mathbb T^3}\nabla\eta\cdot K_s\,dx=0.
\tag{4.6}
\]

---

## 5. Exact positive gradient covariance

The unfiltered and filtered gradient squares are

\[
 |\nabla u^A|^2
 ={b_A(t)^2n^2\over2}(1+\cos2\xi),
\tag{5.1}
\]

\[
 |\nabla v_s|^2
 ={b_A(t)^2n^2\rho^2\over2}(1+\cos2\xi).
\tag{5.2}
\]

Filtering (5.1) multiplies its second harmonic by \(\rho^4\), so

\[
 P_s(|\nabla u^A|^2)
 ={b_A(t)^2n^2\over2}(1+\rho^4\cos2\xi).
\tag{5.3}
\]

Subtracting (5.2) from (5.3) yields exactly (1.4):

\[
 D_{ii,s}
 ={b_A(t)^2n^2\over2}(1-\rho^2)(1-\rho^2\cos2\xi).
\tag{5.4}
\]

For \(A\ne0\) and \(s>0\),

\[
 D_{ii,s}
 \ge {b_A(t)^2n^2\over2}(1-\rho^2)^2>0.
\tag{5.5}
\]

This is the decisive sign separation: nonlinear production vanishes while
the positive heat covariance does not.

---

## 6. Pressure covariance, defect, and the cancellation debt

Because \(p^A=0\),

\[
 Q_s=P_s(p^Au^A)-P_sp^A\,P_su^A=0.
\tag{6.1}
\]

The solution is smooth and satisfies the pointwise local energy equality.
Accordingly its suitable-weak local energy-defect measure is

\[
 \mu^A=0,
 \qquad P_s\mu^A=0.
\tag{6.2}
\]

Equations (4.5), (5.5), and (6.2) do not contradict the trace ledger.  At
fixed \(s>0\), spatial averaging of (3.6) and (5.4) gives

\[
 \int_{\mathbb T^3}k_s\,dx
 ={(2\pi)^3b_A(t)^2\over4}(1-\rho^2),
\tag{6.3}
\]

\[
 \int_{\mathbb T^3}D_{ii,s}\,dx
 ={(2\pi)^3b_A(t)^2n^2\over2}(1-\rho^2).
\tag{6.4}
\]

Since \(\partial_tb_A^2=-2\nu n^2b_A^2\),

\[
 {d\over dt}\int_{\mathbb T^3}k_s\,dx
 +\nu\int_{\mathbb T^3}D_{ii,s}\,dx=0.
\tag{6.5}
\]

Thus, if \(A\ne0\), then on every nondegenerate interval \([a,b]\),

\[
 \nu\int_a^b\!\int_{\mathbb T^3}D_{ii,s}\,dx\,dt
 =\int_{\mathbb T^3}k_s(a)\,dx
  -\int_{\mathbb T^3}k_s(b)\,dx>0,
\tag{6.6}
\]

while \(\int_a^b\int\mathscr S_s=0\).  The positive covariance is paid by
the decrease of subfilter energy.  After localization, the remaining
nonproduction rows--including endpoint, time-cutoff, spatial-cutoff, and
viscous-boundary rows as applicable--provide the corresponding exact
bookkeeping.  Their **sum** is fixed by the ledger, but their absolute values
are not controlled by the vanishing production.

This identifies the missing object in a repaired theorem: an endpoint and
cutoff cancellation debt, or a separate positive covariance hypothesis,
cannot be omitted.

---

## 7. Exact \(|A|^3\) homogeneity and strict positivity

Fix the geometry \((n,\nu,z_0,R,\theta,\square)\).  Since
\(u^A=A u^1\),

\[
 \mathcal E^\square[u^A](z_0,4R)
 =A^2\mathcal E^\square[u^1](z_0,4R).
\tag{7.1}
\]

Every open ball contains a positive-measure subset on which
\(\sin(nx_2)\ne0\).  Hence, for \(A\ne0\),

\[
 \mathcal E^\square[u^A](z_0,4R)>0.
\tag{7.2}
\]

For \(A\ne0\), the velocity row of the Gaussian exterior payment obeys

\[
 \mathcal G_u^\square[u^A]
 =|A|^3\mathcal G_u^\square[u^1]>0.
\tag{7.3}
\]

Strict positivity follows because every lifted annulus has positive measure
and the zero set of the shear is a countable union of planes, hence has
three-dimensional measure zero.

The pressure gauge used in the exterior functional preserves the same
degree.  With the exterior note's fixed cutoff \(\zeta_R\),

\[
 p_R^{\rm loc,A}=A^2p_R^{\rm loc,1},\qquad
 h_R^A=A^2h_R^1,\qquad
 c_R^A=A^2c_R^1.
\tag{7.4}
\]

Here the geometry, \(\zeta_R\), and the rule selecting \(c_R\) are fixed
independently of \(A\), exactly as in the frozen exterior functional.

Therefore

\[
 \mathcal G_p^\square[u^A,p^A]
 =|A|^3\mathcal G_p^\square[u^1,p^1]\ge0.
\tag{7.5}
\]

Likewise, for \(A\ne0\),

\[
 \Lambda_R^A(t)=A^2\Lambda_R^1(t),
 \qquad
 \mathcal H_u^\square[u^A]
 =|A|^3\mathcal H_u^\square[u^1]>0.
\tag{7.6}
\]

Combining (7.1), (7.3), (7.5), and (7.6) proves

\[
 \begin{aligned}
 &\mathcal E^\square[u^A](z_0,4R)^{3/2}
 +\mathcal A_{\rm ext}^\square[u^A,p^A](z_0,R;\theta)\\
 &\quad=|A|^3\left[
 \mathcal E^\square[u^1](z_0,4R)^{3/2}
 +\mathcal A_{\rm ext}^\square[u^1,p^1](z_0,R;\theta)
 \right],
 \end{aligned}
\tag{7.7}
\]

and the bracket is strictly positive.  This is (1.5)--(1.6).

---

## 8. Exact cutoff and characteristic quantifiers

The no-go statement covers more than one special cutoff or descending
path, but it must be phrased at the integrand level.

Let \(I\) be any time interval, let
\(\sigma:I\to(0,\infty)\) be any measurable heat-scale path, and let
\(W(t,x,s)\) be any scalar measurable weight for which the following
integrals exist.  Pointwise vanishing gives

\[
 \int_I\!\int_{\mathbb T^3}
 W(t,x,\sigma(t))\Pi_{\sigma(t)}(t,x)\,dx\,dt=0,
\tag{8.1}
\]

\[
 \int_I\!\int_{\mathbb T^3}
 W(t,x,\sigma(t))\mathscr S_{\sigma(t)}(t,x)\,dx\,dt=0.
\tag{8.2}
\]

The result therefore includes:

1. arbitrary smooth compactly supported or periodic cutoffs, with either
   sign and with or without \(s\)-dependence;
2. every descending heat characteristic \(s'(t)=-\nu\) that remains
   positive;
3. arbitrary non-characteristic positive scale paths, for the direct
   production integral only;
4. every scale weight, including the unweighted and \(s^{-1/2}\)-weighted
   production tents, whenever the expression is defined;
5. signed and absolute production quantities, because the integrands
   themselves vanish.

For this smooth family, \(\Pi_s\) and \(\mathscr S_s\) have the continuous
zero extension at \(s=0\), so (8.1)--(8.2) remain true if
\(\sigma(t)=0\) on part of the interval and that extension is used.  This
does not license an \(s=0\) endpoint for a general suitable weak solution.

The following stronger statements are **not** included:

- an arbitrary path is not automatically a heat characteristic in the
  heat-plane ledger; if \(\sigma'\ne-\nu\), the chain rule has an extra
  scale-derivative term;
- the endpoint, time-cutoff, and viscous-boundary rows are not forced to
  vanish merely because the production vanishes; for this particular shear
  the pressure covariance row is zero and some transport rows also vanish
  by the one-directional geometry;
- the sum of the **absolute values** of those ledger debts is not a
  production-only payment and is not refuted here;
- a criterion containing \(D_{ii,s}\), \(P_s\mu\), a positive Carleson
  tent, a \(BMO^{-1}\) norm, or an explicit cancellation debt is outside
  this theorem's no-go class.

---

## 9. Quantitative no-go corollary

Fix the admissible geometry and define any nonnegative, zero-preserving
production-only functional \(\mathfrak P_A\): it is assembled from
\(\Pi_s\) and \(\mathscr S_s\) by scalar weights, cutoffs, absolute values,
finite sums, or integrals over \((t,x,s)\), and it returns zero when all of
those production inputs vanish.  For (1.2),

\[
 \mathfrak P_A=0\qquad\hbox{for every }A\in\mathbb R.
\tag{9.1}
\]

By (1.5), for every \(M>0\) one may choose

\[
 |A|>\left({M\over C_{n,\nu,z_0,R,\theta,\square}}\right)^{1/3}
\tag{9.2}
\]

and obtain

\[
 \mathfrak P_A=0,
 \qquad
 \mathcal E^\square[u^A](z_0,4R)^{3/2}
 +\mathcal A_{\rm ext}^\square[u^A,p^A](z_0,R;\theta)>M.
\tag{9.3}
\]

Hence there is no amplitude-independent modulus
\(\omega\) with finite \(\omega(0)\), and in particular no modulus with
\(\omega(\delta)\to0\) as \(\delta\downarrow0\), such that universally

\[
 \mathcal E^{3/2}+\mathcal A_{\rm ext}
 \le\omega(\mathfrak P).
\tag{9.4}
\]

The corrected R0.73Y direction must therefore retain positive covariance
or exact cancellation debt.  Pressure projection can organize the pressure
rows, but pressure is identically zero in this counterexample and hence
cannot repair production-only coercivity by itself.

---

## 10. Structural shear-class proof

Write \(\vartheta=k\cdot x\).  From \(a\cdot k=0\),

\[
 \nabla\cdot u^A=A(a\cdot k)\partial_\vartheta F=0,
 \qquad
 (u^A\cdot\nabla)u^A
 =A^2aF(a\cdot k)\partial_\vartheta F=0.
\tag{10.1}
\]

Equation (1.7) gives

\[
 \partial_tu^A=\nu A|k|^2a\,\partial_\vartheta^2F
 =\nu\Delta u^A,
\tag{10.2}
\]

so (1.8) solves Navier--Stokes with zero pressure.  The spatial heat flow
reduces to the one-dimensional heat flow:

\[
 P_su^A=Aa\,H_{s|k|^2}F.
\tag{10.3}
\]

The map \(x\mapsto k\cdot x\pmod{2\pi}\) pushes Haar measure on
\(\mathbb T^3\) to Haar measure on \(\mathbb T\).  Thus the zero mean of
\(f_0\), which is preserved by \(H_\sigma\), gives the asserted spatial zero
mean of \(u^A\).

Consequently

\[
 \tau_s=A^2(a\otimes a)
 \left[H_{s|k|^2}(F^2)-(H_{s|k|^2}F)^2\right],
 \qquad
 \nabla v_s=A(a\otimes k)\partial_\vartheta H_{s|k|^2}F.
\tag{10.4}
\]

The contraction vanishes because

\[
 (a\otimes a):(a\otimes k)=|a|^2(a\cdot k)=0,
\tag{10.5}
\]

which proves \(\Pi_s=0\).  The centered increment has the form

\[
 a_s(x,y)=Aa\,\alpha_s(k\cdot y;k\cdot x).
\tag{10.6}
\]

Using the exact Euclidean-lift Gaussian representation, choose orthonormal
coordinates with one axis parallel to \(a\) and another to \(k\).  The scalar
\(\alpha_s\) is independent of the \(a\)-coordinate of \(y\).  The integrand
defining \(\mathscr S_s\) is therefore odd in that coordinate against the
isotropic Gaussian, proving \(\mathscr S_s=0\).
The pressure covariance vanishes because \(p=0\), and smooth local energy
equality gives \(\mu^A\equiv0\).

Finally,

\[
 |\nabla u^A|^2=A^2|a|^2|k|^2(\partial_\vartheta F)^2,
\tag{10.7}
\]

and subtracting \(|\nabla P_su^A|^2\) gives (1.10).  The bracket in (1.10)
is the variance of \(\partial_\vartheta F\) under the strictly positive
periodic heat kernel.  Equality could hold only if
\(\partial_\vartheta F\) were constant almost everywhere.  Periodicity
would force that constant to be zero and \(F\) to be constant, contrary to
the injectivity of the finite-time heat semigroup on the nonzero Fourier
modes of the nonconstant \(f_0\).  Thus the bracket is strictly positive at
every \((t,x,s)\) with \(t,s>0\).

For positive time, \(F(t,\cdot)\) is real analytic and nonconstant, so its
zero set has one-dimensional measure zero; its pullback under
\(x\mapsto k\cdot x\pmod{2\pi}\) has three-dimensional measure zero.  The
homogeneity and periodic-lift arguments of Section 7 therefore apply verbatim:
every fixed R0.73X positive size is \(|A|^3C\) with \(C>0\).  This completes
Theorem 1.2.

---

## 11. Analytic proof versus certificate

The proof above is exact.  The companion script
`scripts/r073y_exact_shear_certificate.py` performs an independent
dependency-free audit of:

- the Fourier heat multipliers and stress formula in the exact polynomial
  ring \(\mathbb Q[\rho]\) with exact rational-complex Fourier
  coefficients;
- the NSE, \(\Pi_s\), centered-parity, \(D_{ii,s}\), and global trace-ledger
  identities;
- a declared amplitude-degree ledger for every row in (7.7), checked for
  internal consistency but not independently re-derived by symbolic
  exponent propagation;
- direct Gaussian-convolution values on a deterministic numerical grid.

The numerical rows are cross-checks only.  They are not used to prove
pointwise vanishing, strict positivity, the universal quantifiers, or the
no-go corollary.

---

## 12. Claim ledger

\[
\begin{array}{ll}
\texttt{exactShearSolvesNSE}
 &=\texttt{PROVED\_ANALYTICALLY},\\
\texttt{generalOrthogonalShearClass}
 &=\texttt{PROVED\_ANALYTICALLY},\\
\texttt{meanZeroAndGloballySmooth}
 &=\texttt{PROVED\_ANALYTICALLY},\\
\texttt{heatFilteredVelocityAndStress}
 &=\texttt{PROVED\_ANALYTICALLY},\\
\texttt{PiPointwiseZero}
 &=\texttt{PROVED\_ANALYTICALLY},\\
\texttt{centeredProductionPointwiseZero}
 &=\texttt{PROVED\_ANALYTICALLY},\\
\texttt{pressureCovarianceZero}
 &=\texttt{PROVED\_ANALYTICALLY},\\
\texttt{localEnergyDefectZero}
 &=\texttt{PROVED\_ANALYTICALLY},\\
\texttt{gradientCovarianceFormulaAndStrictPositivity}
 &=\texttt{PROVED\_ANALYTICALLY},\\
\texttt{arbitraryCutoffProductionVanishing}
 &=\texttt{PROVED\_ANALYTICALLY},\\
\texttt{arbitraryPositiveScalePathProductionVanishing}
 &=\texttt{PROVED\_ANALYTICALLY},\\
\texttt{energyAndExteriorTailCubicHomogeneity}
 &=\texttt{PROVED\_ANALYTICALLY},\\
\texttt{productionOnlyCoerciveBridge}
 &=\texttt{FALSE\_BY\_EXACT\_NSE\_FAMILY},\\
\texttt{ledgerAbsoluteDebtAlsoZero}
 &=\texttt{FALSE\_NOT\_CLAIMED},\\
\texttt{epsilonRegularityRefuted}
 &=\texttt{FALSE\_NOT\_CLAIMED},\\
\texttt{arbitraryThreeDimensionalGlobalRegularity}
 &=\texttt{OPEN},\\
\texttt{clayConclusion}
 &=\texttt{OPEN}.
\end{array}
\tag{12.1}
\]

No DNS, time stepping, singular solution, blow-up exclusion, or arbitrary
three-dimensional regularity theorem is contained here.

**NOT CLAY.**
