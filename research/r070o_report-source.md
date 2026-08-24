# R0.70O — Spectral rank strata and an exact filtered-to-unfiltered obstruction

**Status:** internal canonical research report; not a public theorem chapter

**Release:** R0.70O
**Date:** 2026-08-25

## 1. Result in one page

R0.70N proved that a finite nonnegative sum of scalar/componentwise filtered
vorticity covariances need not be positive definite.  R0.70O asks whether the
rank-deficient side can nevertheless be converted into an existing
two-component vorticity regularity criterion.

Let

\[
 Q(t)=\sum_{j\in J}w_j
 \int_{\mathbb T^3}\Omega_j(x,t)\otimes\Omega_j(x,t)\,dx,
 \qquad \Omega_j=T_j\omega,
 \tag{1.1}
\]

where the torus measure is normalized, \(w_j\geq0\), and every \(T_j\) is
the same scalar Fourier multiplier on all three target components.  Write

\[
 \lambda_1\geq\lambda_2\geq\lambda_3\geq0,
 \qquad E=\operatorname{tr}Q.
 \tag{1.2}
\]

The two small spectral quantities have different meanings:

\[
 \boxed{
 \lambda_3
 =\min_{|n|=1}\sum_jw_j\|n\cdot\Omega_j\|_2^2,}
 \tag{1.3}
\]

\[
 \boxed{
 \lambda_2+\lambda_3
 =\min_{|\ell|=1}\sum_jw_j
 \|P_{\ell^\perp}\Omega_j\|_2^2.}
 \tag{1.4}
\]

Thus small \(\lambda_3\) means near one plane and controls only one scalar
component.  Small \(\lambda_2+\lambda_3\) means near one line and controls
two transverse components.  Only the second quantity has the algebraic form
of the Chae--Choe and Miller vorticity criteria.

This observation gives an exact exhaustive spectral trichotomy.  Fix

\[
 0<2\delta<\eta<\frac12.
 \tag{1.5}
\]

At every point where \(E>0\), exactly one of the following holds:

\[
 \begin{array}{ll}
 \mathsf C_{\delta}:&\lambda_3/E\geq\delta,
 \quad\hbox{coercive};\\[2mm]
 \mathsf L_{\delta,\eta}:&\lambda_3/E<\delta
 \ \hbox{and}\ (\lambda_2+\lambda_3)/E\leq\eta,
 \quad\hbox{near a line};\\[2mm]
 \mathsf P_{\delta,\eta}:&\lambda_3/E<\delta
 \ \hbox{and}\ (\lambda_2+\lambda_3)/E>\eta,
 \quad\hbox{near a plane but not a line}.
 \end{array}
 \tag{1.6}
\]

The noncoercive branches retain the projector gaps

\[
 \mathsf L_{\delta,\eta}:\quad
 \lambda_1-\lambda_2\geq(1-2\eta)E,
 \tag{1.7}
\]

and

\[
 \mathsf P_{\delta,\eta}:\quad
 \lambda_2-\lambda_3>(\eta-2\delta)E.
 \tag{1.8}
\]

These gaps make the principal line or plane normal algebraically stable.
They do not control its spatial derivatives, because those derivatives also
contain \(\nabla Q\).

The main result is a sharp obstruction to the missing filtered-to-unfiltered
step.  Define the total filter response

\[
 A(k)=\sum_{j\in J}w_j|m_j(k)|^2.
 \tag{1.9}
\]

Assume \(A(e_2)>0\) and that integers \(N\to\infty\) can be chosen with
\(A(Ne_2)\to0\).  For any fixed \(\kappa>1\), set

\[
 a_N^2A(e_2)=1+\kappa N A(Ne_2)
 \tag{1.10}
\]

and consider

\[
 u_N(t,y)
 =a_Ne^{-\nu t}\sin y\,e_1
 +N^{-1/2}e^{-\nu N^2t}\sin(Ny)\,e_3.
 \tag{1.11}
\]

This is an exact smooth global unforced Navier--Stokes solution: it is
divergence free, its nonlinear term vanishes, and it solves the heat
equation.  Its vorticity is

\[
 \omega_N
 =N^{1/2}e^{-\nu N^2t}\cos(Ny)e_1
 -a_Ne^{-\nu t}\cos y\,e_3.
 \tag{1.12}
\]

The observed principal line is \(\operatorname{span}(e_3)\) at every
\(t\geq0\), while the observed best-line residual is

\[
 r_N(t)=\lambda_2(t)+\lambda_3(t)
 =\frac N2A(Ne_2)e^{-2\nu N^2t}.
 \tag{1.13}
\]

It satisfies the exact identity

\[
 \boxed{
 \|r_N\|_{L^2(0,\infty)}
 =\frac{A(Ne_2)}{4\sqrt\nu}\longrightarrow0.}
 \tag{1.14}
\]

In contrast, the unfiltered transverse vorticity has the fixed critical
norm

\[
 \boxed{
 \|P_{e_3^\perp}\omega_N\|_{L_t^4L_x^2}
 =\frac1{2\nu^{1/4}}.}
 \tag{1.15}
\]

The exponent pair is vorticity-critical because
\(2/4+3/2=2\).  By increasing \(\kappa\), the normalized covariance can be
kept in an arbitrarily narrow near-line cone, without changing (1.13)--(1.15).

Consequently, a finite blind or smoothing filter family admits no uniform
quantitative estimate that turns its absolute best-line residual into the
unfiltered critical two-component norm.  In particular, no modulus with
\(\Phi(0)=0\) and \(\Phi(s)\to0\) as \(s\downarrow0\) can make

\[
 \|P_{e_3^\perp}\omega\|_{L_t^4L_x^2}
 \leq \Phi\!\left(\|r\|_{L_t^2}\right)
 \tag{1.16}
\]

hold uniformly on this exact solution family.

For a finite compact-band family the obstruction is stronger.  An infinite
dyadic superposition gives an exact Leray--Hopf shear with \(r\equiv0\) but
\(P_{e_3^\perp}\omega\notin L_t^4L_x^2\) at the initial endpoint.  This
energy-class example does not satisfy the \(H^1\) initial hypothesis of the
Miller theorem and therefore does not contradict that theorem.

The precise positive replacement is also elementary.  For a fixed target
projection \(P\),

\[
 \sum_jw_j\|T_jP\omega\|_2^2
 =\sum_{k\in\mathbb Z^3}A(k)|P\widehat\omega(k)|^2.
 \tag{1.17}
\]

Uniform reconstruction of \(\|P\omega\|_2\) requires the all-frequency
lower frame

\[
 A(k)\geq a_0>0.
 \tag{1.18}
\]

Under (1.18), a common fixed projection and the absolute time condition
\(R_P\in L_t^2\),

\[
 \|P\omega\|_{L_t^4L_x^2}^4
 \leq a_0^{-2}\int R_P(t)^2\,dt.
 \tag{1.19}
\]

For a space-dependent principal direction, (1.19) acquires frequency
commutators.  Applying Miller additionally requires a spatially Lipschitz
unit direction.  Neither property follows from eigenvalue ratios.

The R0.70O decision is therefore narrow:

> The near-plane branch is algebraically too weak for known two-vorticity-
> component criteria.  The near-line branch has the right two-component
> algebra, but finite high-frequency-blind or smoothing scalar-filter
> families satisfying (7.1) cannot supply the unfiltered critical norm by a
> universal quantitative estimate.  A viable conditional bridge
> must add all-frequency coverage, absolute \(L_t^2\) residual control,
> a compatible principal direction, a spectral gap, spatial regularity of
> the covariance, and the resulting commutator ledger.

This is a no-go and requirements theorem.  It is not a new Navier--Stokes
regularity criterion, a blow-up construction, or a solution of the
Millennium problem.

## 2. Conventions and scope

### 2.1 Domain and Fourier normalization

The exact dynamic examples are posed on

\[
 \mathbb T^3=(\mathbb R/2\pi\mathbb Z)^3
 \tag{2.1}
\]

with normalized Haar measure.  Hence

\[
 \int_{\mathbb T^3}\cos^2(k\cdot x)\,dx
 =\int_{\mathbb T^3}\sin^2(k\cdot x)\,dx
 =\frac12
 \tag{2.2}
\]

for every nonzero integer frequency \(k\).

Each \(T_j\) is a translation-invariant scalar Fourier multiplier,

\[
 \widehat{T_jf}(k)=m_j(k)\widehat f(k),
 \tag{2.3}
\]

and acts componentwise on vector fields.  It is assumed to preserve real
fields, so \(m_j(-k)=\overline{m_j(k)}\).  The index set in the obstruction
theorem is finite, although the formula only needs
\(A(k)<\infty\) at the displayed frequencies.  The weights are fixed and
nonnegative.

The full-torus covariance is

\[
 Q(t)=\sum_jw_j\int_{\mathbb T^3}
 T_j\omega\otimes T_j\omega\,dx.
 \tag{2.4}
\]

The exact no-go does not cover component-mixing observations, adaptive
filters whose symbols depend on the solution, or nonlinear observables.
Those objects need new ledgers.

### 2.2 Abstract covariance representation

Several algebraic results use the more general representation

\[
 Q=\int_X V(\xi)\otimes V(\xi)\,d\mu(\xi),
 \qquad d\mu\geq0,
 \tag{2.5}
\]

where \(X\) may combine scales, positions, and times.  The assumptions are
only measurability and \(V\in L^2(d\mu;\mathbb R^3)\).  Then
\(Q=Q^{\mathsf T}\succeq0\).

### 2.3 Meaning of a bridge

Three logically different statements must not be conflated.

1. A **matrix identity** relates eigenvalues to filtered transverse energy.
2. A **reconstruction inequality** estimates an unfiltered norm from the
   observation family.
3. A **regularity theorem** inserts that norm into Navier--Stokes dynamics.

R0.70O proves the first, identifies exact hypotheses for a fixed-direction
version of the second, and disproves its universal quantitative version for
finite high-frequency-blind or smoothing frames satisfying (7.1).  It does
not prove the third.

## 3. Best-plane and best-line identities

### Theorem 3.1 — Exact variational meaning of the two residuals

Let \(Q\) be given by (2.5), with ordered eigenvalues as in (1.2).  Then

\[
 \lambda_3
 =\min_{|n|=1}\int_X|n\cdot V|^2\,d\mu,
 \tag{3.1}
\]

and

\[
 \lambda_2+\lambda_3
 =\min_{|\ell|=1}\int_X
 |P_{\ell^\perp}V|^2\,d\mu.
 \tag{3.2}
\]

If the relevant eigenvalue is simple, the minimizer in (3.1) is the
\(\lambda_3\) eigenline and the minimizer in (3.2) is the \(\lambda_1\)
eigenline.  With multiplicity, the set of minimizers is the corresponding
eigenspace.

#### Proof

For a unit vector \(n\),

\[
 \int_X|n\cdot V|^2\,d\mu=n^{\mathsf T}Qn.
 \tag{3.3}
\]

Rayleigh--Ritz gives (3.1).  For a unit vector \(\ell\),

\[
 \int_X|P_{\ell^\perp}V|^2\,d\mu
 =\operatorname{tr}Q-\ell^{\mathsf T}Q\ell.
 \tag{3.4}
\]

Maximizing the last quadratic form gives
\(\operatorname{tr}Q-\lambda_1=\lambda_2+\lambda_3\).  This proves (3.2).
\(\square\)

### Corollary 3.2 — One small eigenvalue is not a two-component criterion

For

\[
 Q_M=\operatorname{diag}(M,M,0),
 \tag{3.5}
\]

one has \(\lambda_3=0\), but

\[
 \lambda_2+\lambda_3=M.
 \tag{3.6}
\]

The plane residual can vanish while the best-line residual is arbitrarily
large.  This is the exact algebraic reason that the near-plane branch cannot
be inserted into a theorem controlling two transverse vorticity components.

### Corollary 3.3 — Ratios do not control absolute residuals

If \(Q\) is replaced by \(c^2Q\), then both residuals and the trace scale by
\(c^2\), whereas their ratios to \(E\) do not change.  Exact shear solutions
are closed under this amplitude scaling because their nonlinear term is
zero.  Hence a bound on

\[
 \frac{\lambda_2+\lambda_3}{E}
 \tag{3.7}
\]

alone cannot imply the absolute spacetime condition required by a
two-component regularity criterion.

## 4. An exhaustive coercive--near-plane--near-line trichotomy

### Theorem 4.1 — Spectral strata and quantitative gaps

Fix (1.5), and let \(Q\succeq0\) with \(E>0\).  The three sets in (1.6) are
disjoint and exhaustive.  Moreover, (1.7) holds in
\(\mathsf L_{\delta,\eta}\), and
(1.8) holds in \(\mathsf P_{\delta,\eta}\).

#### Proof

If \(\lambda_3/E\geq\delta\), the matrix is in
\(\mathsf C_\delta\), and it is excluded from the other two sets.  Otherwise,
exactly one of \((\lambda_2+\lambda_3)/E\leq\eta\) and its strict complement
holds.  This proves the partition.

In \(\mathsf L_{\delta,\eta}\),

\[
 \lambda_1-\lambda_2
 =E-(2\lambda_2+\lambda_3)
 \geq E-2(\lambda_2+\lambda_3)
 \geq(1-2\eta)E.
 \tag{4.1}
\]

In \(\mathsf P_{\delta,\eta}\),

\[
 \lambda_2
 =\lambda_2+\lambda_3-\lambda_3
 >(\eta-\delta)E,
 \tag{4.2}
\]

and therefore

\[
 \lambda_2-\lambda_3>(\eta-2\delta)E>0.
 \tag{4.3}
\]

\(\square\)

The trichotomy is a bookkeeping device, not a regularity theorem.  Its main
use is that the geometrically relevant projector is separated in each
noncoercive branch: \(P_1\) in the near-line branch and \(P_3\) in the
near-plane branch.

## 5. Exact eigenvalue and projector evolution

Assume on an open time interval that

\[
 \dot Q=\Sigma Q+Q\Sigma+F,
 \qquad
 Q=Q^{\mathsf T},\quad
 \Sigma=\Sigma^{\mathsf T},\quad
 F=F^{\mathsf T}.
 \tag{5.1}
\]

The matrix \(F\) contains all cutoff, diffusion, commutator, source-mismatch,
and moving-weight terms left after the chosen symmetric source \(\Sigma\)
is extracted.  R0.70N derived that PDE ledger.  No sign is imposed on
\(F\).

### Theorem 5.1 — Simple-spectrum ledger

Suppose \(Q\) is \(C^1\) and has a simple spectrum on the interval.  Choose
orthonormal eigenvectors \(e_a\), projectors
\(P_a=e_a\otimes e_a\), and the gauge
\(e_a^{\mathsf T}\dot e_a=0\).  Set

\[
 \sigma_{ab}=e_a^{\mathsf T}\Sigma e_b,
 \qquad f_{ab}=e_a^{\mathsf T}Fe_b.
 \tag{5.2}
\]

Then

\[
 \boxed{
 \dot\lambda_a=2\lambda_a\sigma_{aa}+f_{aa}.}
 \tag{5.3}
\]

For \(b\neq a\),

\[
 \boxed{
 e_b^{\mathsf T}\dot e_a
 =\frac{(\lambda_a+\lambda_b)\sigma_{ba}+f_{ba}}
 {\lambda_a-\lambda_b}.}
 \tag{5.4}
\]

Equivalently,

\[
 \boxed{
 \dot P_a
 =\sum_{b\neq a}
 \frac{
 (\lambda_a+\lambda_b)(P_b\Sigma P_a+P_a\Sigma P_b)
 +P_bFP_a+P_aFP_b}
 {\lambda_a-\lambda_b}.}
 \tag{5.5}
\]

#### Proof

Differentiate \(Qe_a=\lambda_ae_a\).  Pairing with \(e_a\) gives
\(\dot\lambda_a=e_a^{\mathsf T}\dot Qe_a\), hence (5.3).  Pairing with
\(e_b\), \(b\neq a\), gives

\[
 (\lambda_a-\lambda_b)e_b^{\mathsf T}\dot e_a
 =e_b^{\mathsf T}\dot Qe_a.
 \tag{5.6}
\]

Substitution of (5.1) proves (5.4).  Differentiating
\(P_a=e_a\otimes e_a\) and summing the transverse components proves (5.5).
\(\square\)

### 5.2 Trace and normalized residuals

The total observed energy obeys

\[
 \dot E
 =2\operatorname{tr}(\Sigma Q)+\operatorname{tr}F
 =2\sum_{a=1}^3\lambda_a\sigma_{aa}
 +\operatorname{tr}F.
 \tag{5.7}
\]

The two absolute residual ledgers are

\[
 \dot\lambda_3=2\lambda_3\sigma_{33}+f_{33},
 \tag{5.8}
\]

and

\[
 \frac d{dt}(\lambda_2+\lambda_3)
 =2\lambda_2\sigma_{22}+2\lambda_3\sigma_{33}
 +f_{22}+f_{33}.
 \tag{5.9}
\]

For \(E>0\), define

\[
 g_P=\frac{\lambda_3}{E},
 \qquad
 g_L=\frac{\lambda_2+\lambda_3}{E}.
 \tag{5.10}
\]

Their exact derivatives are

\[
 \dot g_P
 =\frac{E(2\lambda_3\sigma_{33}+f_{33})
 -\lambda_3\dot E}{E^2},
 \tag{5.11}
\]

\[
 \dot g_L
 =\frac{E(2\lambda_2\sigma_{22}+2\lambda_3\sigma_{33}
 +f_{22}+f_{33})-(\lambda_2+\lambda_3)\dot E}{E^2}.
 \tag{5.12}
\]

There is no sign in either formula without a new estimate on \(F\).

### 5.3 Rank-boundary tangent condition

If \(Q(t)\succeq0\) on an open interval and a simple
\(\lambda_3(t_0)=0\) occurs at an interior time, then \(\lambda_3\) has a
local minimum and

\[
 \dot\lambda_3(t_0)=0,
 \qquad f_{33}(t_0)=0.
 \tag{5.13}
\]

At an initial endpoint only the one-sided condition

\[
 \dot\lambda_3(t_0^+)\geq0,
 \qquad f_{33}(t_0^+)\geq0
 \tag{5.14}
\]

follows.  Positive semidefiniteness therefore constrains the tangent at rank
loss, but supplies no strictly positive inward speed.

### 5.4 Collisions and cluster projectors

Individual formulas (5.4)--(5.5) are invalid when their denominators vanish.
At a collision, an individual eigenvector need not be differentiable.  A
projector onto a spectral cluster remains differentiable only while that
cluster is separated from the complementary spectrum.  This distinction is
essential: the near-line gap controls \(P_1\), whereas the near-plane gap
controls \(P_3\).

## 6. Spatial direction regularity is a separate estimate

Let \(Q=Q(x,t)\) be differentiable in space with a simple principal
eigenvalue.  Replacing \(\dot Q\) by \(\partial_iQ\) in standard projector
perturbation gives

\[
 \partial_iP_1
 =\sum_{b=2}^3
 \frac{P_b(\partial_iQ)P_1+P_1(\partial_iQ)P_b}
 {\lambda_1-\lambda_b}.
 \tag{6.1}
\]

Consequently,

\[
 \|\partial_iP_1\|_F
 \leq
 \frac{\|\partial_iQ\|_F}{\lambda_1-\lambda_2}.
 \tag{6.2}
\]

In the near-line stratum,

\[
 \|\partial_iP_1\|_F
 \leq
 \frac{\|\partial_iQ\|_F}{(1-2\eta)E}.
 \tag{6.3}
\]

This is useful only if \(|\nabla Q|/E\) is controlled.  An eigenvalue ratio
does not provide that control.  A matrix curve

\[
 Q(t)=R(t)\operatorname{diag}(1,\varepsilon,\varepsilon^2)R(t)^{\mathsf T}
 \tag{6.4}
\]

can retain its spectrum while its projectors rotate arbitrarily fast.  This
matrix example is not asserted to be a Navier--Stokes covariance.

For a unit lift \(v\) of the principal line,
\(P_1=v\otimes v\) and \(v\cdot\partial_iv=0\), so

\[
 \|\partial_iP_1\|_F=\sqrt2\,|\partial_iv|.
 \tag{6.5}
\]

On a contractible spatial domain a continuous simple eigenline admits a
continuous orientation.  On a general domain, orientability is an additional
global issue.  Since covariance determines only \(v\otimes v\), sign choices
must be handled before applying a theorem stated for a vector field \(v\).

## 7. Exact smooth dynamic obstruction

### Theorem 7.1 — Finite smoothing frames do not control the critical transverse norm

Let \(T_1,\ldots,T_J\) satisfy Section 2.1, let \(w_j\geq0\), and define
\(A\) by (1.9).  Assume

\[
 A(e_2)>0,
 \qquad A(N_qe_2)\longrightarrow0
 \tag{7.1}
\]

along integers \(N_q\to\infty\).  Fix \(\kappa>1\), define \(a_N\) by
(1.10), and let \(u_N\) be (1.11).  After discarding finitely many terms,
assume \(N_q\geq2\); every \(N\) below belongs to that subsequence.  Then:

1. \(u_N\) is a smooth global unforced Navier--Stokes solution;
2. \(e_3\) is the unique principal eigenline of \(Q_N(t)\) for every
   \(t\geq0\);
3. the best-line residual and unfiltered transverse norm satisfy
   (1.13)--(1.15);
4. the normalized line residual obeys

   \[
   \frac{\lambda_2+\lambda_3}{E}
   <\frac1{\kappa+1}
   \qquad(t\geq0).
   \tag{7.2}
   \]

#### Proof

The field depends only on \(y\), has components only in \(e_1,e_3\), and
has no \(e_2\) component.  Therefore

\[
 \nabla\cdot u_N=0,
 \qquad
 (u_N\cdot\nabla)u_N=0,
 \qquad
 \partial_tu_N=\nu\Delta u_N.
 \tag{7.3}
\]

Taking the curl gives (1.12).  Fourier orthogonality and (2.2) give

\[
 Q_N(t)
 =\frac N2A(Ne_2)e^{-2\nu N^2t}e_1\otimes e_1
 +\frac{a_N^2}{2}A(e_2)e^{-2\nu t}e_3\otimes e_3.
 \tag{7.4}
\]

Write \(x_N=NA(Ne_2)\).  The two nonzero diagonal entries are

\[
 q_\perp(t)=\frac{x_N}{2}e^{-2\nu N^2t},
 \qquad
 q_\parallel(t)=\frac{1+\kappa x_N}{2}e^{-2\nu t}.
 \tag{7.5}
\]

Since \(N\geq2\), \(\kappa>1\), and
\(e^{-2\nu N^2t}\leq e^{-2\nu t}\), one has
\(q_\parallel>q_\perp\).  Thus

\[
 \lambda_1=q_\parallel,
 \qquad \lambda_2=q_\perp,
 \qquad \lambda_3=0.
 \tag{7.6}
\]

This proves (1.13).  Direct integration gives

\[
 \int_0^\infty r_N(t)^2\,dt
 =\frac{N^2A(Ne_2)^2}{4}
 \int_0^\infty e^{-4\nu N^2t}\,dt
 =\frac{A(Ne_2)^2}{16\nu},
 \tag{7.7}
\]

which proves (1.14).  Also,

\[
 \|P_{e_3^\perp}\omega_N(t)\|_2^2
 =\frac N2e^{-2\nu N^2t},
 \tag{7.8}
\]

and hence

\[
 \int_0^\infty
 \|P_{e_3^\perp}\omega_N(t)\|_2^4\,dt
 =\frac1{16\nu}.
 \tag{7.9}
\]

Finally,

\[
 \frac{q_\perp}{q_\parallel+q_\perp}
 \leq
 \frac{x_N}{1+(\kappa+1)x_N}
 <\frac1{\kappa+1}.
 \tag{7.10}
\]

\(\square\)

### Corollary 7.2 — Exact finite-horizon instability constant

For every fixed \(T>0\), set

\[
 \theta_{N,T}=1-e^{-4\nu N^2T}.
 \tag{7.11}
\]

The same exact integrations on \((0,T)\) give

\[
 \|r_N\|_{L^2(0,T)}
 =\frac{A(Ne_2)}{4\sqrt\nu}\sqrt{\theta_{N,T}},
 \tag{7.12}
\]

and

\[
 \|P_{e_3^\perp}\omega_N\|_{L^4(0,T;L^2)}^2
 =\frac1{4\sqrt\nu}\sqrt{\theta_{N,T}}.
 \tag{7.13}
\]

Whenever \(A(Ne_2)>0\), the exact instability ratio is therefore

\[
 \boxed{
 \frac{
 \|P_{e_3^\perp}\omega_N\|_{L^4(0,T;L^2)}^2}
 {\|r_N\|_{L^2(0,T)}}
 =\frac1{A(Ne_2)}.}
 \tag{7.14}
\]

Thus any homogeneous reconstruction constant must deteriorate at least as
the reciprocal high-frequency response.  This finite-horizon identity is
stronger than merely observing two different limits.

### Corollary 7.3 — No uniform modulus of finite-filter reconstruction

Under Theorem 7.1, no function \(\Phi:[0,\infty)\to[0,\infty)\) with
\(\Phi(0)=0\) and \(\Phi(s)\to0\) as \(s\downarrow0\) can make (1.16) hold
for every member of the solution family.  Equivalently, no reconstruction
modulus continuous at zero exists.  The explicit value at zero is needed
when a compact-band response vanishes exactly.

This is a quantitative observability obstruction.  It does not rule out a
regularity theorem that uses additional unfiltered energy, a resolution
condition tied to viscosity, all frequency scales, or a Navier--Stokes
assimilation mechanism.

The family concentrates its obstruction in an initial layer of width
\(N^{-2}\).  On a fixed delayed interval \([\tau,\infty)\), \(\tau>0\), its
unfiltered high-frequency term tends to zero.  The displayed sequence does
not disprove a delayed-time estimate with constants allowed to depend on
\(\tau\).  Any use near a candidate terminal time would need a separately
justified time translation or rescaling argument.

### Corollary 7.4 — Bounded low-mode amplitude for standard rapid decay

If, in addition,

\[
 \sup_q N_qA(N_qe_2)<\infty,
 \tag{7.15}
\]

then \(a_{N_q}\) remains bounded.  This includes compact-band families and
many standard smoothing multipliers with more than one-half derivative of
high-frequency decay in amplitude.  The obstruction then holds without a
growing observed low mode.

## 8. Exact energy-class blind-zone obstruction

The smooth family proves failure of every uniform quantitative estimate.
For compact spectral support, the corresponding qualitative membership
failure can also be seen at the initial endpoint.

### Theorem 8.1 — A finite compact-band frame can miss an infinite critical transverse norm

Assume \(A(e_2)>0\) and there is \(K<\infty\) such that

\[
 A(ne_2)=0\qquad(n>K).
 \tag{8.1}
\]

Choose \(a\neq0\) and \(k_0\) so \(n_k=2^k>K\) for all
\(k\geq k_0\), and define

\[
 u_\infty(t,y)
 =a e^{-\nu t}\sin y\,e_1
 +\sum_{k=k_0}^\infty
 n_k^{-1/2}e^{-\nu n_k^2t}\sin(n_ky)\,e_3.
 \tag{8.2}
\]

Then \(u_\infty\) is an exact Leray--Hopf solution, smooth for every
\(t>0\), and

\[
 \|u_\infty(0)\|_2^2
 =\frac{a^2}{2}+\frac12\sum_{k=k_0}^\infty\frac1{n_k}<\infty.
 \tag{8.3}
\]

Every high transverse mode is in the observation kernel.  Thus the observed
covariance is rank one in \(e_3\), and

\[
 r(t)=\lambda_2(t)+\lambda_3(t)=0.
 \tag{8.4}
\]

However,

\[
 \|P_{e_3^\perp}\omega_\infty(t)\|_2^2
 =\frac12\sum_{k=k_0}^\infty
 n_ke^{-2\nu n_k^2t}.
 \tag{8.5}
\]

Tonelli's theorem gives

\[
 \begin{aligned}
 \int_0^\infty
 \|P_{e_3^\perp}\omega_\infty(t)\|_2^4\,dt
 &=\frac1{8\nu}
 \sum_{k,l\geq k_0}
 \frac{n_kn_l}{n_k^2+n_l^2}\\
 &\geq\frac1{16\nu}\sum_{k\geq k_0}1
 =\infty.
 \end{aligned}
 \tag{8.6}
\]

The nonlinear term still vanishes because every component depends only on
\(y\) and there is no \(e_2\) velocity.  The energy inequality follows by
the heat semigroup and Parseval.  This proves the theorem.

The divergence in (8.6) occurs at \(t=0\).  The initial datum is in \(L^2\)
but not \(H^1\).  The example therefore does not contradict Chae--Choe,
Miller, or smooth positive-time regularity.  Its role is to prove that a
finite compact-band covariance has no qualitative reconstruction property
at the Leray energy level.

## 9. Exact lower-frame replacement

### Theorem 9.1 — Necessary and sufficient scalar Fourier coverage

Let \(P\) be a fixed orthogonal target-space projection, and define

\[
 R_P(f)=\sum_jw_j\|T_jPf\|_2^2.
 \tag{9.1}
\]

Then Parseval gives

\[
 R_P(f)=\sum_{k\in\mathbb Z^3}A(k)|P\widehat f(k)|^2.
 \tag{9.2}
\]

For a prescribed frequency set \(\Lambda\), the inequality

\[
 a_0\|Pf\|_2^2\leq R_P(f)
 \tag{9.3}
\]

for every \(f\) supported in \(\Lambda\) is equivalent to

\[
 A(k)\geq a_0
 \qquad(k\in\Lambda)
 \tag{9.4}
\]

on every frequency where the range of \(P\) contains an admissible Fourier
coefficient.  Sufficiency follows term by term from (9.2); necessity follows
by testing one Fourier mode.

Similarly,

\[
 a_0\|Pf\|_{\dot H^{-1/2}}^2\leq R_P(f)
 \tag{9.5}
\]

for all mean-zero \(f\) is equivalent to

\[
 A(k)\geq a_0|k|^{-1}
 \qquad(k\neq0)
 \tag{9.6}
\]

on the admissible frequencies.

Finite adjacent compact LP scales fail (9.4) and (9.6).  A complete LP
square function can satisfy an all-frequency analogue.  These are coverage
facts, not consequences of Navier--Stokes evolution.

### Corollary 9.2 — Fixed-direction bridge to the Miller critical norm

Assume (9.4) on all nonzero frequencies and let \(P\) be fixed in space and
time.  If

\[
 R_P(t)=\sum_jw_j\|T_jP\omega(t)\|_2^2
 \in L^2(0,T),
 \tag{9.7}
\]

then

\[
 \boxed{
 \|P\omega\|_{L^4(0,T;L^2)}^4
 \leq a_0^{-2}\|R_P\|_{L^2(0,T)}^2.}
 \tag{9.8}
\]

If \(P=P_{v^\perp}\) for one fixed unit vector \(v\), the left side is
\(\|v\times\omega\|_{L_t^4L_x^2}^4\).  This is the exact linear bridge, but
its all-frequency lower frame and absolute time integrability are added
hypotheses.

## 10. Why a variable principal line needs a new commutator ledger

Let \(v=v(x,t)\) and \(P=P_{v^\perp}\).  Scalar filters no longer commute
with multiplication by \(P\):

\[
 T_j(P\omega)=P\,T_j\omega+[T_j,P]\omega.
 \tag{10.1}
\]

Therefore a covariance built from \(P\,T_j\omega\) does not directly equal
the square function of \(P\omega\).  A valid bridge needs estimates for

\[
 [T_j,P]\omega,
 \tag{10.2}
\]

uniformly across all participating scales.  Such estimates normally involve
spatial regularity of \(P\), hence of \(Q\) divided by its spectral gap.

For the near-line principal projector, the minimal analytic ledger contains:

1. an all-frequency lower frame or a dynamically justified finite-resolution
   replacement;
2. the absolute residual \(R_P\), not only \(R_P/E\);
3. \(R_P\in L_t^2\), to match the \(L_t^4L_x^2\) criterion;
4. a common line across scales and overlapping spatial windows;
5. a lower bound for \(\lambda_1-\lambda_2\);
6. a bound for \(|\nabla Q|/E\), giving spatial control of \(P\);
7. orientation or a projector-form version of the desired regularity theorem;
8. the commutator/paraproduct terms generated by (10.1).

The eigenvalue identities provide items 2 and 5 only after they are assumed
or estimated.  They do not supply the remaining items.

## 11. Exact smooth near-plane initial-face witness

The near-plane branch is not rescued by hidden high frequencies.  A direct
smooth datum separates the observed plane from an unobserved normal mode.
Let

\[
 u_{0,N}
 =a(e_3\sin x_2+e_1\sin x_3)
 +b_NN^{-1}e_2\sin(Nx_1).
 \tag{11.1}
\]

Then

\[
 \nabla\cdot u_{0,N}=0
 \tag{11.2}
\]

and

\[
 \omega_{0,N}
 =a\cos x_2\,e_1+a\cos x_3\,e_2
 +b_N\cos(Nx_1)\,e_3.
 \tag{11.3}
\]

A finite low-frequency family can see the \(e_1,e_2\) plane and miss the
high normal mode.  Choosing \(b_N=N^{1/2}\) keeps that high normal vorticity
at fixed \(\dot H^{-1/2}\) size.  This is an exact initial-face calibration.
Its nonlinear cross terms generally do not vanish, so no positive-time exact
trajectory is claimed for (11.1).

## 12. Literature collision boundary

The separate bounded primary-literature audit records the exact hypotheses.
The three closest regularity mechanisms are:

1. **Chae--Choe (1999):** two unfiltered vorticity components relative to
   one fixed global direction in the critical family
   \(L_t^\alpha L_x^\gamma\),
   \(2/\alpha+3/\gamma\leq2\), \(\gamma>3/2\), with a small endpoint.
2. **Miller (2021):** \(v(x,t)\times\omega\in L_t^4L_x^2\), with a bounded
   unit direction field whose spatial gradient is locally uniformly bounded.
3. **Constantin--Fefferman (1993):** pointwise pairwise coherence of the
   unfiltered vorticity direction on the high-vorticity set.

The R0.70O covariance residual supplies none of these hypotheses without a
bridge.  The exact no-go shows that finite high-frequency-blind or smoothing
scalar frequency observations satisfying (7.1) cannot supply the first two
by a universal reconstruction inequality.
Average covariance also cannot imply the pointwise pairwise coherence in the
third result without a separate all-radius Campanato/Morrey-type estimate.

The bounded search found frequency-localized and finite-observation
regularity theorems, but those retain absolute amplitudes, viscosity-dependent
resolution conditions, high-frequency limits, or a data-assimilation
mechanism.  They do not prove a covariance-eigenvalue lift.

## 13. What R0.70O closes and what remains open

### 13.1 Closed in this release

1. The exact geometric meaning of \(\lambda_3\) and
   \(\lambda_2+\lambda_3\).
2. An exhaustive coercive--near-plane--near-line partition with the correct
   projector gaps.
3. The eigenvalue, eigenvector, projector, trace, and normalized-residual
   ledgers for \(\dot Q=\Sigma Q+Q\Sigma+F\).
4. A smooth exact NSE family disproving uniform quantitative reconstruction
   from a finite smoothing frame.
5. An energy-class exact compact-band shear disproving qualitative
   reconstruction at the initial endpoint.
6. The necessary and sufficient all-frequency lower-frame condition for the
   fixed-projection linear bridge.
7. The precise additional direction and commutator requirements for a
   variable-principal-line route.

### 13.2 Not proved

R0.70O does not prove:

- that near-plane vorticity is regularizing;
- that a near-line covariance ratio is a continuation criterion;
- a bound on the NSE forcing matrix \(F\);
- a uniform spatial bound on \(\nabla Q/E\);
- a variable-direction all-scale commutator theorem;
- a new version of the Chae--Choe, Miller, or Constantin--Fefferman criteria;
- finite-time blow-up or global smoothness.

### 13.3 Next acceptance gate

The only branch still structurally aligned with an existing regularity
criterion is near-line.  A next release should not start with DNS.  It should
first test the following conditional theorem target:

> Given an all-frequency scalar frame, a spatially compatible local
> covariance field with a uniform principal gap, an absolute best-line
> residual in \(L_t^2\), and a scale-summable bound for
> \([T_j,P_{v^\perp}]\omega\), prove that the unfiltered transverse vorticity
> lies in \(L_t^4L_x^2\).

If that bridge closes with hypotheses that can plausibly be propagated by
the covariance PDE ledger, a periodic analogue of Miller's theorem must
first be cited or proved; alternatively, the bridge must be rebuilt on
\(\mathbb R^3\), the domain of Miller's stated theorem.  Only then does that
criterion become a legitimate downstream consumer.  If the commutator or
spatial-direction hypotheses merely restate the critical norm, the route
should be closed rather than simulated.

## 14. Reproducibility boundary

The accompanying exact producer checks:

1. a rational simple-spectrum sample of (5.3)--(5.5);
2. trace and normalized-residual derivatives;
3. homogeneous sum-of-squares certificates for (3.1)--(3.2);
4. rational samples of all three spectral strata and their gap bounds;
5. divergence, curl, heat evolution, and vanishing nonlinearity for (1.11);
6. the exact covariance entries, time norms, and normalized near-line bound;
7. finite compact-band dyadic lower bounds growing linearly with the number
   of hidden modes;
8. finite lower-frame and blind-frequency calibrations.

The producer does not computer-prove Rayleigh--Ritz for arbitrary measures,
the infinite-series Tonelli argument, or the operator theorem for arbitrary
filter symbols.  Those proofs are analytical and are written above.
