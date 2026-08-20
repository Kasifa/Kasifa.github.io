# R0.68B-2a — An exact first-cycle sign for the complete eighth-order heat sum

## 1. Scope

R0.68B-1 proved that the zero-time eighth-order correlation has a strictly
negative dominant projection.  The complete coefficient contains a
seven-simplex heat kernel, so the zero-time result does not determine its
sign.  I first check the smallest stationary four-bit block exactly.  This
fixes the path convention and gives a finite-scale diagnostic before the
asymptotic heat projection is constructed.

The result is

\[
 \boxed{
  0.00741508936
  < S_{8,q}^{(M=16)}
  < 0.00741508940.}
\tag{1.1}
\]

This is a positive sign at one finite scale.  It is not the sign of the
dominant asymptotic projection.

## 2. Complete finite path family

Set

\[
 M=16,\qquad H=64,\qquad q=2,\qquad Q=66.
\tag{2.1}
\]

For offsets in \(\{0,\ldots,15\}\), the carrier constraint is

\[
 A+B+C+D-E-F-G=Q.
\tag{2.2}
\]

An independent one-dimensional convolution gives exactly

\[
 7{,}823{,}536
\tag{2.3}
\]

valid labelled carrier tuples.  There are \(\binom74=35\) sign shuffles, so
the complete sum contains

\[
 273{,}823{,}760
\tag{2.4}
\]

signed ordered paths.  At zero Taylor degree, the signed carrier mass is
\(11{,}896\), independently matching the first R0.68B-1 cycle.  Including
all shuffles gives

\[
 J_0=35\times11{,}896=416{,}360.
\tag{2.5}
\]

## 3. Exact suffix compression

Directly visiting all paths at every Taylor degree is unnecessary.  For a
suffix of the ordered carrier list, keep

\[
 (p,s,u)
 =\bigl(\text{number of positive carriers},
        \text{signed suffix sum},
        \text{suffix square sum}\bigr).
\tag{3.1}
\]

Because the path ends at frequency zero, the next nonzero integer heat rate
is exactly

\[
 \beta=s^2+u=H^2\alpha.
\tag{3.2}
\]

Thus paths with the same \((p,s,u)\) have identical future updates.  Their
signed complete-homogeneous polynomials can be added before the next carrier
is chosen.  At the seven depths the exact state counts are

\[
 32,\ 528,\ 5796,\ 38804,\ 105499,\ 84553,\ 4178.
\tag{3.3}
\]

The largest rate retained by the endpoint-feasible recursion is

\[
 \max\beta_j=114888,
 \qquad
 \max\alpha_j=\frac{114888}{4096}=28.048828125.
\tag{3.4}
\]

This compression is exact.  No path sampling or floating-point summation is
used.

## 4. Rational Taylor enclosure

With seven nonzero rates and one zero endpoint rate,

\[
 K_T^{(7)}
 =\sum_{n=0}^{\infty}
 \frac{(-1)^n h_n(\alpha_0,\ldots,\alpha_6)T^{n+7}}
 {(n+7)!},
 \qquad T=\frac{\log2}{2}.
\tag{4.1}
\]

The audit computes every signed integer coefficient through degree \(44\).
The time is enclosed by the positive rational series
\(T=\operatorname{atanh}(1/3)\).  If \(A=\max\alpha_j\), then

\[
 h_n(\alpha_0,\ldots,\alpha_6)
 \le {n+6\choose6}A^n.
\tag{4.2}
\]

After multiplying by all \(273{,}823{,}760\) absolute path weights, this
gives an omitted-tail bound below

\[
 1.31\times10^{-11}.
\tag{4.3}
\]

The exact rational endpoints and their SHA-256 hashes are stored in the
certificate.  The guarded decimal interval (1.1) follows.

## 5. Interpretation and next step

The first-cycle heat sum is positive, while R0.68B-1 found a negative
dominant zero-time projection.  This sign difference is expected to be
possible: heat weights change the relative contribution of paths, and a
finite block need not have the asymptotic sign.

The next calculation is therefore not extrapolation.  It is a centred
degree-eight Taylor-jet lift of the limiting six-variable heat observable.
There are

\[
 {8+6\choose6}=3003
\tag{5.1}
\]

moment channels per transfer state.  Degree eight is the natural first
target because the zero-eight-jet remainder contracts by

\[
 \frac{16^6}{16^9}=\frac1{4096}
\tag{5.2}
\]

over one four-bit block.  I will compute the dominant jet pairing, aggregate
identical affine shifts before taking absolute values, and then bound the
ninth derivatives of the full 35-shuffle seven-simplex observable.

Nothing in this note controls every Picard order or proves singularity, norm
inflation, or global regularity for the three-dimensional Navier--Stokes
equations.
