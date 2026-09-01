# R0.74E — local mollified-frame gate and transport audit

## Status and scope

R0.74D proves that subtracting only the constant global mean does not repair
the frozen R0.74B large-payment endpoint.  The next transport-aware test must
follow a genuinely local velocity.  This note freezes that test before any
positive or negative conclusion is attempted.

There are two inequivalent changes of variables:

1. move the centre along a mollified velocity but do not subtract that
   velocity from the field; or
2. move the centre and subtract the trajectory velocity.

The first version retains the physical periodic pressure and has no body
force, but its convecting velocity differs from the transported velocity.
The second restores canonical convection but produces a spatially constant
acceleration force.  On the torus that force cannot be hidden in a periodic
pressure.  The two versions must not be mixed.

The coordinate identities and the single-scale cancellation below are
**PROVED**.  The R0.74D reference offset and separate analytic residence
estimate in the new frame are **PROVED**, and
the entire explicit R0.74D family is quantitatively bounded by its harmonic
payment in both frozen local-frame ledgers.  This is a familywise
neutralization theorem, not a positive estimate for arbitrary solutions.  A
complete endpoint estimate in either local frame remains **OPEN**.  The
high-frequency single-cosine test is rejected only as a
small-perturbation packet construction; this is not a universal no-go
theorem.  Labels are literal: **PROVED**, **FROZEN**, **OPEN**, **REJECTED
MECHANISM**, **PRIOR ART**, and **NOT CLAY**.

Throughout,

\[
 \nu=1,\qquad \mathbb T^3=(-\pi,\pi]^3,
 \qquad I_\rho=(t_0-\rho^2,t_0).
\tag{0.1}
\]

The solution class in this gate is smooth, periodic, and unforced on
\((0,T)\times\mathbb T^3\), with

\[
 \overline I_{8R}\Subset(0,T).
\tag{0.2}
\]

---

## 1. One mollifier, one terminal trajectory, and one lift

Fix once and for all an even radial mollifier

\[
 \varphi\in C_c^\infty(B_1),\qquad
 \varphi\ge0,\qquad \int_{\mathbb R^3}\varphi=1.
\tag{1.1}
\]

For every \(0<\rho<\pi\), let

\[
 \varphi_\rho^{\rm per}(x)
 =\sum_{k\in\mathbb Z^3}\rho^{-3}
   \varphi\!\left(\frac{\widetilde x+2\pi k}{\rho}\right),
 \qquad
 u_\rho=\varphi_\rho^{\rm per}*_{\mathbb T^3}u,
 \qquad p_\rho=\varphi_\rho^{\rm per}*_{\mathbb T^3}p.
\tag{1.2}
\]

In (1.2), the prefactor is \(\rho^{-3}\); the letter \(R\) is reserved
below for the principal gate scale.  We assume \(0<R<\pi/16\), and the
trajectory uses \(u_R\).  The same definition is therefore available at
\(2R\) and \(8R\) whenever it is used later.

Given \(z_0=(t_0,x_0)\), define on the whole closed interval
\(\overline I_{8R}\) the terminal-value trajectory

\[
 \boxed{
 \dot X_R(t)=u_R(t,X_R(t)),\qquad X_R(t_0)=x_0.}
\tag{1.3}
\]

For a smooth solution this ODE has a unique smooth solution.  It is solved
backwards from its terminal value; the sign in (1.3) is not reversed.  Fix a
continuous lift \(\widetilde X_R\) with
\(\widetilde X_R(t_0)=\widetilde x_0\), and put

\[
 a_R(t)=\dot X_R(t),
\tag{1.4}
\]

\[
 v_R(t,y)=u(t,y+X_R(t)),\qquad
 \pi_R(t,y)=p(t,y+X_R(t)),
\tag{1.5}
\]

\[
 w_R(t,y)=v_R(t,y)-a_R(t).
\tag{1.6}
\]

Every quantity at radii \(R,2R,8R\) in this gate uses the **same**
trajectory \(X_R\).  This preserves the physical identity between doubled
annuli.  Using a different trajectory at each radius would require a new
comparison theorem for those trajectories and is not licensed here.

Because the same even kernel occurs in (1.2)--(1.3),

\[
 \boxed{
 \int_{\mathbb T^3}\varphi_R^{\rm per}(y)w_R(t,y)\,dy=0.}
\tag{1.7}
\]

The periodic lifts

\[
 \widetilde v_R(t,y)=\widetilde u(t,y+\widetilde X_R(t)),
 \qquad \widetilde w_R=\widetilde v_R-a_R
\tag{1.8}
\]

do not depend on changing \(\widetilde X_R\) by a vector in
\(2\pi\mathbb Z^3\).

---

## 2. The exact transformation identity

The following identity is the algebraic gate for every later estimate.

### Proposition 2.1 — moving and subtracting are distinct operations

Let \(X'=a(t)\), let \(c(t)\) be any spatially constant vector, and set

\[
 W(t,y)=u(t,y+X(t))-c(t),\qquad
 P(t,y)=p(t,y+X(t)).
\tag{2.1}
\]

If \((u,p)\) solves periodic incompressible Navier--Stokes, then

\[
 \boxed{
 \partial_tW-\Delta W
 +(W+c-a)\cdot\nabla W+\nabla P=-c'(t),
 \qquad \nabla\cdot W=0.}
\tag{2.2}
\]

**Proof.**  The chain rule gives

\[
 \partial_tW=(\partial_tu)(t,y+X)
              +a\cdot\nabla u(t,y+X)-c'.
\tag{2.3}
\]

Substitute \(u=W+c\) and the original equation.  Since \(a\) and \(c\)
are independent of \(y\), their spatial derivatives vanish, and (2.2)
follows. \(\square\)

Thus, as a structural identity valid for general \(u\), the transformed pair
is again canonical, unforced, periodic NSE when \(c=a\) and \(a'=0\).
Special degenerate fields can have additional accidental cancellations.  The
global-mean Galilean frame used in R0.74D
has precisely this special property.  A genuinely local trajectory does
not have it in general.

---

## 3. Version M: move the centre and retain the physical velocity

Taking \(c=0\) in Proposition 2.1 gives

\[
 \boxed{
 \partial_tv_R-\Delta v_R
 +(v_R-a_R)\cdot\nabla v_R+\nabla\pi_R=0.}
\tag{3.1}
\]

Both \(v_R\) and \(v_R-a_R\) are divergence free.  There is no body force,
and \(\pi_R\) is the physical periodic pressure.  The price is the residual
transport \(-a_R\cdot\nabla v_R\).

For a nonnegative smooth cutoff \(\chi\), times
\(t_a<\tau\le t_0\), and \(\chi\) supported in
\((t_a,t_0]\times\mathbb T^3\), the corresponding local energy inequality
is

\[
\begin{aligned}
 &\int |v_R(\tau)|^2\chi(\tau)
 +2\int_{t_a}^{\tau}\!\int|\nabla v_R|^2\chi \\
 &\le \int_{t_a}^{\tau}\!\int |v_R|^2
       (\partial_t\chi+\Delta\chi) \\
 &\quad+\int_{t_a}^{\tau}\!\int
   \bigl[|v_R|^2(v_R-a_R)+2\pi_Rv_R\bigr]
   \cdot\nabla\chi .
\end{aligned}
\tag{3.2}
\]

The new-looking term is

\[
 -\int |v_R|^2a_R\cdot\nabla\chi.
\tag{3.3}
\]

It is residual transport, not a body force.  Jensen's inequality gives

\[
 |a_R(t)|^3
 \le \int\varphi_R^{\rm per}(y)|v_R(t,y)|^3\,dy
 \le CR^{-3}\int_{B_R}|v_R(t,y)|^3\,dy.
\tag{3.4}
\]

Consequently Young's inequality pays the shell version of (3.3) with the
same local-plus-exterior cubic ledger used for \(v_R\).  No acceleration
payment is introduced in Version M.  On the other hand, (1.7) is a
zero-mean identity for \(w_R\), not for \(v_R\); it cannot be used to give
\(v_R\) a Poincare gain.

More explicitly, for the target-scale cutoffs frozen below,

\[
\begin{aligned}
 &R^{-2}\sum_j\gamma_j\int_{I_{2R}}
   \int |a_R||v_R|^2|\nabla\psi_j^R|\,R\,dy\,dt\\
 &\quad\le C R^{-2}\int_{I_{2R}}
 \left[\int_{B_R}|v_R|^3
 +\sum_j\gamma_j\int_{\operatorname{supp}\psi_j^R}|v_R|^3\right]dt,
\end{aligned}
\tag{3.5}
\]

where
\(\sum_j\gamma_j|\operatorname{supp}\psi_j^R|\le CR^3\).

### Frozen Version-M quantities

Define

\[
\begin{aligned}
 \mathcal E^{M,R}(z_0,\rho)
 &=\rho^{-1}\mathop{\rm ess\,sup}_{I_\rho}
       \int_{B_\rho}|v_R|^2
   +\rho^{-1}\int_{I_\rho}\!\int_{B_\rho}|\nabla v_R|^2,\\
 U_\gamma^{M,R}(t)
 &=\sum_{j\ge1}\gamma_j
   \int_{A_j(R)}|\widetilde v_R(t,y)|^2\,dy,\\
 G_\gamma^{M,R}(t)
 &=\sum_{j\ge1}\gamma_j
   \int_{A_j(R)}|\nabla\widetilde v_R(t,y)|^2\,dy,
\end{aligned}
\tag{3.6}
\]

where

\[
 A_j(R)=\{2^jR\le|y|<2^{j+1}R\},
 \qquad \gamma_j=e^{-4^{j-1}/32}.
\tag{3.7}
\]

Put

\[
 \mathcal U_{\rm ext}^{\infty,M,R}
 =\mathop{\rm ess\,sup}_{I_R}R^{-1}U_\gamma^{M,R}(t),
 \qquad
 \mathcal D_{\rm ext}^{M,R}
 =R^{-1}\int_{I_R}G_\gamma^{M,R}(t)\,dt.
\tag{3.8}
\]

Fix \(0\le\zeta\in C_c^\infty(B_4)\) with \(\zeta=1\) on \(B_3\), and put
\(\zeta_\rho(y)=\zeta(y/\rho)\).  The local pressure split and gauge are

\[
 p_{\rho}^{\rm loc,M,R}
 =\mathcal R_i\mathcal R_j
   (\zeta_\rho\widetilde v_{R,i}\widetilde v_{R,j}),
 \qquad
 h_\rho^{M,R}=\widetilde\pi_R-p_\rho^{\rm loc,M,R},
 \qquad
 c_\rho^{M,R}(t)=(h_\rho^{M,R})_{B_{2\rho}}.
\tag{3.8a}
\]

Here \(h_\rho^{M,R}\) is harmonic on \(B_{3\rho}\).  Define the exact
all-copy weights

\[
 W_\rho(y)=\sum_{j\ge1}\gamma_j1_{A_j(\rho)}(y),
 \qquad
 L_\rho(y)=\rho\sum_{j\ge1}(2^j\rho)^{-4}
 1_{A_j(\rho)}(y),
\tag{3.8b}
\]

and

\[
\begin{aligned}
 \mathcal G_{v_R,\pi_R}^{M,R}(z_0,\rho;1)
 &=\rho^{-2}\sum_{j\ge1}\gamma_j
   \int_{I_\rho}\!\int_{A_j(\rho)}
   \left(|\widetilde v_R|^3
   +|\widetilde\pi_R-c_\rho^{M,R}|^{3/2}\right)dy\,dt,\\
 \Lambda_\rho^{M,R}(t)
 &=\int_{\mathbb R^3}L_\rho(y)|\widetilde v_R(t,y)|^2\,dy\\
 &=\rho\sum_{j\ge1}(2^j\rho)^{-4}
   \int_{A_j(\rho)}|\widetilde v_R(t,y)|^2\,dy,\\
 \mathcal H_{v_R}^{M,R}(z_0,\rho)
 &=\rho\int_{I_\rho}(\Lambda_\rho^{M,R}(t))^{3/2}\,dt,\\
 \mathcal A_{\rm ext}^{M,R}(z_0,\rho;1)
 &=\mathcal G_{v_R,\pi_R}^{M,R}(z_0,\rho;1)
  +\mathcal H_{v_R}^{M,R}(z_0,\rho).
\end{aligned}
\tag{3.8c}
\]

All annuli in (3.8a)--(3.8c) are centred at the single translated origin
generated by \(X_R\), and all periodic copies are included by the lift.
The frozen endpoint is

\[
 X_R^M=\mathcal U_{\rm ext}^{\infty,M,R}
       +\mathcal D_{\rm ext}^{M,R},
\tag{3.9}
\]

\[
 P_R^M=\mathcal E^{M,R}(z_0,8R)^{3/2}
       +\mathcal A_{\rm ext}^{M,R}(z_0,2R;1),
\tag{3.10}
\]

and the Version-M question is

\[
 \boxed{X_R^M\stackrel{?}{\le}C(P_R^M)^{2/3}.}
\tag{3.11}
\]

Equation (3.11) is **OPEN**.

---

## 4. Version F: move the centre and subtract its velocity

Taking \(c=a_R\) gives

\[
 \boxed{
 \partial_tw_R-\Delta w_R
 +(w_R\cdot\nabla)w_R+\nabla\pi_R=-a_R'(t).}
\tag{4.1}
\]

The acceleration has the exact filtered-stress identity

\[
 \boxed{
 a_R'=\left[
 \Delta u_R-\nabla p_R-\nabla\cdot\tau_R
 \right](t,X_R(t)),
 \qquad
 \tau_R=(u\otimes u)_R-u_R\otimes u_R.}
\tag{4.2}
\]

The Version-F local energy inequality is

\[
\begin{aligned}
 &\int |w_R(\tau)|^2\chi(\tau)
 +2\int_{t_a}^{\tau}\!\int|\nabla w_R|^2\chi \\
 &\le \int_{t_a}^{\tau}\!\int |w_R|^2
       (\partial_t\chi+\Delta\chi)
 +\int_{t_a}^{\tau}\!\int
       (|w_R|^2+2\pi_R)w_R\cdot\nabla\chi \\
 &\quad-2\int_{t_a}^{\tau}a_R'(t)\cdot
       \left(\int\chi(t,y)w_R(t,y)\,dy\right)dt.
\end{aligned}
\tag{4.3}
\]

The periodic pressure source may be computed from \(w_R\) alone:

\[
 \boxed{-\Delta\pi_R
 =\partial_i\partial_j(w_{R,i}w_{R,j}).}
\tag{4.4}
\]

Indeed, the cross terms containing the spatial constant \(a_R(t)\) vanish
after the double divergence, and the constant acceleration has zero spatial
divergence.

### Proposition 4.1 — the acceleration is not periodic pressure

On the Euclidean lift one may formally set

\[
 \Pi_R(t,y)=\pi_R(t,y)+a_R'(t)\cdot y.
\tag{4.5}
\]

Then (4.1) becomes canonical NSE with pressure \(\Pi_R\), but

\[
 \Pi_R(t,y+2\pi k)-\Pi_R(t,y)=2\pi a_R'(t)\cdot k.
\tag{4.6}
\]

Unless \(a_R'=0\), this pressure is not periodic.  Equivalently, no
periodic scalar can have the nonzero constant gradient \(a_R'\).  Also

\[
 \frac d{dt}\overline{w_R}=-a_R',
\tag{4.7}
\]

whereas an unforced periodic canonical NSE solution preserves its mean.
Thus the physical periodic pressure \(\pi_R\) and the acceleration term in
(4.1) must be retained separately. \(\square\)

### Automatic exact cancellation at the matching weight

Let

\[
 \chi_R(y)=R^3\varphi_R^{\rm per}(y).
\tag{4.8}
\]

Equation (1.7) gives the pointwise-in-time cancellation

\[
 \boxed{
 a_R'(t)\cdot\int\chi_R(y)w_R(t,y)\,dy=0.}
\tag{4.9}
\]

This is the algebraic core of the established local mean-free frame.  It is
only a single-scale identity.  If
\(\chi_\rho=\rho^3\varphi_\rho^{\rm per}\), then along the same
\(R\)-trajectory

\[
 \boxed{
 \int\chi_\rho w_R
 =\rho^3\bigl[u_\rho(t,X_R(t))-u_R(t,X_R(t))\bigr].}
\tag{4.10}
\]

The trajectory definition forces the right side to vanish at \(\rho=R\).
No corresponding automatic cancellation is available at \(2R\) or \(8R\),
or for a sharp-ball or R0.74B shell cutoff.  Special fields may of course
produce additional accidental zeros.

### Frozen acceleration payment

Fix a radial function

\[
 \chi^{\rm core}\in C_c^\infty(B_2;[0,1]),\quad
 \chi^{\rm core}=1\ \hbox{on }B_1,
\tag{4.11}
\]

and one fixed nondecreasing \(\vartheta\in C^\infty(\mathbb R;[0,1])\)
with \(\vartheta(s)=0\) for \(s\le-1\) and \(\vartheta(s)=1\) for
\(s\ge0\).  Put

\[
 \chi_{8R}^{\rm core}(y)=\chi^{\rm core}(y/(8R)),
\tag{4.12a}
\]

and, with \(a_j=2^jR\), \(b_j=2^{j+1}R\),

\[
 \psi_j^R(y)
 =\vartheta\!\left(\frac{|y|-a_j}{R/8}\right)
  \vartheta\!\left(\frac{b_j-|y|}{R/8}\right).
\tag{4.12b}
\]

Thus \(\psi_j^R=1\) on the target shell \(A_j(R)\), and

\[
 \operatorname{supp}\psi_j^R
 \subset\{y:{\rm dist}(y,A_j(R))\le R/8\}.
\tag{4.12c}
\]

The pointwise support bookkeeping needed for the auxiliary cubic-velocity
estimate (3.5) is

\[
 \sum_{j\ge1}\gamma_j1_{\operatorname{supp}\psi_j^R}
 \le C1_{B_{8R}}+CW_{2R}.
\tag{4.12d}
\]

Indeed, the finitely many inner and padding pieces are covered by \(B_{8R}\);
outside that ball, finite overlap and monotonicity of \(\gamma_j\) compare
each padded target shell with at most two neighbouring \(2R\)-annuli.  This
support statement does **not** replace any acceleration moment:
\(\mathcal J_{\rm acc,sh}^{F,R}\) below retains every \(j\ge1\) term, and
the core moment (4.14) cannot substitute for a \(\psi_j^R\)-moment.
Define

\[
 \boxed{
 \mathcal J_{\rm acc,sh}^{F,R}
 =\frac2R\sum_{j\ge1}\gamma_j
 \int_{I_{2R}}|a_R'(t)|
 \left|\int_{\mathbb R^3}\psi_j^R(y)
       \widetilde w_R(t,y)\,dy\right|dt.}
\tag{4.13}
\]

The core term required for the \(8R\) energy buffer is

\[
 \boxed{
 \mathcal J_{\rm acc,core}^{F,R}
 =\frac1{4R}\int_{I_{8R}}|a_R'(t)|
 \left|\int\chi_{8R}^{\rm core}(y)w_R(t,y)\,dy\right|dt.}
\tag{4.14}
\]

The coefficient \(1/(4R)=2/(8R)\) follows the normalization in (4.3).
Set

\[
 \mathcal J_{\rm acc}^{F,R}
 =\mathcal J_{\rm acc,sh}^{F,R}
  +\mathcal J_{\rm acc,core}^{F,R}.
\tag{4.15}
\]

For Version F, define the pressure split explicitly by

\[
 p_\rho^{\rm loc,F,R}
 =\mathcal R_i\mathcal R_j
  (\zeta_\rho\widetilde w_{R,i}\widetilde w_{R,j}),
 \qquad
 h_\rho^{F,R}=\widetilde\pi_R-p_\rho^{\rm loc,F,R},
 \qquad
 c_\rho^{F,R}=(h_\rho^{F,R})_{B_{2\rho}}.
\tag{4.15a}
\]

The identity (4.4) makes this the physical periodic-pressure split.  Define
all remaining Version-F quantities by the exact local substitution

\[
\begin{aligned}
 (&\mathcal E^{F,R},U_\gamma^{F,R},G_\gamma^{F,R},
 \mathcal U_{\rm ext}^{\infty,F,R},\mathcal D_{\rm ext}^{F,R},
 \mathcal G_{w_R,\pi_R}^{F,R},\Lambda_\rho^{F,R},
 \mathcal H_{w_R}^{F,R},\mathcal A_{\rm ext}^{F,R})\\
 &:=\left.(\mathcal E^{M,R},U_\gamma^{M,R},G_\gamma^{M,R},
 \mathcal U_{\rm ext}^{\infty,M,R},\mathcal D_{\rm ext}^{M,R},
 \mathcal G_{v_R,\pi_R}^{M,R},\Lambda_\rho^{M,R},
 \mathcal H_{v_R}^{M,R},\mathcal A_{\rm ext}^{M,R})
 \right|_{v_R\mapsto w_R,\ c_\rho^{M,R}\mapsto c_\rho^{F,R}}.
\end{aligned}
\tag{4.15b}
\]

This is a definition by the displayed formulas (3.6)--(3.8c), not an
informal appeal to a different note.  Put

\[
 X_R^F=\mathcal U_{\rm ext}^{\infty,F,R}
       +\mathcal D_{\rm ext}^{F,R}.
\tag{4.15c}
\]

The frozen dimensionless payment is

\[
 P_R^F
 =\mathcal E^{F,R}(z_0,8R)^{3/2}
  +\mathcal A_{\rm ext}^{F,R}(z_0,2R;1)
  +(\mathcal J_{\rm acc}^{F,R})^{3/2},
\tag{4.16}
\]

and the Version-F question is

\[
 \boxed{X_R^F\stackrel{?}{\le}C(P_R^F)^{2/3}.}
\tag{4.17}
\]

Equation (4.17) is **OPEN**.  Omitting (4.13)--(4.15) is not an admissible
version of the question.

---

## 5. The affine-pressure rewrite does not remove the payment

For the super-Gaussian shell weights in (3.7), the standalone affine field
in (4.5) has the exact row

\[
\begin{aligned}
 &\rho^{-2}\sum_{j\ge1}\gamma_j
 \int_{I_\rho}\!\int_{A_j(\rho)}
 |a_R'(t)\cdot y|^{3/2}\,dy\,dt\\
 &\qquad=C_\gamma\rho^{5/2}
 \int_{I_\rho}|a_R'(t)|^{3/2}\,dt,
\end{aligned}
\tag{5.1}
\]

where

\[
 C_\gamma=C_*\sum_{j\ge1}\gamma_j2^{9j/2}<\infty.
\tag{5.2}
\]

Thus the affine rewrite is finite for each fixed \(\rho>0\), but it is a
new scale-dependent pressure row.  A constant pressure gauge cannot remove
its slope, and the velocity-generated harmonic payment does not automatically
pay it.  For the total pressure this row is a triangle-inequality payment,
not a linear decomposition of the \(L^{3/2}\) norm.  Formula (4.3) with the
explicit acceleration is therefore the frozen torus formulation.

---

## 6. R0.74D in the new trajectory: reference offset and analytic residence

Retain the exact R0.74D field

\[
 u=(AF,B_Re^{-t}\cos x_3,0),\qquad p=0,
\tag{6.1}
\]

Retain also its reference path \(Q(t)\), with
\(Q(t_0)=q_m=M_mR\).  Take \(x_0=0\) and the trajectory (1.3).

Write \(q=q_m=M_mR\).  Throughout this section,

\[
 M_m\ge64,\qquad q\le\frac1{32},\qquad 0<R<R_E,
\tag{6.1a}
\]

where \(R_E\) is the minimum of the already frozen R0.74D chart constant
\(R_1\), \(2^{-11}\), and the two compact heat-kernel continuity thresholds
used in Lemma 6.1.  This fixes, rather than silently shrinks, the admissible
range for every statement in this section.  Since \(u_3=0\),

\[
 X_{R,3}(t)=0.
\tag{6.2}
\]

The first component of \(X_R\) does not affect the translated profile or any
frozen functional because the entire field is independent of \(x_1\).
Define the exact multiplier

\[
 \mu_R=\int_{\mathbb T^3}\varphi_R^{\rm per}(y)\cos y_3\,dy.
\tag{6.3}
\]

The support condition in (1.1) gives the explicit bound

\[
 0\le1-\mu_R
 =\int\varphi_R^{\rm per}(y)(1-\cos y_3)\,dy
 \le\frac{R^2}{2}.
\tag{6.4}
\]

The second component of (1.3) is therefore

\[
 \dot X_{R,2}=\mu_RB_Re^{-t},\qquad X_{R,2}(t_0)=0,
\tag{6.5}
\]

and the R0.74D endpoint identities imply

\[
 \boxed{X_{R,2}(t)=\mu_R\,[Q(t)-q_m].}
\tag{6.6}
\]

Consequently the reference-coordinate offset in the translated profile is

\[
 \boxed{
 q_R(t)=Q(t)-X_{R,2}(t)
       =\mu_Rq_m+(1-\mu_R)Q(t)
       =q_m+O_\varphi(R^2).}
\tag{6.7}
\]

Uniformly on \(I_{8R}\),

\[
 0\le q_R(t)-q\le\frac{R^2}{4}\le\frac{R}{8192}.
\tag{6.8}
\]

Thus the R0.74D reference path no longer crosses the local origin: its
translated offset is \(M_mR+O(R^2)\) throughout the payment window.  This
identity alone does not locate the diffused mass; Lemma 6.1 supplies the
separate analytic residence statement.

### Lemma 6.1 — residence on the whole payment interval

There are fixed \(1<b_1<b_2<2\) and \(c_0>0\) such that, for every
parameter triple satisfying (6.1a),

\[
 |G(t,z,x_3)|\ge c_0
\tag{6.9}
\]

for every \(t\in I_{2R}=(61R^2,65R^2)\), \(|x_3|\le R\), and either

\[
 b_1R\le z\le b_2R
 \quad\hbox{or}\quad
 -b_2R\le z\le-b_1R.
\tag{6.10}
\]

The two lobes have opposite signs.

**Proof.**  The proof of R0.74D Lemma 3.1 applies without the final
fixed-centre restriction.  In the reference-centred variable \(G\), the
dimensionless heat age satisfies

\[
 62\le\frac{R^2+t}{R^2}\le66
 \qquad(t\in I_{2R}).
\tag{6.11}
\]

On this compact interval, the two real-Gaussian derivative lobes have a
strict positive minimum after \(b_1,b_2\) are fixed.  The nonautonomous
displacement error remains \(O(R)\) by the same weighted first-moment bound,
and noncentral periodic images are \(O(e^{-c/R^2})\).  Shrinking \(R\)
absorbs both errors.  Oddness of the central derivative kernel supplies the
opposite signs. \(\square\)

Define the translated lobe sets

\[
 \Omega_\pm(t)=\left\{y:\ |y_1|<\frac q8,\quad
 y_2-q_R(t)\in\pm[b_1R,b_2R],\quad |y_3|<R\right\}.
\tag{6.12}
\]

They lie in the same physical shell viewed at the two ledger radii:

\[
 A_m(R)=A_{m-1}(2R)
 =\left\{\frac{2q}{3}\le|y|<\frac{4q}{3}\right\}.
\tag{6.13}
\]

Indeed, on the negative lobe
\(y_2\ge q-2R\ge31q/32>2q/3\), while on both lobes

\[
 \frac{|y|}{q}
 \le\left[\left(\frac18\right)^2
 +\left(1+\frac{2+1/8192}{64}\right)^2
 +\left(\frac1{64}\right)^2\right]^{1/2}
 <\frac43.
\tag{6.14}
\]

Moreover, \(|\Omega_\pm(t)|\ge c qR^2=cM_mR^3\).  Thus the old target does not
disappear or change shell.  It becomes resident throughout \(I_{2R}\).

### Lemma 6.2 — packet upper bound for the moved ledger

Let \(X_{R,F}^M\) denote the contribution of the \(AF\) component to
\(X_R^M\).  Then

\[
 \boxed{X_{R,F}^M\le C\frac{A^2R^2}{M_m^3}.}
\tag{6.15}
\]

**Proof.**  After integrating the invariant \(y_1\)-direction and every
periodic copy, the R0.74D all-copy weight lemma gives

\[
 \omega_R(y_2,y_3)
 \le\frac{CR^4}
 {({\rm dist}_{\mathbb T^2}((y_2,y_3),0)^2+R^2)^{3/2}}.
\tag{6.16}
\]

Put \(\rho={\rm dist}_{\mathbb T^2}((y_2,y_3),0)\), and write the translated
packet profile as

\[
 H(t,y_2,y_3)=G(t,y_2-q_R(t),y_3).
\tag{6.17}
\]

On \(\rho\ge q/2\), (6.16), \(L^2\) contraction, and the global energy
identity give

\[
 \|F(t)\|_2^2\le CR^2,
 \qquad
 \int_{I_R}\|\nabla F(t)\|_2^2dt\le CR^2.
\tag{6.18}
\]

Consequently,

\[
\begin{aligned}
 &R^{-1}\mathop{\rm ess\,sup}_{I_R}
   \int_{\rho\ge q/2}\omega_R|H|^2
 +R^{-1}\int_{I_R}\!\int_{\rho\ge q/2}
   \omega_R|\nabla H|^2\\
 &\qquad\le C\frac{R^2}{M_m^3}.
\end{aligned}
\tag{6.19}
\]

On \(\rho<q/2\), the central lift obeys
\(z=y_2-q_R(t)\le-q/2<0\).  In the stochastic formula from R0.74D, the
residual displacement is nonpositive and its starting-point derivative is
bounded.  Applying the derivative-kernel estimates directly to that formula
gives

\[
 \boxed{
 |H|+R|\nabla H|
 \le C(1+M_m)^6e^{-M_m^2/1056}.}
\tag{6.20}
\]

For completeness, the exponent is the central Gaussian bound with
\(|z|\ge M_mR/2\) and heat age at most \(66R^2\); differentiated terms use
the exact path derivative formula from R0.74D (4.13).  Noncentral periodic
images are smaller because (6.1a) keeps the calculation in the central
chart.  Since \(\int\omega_R\le CR^3\), (6.20) gives

\[
 R^{-1}\mathop{\rm ess\,sup}_{I_R}
   \int_{\rho<q/2}\omega_R|H|^2
 +R^{-1}\int_{I_R}\!\int_{\rho<q/2}
   \omega_R|\nabla H|^2
 \le C\frac{R^2}{M_m^3}.
\tag{6.21}
\]

Here the polynomial times the Gaussian is absorbed uniformly for
\(M_m\ge64\).  Equations (6.19) and (6.21), multiplied by \(A^2\), prove
(6.15).  The all-copy weight (6.16) includes every periodic image.
\(\square\)

### Lemma 6.3 — compulsory harmonic payment for residence

Let \(\mathcal H_{F}^{M,R}\) denote the contribution of the packet to the
algebraic harmonic functional at scale \(S=2R\).  Then

\[
 \boxed{
 \mathcal H_F^{M,R}
 \ge c\frac{A^3R^3}{M_m^{9/2}},
 \qquad
 (\mathcal H_F^{M,R})^{2/3}
 \ge c\frac{A^2R^2}{M_m^3}.}
\tag{6.22}
\]

**Proof.**  On the shell (6.13), the coefficient in

\[
 \Lambda_{2R}(t)
 =2R\sum_{j\ge1}(2^j2R)^{-4}
   \int_{A_j(2R)}|\widetilde v_R|^2
\tag{6.23}
\]

has the exact coefficient

\[
 2R(2^mR)^{-4}=\frac{81}{8}Rq^{-4}
\tag{6.24}
\]

on \(A_{m-1}(2R)\).  Lemma 6.1 supplies packet amplitude \(cA\) on
\(\Omega_+(t)\), of volume \(cM_mR^3\), for every time in \(I_{2R}\).
Therefore

\[
 \Lambda_{2R,F}(t)\ge c\frac{A^2}{M_m^3}.
\tag{6.25}
\]

Multiplying its \(3/2\) power by \(2R|I_{2R}|=8R^3\) proves (6.22).
\(\square\)

In particular, the R0.74D exponentially weighted target block is now paid:

\[
 \frac{A^2M_mR^2e^{-M_m^2/288}}
      {(\mathcal H_F^{M,R})^{2/3}}
 \le CM_m^4e^{-M_m^2/288}\longrightarrow0.
\tag{6.26}
\]

### Proposition 6.4 — complete familywise neutralization in Version M

For every member of the R0.74D exact family and every admissible
\((A,R,m)\),

\[
 \boxed{
 X_R^M\le C(P_R^M)^{2/3}.}
\tag{6.27}
\]

The constant depends only on the frozen mollifier and harmless chart
constants, not on \(A,R,m\).

**Proof.**  The shear component gives

\[
 X_{R,b}^M\le CR^{-2}.
\tag{6.28}
\]

Because it is nonzero on a fixed fraction of the first few shells,

\[
 \mathcal H_b^{M,R}\ge cR^{-3},
 \qquad (\mathcal H_b^{M,R})^{2/3}\ge cR^{-2}.
\tag{6.29}
\]

The two velocity components are orthogonal pointwise, so their quadratic
contributions add.  Lemmas 6.2--6.3 and the elementary comparability of
\((x+y)^{2/3}\) with \(x^{2/3}+y^{2/3}\) give

\[
 X_R^M\le C\left[R^{-2}+\frac{A^2R^2}{M_m^3}\right]
 \le C(\mathcal H_{v_R}^{M,R})^{2/3}.
\tag{6.30}
\]

At the \(\Lambda\) level, the two pointwise-orthogonal components add.
Since \((x+y)^{3/2}\ge x^{3/2}+y^{3/2}\), their separate lower bounds
combine; then concavity gives comparability of the two \(2/3\) powers.
Since \(\mathcal H_{v_R}^{M,R}\le P_R^M\), (6.27) follows. \(\square\)

This theorem says that the explicit family which disproved Version A does
not disprove Version M.  It says nothing about arbitrary Navier--Stokes
solutions.

### Proposition 6.5 — the same family is also paid after local subtraction

For the Version-F field \(w_R=v_R-a_R\), the kinematic part of the frozen
ledger satisfies

\[
 \boxed{
 X_R^F\le C(P_R^F)^{2/3}}
\tag{6.31}
\]

for the entire R0.74D family, provided the nonnegative acceleration rows
required in (4.13)--(4.16) are retained.

**Proof.**  The first-component local mean is sampled at distance at least
\((M_m-2)R\) from the packet.  The buffered Gaussian bound gives

\[
 |a_{R,1}(t)|
 \le CA(1+M_m)^6e^{-M_m^2/528}
 \le C\frac A{M_m^{3/2}}.
\tag{6.32}
\]

This is the translated version of the R0.74D buffered bound, because the
support of \(\varphi_R\) stays at least \((M_m-2)R\) from the reference
lobes.  Its constant contribution to \(X_R^F\) is at most

\[
 Ca_{R,1}^2R^2\le C\frac{A^2R^2}{M_m^3}.
\tag{6.33}
\]

More importantly, let \(g_+\ge c_0\) and \(g_-\le-c_0\) be values at
matched points of the two lobe sets.  For every spatial constant \(\alpha\),

\[
 |g_+-\alpha|^2+|g_--\alpha|^2
 \ge\frac12|g_+-g_-|^2\ge2c_0^2.
\tag{6.34}
\]

Thus subtraction of \(a_{R,1}(t)/A\) cannot cancel both lobe sets, and the
packet lower bound (6.22) remains valid for \(w_{R,1}\).

The residual shear is

\[
 w_{R,2}=B_Re^{-t}(\cos y_3-\mu_R).
\tag{6.35}
\]

Near the origin,
\(|\cos y_3-\mu_R|\le(y_3^2+R^2)/2\).  The exact dyadic moments satisfy

\[
 \int_{\mathbb R^3}W_R(y)|y_3|^{2k}\,dy
 \le C_kR^{3+2k},\qquad k=0,1,2.
\tag{6.36}
\]

Together with \(|\partial_3w_{R,2}|\le|B_Ry_3|\) in the central chart and
the super-Gaussian control of all other lifts, (6.36) gives

\[
 X_{R,w_2}^F\le CR^2.
\tag{6.37}
\]

The required all-copy algebraic lower is separate from the Gaussian moment
upper.  For \(S=2R\), define

\[
 \ell_S^{(1)}(s)
 =\sum_{n\in\mathbb Z}\int_{\mathbb R^2}
 L_S(y_1,y_2,s+2\pi n)\,dy_1dy_2.
\tag{6.38}
\]

For \(s\in[1,3/2]\), restrict the central copy to
\(y_1^2+y_2^2<1/16\).  There \(|y|\asymp1\), so the exact dyadic definition
of \(L_S\) yields

\[
 \ell_S^{(1)}(s)\ge cS=cR.
\tag{6.39}
\]

Also \(\mu_R\ge1-R^2/2\), while \(\cos s\le\cos1\), hence
\(|\cos s-\mu_R|\ge c\).  On \(I_{2R}\),
\(e^{-t}\ge e^{-65R_E^2}>0\).  Since \(|B_R|\asymp R^{-2}\),

\[
 \Lambda_{2R,w_2}(t)\ge cR|B_R|^2\ge cR^{-3},
 \qquad
 \mathcal H_{w_2}^{F,R}\ge cR^{-3/2}.
\tag{6.40}
\]

Consequently,

\[
 (\mathcal H_{w_2}^{F,R})^{2/3}\ge cR^{-1}.
\tag{6.41}
\]

The packet estimates and (6.32)--(6.41) yield

\[
 X_R^F\le C\left[R^2+\frac{A^2R^2}{M_m^3}\right]
 \le C(\mathcal H_{w_R}^{F,R})^{2/3}
 \le C(P_R^F)^{2/3}.
\tag{6.42}
\]

Every acceleration payment is nonnegative and only strengthens the last
inequality. \(\square\)

Proposition 6.5 is a familywise algebraic statement.  It does not turn the
time-dependent subtraction into an unforced periodic symmetry and does not
prove the arbitrary-solution endpoint (4.17).

---

## 7. Why the first high-frequency cosine repair is rejected

A natural attempt is

\[
 b_k(t,x_3)=Be^{-k^2t}\cos(kx_3),
 \qquad k\in\mathbb N,
\tag{7.1}
\]

with a packet layer at \(h\) chosen so that \(kh=2\).  To respect the
periodic Fourier constraint exactly, choose integers \(k_m\to\infty\) and
define

\[
 R_m=\frac4{M_mk_m},\qquad
 h_m=\frac2{k_m}=\frac{M_mR_m}{2},
 \qquad k_mR_m=\frac4{M_m}.
\tag{7.2}
\]

For example, taking
\(k_m=\lceil4e^{M_m^2/96}/M_m\rceil\) recovers
\(R_m\asymp e^{-M_m^2/96}\) without requiring a noninteger torus mode.

The mollified centre sees the multiplier \(\widehat\varphi(kR)\to1\),
whereas the packet layer sees \(\cos2<0\).  Choosing \(B\asymp R^{-2}\)
would indeed create order-one relative displacement in a time of order
\(R^2\).  Exactness and zero global mean are not the problem.

In packet-centred parabolic variables

\[
 \tau=\frac{t-t_*}{R^2},\qquad
 \xi=\frac{x_2-Q(t)}R,\qquad
 \zeta=\frac{x_3-h}R,
\tag{7.3}
\]

the first transverse Taylor term in the residual drift has coefficient

\[
 \boxed{
 \mathfrak s_1=|B|kR^2|\sin(kh)|\asymp k
 =\frac4{M_mR_m}\longrightarrow\infty.}
\tag{7.4}
\]

Equivalently, a transverse Brownian displacement of size \(R\) over time
\(R^2\) produces a horizontal displacement of order

\[
 |B|k_mR_m^3\asymp k_mR_m=\frac4{M_m},
\tag{7.5}
\]

which is exponentially larger than both the packet width \(R\) and the
target radius \(M_mR\) along the R0.74D exponential sequence.

Moving the packet to the negative extremum removes the linear term.  In that
variant take \(k_mh_m=\pi\) and
\(R_m=2\pi/(M_mk_m)\).  The quadratic scaled coefficient is then

\[
 \boxed{
 \mathfrak s_2=|B|k^2R^3\asymp k^2R
 \asymp\frac1{M_m^2R_m}\longrightarrow\infty.}
\tag{7.6}
\]

Hence the required scale-\(R\) heat-packet survival cannot be obtained by
treating this residual drift as a uniformly controlled perturbation.  This
specific single-mode mechanism is **REJECTED**.  Equations (7.4)--(7.6) do
not prove that every nonperturbative single-mode construction fails.

---

## 8. Symmetric separated plateaus: exact family, failed exponent gate

The failure in Section 7 suggests two opposite velocity plateaus, each flat
on a transverse neighbourhood wider than \(R\).  The first exact attempt is
as follows.  Let \(\eta\in C_c^\infty((-1,1))\) be even, nonnegative, and
equal to one on \([-1/2,1/2]\).  Put

\[
 h=\frac{M_mR}{2},\qquad \delta=\frac{M_mR}{16},
 \qquad M_m\ge64,\qquad M_mR\le\frac1{32}.
\tag{8.1}
\]

Define the periodized mean-zero profile

\[
 g_{R,m}(x_3)
 =\eta(x_3/\delta)-\eta((x_3-h)/\delta).
\tag{8.2}
\]

The supports are disjoint and stay in the central torus chart, and the two
terms have exactly equal integrals.  At time zero,

\[
 (\varphi_R^{\rm per}*g_{R,m})(0)=1,
 \qquad
 (\varphi_R^{\rm per}*g_{R,m})(h)=-1.
\tag{8.3}
\]

Let

\[
 b(t,x_3)=B\,e^{t\partial_3^2}g_{R,m}(x_3),
\tag{8.4}
\]

and let a zero-mean scalar solve

\[
 \partial_tF+b\partial_2F
 =\partial_2^2F+\partial_3^2F.
\tag{8.5}
\]

Then

\[
 \boxed{u=(AF,b,0),\qquad p=0}
\tag{8.6}
\]

is exact smooth periodic unforced mean-zero 2D3C Navier--Stokes.  This is
**PROVED**.  At positive time there is no exact plateau: heat propagation is
instantaneous.

### Proposition 8.1 — the midpoint perturbative window is empty

Retain the old target weight \(e^{-M_m^2/288}\) and write

\[
 R=e^{-c_RM_m^2}.
\tag{8.7}
\]

The fast-residence packet cubic row has formal scale
\(A^3R^4/M_m^2\).  The target can dominate its \(2/3\) power only if

\[
 c_R>\frac1{192}.
\tag{8.8}
\]

For (8.2), the remote layer is only
\(d=\delta/2=M_mR/32\) from the edge of its initial plateau.  The direct
heat-kernel isolation exponent over \(65R^2\) is at most

\[
 \frac{d^2}{4(65R^2)}=\frac{M_m^2}{266240}.
\tag{8.9}
\]

Making the resulting order-\(B\) velocity oscillation smaller than one
packet width over time \(R^2\) by this direct perturbative estimate would
require

\[
 c_R<\frac1{266240}.
\tag{8.10}
\]

Equations (8.8) and (8.10) are incompatible.  Hence this **specific
midpoint two-bump perturbative survival mechanism is rejected**.  This is
not a universal no-go for signed caloric cancellation or for every plateau
geometry, and it does not invalidate the exact family (8.6).

---

## 9. Odd paired-stream outer-annulus gate

The exponent loss can be reduced by moving the target near the outer edge of
its dyadic annulus and keeping the nearest transition almost one target
radius away from each remote layer.  Odd inversion symmetry also removes the
Version-F acceleration exactly.

### 9.1 Frozen rational geometry

Fix

\[
 \lambda=\frac{63}{32},\qquad
 c_h=\frac{15}{16},\qquad
 \alpha=\frac{14}{15},\qquad
 \beta=\frac{\sqrt{31}}{16},\qquad
 c_R=\frac1{320}.
\tag{9.1}
\]

For integers \(j\to\infty\), set

\[
 L_j=\lambda2^j,\qquad
 R_j=e^{-c_RL_j^2},\qquad
 r_j=L_jR_j,
\tag{9.2}
\]

\[
 h_j=c_hr_j,qquad q_j=\beta r_j.
\tag{9.3}
\]

Then

\[
 c_h^2+\beta^2=1,
 \qquad |(q_j,h_j)|=r_j,
\tag{9.4}
\]

and \(r_j\in(2^jR_j,2^{j+1}R_j)\).  The annular weight is

\[
 \gamma_j
 =\exp\!\left[-\frac{L_j^2}{128\lambda^2}\right],
 \qquad
 c_\gamma=\frac1{128\lambda^2}=\frac8{3969}.
\tag{9.5}
\]

The exact rational exponent window is

\[
 \boxed{
 \frac{3}{256\lambda^2}=\frac4{1323}
 <\frac1{320}
 <\frac{\alpha^2}{260}=\frac{49}{14625}.}
\tag{9.6}
\]

The left inequality is the packet-\(G_u\) dominance gate; the right is the
direct \(65R_j^2\) caloric-isolation gate once the nearest transition is at
least \(\alpha r_j\) away.  Since
\(c_h-\alpha=1/240\), the explicit profile below has this separation as soon
as \(L_j\ge7680\).  There is also a transverse local-leakage
margin,

\[
 \frac{c_h^2}{264}=\frac{75}{22528}
 >\frac1{320}=c_R
 >\frac8{3969}=c_\gamma.
\tag{9.7}
\]

These finite inequalities are **PROVED**.  They are not a packet-survival
theorem.  Their exact-arithmetic certificate and human-readable report are

- `scripts/r074e_outer_annulus_exponent_certificate.py`;
- `research/r074e_outer_annulus_exponent_certificate.json`; and
- `research/r074e_outer_annulus_exponent_certificate_report.md`.

The certificate checks only the finite rational identities and strict
inequalities in (9.1)--(9.7).  It does not certify any subsequent analytic
survival, leakage, pressure, or endpoint statement.

### 9.2 Exact odd shear and paired passive field

Fix an odd smooth saturation \(\sigma\in C^\infty(\mathbb R;[-1,1])\)
with \(\sigma(s)=\operatorname{sgn}s\) for \(|s|\ge1\), and fix
\(\kappa=16\).  Define

\[
 g_j(x_3)=\sigma\!\left(\frac{\sin x_3}{\kappa R_j}\right),
 \qquad
 \theta_j(t,x_3)=e^{t\partial_3^2}g_j(x_3),
 \qquad
 b_j(t,x_3)=B_j\theta_j(t,x_3).
\tag{9.8}
\]

Set

\[
 t_{-,j}=R_j^2,
 \qquad t_{0,j}=65R_j^2.
\tag{9.8a}
\]

The positive amplitude \(B_j\) and the entrance point
\(q_{{\rm pre},j}\) are fixed by the exact formulas (9.17) and (9.19)
below, respectively.

The function \(g_j\) is smooth, periodic, odd, and mean zero.  It is exactly
constant away from \(O(R_j)\) neighbourhoods of \(0\) and the torus seam;
heat evolution preserves oddness.

Let \(K^{\rm per}\) be the periodic heat kernel.  The entrance point
\(q_{{\rm pre},j}\) is fixed by the exact calibration (9.19) below.
Prescribe

\[
\begin{aligned}
 F_j(0,x_2,x_3)=R_j^3\bigl[&
 \partial_2K_{R_j^2}^{\rm per}(x_2-q_{\rm pre,j})
 K_{R_j^2}^{\rm per}(x_3-h_j)\\
 &+\partial_2K_{R_j^2}^{\rm per}(x_2+q_{\rm pre,j})
 K_{R_j^2}^{\rm per}(x_3+h_j)\bigr],
\end{aligned}
\tag{9.9}
\]

and evolve it by

\[
 \partial_tF_j+b_j\partial_2F_j=\Delta_{23}F_j.
\tag{9.10}
\]

The initial datum satisfies

\[
 F_j(0,-x_2,-x_3)=-F_j(0,x_2,x_3).
\tag{9.11}
\]

Uniqueness and oddness of \(b_j\) preserve (9.11).  Hence every even radial
mollifier gives

\[
 (\varphi_{R_j}^{\rm per}*F_j)(t,0)=0,
 \qquad
 (\varphi_{R_j}^{\rm per}*b_j)(t,0)=0.
\tag{9.12}
\]

The field

\[
 \boxed{u_j=(\mathfrak a_jF_j,b_j,0),\qquad p_j=0}
\tag{9.13}
\]

is exact smooth periodic unforced mean-zero NSE.  Put

\[
 z_{0,j}=(t_{0,j},0).
\tag{9.13a}
\]

Its mollified trajectory terminally anchored at the basepoint \(z_{0,j}\)
is exactly

\[
 \boxed{X_{R_j}(t)\equiv0,qquad a_{R_j}(t)=a_{R_j}'(t)=0.}
\tag{9.14}
\]

Thus Versions M and F coincide and every acceleration row vanishes.  These
symmetry and NSE statements are **PROVED**.

### 9.3 Exact calibration and remaining gates

The notation entering the terminal basepoint is therefore

\[
 I_{R_j}=(64R_j^2,65R_j^2),
 \qquad I_{2R_j}=(61R_j^2,65R_j^2).
\tag{9.15}
\]

### Lemma 9.1 — exact contrast calibration

For all sufficiently large \(j\),

\[
 1-Ce^{-\alpha^2L_j^2/260}
 \le\theta_j(t,h_j)\le1
 \qquad(0\le t\le t_{0,j}).
\tag{9.16}
\]

Consequently, with \(q_*=1/2\),

\[
 \mathfrak D_j
 =\int_{t_{-,j}}^{t_{0,j}}\theta_j(t,h_j)\,dt,
 \qquad
 B_j=\frac{q_j+q_*}{\mathfrak D_j},
\tag{9.17}
\]

one has

\[
 cR_j^{-2}\le B_j\le CR_j^{-2}.
\tag{9.18}
\]

If

\[
 q_{{\rm pre},j}
 =-q_*-B_j\int_0^{t_{-,j}}\theta_j(t,h_j)\,dt,
\tag{9.19}
\]

then the reference path

\[
 Q_j(t)=q_{{\rm pre},j}
 +B_j\int_0^t\theta_j(s,h_j)\,ds
\tag{9.20}
\]

satisfies the exact endpoint identities

\[
 Q_j(t_{-,j})=-q_*,\qquad Q_j(t_{0,j})=q_j.
\tag{9.21}
\]

The inverted layer has path \(-Q_j(t)\).

**Proof.**  The transition set of \(g_j\) nearest \(h_j\) is contained in
\(|x_3|\le\arcsin(\kappa R_j)\).  For large \(j\),

\[
 \arcsin(\kappa R_j)\le2\kappa R_j=32R_j.
\tag{9.22}
\]

Since \(c_h-\alpha=1/240\) and \(L_j\ge7680\), the periodic distance from
\(h_j\) to that transition is at least

\[
 (c_hL_j-32)R_j\ge\alpha r_j.
\tag{9.23}
\]

The seam transition is a fixed positive distance farther away.  At \(t=0\),
\(\theta_j(0,h_j)=1\) exactly.  For \(0<t\le t_{0,j}\), since
\(-1\le g_j\le1\), the periodic heat-kernel representation and the Gaussian
tail bound give

\[
 0\le1-\theta_j(t,h_j)
 \le C\exp\!\left[-\frac{\alpha^2r_j^2}{4t}\right]
 \le Ce^{-\alpha^2L_j^2/260}.
\tag{9.24}
\]

This proves (9.16).  Hence

\[
 64R_j^2(1-o(1))\le\mathfrak D_j\le64R_j^2.
\tag{9.25}
\]

Because \(q_j\to0\), (9.18) follows.  Equations (9.19)--(9.21) are direct
substitution.  Oddness gives the inverted path. \(\square\)

The following are still **OPEN**:

1. a two-packet Feynman--Kac survival lemma uniform in \(j\);
2. buffered local leakage using the strict margin (9.7);
3. every transition, packet, mixed-pressure, and periodic-copy row;
4. an explicit \(\mathfrak a_j\) closing the complete Version-M/F ratio.

No divergence theorem is claimed at this gate.  A same-amplitude packet at
the tracked centre would cost \(\mathcal E\asymp\mathfrak a_j^2R_j^2\), so the
centre must remain the background odd-shear branch, as in (9.14).

---

## 10. Prior-art and claim boundary

Mollified trajectories, local Galilean changes of frame, mean-free
transformed velocities, affine pressure rewrites on Euclidean lifts, and
skewed cylinders are established mechanisms in the
Vasseur--Choi--Yang line of work.  Periodic 2D3C reduction and
time-dependent shear passive transport are also prior art.  R0.74E makes no
priority claim for any of those components.

The exact local-frame identities above are frozen to prevent an invalid
transfer of the R0.74D ledger.  Any later theorem must distinguish:

- a torus-compatible moved-only observable;
- a mean-subtracted observable with explicit acceleration payment; and
- a fixed-centre observable with explicit entrance flux.

These are different mathematical statements.  None currently proves a
regularity criterion, an epsilon-regularity theorem, a continuation theorem,
or global smoothness.  **NOT CLAY.**

---

## 11. Frozen audit ledger

### PROVED

1. The common terminal trajectory and its periodic lift are well defined for
   smooth solutions.
2. The general transformation identity (2.2).
3. Version M has periodic pressure and residual transport but no body force.
4. Version F has canonical convection and the explicit force \(-a_R'\).
5. A nonzero acceleration cannot be absorbed into periodic torus pressure.
6. The matching mollifier gives an automatic exact acceleration
   cancellation.
7. Different radii on one trajectory do not automatically inherit that
   cancellation.
8. The R0.74D translated reference offset is \(q_m+O(R^2)\), and the
   separate two-lobe estimate proves actual residence on \(I_{2R}\).
9. The R0.74D family satisfies the uniform Version-M bound (6.27).
10. The same family satisfies the Version-F familywise bound (6.31), with
    the acceleration rows retained.
11. The proposed high-frequency cosine has divergent rescaled shear at the
   packet layer.
12. The separated-plateau family (8.6) is exact smooth mean-zero NSE.
13. The midpoint two-bump perturbative exponent window is empty.
14. The rational outer-annulus window (9.6)--(9.7) is nonempty.
15. The odd paired-stream field (9.13) is exact mean-zero NSE and has
    identically zero mollified trajectory and acceleration.
16. Lemma 9.1 calibrates the paired reference paths exactly and proves
    \(B_j\asymp R_j^{-2}\).

### OPEN

1. The full Version-M endpoint (3.11).
2. The full Version-F endpoint (4.17) with every acceleration row.
3. The odd paired-stream packet-survival and complete payment ledger.
4. Any positive absorption or regularity consequence.

### REJECTED MECHANISM

The single high-frequency cosine with (7.2) cannot use the perturbative
scale-\(R\) packet-survival argument, because both (7.4) and the extremal
replacement (7.6) diverge.

The symmetric midpoint two-bump profile (8.2) also has no direct
heat-isolation exponent compatible with its required packet cubic row, by
(8.8)--(8.10).  Neither rejection is a universal no-go theorem.
