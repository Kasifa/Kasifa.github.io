# R0.75E primary-source boundary -- shear modes, streamline averages, and localized drift flux

**Audience:** analysts reviewing the R0.75E horizontal cross-mode reduction.

**Search date:** 2026-09-03.

## Scope and direct answer

This bounded primary-source screen asks whether existing work already
supplies the R0.75E conclusion needed here: an exact difference-frequency
formula for the transport flux through a fixed three-dimensional spherical
collar cutoff, normalized by the frozen Version-M payment, together with a
pure \(P^{2/3}\) all-payment closure for the real horizontal zero mode.

The closest literature establishes three neighboring facts:

1. shear advection preserves each streamwise Fourier mode;
2. the streamline average decouples and solves a one-dimensional diffusion
   equation;
3. local drift-diffusion energy estimates retain a boundary/cutoff drift
   flux whose control depends on the drift or boundary geometry.

No searched source states the R0.75E spherical-collar Fourier convolution,
its \(\Xi_{m-n}\) cutoff coefficient, or its Version-M \(P^{2/3}\) payment
normalization. This is a finite non-hit, not evidence of novelty or
priority. The E.6--E.24 formulas are locally derived and independently
audited rather than imported from these papers.

## Evidence reconciliation

### Streamwise modes and the zero mode

Siming He studies passive scalars under a shear \(u(y)\partial_x\). After
Fourier transform in the streamwise variable, the paper writes a separate
equation for each wave number \(k\); the coefficient \(iku(y)\) acts within
that mode rather than coupling different \(k\)'s. The same paper states that
data depending only on the transverse variable solve the heat equation and
do not exhibit shear-enhanced dissipation. This directly supports the
literature boundary behind E.9 and the qualitative distinction between the
zero and nonzero horizontal sectors. It does not address a fixed spherical
physical-space cutoff or the cross-mode terms created by multiplying by
that cutoff.

Gardner, Liss, and Mattingly likewise state that the average along a
streamline decouples and solves one-dimensional diffusion, while the
non-average part can decay faster by shear-enhanced dissipation. Their
pathwise results are local along streamlines and depend on the local shear
profile. That is a different locality from the R0.75E stationary spherical
collar: it does not remove the \(\partial_2\xi\,|F|^2\) flux and does not
produce the frozen payment exponent.

### Local drift flux

Albritton and Dong describe the basic localized energy mechanism for a
divergence-free drift. On a ball, the drift contribution becomes a boundary
term involving \(\theta^2 b\cdot n\), and their quantitative local theory
depends on drift integrability and slicing. This is consistent with R0.75E
retaining the signed cutoff flux rather than discarding it by global
skew-adjointness. Their theorems concern local boundedness, Harnack
inequalities, and fundamental-solution bounds under drift hypotheses; they
do not imply the specific \((P_R^M)^{2/3}\) bound.

## Claim-to-source ledger

| Claim supported | Primary source | Date/version | URL | Access note |
|---|---|---|---|---|
| A shear \(u(y)\partial_x\) yields a separate equation for each streamwise Fourier mode; transverse-only data solve diffusion without enhanced dissipation | Siming He, *Enhanced dissipation, hypoellipticity for passive scalar equations with fractional dissipation* | arXiv:2103.07906v2, revised 2021-10-22 | https://arxiv.org/abs/2103.07906 | arXiv abstract and HTML equations 1.8--1.9 inspected 2026-09-03 |
| The streamline average decouples and solves one-dimensional diffusion; non-average decay is governed by shear across streamlines | Victor Gardner, Kyle L. Liss, Jonathan C. Mattingly, *A pathwise approach to the enhanced dissipation of passive scalars advected by shear flows* | arXiv:2410.05657v1, submitted 2024-10-08 | https://arxiv.org/abs/2410.05657 | arXiv abstract and HTML equations 1.4--1.5 inspected 2026-09-03 |
| A localized drift energy calculation retains a boundary flux and quantitative control depends on the drift/local geometry | Dallas Albritton, Hongjie Dong, *Regularity properties of passive scalars with rough divergence-free drifts* | arXiv:2107.12511v1, submitted 2021-07-26 | https://arxiv.org/abs/2107.12511 | arXiv HTML discussion and equation 1.6 inspected 2026-09-03 |

## Gap matrix

| Question | Evidence status | Consequence |
|---|---|---|
| Does the shear preserve horizontal modes? | Established in primary literature and rederived locally | E.9 is standard structure, not a novelty claim |
| Does the horizontal average decouple? | Established in primary literature and rederived locally | Supports the zero-mode route, but not its collar payment by itself |
| Does physical localization retain drift flux? | Established in local energy literature | Global modal orthogonality cannot simply delete the collar flux |
| Is the exact \(\Xi_{m-n}\) convolution already stated for this collar/payment? | Not found in the bounded search | Treat E.10 as a local algebraic identity; make no priority claim |
| Does existing enhanced dissipation imply E.24? | No matching theorem found | Arbitrary real cross-mode aggregation remains open |

## Search boundary and stopping rule

Searches covered arXiv primary papers on passive scalar shear Fourier modes,
streamline averages, enhanced dissipation, and localized drift-diffusion
energy. Follow-up inspection reached the mode equations, streamline-average
equations, and local drift boundary term. The search stopped when the three
method families converged on the same boundary: they support the surrounding
mechanisms but not the frozen spherical-collar payment theorem. Additional
broad search was unlikely to change the immediate proof decision.

**Literature-established:** modal invariance under a shear independent of
the streamwise coordinate, heat evolution of the streamline average, and
the survival of drift flux under physical localization.

**Locally proved:** R0.75E E.6--E.23 and the real zero-mode implication E.2.

**Open:** E.24 for arbitrary real passive fields, complete-clock extraction,
suitable-weak transfer, fixed deletion, and all Navier--Stokes regularity or
singularity conclusions. **NOT CLAY.**
