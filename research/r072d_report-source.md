# R0.72D -- a spectrally shifted Rudin--Shapiro family with a nonvanishing complete root ledger

**Date:** 2026-08-27
**Status:** analytic result in the exact triangular 2.5D Navier--Stokes class;
the finite algebra is checked by two separate programs, and representative
finite evolutions are checked only by the independent program.  No statement
concerns global regularity or finite-time blow-up for general
three-dimensional Navier--Stokes solutions.

**Keywords:** Navier--Stokes regularity, triangular 2.5D flows, temporal roots,
Rudin--Shapiro polynomials, phase cancellation, rotational charge, sharpness

---

## 0. Direct decision

R0.72C proved the phase-uniform exact-launch upper ledger

\[
 \frac{\mathcal J_{\rm all}}{D^{1/3}\Lambda_1}
 \le C\nu^{-2}e^{2\lambda_0L}
 \frac M{K_s}\eta^{4/3}
 \chi_0\left(\frac{\Omega_0^2}{K_v}\right)^{1/3}
 \left[1+q_\rho+\eta\ell_\times\right].
 \tag{0.1}
\]

For arbitrary phases, the static geometric coefficient can be as large as

\[
 \frac M{K_s}\chi_0
 \left(\frac{\Omega_0^2}{K_v}\right)^{1/3}
 \asymp M^{-8/3}.
 \tag{0.2}
\]

What remained open was dynamical.  The family proving (0.2) did not show that
the exact evolution has a target root with a comparable slope, and it did not
pay the full nonlinear rotational charge in \(\Lambda_1\).

This report closes that gate inside the declared triangular class.  Let
\(M=2^n\), take one block of carrier indices

\[
 r_j=M+j,\qquad 0\le j<M,
 \tag{0.3}
\]

and put Rudin--Shapiro signs on that block.  Choose the scaled coupling so that

\[
 \delta a=\gamma M^{3/2},
 \qquad
 \eta=|\delta|\Omega_0\asymp\gamma M^2,
 \tag{0.4}
\]

where \(a\) is the carrier modulus and \(\gamma>0\) is fixed and sufficiently
small.  The phase cancellation gives \(\Omega_0\asymp a\sqrt M\), while the
spectral translation makes the whole shear pulse live for only \(O(M^{-2})\)
scaled time:

\[
 \int_0^\infty\|V_M(x)\|\,dx\lesssim aM^{-3/2},
 \qquad
 \int_0^\infty\|V_M(x)\|^2\,dx\lesssim a^2M^{-1}.
 \tag{0.5}
\]

Thus the instantaneous coupling is \(\asymp M^2\), but its integrated Dyson
size is only \(O(\gamma)\).  Launch data aligned with the target row give
\(|P_0V_M(0)F(0)|\asymp aM\).  A scalar adjustment of size
\(O(M^{-1/2})\) produces an **exact simple interior root** at

\[
 \tau_M=M^{-3}.
 \tag{0.6}
\]

At that root the row slope still satisfies

\[
 |P_0V_M(\tau_M)F(\tau_M)|\ge c aM.
 \tag{0.7}
\]

After the exact physical amplitude balance and a decoupled low-mode
enstrophy background are included, the root atom and the complete first-row
factor obey

\[
 \frac{\mathcal J_{\rm all}}
 {D^{1/3}\Lambda_1}
 \ge
 c_{\nu,I,T_*,d,K_z,\gamma}>0
 \qquad(M\to\infty).
 \tag{0.8}
\]

More explicitly, the proof gives the scale ledger

\[
 \frac{\mathcal J_{\rm all}}{D^{1/3}}
 \gtrsim\gamma^{4/3},
 \qquad
 \Lambda_1\lesssim C_I(\nu^2+\gamma^2).
 \tag{0.9}
\]

The full projected rotational charge is estimated at every Fourier frequency;
it is not replaced by a target-shell proxy.  Equation (0.8) is therefore an
actual normalized root-ledger lower family.  It proves that the phase-free
\(M^{-8/3}\) coefficient and the \(\eta\asymp M^2\) critical scale can be
realized dynamically in this exact subclass.  It does **not** disprove the
candidate \(D^{1/3}\Lambda_1\) payment, because the ratio stays finite.  It
also does not extend the payment to general three-dimensional solutions.

---

## 1. Exact triangular NSE class and the ledger

Work on the normalized three-torus with coordinates \((x,y,z)\).  Let

\[
 u(x,y,z,t)=(f(y,z,t),0,v(y,t)).
 \tag{1.1}
\]

Then \(\operatorname{div}u=0\), and the unforced Navier--Stokes equations are
equivalent, with constant pressure, to

\[
 \boxed{
 v_t=\nu v_{yy},
 \qquad
 f_t+vf_z=\nu(f_{yy}+f_{zz}).}
 \tag{1.2}
\]

Finite Fourier data therefore give an exact global smooth three-dimensional
solution.  This is an invariant 2.5D class, not a forced passive-scalar
model.

The vorticity and projected Lamb vector are

\[
 \omega=(v_y,f_z,-f_y),
 \qquad
 \boxed{\mathbb P(u\times\omega)=(-vf_z,0,0).}
 \tag{1.3}
\]

The gradient part of \(u\times\omega\) is removed exactly.  This identity is
needed below: estimating the unprojected cross product would incorrectly
charge the decoupled background.

Fix integers \(K_y,K_z,d,Q\), with \(K_z\ne0\), and a compact real-even
annular multiplier \(T_*\) that isolates the conjugate target pair
\(\pm k_*\), where

\[
 k_*=(0,K_y,K_z),
 \qquad m_*(k_*)\ne0.
 \tag{1.4}
\]

Let \(R_*\) be the largest Fourier radius in the support of \(T_*\), assume
\(Q>R_*\), and fix one integer \(q=q_0\), independent of \(M\), such that
\(dq>R_*+|K_y|\).  Then every nonzero active-coset mode, every shear
frequency, the fixed target, and the background frequency are disjoint in the
same sense as R0.71W--R0.72C.  Put

\[
 \widehat f(K_y+dqr,K_z,t)=S F_r(x),
 \qquad x=q^2t.
 \tag{1.5}
\]

The positive-\(K_z\) active sector solves

\[
 \partial_xF=D_qF+\delta V_M(x)F,
 \qquad
 \delta=\frac P{q^2},
 \tag{1.6}
\]

where

\[
 (D_qF)_r=-\lambda_{q,r}F_r,
 \qquad
 \lambda_{q,r}=\nu\left[
 \left(dr+\frac{K_y}{q}\right)^2+\frac{K_z^2}{q^2}
 \right],
 \tag{1.7}
\]

and

\[
 (V_M(x)F)_r=-iK_z\sum_{j=0}^{M-1}
 e^{-\kappa r_j^2x}
 \left(w_jF_{r-r_j}+\overline{w_j}F_{r+r_j}\right),
 \qquad \kappa=\nu d^2.
 \tag{1.8}
\]

The conjugate pairing makes \(V_M(x)\) skew-adjoint.  Hence

\[
 \frac12\frac d{dx}\|F(x)\|_2^2
 =-\sum_r\lambda_{q,r}|F_r(x)|^2\le0.
 \tag{1.9}
\]

Let

\[
 Y(t)=\|\omega(t)\|_2^2,
 \qquad
 \mathcal R_Y(I)=\frac{\sup_IY}{\inf_IY},
 \tag{1.10}
\]

and

\[
 \Lambda_1(I;u)=\mathcal R_Y(I)
 \left[
 \nu^2+\frac1{|I|}\int_I
 \frac{\|\mathbb P(u\times\omega)\|_{\dot H^{-1}}^2}
 {Y(t)}\,dt
 \right].
 \tag{1.11}
\]

At a simple target-shell root \(t_*\), modular isolation and the fixed
multiplier give the exact atom

\[
 J_*(t_*)=c_*
 \frac{S^2P^2|P_0V_M(\tau_*)F(\tau_*)|^2}{Y(t_*)},
 \qquad c_*>0,
 \tag{1.12}
\]

where \(\tau_*=q^2t_*\) and \(c_*\) depends only on the declared target and
multiplier.  The complete ledger \(\mathcal J_{\rm all}\) is nonnegative and
contains every such atom.  Therefore one certified interior root supplies a
valid lower bound for the complete ledger even if additional roots occur.

---

## 2. A thermally short, phase-flat carrier block

Let \(M=2^n\), and let \(\varepsilon_0,\ldots,\varepsilon_{M-1}\in\{\pm1\}\)
be the Rudin--Shapiro coefficients.  Their arbitrary-prefix bound has the
form

\[
 \max_{0\le k<M}\sup_{|z|=1}
 \left|\sum_{j=0}^k\varepsilon_jz^j\right|
 \le C_{\rm RS}\sqrt M,
 \tag{2.1}
\]

with an absolute constant.  A dyadic block decomposition proves the coarse
form needed here; Balister's arbitrary-degree theorem gives a sharper
published version.

Choose

\[
 r_j=M+j,
 \qquad
 w_j=a\varepsilon_j,
 \qquad 0\le j<M,
 \tag{2.2}
\]

where \(a>0\).  The carrier moments are

\[
 \boxed{
 K_s=\sum_{r=M}^{2M-1}r^2
 =\frac{M(2M-1)(7M-1)}6,
 \qquad K_v=a^2K_s.}
 \tag{2.3}
\]

### Lemma 2.1 -- heat-stable Rudin--Shapiro bound

There is an absolute constant \(C\), independent of \(M,a,x\), such that

\[
 \boxed{
 \|V_M(x)\|
 \le C|K_z|a\sqrt M\,e^{-\kappa M^2x}.}
 \tag{2.4}
\]

Moreover,

\[
 \|\partial_\theta V_M(x)\|
 \le C|K_z|aM^{3/2}e^{-\kappa M^2x}.
 \tag{2.5}
\]

Here the second expression means the derivative of the Fourier multiplier
symbol.

#### Proof

For \(|z|=1\), put

\[
 b_j(x)=e^{-\kappa(M+j)^2x},
 \qquad
 A_k(z)=\sum_{j=0}^k\varepsilon_jz^j.
 \tag{2.6}
\]

The weights are decreasing in \(j\).  Abel summation gives

\[
 \sum_{j=0}^{M-1}\varepsilon_jb_jz^j
 =b_{M-1}A_{M-1}
 +\sum_{k=0}^{M-2}(b_k-b_{k+1})A_k.
 \tag{2.7}
\]

Using (2.1) and telescoping the nonnegative weight differences,

\[
 \sup_{|z|=1}
 \left|\sum_{j=0}^{M-1}\varepsilon_jb_jz^j\right|
 \le C_{\rm RS}\sqrt M\,b_0
 =C_{\rm RS}\sqrt M e^{-\kappa M^2x}.
 \tag{2.8}
\]

Multiplication by \(z^M\), conjugate pairing, and the fixed factor \(K_z a\)
prove (2.4).  The symbol has degree at most \(2M-1\).  Bernstein's inequality
for trigonometric polynomials proves (2.5).  \(\square\)

Integrating (2.4) gives

\[
 \boxed{
 \int_0^\infty\|V_M(x)\|\,dx\le C aM^{-3/2},
 \qquad
 \int_0^\infty\|V_M(x)\|^2\,dx\le C a^2M^{-1}.}
 \tag{2.9}
\]

The exact target-row norm is

\[
 \rho(x)^2=2K_z^2a^2
 \sum_{r=M}^{2M-1}e^{-2\kappa r^2x}.
 \tag{2.10}
\]

Consequently

\[
 \rho_0^2=2K_z^2a^2M,
 \qquad
 \int_0^\infty\rho(x)^2\,dx
 =\frac{K_z^2a^2}{\kappa}
 \sum_{r=M}^{2M-1}\frac1{r^2}
 \le Ca^2M^{-1}.
 \tag{2.11}
\]

Parseval and (2.4) at launch imply

\[
 c|K_z|a\sqrt M\le\Omega_0:=\|V_M(0)\|
 \le C|K_z|a\sqrt M.
 \tag{2.12}
\]

Thus

\[
 \chi_0=\frac{\rho_0^2}{\Omega_0^2}\asymp1,
 \qquad
 \frac{\Omega_0^2}{K_v}\asymp M^{-2},
 \tag{2.13}
\]

and the R0.72C phase-free coefficient is dynamically available at the exact
scale

\[
 \boxed{
 \frac M{K_s}\chi_0
 \left(\frac{\Omega_0^2}{K_v}\right)^{1/3}
 \asymp M^{-8/3}.}
 \tag{2.14}
\]

The mixed exposure also remembers the translated heat scale.  Equations
(2.4), (2.10), and (2.12) give

\[
 \ell_\times
 =\frac1{\rho_0\Omega_0}
 \int_0^\infty\rho(x)\|V_M(x)\|\,dx
 \le CM^{-2}.
 \tag{2.15}
\]

This scale also has a matching lower bound.  For
\(0\le x\le c_0M^{-2}\), Abel summation applied to the increasing weights
\(1-e^{-\kappa(M+j)^2x}\) gives

\[
 \|V_M(x)-V_M(0)\|
 \le Ca\sqrt M\,M^2x.
 \tag{2.16}
\]

Choose \(c_0>0\), depending only on the fixed \(\kappa\) and the
Rudin--Shapiro prefix constant, small enough and use
\(\Omega_0\ge\rho_0\asymp a\sqrt M\).  Then
\(\|V_M(x)\|\ge\Omega_0/2\), while (2.10) gives
\(\rho(x)\ge e^{-4\kappa c_0}\rho_0\), throughout that interval.  Hence

\[
 \boxed{\ell_\times\asymp M^{-2}.}
 \tag{2.17}
\]

This factor is essential.  The coarser universal bound
\(\ell_\times\le C_\times\) would lose the short lifetime of the shifted
block.

---

## 3. Exact interior root with a noncollapsing slope

Choose a fixed \(\gamma>0\) and set

\[
 \boxed{\delta a=\gamma M^{3/2}.}
 \tag{3.1}
\]

Then

\[
 \eta=|\delta|\Omega_0\asymp\gamma M^2,
 \qquad
 |\delta|\int_0^\infty\|V_M(x)\|\,dx\le C\gamma.
 \tag{3.2}
\]

The first quantity is large.  The second is the integrated Dyson exposure and
is independent of \(M\).

Let

\[
 G_M=\frac{i\operatorname{sgn}(K_z)}{\sqrt2}
 \sum_{j=0}^{M-1}\varepsilon_j
 \left(e_{r_j}+e_{-r_j}\right).
 \tag{3.3}
\]

Then

\[
 \|G_M\|_2^2=M,
 \qquad (G_M)_0=0,
 \tag{3.4}
\]

and the launch target row is aligned exactly:

\[
 \boxed{
 h_M(0):=P_0V_M(0)G_M
 =\sqrt2|K_z|aM,
 \qquad |h_M(0)|^2=M\rho_0^2.}
 \tag{3.5}
\]

Thus the first-root term in the complete BV theorem is not an artifact of
Cauchy--Schwarz; it can be saturated.

Let \(U_M(x,s)\) be the evolution operator for (1.6), and take

\[
 \tau_M=M^{-3}.
 \tag{3.6}
\]

Define

\[
 A_M=P_0U_M(\tau_M,0)e_0,
 \qquad
 B_M=P_0U_M(\tau_M,0)G_M.
 \tag{3.7}
\]

On \([0,\tau_M]\), equations (2.4) and (3.1) give

\[
 |\delta|\int_0^{\tau_M}\|V_M(x)\|\,dx
 \le C\gamma M^{-1}.
 \tag{3.8}
\]

The target heat damping is \(1+O(M^{-3})\).  Duhamel's formula therefore
gives, using \(\|G_M\|_2=\sqrt M\),

\[
 A_M=1+O_\gamma(M^{-1}),
 \qquad
 |B_M|
 \le |\delta|\int_0^{\tau_M}\|V_M(x)\|\,dx\,\|G_M\|_2
 \le C_\gamma M^{-1/2}.
 \tag{3.9}
\]

In particular \(|A_M|\ge1/2\) for large \(M\).  Put

\[
 \zeta_M=-\frac{B_M}{A_M},
 \qquad
 \widetilde F_M(0)=G_M+\zeta_Me_0,
 \tag{3.10}
\]

and normalize

\[
 F_M(0)=c_M\widetilde F_M(0),
 \qquad
 c_M=\frac{\sqrt M}{\|\widetilde F_M(0)\|_2}.
 \tag{3.11}
\]

Then

\[
 \zeta_M=O_\gamma(M^{-1/2}),
 \qquad
 c_M=1+O_\gamma(M^{-2}),
 \qquad
 \|F_M(0)\|_2^2=M,
 \tag{3.12}
\]

and, exactly,

\[
 \boxed{P_0F_M(\tau_M)=0.}
 \tag{3.13}
\]

This is an interior root, not an endpoint convention.

### Lemma 3.1 -- the interior slope does not collapse

For fixed sufficiently small \(\gamma>0\), there are \(M_0\) and \(c_h>0\)
such that

\[
 \boxed{
 |P_0V_M(\tau_M)F_M(\tau_M)|\ge c_h aM
 \qquad(M\ge M_0).}
 \tag{3.14}
\]

#### Proof

Over \([0,\tau_M]\), every carrier heat factor differs from one by
\(O(M^2\tau_M)=O(M^{-1})\).  The diagonal active heat flow changes the
aligned carrier vector by the same relative order.  Equation (3.8) bounds the
coupling perturbation in \(\ell^2\) by \(O_\gamma(M^{-1})\|F_M(0)\|_2\).
Applying the target row, whose norm is \(O(a\sqrt M)\), gives the explicit
absolute error

\[
 O(a\sqrt M)\,O_\gamma(M^{-1})\,\|F_M(0)\|_2
 =O_\gamma(a),
 \tag{3.15a}
\]

because \(\|F_M(0)\|_2=\sqrt M\).  Thus no additional factor of \(\sqrt M\)
is lost.  The launch value in (3.5) is \(\asymp aM\).  The \(e_0\)
adjustment and the normalization in (3.12) add only lower-order terms.  Hence

\[
 P_0V_M(\tau_M)F_M(\tau_M)
 =\sqrt2|K_z|aM\,[1+O_\gamma(M^{-1})],
 \tag{3.15}
\]

which proves (3.14).  \(\square\)

At a target root the diagonal term vanishes, so

\[
 F_{M,0}'(\tau_M)=\delta
 P_0V_M(\tau_M)F_M(\tau_M)\ne0.
 \tag{3.16}
\]

The root is simple.

---

## 4. Enstrophy control on a fixed physical interval

The lower result needs the complete factor \(\mathcal R_Y\), not only the
root-time value of \(Y\).  Fix a physical interval \(I=[0,T]\), with
\(T>0\) independent of \(M,q\).

Let \(R\) be multiplication by the lattice index \(r\).  Since \(D_q\)
commutes with \(R\) and \(V_M\) is skew-adjoint,

\[
 \frac d{dx}\|RF_M(x)\|_2
 \le |\delta|\|[R,V_M(x)]\|\|F_M(x)\|_2.
 \tag{4.1}
\]

Under Fourier transform, the commutator is the derivative of the multiplier.
Equations (1.9), (2.5), and (3.1) yield

\[
\begin{aligned}
 \sup_{x\ge0}\|RF_M(x)\|_2
 &\le \|RF_M(0)\|_2
 +|\delta|\sqrt M\int_0^\infty
 \|\partial_\theta V_M(x)\|\,dx\\
 &\le C_\gamma M^{3/2}.
\end{aligned}
 \tag{4.2}
\]

The initial value already has order \(M^{3/2}\); the coupling adds only a
fixed relative amount.  Therefore the active enstrophy is bounded by

\[
 Y_{\rm act}(t)\le C_\gamma S^2q^2M^3
 \qquad(t\in I).
 \tag{4.3}
\]

The shear heat flow similarly satisfies

\[
 Y_{\rm shear}(t)\le CP^2a^2q^2K_s
 \le CP^2a^2q^2M^3.
 \tag{4.4}
\]

Let

\[
 K_f=\sum_r r^2|F_{M,r}(0)|^2
 =c_M^2K_s
 =K_s[1+O_\gamma(M^{-2})],
 \tag{4.5}
\]

where the middle identity is exact: the correction \(\zeta_Me_0\) has zero
\(r^2\)-moment, while the two coefficients at \(\pm r_j\) contribute exactly
\(r_j^2\).

Choose the physical amplitudes by the exact balance

\[
 \boxed{S^2K_f=3P^2K_v.}
 \tag{4.6}
\]

Put

\[
 E_M=S^2K_f+P^2K_v=4P^2K_v.
 \tag{4.7}
\]

Add the same decoupled \(z\)-independent background used in
R0.71W--R0.72A,

\[
 f_{b,M}(y,t)=B_M^{\rm bg}e^{-\nu Q^2t}
 (e^{iQy}+e^{-iQy}),
 \qquad
 B_M^{\rm bg}=\frac{b_0q}{Q}\sqrt{E_M}.
 \tag{4.8}
\]

It never enters the target response and, by (1.3), never enters the
projected rotational charge.  Its enstrophy stays comparable to \(q^2E_M\)
on the fixed interval.  Equations (4.2)--(4.8) give

\[
 \boxed{
 c_Iq^2E_M\le Y_M(t)\le C_{I,\gamma}q^2E_M
 \quad(t\in I),
 \qquad
 \mathcal R_{Y_M}(I)\le C_{I,\gamma}.}
 \tag{4.9}
\]

For the inherited data normalization

\[
 D_M:=\|u_M(0)\|_2^2+\|\omega_M(0)\|_2^2,
\]

the initial data size obeys the two-sided comparison

\[
 \boxed{c_Dq^2E_M\le D_M\le C_Dq^2E_M.}
 \tag{4.10}
\]

All constants are independent of \(M\) and \(q\).  They may depend on the
fixed physical interval and declared geometric data.

---

## 5. The full projected rotational charge

Every Fourier mode of \(vf_z\) has nonzero fixed \(z\)-frequency
\(\pm K_z\).  Therefore

\[
 \|\mathbb P(u\times\omega)\|_{\dot H^{-1}}
 \le C_{K_z}\|vf_z\|_2
 \le C\|v\|_\infty\|f_z\|_2.
 \tag{5.1}
\]

The active contraction (1.9) gives

\[
 \|f_z(t)\|_2^2\le C K_z^2S^2M.
 \tag{5.2}
\]

The physical shear and the scaled multiplier differ only by fixed factors,
so (2.9), after \(x=q^2t\), gives

\[
 \int_0^T\|v(t)\|_\infty^2\,dt
 \le C\frac{P^2a^2}{q^2M}.
 \tag{5.3}
\]

Combining (4.9) and (5.1)--(5.3),

\[
\begin{aligned}
 \frac1T\int_I
 \frac{\|\mathbb P(u\times\omega)\|_{\dot H^{-1}}^2}{Y_M(t)}\,dt
 &\le C_I
 \frac{P^2S^2a^2}{q^4E_M}\\
 &=C_I\frac34\frac{P^2a^2}{q^4K_f}\\
 &\le C_I\frac{P^2a^2}{q^4K_s}.
\end{aligned}
 \tag{5.4}
\]

Since \(P/q^2=\delta\), equations (2.3) and (3.1) imply

\[
 \boxed{
 \frac1T\int_I
 \frac{\|\mathbb P(u\times\omega)\|_{\dot H^{-1}}^2}{Y_M(t)}\,dt
 \le C_I\frac{\delta^2a^2}{M^3}
 \le C_I\gamma^2.}
 \tag{5.5}
\]

This is a full-frequency bound.  The target mode, all off-target active
products, and every shear--active convolution remain in the left side.  No
selected-shell proxy is used.

Equations (4.9) and (5.5) prove

\[
 \boxed{\Lambda_1(I;u_M)\le C_{I,\gamma}(\nu^2+\gamma^2).}
 \tag{5.6}
\]

The instantaneous target component of the Lamb vector is large near the
root.  It does not force (5.6) to grow with \(M\), because the translated
carrier block lives for only \(O((qM)^{-2})\) physical time.  The time
integral in \(\Lambda_1\) records that short pulse exactly.

---

## 6. Nonvanishing normalized complete ledger

Let

\[
 t_M=\frac{\tau_M}{q^2}=\frac1{q^2M^3}.
 \tag{6.1}
\]

For large \(M\), this lies in the interior of the fixed interval \(I\).
Indeed \(q=q_0\) was fixed independently of \(M\), so
\(0<t_M\le q_0^{-2}M^{-3}<T\) once \(M\) is large.
Equations (1.12), (3.14), and the upper bound in (4.9) give

\[
\begin{aligned}
 \mathcal J_{\rm all}(I)
 &\ge J_*(t_M)\\
 &\ge c
 \frac{S^2P^2a^2M^2}{q^2E_M}.
\end{aligned}
 \tag{6.2}
\]

Using the exact amplitude balance (4.6) and \(E_M=4P^2K_v\),

\[
 \frac{S^2}{E_M}=\frac{3}{4K_f}.
 \tag{6.3a}
\]

The exact identity \(K_f=c_M^2K_s\) and \(K_s\asymp M^3\) therefore give

\[
 \mathcal J_{\rm all}(I)
 \ge c\frac{P^2a^2}{q^2M}.
 \tag{6.3}
\]

The upper side of (4.10) gives

\[
 D_M^{1/3}\le C
 (q^2P^2a^2M^3)^{1/3}.
 \tag{6.4}
\]

Consequently

\[
\begin{aligned}
 \frac{\mathcal J_{\rm all}(I)}{D_M^{1/3}}
 &\ge c
 \left(\frac{Pa}{q^2}\right)^{4/3}M^{-2}\\
 &=c(\delta a)^{4/3}M^{-2}\\
 &=c\gamma^{4/3}.
\end{aligned}
 \tag{6.5}
\]

Combining (5.6) and (6.5) proves the main result.

### Theorem 6.1 -- dynamical saturation of the phase-free root ledger

Fix \(\nu>0\), a physical interval \(I=[0,T]\), a fixed target multiplier,
and the declared triangular geometry.  There is \(\gamma_0>0\) such that for
every fixed \(0<\gamma\le\gamma_0\), the construction above gives a sequence
of exact smooth global unforced three-dimensional Navier--Stokes solutions
with:

1. \(M=2^n\) shifted Rudin--Shapiro shear carriers;
2. one exact simple target root at \(t_M=q^{-2}M^{-3}>0\);
3. \(\eta_M\asymp\gamma M^2\);
4. bounded enstrophy contrast and bounded full rotational charge;
5. a nonvanishing complete normalized ledger,

\[
 \boxed{
 \liminf_{M\to\infty}
 \frac{\mathcal J_{{\rm all},M}(I)}
 {D_M^{1/3}\Lambda_1(I;u_M)}
 \ge
 c\frac{\gamma^{4/3}}{\nu^2+\gamma^2}>0.}
 \tag{6.6}
\]

The constant in (6.6) also contains the fixed target, interval, background,
and torus normalizations.  It is independent of \(M\) and \(q\).

The complete ledger may contain other roots.  They can only increase its
nonnegative numerator.  No no-spurious-root theorem is needed.

---

## 7. Match to the R0.72C upper theorem

For this family,

\[
 \frac M{K_s}\asymp M^{-2},
 \qquad
 \chi_0\asymp1,
 \qquad
 \left(\frac{\Omega_0^2}{K_v}\right)^{1/3}
 \asymp M^{-2/3},
 \tag{7.1}
\]

and hence the static factor is \(M^{-8/3}\).  Also

\[
 \eta_M^{4/3}\asymp\gamma^{4/3}M^{8/3},
 \qquad
 \eta_M\ell_\times=O(\gamma).
 \tag{7.2}
\]

The inherited differentiated-row estimate is \(q_\rho\le3\).  Together with
(2.17), substitution in the R0.72C upper bound gives an
\(O_\gamma(1)\) normalized ledger.  Theorem 6.1 gives a positive lower
constant.  Thus the upper and lower scales match:

\[
 \boxed{
 \frac{\mathcal J_{{\rm all},M}}
 {D_M^{1/3}\Lambda_1}
 \asymp_{\nu,I,\gamma}1.}
 \tag{7.3}
\]

The match uses all three ingredients together:

1. Rudin--Shapiro phase flatness gives \(\Omega_0\asymp\sqrt M\);
2. spectral translation gives \(\ell_\times\asymp M^{-2}\);
3. target-row launch alignment creates a real simple root with slope
   \(\asymp M\).

Removing any one of them changes the ledger.  Low carriers have too long a
rotational-charge tail.  Coherent phases have a smaller participation factor.
An algebraic multiplier family without row-aligned data need not produce a
root at all.

The theorem also explains the two equality diagnostics.  The first term of
the upper ledger becomes critical at \(\eta\asymp M^2\).  Because the actual
mixed exposure is \(M^{-2}\), the exposure term becomes critical at the same
scale rather than at the coarser fixed-length boundary.

---

## 8. Deterministic certificate and independent checks

The analytic proof is Sections 1--7.  The certificate is corroborating
evidence.  Its producer path reconstructs, at high precision:

1. both Rudin--Shapiro generators;
2. the shifted moment identity (2.3);
3. target-row alignment and the exact launch slope (3.5);
4. Abel-weighted multiplier envelopes and their \(M^{-3/2}\), \(M^{-1}\)
   time scales;
5. the \(M^{-8/3}\) static coefficient;
6. the \(\eta\asymp M^2\), full-charge \(O(1)\), and launch-aligned
   normalized \(M^0\) scaling models.

The independent program uses a separate binary-parity generator, binary64
FFT sampling, a separate finite-lattice assembly, and direct ODE evolution.
It does not import the producer or read its result.  It alone constructs the
representative finite-lattice interior roots at \(\tau_M=M^{-3}\), and checks
their corrections, residuals, row slopes, contractivity, exact corrected
amplitude balance, and truncation-radius stability.  Floating-point root and
slope values do not prove the infinite-lattice theorem; they test the finite
algebra and the direction of every asymptotic scale.

The formal figure uses only certificate-derived normalized quantities.  Its
contract asks one question: does spectral translation keep the static phase
coefficient at \(M^{-8/3}\) while changing the thermal exposure from a long
tail to \(M^{-2}\), so that the critical normalized ledger remains order
one?  Vector PDF/SVG and 600 dpi PNG are archived with the data, source,
caption, manifest, and grayscale QA.

---

## 9. Literature boundary

The literature audit found no theorem that directly estimates time zeros of
one Fourier coordinate, their crossing slopes, or a launch-inclusive root
ledger for the changing heat-decaying profile in (1.8).

The closest enhanced-dissipation results concern different observables and
different profile classes.

- Coble--He treat time-dependent shears with a fixed finite critical-point
  structure and uniform shape constants.
- Benthaus--Nobili treat a scalar time modulation of one fixed spatial
  profile.
- Benthaus--Coclite--Nobili treat one translating sinusoidal shear.
- Gardner--Liss--Mattingly, Albritton--Beekie, and Liss--Luan obtain sharp
  mixing or dissipation information for fixed profiles.
- Cooperman--Iyer--Son treat random alternating shears through a Harris
  theorem.

These works support frozen or post-burn-in comparisons.  None counts the
zeros of \(F_0(t)\) or supplies (3.14).  The Rudin--Shapiro sources of
Balister and Erdelyi support the phase-flat polynomial input; their polynomial
zeros are zeros in the phase variable, not the temporal target roots used
here.  Angenent's zero-set theorem concerns spatial zeros of real scalar
one-dimensional parabolic equations and does not apply to the complex target
coordinate in (1.6).

The new calculation in this report is therefore the direct short-time
construction in Sections 2--6.  Enhanced dissipation is not used as a
substitute for the root proof.

---

## 10. What has and has not been proved

The completed analytic content is:

1. a shifted Rudin--Shapiro multiplier bound stable under unequal heat
   weights;
2. \(M^{-3/2}\) integrated multiplier exposure and \(M^{-1}\) integrated
   square exposure;
3. exact target-row saturation by finite-support launch data;
4. an exact simple **interior** target root at \(\tau_M=M^{-3}\);
5. a noncollapsing target-row slope at that root;
6. fixed-interval enstrophy contrast controlled by a decoupled background;
7. a full-frequency projected rotational-charge bound of order \(\gamma^2\);
8. a positive lower limit for the complete normalized
   \(D^{1/3}\Lambda_1\) root ledger;
9. matching upper and lower order-one scales at \(\eta\asymp M^2\).

The following statements are not proved:

1. divergence of the normalized ledger or failure of the
   \(D^{1/3}\Lambda_1\) payment;
2. a universal payment theorem even for every triangular solution;
3. a continuation criterion for general three-dimensional solutions;
4. finite-time singularity or global regularity for general Navier--Stokes;
5. an \(M\)-uniform enhanced-dissipation theorem for the changing shifted
   profile;
6. a transfer of this root mechanism to a critical norm outside the exact
   triangular class.

R0.72D resolves the specific dynamical gap left by R0.72C: the phase-free
prefactor is not merely algebraically sharp.  A real exact evolution can
saturate it after the complete nonlinear charge is retained.  The result is
still an internal sharpness theorem in a globally regular invariant subclass.

The next finite gate is R0.72E.  It should ask whether the order-one family can
be made supercritical without the rotational charge growing, or whether a
new exact lower mechanism forces a universal order-one ceiling.  Either
outcome must retain the interior-root construction, the full charge, and the
fixed physical interval; a terminal decay plot alone cannot decide it.
