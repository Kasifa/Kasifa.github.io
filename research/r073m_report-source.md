# R0.73M report source: prescribed-action planar nonlinear departure

**Status:** analytic report source frozen after continuum, independent,
adversarial, and Deep Research audits; finite diagnostic and publication
artifacts are not yet appended

**Date:** 2026-08-31 (Asia/Shanghai)

## 1. Direct result

For the exact unforced backgrounds

\[
 \overline U_\Lambda(t,y)
 =(0,0,2\Lambda W(4t,2y)),
 \qquad
 W(d,x)=-\frac12e^{-d}\sin x+\frac14e^{-4d}\sin2x,
\]

set

\[
 D_*={1\over450},\qquad T_*={1\over1800},\qquad
 \mathcal A_*:=\int_0^{D_*}\lambda_0(r)\,\mathrm dr.
\]

There exist \(\rho_0,c_*>0\) and \(\Lambda_0<\infty\) such that, for every
\(\Lambda\ge\Lambda_0\) and \(0<\rho\le\rho_0\), the exact Navier--Stokes
solution launched from

\[
 \overline U_\Lambda(0)
 +\rho e^{-\Lambda\mathcal A_*}\phi_\Lambda
\]

is global and smooth and obeys

\[
 \left\|\Pi_{\{K_z=\pm1\}}
 \bigl(U_\Lambda^\rho(T_*)-\overline U_\Lambda(T_*)\bigr)
 \right\|_2\ge c_*\rho.
\]

At the same time,

\[
 \|U_\Lambda^\rho(0)-\overline U_\Lambda(0)\|_{H^3}
 \le C\rho\Lambda^2e^{-\Lambda\mathcal A_*}\longrightarrow0.
\]

This is the exact R0.73M headline.  It is a family-level planar departure
theorem, not one fixed-background Lyapunov instability.

## 2. New mathematical interface

R0.73H normalized the seed by the unknown actual selected gain
\(G_\Lambda^*\).  R0.73L supplies the missing two-sided prefactor:

\[
 c_Le^{\Lambda\mathcal A_*}
 \le G_\Lambda^*\le
 C_Le^{\Lambda\mathcal A_*}.
\]

Thus the prescribed action seed is exactly a gain-normalized seed with

\[
 \delta_\Lambda
 =\rho G_\Lambda^*e^{-\Lambda\mathcal A_*}
 \in[c_L\rho,C_L\rho].
\]

The R0.73H harmonic hierarchy can be rerun on the full fixed endpoint using
the R0.73J spectral floor and the R0.73L forward-orbit quotient.  The exact
strict margins are

\[
 {1\over1500},\qquad {1\over1000},\qquad {21\over125}.
\]

The first controls the doubled row, the second the cubic rows, and the third
the fourth-order remainder.  No full-space high-Sobolev semigroup estimate
or backward parabolic solve is inserted.

## 3. Deep Research method and outcome

The literature search used two targeted waves and a separate adversarial
source audit.  It covered:

- autonomous Navier--Stokes spectral-to-nonlinear instability;
- Grenier high-order corrector methods and viscous boundary layers;
- forced heat-evolving shear/Prandtl-layer departure;
- exact unforced near-Couette transient nonlinear amplification;
- stability of all-time Rayleigh-stable heat-evolving shears;
- viscosity-induced Rayleigh spectral transition without boundaries;
- periodic Kolmogorov-flow metastability;
- slowly varying finite-amplitude Taylor--vortex response.

Primary sources and exact claim boundaries are recorded in
`r073m_literature_audit.md` and `r073m_claim_source_ledger.md`.

The bounded conclusion is that no single checked theorem simultaneously
contains the periodic boundary-free geometry, selected moving viscous line,
two-sided slow-window action, harmonic return, exact zero forcing, and
fixed-distance endpoint.  This is not an absolute priority or novelty claim.

## 4. Evidence ledger

| Layer | Status | Evidence |
|---|---|---|
| kinetic/physical conjugacy | CLOSED | exact Fourier multiplier identity and row orthogonality |
| two-sided action and selected-orbit localization | CLOSED upstream | R0.73L action/quotient plus R0.73J continuum floor |
| fixed-endpoint harmonic energy transfer | CLOSED | R0.73M proof and independent audit |
| fourth-order remainder | CLOSED | product-measure/Stieltjes energy estimate |
| prescribed-action endpoint | CLOSED | bounded-prefactor recoding |
| planar global smoothness | CLOSED | invariant 2D vorticity equation |
| literature boundary | CLOSED within bounded search | Deep Research plus independent source audit |
| finite diagnostic | PENDING | must use inviscid finite action, not the viscous action |
| formal figure and public release | PENDING | separate release gates |

## 5. Exact boundary for the public note

The public note may state that the selected seed is specified by the full
inviscid action rather than the unknown exact gain.  It must also state all
of the following:

- the background changes with \(\Lambda\) and grows in amplitude;
- every constructed orbit stays in an exactly invariant planar subsystem;
- the constants \(c_*\) and \(\rho_0\) are existential, not numerically
  extracted;
- finite diagnostics do not certify the continuum theorem;
- a prefactor limit, a two-term WKB expansion, one fixed-background
  instability, transverse 3D closure, singularity, and Clay all remain open.
