# R0.74R — primary-literature boundary for terminal-window persistence and arbitrary completed clocks

## Status and scope

This note records a bounded primary-source collision screen completed on
2026-09-02.  The target was deliberately narrow.  It asked whether the
screened literature already proves any theorem of the following form for an
arbitrary suitable weak three-dimensional Navier--Stokes solution:

1. a large defect-completed shell clock at an arbitrary good terminal time
   in the full cutoff interval
   yields, outside only finitely many shell exceptions, a comparable endpoint
   kinetic row plus a time interval of quantitatively non-vanishing kinetic
   persistence;
2. the resulting persistence factors obey the weighted packing

   \[
    \sum_k2^{3k}\gamma_k\Lambda_k^3(\Theta_k^\eta)^{-2}\le C;
   \]

3. dissipation-dominated clocks or recent positive upcrossings can instead be
   charged at the quadratic scale \((P_R^M)^{2/3}\); or
4. these ingredients imply the R0.74Q best-terminal-tail estimate, or the
   unconditional fixed-scale inequality (Q.1).

No direct theorem of these forms was found in the bounded screen.  Several
strongly adjacent results were found and are recorded below.  In particular,
the literature already contains all-left-time local \(L^3\) concentration
near an assumed singular point, Type-I concentration on shrinking parabolic
balls, local-energy upper estimates and reverse Hölder estimates under extra
control, physical-space flux locality under an inertial-range hypothesis, and
two 2026 preprints on endpoint energy atoms or finite-chain signed work.  Those
results materially constrain how R0.74R may be described.

This is a finite non-hit statement, not a novelty, priority, correctness,
peer-review, or publishability certificate.  The two 2026 sources are arXiv
preprints and are not treated as peer-reviewed results.  **LITERATURE
BOUNDARY. NOT CLAY.**

## Search protocol and stop rule

The screen used primary journal pages and original arXiv records through
2026-09-02.  Query families covered `local energy strong energy inequality`,
`endpoint local kinetic energy`, `all times left neighborhood L3
concentration`, `terminal energy spacetime L3 persistence`, `positive
variation local energy flux`, `physical scale shell packing`, `dissipation
alternative`, `endpoint energy atom pressure work`, and `finite chain signed
work depletion`.

Discovery was followed by direct theorem-level checks for the closest hits:
Neustupa's singular-point concentration result; Barker--Prange's localized
smoothing and Type-I concentration theorem; Barker--Prange's later
quantitative spatial-concentration results; and the 2026 Yu and Huang
preprints.  The search stopped after exact-phrase and targeted follow-up
queries returned the same regularity, concentration, local-energy, and
coarse-grained-work families without a completed-clock persistence-packing
theorem.  The stop rule was diminishing primary-source yield, not exhaustive
coverage of every database, thesis, unpublished manuscript, or private
communication.

## Primary-source ledger

| Source | Verified contribution | Boundary relative to R0.74R |
|---|---|---|
| J. Neustupa, [*A note on local interior regularity of a suitable weak solution to the Navier--Stokes problem*](https://doi.org/10.3934/dcdss.2013.6.1391), DCDS-S **6** (2013), 1391--1400. | If \((x_0,t_0)\) is singular, a universal positive amount of local \(L^3\) mass is present in arbitrarily small neighborhoods of \(x_0\) at every time in a left neighborhood of \(t_0\); the paper also proves a strong energy inequality for a localized solution. | This is the closest mature temporal-persistence precedent.  It starts from an assumed singular point and concludes physical-ball \(L^3\) concentration.  It does not start from an arbitrary completed shell clock, separate its kinetic/dissipative/upcrossing branches, or prove the weighted \(\Theta\)-packing required in (R.217). |
| T. Barker, C. Prange, [*Localized smoothing for the Navier--Stokes equations and concentration of critical norms near singularities*](https://arxiv.org/abs/1812.09115), ARMA **236** (2020), 1487--1541. | Proves quantified local smoothing from small local critical initial data.  Under its Type-I local kinetic-energy bound and a first singular point at \((0,T^*)\), Theorem 2 gives a universal lower bound for the \(L^3\) norm on a ball of radius comparable to \(\sqrt{T^*-t}\) for every sufficiently late time. | It is solution-centred, singularity-conditioned, and depends on a Type-I bound.  It does not turn an arbitrary prescribed-centre clock at an arbitrary good time into the endpoint/window decomposition (R.216)--(R.217). |
| T. Barker, C. Prange, [*Quantitative regularity for the Navier--Stokes equations via spatial concentration*](https://doi.org/10.1007/s00220-021-04122-x), CMP **385** (2021), 717--792. | Gives quantitative Type-I concentration and time-slice regularity results, with backward/forward propagation of vorticity concentration and scale summation under explicit critical control. | Strong propagation technology, but its hypotheses and observables differ: it does not give uniform packing of defect-completed physical shell clocks, a persistence ratio \(\Theta_k\), or a quadratic payment for arbitrary dissipation/upcrossing branches. |
| C. Guevara, N. C. Phuc, [*Local energy bounds and ε-regularity criteria for the 3D Navier--Stokes system*](https://arxiv.org/abs/1702.00449), Calc. Var. PDE **56** (2017), 68. | Establishes local-energy bounds and improved ε-regularity criteria using head pressure as a signed negative-order Sobolev distribution. | Provides forward local-cylinder estimates and pressure technology, not the reverse terminal-clock extraction or weighted shell persistence packing. |
| Q. Jiu, Y. Wang, D. Zhou, [*On Wolf's regularity criterion of suitable weak solutions to the Navier--Stokes equations*](https://arxiv.org/abs/1805.04841), J. Math. Fluid Mech. **21** (2019), 29. | Proves a Caccioppoli/ε-regularity criterion from small \(L^{20/7}\) spacetime velocity using local pressure projection. | Converts a small spacetime input into regularity; it does not derive a spacetime lower bound from endpoint completed-clock mass. |
| H. J. Choe, M. Yang, [*Local kinetic energy and singularities of the incompressible Navier--Stokes equations*](https://arxiv.org/abs/1705.04561), JDE **264** (2018), 1171--1191. | Derives a reverse Hölder inequality for the velocity gradient under a uniformly bounded scaled local-kinetic-energy functional and applies it to singular-set dimensions. | The reverse Hölder statement has an additional uniform cylinder-scale hypothesis and concerns gradient integrability.  It neither supplies (R.216) nor reverses accumulated dissipation into a velocity-cubic payment. |
| R. Dascaliuc, Z. Grujić, [*Energy cascades and flux locality in physical scales of the 3D Navier--Stokes equations*](https://arxiv.org/abs/1101.2193), CMP **305** (2011), 199--220. | Proves physical-space ensemble flux bounds and locality under an inertial-range/Taylor-scale condition using local energy inequalities. | The cover/ensemble packing is conditional on a cascade regime and concerns physical balls.  It does not control terminal moving-shell clocks or their shellwise persistence factors. |
| T. M. Leslie, R. Shvydkoy, [*The energy measure for the Euler and Navier--Stokes equations*](https://arxiv.org/abs/1705.04420), ARMA **230** (2018), 459--492. | Defines endpoint energy measures and bounds their local and concentration dimensions from spacetime integrability; Type-I-in-time Navier--Stokes solutions satisfy energy equality at first blowup time. | Establishes the endpoint-measure framework, not an implication from a finite-scale completed clock to a thick kinetic window or a best-terminal shell tail. |
| R. Yu, [*Coarse-Grained Resolution and Pressure--Flux Work Depletion for Navier--Stokes CKN Badness*](https://arxiv.org/abs/2606.25322), arXiv:2606.25322v1 (2026), preprint. | Gives a finite-scale coarse-grained CKN resolution lemma, finite-dimensional active-work extraction, and a fixed finite-chain weighted telescoping inequality.  Forward combined work and resolved dissipation are paid by initial localized kinetic energy, leakage, and negative work/backscatter; an independent coarse observability implication is left unproved. | This is the closest signed-work/depletion collision.  Its finite chain, active test family, resolved filter, leakage, and backscatter ledger are not (R.216)--(R.217), and the missing observability step is analogous evidence that extraction remains a separate problem rather than a solved input. |
| H. Huang, [*Endpoint Energy Atoms Force Local Pressure Concentration in Three-Dimensional Navier--Stokes Flow*](https://arxiv.org/abs/2608.30715), arXiv:2608.30715v1 (2026), preprint. | Under a point atom in an endpoint energy measure on \(\mathbb T^3\), constructs a same-state constrained/passive comparison and obtains an exact nonnegative accumulated pressure-work identity plus mesoscopic pressure-concentration lower bounds. | Requires the much stronger limiting atom hypothesis and produces pressure work after radius-dependent restarts.  It does not start from an arbitrary finite-scale shell clock and does not prove uniform endpoint kinetic persistence or the \(\ell^3\) coefficient packing in (R.217). |
| H. Huang, [*Full-Tail Dynamical Rigidity Forced by Atomic Navier--Stokes Energy Concentration*](https://arxiv.org/abs/2608.04138), arXiv:2608.04138v1 (2026), preprint. | Under endpoint atomic energy concentration, obtains packet/adjoint rigidity and failure of a delayed second-order action budget. | The atom and packet-genealogy hypotheses are outside the R0.74R completed-clock chart.  The result neither proves nor falsifies arbitrary-clock persistence packing. |

## Claim-to-source gap matrix

| R0.74R claim or target | Closest screened source family | Collision result |
|---|---|---|
| A good-time endpoint kinetic row satisfies endpoint averaging plus positive terminal-inclusive variation. | Local/strong energy inequalities; Neustupa; Guevara--Phuc. | **NO NOVELTY CLAIM.**  The R0.74R inequality is an elementary consequence of the inherited completed-clock split and monotonicity of its defect/dissipation row; the mature literature supplies the local-energy setting. |
| Large completed-clock value obeys the exact kinetic/dissipation/upcrossing triage (R.207). | Strong local-energy inequalities; finite-chain resolved-energy ledgers in Yu. | **NO IDENTICAL FORM FOUND.**  The triage is internal clock algebra, not advertised as a literature-level novelty. |
| Cutoff-weighted endpoint kinetic persistence pays with coefficient \(2^k\gamma_k^{1/3}(\Theta_k^\eta)^{-2/3}\) on the full cutoff interval. | Neustupa and Barker--Prange concentration; Jiu--Wang--Zhou spacetime criteria. | **NO IDENTICAL WEIGHTED SHELL ESTIMATE FOUND.**  The estimate itself is Hölder plus the inherited padded-shell geometry and is not a novelty claim. |
| A universal suitable-weak construction satisfying (R.216)--(R.217). | Neustupa; Barker--Prange; Choe--Yang; Yu; Huang. | **NOT FOUND / OPEN IN THIS PROJECT.**  Adjacent theorems require a singular point, Type-I control, uniform local-energy control, finite resolved test families, or endpoint atomic concentration. |
| Dissipation-dominated clocks are quadratically paid by velocity cubic mass. | Local energy bounds and reverse Hölder papers. | **NOT FOUND.**  R0.74R's high-frequency divergence-free functional example forbids a purely functional reverse inequality; a proof would have to use additional Navier--Stokes dynamics. |
| Recent positive upcrossings are summably charged at the square-function scale. | Yu's signed forward/backscatter finite-chain ledger; physical-space cascade locality. | **NOT FOUND.**  Existing adjacent ledgers retain negative work, leakage, a finite chain, or regime hypotheses and do not yield the R0.74R all-shell bound. |
| The unconditional fixed-scale inequality (Q.1), regularity, singularity, or the Millennium conclusion. | All screened sources. | **NOT FOUND / NOT CLAIMED. NOT CLAY.** |

## Exact attribution and research consequence

The bounded screen changes the route description in two useful ways.

First, “kinetic mass persists near a bad terminal point” is not itself a new
idea: Neustupa and Barker--Prange prove powerful all-late-time concentration
statements under singularity and, in the latter case, Type-I hypotheses.
R0.74R must therefore describe its distinct unresolved input more narrowly:
an arbitrary finite-scale, prescribed-centre, defect-completed shell clock
must be converted into endpoint kinetic mass and a packable persistence
ratio without assuming the singular point or Type-I conclusion in advance.

Second, Yu's finite-chain result and Huang's endpoint-atom pressure-work
identity show that signed work can be made rigorous when one retains the
correct leakage/backscatter terms or assumes a strong endpoint concentration
object.  Neither supplies the missing arbitrary-clock observability theorem.
The next PDE step should therefore target one of two explicit bridges:

- a localized stopping-time inequality that sends recent clock upcrossing to
  signed work while keeping negative work and leakage quantitatively visible;
  or
- a dynamical lemma that turns the dissipation branch into either finitely
  many exceptional shells or a parabolically thick kinetic interval.

The screen does not justify an originality statement.  A submission-stage
audit would still require MathSciNet/zbMATH citation tracing and specialist
review.  The arbitrary-clock extraction, (Q.1), scale contraction,
regularity, singularity formation, and the Clay problem remain **OPEN**.
**NOT CLAY.**
