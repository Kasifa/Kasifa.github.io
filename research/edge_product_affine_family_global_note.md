# R0.54 — A global enclosure for the complete product-affine family

## 1. Scope

This note concerns the exact degree-80 center of the reduced canonical edge
generating system.  It gives a global lower-and-upper enclosure for the complete
three-parameter family

\[
\omega_s(c,\lambda,\mu)
=c^s(1+\lambda|s|)(1+\mu|s|),
\qquad c>0,\quad \lambda,\mu\ge0.
\]

The lower endpoint comes from the pinned R0.53 all-order rational witness.  The
upper endpoint is a new exact continuous-parameter exclusion.  No floating
search point is used in a sign decision.

The theorem remains internal to the reduced coefficient model.  It does not
identify the exact maximizing parameters, optimize all possible Banach norms,
construct a scale-critical comparison with arbitrary three-dimensional
Fourier data, or prove or disprove three-dimensional incompressible
Navier--Stokes regularity.

## 2. Symmetric invariant reduction

Let the former active input charge be \(S=162\), and write

\[
\alpha=\frac{\lambda}{1+S\lambda},\qquad
\beta=\frac{\mu}{1+S\mu},\qquad
A=\alpha+\beta,\qquad B=\alpha\beta,
\qquad h=\frac1S.
\]

The closure of \(0\le\alpha,\beta<h\) has the exact invariant image

\[
0\le A\le 2h,
\qquad
\max\{0,h(A-h)\}\le B\le \frac{A^2}{4}.
\]

The upper boundary follows from
\((\alpha-\beta)^2\ge0\).  The second lower boundary follows from
\((h-\alpha)(h-\beta)\ge0\).  Conversely, the two roots of
\(x^2-Ax+B\) lie in \([0,h]\) whenever these inequalities hold, so the
description is exact rather than an outer relaxation.

At fixed radius \(r\) and character \(c\), the active \((j,s)=(81,162)\)
column is

\[
F=f_0+A f_1+B f_2,
\qquad
f_0=M_0-1,\quad f_1=M_1,\quad f_2=M_2>0,
\]

where \(M_k\) is the exact \(q^k\) Laurent moment of the active column.
After multiplication by the positive denominator
\((1-S\alpha)(1-S\beta)\), the zero-charge column is

\[
G=g_0+A g_1+B g_2,
\]

with

\[
\begin{aligned}
g_0&=U_0-1,\\
g_1&=\sum_q U_q(|q|-S)+S,\\
g_2&=\sum_q U_q(|q|-S)^2-S^2.
\end{aligned}
\]

Every \(U_q\) here includes its exact radius and character monomial.

## 3. Three necessary inequalities

The exact audit proves

\[
g_2(c)<0
\qquad
\text{for}\quad
\frac{1337}{10000}\le c\le\frac{803}{1000}
\]

by a complete-interval Bernstein sign certificate.  Since \(f_2>0\), any
point satisfying \(F\le0\) and \(G\le0\) must satisfy all three conditions

\[
\begin{aligned}
H(c,A)&:=F\bigl(c,A,B_{\min}(A)\bigr)\le0,\\
P(c,A)&:=G\left(c,A,\frac{A^2}{4}\right)\le0,\\
Q(c,A)&:=f_2G\left(c,A,-\frac{f_0+A f_1}{f_2}\right)\le0,
\end{aligned}
\]

where

\[
B_{\min}(A)=
\begin{cases}
0,&0\le A\le h,\\
h(A-h),&h\le A\le2h.
\end{cases}
\]

The first condition uses \(B\ge B_{\min}\) and \(f_2>0\).  The second uses
\(B\le A^2/4\) and \(g_2<0\).  For the third, \(F\le0\) gives
\(B\le-(f_0+A f_1)/f_2\); decreasing \(B\) can only increase \(G\), so
feasibility forces \(Q\le0\).

After multiplication by \(c\) or \(c^2\), the three functions are ordinary
bivariate polynomials with exact rational coefficients.  Thus the global
problem has been reduced from \((c,\lambda,\mu)\) to the signs of three
explicit polynomials on two closed rectangles.

## 4. Exact continuous cover at the upper radius

Fix

\[
r_U=\frac{382629}{10^6}=0.382629.
\]

The audit transforms \(H,P,Q\) into exact tensor-product Bernstein form on

\[
\frac{1337}{10000}\le c\le\frac{803}{1000},
\qquad
0\le A\le h
\]

and on the adjacent rectangle \(h\le A\le2h\).  It then uses exact midpoint
de Casteljau subdivision.  Every terminal box has all Bernstein coefficients
of at least one of \(H,P,Q\) strictly positive.  The final cover contains 14
leaves:

- 9 boxes are excluded by \(H>0\);
- 1 box is excluded by \(P>0\);
- 4 boxes are excluded by \(Q>0\).

The deepest character subdivision is six levels and the deepest invariant
subdivision is five levels.  This is a continuous interval proof.  It is not a
finite parameter sample.

## 5. The two character tails

At \(c_L=1337/10000\), the unweighted zero column satisfies

\[
U_0(c_L)>1.0005418736102262231,
\qquad
\partial_{\log c}U_0(c_L)<-0.94479666982550767059.
\]

Its second log derivative is a strictly positive \(q^2\) moment.  Hence the
first derivative is increasing, remains negative to the left of \(c_L\), and
\(U_0(c)>1\) for every \(c\le c_L\).  Multiplying by nonnegative affine
factors cannot restore feasibility.

At \(c_U=803/1000\), the active moments satisfy

\[
M_0(c_U)>1.0000443513376127801,
\qquad
M_1(c_U)>0.0008286359729472594055.
\]

Since \(\partial_{\log c}M_1=M_2>0\), both \(M_1\) and then \(M_0\) remain
above these exclusion thresholds for \(c\ge c_U\).  Because \(A,B\ge0\), the
active column is then strictly larger than one.

The tails and the two Bernstein rectangles cover every \(c>0\) and every
\(\lambda,\mu\ge0\).

## 6. Global enclosure

R0.53 supplies the exact all-order lower bound

\[
r_{\mathrm{prod}}^{\mathrm{opt}}
>0.382628602237879637.
\]

The present continuous exclusion gives

\[
r_{\mathrm{prod}}^{\mathrm{opt}}<0.382629.
\]

Therefore

\[
0.382628602237879637
<r_{\mathrm{prod}}^{\mathrm{opt}}
<0.382629,
\]

an interval of width

\[
3.97762120363\times10^{-7}.
\]

Relative to the complete affine-family upper bound from R0.52, the complete
product-family gain lies between the strict R0.53 lower factor

\[
1.0000107948905119688
\]

and the present upper factor

\[
1.0000118344531892886.
\]

Even perfect optimization inside the complete product family can improve the
R0.53 rational witness by a factor smaller than

\[
1.0000010395514554756.
\]

Thus the family fails the predeclared \(10^{-4}\) continuation threshold by
almost two orders of magnitude.

## 7. Diagnostic localization, kept separate

A deterministic 64-start floating search and a 100-digit diagonal solve both
locate the same symmetric candidate near

\[
\begin{aligned}
r&\approx0.382628912530472845561815315783,\\
c&\approx0.792805538586399517379515861568,\\
\lambda=\mu&\approx0.307861712230494785186988031158.
\end{aligned}
\]

Along \(\alpha=m+d,\ \beta=m-d\), implicit differentiation of the two active
equalities and diagonal stationarity gives the diagnostic coefficient

\[
\frac{dr}{d(d^2)}
\approx-20.2294483654601236551.
\]

This strongly indicates strict loss under symmetry breaking.  It is finite
high-precision evidence, not part of the exact global upper proof.  The global
theorem above remains valid even if that candidate were localized poorly.

## 8. Consequence for the next stage

Adding a second affine factor has now been globally bounded: it creates a real
but ppm-scale improvement, and the remaining optimization freedom is below
about \(1.04\) ppm relative to the R0.53 witness.  Increasing the polynomial
degree of the charge weight is therefore stopped under the stated criterion.

The higher-value unresolved task is no longer another weight fit.  It is to
establish, or disprove, a scale-critical comparison between the full
three-dimensional Fourier interaction operator and the reduced canonical edge
majorant used in R0.29--R0.54.
