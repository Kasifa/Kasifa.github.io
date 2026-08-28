# R0.72W literature audit: exact analytic tails and a merging shear critical point

**Search date:** 2026-08-28

**Nature of audit:** bounded search of primary papers and preprints.  It is
not a novelty, priority, or nonexistence proof.

---

## 1. The combination of properties that matters here

R0.72W studies

\[
 V_\alpha(S,X)=\alpha^{-3}\left[
 2e^{-\alpha^2S}\sin(\alpha X)
 -e^{-4\alpha^2S}\sin(2\alpha X)
 \right]
\]

as $\alpha\downarrow0$.  Its special features have to be kept together:

1. the shear is nonautonomous and follows the heat equation;
2. two critical points merge and disappear at one $A_2$ spacetime event;
3. the collision chart converges to $H_3=X^3+6SX$;
4. the physical torus expands to length $2\pi/\alpha$ after rescaling;
5. every finite heat-polynomial truncation ceases to be small on that scale;
6. the desired graph forcing is $L_S^2H_X^{-1}$, not an autonomous resolvent
   or homogeneous semigroup estimate;
7. the theorem constant must be uniform in the degeneration parameter.

Within the search below, no source was found that already states a theorem
with this complete combination.  The closest results supply important
calibration and proof templates, but none directly replaces the
compact--escaping unit-cell proof in R0.72W.

---

## 2. Stationary finite-type shear theorems

### 2.1 Bedrossian--Coti Zelati

J. Bedrossian and M. Coti Zelati, “Enhanced dissipation,
hypoellipticity, and anomalous small noise inviscid limits in shear flows,”
*Archive for Rational Mechanics and Analysis* 224 (2017), 1161--1204.

- Primary preprint: [arXiv:1510.08098](https://arxiv.org/abs/1510.08098)
- Journal DOI: [10.1007/s00205-017-1099-y](https://doi.org/10.1007/s00205-017-1099-y)

The paper treats fixed periodic or channel shears with finitely many critical
points, each of finite order.  Localized spectral-gap inequalities and a
hypocoercive functional produce the finite-type enhanced-dissipation scale.
For a cubic degeneracy, the resulting exponent is consistent with the
$3/5$--$2/5$ scaling used in R0.72T--W.

**Why it does not substitute for R0.72W:** the critical set and its orders are
fixed.  There is no birth, collision, or disappearance of critical points,
no expanding torus, and no nonautonomous $L_S^2H_X^{-1}$ graph theorem.

### 2.2 Coti Zelati--Gallay

M. Coti Zelati and T. Gallay, “Enhanced dissipation and Taylor dispersion in
higher-dimensional parallel shear flows,” *Journal of the London
Mathematical Society* 108 (2023), 1358--1392.

- Primary preprint: [arXiv:2108.11192](https://arxiv.org/abs/2108.11192)
- Journal DOI: [10.1112/jlms.12782](https://doi.org/10.1112/jlms.12782)

The paper derives optimal enhanced-dissipation and Taylor-dispersion bounds
for a fixed parallel shear on a bounded cross-section, using quantitative
resolvent estimates and also hypocoercivity.  Its thin-level-set coercivity is
a useful static comparison for the noncollision regions.

**Boundary:** the profile and cross-section are fixed.  Constants may depend
on their geometry.  The result does not treat a merging critical set or a
degenerating family on an expanding domain.

### 2.3 Albritton--Beekie--Novack

D. Albritton, R. Beekie, and M. Novack, “Enhanced dissipation and
Hörmander’s hypoellipticity,” *Journal of Functional Analysis* 283 (2022),
109522.

- Primary preprint: [arXiv:2105.12308](https://arxiv.org/abs/2105.12308)
- Journal DOI: [10.1016/j.jfa.2022.109522](https://doi.org/10.1016/j.jfa.2022.109522)

This work proves spacetime subelliptic estimates for fixed finite-type shear
flows on periodic or bounded cross-sections and explains enhanced dissipation
through Hörmander brackets.  It is methodologically close to R0.72V’s direct
spacetime graph approach.

**Boundary:** the stated theorem still fixes the shear type.  It does not give
one constant through a critical-point merger, an unbounded polynomial-tail
family, or the exact heat-path transfer used here.

### 2.4 Li--Zhang on an unbounded cross-section

T. Li and L. Zhang, “Enhanced dissipation and Taylor dispersion by a parallel
shear flow in an infinite cylinder with unbounded cross section,” preprint
(2025).

- Primary source: [arXiv:2510.13097](https://arxiv.org/abs/2510.13097)

Theorem 1.1 treats a fixed autonomous profile on an unbounded one-dimensional
cross-section under a finite-type condition and a nondegenerate tail.  It
gives the expected rate

\[
 \nu^{m/(m+2)}|k|^{2/(m+2)}
\]

in the enhanced-dissipation regime.

**Boundary:** this is the closest autonomous whole-line comparison, but the
constant depends on the fixed profile’s finite-type and tail geometry.  No
uniform statement is made for

\[
 H_3-\frac\epsilon4H_5+
 \frac{\epsilon^2}{40}H_7,
 \qquad\epsilon\downarrow0,
\]

and frozen-time estimates cannot be concatenated into the required
nonautonomous graph theorem.

---

## 3. Time-dependent shear results and the collision boundary

### 3.1 Coble--He

D. Coble and S. He, “A Note on Enhanced Dissipation and Taylor Dispersion of
Time-dependent Shear Flows,” *Communications in Mathematical Sciences* 22
(2024), 1685--1700.

- Primary preprint: [arXiv:2309.15738](https://arxiv.org/abs/2309.15738)
- Journal DOI: [10.4310/CMS.2024.v22.n6.a10](https://doi.org/10.4310/CMS.2024.v22.n6.a10)

Theorem 1.2 assumes that the target and reference shear share a fixed finite
number $N$ of nondegenerate critical points.  Their fixed-radius
neighborhoods remain pairwise disjoint, and

\[
 |V_y(t,y)|\asymp|y-y_i(t)|
\]

near each point.  Those assumptions fail exactly when two points merge.
Theorem 1.3 uses notation that permits a time-dependent number of critical
points, but it concerns low-frequency Taylor dispersion in a bounded
cross-section, not collision-scale enhanced dissipation on the expanding
torus.  The heat-path example in Remark 1.1 is a single decaying sine mode;
its critical topology never changes.

R0.72W therefore treats a geometric case excluded from the main
nondegenerate time-dependent theorem.  It does not contradict or improve the
rates within that theorem’s assumptions.

### 3.2 A rigidly translating critical set

M. Benthaus, G. M. Coclite, and C. Nobili, “Mixing and enhanced dissipation in
a time-translating shear flow,” preprint (2026).

- Primary source: [arXiv:2603.14624](https://arxiv.org/abs/2603.14624)

This is a relevant example where critical points move in time.  For the
translated sinusoidal profile, however, they remain simple, separated, and
constant in number.  Rigid translation does not model an $A_2$ merger.

---

## 4. Imaginary-potential maximal and semiclassical estimates

### 4.1 Helffer--Nourrigat and fixed polynomial graph domains

B. Helffer and J. Nourrigat, “On the domain of a magnetic Schrödinger
operator with complex electric potential,” preprint (2017).

- Primary source: [arXiv:1709.08542](https://arxiv.org/abs/1709.08542)
- Background theorem: J. Nourrigat, *Journal of Functional Analysis* 74
  (1987), [10.1016/0022-1236(87)90027-9](https://doi.org/10.1016/0022-1236(87)90027-9)

The maximal inequalities reviewed there show that a fixed real polynomial
potential has a natural complex Schrödinger graph domain and estimates that
control the second derivative and multiplication by that fixed potential.

**Boundary:** a theorem for each fixed polynomial does not supply one constant
as its leading degree degenerates with $\epsilon$.  Nor does it give the
nonautonomous negative-Sobolev estimate of R0.72W.  A nilpotent-representation
route would require a separate proof that the entire degenerating family lies
in one closed cone and that every limiting representation is injective; that
work is not assumed here.

### 4.2 Arnaiz--Bony--Michel

V. Arnaiz, J.-F. Bony, and L. Michel, “Semiclassical Schrödinger operators
with purely imaginary potential,” preprint (2026).

- Primary source: [arXiv:2607.07301](https://arxiv.org/abs/2607.07301)

For fixed potentials on bounded domains, the paper identifies the low-end
spectrum and resolvent scale from homogeneous models at degenerate critical
points.  A cubic model produces the familiar $h^{6/5}$ semiclassical scale,
consistent with the physical $\nu^{3/5}|k|^{2/5}$ calibration.

**Boundary:** the potential and critical models are fixed.  The paper does
not state an all-$\alpha$ nonautonomous graph theorem through a merger, and
its bounded-domain spectral result is not the expanding-torus transfer proved
in R0.72W.

### 4.3 Arnal--Siegl

A. Arnal and P. Siegl, “Resolvent estimates for one-dimensional Schrödinger
operators with complex potentials,” *Journal of Functional Analysis* 284
(2023), 109856.

- Primary preprint: [arXiv:2203.15938](https://arxiv.org/abs/2203.15938)
- Journal DOI: [10.1016/j.jfa.2023.109856](https://doi.org/10.1016/j.jfa.2023.109856)

The paper gives high-energy resolvent asymptotics for fixed unbounded complex
potentials, with local Airy models at turning points.  It informs a possible
outer-region resolvent analysis, but does not give uniform constants when
turning points merge or a time-dependent $H^{-1}$ graph estimate.

---

## 5. Why abstract unbounded-perturbation theory is not a shortcut

Abstract nonautonomous evolution theorems for graph-bounded perturbations
require the perturbation to map the reference graph domain with a controlled
relative norm.  That hypothesis is exactly what fails here.  For a translated
unit bump,

\[
 \frac{\|x^5u_R\|}{
 \|(-\partial_x^2+ix^3)u_R\|}
 \asymp R^2.
\]

After removing scalar phases, the same failure persists in the spatial odd
part.  Therefore $H_5$ and $H_7$ cannot be inserted as ordinary small
unbounded perturbations of the cubic generator.  R0.72W’s direct theorem for
the exact sine family is not merely one proof choice; it avoids a genuinely
false hypothesis.

---

## 6. What the literature supports, and what R0.72W adds

The primary sources support four contextual statements:

- finite-order critical points produce enhanced-dissipation scales determined
  by their local order;
- direct spacetime subelliptic estimates can replace autonomous spectral
  arguments;
- slowly moving, still-separated nondegenerate critical points can be handled
  by time-dependent hypocoercivity;
- fixed imaginary polynomial potentials possess strong maximal graph
  estimates.

They do not directly supply the result needed here.  R0.72W proves its exact
family theorem by a separate compact--escaping argument:

- bounded cell coefficients force convergence either to a nonconstant exact
  trigonometric chart or to the translated cubic collision chart;
- escaping coefficients have a uniformly positive normalized variance;
- the heat identity keeps their direction slow enough for the scalar endpoint
  ledger;
- disjoint-cell $H^{-1}$ duality globalizes the estimate without tail weights;
- the exact sine tail is retained rather than expanded globally.

The bounded search did not find this precise theorem already packaged in the
literature.  That statement is only a search result, not a claim of first
proof or priority.  Independent expert review remains necessary before any
publication-level novelty statement.
