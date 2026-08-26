# R0.72B -- target-row participation and a coherent many-carrier exclusion

**Date:** 2026-08-27
**Status:** analytic theorem independently checked. Two finite computational audits and
the formal figure package are corroborating evidence only. The statements remain
inside the real-shear, fixed-target, triangular Fourier-lattice class inherited from
R0.71W--R0.72A.

**Keywords:** Navier--Stokes regularity, triangular 2.5D flows, target-row norm,
many-carrier coherence, complete root ledger, enhanced dissipation, burn-in

---

## 0. Direct decision

R0.72A controlled the complete target-root slope mass by the full multiplier
norm,

\[
 G_{\rm all}^{\rm ex}(I)
 \le e^{2\lambda_0L}M\Omega^2
 \bigl[1+q_I+\eta\ell_2(I)\bigr].
 \tag{0.1}
\]

This is uniform in the number and separation of roots, but it ignores how much of
the multiplier is visible from the target row. Define

\[
 \rho(x)^2
 :=\|P_0V_z(x)\|_{\ell^2\to\mathbb C}^2
 =2K_z^2\sum_{l=1}^M|z_l|^2e^{-2\kappa r_l^2x},
 \qquad \rho_A=\rho(A_0).
 \tag{0.2}
\]

The same bounded-variation argument, with the target row retained at every step,
gives the exact refinement

\[
 \boxed{
 G_{\rm all}^{\rm ex}(I)
 \le e^{2\lambda_0L}M\rho_A^2
 \bigl[1+q_\rho(I)+\eta\ell_\times(I)\bigr],}
 \tag{0.3}
\]

where

\[
 q_\rho(I)=\frac1{\rho_A\sqrt M}\int_I|Q(x)F(x)|\,dx\le3,
 \tag{0.4}
\]

\[
 \ell_\times(I)
 =\frac1{\rho_A\Omega}\int_I\rho(x)\|V_z(x)\|\,dx
 \le\min\{L,C_\times\},
 \tag{0.5}
\]

and

\[
 C_\times
 =\sqrt{\frac{C_\kappa}{2\kappa}}
 =\frac{\pi}{\sqrt2\,45^{1/4}\kappa},
 \qquad
 C_\kappa=\frac{\pi^2}{\sqrt{45}\,\kappa},
 \qquad \kappa=\nu d^2.
 \tag{0.6}
\]

The launch-inclusive normalized ledger therefore obeys

\[
 \boxed{
 \frac{\mathcal J_{\rm all}}
 {D^{1/3}\Lambda_1}
 \le C\nu^{-2}e^{2\lambda_0L}
 \frac M{K_s}\eta^{4/3}
 \underbrace{\frac{\rho_A^2}{\Omega^2}}_{\chi_A}
 \left(\frac{\Omega^2}{K_v}\right)^{1/3}
 \bigl[1+q_\rho+\eta\ell_\times\bigr].}
 \tag{0.7}
\]

The full nonnegative rotational charge remains inside the exact denominator
\(\Lambda_1\). It is not replaced by a proxy and is not separately evaluated.

For exact launch, same-sign comparable amplitudes, and distinct positive integer
carriers, both

\[
 \chi_0=O(M^{-1}),
 \qquad
 \frac{\Omega^2}{K_v}=O(M^{-1}).
 \tag{0.8}
\]

Together with \(M/K_s=O(M^{-2})\), this gives

\[
 \boxed{
 \frac{\mathcal J_{\rm all}}
 {D^{1/3}\Lambda_1}
 \le C_*\nu^{-2}e^{2\lambda_0L}
 M^{-10/3}\eta^{4/3}
 \bigl[4+\eta\min\{L,C_\times\}\bigr].}
 \tag{0.9}
\]

For \(\eta_M=M^\alpha\), \(L_M=M^{-\beta}\), and bounded
\(\lambda_{0,M}L_M\), the right side tends to zero whenever

\[
 \boxed{
 \alpha<\min\left\{\frac52,\frac{10+3\beta}{7}\right\}.}
 \tag{0.10}
\]

This is a uniform exclusion theorem for the canonical coherent many-carrier
promotion of the one-carrier Bessel obstruction. It is not a converse outside the
displayed region, a singularity construction, or a solution of the Millennium
problem.

---

## 1. Exact lattice setting

Fix \(\nu>0\), \(d\ge1\), a target frequency
\(k_*=(K_y,K_z)\) with \(K_z\ne0\), pairwise distinct positive integers
\(r_1,\ldots,r_M\), and real shear amplitudes \(z_l\). The active scalar
sector is

\[
 \partial_xF=D_qF+\delta V_z(x)F,
 \qquad \delta=\frac P{q^2},
 \qquad \|F(0)\|_2^2=M,
 \tag{1.1}
\]

with finite-support launch data and

\[
 (D_qF)_r=-\lambda_{q,r}F_r,
 \qquad
 \lambda_{q,r}=\nu\left[
 \left(dr+\frac{K_y}{q}\right)^2+\frac{K_z^2}{q^2}
 \right],
 \tag{1.2}
\]

\[
 (V_z(x)F)_r
 =-iK_z\sum_{l=1}^M z_le^{-\kappa r_l^2x}
 \left(F_{r-r_l}+F_{r+r_l}\right),
 \qquad \kappa=\nu d^2.
 \tag{1.3}
\]

Assume

\[
 q\ge q_*:=\max\left(1,\frac{2|K_y|}{d}\right).
 \tag{1.4}
\]

For \(A_0\ge0\), let

\[
 \Omega=\sup_{x\ge A_0}\|V_z(x)\|,
 \qquad \eta=|\delta|\Omega,
 \qquad \lambda_0=\lambda_{q,0},
 \tag{1.5}
\]

and count exact roots on

\[
 I=[A,A+L]\subset[A_0,\infty).
 \tag{1.6}
\]

The real-shear assumption makes \(V_z(x)\) skew-adjoint. Hence

\[
 \frac12\frac d{dx}\|F(x)\|_2^2
 =-\sum_r\lambda_{q,r}|F_r(x)|^2\le0,
 \tag{1.7}
\]

\[
 \|F(x)\|_2\le\sqrt M,
 \qquad
 \int_0^\infty\sum_r\lambda_{q,r}|F_r(x)|^2\,dx
 \le\frac M2.
 \tag{1.8}
\]

The finite-support launch class gives the target-coordinate regularity needed at
\(A_0=0\), exactly as in R0.72A. No extension to arbitrary \(\ell^2\) launch
data is asserted.

---

## 2. Target-row norm and mixed exposure

Under Fourier transform on \(\ell^2(\mathbb Z)\), \(V_z(x)\) is
multiplication by

\[
 m_x(\theta)=-2iK_z\sum_{l=1}^M
 z_le^{-\kappa r_l^2x}\cos(r_l\theta).
 \tag{2.1}
\]

The target row has only the inputs \(\pm r_l\). Orthogonality gives the exact
row norm

\[
 \rho(x)^2
 =2K_z^2\sum_l|z_l|^2e^{-2\kappa r_l^2x}.
 \tag{2.2}
\]

It is nonincreasing, \(\rho(x)\le\rho_A\), and Parseval gives
\(\rho_A\le\Omega\). Moreover,

\[
 \int_{A_0}^\infty\rho(x)^2\,dx
 =\frac{K_z^2}{\kappa}
 \sum_l\frac{|z_l|^2e^{-2\kappa r_l^2A_0}}{r_l^2}
 \le\frac{\rho_A^2}{2\kappa}.
 \tag{2.3}
\]

R0.72A proved

\[
 \int_{A_0}^\infty\|V_z(x)\|^2\,dx
 \le C_\kappa\Omega^2.
 \tag{2.4}
\]

Cauchy--Schwarz in \(x\) therefore yields

\[
 \int_{A_0}^\infty\rho(x)\|V_z(x)\|\,dx
 \le \rho_A\Omega C_\times.
 \tag{2.5}
\]

On the actual observation interval, the pointwise bounds give the other estimate

\[
 \int_I\rho(x)\|V_z(x)\|\,dx
 \le L\rho_A\Omega.
 \tag{2.6}
\]

Equations (2.5)--(2.6) prove (0.5). A carrier-resolved constant is also
available:

\[
 C_{\times,A_0}
 =\left[
 \frac{C_\kappa}{2\kappa}
 \frac{\sum_l|z_l|^2e^{-2\kappa r_l^2A_0}/r_l^2}
 {\sum_l|z_l|^2e^{-2\kappa r_l^2A_0}}
 \right]^{1/2}
 \le C_\times.
 \tag{2.7}
\]

This refined constant is diagnostic. The uniform theorem only needs
\(C_\times\).

---

## 3. Exact payment of the differentiated row

Put

\[
 h(x)=P_0V_z(x)F(x),
 \qquad F_0'=-\lambda_0F_0+\delta h.
 \tag{3.1}
\]

The combined differentiated row is

\[
 h'+\lambda_0h=Q(x)F+\delta P_0V_z(x)^2F,
 \qquad
 Q=P_0\left[V_z'+V_z(D_q+\lambda_0)\right].
 \tag{3.2}
\]

The explicit \(Q\) row and the condition (1.4) give

\[
 |QF|
 \le6\sqrt{2\nu}\,d|K_z|A(x)\mathcal E(x)^{1/2},
 \tag{3.3}
\]

where

\[
 A(x)^2=\sum_lr_l^2|z_l|^2e^{-2\kappa r_l^2x},
 \qquad
 \mathcal E(x)=\sum_r\lambda_{q,r}|F_r(x)|^2.
 \tag{3.4}
\]

The row norm pays the carrier factor exactly:

\[
 \int_{A_0}^\infty A(x)^2\,dx
 =\frac1{2\kappa}\sum_l|z_l|^2e^{-2\kappa r_l^2A_0}
 =\frac{\rho_A^2}{4\kappa K_z^2}.
 \tag{3.5}
\]

Combining (1.8), (3.3), and (3.5) gives

\[
 \boxed{
 \int_{A_0}^\infty|Q(x)F(x)|\,dx
 \le3\rho_A\sqrt M.}
 \tag{3.6}
\]

Thus (0.4) is exact and is not a heuristic substitution of \(\rho_A\) for
\(\Omega\). The nonlinear row satisfies

\[
 |P_0V_z(x)^2F(x)|
 \le\rho(x)\|V_z(x)\|\sqrt M.
 \tag{3.7}
\]

Consequently

\[
 \int_I|h'+\lambda_0h|\,dx
 \le\rho_A\sqrt M
 \bigl[q_\rho(I)+\eta\ell_\times(I)\bigr].
 \tag{3.8}
\]

---

## 4. Complete target-root theorem

### Theorem 4.1 -- target-row mixed-exposure bound

Assume (1.1)--(1.6), real shear, finite-support launch data, and
\(A_0\ge0\). For every finite set of exact roots of \(F_0\) in \(I\),

\[
 \boxed{
 \sum_{F_0(\tau_j)=0}|F_0'(\tau_j)|^2
 \le e^{2\lambda_0L}\delta^2M\rho_A^2
 \bigl[1+q_\rho(I)+\eta\ell_\times(I)\bigr].}
 \tag{4.1}
\]

If \(\delta\ne0\), then

\[
 \boxed{
 G_{\rm all}^{\rm ex}(I)
 :=\sum_{F_0(\tau)=0}|P_0V_z(\tau)F(\tau)|^2
 \le e^{2\lambda_0L}M\rho_A^2
 \bigl[1+q_\rho(I)+\eta\ell_\times(I)\bigr].}
 \tag{4.2}
\]

Both inequalities hold for the complete extended nonnegative root sum. In
particular,

\[
 G_{\rm all}^{\rm ex}(I)
 \le e^{2\lambda_0L}M\rho_A^2
 \bigl[4+\eta\min\{L,C_\times\}\bigr].
 \tag{4.3}
\]

#### Proof

Set

\[
 g(x)=e^{\lambda_0(x-A)}F_0(x).
 \tag{4.4}
\]

Then

\[
 g'=\delta e^{\lambda_0(x-A)}h,
 \qquad
 g''=\delta e^{\lambda_0(x-A)}
 \left[QF+\delta P_0V_z^2F\right].
 \tag{4.5}
\]

Equations (1.8), (2.2), (3.6), and (3.7) give

\[
 \|g'\|_\infty
 \le e^{\lambda_0L}|\delta|\rho_A\sqrt M,
 \tag{4.6}
\]

\[
 \int_I|g''(x)|\,dx
 \le e^{\lambda_0L}|\delta|\rho_A\sqrt M
 \bigl[q_\rho(I)+\eta\ell_\times(I)\bigr].
 \tag{4.7}
\]

The scalar derivative-mass lemma from R0.72A states that, for any finite
ordered subset of zeros,

\[
 \sum_j|g'(\tau_j)|^2
 \le |g'(\tau_1)|^2
 +\|g'\|_\infty\int_I|g''(x)|\,dx.
 \tag{4.8}
\]

The first root is paid by (4.6). Equations (4.6)--(4.8) prove (4.1).
At a target root, \(F_0'=\delta h\), so division by \(\delta^2\) proves
(4.2). The estimate is independent of the finite subset, the root count, and
the root separation. Taking the supremum over all finite root subsets defines
the complete extended nonnegative sum and proves the same bound for it.
Multiple roots have zero slope. If \(F_0\) vanishes identically, the slope
measure is zero. \(\square\)

### Degenerate branch

If \(\rho_A=0\), every positive exponential weight in (0.2) forces
\(z_l=0\) for all \(l\). Hence \(V_z\equiv0\), \(\Omega=0\), and
\(G_{\rm all}^{\rm ex}=0\). The quotients \(q_\rho\) and
\(\ell_\times\) are set to zero on this branch before any division is made.

---

## 5. Full normalized ledger

Let the launch-inclusive physical-time ledger and amplitudes be those of
R0.71Z--R0.72A. In particular,

\[
 E=S^2K_s+P^2K_v,
 \qquad
 K_s=\sum_{l=1}^Mr_l^2,
 \qquad
 K_v=\sum_{l=1}^Mr_l^2|z_l|^2.
 \tag{5.1}
\]

Launch Parseval gives

\[
 \sup_{K_t}Y\ge c_Yq^2E,
 \qquad D\ge c_Dq^2E.
 \tag{5.2}
\]

The full rotational charge is retained in
\(\Lambda_1(K_t;u)\). Only its exact nonnegative lower term is used, exactly
as in R0.72A. Replacing the root-mass input \(M\Omega^2\) by
\(M\rho_A^2\) before the amplitude optimization gives

\[
 \frac{\mathcal J_{\rm all}}
 {D^{1/3}\Lambda_1}
 \le C\nu^{-2}e^{2\lambda_0L}
 \frac M{K_s}\eta^{4/3}
 \chi_A
 \left(\frac{\Omega^2}{K_v}\right)^{1/3}
 \bigl[1+q_\rho+\eta\ell_\times\bigr],
 \tag{5.3}
\]

where

\[
 \chi_A=\frac{\rho_A^2}{\Omega^2}\le1.
 \tag{5.4}
\]

The scalar amplitude variable remains

\[
 u=\frac{S^2K_s}{P^2K_v},
 \tag{5.5}
\]

and \(u(1+u)^{-4/3}\) is still maximized at \(u=3\). No new
amplitude assumption is hidden in (5.3).

### Corollary 5.1 -- participation-rate phase region

Suppose

\[
 \chi_{A,M}\le C_\chi M^{-\gamma},
 \qquad \gamma\ge0,
 \tag{5.6}
\]

and use the uniform inequalities

\[
 \frac M{K_s}=O(M^{-2}),
 \qquad
 \frac{\Omega^2}{K_v}=O(1).
 \tag{5.7}
\]

Then

\[
 \frac{\mathcal J_{\rm all}}
 {D^{1/3}\Lambda_1}
 \le C M^{-2-\gamma}\eta^{4/3}
 \bigl[4+\eta\min\{L,C_\times\}\bigr].
 \tag{5.8}
\]

For \(\eta_M=M^\alpha\), \(L_M=M^{-\beta}\), and bounded
\(\lambda_{0,M}L_M\), this vanishes whenever

\[
 \boxed{
 \alpha<\min\left\{
 \frac32+\frac{3\gamma}{4},
 \frac{6+3\gamma+3\beta}{7}
 \right\}.}
 \tag{5.9}
\]

For \(\gamma=1\), this coarser participation-only region is

\[
 \alpha<\min\left\{\frac94,\frac{9+3\beta}{7}\right\}.
 \tag{5.10}
\]

---

## 6. Exact-launch coherent exclusion

Assume \(A_0=0\), all nonzero \(z_l\) have the same sign, and there are
constants independent of \(M\) such that

\[
 0<c_-a_M\le|z_l|\le c_+a_M.
 \tag{6.1}
\]

At \(\theta=0\), all multiplier terms have the same phase. Therefore

\[
 \Omega=2|K_z|\sum_l|z_l|,
 \tag{6.2}
\]

and

\[
 \chi_0
 =\frac12\frac{\sum_l|z_l|^2}{(\sum_l|z_l|)^2}
 =\frac1{2M_{\rm eff}},
 \qquad
 M_{\rm eff}=\frac{(\sum_l|z_l|)^2}{\sum_l|z_l|^2}.
 \tag{6.3}
\]

Comparability gives

\[
 \chi_0\le\frac{c_+^2}{2c_-^2}\,M^{-1}.
 \tag{6.4}
\]

Since the carriers are distinct positive integers,

\[
 K_s\ge\frac{M(M+1)(2M+1)}6\ge\frac{M^3}{3}.
 \tag{6.5}
\]

Also,

\[
 K_v\ge c_-^2a_M^2K_s,
 \qquad
 \Omega^2\le4K_z^2c_+^2a_M^2M^2,
 \tag{6.6}
\]

so

\[
 \frac{\Omega^2}{K_v}
 \le12K_z^2\frac{c_+^2}{c_-^2}\,M^{-1}.
 \tag{6.7}
\]

Substitution of (6.4)--(6.7) into (5.3) proves (0.9) and (0.10).

For the canonical choice \(r_l=l\), \(z_l=1\),

\[
 K_s=K_v=\frac{M(M+1)(2M+1)}6,
 \quad
 \Omega=2|K_z|M,
 \quad
 \rho_0^2=2K_z^2M,
 \quad
 \chi_0=\frac1{2M},
 \tag{6.8}
\]

and

\[
 \left(\frac{\Omega^2}{K_v}\right)^{1/3}
 =\left[\frac{24K_z^2M}{(M+1)(2M+1)}\right]^{1/3}
 \asymp M^{-1/3}.
 \tag{6.9}
\]

Thus the exponent \(-10/3\) is an exact asymptotic for this canonical
coherent family, not only a worst-case estimate.

### Positive pre-observation layers

For fixed \(A_0>0\), the weights
\(z_le^{-\kappa r_l^2A_0}\) can concentrate on the lowest carrier as
\(M\to\infty\). Then \(M_{\rm eff}(A_0)\) need not be comparable to
\(M\). The \(M^{-1}\) participation gain is therefore used only at exact
launch, under an explicit effective-participation hypothesis, or after proving
that the heat-weighted amplitudes remain comparable.

---

## 7. Nonautonomous enhanced-dissipation interface

Write the lattice equation in Fourier angle as

\[
 \partial_xf
 =\left[
 \kappa(\partial_\theta+i\beta)^2-\mu
 -i\delta b(x,\theta)
 \right]f,
 \tag{7.1}
\]

where

\[
 \beta=\frac{K_y}{dq},
 \qquad
 \mu=\frac{\nu K_z^2}{q^2},
 \qquad
 b(x,\theta)=2K_z\sum_lz_le^{-\kappa r_l^2x}\cos(r_l\theta).
 \tag{7.2}
\]

The exact energy identity is

\[
 \frac12\frac d{dx}\|f\|_2^2
 +\kappa\|(\partial_\theta+i\beta)f\|_2^2
 +\mu\|f\|_2^2=0.
 \tag{7.3}
\]

When \(\beta\notin\mathbb Z\), a periodic gauge cannot simply remove it.

At a reference time \(A\), distinguish

\[
 B_A=\|b(A,\cdot)\|_\infty,
 \qquad
 \eta_A^{\rm fr}=|\delta|B_A,
 \tag{7.4}
\]

from the future-ledger amplitude

\[
 \Omega_A=\sup_{x\ge A}\|b(x,\cdot)\|_\infty,
 \qquad
 \eta_A^{\rm led}=|\delta|\Omega_A.
 \tag{7.5}
\]

If the frozen profile has maximal finite critical degeneracy \(n\) and
uniform sublevel constants, the adjacent autonomous comparison rate has the
form

\[
 \Gamma_A^{\rm fr}
 \asymp
 \frac{\kappa^{(n+1)/(n+3)}
 (|\delta|B_A)^{2/(n+3)}}
 {\log^2(2+|\delta|B_A/\kappa)}.
 \tag{7.6}
\]

This is only a comparison scale unless a theorem covering the changing profile
has been proved. Record

\[
 \Theta_A=L\Gamma_A^{\rm fr}
 \tag{7.7}
\]

and the coupling-weighted freezing error

\[
 \Xi_A
 :=|\delta|\int_A^{A+L}
 \|b(x)-b(A)\|_\infty\,dx.
 \tag{7.8}
\]

For the heat-decaying profile,

\[
 \Xi_A
 \le2|\delta K_z|\sum_l|z_l|e^{-\kappa r_l^2A}
 \left[
 L-\frac{1-e^{-\kappa r_l^2L}}{\kappa r_l^2}
 \right].
 \tag{7.9}
\]

If \(S_{\rm na}\) and \(S_{\rm fr}\) denote the nonautonomous and frozen
propagators, Duhamel's formula and contractivity give

\[
 \|S_{\rm na}(A+L,A)-S_{\rm fr}(L)\|\le\Xi_A.
 \tag{7.10}
\]

Thus \(L\kappa r_{\max}^2\ll1\) alone is insufficient. The large coupling
can amplify a small profile change.

### Theorem 7.1 -- restart and tail ledger

For any burn-in time \(a>0\), put

\[
 E_a=\|F(a)\|_2^2,
 \quad \rho_a=\rho(a),
 \quad \Omega_a=\sup_{x\ge a}\|V_z(x)\|,
 \quad \eta_a=|\delta|\Omega_a.
 \tag{7.11}
\]

Positive-time smoothing permits a restart at \(a\). The proof of Theorem 4.1
then gives

\[
 \boxed{
 G_{\rm tail}^{\rm ex}((a,a+L])
 \le e^{2\lambda_0L}E_a\rho_a^2
 \bigl[4+\eta_a\min\{L,C_\times\}\bigr].}
 \tag{7.12}
\]

Any valid enhanced-dissipation estimate for \(E_a\) therefore improves the
tail. It does not alter the already accumulated nonnegative ledger:

\[
 G_{\rm all}^{\rm ex}([0,a+L])
 =G_{\rm pre}^{\rm ex}([0,a])
 +G_{\rm tail}^{\rm ex}((a,a+L]).
 \tag{7.13}
\]

---

## 8. Bessel pre-dissipation no-go

R0.72A constructed an exact one-carrier family with

\[
 \delta_R=R^4,
 \qquad \eta_R=2R^4,
 \qquad L_R\asymp R^{-3},
 \tag{8.1}
\]

and

\[
 G_{\rm all}^{\rm ex}([0,L_R])
 \ge1+\frac8{\pi^2}\log R+O(1).
 \tag{8.2}
\]

For the frozen cosine profile, \(n=1\), so

\[
 \Gamma_R^{\rm fr}\asymp\frac{R^2}{(\log R)^2},
 \qquad
 L_R\Gamma_R^{\rm fr}
 \asymp\frac1{R(\log R)^2}\to0.
 \tag{8.3}
\]

The exact freezing error satisfies

\[
 \Xi_R
 =2R^4\left[L_R-(1-e^{-L_R})\right]
 \le R^4L_R^2=O(R^{-2}).
 \tag{8.4}
\]

Writing the rescaled observation length as \(T_R=R^4L_R=O(R)\), the
energy loss obeys the analytic estimate

\[
 0\le1-\|F(L_R)\|_2^2
 \le
 \frac{4T_R+4T_R^2+\frac83T_R^3}{R^4}
 =O(R^{-1}).
 \tag{8.5}
\]

Hence the selected root mass grows while the layer remains before the adjacent
frozen enhanced-dissipation time, the freezing error tends to zero, and the
energy loss tends to zero. Later decay cannot remove the nonnegative mass
already present in (8.2). In particular, choosing a later endpoint
\(B_R=\log R\) gives \(\|F(B_R)\|_2^2\le R^{-2}\), while the
launch-inclusive complete ledger still has the same logarithmic lower bound.

This no-go is narrow but exact: a terminal semigroup estimate cannot by itself
pay a complete root ledger that started at launch.

---

## 9. Five-parameter candidate ledger

Every later many-carrier candidate must report at least

\[
 (\eta_M,L_M,n_M,c_{{\rm sub},M},
 L_M\kappa r_{\max,M}^2),
 \tag{9.1}
\]

together with

\[
 M_{\rm eff}(A_0),\quad
 \chi_{A,M},\quad
 \Theta_{A,M}=L_M\Gamma_{A,M}^{\rm fr},\quad
 \Xi_{A,M}.
 \tag{9.2}
\]

Here \(n_M\) is the maximal frozen critical degeneracy and
\(c_{{\rm sub},M}\) is a quantitative sublevel constant. A fitted decay rate
does not replace these data. A frozen comparison must be labeled as such.

---

## 10. Computational certificates

The analytic proof is primary. The release archives two independent finite
audits.

1. The producer recomputes the exact row norm, mixed-exposure constants,
   \(Q\)-payment constant, participation factors, coherent prefactor, phase
   boundaries, and Bessel comparison ledger.
2. The independent audit imports neither the producer nor its output. It uses
   separate formulas and direct finite-matrix checks for representative
   profiles.

Both paths record configuration, environment, progress, resource use, raw
results, and SHA-256 checksums. Floating-point checks corroborate the analytic
identities. They are not interval arithmetic, an infinite-lattice proof, a
three-dimensional DNS, or evidence for NSE regularity.

The final producer and independent packages each pass (9/9) checks. For the
canonical equal-amplitude sequence, both fitted tail powers are
(-3.333307683918). Two separately chosen comparable but non-equal amplitude
sequences give (-3.33331070) and (-3.33331015), respectively. Thus the
finite audit does not rely only on exact equality of all carrier amplitudes.
At (M=2^{20}), the canonical value of (M^{10/3}) times the normalized
carrier prefactor is (3.43413618).

For the Bessel comparison row at (R=512), the archived diagnostics are

\[
 \Theta_R=7.890686\times10^{-5},\qquad
 \Xi_R=9.429778\times10^{-6},\qquad
 E_{\rm loss}^{\rm upper}=0.02028011.
 \tag{10.1}
\]

The finite-matrix differentiated-row payment ratio is (0.0901184), below
the analytic constant (1). These numbers are regression checks, not sharp
constants or substitutes for the proof.

The R0.72A report is also corrected in this release: its independent finite
evolution uses fixed-step classical RK4, not exponential midpoint.

---

## 11. Claim--evidence boundary

### Proved

1. The complete target-root bound improves from \(M\Omega^2\) to
   \(M\rho_A^2\), with no root-count or root-separation factor.
2. The exact differentiated-row payment is \(q_\rho\le3\).
3. The mixed exposure satisfies
   \(\ell_\times\le\min\{L,C_\times\}\) with the explicit constant
   (0.6).
4. The full normalized ledger acquires the participation factor
   \(\chi_A=\rho_A^2/\Omega^2\).
5. Exact-launch same-sign comparable profiles have the coherent prefactor
   \(M^{-10/3}\) and the sufficient region (0.10).
6. A valid enhanced-dissipation bound after burn-in pays the tail ledger but
   cannot erase the pre-burn-in complete ledger.
7. The R0.72A Bessel family lies before the adjacent frozen enhanced-
   dissipation time and gives an exact no-go to terminal-decay-only payment.

### Not proved

1. A many-carrier lower family that makes the full normalized ledger nonzero
   or divergent.
2. A converse outside either phase boundary.
3. A uniform nonautonomous enhanced-dissipation theorem for heat-decaying,
   \(M\)-dependent profiles.
4. Uniform effective participation for every fixed positive
   pre-observation layer.
5. Uniform critical-point degeneracy or sublevel constants for coherent
   trigonometric polynomials as \(M\to\infty\).
6. A continuation criterion, finite-time singularity, global regularity, or a
   universal three-dimensional Navier--Stokes endpoint estimate.

---

## 12. Research value and next finite gate

The result closes the most natural coherent many-carrier promotion in a
strictly larger strong-coupling region than R0.72A. It identifies two separate
suppression mechanisms: the target sees only an \(M^{-1}\) fraction of a
coherent multiplier in squared row norm, and the launch enstrophy contributes
another \(M^{-1/3}\) after amplitude optimization.

The value to the Millennium problem remains indirect. The theorem rules out
one mechanism inside a triangular 2.5D class. It does not control general
three-dimensional vortex stretching.

The next finite gate is R0.72C. The useful alternatives are:

1. construct an incoherent or phase-cancelled many-carrier family for which
   \(\chi_A\) does not decay while the exact full charge remains payable; or
2. prove a broader exclusion using a participation quantity that survives
   complex phases and positive pre-observation layers.

Every R0.72C candidate must retain the four comparison diagnostics in (9.2)
and distinguish terminal enhanced dissipation from the launch-inclusive root
ledger.

---

## Primary references used for the comparison boundary

- Constantin, Kiselev, Ryzhik, and Zlatoš, *Diffusion and mixing in fluid
  flow*, Annals of Mathematics 168 (2008),
  https://doi.org/10.4007/annals.2008.168.643.
- Bedrossian and Coti Zelati, *Enhanced dissipation, hypoellipticity, and
  anomalous small noise inviscid limits in shear flows*,
  https://doi.org/10.1007/s00205-017-1099-y.
- Albritton, Beekie, and Novack, *Enhanced dissipation and Hörmander's
  hypoellipticity*, https://arxiv.org/abs/2105.12308.
- Coti Zelati and Gallay, *Enhanced dissipation and Taylor dispersion in
  higher-dimensional parallel shear flows*, https://doi.org/10.1112/jlms.12782.
- Coble and He, *A Note on Enhanced Dissipation and Taylor Dispersion of
  Time-dependent Shear Flows*, https://arxiv.org/abs/2309.15738 and
  https://doi.org/10.4310/CMS.2024.v22.n6.a10.
- Gardner, Liss, and Mattingly, *A pathwise approach to the enhanced
  dissipation of passive scalars advected by shear flows*,
  https://arxiv.org/abs/2410.05657.
- Benthaus and Nobili, *Enhanced Dissipation via time-modulated velocity
  fields*, https://arxiv.org/abs/2501.16905.
- Benthaus, Coclite, and Nobili, *Mixing and enhanced dissipation in a
  time-translating shear flow*, https://arxiv.org/abs/2603.14624.
