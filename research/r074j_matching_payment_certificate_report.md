# R0.74J matching-payment finite certificate report

## Result

The exact-arithmetic producer returns **PASS: 38/38**.

The certificate uses Python `Fraction`.  An independent Ruby `Rational`
implementation reconstructs every field and returns **PASS: 38/38**, with
287 terminal-field comparisons and zero mismatches.

This certificate covers finite arithmetic only.  It is not a proof of the
periodic heat equation or any Navier--Stokes theorem.

## 1. Fifth-shell geometry

At payment radius \(2R\), shell \(k=5\) has

\[
 2^5(2R)=64R,\qquad 2^6(2R)=128R.
\]

The box

\[
 |x_1|<R,\quad |x_2|<R,\quad80R<x_3<96R
\]

has volume

\[
 (2R)(2R)(16R)=64R^3.
\]

Its exact outer-square comparison is

\[
 96^2+1^2+1^2=9218<16384=128^2,
\]

with margin \(7166\).  The annular weight exponent is

\[
 \frac{4^{5-1}}{32}=\frac{256}{32}=8.
\]

The certificate therefore reconstructs the finite assertions
\(Q_R\subset A_5(2R)\) and \(\Gamma_5=e^{-8}\), conditional only on the
geometric definitions.

## 2. Rational platform ledger

Under \(R\le1/200\),

\[
 16R\le\frac2{25}<\frac12,
 \qquad \delta_R\le32R,
 \qquad80R-32R=48R.
\]

Using the lower bound \(\pi>3\), the right-platform comparison at the cap is
also strictly larger than \(48R\).

For \(t\le65R^2\), the finite Brownian/Chebyshev coefficients are

\[
 2t\le130R^2,\qquad(48R)^2=2304R^2,
\]

\[
 \frac{130}{2304}=\frac{65}{1152},
 \qquad
 2\frac{65}{1152}=\frac{65}{576},
 \qquad
 1-\frac{65}{576}=\frac{511}{576}>\frac12.
\]

The certificate checks these rational identities.  It does not prove the
periodic Brownian representation, the circle-exit implication, Chebyshev's
inequality, or the analytic heat lower bound.

## 3. Cubic normalization

The exact time length, normalization, box volume, and conservative cubic
floor are

\[
 65-61=4,\qquad(2R)^{-2}=\frac14R^{-2},
\]

\[
 |Q_R|=64R^3,\qquad(1/2)^3=\frac18.
\]

Thus

\[
 \frac14\cdot4\cdot64\cdot\frac18=8,
 \qquad -2+2+3=3.
\]

This is the finite coefficient behind

\[
 \mathcal G_u\ge8e^{-8}B^3R^3.
\]

The certificate does not prove that \(\mathcal G_u\) is a nonnegative row or
that \(|u|^3\ge B^3|\theta|^3\); those are analytic ledger inputs.

## 4. Logarithmic exponents

The exact family has

\[
 \rho=\frac1{320}.
\]

At the matching payment scale \(B^3R^3\), the certificate reconstructs

\[
 3\rho=\frac3{320}.
\]

Since \(L_{j+1}^2=4L_j^2\), the consecutive-index coefficient is

\[
 3\rho(4-1)=9\rho=\frac9{320}.
\]

It also checks

\[
 (B^3R^3)^{2/3}=B^2R^2,
\]

and that the square root of a logarithm proportional to \(L^2\) contributes
one power of \(L\).  Hence the finite monomial frontier is

\[
 B^2LR^2.
\]

The convergence of \(B_jR_j^2\), the matching analytic bounds for \(P_j\),
and the passage from these powers to asymptotic statements are not proved by
the certificate.

## 5. Boundary

Neither implementation nor the frozen JSON proves:

1. the periodic heat-semigroup or Brownian representation;
2. the continuum shear-platform lower bound;
3. the R0.74F exact solution or zero-frame identities;
4. the R0.74G complete-payment upper bound;
5. an upper bound for \(X_j\) or \(\mathfrak C_j\);
6. the literature boundary, novelty, or priority;
7. regularity, exclusion of singularities, or global smoothness; or
8. the Clay Millennium problem.

**NOT CLAY.**
