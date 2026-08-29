# R0.73C gap matrix

**Date:** 2026-08-30  
**Purpose:** bind every public claim to its exact evidence class and prevent
the frozen Rayleigh result from being overextended.

| ID | statement | state | evidence | next falsification or proof gate |
|---|---|---|---|---|
| C1 | exact lift-up lower bound is linear in \(|\Lambda|\) | inherited CLOSED | R0.73B component solution | none in R0.73C |
| C2 | complete physical-kinetic upper is at most \(e^{5|\Lambda|/16}\) from \(s=0\) | inherited CLOSED | R0.73B energy identity | sharpen only after stable/unstable decomposition |
| C3 | cubic collision level has \(\gamma_0=\sqrt7/2\) and a unique negative singular threshold \(-7/4\) | CLOSED | exact periodic Sobolev mode and Pöschl--Teller spectrum | independent symbolic/Fourier recomputation |
| C4 | \(A_{1/2}(0)\) has a positive real eigenvalue in \((0.17035,0.17050)\) | CLOSED | infinite-dimensional periodic-ODE monodromy sign certificate | independent partition/order run plus finite Fourier diagnostic |
| C4a | the unstable root is unique in the bracket | OPEN | not required by sign change | interval derivative or argument count |
| C4b | every \(0<\gamma<\sqrt7/2\) is unstable | OPEN | not implied by the one-row certificate | singular branch/global index theorem |
| C5 | frozen instability transfers to the nonautonomous viscous generator on \(M\log|\Lambda|\) fast time | OPEN | conditional lemma only | vanishing-viscosity eigenvalue, Riesz, dichotomy, graph-domain package |
| C6 | every fixed-degree complete-row polynomial upper fails | CONDITIONAL on C5 | exact quantified implication after C5 | prove C5 for all sufficiently large \(|\Lambda|\), not only a sequence |
| C7 | fixed-window gain is \(e^{\Theta(|\Lambda|)}\) | OPEN | no lower rate on an \(O(1)\) physical window | adiabatic/dichotomy and matching upper/lower rates |
| C8 | a spectrally stable projected class has a polynomial bound | OPEN | no projection/resolvent theorem | freeze projection and uniform resolvent |
| C9 | complete Orr--Sommerfeld--Squire \(A_2\) direct sum | OPEN | one two-dimensional row only | pressure/Squire collision-scale closure |
| C10 | nonlinear Navier--Stokes or Clay implication | OPEN | no nonlinear frequency closure or global estimate | independent nonlinear theorem required |

## Evidence taxonomy

- **Exact theorem:** C3 and the algebraic monodromy reductions.
- **Validated infinite-dimensional computation:** C4 endpoint signs; no
  Fourier truncation appears in its proof.
- **Finite diagnostic:** Galerkin eigenvalue
  \(0.170407976920434\), residuals, sampled Fredholm contour.
- **Conditional theorem:** logarithmic fast-time lower bound under H1--H4.
- **Open problem:** C5--C10 as marked above.

## Release rule

The public note may say `infiniteDimensionalFrozenRayleighInstability=CLOSED`.
It must also place `frozenInstabilityFastTimeTransfer=OPEN` and
`superPolynomialCompleteRowNoGo=CONDITIONAL` in the same direct-decision
block.  No finite contour sampling may be described as an interval Riesz
certificate, and no one-row linear statement may be presented as a
three-dimensional nonlinear result.

