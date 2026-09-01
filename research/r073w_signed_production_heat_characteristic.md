# R0.73W analytic derivation: signed production, heat characteristics, and the energy-class boundary

**Status:** parent derivation, independent sign/index audit, and commit-bound
two-path finite certificate complete; the formal figure and public release
gates remain open

**Ordinary translation path:** `LOCAL_DIRECT_NO_DGX`

**DGX used:** `false`

## 1. Setting and normalization

Work on the normalized periodic torus, so \(\langle1\rangle=1\).  Let \(u\)
be a smooth real mean-zero divergence-free solution of

\[
 \partial_tu+\nabla\!\cdot(u\otimes u)+\nabla p=\nu\Delta u,
 \qquad \nabla\cdot u=0.
\tag{1.1}
\]

For \(s\ge0\), set

\[
 P_s=e^{s\Delta},\quad v_s=P_su,\quad p_s=P_sp,\quad
 \tau_s=P_s(u\otimes u)-v_s\otimes v_s.
\tag{1.2}
\]

The resolved strain, energy density, and signed subgrid production are

\[
 S_s={1\over2}(\nabla v_s+\nabla v_s^T),\qquad
 e_s={1\over2}|v_s|^2,\qquad
 \Pi_s=-\tau_s:\nabla v_s.
\tag{1.3}
\]

The stress is symmetric, so \(\tau_s:\nabla v_s=\tau_s:S_s\).  The sign in
(1.3) makes positive \(\Pi_s\) a sink in the resolved-energy equation.

## 2. Exact stress representation and the deviatoric obstruction

Since \(\partial_sP_s=\Delta P_s\), the Laplacian product rule gives

\[
 \begin{aligned}
 (\partial_s-\Delta)\tau_{ij,s}
 &=2\sum_{\ell=1}^3
 \partial_\ell v_{s,i}\,\partial_\ell v_{s,j},\\
 \tau_{ij,0}&=0.
 \end{aligned}
\tag{2.1}
\]

Duhamel's formula therefore yields

\[
 \boxed{
 \tau_{ij,s}=2\int_0^sP_{s-r}\!\left(
 \partial_\ell v_{r,i}\,\partial_\ell v_{r,j}
 \right)\,dr.}
\tag{2.2}
\]

This is the heat-semigroup normalization of the exact Gaussian-filter stress
formula in Johnson (2020).  It is an established identity, not a novelty
claim.

The covariance form also shows that \(\tau_s(x)\) is positive semidefinite:
for every \(a\in\mathbb R^3\),

\[
 a_i\tau_{ij,s}(x)a_j
 =P_s[(a\cdot u)^2](x)-[P_s(a\cdot u)(x)]^2\ge0.
\tag{2.3}
\]

This positivity does not determine the sign of production.  Incompressibility
gives \(\operatorname{tr}S_s=0\), and hence

\[
 \boxed{
 \Pi_s=-\tau_s^\circ:S_s
 =-2\int_0^sP_{s-r}\!\left[
 (\nabla v_r\nabla v_r^T)^\circ
 \right]:S_s\,dr.}
\tag{2.4}
\]

The isotropic positive part cancels.  The remaining issue is the signed
alignment of the deviatoric covariance with the trace-free strain.  In
particular,

\[
 |\Pi_s|\le 2k_s\|S_s\|_{\mathrm{op}},\qquad
 k_s={1\over2}\operatorname{tr}\tau_s,
\tag{2.5}
\]

but (2.5) has no coercive sign.

## 3. The exact local identity on the \((t,s)\) heat plane

Filtering (1.1) gives

\[
 \partial_tv_s+\nabla\!\cdot(v_s\otimes v_s+\tau_s)
 +\nabla p_s=\nu\Delta v_s.
\tag{3.1}
\]

Taking the scalar product with \(v_s\), using
\(v_s\cdot\Delta v_s=\Delta e_s-|\nabla v_s|^2\), and keeping the stress
transport in divergence form gives

\[
 \partial_te_s+\nabla\!\cdot\!\left[
 (e_s+p_s)v_s+\tau_sv_s\right]
 =\nu\Delta e_s-\nu|\nabla v_s|^2-\Pi_s.
\tag{3.2}
\]

The heat equation for \(v_s\) independently gives

\[
 \partial_se_s=\Delta e_s-|\nabla v_s|^2.
\tag{3.3}
\]

Subtracting \(\nu\) times (3.3) from (3.2) proves

\[
 \boxed{
 (\partial_t-\nu\partial_s)e_s+
 \nabla\!\cdot\!\left[(e_s+p_s)v_s+\tau_sv_s\right]
 =-\Pi_s.}
\tag{3.4}
\]

Thus viscosity is exactly tangent to the descending heat characteristics
\(s'(t)=-\nu\).  On the torus, with
\(E_s(t)=\frac12\langle|v_s(t)|^2\rangle\), spatial integration yields

\[
 \boxed{
 \langle\Pi_s(t)\rangle
 =-(\partial_t-\nu\partial_s)E_s(t).}
\tag{3.5}
\]

If \(s(t)=s_0-\nu(t-t_0)>0\) on \([t_0,t_1]\), then

\[
 \boxed{
 \int_{t_0}^{t_1}\langle\Pi_{s(t)}(t)\rangle\,dt
 =E_{s_0}(t_0)-E_{s(t_1)}(t_1).}
\tag{3.6}
\]

For a smooth solution the endpoint may reach \(s=0\).  For a Leray--Hopf
solution, the interior identity is used only on characteristics separated
from \(s=0\), unless the required endpoint energy equality has been proved.
The signed integral in (3.6) is an exact payment, but it does not control
\(\int|\Pi|\), a pointwise sign, or a fixed-scale supremum.

## 4. An absolute energy-class estimate

The exact stress representation (2.2), heat contraction, and commutation with
derivatives give, at almost every time,

\[
 \begin{aligned}
 \|\tau_s\|_{L^1}
 &\le2\int_0^s
 \|\nabla v_r\nabla v_r^T\|_{L^1}\,dr\\
 &\le2\int_0^s\|\nabla v_r\|_{L^2}^2\,dr
 \le2s\|\nabla u\|_{L^2}^2.
 \end{aligned}
\tag{4.1}
\]

The three-dimensional heat-kernel derivative estimate gives, for
\(0<s\le1\),

\[
 \|\nabla v_s\|_{L^\infty}
 \le C s^{-5/4}\|u\|_{L^2}.
\tag{4.2}
\]

The exponent \(5/4\) is the derivative cost \(1/2\) plus the
\(L^2\to L^\infty\) smoothing cost \(3/4\).  Hölder's inequality,
(4.1)--(4.2), and time integration now prove

\[
 \boxed{
 \|\Pi_s\|_{L^1(I\times\mathbb T^3)}
 \le C s^{-1/4}
 \|u\|_{L_t^\infty L_x^2(I)}
 \|\nabla u\|_{L^2(I\times\mathbb T^3)}^2.}
\tag{4.3}
\]

Consequently,

\[
 \boxed{
 \int_0^S\|\Pi_s\|_{L^1(I\times\mathbb T^3)}\,ds
 \le {4C\over3}S^{3/4}
 \|u\|_{L_t^\infty L_x^2(I)}
 \|\nabla u\|_{L^2(I\times\mathbb T^3)}^2}
\tag{4.4}
\]

for \(0<S\le1\).  This estimate uses only the Leray--Hopf energy class and
extends by standard approximation.  Its scale singularity is integrable, but
the estimate does not give a uniform bound as \(s\downarrow0\).  No claim of
optimality is made for the exponent \(1/4\).  An equivalent factorization
through \(\|\tau_s\|_{3/2}\|\nabla v_s\|_3\) gives the same power.

## 5. A finite exact sign and absorption obstruction

Define the smooth real divergence-free trigonometric polynomial

\[
 \begin{aligned}
 R(x,y,z)={}&\big(\cos(y+z)-\sin(x+y+z)+\cos(2z),\\
 &\qquad \cos x+\sin(x+y+z),\ 0\big),
 \qquad u_A=A R.
 \end{aligned}
\tag{5.1}
\]

Its Fourier support spans rank three over \(\mathbb Q\).  Let \(q=e^{-s}\).
Direct Fourier convolution gives

\[
 \boxed{\langle\Pi_s(u_A)\rangle={A^3\over4}q^2(1-q^2).}
\tag{5.2}
\]

The independent exact certificate records every contributing mode and also
verifies

\[
 \langle|\nabla R|^2\rangle={13\over2},
 \qquad
 \langle|\nabla v_s|^2\rangle
 =A^2\left({q^2\over2}+q^4+3q^6+2q^8\right).
\tag{5.3}
\]

For

\[
 D_{ii,s}=P_s(|\nabla u|^2)-|\nabla v_s|^2,
\tag{5.4}
\]

the mean is

\[
 \boxed{
 \langle D_{ii,s}(u_A)\rangle
 ={A^2\over2}(1-q^2)
 (13+12q^2+10q^4+4q^6).}
\tag{5.5}
\]

Replacing \(u_A\) by \(-u_A\) preserves \(\tau_s\) and \(D_{ii,s}\), but
reverses \(S_s\) and \(\Pi_s\).  Hence both signs occur among smooth initial
data.  Moreover,

\[
 { |\langle\Pi_s(u_A)\rangle|
  \over \nu\langle D_{ii,s}(u_A)\rangle }
 ={Aq^2\over
 2\nu(13+12q^2+10q^4+4q^6)},
\tag{5.6}
\]

which is unbounded as \(A\to\infty\) for every fixed \(s>0\).  As
\(s\downarrow0\), the coefficient tends to \(A/(78\nu)\).  Thus there is no
amplitude-independent same-time inequality

\[
 |\langle\Pi_s\rangle|\le C\nu\langle D_{ii,s}\rangle
\tag{5.7}
\]

valid for all smooth divergence-free data.

The package also recomputes a three-coordinate rank-two triad and a 2D3C
field as diagnostic cross-checks.  The public witness (5.1) has rank-three
Fourier support, but this finite algebra still makes no genericity or blow-up
claim.

## 6. Centered increments, divergence cancellation, and the signed remainder

Let \(g_s\) be the Euclidean heat kernel and extend the periodic field to
\(\mathbb R^3\).  Define the increment centered at the filtered value

\[
 a_s(x,y)=u(x-y)-v_s(x).
\tag{6.1}
\]

The contracted third heat cumulant is the central third moment

\[
 K_{j,s}={1\over2}\kappa_{iij,s}
 ={1\over2}\int_{\mathbb R^3}g_s(y)a_{s,j}(x,y)
 |a_s(x,y)|^2\,dy.
\tag{6.2}
\]

Differentiate (6.2) in \(x_j\).  The terms containing
\(\partial_ja_{s,j}\) vanish by incompressibility, and
\(\int g_sa_{s,i}a_{s,j}\,dy=\tau_{ij,s}\).  Integration by parts in \(y\)
then gives

\[
 \boxed{
 \Pi_s=\partial_jK_{j,s}+\mathscr S_s,}
\tag{6.3}
\]

where

\[
 \boxed{
 \begin{aligned}
 \mathscr S_s
 &=-{1\over2}\int_{\mathbb R^3}
 \nabla g_s(y)\cdot a_s(x,y)|a_s(x,y)|^2\,dy\\
 &={1\over4s}\int_{\mathbb R^3}
 y\cdot a_s(x,y)|a_s(x,y)|^2g_s(y)\,dy.
 \end{aligned}}
\tag{6.4}
\]

The factor \(1/(4s)\) follows from
\(\nabla g_s(y)=-y g_s(y)/(2s)\).  Formula (6.4) is a centered-increment
version of the local coarse-grained transfer.  Its sign is not fixed.

R0.73V established the exact trace equation

\[
 \partial_tk_s+\nabla\cdot(v_sk_s)
 =-\nabla\cdot(K_s+Q_s-\nu\nabla k_s)
 -\nu D_{ii,s}+\Pi_s.
\tag{6.5}
\]

Substituting (6.3) cancels the velocity third-cumulant flux exactly:

\[
 \boxed{
 \partial_tk_s+\nabla\cdot(v_sk_s+Q_s-\nu\nabla k_s)
 =-\nu D_{ii,s}+\mathscr S_s.}
\tag{6.6}
\]

The remaining quadratic row is a nonnegative carré-du-champ:

\[
 \boxed{
 \begin{aligned}
 D_{ii,s}
 &=P_s(|\nabla u|^2)-|\nabla v_s|^2\\
 &=2\int_0^sP_{s-r}|\nabla^2v_r|_F^2\,dr\ge0.
 \end{aligned}}
\tag{6.7}
\]

Thus (6.6) separates a spatial divergence, a nonnegative viscous covariance,
and one signed centered-increment remainder.  It does not absorb that
remainder.  Equation (6.6) is a classical physical-time identity on the
smooth lifespan.  It must not be passed unchanged to an arbitrary weak
limit.  If a suitable weak solution carries local energy-defect measure
\(\mu\ge0\), the corresponding right-hand side contains the additional term
\(-P_s\mu\).  No local trace equality is asserted for a general Leray--Hopf
solution without accounting for that defect.

For completeness, the production itself obeys the exact heat-scale equation

\[
 \boxed{
 (\partial_s-\Delta)\Pi_s
 =2\partial_\ell\tau_{ij,s}\,\partial_{\ell j}v_{s,i}
 -2B_{ij,s}\,\partial_jv_{s,i},\qquad \Pi_0=0,}
\tag{6.8}
\]

where

\[
 B_{ij,s}=\partial_\ell v_{s,i}\partial_\ell v_{s,j}
 =(\nabla v_s\nabla v_s^T)_{ij}.
\tag{6.9}
\]

The order in (6.9) matters.  Under the convention
\((\nabla v)_{ij}=\partial_jv_i\), the matrix is
\(\nabla v\nabla v^T\), not \(\nabla v^T\nabla v\).  Neither cubic source in
(6.8) has a fixed sign.

## 7. The critical scale-weighted spatial mean

Let \(L=-\Delta\) on mean-zero periodic fields and
\(h=(u\cdot\nabla)u\).  The resolved cubic transport has zero spatial mean,
and self-adjointness of \(P_s\) gives

\[
 \boxed{
 \langle\Pi_s\rangle
 =\langle e^{-2sL}u,h\rangle_{L^2}.}
\tag{7.1}
\]

For a weight \(w\) for which the following integrals converge, define

\[
 m_w(\lambda)=\int_0^\infty w(s)e^{-2s\lambda}\,ds.
\tag{7.2}
\]

The exact weighted identity is

\[
 \boxed{
 \int_0^\infty w(s)\langle\Pi_s\rangle\,ds
 =\langle m_w(L)u,(u\cdot\nabla)u\rangle.}
\tag{7.3}
\]

At the critical weight \(w(s)=s^{-1/2}\), spectral calculus gives

\[
 m_w(L)=\sqrt{\pi/2}\,L^{-1/2},
\tag{7.4}
\]

and therefore

\[
 \boxed{
 I_\Pi(u):=\int_0^\infty s^{-1/2}\langle\Pi_s\rangle\,ds
 =\sqrt{\pi/2}\,\langle L^{-1/2}u,(u\cdot\nabla)u\rangle.}
\tag{7.5}
\]

With the periodic Riesz transform \(R_j=\partial_jL^{-1/2}\), integration by
parts yields

\[
 I_\Pi(u)=-\sqrt{\pi/2}\int_{\mathbb T^3}
 u_i u_j R_j u_i\,dx.
\tag{7.6}
\]

The matching scale derivative of subfilter energy is

\[
 \boxed{
 \int_0^\infty s^{-1/2}{d\over ds}\langle k_s\rangle\,ds
 =\sqrt{\pi/2}\,\|L^{1/4}u\|_2^2.}
\tag{7.7}
\]

The scale smoothing in (7.5) exactly cancels the derivative in the
nonlinearity, leaving a zero-order Riesz trilinear form.  Consequently,

\[
 |I_\Pi(u)|\le C\|u\|_3^3
 \le C\|L^{1/4}u\|_2^3.
\tag{7.8}
\]

This is the classical critical \(H^{1/2}\) small-data structure, not an
arbitrary-energy absorption.  For an energy-class solution on \([0,T]\),
interpolation, Hölder in time, and the energy inequality give

\[
 \int_0^T|I_\Pi(u(t))|\,dt
 \le C\|u_0\|_2^3\nu^{-3/4}T^{1/4}.
\tag{7.9}
\]

The order of operations is essential: (7.9) first performs the signed spatial
and heat-scale integrations in (7.5), then takes an absolute value.  It is not
a bound for the local or fixed-scale absolute flux.

## 8. What has and has not been obtained

The first exact positive result is (3.4)--(3.6): after spatial integration,
signed production is paid exactly by resolved energy along the viscous heat
characteristic.  The unconditional absolute result is (4.3)--(4.4):
production is integrable on every small-scale interval \(0<s<S\le1\) for
every energy-class solution.
The centered split (6.3)--(6.7) isolates the nonnegative viscous covariance
from the single signed increment remainder.  The critical average
(7.5)--(7.9) shows precisely why scale smoothing recovers the classical
\(H^{1/2}\) small-data trilinear structure but no arbitrary-energy coercivity.

The finite witness closes two tempting shortcuts.  Positive semidefiniteness
of the heat covariance does not impose a production sign, and a cubic term
cannot be absorbed at the same time by the declared positive quadratic row
with an amplitude-independent coefficient.

None of these statements proves regularity.  The heat-characteristic payment
uses signed cancellation, while the absolute estimate loses \(s^{-1/4}\).
The next mathematically relevant question is whether localization, rather
than a stronger global mean identity, can convert this structure into a
scale-critical criterion without assuming the desired regularity in advance.
