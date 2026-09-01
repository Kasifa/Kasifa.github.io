# R0.74A — localized size lemma for the mixed heat covariance

**Prepared date:** 2026-09-01

**Status:** `PROVED_SIZE_LEMMA + FINITE_DECLARED_TAILS + OPEN_ABSORPTION`

**Claim class:** positive-scale analytic estimate; no regularity criterion

**Domain:** the normalized torus
\(\mathbb T^3=(\mathbb R/2\pi\mathbb Z)^3\), with its Euclidean lift

**Dependencies:** `r073x_problem_freeze.md`,
`r073x_exterior_tail_freeze.md`, and
`r073z_finiteness_obstruction_and_repair.md`

This note proves a localized upper bound for

\[
 \mathcal K_D^\square(z_0,R;\theta)
 =\frac{\nu}{R^2}\int_{I_R^\square}\int_0^{\theta R^2}
   \int_{B_R}D_s\sqrt{k_s}\,dx\,ds\,dt.
\tag{0.1}
\]

The estimate separates inputs to the Gaussian filter into a local core and
lifted exterior annuli.  The core--core term is controlled by the frozen
clock-matched local energy.  The other three terms require one new quadratic
Gaussian tail--an annular velocity energy with an essential time supremum--
together with the favorable annular gradient-energy tail
\(\mathcal D_{\rm ext}^{\square}\) already frozen in R0.73X.

The older exterior functional from R0.73X contains \(|u|^3\),
\(|p|^{3/2}\), and an algebraically weighted \(|u|^2\) pressure tail.  It
does not contain exterior gradient energy.  It is therefore not, by itself,
a right-hand side for the estimate proved here.

This is only a size lemma.  It does not show that any tail is small,
absorbable, compact, or determined by a smaller cylinder.

---

## 1. Frozen definitions and the clock qualification

The standard and viscosity-adapted time intervals frozen in R0.73X are

\[
 I_R^{\rm std}=(t_0-R^2,t_0),
 \qquad
 I_R^\nu=(t_0-R^2/\nu,t_0).
\tag{1.1}
\]

Both scale parabolically because \(\nu\) is unchanged by the
Navier--Stokes scaling.  They are not interchangeable.

For either clock, the canonical local energy frozen in R0.73X is

\[
 \mathcal E^\square(z_0,\rho)
 =\frac1\rho\mathop{\rm ess\,sup}_{t\in I_\rho^\square}
   \int_{B_\rho}|u|^2\,dx
 +\frac\nu\rho\int_{I_\rho^\square}\int_{B_\rho}
   |\nabla u|^2\,dx\,dt,
 \qquad \square\in\{{\rm std},\nu\}.
\tag{1.2}
\]

Every comparison below uses the same \(\square\) on the left and right.
No assertion replaces \(I_R^\nu\) by a standard interval, or conversely.
Because the right-hand side uses radius \(4R\), the common quantifier is

\[
 I_{4R}^\square\Subset(0,T).
\tag{1.3}
\]

Let \(P_s=e^{s\Delta}\) be the periodic heat semigroup.  At almost every
physical time for which \(u(t)\in H^1(\mathbb T^3)\), set

\[
 \begin{aligned}
 k_s&=\frac12\bigl(P_s|u|^2-|P_su|^2\bigr),\\
 D_s&=P_s|\nabla u|_F^2-|\nabla P_su|_F^2.
 \end{aligned}
\tag{1.4}
\]

The exact variance formulas imply

\[
 0\le k_s\le\frac12P_s|u|^2,
 \qquad
 0\le D_s\le P_s|\nabla u|_F^2.
\tag{1.5}
\]

Throughout,

\[
 0<R<\frac\pi8,
 \qquad 0<\theta\le1,
 \qquad I_{4R}^\square\Subset(0,T),
\tag{1.6}
\]

and

\[
 u\in L_t^\infty L_x^2(I_{4R}^\square\times\mathbb T^3)
 \cap L_t^2H_x^1(I_{4R}^\square\times\mathbb T^3).
\tag{1.7}
\]

Pressure does not enter (0.1) or Theorem 4.1.  It enters only through the
inherited pressure-tail interface in Corollary 4.3.

---

## 2. Lifted annuli and the two quadratic exterior inputs

Fix a lift \(\widetilde x_0\in\mathbb R^3\) of \(x_0\), and write
\(\widetilde u\) for the periodic lift.  Put

\[
 C_R=B_{2R}(\widetilde x_0),
 \qquad E_R=\mathbb R^3\setminus C_R,
\tag{2.1}
\]

and, for \(m\ge1\),

\[
 A_m(R)=\{y:2^mR\le|y-\widetilde x_0|<2^{m+1}R\}.
\tag{2.2}
\]

Up to null boundaries, the annuli partition \(E_R\).  They include all
lattice copies of the periodic field.  Use the weight frozen in R0.73X,

\[
 \gamma_m(\theta)
 =\theta^{-2}\exp\!\left(-\frac{4^{m-1}}{32\theta}\right).
\tag{2.3}
\]

For almost every \(t\in I_R^\square\), define

\[
 \begin{aligned}
 U_\gamma(t;R,\theta)
 &=\sum_{m\ge1}\gamma_m(\theta)
   \int_{A_m(R)}|\widetilde u(t,y)|^2\,dy,\\
 G_\gamma(t;R,\theta)
 &=\sum_{m\ge1}\gamma_m(\theta)
   \int_{A_m(R)}|\nabla\widetilde u(t,y)|_F^2\,dy.
 \end{aligned}
\tag{2.4}
\]

The scale-invariant exterior quantities used below are

\[
 \boxed{
 \begin{aligned}
 \mathcal U_{\rm ext}^{\infty,\square}(z_0,R;\theta)
 &=\mathop{\rm ess\,sup}_{t\in I_R^\square}
   \frac{U_\gamma(t;R,\theta)}R,\\
 \mathcal G_{\nabla,\rm ext}^{1,\square}(z_0,R;\theta)
 &=\frac\nu R\int_{I_R^\square}G_\gamma(t;R,\theta)\,dt.
 \end{aligned}}
\tag{2.5}
\]

The superscripts record the time exponents, not derivative orders.  The
second row is not a new tail: comparison with R0.73X (7.2) gives the exact
identity

\[
 \boxed{
 \mathcal G_{\nabla,\rm ext}^{1,\square}(z_0,R;\theta)
 =\mathcal D_{\rm ext}^{\square}(z_0,R;\theta).}
\tag{2.5a}
\]

Only \(\mathcal U_{\rm ext}^{\infty,\square}\) is newly introduced in
this note.  We use \(\mathcal D_{\rm ext}^{\square}\) from now on.

### Lemma 2.1 — scaling and finiteness of the tails

Under

\[
 u_\lambda(t,x)=\lambda u(\lambda^2t,\lambda x),
 \qquad R_\lambda=R/\lambda,
\tag{2.6}
\]

with the corresponding rescaled center and interval,

\[
 \mathcal U_{\rm ext}^{\infty,\square}[u_\lambda]
 =\mathcal U_{\rm ext}^{\infty,\square}[u],
 \qquad
 \mathcal D_{\rm ext}^{\square}[u_\lambda]
 =\mathcal D_{\rm ext}^{\square}[u].
\tag{2.7}
\]

Both quantities are finite under (1.7).

#### Proof

On corresponding annuli,

\[
 \int|u_\lambda|^2\,dx=\lambda^{-1}\int|u|^2\,dx,
 \qquad
 \int|\nabla u_\lambda|^2\,dx
 =\lambda\int|\nabla u|^2\,dx.
\tag{2.8}
\]

Together with \(R_\lambda^{-1}=\lambda R^{-1}\) and
\(dt_\lambda=\lambda^{-2}dt\), this proves (2.7), with the periodic
lattice rescaled in the standard local Navier--Stokes scaling convention.

Each lifted annulus contains at most
\(C[1+(2^mR)^3]\) fundamental cells.  Hence

\[
 \begin{aligned}
 U_\gamma(t)
 &\le C\|u(t)\|_{L^2(\mathbb T^3)}^2
   \sum_{m\ge1}\gamma_m[1+(2^mR)^3],\\
 G_\gamma(t)
 &\le C\|\nabla u(t)\|_{L^2(\mathbb T^3)}^2
   \sum_{m\ge1}\gamma_m[1+(2^mR)^3].
 \end{aligned}
\tag{2.9}
\]

The sums converge because \(\gamma_m\) decays faster than geometrically.
Now (1.7) proves finiteness. \(\square\)

---

## 3. Positive core/exterior majorization

For \(x\in B_R\) and \(0<s\le\theta R^2\), define

\[
 \begin{aligned}
 U_c&=\int_{C_R}g_s(\widetilde x-y)|\widetilde u(y)|^2\,dy,
 &U_e&=\int_{E_R}g_s(\widetilde x-y)|\widetilde u(y)|^2\,dy,\\
 G_c&=\int_{C_R}g_s(\widetilde x-y)|\nabla\widetilde u(y)|_F^2\,dy,
 &G_e&=\int_{E_R}g_s(\widetilde x-y)|\nabla\widetilde u(y)|_F^2\,dy.
 \end{aligned}
\tag{3.1}
\]

These are positive pieces of the uncentered moments.  They are not
separate covariances.  From (1.5),

\[
 \boxed{
 D_s\sqrt{k_s}
 \le\frac1{\sqrt2}\left(
 G_c\sqrt{U_c}+G_c\sqrt{U_e}
 +G_e\sqrt{U_c}+G_e\sqrt{U_e}\right).}
\tag{3.2}
\]

This is the core/core, core/exterior, exterior/core, and
exterior/exterior split used in the theorem.

There is no claimed exact four-term covariance identity.  Directly
splitting \(u=1_{C_R}u+1_{E_R}u\) inside a covariance creates cross terms
such as

\[
 -2(P_s(1_{C_R}\nabla u)):(P_s(1_{E_R}\nabla u)),
\tag{3.3}
\]

and the square root of the velocity covariance cannot be expanded
linearly.  The positive majorization (3.2) avoids that false identity.

The R0.73X Gaussian annulus lemma gives, uniformly in the full scale
interval,

\[
 \boxed{
 U_e(t,x,s)\le CR^{-3}U_\gamma(t),
 \qquad
 G_e(t,x,s)\le CR^{-3}G_\gamma(t).}
\tag{3.4}
\]

Also,

\[
 \int_{B_R}G_c(t,x,s)\,dx
 \le\int_{B_{2R}}|\nabla u(t,y)|_F^2\,dy.
\tag{3.5}
\]

Finally, periodic heat ultracontractivity implies

\[
 \|U_c(t,\cdot,s)\|_{L^\infty(B_R)}^{1/2}
 \le C_{\mathbb T^3}s^{-3/4}
 \|u(t)\|_{L^2(B_{2R})}.
\tag{3.6}
\]

---

## 4. The localized size theorem

For \(I=I_R^\square\), put

\[
 \begin{aligned}
 A_c(I,R)
 &=\frac1R\mathop{\rm ess\,sup}_{t\in I}
   \int_{B_{2R}}|u(t)|^2\,dx,\\
 B_c(I,R)
 &=\frac\nu R\int_I\int_{B_{2R}}|\nabla u|_F^2\,dx\,dt.
 \end{aligned}
\tag{4.1}
\]

### Theorem 4.1 — core/exterior Gaussian size lemma

Assume (1.6)--(1.7).  Then

\[
 \boxed{
 \begin{aligned}
 \mathcal K_D^\square(z_0,R;\theta)
 \le C_{\mathbb T^3}\big[&
 \theta^{1/4}A_c^{1/2}B_c
 +\theta B_c(\mathcal U_{\rm ext}^{\infty,\square})^{1/2}\\
 &+\theta^{1/4}A_c^{1/2}\mathcal D_{\rm ext}^{\square}
 +\theta(\mathcal U_{\rm ext}^{\infty,\square})^{1/2}
   \mathcal D_{\rm ext}^{\square}\big].
 \end{aligned}}
\tag{4.2}
\]

Since \(0<\theta\le1\), this implies the factorized bound

\[
 \mathcal K_D^\square
 \le C_{\mathbb T^3}\theta^{1/4}
 \left(A_c^{1/2}+(\mathcal U_{\rm ext}^{\infty,\square})^{1/2}\right)
 \left(B_c+\mathcal D_{\rm ext}^{\square}\right).
\tag{4.3}
\]

For either clock, the matching R0.73X local energy gives

\[
 \boxed{
 \mathcal K_D^\square(z_0,R;\theta)
 \le C_{\mathbb T^3}\theta^{1/4}
 \left[
 \mathcal E^\square(z_0,4R)
 +\mathcal U_{\rm ext}^{\infty,\square}(z_0,R;\theta)
 +\mathcal D_{\rm ext}^{\square}(z_0,R;\theta)
 \right]^{3/2}.}
\tag{4.4}
\]

Here \(\mathcal K_{D,cc}\) denotes the contribution obtained from
\(G_c\sqrt{U_c}/\sqrt2\) in (3.2).

#### Proof: core--core

By (3.5)--(3.6),

\[
 \int_{B_R}G_c\sqrt{U_c}\,dx
 \le Cs^{-3/4}
 \|u(t)\|_{L^2(B_{2R})}
 \|\nabla u(t)\|_{L^2(B_{2R})}^2.
\tag{4.5}
\]

Since

\[
 \int_0^{\theta R^2}s^{-3/4}\,ds
 =4\theta^{1/4}R^{1/2},
\tag{4.6}
\]

we obtain

\[
 \mathcal K_{D,cc}^\square
 \le C\theta^{1/4}
 A_c^{1/2}B_c.
\tag{4.7}
\]

For either fixed \(\square\), the spatial inclusion
\(B_{2R}\subset B_{4R}\) and the matching time inclusion
\(I_R^\square\subset I_{4R}^\square\) give

\[
 A_c+B_c\le4\mathcal E^\square(z_0,4R).
\tag{4.8}
\]

Thus the core--core row is paid by
\(C\theta^{1/4}(\mathcal E^\square)^{3/2}\).  Combining (4.8)
with (4.3) and the elementary bound
\((a^{1/2}+b^{1/2})(c+d)\le
C(a+b+c+d)^{3/2}\) proves (4.4).

#### Proof: core--exterior

Using (3.4)--(3.5),

\[
 \int_{B_R}G_c\sqrt{U_e}\,dx
 \le CR^{-3/2}U_\gamma(t)^{1/2}
 \int_{B_{2R}}|\nabla u(t)|^2\,dx.
\tag{4.9}
\]

The integrand no longer depends on \(s\).  Integrating over a scale
interval of length \(\theta R^2\), and then over physical time, gives

\[
 \mathcal K_{D,ce}^\square
 \le C\theta B_c
 (\mathcal U_{\rm ext}^{\infty,\square})^{1/2}.
\tag{4.10}
\]

#### Proof: exterior--core

From (3.4) and \(|B_R|\simeq R^3\),

\[
 \int_{B_R}G_e\sqrt{U_c}\,dx
 \le Cs^{-3/4}G_\gamma(t)
 \|u(t)\|_{L^2(B_{2R})}.
\tag{4.11}
\]

Using (4.6) and the definitions (4.1), (2.5),

\[
 \mathcal K_{D,ec}^\square
 \le C\theta^{1/4}A_c^{1/2}
 \mathcal D_{\rm ext}^{\square}.
\tag{4.12}
\]

#### Proof: exterior--exterior

The two estimates in (3.4) give

\[
 \int_{B_R}G_e\sqrt{U_e}\,dx
 \le CR^{-3/2}G_\gamma(t)U_\gamma(t)^{1/2}.
\tag{4.13}
\]

After integration in \(s\) and \(t\),

\[
 \mathcal K_{D,ee}^\square
 \le C\theta
 (\mathcal U_{\rm ext}^{\infty,\square})^{1/2}
 \mathcal D_{\rm ext}^{\square}.
\tag{4.14}
\]

Adding (4.7), (4.10), (4.12), and (4.14) proves (4.2). \(\square\)

### Remark 4.2 — sharper coupled tails

The separated pair in (2.5) is convenient but not the only bookkeeping.
The three exact Hölder pairings produced by the proof are

\[
 \begin{aligned}
 \mathcal T_{ce}
 &=\frac\nu R\int_I
 \left(\int_{B_{2R}}|\nabla u|^2\right)
 \left(\frac{U_\gamma(t)}R\right)^{1/2}dt,\\
 \mathcal T_{ec}
 &=\frac\nu R\int_I G_\gamma(t)
 \left(\frac1R\int_{B_{2R}}|u|^2\right)^{1/2}dt,\\
 \mathcal T_{ee}
 &=\frac\nu R\int_I G_\gamma(t)
 \left(\frac{U_\gamma(t)}R\right)^{1/2}dt.
 \end{aligned}
\tag{4.15}
\]

Each is scale invariant.  They give a sharper mixed-tail formulation if a
later argument can estimate them directly.  This note does not claim that
the separated tails in (2.5) are optimal among every possible coupled
functional.

### Corollary 4.3 — interface with the pressure-cutoff row

Assume in addition that \((u,p)\) is a periodic suitable weak solution on
\(\mathbb T^3\times(0,T)\), with \(p\in L_{t,x}^{3/2}\), and that the
common R0.73X pressure-tail quantifiers hold.  Let

\[
 Q_s=P_s(pu)-P_sp\,P_su,
\tag{4.16}
\]

let \(s:I_R^\square\to(0,\theta R^2]\) be measurable, and let
\(\eta_R\in W_0^{1,\infty}(B_R)\) satisfy
\(\|\nabla\eta_R\|_\infty\le C_\eta/R\).  Combining Theorem 4.1
with the R0.73X pressure-covariance estimate (5.7) and its local-energy
payment (6.2) gives

\[
 \boxed{
 \begin{aligned}
 &\mathcal K_D^\square(z_0,R;\theta)
 +\frac1R\int_{I_R^\square}\int_{B_R}
  |Q_{s(t)}\cdot\nabla\eta_R|\,dx\,dt\\
 &\quad\le C_{\mathbb T^3,\theta,\nu,C_\eta}
 \left\{
 \left[
 \mathcal E^\square(z_0,4R)
 +\mathcal U_{\rm ext}^{\infty,\square}(z_0,R;\theta)
 +\mathcal D_{\rm ext}^{\square}(z_0,R;\theta)
 \right]^{3/2}
 +\mathcal A_{\rm ext}^{\square}(z_0,R;\theta)
 \right\}.
 \end{aligned}}
\tag{4.17}
\]

The new velocity endpoint tail and the reused gradient tail pay
\(\mathcal K_D\).  The older \(\mathcal A_{\rm ext}\) continues to pay
the nonlocal pressure and harmonic rows.  No claim is made that the two
quadratic tails alone control a general \(Q_s\).

---

## 5. Why the older exterior functional is insufficient

The R0.73X functional is

\[
 \mathcal A_{\rm ext}^\square
 =\mathcal G_{u,p}^\square+\mathcal H_u^\square,
\tag{5.1}
\]

where \(\mathcal G_{u,p}\) contains the Gaussian annular integral of

\[
 |u|^3+|p-c_R(t)|^{3/2},
\tag{5.2}
\]

and \(\mathcal H_u\) contains an algebraically weighted annular
\(|u|^2\) moment used for harmonic pressure.  Neither term contains
\(|\nabla u|^2\).  Also, the Gaussian \(|u|^3\) row is integrated in
physical time and does not control an essential time supremum of annular
\(L^2\) energy.

The next examples are pure function-level obstructions.  They are not
Navier--Stokes solutions and do not construct a singularity.

### Example 5.1 — exterior high-frequency packet

Choose a ball \(B_*\Subset A_2(R)\) whose closure is disjoint from
\(B_{4R}\), and choose
\(\phi\in C_c^\infty(B_*)\), \(\phi\ne0\).  For integers \(N\) and
amplitudes \(\varepsilon_N>0\), let

\[
 b_N(y)=\frac{\varepsilon_N}N\phi(y)\sin(Ny_1)e_3,
 \qquad w_N=\nabla\times b_N.
\tag{5.3}
\]

Regard the packet as a periodic field in the fixed chart and set its
associated Poisson pressure to

\[
 p_N=\mathcal R_i\mathcal R_j(w_{N,i}w_{N,j}),
 \qquad -\Delta p_N=\partial_i\partial_j(w_{N,i}w_{N,j}).
\tag{5.3a}
\]

Then \(w_N\) is smooth, divergence free, and supported in \(B_*\).  For
all sufficiently large \(N\),

\[
 \|w_N\|_{L^2}+\|w_N\|_{L^3}\simeq_\phi\varepsilon_N,
 \qquad
 \|\nabla w_N\|_{L^2}\simeq_\phi\varepsilon_NN,
 \qquad
 \|p_N\|_{L^{3/2}}\le C_\phi\varepsilon_N^2.
\tag{5.4}
\]

The last estimate is the periodic Calder\'on--Zygmund bound.  For a
time-independent packet on a fixed interval,

\[
 \mathcal E^\square(z_0,4R)=0,
 \qquad
 \mathcal A_{\rm ext}^\square\le C\varepsilon_N^3.
\tag{5.4a}
\]

Fix \(0<\alpha<\beta\le\theta\).  The periodic heat kernel has a positive
minimum on
\(s\in[\alpha R^2,\beta R^2]\).  Since a periodic curl and its gradient
have zero spatial mean, the exact variance formulas give, uniformly for
\(x\in B_R\) on that scale band,

\[
 k_s[w_N](x)\ge c\varepsilon_N^2,
 \qquad
 D_s[w_N](x)\ge c\varepsilon_N^2N^2.
\tag{5.4b}
\]

Consequently

\[
 \mathcal K_D^\square[w_N]\ge c\varepsilon_N^3N^2.
\tag{5.4c}
\]

Taking \(\varepsilon_N=N^{-2/3}\) yields

\[
 \mathcal K_D^\square[w_N]\ge c,
 \qquad
 \mathcal E^\square(z_0,4R)=0,
 \qquad
 \mathcal A_{\rm ext}^\square=O(N^{-2})\longrightarrow0.
\tag{5.4d}
\]

Thus the older
\((\mathcal E^\square)^{3/2}+\mathcal A_{\rm ext}^\square\)
payment does not control \(\mathcal K_D\) for arbitrary periodic
energy-class velocity/Poisson-pressure pairs.  The static packets are not
unforced Navier--Stokes trajectories, so (5.4d) is not a suitable-weak NSE
counterexample.

### Example 5.2 — exterior time concentration

Let \(w\in C_c^\infty(B_*;\mathbb R^3)\) be nonzero and divergence free.
Choose a time interval \(J_\delta\subset I\) of length \(\delta\), and
smoothly approximate

\[
 w_\delta(t,y)=\delta^{-1/3}1_{J_\delta}(t)w(y).
\tag{5.5}
\]

Then

\[
 \int_I\int|w_\delta|^3\,dy\,dt=\|w\|_3^3,
 \qquad
 \mathop{\rm ess\,sup}_{t\in I}\int|w_\delta|^2\,dy
 =\delta^{-2/3}\|w\|_2^2.
\tag{5.6}
\]

With the associated pressure
\(p_\delta=\mathcal R_i\mathcal R_j
(w_{\delta,i}w_{\delta,j})\), the complete old
\(\mathcal A_{\rm ext}\) remains bounded by Calder\'on--Zygmund, while
\(\mathcal U_{\rm ext}^{\infty}\to\infty\).  This shows why the old
Gaussian velocity tail does not supply the time endpoint used in
core--exterior estimate (4.10).

The sequence (5.5) has no uniform \(L_t^\infty L_x^2\) bound.  It does not
contradict energy-class finiteness for any fixed field.  If a later theorem
allows a global Leray energy on its right-hand side, that global energy can
pay this time supremum, but the resulting estimate is no longer a closure
by the old local-energy and \(\mathcal A_{\rm ext}\) package alone.

---

## 6. Proven rows and remaining gates

### `PROVED`

1. The positive four-block majorization (3.2) is dimensionally and
   algebraically valid.
2. The four blocks satisfy (4.7), (4.10), (4.12), and (4.14), with the
   displayed \(\theta^{1/4}\) or \(\theta\) factors.
3. For both matching clocks, the full observable satisfies the local
   energy/tail bound (4.4).
4. The pressure-cutoff row interfaces with the new estimate through the
   inherited R0.73X payment, giving (4.17).
5. The all-energy-field packets (5.3)--(5.4d) prove that the old
   \((\mathcal E^\square)^{3/2}
   +\mathcal A_{\rm ext}^\square\) right-hand side alone does not control
   \(\mathcal K_D\) in that larger class.
6. All quantities in (4.2) are invariant under Navier--Stokes scaling.

### `FINITE`

For every periodic energy-class velocity on the stated interval,
\(\mathcal U_{\rm ext}^{\infty,\square}\) and
\(\mathcal D_{\rm ext}^{\square}\) are finite.  The first is the one new
endpoint tail; the second is the favorable gradient tail already frozen in
R0.73X.  This is a size statement, not a uniform local bound.

### `OPEN`

1. Control of the new velocity endpoint tail and the reused gradient tail
   by data on one smaller cylinder.
2. Smallness or absorption of either quadratic tail in a local energy
   inequality.
3. A sharper argument replacing the time supremum by a coupled tail that
   is stable under the intended blow-up sequence.
4. Whether the Navier--Stokes equation supplies a stronger closure absent
   for arbitrary energy-class velocity/Poisson-pressure pairs; the static
   packet obstruction does not decide this.
5. Weak stability and lower semicontinuity of the localized observable and
   its chosen exterior payments.
6. Compatibility of this upper bound with a scale-uniform lower bound after
   quotienting the precise first-jet near-kernel.
7. Any epsilon-regularity consequence.

### `NOT CLAY`

Nothing in this note proves compactness, epsilon regularity, smoothness, or
global regularity for three-dimensional Navier--Stokes solutions.
