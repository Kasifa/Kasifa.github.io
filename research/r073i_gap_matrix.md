# R0.73I gap matrix

**Status:** source stage; no public release has been declared  
**Parent:** R0.73H

| ID | Claim | Current state | Required evidence |
|---|---|---|---|
| I0 | `inheritedEndpointStrictlyBelowOneOver450` | CLOSED | R0.73F constants and the R0.73H exact \(H_0\) certificate give \(D=d_0<\sqrt{19/180}/392<1/450\); \(d_0\) remains a noncanonical shrinkable choice |
| I1 | `improvedContinuumUpperAction` | CLOSED | \(G_\varepsilon(D)\le\exp(\Omega_H(D)/\varepsilon-D/4)\) on \(0\le D\le1/450\), with exact \(\Omega_H\) from the \(\gamma=1/2\) numerical form |
| I2 | `zeroWindowTangentAction` | CLOSED | on the complete frozen top block, the minimum and maximum logarithmic gains both have iterated \(D\downarrow0\) tangent rate \(a\) |
| I3 | `fixedWindowActionFromInheritedInputs` | FALSE AS INFERENCE | exact finite-dimensional counterexamples satisfy the inherited abstract structure while producing launch-dependent actions or polynomial prefactors |
| I4 | `theoremEndpointEqualsOneOver450` | FALSE AS INFERENCE | the inherited endpoint is strictly \(d_0<1/450\), and the proof permits further shrinking |
| I5 | `actionLimitAloneGivesBoundedPrefactor` | FALSE AS INFERENCE | \(\Lambda^{-1}\log G_\Lambda\to\mathcal A\) permits unbounded subexponential factors |
| I6 | `finitePilotProvesContinuumAction` | FALSE AS INFERENCE | ordinary cutoff and time-step convergence do not enclose the infinite-dimensional tail |
| I7 | `finiteWkbProvesContinuumTwoTermLaw` | FALSE AS INFERENCE | finite agreement does not prove a continuum branch, a first viscous correction, or an adiabatic remainder |
| I8 | `canonicalSelectedBranch` | OPEN | validated rank-one, simple, unique rightmost inviscid branch with phase anchor |
| I9 | `explicitPositiveActionWindow` | OPEN | explicit \(D_*>0\), contour and rightmost real gap on \([0,D_*]\) |
| I10 | `uniformRankOneViscousBranch` | OPEN | uniform viscous contour, rank one, projection convergence and \(O(\varepsilon)\) eigenvalue error |
| I11 | `matchingSelectedGainAction` | OPEN | two-sided \(C_D^{\pm1}e^{\mathcal A(D)/\varepsilon}\) bound for the exact selected gain |
| I12 | `twoTermSelectedGainAsymptotic` | OPEN | first viscous eigenvalue correction, \(C^2\) branch and relative \(O(\varepsilon)\) complement control |
| I13 | `actionResolvedBackwardLocalization` | OPEN | interval version of the selected-orbit action bound |
| I14 | `prescribedActionSeedDeparture` | OPEN | R0.73H nonlinear hierarchy rerun with the action-resolved orbit and bounded prefactor |
| I15 | `coarseR073FRateIsSharp` | OPEN, NOT ASSUMED | a matching branch action would have to equal the coarse \(rD\); finite pilot suggests otherwise |
| I16 | `fixedBackgroundLyapunovInstability` | OPEN | one background and one topology with a genuine Lyapunov sequence |
| I17 | `transverseThreeDimensionalClosure` | OPEN | nonzero transverse row and nonlinear triad estimates |
| I18 | `finiteTimeSingularity` | OPEN | no evidence in this planar globally smooth family |
| I19 | `Clay` | OPEN | no global regularity proof or singularity construction |

## Finite pilot, not a certificate

At \(N=48\), binary64 Fourier compression gives

\[
 \mathcal A_N(1/450)
 \approx 3.7786035553\times10^{-4},
 \qquad
 \frac{\mathcal A_N(1/450)}{1/450}
 \approx0.17003715992.
\]

The average finite action crosses \(0.17035\) near
\(D\approx3.467410918\times10^{-4}\).  These values are route-selection
diagnostics only.  The run at \(1/450\) lies outside the inherited endpoint
\(D=d_0\), and it neither defines that shrinkable endpoint nor contradicts
the R0.73F theorem.

At the exact analytic upper bound
\(D_{\rm ub}=\sqrt{19/180}/392\), the same finite compression gives

\[
 \mathcal A_N(D_{\rm ub})\approx1.411208745974\times10^{-4},
 \qquad
 \mathcal A_N(D_{\rm ub})/D_{\rm ub}\approx0.1702694677404.
\]

This is labelled
`finite-route-diagnostic-at-analytic-upper-bound-not-theorem-endpoint`:
the actual inherited \(d_0\) is strictly smaller and is not uniquely fixed.

## Release rule

R0.73I may close as a negative audit of what R0.73F--H imply: I0--I2 must be
certified as exact positive statements, and I3--I7 must be sealed with their
precise `FALSE AS INFERENCE` scope.  I8--I15 then transfer unchanged to the
next spectral/adiabatic section.  No homepage, note index, recap endpoint,
version number, or public claim may advance from R0.73H until the exact
certificate, independent audit, finite-diagnostic boundary, formal figure,
bilingual publication, and release tests all pass.
