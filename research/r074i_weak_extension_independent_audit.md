# R0.74I — independent adversarial audit of the suitable-weak extension

## Final verdict and source binding

**FINAL PASS AFTER REPAIR.**

The first audit of the initial source was conditional. The main source was
then repaired and independently re-read. Section 9 records the exact final
source digest and the second-pass decision. Sections 1--8 retain the
adversarial derivation and the initial repair ledger so that the promotion
from conditional to final pass is auditable.

I found no sign error, missing factor of \(R\), invalid pressure-gauge
operation, or counterexample to the proposed Version-M suitable-weak
two-regime estimate. The underlying argument is viable at the stated
energy and pressure regularity. In particular, the terminally anchored
mollified trajectory is well defined, the moving cutoff is admissible by a
precise approximation argument, and the R0.74H finite-shell estimates do
not use pointwise differentiability of \(u\).

The initially audited draft was not freeze-ready as written. Its proof
compressed
three theorem-level passages into assertions:

1. the choice of a jointly measurable representative of \(u_R\), the
   terminal Caratheodory construction on the torus, and the Euclidean lift;
2. the exact topology in which the nonsmooth moving test is approximated
   and every local-energy term converges; and
3. the almost-everywhere terminal-time argument which separately closes the
   essential-supremum energy and the full \(I_R\) dissipation.

Lemma 2.2 also needs an explicit weak-regularity bridge rather than the
single sentence that all smooth R0.74H estimates remain valid. These are
repairable proof omissions, not evidence that the theorem is false.

This initial read-only audit was bound to

    research/r074i_suitable_weak_tube_and_log_obstruction.md
    SHA-256 ab88bf59b91b2ed91c26d2d6baba930a351f9e0f7391620d5c91bd24fb3a85e5

and compared it with the frozen smooth authority

    research/r074h_collar_flux_two_regime_closure.md
    SHA-256 8c1d43f08d5a2c9299ae50ebdd10c8c184f064c6830f1d663524e03fa90d88f1.

The audited R0.74I slice consists of Sections 1--2 through Theorem 2.3.

---

## 1. Periodic suitable-weak setting

### 1.1 Energy-class consequences

On the finite cylinder under consideration,

\[
 u\in L_t^\infty L_x^2\cap L_t^2H_x^1
 \quad\Longrightarrow\quad
 u\in L_{t,x}^{10/3}\subset L_{t,x}^3.
\tag{A1}
\]

Consequently,

\[
 |u|^2,\ |\nabla u|^2,\ |u|^3\in L^1,
 \qquad
 |p|\,|u|\in L^1
\tag{A2}
\]

because \(p\in L^{3/2}\) and \(u\in L^3\). A time-dependent spatial
translation preserves each of these space-time norms. Hence

\[
 v_R(t,y)=u(t,y+X_R(t)),
 \qquad
 \pi_R(t,y)=p(t,y+X_R(t))
\tag{A3}
\]

have exactly the integrability needed by the moving local-energy formula.
Moreover,

\[
 \nabla_yv_R(t,y)=(\nabla_xu)(t,y+X_R(t))
\tag{A4}
\]

for almost every \((t,y)\). No time derivative of \(v_R\) is required in
the weak proof.

The draft should say that the suitable-weak assumptions and pressure class
hold on \(I_{8R}\times\mathbb T^3\), and it should use the standard weakly
continuous \(L^2\) representative when terminal values are mentioned. The
displayed result is only asserted for almost every terminal time, so no
strong \(L^2\) continuity is needed.

**Decision: PASS WITH CLARIFICATION.**

### 1.2 Pressure class and gauge

The periodic distributional equation implies

\[
 -\Delta\pi_R
 =\partial_i\partial_j(v_{R,i}v_{R,j})
\tag{A5}
\]

in the moving spatial coordinates. The spatially constant drift \(a_R(t)\)
adds no term to (A5). Thus the inherited local Riesz split remains valid
at weak regularity. For example,

\[
 p_{2R}^{\rm loc}
 =\mathcal R_i\mathcal R_j
   (\zeta_{2R}v_{R,i}v_{R,j}),
 \qquad
 h_{2R}=\widetilde\pi_R-p_{2R}^{\rm loc}
\tag{A6}
\]

satisfies \(\Delta h_{2R}=0\) distributionally on \(B_{6R}\), hence has a
smooth harmonic representative there. Since \(v_R\in L^3\), the local
part belongs to \(L^{3/2}\), while Jensen gives the required time
integrability of

\[
 c_{2R}^{M,R}(t)=(h_{2R}(t))_{B_{4R}}.
\tag{A7}
\]

Adding an arbitrary scalar function of time to the pressure shifts both
\(\pi_R\) and \(c_{2R}^{M,R}\) by the same amount. The payment and flux are
therefore gauge invariant.

The draft should display (A5) and write \(c_{2R}^{M,R}(t)\), rather than
leave its time dependence implicit.

**Decision: PASS WITH REQUIRED INSERTION.**

---

## 2. Mollified terminal trajectory

### 2.1 Spatial convolution estimates

For almost every \(t\), Young's inequality on the torus gives

\[
 \|u_R(t)\|_\infty
 \le \|\varphi_R^{\rm per}\|_2\|u(t)\|_2
 \le C_\varphi R^{-3/2}\|u(t)\|_2,
\tag{A8}
\]

and

\[
 \|\nabla u_R(t)\|_\infty
 \le \|\nabla\varphi_R^{\rm per}\|_2\|u(t)\|_2
 \le C_\varphi R^{-5/2}\|u(t)\|_2.
\tag{A9}
\]

The powers in R0.74I (1.4) are correct. Since \(\|u(t)\|_2\) is
essentially bounded, both the vector-field bound and its spatial Lipschitz
coefficient belong to \(L^1(I_{8R})\), in fact to
\(L^\infty(I_{8R})\).

### 2.2 Representative, terminal ODE, and lift

Spatial convolution of a jointly measurable representative of \(u\) gives
a representative \(u_R(t,x)\) which is measurable in \(t\) and smooth in
\(x\) for almost every \(t\). Redefining it on a null set of times gives a
Caratheodory vector field without changing any integral or trajectory
equation almost everywhere. The standard Caratheodory theorem, applied
after reversing time, then gives a unique absolutely continuous torus path

\[
 \dot X_R(t)=u_R(t,X_R(t)),
 \qquad X_R(t_0)=x_0.
\tag{A10}
\]

There is no sign reversal in (A10): reversing time is only a device for
solving the terminal-value problem. Because the vector field is periodic,
the path has a continuous Euclidean lift

\[
 \widetilde X_R\in W^{1,\infty}(I_{8R};\mathbb R^3),
 \qquad
 \widetilde X_R(t_0)=\widetilde x_0,
\tag{A11}
\]

with derivative equal to the periodic lift of \(u_R(t,X_R(t))\) almost
everywhere. The lift is unique after its terminal value is fixed.

The phrase “smooth periodic lifts” in the initial draft is incorrect
terminology. A torus path has a Euclidean lift; that lift need not be
periodic in time. It should be replaced by “smooth Euclidean
approximations of the fixed lift.”

**Decision: CONDITIONAL PASS.** The estimates license the ODE, but the
representative and lift must be stated.

---

## 3. Admissibility of the moving test

### 3.1 Exact approximation topology

Fix a finite \(N\). Starting from (A11), choose
\(\widetilde X_R^{(m)}\in C^\infty([s_R,t_0];\mathbb R^3)\) such that

\[
 \widetilde X_R^{(m)}\to\widetilde X_R
 \quad\hbox{uniformly},
 \qquad
 \dot{\widetilde X}_R^{(m)}\to a_R
 \quad\hbox{in }L^1_t.
\tag{A12}
\]

The terminal value may be preserved by an elementary endpoint correction,
although the local-energy argument itself does not require it. Put

\[
 \phi_{N,m}(t,x)
 =\eta_R(t)\Theta_{R,N}
   (x-\widetilde X_R^{(m)}(t)).
\tag{A13}
\]

Every \(\phi_{N,m}\) is smooth, periodic in \(x\), and nonnegative. Since
\(\Theta_{R,N}\in C^\infty(\mathbb T^3)\), (A12) implies

\[
\begin{aligned}
 &\phi_{N,m}\to\phi_N,
 \quad \nabla\phi_{N,m}\to\nabla\phi_N,
 \quad \Delta\phi_{N,m}\to\Delta\phi_N
 &&\text{in }L^\infty_{t,x},\\
 &\partial_t\phi_{N,m}\to\partial_t\phi_N
 &&\text{in }L^1_tL^\infty_x,
\end{aligned}
\tag{A14}
\]

where

\[
 \partial_t\phi_N
 =\eta_R'\Theta_{R,N}(x-X_R(t))
  -\eta_R a_R\cdot\nabla\Theta_{R,N}(x-X_R(t))
\tag{A15}
\]

almost everywhere.

The convergence in (A14), together with (A2), licenses every limit:

- \(L^\infty_{t,x}\) convergence pays the terminal energy, diffusion, and
  Laplacian rows;
- \(L^1_tL^\infty_x\) convergence of the time derivative is paired with
  \(\mathop{\rm ess\,sup}_t\|u(t)\|_2^2\);
- uniform convergence of the spatial gradient is paired with
  \(|u|^3+|p|\,|u|\in L^1\).

This is the missing functional-analytic justification in Lemma 2.1. The
finite-shell payment bounds are not needed to pass \(m\to\infty\); basic
energy-class integrability already suffices.

### 3.2 Terminal cutoff and good times

The local energy inequality is initially available for smooth tests compact
in time. For a fixed \(\tau\in I_R\), extend the moving test smoothly beyond
\(\tau\), multiply it by a future time cutoff which equals one through
\(\tau\), and use the standard integrated suitable inequality. Equivalently,
one may approximate the characteristic of \((s_R,\tau)\) from inside.
Lebesgue differentiation gives the terminal formula for almost every
\(\tau\). Taking a countable intersection over the smooth approximants
gives one full-measure set on which the \(m\to\infty\) passage is valid.

The properties imported from R0.74H must be stated where they are used:

\[
 \eta_R(s_R)=0,
 \qquad
 \eta_R=1\ \hbox{on }I_R,
 \qquad
 |\eta_R'|\le CR^{-2}.
\tag{A16}
\]

The zero at \(s_R=t_0-4R^2\) removes the initial energy term.

**Decision: CONDITIONAL PASS.** The test is admissible, but the initial
draft's one-sentence approximation is not a complete proof.

---

## 4. Sign, factor, and scale audit of (2.2)--(2.3)

Use the half-normalized suitable local energy inequality

\[
\begin{aligned}
 &\frac12\int|u(\tau)|^2\phi(\tau)
 +\int_{s_R}^{\tau}\!\int|\nabla u|^2\phi\\
 &\le
 \frac12\int_{s_R}^{\tau}\!\int|u|^2
   (\partial_t\phi+\Delta\phi)
 +\int_{s_R}^{\tau}\!\int
   \left(\frac12|u|^2+p\right)u\cdot\nabla\phi.
\end{aligned}
\tag{A17}
\]

Insert (A15), translate \(x=y+X_R(t)\), and divide by \(R\). The rows are

| Row | Coefficient and sign |
|---|---|
| terminal energy | \(+(2R)^{-1}\int\Theta_{R,N}|v_R(\tau)|^2\) |
| dissipation | \(+R^{-1}\int\eta_R\Theta_{R,N}|\nabla v_R|^2\) |
| time cutoff | \(+(2R)^{-1}\int\eta_R'\Theta_{R,N}|v_R|^2\) |
| Laplacian cutoff | \(+(2R)^{-1}\int\eta_R|v_R|^2\Delta\Theta_{R,N}\) |
| physical kinetic flux | \(+(2R)^{-1}\int\eta_R|v_R|^2v_R\cdot\nabla\Theta_{R,N}\) |
| moving-cutoff kinetic row | \(-(2R)^{-1}\int\eta_R|v_R|^2a_R\cdot\nabla\Theta_{R,N}\) |
| pressure flux | \(+R^{-1}\int\eta_R\pi_Rv_R\cdot\nabla\Theta_{R,N}\) |

The last three rows combine exactly as

\[
 \frac1R\int\eta_R
 \left[
  \frac12|v_R|^2(v_R-a_R)+\pi_Rv_R
 \right]\cdot\nabla\Theta_{R,N}.
\tag{A18}
\]

Thus the minus sign on \(a_R\), the kinetic factor \(1/2\), and every
\(1/R\) factor in R0.74I (2.2)--(2.3) are correct.

For the time-dependent scalar gauge,

\[
 \int_{\mathbb T^3}c_{2R}^{M,R}(t)
 v_R(t)\cdot\nabla\Theta_{R,N}
 =-c_{2R}^{M,R}(t)
 \langle\nabla\cdot v_R,\Theta_{R,N}\rangle=0
\tag{A19}
\]

for almost every \(t\). This uses distributional incompressibility only;
no smooth integration by parts is hidden.

**Decision: PASS.**

---

## 5. Finite-shell limit and weak payment bounds

### 5.1 The \(N\to\infty\) limit

The R0.74H lattice estimate is

\[
 \|D^k\Psi_j^R\|_\infty
 \le CR^{-k}(1+2^{3j}R^3),
 \qquad 0\le k\le2.
\tag{A20}
\]

Since \(\gamma_j=\exp(-4^{j-1}/32)\), the right side is summable in
\(j\). Therefore

\[
 \Theta_{R,N}\to\Theta_R
 \quad\hbox{in }C^2(\mathbb T^3).
\tag{A21}
\]

After the moving translation, the same norms occur. The terminal energy
converges for every good \(\tau\); diffusion and cutoff rows converge by
dominated convergence; the kinetic, residual-drift, and pressure fluxes
converge because

\[
 |v_R|^3+|a_R|\,|v_R|^2+|\pi_R|\,|v_R|\in L^1.
\tag{A22}
\]

For the middle term, \(a_R\in L^\infty_t\) follows from (A8), although the
sharper cubic payment below is needed for the uniform theorem constant.

**Decision: PASS.**

### 5.2 Quadratic-cutoff row

With

\[
 S_q=\sum_j\gamma_j
 \int_{I_{2R}}\int_{\operatorname{supp}\psi_j^R}|v_R|^q,
\tag{A23}
\]

weighted Holder and the shell-volume sum give

\[
 S_2\le CR^{5/3}S_3^{2/3},
 \qquad
 R^{-3}S_2\le C(R^{-2}S_3)^{2/3}.
\tag{A24}
\]

The inherited support inclusion splits \(S_3\) into the \(8R\) core and
the \(2R\) exterior velocity ledger. The core is paid at weak regularity
by the purely functional interpolation estimate

\[
 R^{-2}\int_{I_{2R}}\int_{B_{8R}}|v_R|^3
 \le C\bigl[\mathcal E^{M,R}(z_0,8R)\bigr]^{3/2}.
\tag{A25}
\]

Equation (A25) follows from spatial \(L^2\)-\(L^6\) interpolation, the
local Sobolev inequality including its \(R^{-1}\|v_R\|_2\) term, Holder
in time, and (1.7). It does not use the equation or smoothness. Hence

\[
 \mathfrak Q_R^M\le C(P_R^M)^{2/3}
\tag{A26}
\]

does extend to the weak setting.

**Decision: PASS**, but (A25) should be displayed in Lemma 2.2.

### 5.3 Velocity-pressure flux

Young's inequality gives

\[
 |\pi_R-c|\,|v_R|
 \le C\bigl(|\pi_R-c|^{3/2}+|v_R|^3\bigr).
\tag{A27}
\]

The outer pieces are entries already present in
\(\mathcal G_{v_R,\pi_R}^{M,R}(z_0,2R;1)\). The inner local pressure is
paid by Calderon--Zygmund from (A25), while the centered harmonic part is
paid by \(\mathcal H_{v_R}^{M,R}(z_0,2R)\). Distributional harmonicity plus
Weyl's lemma is enough for the harmonic estimate. No classical pressure
derivative is used.

**Decision: PASS WITH REQUIRED EXPLICIT REFERENCE TO (A5)--(A7).**

### 5.4 Residual drift

Evenness of the mollifier and Jensen give, almost everywhere in time,

\[
 |a_R(t)|^3
 \le\int\varphi_R^{\rm per}(y)|v_R(t,y)|^3\,dy
 \le CR^{-3}\int_{B_R}|v_R(t,y)|^3\,dy.
\tag{A28}
\]

Using Young pointwise, the weighted support volume
\(\sum_j\gamma_j|\operatorname{supp}\psi_j^R|\le CR^3\), and (A28),

\[
\begin{aligned}
 &R^{-2}\sum_j\gamma_j
 \int_{I_{2R}}\int_{\operatorname{supp}\psi_j^R}
 |a_R|\,|v_R|^2\\
 &\qquad\le
 CR^{-2}\int_{I_{2R}}
 \left[
   \int_{B_R}|v_R|^3
   +\sum_j\gamma_j
    \int_{\operatorname{supp}\psi_j^R}|v_R|^3
 \right]
 \le CP_R^M.
\end{aligned}
\tag{A29}
\]

This calculation is at the \(L^3\) level and is valid for the suitable weak
solution. No derivative of \(a_R\) occurs in Version M.

Combining (A27)--(A29) proves

\[
 \sup_{\tau\in I_R}|\mathfrak F_R^M(\tau)|\le CP_R^M.
\tag{A30}
\]

The indefinite integral defining \(\mathfrak F_R^M(\tau)\) has an
absolutely continuous representative because its integrand belongs to
\(L^1_t\). Thus the ordinary supremum in (A30) is legitimate.

**Decision: PASS**, but the displayed residual calculation is required in
the weak-extension proof.

### 5.5 Regularity actually used

The R0.74H payment estimates use exactly:

| Estimate | Required input |
|---|---|
| local cubic interpolation | \(v_R\in L_t^\infty L_x^2\cap L_t^2H_x^1\) |
| outer cubic ledger | \(v_R\in L^3\) and the definition of \(P_R^M\) |
| pressure product | \(\pi_R\in L^{3/2}\), \(v_R\in L^3\) |
| local pressure | distributional pressure Poisson identity and Calderon--Zygmund |
| harmonic pressure | distributional harmonicity, Weyl's lemma, and the frozen harmonic ledger |
| residual drift | mollifier Jensen, Young, and \(v_R\in L^3\) |
| finite-shell limit | \(C^2\) summability and the preceding \(L^1\) rows |

Thus pointwise differentiability of \(u\) is not needed. However, the
statement in the draft that only (1.2) is used is slightly too terse: the
distributional NSE and incompressibility are also needed for the pressure
identity and gauge cancellation, while suitability is needed for the
one-sided energy inequality.

---

## 6. Exterior terminal energy, dissipation, and essential supremum

After \(N\to\infty\), let

\[
 M_R=C\bigl[(P_R^M)^{2/3}+P_R^M\bigr].
\tag{A31}
\]

The moving local energy inequality and the bounds above imply, for almost
every \(\tau\in I_R\),

\[
 \frac1{2R}\int\Theta_R|v_R(\tau)|^2
 +\frac1R\int_{s_R}^{\tau}\eta_R
   \int\Theta_R|\nabla v_R|^2
 \le M_R.
\tag{A32}
\]

Here the signed Laplacian row has been majorized by its absolute value, and
the signed flux by (A30).

Since \(\Theta_R\) dominates the weighted shell indicators, dropping the
dissipation in (A32) gives

\[
 R^{-1}U_\gamma^{M,R}(\tau)\le 2M_R
\tag{A33}
\]

for almost every \(\tau\in I_R\). Taking the essential supremum proves the
exterior terminal-energy estimate.

For dissipation, choose good times \(\tau_n\uparrow t_0\) from the
full-measure set on which (A32) holds. Drop the terminal energy and use
\(\eta_R=1\) on \(I_R\):

\[
 \frac1R\int_{t_0-R^2}^{\tau_n}
 G_\gamma^{M,R}(t)\,dt\le M_R.
\tag{A34}
\]

Monotone convergence gives

\[
 R^{-1}\int_{I_R}G_\gamma^{M,R}(t)\,dt\le M_R.
\tag{A35}
\]

Adding (A33) and (A35), with a harmless absolute constant, yields

\[
 X_R^M\le C\bigl[(P_R^M)^{2/3}+P_R^M\bigr].
\tag{A36}
\]

This closure does not require continuity of the weak kinetic energy at
\(t_0\). A sequence of good times and monotone convergence are sufficient.
The initial draft's phrase “take the essential supremum in \(\tau\), and
then add the dissipation estimate” must be expanded to (A33)--(A35), because
the two components are obtained in separate limiting operations.

**Decision: CONDITIONAL PASS.** The endpoint mechanism is correct, but the
almost-everywhere terminal sequence is a required proof insertion.

---

## 7. Required repair ledger

The following changes were required before the weak theorem could receive
an unconditional analytic pass.

1. **Specify representatives and the path.** Choose a jointly measurable,
   spatially smooth representative of \(u_R\); state the backward
   Caratheodory theorem and fix the Euclidean lift of \(X_R\).
2. **Correct the approximation terminology.** Replace “smooth periodic
   lifts” by smooth Euclidean approximations satisfying (A12).
3. **State the convergence topology.** Insert (A14) and the integrability
   ledger (A1)--(A2); explain the terminal cutoff and full-measure set of
   good times.
4. **Display the weak pressure identity.** Insert (A5), state that the
   gauge is the time-dependent scalar (A7), and cite distributional
   harmonicity plus Weyl's lemma.
5. **Expand Lemma 2.2.** Display the local interpolation (A25), residual
   estimate (A29), and exact weak inputs summarized in Section 5.5.
6. **Close the two endpoint pieces separately.** Replace the final proof
   sentence by (A33)--(A35), using a good-time sequence rather than an
   unqualified terminal limit.
7. **Retain the weak scope.** The proof licenses Version M only. It gives
   no derivative \(a_R'\) and therefore does not by itself extend Version F.

The insertions do not change (2.2), (2.3), (2.5), (2.7), or (2.8).

---

## 8. Initial audit table

| Question | Result |
|---|---|
| Periodic suitable-weak hypotheses are sufficient | PASS after representative clarification |
| Mollifier powers \(R^{-3/2}\), \(R^{-5/2}\) | PASS |
| Terminal Caratheodory ODE | PASS after Borel representative and lift are stated |
| AC moving test is admissible | PASS IN SUBSTANCE / PROOF INSERTION REQUIRED |
| Sign of the moving drift in (2.3) | PASS |
| Kinetic factor \(1/2\) | PASS |
| \(1/(2R)\) and \(1/R\) normalizations | PASS |
| Time-dependent pressure gauge | PASS with \(c(t)\) made explicit |
| \(C^2\) finite-shell limit | PASS |
| Quadratic cutoff \(C(P_R^M)^{2/3}\) | PASS |
| Absolute flux \(CP_R^M\) | PASS |
| Hidden use of pointwise smoothness | NONE FOUND |
| Essential-supremum terminal energy | PASS after good-time formulation |
| Full \(I_R\) dissipation | PASS after monotone good-time limit |
| Theorem 2.3 at the initial bound SHA | CONDITIONAL / NOT YET FREEZE-READY |

## Initial boundary

The initial audit supports a repairable Version-M suitable-weak size
theorem. It does not prove that \(P_R^M\) is small, does not propagate
smallness between scales, does not extend Version F, and does not prove
epsilon regularity, singularity exclusion, global regularity, novelty, or
priority. **NOT CLAY.**

---

## 9. Re-audit of the repaired source

### 9.1 Final source binding

The repaired source was read again at

    research/r074i_suitable_weak_tube_and_log_obstruction.md
    SHA-256 9b6dfdbc87990e0a31550881799b0aa6f421df6afbfe5f251db1adc9a8227084.

The final verdict applies only to that byte sequence. The smooth authority
remains the R0.74H source bound near the beginning of this audit.

### 9.2 Repair verification

The second pass verified the following changes.

1. **Representative and trajectory: PASS.** Section 1 now chooses a jointly
   measurable periodic representative of \(u_R\), records the correct
   \(R^{-3/2}\) and \(R^{-5/2}\) bounds, extends the field periodically to
   \(\mathbb R^3\), invokes the terminal Caratheodory problem, and records
   \(X_R\in W^{1,\infty}\) at fixed \(R\). This supplies the Borel and
   integrable-Lipschitz hypotheses used in (A10)--(A11).
2. **Composed moving test: PASS.** Lemma 2.1 now approximates the Euclidean
   lift in \(W^{1,1}\), preserves nonnegativity, records uniform convergence
   of the tests and their spatial derivatives, and records
   \(L_t^1L_x^\infty\) convergence of their time derivatives. These are the
   exact topologies audited in (A12)--(A15).
3. **Termwise integrability: PASS.** The repaired proof displays
   \(|u|^2\in L_t^\infty L_x^1\), \(u\in L^3\), and
   \(p\in L^{3/2}\), and explicitly notes \(pu\in L^1\). Together with
   \(|\nabla u|^2\in L^1\) from (1.2), every local-energy term has a valid
   limit.
4. **Signs and normalizations: PASS.** Equations (2.2)--(2.4) are unchanged.
   Their sign, kinetic factor \(1/2\), terminal factor \(1/(2R)\), and
   dissipation/flux factor \(1/R\) still agree with (A17)--(A19).
5. **Weak payment bridge: PASS.** Lemma 2.2 now identifies the exact
   weak-level inputs for the velocity, residual-drift, local pressure, and
   harmonic pressure rows, and explicitly excludes every time derivative
   of \(u\), \(a_R\), or \(p\). The detailed inequalities remain bound by
   the frozen R0.74E--H definitions and R0.74H shell/payment proof. The
   independent reconstruction in Sections 5.2--5.4 confirms that those
   cited rows require only the displayed weak integrability, the
   distributional pressure identity, and incompressibility.
6. **Terminal energy and full dissipation: PASS.** Theorem 2.3 now treats
   the two endpoint components separately. It takes the essential supremum
   over good terminal times for the energy row and chooses
   \(\tau_k\uparrow t_0\) for the dissipation row. The right-hand indefinite
   integrals converge by \(L_t^1\) integrability, the terminal energy is
   nonnegative, and monotone convergence yields the entire \(I_R\)
   dissipation. This is the closure in (A33)--(A35).

### 9.3 Remaining nonblocking clarity items

Two short additions would improve standalone readability but are not
analytic blockers in this linked research series.

1. Lemma 2.2 could cite R0.74H (4.1)--(4.8) and (6.3)--(6.6), and R0.74E
   (3.4)--(3.5), by equation number rather than only by note name.
2. The pressure gauge in (2.3) could be written
   \(c_{2R}^{M,R}(t)\), and the mollifier identity in Lemma 2.2 could be
   written explicitly as
   \(a_R(t)=(\varphi_R^{\rm per}*v_R(t,\cdot))(0)\).

The distributional pressure Poisson identity is already part of the frozen
R0.74H authority and the current proof explicitly invokes its
distributional split. Repeating that identity in R0.74I is therefore a
clarity improvement, not a missing logical premise.

### 9.4 Final decision

At the final bound SHA, Sections 1--2 and Theorem 2.3 pass the requested
adversarial checks:

- the periodic suitable-weak setting is adequate;
- the mollified terminal path is licensed;
- the AC moving test enters the local energy inequality by a valid smooth
  approximation;
- the signs, \(1/2\), and all \(R\)-normalizations are correct;
- the pressure gauge is harmless;
- the finite-shell and payment estimates use no hidden pointwise
  differentiability; and
- the exterior essential-supremum energy and full dissipation close
  separately.

**FINAL ANALYTIC PASS for the Version-M weak two-regime closure.**

This verdict does not extend Version F and does not prove payment
smallness, scale propagation, epsilon regularity, global regularity,
novelty, priority, or the Millennium problem. **NOT CLAY.**
