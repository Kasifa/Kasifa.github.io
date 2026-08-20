# R0.68B-2b pilot — The full degree-eight heat jet is numerically nonzero

## 1. What was computed

The limiting eighth-order heat observable has six free carrier coordinates,
35 sign shuffles, and a seven-simplex kernel.  I lifted the reachable
dominant component of the 1792-state four-bit transfer through centred affine
moments of total degree eight and paired it with the complete heat observable.

The degree-eight binary64 pilot gives

\[
 B_{8,\mathrm{pilot}}
 =-1.4923824320396173\times10^{-8}.
\tag{1.1}
\]

This is a reproducible numerical result.  It is not yet a strict sign
certificate.

## 2. A 64-subset factorization

A direct six-variable channel lift has

\[
 {8+6\choose6}=3003
\tag{2.1}
\]

channels per state and

\[
 3003\times1792=5{,}381{,}376
\tag{2.2}
\]

moment coordinates.  Applying a separate dense translation matrix to every
seven-bit carrier pattern would be unnecessarily expensive.

For a translation pair \(\beta\le\alpha\), let

\[
 S(\alpha-\beta)
 =\{j:\alpha_j-\beta_j>0\}.
\tag{2.3}
\]

At one binary digit, the translation monomial is nonzero exactly when every
free carrier bit in this support equals one.  I therefore aggregate signed
state edges into only

\[
 2^6=64
\tag{2.4}
\]

subset transfer matrices.  The channel binomial operator and the state
transfer are then applied as two sparse matrix products.  The subset-zero
matrix is checked against the original exact digit transfer.

## 3. Dominant moments

Normalized power iteration on the exact sparse cycle reproduces the
R0.68B-1 observable mass:

\[
 -0.026126793630573877.
\tag{3.1}
\]

The maximum eigen residual is about \(5.5\times10^{-12}\).  For homogeneous
degree \(d\ge1\), the new moments solve

\[
 (16^d\nu I-W)m_d=b_d.
\tag{3.2}
\]

The pilot evaluates this inverse by its rapidly convergent Neumann series.
The observed relative linear residuals through degree eight are below
\(4.3\times10^{-16}\).

## 4. Degree convergence

The cumulative centred-jet pairings are

\[
\begin{array}{c|c}
 d & B_d\\ \hline
 0 & -1.3932312878841240\times10^{-8}\\
 1 & -1.5545964304118350\times10^{-8}\\
 2 & -1.4975644107395318\times10^{-8}\\
 3 & -1.4923417404112145\times10^{-8}\\
 4 & -1.4923646769558624\times10^{-8}\\
 5 & -1.4923812917440670\times10^{-8}\\
 6 & -1.4923824104330288\times10^{-8}\\
 7 & -1.4923824363133090\times10^{-8}\\
 8 & -1.4923824320396173\times10^{-8}.
\end{array}
\tag{4.1}
\]

The degree-eight correction is about \(4.27\times10^{-17}\).  Heat Taylor
orders 48 and 64 agree to about \(1.3\times10^{-26}\) in the coefficient
array.  The complete degree-eight run took about 19 seconds and used about
697 MiB at the largest recorded sample on the local arm64 workstation.

These convergence figures are evidence for a stable negative pairing.  They
do not replace an outward error bound.

## 5. What remains for a theorem

The natural degree-eight lift leaves a zero-eight-jet defect whose absolute
transfer scale is

\[
 \frac{16^6}{16^9}=\frac1{4096}.
\tag{5.1}
\]

Two finite estimates remain:

1. aggregate identical six-dimensional affine shifts before taking absolute
   values, and bound the defect after applying the dominant resolvent;
2. bound every ninth spatial derivative of the complete 35-shuffle
   seven-simplex heat observable.

If the product of those two bounds is smaller than the magnitude in (1.1),
the dominant heat projection has a strict negative sign.  If it is not, the
jet degree or the statewise resolvent expansion must be sharpened.

This pilot concerns one fixed eighth-order coefficient in a globally smooth
parallel-shear model.  It does not control all Picard orders, general
three-dimensional perturbations, singularity formation, or the
Navier--Stokes Millennium problem.
