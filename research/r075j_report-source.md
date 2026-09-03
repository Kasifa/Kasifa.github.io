# R0.75J primary-source boundary -- adjoint positivity and drift diffusion

**Audience:** analysts reviewing the R0.75J mean-zero adjoint obstruction.  
**Date:** 2026-09-03.  
**Scope:** passive advection--diffusion, heat-semigroup/adjoint positivity,
and signed collar sources.  
**Exclusion:** no complete-clock, regularity, novelty, or priority claim.

## Direct answer

The R0.75J theorem is derived locally from the passive square equation,
periodic integration by parts, and the mean-zero property of a derivative
source.  The literature supports using heat kernels, Davies perturbations,
and stochastic/pathwise representations for drift diffusion, but none of
the inspected sources supplies a nonnegative majorant whose boundary row is
paid by the frozen Version-M functional.

The exact signed adjoint solution and a positive Feynman--Kac majorant are
different objects.  The first retains cancellation but is forced to change
sign; the second can be nonnegative after replacing the source by a
majorant such as `a_+`, but then its initial occupation row requires a new
estimate.  The bounded search supports that architectural distinction and
does not establish novelty.

## Evidence used and boundary

### Passive scalars with divergence-free drift

Albritton and Dong study the same general operator
`partial_t-Delta+b dot grad`, prove local estimates and fundamental-solution
bounds under stated drift hypotheses, and single out bounded total speed as
a borderline class.  Their theory confirms that localization with drift
retains quantitative coefficient/geometry costs.  It does not prove the
frozen positive-majorant payment J.20.

### Pathwise shear diffusion

Gardner, Liss, and Mattingly develop a pathwise approach to passive scalars
advected by shear and use stochastic changes of measure in their enhanced-
dissipation analysis.  This supports Feynman--Kac/Girsanov methods as a real
source of information beyond the modal energy identity.  Their result is
not the spherical-collar signed-flux estimate and is not imported as one.

### Davies weighted-semigroup method

Hu and Li use Davies' exponential perturbation method to obtain
off-diagonal heat-kernel upper bounds in a regular Dirichlet-form setting.
This supports the use of positive semigroup majorants for spatial leakage.
The setting and conclusion do not provide the Version-M boundary-row
payment required by J.20.

## Claim-to-source ledger

| claim checked | primary source | date / identifier | URL | access and boundary |
|---|---|---|---|---|
| Divergence-free passive drift diffusion has local boundedness, Harnack, and fundamental-solution estimates in the paper's stated classes; bounded total speed is a special borderline regime | Dallas Albritton and Hongjie Dong, *Regularity properties of passive scalars with rough divergence-free drifts* | submitted 2021-07-26, arXiv:2107.12511 | https://arxiv.org/abs/2107.12511 | Abstract and relevant article sections inspected 2026-09-03; no J.20 or E.24 conclusion |
| Pathwise stochastic methods add genuine shear-diffusion information beyond formal energy identities | Victor Gardner, Kyle L. Liss, and Jonathan C. Mattingly, *A pathwise approach to the enhanced dissipation of passive scalars advected by shear flows* | submitted 2024-10-08, arXiv:2410.05657 | https://arxiv.org/abs/2410.05657 | Abstract and modal/pathwise setup inspected 2026-09-03; different geometry and target |
| Davies perturbation yields off-diagonal upper bounds for heat kernels under the paper's Dirichlet-form assumptions | Jiaxin Hu and Xuliang Li, *The Davies method revisited for heat kernel upper bounds of regular Dirichlet forms on metric measure spaces* | submitted 2016-05-18, revised 2017-04-05, arXiv:1605.05548v4 | https://arxiv.org/abs/1605.05548 | Abstract and off-diagonal section inspected 2026-09-03; not substituted for the nonsymmetric frozen payment problem |

## Gap matrix

| question | evidence | R0.75J conclusion |
|---|---|---|
| Can the exact zero-terminal adjoint of the signed derivative source be nonnegative? | Local proof J.7--J.9 | No, unless the source is identically zero |
| Does a constant shift create a free positive adjoint test? | Local proof J.14--J.18 | No; it cancels exactly or incurs the global energy-drop row |
| Can a positive majorant still work? | Local proof J.19--J.20; semigroup literature | Yes as an architecture, but its initial row is unproved |
| Does an inspected source pay that initial row by Version-M? | Bounded primary-source search | No matching theorem found |
| Is E.24 closed? | Main theorem boundary | No |

## Search record and stopping rule

The search reused the verified primary sources already identified for
R0.75F--I and followed the exact terms `adjoint`, `Feynman--Kac`,
`Davies`, `off-diagonal`, `bounded total speed`, and `shear diffusion`.
The search stopped after the relevant mechanism classes and their limits
were established: the new obstruction is an elementary local identity,
and additional generic heat-kernel sources would not prove the missing
Version-M boundary payment.

## Frozen conclusion

**Established locally:** exact inversion of the nonzero mean-zero signed
source forces a sign-changing adjoint; constant positivity shifts are
neutral in the exact identity and costly after dropping dissipation.

**Viable but open:** a nonnegative adjoint majorant with an independently
paid initial occupation/source row.

**Open:** the required payment, positive `R^alpha` gain, transition and
periodic geometry, E.24, complete clock, fixed deletion, suitable-weak
transfer, regularity, and singularity. **NOT CLAY.**
