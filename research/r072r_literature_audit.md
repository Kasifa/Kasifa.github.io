# R0.72R literature and claim-boundary audit

**Date:** 2026-08-28

**Search type:** bounded primary-source search.  This file records overlap and
claim boundaries; it is not a novelty or priority certificate.

## 1. Decision

The following statements must not be presented as new:

1. caustics of a periodic function under variation of its first harmonic;
2. generic cusp geometry for those caustics;
3. the existence and topology of maximal-real-critical-point regions for
   degree-three real trigonometric polynomials;
4. enhanced dissipation for a stationary shear with a finite-order degenerate
   critical point.

The defensible R0.72R increment is narrower: an explicit rational polydisc

\[
 |z_2-3/20|\le1/100,\qquad |z_3|\le1/1000
\]

in the fixed-first-harmonic four-real-dimensional coefficient slice, together
with quantitative normalized root localization for every \(y\ge0\).  On the
declared physical cell \(0\le y\le1\), it also supplies shape and derivative
budgets plus a family-uniform enhanced-dissipation corollary for the fixed
commensurate \(1{:}2{:}3\) triangular affine-row reduction.  The whole initial
polydisc satisfies \(Q_2>1/2\), so it lies outside the sufficient cone of
R0.72Q.

## 2. Primary-source overlap matrix

| Topic | Primary source | What the source supplies | What remains specific to R0.72R |
|---|---|---|---|
| Periodic-function caustics | V. I. Arnol'd, *Astroidal Geometry of Hypocycloids and the Hessian Topology of Hyperbolic Polynomials*, RMS 56 (2001), [DOI](https://doi.org/10.1070/RM2001v056n06ABEH000452) | For \(G=A\cos\phi+B\sin\phi+g(\phi)\), solves \(G'=G''=0\) as a caustic parameterization and studies generic cusps | The fixed-first-harmonic \((z_2,z_3)\in\mathbb C^2\) coordinate slice, the explicit polydisc, rational margins, and heat path |
| Degree-three real chamber topology | V. I. Arnol'd, *Topological Classification of Real Trigonometric Polynomials and Cyclic Serpents Polyhedron*, 1997, [chapter record](https://link.springer.com/chapter/10.1007/978-1-4612-4122-5_8) | Describes proper M-polynomial regions through cyclic-serpent polyhedra; for degree three the maximal region has the known product-of-simplices topology | No claim of discovering that chamber; R0.72R supplies one quantitative compact core and a dynamic certificate |
| Laurent-polynomial caustic and Morse discriminant | A. Voorhaar, *The Newton Polytope of the Morse Discriminant of a Univariate Polynomial*, Adv. Math. 432 (2023), [DOI](https://doi.org/10.1016/j.aim.2023.109275) | Defines the caustic and studies its complex Newton-polytope structure | A complex resultant is not the real self-inversive unit-circle condition; the real incidence and margins are derived here |
| Time-dependent nondegenerate shear ED | D. Coble and S. He, *A Note on Enhanced Dissipation of Time-Dependent Shear Flows*, CMS 22 (2024), [DOI](https://doi.org/10.4310/CMS.2024.v22.n6.a10) | Theorem 1.2 and Appendix A give \(\eta^{1/2}\)-scale decay under slow motion and uniform nondegenerate shape hypotheses | On \(0\le y\le1\), R0.72R verifies one common set of hypotheses over the full polydisc for the fixed commensurate \(1{:}2{:}3\) triangular affine-row reduction; the family statement is a proof-level extraction, not a verbatim theorem |
| Stationary degenerate shear ED | J. Bedrossian and M. Coti Zelati, ARMA 224 (2017), [DOI](https://doi.org/10.1007/s00205-017-1099-y) | Degeneracy-dependent stationary enhanced-dissipation scale, originally with logarithmic loss | Does not treat nonautonomous crossing of a caustic |
| Sharp stationary finite-type scale | D. Albritton, R. Beekie, and M. Novack, JFA 283 (2022), [DOI](https://doi.org/10.1016/j.jfa.2022.109522) | Removes the logarithmic loss and gives the finite-type benchmark | Supplies the next-gate benchmark, not the present time-dependent family theorem |

## 3. Exact caustic language

For

\[
 f(\phi)=\cos\phi+\operatorname{Re}(z_2e^{2i\phi}+z_3e^{3i\phi}),
\]

the coefficient space is \(\mathbb C^2\cong\mathbb R^4\).  For a fixed
\(\phi\), the equations \(f'=f''=0\) impose two real linear constraints.
Allowing \(\phi\) to vary therefore produces a generically three-real-
dimensional incidence hypersurface, not one planar curve.  A curve appears
only after a two-dimensional slice has been declared.

The complement components are open and hence are not compact.  The correct
object in R0.72R is a compact core contained in one component, not a compact
component of the complement.

The condition \(\operatorname{Disc}_uD=0\) for an unconstrained complex
polynomial is also too broad.  It includes repeated roots away from the unit
circle and possible degree-loss factors.  The exact real condition retained
in the report is

\[
 \exists |u|=1:\quad D(u)=D'(u)=0.
\]

## 4. Degeneracy terminology

For a one-variable function germ, a Morse critical point is \(A_1\).
At a caustic point, \(f'=f''=0\) and generically \(f'''\ne0\), giving an
\(A_2\) fold.  If \(f'''=0\) and \(f''''\ne0\), the point is \(A_3\).
These names follow Arnol'd's singularity classification; any claim about the
global \(A_2/A_3\) strata in the four-dimensional slice still requires a
separate transversality and self-intersection analysis.

## 5. Enhanced-dissipation boundary

Coble--He's hypotheses exclude the collision of critical points because they
require a fixed number of nondegenerate critical points and uniform local and
away-from-critical geometry.  On \(0\le y\le1\), R0.72R stays uniformly inside
those hypotheses for the fixed commensurate \(1{:}2{:}3\) triangular affine-row
reduction.

The stationary literature shows that degeneracy changes the decay scale; it
does not show that enhanced dissipation disappears.  Therefore the caustic
may be called a boundary of the present nondegenerate theorem, but not an
enhanced-dissipation failure wall.

## 6. Bounded-search result

The search covered the primary sources above, their stated theorems, and the
caustic/Morse-discriminant terminology.  It did not locate the exact R0.72R
polydisc with its normalized margins for every \(y\ge0\) and its fixed-pattern
Coble--He extraction on \(0\le y\le1\).  That absence is a limited search
result, not proof of global novelty.
