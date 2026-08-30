# R0.73H literature audit: harmonic-resolved nonlinear departure

**Search date:** 2026-08-30  
**Question:** whether an existing theorem already converts the R0.73F
nonautonomous selected-row gain into the R0.73H gain-normalized nonlinear
departure  
**Result:** no direct collision found in the bounded search described below

## 1. Direct conclusion

I did not find an existing theorem that simultaneously covers all of the
following features:

- a periodic, unforced, heat-decaying two-harmonic shear;
- a background family whose amplitude grows with \(\Lambda\);
- a nonautonomous selected \(K_z=\pm1\) moving bundle;
- fixed-window gain of order \(e^{\kappa\Lambda}\);
- exact quadratic generation of \(K_z=0,\pm2\);
- cubic return to \(K_z=\pm1,\pm3\);
- a gain-normalized seed \(\delta/G_\Lambda\);
- and an \(L^2\)-energy closure that avoids uniform high-Sobolev
  propagation.

This is a bounded non-collision result, not a priority or originality
claim.  A journal submission would still require MathSciNet and zbMATH
classification searches plus forward and backward citation tracing.

## 2. Closest nonlinear-upgrade results

### Friedlander--Pavlovi\'c--Shvydkoy (2006)

[Nonlinear instability for the Navier--Stokes
equations](https://arxiv.org/abs/math/0508173),
DOI [10.1007/s00220-006-1526-7](https://doi.org/10.1007/s00220-006-1526-7),
proves an abstract \(L^p\) nonlinear-instability theorem from linear
instability for a fixed autonomous Navier--Stokes linearization.  It is an
important bootstrap template, but R0.73H has a time-dependent generator and
a \(\Lambda\)-dependent background family.  The selected-row lower bound is
not the fixed full-space unstable spectrum assumed there.

### Desjardins--Grenier (2003)

[Linear instability implies nonlinear instability for various types of
viscous boundary
layers](https://doi.org/10.1016/S0294-1449(02)00009-4) constructs higher
order approximate solutions under a package of energy, wave-packet,
interaction-algebra, and resolvent estimates.  Its method explains why the
even/odd interaction algebra is useful, but its boundary-layer geometry and
hypotheses are not a black box for the present periodic nonautonomous
problem.

### Bian--Grenier (2024)

[Onset of nonlinear instabilities in monotonic viscous boundary
layers](https://arxiv.org/abs/2206.01318),
DOI [10.1137/22M1505773](https://doi.org/10.1137/22M1505773), explicitly
studies cubic interactions and nonlinear saturation.  Its single-carrier
expansion has the same support pattern: the second order creates a mean and
double frequency, and the third order returns to the carrier and creates a
triple frequency.  The setting is a viscous boundary layer, and the sign and
size of the cubic coefficient are profile dependent.  Its formal and
numerical saturation evidence does not prove the R0.73H continuum energy
theorem.

## 3. Heat-evolving and unforced shear results

### Lin--Xu (2019)

[Metastability of Kolmogorov flows and inviscid damping of shear
flows](https://arxiv.org/abs/1707.00278),
DOI [10.1007/s00205-018-1311-8](https://doi.org/10.1007/s00205-018-1311-8),
treats an unforced periodic two-dimensional Kolmogorov flow and proves
decay or metastability for suitable perturbations.  It is close in geometry
and in the use of a heat-decaying exact shear, but it concerns a
single-harmonic stable mechanism rather than the R0.73 moving unstable
bundle.

### Li--Zhao (2024)

[Asymptotic stability in the critical space of 2D monotone shear flow in
the viscous fluid](https://arxiv.org/abs/2306.03555),
DOI [10.1007/s00220-024-05155-8](https://doi.org/10.1007/s00220-024-05155-8),
constructs a time-dependent wave operator for an unforced heat-evolving
monotone shear and obtains the sharp \(\nu^{1/2}\) stability threshold in
its setting.  Its spectral-stability hypotheses and unbounded transverse
geometry exclude the present unstable periodic route.

### Li--Zhao (2025)

[Viscosity driven instability of shear flows without
boundaries](https://arxiv.org/abs/2410.23798),
DOI [10.1016/j.matpur.2025.103724](https://doi.org/10.1016/j.matpur.2025.103724),
constructs a shear that evolves from spectral stability to spectral
instability under viscosity.  This confirms that heat evolution can create
instability without a wall, but it is a frozen-time spectral result rather
than a nonautonomous propagation and nonlinear-departure theorem.

### Li--Masmoudi--Zhao (2024)

[A dynamical approach to the study of instability near Couette
flow](https://arxiv.org/abs/2203.10894),
DOI [10.1002/cpa.22183](https://doi.org/10.1002/cpa.22183), proves transient
exponential growth and the sharp \(\nu^{1/2}\) threshold for a specially
constructed near-Couette setting.  It is the closest natural-scale template
in this group, but its profile, domain, critical spaces, and algebraic
viscosity scale differ from the present two-harmonic periodic family.

## 4. Two-dimensional regularity boundary

Ladyzhenskaya's classical two-dimensional Navier--Stokes theory,
[DOI 10.1002/cpa.3160120303](https://doi.org/10.1002/cpa.3160120303),
supports the global smoothness statement once the planar invariant
subspace has been verified directly.  It does not imply stability.  A
globally smooth two-dimensional orbit can still depart a fixed distance
from a time-dependent background.

This distinction is essential for R0.73H:

- the planar departure theorem can be mathematically nontrivial and exact;
- the same planar invariance rules out any claim of three-dimensional
  vortex stretching or finite-time singularity along the selected orbit.

## 5. What R0.73H must prove itself

The literature does not remove any of these obligations:

1. derive the complete \(K_z\) interaction hierarchy with the physical
   Leray projection;
2. prove a continuum numerical-abscissa bound on the doubled row;
3. localize the quadratic and cubic Duhamel responses with constants
   independent of large \(\Lambda\);
4. control the exact fourth-order remainder;
5. preserve the distinction between \(\delta/G_\Lambda\) and the
   prescribed lower-law seed \(\delta e^{-r\Lambda D}\);
6. treat any transverse \(K_x\ne0\) extension as a separate theorem.

## 6. Search boundary

The search covered nonlinear instability from spectral growth, Grenier
high-order constructions, cubic saturation, periodic Kolmogorov flows,
unforced heat-evolving shears, near-Couette threshold results, and
viscosity-driven instability without boundaries.  It used journal DOI
records and primary arXiv records where available.  No claim is made that
this finite search exhausts every language, thesis, monograph, or unpublished
manuscript.
