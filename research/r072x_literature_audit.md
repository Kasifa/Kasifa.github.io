# R0.72X bounded primary-source literature audit

**Date:** 2026-08-28

**Outcome:** the fixed-margin \(A_1\) input used in R0.72X is supported by a
primary time-dependent nondegenerate-shear theorem after the exact slow-time
rescaling.  That theorem cannot be moved with uniform constants to the
shrinking \(A_2\) interface.  The all-center exact-family graph theorem and
block tiling in R0.72X are not quoted from the literature.  A bounded search
did not locate an existing theorem with the same combination of changing
critical-point count, exact two-harmonic heat path, expanding torus, Bloch
twists, negative-Sobolev graph norm, and all-start constants.  This is not a
novelty or priority claim.

---

## 1. Terminology: this is not an Orr critical time

In Couette-flow literature, a Fourier critical or resonant time usually
means an Orr time \(t=\eta/k\), when a tilted Fourier frequency passes through
its least elliptic configuration.  Examples include
[Bedrossian--Masmoudi](https://arxiv.org/abs/1306.5028) for two-dimensional
Euler and [Bedrossian--Germain--Masmoudi](https://arxiv.org/abs/1506.03720)
for three-dimensional Couette flow.

R0.72X instead studies a **geometric collision time**: two spatial critical
points of one time-dependent shear merge and disappear at a fold.  The two
mechanisms must not be identified.  In particular, the scalar shear-row
estimate here contains none of the lift-up, pressure, vortex-stretching, or
nonlinear resonance structure treated in the three-dimensional Couette
work.

---

## 2. Fixed and finite-type shear benchmarks

[Bedrossian--Coti Zelati](https://arxiv.org/abs/1510.08098) proves enhanced
dissipation and hypoelliptic estimates for stationary shears with finitely
degenerate critical points.  The rate retains the order of vanishing of the
profile derivative.  The paper supplies the fixed-profile benchmark but its
constants depend on that profile and do not cross a time at which the number
of critical points changes.

[Coti Zelati--Gallay](https://arxiv.org/abs/2108.11192) obtains optimal
decay estimates for fixed higher-dimensional parallel shear profiles.  It
supports the finite-type rate hierarchy and removes older logarithmic losses
in its setting.  The profile geometry remains fixed.

[Albritton--Beekie--Novack](https://arxiv.org/abs/2105.12308) derives
enhanced dissipation through Hörmander hypoellipticity for fixed finite-type
shears.  It is the closest methodological precedent for a spacetime graph
estimate, but it does not include a nonautonomous topology change in the
critical set or the expanding-period family of R0.72X.

---

## 3. The exact \(A_1\) theorem used on fixed outer margins

[Coble--He, Theorem 1.2](https://arxiv.org/html/2309.15738) treats
time-dependent nondegenerate shears.  Its stated assumptions include:

1. a fixed finite number of shared nondegenerate critical points;
2. pairwise disjoint critical neighborhoods with one fixed positive radius;
3. uniform local Morse comparability and an exterior-gradient floor;
4. uniform derivative bounds;
5. a slowly moving reference shear, measured by
   \(\|\partial_{ty}U\|_\infty\le\nu^{3/4}\).

Under these hypotheses it gives the modewise rate

\[
 \|f_k(t)\|_2
 \le e\,e^{-c\nu^{1/2}|k|^{1/2}t}\|f_k(0)\|_2.
\]

On either fixed R0.72X outer interval, the exact heat path has fixed critical
count, positive separation, a positive Hessian floor, and a positive
away-gradient floor.  With \(t=\varepsilon_c d\) and
\(\nu=\varepsilon_c^{-1}\), the actual profile can be its own reference and

\[
 \|\partial_{tx}W(\nu t)\|_\infty
 \le C_\delta\nu\le\nu^{3/4},
 \qquad 0<\nu\le\min\{1,C_\delta^{-4}\},
\]

for sufficiently small \(\nu\).  This is the precise black-box role of the
paper in R0.72X.  The invocation is restricted to the periodic
representative \(\beta=0\).  R0.72X does not infer a Bloch-uniform
fixed-margin \(A_1\) theorem from this source.

The theorem does **not** cover the shrinking interface.  There the
pre-collision critical separation and Hessian are \(O(\alpha)\), while the
post-collision exterior-gradient floor is \(O(\alpha^2)\).  Its fixed-radius
and fixed-shape assumptions therefore lose uniformity exactly where the
\(A_2\) block begins.

---

## 4. Nonautonomous and gluing precedents

[Coti Zelati--Delgadino--Elgindi](https://arxiv.org/html/1806.03258)
explains that a nonautonomous mixing-to-dissipation argument needs the same
mixing estimate for every initial time.  Their Theorem 2.1 assumes an
arbitrary-start mixing inequality and then converts it into a viscous decay
timescale.  A single collision-centered estimate is therefore not an
all-start semigroup theorem.

[Benthaus--Nobili](https://arxiv.org/html/2501.16905) gives explicit
time-segment gluing for velocity fields of the form \(\xi(t)v(y)\).  It is a
useful cocycle precedent, but the spatial profile is fixed and the constants
are not designed for a fold collision.

[Benthaus--Coclite--Nobili](https://arxiv.org/abs/2603.14624) studies a
rigidly translating sine shear.  It shows quantitatively that motion of
simple critical points changes enhanced-dissipation rates and can even
average transport toward heat behavior.  The critical points remain simple,
separated, and fixed in number.

[Siming He](https://arxiv.org/abs/2603.14657) develops localized,
streamline-wise hypocoercivity for a fixed shear with critical points.  Its
local weights are relevant to a future scale-sharp \(A_1\)-to-monotone
transition theorem, but the profile is not time-dependent and its constants
do not provide the R0.72X fold crossing.

[Elgindi--Liss--Mattingly](https://arxiv.org/abs/2304.05374) proves optimal
mixing and enhanced dissipation for a time-periodic Lipschitz flow assembled
from alternating shears.  Its hyperbolic alternating mechanism is different
from a change in critical-point type.

---

## 5. Support matrix

| R0.72X statement | Closest primary source | Supported use | Unsupported extrapolation |
|---|---|---|---|
| Fixed-margin \(A_1\) rate \(e^{-c\sqrt{\varepsilon_c}d}\) | Coble--He, Theorem 1.2 | Applied to the periodic representative where the exact path has a fixed shape package | Constants uniform as the margin shrinks to the fold, or a Bloch-uniform fast-\(A_1\) extension |
| Finite-type \(A_1/A_2\) benchmark powers | Bedrossian--Coti Zelati; Coti Zelati--Gallay; Albritton--Beekie--Novack | Calibrates expected local timescales | Nonautonomous crossing theorem |
| All-start requirement | Coti Zelati--Delgadino--Elgindi | Confirms that arbitrary initial time is a distinct condition | Direct application to the expanding torus or unbounded polynomial model |
| Segment cocycle | Benthaus--Nobili | Supports exact propagation-factor bookkeeping | Uniform constants through changing critical count |
| Moving critical points | Benthaus--Coclite--Nobili | Shows motion can change the rate and cannot be ignored | Fold creation or annihilation |
| All-center exact graph theorem and \(q^{\lfloor L/(2T\alpha^2)\rfloor}\) tiling | R0.72X Sections 2--5 | Project proof | Not attributed to an external theorem |
| Bloch-twisted expanding-torus direct sum | R0.72X Sections 4 and 6 | Project proof | Does not imply the complete physical row sum |

---

## 6. Remaining literature boundary

The bounded search did not locate a published or preprint theorem that
simultaneously supplies:

1. a time-dependent fold at which the critical-point count changes;
2. uniform all-start propagation through the fold;
3. the exact two-harmonic heat path rather than a fixed profile or rigid
   translation;
4. an expanding periodic domain and every Bloch residue;
5. a negative-Sobolev graph estimate and homogeneous integrated energy;
6. constants ready for the row-dependent linearized Navier--Stokes ledger.

The absence of a hit in a bounded search is not evidence that no such result
exists.  External expert review and a broader priority search are required
before any novelty statement.

The direct Clay value remains low.  These sources and R0.72X concern linear
scalar mixing/dissipation.  They do not control the pressure, nonlocal
velocity recovery, lift-up, vortex stretching, or nonlinear Fourier
convolution of general three-dimensional incompressible Navier--Stokes.
