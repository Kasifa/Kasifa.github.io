# R0.74U Step 20 — bounded primary-literature audit for intrinsic physical-lobe residence

## 0. Verdict and claim boundary

This audit asks whether the named primary sources already state the combined
R0.74U result for the frozen common-shear packet architecture:

1. one exact smooth periodic **unforced** Navier--Stokes solution contains the
   common shear and the inversion-paired passive packets;
2. the centre of a selected canonical packet lobe has speed comparable to
   \(R^{-2}\) throughout the inherited terminal slab;
3. an explicitly computed horizontal room of order \(L_iR\) keeps that lobe
   inside a selected **physical-space annulus**;
4. speed times room gives a certified geometric residence corridor of order
   \(L_iR^3\);
5. total-field dominance turns that corridor into a lower inclusion for the
   completed-clock (K)-superlevel set, yielding only

   \[
   \Omega(L_iR^3);
   \tag{L.U.1}
   \]

6. the same lobe enters the nonnegative weighted exterior velocity-cubic
   payment, so the certified residence conflicts with the inherited
   exponentially short-dwell requirement.

**Bounded-search verdict:** no source in this finite screen states that
six-part combination.  The screen does locate several genuine neighboring
mechanisms: exact Kelvin-wave superposition, columnar and 2D3C passive-scalar
reductions, exact periodic-shear dispersion, shear-induced Fourier-mode
lifetimes, prescribed multi-scale time schedules, physical-space shell flux,
and partial regularity.  It also locates one especially important near-name
collision: Inage (2026) states a residence-time compression theorem for
low-drift coherent Fourier--helical triads.  That theorem concerns a different
state variable, a different shell notion, and an upper temporal estimate; it
is not the physical-lobe residence statement in R0.74U.

This is a **finite primary-source non-hit**, not a proof of novelty or
nonexistence.  It makes no judgment about novelty, priority, correctness, or
publishability--either of R0.74U or of any screened paper.  **LITERATURE
BOUNDARY. NOT CLAY.**

## 1. Exact object being screened

### 1.1 Geometric residence versus completed-clock residence

R0.74U defines the certified geometric corridor by the centre condition

\[
 \mathscr R_i^{\rm cert}
 =\{t\in I_R:|Q_i(t)|<A(L_i)L_iR\}.
\tag{L.U.2}
\]

The two inputs are kinematic: \(Q_i'(t)\asymp R^{-2}\) on the slab and the
available physical annular room is \(A(L_i)L_iR\asymp L_iR\).  Hence the
certified corridor has scale \(L_iR^3\).  This two-sided conclusion is for
\(\mathscr R_i^{\rm cert}\), not for the complete clock.

After the direct packet, inversion partner, other packet, and periodic copies
are compared in the **total field**, the corridor is included in a
\(K_{k_i,R}\)-superlevel set.  For that superlevel set, R0.74U asserts only the
lower residence order in (L.U.1).  It asserts no converse inclusion and no
upper bound.  The literature audit preserves exactly that one-sided boundary.

### 1.2 Hölder is classical

The payment conversion uses the elementary spatial inequality

\[
 \int_{\Omega}|u|^3
 \ge |\Omega|^{-1/2}
      \left(\int_{\Omega}|u|^2\right)^{3/2},
\tag{L.U.3}
\]

followed by restriction of a nonnegative spacetime integral to a measurable
time set.  This is classical Hölder, and neither (L.U.3) nor the abstract
restriction step carries a novelty claim.  The collision question concerns
the PDE construction and its physical-lobe, total-field, clock, and payment
quantifiers, not Hölder's inequality.

## 2. The essential shell disambiguation

Three different uses of the word *shell* occur near this subject and must not
be identified.

1. A **Fourier frequency shell** groups modes with
   \(|k|\sim 2^j\).  A helical decomposition then resolves each Fourier mode
   into curl eigenpolarizations.  Inage's coherent family
   \(\tau=(k,p,q)\) and Biferale--Buzzicotti--Linkmann's helical modes live in
   this frequency-side description.
2. The R0.74U **physical-space annulus** is a subset of the spatial variable
   \(x\), with radius comparable to \(L_iR\), selected by the cutoff
   \(\Psi_{k_i}^R(x)\).  Its moving lobe box \(\Omega_i(t)\) is required to
   remain inside that spatial annulus.
3. Dascaliuc--Grujić also use physical-space shells between two spheres, but
   their observable is a fixed-shell time-averaged signed pressure flux, not
   the R0.74U moving-lobe completed clock.

Frequency localization does not imply support in a physical annulus, and
physical localization does not preserve a single frequency shell.  There is
therefore no formal implication from a Fourier--helical residence theorem to
the geometric inclusion (L.U.2), or conversely.  This distinction is the
decisive answer to the closest lexical collision.

## 3. Near-name collision: Inage (2026)

### 3.1 Source and access record

**Source.** Shin-ichi Inage,
[*Structural Reduction Framework and Residence-Time Compression of Coherent
Same-Scale Triadic Interactions in the 3D Navier--Stokes
Equations*](https://doi.org/10.3390/math14091410), *Mathematics* **14**
(2026), article 1410, DOI
[10.3390/math14091410](https://doi.org/10.3390/math14091410).

The direct DOI landing request and the MDPI HTML article endpoint returned
HTTP 429 during this audit.  Accordingly, this note does **not** claim that
the interactive MDPI article page was opened.  Bibliographic metadata was
cross-checked through the
[Crossref work record](https://api.crossref.org/works/10.3390/math14091410),
and the precise theorem text was checked in MDPI's publisher-hosted static
[JATS XML](https://mdpi-res.com/d_attachment/mathematics/mathematics-14-01410/article_deploy/mathematics-14-01410.xml)
and
[PDF](https://mdpi-res.com/d_attachment/mathematics/mathematics-14-01410/article_deploy/mathematics-14-01410.pdf).
The JATS metadata identifies the DOI, author, journal, volume, issue, article
number, and electronic publication date of 23 April 2026.

### 3.2 Exact anchors checked

Section 1.3, Theorem 1(3), is explicitly titled “Residence-time compression
of the coherent regime.”  For a coherent same-scale triadic family
\(\tau\), it introduces a low-drift set \(D_{\tau,j}(\lambda)\) at Fourier
scale (j) and states a scale-decaying upper measure estimate on bounded
time intervals.  The theorem attributes the estimate to absolute-value
curvature coercivity together with bounded variation of the phase variables.
The theorem's own scope remark says that the result is conditional on the
paper's structural reduction and does not imply full global regularity.

Section 6.6, Lemma 2, equations (221)--(226), gives the local statement in the
following sequence:

- (221) takes an interval
  \(J\subset\{t:|\mathsf\Omega_\tau(t)|\le\lambda\}\);
- (222) states

  \[
   |J|\le C\lambda(2^j\mathsf\Theta_j)^{-1};
  \tag{L.U.4}
  \]

- (223) invokes the curvature-magnitude estimate
  \(|\partial_t\mathsf\Omega_\tau|\ge c2^j\mathsf\Theta_j\) on the
  amplitude-active, geometrically nondegenerate, same-scale coherent set;
- (224)--(226) present the integration step and repeat (L.U.4).

This audit records what those cited locations state.  A literature-collision
audit is not a proof audit, so it neither validates nor rejects the argument
in equations (221)--(226).

### 3.3 Why the collision is lexical rather than mathematical

Inage's time set is selected by the smallness of a **phase-drift variable**
for a coherent family of Fourier--helical triads with
\(|k|\sim|p|\sim|q|\sim2^j\).  Its stated conclusion is an upper bound for a
low-drift interval or time set.

R0.74U's time set is selected by the **physical displacement** of a canonical
heat packet under a common shear.  Its defining implication is that a moving
three-dimensional lobe box remains in a physical-space annulus.  The R0.74U
project note states a two-sided scale only for the certified geometric
corridor, and only the \(\Omega(L_iR^3)\) lower statement for the corresponding
\(K\)-superlevel.
It does not assume amplitude-active, geometrically nondegenerate helical
triads or low phase drift.

Thus the two results use the same words “residence time” but have different
objects, hypotheses, directions of estimate, and downstream observables.
Neither can be substituted for the other.

**Confidence:** high for the source identity, exact locations, and object
distinction; no correctness assessment is made.

## 4. Exact-flow and passive-component sources

### 4.1 Singh--Sridhar: parallel Kelvin-mode superposition

**Source.** N. K. Singh and S. Sridhar,
[*Plane shearing waves of arbitrary form: exact solutions of the
Navier--Stokes equations*](https://arxiv.org/html/1101.5507), arXiv:1101.5507
(2011), later *European Physical Journal Plus* **132** (2017), 403.

**Exact anchors checked.** Equations (1)--(4) set up the linear background
shear, Kelvin ansatz, and vanishing self-interaction.  The paragraph
immediately before equation (15) proves that an arbitrary number of Kelvin
modes with parallel wave vectors can be superposed while the Navier--Stokes
nonlinearity remains zero.  Equations (14)--(19) introduce shear-periodic
coordinates and synthesize the general plane transverse shearing wave,
including the real-space heat-kernel representation.

**Overlap.** This is a primary exact-superposition precedent.  It shows that
many modes may evolve under one shear because their common wavefront geometry
kills the quadratic term.

**Boundary.** The wave is transverse to a common sheared direction and is
extended along its wavefront.  The paper does not construct R0.74U's
three-dimensionally localized canonical lobe, compute a physical annular
travel margin, compare inversion and cross-packet tails in the total field,
or derive either (L.U.1) or the weighted exterior cubic payment.

**Confidence:** high.

### 4.2 Biferale--Buzzicotti--Linkmann: 2D3C and helical coordinates

**Source.** L. Biferale, M. Buzzicotti, and M. Linkmann,
[*From two-dimensional to three-dimensional turbulence through
two-dimensional three-component flows*](https://arxiv.org/html/1706.02371),
*Physics of Fluids* **29** (2017), 111101, DOI
[10.1063/1.4990082](https://doi.org/10.1063/1.4990082).

**Exact anchors checked.** Section II, equations (1)--(5), splits a periodic
2D3C velocity into a planar Navier--Stokes field and a passively advected and
diffused third component.  Section III, equations (13)--(20), rewrites the
Fourier coefficients in the two helical curl eigenpolarizations.  Equations
(38)--(39) define spectra by sums over Fourier wavenumber shells.

**Overlap.** The passive-third-component reduction and helical basis are
established prior structure.  R0.74U makes no novelty claim for either.

**Boundary.** The helical and spectral shells are frequency objects, not the
physical annulus containing \(\Omega_i(t)\).  The paper studies invariants,
cascade direction, and numerical coupling away from the 2D3C manifold.  It
does not give an exact packet-centre corridor, total-field annular lobe
dominance, a completed-clock superlevel residence statement, or the positive
weighted exterior velocity-cubic payment.

**Confidence:** high.

### 4.3 Gibbon--Fokas--Doering: columnar stretched-vortex reduction

**Source.** J. D. Gibbon, A. S. Fokas, and C. R. Doering,
[*Dynamically stretched vortices as solutions of the 3D Navier--Stokes
equations*](https://www.ma.ic.ac.uk/~jdg/GFDPhysD.pdf), *Physica D* **132**
(1999), 497--510, DOI
[10.1016/S0167-2789(99)00067-6](https://doi.org/10.1016/S0167-2789%2899%2900067-6).

**Exact anchors checked.** Section 2.1 begins with the columnar ansatz
\(u_3=z\gamma(x,y,t)+W(x,y,t)\), equation (6).  Theorem 1, equations
(12)--(15), gives the decoupled equations for \(\omega_3\), \(W\), and
\(\gamma\).  Section 2.2, equations (23)--(31), specializes the strain and
introduces Lundgren's variables.  Theorem 2, equations (32)--(34), maps
\(\omega_3\) to two-dimensional Navier--Stokes and \(W\) to a linear passive
scalar, with the strain governed by a Riccati equation.

**Overlap.** This is an earlier exact three-dimensional reduction in which a
velocity component obeys a passive-scalar equation after a time-dependent
change of variables.  The Lundgren time map also shows that compression or
expansion of a scalar evolution clock is established exact-flow technology.

**Boundary.** The affine \(z\gamma\) ansatz and pressure/strain coupling are
not R0.74U's periodic common saturation shear.  The paper does not place a
derivative heat packet inside a selected physical annulus, establish the
centre-speed/annular-room product, compare the full multi-packet velocity, or
deduce (L.U.1) and the exterior cubic payment.

**Confidence:** high.

### 4.4 Jiménez-Urias--Haine: exact periodic-shear scalar dispersion

**Source.** M. A. Jiménez-Urias and T. W. N. Haine,
[*An exact solution to dispersion of a passive scalar by a periodic shear
flow*](https://arxiv.org/html/2101.05406), arXiv:2101.05406 (2021).

**Exact anchors checked.** Section 2.1, equations (1)--(2), states the passive
tracer problem in a re-entrant channel under the periodic shear
\(U_0\cos(2\pi y/M)\); the paragraph following equation (2) permits Fourier
synthesis of more complicated initial data.  Section 2.2, equations
(6)--(12), gives the Floquet/Mathieu eigenfunction solution.  Equations
(15)--(19) treat the modal example and general synthesis.  Section 3,
equations (20)--(43), derives exact averaged closures.

**Overlap.** It supplies an exact all-time analytical solution and Fourier
synthesis for passive scalar dispersion under a prescribed periodic shear.

**Boundary.** The scalar does not form, with the prescribed shear, the exact
unforced multi-packet Navier--Stokes field used by R0.74U.  The source does
not compute a moving physical-annulus corridor, a total-velocity lobe floor,
a completed-clock superlevel lower residence, or a positive exterior cubic
payment.

**Confidence:** high.

## 5. Shear lifetime and scheduled mixing sources

### 5.1 Coti Zelati--Gallay: Fourier-mode lifetime under stationary shear

**Source.** M. Coti Zelati and T. Gallay,
[*Enhanced dissipation and Taylor dispersion in higher-dimensional parallel
shear flows*](https://arxiv.org/html/2108.11192), *Journal of the London
Mathematical Society* **108** (2023), 1358--1392, DOI
[10.1112/jlms.12782](https://doi.org/10.1112/jlms.12782).

**Exact anchors checked.** Equation (1.1) is passive advection--diffusion in
an infinite cylinder by the stationary parallel shear \(u=(v(y),0)\).
Equations (1.2)--(1.5) Fourier transform the streamwise coordinate and reduce
the problem to one (k)-mode.  Theorem 1.1, equations (1.6)--(1.7), gives
the decay rate

\[
 \lambda_{\nu,k}=
 \begin{cases}
 \nu^{m/(m+2)}|k|^{2/(m+2)},&\nu\le |k|,\\
 k^2/\nu,&|k|\le\nu,
 \end{cases}
\tag{L.U.5}
\]

under a finite-degeneracy condition on (v).  The discussion immediately
after Theorem 1.1 calls \(1/\lambda_{\nu,k}\) the lifetime of the Fourier mode.
Assumption 2.2, equation (2.8), and Proposition 2.4, equation (2.9), encode
the cross-sectional level-set geometry used for the resolvent bound.

**Overlap.** This is a sharp primary precedent for a shear-dependent time
scale and for the dependence of decay on the degeneracy of the shear
profile.

**Boundary.** The lifetime in (L.U.5) is a decay time for one streamwise
Fourier mode of a linear stationary-shear semigroup.  It is not the time for
a moving spatial lobe to remain inside a physical annulus.  The source has no
common unforced Navier--Stokes multi-packet field, completed clock,
(K)-superlevel residence statement, or exterior velocity-cubic payment.

**Confidence:** high.

### 5.2 Bruè--De Lellis: 2.5D embedding and spatially disjoint rate blocks

**Source.** E. Bruè and C. De Lellis,
[*Anomalous dissipation for the forced 3D Navier--Stokes
equations*](https://arxiv.org/html/2207.06301), *Communications in
Mathematical Physics* **400** (2023), 1507--1533.

**Exact anchors checked.** Section 3.1, equation (3.1) and the displayed
\((2+\tfrac12)\)-NS system, embeds a planar velocity and passive scalar in a
forced three-dimensional Navier--Stokes solution; Theorems 3.1--3.2 state
the two anomalous-dissipation constructions.  Section 7.1, Proposition 7.1,
provides the exponentially mixing block.  Section 7.2, equations
(7.7)--(7.16), chooses scales \(\lambda_n\), intrinsic rates \(\tau_n\), and
amplitudes \(\gamma_n\), then places the blocks in disjoint spatial cubes
\(Q_n\).

**Overlap.** This is a close precedent for combining a passive component with
many spatially disjoint blocks that evolve on different intrinsic time
scales.

**Boundary.** The construction is forced and is designed for anomalous
dissipation as viscosity vanishes.  The rate \(t/\tau_n\) is not the
R0.74U kinematic residence of one moving lobe in a physical annulus.  It does
not establish the total-field lobe comparison, (L.U.1), or the positive
weighted exterior velocity-cubic payment.

**Confidence:** high.

### 5.3 Bruè--Colombo--Crippa--De Lellis--Sorella: prescribed time intervals

**Source.** E. Bruè, M. Colombo, G. Crippa, C. De Lellis, and M. Sorella,
[*Onsager critical solutions of the forced Navier--Stokes
equations*](https://arxiv.org/html/2212.08413), *Communications on Pure and
Applied Analysis* **23** (2024), 1350--1366, DOI
[10.3934/cpaa.2023071](https://doi.org/10.3934/cpaa.2023071).

**Exact anchors checked.** Section 3.2 defines

\[
 \mathcal I_q=[1-T_q,1-T_{q+1}],\qquad
 \mathcal J_q=[1+T_{q+1},1+T_q].
\tag{L.U.6}
\]

Proposition 3.1, especially equations (3.5)--(3.10), prescribes the temporal
support of the alternating shear, bounds its support length, and states the
advection--diffusion and anomalous-dissipation properties.  Section 4,
equations (4.1)--(4.4) and Lemma 4.1, embeds the construction in smooth
forced three-dimensional Navier--Stokes solutions with zero pressure.

**Overlap.** It is a primary precedent for a carefully engineered
scale-indexed time schedule and exact 2.5D embedding.

**Boundary.** The intervals in (L.U.6) form one globally prescribed cascade
accumulating at \(t=1\); they are not obtained by a packet crossing a spatial
annular margin under \(Q_i'\asymp R^{-2}\).  The source is forced and does not
prove R0.74U's total-field canonical-lobe statement, (L.U.1), or exterior
velocity-cubic payment.

**Confidence:** high.

## 6. Physical-space localization and regularity sources

### 6.1 Dascaliuc--Grujić: fixed physical-shell flux

**Source.** R. Dascaliuc and Z. Grujić,
[*Energy cascades and flux locality in physical scales of the 3D
Navier--Stokes equations*](https://arxiv.org/html/1101.2193),
*Communications in Mathematical Physics* **305** (2011), 199--220.

**Exact anchors checked.** Section 5, equations (5.1)--(5.2), defines a
cutoff for the physical shell between two spheres and its thickness.
Equation (5.3) defines the localized time-averaged flux

\[
 {1\over T}\iint
 \left({1\over2}|u|^2+p\right)u\cdot\nabla\phi.
\tag{L.U.7}
\]

Equations (5.4)--(5.8) define the modified flux, local energy and enstrophy,
and local Taylor length.  Proposition 5.1 and Theorem 5.1, equations
(5.13)--(5.17), compare the modified shell flux with enstrophy under a local
Taylor-scale condition.  Equations (5.20)--(5.29) introduce optimal shell
covers; Theorem 5.2 and Corollary 5.1, equations (5.41)--(5.42), give the
ensemble locality estimates.

**Overlap.** This is the closest screened source at the level of an actual
physical-space annulus.  It establishes rigorous shell cutoffs, suitable-weak
local energy accounting, and time/ensemble averaged flux locality.

**Boundary.** The shell is fixed and (L.U.7) is a signed directional flux
containing pressure.  It is not the nonnegative \(W|u|^3\) payment.  The
source does not track a moving canonical lobe, derive residence from
centre speed and annular room, compare a multi-packet total field, or yield
(L.U.1).  Spatial overlap of an optimal cover is not temporal residence.

**Confidence:** high.

### 6.2 Caffarelli--Kohn--Nirenberg: suitable weak solutions and parabolic bad sets

**Source.** L. Caffarelli, R. Kohn, and L. Nirenberg,
[*Partial regularity of suitable weak solutions of the Navier--Stokes
equations*](https://onlinelibrary.wiley.com/doi/10.1002/cpa.3160350604),
*Communications on Pure and Applied Mathematics* **35** (1982), 771--831,
DOI [10.1002/cpa.3160350604](https://doi.org/10.1002/cpa.3160350604).

**Exact anchors checked.** The Introduction, Theorem B, states that the
parabolic one-dimensional Hausdorff measure of the singular set of any
suitable weak solution is zero.  Section 2, equation (2.5), gives the
generalized local energy inequality; the definition immediately following
equations (2.5)--(2.7) specifies suitable weak solutions.  Sections 3--5
develop the dimensionless local quantities and the epsilon-regularity
iteration, including the small-dissipation regular-point criterion in
Section 5.  Section 6 completes Theorem B.

**Overlap.** CKN supplies the canonical suitable-weak local-energy and
parabolic partial-regularity framework surrounding this research program.

**Boundary.** A parabolic singular set and its Hausdorff measure are not a
canonical packet-lobe residence set.  CKN does not give an exact unforced
common-shear packet family, a physical-annulus centre-speed corridor, a
completed-clock (K)-superlevel lower residence, or the positive weighted
exterior velocity-cubic coercion.  R0.74U does not strengthen or replace CKN
epsilon regularity.

**Confidence:** high for this scope boundary.

## 7. Claim-to-source collision matrix

The symbols mean **Y** = the stated adjacent mechanism is present,
**A** = adjacent but with a materially different object or quantifier, and
**N** = not supplied by the checked anchor.

| Primary source | Exact NS/passive mechanism | Residence-type time statement | Moving total-field physical lobe | (K)-superlevel lower residence | Positive weighted exterior ∫W|u|³ | R0.74U dwell/payment conflict |
|---|---:|---:|---:|---:|---:|---:|
| Inage (2026) | A: Fourier--helical triadic reduction | Y: upper bound for low phase-drift time | N | N | N | N |
| Singh--Sridhar | Y: parallel Kelvin-wave superposition | N | N | N | N | N |
| Biferale--Buzzicotti--Linkmann | Y: periodic 2D3C split | N | N | N | N | N |
| Gibbon--Fokas--Doering | Y: columnar/passive reduction | A: Lundgren time change | N | N | N | N |
| Jiménez-Urias--Haine | A: prescribed-shear scalar solution | A: exact all-time dispersion | N | N | N | N |
| Coti Zelati--Gallay | A: stationary-shear scalar semigroup | Y: Fourier-mode decay lifetime | N | N | N | N |
| Bruè--De Lellis | Y: forced 2.5D embedding | A: block-specific rates | N | N | N | N |
| Bruè et al. | Y: forced alternating-shear embedding | Y: prescribed support intervals | N | N | N | N |
| Dascaliuc--Grujić | A: suitable-weak shell flux | A: common-window time average | N | N | A: signed pressure flux | N |
| Caffarelli--Kohn--Nirenberg | A: suitable-weak local energy | A: parabolic singular-set measure | N | N | N | N |
| R0.74U Step 20 package | inherited exact unforced common-shear packets | certified physical-lobe corridor | stated for the frozen family | lower only: Ω(L_iR³) | inherited Hölder payment after the lobe input | stated only for the frozen architecture |

No screened row gives the R0.74U combination.  Nor may rows be assembled by
informal analogy: the sources differ in equation (forced or unforced), domain,
spectral versus physical localization, time-set definition, sign of the
observable, and quantifier over the total field.

## 8. Search protocol, evidence gaps, and stopping rule

### 8.1 Bounded protocol

The audit snapshot is 3 September 2026.  The first pass checked the exact
theorem and equation anchors in the ten named primary sources.  The second
pass searched their full texts for combinations of

`residence`, `dwell`, `occupation`, `lifetime`, `low drift`, `lobe`,
`packet`, `annulus`, `physical shell`, `superlevel`, `moving centre`,
`target time`, `cubic`, and `exterior`.

The high-impact spot checks were:

- Inage, Section 1.3 Theorem 1(3) and Section 6.6 Lemma 2,
  equations (221)--(226), using the publisher-hosted JATS and PDF;
- the parallel-mode superposition paragraph before Singh--Sridhar (15);
- Biferale et al. Section II (1)--(5) and Section III (13)--(20);
- Gibbon--Fokas--Doering Theorems 1--2, equations (12)--(34);
- Coti Zelati--Gallay Theorem 1.1, equation (1.7);
- the two Bruè constructions at their explicit spatial-rate and temporal
  schedules; and
- Dascaliuc--Grujić Section 5's physical-shell definitions and flux theorems.

### 8.2 Compact gap matrix

| Question | Best primary evidence | Status after this screen |
|---|---|---|
| Is exact passive-component reduction prior art? | Gibbon--Fokas--Doering; Biferale et al.; Bruè--De Lellis | yes; classical/established ingredient |
| Is exact shear-wave or scalar synthesis prior art? | Singh--Sridhar; Jiménez-Urias--Haine | yes; established adjacent mechanism |
| Are shear-dependent lifetimes and prescribed time schedules known? | Coti Zelati--Gallay; Bruè et al.; Inage | yes, for different observables and quantifiers |
| Is physical-shell localization known? | Dascaliuc--Grujić; CKN for local cylinders | yes, but not the R0.74U moving-lobe clock |
| Does a checked source prove the physical centre-speed/annular-room corridor? | none of the named anchors | finite non-hit |
| Does a checked source prove the total-field (K)-superlevel lower residence in (L.U.1)? | none of the named anchors | finite non-hit |
| Does a checked source join that residence to the positive exterior cubic and exponential conflict? | none of the named anchors | finite non-hit |

The search stopped after the second pass because new hits repeated one of the
already classified lanes--frequency/helical phase dynamics, passive-scalar
decay, prescribed mixing schedules, or fixed-shell local energy--without
changing a material gap in the matrix.

### 8.3 Unsearched space

The audit did not exhaust MathSciNet, zbMATH, all forward and backward
citation graphs, theses, non-English literature, unpublished manuscripts,
or expert private knowledge.  Inage was included because its title and main
theorem produce a direct modern lexical collision; inclusion is not an
endorsement or criticism of that paper.  A submission-stage assessment would
require a wider citation-chain and specialist review.

## 9. Safe attribution and final non-claims

The following ingredients must be treated as established prior knowledge:

- Hölder's inequality and restriction of a nonnegative integral;
- the 2D3C/passive-third-component reduction;
- columnar/Lundgren passive-scalar reductions;
- exact superposition of parallel Kelvin modes;
- exact scalar dispersion and Fourier synthesis under periodic shear;
- stationary-shear enhanced dissipation and Fourier-mode lifetime estimates;
- spatially disjoint and temporally scheduled passive-scalar constructions;
- physical-space shell cutoffs, local energy flux, and ensemble locality; and
- suitable-weak local energy inequalities and CKN partial regularity.

The finite screen supports only this narrow statement: none of the exact
anchors checked above states the full R0.74U physical-lobe
centre-speed/annular-room theorem, its total-field inclusion yielding the
\(\Omega(L_iR^3)\) completed-clock superlevel lower residence, and its
subsequent positive-cubic dwell/payment conflict for the frozen common-shear
packet family.

It does **not** support any global statement of novelty, priority,
correctness, or publishability.  It does not prove a completed-clock upper
residence bound, a theorem for arbitrary packets or suitable weak solutions,
regularity, singularity formation, or the Millennium problem.

**NOT CLAY.**
