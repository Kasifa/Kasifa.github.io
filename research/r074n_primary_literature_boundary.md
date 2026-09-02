# R0.74N — bounded primary-source collision audit

## Scope and verdict

Search date: 2026-09-02.

The bounded screen asked whether a primary theorem directly supplies the
complete R0.74N statement

\[
 \sup_{\tau\in I_{R_j}}[\mathcal I_j(\tau)]_+
 \lesssim\Gamma_jL_jR_j^5
\]

for the calibrated periodic two-packet family, including the smooth
super-Gaussian annular sum, the endpoint-correlated inward bridge, and the
infinite lift-side outer tail.

**No direct theorem was found.**  Methodological precedents were found for
weighted Navier--Stokes energy estimates, local-energy aggregation,
shear-enhanced dissipation, Malliavin/Girsanov path methods, and stochastic
mixing.  None of the screened theorem statements contains the exact
family-dependent collar observable or its all-shell synthesis.

This was a bounded collision audit, not a systematic novelty search.  A
finite non-hit is not evidence of novelty, priority, or publishability.

## Primary-source ledger

### Weighted and local Navier--Stokes energy

1. Pedro Gabriel Fernández-Dalgo and Pierre Gilles Lemarié-Rieusset,
   [*Weak solutions for Navier--Stokes equations with initial data in
   weighted \(L^2\) spaces*](https://arxiv.org/abs/1906.11038).

   The paper develops weighted energy controls for whole-space weak
   solutions.  Its polynomial weights and existence objective do not give
   the present periodic super-Gaussian collar identity or a signed
   finite-window shell flux.

2. Pedro Gabriel Fernández-Dalgo and Pierre Gilles Lemarié-Rieusset,
   [*Weighted energy estimates for the incompressible Navier--Stokes
   equations and applications to axisymmetric solutions without
   swirl*](https://arxiv.org/abs/2010.00868).

   This is direct precedent for testing Navier--Stokes with spatial weights
   and controlling the derivative-of-weight terms.  It does not contain the
   R0.74F--H moving family, the endpoint-correlated bridge, or the annular
   weight \(\Gamma_k=e^{-4^{k-1}/32}\).

3. Zachary Bradshaw and Tai-Peng Tsai,
   [*Local energy solutions to the Navier--Stokes equations in Wiener
   amalgam spaces*](https://arxiv.org/abs/2008.09204).

   The paper aggregates local energy over distributed spatial regions.  Its
   amalgam framework is relevant context but does not state the signed
   radial collar trace or the familywise square-root-log saturation law.

4. Hi Jun Choe and Minsuk Yang,
   [*Local kinetic energy and singularities of the incompressible
   Navier--Stokes equations*](https://arxiv.org/abs/1705.04561).

   This source studies local kinetic-energy control and consequences for
   partial regularity.  It does not supply the exact smooth-shell flux bound
   proved here, and R0.74N does not invoke its regularity conclusions.

### Stochastic shear mechanisms

5. Jacob Bedrossian and Michele Coti Zelati,
   [*Enhanced dissipation, hypoellipticity, and anomalous small noise
   inviscid limits in shear flows*](https://arxiv.org/abs/1510.08098).

   The paper establishes quantitative enhanced dissipation and
   hypoellipticity for autonomous shear advection.  It controls semigroup
   decay rather than a signed annular trace for a time-dependent,
   \(j\)-dependent heat shear.

6. David Villringer,
   [*Enhanced Dissipation via the Malliavin
   Calculus*](https://arxiv.org/abs/2405.12787).

   Its covariance argument supports the general shear--Brownian mechanism,
   but its theorem is for a fixed autonomous profile and does not preserve
   the R0.74N endpoint collar correlation.

7. Victor Gardner, Kyle L. Liss, and Jonathan C. Mattingly,
   [*A pathwise approach to the enhanced dissipation of passive scalars
   advected by shear flows*](https://arxiv.org/abs/2410.05657).

   This is close methodological precedent for exceptional-path estimates.
   Its decay and total-variation conclusions do not directly imply the
   complete signed annular sum.

8. Kyle L. Liss and Kunhui Luan,
   [*Uniform-in-diffusivity mixing by shear flows: stochastic and dynamical
   perspectives*](https://arxiv.org/abs/2603.09238).

   Its stochastic representation and integration-by-parts proof are
   structurally related to the path methods used earlier in this route.
   The stated result concerns uniform-in-diffusivity mixing for parallel
   shear flows, not the exponentially flat calibrated family or the target
   \(\Gamma_jL_jR_j^5\) collar scale.

## Collision matrix

| Feature | Primary precedent found | Direct R0.74N theorem found |
|---|---:|---:|
| Weighted Navier--Stokes energy testing | Yes | No |
| Local-energy aggregation over spatial regions | Yes | No |
| Shear-enhanced dissipation and stochastic path methods | Yes | No |
| Smooth super-Gaussian dyadic collar sum | No screened theorem | No |
| Common-forward endpoint-correlated bridge | No screened theorem | No |
| One positive chord for all inward shells | No screened theorem | No |
| Infinite Euclidean outer-lift tail at \(\Gamma_jLR^5\) | No screened theorem | No |
| Familywise square-root-log collar saturation | No screened theorem | No |

## Logical boundary

The weighted-energy papers do not verify the signs, shell constants, or
bridge estimates in R0.74N.  The enhanced-dissipation papers do not supply
the smooth annular test, the calibrated endpoint event, or the infinite
outer-shell ledger.  Conversely, R0.74N proves no semigroup decay theorem,
epsilon-regularity criterion, continuation result, or global existence
statement.

The analytic proof and its independent reconstruction must therefore carry
the full mathematical burden.  This literature file only records where
direct black-box import stops.  **NOT CLAY.**
