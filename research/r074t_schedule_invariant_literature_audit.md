# R0.74T Step 19 — bounded primary-literature audit for schedule-invariant lobe coercivity

## 0. Verdict and claim boundary

This audit asks whether the six primary sources listed below already contain
the following **combined** statement used in R0.74T, Step 19:

1. an exact common-shear or 2D3C Navier--Stokes family containing more than
   one passive packet;
2. independently prescribed packet target times inside one common admissible
   time slab;
3. a uniform total-field lower bound on a spatially localized packet lobe for
   a positive dwell interval;
4. conversion of that lobe floor into the nonnegative, spatially weighted
   exterior payment

   \[
    (2R)^{-2}\int W_{2R}(x)|u(t,x)|^3\,dx\,dt;
   \]

5. a completed-clock fixed-deletion consequence which remains valid when the
   packet windows are disjoint; and
6. the exponential normalized-dwell threshold arising from the inherited
   shell weight and survival window.

**Bounded-search verdict:** no screened source states this six-part
combination.  The sources contain important adjacent mechanisms: exact
shearing-wave superposition, the classical 2D3C/passive-component reduction,
exact scalar dispersion in a prescribed periodic shear, spatially disjoint
multi-rate passive-scalar blocks, prescribed alternating-shear time
intervals, and physical-space shell-flux locality.  None joins those
mechanisms to the R0.74T weighted positive cubic payment and its
schedule-invariant lobe-survival quantifiers.

This is a **finite primary-source non-hit**.  It does not prove novelty,
priority, correctness, or publishability.  It did not exhaust MathSciNet,
zbMATH, all forward and backward citation graphs, dissertations, non-English
sources, unpublished manuscripts, or specialist knowledge.  It cannot be
used as a global literature claim.  **LITERATURE BOUNDARY. NOT CLAY.**

## 1. What is classical and what is actually being screened

### 1.1 The Hölder step is elementary and carries no novelty claim

For every measurable spatial set \(\Omega\) of finite positive measure,
spatial Hölder gives

\[
 \int_\Omega |u|^3
 \ge |\Omega|^{-1/2}
      \left(\int_\Omega |u|^2\right)^{3/2}.
\tag{L.1}
\]

Consequently, if \(W\ge w>0\) on moving sets \(\Omega(t)\), if
\(|\Omega(t)|\le V\), and if
\(\int_{\Omega(t)}|u|^2\ge E\) for almost every \(t\) in a measurable
set \(J\), then direct restriction of a nonnegative integral yields

\[
 \int_J\!\int W|u|^3
 \ge w|J|V^{-1/2}E^{3/2}.
\tag{L.2}
\]

Equations (L.1)--(L.2) are classical measure-theoretic facts.  Step 19's
(T.9)--(T.15) specialize them to the frozen lobe volume, shell weight, and
Version-M normalization.  Neither Hölder nor this abstract
restriction-and-integration pattern is asserted to be new.

The estimate is also formally insensitive to the position of another
packet's target interval: the other interval never enters (L.2).  That
observation alone is not a PDE scheduling theorem.  It applies only after
the hypotheses on the **total field** \(u\), the lobe, the weight, and the
dwell set have already been verified.

### 1.2 The nontrivial collision signature is the PDE combination

The literature question is therefore not whether Hölder was known.  The
actual collision signature is whether an existing theorem simultaneously
proves the following PDE-specific inputs and output:

- two passive packets evolve in one exact smooth periodic unforced
  Navier--Stokes solution under a common shear;
- the packets can be re-centred to independently selected target times while
  preserving oddness, pressure zero, shell placement, heat reserve, and all
  cross-packet dominance estimates with constants independent of the
  relative schedule;
- the full velocity, rather than an isolated summand, has a persistent lobe
  floor on each selected window;
- the positive exterior row \(\int W_{2R}|u|^3\), rather than a signed flux
  containing pressure, pays that lobe;
- disjoint packet windows still force a completed-clock fixed-deletion floor;
  and
- the explicit shell-weight/survival exponents force the dwell collapse in
  Step 19 (T.24)--(T.29).

It is this combined scheduling/lobe-survival/payment result, not (L.1), that
the six-source screen tests.

## 2. Search protocol and stopping rule

The screen used only the six primary sources requested for this audit.

The first pass checked the exact anchors already closest to R0.74T:

- parallel Kelvin-mode superposition and arbitrary-profile shearing waves;
- the 2D3C invariant reduction;
- exact periodic-shear scalar dispersion;
- the Bruè--De Lellis 2.5D embedding and spatially disjoint multi-rate
  construction;
- the later alternating-shear time-interval construction; and
- Dascaliuc--Grujić local and ensemble physical-shell flux theorems.

The second pass searched those primary texts and their exact statements for
`lobe`, `dwell`, `residence time`, `occupation time`, `packet`, `L3`,
`cubic`, `exterior`, `time interval`, and schedule-like constructions.  It
also checked whether different intrinsic time scales or predetermined
activation intervals were equivalent to independently movable packet target
times.  They were not.

The search stopped after that second pass because the remaining hits repeated
one of three already classified mechanisms--spectral/shearing-wave
superposition, passive-scalar mixing or dispersion, and time/ensemble
averaged flux--without adding the missing positive weighted-cubic and
schedule-uniform lobe statement.  This is a diminishing-yield stop, not an
exhaustiveness claim.

## 3. Exact-flow and 2D3C sources

### 3.1 Singh--Sridhar: exact plane shearing waves

**Source.** N. K. Singh and S. Sridhar,
[*Plane shearing waves of arbitrary form: exact solutions of the
Navier--Stokes equations*](https://arxiv.org/pdf/1101.5507), preprint 2011,
published in *European Physical Journal Plus* **132** (2017), 403.

**Exact anchors checked.** Equations (1)--(4) give the perturbation equations,
the Kelvin ansatz, and the vanishing of the nonlinear term for one mode.
The paragraph immediately preceding equation (15) proves that any number of
Kelvin modes whose wave vectors are parallel remain an exact solution after
superposition.  Equations (14)--(19) give the shear-periodic coordinates,
the common sheared direction, the Fourier superposition, and the real-space
sheared-heat-kernel representation.  The Gaussian polarized wavepacket
example follows equations (18)--(19).

**What it supports.** It is a strong primary precedent for an exact nonlinear
superposition mechanism.  Parallel initial wave vectors remain parallel
under the same linear background shear; incompressibility then keeps the
superposed velocity tangent to the common wavefronts, so the quadratic
nonlinearity vanishes.  The Fourier amplitudes may encode an arbitrary
transverse profile and polarization, with unbounded or shear-periodic
boundary conditions.

**What it does not cover.** The construction is a plane transverse shearing
wave tied to one common sheared wavefront and one linear-shear clock.  Its
illustrative wavepacket is localized in the transverse profile but extended
along the wavefront; it is not the R0.74T three-dimensional physical-shell
lobe.  The paper gives no independently prescribed target time for each
packet, no uniform lobe-survival or cross-packet dominance theorem, no moving
shell clock, no positive spatially weighted exterior \(L^3\) payment, and no
dwell threshold.  Thus it establishes an adjacent exact-superposition
principle, not the Step 19 combination.

**Confidence:** high for the stated source boundary.

### 3.2 Biferale--Buzzicotti--Linkmann: the classical 2D3C split

**Source.** L. Biferale, M. Buzzicotti, and M. Linkmann,
[*From two-dimensional to three-dimensional turbulence through
two-dimensional three-component flows*](https://arxiv.org/pdf/1706.02371),
*Physics of Fluids* **29** (2017), 111101.

**Exact anchors checked.** Section II, equations (1)--(5).  Equation (1)
splits \(u\) into an in-plane field \(u^{2D}\) and an out-of-plane component
\(\theta\).  Equation (2) records that \(u^{2D}\) solves two-dimensional
Navier--Stokes while \(\theta\) is passively advected and diffused.  Equations
(3)--(5) give the associated vorticity decomposition.

**What it supports.** It confirms that the 2D3C/passive-third-component
architecture is established prior structure.  The in-plane velocity evolves
autonomously and the third component obeys a linear scalar equation once the
in-plane field is fixed.  This structural reduction must not be presented as
new in R0.74T.

**What it does not cover.** The paper studies analytical invariants, helical
decomposition, cascade directions, and numerical couplings of 2D3C
manifolds.  Section II does not construct R0.74T's localized heat packets or
independently movable terminal lobes.  It contains no packet dwell theorem,
no Version-M shell weight, no positive exterior cubic row, no completed-clock
fixed deletion, and no schedule-invariant coercivity statement.

**Confidence:** high for the stated source boundary.

### 3.3 Jiménez-Urias--Haine: exact scalar dispersion in a periodic shear

**Source.** M. A. Jiménez-Urias and T. W. N. Haine,
[*An exact solution to dispersion of a passive scalar by a periodic shear
flow*](https://arxiv.org/pdf/2101.05406), arXiv preprint (2021).

**Exact anchors checked.** Section 2.2, especially the prescribed
advection--diffusion equation (2.4), Mathieu reduction (2.6)--(2.10), exact
series (2.12), modal example (2.15), and general Fourier-synthesized solution
(2.18)--(2.19).  Section 3, equations (3.1)--(3.5), begins the exact closure
for weighted cross-channel averages.

**What it supports.** For a time-independent prescribed periodic shear, the
paper supplies an exact all-time passive-scalar solution and an exact closure
across the scalar wavenumbers.  Equation (2.19) also confirms linear Fourier
synthesis of more general scalar initial data.

**What it does not cover.** The shear is prescribed rather than coupled as
the common component of an exact unforced three-dimensional Navier--Stokes
packet solution.  Different Fourier modes are not assigned independently
movable target times.  The paper studies dispersion and closure, not
physical-shell lobes, total-velocity dominance, completed clocks, exterior
spatial weights, a positive \(|u|^3\) payment, or dwell-time coercivity.

**Confidence:** high for the stated source boundary.

## 4. Passive-scalar scheduling and embedding sources

### 4.1 Bruè--De Lellis: 2.5D embedding and disjoint multi-rate blocks

**Source.** E. Bruè and C. De Lellis,
[*Anomalous dissipation for the forced 3D Navier--Stokes
equations*](https://arxiv.org/pdf/2207.06301), *Communications in
Mathematical Physics* **400** (2023), 1507--1533.

**Exact anchors checked.** Section 3.1, equation (3.1) and the displayed
\((2+\tfrac12)\)-NS system, together with Theorems 3.1--3.2, give the forced
three-dimensional embedding of a two-dimensional Navier--Stokes velocity and
a passive scalar.  Theorem 4.1, equations (4.3)--(4.8), constructs a
quasi-self-similar chain.  Proposition 7.1, equations (7.1)--(7.6), gives a
smooth exponentially mixing transport block.  Section 7.2, equations
(7.7)--(7.11), Remark 7.2, and Lemma 7.3, equations (7.13)--(7.16), place
rescaled blocks in disjoint cubes \(Q_n\), with spatial scales \(\lambda_n\)
and intrinsic time scales \(\tau_n\), and record their norm estimates.

**What it supports.** This is the nearest screened primary precedent for
combining a passive-scalar architecture with many spatially disjoint blocks
that evolve at different rates.  The disjoint supports permit exact summation
of the transport blocks, and the 2.5D embedding turns the scalar into a third
velocity component of a forced three-dimensional Navier--Stokes solution.

**What it does not cover.** The target is anomalous dissipation in a
vanishing-viscosity, forced construction.  The block parameter
\(t/\tau_n\) changes each block's intrinsic rate, but all blocks use the same
external time origin; Section 7.2 does not prove invariance under arbitrary
per-packet target-time translations.  Its quantitative conclusions concern
mixing, \(H^{-1}\), \(L^2\), scalar gradients, velocity gradients, and
dissipation.  They do not give the R0.74T total-field lobe floor, moving
physical-shell weight, positive exterior \(L^3\) payment, completed-clock
floor, or exponential dwell budget.  Spatial disjointness of construction
blocks is not the same quantifier as two arbitrarily scheduled terminal
lobes in one frozen observation slab.

**Confidence:** high for the stated source boundary.

### 4.2 Bruè--Colombo--Crippa--De Lellis--Sorella: prescribed time intervals

**Source.** E. Bruè, M. Colombo, G. Crippa, C. De Lellis, and M. Sorella,
[*Onsager critical solutions of the forced Navier--Stokes
equations*](https://arxiv.org/pdf/2212.08413), *Communications on Pure and
Applied Analysis* **23** (2024), 1350--1366.

**Exact anchors checked.** Section 3.2 defines the temporal support and the
paired intervals
\(I_q=[1-T_q,1-T_{q+1}]\) and
\(J_q=[1+T_{q+1},1+T_q]\).  Proposition 3.1, especially properties (1)--(5)
and equations (3.5)--(3.10), provides an alternating horizontal/vertical
shear, fixed support-length estimates on those intervals, the associated
advection--diffusion solution, and anomalous dissipation along a viscosity
sequence.  Section 4, equations (4.1)--(4.4) and Lemma 4.1, embeds the
construction into a smooth forced three-dimensional Navier--Stokes solution
with zero pressure.

**What it supports.** It is the closest screened source to an explicit
time-scheduling architecture.  The active intervals accumulate at the fixed
central time \(t=1\), include neighborhoods on which the shear vanishes, and
come with quantitative temporal-support bounds.  It also confirms an exact
alternating-shear 2.5D embedding into forced Navier--Stokes.

**What it does not cover.** The interval schedule is one globally designed,
scale-indexed, reflection-symmetric cascade.  Proposition 3.1 does not allow
each passive packet to choose an arbitrary target time while holding a
common-shear solution and uniform lobe constants fixed.  The result is
forced and vanishing-viscosity; it does not establish a physical-shell lobe
of the total velocity, an exterior radial weight, a positive weighted
\(|u|^3\) lower payment, a completed-clock fixed-deletion floor, or the
R0.74T dwell exponent.  Its \(L_t^3C_x^{1/3-\varepsilon}\) regularity target
must not be confused with Step 19's spatially weighted velocity-cubic
payment.

**Confidence:** high for the stated source boundary.

## 5. Physical-shell flux source

### 5.1 Dascaliuc--Grujić: physical-scale flux locality

**Source.** R. Dascaliuc and Z. Grujić,
[*Energy cascades and flux locality in physical scales of the 3D
Navier--Stokes equations*](https://arxiv.org/pdf/1101.2193),
*Communications in Mathematical Physics* **305** (2011), 199--220.

**Exact anchors checked.** Section 5 defines the shell cutoff and thickness
in (5.1)--(5.2), the localized time-averaged flux in (5.3), and the modified
flux in (5.4)--(5.6).  Equations (5.7)--(5.8) define localized energy,
enstrophy, and the local Taylor scale.  Proposition 5.1 and Theorem 5.1,
equations (5.13)--(5.17), compare the modified shell flux with localized
enstrophy under a local Taylor-scale condition on the fixed interval
\([0,2T]\), \(T\ge R_0^2/\nu\).  Equations (5.20)--(5.29) define optimal
shell covers and their ensemble averages.  Theorem 5.2 and Corollary 5.1,
equations (5.41)--(5.42), give the corresponding ensemble locality bounds.

**What it supports.** This paper is a rigorous physical-space precedent for
localization by shell cutoffs, bounded-overlap optimal covers, and comparison
of time/ensemble-averaged fluxes across physical scales.  Its flux contains
the cubic velocity contribution

\[
 \left(\frac12|u|^2+p\right)u\cdot\nabla\phi,
\tag{L.3}
\]

and its theorem is valid in the suitable/local-energy setting without a
regularity assumption.

**What it does not cover.** Expression (L.3) is a **signed flux** containing
pressure and the directional factor \(u\cdot\nabla\phi\); it is not the
nonnegative payment \(W|u|^3\).  Theorem 5.1 starts from a local Taylor-scale
condition and obtains a common-window time average.  It does not start from
a persistent packet lobe, lower-bound an absolute velocity-cubic integral,
assign target times to passive packets, or prove schedule invariance.
Optimal-cover multiplicity controls spatial overlap among test shells, not
temporal overlap or independent terminal-time choices among packet clocks.
Theorem 5.2 therefore does not imply Step 19 (T.9)--(T.18) or
(T.24)--(T.29).

**Confidence:** high for the stated source boundary.

## 6. Claim-to-source collision matrix

The symbols in the table mean: **Y** = stated mechanism is present;
**A** = adjacent but has a materially different observable or quantifier;
**N** = not supplied by the checked anchor.

| Primary source | Exact NS/passive reduction or superposition | Independently movable packet target times | Uniform total-field physical lobe | Positive weighted exterior \(\int W|u|^3\) | Disjoint-time completed-clock floor | Exponential dwell threshold |
|---|---:|---:|---:|---:|---:|---:|
| Singh--Sridhar | Y: parallel Kelvin waves | N | N | N | N | N |
| Biferale--Buzzicotti--Linkmann | Y: classical 2D3C split | N | N | N | N | N |
| Jiménez-Urias--Haine | A: prescribed-shear scalar equation | N | N | N | N | N |
| Bruè--De Lellis | Y: forced 2.5D embedding; disjoint multi-rate blocks | N: different rates, common origin | N | N | N | N |
| Bruè et al. | Y: forced alternating-shear embedding | N: one fixed accumulating schedule | N | N | N | N |
| Dascaliuc--Grujić | A: suitable-weak physical-shell flux | N | N | A: signed pressure flux only | N | N |
| R0.74T Step 19 package | inherited exact unforced common-shear family | proved only inside the stated slab | proved for the selected lobes | proved by classical Hölder after PDE inputs | proved for \(\mathfrak L^K_{1,R}\) | proved for inherited exponents |

No row from the screened literature reaches the Step 19 combination by
itself.  Combining rows informally would also be invalid: the sources use
different equations, forcing regimes, domains, time quantifiers, observables,
and asymptotic parameters.

## 7. Safe attribution and non-claims

### 7.1 Established ingredients that must be attributed

The following mechanisms are prior knowledge and carry no R0.74T novelty
claim:

- spatial Hölder and restriction of a nonnegative integral;
- the 2D3C decomposition into a two-dimensional velocity and a passive third
  component;
- exact superposition of parallel Kelvin modes in a linear background shear;
- Fourier synthesis for a passive scalar in a prescribed periodic shear;
- quasi-self-similar and spatially disjoint passive-scalar mixing blocks;
- alternating-shear time-interval constructions for forced anomalous
  dissipation; and
- physical-shell localization, optimal covers, and time/ensemble-averaged
  modified-flux locality.

### 7.2 The boundedly distinct combination

Subject to the separate proof certificates, Step 19 internally combines
different ingredients in a way not stated by the six checked sources:

1. the inherited exact smooth periodic **unforced** common-shear packet
   solution;
2. two independently prescribed target windows inside one admissible slab;
3. schedule-uniform persistence, annular placement, and total-field lobe
   dominance, Step 19 (T.34)--(T.40);
4. the completed-clock fixed-deletion floor (T.17), (T.41), even when the
   target windows are disjoint;
5. the positive weighted exterior cubic payment (T.9)--(T.15), obtained by
   the classical inequality (L.1) only after the PDE lobe inputs are proved;
   and
6. the explicit logarithmic dwell identity and necessary collapse threshold
   (T.24)--(T.29), followed by the disjoint-window obstruction (T.42)--(T.43).

Calling this combination “not found in the six-source screen” is warranted.
Calling it globally new, first, optimal among all Navier--Stokes families, or
submission-ready is not warranted.

### 7.3 Safe manuscript wording

A defensible statement is:

> The coercive integration step is an immediate application of spatial
> Hölder and is not claimed as new.  The project contribution at this stage
> is the internally certified combination of common-shear packet
> re-centring, schedule-uniform total-field lobe survival, a completed-clock
> fixed-deletion witness, and the resulting explicit dwell threshold.  A
> bounded screen of six primary sources found adjacent exact-flow,
> passive-scalar, and physical-flux mechanisms, but no theorem with this
> complete combination.  This non-hit is not a novelty or priority claim.

## 8. Final boundary

This audit supports attribution discipline and a narrow collision statement
only.  It does not certify the correctness of Step 19's internal estimates;
those require their analytic and independent certificates.  It does not
prove a general arbitrary-real-time packet scheduling theorem, a payment
upper bound for the full completed-clock functional, the Step 18
fixed-deletion gate, R0.74Q (Q.1), scale contraction, regularity, singularity,
or the Navier--Stokes Millennium problem.  **NOT CLAY.**

<!-- R074T_STEP19_LITERATURE_AUDIT_END -->
