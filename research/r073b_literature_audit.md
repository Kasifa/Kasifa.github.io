# R0.73B primary-literature audit: physical kinetic energy, Squire lift-up, and Bloch low gaps

**Search cutoff:** 2026-08-29

**Status:** bounded primary-source search.  This document is a theorem-design
and scope audit, not a novelty or priority proof.

## 1. Search question

The search asked whether a checked source already supplies, in one theorem,
all of the following for the present heat-decaying two-harmonic shear:

1. the active Orr--Sommerfeld inverse-Laplacian term;
2. a continuous Bloch residue through the zero-gap boundary;
3. the complete three-dimensional Squire/lift-up component;
4. an all-start estimate in the exact physical velocity norm;
5. exceptional rows where OS--Squire inversion degenerates;
6. a row-uniform orthogonal direct sum; and
7. an explicit finite transient for a time-dependent profile whose critical
   points collide.

No checked source supplied that complete combination.  This bounded
non-collision statement only locates the present result; it does not establish
global novelty.

## 2. Consequential primary sources

### 2.1 Colombo--Dolce--Montalto--Ventura: stationary long-wave cancellation

**Source:** Maria Colombo, Michele Dolce, Riccardo Montalto, and Paolo
Ventura, [*Long-wave instability of periodic shear flows for the 2D
Navier--Stokes equations*](https://arxiv.org/html/2509.18070v2),
arXiv:2509.18070v2 (2025).

**Checked use:** their long-wave reduction isolates a zero-mode cancellation,
a simple slow spectral direction, and long-wave instability for stationary
periodic shears.

**Boundary here:** the result is two-dimensional, stationary, and spectral.
It does not give an all-start nonautonomous OS--Squire propagator, the present
Bloch carrier identity, or a physical-velocity direct sum.

### 2.2 Chen--Dai--Wang--Wang: uniform spectral clusters

**Source:** Robin Ming Chen, Tian Dai, Dehua Wang, and Weiqiang Wang,
[*Long-Wave Stability And Instability Of Periodic Shear Flows For The 2D
Navier--Stokes Equations On The beta-Plane*](https://arxiv.org/html/2608.06899v1),
arXiv:2608.06899v1 (2026).

**Checked use:** parameter-dependent contours and Riesz projections show why
singular long-wave clusters require uniform spectral bookkeeping.

**Boundary here:** their \(\beta\) is the Coriolis parameter, not the Bloch
residue in this project.  The flow is stationary, forced, two-dimensional,
and contains a different stabilization mechanism.

### 2.3 Jerome--Chomaz: physical OS--Squire energy and lift-up scaling

**Source:** Jerome J. Jerome and Jean-Marc Chomaz,
[*Extended Squire's transformation and its consequences on transient
growth*](https://arxiv.org/html/1601.07598), arXiv:1601.07598 (2016).

**Checked use:** the paper writes the OS--Squire system in physical kinetic
energy and makes the singular lift-up contribution to transient growth
explicit.

**Boundary here:** the setting is a stationary parallel flow with walls and
nonzero streamwise wave number.  It does not cross a continuous Bloch gap or
sum exceptional nonautonomous rows.

### 2.4 Bedrossian--Germain--Masmoudi: exact streak/lift-up structure

**Source:** Jacob Bedrossian, Pierre Germain, and Nader Masmoudi,
[*On the stability threshold for the 3D Couette flow in Sobolev
regularity*](https://annals.math.princeton.edu/2017/185-2/p07),
Annals of Mathematics 185 (2017), 541--608.

**Checked use:** the streamwise-zero component and lift-up/streak mechanism
are treated as structural parts of the three-dimensional problem rather than
as removable coordinate singularities.

**Boundary here:** Couette geometry has no periodic critical-point collision
and the nonlinear stability theorem uses mixing coordinates and Sobolev
bootstrap estimates not established for the present shear.

### 2.5 Li--Wei--Zhang: three-dimensional good unknown and semigroup payment

**Source:** Te Li, Dongyi Wei, and Zhifei Zhang,
[*Pseudospectral bound and transition threshold for the 3D Kolmogorov
flow*](https://arxiv.org/html/1801.05645v1), arXiv:1801.05645 (2018),
Communications on Pure and Applied Mathematics 73 (2020).

**Checked use:** a direction-dependent good unknown handles the structured
three-dimensional coupling, while resolvent control is converted into a
semigroup bound with an explicit transient payment.

**Boundary here:** the base flow is stationary and single-harmonic, and its
nonzero discrete streamwise mode avoids the present continuous low-gap and
heat-collision boundary.

### 2.6 Wei--Zhang--Zhao: active heat-decaying Kolmogorov operator

**Source:** Dongyi Wei, Zhifei Zhang, and Weiren Zhao,
[*Linear inviscid damping and enhanced dissipation for the Kolmogorov
flow*](https://arxiv.org/html/1711.01822), arXiv:1711.01822 (2017),
Advances in Mathematics 362 (2020), 106963.

**Checked use:** the paper shows that an active inverse-Laplacian term with a
heat-decaying single-harmonic amplitude can be controlled after a structured
projection.

**Boundary here:** a single sine retains fixed critical geometry.  The result
does not contain the double-harmonic collision, a continuous Bloch carrier,
Squire history, or a complete velocity direct sum.

### 2.7 Li--Zhao: all-start nonautonomous evolution

**Source:** Hui Li and Weiren Zhao,
[*Asymptotic stability in the critical space of 2D monotone shear flow in
the viscous fluid*](https://arxiv.org/html/2306.03555v1), arXiv:2306.03555
(2023), Communications in Mathematical Physics 405 (2024), 267.

**Checked use:** the solution operator is genuinely two-parameter and
all-start; a time-dependent wave operator absorbs the active Rayleigh term.

**Boundary here:** strict monotonicity and spectral stability are assumed at
all times.  They fail as a template for the present periodic two-harmonic
critical-point collision.

### 2.8 Bedrossian--Coti Zelati: hypocoercive enhanced-dissipation weights

**Source:** Jacob Bedrossian and Michele Coti Zelati,
[*Enhanced dissipation, hypoellipticity, and anomalous small noise inviscid
limits in shear flows*](https://arxiv.org/abs/1510.08098),
arXiv:1510.08098 (2015), Archive for Rational Mechanics and Analysis 224
(2017), 1161--1204.

**Checked use:** time/frequency-dependent hypocoercive weights provide a
route from shear mixing to enhanced dissipation.

**Boundary here:** this is a passive scalar result with fixed critical-point
degeneracy.  It does not control the active OS pressure term, Squire lift-up,
or collision-changing geometry.

### 2.9 Beaumont: classical periodic Floquet setting

**Source:** D. N. Beaumont, [*The stability of spatially periodic flows*](https://doi.org/10.1017/S0022112081000825),
Journal of Fluid Mechanics 108 (1981), 461--474.

**Checked use:** periodic shear stability naturally decomposes into Floquet
or Bloch fibers; boundary representatives must not be double-counted.

**Boundary here:** the classical frozen spectral analysis does not provide a
nonautonomous physical-energy theorem or a uniform direct sum through a
vanishing gap.

## 3. Consequences for the R0.73B theorem design

The literature supports four conservative choices:

1. keep the exact physical kinetic norm rather than raw \(L^2_q\);
2. keep a finite transient prefactor because nonnormal lift-up is real;
3. state an all-start evolution-family estimate, not only an estimate from
   the original time; and
4. separate the viscous-rate theorem proved here from the still-open
   enhanced-dissipation and nonlinear bootstrap problems.

The literature does **not** authorize claims that physical energy is a new
idea, that Riesz projection or hypocoercive weights are new, or that the
present linear direct sum resolves nonlinear Navier--Stokes regularity.

