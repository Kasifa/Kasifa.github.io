# R0.70A — Parallel gate summary

## Status

R0.70A is an internal research gate, not a public theorem chapter.  Its three
tracks have completed their first pass:

- the literature collision matrix is recorded in
  [`r070a_literature_collision_matrix.md`](r070a_literature_collision_matrix.md);
- the moving-annulus identities and obstruction are recorded in
  [`r070a_moving_annular_balance_note.md`](r070a_moving_annular_balance_note.md);
- the scale-ratio theorem and diagnostic pilot archive are
  recorded in
  [`r070a_scale_ratio_robustness_note.md`](r070a_scale_ratio_robustness_note.md)
  and [`certificates/r070a-pilot/`](certificates/r070a-pilot/).

No item below is claimed to solve, or materially approach by itself, the
Navier--Stokes Millennium Problem.

## What is now rigorous

### 1. A non-explicit open scale-ratio neighborhood

The strict R0.69W two-annulus obstruction at \(\rho=4\), together with joint
continuity in \((a,\rho)\), implies the existence of an open interval
\((4-\eta,4+\eta)\) on which at least one of the two annular functionals is
negative for every \(0\le a\le1\).  The proof does not give a numerical value
of \(\eta\).

At \(\rho=4\), the exact analytic amplitude factor together with the archived
coefficient intervals gives the safely rounded uniform upper margin

\[
 \max_{0\le a\le1}\min\{A_0(a),A_{-2}(a)\}
 \le -1.246030236725547\times 10^{-5}.
\]

Standard local \(H^4\) well-posedness and continuous dependence also give a
non-explicit common short time on which this uniform strict obstruction
persists over the continuous compact parameter family.  This is a local
continuity statement, not a critical regularity estimate.

### 2. The exact moving-label identity

Replacing a fixed annular radius by \(r(t)\) in the instantaneous partition
of vortex stretching introduces no \(\dot r\) term into the enstrophy
identity.  A \(\dot r\) term appears only after differentiating an individual
moving band.  The near, band, and far label-flux terms cancel when the full
partition is restored.

Consequently, a moving cutoff alone does not convert the time integral of
annular production into a boundary term.  For this project's selected
normal-form subroute, the next candidate is a quadratic two-point functional
\(Q_r\) whose Navier--Stokes derivative has the annular cubic term as its
principal contribution, with every remainder controlled at the critical
scale.  No candidate meeting those project-specific obligations has been
constructed; other dynamic organizations are not ruled out.

### 3. A literature boundary with explicit conditions

The signed physical annuli from R0.69T are adjacent to, but not equivalent to,
the nonnegative filtered reservoirs in Yu's arXiv:2606.27560v1.  The following
three items are additional hypotheses in that preprint's Theorem 10.3, whose
conclusion is conditional summability and vanishing of a defect surplus, not a
regularity theorem.  The outer tail remains separate, and this project has not
independently verified the preprint's proofs:

1. unweighted far-field closure across all separated scales;
2. cross-scale summability or rigidity of the derivative-compatible increment
   defect;
3. a summable localization-shell budget.

The moving-annulus calculation does not remove any of these three gaps.  Its
time-dependent separation label is also different from Yu's Section 8.3
"moving shell", which varies with a spatial core point inside an absolute-value
estimate.

Grujić's arXiv:2607.08866v2 is a separate conditional route.  It assumes the
full critical-point profile of Definition 2.1 and a uniform
\(\mathrm{bmo}_{1/|\log r|}\) vorticity-direction condition.  The R0.69T
identity has not produced the required logarithmic smallness.  Neither 2026
preprint has been independently re-proved here.

## What remains diagnostic only

A five-point pilot at
\(\rho\in\{3.8,3.9,4.0,4.1,4.2\}\) was run with coarse interval settings.
Its enclosures are too wide to certify any sign away from the already proved
\(\rho=4\) case.  Midpoint behavior suggests that \(3.9<\rho<4.1\) is worth
testing, but this is only a prioritization signal.  The archived pilot has no
CPU or memory telemetry and is not represented as a formal monitored
certificate.

## Route decision

The main R0.70B gate is a matching-scale bridge test:

- express a smooth signed physical annulus and the filtered reservoir at
  comparable scales;
- seek either a one-way estimate with a summable defect or a rigorous
  counterexample showing that no such estimate can follow from the current
  hypotheses;
- stop this branch if the bridge merely restates one of the three known
  closure assumptions.

In parallel, a small symbolic triad test will ask whether the proposed
quadratic normal form \(Q_r\) can satisfy the required cohomological equation
even before pressure and localization errors are estimated.  Failure at this
symbol level would cheaply rule out the tested translation-invariant quadratic
multiplier class; it would not exclude non-translation-invariant, nonquadratic,
or more general two-point constructions.

The explicit \(\rho\)-interval computation remains a side branch.  It should
resume only after interval bounds for \(\partial_\rho A_j\), or a small
bivariate \((a,\rho)\) pilot, show that the fixed-ratio margin can dominate the
new enclosure widths.

The current work does not justify DGX use.  The next gates are analytic and
small-symbol computations; large parallel interval runs would only make the
present uncertainty more expensive.

## Publication boundary

R0.70A stays outside `public/`.  A public update becomes appropriate only if
R0.70B produces a closed bridge/incomparability lemma, a falsified route with
a reusable proof, or an explicit audited \(\rho\)-interval certificate.
