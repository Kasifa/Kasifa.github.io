# R0.53 — A fixed product-affine charge weight strictly exceeds the complete affine family

## 1. Scope

This note concerns the exact degree-80 center of the reduced canonical edge
generating system.  It proves a strict improvement for one fixed rational
weight

\[
\omega_s(c,\lambda,\mu)
=c^s(1+\lambda |s|)(1+\mu |s|).
\]

The result is an all-order theorem inside that reduced coefficient model.  It
does not optimize the complete three-parameter family, establish a
scale-critical estimate for arbitrary three-dimensional divergence-free
fields, or prove or disprove three-dimensional incompressible Navier--Stokes
regularity.

## 2. Algebra constant one

For every \(t\ge0\) and integers \(a,b\),

\[
1+t|a+b|
\le 1+t|a|+t|b|
\le (1+t|a|)(1+t|b|).
\]

Applying this inequality separately with \(t=\lambda\) and \(t=\mu\), then
multiplying, gives

\[
\omega_{a+b}\le \omega_a\omega_b.
\]

Thus the product-affine family remains a Banach algebra weight with constant
one.  The gain below is not offset by a larger algebra constant.

## 3. Diagnostic compactification

For the former active input charge \(S=162\), introduce

\[
\alpha=\frac{\lambda}{1+162\lambda},\qquad
\beta=\frac{\mu}{1+162\mu}.
\]

Because every center charge satisfies \(q\ge-1\), the active ratio is exactly

\[
\frac{\omega_{162+q}}{\omega_{162}}
=c^q(1+\alpha q)(1+\beta q)
=c^q\{1+(\alpha+\beta)q+\alpha\beta q^2\}.
\]

A non-certified high-precision search over the active and zero-charge
constraints found a symmetric interior candidate near

\[
\begin{aligned}
r&\approx0.38262891253047284265,\\
c&\approx0.79280553858639950451,\\
\alpha=\beta&\approx0.0060515027062626180062,\\
\lambda=\mu&\approx0.30786171223049481702.
\end{aligned}
\]

These decimals are used only to select a simple rational witness.  They are
not used in a sign decision and are not claimed to be a global optimum.

## 4. Fixed rational witness

The formal audit fixes

\[
c=\frac{396403}{500000},\qquad
\lambda=\mu=\frac{153931}{500000}.
\]

For this weight the zero-charge column at its minimum tail degree \(j=81\)
has the positive polynomial

\[
Z_0(r)=\sum_{i=1}^{80}z_i r^i,qquad z_i>0.
\]

Consequently \(Z_0\) is strictly increasing on \(r>0\), starts at zero, and
has exactly one positive solution of \(Z_0(r)=1\).  Exact endpoint signs and a
Sturm count isolate it in

\[
0.382628602237879637
<r_*<
0.382628602237879638.
\]

The interval has exact width \(10^{-18}\).

## 5. Every other charge and degree

For each fixed positive input charge \(2\le s<280\), the exact
input-degree factor is retained inside the complete sum.  Convexity in the
common slope \(x=s/j\) reduces every admissible tail degree to the two
endpoints \(x=0\) and \(x=s/J_s\).  The product-affine charge ratio is
independent of \(j\), so the R0.47 endpoint reduction remains valid without a
degree grid.

The exceptional charges are handled separately:

- \(s=1\) uses the exact termwise all-degree endpoint bound;
- \(s=-1\) is maximal at \(j=82\).  Only the \(q=1\) contribution can have a
  negative \(t=1/j\) derivative, and its product-affine ratio is
  \(1/((1+\lambda)(1+\mu))\).  The exact \(q=2\) seed lower bound exceeds the
  complete weighted \(q=1\) derivative upper bound.

For every \(s\ge280\), each positive-center-charge ratio satisfies

\[
\frac{(1+\lambda(s+q))(1+\mu(s+q))}
{(1+\lambda s)(1+\mu s)}
\le\left(1+\frac{q}{s}\right)^2
\le\left(1+\frac{q}{280}\right)^2.
\]

The \(q=-1\) ratio is bounded by one.  After this coefficientwise envelope,
the exact even and odd minimum-degree branches are rational functions of
\(y=1/s\).  Complete Bernstein derivative signs show that the even branch is
maximal at \(s=280\), while the odd branch is bounded by its \(s\to\infty\)
limit.  The resulting all-order tail bound at the root-box right endpoint is

\[
0.99856429173292745732<1.
\]

In total, the audit records 281 inactive objects: 278 fixed positive charges,
the two exceptional charges, and one infinite large-charge branch.  The
nearest competitor is the former active column \((j,s)=(81,162)\), with exact
gap larger than

\[
1.4883451915609408904\times10^{-6}.
\]

## 6. Strict comparison with R0.52

R0.52 proved the complete single-affine-family upper bound

\[
R_{\mathrm{aff}}
<0.3826244718485988314760952288871012330926.
\]

The present fixed product-affine root satisfies

\[
\frac{r_{*,\mathrm{product}}^{L}}{R_{\mathrm{aff}}^{U}}
>1.0000107948905119688.
\]

Thus one simple rational product-affine weight strictly exceeds the globally
certified optimum of the complete single-affine family.  This is a formal
counterexample to the R0.53 boundary-degeneration alternative.

## 7. Exact fixed-point restart

At the simpler rational restart radius

\[
r_0=\frac{95657}{250000}=0.382628,
\]

the zero-charge column is the complete linearization maximum and obeys

\[
L_0<0.99999769297234707665,
\qquad
1-L_0>2.3070276529233482826\times10^{-6}.
\]

The product-affine weighted residual norm is below

\[
7.5271302784558830723\times10^{-31}.
\]

With the same quadratic constant \(3\) and ball radius
\((1-L_0)/10^6\), the exact self-map and Lipschitz inequalities are strict.
The restart radius itself exceeds the R0.52 upper bound by the factor

\[
1.000009220924589906.
\]

## 8. What remains

The next algebraic question is the complete product-affine optimization:

1. certify the symmetric interior stationary candidate in
   \((r,c,\alpha,\beta)\);
2. prove its type in the antisymmetric \(\alpha-\beta\) direction;
3. eliminate or cover the full square
   \(0\le\alpha,\beta<1/162\);
4. determine whether the fixed rational witness is close to the true global
   product-affine optimum.

That problem remains inside the reduced generating system.  A separate and
more important unresolved task is to construct a scale-critical bridge to the
full three-dimensional Fourier interaction geometry.

