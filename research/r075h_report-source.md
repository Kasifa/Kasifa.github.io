# R0.75H primary-source boundary -- moving tubes, pathwise diffusion, and localized drift

**Audience:** analysts reviewing the R0.75H pure-transport terminal-tube theorem.

**Search date:** 2026-09-03.

## Scope and direct answer

R0.75H is an elementary local theorem for a pure transport equation. Its
characteristic formula, endpoint identity, spacetime Hölder step, and
frozen exponent are proved in the note rather than imported from a paper.
The source question is whether neighboring literature already converts
that benchmark into the required diffusive spherical-collar estimate.

The inspected primary sources show that moving observation geometry,
stochastic trajectories, and localized drift flux all support serious
quantitative theories. None gives the R0.75H terminal-tube cubic estimate
for the frozen Version-M functional, and none removes the target
dissipation from the right side of H.28. The diffusive extension therefore
remains open. This is a finite non-hit, not evidence of novelty or priority.

## Evidence reconciliation

### Moving observation supports

Alphonse and Martin characterize approximate null controllability with
uniform cost for hypoelliptic Ornstein--Uhlenbeck equations using an
integral-thickness condition on moving control supports, and obtain
quantitative weak observability estimates. This confirms that the
space-time sweep of a moving set can be the correct geometric object for a
parabolic problem. Their result is an observability/control theorem on
Euclidean space, not an upper bound for a signed spherical-collar flux in
terms of a local cubic payment. It cannot be substituted for H.23 or E.24.

### Pathwise diffusive shear analysis

Gardner, Liss, and Mattingly study the stochastic differential equation
associated with shear drift diffusion. Their use of Girsanov's theorem and
local-in-space shear estimates shows that a diffusive trajectory method can
add information beyond deterministic characteristics. The result concerns
enhanced dissipation along streamlines; it does not provide the terminal-
tube inclusion H.7 for Brownian paths or a separately paid source row for
the frozen collar.

### Bounded total speed and local drift flux

Albritton and Dong identify `L^1_t L^infinity_x`, the bounded-total-speed
class, as a borderline drift regime in their local passive-scalar theory
and construct transport-based sharpness examples. Their localized energy
framework retains drift flux and depends quantitatively on the drift and
geometry. This reinforces the H.28 boundary: diffusion and transport
cannot be separated by simply deleting the local flux. Their theorems do
not imply the `R^(1/3)` cubic-payment gain.

## Claim-to-source ledger

| Claim supported | Primary source | Date/version | URL | Access note |
|---|---|---|---|---|
| Moving control supports for non-autonomous parabolic/hypoelliptic equations are governed by quantitative integral-thickness geometry | Paul Alphonse, Jérémy Martin, *Approximate null-controllability with uniform cost for the hypoelliptic Ornstein-Uhlenbeck equations* | arXiv:2201.01516v3, revised 2023-02-06 | https://arxiv.org/abs/2201.01516 | arXiv abstract inspected 2026-09-03; URL accessible |
| A stochastic pathwise/Girsanov method yields local-in-space enhanced-dissipation estimates from shear across streamlines | Victor Gardner, Kyle L. Liss, Jonathan C. Mattingly, *A pathwise approach to the enhanced dissipation of passive scalars advected by shear flows* | arXiv:2410.05657v1, submitted 2024-10-08 | https://arxiv.org/abs/2410.05657 | arXiv abstract inspected 2026-09-03; URL accessible |
| Bounded total drift speed is borderline in local passive-scalar theory; localization retains quantitative drift dependence | Dallas Albritton, Hongjie Dong, *Regularity properties of passive scalars with rough divergence-free drifts* | arXiv:2107.12511v1, submitted 2021-07-26 | https://arxiv.org/abs/2107.12511 | arXiv abstract and local-flux discussion inspected 2026-09-03; URL accessible |

## Gap matrix

| Question | Evidence status | Consequence |
|---|---|---|
| Is the pure-transport endpoint identity standard characteristic algebra? | Yes; rederived locally | H.11--H.15 is not a novelty claim |
| Can moving geometry yield quantitative parabolic observability? | Yes in a neighboring control setting | Moving tubes are credible objects, but the estimate direction and norm differ |
| Can stochastic trajectories add diffusive shear information? | Yes in enhanced-dissipation theory | A Feynman--Kac/Girsanov extension is plausible but still requires the frozen payment ledger |
| Does local drift diffusion retain a flux/drift cost? | Yes | H.28 cannot be simplified by global skew-adjointness |
| Does an inspected theorem prove H.23 for diffusion or E.24? | No matching theorem found | The terminal-tube benchmark does not close the actual passive row |

## Search boundary and stopping rule

The bounded search covered primary arXiv work on moving observation
supports, pathwise shear diffusion, and localized passive scalars with
rough divergence-free drift. These are the three method families directly
adjacent to the H.29 continuation. Search stopped after their theorem
directions and geometry were reconciled with the frozen target; none
contained the missing cubic collar/payment estimate.

**Literature-established:** moving-support geometry can govern parabolic
observability, stochastic shear trajectories can yield local enhanced
dissipation, and localized drift theory retains quantitative flux costs.

**Locally proved:** H.11--H.26 for the pure-transport benchmark.

**Open:** an independently paid diffusive terminal-tube or resolvent
estimate, every positive gain for the arbitrary frozen passive field,
E.24, complete-clock extraction, fixed deletion, suitable-weak transfer,
and all regularity or singularity conclusions. **NOT CLAY.**
