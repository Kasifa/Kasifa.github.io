# R0.70N — Exact failure of universal scalar multi-scale vorticity frames

**Status:** internal canonical research report; not a public theorem chapter
**Release:** R0.70N
**Date:** 2026-08-25

## 1. Result in one page

R0.70M isolated one possible way to keep the affine-relative covariance
estimate away from its singular boundary.  At adjacent filter scales \(j\),
form

\[
 Q_j(t)=\int\chi_j(x,t)
 \Omega_j(x,t)\otimes\Omega_j(x,t)\,dx,
 \qquad \Omega_j=P_j\omega,
 \tag{1.1}
\]

and replace one possibly singular \(Q_k\) by the nonnegative sum

\[
 \mathcal Q_k=\sum_{j\in J_k}w_{k,j}Q_j,
 \qquad w_{k,j}\ge0.
 \tag{1.2}
\]

The proposed gate was a universal frame lower bound

\[
 \boxed{
 \mathcal Q_k\succeq
 c\,\operatorname{tr}(\mathcal Q_k)I,
 \qquad c>0,}
 \tag{1.3}
\]

with \(c\) controlled from Navier--Stokes quantities rather than assumed as
an independent nondegeneracy hypothesis.

R0.70N closes this universal route.  The obstruction is exact and occurs
before any estimate or numerical simulation.

For every \(v\in\mathbb R^3\),

\[
 v^{\mathsf T}\mathcal Q_kv
 =\sum_{j\in J_k}w_{k,j}
 \int\chi_j|v\cdot\Omega_j|^2\,dx.
 \tag{1.4}
\]

Consequently, when the trace is positive, the largest possible constant in
(1.3) is

\[
 \boxed{
 c_*(k,t)
 =\frac{\lambda_{\min}(\mathcal Q_k)}
 {\operatorname{tr}\mathcal Q_k}
 =\inf_{|v|=1}
 \frac{
 \sum_jw_{k,j}\int\chi_j|v\cdot\Omega_j|^2dx
 }{
 \sum_jw_{k,j}\int\chi_j|\Omega_j|^2dx
 }.}
 \tag{1.5}
\]

Thus (1.3) is not an enstrophy lower bound.  It is a quantitative angular
spanning condition in all three target-space directions.  Trace or energy
information controls only the denominator in (1.5).

The key structural lemma is the following.  If, at every observed time and
throughout the full spatial input domain of each nonlocal filter,

\[
 \omega(x,t)\in V\subsetneq\mathbb R^3
 \tag{1.6}
\]

for one fixed proper subspace \(V\), then every linear filter that acts by the
same scalar spatial operator on all three components preserves \(V\).  Hence

\[
 \operatorname{Ran}Q_j\subset V,
 \qquad
 \operatorname{Ran}\mathcal Q_k\subset V.
 \tag{1.7}
\]

No number of scales, centers, nonnegative weights, or nonnegative time
averages can remove the common nullspace \(V^\perp\).

Two smooth unforced periodic Navier--Stokes solutions make the obstruction
explicit.  The heat shear

\[
 u_s(x,t)=A e^{-\nu N^2t}\sin(Ny)e_1
 \tag{1.8}
\]

has

\[
 \omega_s=-ANe^{-\nu N^2t}\cos(Ny)e_3.
 \tag{1.9}
\]

Every nonzero \(Q_j\), with any nonnegative cutoff, is a multiple of
\(e_3\otimes e_3\).  Therefore every nonzero multi-scale sum is rank one and

\[
 c_*(k,t)=0.
 \tag{1.10}
\]

The helical wave

\[
 u_b(x,t)=A e^{-\nu N^2t}
 \bigl(\cos(Nz),-\sin(Nz),0\bigr)
 \tag{1.11}
\]

satisfies

\[
 \omega_b=Nu_b.
 \tag{1.12}
\]

Its vorticity direction rotates with \(z\), but remains in \(e_3^\perp\).
Every scalar-filter covariance has the common null direction \(e_3\).  For
the normalized full-torus measure,

\[
 Q_j
 =\frac{A^2N^2e^{-2\nu N^2t}|m_j(Ne_3)|^2}{2}
 \operatorname{diag}(1,1,0).
 \tag{1.13}
\]

This is rank two, not positive definite.  Spatial rotation within a plane,
and even the Beltrami relation, do not supply a three-dimensional frame.

The exact multi-scale evolution also has no hidden cancellation.  If each
scale uses a source \(\Sigma_j\) and a common pullback uses \(\Sigma_*\), then
the aggregate residual contains

\[
 \sum_jw_{k,j}
 \left[(\Sigma_j-\Sigma_*)Q_j
 +Q_j(\Sigma_j-\Sigma_*)\right].
 \tag{1.14}
\]

Time-dependent weights add \(\sum_j\dot w_{k,j}Q_j\).  A time-window Gramian
adds the analogous history-source mismatch.  Directional enrichment is not
free at the level of the exact PDE ledger.

The conclusion is deliberately narrow:

> For scalar/componentwise filters and nonnegative scale, center, or time
> weights, no universal positive multi-scale vorticity-frame constant exists
> for all smooth periodic Navier--Stokes solutions.  Exact shear and Beltrami
> solutions preserve a common proper target-space subspace.  Multi-scale
> summation therefore cannot, by itself, make the affine inverse-covariance
> route universal.

This does not exclude a conditional frame hypothesis, a theorem for a
restricted genuinely three-dimensional solution class, or a different
observable with a newly derived evolution law.  It does not prove that
near-planar vorticity is regularizing, global smoothness, finite-time blow-up,
or the Millennium problem.

## 2. Conventions and exact scope

The principal counterexamples are posed on the flat torus
\(\mathbb T^3=(\mathbb R/2\pi\mathbb Z)^3\), with Haar measure normalized so
that

\[
 \int_{\mathbb T^3}1\,dx=1.
 \tag{2.1}
\]

This removes irrelevant volume constants.  Section 11 records an
initial-face finite-energy boundary on \(\mathbb R^3\).

Let \(P_j\) be a linear scalar/componentwise spatial filter:

\[
 P_j(f_1,f_2,f_3)
 =(T_jf_1,T_jf_2,T_jf_3),
 \tag{2.2}
\]

where the same scalar linear operator \(T_j\) acts on every component.  The
standard convolution filters and scalar Fourier multipliers used in the
preceding releases have this form.  For the complete filtered Navier--Stokes
ledger, \(P_j\) is also assumed smooth and to commute with spatial
derivatives.  The algebraic range lemma needs only (2.2).

Set

\[
 U_j=P_ju,
 \qquad
 \Omega_j=\nabla\times U_j=P_j\omega.
 \tag{2.3}
\]

Let \(0\le\chi_j\in C^\infty\) be either a compactly supported cutoff or a
smooth nonnegative weight for which every displayed integral and integration
by parts is justified.  This includes \(\chi_j\equiv1\) on the torus and,
for sufficiently decaying fields, on \(\mathbb R^3\).  Define \(Q_j\) by
(1.1).  Then

\[
 Q_j=Q_j^{\mathsf T}\succeq0,
 \qquad
 \operatorname{tr}Q_j=\int\chi_j|\Omega_j|^2dx.
 \tag{2.4}
\]

The index set \(J_k\) may be finite or countable.  In the countable case the
assumption is

\[
 \sum_{j\in J_k}w_{k,j}\operatorname{tr}Q_j<\infty,
 \qquad w_{k,j}\ge0,
 \tag{2.5}
\]

so that the positive-semidefinite sum converges in trace norm.  Unless a
time derivative is taken, the weights may depend on the solution, scale,
center, and time.  When differentiated, their derivatives are retained
explicitly.

The no-go theorem does **not** cover component-mixing observations such as
\(R_jP_j\omega\) with different rotations \(R_j\), nonlinear filters, or a
Gramian augmented by strain, pressure, or transported directions.  Those
objects have different evolution ledgers and are addressed only as open
variants in Section 12.

## 3. Exact per-scale and aggregate covariance ledger

For a smooth incompressible Navier--Stokes solution, the \(j\)-filtered
vorticity equation is

\[
 \partial_t\Omega_{j,i}+U_{j,a}\partial_a\Omega_{j,i}
 =\Omega_{j,a}\partial_aU_{j,i}
 +\nu\Delta\Omega_{j,i}
 +\partial_a C^{(j)}_{ai},
 \tag{3.1}
\]

where

\[
 C^{(j)}_{ai}
 =\bigl[P_j(\omega_a u_i)-\Omega_{j,a}U_{j,i}\bigr]
 -\bigl[P_j(u_a\omega_i)-U_{j,a}\Omega_{j,i}\bigr].
 \tag{3.2}
\]

Because the antisymmetric part of \(\nabla U_j\) annihilates
\(\Omega_j=\nabla\times U_j\), the exact covariance equation is

\[
 \dot Q_j
 =F_{\chi,j}+F_{S,j}+F_{\nu,j}+F_{C,j},
 \tag{3.3}
\]

with

\[
 F_{\chi,j}
 =\int a_{\chi,j}\,\Omega_j\otimes\Omega_j\,dx,
 \tag{3.4}
\]

\[
 a_{\chi,j}
 =\partial_t\chi_j+U_j\cdot\nabla\chi_j+\nu\Delta\chi_j,
 \tag{3.5}
\]

\[
 F_{S,j}
 =\int\chi_j\left[
 (S(U_j)\Omega_j)\otimes\Omega_j
 +\Omega_j\otimes(S(U_j)\Omega_j)
 \right]dx,
 \tag{3.6}
\]

\[
 F_{\nu,j}
 =-2\nu\int\chi_j\sum_a
 \partial_a\Omega_j\otimes\partial_a\Omega_j\,dx,
 \tag{3.7}
\]

and

\[
 (F_{C,j})_{pq}
 =-\int\left[
 C^{(j)}_{ap}\partial_a(\chi_j\Omega_{j,q})
 +C^{(j)}_{aq}\partial_a(\chi_j\Omega_{j,p})
 \right]dx.
 \tag{3.8}
\]

Choose one spatially constant reference strain

\[
 \Sigma_*(t)\in\operatorname{Sym}_0(3)
 \tag{3.9}
\]

for the entire scale window and write

\[
 S(U_j)=\Sigma_*+\widetilde S_{j|*}.
 \tag{3.10}
\]

Then

\[
 \dot Q_j
 =\Sigma_*Q_j+Q_j\Sigma_*+F_{j|*},
 \tag{3.11}
\]

where

\[
 F_{j|*}
 =F_{\chi,j}+F_{\widetilde S,j|*}+F_{\nu,j}+F_{C,j},
 \tag{3.12}
\]

\[
 F_{\widetilde S,j|*}
 =\int\chi_j\left[
 (\widetilde S_{j|*}\Omega_j)\otimes\Omega_j
 +\Omega_j\otimes(\widetilde S_{j|*}\Omega_j)
 \right]dx.
 \tag{3.13}
\]

For time-dependent weights, differentiation of (1.2) gives the exact
aggregate ledger

\[
 \boxed{
 \dot{\mathcal Q}_k
 =\Sigma_*\mathcal Q_k+\mathcal Q_k\Sigma_*+\mathcal F_k,}
 \tag{3.14}
\]

\[
 \boxed{
 \mathcal F_k
 =\sum_{j\in J_k}w_{k,j}F_{j|*}
 +\sum_{j\in J_k}\dot w_{k,j}Q_j.}
 \tag{3.15}
\]

There is no cross-scale term in (3.14) because covariance summation is
linear.  There is also no automatic favorable sign or telescoping: all four
per-scale residuals, and the moving-weight term, remain.

An equivalent convention first chooses native sources \(\Sigma_j\) and
writes

\[
 \dot Q_j=\Sigma_jQ_j+Q_j\Sigma_j+F_j.
 \tag{3.16}
\]

Relative to the common \(\Sigma_*\), (3.15) becomes

\[
 \begin{aligned}
 \mathcal F_k
 ={}&\sum_jw_{k,j}
 \left[
 F_j+(\Sigma_j-\Sigma_*)Q_j
 +Q_j(\Sigma_j-\Sigma_*)
 \right]\\
 &+\sum_j\dot w_{k,j}Q_j.
 \end{aligned}
 \tag{3.17}
\]

Equation (3.17) is the scale-source mismatch that must be retained if each
filter scale is centered on its own resolved strain.

## 4. Shape and pullback identities survive, but require coercivity

Assume

\[
 \mathcal E_k=\operatorname{tr}\mathcal Q_k>0,
 \qquad
 \mathcal R_k=\frac{\mathcal Q_k}{\mathcal E_k},
 \qquad
 \mathcal B_k=\mathcal R_k-\frac13I.
 \tag{4.1}
\]

Define

\[
 q_k=\Sigma_*:\mathcal B_k=\Sigma_*:\mathcal R_k
 \tag{4.2}
\]

and, for a symmetric matrix \(F\),

\[
 \mathcal T_{\mathcal B_k}(F)
 =\frac{\operatorname{dev}F
 -\mathcal B_k\operatorname{tr}F}{\mathcal E_k}.
 \tag{4.3}
\]

The R0.70K calculation applies verbatim to (3.14):

\[
 \boxed{
 \dot{\mathcal B}_k
 =\Sigma_*\mathcal R_k+\mathcal R_k\Sigma_*
 -2q_k\mathcal R_k
 +\mathcal T_{\mathcal B_k}(\mathcal F_k).}
 \tag{4.4}
\]

If \(\Sigma_*\) is differentiable, then

\[
 \boxed{
 \dot q_k
 =\dot\Sigma_*:\mathcal B_k
 +2\operatorname{tr}
 \left[\mathcal R_k(\Sigma_*-q_kI)^2\right]
 +\Sigma_*:\mathcal T_{\mathcal B_k}(\mathcal F_k).}
 \tag{4.5}
\]

The frozen-source term remains nonnegative.  Multi-scale summation does not
turn it into damping.

For the common strain-only propagator

\[
 \dot G_*=\Sigma_*G_*,
 \qquad G_*(t_0)=I,
 \tag{4.6}
\]

the pulled aggregate

\[
 \widehat{\mathcal Q}_k
 =G_*^{-1}\mathcal Q_kG_*^{-\mathsf T}
 \tag{4.7}
\]

satisfies

\[
 \boxed{
 \dot{\widehat{\mathcal Q}}_k
 =G_*^{-1}\mathcal F_kG_*^{-\mathsf T}.}
 \tag{4.8}
\]

As in R0.70M, \(G_*\) is an auxiliary strain-only propagator, not the
physical deformation gradient.

If \(\mathcal Q_k\succ0\), the affine-relative shape speed is
condition-number free:

\[
 \mathfrak a(\mathcal Q_k,\mathcal F_k)^2
 =\operatorname{tr}
 \left[(\mathcal Q_k^{-1}\mathcal F_k)^2\right]
 -\frac13
 \left[\operatorname{tr}
 (\mathcal Q_k^{-1}\mathcal F_k)\right]^2.
 \tag{4.9}
\]

The entire purpose of (1.3) was to make this inverse quantitative.  Sections
6--8 show that the premise cannot hold universally for the scalar multi-scale
construction.

## 5. Exact frame criterion

For every \(v\in\mathbb R^3\), positivity gives (1.4).  Hence

\[
 v\in\ker\mathcal Q_k
 \quad\Longleftrightarrow\quad
 v\cdot\Omega_j=0
 \quad\chi_jdx\text{-a.e. for every active }j.
 \tag{5.1}
\]

Equivalently,

\[
 \boxed{
 \ker\mathcal Q_k
 =\bigcap_{j:w_{k,j}>0}\ker Q_j.}
 \tag{5.2}
\]

The equality uses nonnegative weights.  It follows because a sum of
nonnegative numbers is zero exactly when every active summand is zero.

The Rayleigh--Ritz principle gives (1.5).  Therefore

\[
 \mathcal Q_k\succeq
 c\operatorname{tr}(\mathcal Q_k)I
 \quad\Longleftrightarrow\quad
 0\le c\le c_*(k,t).
 \tag{5.3}
\]

Since the three normalized eigenvalues sum to one,

\[
 0\le c_*(k,t)\le\frac13.
 \tag{5.4}
\]

Formula (1.5) is the exact analogue of a persistent-excitation or
observability Gramian condition.  It asks every unit target-space direction
to receive a fixed fraction of the observed filtered-vorticity energy.  No
scalar trace identity supplies this angular lower bound.

For intuition, suppose the active observations are rank one:

\[
 Q_\alpha=E_\alpha n_\alpha\otimes n_\alpha,
 \qquad |n_\alpha|=1.
 \tag{5.5}
\]

After setting

\[
 a_\alpha
 =\frac{w_\alpha E_\alpha}
 {\sum_\beta w_\beta E_\beta},
 \qquad \sum_\alpha a_\alpha=1,
 \tag{5.6}
\]

one obtains

\[
 \frac{\mathcal Q}{\operatorname{tr}\mathcal Q}
 =\sum_\alpha a_\alpha n_\alpha n_\alpha^{\mathsf T}.
 \tag{5.7}
\]

With exactly three active directions,

\[
 \det\left(
 \frac{\mathcal Q}{\operatorname{tr}\mathcal Q}
 \right)
 =a_1a_2a_3
 \left[n_1\cdot(n_2\times n_3)\right]^2.
 \tag{5.8}
\]

Thus a weight tending to zero or directions becoming coplanar forces
degeneracy.  Merely counting three scales is not enough.

## 6. Common-subspace preservation theorem

### Theorem 6.1

Let \(V\subset\mathbb R^3\) be a fixed linear subspace.  Let
\(P_\alpha=T_\alpha I_3\) be any family of scalar/componentwise linear
spatial operators.  At every time used by observation \(\alpha\), suppose

\[
 \Pi_{V^\perp}\omega(\cdot,s)=0
 \tag{6.1}
\]

on the entire spatial input domain of \(T_\alpha\), in the function or
distribution class on which that operator acts.  More generally, it is enough
to assume directly that \(P_\alpha\omega(x,s)\in V\) for
\(d\mu_\alpha\)-almost every observed point.  Let \(d\mu_\alpha\ge0\) be any
family of finite observation measures and let \(w_\alpha\ge0\).  Define

\[
 \mathscr Q
 =\sum_\alpha w_\alpha
 \int(P_\alpha\omega)
 \otimes(P_\alpha\omega)\,d\mu_\alpha,
 \tag{6.2}
\]

assuming convergence in trace norm.  Then

\[
 \operatorname{Ran}\mathscr Q\subset V,
 \qquad
 V^\perp\subset\ker\mathscr Q.
 \tag{6.3}
\]

If \(V\ne\mathbb R^3\) and \(\operatorname{tr}\mathscr Q>0\), then

\[
 \lambda_{\min}(\mathscr Q)=0
 \tag{6.4}
\]

and no inequality

\[
 \mathscr Q\succeq c\operatorname{tr}(\mathscr Q)I
 \tag{6.5}
\]

can hold with \(c>0\).

### Proof

Let \(\Pi_{V^\perp}\) be the orthogonal projection onto \(V^\perp\).  Since
\(P_\alpha\) applies the same scalar operator to every component, it commutes
with every constant matrix, in particular

\[
 \Pi_{V^\perp}P_\alpha
 =P_\alpha\Pi_{V^\perp}.
 \tag{6.6}
\]

The full-input-domain hypothesis gives
\(\Pi_{V^\perp}\omega(\cdot,s)=0\), so

\[
 \Pi_{V^\perp}P_\alpha\omega=0.
 \tag{6.7}
\]

Under the direct filtered-output alternative in the theorem statement,
(6.7) is the assumption itself.

Thus every observed vector lies in \(V\).  For \(v\in V^\perp\),

\[
 v^{\mathsf T}\mathscr Qv
 =\sum_\alpha w_\alpha
 \int|v\cdot P_\alpha\omega|^2d\mu_\alpha=0.
 \tag{6.8}
\]

Since \(\mathscr Q\succeq0\), this implies
\(\mathscr Qv=0\).  Equations (6.3)--(6.4) follow.  Evaluating (6.5) on a unit
\(v\in V^\perp\) gives

\[
 0\ge c\operatorname{tr}(\mathscr Q)>0,
 \tag{6.9}
\]

a contradiction.  \(\square\)

The theorem covers finitely or countably many scales, any number of centers,
moving nonnegative cutoffs, adaptive nonnegative weights, and nonnegative
time integration.  It also covers a sum in which each nonzero \(Q_j\) is
first divided by its trace: positive scalar normalization changes neither
its range nor its kernel.

## 7. Exact rank-one periodic shear

### Theorem 7.1

Let \(A\ne0\), \(N\in\mathbb N\), and \(\nu>0\).  The field (1.8) is a smooth
unforced solution of the incompressible Navier--Stokes equations on
\(\mathbb T^3\).  For every scalar/componentwise filter \(P_j\), every
nonnegative cutoff \(\chi_j\), and every nonnegative weight family satisfying
(2.5), the associated nonzero aggregate covariance has rank at most one.

### Proof

The velocity is divergence free and

\[
 (u_s\cdot\nabla)u_s=0
 \tag{7.1}
\]

because it points in the \(x\)-direction and depends only on \(y\).  Directly,

\[
 \partial_tu_s=\nu\Delta u_s.
 \tag{7.2}
\]

Hence it solves NSE with constant pressure.  Its curl is (1.9).  By
componentwise scalar filtering,

\[
 \Omega_j(x,t)=f_j(x,t)e_3
 \tag{7.3}
\]

for some scalar \(f_j\).  Therefore

\[
 Q_j
 =\left(\int\chi_j|f_j|^2dx\right)e_3\otimes e_3
 =\gamma_j e_3\otimes e_3,
 \qquad \gamma_j\ge0.
 \tag{7.4}
\]

It follows that

\[
 \mathcal Q_k
 =\left(\sum_jw_{k,j}\gamma_j\right)e_3\otimes e_3.
 \tag{7.5}
\]

Whenever its trace is nonzero, (7.5) has rank one and \(c_*=0\).
\(\square\)

The same conclusion holds for a smooth Fourier-series shear

\[
 u(y,t)=\sum_{N\ge1}
 a_Ne^{-\nu N^2t}\sin(Ny)e_1,
 \tag{7.6}
\]

with rapidly decreasing coefficients.  Its nonlinearity remains exactly
zero, while coefficients can be chosen nonzero in arbitrarily many dyadic
bands.  The obstruction is therefore not an artifact of activating only one
filter scale.

## 8. Exact rank-two Beltrami common-null example

### Theorem 8.1

Let \(A\ne0\), \(N\in\mathbb N\), and \(\nu>0\).  The field (1.11) is a
smooth unforced periodic Navier--Stokes solution.  Every scalar/componentwise
filtered covariance, with any nonnegative cutoff, has \(e_3\) in its kernel.

### Proof

The field is divergence free.  It has no \(e_3\) component and depends only
on \(z\), so

\[
 (u_b\cdot\nabla)u_b=0.
 \tag{8.1}
\]

It also satisfies

\[
 \partial_tu_b=\nu\Delta u_b,
 \qquad
 \nabla\times u_b=Nu_b.
 \tag{8.2}
\]

Thus it is both an exact decaying heat mode and a curl eigenfield.  Its
vorticity lies in \(e_3^\perp\) pointwise.  Theorem 6.1 gives

\[
 Q_je_3=0,
 \qquad
 \mathcal Q_ke_3=0.
 \tag{8.3}
\]

For a scalar Fourier multiplier with response \(m_j(Ne_3)\) and the full
normalized torus measure, averaging \(\cos^2(Nz)\), \(\sin^2(Nz)\), and their
product gives (1.13).  It has rank two when the response is nonzero.
\(\square\)

This example separates three statements that must not be conflated:

- the vorticity direction is not spatially constant;
- the vorticity spans two directions and has the Beltrami relation;
- the covariance still has a fixed third null direction.

Three-dimensional coercivity requires quantitative noncoplanarity, not just
directional variation.

### Positive calibration: two helical axes

The no-go must not be overgeneralized to all Beltrami fields.  Define

\[
 b_z=(\sin z,\cos z,0),
 \qquad
 b_x=(0,\sin x,\cos x).
 \tag{8.4}
\]

Both satisfy \(\nabla\times b=b\).  Hence

\[
 u_{2h}(x,t)=e^{-\nu t}(a b_z+b b_x)
 \tag{8.5}
\]

is an exact NSE solution with

\[
 \nabla\times u_{2h}=u_{2h},
 \qquad
 p=-\frac12|u_{2h}|^2.
 \tag{8.6}
\]

For the full torus and translation-invariant scalar Fourier multipliers that
retain both unit-frequency axes, write their nonnegative covariance
coefficients as \(\alpha,\beta>0\).  Fourier orthogonality gives

\[
 \mathcal Q_{2h}
 =\alpha P_{e_3^\perp}+\beta P_{e_1^\perp}
 =\operatorname{diag}(\alpha,\alpha+\beta,\beta).
 \tag{8.7}
\]

Therefore

\[
 \det\mathcal Q_{2h}=\alpha\beta(\alpha+\beta)>0,
 \tag{8.8}
\]

and

\[
 c_*(\mathcal Q_{2h})
 =\frac{\min(\alpha,\beta)}{2(\alpha+\beta)}.
 \tag{8.9}
\]

This is the smallest exact escape from the single-axis Beltrami common-null
example: two nonparallel helical axes must both be seen, and their observed
energies must remain quantitatively balanced.  It is a positive calibration,
not a universal lower bound.

### No uniform constant after merely excluding exactly two-dimensional data

Fix a finite scalar-filter frame and a shear datum whose aggregate has
positive trace.  Let \(v_0\) be a smooth divergence-free perturbation, and put

\[
 u_0^\varepsilon=u_0^s+\varepsilon v_0.
 \tag{8.10}
\]

By linear filtering,

\[
 \Omega_j^\varepsilon
 =f_je_3+\varepsilon\eta_j.
 \tag{8.11}
\]

For every unit \(e\perp e_3\),

\[
 e^{\mathsf T}\mathcal Q^\varepsilon e
 =\varepsilon^2
 \sum_jw_j\int\chi_j|e\cdot\eta_j|^2dx,
 \tag{8.12}
\]

while

\[
 \operatorname{tr}\mathcal Q^\varepsilon
 \longrightarrow\operatorname{tr}\mathcal Q^0>0.
 \tag{8.13}
\]

Thus

\[
 \frac{\lambda_{\min}(\mathcal Q^\varepsilon)}
 {\operatorname{tr}\mathcal Q^\varepsilon}
 \longrightarrow0.
 \tag{8.14}
\]

For an explicit positive-definite calibration, take the full-torus identity
filter and

\[
 v_0=b_z+b_x,
 \tag{8.15}
\]

with \(b_z,b_x\) from (8.4).  The three \(x\)-, \(y\)-, and \(z\)-axis Fourier
families are orthogonal on the full torus.  For every \(\varepsilon>0\), the
datum \(u_0^\varepsilon\) depends on all three coordinates and its covariance
is positive definite, while (8.14) still holds.  This explicit statement is
not asserted for an arbitrary filter frame: a filter may project away every
added direction.  Consequently, removing the exact two-dimensional
invariant class, without a quantitative separation from it, still cannot
produce a solution-independent positive frame constant.

## 9. Exact finite symbolic certificate

The archived producer uses the filter responses

\[
 m_1=1,
 \qquad m_2=\frac12,
 \qquad m_3=\frac13,
 \tag{9.1}
\]

and weights

\[
 w_1=1,
 \qquad w_2=2,
 \qquad w_3=3.
 \tag{9.2}
\]

Then

\[
 \sum_{j=1}^3w_jm_j^2
 =1+\frac12+\frac13
 =\frac{11}{6}.
 \tag{9.3}
\]

After factoring out \(A^2N^2e^{-2\nu N^2t}\), the full-torus shear covariance
is

\[
 \boxed{
 \mathcal Q_s
 =\frac{11}{12}
 \begin{pmatrix}
 0&0&0\\
 0&0&0\\
 0&0&1
 \end{pmatrix},}
 \tag{9.4}
\]

with

\[
 \operatorname{rank}\mathcal Q_s=1,
 \qquad
 \operatorname{tr}\mathcal Q_s=\frac{11}{12}.
 \tag{9.5}
\]

For every \(c>0\), evaluation on \(e_1\) gives

\[
 e_1^{\mathsf T}
 \left(\mathcal Q_s-c\operatorname{tr}(\mathcal Q_s)I\right)e_1
 =-\frac{11}{12}c<0.
 \tag{9.6}
\]

The corresponding Beltrami covariance is

\[
 \boxed{
 \mathcal Q_b
 =\frac{11}{12}
 \begin{pmatrix}
 1&0&0\\
 0&1&0\\
 0&0&0
 \end{pmatrix},}
 \tag{9.7}
\]

with

\[
 \operatorname{rank}\mathcal Q_b=2,
 \qquad
 \operatorname{tr}\mathcal Q_b=\frac{11}{6}.
 \tag{9.8}
\]

Evaluation on \(e_3\) gives

\[
 e_3^{\mathsf T}
 \left(\mathcal Q_b-c\operatorname{tr}(\mathcal Q_b)I\right)e_3
 =-\frac{11}{6}c<0.
 \tag{9.9}
\]

The producer verifies the two NSE identities symbolically, the aggregate
source-mismatch ledger with generic symmetric matrices, the moving-weight
term, scale-wise trace normalization, and exact positive time aggregation.
The finite calculation is a reproducible exemplar.  The arbitrary-family
statement is Theorem 6.1, not an inference from three numerical scales.

## 10. Centers and time windows do not give a free repair

### Multiple centers

Let \(Q_{j,r}\) use center \(r\).  With nonnegative weights,

\[
 \ker\left(\sum_{j,r}w_{j,r}Q_{j,r}\right)
 =\bigcap_{j,r:w_{j,r}>0}\ker Q_{j,r}.
 \tag{10.1}
\]

Multiple centers can remove a local null direction only if the underlying
observations genuinely span new target-space directions.  They do nothing
to the fixed common subspaces in Sections 7--8.

### Positive time windows

Let

\[
 \overline{\mathcal Q}(t)
 =\int_0^\tau a(r)\mathcal Q(t-r)\,dr,
 \qquad a(r)\ge0.
 \tag{10.2}
\]

Its quadratic form is the positive space--scale--time integral of
\(|v\cdot\Omega|^2\).  The common-subspace theorem therefore applies without
change.  In particular, shear remains rank one and the Beltrami wave remains
rank at most two for every \(\tau\).

For a general flow, temporal rotation could make (10.2) positive definite.
That does not make the construction free dynamically.  Suppose

\[
 \dot{\mathcal Q}(s)
 =\Sigma(s)\mathcal Q(s)+\mathcal Q(s)\Sigma(s)
 +\mathcal F(s).
 \tag{10.3}
\]

Choose a current common reference \(\Sigma_*(t)\).  For a fixed integration
kernel and fixed endpoints in the lag variable,

\[
 \dot{\overline{\mathcal Q}}
 =\Sigma_*\overline{\mathcal Q}
 +\overline{\mathcal Q}\Sigma_*+\overline{\mathcal F}_*,
 \tag{10.4}
\]

where

\[
 \begin{aligned}
 \overline{\mathcal F}_*(t)
 =\int_0^\tau a(r)\{&\mathcal F(t-r)\\
 &+[\Sigma(t-r)-\Sigma_*(t)]\mathcal Q(t-r)\\
 &+\mathcal Q(t-r)[\Sigma(t-r)-\Sigma_*(t)]\}\,dr.
 \end{aligned}
 \tag{10.5}
\]

If the kernel or endpoints move independently, their derivative and boundary
terms must be added.  The historical direction changes that can improve rank
also reappear as source mismatch in (10.5).  Moreover, invertibility of the
time average does not imply invertibility of the instantaneous covariance.

## 11. Finite-energy initial-face boundary on \(\mathbb R^3\)

The periodic solutions already disprove a theorem stated for all smooth
periodic NSE flows.  A separate construction records what survives on the
whole space with finite energy.

Take \(\psi\in C_c^\infty(\mathbb R^3)\) and set

\[
 \omega_0=\nabla\times(\psi e_3)
 =(\partial_2\psi,-\partial_1\psi,0).
 \tag{11.1}
\]

Then \(\nabla\cdot\omega_0=0\) and \(\omega_0(x)\in e_3^\perp\).  Define the
Biot--Savart velocity

\[
 u_0=\nabla\times(-\Delta)^{-1}\omega_0.
 \tag{11.2}
\]

The derivative structure in (11.1) removes the zero-frequency singularity;
\(u_0\) is smooth, divergence free, has curl \(\omega_0\), and belongs to the
finite-energy Sobolev classes required for local smooth existence.  Every
scalar/componentwise filtered \(\Omega_j(0)\) remains in \(e_3^\perp\), so

\[
 Q_j(0)e_3=0,
 \qquad
 \mathcal Q_k(0)e_3=0.
 \tag{11.3}
\]

Therefore a universal frame bound that includes the initial face fails on
\(\mathbb R^3\) as well.  This section does not claim that the whole-space
solution preserves the same common nullspace for all positive times.  The
full-time exact examples in this release are periodic.

There is also a full-rank quantitative calibration showing that exact rank
loss is not needed to destroy a data-uniform constant.  For \(L\ge1\), let

\[
 \psi_L
 =\exp\left[-\frac{x^2+y^2}{2}-\frac{z^2}{2L^2}\right],
 \qquad
 u_L=(-y\psi_L,x\psi_L,0).
 \tag{11.4}
\]

This is a divergence-free Schwartz datum depending on all three spatial
variables.  Its vorticity is

\[
 \omega_L
 =\left(
 \frac{xz}{L^2}\psi_L,
 \frac{yz}{L^2}\psi_L,
 (2-x^2-y^2)\psi_L
 \right).
 \tag{11.5}
\]

Exact Gaussian integration for the identity filter and full-space cutoff
gives

\[
 Q_L
 =\pi^{3/2}
 \operatorname{diag}\left(
 \frac1{4L},\frac1{4L},2L
 \right).
 \tag{11.6}
\]

Every finite \(L\ge1\) gives \(Q_L\succ0\), but

\[
 \frac{\lambda_{\min}(Q_L)}{\operatorname{tr}Q_L}
 =\frac1{8L^2+2}
 \longrightarrow0.
 \tag{11.7}
\]

Multiplying \(u_L\) by an arbitrary amplitude leaves this ratio unchanged;
the data may therefore be placed in a small-data global class.  The family
shows, at the initial face, that finite energy, smoothness, genuine
three-dimensional dependence, and even positive definiteness do not provide
a data-uniform frame constant.  It is not a claim about finite-time
singularity or about persistence of (11.7) for the nonlinear solution.

## 12. Apparent repairs and their exact boundaries

### Normalizing every scale

Replacing \(Q_j\) by \(Q_j/\operatorname{tr}Q_j\) when the trace is positive
changes eigenvalue magnitudes but not the range.  Every normalized shear
covariance is \(e_3\otimes e_3\); every normalized full-torus Beltrami
covariance is

\[
 \frac12\operatorname{diag}(1,1,0).
 \tag{12.1}
\]

The common nullspace remains.

### Signed weights

Allowing negative weights destroys the Gramian interpretation and can make
the sum indefinite.  It does not establish a lower positive-semidefinite
bound.  The no-go theorem therefore retains the natural nonnegative weights.

### Isotropic ridge regularization

Adding \(\varepsilon\operatorname{tr}(\mathcal Q)I\) makes the matrix
invertible by definition.  R0.70M already showed that the corresponding
affine-relative residual contains a non-vanishing strain term as
\(\varepsilon\downarrow0\).  The operation assumes the missing directions;
it does not derive them from NSE.

### Artificial component rotations

For a finite rotation family \(R_\alpha\), a designed average

\[
 \sum_\alpha R_\alpha Q R_\alpha^{\mathsf T}
 \tag{12.2}
\]

can be made proportional to \(\operatorname{tr}(Q)I\).  But each rotated
copy evolves under the rotated source

\[
 R_\alpha\Sigma R_\alpha^{\mathsf T}.
 \tag{12.3}
\]

Forcing all copies into one common pullback produces the mismatch terms of
(3.17).  Such a construction is an imposed isotropic observation system,
not a scalar multi-scale covariance theorem.

### Augmented physical observables

A Gramian containing strain, pressure-Hessian directions, transported
frames, or component-mixing vector filters is not excluded.  It must first
pass three tests:

1. every added direction must come from a precisely defined NSE observable;
2. its exact evolution and all commutators must be derived;
3. the coercive lower bound must not be inserted by the observation design
   and then counted as a PDE conclusion.

No augmented construction is certified in R0.70N.

## 13. Position relative to the literature

The closest filtered-vorticity source found in the 2026 search is
[Yu, arXiv:2606.27560](https://arxiv.org/abs/2606.27560).  It derives a
finite-scale filtered vortex-stretching estimate with angular, commutator,
far-field, and localization defects.  It does not introduce the covariance
Gramian (1.1) or prove a lower bound for its smallest eigenvalue.

Vorticity-direction coherence is a genuine regularity mechanism in the
geometric-depletion literature.  The foundational result of
[Constantin--Fefferman](https://iumj.org/article/3627/) and later refinements
such as
[Beirão da Veiga--Berselli](https://doi.org/10.57262/die/1356060864)
control stretching under quantitative direction hypotheses.  These results
do not imply a lower bound for the smallest eigenvalue of a localized
multi-scale covariance.

Component-reduction and locally anisotropic criteria show that singular
behavior, if it occurs, must retain genuinely three-dimensional content.  In
particular,
[Chae--Choe](https://ejde.math.txstate.edu/Volumes/1999/05/abstr.html)
give a criterion in terms of two vorticity components, while
[Miller](https://doi.org/10.1090/bproc/74) proves a locally anisotropic
criterion in terms of vorticity.  These theorems motivate studying the
low-rank branch rather than treating it only as a defect.  The spectral
geometry must be stated correctly: small \(\lambda_{\min}\) means proximity
to a plane, whereas control of two vorticity components is closer to
proximity to a line and requires information on
\(\lambda_{\mathrm{mid}}+\lambda_{\min}\), together with critical space-time
norms and direction-field regularity.  These theorems do not turn the
\(L^2\)-type ratio (1.5) into a known critical continuation norm.

Wavelet and coherent-vorticity studies, including
[Okamoto et al.](https://doi.org/10.1137/10079598X) and
[Zhou et al.](https://doi.org/10.1103/PhysRevE.73.036307), demonstrate useful
multi-resolution decompositions and numerical/statistical structure.  They
do not prove a deterministic uniform angular-frame lower bound for all
smooth NSE solutions.

In control and observability theory, a positive Gramian lower bound is
normally a persistent-excitation or observability assumption.  The exact
identity (1.5) places the proposed covariance bound in that class: it is an
additional directional richness condition, not a consequence of total
observed energy alone.

Affine-invariant SPD geometry does not cross the rank boundary.  The
fixed-rank PSD geometry of
[Bonnabel--Sepulchre](https://arxiv.org/abs/0807.4462) supplies a natural
language for a pseudoinverse and an evolving range, but it preserves rather
than repairs rank.  A Navier--Stokes use would still require an evolution
ledger for the range projector and its commutators.

The bounded primary-source audit found no theorem asserting (1.3) for
scalar-filtered vorticity covariances.  That is a bounded-search statement,
not proof that no differently named construction exists.  The no-go theorem
itself does not depend on novelty: one exact shear solution disproves the
universal assertion.

## 14. What is closed and what remains open

### Proved or exactly derived here

- The complete multi-scale covariance ledger (3.14)--(3.17), including
  moving weights and source mismatch.
- The aggregate normalized-shape and common pullback identities.
- The exact Rayleigh-quotient formula for the optimal frame constant.
- The kernel-intersection formula for nonnegative covariance sums.
- The common-subspace preservation theorem for arbitrary scalar/componentwise
  filter, center, and positive time families.
- Rank-one failure on an exact smooth unforced periodic shear.
- Rank-two common-null failure on an exact smooth unforced periodic helical
  Beltrami wave.
- A two-axis helical positive control with exact determinant and optimal
  frame constant.
- Degeneration of the frame constant along genuinely three-dimensional
  perturbations of shear.
- Failure of per-scale trace normalization and positive time averaging on
  both witnesses.
- A finite-energy whole-space initial-face common-null construction.
- A full-rank genuinely three-dimensional Schwartz family with exact
  frame quotient \(1/(8L^2+2)\to0\).

### Closed route

The branch

> sum finitely or countably many scalar-filtered vorticity covariances with
> nonnegative scale, center, or time weights and thereby obtain a universal
> positive-definite frame for every nonzero smooth NSE state

is closed.  Exact smooth NSE solutions keep all observed vorticity in a
fixed one- or two-dimensional target-space subspace.

The closure remains valid if every nonzero scale is normalized by its trace,
if many dyadic bands are activated by one Fourier-series shear, or if the
weights adapt to the solution while remaining nonnegative.

### Still open

- A conditional lower bound for a restricted quantitatively
  three-dimensional solution class.
- A critical estimate for the affine residual on the branch where
  \(c_*\ge c_0>0\).
- A rigorous bridge from small \(c_*\) to a known geometric-depletion or
  component-reduction regularity criterion.
- An augmented physical Gramian whose exact PDE ledger closes without
  reintroducing an equally hard source-mismatch term.
- A weak-solution passage for any of these covariance constructions.

### Route decision

R0.70O should test a **coercive-versus-rank-stratified dichotomy** rather
than seek universal coercivity.  Write

\[
 \lambda_1\ge\lambda_2\ge\lambda_3\ge0
 \tag{14.1}
\]

for the eigenvalues of \(\mathcal Q_k\).  There are three distinct geometric
regimes:

\[
 \lambda_3\gtrsim\operatorname{tr}\mathcal Q_k
 \quad\text{(coercive),}
 \tag{14.2}
\]

\[
 \lambda_3\ll\operatorname{tr}\mathcal Q_k
 \quad\text{(near a plane only),}
 \tag{14.3}
\]

and

\[
 \lambda_2+\lambda_3\ll\operatorname{tr}\mathcal Q_k
 \quad\text{(near a line).}
 \tag{14.4}
\]

Only the third is geometrically close to controlling two vorticity
components.  Even there, the filtered localized spectrum does not yet give a
critical unfiltered space-time norm or regularity of the principal
direction.

The next gate is:

1. use the exact alternative

   \[
   c_*(k,t)\ge c_0
   \quad\text{or}\quad
   \exists\,|n|=1:\quad
   \sum_jw_j\int\chi_j|n\cdot\Omega_j|^2
   <c_0\mathcal E_k;
   \tag{14.5}
   \]

2. on the coercive branch, quantify
   \(\mathfrak a(\mathcal Q_k,\mathcal F_k)\) without converting through a
   condition number;
3. on the near-plane branch, first test whether one small covariance
   eigenvalue has any critical consequence; no such consequence is assumed;
4. on the near-line branch, test whether
   \(\lambda_2+\lambda_3\) plus a quantitative principal-direction ledger can
   reach a Chae--Choe or Miller-type scaling-critical criterion;
5. derive the fixed-rank projector or pseudoinverse evolution before using
   fixed-rank PSD geometry;
6. construct exact concentrating counterexamples before attempting any DNS;
7. use computation only if the analytic bridge survives the scaling and
   concentration gates.

The first likely obstruction is that (14.5) is a relative localized
\(L^2\) statement, whereas known continuation criteria use stronger critical
space-time control.  R0.70O must establish or refute that bridge explicitly;
it must not describe low rank itself as regularity.

## 15. Reproduction and claim boundary

The exact symbolic producer is

```text
research/r070n_multiscale_frame_audit.py
```

It verifies, using exact symbolic and rational arithmetic:

- the generic common-source aggregate ledger;
- native-source mismatch and time-dependent-weight terms;
- the common pullback cancellation;
- the divergence, vanishing nonlinearity, heat equation, and curl of both
  periodic NSE witnesses;
- the exact three-scale matrices (9.4) and (9.7);
- their ranks, traces, and negative coercivity test directions;
- persistence of the nullspace under scale normalization and positive time
  aggregation.

No trajectory discretization, turbulence closure, empirical sign, DNS, or
DGX computation enters the proof.  The exact finite matrices illustrate the
general analytic theorem; they do not replace it.

This release disproves one proposed universal intermediate lemma.  It does
not prove an unconditional regularity estimate, a new continuation theorem,
finite-time blow-up, global smoothness, or a solution of the Millennium
problem.
