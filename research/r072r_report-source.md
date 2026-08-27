# R0.72R -- a four-real-dimensional caustic-free core beyond the \(Q_2\le 1/2\) cone

**Date:** 2026-08-28

**Status:** a quantitative two-critical-point theorem, physical shape contract,
and family-uniform enhanced-dissipation corollary for an explicit compact
polydisc in the complex \(1{:}2{:}3\) coefficient space.  The whole initial
polydisc lies strictly outside the sufficient coefficient cone used in
R0.72Q.  The complete four-dimensional caustic stratification is not claimed.
The result remains inside the triangular 2.5D Navier--Stokes class and is not
a regularity theorem for general three-dimensional Navier--Stokes.

**Keywords:** Navier--Stokes regularity, enhanced dissipation, trigonometric
polynomial, caustic, Morse shear, complex harmonic coefficients, moving
critical points, quantitative chamber core

---

## 0. Direct decision

R0.72Q used the phase-uniform sufficient condition

\[
 Q_2=\sum_{m=2}^{M}m^2|z_m|\le\frac12
 \tag{0.1}
\]

to obtain two critical points and a uniform shape contract.  That condition
is not a caustic equation.  It is only a convenient inner cone.  The first
question in R0.72R is therefore whether one can leave (0.1) by a positive
amount while retaining a complete, explicit and heat-path-stable contract.

For

\[
 K:=\left\{(z_2,z_3)\in\mathbb C^2:
 \left|z_2-\frac3{20}\right|\le\frac1{100},\quad
 |z_3|\le\frac1{1000}\right\},
 \tag{0.2}
\]

consider

\[
 W_{z_2,z_3}(y,\phi)
 =e^{-y}\cos\phi
 +\operatorname{Re}\!\left(
 z_2e^{-4y}e^{2i\phi}+z_3e^{-9y}e^{3i\phi}
 \right),
 \qquad 0\le y\le1.
 \tag{0.3}
\]

The set \(K\) is a compact connected polydisc with nonempty interior in
\(\mathbb R^4\).  Every one of its initial profiles lies beyond (0.1):

\[
 4|z_2|+9|z_3|
 \ge4\left(\frac3{20}-\frac1{100}\right)
 =\frac{14}{25}
 =\frac12+\frac3{50}.
 \tag{0.4}
\]

Nevertheless, uniformly for every \((z_2,z_3)\in K\) and every
\(0\le y\le1\):

1. \(W(y,\cdot)\) has exactly two critical points;
2. they lie within \(\pi/48\) of \(0\) and \(\pi\), respectively;
3. the physical shear satisfies the explicit Coble--He shape contract

   \[
   \boxed{N_{\rm crit}=2,\qquad r=\frac\pi{48},\qquad
   \mathfrak C_0=144,\qquad \mathfrak C_1=240;}
   \tag{0.5}
   \]

4. the complete affine-row propagator has a coefficient-uniform
   enhanced-dissipation estimate on \(K\).

There is also a useful separation between a sufficient cone boundary and a
true caustic.  Along each normalized heat path,

\[
 Q_2(y)=4|z_2|e^{-3y}+9|z_3|e^{-8y}
 \tag{0.6}
\]

is strictly decreasing.  Equation (0.4) puts it above \(1/2\) at \(y=0\),
whereas \(e>2\) gives

\[
 Q_2(1)<4\frac4{25}\frac18
 +9\frac1{1000}\frac1{256}
 =\frac{20489}{256000}<\frac12.
 \tag{0.7}
\]

Thus every path crosses the old \(Q_2=1/2\) boundary exactly once while its
critical points stay uniformly nondegenerate.  The crossing is not a caustic.

The result does not say that the first Fourier amplitude is smaller than a
higher one.  The precise statement is that the entire class lies outside
R0.72Q's weighted-jet safety cone.  Calling (0.2) a fully classified
\(1{:}2{:}3\) chamber would also be too strong: this report proves that it is
a caustic-free compact core, but does not compute every component of the
four-dimensional complement.

---

## 1. Complete cell reduction

Take commensurate carriers \(R,2R,3R\), fix an orthogonal Fourier label
\(q_*\), and retain the full affine row

\[
 \Lambda_{R,q_*}=\{(nR,q_*):n\in\mathbb Z\}.
 \tag{1.1}
\]

The row is invariant under all six carrier shifts.  The same exact Fourier
transform and rescaling used in R0.72P--Q gives

\[
 \partial_yG
 =(\partial_\phi^2-|q_*|^2R^{-2})G
 -is\varepsilon_c W_{z_2,z_3}(y,\phi)G,
 \tag{1.2}
\]

where \(s\in\{-1,1\}\) and \(\varepsilon_c>0\).  No carrierwise semigroup
estimate has been substituted for the full superposition.

With

\[
 t=\varepsilon_c y,\qquad \eta=\varepsilon_c^{-1},\qquad
 H(t,\phi)=e^{|q_*|^2R^{-2}\eta t}G(\eta t,\phi),
 \tag{1.3}
\]

equation (1.2) becomes

\[
 \partial_tH=\eta\partial_\phi^2H
 -isW_{z_2,z_3}(\eta t,\phi)H.
 \tag{1.4}
\]

Thus the only new analytic work is a quantitative time-dependent shear
contract uniform on \(K\).  The favorable scalar damping removed in (1.3)
is restored after the shear estimate.

---

## 2. Normalized heat path and exact perturbation budgets

Factor out the first heat envelope:

\[
 W(y,\phi)=e^{-y}F_y(\phi),
 \tag{2.1}
\]

\[
 F_y(\phi)=\cos\phi+
 \operatorname{Re}\!\left(
 z_2e^{-3y}e^{2i\phi}+z_3e^{-8y}e^{3i\phi}
 \right).
 \tag{2.2}
\]

Write

\[
 c(y)=\frac3{20}e^{-3y},\qquad
 F_y^0(\phi)=\cos\phi+c(y)\cos2\phi,
 \tag{2.3}
\]

\[
 \xi=z_2-\frac3{20},\qquad
 h_y(\phi)=\operatorname{Re}\!\left(
 \xi e^{-3y}e^{2i\phi}+z_3e^{-8y}e^{3i\phi}
 \right).
 \tag{2.4}
\]

Then \(F_y=F_y^0+h_y\), \(|\xi|\le1/100\), and heat decay makes the
worst derivative budgets occur at \(y=0\):

\[
 \|h_y'\|_\infty\le\frac{23}{1000},\qquad
 \|h_y''\|_\infty\le\frac{49}{1000},\qquad
 \|h_y'''\|_\infty\le\frac{107}{1000}.
 \tag{2.5}
\]

The center slope factors exactly:

\[
 (F_y^0)'(\phi)
 =-\sin\phi\bigl(1+4c(y)\cos\phi\bigr).
 \tag{2.6}
\]

Since \(0\le4c(y)\le3/5\),

\[
 1+4c(y)\cos\phi\ge\frac25,
 \qquad |(F_y^0)'(\phi)|\ge\frac25|\sin\phi|.
 \tag{2.7}
\]

This factorization, rather than the scalar \(Q_2\) bound, is the mechanism
that keeps the entire polydisc away from the caustic.

---

## 3. Exactly two critical points

Set

\[
 \ell=\frac\pi{48}.
 \tag{3.1}
\]

The elementary bounds \(\pi>3\) and
\(\sin x>x-x^3/6\) for \(0<x<1\) give

\[
 \sin\ell>\sin\frac1{16}
 >\frac1{16}-\frac1{24576}
 =\frac{1535}{24576}
 >\frac{23}{400}.
 \tag{3.2}
\]

The endpoint slope retains the exact rational margin

\[
 \frac25\frac{1535}{24576}-\frac{23}{1000}
 =\frac{3047}{1536000}>0.
 \tag{3.3}
\]

If \(F_y'(\phi)=0\), then (2.5)--(2.7) imply

\[
 |\sin\phi|\le\frac52\frac{23}{1000}
 =\frac{23}{400}<\sin\ell.
 \tag{3.4}
\]

Therefore every critical point is in one of the disjoint boxes

\[
 J_0=(-\ell,\ell),\qquad
 J_\pi=(\pi-\ell,\pi+\ell).
 \tag{3.5}
\]

To prove uniqueness, use the larger monotonicity boxes

\[
 I_0=(-\pi/6,\pi/6),\qquad
 I_\pi=(\pi-\pi/6,\pi+\pi/6).
 \tag{3.6}
\]

On \(I_0\),

\[
 -(F_y^0)''=\cos\phi+4c(y)\cos2\phi
 \ge\frac{\sqrt3}{2}>\frac67,
 \tag{3.7}
\]

and hence

\[
 -F_y''>\frac67-\frac{49}{1000}>\frac45.
 \tag{3.8}
\]

On \(I_\pi\), writing \(\phi=\pi+s\),

\[
 (F_y^0)''=\cos s-4c(y)\cos2s
 \ge\frac{\sqrt3}{2}-\frac35,
 \tag{3.9}
\]

so

\[
 F_y''>\frac67-\frac35-\frac{49}{1000}
 =\frac15+\frac{57}{7000}>\frac15.
 \tag{3.10}
\]

The boundary signs from (3.3) give one zero in each small box.  The strict
monotonicity (3.8)--(3.10) gives at most one.  Equation (3.4) excludes all
other zeros.  Thus

\[
 \boxed{N_{\rm crit}(F_y)=2\quad\text{for every }y\ge0
 \text{ and every }(z_2,z_3)\in K.}
 \tag{3.11}
\]

Denote the critical points by \(c_0(y)\in J_0\) and
\(c_\pi(y)\in J_\pi\).  Their torus separation is larger than
\(23\pi/24\).

---

## 4. Quantitative shape contract

If \(d_{\mathbb T}(\phi,c_j(y))\le\ell\), then \(\phi\) is within
\(2\ell=\pi/24\) of \(0\) or \(\pi\).  Near zero, (3.7) is more than
sufficient.  Near \(\pi\), \(\cos2s\le\cos s\) gives

\[
 (F_y^0)''\ge\frac25\cos s>\frac13.
 \tag{4.1}
\]

After subtracting (2.5),

\[
 |F_y''|>\frac14
 \tag{4.2}
\]

throughout both \(\ell\)-critical tubes.  The tight rational margin used in
this last step is

\[
 \frac13-\frac{49}{1000}-\frac14
 =\frac{103}{3000}>0.
 \tag{4.3}
\]

The global upper bound is

\[
 |F_y''|\le1+4|z_2|+9|z_3|
 \le\frac{1649}{1000}<\frac53,
 \tag{4.4}
\]

with margin \(53/3000\).  Integrating from the unique critical point gives

\[
 \boxed{
 \frac14d_{\mathbb T}(\phi,c_j(y))
 <|F_y'(\phi)|
 <\frac53d_{\mathbb T}(\phi,c_j(y)),
 \quad d_{\mathbb T}(\phi,c_j(y))\le\ell.}
 \tag{4.5}
\]

On \(I_0\cup I_\pi\), monotonicity and a distance of at least \(\ell\)
from the critical set give

\[
 |F_y'(\phi)|>\frac15\ell
 =\frac\pi{240}>\frac1{80}.
 \tag{4.6}
\]

Outside the larger boxes, \(|\sin\phi|\ge1/2\), and (2.5)--(2.7) give the
stronger estimate

\[
 |F_y'(\phi)|\ge\frac15-\frac{23}{1000}
 =\frac{177}{1000}>\frac1{80}.
 \tag{4.7}
\]

Therefore

\[
 d_{\mathbb T}(\phi,\{c_0(y),c_\pi(y)\})\ge\ell
 \quad\Longrightarrow\quad |F_y'(\phi)|>\frac1{80}.
 \tag{4.8}
\]

Also

\[
 \|F_y'\|_\infty
 \le1+2\frac4{25}+3\frac1{1000}
 =\frac{1323}{1000}<\frac43.
 \tag{4.9}
\]

For the physical shear (0.3), \(e^{-y}>1/3\) on \(0\le y\le1\).
Equations (4.5), (4.8), and (4.9) imply

\[
 \frac1{12}d_{\mathbb T}(\phi,c_j(y))
 <|W_\phi(y,\phi)|
 <\frac53d_{\mathbb T}(\phi,c_j(y))
 \tag{4.10}
\]

in the critical tubes, and

\[
 \frac1{240}<|W_\phi(y,\phi)|<\frac43
 \tag{4.11}
\]

away from them.  Squaring the local bounds and using one common conservative
constant gives the advertised physical contract

\[
 \boxed{
 r=\frac\pi{48},\qquad
 \mathfrak C_0=144,qquad
 \mathfrak C_1=240,qquad 0\le y\le1.}
 \tag{4.12}
\]

The lower bounds in (4.10)--(4.12) are not uniform as \(y\to\infty\); their
declared window is essential.

---

## 5. Spatial derivatives, slow time, and enhanced dissipation

The full physical profile obeys

\[
 \|W\|_\infty\le\frac{1161}{1000},\qquad
 \|W_\phi\|_\infty\le\frac{1323}{1000},
 \tag{5.1}
\]

\[
 \|W_{\phi\phi}\|_\infty\le\frac{1649}{1000},\qquad
 \|W_{\phi\phi\phi}\|_\infty\le\frac{2307}{1000}<\frac73.
 \tag{5.2}
\]

If the \(W^{3,\infty}\) norm is taken as the sum of the four displayed
suprema, one may use

\[
 C_{\rm sh}=\frac{161}{25}.
 \tag{5.3}
\]

The mixed derivative has the same worst coefficient as the third spatial
derivative:

\[
 \|W_{y\phi}\|_\infty
 \le1+8|z_2|+27|z_3|
 \le\frac{2307}{1000}<\frac73.
 \tag{5.4}
\]

For the reference flow \(U(t,\phi)=sW(\eta t,\phi)\),

\[
 \|U_{t\phi}\|_\infty\le\frac73\eta.
 \tag{5.5}
\]

The Coble--He slow-reference condition follows from

\[
 \boxed{\eta\le\left(\frac37\right)^4=\frac{81}{2401}.}
 \tag{5.6}
\]

Tracking the same fixed cutoffs and absorption parameters as in R0.72Q,
define

\[
 \eta_R:=\min\left\{
 1,\left(\frac37\right)^4,
 \eta_{\rm CH}\!\left(2,\frac\pi{48},144,240,\frac{161}{25}\right)
 \right\}.
 \tag{5.7}
\]

Here \(\eta_{\rm CH}\) is a dependency label for the smallness threshold
read from the proof of Coble--He; it is not a formula stated verbatim in that
paper.  Because every input in (5.7) is uniform on \(K\), the proof produces
constants \(C_R,c_R>0\) such that, for \(0<\eta\le\eta_R\) and
\(0\le t\le\eta^{-1}\),

\[
 \|H(t)\|_2^2\le C_Re^{-c_R\eta^{1/2}t}\|H(0)\|_2^2,
 \qquad 0\le t\le\eta^{-1}.
 \tag{5.8}
\]

Returning to \(G\) gives

\[
 E(y)\le C_Re^{-c_R\sqrt{\varepsilon_c}\,y}E(0),
 \qquad 0\le y\le1,
 \qquad
 \int_0^1E(y)\,dy
 \le C_R\varepsilon_c^{-1/2}E(0),
 \tag{5.9}
\]

with the usual compact-parameter contraction completion outside the small
\(\eta\) range.  The constants are uniform in \((z_2,z_3)\in K\), \(R\),
\(\varepsilon_c\), and the row datum, subject to the fixed-pattern reduction.
This is a theorem about the full \(1{:}2{:}3\) superposition, not a sum of
three carrierwise estimates.

For the physical cross-cubic comparison inherited from R0.72O, the second
coefficient has the uniform floor \(|z_2|\ge7/50\).  If the third carrier is
declared active and its contribution is also to enter an active-count
comparison, one must still impose a fixed floor \(|z_3|\ge\beta_->0\).
No constant uniform as \(\beta_-\downarrow0\) is claimed.

---

## 6. Exact \(1{:}2{:}3\) degeneracy incidence

For the static normalized polynomial

\[
 f(\phi)=\cos\phi+
 \operatorname{Re}\!\left(z_2e^{2i\phi}+z_3e^{3i\phi}\right),
 \tag{6.1}
\]

put \(u=e^{i\phi}\) and write

\[
 z_3u^3=A+iB.
 \tag{6.2}
\]

Solving \(f'=f''=0\) for \(z_2\) gives the exact incidence
parameterization

\[
 \boxed{z_3=(A+iB)e^{-3i\phi},}
 \tag{6.3}
\]

\[
 \boxed{
 z_2=e^{-2i\phi}\left[
 -\frac{\cos\phi+9A}{4}
 -\frac{i(\sin\phi+3B)}2
 \right],}
 \tag{6.4}
\]

where \((\phi,A,B)\in\mathbb T\times\mathbb R^2\).  Equivalently, for
fixed \(z_3\),

\[
 \boxed{
 z_2=\frac18u^{-3}-\frac38u^{-1}
 -\frac{15}{8}z_3u-\frac38\overline{z_3}u^{-5}.}
 \tag{6.5}
\]

Another exact form uses

\[
 D(u)=3z_3u^6+2z_2u^5+u^4-u^2
 -2\overline{z_2}u-3\overline{z_3}.
 \tag{6.6}
\]

On \(|u|=1\),

\[
 D(u)=\frac2i u^3f'(\phi),
 \qquad f'(\phi)=0\Longrightarrow D'(u)=-2u^2f''(\phi).
 \tag{6.7}
\]

Thus the real unit-circle caustic is exactly

\[
 \boxed{\exists |u|=1:\quad D(u)=D'(u)=0.}
 \tag{6.8}
\]

Along the incidence, the next jets reduce to

\[
 f'''=3(5B-\sin\phi),
 \qquad f''''=3(15A-\cos\phi).
 \tag{6.9}
\]

Equations (6.3)--(6.9) define the wall without numerical root finding.  They
do not by themselves classify its self-intersections, singular strata, or
the connected components of its complement.  A complex polynomial
discriminant without the condition \(|u|=1\) is not an equivalent real
caustic test.

---

## 7. Exact real-coefficient slice

For \(z_2=a\in\mathbb R\) and \(z_3=b\in\mathbb R\),

\[
 f'(\phi)=-\sin\phi\,q(\cos\phi),
 \tag{7.1}
\]

\[
 q(x)=12bx^2+4ax+1-3b.
 \tag{7.2}
\]

The algebraic discriminant of (6.6) factors as

\[
 \boxed{
 \operatorname{Disc}_uD
 =-64(4a-9b-1)^3(4a+9b+1)^3
 (a^2+9b^2-3b)^2.}
 \tag{7.3}
\]

After enforcing the unit-circle condition, the real caustic consists of the
endpoint lines

\[
 1+4a+9b=0\quad(\phi=0),
 \qquad
 1-4a+9b=0\quad(\phi=\pi),
 \tag{7.4}
\]

and the internal arc

\[
 a^2=3b(1-3b),
 \qquad \frac1{15}\le b\le\frac13.
 \tag{7.5}
\]

The interval in (7.5) cannot be omitted: the remaining part of the algebraic
ellipse corresponds to a repeated root outside \((-1,1)\), not to a real
unit-circle critical point.  This slice is included as an exact audit of the
general incidence, not as a new complete caustic theorem.

---

## 8. Literature boundary

Arnol'd gives the general caustic formula for
\(A\cos\phi+B\sin\phi+g(\phi)\), describes generic cusp geometry, and
classifies the topology of maximal-real-critical-point regions for real
trigonometric polynomials.  In degree three the maximal region is therefore
not a new discovery of this report.  The formulas in Section 6 are a
specialized, auditable coordinate description for the fixed-first-harmonic
four-real-dimensional slice.

Voorhaar studies caustics and Morse discriminants of univariate Laurent
polynomials through their Newton polytopes.  That complex-algebraic framework
does not replace the real self-inversive unit-circle condition in (6.8).

Coble and He prove enhanced dissipation for slowly varying time-dependent
shears with a fixed number of nondegenerate critical points and uniform shape
control.  The explicit polydisc, heat path, and constants (0.5) are supplied
here; the compact-family constant extraction follows their proof dependencies
and is not a theorem stated verbatim in their paper.

Bedrossian--Coti Zelati and Albritton--Beekie--Novack give the stationary
rates when critical points are degenerate.  Those results show that a caustic
is not the same as failure of enhanced dissipation.  They do not treat a
nonautonomous critical-point collision or passage through a wall.

A bounded primary-source search did not locate this explicit four-real-
dimensional rational polydisc, its full heat-path jet margins, and the
associated family-uniform time-dependent enhanced-dissipation corollary as
one result.  This negative search is not a novelty or priority proof.

---

## 9. Exact certificate contract

The release certificate has two independent implementations:

1. a Python producer using integer and rational arithmetic plus symbolic
   coefficient identities;
2. a JavaScript audit using a separate BigInt rational implementation and
   direct coefficient convolution.

The two routes independently reconstruct:

1. the strict cone-exit margin \(3/50\);
2. all perturbation and derivative budgets in Sections 2, 4, and 5;
3. the rational margins \(3047/1536000\), \(57/7000\),
   \(103/3000\), and \(53/3000\);
4. the physical shape constants and slow-time exponent identity;
5. the incidence identities (6.3)--(6.9);
6. the real-slice factorization (7.3) and the admissible internal-root
   interval (7.5).

The comparator requires exact equality of their canonical payloads.  These
finite certificates audit the algebraic spine.  They do not replace the
continuum monotonicity proof, the Coble--He theorem, or a full four-dimensional
caustic decomposition.

---

## 10. What is proved, and what is not

### 10.1 Proved here

1. an explicit compact \(K\subset\mathbb C^2\) with nonempty four-real-
   dimensional interior and \(Q_2(0)\ge14/25>1/2\);
2. exactly two critical points along every heat path from \(K\);
3. the physical contract
   \((r,\mathfrak C_0,\mathfrak C_1)=(\pi/48,144,240)\) on \(0\le y\le1\);
4. a proof-level family-uniform Coble--He corollary for the complete
   \(1{:}2{:}3\) affine-row superposition;
5. exact incidence formulas for the real unit-circle degeneracy wall;
6. the exact real-coefficient slice and its admissible unit-circle arc.

### 10.2 Not proved here

1. the complete four-dimensional caustic stratification;
2. every connected component and its critical-point count;
3. maximality of \(K\) or its optimal distance to the wall;
4. enhanced dissipation through an \(A_2\) or \(A_3\) collision;
5. arbitrary time-dependent phases or arbitrary fast coefficient motion;
6. uniform constants for growing carrier ceiling or general carrier sets;
7. a continuation criterion for general three-dimensional Navier--Stokes;
8. finite-time blow-up or global regularity for the Clay problem.

---

## 11. Research value

The strict mathematical increment over R0.72Q is not the existence of a
degree-three trigonometric chamber; that topology was already studied by
Arnol'd.  The increment is an explicit four-real-dimensional compact core
outside the old weighted-jet cone, together with rational root-localization,
Hessian, away-gradient, derivative, and slow-time margins that survive the
entire heat path.  Those margins are strong enough to support the complete
superposition enhanced-dissipation corollary.

This is useful as a quantitative lemma for a paper on special triangular
mechanisms and as a certified starting point for approaching a caustic wall.
Its direct value for the Clay problem is still low.  The first harmonic,
commensurate finite pattern, affine-row invariance, triangular 2.5D reduction,
and nondegenerate critical-point assumptions remain far from arbitrary
three-dimensional data.

---

## 12. Next gate

R0.72S should move from a safe core to the wall itself.  The defensible next
targets are:

1. stratify the incidence (6.3)--(6.9) into generic \(A_2\), \(A_3\), and
   higher-codimension pieces on a declared compact coefficient box;
2. construct a heat path that approaches or crosses one declared stratum;
3. compare the nonautonomous decay scale with the stationary
   \(\nu^{3/5}\) and \(\nu^{2/3}\) benchmarks;
4. keep full global chamber classification separate unless a complete
   semialgebraic certificate is obtained.

---

## Claim-to-source ledger

| Claim used here | Primary source | Exact role | Limitation |
|---|---|---|---|
| Caustics of \(A\cos\phi+B\sin\phi+g(\phi)\), generic cusps, and degree-three real trigonometric chamber topology | V. I. Arnol'd, 1997 and 2001 | Establishes the prior caustic and chamber-topology boundary | Does not provide the polydisc \(K\), the stated rational margins, or the heat-path ED corollary |
| Slowly varying time-dependent nondegenerate shears have the \(\eta^{1/2}\) enhanced-dissipation scale | D. Coble and S. He, Theorem 1.2 and Appendix A | Semigroup input after the exact cell reduction | Uniformity on \(K\) is extracted here after supplying explicit common constants |
| Caustic and Morse discriminant for univariate Laurent polynomials | A. Voorhaar, Definition 1.1 | Complex-algebraic terminology and context | A complex discriminant alone is not the real unit-circle condition |
| Stationary degenerate critical points have slower ED scales depending on degeneracy order | J. Bedrossian and M. Coti Zelati; D. Albritton, R. Beekie, and M. Novack | Benchmark for the next wall problem | Does not prove a nonautonomous caustic-crossing theorem |

## References used at this gate

1. V. I. Arnol'd, *Topological Classification of Real Trigonometric
   Polynomials and Cyclic Serpents Polyhedron*, in *The Arnold--Gelfand
   Mathematical Seminars*, Birkh\"auser, 1997,
   [primary chapter record](https://link.springer.com/chapter/10.1007/978-1-4612-4122-5_8).
2. V. I. Arnol'd, *Astroidal Geometry of Hypocycloids and the Hessian
   Topology of Hyperbolic Polynomials*, *Russian Mathematical Surveys*
   **56** (2001), 1019--1083,
   [DOI](https://doi.org/10.1070/RM2001v056n06ABEH000452).
3. D. Coble and S. He, *A Note on Enhanced Dissipation of Time-Dependent
   Shear Flows*, *Communications in Mathematical Sciences* **22** (2024),
   1685--1700,
   [DOI](https://doi.org/10.4310/CMS.2024.v22.n6.a10).
4. A. Voorhaar, *The Newton Polytope of the Morse Discriminant of a
   Univariate Polynomial*, *Advances in Mathematics* **432** (2023),
   109275,
   [DOI](https://doi.org/10.1016/j.aim.2023.109275).
5. J. Bedrossian and M. Coti Zelati, *Enhanced Dissipation,
   Hypoellipticity, and Anomalous Small Noise Inviscid Limits in Shear
   Flows*, *Archive for Rational Mechanics and Analysis* **224** (2017),
   1161--1204,
   [DOI](https://doi.org/10.1007/s00205-017-1099-y).
6. D. Albritton, R. Beekie, and M. Novack, *Enhanced Dissipation and
   H\"ormander's Hypoellipticity*, *Journal of Functional Analysis* **283**
   (2022), 109522,
   [DOI](https://doi.org/10.1016/j.jfa.2022.109522).
