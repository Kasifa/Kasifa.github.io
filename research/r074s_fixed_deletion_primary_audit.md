# R0.74S Step 18 — primary analytic audit

## 0. Audited object and verdict

This audit reviews
research/r074s_fixed_deletion_simultaneous_height.md, equations
(S.476)--(S.493).

**Verdict: PASS within the stated route-reduction scope.**  The note proves
the exact hierarchy

\[
 \mathfrak H^{\rm hyb}
 \le \mathfrak H^{\rm fix}
 \le \mathfrak O^{F,+}
 \le \mathfrak H^F_{1,N},
\]

and the two paid comparisons

\[
 \mathfrak H^{\rm fix}\le\mathfrak L^K+B_Q,
 \qquad
 \mathfrak L^K\le\Pi_R^{\boldsymbol\lambda}
                     +6\mathfrak H^{\rm fix}.
\]

Thus the fixed-deletion stopped-flux height and completed-clock
simultaneous height are equivalent at the target \(A_R=(P_R^M)^{2/3}\)
scale.  Neither estimate proves that target bound.  The direct hybrid gate,
the fixed-deletion strengthening, Q.12, Q.1, scale contraction, regularity,
and the Millennium problem remain open.  **NOT CLAY.**

The pre-freeze audit found and repaired three scope defects:

1. the Taylor-family lower comparison now requires \(R\) to be chosen after
   \(N\) as in Step 17 (S.451);
2. \(A_o(\lambda)\) is now described as a larger all-forward-increment
   envelope, not as the exact temporal union of the hybrid incidence sets;
3. the open completed-clock statement now carries the full uniform
   quantifiers inside (S.487).

## 1. Equation-by-equation ledger

| Equation | Status | Audit conclusion |
|---|---|---|
| (S.476) | PROVED | The completed-clock identity, nonnegativity, common zero start, and inherited \(F,Q\) variation ledgers agree with the locked upstream notes. |
| (S.477) | DEFINITION | Moving and fixed deletion have the correct sup-inf and inf-sup order.  Fixing the shell set does not freeze the terminal-dependent hybrid starts. |
| (S.478) | DEFINITION | \(o_k^F\le\operatorname {TV}F_k\), hence \(o^F\in\ell^1_+\), and every hybrid increment satisfies \(0\le z_k(\tau)\le o_k^F\). |
| (S.479) | PROVED | Weak minimax and coordinatewise domination are applied to the same deletion set before optimization.  Attainment is unnecessary. |
| (S.480) | PROVED | Layer cake and best-\(N\) rearrangement are exact; the fixed-set line uses Tonelli before either optimization. |
| (S.481) | DEFINITION | The simultaneous-height functional uses one time for the whole surviving shell sum. |
| (S.482) | PROVED | \(K(\sigma)\ge0\) and the \(Q\)-variation give \(z_k(\tau)\le K_k(\tau)+\operatorname {TV}Q_k\). |
| (S.483) | PROVED | The same fixed set is retained through summation, terminal supremum, and optimization; \(B_Q\) is paid once. |
| (S.484) | PROVED | Step 10 (S.235), Step 15 \(r_k\le z_k\), \(\ell^1\)-continuity of \(K\), and dense good times yield the reverse comparison. |
| (S.485) | PROVED | Supremum of a nonnegative sum is bounded by the sum of coordinatewise suprema; Step 17 (S.475) supplies the second inequality. |
| (S.486) | OPEN | This is the common fixed-deletion quadratic target, with full uniform quantifiers. |
| (S.487) | OPEN | This is the completed-clock equivalent of (S.486), not a proved estimate. |
| (S.488) | PROVED | The inherited information gives a linear payment; for \(P>1\) the missing factor is exactly \(P^{1/3}\). |
| (S.489)--(S.492) | PROVED / ABSTRACT | The disjoint triangular clocks give exact strict separations and a fixed-\(N\) linear-ledger obstruction. |
| (S.493) | PROVED SCREEN | With \(N\) fixed and \(R\) then chosen by Step 17 (S.451), the recurrent Taylor family is compatible with every surviving quadratic gate. |

## 2. Exact minimax and incidence audit

For a nonnegative \(\ell^1\) vector \(x\), deleting at most \(N\)
coordinates minimizes the residual by deleting its \(N\) largest entries.
Consequently,

\[
 \inf_{\#S\le N}\sum_{k\notin S}x_k
 =
 \int_0^\infty
    \bigl(\#\{k:x_k>\lambda\}-N\bigr)_+\,d\lambda.
\]

Finite truncations prove the identity by sorting.  Monotone convergence
passes to \(x\in\ell^1_+\); no signed series is rearranged.

For every fixed set \(S\),

\[
 \inf_{\#T\le N}\sum_{k\notin T}z_k(\tau)
 \le\sum_{k\notin S}z_k(\tau).
\]

Taking the terminal supremum and then the infimum over \(S\) proves
\(\mathfrak H^{\rm hyb}\le\mathfrak H^{\rm fix}\).  The next comparisons
use

\[
 z_k(\tau)\le o_k^F\le\operatorname {TV}F_k.
\]

Because the comparison is made before optimizing \(S\), the hierarchy does
not mix separately optimal deletion sets.

The hybrid incidence sets satisfy only

\[
 \bigcup_{\tau\in\mathcal D_g}A_\tau(\lambda)
 \subseteq A_o(\lambda).
\]

The inclusion can be strict: \(o_k^F\) optimizes over every forward
increment, whereas \(A_\tau\) sees only the inherited hybrid start.  The
repaired main note now states this exact relation.

## 3. The two paid comparisons

### 3.1 From completed clocks to stopped flux

Fix \(S\in\mathscr S_N\).  On every active coordinate,

\[
 \begin{aligned}
 z_k(\tau)
 &=K_k(\tau)-K_k(\sigma_k(\tau))
   -Q_k(\tau)+Q_k(\sigma_k(\tau))\\
 &\le K_k(\tau)+\operatorname {TV}Q_k,
 \end{aligned}
\]

because \(K_k(\sigma_k(\tau))\ge0\).  Inactive coordinates are zero.
Therefore

\[
 \sup_{\tau\in\mathcal D_g}\sum_{k\notin S}z_k(\tau)
 \le
 \sup_{t\in\mathcal D}\sum_{k\notin S}K_k(t)+B_{Q,R}.
\]

Taking the infimum over the same \(S\) proves (S.483).

### 3.2 From stopped flux back to completed clocks

For every fixed \(S\) and every good terminal \(\tau\), Step 10 (S.235)
gives

\[
 \sum_{k\notin S}K_{k,R}(\tau)
 \le
 \Pi_R^{\boldsymbol\lambda}
6\sum_{k\notin S}r_k(\tau).
\]

Step 15 (S.383) gives \(r_k(\tau)\le z_k(\tau)\) coordinatewise.  Hence

\[
 \sup_{\tau\in\mathcal D_g}\sum_{k\notin S}K_{k,R}(\tau)
 \le
 \Pi_R^{\boldsymbol\lambda}
 +6\sup_{\tau\in\mathcal D_g}\sum_{k\notin S}z_k(\tau).
\]

For each fixed \(S\), the functional

\[
 x\longmapsto\sum_{k\notin S}x_k
\]

is continuous on \(\ell^1\), with operator norm at most one.  The inherited
map \(t\mapsto K(t)\) is continuous into \(\ell^1\), and the common
good-time set is dense in either open terminal domain.  Thus the left
supremum over good times equals its supremum over all terminal times.
No continuity of the hybrid starts or of \(z(\tau)\) is used.

Taking the infimum over \(S\) proves (S.484).  This argument does not require
an optimal deletion set, a maximizing time, or a good endpoint.

### 3.3 Target-scale constants

If
\(\mathfrak H^{\rm fix}\le C A_R\), then

\[
 \mathfrak L^K
 \le(C_{\rm pay}+6C)A_R.
\]

Conversely, if
\((\mathfrak L^K)^{3/2}\le C_LP_R^M\), then

\[
 \mathfrak H^{\rm fix}
 \le(C_L^{2/3}+C_Q)A_R.
\]

The same finite deletion number is retained in both directions.

## 4. Infinite sums, domains, and endpoints

The common zero start and \(K=F+Q\ge0\) imply

\[
 K_k(t)\le o_k^F+\operatorname {TV}Q_k.
\]

Therefore

\[
 \sum_k\sup_tK_k(t)
 \le B_{F,R}+B_{Q,R}<\infty.
\]

This one summable envelope justifies all nonnegative shell sums and uniform
tail passages in the note.

The terminal domains \(I_R\) and \(\mathcal T_R\) are open.  The common
good-time set has full measure and is therefore dense in each.  A continuous
functional can have a supremum approached only at an omitted endpoint or at
a non-good interior time; density still recovers the same supremum.  No
attainment statement appears in the proof.

## 5. Abstract triangular-clock audit

For \(M>N\), height \(H>0\), and pairwise disjoint triangular clocks, at
most one coordinate is positive at any time.  Exact calculation gives

\[
 \mathfrak H_N^{\rm hyb}
 =
 \begin{cases}
 H,&N=0,\\
 0,&N\ge1,
 \end{cases}
 \qquad
 \mathfrak H_N^{\rm fix}
 =\mathfrak L_N^K=H,
\]

and

\[
 \mathfrak O_N^{F,+}
 =\mathfrak M_N^K
 =\mathfrak V_N^K
 =(M-N)H,
\]

\[
 \mathfrak H^F_{1,N}=2(M-N)H,
 \qquad
 \sum_j\operatorname {TV}F_j=2MH.
\]

Thus \(N\ge1\) and \(M\ge N+2\) are exactly the conditions for both strict
gaps in (S.491).  The formerly tempting choice \(M=N+1\) separates moving
from fixed deletion but does not separate simultaneous height from
coordinatewise maxima.

For a proposed constant \(C\) at a fixed \(N\), choose any fixed \(M>N\)
and then take

\[
 H>4C^3M^2.
\]

Cubing the proposed inequality
\(H\le C(2MH)^{2/3}\) gives the contradictory condition
\(H\le4C^3M^2\).  This is the correct fixed-\(N\) negation.  It is purely
abstract and does not realize a Navier--Stokes solution or the Version-M
payment.

## 6. Taylor-family scope audit

Step 17 first fixes \(N\), sets \(M=N+1\), and then chooses \(R\) so that
(S.451) holds.  This makes the first \(N+1\) shell coefficients positive
and yields

\[
 \mathfrak O^{F,+}_{N,R}\asymp_{N,R}A^2,
 \qquad
 B_{Q,R}=O_R(A^2),
 \qquad
 P_R^M\asymp_RA^3.
\]

The main note now repeats this order and includes
\(A\ge A_0(N,R)\).  Its conclusion is only a compatibility screen:

\[
 \mathfrak H^{\rm hyb},
 \mathfrak H^{\rm fix},
 \mathfrak L^K
 =O_{N,R}(A^2).
\]

It neither proves a universal gate nor supplies a lower bound for these
three weaker functionals.

## 7. Literature and route audit

The separate primary-source audit checks ten classical and recent sources.
No inspected theorem combines all of:

- arbitrary deterministic suitable weak solutions;
- for each fixed solution, scale, centre, and terminal domain, one finite
  physical-shell deletion retained across time, with universal cardinality;
- all common good terminal times for stopped flux, or all terminal times for
  the equivalent completed clock;
- forward hybrid stopped increments;
- an infinite-shell \(\ell^1\) tail; and
- a uniform \((P_R^M)^{2/3}\) payment.

The bounded non-hit is not a novelty or priority claim.  The transferable
mechanisms are common-measure finite overlap, dissipation pigeonholing with
persistence, annular reassignment, and signed pressure-flux work depletion.
Each requires a new PDE-specific theorem before it can close (S.486).

## 8. Dependency locks

The freeze certificate must bind the following inherited sources:

| Dependency | Role |
|---|---|
| research/r074s_paid_branch_last_exit_residual.md | Step 10 (S.235), dense-good-time terminal lift, and paid-branch constant six |
| research/r074s_hybrid_flux_tail_equivalence.md | Step 15 (S.383)--(S.385), including \(r_k\le z_k\) |
| research/r074s_recurrent_streamline_temporal_tail_obstruction.md | Step 17 (S.451), (S.471), and (S.475) |
| research/r074p_temporal_observable_triage.md | continuous representatives and absolute variation ledgers |
| research/r074q_problem_freeze.md | Q.9, Q.12, and Q.1 route endpoints |

The deterministic certificate records the byte hashes and fails closed if
the three directly invoked Step 10, Step 15, or Step 17 notes drift.

## 9. Final claim ledger

**PROVED:** (S.476)--(S.485), (S.488), the abstract identities
(S.489)--(S.492), and the quantified Taylor compatibility screen (S.493).

**OPEN:** the direct moving-deletion gate, the fixed-deletion gate (S.486),
the completed-clock gate (S.487), the positive-excursion gate, terminal
crown coercivity, Q.12, Q.1, scale contraction, and regularity.

**ABSTRACT ONLY:** strict minimax and separable-maxima gaps, the unbounded
reverse ratio, and the failure of the linear ledger to force a \(2/3\)
power at fixed \(N\).

**NOT CLAIMED:** novelty, priority, a singular solution, a counterexample to
Navier--Stokes, or a solution of the Millennium problem.
