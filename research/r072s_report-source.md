# R0.72S report source: exact finite-harmonic singular strata and two heat-law collisions

**Date:** 2026-08-28
**Status:** exact analytic theorem for the declared incidence preimages and
two heat paths; global caustic-image classification and collision-scale PDE
estimates remain open

## 0. Scope and theorem statement

Consider the fixed-first-harmonic family

\[
 f(\phi;z_2,z_3)=\cos\phi+
 \operatorname{Re}\!\left(z_2e^{2i\phi}+z_3e^{3i\phi}\right),
 \qquad (z_2,z_3)\in\mathbb C^2.
 \tag{0.1}
\]

R0.72R gave an exact parameterization of the incidence
\(f'=f''=0\).  This report proves three narrower statements about that
incidence.

1. Every incidence preimage has one of the types \(A_2,A_3,A_4,A_5\), with
   exact equations in the incidence parameters.  No higher \(A_k\) occurs.
2. Modulo additive constants, the four coefficient directions give a
   restricted miniversal (\(R^+\)-versal) unfolding through \(A_5\).  Hence a
   single incidence branch of type \(A_k\) has local coefficient-space
   codimension \(k-1\).
3. Two explicit heat-law paths cross the wall at \(y_*=\log2\).  A generic
   full-family \(A_2\) fold has the exact distinct-point sequence \(4/3/2\),
   while a symmetry-restricted \(A_3\) collision has \(4/2/2\).  Both retain
   total multiplicity four at the crossing.

The first statement is a classification of **incidence preimages**.  It is
not a global classification of the image in \(\mathbb R^4\): one coefficient
pair may have more than one degenerate critical point, and the incidence map
may self-intersect.

---

## 1. Exact incidence and higher jets

At a degenerate critical point \(\phi\), write

\[
 z_3e^{3i\phi}=A+iB.
 \tag{1.1}
\]

The R0.72R incidence formulas are

\[
 z_3=(A+iB)e^{-3i\phi},
 \tag{1.2}
\]

\[
 z_2=e^{-2i\phi}\left[
 -\frac{\cos\phi+9A}{4}
 -\frac{i(\sin\phi+3B)}2
 \right].
 \tag{1.3}
\]

Substitution into the next four derivatives gives

\[
 f'''=3(5B-\sin\phi),
 \qquad
 f''''=3(15A-\cos\phi),
 \tag{1.4}
\]

\[
 f'''''=15(\sin\phi-13B),
 \qquad
 f''''''=15(\cos\phi-39A).
 \tag{1.5}
\]

These identities partition the incidence parameter space exactly:

\[
 \begin{array}{lll}
 \Sigma_2:& B\ne\sin\phi/5, & A_2,\\[2mm]
 \Sigma_3:& B=\sin\phi/5,\ A\ne\cos\phi/15, & A_3,\\[2mm]
 \Sigma_4:& B=\sin\phi/5,\ A=\cos\phi/15,\ \sin\phi\ne0,
 & A_4,\\[2mm]
 \Sigma_5:& (\phi,A,B)=(0,1/15,0)\ \text{or}\ (\pi,-1/15,0),
 & A_5.
 \end{array}
 \tag{1.6}
\]

Indeed, on the first two equalities defining \(\Sigma_4\),

\[
 f'''''=-24\sin\phi.
 \tag{1.7}
\]

If this also vanishes, then \(\phi=0\) or \(\pi\), and

\[
 f''''''=-24\cos\phi\ne0.
 \tag{1.8}
\]

Thus the list stops at \(A_5\).  Explicit representatives of the two higher
types are

\[
 (z_2,z_3,\phi)=\left(\frac45i,-\frac15,\frac\pi2\right)
 \quad(A_4),
 \tag{1.9}
\]

and

\[
 (z_2,z_3,\phi)=\left(-\frac25,\frac1{15},0\right)
 \quad(A_5).
 \tag{1.10}
\]

---

## 2. Local codimension and restricted miniversality

Use coefficient coordinates

\[
 (x_2,y_2,x_3,y_3)
 =(\operatorname{Re}z_2,\operatorname{Im}z_2,
   \operatorname{Re}z_3,\operatorname{Im}z_3).
 \tag{2.1}
\]

The four coefficient variations of \(f\) are

\[
 \cos2\phi,\quad-\sin2\phi,\quad
 \cos3\phi,\quad-\sin3\phi.
 \tag{2.2}
\]

Form the coefficient-derivative jet matrix whose rows are derivatives one
through four of these four functions at the declared critical point.  It is
not the order-zero-through-three Wronskian.  Rotation of \(\phi\) rotates the
two frequency blocks and does not change the determinant.  At \(\phi=0\),

\[
 W_0=
 \begin{pmatrix}
 0&-2&0&-3\\
 -4&0&-9&0\\
 0&8&0&27\\
 16&0&81&0
 \end{pmatrix},
 \qquad
 \boxed{\det W_0=5400.}
 \tag{2.3}
\]

Consequently the coefficient family controls all derivative jets of orders
one through four.  This is the restricted miniversal statement appropriate
to critical-point geometry modulo an additive constant.  A full miniversal
unfolding of \(A_5\) that also records the function-value direction would
need one additional constant parameter.

For \(2\le k\le5\), impose

\[
 f'=f''=\cdots=f^{(k)}=0,
 \qquad f^{(k+1)}\ne0
 \tag{2.4}
\]

in \(\mathbb T\times\mathbb R^4\).  The first \(k-1\) rows have independent
coefficient directions by (2.3), while the \(\phi\)-derivative supplies
\(f^{(k+1)}\) in the last row.  The constraint map therefore has rank \(k\).
Its solution set has dimension \(5-k\), and projection to coefficient space
is immersive on the type-\(A_k\) locus.  A single local image branch thus has

\[
 \boxed{\operatorname{codim}_{\mathbb R^4}A_k=k-1,
 \qquad 2\le k\le5.}
 \tag{2.5}
\]

Equation (2.5) is local.  It does not assert that the entire real caustic is
embedded or that its complement has been enumerated.

---

## 3. A generic \(A_2\) heat crossing with an exact global count

Let

\[
 z_{20}=4i,
 \qquad z_{30}=0,
 \qquad \tau=e^{-y},
 \tag{3.1}
\]

so that

\[
 F_y(\phi)=\cos\phi-4\tau^3\sin2\phi.
 \tag{3.2}
\]

Every normalized heat family used below satisfies the exact identity

\[
 \partial_yF=\partial_\phi^2F+F,
 \tag{3.2a}
\]

because the normalized harmonics \(n=1,2,3\) decay with exponents
\(0,3,8=n^2-1\).  Hence, at an incidence point,
\(\partial_yF'=F'''\) and \(\partial_yF''=F''''\).  This fixes the signs of
the time-transversality jets used in both paths.

Put \(k=8\tau^3\).  Then

\[
 F_y'(\phi)=-\sin\phi-k\cos2\phi
 =2k\sin^2\phi-\sin\phi-k.
 \tag{3.3}
\]

The two algebraic sine roots are

\[
 s_\pm(k)=\frac{1\pm\sqrt{1+8k^2}}{4k}.
 \tag{3.4}
\]

For every \(k>0\),

\[
 -1<s_-(k)<0.
 \tag{3.5}
\]

The other root satisfies

\[
 s_+(k)
 \begin{cases}
 >1,&0<k<1,\\
 =1,&k=1,\\
 <1,&k>1.
 \end{cases}
 \tag{3.6}
\]

The sign guard \(4k-1\ge0\) followed by squaring shows that
\(s_+(k)\le1\) is equivalent to \(k\ge1\).  Hence (3.5)--(3.6) give the
global critical-point count without numerical root finding.

The degeneracy equation is equally explicit:

\[
 F_y''(\phi)=\cos\phi\,(-1+4k\sin\phi).
 \tag{3.7}
\]

If \(\cos\phi\ne0\), simultaneous vanishing of (3.3) and (3.7) would require
\(\sin\phi=1/(4k)\), but substitution into (3.3) gives

\[
 -k-\frac1{8k}<0.
 \tag{3.8}
\]

If \(\cos\phi=0\), only \(\phi=\pi/2\), \(k=1\) solves (3.3).  Therefore
the full heat path has exactly one degenerate event:

\[
 y_*=\log2,
 \qquad \phi_*=\frac\pi2,
 \qquad z_2(y_*)=\frac i2,
 \qquad z_3(y_*)=0.
 \tag{3.9}
\]

At that point,

\[
 F'''=-3,
 \qquad \partial_yF'=-3.
 \tag{3.10}
\]

It is an \(A_2\) point, and the heat path is transverse to its local
codimension-one caustic branch in the fixed-first-harmonic coefficient slice
\(\mathbb C^2\cong\mathbb R^4\).  With
\(\delta=y-y_*\) and \(\xi=\phi-\phi_*\),

\[
 F_y'(\phi)=-3\delta-\frac32\xi^2
 +O(\delta^2+|\delta|\xi^2+\xi^4).
 \tag{3.11}
\]

The colliding branches obey

\[
 \xi_\pm=\pm\sqrt{-2\delta}+O(|\delta|^{3/2}),
 \qquad \delta\uparrow0.
 \tag{3.12}
\]

Since \(k>1\) exactly when \(y<\log2\), the number of distinct critical
points is

\[
 \boxed{
 \#\operatorname{Crit}(F_y)=
 \begin{cases}
 4,&0\le y<\log2,\\
 3,&y=\log2,\\
 2,&y>\log2.
 \end{cases}}
 \tag{3.13}
\]

At the middle line, one point is \(A_2\) and the other two are simple.
Counting multiplicity, the middle line has total count four.  After the
collision the two surviving real critical points are simple, so their real
multiplicity count is two; the vanished pair is not retained as a real
count.

---

## 4. A symmetry-restricted \(A_3\) heat crossing

Let

\[
 a_0=-\frac{2563}{1280},
 \qquad b_0=\frac1{30},
 \tag{4.1}
\]

and define the real-even heat path

\[
 H_y(\phi)=\cos\phi+a_0\tau^3\cos2\phi
 +b_0\tau^8\cos3\phi.
 \tag{4.2}
\]

Its derivative factors as

\[
 H_y'(\phi)=-\sin\phi\,q_\tau(\cos\phi),
 \tag{4.3}
\]

where

\[
 q_\tau(x)=12b_0\tau^8x^2+4a_0\tau^3x+1-3b_0\tau^8.
 \tag{4.4}
\]

For \(x\in[-1,1]\) and \(0<\tau\le1\),

\[
 \partial_xq_\tau(x)
 \le4\tau^3(a_0+6b_0\tau^5)
 \le4\tau^3\left(-\frac{2307}{1280}\right)<0.
 \tag{4.5}
\]

Thus \(q_\tau\) is strictly decreasing.  Its left endpoint is always
positive:

\[
 q_\tau(-1)=1-4a_0\tau^3+9b_0\tau^8>0.
 \tag{4.6}
\]

At the right endpoint, put

\[
 h(\tau)=q_\tau(1)=1+4a_0\tau^3+9b_0\tau^8.
 \tag{4.7}
\]

Then

\[
 h'(\tau)=12\tau^2(a_0+6b_0\tau^5)<0,
 \qquad h(1/2)=0.
 \tag{4.8}
\]

Equations (4.5)--(4.8) prove the full count.  If \(\tau>1/2\), there is
exactly one root of \(q_\tau\) in \((-1,1)\), producing two off-axis critical
points in addition to \(0\) and \(\pi\).  If \(\tau<1/2\), there is no
internal root.  Every off-axis root is simple because

\[
 H_y''=\sin^2\phi\,\partial_xq_\tau
 \quad\text{when }q_\tau(\cos\phi)=0.
 \tag{4.9}
\]

The endpoints are simple away from \(\tau=1/2\) by (4.6)--(4.8).  Therefore

\[
 \boxed{
 \#\operatorname{Crit}(H_y)=
 \begin{cases}
 4,&0\le y<\log2,\\
 2,&y\ge\log2,
 \end{cases}}
 \tag{4.10}
\]

where the point \(\phi=0\) at equality is degenerate and \(\phi=\pi\) is
simple.  Counting multiplicity, the crossing still has total count four.  At
the crossing,

\[
 a_*=-\frac{2563}{10240},
 \qquad b_*=\frac1{7680},
 \tag{4.11}
\]

\[
 \partial_xq_{1/2}(1)=-\frac{511}{512},
 \qquad H''''(0)=-\frac{1533}{512},
 \qquad \partial_yH''(0)=-\frac{1533}{512}.
 \tag{4.12}
\]

This is an \(A_3\) critical point.  Near \(\delta=y-y_*=0\), the two
off-axis branches satisfy

\[
 \phi_\pm=\pm\sqrt{-6\delta}+O(|\delta|^{3/2}),
 \qquad \delta\uparrow0.
 \tag{4.13}
\]

The path crosses the endpoint wall transversely **inside the real-even
two-dimensional slice**, because \(\partial_yh=1533/512\ne0\).  The full
\(A_3\) stratum has codimension two in \(\mathbb R^4\), so this one-dimensional
path is not called transverse in the full coefficient space.

---

## 5. What the two paths do and do not show

The two paths realize the same count change by different local mechanisms.

* In Section 3, two critical points annihilate at a generic \(A_2\) fold.
  The collision point itself disappears after the crossing.
* In Section 4, reflection symmetry keeps \(\phi=0\) critical for all time.
  Two off-axis points merge into it at an \(A_3\) event.

For a frozen stationary shear, the finite-type literature associates the
\(A_2\) profile with the \(\nu^{3/5}\) decay-rate benchmark and the \(A_3\)
profile with the \(\nu^{2/3}\) benchmark.  These are stationary statements.
They do not give a nonautonomous estimate across either collision.

Coble--He's time-dependent theorem assumes a fixed number of nondegenerate
critical points with common shape control.  Those hypotheses fail exactly at
\(y=\log2\) for both paths.  Benthaus--Nobili allow time modulation of a fixed
profile with simple critical points; that setting also does not cover a
critical-point collision.  Benthaus--Coclite--Nobili treat a rigidly
translating sine shear and therefore genuinely moving critical points, but
rigid translation preserves their type and number.  It also does not cover
the creation or annihilation in Sections 3--4.

---

## 6. Exact certificate contract

The finite certificate has two independent routes:

1. a Python producer using `fractions.Fraction` and exact integer
   determinants;
2. a JavaScript audit using a separate BigInt rational implementation.

Both routes machine-check only the following finite identities and sign-guard
inputs:

1. all incidence jets in (1.4)--(1.5) and the partition (1.6);
2. the coefficient-jet determinant \(5400\);
3. the \(A_2\) crossing-power identity, representative-regime endpoint signs,
   off-axis exclusion polynomial, nonzero jets, and leading split coefficient
   \(-2\);
4. the \(A_3\) crossing-power identities, monotonicity inputs, endpoint signs,
   nonzero jets, and leading split coefficient \(-6\);
5. the claim boundary that neither route proves a global caustic image
   decomposition or an enhanced-dissipation theorem through a collision.

The comparator requires exact equality of the canonical payloads.  The
programs derive their ledger booleans from those finite exact inputs rather
than writing the conclusions as literals.  Even so, the machine audit does
not quantify over \(y\), \(k\), \(\tau\), or the circle.  The continuous
sign and monotonicity arguments in Sections 3--4 are what imply uniqueness of
the events, the global count transitions, simplicity away from collision, and
the stated transversality interpretations.  The certificate audits that
algebraic spine; it does not replace the continuous proof.

---

## 7. Proved here and not proved here

### 7.1 Proved here

1. the complete \(A_2/A_3/A_4/A_5\) partition by vanishing order of the R0.72R incidence
   **parameter space**;
2. restricted miniversality modulo additive constants through \(A_5\), and
   local codimensions one through four;
3. an explicit transverse \(A_2\) heat crossing in the fixed-first-harmonic
   four-dimensional slice, with exact global distinct-point count
   \(4/3/2\);
4. an explicit real-even \(A_3\) heat crossing with nonzero third carrier and
   exact global distinct-point count \(4/2/2\);
5. the two exact square-root branch laws (3.12) and (4.13).

### 7.2 Not proved here

1. injectivity of the incidence map or all of its self-intersections;
2. all connected components of the four-dimensional complement;
3. the \(A_{2j+1}^{\pm}\) sign refinement required for a complete real
   singularity stratification;
4. a two-parameter full-slice transverse unfolding of \(A_3\);
5. enhanced dissipation uniformly through an \(A_2\) or \(A_3\) collision;
6. arbitrary phases, carrier sets, or coefficient motion;
7. nonlinear stability of a general three-dimensional Navier--Stokes flow;
8. global regularity or finite-time blow-up for the Clay problem.

---

## 8. Research value and next gate

R0.72S replaces a qualitative wall picture by an exact local singularity
ledger and two globally counted heat paths.  It is useful because the next
PDE problem now has explicit coefficients, collision time, jet sizes, and
root-splitting laws.  It also identifies precisely why existing
nondegenerate time-dependent enhanced-dissipation theorems stop at the wall.

Its direct value for the three-dimensional Navier--Stokes Millennium problem
remains low.  The profiles are finite-harmonic scalar shears inside a special
triangular reduction, and no estimate through the collision has yet been
proved.

The next defensible gate is R0.72T:

1. rescale a spacetime neighborhood of the \(A_2\) crossing using
   \(F'\sim-3\delta-(3/2)\xi^2\);
2. determine the candidate nonautonomous mixing length by balancing the time
   drift, quadratic spatial degeneracy, transport frequency, and diffusion;
3. prove a model subelliptic or hypocoercive estimate on that rescaled normal
   form;
4. only then attempt a perturbative transfer back to the exact heat path.

---

## Claim-to-source ledger

| Claim used here | Primary source | Exact role | Limitation |
|---|---|---|---|
| Maximal-real-critical trigonometric-polynomial regions were studied before this report | V. I. Arnol'd, 1997 | Prior topology boundary | Does not supply the present coefficient paths or exact heat counts |
| Periodic caustics and generic cusp geometry | V. I. Arnol'd, 2001 | General geometric context | The local jet partition here is derived directly |
| Complex Laurent-polynomial caustic and Morse discriminant | A. Voorhaar, 2023 | Terminology and algebraic context | Does not impose the real unit-circle condition or classify this real image |
| Stationary finite-type enhanced-dissipation scales | D. Albritton, R. Beekie, M. Novack, 2022 | Frozen \(A_2/A_3\) rate benchmarks | Not nonautonomous collision estimates |
| Slowly varying time-dependent nondegenerate shears | D. Coble, S. He, 2024 | Explains the current theorem boundary | Requires nondegenerate shape control and a fixed critical-point structure |
| Time modulation of a fixed simple-critical profile | J. Benthaus, C. Nobili, 2025 | Additional current nonautonomous boundary | Does not allow the spatial critical points to collide |
| Rigid translation of a simple-critical shear | J. Benthaus, G. M. Coclite, C. Nobili, 2026 | Treats genuinely moving critical points and an intermediate ED rate | Rigid translation preserves critical-point type and count; no collision occurs |

## References

1. V. I. Arnol'd, *Critical Points of Smooth Functions and Their Normal
   Forms*, *Russian Mathematical Surveys* **30** (1975), 1--75,
   [MathNet](https://www.mathnet.ru/eng/rm4237).
2. V. I. Arnol'd, *Topological Classification of Real Trigonometric
   Polynomials and Cyclic Serpents Polyhedron*, in *The Arnold--Gelfand
   Mathematical Seminars*, Birkh\"auser, 1997,
   [official chapter record](https://link.springer.com/chapter/10.1007/978-1-4612-4122-5_4).
3. V. I. Arnol'd, *Astroidal Geometry of Hypocycloids and the Hessian
   Topology of Hyperbolic Polynomials*, *Russian Mathematical Surveys*
   **56** (2001), 1019--1083,
   [DOI](https://doi.org/10.1070/RM2001v056n06ABEH000452).
4. A. Voorhaar, *The Newton Polytope of the Morse Discriminant of a
   Univariate Polynomial*, *Advances in Mathematics* **432** (2023), 109275,
   [DOI](https://doi.org/10.1016/j.aim.2023.109275).
5. A. Esterov, A. Voorhaar, *Basecondary Polytopes*, 2024,
   [arXiv](https://arxiv.org/abs/2411.02234).
6. D. Albritton, R. Beekie, M. Novack, *Enhanced Dissipation and
   H\"ormander's Hypoellipticity*, *Journal of Functional Analysis* **283**
   (2022), 109522,
   [arXiv](https://arxiv.org/abs/2105.12308).
7. D. Coble, S. He, *A Note on Enhanced Dissipation and Taylor Dispersion of
   Time-Dependent Shear Flows*, *Communications in Mathematical Sciences* **22** (2024),
   1685--1700, [arXiv](https://arxiv.org/abs/2309.15738).
8. J. Benthaus, C. Nobili, *Enhanced Dissipation via Time-Modulated Velocity
   Fields*, 2025,
   [arXiv](https://arxiv.org/abs/2501.16905).
9. J. Benthaus, G. M. Coclite, C. Nobili, *Mixing and Enhanced Dissipation in
   a Time-Translating Shear Flow*, 2026,
   [arXiv](https://arxiv.org/abs/2603.14624).
