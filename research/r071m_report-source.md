# R0.71M — The annular-filter Lamb commutator has an exact velocity-increment formula, while the direct tangent estimate produces a four-row critical ledger

## Abstract

R0.71L left one precise question. After the raw viscous collar and the
localized Laplacian commutator are fused, can a scale-critical
velocity-increment estimate pay the remaining signed fixed-cell projective
tangent from the standard Leray energy inequality?

This release gives a finite answer for the direct insertion route.

For every translation-invariant scalar annular filter \(T_j\), the filtered
Lamb commutator

\[
 \mathcal R_j=T_j(u\times\omega)-u\times T_j\omega
\]

has an exact quadratic velocity-increment representation. The complete
fixed-cell projective pairing also has an exact formula:

\[
 \left\langle P_QF_j,P_QM_Q\right\rangle
 =\int\chi_Q
 \left[G_j-\frac{B_Q}{d_Q}\operatorname{curl}C_Q\right]
 \cdot\left[G_j+\nu H_j\right],
 \tag{A.1}
\]

where \(G_j=\operatorname{curl}F_j\) and
\(H_j=(\Delta+\kappa_j^2)W_j\). Formula (A.1) removes the outer
cutoff--curl exactly. It does not reduce the tangent to the increment
commutator alone. Its direct scale-critical absolute envelope contains four
rows: resolved transport, differentiated increment commutator, projective
denominator geometry, and viscous annular mismatch.

An \(L^2\)-normalized divergence-free heat-packet family satisfies the exact
uniform kinetic-energy equality while a Yu-type derivative-compatible
increment defect, the critical velocity square-Carleson mass, and the
normalized projected-Lamb integral grow respectively like
\(r^{-2}\), \(r^{-1}\), and \(r^{-1}\). This proves that these absolute
critical budgets do not follow from Leray energy by a universal
function-space embedding. The packets are not nonlinear Navier--Stokes
solutions, so the result does not exclude an NSE-specific signed
cancellation.

The tested direct Cauchy/Bernstein insertion therefore does not close. A
conditional four-row bridge remains valid, but it is an extra sufficient
critical hypothesis, not a necessary condition and not a regularity theorem.

## 0. Claim boundary

The exact identities below hold for a classical incompressible solution on a
time interval, a fixed smooth annular scalar filter, and a fixed nonnegative
time-independent cell cutoff. Projective formulas are stated only on
\(d_Q>0\).

The heat-packet lemma is a function-space separation. Its fields solve the
linear heat equation on \(\mathbb R^3\), not the nonlinear Navier--Stokes
equation. Consequently it proves no NSE blow-up example and no general
no-go theorem for signed estimates.

This release proves none of the following:

1. an unconditional continuation criterion;
2. a bound for denominator faces or refresh atoms;
3. an infinite frame--cell identity or Leray-limit passage;
4. a finite-time singularity or global regularity theorem;
5. originality or priority beyond the bounded literature comparison in
   Section 11;
6. a solution of the Millennium problem.

## 1. Fixed notation

Work on \(\mathbb T^3=(\mathbb R/2\pi\mathbb Z)^3\) with normalized Haar
measure. On a classical interval let

\[
 \omega=\operatorname{curl}u,\qquad
 L=\mathbb P(u\times\omega),\qquad
 Y=\|\omega\|_2^2.
\]

Let \(T_j\) be one real-even radial scalar member of the broad parent frame,
with frequency \(\kappa_j\), periodic convolution kernel \(\phi_j\), and

\[
 F_j=T_jL,\qquad
 W_j=T_j\omega,\qquad
 G_j=\operatorname{curl}F_j.
 \tag{1.1}
\]

For a fixed nonnegative cutoff \(\chi_Q\), put

\[
 \mathsf A_QV=\operatorname{curl}(\chi_QV),\qquad
 C_Q=\mathsf A_QW_j,\qquad
 d_Q=\|C_Q\|_2^2,\qquad
 r_Q=\sqrt{d_Q},
 \tag{1.2}
\]

\[
 B_Q=\langle F_j,C_Q\rangle,\qquad
 E_Q=\frac{C_Q}{r_Q},\qquad
 P_Q=I-E_Q\otimes E_Q,\qquad
 z_Q=\frac{B_Q}{\sqrt{Yd_Q}}.
 \tag{1.3}
\]

As in R0.71L, set

\[
 H_j=(\Delta+\kappa_j^2)W_j,\qquad
 S_j=G_j+\nu H_j,\qquad
 M_Q=\mathsf A_QS_j.
 \tag{1.4}
\]

The complete scalar source remains

\[
 \mathcal J_Q=z_{Q,t}+\nu\kappa_j^2z_Q.
 \tag{1.5}
\]

R0.71M does not replace (1.5). It audits the proposed increment payment for
the projective component inside this already fused scalar identity.

## 2. Main theorem

### Theorem 2.1 — exact increment and projective bridge

Assume the setup of Section 1 and \(d_Q(t)>0\).

#### (i) Exact annular-filter Lamb commutator

With

\[
 \delta_hu(x)=u(x-h)-u(x),\qquad
 \mathcal R_j=T_j(u\times\omega)-u\times W_j,
 \tag{2.1}
\]

one has

\[
 \boxed{
 \mathcal R_j(x)
 =\int_{\mathbb T^3}
 \left[
 \frac12|\delta_hu(x)|^2\nabla_h\phi_j(h)
 -\bigl(\nabla_h\phi_j(h)\cdot\delta_hu(x)\bigr)
       \delta_hu(x)
 \right]dh.}
 \tag{2.2}
\]

No normalization \(\int\phi_j=1\) is needed. In particular,

\[
 F_j=\mathbb P(u\times W_j+\mathcal R_j),
 \tag{2.3}
\]

\[
 \boxed{
 G_j=\operatorname{curl}(u\times W_j)
     +\operatorname{curl}\mathcal R_j.}
 \tag{2.4}
\]

The two terms on the right of (2.4) need not be supported in the \(j\)-th
annulus. Their off-band pieces cancel in the fused band-limited field
\(G_j=T_j\operatorname{curl}(u\times\omega)\).

#### (ii) Exact fixed-cell projective pairing

The outer cutoff--curl can be moved exactly:

\[
 \boxed{
 \langle P_QF_j,P_QM_Q\rangle
 =\int_{\mathbb T^3}\chi_Q\,
 \widetilde G_{j,Q}\cdot S_j,}
 \tag{2.5}
\]

where

\[
 \boxed{
 \widetilde G_{j,Q}
 =\operatorname{curl}(P_QF_j)
 =G_j-\frac{B_Q}{d_Q}\operatorname{curl}C_Q.}
 \tag{2.6}
\]

Equivalently,

\[
 \boxed{
 \langle P_QF_j,P_QM_Q\rangle
 =\int\chi_QG_j\cdot(G_j+\nu H_j)
 -\frac{B_Q}{d_Q}
  \left(\frac12d_{Q,t}+\nu\kappa_j^2d_Q\right).}
 \tag{2.7}
\]

#### (iii) A rigorous four-row critical envelope

Define

\[
 A_j=\operatorname{curl}(u\times W_j),\qquad
 D_j=\operatorname{curl}\mathcal R_j,
 \tag{2.8}
\]

\[
 K_{j,Q}=\frac{B_Q}{d_Q}\operatorname{curl}C_Q,\qquad
 V_j=\nu H_j,
 \tag{2.9}
\]

and the dimensionless positive-branch coefficient

\[
 \gamma_{j,Q}=\frac{\kappa_jB_Q^+}{Yd_Q}.
 \tag{2.10}
\]

For

\[
 \Theta_{j,Q}
 =\kappa_j^{-2}z_Q^+
 \frac{|\langle P_Qx_j,P_QM_Q\rangle|}{r_Q},
 \qquad x_j=\frac{F_j}{\sqrt Y},
 \tag{2.11}
\]

one has the exact representation

\[
 \Theta_{j,Q}
 =\gamma_{j,Q}\kappa_j^{-3}
 \left|\int\chi_Q(A_j+D_j-K_{j,Q})
                    \cdot(A_j+D_j+V_j)\right|,
 \tag{2.12}
\]

and the direct bound

\[
 \boxed{
 \begin{aligned}
 \Theta_{j,Q}
 \le{}&3\gamma_{j,Q}\kappa_j^{-3}
 \left(\|A_j\|_{L^2(\chi_Q)}^2
      +\|D_j\|_{L^2(\chi_Q)}^2\right)\\
 &+\frac32\gamma_{j,Q}\kappa_j^{-3}
 \left(\|K_{j,Q}\|_{L^2(\chi_Q)}^2
      +\|V_j\|_{L^2(\chi_Q)}^2\right).
 \end{aligned}}
 \tag{2.13}
\]

Every time-integrated term in (2.13) is invariant under the formal local
Euclidean three-dimensional Navier--Stokes scaling when the filter scale and
cell cutoff are co-scaled. This is a dimensional statement, not a continuous
scaling symmetry of one fixed torus and one fixed \(\chi_Q\). Only \(D_j\) is
the differentiated velocity-increment commutator. The known quartic defect controls an undifferentiated
\(\mathcal R_j\) budget; because the split commutator is not annular, it does
not directly control \(D_j\) by Bernstein. The displayed direct estimate
therefore still requires additional consumers.

For clarity, define

\[
 \Theta^{\mathrm{abs}}_{j,Q}
 =\kappa_j^{-2}|z_Q|
  \frac{|\langle P_Qx_j,P_QM_Q\rangle|}{r_Q},
 \qquad
 \gamma^{\mathrm{abs}}_{j,Q}
 =\frac{\kappa_j|B_Q|}{Yd_Q}.
 \tag{2.13a}
\]

The stronger absolute envelope is exactly (2.13) with
\((\Theta_{j,Q},\gamma_{j,Q})\) replaced by
\((\Theta^{\mathrm{abs}}_{j,Q},\gamma^{\mathrm{abs}}_{j,Q})\). Equation
(2.13) is conditional: it neither asserts nor uses a Leray-energy bound for
its right-hand side.

#### (iv) Energy-to-critical-budget separation

There is a sequence of smooth divergence-free heat flows \(u_r\) on
\(\mathbb R^3\), \(r\downarrow0\), such that

\[
 \|u_r(T)\|_2^2
 +2\nu\int_0^T\|\nabla u_r\|_2^2dt=1
 \tag{2.14}
\]

for every \(T>0\), while on a matched parabolic cylinder:

\[
 \widetilde{\mathcal S}_{r,\sigma r}^{(3)}[u_r]
 \asymp_\nu r^{-2},
 \tag{2.15}
\]

\[
 \mathfrak C_\nu(u_r)\gtrsim_\nu r^{-1},
 \tag{2.16}
\]

and, for a fixed divergence-free profile satisfying
\(\mathbb P(\Phi\times\operatorname{curl}\Phi)\ne0\),

\[
 \nu\int_0^{c r^2/\nu}
 \frac{\|\mathbb P(u_r\times\operatorname{curl}u_r)\|_2^2}
      {\|\operatorname{curl}u_r\|_2^2}\,dt
 \gtrsim r^{-1}.
 \tag{2.17}
\]

Here (2.15) is the derivative-compatible quartic increment defect used in
Yu's filtered-enstrophy setting, at fixed relative filter length; (2.16) is
the Koch--Tataru-type velocity square-Carleson mass. Therefore none of
these absolute critical quantities is bounded by the standard energy
quantity through a universal function-space embedding.

The sequence in (iv) is not a nonlinear NSE solution sequence. It does not
exclude cancellation special to the NSE solution set or to the signed
quantity in (1.5).

## 3. Proof of the Lamb increment identity

The vector identity

\[
 u\times\omega
 =\nabla\frac{|u|^2}{2}-(u\cdot\nabla)u
 \tag{3.1}
\]

and periodic integration by parts give, componentwise,

\[
 T_j(u\times\omega)_i
 =\int(\partial_i\phi_j)\frac{|u(x-h)|^2}{2}\,dh
 -\int(\partial_m\phi_j)u_m(x-h)u_i(x-h)\,dh.
 \tag{3.2}
\]

Since \(W_j=\operatorname{curl}T_ju\),

\[
 (u\times W_j)_i
 =u_m(x)\int(\partial_i\phi_j)u_m(x-h)\,dh
 -u_m(x)\int(\partial_m\phi_j)u_i(x-h)\,dh.
 \tag{3.3}
\]

Write \(u(x-h)=u(x)+\delta_hu(x)\). Terms proportional to
\(\int\nabla\phi_j\) vanish. The remaining term linear in
\(\delta_hu\) also vanishes because

\[
 \int\partial_m\phi_j(h)\,\delta_hu_m(x)\,dh
 =\operatorname{div}(T_ju)(x)=0.
 \tag{3.4}
\]

The two quadratic terms are exactly (2.2). The positive sign in the first
term and negative sign in the second are fixed by the convention
\(\delta_hu=u(x-h)-u(x)\).

Because \(T_j\), \(\mathbb P\), and curl are commuting scalar Fourier
multipliers, (2.3)--(2.4) follow. An equivalent filtered transport equation
is

\[
 \boxed{
 (\partial_t+u\cdot\nabla)W_j-(W_j\cdot\nabla)u
 =\nu\Delta W_j+\operatorname{curl}\mathcal R_j.}
 \tag{3.5}
\]

Formula (3.5) is exact, but its two nonlinear terms must be fused before a
shell Bernstein estimate is used. The independent Fourier audit gives an
explicit smooth example in which \(\mathcal R_j\) has nonzero off-band
energy.

## 4. The scalar cutoff numerator

Moving one curl in \(B_Q=\langle F_j,C_Q\rangle\) gives

\[
 B_Q=\langle G_j,\chi_QW_j\rangle.
 \tag{4.1}
\]

Using (2.4) and incompressibility,

\[
 \boxed{
 \begin{aligned}
 B_Q={}&\int\chi_Q(W_j\otimes W_j):\nabla u
 +\frac12\int|W_j|^2u\cdot\nabla\chi_Q
 +\langle\mathcal R_j,C_Q\rangle.
 \end{aligned}}
 \tag{4.2}
\]

The increment commutator enters (4.2) without an extra curl:

\[
 \frac{|\langle\mathcal R_j,C_Q\rangle|}{r_Q}
 \le\|1_{U_Q}\mathcal R_j\|_2.
 \tag{4.3}
\]

This one-derivative saving is real for the scalar numerator. It does not
close the complete projective tangent, where \(G_j\) occurs in both factors
of (2.5).

The same numerator has the local filtered-enstrophy identity

\[
 \boxed{
 \frac12\frac d{dt}\int\chi_Q|W_j|^2
 +\nu\int\chi_Q|\nabla W_j|^2
 =B_Q+\frac\nu2\int(\Delta\chi_Q)|W_j|^2.}
 \tag{4.4}
\]

A transported cutoff would modify the second term in (4.2), but that is a
moving-cell problem and is not imported into this fixed-cell theorem.

## 5. Proof of the projective pairing

At fixed \(t,j,Q\), \(B_Q/d_Q\) is a scalar in space and

\[
 P_QF_j=F_j-\frac{B_Q}{d_Q}C_Q.
 \tag{5.1}
\]

Since \(P_QF_j\perp E_Q\),

\[
 \langle P_QF_j,P_QM_Q\rangle
 =\langle P_QF_j,M_Q\rangle.
 \tag{5.2}
\]

Curl is self-adjoint on periodic \(L^2\). Thus

\[
 \begin{aligned}
 \langle P_QF_j,M_Q\rangle
 &=\left\langle P_QF_j,\operatorname{curl}(\chi_QS_j)\right\rangle\\
 &=\int\chi_Q\operatorname{curl}(P_QF_j)\cdot S_j,
 \end{aligned}
 \tag{5.3}
\]

which proves (2.5)--(2.6).

For (2.7), note that

\[
 \langle C_Q,M_Q\rangle
 =\frac12d_{Q,t}+\nu\kappa_j^2d_Q.
 \tag{5.4}
\]

Therefore

\[
 \langle P_QF_j,P_QM_Q\rangle
 =\langle F_j,M_Q\rangle
 -\frac{B_Q}{d_Q}\langle C_Q,M_Q\rangle,
\]

and \(\langle F_j,M_Q\rangle=\int\chi_QG_j\cdot S_j\).

The radial form shows why the apparent positive source square is not by
itself coercive:

\[
 \int\chi_QG_j\cdot(G_j+\nu H_j)
 =\int\chi_Q\left|G_j+\frac\nu2H_j\right|^2
 -\frac{\nu^2}{4}\int\chi_Q|H_j|^2,
 \tag{5.5}
\]

and it is coupled to the signed \(d_{Q,t}\) row in (2.7).

## 6. The four-row scale-critical ledger

Equations (2.4) and (2.6) give

\[
 \widetilde G_{j,Q}=A_j+D_j-K_{j,Q},
 \qquad
 S_j=A_j+D_j+V_j.
 \tag{6.1}
\]

Also

\[
 \kappa_j^{-2}z_Q^+
 \frac{|\langle P_Qx_j,P_QM_Q\rangle|}{r_Q}
 =\kappa_j^{-2}\frac{B_Q^+}{Yd_Q}
 \left|\int\chi_Q\widetilde G_{j,Q}\cdot S_j\right|.
 \tag{6.2}
\]

Since

\[
 \kappa_j^{-2}\frac{B_Q^+}{Yd_Q}
 =\gamma_{j,Q}\kappa_j^{-3},
\]

(2.12) follows. Cauchy gives

\[
 |\langle a,b\rangle_{L^2(\chi_Q)}|
 \le\frac12\left(\|a\|_{L^2(\chi_Q)}^2
                 +\|b\|_{L^2(\chi_Q)}^2\right).
 \tag{6.3}
\]

For three vectors,

\[
 \|a+b+c\|^2\le3(\|a\|^2+\|b\|^2+\|c\|^2).
 \tag{6.4}
\]

Applying (6.3)--(6.4) to (6.1) proves (2.13).

For the following dimensional audit, pass to the formal local Euclidean
scaling, co-scaling the filter length and physical cutoff. Under

\[
 u_\lambda(t,x)=\lambda u(\lambda^2t,\lambda x),
 \tag{6.5}
\]

one has

\[
 \kappa\mapsto\lambda\kappa,\quad
 z\mapsto\lambda z,\quad
 \sqrt Y\mapsto\lambda^{1/2}\sqrt Y,\quad
 r_Q\mapsto\lambda^{3/2}r_Q,
 \tag{6.6}
\]

and every source field \(A,D,K,V\) has local \(L^2\) scaling
\(\lambda^{5/2}\). Hence \(\gamma_{j,Q}\) and

\[
 \int\kappa_j^{-3}\|A_j\|_{L^2(\chi_Q)}^2dt
 \tag{6.7}
\]

are invariant. The same holds for the other three rows. This is not a
continuous scaling symmetry of the fixed torus or of a single fixed
\(\chi_Q\). Dimensional consistency therefore does not make the rows
energy-paid; it identifies them as extra critical information.

The increment formula yields a one-derivative estimate for
\(\mathcal R_j\). If

\[
 d\mu_j(h)=\frac{|\nabla\phi_j(h)|}{\|\nabla\phi_j\|_1}\,dh,
 \qquad
 M_{j,p}(x)=\left(\int|\delta_hu(x)|^p\,d\mu_j(h)\right)^{1/p},
\]

then for \(p\ge2\)

\[
 |\mathcal R_j(x)|
 \lesssim\kappa_j\|\nabla\phi\|_1M_{j,p}(x)^2.
 \tag{6.8}
\]

Thus a quartic increment defect pays a matched
\(\kappa_j^{-1}\|\mathcal R_j\|_2^2\) budget. The tangent ledger contains
\(\kappa_j^{-3}\|\operatorname{curl}\mathcal R_j\|_2^2\). An upper Bernstein
comparison would follow from
\(\operatorname{supp}\widehat{\mathcal R_j}\subset B(0,C\kappa_j)\); annular
support is not required. No such \(O(\kappa_j)\) upper-frequency support
holds in general, because the unfiltered factor in \(u\times W_j\) can carry
arbitrarily high frequencies. Only the fused sum \(A_j+D_j=G_j\) regains
the annular support.

This is the precise derivative/support mismatch in the direct
increment-only insertion.

## 7. The viscous mismatch is also an increment row, but not a small one

Let

\[
 \psi_j=(\Delta_h+\kappa_j^2)\phi_j.
 \tag{7.1}
\]

Its multiplier is

\[
 \widehat\psi_j(k)=(\kappa_j^2-|k|^2)m_j(k).
 \tag{7.2}
\]

Because the annular multiplier vanishes at \(k=0\),
\(\int\psi_j=0\). Therefore

\[
 H_j(x)=\int\psi_j(h)\,\delta_h\omega(x)\,dh.
 \tag{7.3}
\]

Using \(\omega(x-h)=-\operatorname{curl}_h\delta_hu(x)\) and integrating by
parts once gives the exact one-velocity-increment form

\[
 \boxed{
 H_j(x)=\int\nabla_h\psi_j(h)\times\delta_hu(x)\,dh.}
 \tag{7.4}
\]

For \(\phi_j(h)=\kappa_j^3\phi(\kappa_jh)\),

\[
 \|\nabla\psi_j\|_1
 =\kappa_j^3\|\nabla(\Delta+1)\phi\|_1.
 \tag{7.5}
\]

The factor \(\kappa_j^2-|k|^2\) is generally of order \(\kappa_j^2\) on
the broad parent annulus. It vanishes only on the exact Laplace eigenspace
\(-\Delta W_j=\kappa_j^2W_j\). Hence (7.4) is an exact representation, not
an automatic smallness gain.

## 8. Proof of the energy-separation lemma

Fix \(\nu>0\) and a nonzero divergence-free
\(\Phi\in C_c^\infty(\mathbb R^3;\mathbb R^3)\) with
\(\|\Phi\|_2=1\). Put

\[
 \Phi_r(x)=r^{-3/2}\Phi\!\left(\frac{x-x_0}{r}\right),
 \qquad
 u_r(t)=e^{\nu t\Delta}\Phi_r.
 \tag{8.1}
\]

The heat energy equality is (2.14). In scaled variables

\[
 y=\frac{x-x_0}{r},\qquad
 s=\frac{\nu t}{r^2},\qquad
 v(s)=e^{s\Delta}\Phi,
\]

one has

\[
 u_r(t,x)=r^{-3/2}v(s,y).
 \tag{8.2}
\]

### 8.1 Derivative-compatible quartic increment defect

Fix a nonnegative unit-mass filter \(\varphi\), and write

\[
 d\nu_\ell(z)=\varphi_\ell(z)\,dz,
 \qquad
 d\mu_\ell(z)=
 \frac{\ell|\nabla\varphi_\ell(z)|}{\|\nabla\varphi\|_1}\,dz,
\]

\[
 M_{\varphi,p}[u](t,x)
 =\left(\int|\delta_zu(t,x)|^p\,d\nu_\ell(z)\right)^{1/p},
 \quad
 M_{\nabla,p}[u](t,x)
 =\left(\int|\delta_zu(t,x)|^p\,d\mu_\ell(z)\right)^{1/p},
\]

\[
 \mathfrak M_{\ell,p}=M_{\varphi,p}+M_{\nabla,p}.
\]

Choose a fixed nonnegative compactly supported scaled cutoff
\(\chi_*(s,y)\), supported in a fixed scaled-time window and with a nonzero
profile increment integral, and put

\[
 \chi_r(t,x)=\chi_*\!\left(\frac{\nu t}{r^2},
                         \frac{x-x_0}{r}\right),
 \qquad
 \widetilde{\mathcal S}_{r,\ell}^{(p)}[u]
 =\frac r{\ell^2}\iint\chi_r\mathfrak M_{\ell,p}[u]^4\,dx\,dt.
\]

At \(\ell=\sigma r\), the increment envelope scales as

\[
 \mathfrak M_{\sigma r,3}[u_r]
 =r^{-3/2}\mathfrak M_{\sigma,3}[v].
 \tag{8.3}
\]

The prefactor \(r/\ell^2\) contributes \(r^{-1}/\sigma^2\), while
\(dx\,dt=r^5\,dy\,ds/\nu\). Hence on a fixed scaled-time window

\[
 \widetilde{\mathcal S}_{r,\sigma r}^{(3)}[u_r]
 =\frac{A_{\Phi,\chi,\sigma}}{\nu\sigma^2}r^{-2},
 \qquad A_{\Phi,\chi,\sigma}>0.
 \tag{8.4}
\]

### 8.2 Velocity square-Carleson mass

Define

\[
 \mathfrak C_\nu(u)
 =\sup_{x,R}R^{-3}
 \int_0^{R^2/\nu}\int_{B(x,R)}|u(t,y)|^2\,dy\,dt.
 \tag{8.5}
\]

Choose \(y_*\) so that
\(\int_{B(y_*,1)}|\Phi(y)|^2\,dy>0\). For \(R=r\), continuity of the heat
flow at scaled time zero gives fixed
\(c_0,s_0>0\) such that

\[
 \int_{B(x_0+ry_*,r)}|u_r(t)|^2\ge c_0
 \quad (0\le t\le s_0r^2/\nu).
\]

Thus

\[
 \mathfrak C_\nu(u_r)\ge\frac{c_0s_0}{\nu}r^{-1}.
 \tag{8.6}
\]

### 8.3 Normalized projected-Lamb budget

Choose the fixed profile so that

\[
 \mathbb P(\Phi\times\operatorname{curl}\Phi)\ne0.
 \tag{8.7}
\]

One explicit construction is

\[
 \Phi=\operatorname{curl}(0,0,\chi x_1^2x_2),
 \tag{8.8}
\]

where \(\chi\in C_c^\infty\) equals one near a point with
\(x_1x_2\ne0\), followed by \(L^2\) normalization. In the region where
\(\chi=1\), the curl of
\(\Phi\times\operatorname{curl}\Phi\) has nonzero third component, so that
field is not a gradient and (8.7) follows.

On a sufficiently short fixed scaled interval,

\[
 \|\operatorname{curl}u_r\|_2^2=r^{-2}Y_v(s),\qquad
 \|\mathbb P(u_r\times\operatorname{curl}u_r)\|_2^2
 =r^{-5}\|L_v(s)\|_2^2,
 \tag{8.9}
\]

with \(Y_v>0\) and \(\|L_v\|_2>0\). Changing variables in time gives
(2.17).

Equations (8.4), (8.6), and (8.9) coexist with the uniform equality (2.14).
They prove the stated function-space non-implications.

## 9. The half-derivative interpolation gap

Standard energy interpolation gives

\[
 u\in L_t^{2/\theta}\dot H_x^\theta,\qquad 0\le\theta\le1.
 \tag{9.1}
\]

For \(2\le p\le\infty\), after the standard Sobolev/Bernstein embedding into
an \(L^p\)-based Besov scale, the energy-paid spatial index is

\[
 s_E=\theta-\frac32+\frac3p.
 \tag{9.2}
\]

For the same admissible \(p\) and \(q=2/\theta\), a three-dimensional NSE-critical
velocity norm requires

\[
 s_c=-1+\frac3p+\frac2q=-1+\frac3p+\theta.
 \tag{9.3}
\]

Therefore

\[
 \boxed{s_c-s_E=\frac12.}
 \tag{9.4}
\]

For \(p=q=3\), energy pays

\[
 u\in L_t^3\dot B_{3,3}^{1/6},
 \tag{9.5}
\]

whereas a parabolically critical cubic velocity-increment norm has index
\(2/3\). This \(2/3\) is not the Onsager \(1/3\) threshold, and neither
should be identified with Yu's quartic derivative-compatible defect. They
are three different consumers.

Energy does pay the quadratic increment estimate

\[
 \nu\sup_{h\ne0}|h|^{-2}
 \int\|\delta_hu\|_2^2dt
 \le\nu\int\|\nabla u\|_2^2dt,
 \tag{9.6}
\]

but (9.6) is below the critical absolute budgets tested here.

## 10. Independent finite Fourier audit

research/r071m_independent_audit.py constructs a deterministic smooth
divergence-free Fourier field, a compact annular discrete multiplier, and a
positive nonconstant cutoff. It does not import the exact producer.

The checker verifies independently:

1. the increment commutator from two different algebraic implementations;
2. \(G_j=A_j+D_j\) after off-band cancellation;
3. nonzero off-band energy of \(\mathcal R_j\);
4. the projective pairing (2.5);
5. the radial formula (2.7);
6. the four-row envelope (2.13).

The default 64-point grid is alias-safe for the declared finite mode set. The
result is a deterministic identity diagnostic, not a continuous sign
certificate or an NSE simulation.

## 11. Primary-source boundary

The complete bounded search is recorded in
research/r071m_literature_audit.md. The closest verified structures are:

1. Constantin--E--Titi and Duchon--Robert express filtered energy defects by
   velocity increments under additional Onsager/Besov hypotheses.
2. Cheskidov--Constantin--Friedlander--Shvydkoy give critical
   Littlewood--Paley energy-flux bounds in their
   \(B^{1/3}_{3,c(\mathbb N)}\) endpoint and explicitly distinguish it from
   the larger \(B^{1/3}_{3,\infty}\) vector-field class.
3. Eyink gives neighboring filtered Lamb-force and subgrid-stress
   identities. His \(f^*=\overline{u\times\omega}
   -\bar u\times\bar\omega\), and the increment formula written for
   \(f=-\operatorname{div}\tau\), are not identical to \(\mathcal R_j\):
   the filtering and second factor differ.
4. Koch--Tataru use a scale-invariant heat-Carleson norm as an extra small
   critical datum, not a consequence of \(L^2\) energy.
5. Yu's 2026 preprint proves a derivative-compatible estimate for the
   localized paired work
   \(\Omega_\ell\cdot\operatorname{curl}\operatorname{div}R_\ell\), not a
   norm estimate for that differentiated field. Theorem 8.7 supplies a
   reassigned-annulus \(\ell^p\)-\(\ell^q\) closure; the full unweighted
   closure in Theorem 10.3 additionally assumes the full far-field,
   \(\widetilde\Sigma_S\), and residual summability hypotheses.

No theorem located in the bounded search derives the fixed-cell normalized
projective pairing (2.5), its denominator factor, and all four rows of
(2.13) from Leray energy alone. This is a bounded search result, not a claim
of nonexistence, originality, or priority.

## 12. What is closed and what remains open

### 12.1 Closed in R0.71M

1. The annular-filter Lamb commutator has the exact quadratic velocity-increment
   formula (2.2).
2. Resolved transport and the differentiated commutator fuse to the
   band-limited \(G_j\); neither split row is generally annular.
3. The outer fixed-cell cutoff--curl in the projective tangent can be moved
   exactly, giving (2.5).
4. The same pairing has the radial identity (2.7).
5. A direct absolute estimate produces the explicit four-row critical ledger
   (2.13).
6. The known quartic defect controls an undifferentiated commutator budget,
   while the displayed tangent estimate contains a differentiated,
   non-annular split row; the direct Bernstein insertion does not close.
7. Uniform energy does not universally embed into the tested critical
   increment, Carleson, or normalized projected-Lamb budgets.
8. Energy interpolation stops exactly one half derivative below the critical
   velocity index at the same admissible \((p,q)\) scale.

### 12.2 Not closed

1. No sign is proved for (2.5) or (2.7).
2. No NSE-specific cancellation among the four rows is excluded.
3. No bound for \(\gamma_{j,Q}\), \(d_Q^{-1}\), or denominator faces is proved.
4. No moving-cutoff or refresh ledger is treated.
5. No unweighted Carleson summability is obtained from Leray energy.
6. No infinite frame--cell limit is justified.
7. No unconditional weighted-BV continuation criterion follows.
8. No regularity or singularity conclusion follows.

## 13. Route verdict and next finite gate

The direct R0.71M calculation has the following precise verdict:

\[
 \boxed{
 \text{the known increment defect}
 +\text{ the displayed Cauchy/Bernstein steps}
 \ \text{do not furnish closure of the fixed-cell tangent}.}
 \tag{13.1}
\]

Equation (13.1) is a statement about the checked proof route. It is not a
logical non-implication between the increment defect and the tangent, because
no bounded-defect/unbounded-tangent counterexample is constructed. It is
also not an NSE-wide no-go theorem.

R0.71N should remain on fixed cells and avoid another rowwise absolute split.
Its finite task must start from the whole scalar source
\(\mathcal J_Q=z_{Q,t}+\nu\kappa_j^2z_Q\), not from the projective component
alone. It should expand \(z_Q=B_Q/\sqrt{Yd_Q}\), retain
\(B_{Q,t},d_{Q,t},Y_t\) together, and only then insert the radial identity
(2.7) and the local filtered-enstrophy expression for \(B_Q\), before taking
positive parts. The local filtered enstrophy
\(e_Q=\frac12\int\chi_Q|W_j|^2\) is not the projective state
\(d_Q=\|\operatorname{curl}(\chi_QW_j)\|_2^2\). Thus two outcomes remain on
equal footing: a second exact scalar fusion, or an explicit signed residual
showing that no such quadratic fusion occurs. Only after that audit should
the route enter moving cutoffs, faces, or refresh atoms.

## 14. Reproduction map

research/r071m_exact_audit.py checks the universal Lamb integrand reduction,
a finite exact self-adjoint model of the projective pairing, the four-row
constants, the NSE scale ledger, and the heat-packet exponents.

research/r071m_independent_audit.py reconstructs a standalone periodic
Fourier witness and checks both exact fusions, off-band support, and the
conditional envelope.

research/r071m_gap_matrix.md separates exact identities, conditional
estimates, functional counterexamples, diagnostics, and open implications.
research/r071m_literature_audit.md records the bounded primary-source search.
research/r071m_independent_audit.md documents the standalone checker and its
numerical tolerance.

No DNS, stochastic simulation, fitted model, GPU run, or DGX computation is
used. Exact algebra and scaling are the primary evidence; the finite Fourier
calculation is an independent implementation audit.
