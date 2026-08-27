# R0.72H -- carrier-free critical-log payment of the mixed target row

**Date:** 2026-08-27

**Status:** analytic theorem in the finite-carrier triangular 2.5D
Navier--Stokes class, with an order-sharp all-odd Rudin--Shapiro family and
two finite computational audits. The theorem closes the mixed-row gate left by
R0.72G. It does not yet absorb every data factor into the final physical
\(D^{1/3}\Lambda_{1,*}\) normalization, and it is not a theorem for general
three-dimensional Navier--Stokes solutions.

**Keywords:** Navier--Stokes regularity, triangular 2.5D flow, critical-log
action, negative Sobolev observation, differentiated target row,
Rudin--Shapiro polynomial, temporal roots

---

## 0. Direct decision

R0.72G reduced the next finite-carrier obstruction to

\[
 \mathcal E_Q(I)
 :=\int_I\left|h(x)\,Q(x)F(x)\right|\,dx,
 \qquad
 h=P_0V_wF,
 \qquad
 Q=P_0[V_w'+V_w(D_q+\lambda_0)].
 \tag{0.1}
\]

R0.72H closes that row estimate. Let \(I=[A,A+X]\), let

\[
 \mathfrak q(x)=\|V_w(x)F(x)\|_{A_q^{-1}}^2,
 \qquad
 w_*(s)=s^{-1/3}[1+\log(1/s)],
 \tag{0.2}
\]

and define

\[
 Q_*^I
 :=\int_A^{A+X}w_*\!\left(\frac{x-A}{X}\right)
 \mathfrak q(x)\,dx.
 \tag{0.3}
\]

The reciprocal-weight shear moment is

\[
\begin{aligned}
 m_*(A,X)
 :=\sum_{l=1}^M r_l^2|w_l|^2e^{-2\kappa r_l^2A}
 \sup_{0<s\le1}
 \frac{s^{1/3}e^{-2\kappa Xr_l^2s}}
 {1+\log(1/s)} .
\end{aligned}
 \tag{0.4}
\]

If \(E_A=\|F(A)\|_2^2\), then

\[
 \boxed{
 \mathcal E_Q(I)
 \le
 6\sqrt{\nu}\,d|K_z|
 [\lambda_0E_A\,m_*(A,X)\,Q_*^I]^{1/2}.}
 \tag{0.5}
\]

The numerical constant in (0.5) is independent of the carrier count, carrier
locations, and physical shear phases. Since \(w_*(s)\ge1\),

\[
 m_*(A,X)\le
 K_{v,A}:=\sum_l r_l^2|w_l|^2e^{-2\kappa r_l^2A},
 \tag{0.6}
\]

and hence the simpler existing-data bound

\[
 \boxed{
 \mathcal E_Q(I)
 \le
 6\sqrt{\nu}\,d|K_z|
 [\lambda_0E_AK_{v,A}Q_*^I]^{1/2}}
 \tag{0.7}
\]

also has no carrier-count loss.

The scale encoded by the moment in (0.4) is attained. For
\(M=2^n\), put \(M\) Rudin--Shapiro signs on the all-odd block

\[
 r_j=2M+2j+1,\qquad 0\le j<M.
 \tag{0.8}
\]

For fixed nonzero coupling and fixed carrier modulus \(a\), an exactly
real-gauged, row-aligned evolution satisfies

\[
 \boxed{
 \mathcal E_Q\asymp a^2M^2,\qquad
 Q_*^I\asymp a^2M^{2/3}\log M,\qquad
 m_*(0,X)\asymp\frac{a^2M^{7/3}}{\log M}.}
 \tag{0.9}
\]

Consequently

\[
 \frac{\mathcal E_Q}{Q_*^I}
 \asymp\frac{M^{4/3}}{\log M}\longrightarrow\infty,
 \tag{0.10}
\]

whereas

\[
 [E_0m_*(0,X)Q_*^I]^{1/2}
 \asymp a^2M^2
 \asymp\mathcal E_Q.
 \tag{0.11}
\]

Thus action-only payment is false, while the moment-resolved theorem is
sharp in powers of \(M\).

The same family admits an exact simple interior target root at
\(\tau_M=M^{-3}\), but it is not a counterexample to the complete physical
critical-log normalization. Its normalized ratio still decays. The next gate
is therefore the absorption of the explicit data factors in (0.5), not
another mixed-row carrier-count estimate.

---

## 1. Finite-carrier triangular lattice

Fix \(\nu>0\), \(d\ge1\), a target frequency
\(k_*=(K_y,K_z)\) with \(K_z\ne0\), pairwise distinct positive integers
\(r_1,\ldots,r_M\), and physical shear coefficients \(w_l\in\mathbb C\).
Write

\[
 (D_qF)_r=-\lambda_{q,r}F_r,
 \qquad
 \lambda_{q,r}
 =\nu\left[
 \left(dr+\frac{K_y}{q}\right)^2+\frac{K_z^2}{q^2}
 \right],
 \tag{1.1}
\]

\[
 \lambda_0=\lambda_{q,0},
 \qquad
 \kappa=\nu d^2,
 \qquad
 q\ge\max\left(1,\frac{2|K_y|}{d}\right).
 \tag{1.2}
\]

The active scalar sector is

\[
 \partial_xF=D_qF+\delta V_w(x)F,
 \qquad \delta\in\mathbb R,
 \tag{1.3}
\]

with the conjugate-paired physical operator

\[
 (V_w(x)F)_r
 =-iK_z\sum_{l=1}^M e^{-\kappa r_l^2x}
 \left(w_lF_{r-r_l}+\overline{w_l}F_{r+r_l}\right).
 \tag{1.4}
\]

Under Fourier transform, (1.4) is multiplication by

\[
 -2iK_z\operatorname{Re}
 \sum_lw_le^{-\kappa r_l^2x}e^{ir_l\theta},
 \tag{1.5}
\]

which is purely imaginary. Thus \(V_w(x)^*=-V_w(x)\) and

\[
 \frac12\frac d{dx}\|F(x)\|_2^2
 =-\mathcal D(x),
 \qquad
 \mathcal D(x):=\sum_r\lambda_{q,r}|F_r(x)|^2.
 \tag{1.6}
\]

For every restart time \(A\ge0\),

\[
 \|F(x)\|_2^2\le E_A:=\|F(A)\|_2^2,
 \qquad
 \int_A^\infty\mathcal D(x)\,dx\le\frac{E_A}{2}.
 \tag{1.7}
\]

The conjugate pairing is essential. Merely allowing complex coefficients in
the two equal-shift formula can make the multiplier self-adjoint and destroy
(1.6).

Put

\[
 z=V_wF,\qquad h=P_0z,\qquad
 \mathfrak q=\langle A_q^{-1}z,z\rangle
 =\sum_r\frac{|z_r|^2}{\lambda_{q,r}},
 \tag{1.8}
\]

where \(A_q=-D_q\). The target coordinate gives the exact pointwise bound

\[
 \boxed{|h|^2\le\lambda_0\mathfrak q.}
 \tag{1.9}
\]

Because \(K_z\ne0\), the declared physical class has
\(\lambda_0\ge\nu K_z^2/q^2>0\). If \(K_z=0\), then
\(V_w=h=Q=0\), and all displayed row conclusions are trivial without
division by \(\lambda_0\).

---

## 2. The mixed-row theorem

Differentiate the target row:

\[
 h'+\lambda_0h
 =QF+\delta P_0V_w^2F,
 \qquad
 Q=P_0[V_w'+V_w(D_q+\lambda_0)].
 \tag{2.1}
\]

The explicit two entries associated with carrier \(r_l\), together with
(1.2), give the dissipation-paired estimate established in R0.72B--C:

\[
 \boxed{
 |QF|
 \le6\sqrt{2\nu}\,d|K_z|
 A_1(x)\mathcal D(x)^{1/2},}
 \tag{2.2}
\]

where

\[
 A_1(x)^2
 =\sum_l r_l^2|w_l|^2e^{-2\kappa r_l^2x}.
 \tag{2.3}
\]

No \(\ell^1\) sum appears in (2.2). All carrier coefficients enter through
modulus squares.

### Theorem 2.1 -- critical-log mixed-row payment

Let \(I=[A,A+X]\), \(X>0\), and assume (1.1)--(1.4) with
finite-support launch data. Define \(Q_*^I\) and \(m_*(A,X)\) by
(0.3)--(0.4). Then (0.5) holds.

#### Proof

For \(x=A+Xs\), equations (1.9) and (2.2) imply

\[
\begin{aligned}
 |hQF|
 &\le6\sqrt{2\nu}\,d|K_z|\sqrt{\lambda_0}\,
 \mathfrak q^{1/2}A_1\mathcal D^{1/2}\\
 &=6\sqrt{2\nu}\,d|K_z|\sqrt{\lambda_0}\,
 (w_*\mathfrak q)^{1/2}
 (w_*^{-1}A_1^2\mathcal D)^{1/2}.
\end{aligned}
 \tag{2.4}
\]

The definition (0.4) gives, pointwise on \(I\),

\[
 w_*^{-1}\!\left(\frac{x-A}{X}\right)A_1(x)^2
 \le m_*(A,X).
 \tag{2.5}
\]

Cauchy--Schwarz in time and (1.7) now yield

\[
\begin{aligned}
 \mathcal E_Q(I)
 &\le6\sqrt{2\nu}\,d|K_z|\sqrt{\lambda_0}\,
 (Q_*^I)^{1/2}
 \left[m_*(A,X)\int_I\mathcal D\right]^{1/2}\\
 &\le6\sqrt{\nu}\,d|K_z|
 [\lambda_0E_Am_*(A,X)Q_*^I]^{1/2}.
\end{aligned}
 \tag{2.6}
\]

This is (0.5). \(\square\)

The weight has an integrable singularity at \(s=0\). The reciprocal weight
in (0.4) is defined there by its zero limit; no endpoint value enters an
integral.

Since \(w_*(s)\ge1\), (0.6)--(0.7) follow immediately. There is also a
useful independent fallback. Define

\[
 \rho_A^2
 =2K_z^2\sum_l|w_l|^2e^{-2\kappa r_l^2A}.
 \tag{2.7}
\]

The target row gives \(\sup_I|h|\le\rho_A\sqrt{E_A}\), while the old
dissipation-row estimate restarted at \(A\) gives

\[
 \int_A^\infty|QF|\,dx\le3\rho_A\sqrt{E_A}.
 \tag{2.8}
\]

Therefore

\[
 \boxed{\mathcal E_Q(I)\le3E_A\rho_A^2.}
 \tag{2.9}
\]

Bound (2.9) does not use the critical action; (0.5) is the new
action-resolved statement.

---

## 3. The reciprocal-weight envelope

Put

\[
 \Phi(a)
 :=\sup_{0<s\le1}
 \frac{s^{1/3}e^{-as}}{1+\log(1/s)}.
 \tag{3.1}
\]

### Lemma 3.1 -- sharp scalar crossover

There are absolute constants \(0<c<C<\infty\) such that

\[
 \boxed{
 c\frac{(1+a)^{-1/3}}{1+\log(2+a)}
 \le\Phi(a)\le
 C\frac{(1+a)^{-1/3}}{1+\log(2+a)}
 \qquad(a\ge0).}
 \tag{3.2}
\]

#### Proof

For \(0\le a\le1\), the upper bound \(\Phi(a)\le1\) and the test point
\(s=1\) give \(e^{-1}\le\Phi(a)\le1\), which is equivalent to (3.2).

Let \(a>1\) and set \(y=as\). On \(0<y\le\sqrt a\),

\[
 1+\log(a/y)\ge1+\tfrac12\log a,
 \tag{3.3}
\]

while \(y^{1/3}e^{-y}\) is uniformly bounded. For \(a\ge4\), the tail obeys

\[
 \sup_{y\ge\sqrt a}y^{1/3}e^{-y}
 \le C(1+\log a)^{-1}.
\]

The compact regime \(1<a<4\) is absorbed into the absolute constant. Hence

\[
 \Phi(a)\le
 Ca^{-1/3}(1+\log a)^{-1}.
 \tag{3.4}
\]

The test point \(s=a^{-1}\) gives

\[
 \Phi(a)\ge
 e^{-1}a^{-1/3}(1+\log a)^{-1}.
 \tag{3.5}
\]

Replacing \(a\) by \(1+a\) and \(\log a\) by \(\log(2+a)\) joins the two
regimes. \(\square\)

Consequently

\[
 m_*(A,X)
 =\sum_l r_l^2|w_l|^2e^{-2\kappa r_l^2A}
 \Phi(2\kappa Xr_l^2),
 \tag{3.6}
\]

and, in the high-frequency regime \(\kappa Xr_l^2\gtrsim1\),

\[
 r_l^2\Phi(2\kappa Xr_l^2)
 \asymp
 (\kappa X)^{-1/3}
 \frac{r_l^{4/3}}
 {1+\log(2+\kappa Xr_l^2)}.
 \tag{3.7}
\]

The factor \((\kappa X)^{-1/3}\) and the low-frequency crossover are part
of the theorem. They cannot be hidden if \(X\) varies.

---

## 4. An all-odd Rudin--Shapiro sharpness family

It is tempting to use the consecutive block \(M,\ldots,2M-1\). That block
mixes even and odd shifts and does not preserve the exact real target gauge
needed below. The correct block is

\[
 M=2^n,\qquad
 r_j=2M+2j+1,\qquad
 w_j=a\varepsilon_j,\qquad0\le j<M,
 \tag{4.1}
\]

where \(\varepsilon_j\in\{\pm1\}\) are the Rudin--Shapiro coefficients.
For clarity, this section fixes

\[
 \nu=d=K_z=q=1,\qquad K_y=0,\qquad
 A_\mu e_r=(r^2+\mu)e_r,\qquad\mu>0,
 \tag{4.2}
\]

and a fixed \(\delta\ne0\). Fixed positive values of \(a,\mu,\delta,X\)
are suppressed from asymptotic constants.

The operator and aligned launch are

\[
 (V_M(x)F)_r
 =-ia\sum_{j=0}^{M-1}\varepsilon_j e^{-r_j^2x}
 (F_{r-r_j}+F_{r+r_j}),
 \tag{4.3}
\]

\[
 G_M=\frac{i}{\sqrt2}\sum_{j=0}^{M-1}
 \varepsilon_j(e_{r_j}+e_{-r_j}),
 \qquad
 \|G_M\|_2^2=M.
 \tag{4.4}
\]

### Lemma 4.1 -- thermally short phase-flat block

There are constants \(c,C>0\), independent of \(M,a,x\), such that

\[
 \boxed{
 \|V_M(x)\|\le Ca\sqrt M\,e^{-cM^2x},
 \qquad
 \int_0^\infty\|V_M(x)\|\,dx\le CaM^{-3/2}.}
 \tag{4.5}
\]

Moreover,

\[
 \rho(x)^2
 =2a^2\sum_j e^{-2r_j^2x},
 \tag{4.6}
\]

and, because \(Q\) is \(-2r_j^2\) times the corresponding target-row entry,

\[
 \|Q(x)\|_{\ell^2\to\mathbb C}^2
 =8a^2\sum_jr_j^4e^{-2r_j^2x}
 \le Ca^2M^5e^{-cM^2x}.
 \tag{4.7}
\]

#### Proof

For \(|z|=1\), the positive-frequency symbol is

\[
 z^{2M+1}\sum_{j=0}^{M-1}\varepsilon_j
 b_j(x)(z^2)^j,
 \qquad
 b_j(x)=e^{-(2M+2j+1)^2x}.
 \tag{4.8}
\]

The weights \(b_j\) decrease in \(j\). Abel summation and the
Rudin--Shapiro arbitrary-prefix bound telescope to

\[
 \sup_{|z|=1}\left|
 \sum_{j=0}^{M-1}\varepsilon_jb_j(x)(z^2)^j
 \right|
 \le C\sqrt M\,b_0(x).
 \tag{4.9}
\]

Conjugate pairing proves the first part of (4.5); integration gives the
second. Equations (4.6)--(4.7) follow directly from the target rows.
\(\square\)

Let \(F_M\) denote the coupled evolution from data differing from \(G_M\)
by the \(e_0\) correction in Section 5. The correction is lower order and
does not change any estimate below.

For the free diagonal evolution,

\[
 h_0(x)
 =\sqrt2a\,e^{-\mu x}
 \sum_j e^{-2r_j^2x}>0,
 \tag{4.10}
\]

\[
 QF_0(x)
 =-2\sqrt2a\,e^{-\mu x}
 \sum_jr_j^2e^{-2r_j^2x}<0.
 \tag{4.11}
\]

Thus there is no hidden cancellation in the differentiated row.
Contractivity, Duhamel's formula, and (4.5) give

\[
 \sup_{x\ge0}
 \|F_M(x)-e^{-A_\mu x}F_M(0)\|_2
 \le C|\delta|aM^{-1}.
 \tag{4.12}
\]

After applying (4.6)--(4.7), the relative errors in (4.10)--(4.11) on
\(0\le x\le c_0M^{-2}\) are

\[
 O(|\delta|aM^{-3/2}).
 \tag{4.13}
\]

It follows that

\[
 |h(x)|\asymp aM,\qquad
 |QF(x)|\asymp aM^3
 \quad(0\le x\le c_0M^{-2}),
 \tag{4.14}
\]

and therefore

\[
 \mathcal E_Q([0,X])\gtrsim a^2M^2.
 \tag{4.15}
\]

For all time,

\[
 \mathfrak q(x)
 \le\mu^{-1}\|V_M(x)\|^2\|F_M(x)\|_2^2
 \le C_\mu a^2M^2e^{-cM^2x},
 \tag{4.16}
\]

while (1.9) and (4.14) give

\[
 \mathfrak q(x)\ge c_\mu a^2M^2
 \quad(0\le x\le c_0M^{-2}).
 \tag{4.17}
\]

Elementary integration of the regularly varying weight gives

\[
 \int_0^{cM^{-2}}
 w_*(x/X)\,dx
 \asymp_X M^{-4/3}\log M.
 \tag{4.18}
\]

Equations (4.16)--(4.18) prove

\[
 Q_*^{[0,X]}\asymp a^2M^{2/3}\log M.
 \tag{4.19}
\]

Since every \(r_j\asymp M\), equation (3.7) gives

\[
 m_*(0,X)\asymp_X
 \frac{a^2M^{7/3}}{\log M}.
 \tag{4.20}
\]

The upper half of (0.9) for \(\mathcal E_Q\) now follows from (0.5);
(4.15) supplies the lower half. This proves (0.9)--(0.11).

An equivalent diagnostic uses

\[
 \widetilde m_*
 :=\int_0^Xw_*(x/X)^{-1}|QF(x)|^2\,dx.
 \tag{4.21}
\]

The same calculation gives

\[
 \widetilde m_*
 \asymp\frac{a^2M^{10/3}}{\log M},
 \qquad
 \mathcal E_Q
 \asymp[\mu Q_*^{[0,X]}\widetilde m_*]^{1/2}.
 \tag{4.22}
\]

This is the direct Cauchy--Schwarz saturation behind the profile theorem.

---

## 5. An exact real interior root

All carriers in (4.1) are odd. Under the gauge

\[
 F_r=i^{-r}A_r,
 \tag{5.1}
\]

both shift coefficients become real. The launch (4.4) and an \(e_0\)
correction also become real in this gauge. Hence the target coordinate and
target row remain real.

Let \(U_M(x,s)\) be the evolution operator and set

\[
 \tau_M=M^{-3},
 \qquad
 A_M=P_0U_M(\tau_M,0)e_0,
 \qquad
 B_M=P_0U_M(\tau_M,0)G_M.
 \tag{5.2}
\]

The short-time exposure in (4.5) gives

\[
 A_M=1+o(1),
 \qquad
 B_M=O(|\delta|aM^{-2}).
 \tag{5.3}
\]

Both numbers are real. For large \(M\), define

\[
 \zeta_M=-\frac{B_M}{A_M},
 \qquad
 \widetilde F_M(0)=G_M+\zeta_Me_0,
 \qquad
 F_M(0)=
 \frac{\sqrt M}{\|\widetilde F_M(0)\|_2}
 \widetilde F_M(0).
 \tag{5.4}
\]

Then

\[
 \zeta_M\in\mathbb R,\qquad
 \zeta_M=O(|\delta|aM^{-2}),\qquad
 \|F_M(0)\|_2^2=M,
 \tag{5.5}
\]

and, exactly,

\[
 \boxed{P_0F_M(\tau_M)=0.}
 \tag{5.6}
\]

Equations (4.10)--(4.13) also give

\[
 |P_0V_M(\tau_M)F_M(\tau_M)|
 \ge caM.
 \tag{5.7}
\]

At the root,

\[
 F_{M,0}'(\tau_M)
 =\delta P_0V_M(\tau_M)F_M(\tau_M)\ne0.
 \tag{5.8}
\]

Thus (5.6) is a real simple interior root. In particular, the raw complete
root mass satisfies \(G_{\rm all}\gtrsim a^2M^2\).

---

## 6. A compatible-real complete-root corollary

The mixed-row theorem itself is valid for arbitrary physical phases in
(1.4). To use the sharper Rolle reduction, assume in addition that
\(\delta\ne0\) and that the chosen target sector has a real gauge, so \(F_0\)
and \(h\) are real.
The all-odd family in Sections 4--5 is one such sector.

Define

\[
 B_A^2
 :=K_z^2\sum_l|w_l|^2e^{-2\kappa r_l^2A}
 (\lambda_{q,r_l}+\lambda_{q,-r_l}).
 \tag{6.1}
\]

For \(z=V_wF\) and \(b=P_0V_wz=P_0V_w^2F\), weighted
Cauchy--Schwarz gives

\[
 |b|^2\le B_A^2\mathfrak q
 \quad(x\in I),
 \tag{6.2}
\]

and hence

\[
 \int_I|hb|\,dx
 \le\sqrt{\lambda_0}B_AQ_*^I.
 \tag{6.3}
\]

Let \(G_{\rm all}^{\rm ex}(I)\) be the extended nonnegative sum of
\(|h(\tau)|^2\) over all target roots \(F_0(\tau)=0\) in \(I\).
For a finite ordered root subset, the first root costs at most
\(E_A\rho_A^2\). Between consecutive roots, Rolle's theorem applied to
\(e^{\lambda_0x}F_0(x)\) supplies a zero of \(h\). Therefore

\[
 G_{\rm all}^{\rm ex}(I)
 \le E_A\rho_A^2+2\int_I|hh'|\,dx.
 \tag{6.4}
\]

Using (2.1), (1.9), (0.5), and (6.3), then taking the monotone supremum over
finite subsets, gives

\[
\boxed{
\begin{aligned}
 G_{\rm all}^{\rm ex}(I)
 \le{}&E_A\rho_A^2
 +2\lambda_0^2Q_*^I\\
 &+12\sqrt{\nu}\,d|K_z|
 [\lambda_0E_Am_*(A,X)Q_*^I]^{1/2}\\
 &+2|\delta|\sqrt{\lambda_0}B_AQ_*^I .
\end{aligned}}
 \tag{6.5}
\]

This is a carrier-count-independent complete-root corollary for
\(\delta\ne0\) in every compatible real target sector. Indeed,
\((e^{\lambda_0x}F_0)'=\delta e^{\lambda_0x}h\), so division by \(\delta\)
is essential in the Rolle step. At \(\delta=0\), the physical slope ledger
vanishes, but the raw \(h\)-ledger obtained after dividing by \(\delta^2\)
is not the relevant object and (6.5) is not asserted. The corollary is also
not asserted for an arbitrary complex target coordinate. For complex
targets, the older BV sampling lemma remains valid, but it does not by itself
reproduce the Rolle-weighted formula (6.5).

---

## 7. Physical normalization boundary

The family in Sections 4--5 is a sharp counterfamily to action-only
mixed-row payment, but not to the complete physical critical-log candidate.
Its shear and active frequency moments obey

\[
 K_s\asymp M^3,\qquad K_v\asymp a^2M^3.
 \tag{7.1}
\]

With fixed nonzero \(\delta\), the single exact-root atom constructed in
Section 5 has the inherited physical scale

\[
 \frac{\mathcal J_*(\tau_M)}
 {D^{1/3}\Lambda_{1,*}}
 \asymp M^{-2}.
 \tag{7.2}
\]

At the stronger perturbative scaling
\(\delta a=\gamma M^{3/2}\), with fixed \(0<\gamma\le\gamma_0\) small enough
for the Duhamel and root bounds above, the unweighted atom reaches the old
critical size. Under the inherited exact-amplitude balance, the critical-log
action scale grows like \(M^{2/3}\log M\), and the resulting single-atom
normalized scale is at most

\[
 O\!\left(\frac{M^{-2/3}}{\log M}\right).
 \tag{7.3}
\]

Thus R0.72H does not refute \(D^{1/3}\Lambda_{1,*}\). This scaling check is
not a complete physical-ledger theorem; it identifies the factors produced
by the present row-estimate route.

---

## 8. Literature boundary

A bounded primary-source search through 2026-08-27 found no theorem that
directly controls (0.1) from the current critical-log action with a constant
uniform in the carrier count. The closest literatures cover only parts of the
interface:

1. non-autonomous maximal regularity controls \(F'\) and \(A(x)F\), but
   does not identify the two time-dependent observation rows in (0.1);
2. observation admissibility and semigroup square functions can control a
   fixed observation, but do not supply the \(V'\) row or the present
   internal action;
3. bilinear heat-flow embeddings can be independent of ambient spatial
   dimension, which is different from uniformity in the number of Fourier
   carriers;
4. operator-valued Carleson embeddings can have logarithmic dimension
   growth, so reducing the problem to an unrestricted matrix Carleson
   theorem would lose the structure needed here;
5. BV indicatrix and scattered-zero theorems do not give the fixed-level,
   no-separation derivative sampling used in the present target sector.

The proof of (0.5) avoids those missing abstractions. It uses the scalar
target coordinate, the exact diagonal dissipation, and the shared heat
weights of \(V_w\) and \(Q\).

This is a bounded non-collision check, not a claim of priority,
exhaustiveness, or global novelty.

---

## 9. Audit contract

The analytic proof is the result. The two computational routes check finite
instances only.

The producer audit:

1. generates Rudin--Shapiro signs by the polynomial recurrence;
2. solves the finite Fourier lattice with a sparse complex evolution;
3. constructs the exact \(\zeta_M\) root correction from two evolution
   columns;
4. integrates \(\mathcal E_Q\), \(Q_*^I\), and the reciprocal moment;
5. verifies the scalar envelope and the predicted log--log slopes.

The independent audit:

1. generates the same signs from the binary adjacent-\(11\) parity formula;
2. uses a real-gauge lattice and a different time integrator/quadrature;
3. solves the scalar root correction independently;
4. recomputes the three normalized ratios and fitted exponents.

Both routes preserve their configurations, seeds, environments, progress
streams, resource logs, raw data, failed attempts, and SHA-256 manifests.
Finite agreement corroborates the theorem but does not certify its
asymptotic proof.

---

## 10. Exact conclusion and next gate

R0.72H proves:

1. the mixed target row is paid by the critical-log action and the existing
   shear frequency data with no carrier-count loss;
2. the exact thermal moment has the sharp crossover (3.2);
3. an all-odd Rudin--Shapiro family makes the moment-resolved bound
   order-sharp and rejects action-only payment;
4. the same family supports an exact real simple interior root;
5. a compatible-real complete-root corollary follows at the abstract row
   level.

R0.72H does not prove:

1. absorption of every factor in (6.5) by
   \(D^{1/3}\Lambda_{1,*}\) for the intended physical amplitude class;
2. a critical-log counterexample after that full normalization;
3. a restart covering theorem for non-triangular dynamics;
4. a new continuation criterion or a finite-time singularity for the
   three-dimensional Navier--Stokes equations.

The next finite section, R0.72I, should keep (6.5) fixed and audit the
physical amplitude ledger. It must either absorb
\(E_A,m_*,B_A,\rho_A\) into the declared normalization without a carrier
loss, or exhibit a normalized family for which that absorption fails.
