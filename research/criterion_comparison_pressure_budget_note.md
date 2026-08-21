# R0.69M — Criterion comparison for the three-zone pressure budget

## 1. Decision

R0.69L proved, for a smooth divergence-free velocity field, the normalized
pressure estimate

\[
 r^3|\mathcal P_r|
 \leq C\min\{b_r,\;\sigma_r(N_r+B_\infty)\},
 \qquad
 B_\infty=\sum_{m\geq2}2^{-5m}e_m.                 \tag{1.1}
\]

R0.69M compares the three quantities on the right with the regularity class
of suitable weak solutions and with established scale-invariant criteria.
The result is deliberately negative about the present closure:

> **Route decision.** The weighted exterior term \(B_\infty\) is controlled
> by a critical kinetic Morrey envelope and is strictly weaker than that
> envelope. In contrast, neither \(N_r\) nor the absolute annular quantity
> \(b_r\) is available at the suitable-weak-solution energy level. Small
> velocity or local-energy quantities do not control them by a
> pointwise-in-time functional inequality. Therefore (1.1), as currently
> formulated, is not a new epsilon-regularity criterion.

This conclusion preserves a useful lemma about the far pressure tail, but it
rejects the present near-field norm as a route to a stronger regularity
theorem.  The next mathematical task is to lower the regularity of the near
pairing, not to tune the separation radius again.

## 2. Reference regularity levels

A suitable weak solution on a parabolic cylinder has the energy-class
regularity

\[
 u\in L_t^\infty L_x^2\cap L_t^2H_x^1,
 \qquad p\in L_{t,x}^{3/2},                                      \tag{2.1}
\]

and satisfies the local energy inequality.  The following established
results provide the comparison baseline.

1. The Caffarelli--Kohn--Nirenberg small-dissipation condition, in the form
   recalled by Gustafson--Kang--Tsai, uses
   \(r^{-1}\int_{Q_r}|\nabla u|^2\) at vanishing scales.
2. Gustafson--Kang--Tsai give scale-invariant local criteria for velocity,
   velocity gradient, vorticity, and vorticity gradient.  Their gradient
   criterion includes \((p,q)=(2,2)\), hence the CKN case, and the critical
   mixed-norm line \(3/p+2/q=2\).
3. Escauriaza--Seregin--Sverak prove regularity for the endpoint
   \(u\in L_t^\infty L_x^3\).
4. Seregin formulates a family of sufficient conditions in critical Morrey
   spaces that contains the CKN condition.
5. Local pressure projection removes the nonlocal pressure from the local
   energy inequality; Jiu--Wang--Zhou obtain a velocity-only epsilon criterion
   with \(\iint_{Q(1)}|u|^{20/7}\leq\varepsilon\).

Primary sources are listed in Section 8.  These theorems are not reproved
here; only their stated function spaces and scale exponents are used for the
comparison.

## 3. The far term is controlled by critical kinetic Morrey energy

Assume \(0\leq\chi_m\leq1\) and

\[
 \operatorname{supp}\chi_m\subset B_{2^{m+1}r},\qquad
 E_m=\int\chi_m|u|^2,\qquad e_m=E_m/r.                            \tag{3.1}
\]

Define the centered exterior kinetic Morrey envelope

\[
 \mathfrak M_2(r)
 :=\sup_{\rho\geq4r}\frac1\rho\int_{B_\rho}|u(x)|^2\,dx.          \tag{3.2}
\]

This quantity is invariant under Navier--Stokes scaling.  Since

\[
 E_m\leq\int_{B_{2^{m+1}r}}|u|^2
 \leq2^{m+1}r\,\mathfrak M_2(r),                                 \tag{3.3}
\]

the sharp shell weight from R0.69K gives

\[
 \boxed{
 B_\infty(r)
 \leq2\sum_{m\geq2}2^{-4m}\mathfrak M_2(r)
 =\frac1{120}\mathfrak M_2(r).}                                  \tag{3.4}
\]

There is no converse estimate with a universal constant.  Put a
divergence-free packet with kinetic energy \(E\) in a single shell of index
\(k\).  Then

\[
 B_\infty=2^{-5k}\frac Er,
 \qquad
 \mathfrak M_2(r)\geq\frac{E}{2^{k+1}r},
 \qquad
 \frac{\mathfrak M_2(r)}{B_\infty}\geq2^{4k-1}.                  \tag{3.5}
\]

Thus \(B_\infty\) is a genuinely weaker, origin-centered exterior quantity:
remote kinetic energy is discounted by four additional dyadic powers beyond
the critical Morrey normalization.  This is the positive reusable result of
R0.69M.

## 4. The near norm is above the suitable weak level

Recall

\[
 q_0=\partial_i\partial_j(\eta_0u_i u_j),
 \qquad N_r=r^{5/2}\|q_0\|_2.                                   \tag{4.1}
\]

Using \(\partial_i u_i=0\), the source expands exactly as

\[
 \begin{aligned}
 q_0={}&\eta_0\,\partial_i u_j\,\partial_j u_i
 +(\partial_i\eta_0)u_j\partial_j u_i
 +(\partial_j\eta_0)u_i\partial_i u_j\\
 &+(\partial_{ij}\eta_0)u_i u_j.                                \tag{4.2}
 \end{aligned}
\]

The leading term is quadratic in \(\nabla u\).  Energy regularity gives it
only in \(L^1_x\), while (4.1) asks for \(L^2_x\), roughly
\(\nabla u\in L^4_x\).  Therefore \(N_r\) is not defined as a finite
quantity for a generic suitable weak solution.  The Riesz-transform estimate
used in R0.69L is correct for smooth fields, but it begins above the class in
which epsilon-regularity is needed.

The mismatch is not repaired by small velocity energy.  Let
\(\chi\in C_c^\infty(B_2)\) equal one on a fixed box
\(K\subset B_1\setminus B_{1/2}\), and set

\[
 \psi_N(x)=a_NN^{-1}\chi(x)\sin(Nx_1)\sin(Nx_2),
 \qquad
 u_N=(\partial_2\psi_N,-\partial_1\psi_N,0).                     \tag{4.3}
\]

Then \(u_N\) is smooth, compactly supported, and divergence free.  On \(K\),

\[
 q_N=2a_N^2N^2
 \bigl(\cos^2(Nx_1)\cos^2(Nx_2)
       -\sin^2(Nx_1)\sin^2(Nx_2)\bigr).                         \tag{4.4}
\]

Consequently, for a fixed admissible \(\eta_0\),

\[
 \|u_N\|_3=O(a_N),\qquad
 \mathfrak M_2(1)=O(a_N^2),\qquad
 N_1\geq c a_N^2N^2.                                            \tag{4.5}
\]

Choosing \(a_N=N^{-1/2}\) makes the velocity and kinetic Morrey quantities
tend to zero while \(N_1\to\infty\).  This is a functional counterexample at
one time, not a singular Navier--Stokes solution and not a counterexample to
a parabolic epsilon-regularity theorem.  It proves that no purely spatial
inequality can bound \(N_r\) by the velocity-only quantities above.

## 5. The absolute annular representation has the same mismatch

R0.69L also used

\[
 b_r=r^2\int_{B_r\setminus B_{r/2}}|u|\,|q|,dx
 +r\int_{B_r\setminus B_{r/2}}|u|\,|\nabla p|\,dx.                \tag{5.1}
\]

At the energy level, \(q=\partial_i u_j\partial_j u_i\in L^1_x\) at
almost every time and \(u\in L^6_x\).  These facts do not make
\(|u||q|\) integrable.  Similarly, the distributional pressure regularity of
a suitable weak solution does not justify the pointwise Hessian pairing from
which (5.1) was derived.  The usual local energy flux
\(\int p\,u\cdot\nabla\phi\) is well defined in the standard spaces; the
twice-integrated absolute-value form (5.1) is strictly more demanding.

The same family (4.3) makes this visible.  On the fixed annular box,

\[
 \int_K|u_N|\,|q_N|\,dx\geq c a_N^3N^2.                          \tag{5.2}
\]

For \(a_N=N^{-1/2}\), the right-hand side grows like \(N^{1/2}\), even
though \(\|u_N\|_3\to0\).  Hence the absolute annular bound is not controlled
by velocity smallness through a time-slice inequality either.

## 6. The first lower-exponent repair is still too strong

Formula (4.2) suggests replacing the \(L^2\)--\(L^2\) pairing by
\(L^3\)--\(L^{3/2}\).  Define

\[
 U_r=\|u\|_{L^3(B_{4r})},\qquad
 G_r=r\|\nabla u\|_{L^3(B_{4r})},\qquad
 Q_r=r^2\|q_0\|_{L^{3/2}}.                                      \tag{6.1}
\]

Calderon--Zygmund boundedness and (4.2) give the scale-invariant estimates

\[
 Q_r\leq C(G_r^2+U_rG_r+U_r^2),                                  \tag{6.2}
\]

and

\[
 \boxed{
 r^3\left|\int\phi S:\nabla^2(-\Delta)^{-1}q_0\,dx\right|
 \leq C G_r(G_r^2+U_rG_r+U_r^2).}                               \tag{6.3}
\]

This removes the artificial second derivative of \(u_i u_j\) from the
norm, but it requires \(\nabla u\in L_x^3\).  A parabolic cubic time average
contains

\[
 r\int_{t-r^2}^t\|\nabla u\|_3^3\,ds,                           \tag{6.4}
\]

whose mixed exponent satisfies \(3/3+2/3=5/3<2\), on the regular side of
the established critical gradient line \(3/p+2/q=2\).  Thus (6.3) is a
valid smoother-field estimate but not a weaker regularity criterion.

At the actual energy endpoint, (4.2) supplies only
\(q_0\in L^1\) for its leading term, while \(S\in L^2\).  These spaces are
not dual.  This is the exact near-field exponent gap left by R0.69M.

## 7. Route decision and next falsifiable target

The comparison has three outcomes.

* **Retain:** the shell lemma \(B_\infty\leq\mathfrak M_2/120\), together
  with the absence of a reverse estimate.
* **Reject as a new criterion:** the \(L^2\) near source \(N_r\) and the
  absolute annular quantity \(b_r\).  Both require information unavailable
  for generic suitable weak solutions, and high frequency defeats any
  velocity-only time-slice bound.
* **Do not promote:** the \(L^3\)--\(L^{3/2}\) repair.  It is exact and
  scale invariant but lies on the stronger side of known gradient criteria.

R0.69N will test whether the near pairing can be recast in a negative Sobolev
or Hardy--BMO duality that uses only energy-class quantities and one
derivative of the localized strain.  Its acceptance criterion is explicit:
the new estimate must be meaningful for (2.1), preserve the \(2^{-5m}\)
far-shell gain, and not assume a mixed norm already covered by a known
regularity theorem.  Failure of any one condition closes that functional
route.

R0.69M proves no Navier--Stokes regularity or singularity conclusion and does
not solve the Millennium Problem.

## 8. Primary sources used for the comparison

1. S. Gustafson, K. Kang, and T.-P. Tsai, *Interior regularity criteria for
   suitable weak solutions of the Navier--Stokes equations* (2006),
   <https://arxiv.org/abs/math/0607114>.
2. G. Seregin, *Regularity for Suitable Weak Solutions to the Navier--Stokes
   Equations in Critical Morrey Spaces* (2006),
   <https://arxiv.org/abs/math/0607537>.
3. L. Escauriaza, G. Seregin, and V. Sverak, *\(L_{3,\infty}\)-solutions of
   the Navier--Stokes equations and backward uniqueness* (2003),
   <https://www.mathnet.ru/eng/rm609>.
4. Q. Jiu, Y. Wang, and D. Zhou, *On Wolf's regularity criterion of suitable
   weak solutions to the Navier--Stokes equations* (2018),
   <https://arxiv.org/abs/1805.04841>.
