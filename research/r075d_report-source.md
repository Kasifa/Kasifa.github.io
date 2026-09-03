# R0.75D primary-source boundary -- localized passive dissipation under a large shear

**Audience:** analysts reviewing the R0.75D outer-padding route.

**Search date:** 2026-09-03.
**Scope:** primary sources on localized energy estimates for
advection--diffusion, weighted Navier--Stokes energy, and shear-enhanced
dissipation. The question is whether an existing theorem directly supplies

\[
 D_{k,R}^{{\rm out},F}\lesssim(P_R^M)^{2/3}
\]

for the frozen time-dependent common shear, physical spherical collar,
dyadic weight, and scale-
\(2R\) cubic payment. This is a bounded collision screen, not an exhaustive
priority search.

## Direct answer

No directly matching theorem was found in the bounded primary-source
screen. The closest sources validate three methodological facts already
visible in the exact R0.75D algebra:

1. a divergence-free drift becomes a boundary/cutoff flux in a localized
   \(L^2\) estimate;
2. quantitative local estimates generally retain dependence on a drift
   norm or on the drift profile; and
3. shear-specific localization is possible, but available enhanced-
   dissipation theorems measure streamline decay rather than the R0.75D
   weighted physical-collar gradient integral.

Accordingly, these sources support the claim boundary around (D.19)--
(D.23), but none proves the open pure-\(2/3\) interaction estimate.

## Source-by-source comparison

### 1. Albritton--Dong: localized drift flux and bounded total speed

Dallas Albritton and Hongjie Dong study
\(\partial_t\theta-\Delta\theta+b\cdot\nabla\theta=0\) with a
divergence-free drift. Their introductory energy computation rewrites the
localized transport contribution as
\(-\int\theta^2(b\cdot\nabla\phi)\phi\), exactly the structural cutoff
flux used in R0.75D. They prove local boundedness and single-scale Harnack
results under explicit mixed-norm hypotheses and treat
\(L_t^1L_x^\infty\), ``bounded total speed'', as a borderline case. Their
constants retain drift information; the result is not a drift-independent
physical-collar dissipation bound.

At the collar thickness \(R\), the relevant dimensionless displacement is

\[
 R^{-1}\int_{I_{2R}}\|b(t)\|_\infty\,dt
 \asymp R^{-1},
\]

because \(B\asymp R^{-2}\) and \(|I_{2R}|\asymp R^2\). Thus their
bounded-total-speed mechanism cannot be inserted at the fixed \(R\)-thick
collar with a uniform constant merely because the unscaled total
displacement is \(O(1)\). It instead points toward a co-moving or sliced
domain, whose comparison with the stationary weighted collar remains to
be proved.

Primary source: D. Albritton and H. Dong,
[*Regularity properties of passive scalars with rough divergence-free
drifts*](https://arxiv.org/abs/2107.12511), arXiv:2107.12511 (submitted
2021-07-26), especially the localized transport computation (1.3),
Theorems 1.1--1.2, and Section 3.

### 2. Fernandez-Dalgo--Lemarie-Rieusset: weighted energy keeps the drift row

Pedro Gabriel Fernandez-Dalgo and Pierre Gilles Lemarie-Rieusset prove
weighted energy controls for an advection--diffusion problem with
divergence-free drift in weighted \(L^2\) spaces. Their displayed energy
balance retains
\(\int |u|^2 b\cdot\nabla w\), and their closed a priori estimate depends
on a weighted \(L^3\) norm of the drift. This is directly consistent with
the R0.75D mixed term
\(p_b^{1/3}p_F^{2/3}\): an absolute-value estimate does not erase the
drift factor.

Their weights are polynomial Muckenhoupt weights on \(\mathbb R^3\), and
their conclusion is a global weighted-energy/existence estimate. It does
not state the periodic dyadic-collar inequality (D.1), the outer-padding
weight mismatch, or the payment interaction (D.23).

Primary source: P. G. Fernandez-Dalgo and P. G. Lemarie-Rieusset,
[*Weak solutions for Navier--Stokes equations with initial data in weighted
L2 spaces*](https://arxiv.org/abs/1906.11038), arXiv:1906.11038 (submitted
2019-06-26; published in *Archive for Rational Mechanics and Analysis*),
especially Theorem 2 and its weighted advection--diffusion energy controls.

### 3. Gardner--Liss--Mattingly: local-in-streamline shear information

Victor Gardner, Kyle Liss, and Jonathan Mattingly give a pathwise treatment
of enhanced dissipation for passive scalars advected by shear flows. Their
method yields decay rates localized along streamlines and makes the rate
depend on the local shear differential. This supports the R0.75D decision
that a successful improvement over absolute Hölder must use shear dynamics
or spatial separation.

The theorem is nevertheless not a substitute for (D.1). It concerns
decay toward the streamline average for autonomous shears (with a
viscosity parameter), not the time-dependent heat-evolved frozen shear,
a stationary spherical collar of thickness \(R\), the local
\(\int|\nabla F|^2\) clock, or payment by \(P_R^M\). Its own localization
also records leakage of mass away from a streamline, which is parallel to,
rather than a solution of, the periodic-weight leakage in Section 5 of
R0.75D.

Primary source: V. Gardner, K. L. Liss, and J. C. Mattingly,
[*A pathwise approach to the enhanced dissipation of passive scalars
advected by shear flows*](https://arxiv.org/abs/2410.05657),
arXiv:2410.05657 (submitted 2024-10-08), especially Theorems 1--2 and the
local enhanced-dissipation discussion in Section 2.

## Claim-to-source ledger

| claim used in R0.75D boundary | primary support | confidence | unresolved difference |
|---|---|---:|---|
| localized divergence-free transport produces a cutoff flux | Albritton--Dong, (1.3) | high | no R0.75D payment weights |
| quantitative localization retains drift size/profile information | Albritton--Dong, Theorems 1.1--1.2 and Section 3 | high | their target is boundedness/Harnack, not collar dissipation |
| weighted energy retains the \(|u|^2b\cdot\nabla w\) row | Fernandez-Dalgo--Lemarie-Rieusset, Theorem 2 | high | polynomial whole-space weight, not dyadic periodic shells |
| shear dynamics can yield local streamline-dependent decay | Gardner--Liss--Mattingly, Theorem 2 | high | autonomous shear and semigroup decay, not (D.1) |
| an existing theorem proves (D.23) uniformly | none found | no support | remains OPEN |

## Search limitation and stopping rule

The search used exact combinations of ``advection diffusion'',
``divergence-free drift'', ``local energy/Caccioppoli'', ``bounded total
speed'', ``shear'', ``localized'', and ``enhanced dissipation'', then read
the closest primary papers at theorem/equation level. The search stopped
when the three relevant method families converged on the same boundary and
no result matched the physical collar, time-dependent shear, dyadic
payment, and pure \(2/3\) exponent simultaneously. A finite non-hit is not
evidence of novelty or priority.

**Literature-established:** the general cutoff-flux mechanism, drift-norm
dependence in local estimates, and streamline-sensitive enhanced
dissipation.

**Locally proved:** R0.75D (D.16)--(D.22).

**Open:** (D.23), B.45, complete-clock extraction, suitable-weak transfer,
and every regularity or singularity conclusion. **NOT CLAY.**
