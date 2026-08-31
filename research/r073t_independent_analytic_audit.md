# R0.73T independent analytic audit: dynamic quadratic autocorrelation

**Audit date:** 2026-08-31

**Scope:** independent derivation for a smooth real mean-zero
divergence-free solution of the three-dimensional periodic incompressible
Navier--Stokes equations; exact Fourier autocorrelation evolution, the
quartic identity, viscous and nonlinear terms, shell and heat-filtered
versions, and closure boundaries

**Dependencies checked:** `r073s_problem_freeze.md`,
`r073s_quadratic_autocorrelation_certificate.md`,
`r073s_report-source.md`, `r073r_problem_freeze.md`,
`r073r_independent_analytic_audit.md`, and
`r073r_lp_caloric_certificate_proof.md`

**Verdict:** `EXACT_IDENTITIES_PASS__CRITICAL_DYNAMIC_CLOSURE_OPEN`

The exact evolution can be written with all coefficients and projections
fixed.  It gives a continuum-uniform differential inequality for
\(Q=\|u\|_4^4\), but the resulting closed ODE is superlinear and does not
prevent finite-time growth.  The sharper R0.73S inequality produces
\(Q'\lesssim A Q\), but no closed critical estimate for the Wiener factor
\(A\) follows from \((A,Q)\) or from the complete unweighted autocorrelation.
The obstruction is structural: unweighted autocorrelation loses the carrier
frequency and the velocity polarization needed by dissipation and pressure.

As a coefficient sanity check, a deterministic conjugate-symmetric finite
Fourier field was projected mode by mode onto (k^perp).  The nonlinear
term reconstructed from (3.1) and from the pressure-flux form (3.7) agreed
over every generated shift to (5.6\times10^{-15}); the two reconstructions
of the nonlinear contribution to (Q') agreed to (5.7\times10^{-14}).
This floating-point check is not used as proof, but it independently tests
the conjugates, pressure sign, and factors of two.  It used only the local
CPU and no DGX resource.

## 1. Fourier convention and reality constraints

Use Haar probability measure on \(\mathbb T^3=[0,2\pi]^3\) and

\[
 \widehat f(k)=\int_{\mathbb T^3}f(x)e^{-ik\cdot x}\,d\mu(x),
 \qquad
 f(x)=\sum_{k\in\mathbb Z^3}\widehat f(k)e^{ik\cdot x}.
 \tag{1.1}
\]

Let

\[
 u(x,t)=\sum_k a_k(t)e^{ik\cdot x}
 \tag{1.2}
\]

be a smooth real mean-zero divergence-free solution.  Thus

\[
 a_{-k}=\overline{a_k},\qquad k\cdot a_k=0,\qquad a_0=0.
 \tag{1.3}
\]

For complex vectors write
\(\langle z,w\rangle=z\cdot\overline w\).  Define

\[
 C_h(t)=\sum_k\langle a_{k+h},a_k\rangle .
 \tag{1.4}
\]

If \(g=|u|^2\), then

\[
 C_h=\widehat g(h),\qquad
 C_{-h}=\overline{C_h},\qquad C_0=\|u\|_2^2.
 \tag{1.5}
\]

The coefficients \(C_h\) need not be real when \(h\ne0\).  Smoothness
justifies all differentiations and rearrangements below.  The same identities
hold first for Galerkin solutions and then by smooth convergence.

Although the project fixes viscosity one, a parameter \(\nu>0\) is retained
below to audit every viscous coefficient.  Set \(\nu=1\) for R0.73T.

## 2. Exact Fourier Navier--Stokes equation

For \(k\ne0\), let

\[
 \mathbb P_k=I-{k\otimes k\over |k|^2},
 \qquad \mathbb P_0=I,
 \tag{2.1}
\]

and define

\[
 B_k=\sum_{p+q=k}(q\cdot a_p)a_q.
 \tag{2.2}
\]

Then \(iB_k\) is the Fourier coefficient of \((u\cdot\nabla)u\), and

\[
 \boxed{
 \dot a_k=-\nu|k|^2a_k-i\mathbb P_kB_k.}
 \tag{2.3}
\]

With the zero spatial mean of the pressure fixed to zero,

\[
 \widehat p(k)
 =-{k\cdot B_k\over |k|^2}
 =-{1\over |k|^2}
   \sum_{p+q=k}(k\cdot a_p)(k\cdot a_q),
 \qquad k\ne0.
 \tag{2.4}
\]

Indeed, \(q\cdot a_p=k\cdot a_p\) and
\(k\cdot a_q=p\cdot a_q\) by (1.3).  Thus
\(B_k+k\widehat p(k)=\mathbb P_kB_k\).

The Leray projector cannot be deleted term by term in a shifted
autocorrelation.  For example,

\[
 (k+h)\cdot a_k=h\cdot a_k
 \tag{2.5}
\]

need not vanish, so \(\mathbb P_{k+h}a_k\ne a_k\) in general.  Projection
cancels harmlessly in the total energy pairing \(h=0\), not in each
off-diagonal shift.

## 3. Exact evolution of every autocorrelation coefficient

Put \({\cal B}_k=\mathbb P_kB_k\).  Differentiating (1.4) and using (2.3)
gives

\[
\begin{aligned}
 \dot C_h
 ={}&-\nu\sum_k\bigl(|k+h|^2+|k|^2\bigr)
          \langle a_{k+h},a_k\rangle +{\cal N}_h,\\
 {\cal N}_h
 ={}&-i\sum_k {\cal B}_{k+h}\cdot\overline{a_k}
      +i\sum_k a_{k+h}\cdot\overline{{\cal B}_k}.
\end{aligned}
 \tag{3.1}
\]

Define

\[
 G_h=\sum_k (k+h)\cdot k\,
          \langle a_{k+h},a_k\rangle
      =\widehat{|\nabla u|^2}(h).
 \tag{3.2}
\]

Since

\[
 |k+h|^2+|k|^2=|h|^2+2(k+h)\cdot k,
 \tag{3.3}
\]

the viscous part of (3.1) is exactly

\[
 -\nu|h|^2C_h-2\nu G_h.
 \tag{3.4}
\]

There is also a useful physical-space form.  The local energy density obeys

\[
 \partial_t g
 =\nu\Delta g-2\nu|\nabla u|^2
  -\nabla\cdot\bigl(u(g+2p)\bigr).
 \tag{3.5}
\]

Hence, if

\[
 F_h=\widehat{u(g+2p)}(h)
     =\sum_\ell a_\ell
        \bigl(C_{h-\ell}+2\widehat p(h-\ell)\bigr),
 \tag{3.6}
\]

then the exact compact law is

\[
 \boxed{
 \dot C_h=-\nu|h|^2C_h-2\nu G_h-i h\cdot F_h.}
 \tag{3.7}
\]

Equations (3.1) and (3.7) are equivalent.  They also give the consistency
checks

\[
 \dot C_0=-2\nu\|\nabla u\|_2^2,
 \qquad
 \dot C_{-h}=\overline{\dot C_h}.
 \tag{3.8}
\]

The coefficient \(-2\nu G_h\) is essential.  Replacing the viscous term by
only \(-\nu|h|^2C_h\), or by \(-2\nu|h|^2C_h\), is incorrect.

## 4. Quartic identity and exact \(Q\)-evolution

Parseval gives the R0.73S bridge without any dimensional constant:

\[
 \boxed{
 Q(t):=\sum_h|C_h(t)|^2
      =\||u(t)|^2\|_2^2
      =\|u(t)\|_4^4.}
 \tag{4.1}
\]

Let

\[
 D_1=\|\nabla |u|^2\|_2^2,
 \qquad
 D_2=\int_{\mathbb T^3}|u|^2|\nabla u|^2\,d\mu.
 \tag{4.2}
\]

Multiplying (3.7) by \(2\overline{C_h}\), summing, and taking real parts
gives

\[
\begin{aligned}
 Q'
 ={}&-2\nu\sum_h|h|^2|C_h|^2
     -4\nu\operatorname{Re}\sum_hG_h\overline{C_h}
     +2\operatorname{Re}\sum_h{\cal N}_h\overline{C_h}.
\end{aligned}
 \tag{4.3}
\]

The first two sums are \(-2\nu D_1\) and \(-4\nu D_2\).  The transport
part \(u g\) of (3.6) cancels after integration, but the pressure part does
not.  Therefore

\[
 \boxed{
 Q'+2\nu D_1+4\nu D_2
 =-4\int |u|^2u\cdot\nabla p\,d\mu
 = 4\int p\,u\cdot\nabla |u|^2\,d\mu.}
 \tag{4.4}
\]

This is the standard exact \(L^4\) balance, reconstructed here from the
autocorrelation law.  Both viscous terms on the left are nonnegative.  The
pressure term has no fixed sign.

For completeness, the complete instantaneous autocorrelation also gives

\[
 \|u\|_6^6=\int g^3\,d\mu
 =\sum_{h+\ell+m=0}C_hC_\ell C_m.
 \tag{4.5}
\]

Thus complete \(C\) determines the present sixth moment, but, as Section 7
shows, it does not determine \(\dot C\).

## 5. What can actually be closed

### 5.1 An \(A Q\) inequality with an unclosed Wiener factor

The periodic pressure estimate and Hölder give

\[
 \|p\|_3\le C_P\|u\otimes u\|_3
            \le C_P\|u\|_6^2,
 \tag{5.1}
\]

and hence

\[
 4\left|\int p\,u\cdot\nabla g\,d\mu\right|
 \le C\|u\|_6^3D_1^{1/2}
 \le \nu D_1+C\nu^{-1}\|u\|_6^6.
 \tag{5.2}
\]

Using the exact R0.73S static certificate

\[
 \|u\|_6^6\le A Q,
 \qquad A=\sum_h|C_h|,
 \tag{5.3}
\]

one obtains

\[
 \boxed{
 Q'+\nu D_1+4\nu D_2
 \le C\nu^{-1}A Q.}
 \tag{5.4}
\]

This is a valid dynamic use of the quadratic certificate.  It is not a
closed critical inequality because \(A\) is not controlled by \(Q\) for a
continuum solution.  In a fixed finite Galerkin system,

\[
 A\le\sqrt{D_CQ}
 \tag{5.5}
\]

closes (5.4), but the factor \(\sqrt{D_C}\) diverges with resolution and
therefore supplies no uniform PDE estimate.

### 5.2 A continuum-uniform but superlinear closed ODE

There is a genuine closure that does not use Fourier support.  Put
\(X=D_1^{1/2}\) and \(E=\|u\|_2\).  Interpolation and periodic Sobolev give

\[
\begin{aligned}
 \|u\|_6^3
 &=\|g\|_3^{3/2}
 \le \|g\|_2^{3/4}\|g\|_6^{3/4}\\
 &\le C Q^{3/8}(X+E^2)^{3/4}.
\end{aligned}
 \tag{5.6}
\]

Applying Young's inequality with exponents \(8/7\) and \(8\) to the
\(X^{7/4}\) term, and with exponents \(2,2\) to the remaining term, yields

\[
 C\|u\|_6^3X
 \le \nu X^2
   +C\bigl(\nu^{-7}Q^3+\nu^{-1}E^3Q^{3/4}\bigr).
 \tag{5.7}
\]

Consequently

\[
 \boxed{
 Q'+\nu D_1+4\nu D_2
 \le C\bigl(\nu^{-7}Q^3+\nu^{-1}E^3Q^{3/4}\bigr).}
 \tag{5.8}
\]

Since normalized measure gives \(E\le\|u\|_4=Q^{1/4}\), a coarser closed
form is

\[
 \boxed{
 Q'\le C\bigl(\nu^{-7}Q^3+\nu^{-1}Q^{3/2}\bigr).}
 \tag{5.9}
\]

This proves local quantitative control and is uniform in Fourier
resolution.  It does not provide global control: the comparison ODE itself
allows finite-time blow-up.  It is also not the scale-critical
\(L_t^4L_x^6\) entrance sought in R0.73Q--R0.73S.

## 6. Why \(A(t)Q(t)\) does not close

Even when \(A(t)<\infty\), its derivative must be interpreted with an upper
Dini derivative because some \(C_h\) may cross zero.  Equation (3.7) gives

\[
 D^+A+\nu\sum_h|h|^2|C_h|
 \le 2\nu\sum_h|G_h|+\sum_h|h|\,|F_h|.
 \tag{6.1}
\]

The right side contains Wiener norms of \(|\nabla u|^2\) and one derivative
of \(u(g+2p)\).  For example,

\[
 \sum_h|G_h|
 \le\left(\sum_k|k|\,|a_k|\right)^2.
 \tag{6.2}
\]

The flux term similarly requires derivative-weighted Wiener norms of
\(u\), \(g\), and \(p\).  These are higher regularity or analyticity
budgets, not functions of \((A,Q,E)\).  Therefore differentiating \(A Q\)
does not create a closed R0.73S dynamic quantity; it simply moves the
unknown into stronger Wiener norms.

The minimum and support cardinalities in the static shell proxy
\(U_j=Q_j\min\{M_jE_j^2,\sqrt{D_{\Delta,j}Q_j}\}\) are even less suitable
for direct differentiation.  Support changes discontinuously in Galerkin
models and is infinite for a generic smooth nonlinear solution.

## 7. Exact non-autonomy witness

The failure of a \(C\)-only evolution is not merely a weakness of (6.1).
For every positive integer \(n\), define

\[
 u^{(n)}(x)=\bigl(0,\cos(nx_1),\sin(nx_1)\bigr).
 \tag{7.1}
\]

This field is real, mean zero, divergence free, and

\[
 (u^{(n)}\cdot\nabla)u^{(n)}=0,
 \qquad |u^{(n)}|^2\equiv1.
 \tag{7.2}
\]

Thus every member has exactly the same complete autocorrelation,

\[
 C_h=\mathbf 1_{h=0},\qquad A=Q=E^2=1,
 \tag{7.3}
\]

but

\[
 G_0=n^2,\qquad
 \dot C_0(0)=-2\nu n^2,\qquad
 Q'(0)=-4\nu n^2.
 \tag{7.4}
\]

Indeed the exact solution is
\(u^{(n)}(t)=e^{-\nu n^2t}u^{(n)}(0)\).  Hence two smooth solutions can have
the same entire \(C\) at one time and different \(\dot C\), even with zero
nonlinearity and zero pressure.  Unweighted autocorrelation loses the
absolute carrier scale.  Any autonomous dynamic certificate must restore
at least an absolute-frequency weight; pressure additionally requires
polarization information.

## 8. Littlewood--Paley shell evolution

Let \(v_j=P_ju\), where \(P_j\) has a real even self-adjoint symbol, and put

\[
 {\cal F}_j=P_j\mathbb P((u\cdot\nabla)u),
 \qquad g_j=|v_j|^2,
 \qquad C_{j,h}=\widehat{g_j}(h),
 \qquad Q_j=\|v_j\|_4^4.
 \tag{8.1}
\]

Since \(\partial_tv_j=\nu\Delta v_j-{\cal F}_j\), the exact shell laws are

\[
 \boxed{
 \dot C_{j,h}
 =-\nu|h|^2C_{j,h}-2\nu\widehat{|\nabla v_j|^2}(h)
  -2\widehat{v_j\cdot{\cal F}_j}(h),}
 \tag{8.2}
\]

and

\[
 \boxed{
 Q_j'+2\nu\|\nabla g_j\|_2^2
      +4\nu\int g_j|\nabla v_j|^2\,d\mu
 =-4\int g_jv_j\cdot{\cal F}_j\,d\mu.}
 \tag{8.3}
\]

Self-adjointness gives the equivalent flux pairing

\[
 \int g_jv_j\cdot{\cal F}_j
 =\int \mathbb P P_j(g_jv_j)\cdot (u\cdot\nabla)u.
 \tag{8.4}
\]

The Leray projector must remain on \(P_j(g_jv_j)\), because that cubic
vector field is not divergence free.  Two elementary bounds are

\[
 4\left|\int g_jv_j\cdot{\cal F}_j\right|
 \le4\|v_j\|_6^3\|{\cal F}_j\|_2,
 \tag{8.5}
\]

and

\[
 4\left|\int g_jv_j\cdot{\cal F}_j\right|
 \le4Q_j^{3/4}\|{\cal F}_j\|_4.
 \tag{8.6}
\]

Both require an external shell-flux norm.  The pair \((E_j,Q_j)\), or the
static support data from R0.73S, does not determine that flux.  Summing
(8.3) with critical shell weights therefore remains open until a signed
paraproduct/flux estimate absorbs the right side without introducing an
uncontrolled supercritical norm.

## 9. Two heat-weighted versions

### 9.1 Heat applied to the velocity: an exact two-parameter law

For \(s\ge0\), put

\[
 v_s=e^{s\Delta}u,
 \qquad
 C_h^{(s)}=\widehat{|v_s|^2}(h)
 =\sum_k e^{-s(|k+h|^2+|k|^2)}
        \langle a_{k+h},a_k\rangle,
 \tag{9.1}
\]

and

\[
 Q_s=\sum_h|C_h^{(s)}|^2=\|v_s\|_4^4,
 \qquad
 R_s=e^{s\Delta}\mathbb P((u\cdot\nabla)u).
 \tag{9.2}
\]

Because

\[
 (\partial_t-\nu\partial_s)v_s=-R_s,
 \tag{9.3}
\]

one obtains the exact heat-plane identities

\[
 \boxed{
 (\partial_t-\nu\partial_s)C_h^{(s)}
 =-2\widehat{v_s\cdot R_s}(h),}
 \tag{9.4}
\]

and

\[
 \boxed{
 (\partial_t-\nu\partial_s)Q_s
 =-4\int |v_s|^2v_s\cdot R_s\,d\mu.}
 \tag{9.5}
\]

The heat derivative itself has the favorable exact sign

\[
 \partial_sQ_s
 =-2\|\nabla|v_s|^2\|_2^2
  -4\int |v_s|^2|\nabla v_s|^2\,d\mu\le0.
 \tag{9.6}
\]

This weighting repairs the missing carrier information in Section 7.  It
still does not close, because \(R_s\) is formed from the unfiltered \(u\),
not from \(v_s\) alone.  More explicitly,

\[
 R_s
 =\mathbb P((v_s\cdot\nabla)v_s)+{\cal K}_s,
 \tag{9.7}
\]

where

\[
 {\cal K}_s
 =e^{s\Delta}\mathbb P((u\cdot\nabla)u)
  -\mathbb P((e^{s\Delta}u\cdot\nabla)e^{s\Delta}u)
 \tag{9.8}
\]

is a bilinear heat commutator.  A bound such as

\[
 \left|\text{right side of (9.5)}\right|
 \le4\|v_s\|_6^3\|R_s\|_2
 \tag{9.9}
\]

introduces \(\|R_s\|_2\), which is not controlled by \(Q_s\).  A useful
R0.73T theorem would need a scale-critical, time-integrable estimate for
this commutator or for its signed pairing in (9.5).

### 9.2 Heat applied only to the energy density

For fixed \(\tau>0\), let

\[
 Z_\tau=e^{\tau\Delta}g,
 \qquad
 \widetilde Q_\tau=\|Z_\tau\|_2^2
 =\sum_h e^{-2\tau|h|^2}|C_h|^2.
 \tag{9.10}
\]

Applying \(e^{\tau\Delta}\) to (3.5) gives

\[
\begin{aligned}
 {1\over2}\widetilde Q_\tau'
 ={}&-\nu\|\nabla Z_\tau\|_2^2
 -2\nu\langle e^{\tau\Delta}|\nabla u|^2,Z_\tau\rangle\\
 &-\left\langle
 e^{\tau\Delta}\nabla\cdot\bigl(u(g+2p)\bigr),Z_\tau
 \right\rangle .
\end{aligned}
 \tag{9.11}
\]

The second term is nonpositive because the heat semigroup preserves
nonnegativity.  However, the transport cancellation is lost after filtering:
the last pairing is not zero even for the \(ug\) part.  Thus a heat weight on
the shift \(h\) alone does not solve the flux problem.  A time-dependent
\(\tau(t)\) adds another favorable gradient term when \(\tau'\ge0\), but
does not remove this commutator.

## 10. Closure matrix

| Quantity | Exact evolution | Resolution-uniform closure | Global/critical closure |
| --- | --- | --- | --- |
| \(C_h\) | (3.7) | no, needs \(G_h\) and pressure flux | no |
| \(Q=\sum|C_h|^2\) | (4.4) | yes, the superlinear ODE (5.9) | no |
| \(A Q\) | (5.4), (6.1) | no, derivative Wiener norms enter | no |
| fixed Galerkin \(Q\) | (5.4)--(5.5) | yes with cutoff-dependent \(\sqrt{D_C}\) | no continuum statement |
| shell \(Q_j\) | (8.3) | only after supplying \({\cal F}_j\) | open signed flux estimate |
| velocity-heat \(Q_s\) | (9.5) | only after supplying \(R_s\) | open heat-commutator estimate |
| density-heat \(\widetilde Q_\tau\) | (9.11) | flux commutator remains | no current closure |

## 11. Proved propositions available to the parent draft

1. **Exact coefficient law.**  Equations (3.1) and (3.7) give the full
   Fourier evolution of \(C_h\) with correct conjugates, viscosity, pressure,
   and Leray projection.
2. **Exact quartic balance.**  Equations (4.1) and (4.4) identify
   \(Q=\|u\|_4^4\) and its two positive viscous dissipations, leaving only
   the pressure work.
3. **Dynamic use of R0.73S.**  Equation (5.4) rigorously converts the static
   \(\|u\|_6^6\le A Q\) certificate into a differential inequality, while
   exposing \(A\) as the missing dynamic budget.
4. **Continuum local closure.**  Equations (5.8)--(5.9) give a
   resolution-uniform closed ODE for \(Q\), but it is not global.
5. **Non-autonomy theorem.**  The family (7.1) has identical complete
   unweighted autocorrelation and different autocorrelation derivatives.
6. **Exact shell law.**  Equations (8.2)--(8.4) isolate the signed inter-shell
   forcing that any critical closure must pay.
7. **Exact heat-plane law.**  Equations (9.4)--(9.6) restore carrier
   information and separate favorable heat dissipation from the remaining
   nonlinear commutator.

## 12. Missing lemmas required for genuine R0.73T progress

The following are not proved here and should not be inferred from the exact
identities.

1. A signed paraproduct estimate for the sum of the shell fluxes in (8.3)
   with the R0.73R critical weights, absorbable by the displayed viscous
   terms plus a time-integrable critical quantity.
2. A resolution-uniform substitute for \(A\le\sqrt{D_CQ}\), or a propagated
   weighted Wiener budget whose hypothesis is itself scale-appropriate.
3. A bound for the heat commutator \({\cal K}_s\) in (9.8), integrated in
   the heat variable and physical time with exactly the exponents required
   by the R0.73Q \(L_t^4L_x^6\) tube.
4. A mechanism that turns any local or conditional inequality above into
   eventual entrance for arbitrary smooth data.  No such mechanism follows
   from (5.9).
5. An extremal or cancellation lemma using divergence-free polarization to
   control the pressure pairing more sharply than absolute Hölder bounds.

## 13. Likely error points for subsequent drafts

- treating \(C_h\) as real instead of only Hermitian;
- omitting one differentiated factor in \(\dot C_h\), which loses the
  second conjugate term in (3.1);
- dropping \(\mathbb P_{k+h}\) against \(a_k\) for \(h\ne0\);
- replacing the viscous term by a multiple of \(|h|^2C_h\) and omitting
  \(G_h\);
- claiming \(G_h\overline{C_h}\ge0\) shift by shift; positivity appears only
  after the full unweighted sum (or a separately justified positive heat
  kernel argument);
- canceling the pressure together with advection in the \(L^4\) balance;
- differentiating \(A=\sum|C_h|\) classically through zeros;
- treating a Galerkin support count as uniform in the PDE limit;
- confusing \(e^{s\Delta}(u\cdot\nabla u)\) with
  \((e^{s\Delta}u\cdot\nabla)e^{s\Delta}u\);
- assuming the LP shell forcing is the self-advection of that shell;
- losing the factors \(2\) and \(4\) in (4.4), (8.3), or (9.6);
- using the exact instantaneous identity (4.5) as if it supplied an
  autonomous evolution for \(C\).

## 14. Strict research boundary

This audit establishes exact identities and identifies a precise closure
problem.  It proves neither a new regularity criterion nor global control of
an arbitrary three-dimensional solution.  The strongest unconditional
closed estimate here is the local superlinear inequality (5.9).  The
critical shell and heat-flow closures remain open, so no Clay Millennium
conclusion or partial-resolution claim is authorized.
