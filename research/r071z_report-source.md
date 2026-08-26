# R0.71Z -- all-root bounded-variation sampling and launch-inclusive floor cancellation

**Date:** 2026-08-27  
**Status:** release source. The theorem is restricted to the real-shear,
fixed-target, triangular Fourier-lattice class inherited from R0.71W--Y. It
does not prove a universal Navier--Stokes endpoint estimate, a continuation
criterion, finite-time blow-up, or global regularity.

**Keywords:** Navier--Stokes regularity, triangular 2.5D flows, temporal zeros,
bounded variation, dissipation, Fourier multipliers, enstrophy contrast,
endpoint scaling

---

## 0. Direct decision

R0.71Y controlled any selected set of exact target roots. With \(M\)
unit-modulus launched carriers and \(R\) sampled roots, its pointwise argument
gave

\[
 \frac{\mathcal J_R}{D^{1/3}\Lambda_1}
 \lesssim \nu^{-2}\frac{R}{M^2}\delta_{\rm obs}^{4/3}.
 \tag{0.1}
\]

It left open a possible escape through \(R\gtrsim M^2\) additional nonlinear
roots. A uniform bound on the number of roots is neither available nor
appropriate: R0.71U already constructs exact smooth 2.5D solutions with
arbitrarily many prescribed shell recurrences and uniformly bounded launch
energy and enstrophy.

The correct quantity is the total squared slope mass, not root cardinality.
For the exact triangular evolution, this report proves

\[
 \boxed{
 G_{\rm all}^{\rm ex}
 :=\sum_{F_0(\tau)=0}|P_0V_z(\tau)F(\tau)|^2
 \le C_{\rm BV}(\delta_{\rm obs})M\Omega^2,}
 \tag{0.2}
\]

where

\[
 C_{\rm BV}(\eta)
 =e^{2\lambda_0L}\left(4+C_\kappa\eta\right),
 \qquad
 C_\kappa=\frac{\pi^2}{\sqrt{45}\,\nu d^2},
 \qquad \eta=\delta_{\rm obs}.
 \tag{0.3}
\]

The constant is independent of the root count, carrier count, largest carrier
frequency, and minimum root separation. The proof uses a bounded-variation
zero-sampling identity together with the exact scalar dissipation. It invokes
no ECT inverse, zero count, or second-time NSE jet.

There is a second closure. Let the roots still be counted on their original
observation interval \(I_t=[a,b]\), but compute the complete first-row factor
on

\[
 K_t=[\sigma_q,b],
 \qquad \sigma_q=a-A_0q^{-2},
 \tag{0.4}
\]

which includes launch:

\[
 \Lambda_1(K_t;u)=\mathcal R_Y(K_t)
 \left[\nu^2+\frac1{|K_t|}\int_{K_t}
 \frac{\|\mathbb P(u\times\omega)\|_{\dot H^{-1}}^2}{Y(t)}\,dt\right].
 \tag{0.5}
\]

At every counted root,

\[
 \frac1{Y(t_*)\mathcal R_Y(K_t)}
 \le\frac1{\sup_{K_t}Y}.
 \tag{0.6}
\]

Parseval at launch gives

\[
 \sup_{K_t}Y\ge Y(\sigma_q)\gtrsim
 q^2\left(S^2K_s+P^2K_v\right).
 \tag{0.7}
\]

Thus the matched persistent background and the separate root-time enstrophy
floor are unnecessary for the normalized launch-inclusive ledger. After the
same exact amplitude optimization as R0.71Y,

\[
 \boxed{
 \frac{\mathcal J_{\rm all}(I_t)}
 {D^{1/3}\Lambda_1(K_t;u)}
 \le C\nu^{-2}
 \frac{\delta_{\rm obs}^{4/3}(1+\delta_{\rm obs})}{M^2}.}
 \tag{0.8}
\]

For bounded observation coupling the complete all-root ratio decays at least
as \(M^{-2}\). This closes the quadratic-extra-root and matched-floor escape
routes inside the declared triangular class. Strong observation coupling,
non-unit launch phases, \(A_0\downarrow0\), and different geometries remain
open.

---

## 1. Exact Fourier-lattice setting

Fix viscosity \(\nu>0\), target frequency \(k_*=(K_y,K_z)\) with
\(K_z\ne0\), carrier modulus \(d\ge1\), and scaled left observation time
\(A_0>0\). Let

\[
 r_1,\ldots,r_M\in\mathbb N
 \tag{1.1}
\]

be pairwise distinct. The positive-\(K_z\) active scalar sector solves

\[
 \partial_xF=D_qF+\delta V_z(x)F,
 \qquad \delta=\frac P{q^2},
 \qquad \|F(0)\|_{\ell^2}^2=M.
 \tag{1.2}
\]

Here

\[
 (D_qF)_r=-\lambda_{q,r}F_r,
 \qquad
 \lambda_{q,r}=\nu\left[
 \left(dr+\frac{K_y}{q}\right)^2+\frac{K_z^2}{q^2}
 \right],
 \tag{1.3}
\]

and, for real coefficients \(z_l\),

\[
 (V_z(x)F)_r
 =-iK_z\sum_{l=1}^Mz_le^{-\kappa r_l^2x}
 \left(F_{r-r_l}+F_{r+r_l}\right),
 \qquad \kappa=\nu d^2.
 \tag{1.4}
\]

Put

\[
 \Omega=\sup_{x\ge A_0}\|V_z(x)\|_{\ell^2\to\ell^2},
 \qquad
 \eta=|\delta|\Omega=\delta_{\rm obs},
 \qquad
 \lambda_0=\lambda_{q,0}.
 \tag{1.5}
\]

The counted roots lie in a scaled interval

\[
 I_x=[A,A+L]\subset[A_0,\infty).
 \tag{1.6}
\]

The factor \(e^{\lambda_0L}\) below is harmless for a fixed physical window:
because \(x=q^2(t-\sigma_q)\),
\(\lambda_0L\le\nu|k_*|^2|I_t|\). It is independent of \(q,M\), and the
carrier frequencies.

The real-shear assumption is essential. Every shift sum
\(T_{r_l}+T_{-r_l}\) is self-adjoint, so \(V_z(x)\) is skew-adjoint. Hence

\[
 \frac12\frac d{dx}\|F(x)\|_2^2
 =\langle D_qF,F\rangle
 =-\sum_r\lambda_{q,r}|F_r|^2\le0.
 \tag{1.7}
\]

Consequently

\[
 \|F(x)\|_2\le\sqrt M,
 \qquad
 \int_0^\infty\sum_r\lambda_{q,r}|F_r(x)|^2\,dx
 \le\frac M2.
 \tag{1.8}
\]

Both statements are exact and contain no Gronwall exponential.

---

## 2. A bounded-variation zero-sampling lemma

### Lemma 2.1 -- derivative mass at scalar zeros

Let \(g\in C^1([a,b];\mathbb C)\), with \(g'\) absolutely continuous. If

\[
 a\le\tau_1<\cdots<\tau_R\le b,
 \qquad g(\tau_m)=0,
 \tag{2.1}
\]

then

\[
 \boxed{
 \sum_{m=1}^R|g'(\tau_m)|^2
 \le |g'(\tau_1)|^2
 +\|g'\|_{L^\infty(a,b)}
 \int_a^b|g''(x)|\,dx.}
 \tag{2.2}
\]

#### Proof

For \(m\ge2\), the endpoint zeros imply

\[
 \int_{\tau_{m-1}}^{\tau_m}g'(s)\,ds=0.
 \tag{2.3}
\]

Writing \(\ell_m=\tau_m-\tau_{m-1}\), integration by parts gives

\[
 g'(\tau_m)
 =\frac1{\ell_m}\int_{\tau_{m-1}}^{\tau_m}
 (s-\tau_{m-1})g''(s)\,ds.
 \tag{2.4}
\]

Therefore

\[
 \sum_{m=2}^R|g'(\tau_m)|
 \le\int_a^b|g''(s)|\,ds.
 \tag{2.5}
\]

Multiplying by \(\|g'\|_\infty\) and adding the first root proves (2.2).
The proof works for complex scalars and has no root-separation factor.
\(\square\)

The same estimate applies to every finite subset of a larger zero set.
Taking the supremum over finite subsets defines the extended nonnegative sum.
Multiple roots have zero slope. If \(g\equiv0\), every sampled derivative is
zero.

---

## 3. Shear multiplier integrals

Write

\[
 a_l(x)=z_le^{-\kappa r_l^2x}.
 \tag{3.1}
\]

Under Fourier transform on \(\ell^2(\mathbb Z)\), \(V_z(x)\) is
multiplication by

\[
 m_x(\theta)=-2iK_z\sum_{l=1}^Ma_l(x)\cos(r_l\theta).
 \tag{3.2}
\]

Thus \(\|V_z(x)\|=\|m_x\|_{L^\infty(\mathbb T)}\). Normalized Haar
\(L^2\) gives

\[
 \Omega^2\ge\|V_z(A_0)\|^2
 \ge2K_z^2\sum_{l=1}^M|a_l(A_0)|^2.
 \tag{3.3}
\]

Because \(m_x\) is the torus heat evolution of \(m_{A_0}\),
\(L^\infty\) contractivity gives

\[
 \|V_z(x)\|\le\Omega
 \qquad(x\ge A_0).
 \tag{3.4}
\]

The time integral is controlled without a carrier-count loss:

\[
\begin{aligned}
 \int_{A_0}^\infty\|V_z(x)\|\,dx
 &\le \frac{2|K_z|}{\kappa}
 \sum_{l=1}^M\frac{|a_l(A_0)|}{r_l^2}\\
 &\le\frac{2|K_z|}{\kappa}
 \left(\sum_l|a_l(A_0)|^2\right)^{1/2}
 \left(\sum_{r=1}^\infty r^{-4}\right)^{1/2}\\
 &\le \frac{\pi^2}{\sqrt{45}\,\kappa}\Omega
 =C_\kappa\Omega.
\end{aligned}
 \tag{3.5}
\]

Combining (3.4) and (3.5),

\[
 \int_{A_0}^\infty\|V_z(x)\|^2\,dx
 \le C_\kappa\Omega^2.
 \tag{3.6}
\]

The summability of \(r^{-4}\), rather than an unweighted coefficient
\(\ell^1\) estimate, prevents a hidden \(M^{1/2}\) loss.

---

## 4. The target-row variation is paid by dissipation

Set

\[
 h(x)=P_0V_z(x)F(x).
 \tag{4.1}
\]

The target coordinate solves

\[
 F_0'=-\lambda_0F_0+\delta h.
 \tag{4.2}
\]

Differentiating \(h\) for \(x>A_0\) gives

\[
 h'+\lambda_0h
 =Q(x)F+\delta P_0V_z(x)^2F,
 \qquad
 Q=P_0\left[V_z'+V_z(D_q+\lambda_0)\right].
 \tag{4.3}
\]

Although \(D_q\) is unbounded, the row \(Q(x)\) is explicit. Its only
nonzero input coordinates are \(\pm r_l\). Apart from the common factor
\(-iK_za_l(x)\), their coefficients are

\[
\begin{array}{c|c}
 \text{input coordinate}&\text{coefficient}\\ \hline
 -r_l&-2\nu d^2r_l^2+2\nu dr_lK_y/q\\
 +r_l&-2\nu d^2r_l^2-2\nu dr_lK_y/q.
\end{array}
 \tag{4.4}
\]

Assume

\[
 q\ge q_*:=\max\left(1,\frac{2|K_y|}{d}\right).
 \tag{4.5}
\]

Since \(r_l\ge1\), each row coefficient is at most
\(3\nu d^2|K_z|r_l^2|a_l(x)|\). Put

\[
 A(x)^2=\sum_lr_l^2|a_l(x)|^2,
 \qquad
 \mathcal E(x)=\sum_r\lambda_{q,r}|F_r(x)|^2.
 \tag{4.6}
\]

Weighted Cauchy--Schwarz gives

\[
 |Q(x)F(x)|
 \le6\sqrt{2\nu}\,d|K_z|A(x)\mathcal E(x)^{1/2}.
 \tag{4.7}
\]

Moreover,

\[
 \int_{A_0}^\infty A(x)^2\,dx
 =\frac1{2\kappa}\sum_l|a_l(A_0)|^2
 \le\frac{\Omega^2}{4\kappa K_z^2}.
 \tag{4.8}
\]

Equations (1.8), (4.7), and (4.8) yield

\[
 \boxed{
 \int_{A_0}^\infty|Q(x)F(x)|\,dx
 \le3\Omega\sqrt M.}
 \tag{4.9}
\]

The combined row \(V_z'+V_z(D_q+\lambda_0)\) is essential. Estimating a
global \(\|D_qF\|_2\) first would introduce an unnecessary second spectral
moment. Equation (4.7) pairs exactly one carrier derivative with exactly one
dissipative derivative of \(F\).

Finally, (1.8), (3.6), and (4.9) give

\[
 \int_{I_x}|h'+\lambda_0h|\,dx
 \le\Omega\sqrt M\left(3+C_\kappa\eta\right).
 \tag{4.10}
\]

---

## 5. All-root slope-mass theorem

### Theorem 5.1 -- complete target-root packing

Assume (1.1)--(1.6), real shear, unit-modulus launched carrier phases, and
\(\delta\ne0\). For every finite set of exact roots

\[
 F_0(\tau_m)=0,
 \qquad A\le\tau_1<\cdots<\tau_R\le A+L,
 \tag{5.1}
\]

one has

\[
\boxed{
 \sum_{m=1}^R|F_0'(\tau_m)|^2
 \le e^{2\lambda_0L}\eta^2M
 \left(4+C_\kappa\eta\right).}
 \tag{5.2}
\]

Equivalently, because \(F_0'(\tau_m)=\delta h(\tau_m)\),

\[
\boxed{
 G_R^{\rm ex}:=\sum_{m=1}^R|h(\tau_m)|^2
 \le e^{2\lambda_0L}M\Omega^2
 \left(4+C_\kappa\eta\right).}
 \tag{5.3}
\]

The same bound holds for the extended sum over the complete root set.

#### Proof

Use the integrating factor

\[
 g(x)=e^{\lambda_0(x-A)}F_0(x).
 \tag{5.4}
\]

Equations (4.2)--(4.3) give

\[
 g'=\delta e^{\lambda_0(x-A)}h,
 \qquad
 g''=\delta e^{\lambda_0(x-A)}
 \left[QF+\delta P_0V_z^2F\right].
 \tag{5.5}
\]

Contraction and the definition of \(\eta\) imply

\[
 \|g'\|_{L^\infty(I_x)}
 \le e^{\lambda_0L}\eta\sqrt M.
 \tag{5.6}
\]

Equations (3.6) and (4.9) imply

\[
 \int_{I_x}|g''(x)|\,dx
 \le e^{\lambda_0L}\eta\sqrt M
 \left(3+C_\kappa\eta\right).
 \tag{5.7}
\]

Apply Lemma 2.1 and combine (5.6)--(5.7). This proves (5.2). At every root,
\(g'(\tau_m)=e^{\lambda_0(\tau_m-A)}\delta h(\tau_m)\), whose exponential
factor is at least one. Division by \(\delta^2\) proves (5.3).
\(\square\)

The theorem does not count roots; it makes their total positive-slope mass
summable. For the finite-support launch used in R0.71W--Y, positive-time
parabolic regularity makes \(g\in W^{2,1}(I_x)\). A multiple root costs zero.
If the target coordinate vanishes identically, its physical root slope and
atom measure vanish identically.

---

## 6. Launch-inclusive floor cancellation

Let roots be counted only on \(I_t=[a,b]\), while

\[
 K_t=[\sigma_q,b],
 \qquad
 \sigma_q=a-A_0q^{-2}.
 \tag{6.1}
\]

Assume the solution is nontrivial and classical on a neighborhood of \(K_t\),
so

\[
 0<\inf_{K_t}Y\le\sup_{K_t}Y<\infty.
 \tag{6.2}
\]

For every root \(t_*\in I_t\subset K_t\),

\[
\begin{aligned}
 \frac1{Y(t_*)\mathcal R_Y(K_t)}
 &=\frac{\inf_{K_t}Y}{Y(t_*)\sup_{K_t}Y}\\
 &\le\frac1{\sup_{K_t}Y}.
\end{aligned}
 \tag{6.3}
\]

This uses the single common factor \(1/\mathcal R_Y\) linearly inside the
atom sum; it does not duplicate that factor for different roots.

Put

\[
 E=S^2K_s+P^2K_v,
 \qquad
 K_s=\sum_{l=1}^Mr_l^2,
 \qquad
 K_v=\sum_{l=1}^Mr_l^2|z_l|^2.
 \tag{6.4}
\]

Launch orthogonality and Parseval give

\[
 \sup_{K_t}Y\ge Y(\sigma_q)\ge c_Yq^2E,
 \qquad
 D\ge c_Dq^2E.
 \tag{6.5}
\]

Neither lower bound requires the decoupled persistent background used in
R0.71W--Y.

The fixed target multiplier gives

\[
 \mathcal J_{\rm all}(I_t)
 \le C_TS^2P^2
 \sum_{t_*\in Z_*^+(I_t)}\frac{|h(t_*)|^2}{Y(t_*)}.
 \tag{6.6}
\]

Since the square bracket in (0.5) is at least \(\nu^2\), equations
(5.3), (6.3), (6.5), and (6.6) yield

\[
 \frac{\mathcal J_{\rm all}(I_t)}
 {D^{1/3}\Lambda_1(K_t;u)}
 \le C\nu^{-2}C_{\rm BV}(\eta)
 \frac{MS^2P^2\Omega^2}
 {q^{8/3}(S^2K_s+P^2K_v)^{4/3}}.
 \tag{6.7}
\]

Set

\[
 u=\frac{S^2K_s}{P^2K_v}.
 \tag{6.8}
\]

The scalar factor \(u(1+u)^{-4/3}\) is maximal at \(u=3\), with maximum
\(3/4^{4/3}\). Therefore

\[
 \frac{\mathcal J_{\rm all}(I_t)}
 {D^{1/3}\Lambda_1(K_t;u)}
 \le C\nu^{-2}C_{\rm BV}(\eta)
 \frac M{K_s}\eta^{4/3}
 \left(\frac{\Omega^2}{K_v}\right)^{1/3}.
 \tag{6.9}
\]

R0.71Y proved

\[
 \frac{\Omega^2}{K_v}\le\frac{2\pi^2K_z^2}{3},
 \qquad
 K_s\ge\frac{M(M+1)(2M+1)}6.
 \tag{6.10}
\]

Since \(e^{2\lambda_0L}\) is fixed by the physical observation window,
(6.9)--(6.10) prove

\[
 \boxed{
 \frac{\mathcal J_{\rm all}(I_t)}
 {D^{1/3}\Lambda_1(K_t;u)}
 \le C\nu^{-2}
 \frac{\eta^{4/3}(1+\eta)}{M^2}.}
 \tag{6.11}
\]

For \(M=2N+1\) and bounded \(\eta\), the complete ratio is \(O(N^{-2})\).
For large coupling, this estimate alone becomes nonvanishing at
\(\eta\asymp M^{6/7}\). That exponent is an upper-bound diagnostic, not a
construction of a strong-coupling root family.

The roots are not enlarged from \(I_t\) to \(K_t\). The pre-observation layer
may contain other roots and is not controlled by
\(\Omega=\sup_{x\ge A_0}\|V_z(x)\|\). Only the payment interval is enlarged.

The length changes from \(\ell=b-a\) to
\(\ell+A_0q^{-2}\). For the nonnegative normalized Lamb integrand,

\[
 \frac1{|K_t|}\int_{K_t}\frac{\|L\|_{\dot H^{-1}}^2}{Y}
 \ge\frac{\ell}{\ell+A_0q^{-2}}
 \frac1\ell\int_{I_t}\frac{\|L\|_{\dot H^{-1}}^2}{Y}.
 \tag{6.12}
\]

Also \(\mathcal R_Y(K_t)\ge\mathcal R_Y(I_t)\). Thus

\[
 \Lambda_1(K_t)\ge
 \frac{\ell}{\ell+A_0q^{-2}}\Lambda_1(I_t).
 \tag{6.13}
\]

No reverse uniform bound is claimed; the pre-observation layer can only make
the complete payment larger.

---

## 7. Why a fixed interval excluding launch is different

If the ledger must use \(I_t=[a,b]\), (6.3) still gives

\[
 \frac1{Y(t_*)\mathcal R_Y(I_t)}
 \le\frac1{\sup_{I_t}Y}.
 \tag{7.1}
\]

Define the retention factor

\[
 \theta_I
 =\frac{\sup_{I_t}Y}{q^2(S^2K_s+P^2K_v)}.
 \tag{7.2}
\]

The resulting estimate is (6.11) multiplied by \(\theta_I^{-1}\). No
uniform positive lower bound for \(\theta_I\) follows from launch data.
The exact heat shear

\[
 u_{q,R}(t)=
 \left(0,0,
 Ae^{-\nu(dRq)^2(t-\sigma_q)}\sin(dRq\,y)\right)
 \tag{7.3}
\]

is a global unforced NSE solution with zero projected Lamb term. It satisfies

\[
 D_{q,R}\asymp A^2q^2R^2,
 \qquad
 \sup_{I_t}Y\asymp
 A^2q^2R^2e^{-2\nu d^2R^2A_0}.
 \tag{7.4}
\]

Hence \(\theta_I\to0\) as \(R\to\infty\). This strictly disproves the hidden
retention implication

\[
 D\gtrsim q^2E
 \quad\Longrightarrow\quad
 \sup_{I_t}Y\gtrsim q^2E.
 \tag{7.5}
\]

The pure heat shear has no nonzero target-root atom. It is therefore not a
counterexample to every possible fixed-window floor-free atom theorem. It
only proves that such a theorem cannot obtain uniform retention from the
launch data by this step. Three honest alternatives remain:

1. compute \(\Lambda_1\) on the launch-inclusive interval \(K_t\);
2. retain a matched background or root-time floor;
3. assume \(\theta_I\ge\theta_0>0\).

R0.71Z uses the first alternative and does not identify the two windows.

---

## 8. Computational certificates

The analytic proof is primary. Two finite calculations audit different
parts.

1. The high-precision producer checks the amplitude optimizer, \(M^{-2}\)
   lattice factor, bounded- and strong-coupling powers, the floor-cancellation
   identity, and heat-retention loss.
2. The independent finite-matrix program constructs the shift generator and
   row \(Q\) without importing the producer. It checks skew-adjointness,
   contraction, the exact \(Q\)-coefficient formula, dissipative payment, and
   the bounded-variation sampling inequality.

The calculations do not prove the infinite-lattice theorem, certify a
growing-dimensional IFT branch, or time-step three-dimensional turbulence.
The formal figure shows only audited envelopes, exact algebraic factors, and
the retention boundary.

---

## 9. Literature boundary

The proof is compared with four neighboring literatures.

1. Karlin--Studden ECT theory and total positivity control zeros of finite
   exponential systems. They do not control the infinite nonlinear Dyson
   target coordinate and are not used in Theorem 5.1.
2. Exponential-sum sampling and moment-method estimates quantify dimension,
   gap, and observation-time losses for different systems. They do not contain
   the exact root-coordinate identity or the dissipation-paired row \(Q\).
3. Analytic-semigroup and maximal-regularity theory supplies the classical
   positive-time differentiability framework. The present proof needs only
   the explicitly differentiated target row and proves its own integrals.
4. NSE time-analyticity results imply isolated temporal zeros unless a target
   coordinate vanishes identically. Analyticity alone supplies neither the
   squared-slope mass bound nor its \(M^{-2}\) endpoint payment.

The bounded primary-source audit found no source that states Theorem 5.1 or
(6.11). This is a non-collision check, not a claim of originality, priority,
or nonexistence.

---

## 10. Claim--evidence boundary

### Proved

1. A complex-scalar BV zero-sampling inequality independent of zero count and
   separation.
2. Exact active-sector contraction and integrated dissipation for real shear.
3. Dimension-free \(L_x^1\) and \(L_x^2\) bounds for the heat-decaying shear
   multiplier in terms of its observation-layer operator norm.
4. A dimension-free dissipative payment for
   \(P_0[V'+V(D_q+\lambda_0)]\).
5. Complete all-root squared-slope mass bounded by
   \(CM\Omega^2(1+\delta_{\rm obs})\).
6. Launch-inclusive cancellation of the root-time floor through
   \(\mathcal R_Y\), followed by the normalized all-root bound
   \(C\nu^{-2}M^{-2}\delta_{\rm obs}^{4/3}(1+\delta_{\rm obs})\).
7. The fixed-window version pays the explicit retention loss
   \(\theta_I^{-1}\), which is not uniformly bounded over the declared class.

### Not proved

1. A uniform raw count of all nonlinear target zeros.
2. A floor-free theorem on every fixed window excluding launch and having no
   retention hypothesis.
3. A strong-coupling exact-root construction near the \(M^{6/7}\) diagnostic.
4. Uniformity as \(A_0\downarrow0\), non-unit or sparse launch phases, complex
   shear, non-diagonal target generators, or different Fourier geometries.
5. A universal \(D^{1/3}\Lambda_1\) estimate for general three-dimensional
   Navier--Stokes solutions.
6. A continuation criterion, finite-time singularity, or global regularity.

---

## 11. Research value and next gate

R0.71Y left two concrete loopholes in the bounded-coupling triangular route:
quadratically many uncounted roots and the cost of a matched root-time floor.
R0.71Z closes both when the actual object is the all-root slope measure and
the complete payment interval includes launch. The improvement is from a
selected-root \(N^{-1}\) suppression to complete all-root \(N^{-2}\)
suppression under bounded coupling.

This is a structural closure only for the declared exact triangular class. It
does not narrow the full set of possible three-dimensional NSE singular
mechanisms. The next finite gate should test one surviving change of regime:

1. observation coupling growing toward the \(M^{6/7}\) diagnostic, with an
   exact-root construction and full nonlinear charge;
2. \(A_{0,M}\downarrow0\), where observation and launch layers merge;
3. sparse or non-unit carrier phases, where \(K_s\gtrsim M^3\) changes;
4. a non-triangular geometry in which the target heat coordinate no longer
   cancels exactly at a root.

None is promoted to a result before its proof and certificate close.
