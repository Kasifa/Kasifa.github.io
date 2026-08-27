# R0.72S literature audit: singular strata, time-dependent shear, and the Clay boundary

**Date:** 2026-08-28

**Status:** primary-source boundary audit

**Scope:** the fixed-first-harmonic real trigonometric family used in R0.72S, its
local \(A_k\) incidence geometry, stationary and nonautonomous enhanced
dissipation, and the logical relation to the three-dimensional Navier--Stokes
Millennium Problem.

This document is deliberately narrower than a survey.  It checks the claims
needed by R0.72S against original papers, publisher records, arXiv manuscripts,
and the official Clay problem statement.  It separates three different things:

1. what the cited literature proves;
2. what the exact algebra in R0.72S proves independently;
3. what remains unsupported or open.

The search was bounded and source-constrained.  It stopped after the relevant
Arnol'd, Voorhaar, stationary-shear, nonautonomous-shear, and Clay source lanes
converged and further targeted queries returned the same papers.  Failure to
locate an exact prior result is reported only as a **bounded-search absence**.
It is not a proof of novelty, priority, or completeness of the literature.

## 1. Direct conclusion

The local singularity claims in R0.72S are compatible with the standard
Arnol'd conventions provided that the word *versal* is qualified.  The
four coefficient directions constitute a restricted miniversal, or
\(R^+\)-versal, unfolding for critical-point geometry modulo additive
constants.  In that convention a local \(A_k\) branch has coefficient-space
codimension \(k-1\).

The existing literature does not supply a global stratification of the
fixed-first-harmonic \(\mathbb C^2\cong\mathbb R^4\) real unit-circle caustic.
Arnol'd's 1997 result gives the topology of the maximal-real-critical region
in a different normalization; Voorhaar's 2023 result computes a Newton
polytope in a complex Laurent coefficient space; Esterov--Voorhaar 2024
explicitly leaves higher-codimension Lyashko--Looijenga strata as a question.
None of these results by itself classifies the image self-intersections,
multisingularities, or all real complement chambers used by R0.72S.

Stationary finite-type theory gives the frozen-profile benchmarks
\(\nu^{3/5}\) at an \(A_2\) shear critical point and \(\nu^{2/3}\) at an
\(A_3\) point.  Existing nonautonomous theorems cover slowly moving
nondegenerate critical points, time modulation of a fixed spatial profile,
or rigid translation of a fixed simple-critical profile.  The bounded search
did not locate an enhanced-dissipation theorem uniform through the creation,
annihilation, or collision of critical points at an \(A_2\) or \(A_3\) event.

Consequently R0.72S supplies a useful geometric input for a possible new
nonautonomous PDE model, but it is not a regularity result for general
three-dimensional Navier--Stokes data and does not discharge any clause of
the Clay problem.

## 2. Conventions that must be fixed before stating the theorem

For a one-variable function germ, the standard complex normal form is

\[
 A_k:\qquad x^{k+1},
\]

so that

\[
 \begin{aligned}
 A_2 &: f'=f''=0,\quad f'''\ne0,\\
 A_3 &: f'=f''=f'''=0,\quad f''''\ne0.
 \end{aligned}
\]

Arnol'd distinguishes two parameter counts.  A full miniversal deformation
of an isolated germ of multiplicity \(\mu\) has \(\mu\) parameters.  After
fixing the critical value, or equivalently working modulo an arbitrary
additive constant for critical-point geometry, the restricted miniversal
deformation has \(\mu-1\) parameters.  Since \(A_k\) is simple and
\(\mu=k\), its codimension in the space of germs with critical point and
critical value fixed is

\[
 \operatorname{codim} A_k=k-1.
\]

These statements are found in V. I. Arnol'd,
[*Critical points of smooth functions and their normal forms*](https://www.mathnet.ru/eng/rm4237),
Russian Mathematical Surveys **30** (1975), Section 5, p. 8; Section 6,
pp. 10--11; the relation \(\mu=c+m+1\) on p. 24; and the simple-series list
in Section 13, p. 27
([DOI](https://doi.org/10.1070/RM1975v030n05ABEH001521)).  The original
normal-form paper is Arnol'd,
[*Normal forms for functions near degenerate critical points...*](https://www.mathnet.ru/eng/faa2531),
Functional Analysis and Its Applications **6** (1972), 254--272
([DOI](https://doi.org/10.1007/BF01077644)).

Accordingly, the determinant computation in R0.72S supports the phrase

> restricted miniversal, or \(R^+\)-versal, unfolding for critical-point
> geometry modulo additive constants,

not the unqualified claim that four coefficient parameters form the full
miniversal unfolding of \(A_5\).  The latter would also include the constant
direction and would have five parameters.

For a refined real classification, signs must also be tracked when the two
real normal forms are inequivalent.  Labels such as \(A_3^+\) and \(A_3^-\)
may therefore be required if the report later claims a complete real
stratification.  The unsigned \(A_k\) label is sufficient when only the
order of vanishing and local codimension are being recorded.

## 3. Claim-to-source gap matrix

| Candidate claim | Primary source and exact location | Exact support | What the source does not imply | Confidence |
|---|---|---|---|---|
| The \(A_k\) incidence type and local codimension are determined by the first nonzero higher derivative | Arnol'd 1975, Sections 5--6, pp. 8--11; p. 24; Section 13, p. 27 | \(A_k\sim x^{k+1}\), \(\mu=k\), and restricted codimension \(k-1\) for a simple germ | It does not verify the R0.72S jet identities or determinant; those are supplied by the report's exact calculation | High |
| The four R0.72S coefficient directions give versality through \(A_5\) | Arnol'd 1975, Section 5, p. 8 and Section 6, p. 10 | Transversality to the right-equivalence orbit is the versality criterion; modulo constants the required dimension is \(\mu-1=4\) | Four directions do not give the five-parameter full miniversal deformation including constants; the determinant must be interpreted in the restricted or \(R^+\) category | High |
| The locus \(f'=f''=0\) is the Morse discriminant | Arnol'd 1975, Section 6, p. 11; Voorhaar 2023, Definitions 1.1--1.4, p. 2 | The multiple-critical-point locus is the caustic.  The Maxwell stratum records distinct critical points with equal critical values.  Voorhaar's Morse discriminant contains both and uses the equation \(h_m^2h_c\) when both are hypersurfaces | The R0.72S incidence is only the caustic unless the Maxwell stratum is also analyzed | High |
| The topology of real degree-three trigonometric-polynomial regions was previously unknown | Arnol'd, [*Topological classification of real trigonometric polynomials and cyclic serpents polyhedron*](https://link.springer.com/chapter/10.1007/978-1-4612-4122-5_4), 1997, pp. 103--105, especially Theorem 3 on p. 104 | In the normalization \(\cos nt+\sum_{0<k<n}(a_k\cos kt+b_k\sin kt)\), the region with all \(2n\) critical points real is modeled by the cyclic serpent polyhedron; proper \(M\)-polynomials form its interior | It does not classify the regions with four or two real critical points, the complete caustic, all complement components, or the R0.72S heat paths | High |
| Arnol'd's 1997 coefficient space is disjoint from the R0.72S four-dimensional family | Arnol'd 1997, p. 103 | Both are four-dimensional normalizations of the degree-three quotient | The charts overlap where both the first and third harmonics are nonzero: phase translation and amplitude scaling change one normalization into the other.  A chart-change argument is required before importing topology | High |
| The exact \(1{:}2\) astroid is established | Arnol'd, [*Astroidal geometry of hypocycloids and the Hessian topology of hyperbolic polynomials*](https://www.mathnet.ru/eng/rm452), Russian Mathematical Surveys **56** (2001), Theorem 4, pp. 1023--1024 and Section 9, pp. 1053--1054 ([DOI](https://doi.org/10.1070/RM2001v056n06ABEH000452)) | A periodic-function caustic has at least four cusps in the stated generic setting; the caustic of the double-angle cosine with first-harmonic parameters is an astroid, with four real critical points inside and two outside | This is a two-parameter \(1{:}2\) result, not a four-dimensional \(1{:}2{:}3\) caustic classification | High |
| Voorhaar 2023 gives a global coefficient-space stratification usable directly for R0.72S | A. Voorhaar, [*The Newton Polytope of the Morse Discriminant of a Univariate Polynomial*](https://arxiv.org/abs/2104.05123), Definitions 1.1--1.4 and Assumption 1.6, p. 2; Proposition 3.10, p. 9; Theorem 3.14, p. 10; Corollary 3.23, p. 12; Advances in Mathematics **432** (2023), 109275 ([DOI](https://doi.org/10.1016/j.aim.2023.109275)) | The paper works in the complex Laurent coefficient space \(\mathbb C^A\), defines the complex caustic and Maxwell stratum, and computes the Newton polytope of the Morse discriminant using tropical combinatorial data | A Newton polytope or tropical cone decomposition is not a real self-conjugate unit-circle chamber decomposition.  It gives neither real critical-point counts nor all \(A_k\) strata of the R0.72S slice.  Assumption 1.6 must also be checked for the declared support and gauge | High |
| Esterov--Voorhaar 2024 settles higher-codimension Morse strata | A. Esterov and A. Voorhaar, [*Basecondary polytopes*](https://arxiv.org/abs/2411.02234), Definition 1.6, pp. 3--4 and Question 1.7, p. 4 | The basecondary framework gives the codimension-one tropical Morse-discriminant result | The authors explicitly state the higher-\(k\) Lyashko--Looijenga singularity-stratum problem as a question.  It cannot be cited as a global \(A_3\) or higher-codimension classification | High |
| A stationary \(A_2\) or \(A_3\) shear has a known finite-type enhanced-dissipation scale | J. Bedrossian and M. Coti Zelati, [arXiv:1510.08098](https://arxiv.org/abs/1510.08098), Theorem 1.1, p. 2 ([DOI](https://doi.org/10.1007/s00205-017-1099-y)); D. Albritton, R. Beekie, M. Novack, [arXiv:2105.12308](https://arxiv.org/abs/2105.12308), equations (1.2), p. 2 and Theorem 1.1, p. 3 ([DOI](https://doi.org/10.1016/j.jfa.2022.109522)) | For a fixed shear whose derivative has maximal finite vanishing order \(N\), the decay exponent is \((N+1)/(N+3)\), up to the logarithmic issue in the earlier periodic theorem.  Frozen \(A_2\) and \(A_3\) profiles therefore give rates \(\nu^{3/5}\) and \(\nu^{2/3}\) | These are autonomous estimates.  They cannot be patched pointwise in time to give a uniform estimate through a changing critical-point multiplicity | High |
| Existing time-dependent enhanced-dissipation theory covers the R0.72S collisions | D. Coble and S. He, [*A Note on Enhanced Dissipation and Taylor Dispersion of Time-dependent Shear Flows*](https://arxiv.org/abs/2309.15738), Theorem 1.2, pp. 3--4 and Remark 1.2, p. 4 ([DOI](https://doi.org/10.4310/CMS.2024.v22.n6.a10)) | The enhanced-dissipation theorem assumes a fixed finite number of common nondegenerate critical points, disjoint fixed-radius neighborhoods, uniform quadratic shape, and slow reference motion \(\|\partial_{ty}U\|_\infty\leq\nu^{3/4}\) | Those assumptions fail at critical-point creation or collision.  Theorem 1.3 permits finite-order degeneracy only in its Taylor-dispersion regime; it is not an ED-through-collision theorem | High |
| Later nonautonomous results remove the collision gap | J. Benthaus and C. Nobili, [*Enhanced Dissipation via time-modulated velocity fields*](https://arxiv.org/abs/2501.16905), 2025 ([DOI](https://doi.org/10.3934/eect.2025051)); J. Benthaus, G. M. Coclite, C. Nobili, [*Mixing and enhanced dissipation in a time-translating shear flow*](https://arxiv.org/abs/2603.14624), 2026, Theorem 2, p. 7 | The 2025 paper treats \(v(y,t)=\xi(t)w(y)\), so the spatial profile is fixed.  The 2026 paper proves ED for the rigidly translating profile \(\sin(y-ct)\) and therefore genuinely treats moving critical points | In both models the spatial critical-point type and count are fixed.  Neither theorem crosses an \(A_2\) or \(A_3\) creation--annihilation event | High for scope; medium for the absence claim |
| R0.72S advances the Clay Millennium Problem directly | C. L. Fefferman, [*Existence and Smoothness of the Navier--Stokes Equation*](https://www.claymath.org/wp-content/uploads/2022/06/navierstokes.pdf), official Clay statement, pp. 1--2, alternatives (A)--(D) | The problem asks for global smooth solutions for arbitrary smooth divergence-free three-dimensional data on \(\mathbb R^3\) or the periodic domain, or a valid breakdown example | Finite-harmonic shear geometry and passive-scalar or triangular enhanced dissipation do not control general pressure coupling, vortex stretching, nonlinear perturbations, or arbitrary data | High |

## 4. Consequences for the precise R0.72S claims

### 4.1 Claims that survive the literature audit

The following statements are not contradicted or subsumed by the sources
above, provided that their proofs in R0.72S are correct:

1. the explicit partition of the declared incidence parameter space into
   \(A_2,A_3,A_4,A_5\) preimages;
2. the absence of higher \(A_k\) within that fixed-first-harmonic incidence;
3. restricted local versality through \(A_5\), certified by the coefficient
   jet determinant;
4. a full-family transverse \(A_2\) heat-law crossing with an exact global
   critical-point count;
5. a symmetry-restricted \(A_3\) passage in the real-even slice with an exact
   global count and square-root branch law.

These are local or pathwise results.  They are not a classification of the
whole caustic image.

### 4.2 Terms likely to draw a referee objection

**Unqualified versal unfolding.**  The report should use *restricted
miniversal* or *\(R^+\)-versal modulo constants*.  The difference is not
cosmetic: the full \(A_5\) miniversal base has dimension five, whereas the
critical-point caustic base modulo constants has dimension four.

**Full-space transverse \(A_3\).**  In the fixed-first-harmonic
\(\mathbb R^4\) slice, a local \(A_3\) branch has codimension two.  A
one-dimensional curve that hits it cannot be transverse to it in
\(\mathbb R^4\), because its tangent supplies only one of the two normal
directions.  A generic one-parameter full-family path avoids \(A_3\).
The defensible alternatives are:

1. a one-parameter symmetry-forced \(A_3\) passage, transverse only inside
   the real-even two-dimensional slice; or
2. a two-parameter full-family transverse unfolding of \(A_3\).

**Full coefficient space.**  The phrase must identify the space.  The R0.72S
space is the fixed-first-harmonic slice
\(\mathbb C^2\cong\mathbb R^4\), not the six-real-dimensional space of all
nonconstant real trigonometric polynomials of degree three and not
Voorhaar's independent complex Laurent coefficient space \(\mathbb C^A\).

**M-polynomial versus Morse polynomial.**  Arnol'd's \(M\)-polynomial means
that all \(2n\) possible critical points are real.  Voorhaar's *Morse*
condition means nondegenerate critical points with distinct critical values.
The two terms must not be identified.

**Caustic versus Morse discriminant.**  The caustic records degenerate
critical points; the Morse discriminant also contains the Maxwell stratum.
R0.72S presently studies the former.

**Incidence classification versus image stratification.**  A complete list
of incidence preimage types does not determine injectivity of the incidence
map.  A single coefficient pair may support more than one degenerate
critical point, producing self-intersections and multisingularity strata.
All such image questions remain separate.

**Enhanced dissipation through degeneracy.**  A stationary theorem applied
to frozen profiles is a benchmark, not a nonautonomous theorem.  Uniform
constants, localization radii, and spectral gaps may all degenerate at the
collision.  R0.72S should not infer a PDE estimate from the two local
square-root laws alone.

## 5. What was and was not located for the exact \(1{:}2{:}3\) problem

The primary-source search located three close predecessors:

1. Arnol'd 1997 gives the topology of the degree-\(n\) maximal-real-critical
   \(M\)-polynomial region, including the four-dimensional \(n=3\) quotient;
2. Arnol'd 2001 gives the exact two-parameter \(1{:}2\) astroidal caustic and
   general periodic-caustic cusp geometry;
3. Voorhaar 2023 and Esterov--Voorhaar 2024 give complex-algebraic and
   tropical information about the Laurent-polynomial Morse discriminant.

Within the bounded search, no primary source was located that gives all of
the following package:

1. the fixed-first-harmonic \(1{:}2{:}3\) real unit-circle incidence formulas;
2. the complete local \(A_2/A_3/A_4/A_5\) preimage partition used by R0.72S;
3. the two declared heat-law paths and their exact distinct-point sequences
   \(4/3/2\) and \(4/2/2\);
4. a complete global stratification of the corresponding four-real-dimensional
   caustic image.

The first three items may therefore be described as **not located in this
bounded primary-source search**.  They must not be described as the first
such results in the literature without a broader novelty search.  The fourth
item is not proved by R0.72S either.

Arnol'd's fixed-highest-harmonic chart and the R0.72S fixed-first-harmonic
chart overlap whenever both harmonics are nonzero.  Consequently no novelty
claim should be based merely on the different normalization.  Any comparison
with Arnol'd's degree-three region should state the phase-and-amplitude chart
change explicitly and distinguish the six-, four-, and two-real-critical
regions.

## 6. Enhanced-dissipation boundary and the next defensible PDE question

The stationary theory is sufficiently strong to identify the two frozen
scales:

\[
 A_2:\quad t_{\mathrm{ED}}\sim\nu^{-3/5},
 \qquad
 A_3:\quad t_{\mathrm{ED}}\sim\nu^{-2/3}.
\]

It does not determine the scale near a time-dependent collision.  Coble--He
requires uniform nondegeneracy and a fixed critical-point structure.  The
2025 time-modulation paper changes only the temporal amplitude of a fixed
spatial shear.  The 2026 rigid-translation paper moves simple critical points
but preserves their multiplicity and count.  These results show that
nonautonomous enhanced dissipation itself is no longer the missing concept;
the unresolved mechanism is specifically **enhanced dissipation through a
change of critical-point multiplicity**.

The next defensible research question is therefore local and model-specific:

> Can one prove a viscosity-uniform subelliptic or hypocoercive estimate for
> the spacetime normal form of the explicit R0.72S \(A_2\) collision, and
> then perturbatively transfer it to the exact heat path?

That question is not answered by the sources audited here.  A proof would be
a genuine PDE result independent of any claim about the full caustic or the
Clay problem.

## 7. Boundary with the three-dimensional Navier--Stokes problem

The official Clay formulation asks for one of four outcomes: global smooth
solutions for arbitrary smooth divergence-free data on \(\mathbb R^3\) or
the periodic three-torus, or a valid breakdown construction in one of those
settings.  R0.72S instead concerns explicit finite-harmonic shear profiles
inside a special scalar or triangular mechanism.

Even a successful collision-uniform enhanced-dissipation theorem would not
by itself provide:

1. an a priori bound for arbitrary three-dimensional Navier--Stokes data;
2. control of general vortex stretching and pressure coupling;
3. a nonlinear perturbation theorem covering all modes and amplitudes;
4. either global regularity or a finite-time singular solution.

The direct Clay value of the current result is therefore low.  Its more
realistic value is as a precise finite-dimensional singularity ledger and a
test case for a nonautonomous enhanced-dissipation mechanism that existing
theorems do not cover.  That can support a serious standalone PDE project,
but it must not be presented as a partial solution or a measurable fraction
of the Millennium Problem.

## 8. Canonical primary references

1. V. I. Arnol'd, *Normal forms for functions near degenerate critical
   points, the Weyl groups of \(A_k,D_k,E_k\) and Lagrangian singularities*,
   Functional Analysis and Its Applications **6** (1972), 254--272,
   [official record](https://www.mathnet.ru/eng/faa2531),
   [DOI](https://doi.org/10.1007/BF01077644).
2. V. I. Arnol'd, *Critical points of smooth functions and their normal
   forms*, Russian Mathematical Surveys **30** (1975), 1--75,
   [official record](https://www.mathnet.ru/eng/rm4237),
   [DOI](https://doi.org/10.1070/RM1975v030n05ABEH001521).
3. V. I. Arnold, *Topological classification of real trigonometric
   polynomials and cyclic serpents polyhedron*, in *The Arnold--Gelfand
   Mathematical Seminars*, Birkhäuser, 1997, pp. 101--106,
   [publisher record](https://link.springer.com/chapter/10.1007/978-1-4612-4122-5_4).
4. V. I. Arnol'd, *Astroidal geometry of hypocycloids and the Hessian
   topology of hyperbolic polynomials*, Russian Mathematical Surveys **56**
   (2001), 1019--1083,
   [official record](https://www.mathnet.ru/eng/rm452),
   [DOI](https://doi.org/10.1070/RM2001v056n06ABEH000452).
5. A. Voorhaar, *The Newton Polytope of the Morse Discriminant of a
   Univariate Polynomial*, Advances in Mathematics **432** (2023), 109275,
   [arXiv manuscript](https://arxiv.org/abs/2104.05123),
   [DOI](https://doi.org/10.1016/j.aim.2023.109275).
6. A. Esterov and A. Voorhaar, *Basecondary polytopes*, 2024,
   [arXiv manuscript](https://arxiv.org/abs/2411.02234).
7. J. Bedrossian and M. Coti Zelati, *Enhanced dissipation,
   hypoellipticity, and anomalous small noise inviscid limits in shear
   flows*, Archive for Rational Mechanics and Analysis **224** (2017),
   1161--1204, [arXiv manuscript](https://arxiv.org/abs/1510.08098),
   [DOI](https://doi.org/10.1007/s00205-017-1099-y).
8. D. Albritton, R. Beekie, and M. Novack, *Enhanced dissipation and
   Hörmander's hypoellipticity*, Journal of Functional Analysis **283**
   (2022), 109522, [arXiv manuscript](https://arxiv.org/abs/2105.12308),
   [DOI](https://doi.org/10.1016/j.jfa.2022.109522).
9. D. Coble and S. He, *A Note on Enhanced Dissipation and Taylor
   Dispersion of Time-dependent Shear Flows*, Communications in Mathematical
   Sciences **22** (2024), 1685--1700,
   [arXiv manuscript](https://arxiv.org/abs/2309.15738),
   [DOI](https://doi.org/10.4310/CMS.2024.v22.n6.a10).
10. J. Benthaus and C. Nobili, *Enhanced Dissipation via time-modulated
    velocity fields*, Evolution Equations and Control Theory (2025),
    [arXiv manuscript](https://arxiv.org/abs/2501.16905),
    [DOI](https://doi.org/10.3934/eect.2025051).
11. J. Benthaus, G. M. Coclite, and C. Nobili, *Mixing and enhanced
    dissipation in a time-translating shear flow*, 2026,
    [arXiv manuscript](https://arxiv.org/abs/2603.14624), especially
    Theorem 2, p. 7.
12. C. L. Fefferman, *Existence and Smoothness of the Navier--Stokes
    Equation*, official Clay Millennium Problem description,
    [Clay Mathematics Institute PDF](https://www.claymath.org/wp-content/uploads/2022/06/navierstokes.pdf),
    especially pp. 1--2.

## 9. Audit verdict

R0.72S can responsibly claim an exact local incidence ledger and two
globally counted heat-law collisions in its declared fixed-first-harmonic
family.  It should claim restricted versality, not unqualified versality;
slice-transverse, not full-space-transverse, \(A_3\) passage; caustic, not
the whole Morse discriminant; and bounded-search absence, not novelty.

The literature boundary is equally clear on the PDE side: stationary
finite-type rates are available, and moving nondegenerate critical points
are now covered, including rigid translation.  Uniform enhanced dissipation
through a change in critical-point multiplicity was not located.  Proving
that estimate is the next serious mathematical gate.  It remains a special
PDE problem and not a resolution of the three-dimensional Navier--Stokes
Millennium Problem.
