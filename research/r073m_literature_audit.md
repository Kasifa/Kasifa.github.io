# R0.73M literature audit: non-autonomous nonlinear departure

**Status:** bounded two-wave primary-source audit and independent source audit
PASS; absence claims are limited to the sources and searches recorded below

**Search date:** 2026-08-31 (Asia/Shanghai)

## 1. Direct literature decision

No checked source supplies a theorem that can be invoked as a black box to
turn the R0.73L non-autonomous rank-one action estimate into the R0.73M
fixed-distance nonlinear departure theorem for the exact periodic,
boundary-free, unforced two-dimensional Navier--Stokes subsystem.

The literature covers important neighboring mechanisms: autonomous
spectral instability bootstraps; high-order Grenier constructions for
singular boundary layers; transient nonlinear growth for special exact heat
flows near Couette; stability for heat-evolving shears whose full path stays
spectrally stable; and a viscosity-driven transition from stable to unstable
Rayleigh spectrum without boundaries.  None of those results simultaneously
contains the moving simple viscous branch, the complete slow-window action,
the exact harmonic return, and the zero-forcing endpoint required here.

This is a bounded-search gap, not an absolute novelty theorem.

## 2. Autonomous spectral instability

Friedlander, Pavlović, and Shvydkoy prove that spectral instability of the
linearization about a smooth steady Navier--Stokes flow implies nonlinear
\((L^q,L^p)\) Lyapunov instability for \(q>\max\{p,n\}\).  Their
analytic-semigroup bootstrap is an important model for controlling the
nonlinear remainder.

- S. Friedlander, N. Pavlović, and R. Shvydkoy,
  [*Nonlinear instability for the Navier--Stokes equations*](https://arxiv.org/abs/math/0508173),
  Communications in Mathematical Physics 264 (2006), 335--347.

R0.73M is not autonomous: its generator, selected line, and instantaneous
growth rate vary across a window of length \(D_*/\varepsilon\) in fast
time.  The cited theorem contains neither a moving projector nor an
adiabatic action, so it is a structural comparison rather than a closure.

## 3. Grenier-type high-order constructions

Grenier introduced high-order approximate-solution and corrector schemes for
nonlinear instability of Euler and Prandtl equations.

- E. Grenier,
  [*On the nonlinear instability of Euler and Prandtl equations*](https://doi.org/10.1002/1097-0312%28200009%2953%3A9%3C1067%3A%3AAID-CPA1%3E3.0.CO%3B2-Q),
  Communications on Pure and Applied Mathematics 53 (2000), 1067--1091.

Desjardins and Grenier apply a related wave-packet/corrector mechanism to
viscous Ekman and mixed Ekman--Hartmann boundary layers.

- B. Desjardins and E. Grenier,
  [*Linear instability implies nonlinear instability for various types of
  viscous boundary layers*](https://numdam.org/item/AIHPC_2003__20_1_87_0/),
  Annales de l'Institut Henri Poincaré C 20 (2003), 87--106.

Grenier and Nguyen give a direct precursor for \(L^\infty\) instability of
Prandtl layers near a boundary.

- E. Grenier and T. T. Nguyen,
  [*\(L^\infty\) instability of Prandtl layers*](https://doi.org/10.1007/s40818-019-0074-3),
  Annals of PDE 5 (2019), article 18.

Bian and Grenier study nonlinear instability of shear and Prandtl boundary
layers in a half-plane, including heat-evolving background profiles and
high-order constructions.

- D. Bian and E. Grenier,
  [*Instability of shear layers and Prandtl's boundary layers*](https://arxiv.org/abs/2401.15679),
  arXiv:2401.15679 (2024).

The displayed Bian--Grenier nonlinear theorems construct solutions of the
**forced** Navier--Stokes equations with a force \(F^\nu\) that can be made
arbitrarily high-order small but is not identically zero.  Their
\(O(1)\) endpoint theorem assumes a holomorphic, Euler-spectrally unstable
initial profile; for merely \(C^\infty\) profiles the stated lower-bound scale is
\(\nu^\theta\).  These papers are the closest high-order-corrector
precedents, but their boundary geometry, sublayers, regularity, and forcing
do not match the exact periodic, boundary-free, zero-forcing equation in
R0.73M.  They must not be cited as a theorem for the present orbit.

## 4. Exact unforced heat-evolving shears

Li, Masmoudi, and Zhao prove transient nonlinear exponential amplification
for a specially constructed exact heat-evolving near-Couette shear and
establish the sharpness of the \(\nu^{1/2}\) transition threshold.  Their
mechanism is a dynamical frequency cascade.

- H. Li, N. Masmoudi, and W. Zhao,
  [*A dynamical approach to the study of instability near Couette flow*](https://arxiv.org/abs/2203.10894),
  Communications on Pure and Applied Mathematics 77 (2024), 2863--2946.

This is the strongest checked zero-forcing nonlinear transient-growth
precedent.  It is a relative-growth and enhanced-dissipation-threshold
result: its absolute endpoint scale may still vanish as \(\nu\to0\).  It
does not use a moving rank-one viscous eigenbranch or the R0.73L selected
action and is not the prescribed-action fixed-distance theorem sought here.

Li and Zhao prove the complementary stability result for heat-evolving
monotone shears under the assumption that the Rayleigh operator remains free
of eigenvalues and embedded eigenvalues along the relevant path.

- H. Li and W. Zhao,
  [*Asymptotic stability in the critical space of 2D monotone shear flow in
  the viscous fluid*](https://arxiv.org/abs/2306.03555), arXiv:2306.03555
  (2023).

Li--Zhao assume that, for every time and every nonzero Fourier mode, the
Rayleigh operator has neither eigenvalues nor embedded eigenvalues.  R0.73M
instead uses a selected moving viscous branch and does not invoke that
all-time Rayleigh-stability hypothesis.  Their theorem is therefore not
directly applicable, and no contradiction follows.

## 5. Viscosity-driven spectral transition without boundaries

Li and Zhao construct an exact heat-evolving shear whose inviscid Rayleigh
operator starts without point spectrum, passes through an embedded mode,
and later has a unique unstable eigenvalue on \(k=\pm1\) in a boundary-free
domain.

- H. Li and W. Zhao,
  [*Viscosity driven instability of shear flows without boundaries*](https://arxiv.org/abs/2410.23798),
  arXiv:2410.23798 (2024).

This is the closest positive source for the claim that heat evolution can
drive a genuine Rayleigh spectral transition without a wall.  It is not a
viscous Orr--Sommerfeld or Navier--Stokes generator theorem.  Remark 1.5
explicitly leaves nonlinear growth of the exact unforced evolving shear for
future work, with a relative-growth target rather than a fixed-distance
endpoint; Remark 1.6 explains why adding an arbitrarily small force makes
nonlinear growth easier.  This is closely related to, but not identical
with, R0.73L--M, which begins after a selected moving viscous branch and its
action estimates are already available.

## 6. Periodic decaying shear on the stable side

Lin and Xu prove metastability and decay of non-shear perturbations near
periodic Kolmogorov flows, including a nonlinear result for perturbations of
vorticity size comparable to viscosity.

- Z. Lin and M. Xu,
  [*Metastability of Kolmogorov flows and inviscid damping of shear flows*](https://arxiv.org/abs/1707.00278),
  Archive for Rational Mechanics and Analysis 231 (2019), 1811--1852.

This is the nearest periodic stable-side collision.  It shows that a
decaying periodic shear does not by itself imply departure.  The sign and
isolation of the selected branch, the complete positive action, and the
generated-harmonic energy bounds cannot be omitted.

## 7. Slowly varying finite-amplitude precedent

Hall studies viscous flows whose Reynolds or Rayleigh parameter changes
slowly and identifies a short interval in which a quasi-steady approximation
breaks down and a finite-amplitude response forms.  The displayed model is a
slowly modulated Taylor--vortex problem.

- P. Hall,
  [*On the nonlinear stability of slowly varying time-dependent viscous
  flows*](https://doi.org/10.1017/S0022112083000208), Journal of Fluid
  Mechanics 126 (1983), 357--368.

This is a direct conceptual collision for slow passage and finite-amplitude
response.  It is a problem-specific weakly nonlinear/asymptotic analysis,
not a periodic boundary-free Navier--Stokes theorem with a uniformly tracked
moving spectral projection, Sobolev remainder, and exact zero forcing.

## 8. Exact gap left by the checked literature

No single checked theorem provides all of the following features
simultaneously in one compatible setting:

1. a periodic boundary-free heat-evolving background geometry;
2. a simple moving viscous spectral line tracked over
   \(0\le d\le D_*\) with two-sided bounded action prefactor;
3. endpoint-normalized forward-orbit localization at a rate above the exact
   doubled-harmonic numerical-abscissa gate;
4. uniform control of the generated \(K_z=0,\pm2,\pm3\) rows and their cubic
   return to \(K_z=\pm1\);
5. a fixed-distance nonlinear endpoint from the prescribed seed
   \(\rho e^{-\Lambda\mathcal A_*}\phi_\Lambda\);
6. exact zero forcing throughout the construction.

R0.73M therefore needs its own harmonic energy/Stieltjes proof.  The
literature is used to set the claim boundary and to identify missing
hypotheses, not to replace that proof.

## 9. Evidence-supported wording

Conditional on the independent closure of M1--M6, the strongest admissible
wording is:

> In the sealed periodic two-harmonic family, the R0.73L two-sided selected
> action and forward-orbit localization combine with a model-specific
> harmonic energy expansion to give a prescribed-action, fixed-distance
> nonlinear departure inside an exactly invariant planar subsystem.

The following wording is not supported:

- “the first theorem of nonlinear instability for evolving shears”;
- “a direct consequence of autonomous spectral instability theory”;
- “a generic theorem for non-autonomous Navier--Stokes flows”;
- “one fixed-background Lyapunov instability”;
- “a genuinely three-dimensional instability mechanism”;
- “progress on finite-time singularity or the Clay conclusion.”
