# R0.73V primary-literature audit: signed third moments and the next-level boundary

**Audit date:** 2026-09-01

**Status:** two bounded primary-source search waves complete; formula and
index readback remain part of the analytic gate

**Ordinary translation path:** `LOCAL_DIRECT_NO_DGX`

## 1. Direct classical collision: Germano's generalized moments

Massimo Germano treated a general linear, constant-preserving filter that
commutes with space and time derivatives:

- M. Germano, *Turbulence: the filtering approach*, Journal of Fluid
  Mechanics 238 (1992), 325--336,
  [DOI](https://doi.org/10.1017/S0022112092001733),
  [primary PDF](https://gibbs.science/teaching/les/handouts/germano_1992.pdf).

Equations (22)--(25) give the exact generalized-central-moment equations.  The
second velocity cumulant is transported by the filtered velocity and couples
to the third velocity cumulant, pressure--velocity cumulants,
pressure--strain, gradient covariance, and lower-order production.  The
algebraic structure is the same as the Reynolds hierarchy.  This is the
closest classical source for R0.73V.

The consequence is decisive but narrow.  A local third velocity cumulant by
itself is not the complete list of terms in the exact tensor-stress equation.
The pressure rows must be retained, or replaced by an exactly equivalent
nonlocal Leray/Riesz cubic lift.  Germano does not provide the heat-parameter
PDE derived in R0.73V, a single-scale constitutive closure, or a theorem of
componentwise minimality.

Germano's contracted equation (25) is the generalized turbulent-energy
equation.  In that trace, pressure--strain vanishes by incompressibility and
pressure remains inside a third-order flux.  R0.73V's trace equation is a
heat-filter specialization of this classical identity; only its stated
\(L_t^{4/3}L_x^2\) conditional norm bookkeeping is a local corollary.

R0.73V also uses an equivalent equation-slot compression.  With
\(N=\mathbb P\nabla\cdot(u\otimes u)\), the cross-covariance
\(\chi_s=\tau_s(u,N)+\tau_s(N,u)\) combines transport and pressure into one
symmetric tensor.  This compression is a local derivation in the present
work, not a theorem attributed to Germano and not a uniqueness claim.

Germano's equation (33) also supplies the exact nested-filter stress identity.
It organizes levels of resolution; it does not turn an unknown high-order
moment into a function of the resolved state.

## 2. Exact higher-order hierarchy

The classical two-point and structure-function hierarchy advances in order:

- T. von K\'arm\'an and L. Howarth, *On the Statistical Theory of Isotropic
  Turbulence*, Proceedings of the Royal Society A 164 (1938), 192--215,
  [DOI](https://doi.org/10.1098/rspa.1938.0013).
- R. J. Hill, *Equations Relating Structure Functions of all Orders*, Journal
  of Fluid Mechanics 434 (2001), 379--388,
  [DOI](https://doi.org/10.1017/S0022112001003949).

Hill derives arbitrary-order exact equations from Navier--Stokes and
incompressibility.  These are two-point increment objects, not the local heat
cumulants used here.  They establish the hierarchy context, not the R0.73V
heat-scale formula.

A recent explicit comparison is:

- N. Zambrano and K. Duraisamy, *Two-point turbulence closures in physical
  space*, Journal of Fluid Mechanics 1034 (2026), A12,
  [DOI](https://doi.org/10.1017/jfm.2026.11485).

Their second-order equation contains third-order and pressure--velocity
moments; the third-order equation contains fourth-order and
pressure--quadratic moments.  Their subsequent quasi-normal, Markovian, and
eddy-damping assumptions define a model for homogeneous isotropic turbulence,
not a deterministic finite closure for general three-dimensional
Navier--Stokes.

## 3. Signed cubic transfer and scale locality

Exact subgrid energy transfer is a signed cubic object.  Rigorous locality and
multiscale-gradient results include:

- G. L. Eyink, *The Multifractal Model of Turbulence and A Priori Estimates
  in Large-Eddy Simulation, I. Subgrid Flux and Locality of Energy Transfer*
  (1996), [arXiv](https://arxiv.org/abs/chao-dyn/9602018).
- G. L. Eyink, *Multi-Scale Gradient Expansion of the Turbulent Stress
  Tensor*, Journal of Fluid Mechanics 549 (2006), 159--190,
  [DOI](https://doi.org/10.1017/S0022112005007895).

The estimates have stated filter and regularity hypotheses.  They are not a
sign theorem for the flux, a closure of the complete tensor equation, or an
arbitrary-energy critical estimate.

Duchon and Robert express the local energy defect by a signed third-order
velocity-increment integral:

- J. Duchon and R. Robert, *Inertial energy dissipation for weak solutions of
  incompressible Euler and Navier--Stokes equations*, Nonlinearity 13 (2000),
  249--255, [DOI](https://doi.org/10.1088/0951-7715/13/1/312).

That formula concerns scalar local energy.  It does not identify a minimal
state for the complete second-order tensor tangent.

## 4. Moment-chain comparisons

The Lundgren--Monin--Novikov hierarchy has the schematic form
\(\partial_t f_N=L_Nf_N+L_{N,N+1}f_{N+1}\) and is equivalent to the
Hopf/moment hierarchy.  A modern source with the historical references is:

- R. Friedrich et al., *The Lundgren--Monin--Novikov hierarchy: Kinetic
  equations for turbulence*, 2012,
  [arXiv](https://arxiv.org/abs/1209.6454).

This is an ensemble and multipoint PDF hierarchy, not a deterministic finite
local heat state.

A rigorous moment-chain formulation is:

- A. V. Fursikov, *Moment theory for the Navier--Stokes equations with a
  random right side*, Russian Academy of Sciences Izvestiya Mathematics 41
  (1993), 515--555,
  [DOI](https://doi.org/10.1070/IM1993v041n03ABEH002274).

The chain couples order \(k\) to order \(k+1\).  Finite extremal problems
followed by a limit in the truncation order are not a fixed finite exact
autonomous closure.

Rubinstein and Girimaji show an inconsistency for a particular class of
Markovian second-moment models near the two-component limit:

- R. Rubinstein and S. S. Girimaji, *Second moment closure near the
  two-component limit*, Journal of Fluid Mechanics 548 (2006), 197--206,
  [DOI](https://doi.org/10.1017/S0022112005007792).

That result is not a no-go theorem for every deterministic finite heat-tensor
state.

## 5. Bounded-search conclusion

The primary literature establishes the general \(2\to3\to4\) closure
hierarchy and gives an exact filtered second-stress equation.  The search did
not locate a paper writing the R0.73V third heat-cumulant \(s\)-PDE in the
present form, nor a theorem proving universal minimality or non-closure for a
finite local heat-moment state.

This is a bounded negative finding.  It cannot support “does not exist,”
“first,” novelty, or priority language.  The safe release classification is:

```text
germanoGeneralizedStressEquation=VERIFIED_CLASSICAL
thirdHeatCumulantScalePDE=INTERNAL_EXACT_AUDITED
velocityCumulantAloneIsCompleteTensorLift=FALSE_AS_TRUNCATED_EQUATION
componentwiseMinimality=NOT_ESTABLISHED
finiteLocalHeatMomentUniversalNoGo=NOT_ESTABLISHED
physicalTimeThirdToFourthHierarchy=VERIFIED_CLASSICAL
arbitraryThreeDimensionalGlobalRegularity=OPEN
clayConclusion=OPEN
NOT CLAY
```
