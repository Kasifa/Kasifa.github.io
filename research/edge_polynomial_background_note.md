# R0.34: exact exclusion of bounded-degree polynomial Stieltjes backgrounds

## Status and boundary

R0.33 proves that the sign-transformed transport series

\[
B_U(x),\qquad B_V(x)
\]

and their logarithmic derivatives

\[
H_U(x)=\frac{B_U'(x)}{B_U(x)},\qquad
H_V(x)=\frac{B_V'(x)}{B_V(x)}
\]

are not direct nonnegative-measure Markov/Stieltjes series.  R0.34 tests the
next simplest repair: subtract an arbitrary polynomial analytic background
before asking for a positive-measure representation.

The result is again negative, and substantially stronger than checking one
chosen subtraction.  No fitting is performed.  The polynomial coefficients
are allowed to be arbitrary real numbers.  Exact tail Hankel witnesses prove
that the representation is impossible for every background polynomial up to
degree 43 for \(B_U\), 44 for \(B_V\), 46 for \(H_U\), and 45 for \(H_V\).

These are universal theorems for the stated finite-dimensional background
classes.  The numerical degree thresholds come from the available 50/49
exact coefficients.  They do not exclude a genuinely infinite analytic
background, and they do not prove or disprove the R0.32 singularity candidate
near \(R=-0.7495\).  Nothing here proves three-dimensional Navier--Stokes
regularity or blow-up.

## 1. The background class

For one of the four exact formal series

\[
C(x)=\sum_{n\ge0}c_nx^n,
\]

consider a decomposition

\[
C(x)=P_d(x)+M(x),
\qquad
M(x)=\int_{[0,\infty)}\frac{d\mu(t)}{1-xt},
\qquad \mu\ge0,
\tag{1.1}
\]

where \(P_d\) is any real polynomial with \(\deg P_d\le d\).  No sign,
size, or interpolation condition is imposed on its coefficients.

Writing \(M(x)=\sum m_nx^n\), polynomial subtraction leaves the tail fixed:

\[
m_n=c_n\qquad(n>d).
\tag{1.2}
\]

This elementary invariance makes the class falsifiable without choosing or
fitting \(P_d\).

## 2. Tail Gram matrices

Let \(s>d\), and let \(I=\{i_0,\ldots,i_{r-1}\}\) be a finite set of
nonnegative monomial indices.  A Stieltjes moment sequence must satisfy

\[
G^{(s,I)}_{\alpha\beta}
=m_{s+i_\alpha+i_\beta}
=\int t^s t^{i_\alpha}t^{i_\beta}\,d\mu(t).
\tag{2.1}
\]

Because \(t^s\ge0\) on \([0,\infty)\), this is a Gram matrix and hence

\[
G^{(s,I)}\succeq0.
\tag{2.2}
\]

Every coefficient appearing in (2.1) has index at least \(s>d\), so (1.2)
replaces it by the corresponding exact coefficient of \(C\).  One negative
determinant therefore excludes **all** possible coefficients of \(P_d\).

## 3. Exact universal exclusions

### Theorem 1: transport backgrounds

There is no representation (1.1) for \(C=B_U\) with any real polynomial
background of degree at most 43.  There is no such representation for
\(C=B_V\) with any real polynomial background of degree at most 44.

**Proof.**  For \(B_U\), take

\[
s=44,\qquad I=\{0,1,2\}.
\]

The required Gram matrix is

\[
G_U=
\begin{pmatrix}
b^U_{44}&b^U_{45}&b^U_{46}\\
b^U_{45}&b^U_{46}&b^U_{47}\\
b^U_{46}&b^U_{47}&b^U_{48}
\end{pmatrix}.
\tag{3.1}
\]

Exact rational evaluation gives \(\det G_U<0\).  Its reduced numerator and
denominator have 918 and 914 decimal digits; the SHA-256 of the canonical
fraction string is

```text
c8fb036dea3c66834b07b39666537f0b85ea138ac105b6315f7519d0488a3e2a
```

The full fraction and matrix entries are stored in the machine certificate.
Since \(44>d\) for every \(d\le43\), the polynomial cannot change any entry
of (3.1).

For \(B_V\), use

\[
s=45,\qquad I=\{0,1,2\},
\]

which produces the index matrix

\[
\begin{pmatrix}
45&46&47\\
46&47&48\\
47&48&49
\end{pmatrix}.
\tag{3.2}
\]

Its exact determinant is negative.  The reduced numerator and denominator
have 941 and 935 digits, and the fraction-string SHA-256 is

```text
516aaee23c11bcf030247d5d3d657ad754289d83ade88d1a70bafba1fb782ccb
```

Thus every background degree \(d\le44\) is excluded. \(\square\)

### Theorem 2: D-log backgrounds

There is no representation (1.1) for \(C=H_U\) with a polynomial background
of degree at most 46, and none for \(C=H_V\) with a polynomial background of
degree at most 45.

**Proof.**  The exact coefficient \(h^U_{47}\) is negative.  Taking
\(s=47\) and \(I=\{0\}\) makes the required Gram matrix the one-by-one
matrix \((h^U_{47})\).  A background of degree at most 46 cannot alter it.

For \(H_V\), take \(s=46\) and \(I=\{0,1\}\).  The exact determinant

\[
h^V_{46}h^V_{48}-(h^V_{47})^2
\tag{3.3}
\]

is negative, while every entry lies beyond degree 45. \(\square\)

## 4. What “largest threshold” means here

The audit enumerates every principal minor

\[
\det\bigl(c_{s+i_\alpha+i_\beta}\bigr)_{\alpha,\beta}
\]

that can be formed from the available coefficient window, contains monomial
index zero, and has tail start \(40\le s\le49\) for \(B_U,B_V\) or
\(40\le s\le48\) for \(H_U,H_V\).  It finds no negative tested principal
minor at a larger \(s\) than the four witnesses above.

This proves maximality only **inside this finite search window**.  It does not
show that a polynomial of degree 44 works for \(B_U\), that degree 45 works
for \(B_V\), or that any higher-degree repair exists.  A later exact
coefficient could provide another negative tail witness.

## 5. Research meaning

R0.34 eliminates a broad family of ad hoc rescues.  It is not possible to
remove an arbitrary low-order Taylor jet--even one with more than forty free
coefficients--and then claim that the remaining exact series is a positive
moment sequence.  This makes the negative R0.33 conclusion robust against
all bounded-degree polynomial backgrounds covered by the theorem.

The result does not address a genuinely infinite analytic background.  Such
a function changes every tail coefficient.  Without a proved radius and
coefficient bound for that background, finite data cannot distinguish it
from an arbitrary correction.  Allowing an unconstrained infinite
background would therefore make the proposed Stieltjes explanation
unfalsifiable rather than stronger.

The appropriate next step is not to fit more background coefficients.  It is
to leave this positive-measure route and construct a validated analytic
continuation mechanism with explicit remainder bounds.

## 6. Reproducibility

The audit pins both upstream certificates:

```text
R0.32  bd70ed05779631b729e89c269f82d287da361fdcea34e3c42703a712222f5575
R0.33  ccbf8ab05615378f6d4b9824e86b679b6d0df2882cbc6e563b063b8769292367
```

A formal run is

```text
python research/run_with_monitor.py \
  --output /tmp/r034-resources.csv --interval 0.02 -- \
  python research/edge_polynomial_background_audit.py \
  --minimum-tail-start 40 \
  --progress --progress-log /tmp/r034-progress.ndjson \
  --check --pretty --output /tmp/r034-polynomial-background.json
```

Every search determinant uses exact rational arithmetic.  Each theorem
witness is recomputed independently by the Leibniz formula over Python
`Fraction`.  Decimal values are display fields only, and no random seed is
used.

## 7. Next decision

R0.35 will begin the analytic-continuation route.  The first task is to write
the fixed-charge extraction and charge ladder as an explicit operator system
on a weighted sequence space, identify the domain needed to move from the
proved circle toward the negative real axis, and state a continuation lemma
with a checkable norm condition.  No singularity claim will be made until an
actual chain of validated domains reaches the R0.32 candidate.
