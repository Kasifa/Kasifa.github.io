# R0.70R — A sharp near-rank-one diffusion deficit and the remaining enstrophy barrier

**Status:** internal canonical candidate; not a public theorem chapter

**Release:** R0.70R

**Date:** 2026-08-25

## 1. Decision

R0.70Q proved that spectral curvature is exactly absorbed by projected
gradient covariance when the filtered covariance has rank one.  R0.70R
quantifies the loss of that absorption away from the rank-one stratum.

The finite-dimensional result is exact and sharp.  Put

\[
 \rho=\frac{\lambda_2}{\lambda_1}<1,
 \qquad
 c(\rho)=\frac{\sqrt\rho}{1-\sqrt\rho}.
 \tag{1.1}
\]

For the quantities defined below,

\[
 \boxed{
 \mathcal D_P-\mathcal K_Q
 \geq-c(\rho)\mathcal G.}
 \tag{1.2}
\]

Here \(\mathcal D_P\) is the projected block-gradient density,
\(\mathcal K_Q\) is the half-curvature convention of R0.70Q, and
\(\mathcal G\) is the full block-gradient density.  The constant in (1.2)
cannot be reduced.  A two-frequency divergence-free periodic vorticity
realizes equality at one point for the pinned real-even tight frame and is
realized by a smooth global Navier--Stokes shear heat flow.

If

\[
 \eta=\frac{r}{E}<\frac12,
 \tag{1.3}
\]

then

\[
 \rho\leq\frac{\eta}{1-\eta}
 \tag{1.4}
\]

and hence

\[
 \boxed{
 \mathcal D_P-\mathcal K_Q
 \geq
 -\frac{\sqrt\eta}
        {\sqrt{1-\eta}-\sqrt\eta}\,\mathcal G.}
 \tag{1.5}
\]

This is genuine progress on the propagation ledger: the two diffusion terms
must not be estimated separately, and their entire possible positive error
is small of order \(\sqrt\eta\) near the aligned stratum.

It does not close the Navier--Stokes problem.  The right side of (1.5)
contains the full block-gradient density; after spatial integration,
tightness identifies it with \(\|\nabla\omega\|_2^2\).  That is enstrophy
dissipation, one derivative above the kinetic-energy ledger.  The exact
inequality therefore converts an uncontrolled spectral denominator into a
quantified enstrophy-level error; it does not convert it into an energy-level
estimate.

No DNS or DGX computation is needed for this exact gate.  No public-page
update or GitHub publication is authorized by this report.

## 2. Covariance notation

Use the fixed complete real-even scalar frame from R0.70P.  At a point where
the top eigenvalue of

\[
 Q=\sum_\alpha\Omega_\alpha\otimes\Omega_\alpha,
 \qquad
 \Omega_\alpha=T_\alpha\omega,
 \tag{2.1}
\]

is simple, write

\[
 \lambda_1>\lambda_2\geq\lambda_3\geq0,
 \qquad
 L=v_1\otimes v_1,
 \qquad
 P=I-L.
 \tag{2.2}
\]

The residual and total covariance energy are

\[
 r=\lambda_2+\lambda_3,
 \qquad
 E=\lambda_1+\lambda_2+\lambda_3.
 \tag{2.3}
\]

Let

\[
 \mathcal R_Q
 =P(\lambda_1I-Q)^{-1}P
 \tag{2.4}
\]

be the reduced resolvent, and retain the R0.70Q half-curvature convention

\[
 \mathcal K_Q
 =\sum_k
  \left(P(\partial_kQ)v_1\right)^{\mathsf T}
  \mathcal R_Q
  \left(P(\partial_kQ)v_1\right).
 \tag{2.5}
\]

Define

\[
 \mathcal D_P
 =\sum_{\alpha,k}|P\partial_k\Omega_\alpha|^2,
 \tag{2.6}
\]

\[
 \mathcal D_L
 =\sum_{\alpha,k}|L\partial_k\Omega_\alpha|^2,
 \tag{2.7}
\]

and

\[
 \mathcal G
 =\mathcal D_P+\mathcal D_L
 =\sum_{\alpha,k}|\partial_k\Omega_\alpha|^2.
 \tag{2.8}
\]

The residual equation from R0.70Q contains the net diffusion contribution

\[
 -2\nu\mathcal D_P+2\nu\mathcal K_Q
 =-2\nu(\mathcal D_P-\mathcal K_Q).
 \tag{2.9}
\]

## 3. Coefficient-space decomposition

Let \(\mathbb H=\ell^2(\mathcal I;\mathbb R)\) be the frame-index Hilbert
space.  Decompose each block at the point as

\[
 a_\alpha=v_1\cdot\Omega_\alpha,
 \qquad
 b_\alpha=P\Omega_\alpha.
 \tag{3.1}
\]

Let \(a=(a_\alpha)\in\mathbb H\), and define

\[
 B:\mathbb H\longrightarrow\operatorname{Ran}P,
 \qquad
 Bz=\sum_\alpha z_\alpha b_\alpha.
 \tag{3.2}
\]

The eigenvector equation \(Qv_1=\lambda_1v_1\) gives

\[
 \|a\|_{\mathbb H}^2=\lambda_1,
 \qquad
 Ba=0.
 \tag{3.3}
\]

Moreover,

\[
 BB^{\mathsf T}=PQP,
 \qquad
 \|B\|_{\mathrm{op}}^2=\lambda_2.
 \tag{3.4}
\]

For each spatial index \(k\), put

\[
 c_{\alpha k}=v_1\cdot\partial_k\Omega_\alpha,
 \qquad
 h_{\alpha k}=P\partial_k\Omega_\alpha.
 \tag{3.5}
\]

Write \(c_k=(c_{\alpha k})\in\mathbb H\), and define

\[
 H_k:\mathbb H\longrightarrow\operatorname{Ran}P,
 \qquad
 H_kz=\sum_\alpha z_\alpha h_{\alpha k}.
 \tag{3.6}
\]

Then

\[
 \|H_k\|_{\mathrm{HS}}^2
 =\sum_\alpha|h_{\alpha k}|^2
 =:\mathcal D_{P,k},
 \tag{3.7}
\]

\[
 \|c_k\|_{\mathbb H}^2
 =\sum_\alpha|c_{\alpha k}|^2
 =:\mathcal D_{L,k}.
 \tag{3.8}
\]

Direct differentiation of (2.1) supplies the exact off-diagonal identity

\[
 \boxed{
 P(\partial_kQ)v_1=H_ka+Bc_k.}
 \tag{3.9}
\]

The term \(H_ka\) differentiates the principal block components in a
transverse direction.  The term \(Bc_k\) changes the longitudinal amplitudes
of already transverse block components.  The second mechanism is absent at
rank one and is the source of the near-rank-one absorption deficit.

## 4. Sharp near-rank-one theorem

### Theorem 4.1 — Quantitative diffusion-deficit bound

Let \(\mathcal I\) be finite or countable.  Assume

\[
 (\Omega_\alpha)_\alpha\in\ell^2(\mathcal I;\mathbb R^3),
 \qquad
 (\partial_k\Omega_\alpha)_\alpha
 \in\ell^2(\mathcal I;\mathbb R^3)
 \quad(k=1,2,3).
 \tag{4.0}
\]

Define \(Q\) and \(\partial_kQ\) by the corresponding norm-convergent
series

\[
 Q=\sum_\alpha\Omega_\alpha\otimes\Omega_\alpha,
 \qquad
 \partial_kQ
 =\sum_\alpha
 \left(
  \partial_k\Omega_\alpha\otimes\Omega_\alpha
  +\Omega_\alpha\otimes\partial_k\Omega_\alpha
 \right).
 \tag{4.0a}
\]

The derivative series converges absolutely in Frobenius norm by
Cauchy--Schwarz.  Suppose \(\lambda_1>\lambda_2\).  Then

\[
 \boxed{
 \mathcal K_Q
 \leq
 \frac{
  \left(
   \sqrt{\lambda_1\mathcal D_P}
   +\sqrt{\lambda_2\mathcal D_L}
  \right)^2}
 {\lambda_1-\lambda_2}.}
 \tag{4.1}
\]

Consequently, with \(\rho=\lambda_2/\lambda_1\),

\[
 \boxed{
 \mathcal D_P-\mathcal K_Q
 \geq
 -\frac{\sqrt\rho}{1-\sqrt\rho}
  \left(\mathcal D_P+\mathcal D_L\right).}
 \tag{4.2}
\]

The coefficient in (4.2) is optimal among all estimates depending only on
\(\rho\) and \(\mathcal G=\mathcal D_P+\mathcal D_L\).

### Proof

The reduced resolvent satisfies

\[
 0\leq\mathcal R_Q
 \leq\frac1{\lambda_1-\lambda_2}P.
 \tag{4.3}
\]

Equations (3.3)--(3.4), (3.7)--(3.9) give

\[
 \begin{aligned}
 |P(\partial_kQ)v_1|
 &\leq|H_ka|+|Bc_k|\\
 &\leq
 \sqrt{\lambda_1\mathcal D_{P,k}}
 +\sqrt{\lambda_2\mathcal D_{L,k}}.
 \end{aligned}
 \tag{4.4}
\]

Sum the square of (4.4) in \(k\), and use Cauchy--Schwarz on the mixed
sum.  Together with (4.3), this proves (4.1).

Let

\[
 X=\sqrt{\mathcal D_P},
 \qquad
 Y=\sqrt{\mathcal D_L}.
 \tag{4.5}
\]

Subtracting the right side of (4.1) from \(\mathcal D_P\) gives

\[
 \mathcal D_P-\mathcal K_Q
 \geq
 -\frac{
  \rho X^2+2\sqrt\rho\,XY+\rho Y^2}
 {1-\rho}.
 \tag{4.6}
\]

Equivalently, with \(s=\sqrt\rho\), the exact sum-of-squares identity is

\[
 \begin{aligned}
 &\mathcal D_P
 +\frac{s}{1-s}(\mathcal D_P+\mathcal D_L)
 -\frac{
  \left(\sqrt{\mathcal D_P}
        +s\sqrt{\mathcal D_L}\right)^2}
 {1-s^2}\\
 &\hspace{3em}
 =\frac{s
  \left(\sqrt{\mathcal D_P}
        -\sqrt{\mathcal D_L}\right)^2}
 {1-s^2}
 \geq0.
 \end{aligned}
 \tag{4.7}
\]

The same optimal coefficient is also the largest eigenvalue of

\[
 \frac1{1-\rho}
 \begin{pmatrix}
  \rho&\sqrt\rho\\
  \sqrt\rho&\rho
 \end{pmatrix}
 \tag{4.8}
\]

namely

\[
 \frac{\rho+\sqrt\rho}{1-\rho}
 =\frac{\sqrt\rho}{1-\sqrt\rho}.
 \tag{4.9}
\]

Applying this Rayleigh quotient to \(X^2+Y^2=\mathcal G\) proves (4.2).

For \(\rho=0\), equation (4.2) reduces to the exact rank-one absorption
\(\mathcal D_P-\mathcal K_Q\geq0\) from R0.70Q.

## 5. Exact sharpness inside the pinned frame

Work on normalized \(\mathbb T^3\).  Let \(v,w\) be orthonormal vectors in
the plane perpendicular to \(e_1\).  For the compactly supported annular
frame, choose positive integers \(k,\ell\) far enough apart that their active
filter-index sets

\[
 J_k=\{j:\varphi(2^{-j}ke_1)\ne0\},
 \qquad
 J_\ell=\{j:\varphi(2^{-j}\ell e_1)\ne0\}
 \tag{5.1}
\]

are disjoint.

Let \(A>\beta>0\) and \(p,q\in\mathbb R\).  Define the smooth mean-zero
divergence-free vorticity

\[
 \begin{aligned}
 \omega_0(x)
 ={}&
 A\cos(kx_1)v+\frac pk\sin(kx_1)w\\
 &+\beta\cos(\ell x_1)w+\frac q\ell\sin(\ell x_1)v.
 \end{aligned}
 \tag{5.2}
\]

At \(x_1=0\), real-evenness of the multipliers, disjointness of
\(J_k,J_\ell\), and tightness give

\[
 Q=A^2v\otimes v+\beta^2w\otimes w,
 \tag{5.3}
\]

\[
 (\lambda_1,\lambda_2,\lambda_3)=(A^2,\beta^2,0),
 \qquad
 \rho=\frac{\beta^2}{A^2},
 \tag{5.4}
\]

\[
 \mathcal D_P=p^2,
 \qquad
 \mathcal D_L=q^2,
 \tag{5.5}
\]

and

\[
 \mathcal K_Q
 =\frac{(Ap+\beta q)^2}{A^2-\beta^2}.
 \tag{5.6}
\]

Taking \(p=q\ne0\) yields

\[
 \frac{\mathcal K_Q-\mathcal D_P}{\mathcal G}
 =\frac{\beta}{A-\beta}
 =\frac{\sqrt\rho}{1-\sqrt\rho}.
 \tag{5.7}
\]

Thus every inequality in Theorem 4.1 is an equality for this datum, and the
coefficient cannot be lowered.

The construction is not merely an abstract covariance jet.  Since
\(\omega_0\) is smooth, mean zero, and divergence free,

\[
 u_0=\nabla\times(-\Delta)^{-1}\omega_0
 \tag{5.8}
\]

is a smooth periodic divergence-free velocity with
\(\nabla\times u_0=\omega_0\).  It has no \(e_1\) component and depends only
on \(x_1\), so

\[
 (u_0\cdot\nabla)u_0=0.
 \tag{5.9}
\]

The heat flow

\[
 u(t)=e^{\nu t\Delta}u_0
 \tag{5.10}
\]

is therefore a smooth global unforced Navier--Stokes solution.  Equality in
(5.7) holds at the initial time when \(p=q>0\).  More explicitly, if
\(\ell>k\) and \(t_*>0\), then

\[
 \begin{aligned}
 A_*&=Ae^{-\nu k^2t_*},
 &p_*&=pe^{-\nu k^2t_*},\\
 \beta_*&=\beta e^{-\nu\ell^2t_*},
 &q_*&=qe^{-\nu\ell^2t_*}.
 \end{aligned}
 \tag{5.11}
\]

Choosing

\[
 \frac pq=e^{-\nu(\ell^2-k^2)t_*}
 \tag{5.12}
\]

gives \(p_*=q_*\), while \(A>\beta\) ensures \(A_*>\beta_*\).  Equality can
therefore be arranged at any prescribed positive time.  The two frequencies
decay at different rates, so a single choice does not keep the equality
relation for all times.

## 6. Residual-ratio form

If \(E>0\) and

\[
 \eta=\frac rE<\frac12,
 \tag{6.1}
\]

then \(\lambda_1=E-r\), \(\lambda_2\leq r\), and

\[
 \rho=\frac{\lambda_2}{\lambda_1}
 \leq\frac{\eta}{1-\eta}.
 \tag{6.2}
\]

The function \(c(\rho)\) in (1.1) is increasing.  Theorem 4.1 therefore
gives

\[
 \boxed{
 \mathcal D_P-\mathcal K_Q
 \geq-c_\eta\mathcal G,
 \qquad
 c_\eta
 =\frac{\sqrt\eta}
        {\sqrt{1-\eta}-\sqrt\eta}.}
 \tag{6.3}
\]

The coefficient in (6.3) is also optimal: the example in Section 5 has
\(\lambda_3=0\), so
\(\rho=\eta/(1-\eta)\), and (5.7) attains equality.

In the residual equation,

\[
 \boxed{
 -2\nu\mathcal D_P+2\nu\mathcal K_Q
 \leq2\nu c_\eta\mathcal G.}
 \tag{6.4}
\]

The coefficient satisfies

\[
 c_\eta=\sqrt\eta+O(\eta)
 \qquad(\eta\downarrow0),
 \tag{6.5}
\]

and

\[
 c_\eta<1
 \quad\Longleftrightarrow\quad
 \eta<\frac15.
 \tag{6.6}
\]

These are algebraic statements.  They require pointwise control of
\(r/E\), not only the spatial integral \(R=\int r\).

## 7. Why the estimate still does not close

The trace equation contains the full negative term

\[
 -2\nu\mathcal G.
 \tag{7.1}
\]

After spatial integration, tightness and commutation with derivatives give

\[
 \int_{\mathbb T^3}\mathcal G\,dx
 =\sum_\alpha\|\nabla T_\alpha\omega\|_2^2
 =\|\nabla\omega\|_2^2.
 \tag{7.1a}
\]

Thus the error is exactly at the palinstrophy level.

For a constant \(\mu>0\), the diffusion part of the equation for

\[
 \Phi_\mu=r+\mu E
 \tag{7.2}
\]

obeys, on a region where \(\eta\leq\eta_0<1/2\),

\[
 \operatorname{Diff}(\mathscr L_\nu\Phi_\mu)
 \leq-2\nu\bigl(\mu-c_{\eta_0}\bigr)\mathcal G.
 \tag{7.3}
\]

Here \(\operatorname{Diff}\) denotes only the gradient-covariance and
spectral-curvature terms inherited from the residual and trace equations.
Thus \(\mu>c_{\eta_0}\) restores coercivity of this diffusion part only.

This observation is not a continuation theorem.  Since

\[
 \Phi_\mu\geq\mu E,
 \tag{7.4}
\]

a uniform-in-time bound on the spatial integral \(\int\Phi_\mu\) already
bounds the enstrophy
\(\|\omega\|_2^2\).  The stretching and filter-defect sources in the
\(\Phi_\mu\) equation remain uncontrolled by kinetic energy.  Simply
adding \(\mu E\) can therefore hide the target regularity inside the
functional one is trying to propagate.

The exact gain from R0.70R is narrower:

1. the spectral denominator no longer appears as an isolated positive term;
2. the absorption loss is quantified only by the normalized departure from
   rank one;
3. the resulting error is identified exactly as an enstrophy-dissipation
   error;
4. the coefficient and its square-root behavior cannot be improved without
   using more structure than \(\eta\) and \(\mathcal G\).

## 8. Next analytic gate

A productive continuation of this route must add information not used in
Theorem 4.1.  The next tests are:

1. exploit the common-vorticity origin
   \(\Omega_\alpha=T_\alpha\omega\) in the stretching and filter-defect
   terms, rather than treating the block jets independently;
2. determine whether the pointwise small-ratio region can be coupled to the
   large-ratio region by a truncation or entropy that uses only the spatial
   residual \(R\);
3. test whether the exact commutator square from R0.70Q supplies the missing
   control on the longitudinal derivative channel \(\mathcal D_L\);
4. reject any argument that bounds \(\mathcal G\) by assuming the target
   \(H^1\) continuation norm.

The first hard subproblem is now concrete: find a non-circular bound for

\[
 \int_{\{E>0,\ r/E\leq\eta_0\}}
 c_{r/E}\,\mathcal G\,dx
 \tag{8.1}
\]

together with the complementary large-residual region.  The set \(E=0\)
and the non-simple top-spectrum region require a separate
extension/regularization rule.  A different acceptable outcome would be an
exact Navier--Stokes-compatible family proving that the desired bound cannot
follow from the current ledger.

## 9. Claim boundary

What is proved:

- the coefficient-space identity (3.9);
- the exact inequalities (4.1)--(4.2);
- the optimal constant \(c(\rho)\);
- a fixed-frame divergence-free periodic sharpness datum;
- the residual-ratio form (6.3) and the combined diffusion observation
  (7.3).

What is not proved:

- propagation of a pointwise near-rank-one condition;
- control of the enstrophy-gradient error by kinetic energy;
- propagation of \(R\in L_t^2\), the exact commutator square, or the weighted
  direction cost;
- persistence of the sharp initial equality under Navier--Stokes evolution;
- global regularity or finite-time singularity.

The exact certificate for this release checks finite algebra, the sharp
Rayleigh quotient, and the two-frequency pointwise realization.  It does not
computer-prove the infinite-frame limit or any PDE propagation theorem.
