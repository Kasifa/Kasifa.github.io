# R0.40: exact two-endpoint transport theorem

## Status and conclusion boundary

R0.39 certified the reduced active and normalized transport fields on the
isotropic polydisc of radius \(397/2000\). Its active-tail theorem retained
every input charge, but its normalized transport estimate maximized the input
slope separately for every center monomial. That interchange of maximum and
summation became the binding loss.

Here I keep the common input slope until after the complete column sum. A
convexity argument reduces every input slope to two actual endpoint monomials,
and a monotonicity argument reduces every input degree to degree one. Exact
rational arithmetic then proves the common isotropic radius

\[
 \boxed{r_*=\frac{32}{125}=0.256}
\tag{0.1}
\]

for the reduced active field \(a\) and normalized transport fields \(U,V\).
The radius gain relative to R0.39 is

\[
 \frac{32/125}{397/2000}
 =\frac{512}{397}
 \approx1.28967,
\tag{0.2}
\]

and the corresponding fixed-charge \(R=Z^2W\) disk grows by
\((512/397)^3\).

This is an all-order theorem for the reduced edge generating system. It is
not a theorem about global regularity or finite-time blow-up for the full
three-dimensional Navier--Stokes equation. The finite R0.32 Padé cluster
remains a diagnostic only.

## 1. The exact transport column

Write a center monomial in degree-charge coordinates as \((i,q)\) and an
input monomial as \((j,s)\). The normalized transport operator is

\[
 T_a f=(\mathcal L-1)^{-1}\{a,f\}.
\tag{1.1}
\]

The log-canonical determinant and the output divisor give the exact
coefficient

\[
 \beta_{i,q;j,s}
 =\frac{is-qj}{3(i+j-1)}.
\tag{1.2}
\]

In the weighted Wiener norm

\[
 \|f\|_{\mathcal B_r}
 =\sum_{j,s}j|f_{j,s}|r^j,
\tag{1.3}
\]

the column factor for one base monomial is

\[
 \frac{i+j}{j}|\beta_{i,q;j,s}|
 =\frac{i+j}{i+j-1}\frac{|i(s/j)-q|}{3}.
\tag{1.4}
\]

For a polynomial center \(p\), different center monomials send a fixed input
monomial to different output exponents. Its complete absolute column sum is
therefore

\[
 K_{j,s}(r)
 =\sum_{i,q}|p_{i,q}|r^i
 \frac{i+j}{i+j-1}\frac{|i(s/j)-q|}{3}.
\tag{1.5}
\]

The induced \(\ell^1\) norm is the supremum of these exact column sums.

## 2. Convexity closes every input slope

Every bivariate input monomial satisfies

\[
 -1\le x=\frac{s}{j}\le2.
\tag{2.1}
\]

For fixed \(j\), equation (1.5) is a positive sum of absolute affine
functions of \(x\), hence it is convex. A convex function on an interval
attains its maximum at an endpoint. Thus

\[
 \sup_s K_{j,s}(r)
 =\max\{K_{j,-j}(r),K_{j,2j}(r)\}.
\tag{2.2}
\]

The endpoints are not a continuous relaxation artifact: \(s=-j\) and
\(s=2j\) are the actual pure-\(Z\) and pure-\(W\) monomials.

At either endpoint every factor

\[
 \frac{i+j}{i+j-1}=1+\frac1{i+j-1}
\tag{2.3}
\]

decreases with \(j\). Therefore the maximum over every input degree
\(j\ge1\) occurs at \(j=1\). Since the active center obeys
\(-1\le q\le2i\), the two exact columns are

\[
 P_-(r)
 =\sum_{i,q}|p_{i,q}|r^i
 \frac{i+1}{i}\frac{i+q}{3},
\tag{2.4}
\]

\[
 P_+(r)
 =\sum_{i,q}|p_{i,q}|r^i
 \frac{i+1}{i}\frac{2i-q}{3}.
\tag{2.5}
\]

Consequently

\[
 \boxed{\|T_p\|_{\mathcal B_r\to\mathcal B_r}
 =\max\{P_-(r),P_+(r)\}.}
\tag{2.6}
\]

This is an identity for the finite polynomial operator and an all-order
statement about every input degree, charge, and slope. R0.39 instead used
the larger quantity obtained by putting the maximum inside the sum.

## 3. The unknown strict tail

Let \(h\) be supported on active degrees \(i>N\). At \(x=-1\), divide the
endpoint factor by the input weight \(i\). Its maximum over
\(-1\le q\le2i\) occurs at \(q=2i\):

\[
 \frac1i\frac{i+1}{i}\frac{i+q}{3}
 \le\frac{i+1}{i}
 \le\frac{N+2}{N+1}.
\tag{3.1}
\]

At \(x=2\), the maximum occurs at \(q=-1\):

\[
 \frac1i\frac{i+1}{i}\frac{2i-q}{3}
 \le\frac{(i+1)(2i+1)}{3i^2}
 \le\frac{(N+2)(2N+3)}{3(N+1)^2}.
\tag{3.2}
\]

Both right-hand sides decrease with \(i\). If
\(\|h\|_{\mathcal B_r}\le\varepsilon\), equations (2.6), (3.1), and (3.2)
give

\[
 \|T_{p+h}\|
 \le\max\left\{
 P_-(r)+\frac{N+2}{N+1}\varepsilon,\,
 P_+(r)+\frac{(N+2)(2N+3)}{3(N+1)^2}\varepsilon
 \right\}.
\tag{3.3}
\]

No finite input partition or slope cutoff appears in (3.3).

## 4. Exact degree-80 restart at \(32/125\)

Take \(N=80\) and \(r_*=32/125\). The R0.39 all-order active-tail kernel
gives

\[
 Z_{80}(r_*)
 \approx0.99440931119167253866<1.
\tag{4.1}
\]

The exact degree-80 residual contains every term in degrees 81 through 160.
Set

\[
 \varepsilon=\frac{1-Z_{80}(r_*)}{10^6}.
\tag{4.2}
\]

The formal certificate checks the complete residual, ball-image, and
Lipschitz inequalities in exact rational arithmetic.

For the polynomial transport center,

\[
 P_-(r_*)\approx0.85855627725994366797,
\qquad
 P_+(r_*)\approx0.86219920724580816843.
\tag{4.3}
\]

After the strict-tail contribution in (3.3), the bound remains strictly
below one. The precise value is recorded by the exact certificate. The
R0.39 termwise endpoint maximum is greater than one at the same radius, so
the new radius does not follow from the previous transport estimate.

## 5. Nearby negative control

At the adjacent rational probe

\[
 r_{\mathrm{probe}}=\frac{257}{1000}=0.257,
\tag{5.1}
\]

the exact polynomial two-endpoint transport bound is still only about
\(0.867286688\). The active-tail sufficient bound, however, becomes

\[
 Z_{80}(r_{\mathrm{probe}})
 \approx1.0002561524370209106>1.
\tag{5.2}
\]

Thus R0.40 removes the old transport bottleneck and transfers the current
proof boundary to the active-tail estimate. Failure of (5.2) is not
evidence that the reduced fields are nonanalytic at \(0.257\), and it is not
evidence of a Navier--Stokes singularity.

## 6. Finite regressions

The certificate keeps finite implementation evidence separate from the
all-order theorem:

1. the exact coefficient (1.2) is compared with the original bracket
   implementation on every ordered pair through degree 10;
2. complete transport-column scans at input degrees 1, 2, 5, 20, and 81
   stay below the two-endpoint theorem;
3. the degree-one scan attains the theorem at one of the two endpoint
   monomials;
4. the active recurrence residual vanishes through degree 80 and includes
   every term through degree 160;
5. every threshold decision uses exact GMP rationals.

These finite regressions check the implementation. Equations (2.1)--(3.3)
provide the all-order closure.

## 7. Value and remaining distance

Within the reduced edge model, the common radius increases from \(0.1985\)
to \(0.256\). The more useful structural result is that the normalized
transport norm is an exact maximum of two endpoint columns, rather than a
sum of termwise endpoint maxima. The current endpoint is now limited by
the active correction theorem.

No theorem here shows that the reduced edge system controls all
three-dimensional critical Navier--Stokes interactions. The result should
be read as a rigorous theorem about one derived generating system, not as a
solution or partial solution of the Millennium problem.

## 8. Next mathematical question

R0.41 should sharpen the active-tail kernel near its worst input charge
\(s=162\). The adjacent failure at \(0.257\) is the acceptance test. A
finite column scan may reveal the lost correlation between center charge,
input degree, and the fixed-charge minimum degree, but the final theorem
must still cover every uncomputed degree and every input charge.

## Reproduction

Run research/edge_slope_resolved_transport_audit.py from the repository root.
The formal certificate pins its clean source commit and the SHA-256 digest
of the R0.39 input certificate. The computation uses exact GMP rationals,
an append-only progress log, and a process-tree resource log. It has no
random seed, GPU dependency, or floating-point sign decision.

## References

1. R0.29, *Canonical transport reduction and the infinite charge ladder*.
2. R0.37, *A weighted-Wiener restart beyond the R0.31 radius*.
3. R0.38, *A tail-aware Newton restart beyond the R0.37 radius*.
4. R0.39, *Charge-resolved tail and transport bounds*.
