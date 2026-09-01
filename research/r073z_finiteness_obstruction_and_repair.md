# R0.73Z-A — finiteness obstruction for the cubic gradient covariance and an energy-compatible repair

**Frozen date:** 2026-09-01

**Status:** EXACT ANALYTIC THEOREMS / CERTIFICATE PENDING

**Claim class:** scale-critical positive observables; exact initial-endpoint
counterexample; energy-class upper bound; local oscillation lower bound

**Domain:** the normalized torus
\(\mathbb T^3=(\mathbb R/2\pi\mathbb Z)^3\), viscosity \(\nu>0\)

**Dependencies:** r073x_problem_freeze.md,
r073x_exterior_tail_freeze.md, and r073y_exact_shear_no_go.md

This note resolves the first gate frozen at the end of R0.73Y.  The proposed
observable

\[
 \mathcal D_{3/2}^{\square}(z_0,R;\theta)
 ={1\over R}\int_{I_R^\square}\int_0^{\theta R^2}
 \int_{B_R}D_{ii,s}^{3/2}\,dx\,ds\,dt
\tag{0.1}
\]

has the intended Navier--Stokes scaling, cubic amplitude homogeneity, and
strict detection of the exact shear kernel from R0.73Y.  It is finite on a
cylinder compactly contained in a smooth lifespan.  It is **not**, however,
an automatically finite functional on the energy class: a global exact
Leray--Hopf shear with \(L^2\) initial data makes (0.1) infinite on every
time interval touching the initial trace.  Even smooth one-mode shears show
that no initial-endpoint bound by the Leray energy can be uniform in
frequency.

The repair proposed and proved here is

\[
 \boxed{
 \mathcal K_D^{\square}(z_0,R;\theta)
 ={\nu\over R^2}\int_{I_R^\square}\int_0^{\theta R^2}
 \int_{B_R}D_{ii,s}\,k_s^{1/2}\,dx\,ds\,dt,}
\tag{0.2}
\]

where

\[
 k_s={1\over2}\left(P_s|u|^2-|P_su|^2\right).
\tag{0.3}
\]

It is nonnegative, scale invariant, cubic in amplitude, and finite for every
periodic energy-class velocity.  It strictly detects spatial nonconstancy
whenever that nonconstancy occurs on a positive-measure set of physical
times.  At scales \(s\simeq R^2\), it controls a precise product of the
local velocity oscillation and local gradient oscillation.  These facts do
**not** yet give a CKN smallness bridge, epsilon regularity, or a Clay
conclusion.

---

## 1. Heat covariances and conventions

Let \(P_s=e^{s\Delta}\) be the periodic heat semigroup.  For almost every
physical time at which \(u(t)\in H^1(\mathbb T^3)\), set

\[
 \begin{aligned}
 k_s[u](t,x)
 &=\frac12\left(P_s|u(t)|^2(x)-|P_su(t,x)|^2\right),\\
 D_s[u](t,x)
 &=P_s(|\nabla u(t)|_F^2)(x)-|\nabla P_su(t,x)|_F^2.
 \end{aligned}
\tag{1.1}
\]

We abbreviate \(D_s=D_{ii,s}\).  If \(K_s^{\rm per}\) denotes the strictly
positive periodic heat kernel, the exact variance formulas are

\[
 \begin{aligned}
 2k_s(x)
 &=\int_{\mathbb T^3}K_s^{\rm per}(x-y)
   |u(y)-P_su(x)|^2\,dy,\\
 D_s(x)
 &=\int_{\mathbb T^3}K_s^{\rm per}(x-y)
   |\nabla u(y)-P_s\nabla u(x)|_F^2\,dy.
 \end{aligned}
\tag{1.2}
\]

Consequently

\[
 0\le k_s\le\frac12P_s|u|^2,
 \qquad
 0\le D_s\le P_s|\nabla u|_F^2.
\tag{1.3}
\]

The gradient covariance also has the positive scale integral

\[
 D_s=2\int_0^sP_{s-r}|\nabla^2P_ru|_F^2\,dr,
\tag{1.4}
\]

while the velocity covariance satisfies

\[
 k_s=\int_0^sP_{s-r}|\nabla P_ru|_F^2\,dr.
\tag{1.5}
\]

Equations (1.4)--(1.5) are separate forced heat equations.  In particular,
\(D_s\) must not be identified with \(\partial_sk_s\).

For suitable weak solutions we first define, monotonically,

\[
 \mathcal D_{3/2,\varepsilon}^{\square}
 ={1\over R}\int_{I_R^\square}\int_\varepsilon^{\theta R^2}
 \int_{B_R}D_s^{3/2}\,dx\,ds\,dt,
 \qquad \varepsilon>0,
\tag{1.6}
\]

and then

\[
 \mathcal D_{3/2}^{\square}
 =\lim_{\varepsilon\downarrow0}
 \mathcal D_{3/2,\varepsilon}^{\square}\in[0,+\infty].
\tag{1.7}
\]

The limit exists as an extended value.  Finiteness is a theorem only under
additional hypotheses stated below.

---

## 2. Exact formal properties of the original candidate

### Proposition 2.1 — scaling and amplitude

On \(\mathbb R^3\), let

\[
 u_\lambda(t,x)=\lambda u(\lambda^2t,\lambda x),
 \qquad z_0^\lambda=(t_0/\lambda^2,x_0/\lambda),
 \qquad R_\lambda=R/\lambda.
\tag{2.1}
\]

Then

\[
 D_s[u_\lambda](t,x)
 =\lambda^4D_{\lambda^2s}[u](\lambda^2t,\lambda x),
\tag{2.2}
\]

and therefore, for either frozen cylinder clock,

\[
 \boxed{
 \mathcal D_{3/2}^{\square}[u_\lambda]
 (z_0^\lambda,R/\lambda;\theta)
 =\mathcal D_{3/2}^{\square}[u](z_0,R;\theta).}
\tag{2.3}
\]

For every \(A\in\mathbb R\),

\[
 \boxed{
 \mathcal D_{3/2}^{\square}[Au]
 =|A|^3\mathcal D_{3/2}^{\square}[u].}
\tag{2.4}
\]

Indeed, \(D_s^{3/2}\) contributes \(\lambda^6\),
\(dt\,dx\,ds\) contributes \(\lambda^{-7}\), and \(R^{-1}\)
contributes \(\lambda\).  Amplitude scaling follows from
\(D_s[Au]=A^2D_s[u]\).  On the fixed torus, (2.3) is interpreted only for
lattice-compatible scalings, exactly as in R0.73X.

### Proposition 2.2 — smooth finiteness and shear detection

Suppose the closure of \(I_R^\square\) is compactly contained in a smooth
lifespan and

\[
 M_2=\sup_{t\in I_R^\square}
 \|\nabla^2u(t)\|_{L^\infty(\mathbb T^3)}<\infty.
\tag{2.5}
\]

Then

\[
 0\le D_s\le2sM_2^2,
\tag{2.6}
\]

and hence

\[
 \mathcal D_{3/2}^{\square}
 \le {2^{5/2}\over5R}|I_R^\square|\,|B_R|\,M_2^3
 (\theta R^2)^{5/2}<\infty.
\tag{2.7}
\]

For every nonzero member of the R0.73Y orthogonal shear class,
\(D_s(t,x)>0\) for every \(t>0,x\in\mathbb T^3,s>0\).  Thus

\[
 \mathcal D_{3/2}^{\square}[u^A]=|A|^3C_D,
 \qquad C_D>0\quad(A\ne0),
\tag{2.8}
\]

on every admissible smooth cylinder.  This verifies the intended formal
gates but says nothing yet about energy-class finiteness.

---

## 3. Exact failure at an energy-class initial endpoint

The next two theorems use an interval touching the initial trace.  This is
deliberate.  The R0.73X suitable-weak cylinders satisfy
\(I_{4R}^\square\Subset(0,T)\); therefore the theorems below do not assert
an interior singular example.  They prove that energy control alone cannot
justify a finite extension through an initial endpoint, and that any
interior proof must use more than the bare Leray norms or must retain a
quantified distance from the initial time.

### Theorem 3.1 — smooth high-frequency noncompactness

For \(n\ge1\), let

\[
 u^{(n)}(t,x)=e^{-\nu n^2t}\sin(nx_2)e_1,
 \qquad p^{(n)}=0,
 \qquad t\ge0.
\tag{3.1}
\]

Fix \(R>0\), a ball \(B_R\), a physical-time depth \(T_*>0\), and
\(0<s_0<s_1\le\theta R^2\).  Then there are constants
\(c=c(\nu,R,s_0,s_1)>0\) and \(n_0=n_0(\nu,T_*)\), independent of
\(n\), such that

\[
 {1\over R}\int_0^{T_*}\int_{s_0}^{s_1}
 \int_{B_R}D_s[u^{(n)}]^{3/2}\,dx\,ds\,dt
 \ge c n,
 \qquad n\ge n_0.
\tag{3.2}
\]

In contrast,

\[
 \sup_{t\ge0}\|u^{(n)}(t)\|_2^2
 +\nu\int_0^\infty\|\nabla u^{(n)}(t)\|_2^2\,dt
\tag{3.3}
\]

is independent of \(n\).  Consequently there is no frequency-uniform bound
of the initial-endpoint version of (0.1) by a cubic function of the Leray
energy.

#### Proof

Let \(H_s=e^{s\partial_2^2}\) and
\(G_n(t)=\partial_2u^{(n)}_1(t)\).  Since the one-dimensional periodic heat
kernel is continuous and strictly positive,

\[
 \kappa=\min_{s\in[s_0,s_1],\,\xi\in\mathbb T}K_s^{\rm per}(\xi)>0.
\tag{3.4}
\]

For \(c_{s,x}=H_sG_n(t,x_2)\), the variance formula and the zero mean of
\(G_n\) give

\[
 \begin{aligned}
 D_s(t,x)
 &=\int_{\mathbb T}K_s^{\rm per}(x_2-y)
   |G_n(t,y)-c_{s,x}|^2\,dy\\
 &\ge\kappa\int_{\mathbb T}|G_n(t,y)-c_{s,x}|^2\,dy
 \ge\kappa\|G_n(t)\|_{L^2(\mathbb T)}^2.
 \end{aligned}
\tag{3.5}
\]

On

\[
 J_n=\left[{1\over2\nu n^2},{1\over\nu n^2}\right]
 \subset(0,T_*)
\tag{3.6}
\]

for all sufficiently large \(n\),

\[
 \|G_n(t)\|_{L^2(\mathbb T)}
 =\sqrt\pi\,n e^{-\nu n^2t}
 \ge\sqrt\pi e^{-1}n.
\tag{3.7}
\]

Integrating the cube of (3.7) over \(J_n\), then using (3.5), yields
(3.2).  Formula (3.3) follows directly from heat-energy equality. \(\square\)

### Theorem 3.2 — one exact Leray--Hopf shear with infinite observable

Let \(N_j=8^j\), \(a_j=N_j^{-1/3}=2^{-j}\), and define in
\(L^2(\mathbb T)\)

\[
 F_0(\xi)=\sum_{j=1}^\infty a_j\sin(N_j\xi).
\tag{3.8}
\]

Set

\[
 F(t)=H_{\nu t}F_0,
 \qquad
 u(t,x)=F(t,x_2)e_1,
 \qquad p=0.
\tag{3.9}
\]

Then (3.9) is a global mean-zero Leray--Hopf and suitable weak solution of
the unforced three-dimensional Navier--Stokes equations.  It is smooth for
every \(t>0\), satisfies the global energy equality, and for every
\(T_*>0\), every ball \(B_R\), and every
\(0<s_0<s_1\le\theta R^2\),

\[
 \boxed{
 {1\over R}\int_0^{T_*}\int_{s_0}^{s_1}
 \int_{B_R}D_s[u]^{3/2}\,dx\,ds\,dt=+\infty.}
\tag{3.10}
\]

#### Proof

Since \(\sum_ja_j^2<\infty\), \(F_0\in L^2(\mathbb T)\).  The convection
term vanishes identically because \(u_1\) depends only on \(x_2\), so (3.9)
is exactly the one-dimensional heat flow embedded in three dimensions.

For completeness, let \(F_0^{(J)}\) be the finite Fourier truncation and let
\(u^{(J)}\) be its heat evolution.  Every \(u^{(J)}\) is smooth and satisfies
the local energy equality.  Fourier orthogonality and the heat-energy
identity give, on every finite time interval,

\[
 u^{(J)}\longrightarrow u
 \quad\hbox{strongly in}\quad
 L_t^\infty L_x^2\cap L_t^2H_x^1.
\tag{3.9a}
\]

Passing the local equality to the limit proves suitability on the open
time domain \(\mathbb T^3\times(0,T)\); equivalently one may use the
renormalized local energy identity for the linear heat equation.  The same
convergence gives the global Leray--Hopf energy equality, while standard heat
smoothing gives \(C^\infty\) regularity for every \(t>0\).

Writing \(G(t)=\partial_2F(t)\), Fourier orthogonality gives

\[
 \|G(t)\|_{L^2(\mathbb T)}^2
 =\pi\sum_{j=1}^\infty
 a_j^2N_j^2e^{-2\nu N_j^2t}.
\tag{3.11}
\]

The intervals

\[
 J_j=\left[{1\over2\nu N_j^2},{1\over\nu N_j^2}\right]
\tag{3.12}
\]

are pairwise disjoint.  For all sufficiently large \(j\), they lie in
\((0,T_*)\), and on \(J_j\),

\[
 \|G(t)\|_2^3
 \ge\pi^{3/2}e^{-3}a_j^3N_j^3.
\tag{3.13}
\]

Hence

\[
 \int_0^{T_*}\|G(t)\|_2^3\,dt
 \ge {\pi^{3/2}e^{-3}\over2\nu}
 \sum_{j\ge j_0}a_j^3N_j
 =+\infty,
\tag{3.14}
\]

because \(a_j^3N_j=1\).  The kernel lower bound (3.5) is uniform in
\(x\) and \(s\in[s_0,s_1]\), so (3.14) implies (3.10). \(\square\)

### Corollary 3.3 — exact endpoint boundary

For every \(\delta>0\), the same solution is smooth on
\([\delta,T_*]\), and its version of (0.1) is finite there.  By monotone
convergence it diverges as \(\delta\downarrow0\).  Thus the obstruction is
an initial-trace uniformity failure, not a constructed interior singularity.

For an arbitrary suitable weak solution on an admissible interior cylinder,
(1.7) remains a legitimate nonnegative extended-value definition.  The
present energy estimates do not establish that the value is finite, and the
theorems above rule out closing that gap by a bare energy bound that is
uniform up to the initial trace.

---

## 4. The repaired positive cubic observable

### Theorem 4.1 — exact algebraic gates

The functional \(\mathcal K_D^\square\) in (0.2) is nonnegative.  Under
the Navier--Stokes scaling (2.1),

\[
 k_s[u_\lambda](t,x)
 =\lambda^2k_{\lambda^2s}[u](\lambda^2t,\lambda x),
\tag{4.1}
\]

and hence

\[
 \boxed{
 \mathcal K_D^\square[u_\lambda]
 (z_0^\lambda,R/\lambda;\theta)
 =\mathcal K_D^\square[u](z_0,R;\theta).}
\tag{4.2}
\]

Moreover,

\[
 \boxed{
 \mathcal K_D^\square[Au]
 =|A|^3\mathcal K_D^\square[u].}
\tag{4.3}
\]

Indeed, \(D_s\sqrt{k_s}\) contributes \(\lambda^5\), the
space--time--scale measure contributes \(\lambda^{-7}\), and \(R^{-2}\)
contributes \(\lambda^2\).  The viscosity is unchanged by the scaling.

### Theorem 4.2 — energy-class finiteness

Let \(I\subset(0,T)\), or let \(I\) touch the initial trace, and assume

\[
 u\in L^\infty(I;L^2(\mathbb T^3))
 \cap L^2(I;H^1(\mathbb T^3)).
\tag{4.4}
\]

Put

\[
 U_I=\operatorname*{ess\,sup}_{t\in I}\|u(t)\|_2,
 \qquad
 Q_I=\int_I\|\nabla u(t)\|_2^2\,dt.
\tag{4.5}
\]

For \(0<R<\pi/8\) and \(0<\theta\le1\),

\[
 \boxed{
 \mathcal K_D[I,B_R;\theta]
 \le C_{\mathbb T^3}\,\nu\theta^{1/4}R^{-3/2}U_IQ_I<\infty.}
\tag{4.6}
\]

Here the left side denotes (0.2) with \(I\) in place of
\(I_R^\square\).  The constant is independent of the solution, \(I,R\),
and \(\theta\).

#### Proof

For \(0<s\le\theta R^2<1\), the periodic heat kernel obeys the standard
ultracontractive estimate

\[
 \|P_sh\|_\infty\le C_{\mathbb T^3}s^{-3/2}\|h\|_1.
\tag{4.7}
\]

Using (1.3), positivity, preservation of the spatial integral, and then
(4.7),

\[
 \begin{aligned}
 \int_{B_R}D_s\sqrt{k_s}\,dx
 &\le {1\over\sqrt2}
 \|P_s|u|^2\|_\infty^{1/2}
 \int_{\mathbb T^3}P_s|\nabla u|^2\,dx\\
 &\le C_{\mathbb T^3}s^{-3/4}
 \|u(t)\|_2\|\nabla u(t)\|_2^2.
 \end{aligned}
\tag{4.8}
\]

Since

\[
 \int_0^{\theta R^2}s^{-3/4}\,ds
 =4\theta^{1/4}R^{1/2},
\tag{4.9}
\]

integration of (4.8) proves (4.6). \(\square\)

The factor \(\sqrt{k_s}\) is therefore not cosmetic: it changes the direct
time demand from the unavailable \(\|\nabla u\|_2^3\) to the Leray-integrable
\(\|u\|_2\|\nabla u\|_2^2\).

### Theorem 4.3 — exact spatial kernel

Fix \(t\) with \(u(t)\in H^1(\mathbb T^3)\), and fix \(s>0\).  Then the
following are equivalent:

1. \(u(t,\cdot)\) is spatially constant almost everywhere;
2. \(k_s(t,x)=0\) for one, hence every, \(x\);
3. \(D_s(t,x)=0\) for one, hence every, \(x\);
4. \(D_s(t,x)\sqrt{k_s(t,x)}=0\) for one, hence every, \(x\).

If \(u(t,\cdot)\) is not constant, both \(k_s(t,x)\) and \(D_s(t,x)\)
are strictly positive for every \(x\).

#### Proof

The kernel in (1.2) is strictly positive.  Equality in its variance forces
the sampled function to be constant almost everywhere on the whole torus.
Thus \(k_s(x)=0\) forces \(u\) to be constant.  Likewise \(D_s(x)=0\)
forces \(\nabla u\) to be a constant matrix.  Periodicity then forces that
matrix to be zero, so \(u\) is constant.  The converse is immediate.
\(\square\)

In particular, (0.2) detects every nonzero R0.73Y orthogonal shear on every
positive-measure smooth cylinder.  On a nondegenerate physical-time interval,
\(\mathcal K_D=0\) if and only if \(u(t,\cdot)\) is spatially constant for
almost every \(t\).  For a general energy-class field this spatial constant
may depend on time.  For an unforced periodic Navier--Stokes trajectory, the
equation further makes it a time-independent Galilean mode.

---

## 5. A local quotient lower bound at scales comparable to the ball

For a ball in the fixed Euclidean chart define

\[
 \begin{aligned}
 V_R[u](t)
 &=\int_{B_R}|u(t,x)-(u(t))_{B_R}|^2\,dx,\\
 G_R[u](t)
 &=\int_{B_R}|\nabla u(t,x)-(\nabla u(t))_{B_R}|_F^2\,dx.
 \end{aligned}
\tag{5.1}
\]

### Theorem 5.1 — local centered-oscillation product lower bound

Fix \(0<\alpha<\beta\le\theta\).  Every energy-class periodic field
satisfies

\[
 \boxed{
 {\nu\over R^2}\int_I\int_{\alpha R^2}^{\beta R^2}
 \int_{B_R}D_s\sqrt{k_s}\,dx\,ds\,dt
 \ge c_{\alpha,\beta}\nu R^{-3/2}
 \int_I G_R[u](t)V_R[u](t)^{1/2}\,dt.}
\tag{5.2}
\]

#### Proof

For \(x,y\in B_R\) and \(s\in[\alpha R^2,\beta R^2]\), one Euclidean
summand of the lifted periodic heat kernel gives

\[
 g_s(x-y)\ge c_{\alpha,\beta}R^{-3}.
\tag{5.3}
\]

Restricting the nonnegative variance integrals (1.2) to \(B_R\), and using
the fact that the mean minimizes the squared distance to a constant, yields

\[
 D_s(t,x)\ge c_{\alpha,\beta}R^{-3}G_R[u](t),
 \qquad
 k_s(t,x)\ge c_{\alpha,\beta}R^{-3}V_R[u](t).
\tag{5.4}
\]

Multiply (5.4), integrate over \(x\in B_R\), then over a scale interval of
length \((\beta-\alpha)R^2\), and multiply by \(\nu/R^2\).  Absorbing
geometric constants proves (5.2). \(\square\)

The two centered factors separately remove a velocity constant and a gradient
constant.  They do not define one common first-jet quotient: under
\(u\mapsto u+b+Mx\), \(G_R\) is unchanged but \(V_R\) generally changes.
Accordingly (5.2) is a centered-oscillation product lower bound, not
first-jet coercivity and not coercivity of the full CKN energy.  A locally
affine field makes \(G_R=0\), so the bound degenerates completely.  On the
torus the nonlocal heat tail makes the exact kernel smaller, but no
scale-uniform constant may be extracted from that exponentially weak tail as
\(R\to0\).

---

## 6. Literature boundary

The individual ingredients are established.  Positive-filter covariance is
classical; Germano's multilevel central moments and Johnson's exact Gaussian
scale evolution already supply the relevant stress and gradient-covariance
structures.  Heat-semigroup Besov and carré-du-champ theory supplies nearby
single-covariance seminorms.  LES one-equation models also use
\(\sqrt{k_{\rm sgs}}\) as an unresolved velocity scale next to gradient-based
dissipation terms.

A bounded primary-source audit did not locate the exact mixed functional
\(D_s\sqrt{k_s}\) with the same heat scale, \(ds\) measure, local cylinder,
and \(R^{-2}\) normalization, nor a direct semigroup norm equivalence.  This
is a bounded non-collision finding, **not** a novelty or priority proof.
The observable must not be called the standard signed LES energy flux:
\(-\tau_s:\nabla P_su\) is signed, whereas (0.2) is a nonnegative mixed
variance.

---

## 7. Closed and open rows after R0.73Z-A

### Closed analytically

1. \(\mathcal D_{3/2}\) has the intended scaling, amplitude, smooth
   finiteness, and exact-shear detection.
2. Bare energy control does not give an initial-endpoint finite extension:
   there is both a smooth high-frequency noncompact sequence and one exact
   \(L^2\) Leray--Hopf shear with infinite \(\mathcal D_{3/2}\).
3. \(\mathcal K_D\) is positive, scale invariant, cubic, energy-class
   finite, and detects all spatially nonconstant periodic fields.
4. At \(s\simeq R^2\), \(\mathcal K_D\) controls the local centered
   product \(G_RV_R^{1/2}\), with explicit degeneration on affine profiles.

### Still open

1. finite-valued \(\mathcal D_{3/2}\) on every admissible interior suitable-
   weak cylinder;
2. a local upper bound for \(\mathcal K_D\) using only
   \(\mathcal E^\square(z_0,4R)\) plus a minimal declared exterior tail;
3. a scale-uniform lower bound controlling a CKN quantity after quotienting
   the precise local first-jet near-kernel;
4. pressure-active and genuinely three-dimensional tests of that quotient;
5. weak stability, compactness, and lower semicontinuity strong enough to pass
   to blow-up limits;
6. any epsilon-regularity or global regularity implication.

**NOT CLAY.**
