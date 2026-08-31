# R0.73U analytic proof: a full-tensor heat hierarchy and its non-autonomy

**Status:** parent derivation and independent analytic readback agree; the
formal finite certificate and publication package remain release gates

**Ordinary translation path:** `LOCAL_DIRECT_NO_DGX`

## 1. Setting and conventions

Work on \(\mathbb T^3=[0,2\pi]^3\) with normalized Haar measure.  Let
\(u\) be a smooth real mean-zero divergence-free solution of

\[
 \partial_tu+(u\cdot\nabla)u+\nabla p=\nu\Delta u,
 \qquad \nabla\cdot u=0.
 \tag{1.1}
\]

The mean-zero pressure is fixed by

\[
 -\Delta p=\partial_i\partial_j(u_i u_j).
 \tag{1.2}
\]

For \(h\ne0\), the Fourier convention
\(\widehat f(h)=\int f(x)e^{-ih\cdot x}\,d\mu(x)\) gives

\[
 \widehat p(h)
 =-{h_i h_j\over |h|^2}\widehat{u_i u_j}(h).
 \tag{1.3}
\]

Equivalently, if \(R_j=\partial_j(-\Delta)^{-1/2}\), then
\(p=R_iR_j(u_i u_j)\).

For \(s\ge0\), put

\[
 P_s=e^{s\Delta},\qquad
 v_s=P_su,\qquad
 \Theta_s=P_s(u\otimes u),\qquad
 \tau_s=\Theta_s-v_s\otimes v_s,
 \qquad p_s=P_sp.
 \tag{1.4}
\]

Tensor pointwise norms below are Frobenius norms.  Finite component sums are
absorbed into the stated periodic Riesz/Stokes constants.

## 2. Positivity and the exact scale law

### Proposition 2.1: heat covariance structure

For every \(s\ge0\), \(\Theta_s\) and \(\tau_s\) are symmetric positive
semidefinite at each \((x,t)\).  Moreover,

\[
 \boxed{
 \partial_s\tau_s
 =\Delta\tau_s
 +2\sum_{\ell=1}^3
   (\partial_\ell v_s)\otimes(\partial_\ell v_s),
 \qquad \tau_0=0.}
 \tag{2.1}
\]

Consequently,

\[
 \boxed{
 \tau_s
 =2\int_0^sP_{s-r}
  \left[\sum_{\ell=1}^3
  (\partial_\ell v_r)\otimes(\partial_\ell v_r)\right]dr.}
 \tag{2.2}
\]

#### Proof

The periodic heat kernel is nonnegative and has mass one.  For every fixed
\(a\in\mathbb R^3\),

\[
 a^T\Theta_sa=P_s((a\cdot u)^2)\ge0
 \tag{2.3}
\]

and Jensen gives

\[
 a^T\tau_sa
 =P_s((a\cdot u)^2)-(P_s(a\cdot u))^2\ge0.
 \tag{2.4}
\]

Thus both tensors are symmetric positive semidefinite.  Since
\(\partial_s\Theta_s=\Delta\Theta_s\) and
\(\partial_sv_s=\Delta v_s\), the product rule gives

\[
\begin{aligned}
 \partial_s\tau_s
 &=\Delta\Theta_s-(\Delta v_s)\otimes v_s
   -v_s\otimes(\Delta v_s)\\
 &=\Delta\tau_s
   +\Delta(v_s\otimes v_s)
   -(\Delta v_s)\otimes v_s-v_s\otimes(\Delta v_s)\\
 &=\Delta\tau_s
   +2\sum_\ell(\partial_\ell v_s)\otimes
                    (\partial_\ell v_s).
\end{aligned}
 \tag{2.5}
\]

Equation (2.2) is Duhamel's formula in the scale variable.  \(\square\)

The same semigroup algebra also gives the exact two-level identity

\[
 \boxed{
 \tau_{s+r}(u)=P_r\tau_s(u)+\tau_r(P_su),
 \qquad r,s\ge0.}
 \tag{2.6}
\]

This is a heat-semigroup version of the filtering identity.  It organizes
scales, but it does not express \(\tau_s\) as a function of the single field
\(v_s\).

## 3. Same-scale pressure and the filtered equation

The heat semigroup commutes with derivatives and periodic Riesz transforms.
Therefore

\[
 \boxed{
 p_s=R_iR_j\Theta_{s,ij}
 =R_iR_j(v_{s,i}v_{s,j}+\tau_{s,ij}).}
 \tag{3.1}
\]

Thus the full local-product tensor retains the polarization that the scalar
trace in R0.73T lost.  Filtering (1.1) gives

\[
 \boxed{
 \partial_tv_s
 +\mathbb P\nabla\!\cdot(v_s\otimes v_s+\tau_s)
 =\nu\Delta v_s.}
 \tag{3.2}
\]

In primitive variables,

\[
 \partial_tv_s+(v_s\cdot\nabla)v_s+\nabla\!\cdot\tau_s+\nabla p_s
 =\nu\Delta v_s.
 \tag{3.3}
\]

The resolved local energy identity is

\[
 \boxed{
 \partial_t{|v_s|^2\over2}
 +\nabla\!\cdot\left[
   \left({|v_s|^2\over2}+p_s\right)v_s+\tau_sv_s\right]
 =\nu\Delta{|v_s|^2\over2}-\nu|\nabla v_s|^2
  +\tau_s:\nabla v_s.}
 \tag{3.4}
\]

Writing \(\Pi_s=-\tau_s:\nabla v_s\), the last term is \(-\Pi_s\).
Although \(\tau_s\) is positive semidefinite, \(\Pi_s\) has no fixed sign:
the incompressible strain is trace-free and generally indefinite.  Positivity
of the covariance is therefore not an eddy-viscosity closure.

## 4. Critical product-space compatibility

Let \(I\) be a time interval and

\[
 E(I)=L^4(I;L^6(\mathbb T^3)).
 \tag{4.1}
\]

For a positive semidefinite matrix \(A\), \(|A|_F\le\operatorname{tr}A\).
Equations (2.3)--(2.4) therefore give the pointwise bounds

\[
 |\Theta_s|_F\le P_s|u|^2,
 \qquad
 |\tau_s|_F\le\operatorname{tr}\tau_s
 \le P_s|u|^2.
 \tag{4.2}
\]

Heat contraction and H\"older imply the uniform critical row

\[
 \boxed{
 \sup_{s\ge0}\|\Theta_s\|_{L_t^2L_x^3(I)}
 \le\|u\|_{E(I)}^2,
 \qquad
 \sup_{s\ge0}\|\tau_s\|_{L_t^2L_x^3(I)}
 \le\|u\|_{E(I)}^2.}
 \tag{4.3}
\]

For a periodic double-Riesz constant \(C_R\), (3.1) also gives

\[
 \boxed{
 \sup_{s\ge0}\|p_s\|_{L_t^2L_x^3(I)}
 \le C_R\|u\|_{E(I)}^2.}
 \tag{4.4}
\]

Define the causal Stokes map

\[
 \mathcal S_\nu F(t)
 =\int_{t_0}^t e^{\nu(t-r)\Delta}
   \mathbb P\nabla\!\cdot F(r)\,dr.
 \tag{4.5}
\]

The same periodic heat-kernel and one-dimensional HLS proof used in R0.73Q
gives, for fixed \(\nu>0\),

\[
 \|\mathcal S_\nu F\|_{E(I)}
 \le C_{B,\nu}\|F\|_{L_t^2L_x^3(I)}.
 \tag{4.6}
\]

Hence

\[
 \boxed{
 \sup_{s\ge0}\|\mathcal S_\nu\tau_s\|_{E(I)}
 \le C_{B,\nu}\|u\|_{E(I)}^2.}
 \tag{4.7}
\]

This is the precise positive answer to the exponent question: the tensor
stress occupies the same critical product space as \(u\otimes u\), and its
Stokes image returns to \(E\).  It is conditional and circular for the Clay
problem because its right-hand side already assumes the critical strong norm
\(u\in E\).  It creates no new arbitrary-data bound.

There is also an energy-only estimate at every fixed positive heat scale.  Fix
\(0<T<T_*\) inside the smooth lifespan and let

\[
 E_0=\|u(0)\|_2^2,
 \qquad
 H_3(s)=\|P_s\|_{L^1\to L^3}.
 \tag{4.8}
\]

The energy inequality and periodic mean-zero Sobolev inequality give

\[
 \|\tau_s\|_{L_t^1(0,T;L_x^3)}
 \le C_S^2\int_0^T\|\nabla u(t)\|_2^2dt
 \le {C_S^2E_0\over2\nu},
 \tag{4.9}
\]

while heat smoothing and the energy bound give

\[
 \|\tau_s\|_{L_t^\infty(0,T;L_x^3)}
 \le H_3(s)E_0.
 \tag{4.10}
\]

Interpolation in time yields

\[
 \boxed{
 \|\tau_s\|_{L_t^2(0,T;L_x^3)}^2
 \le {C_S^2H_3(s)\over2\nu}E_0^2.}
 \tag{4.11}
\]

On the three-dimensional torus, \(H_3(s)\lesssim s^{-1}\) for
\(0<s\le1\).  Thus the energy-only bound costs

\[
 \|\tau_s\|_{L_t^2(0,T;L_x^3)}
 \lesssim {E_0\over\sqrt{\nu s}}.
 \tag{4.12}
\]

The constant is independent of \(T<T_*\).  This is finite at every positive
scale but not uniform as \(s\downarrow0\).
It is the analytic version of the one-derivative heat loss later isolated by
the exact finite witness.  The word “critical” here refers to the Euclidean or
local parabolic exponent relation; it is not a literal invariance of normalized
fixed-torus covering dilations.

Combining (4.6) and (4.11) gives the corresponding fixed-scale Stokes output

\[
 \boxed{
 \|\mathcal S_\nu\tau_s\|_{E(0,T)}
 \le C_{B,\nu}
 \left({C_S^2H_3(s)\over2\nu}\right)^{1/2}E_0.}
 \tag{4.13}
\]

Thus the positive-scale forcing is controlled from energy through the same
critical Stokes row; the obstruction is precisely the nonuniform short-scale
factor.

## 5. A centered pressure-variance refinement of R0.73T

The full tensor also suggests a gauge-invariant refinement of the R0.73T
one-sided estimate.  Put

\[
 w=|u|^2,\quad Q=\int w^2d\mu,\quad
 X^2=\int|\nabla w|^2d\mu,\quad
 Y=\int w|\nabla u|^2d\mu.
 \tag{5.1}
\]

For every spatial constant \(c=c(t)\), incompressibility gives

\[
 \int c(t)u\cdot\nabla w\,d\mu=0.
 \tag{5.2}
\]

Define the weighted pressure variance

\[
 \bar p_w={\int wp\,d\mu\over\int w\,d\mu},
 \qquad
 \mathcal P_*=\int w(p-\bar p_w)^2d\mu,
 \tag{5.3}
\]

with the zero solution treated separately.  The exact quartic balance and
weighted Cauchy inequality give

\[
 \left|\int(p-\bar p_w)u\cdot\nabla w\,d\mu\right|
 \le\mathcal P_*^{1/2}X.
 \tag{5.4}
\]

Therefore, for every \(0<\vartheta\le2\), Young's inequality gives

\[
 \boxed{
 Q'+4\nu Y+(2-\vartheta)\nu X^2
 \le {4\over\vartheta\nu}\mathcal P_*.}
 \tag{5.5}
\]

If \(Q>0\), write \(\beta_*=\mathcal P_*/Q\).  At \(\vartheta=1\),

\[
 \boxed{
 Q'+4\nu Y+\nu X^2\le {4\over\nu}\beta_*Q.}
 \tag{5.6}
\]

This has the same left side as the R0.73T \(AQ\) estimate, while

\[
 \mathcal P_*
 \le\int wp^2d\mu
 \le\|p\|_3^2\|w\|_3
 \le C_R^2\|u\|_6^6
 \le C_R^2AQ.
 \tag{5.7}
\]

Thus \(\beta_*\le C_R^2A\): the centered variance bound is never worse and
is strict for examples such as pressure-free shears.  At \(\vartheta=2\),

\[
 Q'+4\nu Y\le {2\over\nu}\beta_*Q.
 \tag{5.8}
\]

Consequently, \(\beta_*\in L^1_t\) bounds \(Q\) by Gronwall and then enters
the classical \(L_t^\infty L_x^4\) continuation route.  The time integral is
critical under Euclidean/local Navier--Stokes scaling.  This is an internal
centered corollary of the classical \(L^4\) pressure method, not a claimed new
regularity criterion.  Tran--Yu--Dritschel (JFM 2021) directly study the
closely related weighted pressure quantity
\(\int p^2|u|^{q-2}\) and velocity--pressure correlation coefficients.

## 6. Exact tensor heat-plane law

Put \(T_{ij}=u_i u_j\).  A direct product calculation from (1.1) gives

\[
 \partial_tT_{ij}
 =\nu\Delta T_{ij}
 -2\nu\partial_\ell u_i\,\partial_\ell u_j
 -\partial_k(u_k u_i u_j)
 -(u_j\partial_i p+u_i\partial_jp).
 \tag{6.1}
\]

Applying \(P_s\) and using \(\partial_s\Theta_s=\Delta\Theta_s\) yields

\[
 \boxed{
 (\partial_t-\nu\partial_s)\Theta_{s,ij}
 =-2\nu P_s(\partial_\ell u_i\,\partial_\ell u_j)
  -\partial_kP_s(u_k u_i u_j)
  -P_s(u_j\partial_i p+u_i\partial_jp).}
 \tag{6.2}
\]

The first term is even under \(u\mapsto-u\).  Pressure is quadratic and is
also unchanged, so the last two terms are odd.  The full tensor has repaired
instantaneous pressure reconstruction, but the signed third-order time tangent
has not become a function of the quadratic tensor data.

## 7. Exact four-site non-autonomy witness

Consider the real mean-zero divergence-free trigonometric polynomial

\[
 u(x,y,z)=
 \bigl(2\sin(x+y),\;2\sin x-2\sin(x+y),\;0\bigr).
 \tag{7.1}
\]

Its positive Fourier sites are

\[
 \widehat u(1,0,0)=(0,-i,0),
 \qquad
 \widehat u(1,1,0)=(-i,i,0),
 \tag{7.2}
\]

with conjugate coefficients at the two negative sites.  Let
\(h=(1,2,0)\).  Exact sparse convolution gives

\[
 \widehat T(h)=0,
 \qquad
 \widehat{\nu\Delta T-2\nu\partial_\ell u\otimes
 \partial_\ell u}(h)=0,
 \tag{7.3}
\]

while the nonlinear tensor tangent is

\[
 K=
 \begin{pmatrix}
 -2&1&0\\
 1&0&0\\
 0&0&0
 \end{pmatrix},
 \qquad |K|_F=\sqrt6.
 \tag{7.4}
\]

The exact certificate fixes \(K\) as the nonlinear contribution to
\(\partial_t\widehat T(h)\) for the field (7.1).  Therefore

\[
 \partial_t\widehat T(h;u)
 -\partial_t\widehat T(h;-u)=2K\ne0.
 \tag{7.5}
\]

For every \(s\ge0\), however,

\[
 \Theta_s(-u)=\Theta_s(u),\qquad
 \tau_s(-u)=\tau_s(u),\qquad
 p_s(-u)=p_s(u).
 \tag{7.6}
\]

At heat scale \(s\), (7.5) becomes

\[
 \boxed{
 \partial_t\widehat\Theta_s(h;u)
 -\partial_t\widehat\Theta_s(h;-u)
 =2e^{-5s}K.}
 \tag{7.7}
\]

Thus no single-valued autonomous evolution law based only on the complete
quadratic state \(\{\Theta_s,\tau_s,p_s:s\ge0\}\) can recover the signed
tensor tangent for all smooth divergence-free fields.  This statement does
not apply after the signed velocity is added to the state.

## 8. Parabolic-scale derivative cost

For an integer \(L\ge1\), let \(u_L(x)=u(Lx)\) and
\(h_L=(L,2L,0)\).  Spatial differentiation multiplies the nonlinear tangent
by \(L\), while heat filtering contributes
\(e^{-s|h_L|^2}=e^{-5sL^2}\).  Hence

\[
 \partial_t\widehat\Theta_s(h_L;u_L)
 -\partial_t\widehat\Theta_s(h_L;-u_L)
 =2Le^{-5sL^2}K.
 \tag{8.1}
\]

At \(s=\theta L^{-2}\), \(\theta>0\), its Frobenius size is

\[
 \boxed{
 2\sqrt6\,Le^{-5\theta}
 =2\sqrt{6\theta}\,e^{-5\theta}s^{-1/2}.}
 \tag{8.2}
\]

The normalized profile \(2\sqrt{6\theta}e^{-5\theta}\) is maximal at
\(\theta=1/10\).  Equation (8.2) proves a one-derivative cost for recovering
this coefficient's signed tangent from a fixed parabolic heat slice.  It does
not rule out time integration, an explicitly signed cubic state, or other
cancellations.

## 9. Relation to KHM and filtering literature

The tensor in (1.4) is a heat-filtered local product.  It is not the classical
two-point covariance

\[
 R_{ij}(r)=\int u_i(x)u_j(x+r)\,d\mu(x).
 \tag{9.1}
\]

The scalar trace of the homogeneous KHM equation can cancel pressure after
spatial or ensemble averaging, but a third-order increment flux remains.  The
full KHM tensor equation contains third-order moments and pressure--velocity
correlations.  Those facts agree with (5.2): changing the quadratic tensor
representation can move the pressure term, but it does not remove the signed
third-order hierarchy.

Germano's filtering identities and exact subgrid-stress formulae organize the
same scale structure as (2.6).  Constantin--E--Titi and Duchon--Robert
commutator/defect formulae likewise identify a signed third-order increment as
the energy-transfer object.  R0.73U uses these as attribution and collision
boundaries, not as a claim that the four-site parity witness appears in those
papers.

## 10. Exact conclusion

The full tensor heat hierarchy achieves three things that scalar R0.73T data
could not:

1. it preserves pressure polarization at every heat scale;
2. it yields a positive covariance stress with an exact scale evolution;
3. it stays in the critical \(L_t^2L_x^3\to L_t^4L_x^6\) Stokes row.

It does not close the dynamics.  The exact time law contains signed cubic
transport and pressure--velocity terms, and the four-site sign pair proves
that no quadratic-tensor-only autonomous law can recover that tangent.  The
missing object is now sharply identified: a signed third-order flux or an
equivalent phase-sensitive augmentation.  Arbitrary three-dimensional global
regularity remains open.
