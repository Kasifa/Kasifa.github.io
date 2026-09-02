# R0.74P main note — independent analytic audit

## Verdict

**PASS for promotion within the stated scope.**  Three independent read-only
audits covered the clock balance and BV ledger, the fixed-scale weak
compactness argument, and the full claim/quantifier/literature boundary.
No mathematical blocker remained after the recorded repairs.

## Audit A — clock balance and shell ledgers

The audit confirmed:

- the fixed pressure gauge and shellwise gauge cancellation;
- the sign of total local dissipation and the identity (K=Q+F);
- the complete absolute flux ledger, including velocity, drift, pressure,
  gradient, time cutoff, and the correct \(\gamma_k/R\) factors;
- the periodized derivative majorants and unfolding before single-lift
  estimates;
- monotone convergence for the nonnegative infinite-shell sums;
- passage \(\tau\uparrow t_0\) in the target-shell absolute bound;
- the \(\ell^1\) BV closure, target-shell two-sided scale, and the
  over-weighted lower bound.

Audit binding before final release rebind:
`98fa42415266cc7b8a6c96b11fe5a02e9eb790591e73eb62d2efab3ca495ba44`.

## Audit B — fixed-scale weak stability

The audit confirmed:

- fixed-(R) mollified-path stability by the backward
  Caratheodory--Gronwall estimate;
- strong moving-velocity and drift convergence, and weak translated
  gradient/pressure convergence;
- distributional convergence plus local mass bounds for
  \(\boldsymbol\mu_n\rightharpoonup^*\boldsymbol\mu\);
- uniform convergence of the canonical (Q,F,K) primitives, including
  pressure-primitive equicontinuity;
- positive-variation lower semicontinuity and the finite-Fatou passage to
  (Y_1) and (Y_2^{\rm sf});
- lower semicontinuity of the window baselines and exterior dissipation.

The result is explicitly fixed-scale.  It does not claim cross-scale
compactness, continuity of positive variation, a hard-time measure section,
or a useful lower-semicontinuity direction for anomalous dissipation alone.

## Audit C — full scope and quantifiers

The audit confirmed:

- suitable-weak and compactness results are Version M only;
- two-frame statements are confined to the smooth exact family;
- every window no-go has fixed \(\sigma>0\) and is nonuniform as
  \(\sigma\downarrow0\);
- (v_{j,R}\asymp T_*) is stated only for the target component;
- the full (Y_2^{\rm sf}) has only a lower detection bound and its upper
  bound remains open;
- inherited R0.74H--O inputs are distinguished from new project lemmas;
- literature sources are used only for their actual surrounding tools;
- the contraction and scale-packing routes remain conditional;
- no singularity, regularity, novelty, priority, or Clay conclusion is
  inferred.

At the audited source, all 87 displayed equation tags were unique, the
display delimiters balanced, and `git diff --check` passed.  The final
release rebind repeats these checks after all publication references are
frozen.

## Claim boundary

The promoted result is an observable triage, a defect-completed clock
balance, shellwise BV closure, target-component discrimination, and
fixed-scale weak lower semicontinuity.  The central compression

\[
 \mathfrak C_R^M
 \stackrel?\le
 C\left[(P_R^M)^{2/3}+Y_{2,R}^{\rm sf}\right]
\]

remains **OPEN**.  **NOT CLAY.**
