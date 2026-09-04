# R0.76G bounded primary-source report

## Report frame

- Audience: analysts auditing the complete-clock exact-shear route.
- Date: 2026-09-04.
- Question: does established heat observability or Remez theory already
  supply the signed radial-flux lower bound in R0.76G, and what literature
  boundary should be retained?
- Scope: primary papers and author manuscripts on heat observability,
  spectral inequalities, small-time cost, and exponential-polynomial
  propagation of smallness.
- Exclusions: an exhaustive priority search, general nonlinear
  Navier--Stokes dynamics, and a claim about the full Version-M payment.

## Direct answer

The inspected literature explains why heat observation costs can be
exponential and why geometry, time, and vanishing order matter.  It does not
state the R0.76G functional: a complete-clock signed derivative of a
shrinking radial cutoff evaluated on one explicit finite dyadic transported
heat shear and divided by a central local spacetime `L^3` mass.

R0.76G does not import a control or observability theorem.  Its proof is an
explicit Gaussian expectation calculation for a trigonometric polynomial.
The sources below delimit the surrounding theory and prevent the local
calculation from being described as a new general Remez or heat-observability
principle.  The bounded search found no exact collision; that is not evidence
of novelty or priority.

## Primary evidence

### General measurable-set heat observation

Gengsheng Wang, Ming Wang, Can Zhang, and Yubiao Zhang characterize
observable subsets for the heat equation on Euclidean space through
thickness and relate observability, interpolation, and spectral
inequalities.  Their observation sets and global `L^2` framework are
different from the signed collar functional and central `L^3` proxy used in
G.

- *Observable set, observability, interpolation inequality and spectral
  inequality for the heat equation in R^n*, 2017 author preprint,
  <https://arxiv.org/abs/1711.04279>.

Michela Egidi and Ivan Veselic give a sharp thickness condition and explicit
control-cost dependence on Euclidean domains and cubes.  This is adjacent
evidence for the role of observation geometry, not a source for G.8.

- *Sharp geometric condition for null-controllability of the heat equation
  on R^d and consistent estimates on the control cost*, 2018 author
  preprint, <https://arxiv.org/abs/1711.06088>.

### Small-time cost and geometry

Luc Miller proves lower geometric bounds for the exponential small-time
null-control cost, including a distance-squared lower bound.  R0.76G uses a
fixed scaled time and an explicit high-vanishing-order packet, so Miller's
theorem is context rather than an imported step.

- *Geometric bounds on the growth rate of null-controllability cost for the
  heat equation in small time*, Journal of Differential Equations 204
  (2004), 202--226, author preprint
  <https://arxiv.org/abs/math/0307158>, DOI
  <https://doi.org/10.1016/j.jde.2004.05.007>.

Camille Laurent and Matthieu Leautaud show that heat observability constants
can reflect eigenfunction vanishing and more geometry than a naive maximal
distance law.  Their results reinforce the need to keep the explicit packet
and the exact observation geometry separate from a general control claim.

- *Observability of the heat equation, geometric constants in control
  theory, and a conjecture of Luc Miller*, Analysis & PDE 14 (2021),
  355--423, <https://arxiv.org/abs/1806.00969>, DOI
  <https://doi.org/10.2140/apde.2021.14.355>.

### Exponential-polynomial boundary inherited from R0.76F

F. L. Nazarov's measurable Turan--Nazarov inequality and sharp Remez results
already establish exponential-order propagation costs for general finite
exponential or trigonometric polynomials.  R0.76F records the exact sources
and restricts the obstruction to the project's real dyadic fibres.
R0.76G goes in a different direction: it evolves one explicit packet under
the heat equation and retains the signed complete-clock integral.

- F. L. Nazarov, *Local estimates for exponential polynomials and their
  applications to inequalities of the uncertainty principle type*,
  Algebra i Analiz 5:4 (1993), 3--66; official bibliographic record
  <https://www.mathnet.ru/eng/aa397>.
- S. Tikhonov and P. Yuditskii, *Sharp Remez Inequality*, Constructive
  Approximation 52 (2020), 491--507,
  <https://arxiv.org/abs/1809.09726>, DOI
  <https://doi.org/10.1007/s00365-019-09473-2>.

## Claim-to-source ledger

| claim | source support | use in R0.76G |
|---|---|---|
| Heat observability on Euclidean space is tied to thickness and spectral inequalities. | Wang--Wang--Zhang--Zhang; Egidi--Veselic | Context only; no theorem imported. |
| Small-time heat observation has exponential geometric cost. | Miller 2004 | Context only. |
| Vanishing structure can alter geometric heat-observability constants. | Laurent--Leautaud 2021 | Context and caution against a naive generalization. |
| Exponential order is expected for finite exponential-polynomial observation. | Nazarov; Tikhonov--Yuditskii | Inherited literature boundary from F. |
| G.8 itself follows from the listed literature. | None | Explicitly false; G.8 is proved locally by G.20--G.34. |

## Search record and stop rule

The search covered primary records for heat observability on measurable and
thick sets, explicit small-time control cost, geometric lower bounds, and
Remez or Turan propagation.  A second targeted pass checked moving or local
heat observation and one-dimensional small-time estimates.  Those results
use different observation functionals and do not close or contradict G.8.
The search stopped because the remaining proof is elementary and
source-independent, and further broad control-theory searches were unlikely
to change its validity or its narrow boundary.

The Deep Research planning helper required by the selected skill was not
available in this environment.  Scope, evidence classes, follow-up search,
claim ledger, and stopping reason are recorded here instead.

No completeness, novelty, or priority claim is made.  The full physical
plateau estimate, arbitrary fields, Version-M transfer, regularity, and
singularity remain open.  **NOT CLAY.**
