# R0.74G — complete-payment closure rejects the frozen local-frame inequalities

## Status and scope

R0.74F proved that two passive packets survive in a selected Gaussian
outer annulus for an explicit smooth periodic mean-zero 2D3C
Navier--Stokes family.  It did not estimate the complete denominator in
the frozen Version-M and Version-F questions of R0.74E.

This note closes that familywise denominator ledger.  Its decisive new
ingredient is a full-time weighted occupation lemma.  The lemma uses a
pathwise one-sided displacement bound, a normalized periodic Brownian
bridge, and a periodic Peetre convolution estimate.  It does not divide a
small shift error by the packet radius, and hence has no spurious
\(R^{-1}\) loss.

The resulting statement is:

> The frozen proposed inequalities R0.74E (3.11) and (4.17) are false.
> They fail on one explicit sequence of smooth periodic unforced
> Navier--Stokes solutions.

This is a negative theorem about two internally proposed local-frame
estimates.  It is not a singular solution, a blow-up theorem, a regularity
criterion, or a solution of the Millennium problem.  **NOT CLAY.**

Current status:

    DERIVED / SAME-SOURCE AUDITS AND CERTIFICATE PENDING / NOT FROZEN

The inherited R0.74F source is frozen at commit

    56f53d4e8b905203589e1129fd15a61863cd8cc1.

---

## 1. Frozen family and the counterexample scale

Retain the R0.74F constants

\[
 \lambda=\frac{63}{32},\qquad
 c_h=\frac{15}{16},\qquad
 \alpha=\frac{14}{15},\qquad
 \beta=\frac{\sqrt{31}}{16},\qquad
 c_R=\frac1{320},\qquad
 \kappa=16.
\tag{1.1}
\]

For integers \(j\to\infty\), put

\[
 L_j=\lambda2^j,\qquad
 R_j=e^{-c_RL_j^2},\qquad
 r_j=L_jR_j,
\tag{1.2}
\]

\[
 h_j=c_hr_j,\qquad q_j=\beta r_j,
 \qquad h_j^2+q_j^2=r_j^2.
\tag{1.3}
\]

Let \(\theta_j,B_j,Q_j,F_j^\pm\) be exactly the calibrated shear,
amplitude, reference path, and passive packets in R0.74F (1.4)--(1.11).
Thus

\[
 u_j=(\mathfrak a_jF_j,B_j\theta_j,0),
 \qquad F_j=F_j^++F_j^-,
 \qquad p_j=0
\tag{1.4}
\]

is a smooth periodic mean-zero unforced Navier--Stokes solution, and

\[
 X_{R_j}(t)=a_{R_j}(t)=a_{R_j}'(t)=0.
\tag{1.5}
\]

Versions M and F therefore coincide on this family, including the complete
acceleration ledger.

The Gaussian target weight is

\[
 \gamma_j=e^{-c_\gamma L_j^2},
 \qquad c_\gamma=\frac8{3969}.
\tag{1.6}
\]

This note fixes the amplitude

\[
 \boxed{\mathfrak a_j=B_j\gamma_j^{-1/2}.}
\tag{1.7}
\]

The exact contrast calibration gives

\[
 B_jR_j^2\longrightarrow\frac1{128}.
\tag{1.8}
\]

For the proof, abbreviate

\[
 R=R_j,\quad L=L_j,\quad h=h_j,\quad q=q_j,
 \quad B=B_j,\quad Q=Q_j,\quad \mathfrak a=\mathfrak a_j.
\tag{1.9}
\]

### Theorem 1.1 — complete-payment counterexample

For all sufficiently large \(j\), the fields (1.4) with amplitude (1.7)
satisfy

\[
 \boxed{
 P_{R_j}^M=P_{R_j}^F\le C B_j^3R_j^3,}
\tag{1.10}
\]

while the R0.74F survival theorem gives

\[
 \boxed{
 X_{R_j}^M=X_{R_j}^F
 \ge cB_j^2L_jR_j^2.}
\tag{1.11}
\]

Consequently,

\[
 \boxed{
 \frac{X_{R_j}^M}{(P_{R_j}^M)^{2/3}}
 =
 \frac{X_{R_j}^F}{(P_{R_j}^F)^{2/3}}
 \ge cL_j\longrightarrow\infty.}
\tag{1.12}
\]

Hence no constant \(C\), independent of the smooth solution and scale,
can make either proposed inequality R0.74E (3.11) or (4.17) true.

The proof occupies Sections 2--7.

---

## 2. Buffered local energy

The buffered energy is evaluated at radius \(8R\), with

\[
 I_{8R}=(R^2,65R^2).
\tag{2.1}
\]

### Lemma 2.1 — packet exclusion from the buffered ball

Let

\[
 d_E=\frac{\alpha^2}{262}=\frac{98}{29475}.
\tag{2.2}
\]

For the complete paired packet \(F=F^++F^-\),

\[
 \boxed{
 \mathcal E_F(z_0,8R)
 \le C\mathfrak a^2R^2
 \left(e^{-d_EL^2}+e^{-c/R^2}\right).}
\tag{2.3}
\]

Here \(\mathcal E_F\) denotes the packet contribution after the factor
\(\mathfrak a^2\) is included.

**Proof.**  Define the exact transverse marginal

\[
 H(t,z)=\int_{\mathbb T_{x_2}}|F(t,x_2,z)|^2\,dx_2.
\tag{2.4}
\]

The scalar equation is

\[
 \partial_tF+B\theta(t,z)\partial_2F
 =\partial_2^2F+\partial_z^2F.
\tag{2.5}
\]

Because the transport coefficient is independent of \(x_2\), exact
periodic integration gives

\[
 \boxed{
 \partial_tH-\partial_z^2H
 =-2\int_{\mathbb T}
 \left(|\partial_2F|^2+|\partial_zF|^2\right)dx_2\le0.}
\tag{2.6}
\]

The paired heat-kernel datum and
\(|F^++F^-|^2\le2(|F^+|^2+|F^-|^2)\) imply

\[
 H(0,z)
 \le CR\sum_{\pm}
 \exp\!\left[-\frac{d_{\mathbb T}(z,\pm h)^2}{2R^2}\right]
 +Ce^{-c/R^2}.
\tag{2.7}
\]

The scalar maximum principle applied to (2.6) therefore yields, for
\(0\le t\le65R^2\) and \(|z|\le16R\),

\[
 H(t,z)
 \le CR\left(e^{-d_EL^2}+e^{-c/R^2}\right).
\tag{2.8}
\]

Indeed, \(h-16R\ge\alpha LR\) for all sufficiently large \(L\), and
the convolved Gaussian denominator is at most
\(2R^2+4t\le262R^2\).

The kinetic part of the \(8R\)-energy follows by integrating (2.8) over
the \(x_3\)-interval and using the \(O(R)\) invariant \(x_1\)-section.
For the gradient part choose \(\eta_R(z)\) with

\[
 \eta_R=1\quad(|z|\le8R),\qquad
 \operatorname{supp}\eta_R\subset\{|z|<16R\},
 \qquad |\eta_R''|\le CR^{-2}.
\tag{2.9}
\]

Multiplication of (2.5) by \(\eta_RF\) gives the exact identity

\[
 \frac12\frac d{dt}\int_{\mathbb T^2}\eta_RF^2
 +\int_{\mathbb T^2}\eta_R
 \left(|\partial_2F|^2+|\partial_zF|^2\right)
 =\frac12\int_{\mathbb T^2}\eta_R''F^2.
\tag{2.10}
\]

The shear transport vanishes because \(\eta_R\) is independent of
\(x_2\).  Integrating (2.10) over (2.1), applying (2.8) both to the
initial cutoff mass and to the right side, multiplying by the invariant
\(x_1\)-section, and dividing by \(8R\) proves (2.3). \(\square\)

### Lemma 2.2 — full buffered-energy upper bound

For the full velocity (1.4),

\[
 \boxed{
 \mathcal E(z_0,8R)
 \le C\left[
 B^2R^2+
 \mathfrak a^2R^2
 \left(e^{-d_EL^2}+e^{-c/R^2}\right)
 \right].}
\tag{2.11}
\]

**Proof.**  The packet row is Lemma 2.1.  The maximum principle gives
\(|\theta|\le1\), while the heat-kernel gradient bound on (2.1) gives
\(|\partial_3\theta|\le C/R\).  The kinetic and gradient rows of
\(B\theta\) are therefore each at most \(CB^2R^2\).  The two velocity
components are pointwise orthogonal, so their quadratic rows add exactly.
\(\square\)

At the selected amplitude (1.7),

\[
 d_E-c_\gamma
 =\frac{17018}{12998475}>0.
\tag{2.12}
\]

The periodic error is super-exponentially smaller.  Hence

\[
 \boxed{
 \mathcal E(z_0,8R)\le CB^2R^2,
 \qquad
 \mathcal E(z_0,8R)^{3/2}\le CB^3R^3.}
\tag{2.13}
\]

---

## 3. The gauge-fixed pressure row is redundant

Although the physical pressure is zero, the frozen local pressure gauge
does not vanish automatically.  This section retains it exactly.

Fix a radius \(\rho\), let

\[
 p_\rho^{\rm loc}
 =\mathcal R_i\mathcal R_j(\zeta_\rho u_i u_j),
 \qquad
 g_\rho(t)=(p_\rho^{\rm loc}(t))_{B_{2\rho}}.
\tag{3.1}
\]

Since \(\pi=0\), the frozen harmonic gauge satisfies

\[
 c_\rho=-g_\rho,
 \qquad
 \boxed{\pi-c_\rho=g_\rho.}
\tag{3.2}
\]

Thus the pressure row is spatially constant but generally nonzero.

### Lemma 3.1 — averaged local Riesz bound

For every time,

\[
 \boxed{
 |g_\rho(t)|
 \le C\rho^{-3}\int_{B_{4\rho}}|u(t,y)|^2\,dy.}
\tag{3.3}
\]

**Proof.**  Put

\[
 \Gamma(y)=\frac1{4\pi|y|},\qquad
 a=2\rho,qquad V_a=|B_a|,
\tag{3.4}
\]

and define the uniform-ball Newton potential

\[
 N_a(y)=\frac1{V_a}\int_{B_a}\Gamma(x-y)\,dx.
\tag{3.5}
\]

Newton's ball formula gives

\[
 D^2N_a(y)=
 \begin{cases}
  -I/(3V_a),&|y|<a,\\
  D^2\Gamma(y),&|y|>a.
 \end{cases}
\tag{3.6}
\]

Because \(a=2\rho<3\rho\) and \(\zeta_\rho=1\) on
\(B_{3\rho}\), averaging the Riesz split over \(B_a\) yields

\[
 \boxed{
 g_\rho
 =-\frac1{3V_a}\int_{B_a}|u|^2\,dy
 +\int_{B_{4\rho}\setminus B_a}
 D^2\Gamma(y):\bigl(\zeta_\rho u\otimes u\bigr)\,dy.}
\tag{3.7}
\]

The core term and the outer anisotropic term can cancel, so (3.7) is not
a pressure lower bound.  Since both kernels are bounded by \(C\rho^{-3}\)
on their respective regions, (3.3) follows. \(\square\)

### Lemma 3.2 — pressure payment is controlled by buffered energy

At the frozen denominator radius,

\[
 \boxed{
 \mathcal G_p(z_0,2R;1)
 \le C\mathcal E(z_0,8R)^{3/2}.}
\tag{3.8}
\]

**Proof.**  The exact annulus volume is

\[
 |A_k(\rho)|=\frac{28\pi}{3}8^k\rho^3.
\tag{3.9}
\]

Because \(g_\rho(t)\) is spatially constant, all annuli collapse to

\[
 \mathcal G_p(z_0,\rho;1)
 =M_\gamma\rho\int_{I_\rho}|g_\rho(t)|^{3/2}\,dt,
\tag{3.10}
\]

where

\[
 M_\gamma=\frac{28\pi}{3}
 \sum_{k\ge1}8^ke^{-4^{k-1}/32}<\infty.
\tag{3.11}
\]

Apply (3.3), use \(|I_\rho|=\rho^2\), and take the essential supremum:

\[
\begin{aligned}
 \mathcal G_p(z_0,\rho;1)
 &\le C\rho\int_{I_\rho}
 \left(\rho^{-3}\int_{B_{4\rho}}|u|^2\right)^{3/2}dt\\
 &\le C\left[
 \rho^{-1}\mathop{\rm ess\,sup}_{I_\rho}
 \int_{B_{4\rho}}|u|^2
 \right]^{3/2}\\
 &\le C\mathcal E(z_0,4\rho)^{3/2}.
\end{aligned}
\tag{3.12}
\]

Set \(\rho=2R\).  Then \(4\rho=8R\), proving (3.8). \(\square\)

Combining (2.13) and (3.8),

\[
 \boxed{\mathcal G_p(z_0,2R;1)\le CB^3R^3.}
\tag{3.13}
\]

---

## 4. Full-time two-packet occupation

This is the decisive new lemma.  All weights and all periodic copies are
those frozen in R0.74E.

Let

\[
 s(t)^2=h^2+Q(t)^2,
 \qquad I_{2R}=(61R^2,65R^2).
\tag{4.1}
\]

### Theorem 4.1 — sharp all-copy occupation

For each sign and every \(t\in I_{2R}\),

\[
 \boxed{
 \int_{\mathbb R^3}W_{2R}(x)
 |\widetilde F^\pm(t,x_2,x_3)|^3\,dx
 \le
 C\frac{R^6}{(R^2+s(t)^2)^{3/2}},}
\tag{4.2}
\]

and

\[
 \boxed{
 \int_{\mathbb R^3}L_{2R}(x)
 |\widetilde F^\pm(t,x_2,x_3)|^2\,dx
 \le
 C\frac{R^3}{(R^2+s(t)^2)^{3/2}}.}
\tag{4.3}
\]

No transition or periodic-copy error is required on the right side.

### 4.1 Reduction of the lifted weights

For \(x'=(x_2,x_3)\in\mathbb T^2\), define

\[
\begin{aligned}
 \omega_R(x')
 &=\sum_{n\in\mathbb Z^2}\int_{\mathbb R}
 W_{2R}(x_1,x'+2\pi n)\,dx_1,\\
 \ell_R(x')
 &=\sum_{n\in\mathbb Z^2}\int_{\mathbb R}
 L_{2R}(x_1,x'+2\pi n)\,dx_1.
\end{aligned}
\tag{4.4}
\]

Periodicity and Tonelli give exact unfolding identities.  The R0.74D
all-copy weight lemma gives

\[
 \boxed{
 \omega_R(x')\le
 C\frac{R^4}{(R^2+d_{\mathbb T^2}(x',0)^2)^{3/2}},
 \qquad
 \ell_R(x')\le
 C\frac{R}{(R^2+d_{\mathbb T^2}(x',0)^2)^{3/2}}.}
\tag{4.5}
\]

Thus no Euclidean annulus or torus copy is discarded.

### 4.2 Normalized periodic bridge

For the positive packet put

\[
 G(t,z,y)=F^+(t,Q(t)+z,h+y),
 \qquad T=R^2+t.
\tag{4.6}
\]

R0.74F proves

\[
 G(t,z,y)=R^3\mathbb E_y\left[
 \partial K_T(z+\mathfrak S_t^y)K_{R^2}(Y_t^y)
 \right].
\tag{4.7}
\]

The semigroup identity gives

\[
 \mathbb E_yK_{R^2}(Y_t^y)=K_T(y)>0.
\tag{4.8}
\]

Define the probability measure

\[
 d\mathbb P_{t,y}^{\rm br}
 =\frac{K_{R^2}(Y_t^y)}{K_T(y)}\,d\mathbb P_y.
\tag{4.9}
\]

Then, for \(p=2,3\), Jensen gives the correctly normalized estimate

\[
 \boxed{
 |G(t,z,y)|^p
 \le R^{3p}K_T(y)^p
 \mathbb E_{t,y}^{\rm br}
 |\partial K_T(z+\mathfrak S_t^y)|^p.}
\tag{4.10}
\]

### 4.3 One-sided path geometry

Let

\[
 a=\frac{\alpha^2}{260}=\frac{49}{14625}.
\tag{4.11}
\]

The plateau estimate is

\[
 0\le1-\theta(t,h)\le4e^{-aL^2}.
\tag{4.12}
\]

Since \(\theta\le1\), the displacement in (4.7) satisfies pathwise

\[
 \mathfrak S_t^y\ge-\delta,
 \qquad \delta=4Bte^{-aL^2}.
\tag{4.13}
\]

For all sufficiently large \(j\),

\[
 B\le\frac1{64R^2},
 \qquad B\ge\frac1{128R^2},
\tag{4.14}
\]

because \(q\le1/4\), \(\theta(t,h)\ge3/4\), and the calibration
interval has length \(64R^2\).  Therefore

\[
 \frac\delta R
 \le\frac{65}{16}
 e^{-(a-c_R)L^2}\longrightarrow0,
 \qquad
 a-c_R=\frac{211}{936000}>0.
\tag{4.15}
\]

Increase the base index so that \(\delta\le R<h\).  The opposite bound
\(|\theta(t,h)-\theta(t,h+y)|\le2\) gives

\[
 \mathfrak S_t^y\le2Bt\le\frac{65}{32}.
\tag{4.16}
\]

The calibrated path is increasing and satisfies

\[
 -\frac12\le Q(t)\le q,
 \qquad
 q=\frac{\sqrt{31}}{15}h<\frac h2.
\tag{4.17}
\]

For each bridge path define its spatial centre

\[
 c_{\mathfrak S}=(Q-\mathfrak S,h)\in\mathbb T^2.
\tag{4.18}
\]

If \(Q\ge-2h\), then \(|Q|\le2h\) and the fixed transverse coordinate
already gives

\[
 d_{\mathbb T^2}(c_{\mathfrak S},0)
 \ge h\ge s/\sqrt5.
\tag{4.19}
\]

If \(Q<-2h\), then (4.13) and \(\delta<h\) give

\[
 Q-\mathfrak S<0,
 \qquad |Q-\mathfrak S|\ge|Q|/2\ge s/\sqrt5.
\tag{4.20}
\]

There is no hidden wrap: (4.16)--(4.17) give

\[
 -\frac{81}{32}\le Q-\mathfrak S\le q+\delta,
 \qquad \frac{81}{32}<\pi.
\tag{4.21}
\]

Combining both cases,

\[
 \boxed{
 R^2+d_{\mathbb T^2}(c_{\mathfrak S},0)^2
 \ge\frac15(R^2+s(t)^2).}
\tag{4.22}
\]

This is the step that avoids the invalid use of the R0.74F pointwise
comparison error over the full time interval.

### 4.4 Periodic Peetre convolution

Set

\[
 \Phi_R(x)=
 \left(R^2+d_{\mathbb T^2}(x,0)^2\right)^{-3/2}.
\tag{4.23}
\]

The torus triangle inequality gives the periodic Peetre bound

\[
 \Phi_R(c+\xi)
 \le C\Phi_R(c)
 \left(1+\frac{d_{\mathbb T^2}(\xi,0)}R\right)^3.
\tag{4.24}
\]

The one-dimensional periodic heat kernels, uniformly for
\(T/R^2\in[62,66]\), satisfy

\[
 \int_{\mathbb T}K_T(y)^p
 \left(1+\frac{d_{\mathbb T}(y,0)}R\right)^3dy
 \le C_pR^{1-p},
\tag{4.25}
\]

and

\[
 \int_{\mathbb T}|\partial K_T(z)|^p
 \left(1+\frac{d_{\mathbb T}(z,0)}R\right)^3dz
 \le C_pR^{1-2p}.
\tag{4.26}
\]

These are periodic Gaussian moment bounds; their noncentral kernel copies
are part of the left sides.

Apply (4.24) with \(c=c_{\mathfrak S}\) and
\(\xi=(z+\mathfrak S,y)\).  Use (4.10), Tonelli, and the periodic
translation \(u=z+\mathfrak S\).  Equations (4.22), (4.25), and (4.26)
give

\[
 I_p^+(t)
 \le C a_p R^{3p}(R^2+s^2)^{-3/2}
 R^{1-p}R^{1-2p},
\tag{4.27}
\]

where

\[
 a_3=R^4,qquad a_2=R.
\tag{4.28}
\]

The exact common scaling is

\[
 R^{3p}R^{1-p}R^{1-2p}=R^2.
\tag{4.29}
\]

Thus (4.27) is (4.2) for \(p=3\) and (4.3) for \(p=2\).
Finally,

\[
 F^-(t,x_2,x_3)=-F^+(t,-x_2,-x_3),
\tag{4.30}
\]

and the weights are radial.  This proves Theorem 4.1 for both packets.
\(\square\)

---

## 5. The complete velocity cubic row

At \(\rho=2R\), the frozen cubic row is

\[
 \mathcal G_u
 =(2R)^{-2}\int_{I_{2R}}
 \int_{\mathbb R^3}W_{2R}|u|^3\,dx\,dt.
\tag{5.1}
\]

### Lemma 5.1 — shear and packet upper bounds

\[
 \boxed{
 \mathcal G_u
 \le C\left(B^3R^3+\mathfrak a^3R^4L^{-2}\right).}
\tag{5.2}
\]

**Proof.**  The exact weight mass satisfies

\[
 \int_{\mathbb R^3}W_{2R}(x)\,dx
 =C_W R^3,
 \qquad
 C_W<\infty.
\tag{5.3}
\]

Since \(|\theta|\le1\) and \(|I_{2R}|=4R^2\), the shear row is at most
\(CB^3R^3\).

For the packets, use

\[
 |F^++F^-|^3\le4(|F^+|^3+|F^-|^3)
\tag{5.4}
\]

and Theorem 4.1.  On \(I_{2R}\),

\[
 Q'(t)=B\theta(t,h)\ge\frac34B.
\tag{5.5}
\]

Hence

\[
\begin{aligned}
 \mathcal G_{u,F}
 &\le C\mathfrak a^3R^{-2}R^6B^{-1}
 \int_{\mathbb R}(h^2+R^2+q^2)^{-3/2}\,dq\\
 &\le C\mathfrak a^3R^4B^{-1}(h^2+R^2)^{-1}\\
 &\le C\mathfrak a^3R^4L^{-2}.
\end{aligned}
\tag{5.6}
\]

In the last step, \(B^{-1}\le128R^2\) and \(h=c_hLR\).
Finally,

\[
 (\mathfrak a^2F^2+B^2\theta^2)^{3/2}
 \le\sqrt2(\mathfrak a^3|F|^3+B^3|\theta|^3),
\tag{5.7}
\]

so no mixed cubic term remains. \(\square\)

At amplitude (1.7), the packet-to-background ratio is at most

\[
 C R\gamma^{-3/2}L^{-2}.
\tag{5.8}
\]

The exact exponent gap is

\[
 \boxed{
 c_R-\frac32c_\gamma
 =\frac1{320}-\frac4{1323}
 =\frac{43}{423360}>0.}
\tag{5.9}
\]

Therefore

\[
 \boxed{\mathcal G_u(z_0,2R;1)\le CB^3R^3.}
\tag{5.10}
\]

---

## 6. The complete algebraic harmonic row

At \(\rho=2R\),

\[
 \Lambda_{2R}(t)
 =\int_{\mathbb R^3}L_{2R}(x)|u(t,x)|^2\,dx,
\tag{6.1}
\]

\[
 \mathcal H_u=2R\int_{I_{2R}}\Lambda_{2R}(t)^{3/2}\,dt.
\tag{6.2}
\]

### Lemma 6.1 — shear and packet upper bounds

\[
 \boxed{
 \mathcal H_u
 \le C\left(B^3R^3+\mathfrak a^3R^4L^{-7/2}\right).}
\tag{6.3}
\]

**Proof.**  Direct annulus integration gives

\[
 \int_{\mathbb R^3}L_{2R}(x)\,dx=C_L<\infty.
\tag{6.4}
\]

Thus \(\Lambda_b(t)\le CB^2\), and the shear contribution to (6.2)
is at most \(CB^3R^3\).

Theorem 4.1 gives

\[
 \Lambda_F(t)
 \le C\mathfrak a^2
 \frac{R^3}{(h^2+Q(t)^2+R^2)^{3/2}}.
\tag{6.5}
\]

Using (5.5),

\[
\begin{aligned}
 \mathcal H_F
 &\le C\mathfrak a^3R^{11/2}B^{-1}
 \int_{\mathbb R}
 (h^2+R^2+q^2)^{-9/4}\,dq\\
 &\le C\mathfrak a^3R^{11/2}B^{-1}
 (h^2+R^2)^{-7/4}\\
 &\le C\mathfrak a^3R^4L^{-7/2}.
\end{aligned}
\tag{6.6}
\]

The pointwise orthogonality of the two velocity components and

\[
 (x+y)^{3/2}\le\sqrt2(x^{3/2}+y^{3/2})
\tag{6.7}
\]

separate the shear and packet \(\Lambda\)-rows.  Equation (5.4) with
power two separates the two passive packets. \(\square\)

At amplitude (1.7), the packet-to-background ratio is at most

\[
 C R\gamma^{-3/2}L^{-7/2},
\tag{6.8}
\]

which tends to zero by (5.9).  Hence

\[
 \boxed{\mathcal H_u(z_0,2R)\le CB^3R^3.}
\tag{6.9}
\]

---

## 7. Denominator closure and rejection of the frozen questions

The Version-M denominator is

\[
 P_R^M
 =\mathcal E(z_0,8R)^{3/2}
 +\mathcal G_u(z_0,2R;1)
 +\mathcal G_p(z_0,2R;1)
 +\mathcal H_u(z_0,2R).
\tag{7.1}
\]

Equations (2.13), (3.13), (5.10), and (6.9) give

\[
 \boxed{P_R^M\le CB^3R^3.}
\tag{7.2}
\]

For Version F, (1.5) implies \(w_R=v_R=u\), the affine acceleration
pressure is zero, and

\[
 \mathcal J_{\rm acc}^{F,R}=0.
\tag{7.3}
\]

Thus

\[
 \boxed{P_R^F=P_R^M\le CB^3R^3.}
\tag{7.4}
\]

R0.74F Theorem 6.2 proves, for every amplitude,

\[
 X_R^M=X_R^F
 \ge c\mathfrak a^2LR^2\gamma.
\tag{7.5}
\]

Substituting \(\mathfrak a=B\gamma^{-1/2}\) gives

\[
 \boxed{X_R^M=X_R^F\ge cB^2LR^2.}
\tag{7.6}
\]

Taking the \(2/3\) power of (7.2)--(7.4),

\[
 (P_R^M)^{2/3}=(P_R^F)^{2/3}
 \le CB^2R^2.
\tag{7.7}
\]

Equations (7.6)--(7.7) prove (1.12).  This completes the analytic
counterexample, subject to the frozen-audit promotion stated at the start
of this draft. \(\square\)

---

## 8. What this result does and does not establish

### Established by the analytic derivation

1. The \(8R\) buffered local packet energy has a squared-Gaussian
   exclusion gain, including the complete packet gradient row.
2. The gauge-fixed pressure row is controlled by the buffered local energy;
   physical pressure zero is not incorrectly identified with gauge row zero.
3. The two packets satisfy full-time, all-annulus, all-periodic-copy
   \(p=2,3\) occupation bounds.
4. The complete \(G_u\) and \(H_u\) packet rows are smaller than the shear
   floor at the selected amplitude.
5. The explicit smooth family makes both frozen proposed ratios diverge.

### Consequence for the research route

The particular frozen right side in R0.74E is too weak.  Any replacement
that seeks a valid arbitrary-solution estimate must add information that
detects this travelling two-packet mechanism.  Merely changing between the
moved-only and mean-subtracted frames does not help, because inversion
symmetry makes the trajectory, local velocity, and acceleration vanish
simultaneously on this family.

This is a route-elimination result.  It does not imply that every local
frame estimate fails, and it does not identify a sufficient replacement.

### Still open

1. a new scale-invariant denominator that pays this exact family without
   becoming tautological;
2. an arbitrary-solution theorem for such a corrected denominator;
3. any epsilon-regularity, continuation, singularity-exclusion, or global
   smoothness consequence;
4. every claim concerning the Navier--Stokes Millennium problem.

**NOT CLAY.**

---

## 9. Verification boundary before freeze

Before promotion from this draft to a frozen theorem, the following are
required:

1. a same-source independent audit of Sections 2--3;
2. a separate same-source audit of the normalized bridge, path geometry,
   Peetre convolution, and Sections 5--7;
3. an exact-arithmetic certificate for every rational exponent and finite
   geometry gate used above;
4. a journal figure package showing the target, background floor, packet
   \(G_u\), and packet \(H_u\) exponents from exact source data;
5. a freeze manifest binding all source, audit, certificate, and figure
   hashes.

No finite certificate can prove the heat-kernel, Riesz-transform, bridge,
or asymptotic arguments.  Those remain analytic proof obligations.

