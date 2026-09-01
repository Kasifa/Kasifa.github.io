# R0.73Z-B — a pressure-active exact kernel invisible to both production channels

**Frozen date:** 2026-09-01

**Status:** EXACT ANALYTIC THEOREM / CERTIFICATE PENDING

**Claim class:** smooth exact Navier--Stokes trajectory; pressure-active
production kernel; positive-covariance separation; no regularity theorem

**Domain:** \(\mathbb T^3=(\mathbb R/2\pi\mathbb Z)^3\), \(\nu>0\)

**Dependencies:** r073x_problem_freeze.md,
r073x_localized_heat_characteristic.md,
r073y_exact_shear_no_go.md, and
r073z_finiteness_obstruction_and_repair.md

R0.73Y showed that a zero-pressure orthogonal shear can make both heat-scale
production channels vanish while the positive gradient covariance is
strictly positive.  The family below closes the next pressure test.  It is an
exact Navier--Stokes trajectory with nonconstant pressure for which

\[
 \Pi_s=0,\qquad \mathscr S_s=0,
\tag{0.1}
\]

at every positive heat scale, but

\[
 Q_s=P_s(pu)-P_sp\,P_su\not\equiv0.
\tag{0.2}
\]

Thus quotienting only the zero-pressure shear class is insufficient.  A
local pressure-cutoff row remains active even when both production channels
are pointwise zero.  The positive gradient covariance and the repaired mixed
observable from R0.73Z-A detect the family.

The underlying two-dimensional cellular Euler mode is not claimed as new.
For \(A=\pm B\), up to reflections, phase shifts, and exchange of axes, it
belongs to the classical two-dimensional Taylor--Green family; see Taylor
and Green, *Proc. R. Soc. A* **158** (1937),
[doi:10.1098/rspa.1937.0036](https://doi.org/10.1098/rspa.1937.0036).
For general \(A,B\), the precise description is a two-mode,
same-Laplacian-eigenvalue steady Euler flow with viscous exponential decay:
its streamfunction is a Laplacian eigenfunction, so the vorticity is a
linear function of the streamfunction.  Each component is an orthogonal
sinusoidal, Kolmogorov-type shear.

The Gaussian-filter ingredients are also established.  Johnson,
*Phys. Rev. Lett.* **124** (2020),
[doi:10.1103/PhysRevLett.124.104501](https://doi.org/10.1103/PhysRevLett.124.104501),
gives the exact Gaussian stress scale equation, and Vreman,
*Physics of Fluids* **16** (2004),
[doi:10.1063/1.1785131](https://doi.org/10.1063/1.1785131),
classifies zero theoretical SGS dissipation for simple shear types.
A bounded search did not locate the simultaneous all-scale separation
(0.1)--(0.2) on this witness; that non-hit is not a novelty inference.  The
auditable increment here is only its placement in the exact R0.73X heat
ledger with the explicitly declared
\(Q_s=P_s(pu)-P_sp\,P_su\).

---

## 1. Finite rank-one algebra

Consider a finite superposition

\[
 u(x)=\sum_{\alpha=1}^N
 a_\alpha F_\alpha(k_\alpha\cdot x),
 \qquad a_\alpha\cdot k_\alpha=0.
\tag{1.1}
\]

Let \(F_{\alpha,s}=P_sF_\alpha\), with the scalar heat flow understood in
the phase coordinate, and define

\[
 C_{\alpha\beta,s}
 =P_s(F_\alpha F_\beta)-F_{\alpha,s}F_{\beta,s}.
\tag{1.2}
\]

Then

\[
 \tau_s
 =\sum_{\alpha,\beta}
 (a_\alpha\otimes a_\beta)C_{\alpha\beta,s},
\qquad
 \nabla P_su
 =\sum_\gamma
 (a_\gamma\otimes k_\gamma)
 \partial_{\theta_\gamma}F_{\gamma,s}.
\tag{1.3}
\]

Therefore the signed subfilter production is exactly

\[
 \boxed{
 \Pi_s
 =-\sum_{\alpha,\beta,\gamma}
 (a_\alpha\cdot a_\gamma)
 (a_\beta\cdot k_\gamma)
 C_{\alpha\beta,s}
 \partial_{\theta_\gamma}F_{\gamma,s}.}
\tag{1.4}
\]

The convection is

\[
 \boxed{
 (u\cdot\nabla)u
 =\sum_{\gamma,\beta}
 a_\gamma(a_\beta\cdot k_\gamma)
 F_\beta F_\gamma'.}
\tag{1.5}
\]

Equations (1.4)--(1.5) separate an instantaneous filter kernel from a
dynamically invariant Navier--Stokes class.

### Proposition 1.1 — rectangular zero-pressure class

Let

\[
 V=\operatorname{span}\{a_\alpha\},
 \qquad
 W=\operatorname{span}\{k_\alpha\}.
\tag{1.6}
\]

If \(V\perp W\), and every profile evolves by its corresponding
one-dimensional heat equation, then

\[
 (u\cdot\nabla)u=0,\qquad p=0,
\qquad
 \Pi_s=\mathscr S_s=Q_s=0
\tag{1.7}
\]

for every \(t,x,s>0\).

The convection and tensor production vanish coefficientwise by
\(a_\beta\cdot k_\gamma=0\).  For the centered production, all velocity
increments lie in \(V\), while their scalar coefficients depend only on the
Gaussian projection of the increment variable onto \(W\).  Orthogonality
factorizes the Gaussian integral, and the remaining first moment in \(V\)
is zero.

In three dimensions this class contains both a common velocity direction
with a two-dimensional phase space and a common phase direction with a
two-dimensional velocity space.  It is strictly larger than the one-profile
shear used in R0.73Y.

### Proposition 1.2 — exact two-profile formula

For

\[
 u=a f(k\cdot x)+b g(\ell\cdot x),
\tag{1.8}
\]

write

\[
 h=a\cdot b,\qquad c=b\cdot k,\qquad d=a\cdot\ell.
\tag{1.9}
\]

Then

\[
 \boxed{
 \tau_s:\nabla P_su
 =c f_s'\bigl(hC_{gg,s}+|a|^2C_{fg,s}\bigr)
 +d g_s'\bigl(hC_{ff,s}+|b|^2C_{fg,s}\bigr).}
\tag{1.10}
\]

Orthogonality of the wavevectors alone is not enough for zero production:
it makes \(C_{fg,s}=0\) for factorized Gaussian phases, but the terms
containing \(h\) remain unless the amplitude directions are also orthogonal.

---

## 2. Crossed cellular exact solution

Fix \(n\in\mathbb N\), an origin time \(t_*\), and amplitudes
\(A,B\in\mathbb R\).  Put

\[
 a(t)=Ae^{-\nu n^2(t-t_*)},
 \qquad
 b(t)=Be^{-\nu n^2(t-t_*)},
 \qquad t>t_*,
\tag{2.1}
\]

and define

\[
 \boxed{
 u^{A,B}(t,x)
 =a(t)\sin(nx_2)e_1+b(t)\sin(nx_1)e_2,}
\tag{2.2}
\]

\[
 \boxed{
 p^{A,B}(t,x)
 =a(t)b(t)\cos(nx_1)\cos(nx_2).}
\tag{2.3}
\]

### Theorem 2.1 — exact pressure-active production kernel

The pair (2.2)--(2.3) is a smooth mean-zero exact solution of the unforced
three-dimensional Navier--Stokes equations.  If \(AB\ne0\), its pressure is
nonconstant.  For every \(t>t_*,x\in\mathbb T^3,s>0\),

\[
 \boxed{\Pi_s[u^{A,B}](t,x)=0,}
\qquad
 \boxed{\mathscr S_s[u^{A,B}](t,x)=0.}
\tag{2.4}
\]

Its pressure covariance is nonzero:

\[
 \boxed{
 \begin{aligned}
 Q_{1,s}
 &=\frac{a(t)^2b(t)}2(r^5-r^3)
   \cos(nx_1)\sin(2nx_2),\\
 Q_{2,s}
 &=\frac{a(t)b(t)^2}2(r^5-r^3)
   \sin(2nx_1)\cos(nx_2),\\
 Q_{3,s}&=0,
 \end{aligned}}
\qquad r=e^{-n^2s}.
\tag{2.5}
\]

In particular, \(Q_s\not\equiv0\) whenever \(AB\ne0\).

#### Proof

The only nonlinear terms are

\[
 (u\cdot\nabla)u
 =na(t)b(t)
 \begin{pmatrix}
 \sin(nx_1)\cos(nx_2)\\
 \cos(nx_1)\sin(nx_2)\\
 0
 \end{pmatrix},
\tag{2.6}
\]

and direct differentiation of (2.3) gives
\(\nabla p=-(u\cdot\nabla)u\).  The remaining evolution is precisely the
heat decay in (2.1), proving the Navier--Stokes equation.

The heat-filtered velocity is

\[
 v_s=P_su
 =r a(t)\sin(nx_2)e_1+r b(t)\sin(nx_1)e_2.
\tag{2.7}
\]

The Gaussian coordinates \(x_1\) and \(x_2\) factorize, so

\[
 P_s(u_1u_2)=P_su_1\,P_su_2,
 \qquad \tau_{12,s}=\tau_{21,s}=0.
\tag{2.8}
\]

The only nonzero entries of \(\nabla v_s\) are
\(\partial_2v_{1,s}\) and \(\partial_1v_{2,s}\).  Their contraction with
\(\tau_s\) uses only the zero entries in (2.8), proving \(\Pi_s=0\).

Let the centered component increments be

\[
 \begin{aligned}
 X&=a(t)\{\sin(n(x_2-y_2))-r\sin(nx_2)\},\\
 Z&=b(t)\{\sin(n(x_1-y_1))-r\sin(nx_1)\}.
 \end{aligned}
\tag{2.9}
\]

They are independent under the periodic Gaussian and each has zero mean.
The third centered moment flux therefore has the form

\[
 K_s=\frac12\bigl(\mathbb E X^3,\mathbb E Z^3,0\bigr).
\tag{2.10}
\]

Its first component depends only on \(x_2\), and its second only on \(x_1\);
hence \(\nabla\cdot K_s=0\).  The exact R0.73W identity
\(\Pi_s=\nabla\cdot K_s+\mathscr S_s\) now gives
\(\mathscr S_s=0\).

Finally, \(p\,u_1\) has phase \((n,2n)\), so its heat multiplier is \(r^5\);
\((P_sp)(P_su_1)\) has multiplier \(r^2r=r^3\).  The same calculation with
the coordinates exchanged proves (2.5). \(\square\)

---

## 3. The local pressure-cutoff debt is genuinely active

Differentiating (2.5) gives

\[
 \nabla\cdot Q_s
 =-\frac n2(r^5-r^3)
 \left[
 a(t)^2b(t)\sin(nx_1)\sin(2nx_2)
 +a(t)b(t)^2\sin(2nx_1)\sin(nx_2)
 \right].
\tag{3.1}
\]

If \(a(t)=b(t)>0\) and

\[
 nx_1=nx_2=\frac\pi3,
\tag{3.2}
\]

then

\[
 \nabla\cdot Q_s
 ={3n\,a(t)^3\over4}(r^3-r^5)>0.
\tag{3.3}
\]

Choose a nonnegative smooth bump \(\chi\) supported in a sufficiently small
neighborhood of this point.  Then

\[
 \boxed{
 \int_{\mathbb T^3}Q_s\cdot\nabla\chi\,dx
 =-\int_{\mathbb T^3}\chi\,\nabla\cdot Q_s\,dx<0.}
\tag{3.4}
\]

Thus the pressure-cutoff row cannot be deleted after observing
\(\Pi_s=\mathscr S_s=0\).  The crossed family is invisible to both
production channels but visible to the local pressure covariance.

---

## 4. Positive covariance detects the crossed family

For (2.2), the full gradient covariance is

\[
 \boxed{
 D_s
 ={n^2\over2}(1-r^2)
 \left[
 a(t)^2\{1-r^2\cos(2nx_2)\}
 +b(t)^2\{1-r^2\cos(2nx_1)\}
 \right].}
\tag{4.1}
\]

Consequently

\[
 D_s\ge {n^2\over2}(1-r^2)^2
 \left(a(t)^2+b(t)^2\right)>0
\tag{4.2}
\]

whenever \((A,B)\ne(0,0)\).  This is consistent with the exact periodic
kernel theorem in R0.73Z-A: \(D_s(x)=0\) for one positive scale and one
point if and only if the velocity is spatially constant.

### Theorem 4.1 — fixed-geometry cubic separation

Fix \(n,\nu,z_0,R,\theta,\square\) and an admissible cylinder compactly
contained in \((t_*,\infty)\).  There are constants

\[
 0<c\le C<\infty,
\tag{4.3}
\]

depending only on that fixed geometry and on \(n,\nu\), such that

\[
 \boxed{
 c(A^2+B^2)^{3/2}
 \le
 \mathcal D_{3/2}^{\square}[u^{A,B}](z_0,R;\theta)
 \le
 C(A^2+B^2)^{3/2}.}
\tag{4.4}
\]

The upper bound follows from (4.1) and the finite measure of the cylinder.
For the lower bound, restrict the scale integral to any fixed interval
\([\alpha R^2,\beta R^2]\subset(0,\theta R^2)\), use (4.2), and use the
positive minimum of the common heat-decay factor on the compact physical-time
interval.  No constant in (4.4) is claimed uniform in frequency or geometry.

The same family has

\[
 \mathcal K_D^\square[u^{A,B}]
 =\bigl(A^2+B^2\bigr)^{3/2}
 \times \hbox{a positive bounded function of }A/\sqrt{A^2+B^2},
\tag{4.5}
\]

so compactness of the amplitude unit circle also gives fixed-geometry
two-sided cubic bounds for the repaired observable.

---

## 5. Snapshot kernels versus exact trajectories

Two warnings prevent overclassification.

First, mutually orthogonal wavevectors and mutually orthogonal amplitude
directions make the cross heat covariances vanish, so they can produce a
larger instantaneous kernel of \(\Pi_s\) and \(\mathscr S_s\).  They need
not be invariant under Navier--Stokes evolution because cross-advection may
create new solenoidal Fourier modes.

For example,

\[
 u=(\sin x_3,\sin x_1,\sin x_2)
\tag{5.1}
\]

is a genuinely three-dimensional instantaneous zero-production snapshot,
but

\[
 (u\cdot\nabla)u
 =(\sin x_2\cos x_3,\sin x_3\cos x_1,\sin x_1\cos x_2)
\tag{5.2}
\]

is not a gradient.  Pure heat decay of (5.1) is therefore not an exact
Navier--Stokes trajectory.

Second, orthogonal wavevectors without orthogonal amplitude directions do
not even guarantee an instantaneous kernel.  The exact contraction (1.10)
retains the diagonal covariance terms proportional to \(h=a\cdot b\).

The genuinely three-dimensional, pressure-active, all-time exact
production-invisible family remains open.

---

## 6. Closed and open rows after R0.73Z-B

### Closed analytically

1. The rectangular condition \(V\perp W\) gives a multi-profile exact
   zero-pressure production kernel.
2. The crossed cellular family (2.2)--(2.3) is exact, pressure-active, and
   satisfies \(\Pi_s=\mathscr S_s=0\) for all positive heat scales.
3. Its pressure covariance is explicit and activates a compactly supported
   local pressure-cutoff test.
4. Both \(\mathcal D_{3/2}\) and \(\mathcal K_D\) detect it with
   fixed-geometry cubic amplitude bounds.
5. A genuinely three-dimensional cyclic snapshot shows that filter-kernel
   algebra alone does not imply Navier--Stokes invariance.

### Still open

1. a full classification of smooth exact all-time production-invisible
   trajectories;
2. a genuinely three-dimensional pressure-active exact family;
3. a positive estimate paying the local pressure-cutoff debt from
   \(\mathcal K_D\), local energy, and a minimal exterior tail;
4. scale-uniform first-jet quotient coercivity;
5. suitable-weak compactness and any epsilon-regularity implication.

**NOT CLAY.**
