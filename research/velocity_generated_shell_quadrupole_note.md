# R0.69K — Velocity-generated shell quadrupoles gain two derivatives

## 1. Result

R0.69J treated a general scalar pressure source and found that zero mass and
zero dipole do not remove its leading \(R^{-3}\) quadrupole. The actual
Navier--Stokes pressure source has more structure. For a smooth
divergence-free velocity,

\[
 q:=\operatorname{tr}((\nabla u)^2)
   =\partial_i\partial_j(u_i u_j),\qquad -\Delta p=q.
 \tag{1.1}
\]

Choose a smooth, nonnegative, locally finite partition of unity
\(\sum_m\chi_m=1\), with
each \(\chi_m\) supported on a dyadic spatial shell, and define

\[
 T^{(m)}_{ij}:=\chi_m u_i u_j,\qquad
 q_m:=\partial_i\partial_jT^{(m)}_{ij}.
 \tag{1.2}
\]

Then the decomposition is exact:

\[
 \boxed{\sum_m q_m=q.}
 \tag{1.3}
\]

Every shell source separately has zero mass and zero dipole. If its support
lies at distance comparable to \(R_m\) from the observation point, then its
constant pressure Hessian satisfies

\[
 \boxed{
 Q^{(m)}_{ab}
 =\int \partial_i\partial_jK_{ab}(-y)\,
       \chi_m(y)u_i(y)u_j(y)\,dy,}
 \tag{1.4}
\]

where

\[
 K_{ab}(z)=\partial_a\partial_b\frac1{4\pi|z|}.
 \tag{1.5}
\]

Consequently,

\[
 \boxed{
 |Q^{(m)}|
 \le \frac{C}{R_m^5}
 \int_{\operatorname{supp}\chi_m}|u|^2\,dy.}
 \tag{1.6}
\]

This is two powers of shell distance better than the \(R_m^{-3}\) scalar
source estimate. It comes from the double-divergence identity (1.1), not from
a sign cancellation.

The \(R_m^{-5}\) power is sharp for anisotropic velocity packets. Thus
velocity generation repairs the scalar \(R^{-3}\) witness from R0.69J, but it
does not annihilate the shell quadrupole altogether.

## 2. Exact shell decomposition

Using \(\partial_i u_i=0\),

\[
 \begin{aligned}
 \partial_i\partial_j(u_i u_j)
 &=
 \partial_i\bigl((\partial_j u_i)u_j+u_i\partial_j u_j\bigr)\\
 &=\partial_i u_j\,\partial_j u_i
 =\operatorname{tr}((\nabla u)^2).
 \end{aligned}
 \tag{2.1}
\]

Linearity and \(\sum_m\chi_m=1\) give

\[
 \sum_m\partial_i\partial_j(\chi_m u_i u_j)
 =\partial_i\partial_j(u_i u_j).
 \tag{2.2}
\]

This is not the same as the naive scalar localization
\(\chi_m q\). Each \(q_m\) contains the cutoff commutators needed to make
(2.2) exact. They must not be discarded or estimated separately before the
double integration by parts.

Because \(T^{(m)}\) is compactly supported,

\[
 \int q_m\,dy=0,\qquad
 \int y_kq_m(y)\,dy=0.
 \tag{2.3}
\]

The second moment is the shell kinetic stress:

\[
 \boxed{
 \int y_a y_bq_m(y)\,dy
 =2\int \chi_m(y)u_a(y)u_b(y)\,dy.}
 \tag{2.4}
\]

Thus the first nontrivial scalar multipole is not arbitrary: it is twice a
positive-semidefinite energy tensor.

## 3. Far-field Hessian bound

Let \(p_m=(-\Delta)^{-1}q_m\). If the shell stays away from the observation
ball, integration by parts twice gives

\[
 \begin{aligned}
 \partial_a\partial_b p_m(0)
 &=\int K_{ab}(-y)\,
       \partial_i\partial_jT^{(m)}_{ij}(y)\,dy\\
 &=\int \partial_i\partial_jK_{ab}(-y)\,
       T^{(m)}_{ij}(y)\,dy.
 \end{aligned}
 \tag{3.1}
\]

Since

\[
 |\nabla^2K(z)|\le C|z|^{-5},
 \tag{3.2}
\]

(1.6) follows. For all shells outside radius \(R\),

\[
 \boxed{
 \left|\sum_{R_m\ge R}Q^{(m)}\right|
 \le \frac{C}{R^5}
 \sum_{R_m\ge R}\int\chi_m|u|^2
 \le \frac{C}{R^5}\|u\|_2^2.}
 \tag{3.3}
\]

No same-sign or Carleson hypothesis is required for this absolute tail
bound. The price is that the near shells and the cutoff-transition region
remain in the near-field pressure budget.

## 4. Exact anisotropic stress witness

The double-divergence structure improves the power but does not force the
coefficient to vanish. Suppress the factor \(4\pi\), place the packet center
at \(Re_1\), and differentiate the Newtonian Hessian. The two diagonal
velocity-stress channels give

\[
 \partial_1^2\nabla^2|x|^{-1}\big|_{Re_1}
 =\frac1{R^5}\operatorname{diag}(24,-12,-12),
 \tag{4.1}
\]

\[
 \partial_2^2\nabla^2|x|^{-1}\big|_{Re_1}
 =\frac1{R^5}\operatorname{diag}(-12,9,3).
 \tag{4.2}
\]

For the positive-semidefinite shell energy tensor

\[
 E=\operatorname{diag}(1,2,0),
 \tag{4.3}
\]

the normalized leading Hessian is

\[
 4\pi Q_R
 =\frac1{R^5}\operatorname{diag}(0,6,-6).
 \tag{4.4}
\]

Pairing it with \(S_0=\operatorname{diag}(1,-1,0)\) yields

\[
 \boxed{S_0:Q_R=-\frac{3}{2\pi R^5}\ne0.}
 \tag{4.5}
\]

This tensor is realizable as the leading energy tensor of smooth compactly
supported divergence-free packets. Take

\[
 u=(\partial_2\psi,-\partial_1\psi,0)
 \tag{4.6}
\]

with a separable even compactly supported stream function. The cross energy
vanishes. Using the same one-dimensional profile in \(x_1,x_2\) and choosing
the width ratio \(b/a=\sqrt2\) gives
\(\int u_2^2=2\int u_1^2\). Translating the packet to \(Re_1\) and expanding
the smooth kernel proves (4.4)--(4.5) at leading order. In particular, for
sufficiently large separation the exact smooth-packet coefficient is
nonzero.

## 5. Scaling and route decision

Under Navier--Stokes scaling, \(R^{-5}\|u\|_2^2\) has the same degree as a
pressure Hessian. The estimate is therefore scaling-consistent, not a global
subcritical a priori bound. Its gain is a separation gain: remote spatial
shells become small compared with a fixed observation scale.

R0.69K changes the route in two ways:

1. the scalar four-source witness from R0.69J is not admissible as a
   velocity-generated shell source under stress localization;
2. the admissible shell quadrupole is controlled absolutely by shell kinetic
   energy with an \(R_m^{-5}\) kernel, but the power is sharp and the
   coefficient has no universal sign.

The next step is a three-zone localized strain budget. R0.69L will retain a
near pressure region, a transition annulus, and the stress-localized far
tail. It will optimize the separation ratio and test whether the far
\(R^{-5}\) gain survives after the near Calderón--Zygmund and boundary-flux
terms are placed at the same scale.

R0.69K gives no Navier--Stokes regularity or singularity conclusion and does
not solve the Millennium Problem.
