# R0.74R Step 2 — the arbitrary-clock extraction gate

## 0. Result and decision

R0.74R Step 1 proves a sharp first-shell stability theorem once weighted
kinetic mass is already present on a terminal time window.  The remaining
question is whether a large defect-completed clock must supply such a
window.  This note separates that question into exact parts.

There are three results.

1. Every single clock obeys a rigorous three-way alternative on the full
   cutoff interval: a large terminal value is carried either by accumulated
   dissipation, by averaged cutoff-weighted kinetic energy on a preceding
   window, or by recent positive variation.
2. Padded-shell Hölder converts kinetic persistence into the precise
   coefficient
   \(2^k\gamma_k^{1/3}\Theta_{k,R}^{-2/3}\).  Its cube is the summable
   coefficient \(2^{3k}\gamma_k\Theta_{k,R}^{-2}\).
3. A frozen two-factor condition — clock-to-endpoint extraction plus this
   persistence packing — implies the R0.74Q best-terminal-tail estimate and
   hence the fixed-scale inequality (Q.1).

The two factors are not consequences of the completed-clock algebra alone.
A short smooth time spike destroys every uniform persistence lower bound,
and a smooth divergence-free high-frequency field separates accumulated
gradient dissipation from velocity-cubic mass.  These are functional
no-go examples, not Navier--Stokes solutions.  Thus they do not disprove the
conditional theorem or (Q.1).

The arbitrary-clock extraction theorem itself remains **OPEN**.  Signed
flux, scale contraction, regularity, singularity formation, and the Clay
Millennium problem remain **OPEN**.  **NOT CLAY.**

No simulation or DGX computation is used.

## 1. Frozen completed-clock decomposition

Work in the suitable-weak Version-M chart of R0.74P.  At local-energy good
times write the endpoint kinetic and accumulated dissipation parts as

\[
\begin{aligned}
 E_{k,R}(t)
 &:={\gamma_k\eta_R(t)\over2R}
   \int_{\mathbb T^3}\Psi_k^R(y)|v_R(t,y)|^2\,dy,\\
 D_{k,R}(t)
 &:={\gamma_k\over R}
   \int_{(s_R,t)\times\mathbb T^3}
   \eta_R(r)\Psi_k^R(x-X_R(r))\,d\boldsymbol\mu(r,x).
\end{aligned}
\tag{R.200}
\]

Then

\[
 K_{k,R}=E_{k,R}+D_{k,R}=Q_{k,R}+F_{k,R},
 \qquad K_{k,R}(s_R)=0,
 \qquad K_{k,R}\ge0.
\tag{R.201}
\]

The canonical representative of \(K_{k,R}\) is absolutely continuous,
while \(D_{k,R}\) is nondecreasing because its integrand is a nonnegative
measure.  The inherited ledgers give

\[
 \sum_{k\ge1}\operatorname {TV}Q_{k,R}
 \le C(P_R^M)^{2/3},
 \qquad
 \sum_{k\ge1}\operatorname {TV}F_{k,R}
 \le CP_R^M.
\tag{R.202}
\]

Set

\[
 A_R:=(P_R^M)^{2/3},
 \qquad
 Z_R:=Y_{2,R}^{\rm sf}
 =\left(\sum_{k\ge1}v_{k,R}^2\right)^{1/2}.
\tag{R.203}
\]

The aim is not to reprove the coarse \(\ell^1\) bound in (R.202), but to
identify what would compress a terminal clock tail to \(A_R+Z_R\).

## 2. An exact window-mass/dissipation/upcrossing alternative

### Lemma 2.1 — endpoint averaging

Let \(J=(a,\tau)\subset(s_R,t_0)\), with \(|J|>0\), and take \(\tau\) to be
a local-energy good time.  Write

\[
 \operatorname {Var}^{+}_{J\rightsquigarrow\tau}K
 :=\sup_{a<t_0<\cdots<t_m=\tau}
   \sum_{i=1}^{m}[K(t_i)-K(t_{i-1})]_+,
\]

where the supremum is over finite partitions whose initial point lies in
\(J\).  Thus the variation interval explicitly includes the terminal value
at \(\tau\).  Then

\[
 \boxed{
 E_{k,R}(\tau)
 \le \fint_JE_{k,R}(t)\,dt
    +\operatorname {Var}^{+}_{J\rightsquigarrow\tau}K_{k,R}.}
\tag{R.204}
\]

Moreover,

\[
 \operatorname {Var}^{+}_{J\rightsquigarrow\tau}K_{k,R}
 \le\operatorname {TV}_{J\rightsquigarrow\tau}Q_{k,R}
    +\operatorname {TV}_{J\rightsquigarrow\tau}F_{k,R}.
\tag{R.205}
\]

**Proof.**  For almost every good \(t\in J\), monotonicity of \(D_{k,R}\)
and (R.201) give

\[
 E_{k,R}(\tau)-E_{k,R}(t)
 =K_{k,R}(\tau)-K_{k,R}(t)
  -[D_{k,R}(\tau)-D_{k,R}(t)]
 \le\operatorname {Var}^{+}_{J\rightsquigarrow\tau}K_{k,R}.
\tag{R.206}
\]

Average in \(t\).  The subadditivity of positive variation and
\(K=Q+F\) prove (R.205).  \(\square\)

### Corollary 2.2 — exact three-way triage

Put \(T=K_{k,R}(\tau)\).  At least one of the following holds:

\[
 \boxed{
 D_{k,R}(\tau)\ge\frac T2,
 \quad\text{or}\quad
 \fint_JE_{k,R}(t)\,dt\ge\frac T4,
 \quad\text{or}\quad
 \operatorname {TV}_{J\rightsquigarrow\tau}Q_{k,R}
 +\operatorname {TV}_{J\rightsquigarrow\tau}F_{k,R}\ge\frac T4.}
\tag{R.207}
\]

Indeed, if the first alternative fails then
\(E_{k,R}(\tau)>T/2\); (R.204)--(R.205) force at least one of the last two
terms to be at least \(E_{k,R}(\tau)/2>T/4\).

This is a complete algebraic triage, but not yet a compression theorem.  The
dissipation branch has no reverse velocity-cubic estimate, and the last
branch is controlled by (R.202) only linearly in \(P_R^M\).

## 3. Kinetic persistence has the correct \(\ell^3\) coefficient

Use the unfolded padded cutoff from R0.74E--H.  At almost every
\(t\in(s_R,t_0)\), define the cutoff-weighted kinetic row

\[
 e_{k,R}^{\eta}(t)
 :={\gamma_k\eta_R(t)\over2R}
   \int_{\mathbb R^3}\psi_k^R(y)|\widetilde v_R(t,y)|^2\,dy
 =E_{k,R}(t).
\tag{R.208}
\]

On the plateau \(I_R\), this is the old unweighted row because
\(\eta_R=1\).  For a measurable \(J\subset(s_R,t_0)\), define the
nonnegative cutoff-weighted local velocity-cubic payment

\[
 p_{k,R}^{u,\eta}(J)
 :=R^{-2}\gamma_k
   \int_J\eta_R(t)^{3/2}
   \int_{\operatorname {supp}\psi_k^R}
   |\widetilde v_R(t,y)|^3\,dy\,dt.
\tag{R.209}
\]

The frozen support geometry gives

\[
 |\operatorname {supp}\psi_k^R|
 \le C_\psi2^{3k}R^3,
 \qquad 0\le\psi_k^R\le1.
\tag{R.210}
\]

For any family of measurable sets \(J_k\subset(s_R,t_0)\), nonnegativity,
\(0\le\eta_R^{3/2}\le1\), support of \(\eta_R\) in \(I_{2R}\), and the
R0.74H doubled-radius support ledger imply

\[
 \sum_{k\ge1}p_{k,R}^{u,\eta}(J_k)\le C_P P_R^M.
\tag{R.211}
\]

### Proposition 3.1 — persistence-to-payment estimate

For a good time \(\tau\in(s_R,t_0)\), let
\(J\subset(s_R,\tau)\) be measurable with positive measure and define

\[
 \Theta_{k,R}^{\eta}(\tau;J)
 :={R^{-2}\int_J e_{k,R}^{\eta}(t)^{3/2}\,dt
    \over e_{k,R}^{\eta}(\tau)^{3/2}}.
\tag{R.212}
\]

Use the conventions \(\Theta^\eta=+\infty\) when
\(e_{k,R}^{\eta}(\tau)=0\), and \(\Theta^\eta=0\) when the denominator is
positive but the numerator vanishes.  Then

\[
 \boxed{
 e_{k,R}^{\eta}(\tau)
 \le C_0\,2^k\gamma_k^{1/3}
       \Theta_{k,R}^{\eta}(\tau;J)^{-2/3}
       p_{k,R}^{u,\eta}(J)^{2/3}.}
\tag{R.213}
\]

**Proof.**  Spatial Hölder and (R.210) give, for almost every \(t\),

\[
 e_{k,R}^{\eta}(t)^{3/2}
 \le C_1\,2^{3k/2}R^2\gamma_k^{1/2}
 \left[R^{-2}\gamma_k
  \eta_R(t)^{3/2}
  \int_{\operatorname {supp}\psi_k^R}
       |\widetilde v_R(t)|^3\right].
\tag{R.214}
\]

Integrate on \(J\), divide by \(R^2\), use (R.209), and then use
(R.212).  Raising the result to the power \(2/3\) proves (R.213).
\(\square\)

Consequently, for any nonnegative coefficients \(\Lambda_k\),

\[
\begin{aligned}
 \sum_{k\in I}\Lambda_ke_{k,R}^{\eta}(\tau)
 \le{}&C_0
 \left(
  \sum_{k\in I}2^{3k}\gamma_k\Lambda_k^3
       \Theta_{k,R}^{\eta}(\tau;J_k)^{-2}
 \right)^{1/3}\\
 &\times
 \left(\sum_{k\in I}p_{k,R}^{u,\eta}(J_k)\right)^{2/3}.
\end{aligned}
\tag{R.215}
\]

This is ordinary Hölder with exponents \(3\) and \(3/2\).  It is the exact
reason the persistence coefficient must be packed in \(\ell^3\).

## 4. A sufficient two-factor theorem for arbitrary clocks

### Theorem 4.1 — conditional terminal-clock extraction

Assume there are constants \(N_0,C_q,C_*<\infty\), independent of the
solution, \(R\), and \(\tau\), with the following property.  For every good
terminal time \(\tau\in(s_R,t_0)\), there are

- a set \(S_\tau\subset\mathbb N\) with \(\#S_\tau\le N_0\);
- nonnegative errors \(q_{k,R,\tau}\) and factors
  \(\Lambda_{k,R,\tau}\) for \(k\notin S_\tau\); and
- measurable sets
  \(J_{k,\tau}\subset(s_R,\tau)\) of positive measure,

such that

\[
 \sum_{k\notin S_\tau}q_{k,R,\tau}\le C_qA_R,
 \qquad
 K_{k,R}(\tau)
 \le q_{k,R,\tau}
    +\Lambda_{k,R,\tau}e_{k,R}^{\eta}(\tau),
\tag{R.216}
\]

and

\[
 \boxed{
 \sum_{k\notin S_\tau}
 2^{3k}\gamma_k\Lambda_{k,R,\tau}^3
 \Theta_{k,R}^{\eta}(\tau;J_{k,\tau})^{-2}
 \le C_*.}
\tag{R.217}
\]

Then

\[
 \boxed{
 \mathcal S_{N_0,R}^{K}\le C A_R,}
\tag{R.218}
\]

and therefore the R0.74Q terminal reduction gives

\[
 \boxed{
 \mathfrak C_R^M
 \le C\left[(P_R^M)^{2/3}+Y_{2,R}^{\rm sf}\right].}
\tag{R.219}
\]

**Proof.**  Sum (R.216) outside \(S_\tau\), apply (R.215), (R.217), and
(R.211), and use \(A_R=(P_R^M)^{2/3}\).  This gives

\[
 \sum_{k\notin S_\tau}K_{k,R}(\tau)\le CA_R.
\tag{R.220}
\]

Because every \(K_{k,R}\ge0\), (R.220) is an admissible competitor for
the best-terminal-tail functional at every good time.  To pass to all
terminal times, use the following elementary representation for every
nonnegative \(x\in\ell^1\):

\[
 \mathcal S_N(x)
 =\sup_{G\Subset\mathbb N}
   \inf_{\substack{S\subset G\\ \#S\le N}}
   \sum_{k\in G\setminus S}x_k.
\]

The finite-coordinate functions inside the supremum are continuous, so
\(\mathcal S_N\) is lower semicontinuous for coordinatewise convergence.
Local-energy good times are dense, and every canonical clock
\(K_{k,R}\) is continuous.  Hence a sequence of good times converging to an
arbitrary \(\tau<t_0\), followed by lower semicontinuity, extends the bound
in (R.220) to that \(\tau\).  Times at or before \(s_R\) contribute zero by
the frozen extension.  Taking the supremum now gives (R.218).  Insert it in
R0.74Q (Q.9); \(N_0\) is fixed, so the factor \(\sqrt{N_0}\) is absorbed in
\(C\).  \(\square\)

The two assumptions have separate meanings.  Equation (R.216) must either
absorb accumulated dissipation into a quadratic error or compare the clock
to its endpoint kinetic part.  Equation (R.217) must prevent endpoint
energy from living on time sets too thin for the cubic payment.  The
three-way alternative (R.207) identifies recent positive variation as the
third object that a proof may instead charge or place among the finitely
many exceptions.

## 5. Three sharp functional no-go tests

These tests identify what cannot be obtained from positivity, absolute
continuity, incompressibility, and Hölder alone.  None of the constructed
fields is asserted to solve Navier--Stokes.

### Proposition 5.1 — completed-clock algebra does not extract energy

Let \(h\in C^\infty([0,1])\) be nondecreasing, with \(h=0\) near zero and
\(h=1\) near one.  For any \(T>0\), set

\[
 E(t)=0,
 \qquad D(t)=K(t)=F(t)=Th(t),
 \qquad Q(t)=0.
\tag{R.221}
\]

Then \(K=E+D=Q+F\), \(K(0)=0\), \(K\ge0\), \(K(1)=T\), and \(D\) is
nondecreasing, but every kinetic window average vanishes.  Thus the clock
axioms alone cannot imply (R.216) with an error smaller than order \(T\).
The example pays \(\operatorname {TV}F=T\), exactly as (R.207) predicts.

### Proposition 5.2 — an endpoint slice has no time thickness

Choose a nonzero smooth divergence-free field \(w\) supported in one hard
annulus and a smooth scalar \(\chi\) with \(\chi(0)=1\) and compact support.
For \(\varepsilon>0\), put

\[
 u_\varepsilon(t,x)
 :=\chi\!\left({t-\tau\over\varepsilon}\right)w(x).
\tag{R.222}
\]

Its endpoint weighted energy is independent of \(\varepsilon\), whereas

\[
 \int|u_\varepsilon|^3\,dx\,dt=O(\varepsilon),
 \qquad
 \Theta_{k,R}^{\eta}(\tau;J)=O(\varepsilon/R^2)\longrightarrow0.
\tag{R.223}
\]

Choose \(\tau\in I_R\), so \(\eta_R=1\) on the spike after shrinking its
time support.  Hence there is no positive universal lower bound for
\(\Theta^\eta\), and no
endpoint-to-spacetime cubic estimate can omit its negative power.

### Proposition 5.3 — dissipation has no reverse velocity-cubic bound

Choose \(0\ne\zeta\in C_c^\infty\) supported in a fixed hard annulus and
define a vector potential and divergence-free field by

\[
 A_n(x)=n^{-2}\zeta(x)\sin(nx_1)e_3,
 \qquad
 w_n=\nabla\times A_n.
\tag{R.224}
\]

Then

\[
 \|\nabla w_n\|_{L^2}\ge c_\zeta>0,
 \qquad
 \|w_n\|_{L^3}^3\le C_\zeta n^{-3}\longrightarrow0.
\tag{R.225}
\]

The first estimate follows from the leading term
\(\partial_1(w_n)_2=\zeta\sin(nx_1)+O(n^{-1})\) in \(L^2\); the second
follows from \(w_n=O(n^{-1})\) in every fixed \(L^p\).  Multiplication by
a fixed smooth time cutoff preserves both comparisons after time
integration.  Therefore no pure functional inequality can control a fixed
accumulated gradient-dissipation mass from below by a velocity-cubic
payment.  Navier--Stokes evolution may add relations between these rows,
but those relations must be used explicitly.

## 6. Inherited source ledger

| Use in this note | Frozen source | Status |
|---|---|---|
| Definition and nonnegativity of \(K=E+D=Q+F\) | `r074p_temporal_observable_triage.md`, (2.6)--(2.10) | **INHERITED / PROVED** |
| Absolute variation bounds in (R.202) | `r074p_temporal_observable_triage.md`, (3.5)--(3.6) | **INHERITED / PROVED** |
| Explicit padded cutoff and support geometry | `r074e_local_mollified_frame_gate.md`, (4.12b)--(4.12d) | **INHERITED / PROVED** |
| Periodization and unfolding | `r074h_collar_flux_two_regime_closure.md`, (2.1)--(2.7) | **INHERITED / PROVED** |
| Cubic support sum in (R.211) | `r074h_collar_flux_two_regime_closure.md`, (4.1)--(4.6) | **INHERITED / PROVED** |
| Best-terminal-tail reduction used in (R.218)--(R.219) | `r074q_problem_freeze.md`, (Q.7)--(Q.12) | **INHERITED / PROVED** |
| Window-lobe special case and first-shell stability | `r074r_persistent_lobe_cubic_packing.md`, (R.108)--(R.132) | **PROVED IN STEP 1** |

The new proofs in this note are (R.204)--(R.207), (R.213)--(R.215),
the conditional implication (R.216)--(R.220), its good-time-to-all-time
lower-semicontinuity closure, and the functional no-go tests
(R.221)--(R.225).  No novelty or priority claim is made.

## 7. Exact boundary for the next PDE step

The following are now **PROVED**:

- the endpoint averaging lemma (R.204)--(R.205);
- the three-way clock triage (R.207);
- the cutoff-weighted padded-shell persistence coefficient
  (R.213)--(R.215);
- the good-time-to-all-time best-tail closure; and
- the conditional implication (R.216)--(R.219).

The following remain **OPEN**:

- a uniform construction of \(S_\tau,q_{k,R,\tau},\Lambda_{k,R,\tau}\),
  and \(J_{k,\tau}\) satisfying (R.216)--(R.217) for arbitrary suitable
  weak solutions;
- a PDE mechanism paying or sparsifying the dissipation-dominated branch;
- a signed stopping-time argument that charges recent upcrossings without
  replacing the matched square function by the already-known \(\ell^1\)
  absolute ledger; and
- the fixed-scale inequality without the hypotheses of Theorem 4.1.

The immediate next falsification gate is therefore precise: test whether
the local-energy balance can force (R.216)--(R.217), or construct an exact
smooth Navier--Stokes family violating those two factors while retaining a
large positive cumulative signed flux.  Functional examples (R.221)--
(R.225) alone cannot decide that PDE question.  **NOT CLAY.**
