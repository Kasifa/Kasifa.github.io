# R0.75G primary-source boundary -- quantitative mixing input and the local gain threshold

**Audience:** analysts reviewing the R0.75G signed-flux gain threshold.

**Search date:** 2026-09-03.

## Scope and direct answer

R0.75G does not import a published exponent. Its critical values

\[
 \alpha_* = \frac{27163}{107163},\qquad
 \beta_* = \frac{27163}{35721}
\]

are exact consequences of the frozen local definitions of `R`, `omega`,
and the common-shear cubic atom. The literature question is narrower: do
existing shear-flow methods show what kind of information could supply a
positive correlation or residence-time gain beyond absolute Hölder?

The inspected primary sources exhibit resolvent, pathwise stochastic, and
localized drift-flux mechanisms. None states the R0.75G estimate (G.1), the
`R^(1/3)` target (G.24), or a Version-M spherical-collar theorem. The
source screen therefore supports route classification only. It supplies no
proof of the new gain and no novelty or priority conclusion.

## Evidence reconciliation

### Resolvent and semigroup input

Siming He separates streamwise Fourier modes for a shear passive scalar
and obtains enhanced decay of nonzero modes through resolvent estimates
and semigroup control. Such estimates add quantitative coercivity absent
from a bare energy identity, so they belong to the class of inputs that
could in principle affect the correlation ratio in G.17. The paper does
not localize to the fixed three-dimensional collar or compare its result
with the frozen cubic payment.

### Pathwise and local-shear input

Gardner, Liss, and Mattingly use a pathwise stochastic representation and
local shear structure to quantify enhanced dissipation. This is the
closest inspected method family to the residence interpretation in
G.18--G.20: trajectory information can be stronger than full-window
absolute Hölder. Their estimates follow streamlines and local shear
profiles; they do not prove an interaction atom with
`p_b^int <= C R^beta p_b` for the stationary spherical collar.

### Local drift flux

Albritton and Dong retain the drift boundary contribution in localized
energy estimates for passive scalars with divergence-free drift. This
supports the requirement that the R0.75G proof continue to control the
signed physical-space flux rather than delete it using global
skew-adjointness. Their local theory uses drift integrability and geometric
slicing but does not provide the frozen gain exponent.

## Claim-to-source ledger

| Claim supported | Primary source | Date/version | URL | Access note |
|---|---|---|---|---|
| Enhanced decay of nonzero shear modes uses resolvent/semigroup information beyond modal energy algebra | Siming He, *Enhanced dissipation, hypoellipticity for passive scalar equations with fractional dissipation* | arXiv:2103.07906v2, revised 2021-10-22 | https://arxiv.org/abs/2103.07906 | arXiv abstract and HTML equations 1.8--1.9 inspected 2026-09-03; URL rechecked HTTP 200 |
| Pathwise stochastic estimates exploit local shear and trajectory separation; the streamline average decouples | Victor Gardner, Kyle L. Liss, Jonathan C. Mattingly, *A pathwise approach to the enhanced dissipation of passive scalars advected by shear flows* | arXiv:2410.05657v1, submitted 2024-10-08 | https://arxiv.org/abs/2410.05657 | arXiv abstract and HTML equations 1.4--1.5 inspected 2026-09-03; URL rechecked HTTP 200 |
| Physical localization retains a drift boundary flux and requires quantitative drift/geometric control | Dallas Albritton, Hongjie Dong, *Regularity properties of passive scalars with rough divergence-free drifts* | arXiv:2107.12511v1, submitted 2021-07-26 | https://arxiv.org/abs/2107.12511 | arXiv HTML discussion and equation 1.6 inspected 2026-09-03; URL rechecked HTTP 200 |

## Gap matrix

| Question | Evidence status | Consequence |
|---|---|---|
| Is the value of `alpha_*` literature-derived? | No; it is frozen local exponent arithmetic | Treat G.2 as a local conditional theorem, not a cited universal threshold |
| Can resolvent estimates add information absent from F.17? | Yes in neighboring shear problems | The resolvent route remains viable but requires a collar/payment theorem |
| Can pathwise analysis encode residence or mixing? | Yes in neighboring shear problems | It motivates G.18 but does not prove its interaction atom |
| Does localization retain the drift flux? | Yes in primary local drift theory | The signed collar term must remain visible in any proof |
| Does any inspected source prove G.24 or E.24? | No matching theorem found | The positive gain and arbitrary-real closure remain open |

## Search boundary and stopping rule

The source set is inherited from the immediately preceding bounded screen
and was rechecked at the three primary URLs. It covers the three method
families actually distinguished by G: resolvent/semigroup coercivity,
pathwise trajectory information, and localized drift flux. No broader
search was used to turn the finite non-hit into a literature-completeness
claim.

**Literature-established:** enhanced-dissipation mechanisms can use
resolvent or pathwise information beyond energy algebra, and drift flux
survives physical localization.

**Locally proved:** G.2--G.4, G.9--G.19, and the pure-transport benchmark
G.22--G.23.

**Open:** every positive gain in G.1 for the arbitrary real frozen family,
the interaction atom G.18, G.24, E.24, complete-clock extraction, fixed
deletion, suitable-weak transfer, and all regularity or singularity
conclusions. **NOT CLAY.**
