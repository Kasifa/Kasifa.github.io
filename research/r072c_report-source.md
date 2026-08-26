# R0.72C -- physical phases, heat participation, and the sharp phase-free carrier scale

**Date:** 2026-08-27
**Status:** analytic proof independently audited; deterministic producer and
independent checker passed. The claims in Sections 2--7 are analytic statements
inside the finite-carrier triangular 2.5D class. No statement concerns general
three-dimensional Navier--Stokes regularity.

**Keywords:** Navier--Stokes regularity, triangular 2.5D flows, physical Fourier
phases, target-row participation, Rudin--Shapiro polynomials, heat burn-in,
complete root ledger

---

## 0. Direct decision

R0.72B proved, for real shear coefficients and \(\delta\ne0\), the normalized
complete-root ledger

\[
 \frac{\mathcal J_{\rm all}}{D^{1/3}\Lambda_1}
 \le C\nu^{-2}e^{2\lambda_0L}
 \frac M{K_s}\eta^{4/3}
 \chi_A\left(\frac{\Omega_A^2}{K_v}\right)^{1/3}
 \left[1+q_\rho+\eta\ell_\times\right].
 \tag{0.1}
\]

Here

\[
 \chi_A=\frac{\rho_A^2}{\Omega_A^2},\qquad
 q_\rho\le3,\qquad
 \ell_\times\le\min\{L,C_\times\}.
 \tag{0.2}
\]

Same-sign comparable coefficients at exact launch give the coherent geometric
factor

\[
 \Phi_{0,M}:=
 \frac M{K_s}\chi_0
 \left(\frac{\Omega_0^2}{K_v}\right)^{1/3}
 =O(M^{-10/3}).
 \tag{0.3}
\]

R0.72C answers the two questions left open there.

1. Arbitrary physical Fourier phases preserve the complete-root theorem only
   after the two opposite shifts are paired by complex conjugation. A naive
   complexification of the R0.72B formula destroys skew-adjointness.
2. The two phase-sensitive factors in (0.1) must be estimated jointly:

\[
 \boxed{
 \chi_A\left(\frac{\Omega_A^2}{K_v}\right)^{1/3}
 \le\left(\frac{\rho_A^2}{K_v}\right)^{1/3}.}
 \tag{0.4}
\]

For pairwise distinct positive integer carriers and comparable coefficient
moduli, define

\[
 H_M(A)=\sum_{j=1}^M e^{-2\kappa A j^2}.
 \tag{0.5}
\]

Then, uniformly in all physical phases,

\[
 \boxed{
 \Phi_{A,M}\le C(K_z,c_+/c_-)
 M^{-3}H_M(A)^{1/3}.}
 \tag{0.6}
\]

Consequently,

\[
 \Phi_{0,M}=O(M^{-8/3}),
 \qquad
 \Phi_{A_*,M}
 =O_{\nu,d,A_*,K_z,c_+/c_-}(M^{-3})
 \quad(A_*>0\text{ fixed}).
 \tag{0.7}
\]

Both exponents are sharp for the displayed algebraic prefactor. At exact
launch, a Rudin--Shapiro sign family along
\(M=2^n\) with odd \(n\) has

\[
 \Phi_{0,M}\asymp M^{-8/3},
 \tag{0.8}
\]

so the coherent \(M^{-10/3}\) rate cannot hold uniformly over phases. At fixed
positive \(A_*\), the canonical same-sign family has

\[
 \Phi_{A_*,M}\asymp M^{-3}.
 \tag{0.9}
\]

This sharpness concerns the coefficient in an upper ledger. It is not a lower
bound on the actual root mass, not a singularity construction, and not a
continuation theorem for general Navier--Stokes solutions.

---

## 1. Why the phase model must change

Fix \(\nu>0\), \(d\ge1\), a target frequency
\(k_*=(K_y,K_z)\) with \(K_z\ne0\), and pairwise distinct positive integers
\(r_1,\ldots,r_M\). As in R0.72B,

\[
 (D_qF)_r=-\lambda_{q,r}F_r,
 \qquad
 \lambda_{q,r}=\nu\left[
 \left(dr+\frac{K_y}{q}\right)^2+\frac{K_z^2}{q^2}
 \right],
 \tag{1.1}
\]

\[
 \partial_xF=D_qF+\delta V_w(x)F,
 \qquad
 \delta=\frac P{q^2},
 \qquad \delta\in\mathbb R,
 \qquad
 \|F(0)\|_2^2=M,
 \tag{1.2}
\]

with finite-support launch data and

\[
 q\ge q_*:=\max\left(1,\frac{2|K_y|}{d}\right),
 \qquad \kappa=\nu d^2.
 \tag{1.3}
\]

### 1.1 Naive complexification fails

The R0.72B operator was

\[
 -iK_z\sum_l z_le^{-\kappa r_l^2x}
 (T_{r_l}+T_{-r_l}),
 \tag{1.4}
\]

with \(z_l\in\mathbb R\). The shift sum is self-adjoint, so (1.4) is
skew-adjoint. Merely allowing \(z_l\in\mathbb C\) is invalid. For one carrier
and \(z_1=i\), (1.4) becomes

\[
 K_z(T_1+T_{-1}),
 \tag{1.5}
\]

which is self-adjoint. With \(F=(e_0+e_1)/\sqrt2\), the instantaneous energy
derivative contains

\[
 \frac12\frac d{dx}\|F\|_2^2
 =-\frac{\lambda_{q,0}+\lambda_{q,1}}2+\delta K_z.
 \tag{1.6}
\]

It is positive for sufficiently large \(\delta K_z\). Thus the exact energy
identity, dissipation budget, and all later root-ledger estimates would fail.

### 1.2 Conjugate pairing is the physical phase extension

For \(w_l\in\mathbb C\), define instead

\[
 \boxed{
 (V_w(x)F)_r=-iK_z\sum_{l=1}^M e^{-\kappa r_l^2x}
 \left(w_lF_{r-r_l}+\overline{w_l}F_{r+r_l}\right).}
 \tag{1.7}
\]

Under Fourier transform on \(\ell^2(\mathbb Z)\), this is multiplication by

\[
 m_x(\theta)
 =-iK_z\sum_l e^{-\kappa r_l^2x}
 \left(w_le^{ir_l\theta}+\overline{w_l}e^{-ir_l\theta}\right)
 =-ib(x,\theta),
 \tag{1.8}
\]

where

\[
 b(x,\theta)
 =2K_z\operatorname{Re}\sum_l
 w_le^{-\kappa r_l^2x}e^{ir_l\theta}
 \tag{1.9}
\]

is real. Hence \(V_w(x)^*=-V_w(x)\), and

\[
 \frac12\frac d{dx}\|F(x)\|_2^2
 =-\sum_r\lambda_{q,r}|F_r(x)|^2\le0,
 \tag{1.10}
\]

\[
 \|F(x)\|_2\le\sqrt M,
 \qquad
 \int_0^\infty\sum_r\lambda_{q,r}|F_r(x)|^2\,dx
 \le\frac M2.
 \tag{1.11}
\]

Writing \(w_l=|w_l|e^{i\phi_l}\), equation (1.9) is the real shear

\[
 b(x,\theta)=2K_z\sum_l|w_l|e^{-\kappa r_l^2x}
 \cos(r_l\theta+\phi_l).
 \tag{1.12}
\]

Thus (1.7), rather than (1.4) with complex coefficients, is the correct
arbitrary-phase model.

---

## 2. Phase-stable target-row theorem

For \(A_0\ge0\), put

\[
 \Omega_A=\sup_{x\ge A_0}\|V_w(x)\|,
 \qquad
 \eta=|\delta|\Omega_A,
 \qquad
 \lambda_0=\lambda_{q,0},
 \tag{2.1}
\]

and

\[
 \rho(x)^2
 :=\|P_0V_w(x)\|_{\ell^2\to\mathbb C}^2
 =2K_z^2\sum_l|w_l|^2e^{-2\kappa r_l^2x},
 \qquad
 \rho_A=\rho(A_0).
 \tag{2.2}
\]

Normalized Haar Parseval applied to (1.9) gives

\[
 \rho_A\le\|V_w(A_0)\|\le\Omega_A.
 \tag{2.3}
\]

The multiplier \(m_x\) is the torus heat evolution of \(m_{A_0}\). The
\(L^\infty\) heat contraction and the coefficient estimate from R0.71Z give

\[
 \Omega_A=\|V_w(A_0)\|,
 \tag{2.4}
\]

\[
 \int_{A_0}^\infty\|V_w(x)\|^2\,dx
 \le C_\kappa\Omega_A^2,
 \qquad
 C_\kappa=\frac{\pi^2}{\sqrt{45}\,\kappa}.
 \tag{2.5}
\]

No sign assumption is used: the proof applies the triangle inequality to
\(|w_l|/r_l^2\) and Parseval to \(\sum|w_l|^2\). Direct integration also gives

\[
 \int_{A_0}^\infty\rho(x)^2\,dx
 \le\frac{\rho_A^2}{2\kappa}.
 \tag{2.6}
\]

If \(\rho_A=0\), all positive heat weights in (2.2) force
\(w_l=0\) for every \(l\). Then \(V_w\equiv Q\equiv0\),
\(\Omega_A=\eta=0\), and every target-row slope and root-mass sum below is
zero. On this degenerate branch set
\(q_\rho=\ell_\times=\chi_A=0\) before taking any quotient. The rest of
Sections 2--7 assumes \(\rho_A>0\), equivalently a nonzero carrier profile.

Therefore

\[
 \ell_\times(I)
 :=\frac1{\rho_A\Omega_A}
 \int_I\rho(x)\|V_w(x)\|\,dx
 \le\min\{L,C_\times\},
 \tag{2.7}
\]

where

\[
 C_\times=\sqrt{\frac{C_\kappa}{2\kappa}}
 =\frac{\pi}{\sqrt2\,45^{1/4}\kappa}.
 \tag{2.8}
\]

Let

\[
 Q=P_0\left[V_w'+V_w(D_q+\lambda_0)\right].
 \tag{2.9}
\]

The two entries associated with one carrier contain \(w_l\) and
\(\overline{w_l}\), and hence have the same moduli as in the real-coefficient
calculation. The dissipation-paired estimate remains

\[
 \int_{A_0}^\infty|Q(x)F(x)|\,dx
 \le3\rho_A\sqrt M.
 \tag{2.10}
\]

For \(\rho_A>0\), set

\[
 q_\rho(I)=\frac1{\rho_A\sqrt M}
 \int_I|Q(x)F(x)|\,dx\le3.
 \tag{2.11}
\]

The nonlinear row estimate is phase-free:

\[
 |P_0V_w(x)^2F(x)|
 \le\rho(x)\|V_w(x)\|\sqrt M.
 \tag{2.12}
\]

### Theorem 2.1 -- complete target-root ledger with physical phases

Let \(I=[A,A+L]\subset[A_0,\infty)\). Under (1.1)--(1.3) and the
conjugate-paired operator (1.7), every finite set of exact target roots
satisfies

\[
 \boxed{
 \sum_{F_0(\tau_j)=0}|F_0'(\tau_j)|^2
 \le e^{2\lambda_0L}\delta^2M\rho_A^2
 \left[1+q_\rho(I)+\eta\ell_\times(I)\right].}
 \tag{2.12a}
\]

If \(\delta\ne0\), then

\[
 \boxed{
 G_{\rm all}^{\rm ex}(I)
 :=\sum_{F_0(\tau)=0}|P_0V_w(\tau)F(\tau)|^2
 \le e^{2\lambda_0L}M\rho_A^2
 \left[1+q_\rho(I)+\eta\ell_\times(I)\right].}
 \tag{2.13}
\]

The slope estimate holds for its complete extended nonnegative sum. When
\(\delta\ne0\), the same is true for \(G_{\rm all}^{\rm ex}\). In particular,

\[
 \boxed{
 G_{\rm all}^{\rm ex}(I)
 \le e^{2\lambda_0L}M\rho_A^2
 \left[4+\eta\min\{L,C_\times\}\right].}
 \tag{2.14}
\]

#### Proof

Set \(h=P_0V_wF\) and
\(g(x)=e^{\lambda_0(x-A)}F_0(x)\). Then

\[
 g'=\delta e^{\lambda_0(x-A)}h,
 \qquad
 g''=\delta e^{\lambda_0(x-A)}
 \left[QF+\delta P_0V_w^2F\right].
 \tag{2.15}
\]

Equations (1.11), (2.2), and (2.10)--(2.12) give

\[
 \|g'\|_\infty
 \le e^{\lambda_0L}|\delta|\rho_A\sqrt M,
 \tag{2.16}
\]

\[
 \int_I|g''|
 \le e^{\lambda_0L}|\delta|\rho_A\sqrt M
 \left[q_\rho+\eta\ell_\times\right].
 \tag{2.17}
\]

The scalar bounded-variation zero-sampling lemma gives, for every finite set
of zeros \(\tau_j\),

\[
 \sum_j|g'(\tau_j)|^2
 \le |g'(\tau_1)|^2
 +\|g'\|_\infty\int_I|g''|.
 \tag{2.18}
\]

Equations (2.16)--(2.18), followed by the monotone supremum over finite root
subsets, prove (2.12a). At a target root, \(F_0'=\delta h\). If
\(\delta\ne0\), division by \(\delta^2\) proves (2.13). No target-row
conclusion is inferred by division on the \(\delta=0\) branch. The zero-row
branch was defined before division above. \(\square\)

The normalized optimizer from R0.72B is unchanged. With

\[
 K_s=\sum_lr_l^2,
 \qquad
 K_v=\sum_lr_l^2|w_l|^2,
 \tag{2.19}
\]

for \(\delta\ne0\), the complete physical-time ledger satisfies (0.1), now
for all physical phases in (1.7). The full nonnegative rotational charge
remains inside the exact denominator \(\Lambda_1\).

The historical subscript \(A\) in
\(\Omega_A,\rho_A,\chi_A\), and \(\Phi_{A,M}\) records the restart layer:
these quantities are evaluated at \(A_0\). The interval left endpoint is the
separate variable \(A\) in \(I=[A,A+L]\). Every fixed-positive-time result
below explicitly takes \(A_0=A=A_*\).

---

## 3. The joint phase inequality

The participation factor alone can be order one after phase cancellation.
The multiplier-to-carrier moment then becomes smaller. Estimating the two
quantities independently loses this compensation. Algebra gives

\[
\begin{aligned}
 \chi_A\left(\frac{\Omega_A^2}{K_v}\right)^{1/3}
 &=\frac{\rho_A^2}{\Omega_A^2}
 \frac{\Omega_A^{2/3}}{K_v^{1/3}}\\
 &=\frac{\rho_A^2}{\Omega_A^{4/3}K_v^{1/3}}\\
 &\le\frac{\rho_A^{2/3}}{K_v^{1/3}}
 =\left(\frac{\rho_A^2}{K_v}\right)^{1/3},
\end{aligned}
 \tag{3.1}
\]

because \(\Omega_A\ge\rho_A\). This proves (0.4).

For diagnostics, write

\[
 Z_{1,A}=\sum_l|w_l|e^{-\kappa A_0r_l^2},
 \qquad
 Z_{2,A}=\sum_l|w_l|^2e^{-2\kappa A_0r_l^2},
 \tag{3.2}
\]

and

\[
 N_{\rm eff}(A_0)=\frac{Z_{1,A}^2}{Z_{2,A}}.
 \tag{3.3}
\]

The triangle and Parseval bounds yield

\[
 \rho_A^2=2K_z^2Z_{2,A},
 \qquad
 \rho_A\le\Omega_A\le2|K_z|Z_{1,A},
 \tag{3.4}
\]

and hence

\[
 \boxed{
 \frac1{2N_{\rm eff}(A_0)}\le\chi_A\le1.}
 \tag{3.5}
\]

Equation (3.5) explains why an effective-carrier diagnostic cannot by itself
predict phase cancellation. Equation (3.1), not a separate upper estimate for
\(\chi_A\), is the uniform tool.

---

## 4. Uniform heat-participation theorem

Assume that a scale \(a_M>0\) and constants independent of \(M\) satisfy

\[
 0<c_-a_M\le|w_l|\le c_+a_M.
 \tag{4.1}
\]

After sorting the distinct positive integers, \(r_{(j)}\ge j\). Therefore

\[
 K_s\ge S_M:=\frac{M(M+1)(2M+1)}6\ge\frac{M^3}{3},
 \tag{4.2}
\]

\[
 K_v\ge c_-^2a_M^2K_s,
 \tag{4.3}
\]

and

\[
 \rho_A^2
 \le2K_z^2c_+^2a_M^2
 \sum_{j=1}^M e^{-2\kappa A_0j^2}
 =2K_z^2c_+^2a_M^2H_M(A_0).
 \tag{4.4}
\]

### Theorem 4.1 -- phase-free carrier prefactor

Under (4.1),

\[
\begin{aligned}
 \Phi_{A,M}
 &:=\frac M{K_s}\chi_A
 \left(\frac{\Omega_A^2}{K_v}\right)^{1/3}\\
 &\le
 (2K_z^2)^{1/3}
 \left(\frac{c_+}{c_-}\right)^{2/3}
 \frac{M H_M(A_0)^{1/3}}{K_s^{4/3}}\\
 &\le
 3\left[6K_z^2
 \left(\frac{c_+}{c_-}\right)^2\right]^{1/3}
 M^{-3}H_M(A_0)^{1/3}.
\end{aligned}
 \tag{4.5}
\]

#### Proof

Equation (3.1) and (4.3)--(4.4) give the first displayed upper bound.
Equation (4.2) gives the second. \(\square\)

At exact launch, \(A_0=0\) and \(H_M(0)=M\), so

\[
 \boxed{
 \Phi_{0,M}=O(M^{-8/3})}
 \tag{4.6}
\]

uniformly in all phases. For a fixed \(A_*>0\), take
\(A_0=A=A_*\). Then

\[
 H_M(A_*)
 \le\sum_{j=1}^\infty e^{-2\kappa A_*j^2}
 \le\frac{\sqrt\pi}{2\sqrt{2\kappa A_*}},
 \tag{4.7}
\]

so

\[
 \boxed{
 \Phi_{A_*,M}=O_{\nu,d,A_*}(M^{-3}).}
 \tag{4.8}
\]

The fixed-positive-time statement concerns roots observed from \(A_*\). The
nonnegative ledger accumulated on \([0,A_*]\) remains a separate pre-ledger.

---

## 5. Burn-in transition scales

Put

\[
 t_M=\kappa A_{0,M},
 \qquad
 H_M(t_M)=\sum_{j=1}^M e^{-2t_Mj^2}.
 \tag{5.1}
\]

There are three elementary regimes.

### 5.1 Sub-carrier burn-in: \(t_MM^2\to0\)

Uniformly for \(1\le j\le M\), \(e^{-2t_Mj^2}=1+o(1)\). Hence

\[
 H_M(t_M)=M(1+o(1)),
 \qquad
 \Phi_{A,M}=O(M^{-8/3}).
 \tag{5.2}
\]

### 5.2 Critical burn-in: \(t_MM^2\to c\in(0,\infty)\)

The Riemann sum gives

\[
 \frac{H_M(t_M)}M
 \longrightarrow\int_0^1e^{-2cs^2}\,ds,
 \tag{5.3}
\]

so the exponent remains \(M^{-8/3}\), with a smaller constant.

### 5.3 Effective-carrier burn-in: \(t_MM^2\to\infty\)

If \(t_M\to0\), the theta-sum asymptotic gives

\[
 H_M(t_M)\sim\frac{\sqrt\pi}{2\sqrt{2t_M}},
 \qquad
 \Phi_{A,M}=O(M^{-3}t_M^{-1/6}).
 \tag{5.4}
\]

If \(t_M\to t_*>0\), then

\[
 H_M(t_M)\longrightarrow
 \sum_{j=1}^\infty e^{-2t_*j^2}<\infty,
 \tag{5.5}
\]

and (4.8) follows.

If \(t_M\to\infty\), the first carrier dominates:

\[
 H_M(t_M)
 =e^{-2t_M}\left[1+O(e^{-6t_M})\right],
 \qquad
 \Phi_{A,M}
 =O\!\left(M^{-3}e^{-2t_M/3}\right).
 \tag{5.5a}
\]

In particular, if

\[
 A_{0,M}\asymp M^{-\sigma},
 \tag{5.6}
\]

then

\[
 \Phi_{A,M}=O(M^{-p_\sigma}),
 \qquad
 p_\sigma=
 \begin{cases}
 3-\sigma/6,&0<\sigma<2,\\
 8/3,&\sigma\ge2.
 \end{cases}
 \tag{5.7}
\]

Fixed positive burn-in corresponds to \(p=3\).

---

## 6. Sufficient phase regions

Suppose the geometric prefactor obeys

\[
 \Phi_{A,M}=O(M^{-p}),
 \tag{6.1}
\]

and take

\[
 \eta_M=M^\alpha,
 \qquad
 L_M=M^{-\beta},
 \tag{6.2}
\]

with bounded \(\lambda_{0,M}L_M\). The constant term in the bracket in
(2.14) vanishes after normalization when

\[
 -p+\frac{4\alpha}{3}<0.
 \tag{6.3}
\]

Using \(\ell_\times\le L_M\), the local-exposure term vanishes when

\[
 -p+\frac{7\alpha}{3}-\beta<0.
 \tag{6.4}
\]

Thus the sufficient region is

\[
 \boxed{
 \alpha<\min\left\{
 \frac{3p}{4},\frac{3p+3\beta}{7}
 \right\}.}
 \tag{6.5}
\]

At exact launch, arbitrary physical phases have \(p=8/3\), giving

\[
 \boxed{
 \alpha<\min\left\{2,\frac{8+3\beta}{7}\right\}.}
 \tag{6.6}
\]

For \(A_{0,M}\asymp M^{-\sigma}\), \(0<\sigma<2\),

\[
 \boxed{
 \alpha<\min\left\{
 \frac94-\frac\sigma8,
 \frac{9-\sigma/2+3\beta}{7}
 \right\}.}
 \tag{6.7}
\]

For fixed \(A_*>0\),

\[
 \boxed{
 \alpha<\min\left\{
 \frac94,\frac{9+3\beta}{7}
 \right\}.}
 \tag{6.8}
\]

These are sufficient upper regions. Equality lines and exterior points are
not converses.

### 6.1 Fixed \(\eta\) and fixed \(\delta\) are different comparisons

The phase comparison above holds at fixed effective coupling
\(\eta=|\delta|\Omega_A\). If the raw coupling \(\delta\) is fixed instead,
the multiplier norm cancels from the leading normalized coefficient:

\[
 \eta^{4/3}\Phi_{A,M}
 =|\delta|^{4/3}\frac M{K_s}
 \frac{\rho_A^2}{K_v^{1/3}}.
 \tag{6.9}
\]

This leading factor is phase-independent when the coefficient moduli are
fixed. The complete bracket is not automatically phase-independent:
\(\eta\ell_\times\) still contains the actual multiplier exposure, and
\(q_\rho\) is evaluated along the phase-dependent solution. The
Rudin--Shapiro failure of the coherent \(M^{-10/3}\) rate must therefore be
read as a fixed-\(\eta\) geometric comparison, exactly as in the
\((\alpha,\beta)\) phase diagram.

---

## 7. Sharpness of the algebraic prefactor

### 7.1 Rudin--Shapiro exact-launch family

For \(M=2^n\), define

\[
 P_0(z)=Q_0(z)=1,
 \tag{7.1}
\]

\[
 P_{n+1}(z)=P_n(z)+z^{2^n}Q_n(z),
 \qquad
 Q_{n+1}(z)=P_n(z)-z^{2^n}Q_n(z).
 \tag{7.2}
\]

Write

\[
 P_n(z)=\sum_{j=0}^{M-1}\varepsilon_jz^j,
 \qquad \varepsilon_j\in\{-1,1\}.
 \tag{7.3}
\]

The parallelogram identity gives, on \(|z|=1\),

\[
 |P_n(z)|^2+|Q_n(z)|^2=2M,
 \tag{7.4}
\]

and hence

\[
 \|P_n\|_\infty\le\sqrt{2M}.
 \tag{7.5}
\]

For odd \(n\), the recurrence at \(z=1\) gives

\[
 P_n(1)=\sqrt{2M}.
 \tag{7.6}
\]

Choose

\[
 r_l=l,
 \qquad
 w_l=a_M\varepsilon_{l-1}.
 \tag{7.7}
\]

This is already a legal real shear, with phases \(0\) and \(\pi\). Equations
(7.5)--(7.6) give the exact multiplier norm

\[
 \Omega_0=2|K_z|a_M\sqrt{2M}.
 \tag{7.8}
\]

Also,

\[
 K_s=S_M,
 \qquad
 K_v=a_M^2S_M,
 \qquad
 \rho_0^2=2K_z^2a_M^2M,
 \qquad
 \chi_0=\frac14.
 \tag{7.9}
\]

Therefore

\[
 \boxed{
 \Phi_{0,M}
 =\frac{|K_z|^{2/3}}2
 \left(\frac M{S_M}\right)^{4/3}
 \sim\frac{3^{4/3}}2|K_z|^{2/3}M^{-8/3}.}
 \tag{7.10}
\]

In particular,

\[
 M^{10/3}\Phi_{0,M}\asymp M^{2/3}\longrightarrow\infty.
 \tag{7.11}
\]

Thus a phase-uniform \(O(M^{-10/3})\) bound is false, and the exponent in
(4.6) is optimal for \(\Phi_{0,M}\).

The recursion and identity (7.2)--(7.4) are classical. A modern primary
source recording them is T. Erdelyi,
[*The L-q norm of the Rudin--Shapiro polynomials on subarcs of the unit
circle*](https://arxiv.org/abs/2311.04395), arXiv:2311.04395 (2023),
equations (1.1)--(1.3). P. Balister,
[*Bounds on Rudin--Shapiro polynomials of arbitrary degree*](https://arxiv.org/abs/1909.08777),
arXiv:1909.08777 (2019), records the coefficient recursion and the binary
description used by the certificate implementation.

### 7.2 Fixed positive observation time

Fix \(A_0=A=A_*>0\), put \(t=\kappa A_*\), take \(r_l=l\), and set
\(w_l=a_M>0\). Define

\[
 H_{t,M}=\sum_{l=1}^Me^{-tl^2},
 \qquad
 J_{t,M}=\sum_{l=1}^Me^{-2tl^2}.
 \tag{7.12}
\]

The same-sign heat-weighted profile has

\[
 \Omega_A=2|K_z|a_MH_{t,M},
 \qquad
 \rho_A^2=2K_z^2a_M^2J_{t,M},
 \qquad
 \chi_A=\frac{J_{t,M}}{2H_{t,M}^2}.
 \tag{7.13}
\]

Consequently,

\[
 \boxed{
 \Phi_{A,M}
 =2^{-1/3}|K_z|^{2/3}
 \frac{M J_{t,M}}
 {S_M^{4/3}H_{t,M}^{4/3}}
 \asymp M^{-3}.}
 \tag{7.14}
\]

Both heat sums converge to finite positive limits. Thus the fixed-positive
exponent in (4.8) is also optimal for the algebraic prefactor.

---

## 8. Enhanced-dissipation boundary

The physical-phase extension changes the frozen profile to

\[
 b(x,\theta)=2K_z\operatorname{Re}\sum_l
 w_le^{-\kappa r_l^2x}e^{ir_l\theta}.
 \tag{8.1}
\]

Existing enhanced-dissipation theorems checked for this release cover fixed
profiles, profiles with uniformly controlled moving critical points, scalar
time modulation of one fixed spatial shape, or a translating sine. They do
not supply constants uniform in the present \(M\)-dependent heat-decaying
phase family, and they do not estimate a launch-inclusive target-root slope
ledger.

The closest time-dependent result is D. Coble and S. He,
[*A Note on Enhanced Dissipation and Taylor Dispersion of Time-dependent
Shear Flows*](https://arxiv.org/abs/2309.15738), Commun. Math. Sci. 22
(2024). Its hypotheses retain a fixed finite critical structure, uniform
shape bounds, and slow motion relative to a reference shear. J. Benthaus and
C. Nobili,
[*Enhanced Dissipation via time-modulated velocity fields*](https://arxiv.org/abs/2501.16905)
(2025), keeps one fixed spatial profile and modulates it by a scalar function.
J. Benthaus, G. M. Coclite, and C. Nobili,
[*Mixing and enhanced dissipation in a time-translating shear flow*](https://arxiv.org/abs/2603.14624)
(2026), treats a rigidly translating sine profile. V. Gardner, K. L. Liss,
and J. C. Mattingly,
[*A pathwise approach to the enhanced dissipation of passive scalars advected
by shear flows*](https://arxiv.org/abs/2410.05657) (2024), treats fixed shear
profiles through local streamline geometry.

Any separately proved terminal energy decay can still improve the restarted
tail theorem from R0.72B. It cannot subtract the nonnegative pre-ledger:

\[
 G_{\rm all}^{\rm ex}([0,A_*+L])
 =G_{\rm pre}^{\rm ex}([0,A_*])
 +G_{\rm tail}^{\rm ex}((A_*,A_*+L]).
 \tag{8.2}
\]

For any proposed phase family, the audit must therefore continue to record

\[
 (\eta_M,L_M,n_M,c_{{\rm sub},M},
 L_M\kappa r_{\max,M}^2,N_{\rm eff},\chi_M,
 \Theta_M,\Xi_M).
 \tag{8.3}
\]

The Rudin--Shapiro family in Section 7 is an algebraic sharpness family. No
uniform critical-point, sublevel, or enhanced-dissipation assertion is made
for it.

---

## 9. What has and has not been proved

The completed analytic content is:

1. a necessary correction from naive complex coefficients to a
   conjugate-paired real-shear operator;
2. a phase-stable extension of the target-row complete-root theorem with the
   same constants \(3\) and \(C_\times\);
3. the joint inequality (3.1), which couples participation loss to multiplier
   cancellation;
4. the phase-uniform heat-participation bound (4.5);
5. exact-launch, transition-layer, and fixed-positive-time sufficient regions;
6. exact sharpness of the \(M^{-8/3}\) and \(M^{-3}\) algebraic exponents.

The following statements remain open:

1. a lower bound showing that the actual Rudin--Shapiro target-root ledger
   saturates the upper prefactor;
2. a normalized many-carrier root family surviving the full rotational charge;
3. an \(M\)-uniform enhanced-dissipation theorem for the changing phase
   profile;
4. any bridge from this triangular 2.5D exclusion to a critical norm for
   general three-dimensional Navier--Stokes solutions.

The next finite gate is therefore dynamical rather than algebraic: either
construct a phase-cancelled family with explicit launch data, coupling,
observation interval, exact roots, and a nonvanishing normalized lower ledger,
or prove a stronger dynamical exclusion that uses more than the static
coefficient \(\Phi_{A,M}\).
