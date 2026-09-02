# R0.74S Step 9 — primary audit of the canonical best-\(N\) last-exit equivalence

## 1. Verdict and locked source

**UNCONDITIONAL PASS ON THE LOCKED SOURCE.**  The audited source is

`research/r074s_best_n_last_exit_equivalence.md`

with SHA-256

`85003b3fdfdf28618a82a57d241e86c086704ea3ed3a9b192de223f3b8c3a4dd`.

All twenty-three numbered statements (S.200)--(S.222) pass.  In particular:

- the inherited plateau domain \(I_R\) is kept separate from the full clock
  interval \(\mathcal T_R=(s_R,t_0)\);
- the signed best-\(N\) functional is a forced full-tail quantity with the
  correct order \(\sup_\tau\inf_{\#S_\tau\le N}\);
- the signed terminal half-exit gives exactly one half of the signed
  best-\(N\) tail, including negative terminal fluxes and zero coordinates;
- the \(K\)-level last exit gives exactly
  \((1-\theta)T_k-\Delta Q_{k,\theta}\), and the aggregate comparison loses
  one, not two, full \(Q\)-variation ledgers;
- the infinite tails are absolutely convergent and are not inserted as one
  infinite discontinuous local-energy test;
- finite positive-terminal \(K\)-families at good terminal times lie in the
  closure of the strict Step 2 upcrossing class when \(0<\theta<3/4\);
- the source does not claim continuity of the terminal-dependent last-exit
  selector;
- the quantifier, cancellation, simultaneous-plateau, \(K=0\), \(F=0\),
  and recent-window stress tests have the stated meanings; and
- the canonical constructions are proved equivalent to the existing open
  R0.74Q best-\(N\) tails, not promoted to a new quadratic compression.

This is a primary analytic audit.  It checks the locked source against the
frozen inputs and gives direct proofs of its reductions, but it is not an
independent proof of all inherited suitable-weak theory, a novelty or
priority certificate, or a regularity theorem.  **NOT CLAY.**

## 2. Frozen-source backtracking

| Input used by Step 9 | Direct source check | Audit result |
|---|---|---|
| Canonical completed clocks | R0.74P, (2.7)--(2.10), gives continuous representatives \(K=Q+F\), zero starts, and \(K\ge0\) | **PASS** |
| Absolute shell ledgers and square function | R0.74P, (3.4)--(3.7), gives summable \(Q/F\) variation, \(v_{k,R}=\operatorname{Var}^+K_{k,R}\), \(K_{k,R}(\tau)\le v_{k,R}\), and \(Z_R=(\sum_kv_{k,R}^2)^{1/2}\) | **PASS** |
| Best-\(N\) terminal reduction | R0.74Q, (Q.7)--(Q.12), gives the fixed-\(N\), terminal-dependent-exception functional and the \(\sqrt N Z_R\) exceptional payment | **PASS / PDE TAIL BOUND OPEN** |
| Strict stopped-work class | R0.74S Step 2, (S.25)--(S.38), requires a good terminal time, finite shell family, good stops, and strict quarter upcrossings | **PASS** |
| Plateau/full-time and no-exception boundary | R0.74S Step 8, (S.197)--(S.199), separates \(\mathfrak C_R^M\) from \(\mathfrak C_{{\rm full},R}^M\), proves the sharp one-\(B_Q\) comparison, and refutes the universal no-exception quadratic antecedent | **PASS** |

The checked hashes are

- locked Step 9 source:
  `85003b3fdfdf28618a82a57d241e86c086704ea3ed3a9b192de223f3b8c3a4dd`;
- R0.74P:
  `a3cb872735b92b32ddfa7b96bc4184d70b0287ff2ce7d3da8cadbbcc494d0867`;
- R0.74Q:
  `42efa94f5310d8f7ce3cea1896ee1e0a8ddd9bddf5d588f9bb853c8696a1a962`;
- R0.74S Step 2:
  `3ec5f9b894f89e9febb95e5a100836b5b18e455f8366bf99e93b746ac6353da4`;
  and
- R0.74S Step 8:
  `0a79f2c5bb59644eca710b3d9341776853ceb4d1f65a36869c2465073f8c08ab`.

The R0.74Q source writes its terminal supremum on the full clock interval.
Step 9 correctly parameterizes the domain: \(\mathcal D=\mathcal T_R\)
recovers that full-terminal gate, whereas \(\mathcal D=I_R\) is the weaker
plateau restriction sufficient for the inherited plateau observable.

## 3. Preliminary functional and topology audit

For \(x\in\ell^1\), deleting a coordinate with \(x_k\le0\) cannot lower the
remaining signed sum.  Therefore an optimizing or approximating exceptional
set may be chosen among the largest positive coordinates.  If
\((x_m^{+*})\) is their nonincreasing rearrangement, padded by zeroes, then

\[
 \mathcal S_N(x)
 =\left[\sum_kx_k-\sum_{m=1}^Nx_m^{+*}\right]_+
 =\left[\sum_{m>N}x_m^{+*}-\|x_-\|_1\right]_+.
\]

For a fixed exceptional set \(S\), the map

\[
 x\longmapsto\left[\sum_{k\notin S}x_k\right]_+
\]

is one-Lipschitz on \(\ell^1\).  Comparing the same set in the two infima
therefore gives

\[
 |\mathcal S_N(x)-\mathcal S_N(y)|\le\|x-y\|_{\ell^1}.
\]

The summable variation rows imply uniform tail control.  For example, if
\(t_j\to t\), then for every finite prefix \(M\),

\[
 \sum_{k\le M}|F_k(t_j)-F_k(t)|\longrightarrow0,
 \qquad
 \sup_j\sum_{k>M}|F_k(t_j)-F_k(t)|
 \le\sum_{k>M}\operatorname{TV}F_k.
\]

First let \(j\to\infty\), then \(M\to\infty\).  This proves
\(\ell^1\)-continuity of the \(F\)-vector.  The same argument applies to
\(Q\), and hence to \(K=Q+F\).  Consequently the cumulative terminal flux
and the two best-\(N\) tails are continuous in terminal time.  Since the
inherited common good-time set has full measure, it is dense in each of the
open domains \(I_R\) and \(\mathcal T_R\); their terminal suprema are
unchanged when restricted to that good set.

This conclusion concerns the terminal vectors and \(\mathcal S_N\).  It
does not assert continuity of \(\tau\mapsto\ell_{k,\theta}^K(\tau)\) or of
the corresponding canonical last-exit work.

## 4. Equation-by-equation audit

| Equation | Primary check | Decision |
|---|---|---|
| (S.200) | \(I_R\subset\mathcal T_R\) gives \(\mathfrak C_R^M\le\mathfrak C_{{\rm full},R}^M\).  The two equalities are domain-specific definitions; no converse equality is asserted. | **PASS** |
| (S.201) | \(A_R=(P_R^M)^{2/3}\), \(Z_R=(\sum_kv_{k,R}^2)^{1/2}\), and \(B_Q=\sum_k\operatorname{TV}Q_k\le C_QA_R\) match the inherited rows. | **PASS** |
| (S.202) | The infimum is over at most \(N\) coordinates after the complete signed sum is formed and before the terminal supremum.  Absolute summability makes it well defined. | **PASS** |
| (S.203) | The same fixed integer \(N\) is used at every terminal time, scale, and solution; only the exceptional set may depend on \(\tau\).  The domains are explicitly \(I_R\) or \(\mathcal T_R\). | **PASS** |
| (S.204) | For \(f_k\ne0\), the level set is nonempty, compact, excludes \(\tau\), and has an interior last point.  For \(f_k=0\), the convention \(\ell_k^F=\tau\) produces zero increment. | **PASS** |
| (S.205) | With \(g(t)=\operatorname{sgn}(f_k)F_k(t)\), maximality and continuity force \(g(\ell)=|f_k|/2\).  Multiplying by the terminal sign proves both identities, including \(f_k<0\). | **PASS** |
| (S.206) | The nonexceptional tail is forced: there is no further arbitrary-subset supremum.  Its absolute sum is \(\frac12\sum_{k\notin S}|F_k(\tau)|<\infty\). | **PASS** |
| (S.207) | For every \((\tau,S)\), the stopped sum is exactly one half of the terminal signed sum.  Positive homogeneity, then infimum and supremum, preserve the literal factor \(1/2\). | **PASS / EXACT FACTOR** |
| (S.208) | Split \(\sum_kF_k\) into \(S\) and its complement.  On \(S\), \(F_k=K_k-Q_k\le v_k+\operatorname{TV}Q_k\); Cauchy--Schwarz gives \(\sum_{S}v_k\le\sqrt N Z_R\).  Infimum, plateau supremum, and (S.207) give the displayed bound. | **PASS** |
| (S.209) | At \(\tau=1\), \(F(1)=K(1)=1\), \(\ell^F=1/2\), and \(K(1/2)=1\).  Hence \(\Delta K=0\), disproving automatic strict-quarter admissibility. | **PASS / ABSTRACT CLOCK TEST** |
| (S.210) | If \(T_k>0\), continuity and \(K_k(s_R)=0<\theta T_k<K_k(\tau)\) give an interior last level with \(K_k(\ell)=\theta T_k\).  The \(T_k=0\) convention again gives zero increment. | **PASS** |
| (S.211) | Subtract \(F=K-Q\) at \(\tau\) and \(\ell\); the \(K\)-increment is exactly \((1-\theta)T_k\). | **PASS** |
| (S.212) | From (S.211), \(\sum_k|L_{k,\theta}|\le(1-\theta)\sum_kT_k+B_Q<\infty\).  Thus the infinite forced tail is unambiguous. | **PASS** |
| (S.213) | Put \(a=(1-\theta)\sum_{k\notin S}T_k\ge0\) and \(b=\sum_{k\notin S}\Delta Q_{k,\theta}\).  Then \(|[a-b]_+-a|\le|b|\le\sum_{k\notin S}|\Delta Q_k|\le B_Q\). | **PASS / ONE \(B_Q\)** |
| (S.214) | A uniform additive \(B_Q\) perturbation remains \(B_Q\) after infimum over \(S\) and supremum over \(\tau\).  No triangle step doubles it. | **PASS / COEFFICIENT ONE** |
| (S.215) | For \(T_k>0\), \(\Delta K=(1-\theta)T_k>T_k/4\) exactly when \(\theta<3/4\).  At a good terminal and for a finite shell family, continuity leaves a strict neighborhood and density supplies good stops converging to each canonical stop.  Zero-terminal shells are omitted. | **PASS / GOOD-TERMINAL CLOSURE ONLY** |
| (S.216) | The clock reduction gives \(\mathfrak C_R^M\le B_Q+\sqrt N Z_R+\mathcal S_{N,R}^K(I_R)\).  The lower half of (S.214) gives \(\mathcal S_N^K\le(\mathfrak W_\theta^K+B_Q)/(1-\theta)\), yielding the displayed coefficients. | **PASS** |
| (S.217) | For every \((\tau,S)\), the two residual sums differ by \(-\sum_{k\notin S}Q_k(\tau)\), whose absolute value is at most \(B_Q\).  The same uniform-infimum-supremum argument proves the result. | **PASS / ONE \(B_Q\)** |
| (S.218) | The first equivalence is (S.207); the second follows in both directions from (S.214) and \(B_Q\le C_QA_R\).  The implicit constant may depend on fixed \(\theta\), but not on \(R\) or the solution. | **PASS / NO-GAIN EQUIVALENCE** |
| (S.219) | Terminal-dependent deletion removes the sole positive coordinate at each state, giving zero.  Either one fixed deletion leaves the other state's unit coordinate, giving one. | **PASS / QUANTIFIER TEST** |
| (S.220) | The forced half-exit vector is \((1/2,-1/2)\), whose complete signed sum is zero; an arbitrary-subset supremum selects \(1/2\).  The source correctly does not call this an (S.25) family. | **PASS / CANCELLATION TEST** |
| (S.221) | With exactly \(M\) identical plateau coordinates of height \(H\), best-\(N\) deletion leaves \((M-N)H\).  The two last-exit values follow from (S.207) and (S.211) with \(Q=0\). | **PASS / ABSTRACT CLOCK TEST** |
| (S.222) | At \(\theta=2/3\), \(\Delta K=T_k/3\).  Since \(\Delta F=\Delta K-\Delta Q\) and \(\Delta Q\le|\Delta Q|<T_k/6\), one gets the strict lower bound \(\Delta F>T_k/6\). | **PASS / COMPATIBILITY, NOT OPTIMALITY** |

All twenty-three tags occur exactly once and in increasing order.  No sign,
positive part, strict inequality, power, or displayed constant in
(S.200)--(S.222) requires repair.

## 5. Constant and quantifier ledger

The literal constants and their origins are:

| Quantity | Exact source | Audited value |
|---|---|---|
| Signed half-exit increment | \(F(\tau)-F(\ell^F)\) | \(F(\tau)/2\) |
| Signed half-exit terminal reduction | \(\mathcal S_N^F=2\mathfrak W_{1/2,N}^F\) | factor \(2\) |
| \(K\)-last-exit clock increment | \(K(\tau)-K(\ell_\theta^K)\) | \((1-\theta)T\) |
| Last-exit perturbation | \(\sum|\Delta Q_k|\) | one \(B_Q\) |
| Recovery of \(\mathcal S_N^K\) | lower side of (S.214) | \((\mathfrak W_\theta^K+B_Q)/(1-\theta)\) |
| Plateau \(K\)-reduction \(Q\) coefficient | original \(B_Q\) plus recovered tail | \(1+(1-\theta)^{-1}\) |
| Strict Step 2 margin | \((1-\theta)T-T/4\) | \((3/4-\theta)T>0\) |
| Step 8-compatible choice | \(\theta=2/3\) and \(|\Delta Q|<T/6\) | \(\Delta F>T/6\) |

The coefficient one in (S.213)--(S.214) is algebraically sharp.  On
\([0,1]\), take \(K(t)=t\), \(\tau=1\), keep \(Q=0\) through
\(t=\theta\), and then vary it monotonically to \(\pm B\), with
\(0<B\le1-\theta\).  Then \(\operatorname{TV}Q=B\), and the positive
stopped value differs from \(1-\theta\) by exactly \(B\).

The quantifier order is fixed throughout:

\[
 \sup_{\tau\in\mathcal D}
 \inf_{S_\tau\subset\mathbb N,\ \#S_\tau\le N}.
\]

The integer \(N\) is universal for the proposed gate.  The exceptional set
may depend on \(\tau\); a single set fixed before the terminal supremum is a
strictly stronger problem.  The full nonexceptional tail is summed before
the positive part.  Taking a supremum over arbitrary finite subsets would
remove negative shells and change the signed problem.

## 6. Endpoint, infinite-tail, and good-time audit

1. **Left endpoint.**  For \(f_k\ne0\), the half level is nonzero, so the
   last half-exit cannot equal \(s_R\).  For \(T_k>0\) and \(\theta>0\),
   the \(K\)-level last exit is also strictly after \(s_R\).
2. **Zero terminal values.**  The conventions \(\ell=\tau\) for
   \(f_k=0\) or \(T_k=0\) give zero stopped increments and require no
   fictitious strict stop.
3. **Right endpoint.**  Every terminal time satisfies \(\tau<t_0\), so
   the maximum is taken on the compact interval \([s_R,\tau]\).  No value at
   \(t_0\), and no attainment of a terminal supremum, is assumed.
4. **Infinite shell tail.**  Summable \(F/Q\) variation and
   \(\sum_kK_k(\tau)<\infty\) give absolute convergence before any
   rearrangement, infimum, or positive part.
5. **Finite local-energy tests.**  For a prescribed exception set, exhaust
   its complement by finite shell families.  Absolute convergence passes
   their stopped sums to the forced full tail.  The source does not insert
   the infinite discontinuous stopped weight as one test.
6. **Good stops.**  At a good terminal time and for finitely many positive
   terminal clocks, the margin \((3/4-\theta)T_k>0\) survives small changes
   of each stop.  The common dense good set supplies the approximating
   stops, and continuity of \(F_k\) passes their flux increments to the
   canonical values.
7. **Non-good terminals.**  Dense-good-time recovery is asserted for the
   terminal vector functionals in (S.203), not for the last-exit selector.
   The latter is compared algebraically to the terminal tail by (S.214),
   within \(B_Q\).

All seven boundary checks pass.

## 7. Stress-test audit

| Stress row | What it tests | Result |
|---|---|---|
| Signed half-exit example (S.209) | A canonical \(F\)-level stop need not be a strict \(K\)-upcrossing | **PASS / FAILURE EXHIBITED** |
| Two terminal states (S.219) | \(\sup_\tau\inf_{S_\tau}\ne\inf_S\sup_\tau\) | **PASS / VALUES \(0\) AND \(1\)** |
| Vector \((1,-1)\) (S.220) | Forced signed tail cannot be replaced by arbitrary-subset selection | **PASS / VALUES \(0\) AND \(1/2\)** |
| \(M\) simultaneous plateau clocks (S.221) | Last exits do not turn an \(\ell^1\) tail into an \(\ell^2\) bound | **PASS / \((M-N)H\) TAIL** |
| \(K=0,\ Q=-F\) | The signed and nonnegative tails may differ by the entire paid \(Q\) row | **PASS / (S.217) SHARP** |
| \(F=0,\ K=Q\) | A positive clock tail may have zero stopped physical-flux increment | **PASS / \(Q\) ERROR NECESSARY** |
| Early plateau before a recent window | A fixed recent window need not contain any \(\theta\)-level exit | **PASS / FULL HISTORY NECESSARY ABSENT NEW PDE INPUT** |
| Scalar \(Q\)-sign fixture | The one-\(B_Q\) perturbation in (S.213)--(S.214) cannot be improved algebraically | **PASS / COEFFICIENT ONE SHARP** |

All eight scalar/vector constructions are algebraic or continuous-clock
tests, not Navier--Stokes solutions.  Their role is to falsify deductions
from the completed-clock algebra alone.  They do not rule out a future PDE
packing theorem using additional Navier--Stokes structure.

## 8. Claim and route boundary

| Claim | Audit status |
|---|---|
| Domain-parametrized best-\(N\) tails and their \(\ell^1\) stability | **PROVED** |
| Signed half-exit representation | **PROVED EXACTLY** |
| \(K\)-last-exit representation and one-\(B_Q\) comparison | **PROVED EXACTLY** |
| Finite good-stop closure | **PROVED FOR POSITIVE-TERMINAL SHELLS AT GOOD TERMINAL TIMES AND \(0<\theta<3/4\)** |
| Continuity of the last-exit selector | **NOT PROVED / NOT CLAIMED** |
| Plateau reductions (S.208) and (S.216) | **PROVED** |
| Full-terminal R0.74Q best-\(N\) gate | **EQUIVALENTLY REWRITTEN; PDE QUADRATIC BOUND OPEN** |
| Plateau restriction of the best-\(N\) gate | **SUFFICIENT FOR \(\mathfrak C_R^M\); STILL OPEN AS A PDE ESTIMATE** |
| Universal no-exception bound \(\mathfrak W_{{\rm up},R}^M\lesssim A_R\) | **REFUTED IN STEP 8 BY THE SMOOTH R0.74O/P FAMILY** |
| Conditional Step 2 implication (S.38) | **REMAINS PROVED** |
| Canonical last exits alone create shell compression | **REFUTED AT THE COMPLETED-CLOCK ALGEBRA LEVEL** |
| Fixed \(N_0\), solution- and scale-independent residual packing | **OPEN** |
| Step 7/8 residual full tail | **TO BE DEFINED AND AUDITED IN THE NEXT STEP** |
| Fixed-scale inequality (Q.1), extraction, contraction, prescribed-centre packing, and regularity | **OPEN** |
| Novelty, priority, singularity formation, or Millennium conclusion | **NOT CLAIMED / NOT CLAY** |

The value \(\theta=2/3\) is only a compatibility choice for the next
one-sixth decomposition.  It is not globally optimal: the algebraic factor
\((1-\theta)^{-1}\) decreases as \(\theta\downarrow0\).  The next possible
advance must therefore be a PDE estimate for the forced residual tail after
the already-paid branches are removed, not another last-exit definition.

## 9. Machine-verifiable and human-verifiable boundaries

The following checks are mechanical:

- recomputing the locked source and dependency SHA-256 values;
- checking that the twenty-three tags (S.200)--(S.222) occur once each and
  in increasing order;
- evaluating the finite rational fixtures in (S.209), (S.219)--(S.222), and
  the scalar sharpness rows; and
- checking literal presence of the two terminal domains, the order
  \(\sup_\tau\inf_{S_\tau}\), the strict range \(0<\theta<3/4\), and the
  OPEN/REFUTED/NOT CLAIMED labels.

Those checks can detect changed constants, reversed signs, missing tags,
wrong quantifier order, domain collapse, and claim-ledger drift.  They do
not prove:

- the inherited local-energy identities or variation/payment estimates;
- compactness, continuity, or density arguments in infinite-dimensional
  function spaces;
- that finite good-stop approximations are legitimate in the suitable-weak
  framework;
- that an algebraic stress fixture is realizable by a Navier--Stokes
  solution; or
- the open PDE best-\(N\) packing estimate.

Those items require the analytic source audit above and, for inherited
results, the cited prior freezes.  A passing certificate or structural
check is evidence of artifact integrity, not a proof of regularity.

## 10. Counted final decision

| Audit group | Passed | Failed |
|---|---:|---:|
| Locked source and four dependency hash bindings | 5 | 0 |
| Numbered equations (S.200)--(S.222) | 23 | 0 |
| Constant and quantifier invariants | 8 | 0 |
| Endpoint, infinite-tail, and good-time boundaries | 7 | 0 |
| Explicit stress rows | 8 | 0 |
| Claim-status categories: PROVED, INHERITED, REFUTED, OPEN/NOT CLAIMED | 4 | 0 |

**Required source repairs remaining: 0.**  The locked note proves a
domain-safe and endpoint-safe representation/no-gain theorem.  It leaves the
fixed best-\(N_0\) PDE tail estimate, the next residual packing statement,
and all regularity implications visibly open.

**NOT CLAY.**
