# R0.70C — Linear-parity obstruction to dynamical recovery of annular sign defects

> **Status:** internal canonical research report; not a public theorem chapter
> **Date:** 2026-08-24
> **Audience:** researchers in three-dimensional incompressible Navier--Stokes
> **Baseline:** R0.70B, commit `c16f518`
> **Domain:** primarily \(\mathbb R^3\); one explicitly separated periodic corollary
> **Arithmetic certificate:** `certificates/r070c/result.json`

The labels used below are **[F]** for an externally sourced fact, **[P]** for
a proof completed in this report, **[O]** for a proved obstruction, and
**[U]** for an unresolved statement.  Every conclusion is restricted to the
objects and domains stated here.

## 1. Direct answer and route decision

R0.70B isolated the sign defect

\[
 D_I^{\mathrm{sign}}
 =\iint_{I\times\mathbb R^3}|w(x,t)|\,dx\,dt
  -\left|\iint_{I\times\mathbb R^3}w(x,t)\,dx\,dt\right|.
 \tag{1.1}
\]

R0.70C asks whether the fact that \(w\) comes from a genuine smooth
Navier--Stokes trajectory can make this defect lower order.  The answer is
**no without an additional sign-selection hypothesis**.

1. **[O] Initial-trace gate.**  Any instantaneous estimate asserted for all
   smooth solutions at \(t=0\) must already hold for every smooth
   divergence-free datum.  Navier--Stokes dynamics cannot repair a
   kinematic failure at the lower face of a cylinder.
2. **[P] Linear parity.**  If a velocity is even under \(x\mapsto-x\), then
   its vorticity is odd and every even-window annular density is odd.  Its
   signed integral vanishes although its absolute integral need not.
3. **[O] Genuine \(\mathbb R^3\) small-data trajectories for a fixed
   annular functional.**  There are finite-energy global smooth solutions
   \(u^\varepsilon\) on a fixed cylinder for which

   \[
    \iint|w[u^\varepsilon]|
       =A_I\varepsilon^3+O_I(\varepsilon^4),
    \qquad
    \iint w[u^\varepsilon]=O_I(\varepsilon^4),
    \qquad A_I>0.
    \tag{1.2}
   \]

   Thus \(|W_I|/\iint|w|\to0\), even within the class of global smooth
   small-data solutions.
4. **[O] Exact nonlinear cancellation for a fixed functional in this
   class.**  A one-parameter amplitude tuning and the implicit-function
   theorem sharpen (1.2): for a fixed even cutoff large enough to contain two
   separated interaction regions, one can arrange on a sufficiently short
   cylinder

   \[
    W_I[u^\varepsilon]=0,
    \qquad
    D_I^{\mathrm{sign}}[u^\varepsilon]>0
    \tag{1.3}
   \]

   for an actual global smooth \(\mathbb R^3\) Navier--Stokes solution.
5. **[O] Exact periodic total-production model.**  The unit ABC Beltrami
   field gives an all-time example with zero signed total vortex stretching
   and nonzero absolute stretching.  Its shellwise upgrade requires a
   separately specified periodized annular reconstruction.
6. **[U] What remains.**  A pre-singular estimate may still impose an
   independent geometric, ensemble, or sign-selection condition.  It cannot
   derive a favorable sign ratio from smooth Navier--Stokes evolution alone.

The R0.69T signed annulus therefore cannot replace a positive far-field
budget by appeal to an unrestricted ``Navier--Stokes dynamics creates the
sign'' principle.  The sign defect is already present in the cubic linear
heat layer and is not merely a nonlinear turbulence effect.  Transfer of the
obstruction to every prescribed Yu \(\chi_k,\eta_j,I_k\) geometry is a
separate unresolved matching problem.  Nothing here proves regularity,
blow-up, or any part of the Millennium claim.

## 2. Locked annular functional

Fix a smooth compactly supported even filter \(\varphi_\ell\), an even
nonnegative annular window \(\eta\), and an even nonnegative spatial cutoff
\(\chi\).  Put

\[
 U=\varphi_\ell*u,
 \qquad
 \Omega=\nabla\times U,
 \qquad
 e_z=\frac z{|z|}.
 \tag{2.1}
\]

The fixed-shell density used in R0.70B can be written, with its positive
normalizing constant denoted by \(c_*\), as

\[
 w_\eta[U](x,t)
 =c_*\int_{\mathbb R^3}
 \frac{\eta(z)}{|z|^3}
 \bigl(e_z\cdot\Omega(x,t)\bigr)
 \bigl(e_z\cdot(\Omega(x+z,t)\times\Omega(x,t))\bigr)
 \,dz.
 \tag{2.2}
\]

Here \(c_*\) may include the factor \(3r_k/(4\pi)\) from R0.70B.  Its value
does not affect signs or the ratios below.  For a compact time interval \(I\)
define

\[
 \begin{aligned}
  W_I[u]&=\int_I\int\chi(x)w_\eta[U](x,t)\,dx\,dt,\\
  P_I[u]&=\int_I\int\chi(x)|w_\eta[U](x,t)|\,dx\,dt,\\
  D_I^{\mathrm{sign}}[u]&=P_I[u]-|W_I[u]|.
 \end{aligned}
 \tag{2.3}
\]

The density is cubic:

\[
 w_\eta[aU]=a^3w_\eta[U].
 \tag{2.4}
\]

Because \(\eta\) is supported away from zero, (2.2) is a continuous
trilinear local functional.  If

\[
 K\supset\operatorname{supp}\chi\ \cup\
 (\operatorname{supp}\chi+\operatorname{supp}\eta),
 \tag{2.5}
\]

then for smooth \(U,V\),

\[
 \|\chi(w_\eta[U]-w_\eta[V])\|_{L^1}
 \le C_{\eta,\chi,K}
 (\|U\|_{C^1(K)}+\|V\|_{C^1(K)})^2
 \|U-V\|_{C^1(K)}.
 \tag{2.6}
\]

This follows by polarizing the three vorticity factors and applying the
triangle inequality.  Formula (2.6) is the continuity input for every
\(O(\varepsilon^4)\) remainder below; no statistical closure is used.

For completeness, the pointwise full R0.69T partition is legitimate for
smooth compactly supported vorticity.  Near \(z=0\),
\(\Omega(x+z)\times\Omega(x)=O_x(|z|)\), so the absolute radial integrand is
locally \(O_x(1)\,d|z|\); at infinity compact support removes the tail.
Dominated convergence therefore permits a nonnegative dyadic partition in
\(z\) to be summed inside the pointwise Biot--Savart representation.  This is
the pointwise reconstruction used in Section 6, not a periodic reconstruction.

## 3. Literature gap matrix

The literature search was restricted to original papers and exact claims.
It stopped when the remaining gap became a theorem-design question rather
than a missing reference.

| Claim family | Primary result | What it proves | Why it does not control (1.1) |
|---|---|---|---|
| Local and small-data strong solutions | [Kato, 1984](https://doi.org/10.1007/BF01174182) | Local strong solutions for divergence-free \(L^3\) data in \(\mathbb R^3\), and global solutions for sufficiently small \(L^3\) data | It realizes arbitrary smooth data as initial traces; it supplies no sign coherence |
| Vorticity-direction depletion | [Constantin--Fefferman, 1993](https://iumj.org/article/3627/) | Smoothness under a coherence condition on high-vorticity directions | Coherence is an added hypothesis, not an automatic NSE consequence |
| Physical-scale energy cascade | [Dascaliuc--Grujić, 2011](https://arxiv.org/abs/1101.2193) | Positive, comparable ensemble-averaged flux under a Taylor-scale condition | Positive cover averages do not bound the absolute local negative mass |
| Coherent enstrophy cascade | [Dascaliuc--Grujić, 2012](https://arxiv.org/abs/1107.0058) | Positive ensemble enstrophy flux under direction coherence, modulation, and a Kraichnan-scale condition | The geometric, scale, localization, and modulation assumptions are inputs; the positive conclusion remains an ensemble average |
| Smooth coarse-graining | [Eyink--Aluie, 2009](https://arxiv.org/html/0909.2386v1) | Rigorous absolute locality bounds and a distinction between absolute and signed transfers | Faster signed decay is attributed to cancellation after averaging, not a deterministic lower bound on the sign ratio |
| Localized Beltrami data | [Ciampa--Lucà, 2024](https://arxiv.org/html/2311.01369v3) | Finite-energy global smooth \(\mathbb R^3\) solutions from suitably localized Beltrami structures satisfying a nonlinear smallness condition | Localization destroys the exact Beltrami identity; the construction does not impose shellwise sign |
| Filtered vortex stretching | [Yu, 2026 v1](https://arxiv.org/html/2606.27560v1) | A positive-part far-field budget whose reassigned annular portion admits conditional Carleson closure, with commutator, localization, and exterior-tail budgets kept separate | The annular reservoirs are nonnegative magnitude majorants; replacing them by signed \(W_I\) requires the missing sign-defect estimate, and the exterior tail is not covered by the annular closure |

No source found in this bounded search proves a deterministic estimate of the
form \(D_I^{\mathrm{sign}}\le C|W_I|\).  This is a search result, not a claim
that no historically equivalent observation exists.

## 4. The initial-trace gate

### Proposition 4.1 [O]

Let \(\mathcal D\) and \(\mathcal R\) be continuous functionals on smooth
divergence-free fields.  If

\[
 \mathcal D(u(t))\le\mathcal R(u(t))
 \tag{4.1}
\]

is asserted for every classical \(\mathbb R^3\) Navier--Stokes solution and
every \(t\in[0,T_u)\), then (4.1) must hold for every divergence-free
Schwartz field.

**Proof.**  Given an arbitrary divergence-free Schwartz field \(u_0\), Kato
local well-posedness supplies a classical solution with \(u(0)=u_0\).
Evaluate (4.1) at \(t=0\).  \(\square\)

The same argument applies to a family of shrinking cylinders: continuity
gives

\[
 \frac1T\int_0^T F(u(t))\,dt\longrightarrow F(u_0)
 \quad(T\downarrow0).
 \tag{4.2}
\]

Thus any claimed dynamic improvement that includes the lower time face must
either survive every kinematic datum or contain an explicit initial-trace,
time-history, or positive-time hypothesis.  R0.70C next removes the possible
objection that cancellation might disappear on a fixed nonzero interval.

## 5. Inversion parity acts at cubic order

### Lemma 5.1 [P]

If \(U(-x)=U(x)\), then

\[
 \Omega(-x)=-\Omega(x),
 \qquad
 w_\eta[U](-x)=-w_\eta[U](x).
 \tag{5.1}
\]

Consequently, for even \(\chi\),

\[
 \int\chi(x)w_\eta[U](x)\,dx=0.
 \tag{5.2}
\]

**Proof.**  The curl of an even vector field is odd.  In (2.2), evaluate at
\(-x\), use

\[
 \Omega(-x)=-\Omega(x),
 \qquad
 \Omega(-x+z)=-\Omega(x-z),
 \tag{5.3}
\]

and then change variables \(z\mapsto-z\).  Both appearances of \(e_z\)
change sign, while the initial factor from \(\Omega(-x)\) remains.  Hence the
complete cubic density changes sign.  Equation (5.2) follows by integrating
an odd function against an even cutoff.  \(\square\)

This is not a preserved nonlinear symmetry.  The Euclidean inversion action
on polar velocities is

\[
 (\mathcal Ru)(x)=-u(-x).
 \tag{5.4}
\]

The full Navier--Stokes equation is equivariant under \(\mathcal R\), whereas
an even velocity satisfies \(\mathcal Ru=-u\).  The heat equation preserves
evenness, but the projected quadratic nonlinearity generated by an even
field is odd.  The full solution therefore has the perturbative parity
structure

\[
 u^\varepsilon
 =\varepsilon u^{(1)}_{\mathrm{even}}
  +\varepsilon^2u^{(2)}_{\mathrm{odd}}+O(\varepsilon^3).
 \tag{5.5}
\]

This is precisely why the signed work begins at fourth order while the
absolute activity begins at third order.

## 6. A nontrivial even seed

Consider the periodic field

\[
 V(x,y,z)=(\cos y,\cos z,\cos x).
 \tag{6.1}
\]

It has the odd vector potential

\[
 A(x,y,z)=(\sin z,\sin x,\sin y),
 \qquad
 \nabla\times A=V,
 \tag{6.2}
\]

and

\[
 \nabla\cdot V=0,
 \quad
 \nabla\times V=A,
 \quad
 \Delta V=-V.
 \tag{6.3}
\]

Direct exact calculation gives

\[
 (\nabla\times V)\cdot S[V](\nabla\times V)
 =-3\sin x\sin y\sin z.
 \tag{6.4}
\]

This is odd, has zero torus mean, and is not zero.  In fact

\[
 \int_{\mathbb T^3}|-3\sin x\sin y\sin z|\,dx\,dy\,dz=192,
 \qquad
 \int_{\mathbb T^3}9\sin^2x\sin^2y\sin^2z\,dx\,dy\,dz=9\pi^3.
 \tag{6.5}
\]

Let \(\rho_R\) be a smooth even cutoff, equal to one on \(B_R\) and zero
outside \(B_{2R}\), and define

\[
 V_R=\nabla\times(\rho_R A).
 \tag{6.6}
\]

Then \(V_R\in C_c^\infty(\mathbb R^3)\), it is divergence free and even,
and it equals \(V\) on \(B_R\).  For a sufficiently small even filter, the
filtered stretching remains nonzero on a fixed inner ball.  The pointwise
R0.69T annular decomposition reconstructs that filtered stretching, so at
least one R0.69T dyadic shell \(n_*\) satisfies

\[
 \chi w_{n_*}[\varphi_\ell*V_R]\not\equiv0.
 \tag{6.7}
\]

The pointwise unsymmetrized Biot--Savart representation, partitioned by the
R0.69T windows before the \(x\)-integration, reconstructs (6.4) inside the
periodic core.  Hence at every point where (6.4) is nonzero, at least one
R0.69T physical shell has nonzero density.  Fix one such point, one such shell
\(n_*\), and a small even pair of neighborhoods around that point and its
inversion image.  After taking \(R\) large enough to contain the selected
interaction region, continuity under a sufficiently small even filter gives
a fixed even cutoff with positive absolute shell activity.  Common
Navier--Stokes dilation places this fixed-functional construction in any
prescribed physical cylinder.

This argument does **not** yet identify a literal Yu index \(j_Y\le k\).
R0.69T labels length by \(2^n\), whereas Yu uses \(r_j=2^{-j}\), so the first
required relabeling is \(n(j)=-j+O(1)\).  More importantly, varying \(k\)
also changes \(\ell_k,\chi_k\), and \(I_k\).  Continuity for the fixed cutoff
above does not verify nontriviality for that full \(k\)-dependent geometry.
That matching transfer remains **[U]**.

## 7. Fixed-cylinder small-data obstruction

### Theorem 7.1 [O]

There exist smooth compactly supported divergence-free data \(V_R\), a fixed
even filter, a fixed even R0.69T annular window, a fixed even cutoff, and a
compact time interval \(I\), such that for all sufficiently small
\(\varepsilon>0\), the unique global smooth Navier--Stokes solution with
initial datum
\(\varepsilon V_R\) obeys

\[
 \boxed{
 P_I[u^\varepsilon]
 =A_I\varepsilon^3+O_I(\varepsilon^4),
 \qquad
 W_I[u^\varepsilon]=O_I(\varepsilon^4),
 \qquad A_I>0.}
 \tag{7.1}
\]

Consequently,

\[
 D_I^{\mathrm{sign}}[u^\varepsilon]
 =A_I\varepsilon^3+O_I(\varepsilon^4),
 \qquad
 \frac{|W_I[u^\varepsilon]|}{P_I[u^\varepsilon]}\longrightarrow0.
 \tag{7.2}
\]

**Proof.**  Kato's small-data theorem gives a global mild solution.  Fix an
integer \(m\ge4\).  High-Sobolev persistence and smooth dependence on every
fixed compact interval give

\[
 u^\varepsilon(t)
 =\varepsilon v(t)+\varepsilon^2q^\varepsilon(t),
 \qquad
 v(t)=e^{\nu t\Delta}V_R,
 \qquad
 \sup_{0<\varepsilon<\varepsilon_0}
 \|q^\varepsilon\|_{C(I;H^m(\mathbb R^3))}<\infty.
 \tag{7.3}
\]

The embedding \(H^m(\mathbb R^3)\hookrightarrow C^1(\mathbb R^3)\) supplies
the uniform \(C(I;C^1(K))\) bound required in (2.6).

The heat flow \(v(t)\) is even.  Lemma 5.1 therefore gives

\[
 \int\chi w_\eta[\varphi_\ell*v(t)]\,dx=0
 \quad(t\in I).
 \tag{7.4}
\]

Choose the shell from Section 6 and an interval on which its time-space
absolute activity is nonzero, and set

\[
 A_I=\int_I\int\chi
 |w_\eta[\varphi_\ell*v(t)]|\,dx\,dt>0.
 \tag{7.5}
\]

The cubic homogeneity and continuity estimate (2.6) now yield

\[
 \chi w_\eta[\varphi_\ell*u^\varepsilon]
 =\varepsilon^3\chi w_\eta[\varphi_\ell*v]
  +O_{L^1(I\times\mathbb R^3)}(\varepsilon^4).
 \tag{7.6}
\]

Integrating (7.6), with and without the absolute value, proves (7.1)--(7.2).
\(\square\)

For an interval bounded away from zero, choose \(R\) large.  On every fixed
compact cylinder, \(e^{\nu t\Delta}V_R\) converges in \(C^m\) to
\(e^{-\nu t}V\) as \(R\to\infty\).  Formula (6.4) then guarantees a nonzero
time-space annular component on that positive-time interval.  The obstruction
is therefore not confined to the initial time face.

### Corollary 7.2 [O]

There is no constant \(C\), independent of the smooth small-data solution,
such that

\[
 P_I[u]\le C|W_I[u]|
 \quad\hbox{or}\quad
 D_I^{\mathrm{sign}}[u]\le C|W_I[u]|.
 \tag{7.7}
\]

More generally, let \(X,Y\) be nonnegative quantities satisfying, along this
family,

\[
 X(u^\varepsilon)\le C_X\varepsilon,
 \qquad
 Y(u^\varepsilon)\le C_Y\varepsilon^2.
 \tag{7.8}
\]

Any homogeneous product estimate

\[
 D_I^{\mathrm{sign}}
 \le C|W_I|^aX^bY^c,
 \qquad
 a>0,\quad b,c\ge0,
 \qquad
 3a+b+2c=3,
 \tag{7.9}
\]

fails on this family: its right side is
\(O(\varepsilon^{3+a})\), while its left side is
\(\Theta(\varepsilon^3)\).  This statement does not exclude an independent
additive cubic positive term; such a term directly pays for the missing
absolute activity and recovers no cancellation gain.

## 8. Exact zero for a fixed large-cutoff functional

The preceding theorem makes the signed term one order smaller.  For a fixed
member of the annular-functional class (2.2)--(2.3), with an even cutoff that
can contain two separated copies and their interaction neighborhoods, it can
be made exactly zero without leaving the class of global smooth
\(\mathbb R^3\) solutions.

For this section define the instantaneous filtered scalar

\[
 F(v):=\int_{\mathbb R^3}\chi(x)
 w_\eta[\varphi_\ell*v](x)\,dx,
 \qquad
 W_I[v]=\int_I F(v(t))\,dt.
\]

R0.69W supplies a compactly supported divergence-free seed \(q\) and a
physical annulus for which the instantaneous signed scalar is strictly
nonzero.  A sufficiently small even filter preserves that strict inequality
by continuity.  Translate the seed far from the origin, call it \(q^+\), and
let

\[
 q^-=\mathcal Rq^+,
 \qquad
 (\mathcal Rq^+)(x)=-q^+(-x)
 \tag{8.1}
\]

be the natural inversion action.  With the two filtered supports and their
annular neighborhoods disjoint at time zero, define

\[
 q_\lambda=q^+-\lambda q^-.
 \tag{8.2}
\]

Write

\[
 K_\pm=\operatorname{supp}\nabla\times(\varphi_\ell*q^\pm).
 \tag{8.3}
\]

Choose the translation and cutoff so that

\[
 [(K_+-K_-)\cup(K_--K_+)]\cap\operatorname{supp}\eta=\varnothing,
 \qquad
 \chi\equiv1\quad\hbox{on }K_+\cup K_-.
 \tag{8.4}
\]

The first condition excludes every cross-pair and the second retains the
full-space one-copy scalar certified in R0.69W.  If that scalar is
\(A\ne0\), scalar covariance gives \(F(q^-)=F(q^+)=A\), while cubic
homogeneity gives \(F(-\lambda q^-)=-\lambda^3A\).  Therefore, exactly,

\[
 F(q_\lambda)=A(1-\lambda^3),
 \qquad
 F(q_1)=0,
 \qquad
 \partial_\lambda F(q_\lambda)|_{\lambda=1}=-3A\ne0.
 \tag{8.5}
\]

### Theorem 8.1 [O]

Fix the even window and the even cutoff just constructed.  For a sufficiently
short interval \(I=[0,T]\), there are
\(\varepsilon_0>0\) and a \(C^1\) function
\(\lambda:(-\varepsilon_0,\varepsilon_0)\to\mathbb R\), with
\(\lambda(0)=1\), such that the global smooth solution with initial datum

\[
 u_0^\varepsilon=\varepsilon q_{\lambda(\varepsilon)}
 \tag{8.6}
\]

satisfies, for every \(0<\varepsilon<\varepsilon_0\),

\[
 \boxed{
 W_I[u^\varepsilon]=0,
 \qquad
 P_I[u^\varepsilon]>0,
 \qquad
 D_I^{\mathrm{sign}}[u^\varepsilon]=P_I[u^\varepsilon].}
 \tag{8.7}
\]

**Proof.**  Smallness in \(L^3\) gives a global Kato solution uniformly for
\(\lambda\) near one.  To justify differentiability at zero amplitude, do not
divide only an \(O(\varepsilon^2)\) expansion.  Instead write
\(a^{\varepsilon,\lambda}=u^{\varepsilon,\lambda}/\varepsilon\) for
\(\varepsilon\ne0\).  In the small-data Kato contraction space it satisfies

\[
 a^{\varepsilon,\lambda}(t)
 =e^{\nu t\Delta}q_\lambda
  -\varepsilon\int_0^t e^{\nu(t-s)\Delta}
   \mathbb P\nabla\!\cdot
   (a^{\varepsilon,\lambda}\otimes a^{\varepsilon,\lambda})(s)\,ds.
 \tag{8.8}
\]

The uniform contraction and its differentiated fixed-point equation extend
\(a^{\varepsilon,\lambda}\) as a \(C^1\) function of
\((\varepsilon,\lambda)\) through
\(a^{0,\lambda}=e^{\nu t\Delta}q_\lambda\), also in the local smooth norm
used in (2.6).  For \(\varepsilon\ne0\), set

\[
 H(\varepsilon,\lambda,T)
 =\varepsilon^{-3}W_{[0,T]}[u^{\varepsilon,\lambda}].
 \tag{8.9}
\]

By exact cubic homogeneity,
\(H(\varepsilon,\lambda,T)=W_{[0,T]}[a^{\varepsilon,\lambda}]\).
The normalized fixed-point result and the trilinear continuity estimate thus
extend \(H\) as a \(C^1\) function to \(\varepsilon=0\), where

\[
 H(0,\lambda,T)
 =\int_0^T F(e^{\nu t\Delta}q_\lambda)\,dt.
 \tag{8.10}
\]

At \(\lambda=1\), the heat flow is even, so
\(H(0,1,T)=0\).  Moreover, (8.5) and time continuity imply

\[
 \frac1T\partial_\lambda H(0,1,T)
 \longrightarrow-3A\ne0
 \quad(T\downarrow0).
 \tag{8.11}
\]

At \(\lambda=1\), the identity
\(q_1=q^+-q^-=q^++q^+(-\cdot)\) also makes explicit that the heat datum is
even.  At \(t=0\), the two same-copy densities are nonzero and have disjoint
\(x\)-supports.  In fact

\[
 p_0:=\int\chi|w_\eta[\varphi_\ell*q_1]|\,dx
 =2\int\chi|w_\eta[\varphi_\ell*q^+]|\,dx\ge2|A|>0.
 \tag{8.12}
\]

For \(v_1(t)=e^{\nu t\Delta}q_1\), local \(C^1\) heat-flow continuity makes
\(p(t)=\int\chi|w_\eta[\varphi_\ell*v_1(t)]|\,dx\) continuous at zero.  Thus
\(P_{[0,T]}[v_1]>0\) for every sufficiently small \(T>0\).  Fix one \(T\)
for which both this property and the nonzero derivative hold.  The
implicit-function theorem produces \(\lambda(\varepsilon)\) with
\(H(\varepsilon,\lambda(\varepsilon),T)=0\).  Equation (2.6) then gives

\[
 P_I[u^\varepsilon]
 =\varepsilon^3P_I[a^{\varepsilon,\lambda(\varepsilon)}]
 \ge\frac12\varepsilon^3P_I[v_1]>0
 \tag{8.13}
\]

for sufficiently small positive \(\varepsilon\).  This proves (8.7).
\(\square\)

The exact tuning is an existence theorem, not a universal explicit formula
for \(\lambda(\varepsilon)\).  Its only purpose is to rule out the possibility
that the \(O(\varepsilon^4)\) signed remainder could rescue a reverse bound.

The scope boundary is essential.  The two-copy separation requires a cutoff
large enough to contain both copies while their selected annular interaction
regions remain disjoint.  It does **not** prove exact zero for every
prescribed Yu core cutoff \(\chi_k\), nor simultaneously for every
\(j\le k\).  Theorem 7.1 is a perturbative obstruction for one fixed generic
annular functional.  Its transfer, and exact implicit-function tuning, inside
the full separated Yu geometry remain **[U]**.  They are unnecessary for the
generic-class reverse-bound obstruction because (7.2) already makes the
signed ratio tend to zero.

## 9. Exact periodic total-production comparator

On \(\mathbb T^3\), let

\[
 B(x,y,z)=
 (\sin z+\cos y,\ \sin x+\cos z,\ \sin y+\cos x).
 \tag{9.1}
\]

Exact calculation gives

\[
 \nabla\cdot B=0,
 \qquad
 \nabla\times B=B,
 \qquad
 \Delta B=-B.
 \tag{9.2}
\]

Hence, for every amplitude \(a\),

\[
 u(t)=ae^{-\nu t}B,
 \qquad
 p(t)=-\frac12a^2e^{-2\nu t}|B|^2
 \tag{9.3}
\]

is an exact global smooth periodic Navier--Stokes solution.  With
\(h=\pi(1,1,1)\),

\[
 B(x+h)=-B(x).
 \tag{9.4}
\]

The total vortex-stretching density is cubic and translation covariant, hence

\[
 (\nabla\times u)\cdot S[u](\nabla\times u)(x+h,t)
 =-(\nabla\times u)\cdot S[u](\nabla\times u)(x,t),
 \qquad
 \int_{\mathbb T^3}(\nabla\times u)\cdot S[u](\nabla\times u)\,dx=0.
 \tag{9.5}
\]

The density is not identically zero: at the origin,

\[
 (\nabla\times B)\cdot S[B](\nabla\times B)=3.
 \tag{9.6}
\]

Thus the periodic full-domain **total-production** sign defect is strictly
positive and the signed total production is zero on every time interval.
This does not by itself identify a nonzero member of the R0.69T decomposition:
that identity was proved on \(\mathbb R^3\), not for a periodized Biot--Savart
kernel.  A shellwise torus corollary requires a separately defined,
convergent periodized pointwise reconstruction and remains **[U]**.

This comparator is stronger in time but belongs to the periodic domain and
concerns total production.  It is not substituted for Theorem 7.1 or for the
fixed-large-cutoff exact-tuning result in Theorem 8.1.

## 10. Exact certificate

The script `r070c_parity_audit.py` checks, with exact SymPy arithmetic,

1. the divergence, curl, heat eigenvalue, parity, stretching formula, and
   exact \(L^1/L^2\) values of the seed (6.1);
2. the Beltrami, heat, anti-translation, and nonzero-stretching identities
   for the ABC field;
3. the simple root of the normalized transversality polynomial
   \(1-\lambda^3\).

The certificate does not numerically prove Kato theory, smooth solution-map
dependence, the annular reconstruction, or the implicit-function theorem.
Those are human analytic steps in Sections 6--8.  The certificate prevents
the explicit parity and coefficient calculations from drifting.

The journal-oriented explanatory package is archived at
`figures/r070c-parity-obstruction/fig-r070c-parity-obstruction/`.  Panel A
plots the exact analytic heat-layer witness on \(z=y\); panel B plots only the
normalized asymptotic orders \(\varepsilon^3\) and \(\varepsilon^4\).  Its
caption, source data, validation record, vector outputs, and 600 dpi PNG are
retained together.  It is explicitly not DNS or trajectory evidence.

## 11. Claim--source ledger

| Claim used here | Evidence | Boundary |
|---|---|---|
| Local strong solutions and global small-data solutions in \(L^3\) | [Kato, *Math. Z.* 187 (1984)](https://doi.org/10.1007/BF01174182) | Published theorem; used only for smooth finite-energy data and sufficiently small amplitude |
| Conditional direction coherence can regularize 3D NSE | [Constantin--Fefferman, *IUMJ* 42 (1993)](https://iumj.org/article/3627/) | The coherence is an assumption, not derived here |
| Positive physical-scale flux is proved for ensemble averages under explicit scale assumptions | [Dascaliuc--Grujić, arXiv:1101.2193](https://arxiv.org/abs/1101.2193) and [arXiv:1107.0058](https://arxiv.org/abs/1107.0058) | These are sufficient conditions; no conversion from cover averages to \(L^1\) sign defect is claimed |
| Absolute and signed coarse-grained transfers have different cancellation content | [Eyink--Aluie, arXiv:0909.2386v1](https://arxiv.org/html/0909.2386v1) | Their numerical/phenomenological cancellation discussion is not used as proof |
| Exact Beltrami fields solve NSE; suitably localized Beltrami structures satisfying a nonlinear smallness condition can yield finite-energy global smooth solutions | [Ciampa--Lucà, JFA 287 (2024)](https://arxiv.org/html/2311.01369v3) | Localization is not itself exactly Beltrami; Theorem 8.1 instead uses ordinary Kato smallness |
| The filtered far-field framework majorizes a positive part and conditionally closes its reassigned annular portion | [Yu, arXiv:2606.27560v1](https://arxiv.org/html/2606.27560v1) | Commutator, localization, and exterior-tail budgets remain separate; the preprint's full proof is not independently certified here |
| Strict nonzero compact seed annulus | Local R0.69W certificate and `two_scale_annular_interval_note.md` | One declared smooth compact family and shell; no universal sign statement |
| Parity theorem, perturbative orders, fixed-large-cutoff exact tuning, and periodic total-production comparator | Sections 5--9 and `certificates/r070c/` | New project derivation; neither generic obstruction is asserted for every Yu core geometry and independent manuscript-level review is required before public theorem status |

## 12. Proof-gap matrix

| Proposed route | Status after R0.70C | Exact reason | Decision |
|---|---|---|---|
| NSE dynamics automatically makes \(D^{\mathrm{sign}}\) lower order | **[O] false** | The defect is already \(\Theta(\varepsilon^3)\) in the even linear heat layer | Stop |
| \(P_I\lesssim|W_I|\) on smooth trajectories | **[O] false** | Theorem 7.1 has \(|W_I|/P_I\to0\); Theorem 8.1 gives exact zero for a fixed large-cutoff member of the class | Stop |
| Exact two-copy tuning for every prescribed Yu \(\chi_k\) and \(j\le k\) | **[U]** | The required disjoint copies need not fit inside that core geometry | Do not claim |
| Homogeneous interpolation with a positive power of \(|W_I|\) | **[O] false for perturbatively regular factors** | Amplitude order improves the right side by \(\varepsilon^a\) | Stop |
| Independent additive positive cubic reservoir | **[P] possible but no gain** | It directly pays for \(P_I\) and reproduces the missing hypothesis | Do not present as depletion |
| Optimal-cover or direction-coherent sign selection | **[U] conditional** | Existing theorems control ensemble signed flux under added hypotheses, not absolute negative mass | Test next |
| Positive-time, large-data, pre-singular geometry excluding the parity family | **[U]** | Not touched by small-data counterexamples | Continue only with an explicit nondegeneracy mechanism |

## 13. Value, compute, and publication decision

The R0.70C result is a strict generic-route elimination stronger than
R0.70B's kinematic warning: the generic-functional reverse direction now
fails on genuine global smooth finite-energy Navier--Stokes trajectories.
Exact spacetime signed cancellation is additionally available for a fixed
large-cutoff member of the annular-functional class, but neither result is
promoted to every Yu core geometry.

Its value is methodological rather than a direct regularity advance.  It
shows that any successful annular closure must pay the sign defect at cubic
order or assume a mechanism that removes the parity family.  It does not
reduce a known regularity hypothesis.

- **DGX:** not justified.  The decisive gates are parity, cubic homogeneity,
  small-data perturbation theory, and a one-dimensional implicit-function
  argument.
- **Figure:** archive an analytic journal-style parity map and amplitude-order
  panel.  It is explanatory evidence, not part of the proof.
- **Independent review:** three read-only audits passed after corrections to
  the normalized fixed-point argument, cutoff geometry, periodic scope, and
  primary-source claims.
- **Public site:** the review gate is passed, so an R0.70C recap and its figure
  may be prepared on a draft branch/PR.  Do not merge it into the public site
  without the separate publication approval required by the project workflow.
- **Next gate (R0.70D):** determine whether physical-scale optimal-cover
  positivity can quantitatively control a coarse negative mass.  First test
  the abstract measure-theoretic implication; only then return to NSE.
