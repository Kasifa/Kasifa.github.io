# R0.72E -- a one-carrier supercritical root ledger and failure of the candidate one-third payment

**Date:** 2026-08-27
**Status:** analytic theorem in the exact triangular 2.5D Navier--Stokes
class.  The action estimate uses a quantitative parabolic-Hörmander density
bound and is checked independently from the physical scaling ledger.  The
result disproves one candidate intermediate estimate.  It does not prove a
finite-time singularity, global regularity, or a continuation criterion for
general three-dimensional Navier--Stokes solutions.

**Keywords:** Navier--Stokes regularity, triangular 2.5D flows, temporal
roots, Bessel functions, negative Sobolev action, Feynman--Kac,
parabolic Hörmander diffusion, sharpness

---

## 0. Direct decision

R0.72D constructed an exact smooth triangular family for which

\[
 \frac{\mathcal J_{\rm all}}
 {D^{1/3}\Lambda_1}
\]

stays bounded below by a positive constant.  It did not decide whether the
ratio can diverge.  The one-carrier Bessel family from R0.72A already had the
required logarithmic root-slope mass, but the full projected rotational
charge had not been controlled on a fixed physical interval.

This report closes that missing action estimate.  Fix once and for all an
integer \(q_0\) larger than the Fourier radius of the target multiplier.
For the scaled one-carrier equation

\[
 \partial_x\phi
 =\left(\partial_\theta^2-q_0^{-2}\right)\phi
 -2i\delta e^{-x}\cos\theta\,\phi,
 \qquad
 \phi(0,\theta)=ie^{-i\theta},
 \tag{0.1}
\]

put

\[
 A_q=q_0^{-2}-\partial_\theta^2,
 \qquad
 V(x)=-2ie^{-x}\cos\theta,
 \tag{0.2}
\]

and

\[
 Q_{\delta,q_0}(X)
 :=\int_0^X\|V(x)\phi(x)\|_{A_q^{-1}}^2\,dx.
 \tag{0.3}
\]

The main analytic estimate is

\[
 \boxed{
 Q_{\delta,q_0}(X)
 \le C_{X,q_0}\frac{1+\log(2+\delta)}{\delta},
 \qquad \delta\ge1.}
 \tag{0.4}
\]

The constant is uniform in \(\delta\), but not in a limit
\(q_0\to\infty\).  That distinction is essential.

Take the exact Bessel sequence

\[
 \delta_R=R^4,
 \qquad
 P_R=q_0^2\delta_R,
 \qquad
 S_R^2=\frac{\delta_R}{\log(2+\delta_R)}.
 \tag{0.5}
\]

Here \(P_R\) is the physical shear amplitude and \(S_R\) is the active
amplitude.  On every fixed physical interval \(I=[0,T]\), the resulting
exact smooth global unforced NSE solutions satisfy

\[
 D_R\asymp_{q_0}\delta_R^2,
 \qquad
 \mathcal R_{Y_R}(I)\le C_{T,q_0},
 \qquad
 \Lambda_1(I;u_R)\le C_{T,q_0},
 \tag{0.6}
\]

while their selected positive root ledger obeys

\[
 \mathcal J_{{\rm all},R}(I)
 \ge c_{T,q_0}\delta_R.
 \tag{0.7}
\]

Consequently

\[
 \boxed{
 \frac{\mathcal J_{{\rm all},R}(I)}
 {D_R^{1/3}\Lambda_1(I;u_R)}
 \ge c_{T,q_0}\delta_R^{1/3}
 =c_{T,q_0}R^{4/3}\longrightarrow\infty.}
 \tag{0.8}
\]

Thus no data-independent constant can make the candidate
\(D^{1/3}\Lambda_1\) payment valid for every smooth solution, even inside
this exact globally regular triangular subclass.  This is a negative result
about one proposed proof route.  It is not a counterexample to regularity:
every member of the family is smooth for all positive time.

---

## 1. Exact triangular NSE class and fixed target isolation

Work on the normalized three-torus.  Let

\[
 u(x,y,z,t)=(f(y,z,t),0,v(y,t)).
 \tag{1.1}
\]

The unforced Navier--Stokes equations reduce exactly to

\[
 \boxed{
 v_t=\nu v_{yy},
 \qquad
 f_t+vf_z=\nu(f_{yy}+f_{zz}).}
 \tag{1.2}
\]

The vorticity and projected Lamb vector are

\[
 \omega=(v_y,f_z,-f_y),
 \qquad
 \boxed{\mathbb P(u\times\omega)=(-vf_z,0,0).}
 \tag{1.3}
\]

The gradient part of \(u\times\omega\) is removed exactly.  All charge
estimates below concern the projected field in (1.3), not a target-shell
proxy.

Set

\[
 \nu=d=K_z=z_1=1,
 \qquad K_y=0,
 \qquad r_1=1.
 \tag{1.4}
\]

Fix a compact real-even annular multiplier \(T_*\) which is nonzero at

\[
 k_*=(0,0,1),
 \tag{1.5}
\]

and let \(R_*\) be the largest Fourier radius in its support.  Choose a
single integer

\[
 q_0>R_*.
 \tag{1.6}
\]

This integer remains fixed as \(R\to\infty\).  The shear is

\[
 v_R(y,t)=P_Re^{-q_0^2t}
 \left(e^{iq_0y}+e^{-iq_0y}\right).
 \tag{1.7}
\]

For the positive \(K_z\) sector, write

\[
 \widehat f_R(q_0r,1,t)=S_RF_{R,r}(x),
 \qquad x=q_0^2t.
 \tag{1.8}
\]

Then

\[
 \partial_xF_R=D_qF_R+\delta_RV(x)F_R,
 \tag{1.9}
\]

where

\[
 (D_qF)_r=-(r^2+q_0^{-2})F_r,
 \qquad
 (V(x)F)_r=-ie^{-x}(F_{r-1}+F_{r+1}),
 \tag{1.10}
\]

and

\[
 F_R(0)=ie_{-1},
 \qquad
 \delta_R=P_R/q_0^2.
 \tag{1.11}
\]

The negative \(K_z\) sector is its real conjugate, so the physical velocity
is real.  Finite Fourier initial data in (1.7)--(1.11) produce exact global
smooth solutions of (1.2).

Condition (1.6) also repairs an isolation issue that would occur at
\(q_0=1\).  Every non-target active mode has frequency \((q_0r,\pm1)\) with
\(r\ne0\), and the shear has frequency \((\pm q_0,0)\).  All lie outside
the support of \(T_*\).  Therefore zeroing \(F_{R,0}\) zeros the complete
declared target shell, not only one coefficient.

---

## 2. Fixed-\(q_0\) persistence of the Bessel roots

The fixed \(q_0\) extension of R0.72A changes only the constant diagonal
term in \(D_q\).  In fact, if \(F_1\) denotes the solution with diagonal
\(-(r^2+1)\), then the identity

\[
 \boxed{F_{q_0}(x)=e^{(1-q_0^{-2})x}F_1(x)}
 \tag{2.1}
\]

is exact.  Thus the target roots are identical, and the row slope at a root
is multiplied by the positive factor \(e^{(1-q_0^{-2})x}\).  Put

\[
 U_R(\tau)=F_R(\tau/\delta_R).
 \tag{2.2}
\]

Then

\[
 U_R'=\delta_R^{-1}D_qU_R
 +V(\tau/\delta_R)U_R.
 \tag{2.3}
\]

The frozen system is independent of \(q_0\):

\[
 W'=V(0)W,
 \qquad W(0)=ie_{-1}.
 \tag{2.4}
\]

Under lattice Fourier transform,

\[
 W(\theta,\tau)
 =ie^{-i\theta}e^{-2i\tau\cos\theta},
 \qquad
 P_0W(\tau)=J_1(2\tau).
 \tag{2.5}
\]

For each fixed \(q_0\), the same energy comparison as in R0.72A gives

\[
 \sup_{0\le\tau\le X}
 \|U_R(\tau)-W(\tau)\|_2
 +\sup_{0\le\tau\le X}
 \left|P_0U_R'(\tau)-2J_1'(2\tau)\right|
 \le C_{q_0}\frac{1+X^3}{\delta_R}.
 \tag{2.6}
\]

Indeed, \(\|D_qW(\tau)\|_2\le C_{q_0}(1+\tau^2)\), while

\[
 \|V(\tau/\delta_R)-V(0)\|
 \le2\tau/\delta_R.
 \tag{2.7}
\]

Let \(j_{1,k}\) be the positive zeros of \(J_1\) and
\(\tau_k=j_{1,k}/2\).  Taking \(X=O(R)\) and \(\delta_R=R^4\) makes the
\(C^1\) error in (2.6) \(O_{q_0}(R^{-1})\), smaller than the weakest
Bessel slope \(R^{-1/2}\).  Hence, for all sufficiently large \(R\), there
is one simple exact root \(s_{k,R}\) near each \(\tau_k\),
\(1\le k\le R\).  In scaled and physical time,

\[
 x_{k,R}=s_{k,R}/\delta_R,
 \qquad
 t_{k,R}=x_{k,R}/q_0^2,
 \qquad
 0<t_{k,R}\le C_{q_0}R^{-3}.
 \tag{2.8}
\]

At an exact root the target diagonal term vanishes, so

\[
 h_{k,R}:=P_0V(x_{k,R})F_R(x_{k,R})
 =P_0U_R'(s_{k,R}).
 \tag{2.9}
\]

The standard Bessel zero and derivative asymptotics therefore give

\[
 \boxed{
 G_R^{\rm sel}:=\sum_{k=1}^R|h_{k,R}|^2
 =\frac8{\pi^2}\log R+O_{q_0}(1).}
 \tag{2.10}
\]

Every selected root is a complete target-shell root by Section 1.  It is
simple and its target component of the projected Lamb vector is nonzero.  At
such a root, the inherited global-shell equations give

\[
 C_{*,t}=-\Delta F_*,
 \qquad
 \langle F_*,C_{*,t}\rangle=\|\nabla F_*\|_2^2>0.
 \tag{2.11}
\]

Thus every selected root is a positive right entry even though the scalar
crossing derivatives alternate in sign.  There is no parity loss.  Additional
roots can only increase the nonnegative complete ledger.

---

## 3. The negative Sobolev action theorem

This is the new analytic gate.  Use normalized Haar measure on
\(\mathbb T\) and write

\[
 \|g\|_{A_q^{-1}}^2
 =\sum_{n\in\mathbb Z}
 \frac{|\widehat g_n|^2}{q_0^{-2}+n^2}.
 \tag{3.1}
\]

### Lemma 3.1 -- a uniform oscillatory \(A_q^{-1}\) bound

For fixed \(q_0\), all \(\kappa\ge0\), and all \(\beta\in\mathbb R\),

\[
 h_{\kappa,\beta}(\theta)
 =\cos\theta\,e^{-i\theta}
 e^{-i\kappa\cos(\theta+\beta)}
 \tag{3.2}
\]

satisfies

\[
 \boxed{
 \|h_{\kappa,\beta}\|_{A_q^{-1}}^2
 \le\frac{C_{q_0}}{1+\kappa}.}
 \tag{3.3}
\]

#### Proof

For \(\kappa\ge4\) and \(|n|\le\kappa/2\), the phase in the \(n\)-th
Fourier coefficient has two uniformly nondegenerate stationary points.
The one-dimensional stationary-phase estimate is uniform in \(n\) and
\(\beta\), and gives

\[
 |\widehat h_{\kappa,\beta}(n)|
 \le C\kappa^{-1/2}.
 \tag{3.4}
\]

Therefore the low modes contribute at most

\[
 C\kappa^{-1}
 \sum_{n\in\mathbb Z}\frac1{q_0^{-2}+n^2}
 =C\kappa^{-1}\pi q_0\coth(\pi/q_0).
 \tag{3.5}
\]

For \(|n|>\kappa/2\), Parseval and
\((q_0^{-2}+n^2)^{-1}\le C\kappa^{-2}\) give an
\(O(\kappa^{-2})\) contribution.  When \(\kappa<4\), use
\(\|A_q^{-1}\|=q_0^2\) and enlarge the constant.  This proves (3.3).
\(\square\)

The zero Fourier weight in (3.5) explains why the constant is not uniform
as \(q_0\to\infty\).

### Lemma 3.2 -- exact Feynman--Kac representation

Let \(B_t=\sqrt2W_t\) and

\[
 Z_t=\int_0^t e^{-(t-s)}e^{iB_s}\,ds.
 \tag{3.6}
\]

Then the solution of (0.1) is

\[
 \boxed{
 \phi(t,\theta)
 =ie^{-q_0^{-2}t}e^{-i\theta}
 \mathbb E\!\left[
 e^{-iB_t}
 \exp\{-2i\delta\operatorname{Re}(e^{i\theta}Z_t)\}
 \right].}
 \tag{3.7}
\]

The reverse-time potential in the initial-value Feynman--Kac formula is
what produces \(e^{-(t-s)}\) in (3.6).  Replacing it by \(e^{-s}\) would
be an incorrect time ordering.

Hilbert-space Jensen and Lemma 3.1 now give

\[
\begin{aligned}
 \|V(t)\phi(t)\|_{A_q^{-1}}^2
 &\le4e^{-2(1+q_0^{-2})t}
 \mathbb E\left\|
 h_{2\delta|Z_t|,\arg Z_t}
 \right\|_{A_q^{-1}}^2\\
 &\le C_{q_0}
 \mathbb E\frac1{1+\delta|Z_t|}.
\end{aligned}
 \tag{3.8}
\]

### Lemma 3.3 -- polynomial marginal density and a negative moment

The process in (3.6) satisfies

\[
 dB_t=\sqrt2\,dW_t,
 \qquad
 dZ_t=(-Z_t+e^{iB_t})\,dt.
 \tag{3.9}
\]

On the lifted state space \(\mathbb R\times\mathbb R^2\), take

\[
 X_1=\sqrt2\,\partial_b,
 \qquad
 X_0=(-x+\cos b)\partial_x+(-y+\sin b)\partial_y.
 \tag{3.10}
\]

The drift brackets are

\[
 [X_1,X_0]
 =\sqrt2(-\sin b\,\partial_x+\cos b\,\partial_y),
 \tag{3.11}
\]

\[
[X_1,[X_1,X_0]]
=-2(\cos b\,\partial_x+\sin b\,\partial_y).
\tag{3.12}
\]

In the ordered coordinates \((b,x,y)\), the absolute determinant of these
three vectors is exactly \(4\).  They therefore form a uniformly
nondegenerate frame.  The
quantitative parabolic-Hörmander density estimate in Kusuoka--Stroock,
*Applications of the Malliavin calculus, Part II*, Corollary (3.25) and
inequality (3.27), pp. 22--23, therefore applies.  The frame above puts the
fixed starting point in every required \(U_L\).  Choose the off-diagonal
order in (3.27) larger than one; its polynomial terminal-angle weight is then
integrable over the lifted terminal angle.  Thus the marginal law of \(Z_t\)
has a density \(\rho_t\) such that, for each fixed \(X<\infty\),

\[
 \|\rho_t\|_\infty\le C_Xt^{-N},
 \qquad 0<t\le X,
 \tag{3.13}
\]

for some finite \(N\).  Existence of a smooth density alone would not be
enough; the polynomial small-time control in (3.13) is the property used
below.

Let

\[
 \mathcal G_t
 =\left\{\sup_{0\le s\le t}|B_s|\le\pi/3\right\}.
 \tag{3.14}
\]

On this event,

\[
 |Z_t|\ge\operatorname{Re}Z_t
 \ge\frac12(1-e^{-t})
 \ge\frac12e^{-X}t.
 \tag{3.15}
\]

The reflection principle gives

\[
 \mathbb P(\mathcal G_t^c)
 \le4e^{-\pi^2/(36t)}.
 \tag{3.16}
\]

Since \(|Z_t|\le1\), (3.13) and polar integration give a polynomial bound
for \(\mathbb E|Z_t|^{-3/2}\).  Hölder's inequality on
\(\mathcal G_t^c\), together with (3.16), then yields

\[
\begin{aligned}
 \mathbb E\left[|Z_t|^{-1}\mathbf1_{\mathcal G_t^c}\right]
 &\le
 \left(\mathbb E|Z_t|^{-3/2}\right)^{2/3}
 \mathbb P(\mathcal G_t^c)^{1/3}\\
 &\le C_X/t.
\end{aligned}
 \tag{3.17}
\]

Equation (3.15) gives the same bound on \(\mathcal G_t\).  Hence

\[
 \boxed{\mathbb E|Z_t|^{-1}\le C_X/t,
 \qquad0<t\le X.}
 \tag{3.18}
\]

### Theorem 3.4 -- action decay

For fixed \(q_0\) and \(X\), equations (3.8) and (3.18) imply

\[
 \mathbb E\frac1{1+\delta|Z_t|}
 \le\min\left\{1,\frac{C_X}{\delta t}\right\}.
 \tag{3.19}
\]

Integrating at the transition scale \(t\asymp\delta^{-1}\) proves

\[
\begin{aligned}
 Q_{\delta,q_0}(X)
 &\le C_{q_0}\int_0^X
 \min\left\{1,\frac{C_X}{\delta t}\right\}\,dt\\
 &\le C_{X,q_0}
 \frac{1+\log(2+\delta)}{\delta}.
\end{aligned}
 \tag{3.20}
\]

This proves (0.4).  The logarithm comes from integrating the worst
stationary-phase direction.  No claim of a sharp constant is made.

---

## 4. Active enstrophy bound

The full physical ledger also needs a uniform first Fourier moment.  Let

\[
 E(x)=\|\phi(x)\|_2^2,
 \qquad
 X(x)=\|\phi_\theta(x)\|_2^2.
 \tag{4.1}
\]

Skew-adjointness of the imaginary potential gives

\[
 \frac12E'
 =-X-q_0^{-2}E,
 \qquad E(x)\le1.
 \tag{4.2}
\]

After differentiating (0.1),

\[
 \frac12X'
 \le-\|\phi_{\theta\theta}\|_2^2
 -q_0^{-2}X+2\delta\sqrt X.
 \tag{4.3}
\]

Because

\[
 X=|\langle-\phi_{\theta\theta},\phi\rangle|
 \le\|\phi_{\theta\theta}\|_2\|\phi\|_2
 \le\|\phi_{\theta\theta}\|_2,
 \tag{4.4}
\]

we obtain

\[
 X'\le-2X^2-2q_0^{-2}X+4\delta\sqrt X.
 \tag{4.5}
\]

At \(X\ge(2\delta)^{2/3}\), the nonlinear source is no larger than
\(2X^2\).  Since \(X(0)=1\), the scalar barrier gives

\[
 \boxed{
 \sup_{x\ge0}\|\phi_\theta(x)\|_2^2
 \le\max\{1,(2\delta)^{2/3}\}.}
 \tag{4.6}
\]

This estimate is deliberately coarse.  It is sufficient because the chosen
active amplitude remains below the shear enstrophy scale.

---

## 5. Full physical ledger on a fixed interval

Fix \(I=[0,T]\), independent of \(R\).  Parseval and (1.7) give

\[
 \|v_{R,y}(t)\|_2^2
 =2q_0^2P_R^2e^{-2q_0^2t}.
 \tag{5.1}
\]

In fact, with \(x=q_0^2t\), the full enstrophy has the exact decomposition

\[
 Y_R(t)=2q_0^2P_R^2e^{-2x}
 +2S_R^2\left(
 \|F_R(x)\|_2^2+q_0^2\|\phi_{R,\theta}(x)\|_2^2
 \right).
 \tag{5.2}
\]

The active sector satisfies, by (4.2) and (4.6),

\[
 \|f_{R,z}(t)\|_2^2+\|f_{R,y}(t)\|_2^2
 \le C_{q_0}S_R^2
 \left[1+\delta_R^{2/3}\right].
 \tag{5.3}
\]

For the amplitudes in (0.5),

\[
 S_R^2\delta_R^{2/3}
 =\frac{\delta_R^{5/3}}{\log(2+\delta_R)}
 =o(\delta_R^2),
 \tag{5.4}
\]

whereas \(P_R^2=q_0^4\delta_R^2\).  Therefore

\[
 \boxed{
 c_{T,q_0}\delta_R^2
 \le Y_R(t)=\|\omega_R(t)\|_2^2
 \le C_{q_0}\delta_R^2,
 \quad t\in I,}
 \tag{5.5}
\]

and

\[
 \boxed{\mathcal R_{Y_R}(I)\le C_{T,q_0}.}
 \tag{5.6}
\]

At launch the active sector occupies only the conjugate modes generated by
\((q_0(-1),1)\), and the shear occupies \((\pm q_0,0)\).  Under normalized
Fourier Parseval, the data size has the exact form

\[
 D_R=\|u_R(0)\|_2^2+\|\omega_R(0)\|_2^2
 =2P_R^2(1+q_0^2)+2S_R^2(q_0^2+2).
 \tag{5.7}
\]

Thus

\[
 \boxed{c_{q_0}\delta_R^2\le D_R\le C_{q_0}\delta_R^2.}
 \tag{5.8}
\]

No decoupled enstrophy background is required in this family.  The single
fixed shear frequency itself persists by a fixed relative amount throughout
\(I\).

---

## 6. Full projected rotational charge

The positive \(K_z\) sector of \(-vf_z\) has lattice coefficients
\(S_RP_RV(x)F_R(x)\).  Its physical frequency is \((q_0r,1)\), so

\[
 \frac1{q_0^2r^2+1}
 =q_0^{-2}\frac1{r^2+q_0^{-2}}.
 \tag{6.1}
\]

Including the conjugate sector gives the exact Fourier identity

\[
 \|\mathbb P(u_R\times\omega_R)(t)\|_{\dot H^{-1}}^2
 =2S_R^2P_R^2q_0^{-2}
 \|V(x)F_R(x)\|_{A_q^{-1}}^2.
 \tag{6.2}
\]

Changing variables \(x=q_0^2t\) gives the exact identity

\[
 \int_0^T
 \|\mathbb P(u_R\times\omega_R)(t)\|_{\dot H^{-1}}^2\,dt
 =2S_R^2P_R^2q_0^{-4}
 Q_{\delta_R,q_0}(q_0^2T).
 \tag{6.3}
\]

The exact shear floor from (5.2) is

\[
 Y_R(t)\ge2q_0^2P_R^2e^{-2q_0^2T},
 \qquad t\in[0,T].
 \tag{6.4}
\]

Dividing (6.3) by (6.4) exposes all three fixed-scale factors: one
\(q_0^{-2}\) from the negative Sobolev weight, one from the time Jacobian,
and one from the shear-enstrophy denominator.  Applying (3.20),

\[
\begin{aligned}
 \frac1T\int_I
 \frac{\|\mathbb P(u_R\times\omega_R)\|_{\dot H^{-1}}^2}
 {Y_R(t)}\,dt
 &\le\frac{e^{2q_0^2T}S_R^2}{Tq_0^6}
 Q_{\delta_R,q_0}(q_0^2T)\\
 &\le C_{T,q_0}
 \frac{\delta_R}{\log(2+\delta_R)}
 \frac{1+\log(2+\delta_R)}{\delta_R}\\
 &\le C_{T,q_0}.
\end{aligned}
 \tag{6.5}
\]

With \(\nu=1\), equations (5.6) and (6.5) prove

\[
 \boxed{
 \Lambda_1(I;u_R)
 =\mathcal R_{Y_R}(I)
 \left[1+\frac1T\int_I
 \frac{\|\mathbb P(u_R\times\omega_R)\|_{\dot H^{-1}}^2}
 {Y_R(t)}\,dt\right]
 \le C_{T,q_0}.}
 \tag{6.6}
\]

This is the point at which R0.72A stopped.  The estimate concerns every
Fourier mode of the projected rotational charge.

---

## 7. Divergence of the complete normalized root ledger

At every selected simple root, the fixed target multiplier and the exact
global-shell identity give

\[
 J_*(t_{k,R})
 =c_*\frac{S_R^2P_R^2|h_{k,R}|^2}{Y_R(t_{k,R})},
 \qquad c_*>0.
 \tag{7.1}
\]

The upper enstrophy bound in (5.5), the fixed relation
\(P_R=q_0^2\delta_R\), and (2.10) yield

\[
\begin{aligned}
 \mathcal J_{{\rm all},R}(I)
 &\ge\sum_{k=1}^RJ_*(t_{k,R})\\
 &\ge c_{q_0}S_R^2G_R^{\rm sel}\\
 &\ge c_{q_0}
 \frac{\delta_R}{\log(2+\delta_R)}\log R.
\end{aligned}
 \tag{7.2}
\]

Since \(\log\delta_R=4\log R\),

\[
 \boxed{\mathcal J_{{\rm all},R}(I)\ge c_{q_0}\delta_R.}
 \tag{7.3}
\]

Combining (5.8), (6.6), and (7.3) gives (0.8).

### Theorem 7.1 -- failure of the candidate one-third payment

Fix \(T>0\), the target multiplier, and an integer \(q_0>R_*\).  There is
a sequence of exact, smooth, global, unforced three-dimensional
Navier--Stokes solutions in the triangular class (1.1) such that

1. each solution has at least \(R\) simple positive complete target-shell
   roots in \((0,C_{q_0}R^{-3})\);
2. \(D_R\asymp\delta_R^2\), with \(\delta_R=R^4\);
3. \(\mathcal R_{Y_R}([0,T])\) and the full normalized rotational charge
   remain bounded;
4. \(\mathcal J_{{\rm all},R}([0,T])\gtrsim\delta_R\); and
5. the normalized ratio diverges at least as \(R^{4/3}\).

In particular, there is no constant \(C\), independent of the smooth
initial data, for which

\[
 \mathcal J_{\rm all}(I)
 \le C D^{1/3}\Lambda_1(I;u)
 \tag{7.4}
\]

holds throughout this exact subclass.

The theorem does not rule out estimates with a stronger data factor, a new
frequency-sensitive term, or a different nonlocal payment.  It also does
not produce blow-up: the triangular equations remain globally smooth.

---

## 8. Computational certificates

The proof is analytic.  The release includes two independent finite audits.

1. The producer recomputes the fixed-\(q_0\) Bessel roots, selected slope
   mass, action integral under a Fourier split-step scheme, first-moment
   barrier, and the full exponent ledger.
2. The independent audit shares neither the producer code nor its output.
   It uses a fixed-step real-lattice RK4 root scan and a separate adaptive
   BDF action solve with an analytic sparse tridiagonal Jacobian.  It
   re-derives the physical powers from raw amplitude definitions.

Both programs pass 16 of 16 declared checks and preserve progress and
resource logs, configuration, software versions, raw results, and checksums.
The producer integrates the action through scaled time \(X=6\); the
independent BDF audit uses \(X=1\), so their finite action values are not
presented as same-endpoint duplicates.  The finite calculations corroborate
the signs, normalizations, and scaling choices.  They do not replace the
infinite-lattice root proof, the Kusuoka--Stroock density theorem, or the
stationary-phase estimate.

---

## 9. Literature boundary

The only external theorem used in the new action proof is the quantitative
uniform parabolic-Hörmander density estimate in Kusuoka--Stroock,
*Applications of the Malliavin calculus, Part II*, Corollary (3.25) and
inequality (3.27), pp. 22--23,
[DOI 10.15083/00039520](https://doi.org/10.15083/00039520).  Part III is
not the correct source for this step because its relevant density section
removes the drift, whereas the two \(Z\)-directions here are created by
brackets with the drift.

The Jacobi--Anger identity, simplicity and asymptotics of the Bessel zeros,
and derivative asymptotics are recorded in the NIST DLMF
[Sections 10.12](https://dlmf.nist.gov/10.12),
[10.21](https://dlmf.nist.gov/10.21), and
[10.17](https://dlmf.nist.gov/10.17).  They justify the frozen Bessel
constants, not persistence under the exact dissipative evolution; the latter
is proved in Section 2.

Fixed-profile enhanced-dissipation results generally control terminal or
space-time norms.  The closest deterministic transfers give a weaker global
decay scale and do not state the integrated \(A_q^{-1}\) observation in
(0.4).  The Feynman--Kac reduction is therefore not being quoted from that
literature.

No cited source states Theorem 7.1.  The literature audit is a bounded
non-collision check, not a claim of originality or priority.

---

## 10. Claim--evidence boundary

### Proved

1. The fixed-\(q_0\) one-carrier evolution has the exact Feynman--Kac
   representation (3.7).
2. The deterministic oscillatory factor obeys the uniform
   \(A_q^{-1}\) estimate (3.3).
3. The kinetic phase process has the polynomial marginal density bound
   needed for (3.18), by the cited quantitative drift-bracket theorem.
4. The full negative Sobolev action obeys (3.20).
5. The active first Fourier moment obeys the global barrier (4.6).
6. The fixed-\(q_0\) Bessel family retains \(R\) exact simple positive
   target-shell roots and logarithmic selected slope mass.
7. The complete full-frequency \(\Lambda_1\) remains bounded for the
   amplitudes (0.5).
8. The candidate \(D^{1/3}\Lambda_1\) payment fails inside the declared
   exact triangular class.

### Not proved

1. Sharpness of the logarithm in (3.20), or a sharp action constant.
2. A bound uniform when \(q_0\) grows with \(R\).
3. Failure of every possible data-dependent payment.
4. Transfer of the root family to nontriangular dynamics with genuine
   feedback from \(f\) into \(v\).
5. A new continuation criterion for arbitrary three-dimensional solutions.
6. Finite-time singularity or global regularity for general Navier--Stokes.
7. An originality, priority, or exhaustive-literature claim.

---

## 11. Research value and next finite gate

The result has a clear negative value.  The one-third candidate survived the
bounded-coupling, many-carrier, phase-cancellation, and order-one dynamical
audits through R0.72D.  R0.72E shows that it fails in a much simpler
one-carrier strong-coupling family once the exact negative Sobolev action is
paid.  Continuing to seek a proof of (7.4) would therefore be wasted effort.

The value to the Millennium problem remains indirect.  A failed candidate
estimate removes one route; it does not decide regularity.  Moreover, the
counterfamily lies in a globally regular invariant class and exploits roots
accumulating near launch.  The next finite gate, R0.72F, should ask what
additional quantity blocks this family without becoming stronger than the
unknown general problem.  Natural candidates are a frequency-sensitive
initial layer charge, a time-weighted rotational action, or a payment that
sees the coupling scale \(\delta\).  Any replacement must first be tested on
the exact family above before it is used in a general three-dimensional
argument.
