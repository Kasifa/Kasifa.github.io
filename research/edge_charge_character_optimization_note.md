# Global optimization of the multiplicative charge character

## R0.50 research note

### Abstract

R0.49 introduced the exact multiplicative charge weight

\[
\omega_s=c^s
\]

and fixed the simple rational value \(c=4/5\).  For the exact degree-80
center of the reduced canonical edge generating system, the true tail-input
column \((j,s)=(81,162)\) then had a unique threshold root in

\[
0.382618642388680778
<r_*^{(4/5)}
<0.382618642388680779.
\]

R0.50 leaves \(c\) free.  The active column is a positive Laurent polynomial

\[
A(r,c)=\sum_{i,q}b_{iq}r^ic^q,
\qquad b_{iq}>0,
\]

with degrees \(1\le i\le80\) and charge support \(-1\le q\le157\).  The
optimal character is determined by

\[
A(r,c)=1,
\qquad
\partial_{\log c}A(r,c)=0.
\]

Four complete-face exact Bernstein certificates and the
Poincare--Miranda theorem place a simultaneous solution in

\[
0.382619813709565<r_*<0.382619813709566,
\]

\[
0.8024563827<c_*<0.8024563828.
\]

For every fixed radius, \(A(r,e^t)\) is strictly convex and coercive in
\(t\).  Its minimum is strictly increasing in \(r\).  This structure makes
the simultaneous solution unique and proves that it is the unique global
maximum of the active threshold over all \(c>0\).

Coefficientwise charge envelopes extend the comparison to the complete
two-dimensional rational rectangle.  All 243 competing columns remain
strictly below the true \((81,162)\) column.  The nearest is the fixed
\(s=164\) sector, with exact positive gap approximately
\(1.4580280493538903081\times10^{-4}\).

Relative to the R0.49 upper root, the optimized lower threshold improves by a
factor greater than

\[
1.0000030613272706956,
\]

or about \(3.061\) parts per million.  The corresponding fixed-charge disk
radius \(r^3\) improves by a factor greater than

\[
1.0000091840099272895.
\]

The gain beyond \(c=4/5\) is therefore real but small.  The result is a global
optimization theorem for one exact Banach-weight family in the reduced
generating system.  It is not a theorem for arbitrary three-dimensional
velocity fields and does not prove or disprove three-dimensional
Navier--Stokes regularity.

---

## 1. The active Laurent polynomial

For a center monomial \(Z^mW^n\), write

\[
i=m+n,
\qquad
q=2n-m.
\tag{1.1}
\]

The multiplicative character norm is

\[
\|f\|_{r,c}
=\sum_{m+n>0}(m+n)|f_{mn}|r^{m+n}c^{2n-m}.
\tag{1.2}
\]

Charge additivity makes \(S_c[Z^mW^n]=c^qZ^mW^n\) an exact algebra
automorphism.  The output/input weight ratio for a center charge \(q\) and an
input charge \(s\) is exactly \(c^q\).  Consequently, for the true input
column \((j,s)=(81,162)\), the induced norm is

\[
A(r,c)
=\sum_{i,q}b_{iq}r^ic^q.
\tag{1.3}
\]

The exact degree-80 construction has

- 2161 center monomials;
- 2160 nonzero active Laurent terms;
- 1,113,168 ordered recurrence interactions;
- 158 distinct center charges from \(-1\) through \(157\);
- 27 negative-charge terms, 26 zero-charge terms, and 2107 positive-charge
  terms.

Every coefficient \(b_{iq}\) is positive and every degree \(i\) is positive.
The degree-80 center digest is

```text
056a0adba7f3cba41a6e9bd6d943a8f59be28f50f44c6035df1f68393ed26be7
```

which is the same pinned center used by R0.49.

---

## 2. Global structure of the optimization problem

Set \(t=\log c\) and

\[
F(r,t)=A(r,e^t)=\sum_{i,q}b_{iq}r^ie^{qt}.
\tag{2.1}
\]

For fixed \(c>0\),

\[
\partial_r A(r,c)
=\sum_{i,q}i b_{iq}r^{i-1}c^q>0
\qquad(r>0).
\tag{2.2}
\]

Thus \(A(0,c)=0\), \(A(r,c)\to\infty\) as \(r\to\infty\), and the equation
\(A(r,c)=1\) has one positive solution \(r_*(c)\).

For fixed \(r>0\),

\[
\partial_t^2F(r,t)
=\sum_{i,q}q^2b_{iq}r^ie^{qt}>0.
\tag{2.3}
\]

The charge support contains \(q=-1\) and positive charges.  Therefore
\(F(r,t)\to\infty\) as \(t\to-\infty\) and as \(t\to+\infty\).  It has one
global minimizer \(t(r)\).

Define the lower envelope

\[
M(r)=\min_{t\in\mathbb R}F(r,t).
\tag{2.4}
\]

If \(r_2>r_1>0\), then \(F(r_2,t)>F(r_1,t)\) for every \(t\).  Evaluating at
the minimizer for \(r_2\) gives

\[
M(r_2)=F(r_2,t(r_2))
>F(r_1,t(r_2))
\ge M(r_1).
\tag{2.5}
\]

Hence \(M\) is strictly increasing.  There is at most one simultaneous
solution of

\[
F(r,t)=1,
\qquad
\partial_tF(r,t)=0.
\tag{2.6}
\]

The implicit-function theorem applies because \(\partial_rF>0\).  Along the
threshold curve,

\[
\frac{d r_*}{dt}
=-\frac{\partial_tF}{\partial_rF}.
\tag{2.7}
\]

Moreover, \(r_*(c)\to0\) as \(c\to0\) or \(c\to\infty\), because the
negative or positive charge terms, respectively, diverge at every fixed
\(r>0\).  A global maximum exists in the interior and must satisfy (2.6).
Once existence is certified, (2.5)--(2.7) prove that the simultaneous root is
the unique global threshold maximum.

---

## 3. Exact two-dimensional root box

Because the minimum charge is \(-1\), define the two ordinary polynomials

\[
P(r,c)=c\bigl(A(r,c)-1\bigr),
\tag{3.1}
\]

and

\[
Q(r,c)=c\,\partial_tF(r,\log c)
=c\sum_{i,q}q b_{iq}r^ic^q.
\tag{3.2}
\]

The rational rectangle is

\[
\mathcal R=[r_L,r_U]\times[c_L,c_U],
\tag{3.3}
\]

where

\[
r_L=\frac{382619813709565}{10^{15}},
\qquad
r_U=\frac{382619813709566}{10^{15}},
\tag{3.4}
\]

and

\[
c_L=\frac{8024563827}{10^{10}},
\qquad
c_U=\frac{8024563828}{10^{10}}.
\tag{3.5}
\]

On each radius face, \(P\) is converted to exact Bernstein form over the
complete \(c\)-interval.  On each character face, \(Q\) is converted to exact
Bernstein form over the complete \(r\)-interval.  The four signed minima are

| face | required sign | Bernstein degree | minimum signed coefficient |
|---|:---:|---:|---:|
| \(r=r_L\) | \(-\) | 158 | \(7.6002388027103656410\times10^{-16}\) |
| \(r=r_U\) | \(+\) | 158 | \(3.0890673114272995553\times10^{-15}\) |
| \(c=c_L\) | \(-\) | 80 | \(1.5530691794509144743\times10^{-12}\) |
| \(c=c_U\) | \(+\) | 80 | \(1.1791231558039636147\times10^{-10}\) |

Every value in the table is a display of a strictly positive GMP rational.
Thus \(P\) has opposite signs on the two radius faces and \(Q\) has opposite
signs on the two character faces.  The Poincare--Miranda theorem gives a
simultaneous zero in \(\mathcal R\).

Combining this existence result with Section 2 yields the theorem.

### Theorem 3.1

For the exact degree-80 active Laurent polynomial of the reduced canonical
edge generating system, the multiplicative charge-character threshold has a
unique global maximizer \(c_*\), and

\[
0.8024563827<c_*<0.8024563828,
\tag{3.6}
\]

\[
0.382619813709565<r_*(c_*)<0.382619813709566.
\tag{3.7}
\]

No floating-point sign decision enters this theorem.

---

## 4. Uniform dominance of all 243 competitors

The optimum of the active column is not enough.  The true induced norm equals
that column only if every competitor is smaller throughout \(\mathcal R\).

For a center coefficient of charge \(q\), define lower and upper character
envelopes on \([c_L,c_U]\).  Since the only negative charge is \(-1\),

\[
c_U^{-1}\le c^{-1}\le c_L^{-1},
\tag{4.1}
\]

while for every \(q\ge0\),

\[
c_L^q\le c^q\le c_U^q.
\tag{4.2}
\]

Applying (4.1)--(4.2) coefficientwise gives a lower polynomial for the active
column and an upper polynomial for every competitor.  Positivity in \(r\)
then gives the rectangle sandwich

\[
C_{\mathrm{active}}(r,c)
\ge C_{\mathrm{active}}^{\mathrm{lower}}(r_L),
\tag{4.3}
\]

\[
C_{\mathrm{competitor}}(r,c)
\le C_{\mathrm{competitor}}^{\mathrm{upper}}(r_U).
\tag{4.4}
\]

The all-order charge-degree reduction covers

- 238 other fixed positive charges;
- the inactive endpoint of the active charge \(s=162\);
- the \(s=0,-1,1\) sectors;
- the complete infinite large-positive-charge sector \(s\ge241\).

The large-charge endpoint proof retains its exact odd and even Bernstein
certificates after applying the upper envelope.  No charge grid beyond the
finite theorem list and no tail-degree grid is used.

All 243 competitors have positive exact gaps.  The nearest is the fixed
\(s=164\) sector:

\[
C_{\mathrm{active}}^{\mathrm{lower}}(r_L)
-C_{s=164}^{\mathrm{upper}}(r_U)
=1.4580280493538903081\times10^{-4}>0.
\tag{4.5}
\]

Therefore the same true \((j,s)=(81,162)\) column is active throughout the
complete optimum box.

---

## 5. An exact rational restart beyond the R0.49 threshold

The simple rational point

\[
r=0.382619,
\qquad
c=0.8024563827
\tag{5.1}
\]

lies strictly beyond the R0.49 upper root at \(c=4/5\).  At (5.1), the true
tail maximum is still the \(s=162\) column and the linearization bound is

\[
L=0.99999609693061278829\ldots<1.
\tag{5.2}
\]

The contraction margin is

\[
\delta=1-L
=3.9030693872117144474\times10^{-6}.
\tag{5.3}
\]

Using \(\eta=\delta/10^6\), the exact total-degree-weighted residual norm is

\[
\|R\|_{r,c}
=1.7828790986376003423\times10^{-30}.
\tag{5.4}
\]

The residual allowance is

\[
1.5233904939537303958\times10^{-17},
\tag{5.5}
\]

and the ball mapping bound is

\[
3.9030541533067749118\times10^{-12}<\eta.
\tag{5.6}
\]

The Lipschitz upper bound is

\[
0.99999609695403120461\ldots<1.
\tag{5.7}
\]

The anisotropic fixed-point ball and the conjugated canonical-field
construction both close.  The proof uses the total-degree-weighted residual;
the certificate retains the smaller unweighted quantity only as an excluded
diagnostic.

---

## 6. Size and interpretation of the gain

Let \(r_U^{(49)}\) be the upper endpoint of the R0.49 root interval.  From
(3.7),

\[
\frac{r_L}{r_U^{(49)}}
>1.0000030613272706956.
\tag{6.1}
\]

Thus optimizing \(c\) beyond \(4/5\) adds slightly more than \(3.061\) parts
per million in the threshold radius.

The equivalent anisotropic polyradii remain

\[
\rho_Z=\frac r c,
\qquad
\rho_W=rc^2.
\tag{6.2}
\]

For the fixed-charge variable \(R=Z^2W\),

\[
\rho_R=\rho_Z^2\rho_W=r^3.
\tag{6.3}
\]

Therefore

\[
\frac{r_L^3}{(r_U^{(49)})^3}
>1.0000091840099272895.
\tag{6.4}
\]

The strict gain matters because it closes the optimization question left open
by R0.49.  Its small size matters just as much: \(c=4/5\) was already within
about three parts per million of the best threshold available in the entire
multiplicative family.  Further material improvement cannot come from a
different positive multiplicative character alone.

---

## 7. Journal figure and presentation sampling

The formal figure contains three panels:

1. 191 global samples of \(r_*(c)\) on \(0.45\le c\le1.40\);
2. 151 local samples on \(0.795\le c\le0.810\), expressed in parts per
   million relative to \(c=4/5\);
3. all 243 exact rectangle competitor gaps.

The curves use 90-decimal-digit Newton evaluation of the reconstructed exact
Laurent polynomial.  The maximum sampled equation residual is below
\(3.7\times10^{-91}\).  These samples illustrate shape only.  The root box,
four face signs, uniqueness, and competitor gaps come from the exact GMP
certificate.

The figure package includes

- source data and sampling metadata;
- plotting and independent validation scripts;
- exact formal and high-precision sampling resource logs;
- a manifest, caption, and SHA-256 list;
- PDF, SVG, and 600 dpi PNG outputs.

The 178 by 112 millimetre output was inspected in color, true grayscale, and
as a Poppler-rendered PDF.  Three CID TrueType font resources are embedded and
no Type 3 font is present.

---

## 8. Formal computation and provenance

The successful exact audit used

- Python 3.12.13;
- gmpy2 2.3.1 over GMP 6.3.0;
- 137.928040 seconds of scientific wall time;
- 138.1 seconds of monitored wall time;
- 70 process-tree resource samples at two-second intervals;
- 100.0% peak observed CPU and 104.234 MiB peak resident memory;
- no GPU, randomness, floating-point sign decision, charge grid beyond the
  theorem list, or tail-degree grid.

All 33 exact checks passed.  The certificate SHA-256 is

```text
fc173a2108ef881d21d9d54046085f0d5daf5cc33ed50e024ca32ec867f7b79a
```

The formal source commit is

```text
a9c469a96462e60655b0fea435177ececb8aef20
```

and the certificate archive commit is

```text
1430978ad7e4ac04f4b6f5daf04c641b05573edd
```

The development audit was run twice before the pinned formal run.  After
removing time and Git metadata, both development payloads and the formal
payload had the same canonical SHA-256 digest.  This checks that the long
rational envelope calculation is deterministic.

---

## 9. Mathematical value and boundary

R0.50 closes a precise problem left open by R0.49:

1. it proves global, rather than sampled, optimality in the full positive
   multiplicative character family;
2. it replaces a numerical stationary point with an exact two-dimensional
   root box;
3. it keeps the true active column and all 243 competitors stable throughout
   that box;
4. it certifies a simple rational restart beyond the previous sharp threshold;
5. it quantifies the remaining improvement and shows that the rational choice
   \(c=4/5\) was already almost optimal.

The result does not cross the main gap to the Millennium Problem.  The current
system is a reduced two-variable generating model.  There is still no theorem
that embeds arbitrary divergence-free three-dimensional initial data into
this model, propagates a scale-critical PDE norm, or controls the complete
Fourier interaction geometry.  The optimized threshold is not a regularity
time, a singularity location, or a critical Reynolds number.

---

## 10. The next falsifiable question

Positive multiplicative characters of the charge group are exhausted by
\(c^s\), so continuing to tune \(c\) cannot produce another structural gain.
The next smallest extension that keeps an algebra constant of one is the
submultiplicative affine correction

\[
\omega_s(c,\lambda)
=c^s(1+\lambda|s|),
\qquad c>0,
\quad \lambda\ge0.
\tag{10.1}
\]

Indeed,

\[
1+\lambda|a+b|
\le(1+\lambda|a|)(1+\lambda|b|).
\tag{10.2}
\]

The next question is:

> Does a rational \(\lambda>0\), jointly optimized with \(c\), give a
> materially larger certified threshold while preserving an all-order proof
> for every charge and tail degree?

The acceptance tests should be:

1. derive the exact column ratio
   \(c^q(1+\lambda|s+q|)/(1+\lambda|s|)\);
2. locate candidate active-column changes before any formal claim;
3. construct exact rational parameter boxes for \((r,c,\lambda)\);
4. prove all finite fixed-charge and infinite large-charge bounds uniformly;
5. compare any gain with the extra loss caused by abandoning exact character
   conjugacy;
6. produce a negative certificate if \(\lambda=0\) is already optimal or if
   a competitor switches first.

Either outcome would identify whether the remaining obstruction is specific
to exact characters or persists for a wider submultiplicative Banach geometry.
It would still remain separate from any claim about the full
three-dimensional Navier--Stokes equations.
