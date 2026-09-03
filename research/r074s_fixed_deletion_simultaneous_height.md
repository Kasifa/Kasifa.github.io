# R0.74S Step 18 — fixed deletion, simultaneous height, and the exact temporal quantifier gap

## 0. Result, correction, and scope

Step 17 proved that every sublinear power estimate for the absolute
temporal-variation tail is false, and retained the coordinatewise positive
excursion \(\mathfrak O^{F,+}_{N,R}\) as a sufficient signed successor.
That successor is valid, but it still takes one temporal supremum for every
shell before summing the shells.  The actual Step 15 residual gate takes one
terminal time first.  This step records the missing middle functional and
separates the three quantifier orders exactly.

The conclusions are:

1. The Step 15 hybrid gate is
   \[
   \sup_\tau\inf_{\#S\le N}\sum_{k\notin S}z_k(\tau).
   \]
   Requiring one exceptional set for all common good terminal times gives
   the stronger, but still nonseparable, functional
   \[
   \inf_{\#S\le N}\sup_\tau\sum_{k\notin S}z_k(\tau).
   \]
   It is weaker than \(\mathfrak O^{F,+}_{N,R}\).
2. A completed-clock simultaneous-height functional bounds this fixed-set
   hybrid tail after paying the already-controlled \(Q\)-variation once.
   Conversely, the Step 10 paid-branch inequality bounds simultaneous
   height by the fixed hybrid tail plus known \(A_R\)-scale payments.
   Hence the two functionals are equivalent at the target scale.
3. Mutually disjoint triangular clocks show that the first two inequalities in
   the hierarchy can be strict, and that coordinatewise maxima can overcount
   the simultaneous height by an arbitrarily large factor.  The correct
   strict example uses \(M\ge N+2\), not \(M=N+1\).
4. The same abstract clocks show that the inherited nonnegativity,
   \(Q\)-variation, and linear absolute-flux ledger do not algebraically
   imply the desired \(2/3\)-power estimate, even for a fixed deletion
   budget.  This is an abstract information-theoretic obstruction, not a
   Navier--Stokes counterexample.
5. Taylor's recurrent smooth family from Step 17 does not refute any of the
   surviving gates.  After \(N\) is fixed and \(R\) is chosen as in Step 17
   (S.451), it saturates the quadratic positive-excursion scale while
   refuting only the discarded absolute-variation route.

This is a rigorous route reduction and correction.  It does not prove the
fixed-deletion gate, the direct hybrid gate, Q.12, Q.1, scale contraction,
or regularity.  **NOT CLAY.**

## 1. Frozen setting and the three deletion orders

Fix one frozen Version-M suitable weak solution, one admissible scale \(R\),
one admissible profile \(\boldsymbol\lambda\), one terminal domain
\(\mathcal D\in\{I_R,\mathcal T_R\}\), and one integer
\(N\in\mathbb N_0\).  Put

\[
 I=[s_R,t_0),\qquad
 \mathcal D_g=\mathcal D\cap\mathcal G_R.
\]

The inherited objects satisfy

\[
 \boxed{
 K_{k,R}=F_{k,R}+Q_{k,R}\ge0,\qquad
 F_{k,R}(s_R)=Q_{k,R}(s_R)=K_{k,R}(s_R)=0,}
 \tag{S.476}
\]

and

\[
 B_{F,R}:=\sum_{k\ge1}\operatorname {TV}_{I}F_{k,R}
 \le C_FP_R^M,\qquad
 B_{Q,R}:=\sum_{k\ge1}\operatorname {TV}_{I}Q_{k,R}
 \le C_QA_R,
 \qquad A_R=(P_R^M)^{2/3}.
\]

Retain the Step 15 nonnegative stopped-flux vector
\[
 z_k(\tau)
 =F_{k,R}(\tau)
  -F_{k,R}(\sigma_k^{\rm hyb}(\tau)),
 \qquad \tau\in\mathcal D_g.
\]
Here \(\sigma_k^{\rm hyb}(\tau)\in[s_R,\tau]\) on every active
coordinate and \(z_k(\tau)=0\) otherwise.  Step 15 proves
\(z(\tau)\in\ell^1_+\).

Let
\[
 \mathscr S_N=\{S\subset\mathbb N:\#S\le N\}.
\]
Define the moving-deletion hybrid tail and the common fixed-deletion tail by

\[
 \boxed{
 \begin{aligned}
 \mathfrak H^{\rm hyb}_{N,R}(\mathcal D)
 &:=
 \sup_{\tau\in\mathcal D_g}
 \inf_{S\in\mathscr S_N}
 \sum_{k\notin S}z_k(\tau)
 =\mathfrak Z_{N,R}^{\boldsymbol\lambda}(\mathcal D),\\
 \mathfrak H^{\rm fix}_{N,R}(\mathcal D)
 &:=
 \inf_{S\in\mathscr S_N}
 \sup_{\tau\in\mathcal D_g}
 \sum_{k\notin S}z_k(\tau).
 \end{aligned}}
 \tag{S.477}
\]

The superscript fix means only that, for each fixed solution, scale, centre,
and terminal domain, the same shell set is used for every common good
terminal time.  The set itself may depend on those fixed data.  This does
not freeze the hybrid starts, which retain their Step 15 terminal
dependence.

For comparison, put

\[
 \boxed{
 o_{k,R}^F
 :=\sup_{s_R\le a<b<t_0}
       [F_{k,R}(b)-F_{k,R}(a)]_+,
 \qquad
 \mathfrak O^{F,+}_{N,R}
 :=\inf_{S\in\mathscr S_N}\sum_{k\notin S}o_{k,R}^F.}
 \tag{S.478}
\]

Since \(o_{k,R}^F\le\operatorname {TV}_I F_{k,R}\), the sequence
\((o_{k,R}^F)_k\) lies in \(\ell^1_+\).  Moreover,
\[
 0\le z_k(\tau)\le o_{k,R}^F
\]
for every \(k\) and \(\tau\).  Thus every series below is dominated by one
summable sequence, and no exchange of an infinite signed sum is used.

## 2. Exact hierarchy and its proof

The minimax inequality and the preceding coordinatewise domination give

\[
 \boxed{
 \mathfrak H^{\rm hyb}_{N,R}(\mathcal D)
 \le
 \mathfrak H^{\rm fix}_{N,R}(\mathcal D)
 \le
 \mathfrak O^{F,+}_{N,R}
 \le
 \mathfrak H^F_{1,N,R}.}
 \tag{S.479}
\]

For completeness, fix \(S\in\mathscr S_N\).  For every \(\tau\),
\[
 \inf_{T\in\mathscr S_N}\sum_{k\notin T}z_k(\tau)
 \le\sum_{k\notin S}z_k(\tau).
\]
Take the supremum in \(\tau\), then the infimum in \(S\), to obtain the
first inequality.  No minimax equality or attainment is assumed.  Next,
\[
 \sup_{\tau\in\mathcal D_g}\sum_{k\notin S}z_k(\tau)
 \le\sum_{k\notin S}o_{k,R}^F.
\]
Optimization gives the second inequality.  The third follows from
\(o_{k,R}^F\le\operatorname {TV}_I F_{k,R}\), again before optimizing.
If an infimum is not attained, use an \(\varepsilon\)-minimizing set and
let \(\varepsilon\downarrow0\).

There is also an exact incidence representation.  For
\(\lambda>0\), define

\[
 A_\tau(\lambda)=\{k:z_k(\tau)>\lambda\},
 \qquad
 A_o(\lambda)=\{k:o_{k,R}^F>\lambda\}.
\]

The layer-cake formula and best-\(N\) rearrangement give

\[
 \boxed{
 \begin{aligned}
 \mathfrak H^{\rm hyb}_{N,R}(\mathcal D)
 &=\sup_{\tau\in\mathcal D_g}
   \int_0^\infty\bigl(\#A_\tau(\lambda)-N\bigr)_+\,d\lambda,\\
 \mathfrak H^{\rm fix}_{N,R}(\mathcal D)
 &=\inf_{S\in\mathscr S_N}\sup_{\tau\in\mathcal D_g}
   \int_0^\infty\#\bigl(A_\tau(\lambda)\setminus S\bigr)\,d\lambda,\\
 \mathfrak O^{F,+}_{N,R}
 &=\int_0^\infty
   \bigl(\#A_o(\lambda)-N\bigr)_+\,d\lambda.
 \end{aligned}}
 \tag{S.480}
\]

For a nonnegative \(\ell^1\) sequence \(x\), the identity used here is
\[
 \inf_{\#S\le N}\sum_{k\notin S}x_k
 =\int_0^\infty(\#\{k:x_k>\lambda\}-N)_+\,d\lambda.
\]
It follows first for finite truncations by sorting, then for the full
sequence by monotone convergence.  The middle line of (S.480) is merely
Tonelli's identity for each fixed \(S,\tau\); neither optimization is moved
through the integral.

Equation (S.480) identifies the missing structure.  The direct gate may
delete a different set after every common good terminal time is known.  The
fixed gate asks for one hitting set across all common good terminal times.
The separable
positive-excursion gate replaces the family \(A_\tau(\lambda)\) by the
larger coordinatewise envelope \(A_o(\lambda)\).  More precisely,
\[
 \bigcup_{\tau\in\mathcal D_g}A_\tau(\lambda)
 \subseteq A_o(\lambda),
\]
and equality is not asserted because \(o_{k,R}^F\) ranges over every forward
increment of \(F_{k,R}\), not only the hybrid stops.  This replacement
forgets whether different shell peaks occur at mutually exclusive times.

## 3. Completed-clock simultaneous height

Define the fixed-deletion simultaneous height on a terminal domain by

\[
 \boxed{
 \mathfrak L^K_{N,R}(\mathcal D)
 :=
 \inf_{S\in\mathscr S_N}
 \sup_{t\in\mathcal D}\sum_{k\notin S}K_{k,R}(t).}
 \tag{S.481}
\]

It differs from the Step 17 separable maximum
\[
 \mathfrak M^K_{N,R}
 =\inf_{S\in\mathscr S_N}
   \sum_{k\notin S}\sup_{t\in I}K_{k,R}(t).
\]
The time supremum in \(\mathfrak L^K\) is outside the shell sum, but only
one deletion set is retained.

For an active hybrid coordinate, \(K=F+Q\), \(K\ge0\), and
\(\sigma_k^{\rm hyb}(\tau)\le\tau\) imply

\[
 \boxed{
 \begin{aligned}
 z_k(\tau)
 &=K_k(\tau)-K_k(\sigma_k^{\rm hyb}(\tau))
   -Q_k(\tau)+Q_k(\sigma_k^{\rm hyb}(\tau))\\
 &\le K_k(\tau)+\operatorname {TV}_I Q_k.
 \end{aligned}}
 \tag{S.482}
\]

The same inequality is trivial on inactive coordinates.  Sum it outside
one fixed \(S\), take the terminal supremum, and only then optimize.  This
proves

\[
 \boxed{
 \mathfrak H^{\rm fix}_{N,R}(\mathcal D)
 \le \mathfrak L^K_{N,R}(\mathcal D)+B_{Q,R}
 \le \mathfrak L^K_{N,R}(\mathcal D)+C_QA_R.}
 \tag{S.483}
\]

All clock sums are finite.  Indeed, the common zero start gives
\[
 K_k(t)\le o_{k,R}^F+\operatorname {TV}_I Q_{k,R},
\]
and hence
\[
 \sum_k\sup_{t\in I}K_k(t)\le B_{F,R}+B_{Q,R}<\infty.
\]

There is a reverse estimate at the same target scale.  Put
\[
 \Pi_R^{\boldsymbol\lambda}
 :=6B_{Q,R}
   +C_5\mathscr L(\boldsymbol\lambda)^{1/3}A_R
 \le C_{\rm pay}(\boldsymbol\lambda)A_R.
\]
Step 10 (S.235)
holds for every fixed \(S\in\mathscr S_N\) and every good terminal time:

\[
 \sum_{k\notin S}K_{k,R}(\tau)
 \le \Pi_R^{\boldsymbol\lambda}
      +6\sum_{k\notin S}r_k(\tau)
 \le \Pi_R^{\boldsymbol\lambda}
      +6\sum_{k\notin S}z_k(\tau).
\]

The second inequality is the coordinatewise Step 15 comparison
\(r_k\le z_k\).  The map \(t\mapsto(K_{k,R}(t))_k\) is continuous into
\(\ell^1\), and the common good-time set is dense.  Hence its supremum on
\(\mathcal D\) equals its supremum on \(\mathcal D_g\).  Take the
supremum for the same \(S\) and only then optimize to obtain

\[
 \boxed{
 \mathfrak L^K_{N,R}(\mathcal D)
 \le \Pi_R^{\boldsymbol\lambda}
      +6\mathfrak H^{\rm fix}_{N,R}(\mathcal D).}
 \tag{S.484}
\]

Thus, for a fixed admissible profile and fixed universal \(N\),
\[
 \mathfrak H^{\rm fix}_{N,R}(\mathcal D)\lesssim A_R
 \quad\Longleftrightarrow\quad
 \mathfrak L^K_{N,R}(\mathcal D)\lesssim A_R.
\]
This is an equivalence at the \(A_R\) scale after known payments.  It is
not a literal equality and does not identify either functional with the
weaker moving-deletion hybrid tail.

For every fixed deletion set, supremum of a sum is at most the sum of the
coordinatewise suprema.  Combining this with Step 17 (S.475) yields

\[
 \boxed{
 \mathfrak L^K_{N,R}(\mathcal D)
 \le\mathfrak M^K_{N,R}
 \le\mathfrak O^{F,+}_{N,R}+B_{Q,R}.}
 \tag{S.485}
\]

There is no universal reverse comparison from \(\mathfrak L^K\) to
\(\mathfrak M^K\); Section 5 gives an unbounded abstract separation.

## 4. The corrected open targets

The exact direct Step 15 target remains
\[
 \mathfrak H^{\rm hyb}_{N_0,R}(\mathcal T_R)
 \le C A_R
\]
for some universal finite \(N_0,C\).  It is equivalent, up to the literal
factor \(5\) in Step 15 (S.385), to the full residual gate.

If one insists that the exceptional shells be selected once for all common
good terminal times, the route-minimal fixed-deletion successor is

\[
 \boxed{
 \begin{gathered}
 \exists N_{\rm fix}\in\mathbb N_0,\ C_{\rm fix}<\infty
 \text{ for the fixed universal admissible profile, such that}\\
 \mathfrak H^{\rm fix}_{N_{\rm fix},R}(\mathcal T_R)
 \le C_{\rm fix}(P_R^M)^{2/3}
 \quad\text{uniformly in the solution and admissible }R,z_0.
 \end{gathered}}
 \tag{S.486}
\]

Equation (S.486) is **OPEN**.  It implies the direct hybrid gate by
(S.479), and therefore implies Step 10 (S.243), Q.12, and Q.1 through the
already-proved reductions.  It is stronger than the direct gate because
the direct exceptional set may depend on \(\tau\).

The target-scale-equivalent completed-clock formulation is

\[
\boxed{
 \begin{gathered}
 \exists N_L\in\mathbb N_0,\ C_L<\infty
 \text{ for the fixed universal admissible profile, such that}\\
 \bigl(\mathfrak L^K_{N_L,R}(\mathcal T_R)\bigr)^{3/2}
 \le C_LP_R^M
 \quad\text{uniformly in the solution and admissible }R,z_0.
 \end{gathered}}
 \tag{S.487}
\]

Equation (S.487) is also **OPEN**.  Equations (S.483)--(S.484) show that
it is equivalent at the target scale to (S.486), with constants depending
only on the same frozen admissible profile.  Both are stronger than the
direct moving-deletion gate.

The inherited unconditional information gives only

\[
 \boxed{
 \mathfrak H^{\rm fix}_{N,R}(\mathcal D)
 \le B_{F,R}\le C_FP_R^M,\qquad
 \mathfrak L^K_{N,R}(\mathcal D)
 \le B_{F,R}+B_{Q,R}
 \le C_FP_R^M+C_QA_R.}
 \tag{S.488}
\]

For \(P_R^M\le1\), the first estimate is already at most \(C_FA_R\).
For \(P_R^M>1\), it misses the target by the factor
\((P_R^M)^{1/3}\).  No manipulation of the displayed linear ledger alone
removes that factor.

## 5. Exact abstract separation by disjoint triangular clocks

Fix integers \(M>N\), a height \(H>0\), and \(I=[0,1]\).  For
\(1\le j\le M\), let

\[
 \boxed{
 \phi_j(t)
 =\left(1-2M\left|t-\frac{2j-1}{2M}\right|\right)_+,
 \qquad
 K_j(t)=F_j(t)=H\phi_j(t),\qquad Q_j(t)=0,}
 \tag{S.489}
\]

and set every later coordinate to zero.  The interiors of the supports are
pairwise disjoint.  For this abstract test, take the common-zero-start
increment \(z_j(\tau)=F_j(\tau)-F_j(0)=H\phi_j(\tau)\).

At each time at most one coordinate is positive.  Every fixed deletion set
with at most \(N<M\) elements leaves the peak of some coordinate.  Each
coordinate has positive excursion, clock maximum, and positive variation
equal to \(H\), and total variation equal to \(2H\).  Therefore

\[
 \boxed{
 \begin{aligned}
 \mathfrak H^{\rm hyb}_N
 &=
 \begin{cases}
 H,&N=0,\\
 0,&N\ge1,
 \end{cases}
 &\mathfrak H^{\rm fix}_N&=H,
 &\mathfrak L^K_N&=H,\\
 \mathfrak O_N^{F,+}
 &=\mathfrak M_N^K=\mathfrak V_N^K=(M-N)H,
 &\mathfrak H^F_{1,N}&=2(M-N)H,
 &\sum_j\operatorname {TV}F_j&=2MH.
 \end{aligned}}
 \tag{S.490}
\]

In particular, if \(N\ge1\) and \(M\ge N+2\), then

\[
 \boxed{
 0=\mathfrak H^{\rm hyb}_N
 <\mathfrak H^{\rm fix}_N
 =\mathfrak L^K_N
 <\mathfrak O_N^{F,+}
 =\mathfrak M_N^K.}
 \tag{S.491}
\]

The ratio
\[
 {\mathfrak O_N^{F,+}\over\mathfrak H_N^{\rm fix}}=M-N
\]
is unbounded at fixed \(N\) as \(M\to\infty\).  Thus there is no universal
reverse comparison from the fixed simultaneous functional to the separable
coordinatewise maximum in the abstract clock class.

The previously tempting choice \(M=N+1\) does not prove the second strict
inequality: then
\[
 \mathfrak H_N^{\rm fix}
 =\mathfrak L_N^K
 =\mathfrak O_N^{F,+}
 =\mathfrak M_N^K=H.
\]
It separates moving deletion from fixed deletion when \(N\ge1\), but not
fixed simultaneous height from coordinatewise maxima.

### 5.1 Why the linear ledger cannot create a \(2/3\) power

Normalize the abstract payment by the full absolute-flux ledger
\[
 \mathcal P:=\sum_{j=1}^M\operatorname {TV}F_j=2MH.
\]
For fixed \(N\), fix any \(M>N\) and let \(H\to\infty\).  Then

\[
 \boxed{
 {\mathfrak H_N^{\rm fix}\over\mathcal P^{2/3}}
 =
 {\mathfrak L_N^K\over\mathcal P^{2/3}}
 =
 {H^{1/3}\over(2M)^{2/3}}
 \longrightarrow\infty.}
 \tag{S.492}
\]

Consequently, the abstract assumptions
\[
 K\ge0,\qquad K=F+Q,\qquad
 B_Q\lesssim\mathcal P^{2/3},\qquad
 \sum_k\operatorname {TV}F_k\lesssim\mathcal P
\]
do not imply a fixed-deletion quadratic bound for any prescribed finite
\(N\).  The height \(H\) is an independent parameter; varying only
\(M=N+1\) with \(H=M^3\) would test uniformity in \(N\), not disprove a
fixed-\(N\) statement.

Equations (S.489)--(S.492) are **ABSTRACT CLOCK STRESS TESTS**.  They are
not spatial fields, do not realize the Version-M payment, and are not
Navier--Stokes solutions or counterexamples.

## 6. The recurrent Taylor family passes the surviving gates

On the exact smooth family of Step 17, first fix a finite \(N\), then choose
and fix \(R\) as in Step 17 (S.451).  For that quantified choice and
\(A\ge A_0(N,R)\),

\[
 \mathfrak O^{F,+}_{N,R}\asymp_{N,R}A^2,
 \qquad
 B_{Q,R}=O_R(A^2),
 \qquad
 P_R^M\asymp_RA^3.
\]

Equations (S.479) and (S.485) therefore give

\[
 \boxed{
 \mathfrak H^{\rm hyb}_{N,R}
 \le\mathfrak H^{\rm fix}_{N,R}
 \lesssim_{N,R}A^2
 \asymp_{N,R}(P_R^M)^{2/3},
 \qquad
 \mathfrak L^K_{N,R}(\mathcal T_R)\lesssim_{N,R}A^2.}
 \tag{S.493}
\]

This is a fixed-\(R\) screen, not a proof of the universal estimates
(S.486) or (S.487).  It shows only that the family which destroys absolute
temporal variation is compatible with all surviving quadratic gates.  The
same recurrence creates \(O(A)\) repeated circuits, but their peaks occur
in the same phase geometry and their signed excursion remains \(O(A^2)\).

## 7. What a successful PDE theorem must add

The exact reductions leave three nested research targets.

1. **Direct hybrid target.**  Prove the moving-deletion
   \(\mathfrak H^{\rm hyb}\lesssim A_R\).  This is the weakest target and
   exactly matches the Step 15 route.
2. **Fixed-deletion target.**  Prove (S.486).  This requires one common
   finite shell set, but retains simultaneous terminal incidence and avoids
   coordinatewise temporal overcount.
3. **Completed-clock equivalent target.**  Prove (S.487), or the stronger
   Step 17 positive-excursion bound.  The simultaneous-height form is
   equivalent to the fixed hybrid gate after known payments; the separable
   positive-excursion form still demands extra cross-time information.

The triangular clocks prove that a new input cannot consist only of
nonnegativity and the inherited linear ledgers.  A viable theorem must add
at least one genuinely PDE-specific mechanism, for example:

- a simultaneous height-to-cubic-payment estimate;
- persistence or dwell-time forcing a high clock aggregate to occupy
  enough parabolic time to be paid cubically;
- a deterministic stopping-time/Carleson charge that controls the
  time--shell incidence sets in (S.480); or
- a signed entrance or collar-flux payment tied to the hybrid first-passage
  intervals.

These are mechanism classes, not proved lemmas.

## 8. Primary-source collision boundary

A bounded two-wave primary-source search did not locate a theorem with all
of the quantifiers in (S.486): deterministic suitable weak solutions; for
each fixed solution, scale, centre, and terminal domain, one finite shell
deletion retained over every common good terminal time; an infinite-shell
\(\ell^1\) sum of forward stopped increments; a universal deletion budget;
and a \((P_R^M)^{2/3}\) payment.

- Dascaliuc and Grujić, *Energy cascades and flux locality in physical
  scales of the 3D Navier--Stokes equations*
  (https://arxiv.org/abs/1101.2193), prove signed time/ensemble-averaged
  physical-space flux estimates under an inertial-range condition.  Their
  result is not a terminal-time maximum with one shell deletion.
- Yang, *Construction of Maximal Functions associated with Skewed
  Cylinders Generated by Incompressible Flows and Applications*
  (https://arxiv.org/abs/2008.05588), proves weak-\((1,1)\) and
  strong-\((p,p)\) bounds for space-time averages over flow-generated
  cylinders.  It does not control the simultaneous clock height or the
  fixed best-\(N\) terminal functional.
- Yu, *Finite-Chain CKN-Bad Scale Counting for Navier-Stokes*
  (https://arxiv.org/abs/2606.21783), gives a weighted count on a
  preassigned finite scale chain using nonnegative channel costs and a
  one-component compactness closure.  It concludes that small total
  finite-chain cost yields at least one CKN-small scale; it does not give
  the infinite-shell, all-good-terminal bound (S.486).
- Yu, *Coarse-Grained Resolution and Pressure-Flux Work Depletion for
  Navier-Stokes CKN Badness* (https://arxiv.org/abs/2606.25322), gives an
  exact fixed-chain signed-work depletion theorem.  The paper explicitly
  retains negative work/backscatter and does not claim smallness of the
  negative set, uniform moving-window constants, or summability as the
  chain length tends to infinity.

These are adjacent tools and possible ingredients, not proofs of the open
gate.  The search was bounded and its non-hit is not a novelty or priority
claim.

## 9. Claim ledger and route decision

The following are **PROVED**:

- the hierarchy and infinite-shell justification (S.476)--(S.479);
- the exact layer-cake incidence formulas (S.480);
- the completed-clock two-sided target-scale reduction and comparison
  (S.481)--(S.485);
- the unconditional linear fallback (S.488);
- every value in the abstract triangular-clock test (S.489)--(S.492); and
- the fixed-\(R\) Taylor-family compatibility screen (S.493).

The following are **ABSTRACT ONLY**:

- strictness and unbounded reverse ratios in (S.491);
- failure of the listed ledger assumptions to imply a \(2/3\)-power bound
  in (S.492).

The following are **OPEN**:

- the direct moving-deletion hybrid gate;
- the route-minimal fixed-deletion gate (S.486);
- its target-scale-equivalent simultaneous-height gate (S.487);
- the Step 17 positive-excursion gate (S.472);
- terminal-crown coercivity (S.407), Q.12, Q.1, scale contraction, and
  regularity.

The route decision is now exact.  Future fixed-deletion work should target
\(\mathfrak H^{\rm fix}\), not automatically the stronger
\(\mathfrak O^{F,+}\).  Future completed-clock work may target
\(\mathfrak L^K\), which is equivalent at the target scale after the known
paid term.  The
weakest valid route remains the direct Step 15 hybrid gate with a
terminal-dependent deletion set.
