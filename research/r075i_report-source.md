# R0.75I primary-source boundary -- short-block diffusion and occupation

**Audience:** analysts reviewing the R0.75I diffusion-safe block theorem.  
**Date:** 2026-09-03.  
**Scope:** passive advection--diffusion with divergence-free shear drift;
short-time cubic payment; multi-block occupation.  
**Exclusion:** no claim of priority, no complete-clock theorem, and no
Navier--Stokes regularity conclusion.

## Direct answer

R0.75I is an elementary local Holder estimate.  It proves that diffusion
cannot spoil payment of the collar flux on one `O(R^3)` block because the
proof does not use the passive equation at all.  For the absolute
block-summation route, the next dynamical target is the distribution of
cubic payment across the `O(R^(-1))` blocks of the full clock.  This is a
sufficient route only: an `x_2`-independent passive zero mode can have
maximal participation while every signed block flux vanishes exactly.

The primary literature confirms that bounded-total-speed drift is a
distinguished regime for passive-scalar heat kernels and that pathwise or
weighted-semigroup methods can encode transport plus diffusion.  None of
the inspected sources gives the R0.75I participation estimate (I.19), the
signed cross-mode estimate E.24, or the frozen Version-M payment ledger.
This is a bounded non-hit, not evidence of novelty or priority.

## Evidence used and exact limit

### Rough divergence-free drift and bounded total speed

Dallas Albritton and Hongjie Dong study
`partial_t theta-Delta theta+b dot grad theta=0`, including local
boundedness, Harnack estimates, and upper bounds on fundamental solutions.
Their abstract identifies `L^1_t L^infinity_x`, the bounded-total-speed
class, as a borderline regime with a special role.  This supports treating
the integrated speed separately from diffusion.  Their theorem is not the
participation bound (I.19), and R0.75I does not import it as one.

### Davies weighted-semigroup method

Davies-type arguments perturb a heat semigroup by exponential spatial
weights to obtain off-diagonal decay.  The modern Dirichlet-form treatment
by Hu and Li derives off-diagonal upper bounds by this method.  Such an
estimate may control leakage between a terminal collar and an enlarged
tube.  R0.75I shows that this would address only one block unless it also
controls the effective number of occupied blocks or their signed sum.

### Classical Gaussian bounds

Aronson's classical work proves Gaussian upper and lower estimates for
fundamental solutions of broad uniformly parabolic equations.  These
bounds justify Gaussian-tail intuition in a future localization lemma, but
they do not encode the frozen shear payment, the collar normal, or the
participation count.  No Aronson estimate is used in the proof of I.1.

## Claim-to-source ledger

| claim checked | primary source | date / identifier | URL | access and boundary |
|---|---|---|---|---|
| Passive scalar with divergence-free drift admits local boundedness/Harnack/fundamental-solution analysis in stated drift classes; bounded total speed has a special borderline role | Dallas Albritton and Hongjie Dong, *Regularity properties of passive scalars with rough divergence-free drifts* | submitted 2021-07-26, arXiv:2107.12511 | https://arxiv.org/abs/2107.12511 | Abstract and article sections inspected 2026-09-03; does not prove I.19 or E.24 |
| Exponential perturbation of heat semigroups is a standard route to off-diagonal bounds | Jiaxin Hu and Xuliang Li, *The Davies method revisited for heat kernel upper bounds of regular Dirichlet forms on metric measure spaces* | arXiv:1605.05548 | https://arxiv.org/abs/1605.05548 | Abstract and off-diagonal section inspected 2026-09-03; symmetric Dirichlet-form setting is not substituted for the frozen drift problem |
| Uniformly parabolic fundamental solutions satisfy classical Gaussian comparison bounds under the paper's hypotheses | D. G. Aronson, *Bounds for the fundamental solution of a parabolic equation* | Bull. AMS 73 (1967), DOI 10.1090/S0002-9904-1967-11830-5 | https://doi.org/10.1090/S0002-9904-1967-11830-5 | Bibliographic record and theorem summary inspected 2026-09-03; no Version-M or signed-flux consequence inferred |

## Search record and stopping rule

Searches combined the exact phrases `Davies-Gaffney`, `bounded drift`,
`divergence-free drift`, `passive scalar`, `off-diagonal`, and
`fundamental solution`.  Follow-up inspection reached the Albritton--Dong
bounded-total-speed boundary, a modern Davies-method derivation, and the
classical Aronson source.  The search stopped because the mathematical
claim proved in R0.75I is self-contained, the only consequential literature
boundary is now supported by primary sources, and further generic heat-
kernel sources would not establish the missing participation estimate.

## Frozen conclusion

**Established locally:** one-block absolute collar flux is paid at the
same favorable exponential rate as the R0.75H transport benchmark, for an
arbitrary measurable field.

**Conditional:** all selected blocks are paid if their cubic participation
count satisfies `N_eff <= C R^(-theta)` with
`theta<8558/35721`.

**Exact warning:** high participation is not a counterexample or a
necessary obstruction; the real horizontal zero mode has zero flux even
when its cubic mass persists on all blocks.

**Open:** proving that participation bound or stronger signed cancellation
for the frozen diffusing passive solution, E.24, complete-clock extraction,
fixed deletion, suitable-weak transfer, regularity, and singularity.
**NOT CLAY.**
