# R0.73Z independent analytic audit

**Audit date:** 2026-09-01

**Scope:** r073z_finiteness_obstruction_and_repair.md, before executable
certificate sealing

**Method:** independent line-by-line reconstruction of the five principal
arguments: high-frequency noncompactness, lacunary suitable shear,
energy-class upper bound, exact positive-scale kernel, and local Gaussian
lower bound.

## Verdict

After the corrections recorded below, all five boxed mathematical claims in
scope pass.  The audit does not cover a novelty claim, an executable
certificate, interior suitable-weak finiteness, a CKN bridge, or any Clay
conclusion.

## 1. High-frequency exact shear

For

\[
 u^{(n)}=e^{-\nu n^2t}\sin(nx_2)e_1,
\]

the periodic heat-kernel minimum on a compact positive scale interval gives

\[
 D_s(t,x)\ge\kappa\|\partial_2u_1^{(n)}(t)\|_{L^2(\mathbb T)}^2.
\]

On
\(J_n=[(2\nu n^2)^{-1},(\nu n^2)^{-1}]\), integration yields the exact
linear lower growth \(c n\).  On the three-torus,

\[
 \sup_t\|u^{(n)}(t)\|_2^2=4\pi^3,\qquad
 \nu\int_0^\infty\|\nabla u^{(n)}(t)\|_2^2dt=2\pi^3.
\]

Thus the energy total is \(6\pi^3\), independent of \(n\).  PASS.

## 2. Lacunary suitable shear

For \(N_j=8^j\), \(a_j=2^{-j}=N_j^{-1/3}\),

\[
 \sum_ja_j^2<\infty,\qquad a_j^3N_j=1.
\]

The disjoint intervals
\[
 J_j=[(2\nu N_j^2)^{-1},(\nu N_j^2)^{-1}]
\]
give
\[
 \int_0^{T_*}\|\partial_2F(t)\|_2^3dt
 \ge {\pi^{3/2}e^{-3}\over2\nu}\sum_{j\ge j_0}1=+\infty.
\]

Finite Fourier truncations converge strongly in
\(L_t^\infty L_x^2\cap L_t^2H_x^1\).  Passing their local heat-energy
equalities to the limit proves suitability on the open time domain
\(\mathbb T^3\times(0,T)\).  The result is an initial-trace obstruction,
not an interior singular solution.  PASS.

## 3. Energy-class upper bound for the repair

The inequalities

\[
 k_s\le\frac12P_s|u|^2,\qquad D_s\le P_s|\nabla u|^2
\]

and torus ultracontractivity imply

\[
 \int_{B_R}D_s\sqrt{k_s}
 \le Cs^{-3/4}\|u(t)\|_2\|\nabla u(t)\|_2^2.
\]

Since
\[
 \int_0^{\theta R^2}s^{-3/4}ds
 =4\theta^{1/4}R^{1/2},
\]
the prefactor \(\nu R^{-2}\) gives exactly
\[
 \mathcal K_D\le
 C\nu\theta^{1/4}R^{-3/2}U_IQ_I.
\]

No ball-volume factor is missing because the \(D_s\) integral is enlarged to
the whole torus and heat flow preserves its \(L^1\) mass.  PASS.

## 4. Exact positive-scale kernel

Strict positivity of the periodic heat kernel makes equality in either
variance equivalent to global spatial constancy of the sampled field.
For \(D_s=0\), the gradient is a constant matrix; periodicity forces that
matrix to vanish.  Hence, at fixed \(t,s>0\),

\[
 D_s(x)\sqrt{k_s(x)}=0
\quad\Longleftrightarrow\quad
u(t,\cdot)\ \hbox{is spatially constant}.
\]

For the integrated functional, the exact statement is spatial constancy for
almost every physical time.  Only an unforced periodic Navier--Stokes
trajectory makes that constant time independent.  The source was corrected
to retain this quantifier.  PASS.

## 5. Local centered-oscillation product

For \(x,y\in B_R\) and
\(s\in[\alpha R^2,\beta R^2]\), one lifted Euclidean Gaussian term obeys

\[
 g_s(x-y)\ge
 (4\pi\beta)^{-3/2}e^{-1/\alpha}R^{-3}.
\]

Restriction of the two variance integrals to \(B_R\), followed by minimization
over constants, gives

\[
 D_s\ge cR^{-3}G_R,\qquad k_s\ge cR^{-3}V_R.
\]

After space, scale, and the \(\nu/R^2\) normalization are integrated, the
power is exactly

\[
 c_{\alpha,\beta}\nu R^{-3/2}
 \int_I G_RV_R^{1/2}dt.
\]

The source now calls this a centered-oscillation product lower bound.  It is
not a common first-jet quotient: \(V_R\) and \(G_R\) remove different
constants, and the bound degenerates on local affine profiles.  PASS with
that corrected claim boundary.

## 6. Required publication boundary

- The original \(D_s^{3/2}\) functional is finite on compact smooth
  cylinders, but only extended-valued on the general suitable-weak class.
- The exact divergence example touches the initial trace.
- The repaired observable has a global periodic energy upper bound; a local
  upper bound with a minimal exterior tail is still open.
- The centered-oscillation lower bound is not CKN coercivity.
- No epsilon-regularity or global regularity theorem follows.

**NOT CLAY.**
