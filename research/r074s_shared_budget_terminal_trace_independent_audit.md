# R0.74S Step 11 — independent audit of the terminal-trace reduction

## 1. Verdict

**PASS, with no mathematical reservation on the locked finite claims.**

The independent review reconstructed the shared-budget theorem, both branch
reductions, every rational witness, and the exact-family implication without
using the primary producer as a mathematical oracle.  It found and required
repairs to the first draft before this source was locked: the short-branch
sum domain, supportwise strictness, zero-start clock conditions, the
high-Rayleigh positive-variation caveat, and the full uniform quantifiers
were all corrected.

The locked main note is

research/r074s_shared_budget_terminal_trace_obstruction.md

at SHA-256

fd022de342b935e3e6e5fe0231f6b08ab9494e2bd38e23da15de6807f14d4693.

This verdict concerns the proved reductions and finite stress tests.  The
PDE hypotheses (S.261), (S.269), and (S.272) remain open.  So do Step 10
(S.243), Q.12, Q.1, scale contraction, prescribed-centre packing, and
regularity.  **NOT CLAY.**

## 2. Locked artifact set

| Artifact | SHA-256 |
|---|---|
| Main note | fd022de342b935e3e6e5fe0231f6b08ab9494e2bd38e23da15de6807f14d4693 |
| Primary audit | d8bf38f4337af366cd450a50622f7105b8925db37cd87c09ce839fe129a058d5 |
| Primary generator | a397d27943fca4d4a487038b5c14956667c7d36b3be5eb069262d2593f8ad2de |
| Primary JSON | ea5c9f13ba412703995b2875a26c84fa20779457399ffa9117871b65fafaf8d0 |
| Primary report | 6e86813ab2b001a8f357af42d952a9104ba70859b32441148ad5cd3ab283ffc4 |

The primary report records 14/14 exact checks, 7/7 finite checks, 34/34
structural checks, and 7/7 rejected semantic mutations.  Its overall status
is PASS.

## 3. Independent shared-budget reconstruction

Let \(a,b\in\ell^1_+\) have disjoint supports.  For any joint deletion set
\(S\), put

\[
 S_a=S\cap\operatorname{supp}a,\qquad
 S_b=S\cap\operatorname{supp}b.
\]

Then \(\#S_a+\#S_b\le N\), and the remaining mass splits exactly.  This
proves the lower bound in

\[
 \mathcal S_N(a+b)
 =\min_{n+m=N}\bigl[\mathcal S_n(a)+\mathcal S_m(b)\bigr].
\]

For the reverse inequality, take branch deletion sets approaching the two
infima and unite them.  Unused budget may be placed in either branch.  The
finite proof passes to \(\ell^1\) by truncation, or by deleting the
top-\(N\) coordinates with an index tie-break.

The terminal-domain corollary has only the direction

\[
 \sup_\tau\min_n f_n(\tau)\le\min_n\sup_\tau f_n(\tau).
\]

The two-state fixture in the main note proves that equality can fail by an
arbitrarily large factor.  The branch allocation may therefore depend on
the terminal time.  No selector measurability is needed for the pointwise
infimum followed by a supremum.

## 4. Independent short-branch reconstruction

On \(\mathcal R_{\rm sh}\), Step 10 gives

\[
 e_k(t)>T_k/6\quad\text{a.e. on }J_k^{\rm LE},
 \qquad r_k<T_k/2.
\]

Integrating R0.74R (R.214) over the last-exit interval yields

\[
 d_k(T_k/6)^{3/2}<C_1(2^{3k}\gamma_k)^{1/2}p_k.
\]

Taking the power \(2/3\) and then using \(r<T/2\) gives exactly

\[
 r_k<3C_1^{2/3}
        (2^{3k}\gamma_kd_k^{-2})^{1/3}p_k^{2/3}.
\]

Finite-shell Hölder and (R.211) prove (S.254), with no duplicated cubic
ledger.

The normalized variables satisfy the identity

\[
 (2^{3k}\gamma_k\lambda_k^3)
 (d_k\lambda_k^{3/2})^{-2}
 =2^{3k}\gamma_kd_k^{-2}.
\]

Hence profile tuning cannot erase the short-branch inverse duration.  The
layer-cake formula follows atomwise from
\(h^{-2}=1+2\int_h^1s^{-3}\,ds\).  The critical example
\(h_k=\sqrt{w_k}\) has every inverse moment equal to one, even though the
tail distribution is \(O(s^2)\).  A Dini improvement is genuinely needed
for this particular coefficient route.

For the tent estimate, at reverse time \(s\) the active indices are exactly
\(\{k:d_k>s\}\).  Weighted Hölder gives

\[
 {M(s)^{3/2}\over V(s)^{1/2}}
 \le3^{3/2}\sum_{d_k>s}{e_k(t)^{3/2}\over a_k^{1/2}}.
\]

The substitution \(ds=dt/R^2\) and (R.214) prove (S.258).  Integrating only
over \(0<s<\delta\) proves (S.259).  Neither argument controls the value at
\(s=0\), and the strictly nested clock tower in (S.260) confirms that this
failure is not repaired by interval geometry alone.

## 5. Independent selected-excess reconstruction

On \(\mathcal I_x\), let \(q=\Delta Q\).  The full-history threshold
conditions imply

\[
 |q|\le\beta<T/6,\quad
 2\lambda\sigma\le T/6,\quad
 T/2\le D\le T,\quad
 x=D-\beta-2\lambda\sigma>T/6,\quad
 r=T/3-q.
\]

Thus \(r<T/2<3x\).  Also \(x\le T-\beta\), so

\[
 5r-x\ge2T/3-5q+\beta.
\]

For \(q\ge0\), the right side is at least \(2T/3-4q>0\); for \(q<0\), it is
at least \(2T/3-6q>0\).  Hence

\[
 x/5<r<3x.
\]

The limiting threshold tuples in the main note approach both constants, so
they are sharp within the scalar constraints.  Applying the inequalities
outside one common deletion set and then optimizing proves the best-\(N\)
equivalence (S.263).

The ancestor domination is one-sided:

\[
 r^x\le3x^{\rm sel}\le3b,\qquad
 b_k\le D_k\le K_k\le v_k.
\]

It gives linear summability, not a quadratic universal count.  By contrast,
the fixed-solution statement (S.265) is valid because a single prefix makes
the \(\ell^1\) tail of \(v\) small uniformly in the terminal time.  Its
prefix size depends on the solution, scale, and tolerance, so it is not
Q.12.

## 6. Independent rational-clock audit

The common piecewise-linear kinetic row has three nonzero trapezoids:

\[
 {1\over300},\qquad {15561\over240000},\qquad
 {2819\over240000}.
\]

Their sum is \(959/12000\).  With terminal dissipation \(3/5\), the pure
defect row therefore has

\[
 x={3\over5}-2{959\over12000}={2641\over6000}.
\]

The early high-Rayleigh bump integrates to \(1/500\), and its
\(g=300e_0\) row integrates to \(3/5\).  Consequently

\[
 \sigma={983\over12000},\qquad
 x={3\over5}-2{983\over12000}={2617\over6000}.
\]

Both kinetic masses are below \(1/12\), both excesses exceed \(1/6\), and
both clocks have their last \(2/3\) exit at one.  The selected defect or
high-Rayleigh mass lies entirely before that exit.  These are valid scalar
counterexamples to last-exit localization, not PDE solutions.

Only the pure-defect row is used for the exact \(v_k=1\) flat tower.  The
high-Rayleigh clock has a small early decrease and would have positive
variation strictly above one; the locked source does not make that false
identification.

## 7. Exact-family and literature boundaries

The conditional falsification test (S.270) is correct.  If \(N+1\) targets
each dominate \(A_R>0\), the total \(O(A_R)\) paid ledger excludes every one
from the paid classes, and any \(N\)-deletion leaves a residual exceeding
one-sixth of the smallest target.

The locked source says only that the currently proved R0.74O/P lower bound
certifies one target.  It does not infer that uncomputed off-target clocks
are small.  Likewise, the R0.74Q exterior cubic lower bound is used only to
show that the intended \(NT\) lower scale is not enough for (S.270); it is
not misused as an upper bound on the clock.

The cited primary literature does not directly supply a prescribed-centre,
terminal, weighted-annular best-\(N\) theorem with the bare suitable-weak
quantifiers.  The source labels the collision search bounded and
nonexhaustive.  No novelty or priority conclusion is drawn.

## 8. Independent machine audit

The standard-library Ruby verifier reconstructed seven independent groups
before reading the primary artifact contract.  It passed 7/7 groups and
206,891 exact Rational/finite cases, 59/59 note checks, 6/6 artifact locks,
and 7/7 dependency locks.  Its release-ready flag is true.  Repeated direct,
disabled-gems, isolated-working-directory, and environment-override runs
were byte-identical, and the warning-enabled syntax check was clean.

These counts certify finite algebra, parser and byte-lock behavior.  They do
not convert an open PDE antecedent into a theorem.

## 9. Final scope

The independent audit confirms:

- **PROVED:** (S.248)--(S.260), (S.262)--(S.268), and every conditional
  implication attached to (S.261), (S.269), (S.270), and (S.272);
- **OPEN:** the antecedents of (S.261), (S.269), and (S.272), the universal
  fixed count, Step 10 (S.243), Q.12, Q.1, and regularity;
- **ABSTRACT ONLY:** (S.252), (S.257), (S.260), and (S.266)--(S.268); and
- **NOT CLAIMED:** selector measurability, an exhaustive literature search,
  PDE realizability of the stress tests, novelty, or a Clay solution.

**NOT CLAY.**
