# R0.74D — zero-global-mean local-transport gate

## Status and scope

R0.74C shows that a constant spatial mean can advect a heat packet through a
fixed cylinder quickly enough to defeat the frozen large-payment endpoint.
Version A repairs that specific defect by subtracting the mean and translating
the cylinder.  It is not, by itself, the end of the transport audit: a
velocity with zero **global** mean can still have a large, coherent local
drift.  A fixed-centre entrance-flux payment remains a different possible
repair and is not assessed here.

This note freezes one exact family that isolates that second issue.  It is
not a restatement of Galilean invariance.  The family below has zero total
spatial mean at every time, so the constant-mean co-moving centre does not
move.  The exact Navier--Stokes construction is **PROVED**.  The heat-packet
survival estimate and every quantitative payment estimate needed to turn it
into a counterexample are **OPEN**.

Throughout,

\[
 \nu=1,\qquad \theta=1,
 \qquad \mathbb T^3=(-\pi,\pi]^3.
\tag{0.1}
\]

Labels are literal: **PROVED**, **TARGET**, **OPEN**, **FINITE**, and
**NOT CLAY**.  In particular, a formula labelled `TARGET/OPEN` is not a
theorem and is not evidence that the co-moving estimate fails.

---

## 1. Frozen scales and reference characteristic

Fix

\[
 q_*=\frac12,\qquad M_m=3\,2^{m-1},\qquad q_m=M_mR,
\tag{1.1}
\]

and

\[
 t_-=R^2,\qquad t_0=65R^2,\qquad T_R=66R^2.
\tag{1.2}
\]

In particular,

\[
 I_{8R}=(t_0-64R^2,t_0)=(R^2,65R^2),
 \qquad
 \overline{I_{8R}}=[R^2,65R^2]\Subset(0,T_R).
\tag{1.2a}
\]

As in R0.74C, the analytic regime to be tested is

\[
 0<R<R_0<\frac{\pi}{16},\qquad M_m\ge64,
 \qquad q_m=M_mR\le\frac{q_*}{16}.
\tag{1.3}
\]

Define

\[
 D_R=e^{-R^2}-e^{-65R^2}>0,
 \qquad
 B_R=\frac{q_m-q_*}{D_R},
\tag{1.4}
\]

and

\[
 q_{\rm pre}=q_*-B_R(1-e^{-R^2}).
\tag{1.5}
\]

The scalar transverse velocity is

\[
 b_R(t,x_3)=B_Re^{-t}\cos x_3.
\tag{1.6}
\]

The characteristic of (1.6) lying in the plane \(x_3=0\) has reference
position

\[
 Q_R(t)=q_{\rm pre}+B_R(1-e^{-t}).
\tag{1.7}
\]

The choices (1.4)--(1.5) give the exact endpoint identities

\[
 Q_R(t_-)=q_*,\qquad Q_R(t_0)=q_m.
\tag{1.8}
\]

These identities concern a reference characteristic.  Because the scalar
profile below also diffuses in \(x_3\), they do not by themselves locate the
mass or the \(L^2\) energy of that profile at time \(t_0\).

The mean-value theorem gives, for some
\(\xi_R\in(R^2,65R^2)\),

\[
 D_R=64R^2e^{-\xi_R},\qquad
 B_R=\frac{q_m-q_*}{64R^2}e^{\xi_R}.
\tag{1.9}
\]

Consequently, under (1.3),

\[
 |B_R|\le C_{R_0}R^{-2}.
\tag{1.10}
\]

The large velocity scale is therefore the same \(R^{-2}\) scale that drove
the constant-drift R0.74C witness, but its periodic spatial mean is zero.

---

## 2. Exact periodic family

Let

\[
 K_\tau^{\rm per}(z)
 =\frac1{\sqrt{4\pi\tau}}
  \sum_{n\in\mathbb Z}e^{-(z+2\pi n)^2/(4\tau)}
\tag{2.1}
\]

be the one-dimensional periodic heat kernel.  For \(A>0\), prescribe

\[
 f(0,x_2,x_3)
 =A R^3\,
   \partial_2K_{R^2}^{\rm per}(x_2-q_{\rm pre})
   K_{R^2}^{\rm per}(x_3),
\tag{2.2}
\]

and let \(f=f_{A,R,m}\) solve

\[
 \partial_tf+b_R\partial_2f
   =(\partial_2^2+\partial_3^2)f
 \quad\hbox{on }(0,T_R)\times\mathbb T^2.
\tag{2.3}
\]

Finally set

\[
 \boxed{
 u_{A,R,m}(t,x)=\bigl(f(t,x_2,x_3),b_R(t,x_3),0\bigr),
 \qquad p_{A,R,m}(t,x)=0.}
\tag{2.4}
\]

### Proposition 2.1 — exact, smooth, unforced, divergence-free, mean-zero NSE

For every fixed admissible triple \((A,R,m)\), (2.4) is a smooth periodic
solution of the unforced three-dimensional incompressible Navier--Stokes
equations on \([0,T_R]\times\mathbb T^3\).  Its total spatial mean is zero
at every time.

**Proof.**  The coefficient \(b_R\) and datum (2.2) are smooth and periodic.
Uniform parabolicity of (2.3) on the compact torus gives a unique smooth
periodic solution on the whole finite interval.  No limiting or weak-solution
argument is being used here.

The field (2.4) is divergence free because \(f\) is independent of \(x_1\)
and \(b_R\) is independent of \(x_2\):

\[
 \nabla\cdot u=\partial_1f+\partial_2b_R=0.
\tag{2.5}
\]

Its nonlinear term has only a first component,

\[
 (u\cdot\nabla)u=(b_R\partial_2f,0,0).
\tag{2.6}
\]

For the second component,

\[
 \partial_tb_R=-b_R=\partial_3^2b_R=\Delta b_R.
\tag{2.7}
\]

Equation (2.3), together with (2.6)--(2.7), therefore gives

\[
 \partial_tu-\Delta u+(u\cdot\nabla)u+\nabla p=0
\tag{2.8}
\]

pointwise, with \(p=0\).  Thus the solution is exact, periodic, smooth,
unforced, and three dimensional.  It is not a solution of a modified or
forced equation.

The second component has zero mean because
\(\int_{-\pi}^{\pi}\cos x_3\,dx_3=0\).  The first component initially has
zero mean because the \(x_2\)-integral of the derivative kernel vanishes.
Moreover, periodic integration of (2.3) yields

\[
 \frac{d}{dt}\int_{\mathbb T^2}f
 =-\int_{\mathbb T^2}b_R\partial_2f
   +\int_{\mathbb T^2}(\partial_2^2+\partial_3^2)f=0,
\tag{2.9}
\]

where \(b_R\) is independent of \(x_2\).  Hence

\[
 \overline u(t)
 :=\frac1{(2\pi)^3}\int_{\mathbb T^3}u(t,x)\,dx=0
 \quad(0\le t\le T_R).
\tag{2.10}
\]

This proves every assertion. \(\square\)

### What Proposition 2.1 does not prove

Proposition 2.1 proves the PDE identity and mean-zero property only.  It
does not show that the packet in (2.2) remains close to the reference
characteristic (1.7), and it gives no lower bound for an annular observable.

---

## 3. Version A: constant-global-mean co-moving observable

This section freezes the first repaired endpoint exactly.  For any smooth
periodic unforced Navier--Stokes solution, let

\[
 \bar u=\frac1{(2\pi)^3}\int_{\mathbb T^3}u(t,x)\,dx.
\tag{3.1}
\]

Periodic integration of NSE shows that \(\bar u\) is constant in time.
Given \(z_0=(t_0,x_0)\), set

\[
 x_c(t)=x_0+\bar u(t-t_0),
\tag{3.2}
\]

and introduce fixed co-moving coordinates

\[
 w(t,y)=u(t,y+x_c(t))-\bar u,
 \qquad \pi(t,y)=p(t,y+x_c(t)).
\tag{3.3}
\]

The pair \((w,\pi)\) again solves periodic NSE.  **Version A** means:
evaluate every frozen R0.74B standard-clock quantity on \((w,\pi)\), with
all balls and lifted annuli centred at \(y=0\).  Thus, for

\[
 I_\rho=(t_0-\rho^2,t_0),
 \qquad
 A_j(R)=\{2^jR\le|y|<2^{j+1}R\},
 \qquad
 \gamma_j=e^{-4^{j-1}/32},
\tag{3.4}
\]

put

\[
 \begin{aligned}
 \mathcal E^A(z_0,\rho)
 &=\rho^{-1}\mathop{\rm ess\,sup}_{I_\rho}
     \int_{B_\rho}|w|^2
   +\rho^{-1}\int_{I_\rho}\!\int_{B_\rho}|\nabla w|^2,\\
 U_\gamma^A(t)
 &=\sum_{j\ge1}\gamma_j\int_{A_j(R)}|\widetilde w(t,y)|^2\,dy,\\
 G_\gamma^A(t)
 &=\sum_{j\ge1}\gamma_j\int_{A_j(R)}
                 |\nabla\widetilde w(t,y)|^2\,dy,\\
 \mathcal U_{\rm ext}^{\infty,A}
 &=\mathop{\rm ess\,sup}_{I_R}R^{-1}U_\gamma^A(t),\\
 \mathcal D_{\rm ext}^A
 &=R^{-1}\int_{I_R}G_\gamma^A(t)\,dt.
 \end{aligned}
\tag{3.5}
\]

For completeness, retain the exact R0.73X/R0.74B pressure gauge and both
exterior-payment laws.  With the local pressure split at scale \(\rho\),
let

\[
 c_\rho^A(t)=(h_\rho^A(t,\cdot))_{B_{2\rho}},
\tag{3.6}
\]

and define

\[
 \begin{aligned}
 \mathcal G_{w,\pi}^A(z_0,\rho;1)
 &=\rho^{-2}\sum_{j\ge1}\gamma_j
   \int_{I_\rho}\!\int_{A_j(\rho)}
   \left(|\widetilde w|^3
   +|\widetilde\pi-c_\rho^A|^{3/2}\right)dy\,dt,\\
 \Lambda_\rho^A(t)
 &=\rho\sum_{j\ge1}(2^j\rho)^{-4}
   \int_{A_j(\rho)}|\widetilde w(t,y)|^2\,dy,\\
 \mathcal H_w^A(z_0,\rho)
 &=\rho\int_{I_\rho}(\Lambda_\rho^A(t))^{3/2}\,dt,\\
 \mathcal A_{\rm ext}^A(z_0,\rho;1)
 &=\mathcal G_{w,\pi}^A(z_0,\rho;1)
   +\mathcal H_w^A(z_0,\rho).
 \end{aligned}
\tag{3.7}
\]

Here \(A_j(\rho)\) is the annulus (3.4) with \(R\) replaced by \(\rho\),
and the periodic lift is centred at \(y=0\).  No pressure row is discarded
merely because a representative pressure happens to equal zero: the frozen
gauge \(c_\rho^A\) is still the one produced by the local pressure split.

The complete Version-A gate is

\[
 \boxed{
 X_R^A=\mathcal U_{\rm ext}^{\infty,A}+\mathcal D_{\rm ext}^A,
 \qquad
 P_R^A=\mathcal E^A(z_0,8R)^{3/2}
       +\mathcal A_{\rm ext}^A(z_0,2R;1).}
\tag{3.8}
\]

The all-solution endpoint under test is

\[
 \boxed{X_R^A\stackrel{?}{\le}C(P_R^A)^{2/3}.}
\tag{3.9}
\]

For the family (2.4), (2.10) gives \(\bar u=0\).  Taking \(x_0=0\),

\[
 x_c(t)=0,\qquad w=u,qquad \pi=p=0.
\tag{3.10}
\]

Thus the constant-global-mean repair does nothing to this family.  This
fact makes the family an admissible test of (3.9); it does **not** make the
family a counterexample to (3.9).

---

## 4. Why the local drift is perturbative only inside a tube

Move only with the reference characteristic (1.7), and parabolically
rescale.  For

\[
 t=R^2\sigma,\qquad
 x_2=Q_R(R^2\sigma)+Rz_2,\qquad x_3=Rz_3,
\tag{4.1}
\]

write

\[
 F(\sigma,z_2,z_3)
 =f(R^2\sigma,Q_R(R^2\sigma)+Rz_2,Rz_3).
\tag{4.2}
\]

An exact chain-rule calculation gives

\[
 \partial_\sigma F+a_R(\sigma,z_3)\partial_{z_2}F
 =(\partial_{z_2}^2+\partial_{z_3}^2)F,
\tag{4.3}
\]

where

\[
 a_R(\sigma,z_3)
 =RB_Re^{-R^2\sigma}\bigl(\cos(Rz_3)-1\bigr).
\tag{4.4}
\]

For each fixed \(L<\infty\), (1.10) and
\(|1-\cos y|\le y^2/2\) imply

\[
 \sup_{0\le\sigma\le66,\ |z_3|\le L}|a_R(\sigma,z_3)|
 \le C_{R_0}L^2R.
\tag{4.5}
\]

This is the exact source of the phrase “scaled residual drift \(O(R)\).”
It is a **local** statement on each fixed scaled tube.  Globally,

\[
 |a_R|\le2R|B_R|\lesssim R^{-1},
\tag{4.6}
\]

so (4.5) cannot be inserted into a global perturbation argument without a
tail analysis.  A proof must simultaneously control escape in \(z_3\), the
transport accumulated outside the tube, all periodic copies, and the
derivative sign changes of the packet.  Pointwise coefficient convergence
on compact \(z\)-sets is not such a proof.

---

## 5. Frozen target and complete analytic ledger

The annulus selected by \(M_m=3\,2^{m-1}\) has the exact weight identity

\[
 \gamma_m=e^{-4^{m-1}/32}=e^{-M_m^2/288}.
\tag{5.1}
\]

The intended packet-survival statement is

\[
 \boxed{
 X_R^A\ge
 cA^2M_mR^2e^{-M_m^2/288}.}
\tag{5.2}
\]

Equation (5.2) is **TARGET/OPEN**.  Neither Proposition 2.1 nor the compact
tube estimate (4.5) proves it.  In particular, (5.2) requires a quantitative
lower bound for the solution of the variable-coefficient parabolic equation
(2.3), not a formal characteristic calculation.

Any valid attempt to settle this candidate must keep the following ledger
complete.

### Gate T — target survival

Prove (5.2), with a constant uniform over the declared admissible parameter
regime, including the full periodic kernel and a time slice licensed by the
essential supremum in \(I_R\).

### Gate E — buffered local energy

Estimate both components and both gradient rows in

\[
 \mathcal E^A(z_0,8R)
 =\mathcal E^A[f](z_0,8R)
  +\mathcal E^A[b_R](z_0,8R),
\tag{5.3}
\]

where (5.3) is schematic notation for the exact quadratic expansion in
(3.5).  The \(b_R\), \(\partial_3b_R\), \(f\), \(\partial_2f\), and
\(\partial_3f\) contributions must all appear.  The locally large
zero-mean drift is not an ignorable background row.

### Gate \(G_u\) — Gaussian cubic velocity payment

Bound the full \(|(f,b_R,0)|^3\) integral in (3.7), on every lifted annulus
and over all periodic copies.  An estimate only for \(|f|^3\) or only for
\(|b_R|^3\) does not close this gate.

### Gate \(G_p\) — gauge-fixed pressure payment

Although the global pressure representative is \(p=0\), compute the frozen
local split and its gauge \(c_{2R}^A(t)\), then retain

\[
 (2R)^{-2}\sum_{j\ge1}\gamma_j
 \int_{I_{2R}}\!\int_{A_j(2R)}|c_{2R}^A(t)|^{3/2}\,dy\,dt.
\tag{5.4}
\]

Any Calderon--Zygmund or Jensen step used to control (5.4) remains an
analytic step; it is not supplied by exactness of the solution.

### Gate \(H_u\) — algebraic harmonic-pressure payment

Bound the full moment \(\Lambda_{2R}^A\) from (3.7), including the slowly
decaying annular contribution of \(b_R\), the packet contribution, and all
cross-regime parameter powers.  Gaussian localization cannot replace this
algebraic row.

### Gate P — one simultaneous denominator

Only after Gates E, \(G_u\), \(G_p\), and \(H_u\) are proved may their
bounds be combined into the single frozen denominator

\[
 P_R^A=\mathcal E^A(z_0,8R)^{3/2}
       +\mathcal G_{w,\pi}^A(z_0,2R;1)
       +\mathcal H_w^A(z_0,2R).
\tag{5.5}
\]

A favourable estimate obtained after omitting any one row is not evidence
about (3.9).

All five gates are **OPEN** beyond the exact identities already displayed.

---

## 6. The exhaustive two-way endpoint for this candidate

Let \(\mathfrak F_D\) be the family (2.4) over all triples satisfying
(1.3) and \(A>0\), and define the finite positive ratio

\[
 \mathscr R_D(A,R,m)=\frac{X_R^A}{(P_R^A)^{2/3}}.
\tag{6.1}
\]

R0.74D ends only after one of the following mutually exclusive statements
has been proved with the full ledger in Section 5.

### Endpoint D1 — ratio divergence

Construct an explicit admissible sequence \((A_k,R_k,m_k)\) and prove

\[
 \mathscr R_D(A_k,R_k,m_k)\longrightarrow\infty.
\tag{6.2}
\]

This would disprove the all-solution Version-A estimate (3.9).  At present
(6.2) is **OPEN**.  The family is a candidate, not a counterexample.

### Endpoint D2 — uniform survival against this family

Prove

\[
 \sup_{(A,R,m)\in\mathfrak F_D}\mathscr R_D(A,R,m)<\infty.
\tag{6.3}
\]

This would close this particular candidate obstruction and show that the
constant-global-mean endpoint survives the entire frozen family.  It would
not prove (3.9) for arbitrary smooth or suitable solutions.  At present
(6.3) is also **OPEN**.

The dichotomy (6.2)--(6.3) is deliberately stronger than reporting a few
numerical parameter values.  Numerical experiments may guide the estimates,
but they do not decide either infinite-parameter statement.

---

## 7. Prior-art and attribution boundary

The underlying mechanisms are not new claims.  Galilean reductions,
subtraction of a local or mollified mean, flow-following trajectories, and
skewed parabolic cylinders already occur in the Vasseur--Choi--Yang line of
work.  In particular:

1. Vasseur (2010) performs local changes of frame along a mollified flow;
2. Choi--Vasseur (2014) combine Galilean trajectory scaling with mean-zero
   reductions and explicitly discuss fast flow escaping a fixed cylinder;
3. Yang (2022) develops maximal functions for skewed cylinders generated by
   incompressible flows; and
4. Vasseur--Yang (2021) use zero-mean local analysis and skewed cylinders for
   suitable solutions.

The precise references and claim-by-claim source audit are recorded in
`research/r074c_primary_literature_audit.md`.  Accordingly, this note must
not claim the first local-transport obstruction, the first moving cylinder,
the first zero-mean reduction, or the first use of a flow-following frame.

The only frozen research question here is narrower: does the explicit
zero-total-mean periodic family (2.4) make the **specific** Version-A
R0.74B ratio (6.1) diverge after every frozen payment row is retained, or
does that ratio remain uniformly bounded on this family?  No novelty or
priority conclusion follows from posing that question.

---

## 8. Audit ledger

### PROVED

1. The parameters (1.1)--(1.6) are finite for every fixed admissible
   \((R,m)\), and (1.8) is exact.
2. The linear problem (2.2)--(2.3) has a smooth periodic solution on the
   full interval \([0,T_R]\).
3. Equation (2.4) is an exact smooth periodic unforced divergence-free
   three-dimensional Navier--Stokes solution with \(p=0\).
4. The full velocity, not merely its first component, has zero total spatial
   mean for every time.
5. Version A is defined by the exact constant-global-mean Galilean transform
   and the complete R0.74B target and payment rows.
6. For (2.4), Version A has a stationary centre because \(\bar u=0\).
7. In reference-characteristic variables, the residual drift is \(O(R)\)
   on every fixed scaled \(x_3\)-tube, as quantified in (4.5).
8. The selected annular weight satisfies the exact identity (5.1).

### TARGET/OPEN

1. The annular lower bound (5.2).
2. A global quantitative packet-survival theorem upgrading (4.5).
3. Uniform upper bounds for every row in Gates E, \(G_u\), \(G_p\), and
   \(H_u\).
4. An explicit parameter sequence proving (6.2), or a uniform estimate
   proving (6.3).
5. Any conclusion about local-flow trajectories or stronger skewed-cylinder
   observables after Version A.

### FINITE

For each fixed admissible triple, the solution is smooth on a compact
periodic domain and all positive-scale quantities in (3.8) are finite.
There is no asserted uniform energy bound as the parameters vary.

### NOT CLAY

This note freezes an exact smooth test family and an open positive-scale
estimate.  It proves no singularity, no blow-up, no epsilon-regularity
criterion, and no global regularity theorem for three-dimensional
Navier--Stokes.  It is not a solution, partial solution, or claimed route
completion for the Clay Millennium problem.
