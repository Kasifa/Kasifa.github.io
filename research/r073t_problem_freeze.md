# R0.73T problem freeze: dynamic autocorrelation and the pressure-tensor barrier

**Frozen date:** 2026-08-31

**Domain:** the normalized periodic torus \(\mathbb T^3=[0,2\pi]^3\),
with normalized Haar measure \(d\mu=(2\pi)^{-3}dx\), viscosity \(\nu>0\),
and a smooth real mean-zero divergence-free Navier--Stokes solution on an
interval on which it exists smoothly

**Dependencies:** the R0.73Q stability-tube entrance, the R0.73R
LP--caloric equivalence, and the R0.73S quadratic autocorrelation certificate

## 1. Frozen question

R0.73S produced a static sufficient upper certificate for a sixth moment.
R0.73T asks exactly how far the same scalar autocorrelation data can be
transported through Navier--Stokes dynamics.  The bounded questions are:

1. What is the exact evolution of
   \(C(h,t)=\widehat{|u(t)|^2}(h)\) and
   \(Q(t)=\sum_h|C(h,t)|^2=\|u(t)\|_4^4\)?
2. Does the R0.73S estimate \(\|u\|_6^6\le A Q\),
   \(A=\sum_h|C(h)|\), yield a valid differential inequality?
3. Does that inequality close at critical scaling, or does it merely
   repackage a classical critical regularity budget?
4. Can a shellwise or heat-weighted version repair the information lost by
   scalar autocorrelation, and what exact forcing remains?

The target is an auditable positive estimate together with a sharp closure
boundary.  It is not an a priori global estimate from the Leray energy class.

## 2. Frozen notation and Fourier convention

For a scalar or vector field \(f\), use

\[
 \widehat f(h)=\int_{\mathbb T^3}f(x)e^{-ih\cdot x}\,d\mu(x),
 \qquad d\mu=(2\pi)^{-3}dx.
 \tag{2.1}
\]

Put

\[
 w=|u|^2,
 \qquad C(h)=\widehat w(h),
 \qquad Q=\sum_h|C(h)|^2=\|u\|_4^4,
 \qquad A=\sum_h|C(h)|,
 \tag{2.2}
\]

and

\[
 X^2=\|\nabla w\|_2^2,
 \qquad Y=\int_{\mathbb T^3}w|\nabla u|^2\,d\mu.
 \tag{2.3}
\]

For a real self-adjoint Littlewood--Paley projection \(P_j\) to a fixed
annulus \(|k|\asymp\lambda_j=2^j\), define

\[
 u_j=P_ju,
 \qquad N_j=P_j\mathbb P\nabla\!\cdot(u\otimes u),
 \qquad \partial_tu_j=\nu\Delta u_j-N_j,
 \tag{2.4}
\]

\[
 e_j=|u_j|^2,
 \quad C_j(h)=\widehat{e_j}(h),
 \quad Q_j=\sum_h|C_j(h)|^2=\|u_j\|_4^4,
 \quad A_j=\sum_h|C_j(h)|,
 \tag{2.5}
\]

\[
 Y_j=Q_j^{1/2}=\|u_j\|_4^2,
 \quad X_j=Q_j^{1/4}=\|u_j\|_4,
 \quad F_j=\|N_j\|_2,
 \tag{2.6}
\]

and

\[
 \mathcal D_j
 :=-\int\Delta u_j\cdot |u_j|^2u_j\,d\mu
 =\int |u_j|^2|\nabla u_j|^2\,d\mu
  +{1\over2}\int|\nabla |u_j|^2|^2\,d\mu.
 \tag{2.7}
\]

All exact identities are first checked for finite Fourier fields and then
extended to smooth solutions by approximation.

## 3. Exact full-field identities

The scalar energy-density equation is

\[
 \partial_tw
 =\nu\Delta w-2\nu|\nabla u|^2
  -\nabla\!\cdot\bigl(u(w+2p)\bigr),
 \tag{3.1}
\]

and hence

\[
 \boxed{
 \partial_tC(h)
 =-\nu|h|^2C(h)-2\nu\widehat{|\nabla u|^2}(h)
  -ih\cdot\widehat{u(w+2p)}(h).}
 \tag{3.2}
\]

Multiplying (3.1) by \(2w\), using periodicity and
\(\nabla\cdot u=0\), gives

\[
 \boxed{
 Q'+4\nu Y+2\nu X^2
 =4\int_{\mathbb T^3}p\,u\cdot\nabla w\,d\mu.}
 \tag{3.3}
\]

The factors, signs, complex conjugates and normalization in (3.2)--(3.3)
are part of the analytic gate.

Equation (3.2) contains two distinct information gaps.  Even if \(p\) were
supplied, scalar \(C\) does not determine the signed vector flux
\(u(w+2p)\).  Separately, reconstructing \(p\) in general requires

\[
 T_{ij}=u_i u_j,
 \qquad p=R_iR_jT_{ij},
 \qquad C=\widehat{\operatorname{tr}T},
 \tag{3.4}
\]

so the scalar trace data do not contain the full pressure tensor.  These two
obstructions must not be conflated.

## 4. Primary positive theorem: a one-sided dynamic \(AQ\) inequality

Let \(C_R\) denote a valid \(L^3(\mathbb T^3)\) operator bound, with the
finite tensor-component sum absorbed, for the periodic double-Riesz pressure
operator \(p=R_iR_j(u_i u_j)\).  Then

\[
 \|p\|_3\le C_R\|u\|_6^2
 \tag{4.1}
\]

and Hölder plus Young give

\[
 4\left|\int p\,u\cdot\nabla w\,d\mu\right|
 \le \nu X^2+{4C_R^2\over\nu}\|u\|_6^6.
 \tag{4.2}
\]

The R0.73S certificate \(\|u\|_6^6\le A Q\) therefore yields

\[
 \boxed{
 Q'+4\nu Y+\nu X^2
 \le {4C_R^2\over\nu}A Q.}
 \tag{4.3}
\]

Consequently, whenever \(A\in L^1(0,T)\),

\[
 Q(t)\le Q(0)
 \exp\!\left({4C_R^2\over\nu}\int_0^tA(s)\,ds\right).
 \tag{4.4}
\]

This is a genuine dynamic use of the R0.73S static certificate, but not a
new global regularity theorem.  Under the Navier--Stokes scaling,
\(A^{[\lambda]}(t)=\lambda^2A(\lambda^2t)\), so \(\int A\,dt\) is critical.
Moreover

\[
 \|u(t)\|_\infty^2=\||u(t)|^2\|_\infty\le A(t),
 \tag{4.5}
\]

so \(A\in L_t^1\) is at least as restrictive as, and directly implies, the
classical endpoint Serrin budget \(u\in L_t^2L_x^\infty\).  Equation (4.3)
exposes the missing critical
budget; it does not produce it.

## 5. Shellwise transport and the unresolved forcing

Define

\[
 G_j(h)=\widehat{|\nabla u_j|^2}(h),
 \qquad H_j(h)=\widehat{u_j\cdot N_j}(h).
 \tag{5.1}
\]

Then

\[
 \boxed{
 \partial_tC_j(h)
 =-\nu|h|^2C_j(h)-2\nu G_j(h)-2H_j(h),}
 \tag{5.2}
\]

and equivalently

\[
 \boxed{
 {1\over4}Q_j'+\nu\mathcal D_j
 =-\int |u_j|^2u_j\cdot N_j\,d\mu.}
 \tag{5.3}
\]

The periodic scalar frequency-localized nonlinear Bernstein inequality at
\(p=4\), applied componentwise and combined with
\((\sum_i u_{j,i}^2)^2\le3\sum_i u_{j,i}^4\), gives a cutoff-dependent
constant \(c_{\rm B}>0\) such that

\[
 \mathcal D_j\ge c_{\rm B}\lambda_j^2Q_j.
 \tag{5.4}
\]

This is classical input, not an R0.73T novelty.  Hölder and R0.73S give

\[
 \left|\int |u_j|^2u_j\cdot N_j\,d\mu\right|
 \le\|u_j\|_6^3F_j
 \le(A_jQ_j)^{1/2}F_j.
 \tag{5.5}
\]

At positive \(Y_j\), and in the upper-Dini sense at its zeros,

\[
 \boxed{
 Y_j'+2\nu c_{\rm B}\lambda_j^2Y_j
 \le2A_j^{1/2}F_j.}
 \tag{5.6}
\]

Thus, for \(s\le t\),

\[
 \boxed{
 Y_j(t)\le e^{-2\nu c_{\rm B}\lambda_j^2(t-s)}Y_j(s)
 +2\int_s^t e^{-2\nu c_{\rm B}\lambda_j^2(t-r)}
 A_j(r)^{1/2}F_j(r)\,dr.}
 \tag{5.7}
\]

If \(D_{C,j}=|\operatorname{supp}C_j|\) is finite, then
\(A_j\le\sqrt{D_{C,j}Q_j}=D_{C,j}^{1/2}X_j^2\).  Dividing (5.3) by
\(X_j^3\) gives the complementary branch

\[
 \boxed{
 X_j'+\nu c_{\rm B}\lambda_j^2X_j
 \le D_{C,j}^{1/4}F_j,}
 \tag{5.8}
\]

again interpreted by upper Dini derivatives through zeros.  Hence

\[
 \boxed{
 X_j(t)\le e^{-\nu c_{\rm B}\lambda_j^2(t-s)}X_j(s)
 +D_{C,j}^{1/4}\int_s^t
 e^{-\nu c_{\rm B}\lambda_j^2(t-r)}F_j(r)\,dr.}
 \tag{5.9}
\]

Writing the right side of (5.9) as \(\mathcal X_j(t;s)\) and using
\(D_{C,j}\le D_{\Delta,j}\), the R0.73S caloric proxy obeys the formal
final-time budget

\[
 \lambda_j^{-2}(A_jQ_j)^{2/3}
 \le \lambda_j^{-2}D_{\Delta,j}^{1/3}
       \mathcal X_j(t;s)^4.
 \tag{5.10}
\]

The remaining forcing has the elementary alternatives

\[
 F_j\lesssim\lambda_j\|u\|_4^2,
 \qquad
 F_j\lesssim\lambda_j^{5/2}\|u\|_2^2.
 \tag{5.11}
\]

The first reintroduces a classical critical/strong norm; the second is
energy-only but supercritical in the shell index.  Therefore (5.7)--(5.10)
are auditable conditional transports, not a closure from Leray energy.

## 6. Exact non-closure witnesses

### 6.1 Carrier-scale loss already in the heat equation

For an integer \(N\ge1\), put

\[
 v_N(x)=\bigl(0,\cos(Nx_1),\sin(Nx_1)\bigr).
 \tag{6.1}
\]

Then \(v_N\) is real, mean zero, divergence free,
\((v_N\cdot\nabla)v_N=0\), and

\[
 |v_N|^2\equiv1,
 \qquad C_N(h)=\mathbf1_{h=0},
 \qquad A_N=Q_N=1.
 \tag{6.2}
\]

Its exact solution is \(v_N(t)=e^{-\nu N^2t}v_N\), so

\[
 \dot C_N(0,0)=-2\nu N^2,
 \qquad Q_N'(0)=-4\nu N^2.
 \tag{6.3}
\]

Thus complete unweighted scalar autocorrelation does not determine its own
derivative: it loses the absolute carrier scale.

### 6.2 Signed velocity-phase loss in the pressure pairing

There is also an explicit six-mode, real, divergence-free annular field
\(u_L\), recorded and exactly certified in the R0.73T no-go audit, for which

\[
 \mathcal E=42,
 \qquad Q=2918,
 \qquad A=164,
 \qquad D_C=15
 \tag{6.4}
\]

are independent of the dilation parameter \(L\), while the pressure work is

\[
 \mathcal N_4(u_L)=-384L,
 \qquad \mathcal N_4(-u_L)=+384L.
 \tag{6.5}
\]

The pair \(u_L,-u_L\) has identical complete \(C\), not merely identical
summaries.  More strongly,

\[
 (-u_L)\otimes(-u_L)=u_L\otimes u_L,
 \qquad p[-u_L]=p[u_L].
 \tag{6.6}
\]

Thus the sign change in (6.5) comes solely from the signed velocity factor
in \(p\,u\cdot\nabla w\), equivalently in the flux \(u(w+2p)\).  This
certificate isolates velocity-phase information absent from scalar \(C\);
because the tensor and pressure are the same for the pair, it does not by
itself prove pressure-tensor-polarization non-identifiability.  The general
pressure-tensor barrier is instead the formula-level fact (3.4).  The
stronger negative viscous term, of order \(-\nu L^2\), keeps (6.5) fully
compatible with the one-sided inequality (4.3).

These witnesses are smooth trigonometric polynomials.  They are neither
singular examples nor evidence for blow-up.

## 7. Gate and exact exclusions

R0.73T may close only after independent checks establish:

1. the coefficient evolution (3.2), quartic identity (3.3), and constants
   in (4.3);
2. a primary-source-supported periodic scalar inequality and the explicit
   componentwise deduction of (5.4);
3. the Dini/zero handling and integrated inequalities (5.7), (5.9);
4. exact rational reconstruction of the witnesses in Section 6;
5. a source/claim matrix distinguishing classical input, local proof,
   finite computation, and open closure claims.

R0.73T will not claim:

- a new \(L^p\) energy method, Riesz estimate, Serrin criterion, or
  frequency-localized Bernstein inequality;
- that \(C\), \(Q\), \(A Q\), or their shellwise analogues form an
  autonomous closed system;
- control of \(\int A\,dt\) or of shell forcing from Leray energy;
- a new regularity theorem, a blow-up obstruction, or progress resolving
  the Clay Millennium problem.
