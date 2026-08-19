# R0.33: exact Hankel obstructions to the direct positive-measure Padé route

## Status and boundary

R0.32 found a stable finite D-log Padé candidate near

\[
R\approx-0.7495
\]

for two fixed-charge transport series.  A pole table alone is not a
convergence theorem.  R0.33 tests the simplest structural theorem that might
have justified it: membership in a positive-measure Markov/Stieltjes class.

The test gives a decisive negative result.  Four low-order Hankel witnesses,
computed with exact rational arithmetic, prove that neither sign-transformed
transport series nor either logarithmic derivative belongs to the direct
positive-measure class.  This is an all-order exclusion: later coefficients
cannot repair a negative principal minor formed from the first few exact
coefficients.

This does **not** disprove the R0.32 candidate.  It removes one proposed proof
route.  Other Padé convergence classes, a transformed representation, an
analytic-background subtraction, or signed and complex measures remain open.
The result concerns the reduced edge system and gives no conclusion about
three-dimensional Navier--Stokes regularity or blow-up.

## 1. The sign-transformed fixed-charge series

R0.32 defines

\[
\widehat F_1(R)=\frac{F_1(R)}R.
\]

Move the negative-real candidate to the positive axis by setting \(x=-R\),
and normalize the two leading signs:

\[
B_U(x)=\widehat U_1(-x)=\sum_{n\ge0}b^U_nx^n,
\qquad
B_V(x)=-\widehat V_1(-x)=\sum_{n\ge0}b^V_nx^n.
\tag{1.1}
\]

The first coefficients are

\[
\begin{aligned}
B_U(x)&=\frac1{12}+\frac{13}{72}x+\frac{1055}{6048}x^2
+\frac{180989}{777600}x^3+\cdots,\\
B_V(x)&=\frac13+\frac1{18}x+\frac{811}{3024}x^2
+\frac{414727}{2721600}x^3+\cdots.
\end{aligned}
\tag{1.2}
\]

All 50 available coefficients of both series are positive.  That is an exact
finite observation, not an all-order positivity theorem.

For the D-log Padé objects, set

\[
H_U(x)=\frac{B_U'(x)}{B_U(x)},
\qquad
H_V(x)=\frac{B_V'(x)}{B_V(x)}.
\tag{1.3}
\]

## 2. The positive-measure condition being tested

Use the Markov generating-function convention

\[
M(x)=\int_{[0,\infty)}\frac{d\mu(t)}{1-xt}
=\sum_{n\ge0}m_nx^n,
\qquad \mu\ge0.
\tag{2.1}
\]

Then

\[
m_n=\int t^n\,d\mu(t).
\]

Consequently, for every real finite vector \(c=(c_0,\ldots,c_r)\),

\[
\sum_{i,j}c_ic_jm_{i+j}
=\int\left(\sum_i c_it^i\right)^2d\mu(t)\ge0,
\tag{2.2}
\]

and

\[
\sum_{i,j}c_ic_jm_{i+j+1}
=\int t\left(\sum_i c_it^i\right)^2d\mu(t)\ge0.
\tag{2.3}
\]

Thus both Hankel families

\[
\mathcal H^{(0)}_r=(m_{i+j})_{i,j=0}^{r-1},
\qquad
\mathcal H^{(1)}_r=(m_{i+j+1})_{i,j=0}^{r-1}
\tag{2.4}
\]

must be positive semidefinite.  This is the standard Stieltjes moment
criterion; see the classical moment-problem summary in
[NIST DLMF §18.40(ii)](https://dlmf.nist.gov/18.40.ii) and the equivalent
Hankel/S-fraction formulations in A. D. Sokal et al.,
[“Stieltjes moment sequences”](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v27i4p20/pdf/),
*Electronic Journal of Combinatorics* 27(4), 2020, P4.20.

Only necessity is used here.  One negative principal minor is enough to
exclude (2.1).

## 3. Exact theorem: all four direct representations fail

### Theorem 1: transport-series obstruction

Neither \(B_U\) nor \(B_V\) has a representation of the form (2.1) with a
nonnegative measure on \([0,\infty)\).

**Proof.**  For \(B_U\), the leading ordinary \(2\times2\) Hankel determinant
is

\[
\det\begin{pmatrix}
b^U_0&b^U_1\\
b^U_1&b^U_2
\end{pmatrix}
=\frac1{12}\frac{1055}{6048}-\left(\frac{13}{72}\right)^2
=\boxed{-\frac{437}{24192}}<0.
\tag{3.1}
\]

For \(B_V\), the first ordinary determinant is positive, but the shifted
determinant is

\[
\det\begin{pmatrix}
b^V_1&b^V_2\\
b^V_2&b^V_3
\end{pmatrix}
=\boxed{-\frac{43522897}{685843200}}<0.
\tag{3.2}
\]

Each matrix would have to be positive semidefinite under (2.1), so both
representations are impossible. \(\square\)

### Theorem 2: D-log obstruction

Neither \(H_U=B_U'/B_U\) nor \(H_V=B_V'/B_V\) has a representation of the
form (2.1) with a nonnegative measure on \([0,\infty)\).

**Proof.**  Exact formal division gives

\[
H_U(x)=\frac{13}{6}-\frac{32}{63}x
+\frac{249191}{50400}x^2+\cdots.
\tag{3.3}
\]

The shifted order-one Hankel matrix is simply \((-32/63)\), which is not
positive semidefinite.  For the second logarithmic derivative,

\[
H_V(x)=\frac16+\frac{797}{504}x
+\frac{98159}{100800}x^2+\cdots,
\tag{3.4}
\]

but its leading ordinary determinant is

\[
\det\begin{pmatrix}
1/6&797/504\\
797/504&98159/100800
\end{pmatrix}
=\boxed{-\frac{29699111}{12700800}}<0.
\tag{3.5}
\]

Therefore both D-log representations fail. \(\square\)

### Why a low-order calculation proves an all-order exclusion

The statement is not “the first 50 coefficients look non-Stieltjes.”  If an
infinite positive measure existed, every finite principal moment matrix made
from its coefficients would be positive semidefinite.  Equations (3.1),
(3.2), (3.3), and (3.5) use exact coefficients already fixed by the formal
edge recurrence.  No future coefficient can change any of these matrices.

## 4. Finite diagnostics beyond the theorem

The certificate also computes, exactly:

1. all 48 local Turán minors
   \(\Delta_n=b_{n-1}b_{n+1}-b_n^2\) for each transport series;
2. ordinary and shifted leading Hankel determinants through order 12 for
   \(B_U,B_V,H_U,H_V\);
3. all 49 available D-log coefficients.

Among the 48 local minors, 13 are negative for \(B_U\) and 20 are negative
for \(B_V\).  The first 49 \(H_U\) coefficients alternate in sign, while the
first 49 \(H_V\) coefficients are positive.  These tables show that the
obstruction is repeated rather than isolated, but they remain finite
diagnostics.  Theorems 1–2 need only the four boxed exact witnesses.

## 5. What this changes in the R0.32 interpretation

The R0.32 pole cluster cannot be promoted to a singularity theorem by simply
asserting that the sign-transformed series or their logarithmic derivatives
are Stieltjes functions.  The necessary moment inequalities fail exactly.

The candidate itself is unchanged.  In particular, R0.33 does not show that
the Padé poles are spurious.  It shows only that one standard mechanism for
controlling their convergence is unavailable in its direct form.

## 6. Reproducibility

The audit reads the pinned R0.32 certificate with SHA-256

```text
bd70ed05779631b729e89c269f82d287da361fdcea34e3c42703a712222f5575
```

and refuses to run if that file changes.  A formal run is

```text
python research/run_with_monitor.py \
  --output /tmp/r033-resources.csv --interval 0.05 -- \
  python research/edge_moment_structure_audit.py \
  --maximum-hankel-order 12 \
  --progress --progress-log /tmp/r033-progress.ndjson \
  --check --pretty --output /tmp/r033-edge-moment-structure.json
```

The computation uses `Fraction` and exact SymPy rational determinants.  It
has no random seed or floating-point decision.  Decimal values are display
fields only.

## 7. Next decision

R0.34 should not add another unstructured Padé table.  The next useful test
is one of the following:

1. search for a minimal analytic-background subtraction that restores a
   provable moment class, with the subtraction fixed independently of the
   high-order coefficients;
2. derive a continued-fraction or total-positivity structure directly from
   the edge recurrence, if one exists;
3. construct a validated analytic-continuation chain with explicit remainder
   bounds toward the negative axis.

The first option is cheapest to falsify and will be tested before any long
continuation computation.
