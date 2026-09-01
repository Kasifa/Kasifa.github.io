# R0.74I — suitable-weak moving-tube bridge and logarithmic payment obstruction

## Status and scope

R0.74H proves a two-regime exterior-size estimate for smooth periodic
solutions and identifies the positive cumulative collar flux
\(\mathfrak C_R^\alpha\) as the missing row in the failed pure
\(P^{2/3}\) extrapolation.  It does not pass that estimate to suitable weak
solutions and does not obtain an epsilon-regularity criterion.

This note makes two separate advances.

1. It passes the Version-M two-regime estimate to periodic suitable weak
   solutions by using the local energy inequality with the terminally
   anchored moving test function.
2. It proves a moving-tube epsilon criterion: sufficiently small Version-M
   moving local energy confines the mollified path, gives a small fixed-
   cylinder \(L^3\) velocity quantity, and hence implies regularity at the
   terminal point.

The exact R0.74F--H two-packet family also gives a negative boundary.  Any
universal scalar payment below

\[
 P^{2/3}\sqrt{1+\log_+ P},
 \qquad \log_+P=\log\max\{P,1\},
\]

fails along that family.  The square-root logarithmic endpoint is only the
first exponent not rejected by this screen; no endpoint upper bound is
proved here.

Current status:

    FROZEN / INDEPENDENT ANALYTIC PASS /
    CERTIFICATE 36/36 + INDEPENDENT 36/36 PASS /
    BOUNDED LITERATURE PASS / FIGURE 82/82 PASS

This note does not prove that the moving payment is small at every point or
scale.  It does not prove a Version-F weak extension, an endpoint
logarithmic upper bound, scale propagation, global regularity, or the
Millennium problem.  **NOT CLAY.**

The frozen R0.74H research commit is

    5cd31fd8cde1574f02d9e9af3417686d2a8f8d9c.

---

## 1. Suitable weak setting and the mollified terminal path

Work on

\[
 \mathbb T^3=(-\pi,\pi]^3,
 \qquad I_\rho=(t_0-\rho^2,t_0),
 \qquad 0<R<\frac\pi{16},
\tag{1.1}
\]

with \(\overline I_{8R}\Subset(0,T)\).  Let \((u,p)\) be a periodic
suitable weak solution of the unforced three-dimensional incompressible
Navier--Stokes equations.  Thus, locally in time,

\[
 u\in L_t^\infty L_x^2\cap L_t^2H_x^1,
 \qquad p\in L^{3/2},
\tag{1.2}
\]

the equations hold distributionally, and the standard local energy
inequality holds for every nonnegative smooth periodic test function.

Use exactly the even radial R0.74E mollifier \(\varphi_R^{\rm per}\) and
write

\[
 u_R=\varphi_R^{\rm per}*u.
\tag{1.3}
\]

Choose the standard jointly measurable periodic representative of the spatial
convolution.  For almost every time,

\[
 \|u_R(t)\|_{L^\infty}
 \le C_\varphi R^{-3/2}\|u(t)\|_{L^2},
 \qquad
 \|\nabla u_R(t)\|_{L^\infty}
 \le C_\varphi R^{-5/2}\|u(t)\|_{L^2}.
\tag{1.4}
\]

The vector field is therefore Borel measurable in time, bounded and spatially
Lipschitz, with an essentially bounded time-dependent Lipschitz coefficient.
Extend it periodically to \(\mathbb R^3\).  The terminal-value Caratheodory
problem for a Euclidean lift

\[
 \boxed{
 \dot X_R(t)=u_R(t,X_R(t)),
 \qquad X_R(t_0)=x_0}
\tag{1.5}
\]

has a unique absolutely continuous solution on \(\overline I_{8R}\); different
lifts give the same path on the torus.  In fact \(X_R\in W^{1,\infty}\) at
every fixed \(R>0\).
Define

\[
 v_R(t,y)=u(t,y+X_R(t)),
 \qquad \pi_R(t,y)=p(t,y+X_R(t)),
 \qquad a_R=\dot X_R.
\tag{1.6}
\]

All Version-M quantities below are the exact R0.74E--H quantities, now
interpreted through essential suprema and weak derivatives.  In particular,

\[
\begin{aligned}
 \mathcal E_R
 :=\mathcal E^{M,R}(z_0,8R)
 &=\frac1{8R}\mathop{\rm ess\,sup}_{I_{8R}}
   \int_{B_{8R}}|v_R|^2\\
 &\quad+\frac1{8R}\int_{I_{8R}}\int_{B_{8R}}|\nabla v_R|^2,
\end{aligned}
\tag{1.7}
\]

\[
 P_R^M=\mathcal E_R^{3/2}
       +\mathcal A_{\rm ext}^{M,R}(z_0,2R;1),
 \qquad
 X_R^M=\mathcal U_{\rm ext}^{\infty,M,R}
       +\mathcal D_{\rm ext}^{M,R}.
\tag{1.8}
\]

The pressure split, gauges, shell weights \(\gamma_j\), padded cutoffs
\(\psi_j^R\), and finite periodized weights \(\Theta_{R,N}\) are unchanged.

---

## 2. The moving local-energy test survives at weak regularity

### Lemma 2.1 — admissibility of the terminally moving test

Let \(\eta_R\) be the frozen R0.74H time cutoff.  For every finite \(N\),
the local energy inequality may be tested, after smooth approximation, with

\[
 \phi_N(t,x)=\eta_R(t)\Theta_{R,N}(x-X_R(t)).
\tag{2.1}
\]

For almost every \(\tau\in I_R\), the result is

\[
\begin{aligned}
 &\frac1{2R}\int_{\mathbb T^3}\Theta_{R,N}|v_R(\tau)|^2
 +\frac1R\int_{s_R}^{\tau}\eta_R
       \int_{\mathbb T^3}\Theta_{R,N}|\nabla v_R|^2\\
 &\le
 \frac1{2R}\int_{s_R}^{\tau}\eta_R'
       \int_{\mathbb T^3}\Theta_{R,N}|v_R|^2
 +\frac1{2R}\int_{s_R}^{\tau}\eta_R
       \int_{\mathbb T^3}|v_R|^2\Delta\Theta_{R,N}
 +\mathfrak F_{R,N}^M(\tau),
\end{aligned}
\tag{2.2}
\]

where

\[
\begin{aligned}
 \mathfrak F_{R,N}^M(\tau)
 =\frac1R\int_{s_R}^{\tau}\eta_R(t)
 \int_{\mathbb T^3}
 \left[
  \frac12|v_R|^2(v_R-a_R)
  +(\pi_R-c_{2R}^{M,R}(t))v_R
 \right]\cdot\nabla\Theta_{R,N}.
\end{aligned}
\tag{2.3}
\]

**Proof.**  Since \(X_R\in W^{1,\infty}\), (2.1) is a nonnegative periodic
test in \(W_t^{1,\infty}C_x^2\), with the almost-everywhere time derivative

\[
 \partial_t\phi_N
 =\eta_R'\Theta_{R,N}
  -\eta_R a_R\cdot\nabla\Theta_{R,N}.
\tag{2.4}
\]

Approximate its Euclidean lift in \(W^{1,1}\) by smooth paths, preserve the
nonnegativity of the composed test, and approximate the terminal time from
below through good times of the local energy inequality.  The composed tests
converge uniformly, their spatial derivatives converge uniformly, and their
time derivatives converge in \(L_t^1L_x^\infty\).  The local-energy terms pass
to the limit because

\[
 |u|^2\in L_t^\infty L_x^1,
 \qquad u\in L^3_{t,x},
 \qquad p\in L^{3/2}_{t,x},
\tag{2.4a}
\]

on the finite cylinder; in particular \(pu\in L^1\).  The second term in (2.4)
combines with the physical velocity flux to replace \(v_R\) by
\(v_R-a_R\) in the kinetic part of (2.3).  A time-dependent pressure gauge
contributes zero because \(v_R\) is divergence free.  This is (2.2).
\(\square\)

### Lemma 2.2 — finite-shell limit and payment bounds

The finite-shell limits used in R0.74H remain valid, and

\[
 \mathfrak Q_R^M\le C(P_R^M)^{2/3},
 \qquad
 \sup_{\tau\in I_R}|\mathfrak F_R^M(\tau)|\le CP_R^M.
\tag{2.5}
\]

**Proof.**  The shell convergence is geometric and uses the same
super-Gaussian \(C^2\) majorant as R0.74H.  More precisely, the first estimate
is the weak-integrability version of R0.74H (4.4)--(4.8): weighted Holder,
the shell-volume sum, the radius shift, and the local and exterior
velocity-cubic ledger give the \((P_R^M)^{2/3}\) row.  The second estimate is
the Version-M case of R0.74H (6.3)--(6.6) and uses

\[
 |\pi_R-c|\,|v_R|
 \le C\bigl(|\pi_R-c|^{3/2}+|v_R|^3\bigr),
\tag{2.6}
\]

the distributional pressure split, harmonic estimates, and the residual
drift bound.  More explicitly, the local-cubic and shell-cubic rows are
bounded by the corresponding nonnegative velocity ledger, while the
residual-drift row uses that ledger together with the identity
\(a_R=\varphi_R*v_R(0)\); the pressure row uses
\(p\in L^{3/2}\), Calderon--Zygmund applied to
\(v_R\otimes v_R\), and harmonic interior estimates.  No time derivative of
\(u\), \(a_R\), or the pressure is used.  Thus these arguments require only
the integrability in (1.2), not pointwise differentiability of \(u\).  The
local energy inequality changes the identity into the favorable inequality
(2.2); it does not change either upper bound. \(\square\)

### Theorem 2.3 — Version-M weak two-regime closure

Every periodic suitable weak solution in the scope of Section 1 satisfies

\[
 \boxed{
 X_R^M\le C\bigl[(P_R^M)^{2/3}+P_R^M\bigr].}
\tag{2.7}
\]

Consequently,

\[
 \boxed{
 P_R^M\le1
 \quad\Longrightarrow\quad
 X_R^M\le C(P_R^M)^{2/3}.}
\tag{2.8}
\]

**Proof.**  Pass \(N\to\infty\) in (2.2).  The pointwise lower bound for
the weight controls the exterior terminal energy and dissipation.  For the
energy bound, drop the nonnegative dissipation and take the essential
supremum over good \(\tau\in I_R\).  For the full dissipation, choose good
times \(\tau_k\uparrow t_0\); the time-integrated right-hand terms and
\(\mathfrak F_R^M(\tau_k)\) converge because their integrands are in
\(L^1_t\), while the terminal energy is nonnegative and may be dropped.
Adding the two estimates gives (2.7).  Equation (2.8) follows from
\(P\le P^{2/3}\) for \(0\le P\le1\).
\(\square\)

This theorem is a genuine weak-solution extension of the Version-M size
estimate.  It is not yet a regularity statement because it does not force
\(P_R^M\) to be small.

---

## 3. A moving-tube epsilon-regularity bridge

### Lemma 3.1 — small moving energy confines the path

For almost every \(t\in I_{8R}\),

\[
 \boxed{
 |a_R(t)|\le C_XR^{-1}\mathcal E_R^{1/2}.}
\tag{3.1}
\]

Hence, for every \(t\in I_{R/2}\),

\[
 \boxed{
 |X_R(t)-x_0|\le \frac{C_X}{4}R\mathcal E_R^{1/2}.}
\tag{3.2}
\]

**Proof.**  The mollifier is supported in \(B_R\).  Cauchy--Schwarz and
(1.7) give

\[
\begin{aligned}
 |a_R(t)|
 &\le \|\varphi_R\|_{L^2}
       \left(\int_{B_R}|v_R(t,y)|^2dy\right)^{1/2}\\
 &\le C_\varphi R^{-3/2}(8R\mathcal E_R)^{1/2}.
\end{aligned}
\tag{3.3}
\]

This is (3.1).  Integrate the almost-everywhere bound along the absolutely
continuous path from \(t\) to \(t_0\).  The time length of \(I_{R/2}\) is
\(R^2/4\), which gives (3.2). \(\square\)

Choose \(\varepsilon_{\rm geom}>0\), depending only on the frozen
mollifier, so that

\[
 \mathcal E_R\le\varepsilon_{\rm geom}
 \quad\Longrightarrow\quad
 |X_R(t)-x_0|\le\frac R2
 \quad(t\in I_{R/2}).
\tag{3.4}
\]

Here and in the following inclusion, distances and balls are read in the
Euclidean lift anchored by \(X_R(t_0)=x_0\).  The restriction
\(R<\pi/16\) prevents ambiguity when the result is projected to the torus.
Thus

\[
 B_{R/2}(x_0)\subset X_R(t)+B_R
 \qquad(t\in I_{R/2}).
\tag{3.5}
\]

### Lemma 3.2 — moving energy gives fixed-cylinder cubic smallness

There is a constant \(C_I\), depending only on the fixed radius ratios,
such that

\[
 \boxed{
 \left(\frac R2\right)^{-2}
 \int_{I_{R/2}}\int_{B_{R/2}(x_0)}|u|^3
 \le C_I\mathcal E_R^{3/2}}
\tag{3.6}
\]

whenever (3.4) holds.

**Proof.**  Apply the standard local interpolation inequality to the
function \(v_R\) on the fixed \(y\)-cylinder \(B_{8R}\times I_{8R}\),
with inner radius \(R\).  This step is purely functional and does not require
\(v_R\) to solve the canonical fixed-frame equation.  If \(A(8R)\) and
\(E(8R)\) denote its scaled kinetic-energy and dissipation terms, then
\(A(8R)+E(8R)=\mathcal E_R\), and the scale-explicit inequality gives

\[
 R^{-2}\int_{I_R}\int_{B_R}|v_R|^3
 \le C\left(
  A(8R)^{3/4}E(8R)^{3/4}
  +A(8R)^{3/2}
 \right)
 \le C\mathcal E_R^{3/2}.
\tag{3.7}
\]

Use (3.5), restrict the time interval, and account for the factor
\((R/2)^{-2}=4R^{-2}\). \(\square\)

### Theorem 3.3 — suitable-weak moving-tube epsilon criterion

There exists \(\varepsilon_{\rm tube}>0\), depending only on the frozen
mollifier and universal one-scale regularity constants, such that

\[
 \boxed{
 \mathcal E^{M,R}(z_0,8R)\le\varepsilon_{\rm tube}
 \quad\Longrightarrow\quad
 z_0\text{ is a regular point of }u.}
\tag{3.8}
\]

In particular, there is \(\varepsilon_P>0\) such that

\[
 \boxed{
 P_R^M\le\varepsilon_P
 \quad\Longrightarrow\quad
 z_0\text{ is regular}.}
\tag{3.9}
\]

**Proof.**  Let \(\varepsilon_{L^3}>0\) be the universal constant in a
one-scale velocity-only epsilon-regularity theorem for suitable weak
solutions.  Choose

\[
 \varepsilon_{\rm tube}
 \le\min\left\{
  \varepsilon_{\rm geom},
  (\varepsilon_{L^3}/C_I)^{2/3}
 \right\}.
\tag{3.10}
\]

Then (3.6) gives the scaled one-cylinder condition

\[
 (R/2)^{-2}\int_{Q_{R/2}(z_0)}|u|^3
 \le\varepsilon_{L^3}.
\tag{3.11}
\]

Indeed, with \(r=R/2\), the Navier--Stokes rescaling

\[
 U(s,\xi)=r\,u(t_0+r^2s,x_0+r\xi),
 \qquad
 \Pi(s,\xi)=r^2p(t_0+r^2s,x_0+r\xi)
\tag{3.11a}
\]

is again a suitable weak solution on the rescaled cylinder and satisfies

\[
 \int_{Q_1}|U|^3\,d\xi\,ds
 =r^{-2}\int_{Q_r(z_0)}|u|^3\,dx\,dt.
\tag{3.11b}
\]

The velocity-only criterion therefore gives boundedness in a smaller
cylinder and regularity at \(z_0\).  Finally, every row of
\(\mathcal A_{\rm ext}^{M,R}\) is nonnegative, so
\(\mathcal E_R^{3/2}\le P_R^M\).  Thus (3.9) follows by taking
\(\varepsilon_P\le\varepsilon_{\rm tube}^{3/2}\). \(\square\)

The theorem supplies a rigorous epsilon gate.  It does not show that its
hypothesis holds at a possible singular point.

---

## 4. The two-packet family forces a square-root logarithmic frontier

Return to the exact R0.74F--H family and write

\[
 P_j=P_{R_j}^M=P_{R_j}^F,
 \quad X_j=X_{R_j}^M=X_{R_j}^F,
 \quad \mathfrak C_j=\mathfrak C_{R_j}^M=\mathfrak C_{R_j}^F.
\tag{4.1}
\]

Its parameters satisfy

\[
 L_j=\frac{63}{32}2^j,
 \qquad R_j=e^{-\rho L_j^2},
 \qquad \rho=\frac1{320},
 \qquad b_j:=B_jR_j^2\longrightarrow\frac1{128}.
\tag{4.2}
\]

Therefore, after increasing the index if necessary, one may fix

\[
 0<b_-\le b_j\le b_+<\infty;
 \quad\text{for example }b_-=\frac1{256},\ b_+=\frac1{64}.
\tag{4.3}
\]

The frozen theorems provide constants \(A,a_P,a_X,a_C>0\) such that

\[
 P_j\le AB_j^3R_j^3,
 \qquad P_j\ge a_PB_j^2L_jR_j^2,
\tag{4.4}
\]

\[
 X_j\ge a_XB_j^2L_jR_j^2,
 \qquad \mathfrak C_j\ge a_CB_j^2L_jR_j^2.
\tag{4.5}
\]

The lower payment bound is used only to prove \(P_j\to\infty\) and the
lower logarithmic window.  The upper payment bound is the one used below
to upper-bound powers of \(P_j\).

Since \(B_j=b_jR_j^{-2}\),

\[
 B_j^3R_j^3=b_j^3e^{3\rho L_j^2},
 \qquad
 B_j^2L_jR_j^2=b_j^2L_je^{2\rho L_j^2}.
\tag{4.6}
\]

It follows that

\[
 \boxed{
 2\rho
 \le\liminf_{j\to\infty}\frac{\log P_j}{L_j^2}
 \le\limsup_{j\to\infty}\frac{\log P_j}{L_j^2}
 \le3\rho.}
\tag{4.7}
\]

### Theorem 4.1 — sub-frontier scalar payments fail

For \(Y_j=X_j\) and for \(Y_j=\mathfrak C_j\),

\[
 \boxed{
 \liminf_{j\to\infty}
 \frac{Y_j}{P_j^{2/3}\sqrt{1+\log_+ P_j}}>0.}
\tag{4.8}
\]

Consequently, if a function \(\Phi:[0,\infty)\to[0,\infty)\) satisfies

\[
 \Phi(p)=o\!\left(p^{2/3}\sqrt{1+\log_+ p}\right)
 \qquad(p\to\infty),
\tag{4.9}
\]

then no constant \(K>0\), independent of the solution and scale, can make

\[
 X_R^\alpha\le K\Phi(P_R^\alpha)
 \quad\text{or}\quad
 \mathfrak C_R^\alpha\le K\Phi(P_R^\alpha),
 \qquad \alpha\in\{M,F\},
\tag{4.10}
\]

valid for all smooth periodic solutions.

**Proof.**  Fix \(\delta>0\).  Equations (4.4)--(4.6) give, for all
sufficiently large \(j\),

\[
 1+\log_+P_j\le(3\rho+\delta)L_j^2,
 \qquad
 P_j^{2/3}\le A^{2/3}B_j^2R_j^2.
\tag{4.11}
\]

Multiplying these two estimates yields

\[
 P_j^{2/3}\sqrt{1+\log_+P_j}
 \le A^{2/3}\sqrt{3\rho+\delta}\,
 B_j^2L_jR_j^2.
\tag{4.12}
\]

Use either lower bound in (4.5), then let \(\delta\downarrow0\).  This
proves (4.8).  Since \(P_j\to\infty\), (4.9) contradicts either estimate
in (4.10) along the realized sequence. \(\square\)

### Corollary 4.2 — the logarithmic exponent screen

For every fixed \(\gamma<1/2\), no uniform estimate of either form

\[
 X_R^\alpha\le K (P_R^\alpha)^{2/3}
 (1+\log_+P_R^\alpha)^\gamma,
 \qquad
 \mathfrak C_R^\alpha\le K (P_R^\alpha)^{2/3}
 (1+\log_+P_R^\alpha)^\gamma,
 \qquad \alpha\in\{M,F\},
\tag{4.13}
\]

can hold.  Indeed,

\[
 \frac{Y_j}{P_j^{2/3}(1+\log_+P_j)^\gamma}
 \ge c(1+\log_+P_j)^{1/2-\gamma}\longrightarrow\infty.
\tag{4.14}
\]

At \(\gamma=1/2\), this proof gives only a positive lower ratio, not a
divergent one.  It neither proves nor refutes a universal endpoint upper
bound.  To see what such an upper bound would require, suppose for either
\(Y=X\) or \(Y=\mathfrak C\) that

\[
 Y_R^\alpha\le K(P_R^\alpha)^{2/3}
 \sqrt{1+\log_+P_R^\alpha}.
\tag{4.15}
\]

On the explicit family, (4.5), (4.11), and (4.15) give

\[
 a_YB_j^2L_jR_j^2
 \le Y_j\le CKL_jP_j^{2/3}.
\tag{4.16}
\]

Cancel \(L_j\) and raise to the \(3/2\) power to obtain

\[
 \boxed{P_j\ge cK^{-3/2}B_j^3R_j^3.}
\tag{4.17}
\]

This is the currently unproved matching payment lower bound.  Equation
(4.17) is only a consequence of the hypothetical endpoint upper estimate;
it is not a theorem of the frozen family.

The values \(P_j\) form a highly lacunary sequence.  Indeed,
\(L_{j+1}=2L_j\), and the lower bound for \(P_{j+1}\) together with the upper
bound for \(P_j\) yields

\[
 \log\frac{P_{j+1}}{P_j}
 \ge 2\rho L_{j+1}^2-3\rho L_j^2
      +\log L_{j+1}+O(1)
 =5\rho L_j^2+\log L_{j+1}+O(1)\longrightarrow\infty.
\tag{4.18}
\]

Thus \(P_{j+1}/P_j\to\infty\).  Without additional regularity assumptions
on \(\Phi\), Theorem 4.1 constrains \(\Phi\) along that realized sequence;
it is not a pointwise lower bound at every large real argument.

---

## 5. Literature boundary

The weak formulation and local energy inequality used above are standard
in the suitable-weak theory initiated by Caffarelli, Kohn, and Nirenberg:

- L. Caffarelli, R. Kohn, and L. Nirenberg,
  [Partial regularity of suitable weak solutions of the Navier--Stokes
  equations](https://doi.org/10.1002/cpa.3160350604),
  *Communications on Pure and Applied Mathematics* 35 (1982), 771--831.

The fixed-cylinder interpolation inequality and several one-scale local
energy bounds are recorded explicitly by Guevara and Phuc:

- C. Guevara and N. C. Phuc,
  [Local energy bounds and epsilon-regularity criteria for the 3D
  Navier--Stokes system](https://doi.org/10.1007/s00526-017-1151-7),
  *Calculus of Variations and Partial Differential Equations* 56 (2017),
  Article 68; [arXiv:1702.00449](https://arxiv.org/abs/1702.00449).

For Theorem 3.3, one may use Theorem 1.1 of Wang, Wu, and Zhou with their
velocity exponent \(5/2+\delta\) specialized to \(\delta=1/2\):

- Y. Wang, G. Wu, and D. Zhou,
  [A regularity criterion at one scale without pressure for suitable weak
  solutions to the Navier--Stokes
  equations](https://doi.org/10.1016/j.jde.2019.05.003),
  *Journal of Differential Equations* 267 (2019), 4673--4704;
  [arXiv:1811.09927](https://arxiv.org/abs/1811.09927).

Mollified trajectories and their tubular, or skewed, cylinders are direct
precedents in the work of Yang and of Vasseur--Yang:

- J. Yang,
  [Construction of maximal functions associated with skewed cylinders
  generated by incompressible flows and
  applications](https://doi.org/10.4171/AIHPC/20),
  *Annales de l'Institut Henri Poincare C* 39 (2022), 793--818;
  [arXiv:2008.05588](https://arxiv.org/abs/2008.05588);
- A. Vasseur and J. Yang,
  [Second derivatives estimate of suitable solutions to the 3D
  Navier--Stokes equations](https://doi.org/10.1007/s00205-021-01661-4),
  *Archive for Rational Mechanics and Analysis* 241 (2021), 683--727;
  [arXiv:2009.14291](https://arxiv.org/abs/2009.14291).

More specifically, the mollified flow is anchored at a reference time, and
Vasseur--Yang prescribe

\[
 \dot X(s)=u_\varepsilon(s,X(s)),\qquad X(t)=x,
\]

before using a one-sided backward skewed cylinder.  Reference-time, or
terminal, anchoring and backward skewness are therefore established devices,
not novelty-bearing features of this note.  What differs in Section 3 is the
full analytic combination: the exact moving local-energy test and its weak
passage, the Version-M payment, the positive collar flux, and the resulting
moving-to-fixed epsilon implication.

Logarithmic improvements of global Prodi--Serrin conditions exist, for
example the \(|u|^5/\log(1+|u|)\) condition of Chan and Vasseur:

- C. H. Chan and A. Vasseur,
  [Log improvement of the Prodi--Serrin criteria for Navier--Stokes
  equations](https://doi.org/10.4310/maa.2007.v14.n2.a5),
  *Methods and Applications of Analysis* 14 (2007), 197--212;
  [arXiv:0705.3659](https://arxiv.org/abs/0705.3659).

The other screened logarithmic mechanisms also use different observables:

- S. Montgomery-Smith,
  [Conditions implying regularity of the three dimensional Navier--Stokes
  equation](https://doi.org/10.1007/s10492-005-0032-0),
  *Applications of Mathematics* 50 (2005), 451--464;
  [arXiv:math/0301207](https://arxiv.org/abs/math/0301207), treats a
  global-in-space critical Prodi--Serrin-type hypothesis on a finite interval
  \([0,T]\), weakened by a logarithmic denominator.
- J.-Y. Chemin,
  [Non linear equivalence of some scaling invariant norms for solutions of
  incompressible Navier--Stokes
  equations](https://doi.org/10.3934/cam.2025038),
  *Communications in Analysis and Mechanics* 17 (2025), 944--954, proves a
  genuine \(\sqrt{\log}\) comparison in Theorem 1.3 between
  \[
   N_T(u)=\sup_{I\subset[0,T)}|I|^{-1/2}
      \int_I\|\nabla u(t)\|_{L^2}^2\,dt
  \]
  and \(\|u\|_{L_t^\infty\dot B^{1/2}_{2,\infty}}\).
- T. Ogawa and Y. Taniuchi,
  [The limiting uniqueness criterion by vorticity for Navier--Stokes
  equations in Besov
  spaces](https://doi.org/10.2748/tmj/1113246381),
  *Tohoku Mathematical Journal* 56 (2004), 65--77, obtain logarithmic exponent
  \(1/\nu-1/\rho\) in Theorem 3.1; the choice
  \((\nu,\rho)=(1,2)\) gives \(1/2\) in a global Besov/Orlicz vorticity
  uniqueness argument.
- Z. Lei and X. Ren,
  [Quantitative partial regularity of the Navier--Stokes equations and
  applications](https://doi.org/10.1016/j.aim.2024.109654),
  *Advances in Mathematics* 445 (2024), Article 109654;
  [arXiv:2210.01783](https://arxiv.org/abs/2210.01783), place their logarithm
  in a multiscale singular-set gauge.
- T. Tao,
  [Quantitative bounds for critically bounded solutions to the Navier--Stokes
  equations](https://doi.org/10.1090/pspum/104/01874), in
  *Nine Mathematical Challenges---An Elucidation*, *Proceedings of Symposia in
  Pure Mathematics* 104 (AMS, 2021), 149--193;
  [arXiv:1908.04958](https://arxiv.org/abs/1908.04958), uses iterated
  logarithms in quantitative critical-norm and possible-blow-up estimates.

None of these is the local scalar payment frontier in Section 4: even the
matching exponent \(1/2\) in Chemin or Ogawa--Taniuchi acts on a different
functional and has a different logical role.  The bounded primary-source
screen found no statement of
\(Y_R\lesssim P_R^{2/3}\sqrt{1+\log_+P_R}\) for the R0.74I observables, but
that is only a finite non-hit.  No novelty or priority conclusion is drawn.

---

## 6. What is proved, and what remains open

The completed analytic audits establish that this note proves:

1. the Version-M two-regime estimate at suitable-weak regularity;
2. a moving-tube local-energy epsilon criterion and its small-\(P_R^M\)
   corollary;
3. a square-root logarithmic necessary frontier along the exact two-packet
   family; and
4. failure of every fixed logarithmic power below \(1/2\).

It does not prove:

1. the Version-F suitable-weak extension;
2. that \(P_R^M\) or \(\mathcal E_R\) is small at a possible singular point;
3. any endpoint upper bound at logarithmic exponent \(1/2\);
4. propagation of smallness from one scale to all smaller scales;
5. exclusion of all singular points or global smoothness; or
6. novelty or publication priority.

The route decision is therefore precise.  A subcritical scalar repair of
the R0.74H collar flux is not available.  Version M nevertheless has a
rigorous weak-solution epsilon gate because small moving local energy
confines the path and enters an established fixed-cylinder criterion.  The
remaining global problem is to derive that smallness, or an equivalent
scale-propagating condition, from the Navier--Stokes dynamics.

**NOT CLAY.**

---

## 7. Verification record

The frozen record separates the following evidence classes.

1. `r074i_weak_extension_independent_audit.md` independently checks the
   Caratheodory representative, the moving-test approximation, every sign and
   factor in the local energy inequality, the pressure gauge, the weak
   finite-shell passage, and Theorem 2.3.
2. `r074i_epsilon_log_independent_audit.md` records the adversarial
   pre-promotion review of Sections 3--4.  Its four conditional repairs
   (the \(\log_+\) convention, the endpoint derivation, lacunarity, and the
   M/F labels) are all incorporated here; the final-source rebind checks the
   repaired text.
3. The exact producer and an independent Ruby `Rational` reconstruction both
   return 36/36, with 269 terminal fields compared and zero mismatches.  This
   is finite exponent algebra only, not a PDE proof.
4. `r074i_report-source.md`, `r074i_primary_literature_boundary.md`, and the
   immutable independent literature audit record the component-level
   collisions and the bounded observable-level non-hit.  They do not establish
   novelty or priority.
5. The exact-source journal figure package
   `fig-r074i-moving-tube-log-screen` passes 82/82 deterministic checks.  Its
   SVG, vector PDF, 600-dpi PNG, final-size, grayscale, and independently
   rasterized PDF surfaces were inspected.  It is a formal implication and
   exponent diagram, not DNS or simulation.
6. `r074i_final_source_rebind_audit.md` is the separate post-promotion audit
   that binds this immutable source, the repaired literature ledger, the
   certificate, gap matrix, and sealed figure package.  The freeze manifest
   records the resulting SHA-256 values.
