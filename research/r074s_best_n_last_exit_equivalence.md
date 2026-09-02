# R0.74S Step 9 — canonical best-\(N\) last exits are terminal-tail representations, not a new compression

## 0. Result and scope

Step 8 closes two logically separate points.  First, the dissipation and
defect residuals reduce to the stopped signed-work gate from Step 2.  Second,
that gate, without terminal exceptions, is equivalent up to the already-paid
quadratic row to the full-time positive cumulative flux and is therefore
false at the desired quadratic scale on the inherited R0.74O/P smooth exact
family.

The next admissible route must restore the terminal-dependent, fixed
best-\(N\) exceptions of R0.74Q.  This note makes that repair canonical and
tests whether a last-exit construction supplies any additional compression.
There are two exact representations.

1. A signed \(F\)-half-exit converts the forced full tail of stopped fluxes
   exactly into one half of the signed best-\(N\) terminal tail.
2. A \(K\)-level last exit converts the forced full tail of stopped fluxes
   into \((1-\theta)\) times the nonnegative best-\(N\) clock tail, with a
   sharp error of one full \(Q\)-variation ledger.  When
   \(0<\theta<3/4\), every finite positive-terminal part at a good terminal
   time lies in the closure of the strict Step 2 upcrossing class.

These identities fix the correct order
\(\sup_\tau\inf_{\#S_\tau\le N}\), retain cancellation in the entire
nonexceptional tail, and remove arbitrary choices of stopping times.  They do
**not** prove a new shell-packing estimate: after the already-paid \(Q\) row
is removed, both constructions are quantitatively equivalent to the open
R0.74Q best-\(N\) tail.  The \(F\)-half-exits need not satisfy the Step 2
upcrossing condition, and neither infinite tail is inserted directly as a
local-energy test.  No fixed \(N_0\), quadratic tail estimate, regularity, or
Millennium conclusion is proved.  **NOT CLAY.**

No novelty or priority claim is made.

## 1. Terminal domains and the fixed best-\(N\) order

Retain the fixed-scale Version-M setting and canonical continuous clocks from
R0.74P--R0.74S.  It is important to distinguish the inherited plateau
terminal domain \(I_R\) from the full clock interval
\(\mathcal T_R=(s_R,t_0)\).  For
\(\mathcal D\in\{I_R,\mathcal T_R\}\), put

\[
 \boxed{
 \mathfrak C_R^M(\mathcal D)
 :=\sup_{\tau\in\mathcal D}
      \left[\sum_{k\ge1}F_{k,R}(\tau)\right]_+,
 \qquad
 \mathfrak C_R^M(I_R)=\mathfrak C_R^M,
 \qquad
 \mathfrak C_R^M(\mathcal T_R)
   =\mathfrak C_{{\rm full},R}^M.}
\tag{S.200}
\]

Only the inequality
\(\mathfrak C_R^M\le\mathfrak C_{{\rm full},R}^M\) is inherited; equality
is neither used nor asserted.  Write

\[
 \boxed{
 A_R:=(P_R^M)^{2/3},
 \qquad Z_R:=Y_{2,R}^{\rm sf},
 \qquad
 B_{Q,R}^M:=\sum_{k\ge1}
       \operatorname {TV}_{[s_R,t_0)}Q_{k,R}
       \le C_QA_R.}
\tag{S.201}
\]

Here
\(v_{k,R}:=\operatorname {Var}_{[s_R,t_0)}^+K_{k,R}\), so that
\(Z_R=(\sum_kv_{k,R}^2)^{1/2}\) and \(K_{k,R}(\tau)\le v_{k,R}\).
These are the inherited clock and square-function conventions.

For every shell,

\[
 K_{k,R}=Q_{k,R}+F_{k,R},
 \qquad
 Q_{k,R}(s_R)=F_{k,R}(s_R)=K_{k,R}(s_R)=0,
 \qquad K_{k,R}\ge0.
\]

The three primitives are continuous.  Moreover,
\(\sum_k\operatorname {TV}F_{k,R}<\infty\),
\(\sum_k\operatorname {TV}Q_{k,R}<\infty\), and Step 8 proves
\(\sum_kK_{k,R}(\tau)<\infty\).  All infinite series below are therefore
absolutely convergent.

For \(x\in\ell^1(\mathbb N;\mathbb R)\) and an integer \(N\ge0\), retain
the R0.74Q functional

\[
 \boxed{
 \mathcal S_N(x)
 :=\inf_{S\subset\mathbb N,\ \#S\le N}
       \left[\sum_{k\notin S}x_k\right]_+.}
\tag{S.202}
\]

Its domain-parametrized clock and flux versions are

\[
 \boxed{
 \begin{aligned}
 \mathcal S_{N,R}^{K}(\mathcal D)
  &:=\sup_{\tau\in\mathcal D}
       \mathcal S_N((K_{k,R}(\tau))_k),\\
 \mathcal S_{N,R}^{F}(\mathcal D)
  &:=\sup_{\tau\in\mathcal D}
       \mathcal S_N((F_{k,R}(\tau))_k).
 \end{aligned}}
\tag{S.203}
\]

The signed functional is genuinely an \(\ell^1\) full-tail quantity.  If
\((x_m^{+*})_{m\ge1}\) is the nonincreasing rearrangement of the positive
coordinates of \(x\), padded by zeroes, then

\[
 \mathcal S_N(x)
 =\left[\sum_kx_k-\sum_{m=1}^{N}x_m^{+*}\right]_+
 =\left[\sum_{m>N}x_m^{+*}-\|x_-\|_{\ell^1}\right]_+,
 \qquad
 |\mathcal S_N(x)-\mathcal S_N(y)|\le\|x-y\|_{\ell^1}.
\]

The first identity follows because an optimal set deletes only the largest
positive coordinates; the second estimate follows by comparing the same
set in the two infima.  In particular, positive part and infimum commute,
but an arbitrary finite-subset supremum cannot reconstruct the signed tail.
The summable variation bounds and finite-head continuity also imply
\(t\mapsto(F_{k,R}(t))_k\) and \(t\mapsto(K_{k,R}(t))_k\) are continuous
into \(\ell^1\).  Hence the supremum over the common dense good-time set
equals the all-time supremum on either terminal domain.

Thus \(N\) is fixed independently of the terminal time, scale, and
solution, while a minimizing or approximating set \(S=S_\tau\) may depend on
\(\tau\).  This is the order
\(\sup_{\tau}\inf_{S_\tau}\), not
\(\inf_S\sup_\tau\).

## 2. The exact signed half-exit representation

Fix \(\tau\in\mathcal D\), and write \(f_k=F_{k,R}(\tau)\).  If
\(f_k\ne0\), define the terminal half-exit

\[
 \boxed{
 \ell_{k}^{F}(\tau)
 :=\max\left\{t\in[s_R,\tau]:
      \operatorname {sgn}(f_k)F_{k,R}(t)
          \le {|f_k|\over2}\right\};
 \qquad
 \ell_k^F(\tau):=\tau\quad\hbox{if }f_k=0.}
\tag{S.204}
\]

The defining set is nonempty because \(F_k(s_R)=0\), is compact by
continuity, and excludes \(\tau\) when \(f_k\ne0\).  At its maximum the
inequality is an equality: otherwise continuity would extend the defining
set to the right.  Consequently

\[
 \boxed{
 F_{k,R}(\ell_k^F(\tau))={1\over2}F_{k,R}(\tau),
 \qquad
 F_{k,R}(\tau)-F_{k,R}(\ell_k^F(\tau))
     ={1\over2}F_{k,R}(\tau).}
\tag{S.205}
\]

Define the forced-full-tail half-exit observable by

\[
 \boxed{
 \mathfrak W_{1/2,N,R}^{F}(\mathcal D)
 :=\sup_{\tau\in\mathcal D}
   \inf_{\#S\le N}
   \left[
    \sum_{k\notin S}
     \bigl(F_{k,R}(\tau)-F_{k,R}(\ell_k^F(\tau))\bigr)
   \right]_+.}
\tag{S.206}
\]

The sum is well defined since (S.205) gives
\(\sum_k|\Delta F_k|=\frac12\sum_k|F_k(\tau)|<\infty\).  Substitution
before taking the positive part, infimum, and supremum gives the exact
identity

\[
 \boxed{
 \mathfrak W_{1/2,N,R}^{F}(\mathcal D)
   ={1\over2}\mathcal S_{N,R}^{F}(\mathcal D).}
\tag{S.207}
\]

For the plateau domain, the signed version of the R0.74Q terminal reduction
can be written with the sharp explicit \(Q\) row as

\[
 \boxed{
 \mathfrak C_R^M
 \le B_{Q,R}^M+\sqrt N\,Z_R
       +2\mathfrak W_{1/2,N,R}^{F}(I_R).}
\tag{S.208}
\]

Indeed, for every \(S\) with \(\#S\le N\), the exceptional flux is bounded
above by
\(\sum_{k\in S}v_{k,R}+\sum_{k\in S}\operatorname {TV}Q_{k,R}\), and
Cauchy--Schwarz gives \(\sum_{k\in S}v_{k,R}\le\sqrt N Z_R\).  The
nonexceptional row is exactly (S.202), and (S.207) finishes the proof.

The half-exit times in (S.204) are canonical algebraic stops, but they need
not be admissible in the Step 2 supremum (S.37).  On \([0,1]\), for example,

\[
 \boxed{
 F(t)=t,
 \qquad K(t)=\min\{2t,1\},
 \qquad Q(t)=K(t)-F(t),
 \qquad \tau=1.}
\tag{S.209}
\]

Here \(\ell^F(1)=1/2\), but
\(K(1)-K(1/2)=0\), so the strict upcrossing condition (S.25) fails.  Since
the common good-time set is dense and \(F_k\) is continuous, each finite
family of half-exit increments is the limit of increments with good stopping
times.  This closure statement does not turn them into (S.37)-admissible
upcrossings.

## 3. The \(K\)-level last exit and the sharp \(Q\) error

Let \(0<\theta<1\), fix \(\tau\in\mathcal D\), and put
\(T_k=K_{k,R}(\tau)\).  For \(T_k>0\), define

\[
 \boxed{
 \ell_{k,\theta}^{K}(\tau)
 :=\max\{t\in[s_R,\tau]:K_{k,R}(t)\le\theta T_k\};
 \qquad
 \ell_{k,\theta}^{K}(\tau):=\tau\quad\hbox{if }T_k=0.}
\tag{S.210}
\]

Continuity and the zero start give
\(K_k(\ell_{k,\theta}^{K})=\theta T_k\).  With

\[
 \Delta Q_{k,\theta}(\tau)
 :=Q_{k,R}(\tau)-Q_{k,R}(\ell_{k,\theta}^{K}(\tau)),
\]

the exact balance \(F=K-Q\) yields

\[
 \boxed{
 L_{k,\theta}(\tau)
 :=F_{k,R}(\tau)-F_{k,R}(\ell_{k,\theta}^{K}(\tau))
 =(1-\theta)T_k-\Delta Q_{k,\theta}(\tau).}
\tag{S.211}
\]

Define, again with the complete nonexceptional tail retained,

\[
 \boxed{
 \mathfrak W_{\theta,N,R}^{K}(\mathcal D)
 :=\sup_{\tau\in\mathcal D}
   \inf_{\#S\le N}
   \left[\sum_{k\notin S}L_{k,\theta}(\tau)\right]_+.}
\tag{S.212}
\]

This infinite sum is absolute, since

\[
 \sum_k|L_{k,\theta}(\tau)|
 \le(1-\theta)\sum_kT_k+B_{Q,R}^M<\infty.
\]

For each fixed pair \((\tau,S)\), the Lipschitz property of the positive
part and the shellwise variation ledger give

\[
 \boxed{
 \left|
  \left[\sum_{k\notin S}L_{k,\theta}(\tau)\right]_+
  -(1-\theta)\sum_{k\notin S}T_k
 \right|
 \le\sum_{k\notin S}|\Delta Q_{k,\theta}(\tau)|
 \le B_{Q,R}^M.}
\tag{S.213}
\]

The clock tail is nonnegative, so its positive part is redundant.  Taking
the infimum in \(S\) and then the supremum in \(\tau\) preserves the same
error, not twice the error.  Thus

\[
 \boxed{
 (1-\theta)\mathcal S_{N,R}^{K}(\mathcal D)-B_{Q,R}^M
 \le\mathfrak W_{\theta,N,R}^{K}(\mathcal D)
 \le(1-\theta)\mathcal S_{N,R}^{K}(\mathcal D)+B_{Q,R}^M.}
\tag{S.214}
\]

The coefficient one is sharp already for a scalar continuous clock.  Take
\(K(t)=t\) on \([0,1]\), \(\tau=1\), keep \(Q=0\) through the last exit
\(t=\theta\), and then vary \(Q\) monotonically to either \(B\) or
\(-B\), where \(0<B\le1-\theta\).  Its total variation is \(B\), and the
positive part in (S.213) differs from \(1-\theta\) by exactly \(B\).

Unlike the signed half-exit, this construction is compatible with the
strict Step 2 upcrossing class whenever

\[
 \boxed{
 0<\theta<{3\over4}:
 \qquad
 T_k>0,
 \qquad
 K_{k,R}(\tau)-K_{k,R}(\ell_{k,\theta}^{K}(\tau))
 =(1-\theta)T_k>{1\over4}T_k.}
\tag{S.215}
\]

The canonical last exit need not itself be a good time.  Fix a good terminal
\(\tau\) and a finite set \(G\subset\{k:T_k>0\}\).  Continuity leaves,
around every canonical stop, a neighborhood in which \(K_k<3T_k/4\);
density of the common good-time set supplies good stops in those
neighborhoods.  Their stopped fluxes converge to (S.211) and retain the
strict inequality (S.25).  Shells with \(T_k=0\) have
\(L_{k,\theta}=0\) and are omitted.  Absolute convergence then permits a
prescribed finite-shell exhaustion.  The all-time algebraic best-\(N\) clock
tail in (S.203), not the canonical last-exit selector itself, is recovered
from good terminal times by the \(\ell^1\)-continuity observation following
(S.203); (S.214) then compares that tail with the last-exit observable within
\(B_{Q,R}^M\).  This proves a good-stop closure statement only at good
terminals, not continuity of the last-exit map or the right to insert one
infinite, temporally discontinuous cutoff into the local energy inequality.
The endpoint \(\theta=3/4\) is excluded because no strict margin remains.

Combining the clock version of the R0.74Q terminal reduction with the lower
bound in (S.214) gives

\[
 \boxed{
 \mathfrak C_R^M
 \le \sqrt N\,Z_R
    +{\mathfrak W_{\theta,N,R}^{K}(I_R)\over1-\theta}
    +\left(1+{1\over1-\theta}\right)B_{Q,R}^M.}
\tag{S.216}
\]

## 4. Equivalence with the existing R0.74Q gate

For every \((\tau,S)\), the full nonexceptional \(F\) and \(K\) sums differ
by \(-\sum_{k\notin S}Q_k(\tau)\), whose absolute value is at most
\(B_{Q,R}^M\).  The same infimum--supremum stability used above proves

\[
 \boxed{
 \left|\mathcal S_{N,R}^{F}(\mathcal D)
       -\mathcal S_{N,R}^{K}(\mathcal D)\right|
 \le B_{Q,R}^M.}
\tag{S.217}
\]

Consequently, for a fixed integer \(N_0\) independent of \(R\) and the
solution, and for either fixed terminal domain,

\[
 \boxed{
 \begin{aligned}
 \mathcal S_{N_0,R}^{F}(\mathcal D)\lesssim A_R
 &\quad\Longleftrightarrow\quad
 \mathfrak W_{1/2,N_0,R}^{F}(\mathcal D)\lesssim A_R,\\
 \mathcal S_{N_0,R}^{K}(\mathcal D)\lesssim A_R
 &\quad\Longleftrightarrow\quad
 \mathfrak W_{\theta,N_0,R}^{K}(\mathcal D)\lesssim A_R,
 \qquad 0<\theta<1.
 \end{aligned}}
\tag{S.218}
\]

Here the implicit constants may depend on the fixed \(\theta\), and the
second equivalence uses \(B_{Q,R}^M\le C_QA_R\).  Equation (S.218) is the
precise no-gain conclusion: a proof of a last-exit quadratic bound would be
a proof of the already-open best-\(N\) terminal-tail estimate, not a weaker
intermediate theorem obtained from the completed-clock algebra alone.
Taking \(\mathcal D=\mathcal T_R\) recovers exactly the full-terminal
R0.74Q gate (Q.12).  Taking \(\mathcal D=I_R\) gives its weaker plateau
restriction, which is sufficient for the plateau observable
\(\mathfrak C_R^M\).

## 5. Quantifier and cancellation stress tests

The terminal dependence of the exceptional set is essential.  With two
terminal states

\[
 \boxed{
 x(\tau_1)=(1,0),
 \qquad x(\tau_2)=(0,1),
 \qquad N=1,}
\tag{S.219}
\]

one has
\(\sup_\tau\inf_{\#S_\tau\le1}\sum_{k\notin S_\tau}x_k=0\), whereas
\(\inf_{\#S\le1}\sup_\tau\sum_{k\notin S}x_k=1\).  A single fixed
exceptional set is strictly stronger than the target and must not be
silently substituted.

The complete signed tail is equally essential.  For the terminal flux vector

\[
 \boxed{F(\tau)=(1,-1),\qquad N=0,}
\tag{S.220}
\]

(S.207) gives zero, while applying an arbitrary finite-subset supremum to the
half-exit vector selects only the positive coordinate and gives \(1/2\).
Thus that substitution destroys precisely the cancellation that the signed
best-\(N\) repair is intended to retain.  This two-coordinate calculation is
not asserted to be an (S.25)-admissible Step 2 family.

Finally, let \(h:[s_R,t_0)\to[0,H]\) be continuous, with
\(h(s_R)=0\), and suppose it has reached the plateau height \(H>0\) by the
chosen terminal time \(\tau\).  Take a scalar completed-clock family with
\(M>N\) simultaneous shells,

\[
 \boxed{
 K_k(t)=F_k(t)=h(t),
 \qquad Q_k=0,
 \qquad 1\le k\le M.}
\tag{S.221}
\]

At a plateau terminal time,

\[
 \mathcal S_N(F(\tau))=\mathcal S_N(K(\tau))=(M-N)H,
 \qquad
 \mathfrak W_{1/2,N}^F={M-N\over2}H,
 \qquad
 \mathfrak W_{\theta,N}^K=(1-\theta)(M-N)H.
\]

This is an abstract continuous-clock stress test, not a Navier--Stokes
solution.  It shows that last exits alone do not convert an \(\ell^1\) tail
into an \(\ell^2\) payment.

Two one-shell boundary rows show why the \(Q\) errors and the full history
cannot be removed.  If \(K\equiv0\), while \(F\) rises continuously from
zero to \(B\) and \(Q=-F\), then
\(\mathcal S_0^K=0\), \(\mathcal S_0^F=B\), and
\(\mathfrak W_{1/2,0}^F=B/2\); no strict (S.25) stop exists, and (S.217)
is sharp because \(B_Q=B\).  If instead \(K=Q=h\) and \(F=0\), then the
\(K\)-tail is positive while every last-exit flux increment vanishes; the
error is necessarily carried by \(Q\).  Finally, if \(K=F=h\) reaches its
plateau before a proposed recent window begins, that recent window contains
no \(\theta\)-level exit at all.  Thus (S.210) must retain the full history
\([s_R,\tau]\) unless an additional PDE theorem pays the earlier segment.

## 6. Route decision

The value \(\theta=2/3\) is useful for the next PDE decomposition because it
matches the one-sixth rows in Step 8:

\[
 \boxed{
 \Delta K_{k,2/3}={1\over3}T_k,
 \qquad
 |\Delta Q_{k,2/3}|<{1\over6}T_k
 \quad\Longrightarrow\quad
 \Delta F_{k,2/3}>{1\over6}T_k.}
\tag{S.222}
\]

This is a compatibility choice, not a global optimization theorem; the
pure algebraic coefficient \((1-\theta)^{-1}\) improves as
\(\theta\downarrow0\).  The next genuinely new target is therefore not
another definition of stopped work.  It is a PDE packing statement for a
forced full residual tail after the Step 7 low-Rayleigh branch and the Step 8
\(Q\)-visible \(\mathcal I_\beta\) and kinetic-mass
\(\mathcal I_\sigma\) branches have been removed, with at most \(N_0\)
terminal-dependent exceptions paid by \(\sqrt{N_0}Z_R\).  That residual may
still contain anomalous-defect or high-Rayleigh dissipation and will be
defined and audited in the next step.

## 7. Decision and claim ledger

The following are **PROVED**:

- the terminal-domain separation and domain-parametrized best-\(N\) tails
  (S.200)--(S.203);
- the canonical signed half-exit identity and exact representation
  (S.204)--(S.207);
- the plateau terminal reduction (S.208);
- the explicit failure of Step 2 admissibility for general signed half-exits
  (S.209);
- the \(K\)-last-exit identity, sharp one-\(B_Q\) comparison, and finite
  good-stop closure for \(0<\theta<3/4\), (S.210)--(S.215);
- the plateau reduction (S.216), the signed/nonnegative tail comparison
  (S.217), and the exact no-gain equivalences (S.218); and
- the quantifier, cancellation, and simultaneous-plateau stress tests
  (S.219)--(S.221), together with the \(\theta=2/3\) implication (S.222).

The following are **INHERITED**:

- continuity and zero initial values of \(Q,F,K\), nonnegativity of \(K\),
  and absolute summability of the shell ledgers from R0.74P;
- the quadratic \(Q\)-variation bound and square function \(Z_R\) from
  R0.74P;
- the terminal best-\(N\) reduction from R0.74Q; and
- the distinction between the plateau and full-time flux suprema, and the
  refutation of the no-exception quadratic gate, from Step 8.

The following are **REFUTED**:

- the universal no-exception antecedent
  \(\mathfrak W_{{\rm up},R}^M\lesssim A_R\), by the Step 8/R0.74O--P
  smooth exact family.  The conditional implication (S.38) remains valid;
  and
- the claim that choosing canonical last exits alone creates a quadratic
  shell compression; equations (S.207), (S.214), and (S.218) give an exact
  equivalence with the existing best-\(N\) tails, modulo \(B_Q\).

The following remain **OPEN**:

- a fixed \(N_0\), solution- and scale-independent PDE estimate for either
  best-\(N_0\) tail in (S.218);
- the residual full tail to be defined and audited in the next step, after
  the already-proved Step 7/8 paid branches are removed;
- the fixed-scale inequality (Q.1), the R0.74R extraction hypotheses, scale
  contraction, prescribed-centre packing, and regularity.

The following are **NOT CLAIMED**:

- that the \(F\)-half-exits satisfy (S.25), or that any canonical last exit
  is itself a good time;
- that the canonical last-exit selector is continuous in the terminal time;
- that one infinite stopped cutoff is an admissible local-energy test;
- that an arbitrary finite-subset supremum may replace the forced full tail;
- that \(\sup_\tau\inf_{S_\tau}\) may be replaced by
  \(\inf_S\sup_\tau\);
- that \(I_R\) and \(\mathcal T_R\) give the same flux supremum;
- that the R0.74O/P single dominant packet proves \(N_0=1\) is sufficient;
- that the scalar stress tests are PDE solutions; or
- novelty, priority, singularity formation, or a solution of the
  Navier--Stokes Millennium problem.

## 8. Inherited source ledger

| Use in this note | Frozen source | Status |
|---|---|---|
| Canonical continuous shell clocks, zero starts, absolute \(Q/F\) variation, and square function | R0.74P, (2.7)--(3.7) | **INHERITED / PROVED** |
| Best-\(N\) terminal tails and \(\sqrt N Z_R\) exceptional payment | R0.74Q, (Q.7)--(Q.12) | **INHERITED / PROVED REDUCTION; PDE TAIL BOUND OPEN** |
| Strict terminal upcrossing condition and arbitrary finite-family stopped-work supremum | R0.74S Step 2, (S.25)--(S.38) | **INHERITED / CONDITIONAL IMPLICATION PROVED** |
| Plateau/full-time separation, sharp \(B_Q\) comparison, and no-exception exact-family refutation | R0.74S Step 8, (S.197)--(S.199) | **INHERITED / PROVED** |

The new content is the domain-safe canonical last-exit representation,
sharp \(Q\)-error, good-stop closure, quantifier/cancellation audit, and
no-gain theorem (S.200)--(S.222).  No novelty or priority claim is made.

**NOT CLAY.**
