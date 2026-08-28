# R0.72Z primary-literature audit

**Search cutoff:** 2026-08-28

**Scope:** Orr--Sommerfeld pressure feedback, Squire orientation and lift-up,
time-dependent active shears, Bloch/long-wave rows, and structured forcing.

## 1. Search method and claim boundary

I searched title/abstract records and inspected primary papers or publisher
records.  Secondary reviews were used only to locate primary work.  The
search asked whether an existing theorem simultaneously covers:

1. an active Orr--Sommerfeld nonlocal term;
2. a time-dependent shear whose critical-point count changes;
3. three-dimensional Squire transfer and lift-up;
4. continuous Bloch residue classes;
5. all-start propagation and structured forcing;
6. a row-uniform physical kinetic-energy direct sum.

No checked paper supplied that combination.  This is a bounded-search
statement, not a novelty or priority proof.

## 2. Source ledger

### 2.1 Li--Wei--Zhang: three-dimensional Kolmogorov flow

**Source:** Te Li, Dongyi Wei, and Zhifei Zhang,
[*Pseudospectral bound and transition threshold for the 3D Kolmogorov
flow*](https://arxiv.org/abs/1801.05645), CPAM 73 (2020),
[DOI](https://doi.org/10.1002/cpa.21863).

**Relevant content:** the paper derives a complete three-dimensional
OS--Squire triangular system.  Theorem 1.1 gives a vorticity response with an
inverse streamwise-wavenumber payment, and the good-unknown construction in
Section 5 contains a spanwise/streamwise ratio.  Sections 5--6 also treat
structured forcing.

**Supports:** an exact Squire payment is structural; a scalar OS estimate
does not by itself remove lift-up.

**Does not support:** the base flow is stationary and single-sine, the
streamwise mode is a nonzero integer, and there is no critical-point
collision or continuous Bloch phase.

### 2.2 Jerome--Chomaz: extended Squire transformation

**Source:** Soundar Jerome and Jean-Marc Chomaz,
[*Extended Squire's transformation and its consequences on transient growth
for a confined shear flow*](https://arxiv.org/html/1601.07598), Journal of
Fluid Mechanics 744 (2014),
[DOI](https://doi.org/10.1017/jfm.2014.83).

**Relevant content:** the extended transformation writes the wall-normal
vorticity of an OS mode with an explicit spanwise/streamwise factor and
identifies the lift-up contribution to transient energy growth.  The
streamwise-zero boundary is singular in that representation.

**Supports:** R0.72Z must retain an orientation or equivalent weighted
payment and an equal-rate transient.

**Does not support:** the paper treats stationary wall-bounded parallel
shears with a discrete nondegenerate spectrum; it is not a nonautonomous
Bloch-uniform forcing theorem.

### 2.3 Jia: monotone Orr--Sommerfeld limiting absorption

**Source:** Hao Jia,
[*Uniform linear inviscid damping and enhanced dissipation near monotonic
shear flows in high Reynolds number regime (I): the whole space
case*](https://arxiv.org/abs/2207.10987), Journal of Mathematical Fluid
Mechanics 25 (2023),
[DOI](https://doi.org/10.1007/s00021-023-00794-8).

**Relevant content:** the full nonlocal Orr--Sommerfeld term is handled as a
compact perturbation of a critical-layer problem, with a limiting-absorption
estimate and enhanced dissipation.

**Supports:** active pressure feedback can be controlled by structure; it
need not be treated as generic forcing.

**Does not support:** the shear is strictly monotone and subject to a
no-discrete-spectrum assumption.  There is no critical-point collision,
Squire system, or Bloch collision estimate.

### 2.4 Beekie--Chen--Jia: periodic nonmonotone shears

**Source:** Ryan Beekie, Shan Chen, and Hao Jia,
[*Uniform vorticity depletion and inviscid damping for periodic shear flows
in the high Reynolds number regime*](https://arxiv.org/abs/2403.13104),
Archive for Rational Mechanics and Analysis 250 (2026), Article 7,
[DOI](https://doi.org/10.1007/s00205-025-02162-4).

**Relevant content:** complete Orr--Sommerfeld limiting absorption and
enhanced dissipation are obtained for periodic nonmonotone shears under
fixed separated nondegenerate critical points and spectral hypotheses.

**Supports:** there are rigorous active nonlocal estimates beyond monotone
geometry.

**Does not support:** the number and location type of critical points remain
fixed.  The assumptions are not uniform through a birth/death collision.

### 2.5 Ding--Lin: forced Poiseuille resolvent

**Source:** Shijin Ding and Zhiwu Lin,
[*Enhanced dissipation and transition threshold for the 2-D plane
Poiseuille flow via resolvent estimate*](https://arxiv.org/abs/2008.10057),
Journal of Differential Equations 332 (2022).

**Relevant content:** the paper proves a resolvent estimate for the complete
Poiseuille Orr--Sommerfeld operator and spacetime estimates for divergence
forcing.

**Supports:** full OS pressure and structured forcing can coexist in a
rigorous estimate.

**Does not support:** this is a stationary two-dimensional channel problem;
its viscosity powers are not the R0.72 collision powers.

### 2.6 Wei--Zhang--Zhao: heat-decaying active Kolmogorov flow

**Source:** Wenting Wei, Zhifei Zhang, and Weiren Zhao,
[*Linear inviscid damping and enhanced dissipation for the Kolmogorov
flow*](https://arxiv.org/abs/1711.01822), Advances in Mathematics 362
(2020), [DOI](https://doi.org/10.1016/j.aim.2019.106963).

**Relevant content:** a time-dependent wave operator treats a
heat-decaying Kolmogorov amplitude with an active inverse-Laplacian term.

**Supports:** nonautonomous active linearized operators are tractable in
special geometry.

**Does not support:** the critical points remain fixed and separated; the
paper has no critical-point creation/annihilation or Squire/Bloch direct sum.

### 2.7 Li--Zhao: monotone heat evolution

**Source:** Te Li and Weiren Zhao,
[*Asymptotic stability in the critical space of 2D monotone shear flow in
the viscous fluid*](https://arxiv.org/abs/2306.03555), Communications in
Mathematical Physics 405 (2024), 267,
[DOI](https://doi.org/10.1007/s00220-024-05155-8).

**Relevant content:** an all-start propagator is obtained for a heat-evolving
strictly monotone shear under a no-point-spectrum assumption at every time.

**Supports:** all-start nonautonomous propagation is the right object.

**Does not support:** strict monotonicity excludes the R0.72 collision.

### 2.8 Colombo--Dolce--Montalto--Ventura: long-wave instability

**Source:** Maria Colombo, Michele Dolce, Riccardo Montalto, and Paolo
Ventura,
[*Long-wave instability of periodic shear flows for the 2D Navier--Stokes
equations*](https://arxiv.org/html/2509.18070), arXiv:2509.18070v2 (2025).

**Relevant content:** Theorem 1.1 proves an unstable eigenvalue for general
stationary periodic shears in a sufficiently long-wave regime when an
explicit shear/viscosity condition holds.

**Supports:** weak streamwise rows cannot be declared stable solely by
continuity from nonzero modes; active inverse-Laplacian terms can change the
sign of the leading long-wave eigenvalue.

**Does not support:** the shear is stationary and externally maintained.
The theorem does not decide the exact two-harmonic heat path.

### 2.9 Li--Zhao and Li--Ren--Wang--Zhang: spectral boundaries

**Sources:**

- Te Li and Weiren Zhao,
  [*Viscosity driven instability of shear flows without
  boundaries*](https://arxiv.org/html/2410.23798), arXiv:2410.23798.
- Te Li, Xiaoyutao Ren, Dongyi Wang, and Zhifei Zhang,
  [*Instability of shear flows with neutral embedded
  eigenvalues*](https://arxiv.org/abs/2602.07807), arXiv:2602.07807.

**Relevant content:** the first shows that a heat-evolving shear can cross a
frozen-time spectral boundary; the second shows large nonnormal growth near
neutral embedded eigenvalues.

**Supports:** initial spectral stability and absence of a positive
eigenvalue are not enough for an all-time nonnormal propagator bound.

**Does not support:** neither paper proves the R0.72Z nonautonomous
collision estimate.

## 3. Gap matrix against the checked literature

| Required feature | Strongest checked precedent | Remaining mismatch |
|---|---|---|
| Active OS pressure term | Jia; Beekie--Chen--Jia; Ding--Lin | fixed spectral/critical geometry |
| Nonautonomous active shear | Wei--Zhang--Zhao; Li--Zhao | fixed critical type or strict monotonicity |
| Three-dimensional Squire | Li--Wei--Zhang; Jerome--Chomaz | stationary, nonzero streamwise mode |
| Critical-point collision | scalar R0.72T--X only | no checked active OS--Squire theorem |
| Continuous Bloch residue | classical Floquet analyses | no collision-uniform forced propagator |
| Structured forcing | Ding--Lin; Li--Wei--Zhang | different geometry and scale |
| Weak streamwise rows | 2025 long-wave instability | warns against, does not decide exact path |
| Physical-energy direct sum | Couette/Kolmogorov special cases | row weights and zero modes remain |

## 4. Frozen literature decisions

- `existingFixedGeometryOSAbsorption`: **SUPPORTED**.
- `existingThreeDimensionalSquireOrientationPayment`: **SUPPORTED**.
- `existingNonautonomousActiveSpecialGeometry`: **SUPPORTED**.
- `existingCriticalCollisionOSSquireTheorem`: **NOT FOUND IN THIS SEARCH**.
- `existingBlochUniformForcedPhysicalDirectSumThroughCollision`:
  **NOT FOUND IN THIS SEARCH**.
- `weakStreamwiseRowsAutomaticallyStable`: **CONTRADICTED AS A GENERAL
  PRINCIPLE** by the long-wave instability theorem.

These decisions determine the safe R0.72Z wording: the new exact
commutator and orientation ledger is compared with precedents, but no
priority claim and no complete-system claim is made.
