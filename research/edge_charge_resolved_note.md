# R0.39: charge-resolved tail and transport bounds

## Status and conclusion boundary

R0.38 certified the reduced active and normalized transport series on the
isotropic polydisc of radius (59/500).  Its tail theorem was all order, but
it discarded the input and output charges after applying the mixed-layer
estimate.  At larger radii that scalar estimate fails.

Here I retain the charge of every input column.  The resulting induced
(ell^1) bound is finite for charges (-1le s<241), with one analytic
estimate closing all (sge241).  A second charge-resolved estimate treats
the normalized transport operator.  Exact rational arithmetic then proves
the common isotropic radius

\[
 \boxed{r_* = \frac{397}{2000}=0.1985}
\tag{0.1}
\]

for the reduced active field (a) and normalized transport fields (U,V).
The radius gain relative to R0.38 is (397/236\approx1.68220); the
corresponding fixed-charge (R=Z^2W) disk grows by the exact factor

\[
 \left(\frac{397}{236}\right)^3
 =\frac{62570773}{13144256}
 \approx4.76031.
\tag{0.2}
\]

This is an all-order theorem for the reduced edge generating system.  It is
not a theorem about global regularity or finite-time blow-up for the full
three-dimensional Navier--Stokes equation.  The finite R0.32 Padé cluster
remains a diagnostic only.

## 1. Degree-charge coordinates give the exact derivative coefficient

For a monomial (Z^zW^w), write

\[
 i=z+w,
 \qquad
 q=2w-z.
\tag{1.1}
\]

Then

\[
 z=\frac{2i-q}{3},
 \qquad
 w=\frac{i+q}{3}.
\tag{1.2}
\]

If the left monomial has coordinates ((i,q)) and the right one has
((j,s)), their log-canonical determinant is

\[
 z_iw_j-w_iz_j=\frac{is-qj}{3}.
\tag{1.3}
\]

The reduced active map from R0.36 is

\[
 \Phi(f)
 = (\mathcal L-1)^{-1}
 \left[
 \mathcal Q^{-1}(I-\Pi_0)\{f,\mathcal Qf\}
 +\mathcal L^{-1}\Pi_0\{f,\mathcal Lf\}
 \right].
\tag{1.4}
\]

Polarizing (1.4) and inserting (1.3) gives one output monomial of degree
(i+j) and charge (q+s).  Its exact coefficient in
(D\Phi(p_{i,q})h_{j,s}) is

\[
 \gamma_{i,q;j,s}
 =\frac{(is-qj)(s-q)}{3(s+q)(i+j-1)},
 \qquad s+q\ne0,
\tag{1.5}
\]

and on the zero-charge output,

\[
 \gamma_{i,q;j,s}
 =\frac{(is-qj)(j-i)}{3(i+j)(i+j-1)},
 \qquad s+q=0.
\tag{1.6}
\]

The certificate compares (1.5)--(1.6) with the original polynomial
implementation on every ordered admissible pair through degree 10.  All
2209 pairs agree exactly.  This finite comparison checks the implementation;
the formulas themselves follow algebraically from (1.3)--(1.4).

## 2. Exact charge columns in the weighted Wiener space

Use the R0.37 norm

\[
 \|f\|_{\mathcal B_r}
 =\sum_{j,s}j\,|f_{j,s}|r^j.
\tag{2.1}
\]

Let (p_N) have degree at most (N), and let the correction (h) be
supported on degrees (j>N) in the active cone (s\ge-1).  Put

\[
 A_{i,q}=|p_{i,q}|.
\tag{2.2}
\]

For a fixed input monomial ((j,s)), (1.5)--(1.6) give the exact positive
column sum

\[
 K_{j,s}(r)
 =\sum_{i,q}
 \frac{i+j}{j}
 |\gamma_{i,q;j,s}|A_{i,q}r^i.
\tag{2.3}
\]

Different base monomials produce different output exponents.  Applying the
triangle inequality to a general tail therefore gives

\[
 \|D\Phi(p_N)h\|_{\mathcal B_r}
 \le
 \left(\sup_{j>N,\ s\ge-1}K_{j,s}(r)\right)
 \|h\|_{\mathcal B_r}.
\tag{2.4}
\]

The task is to bound the infinite supremum in (2.4), not merely to scan a
few degrees.

## 3. Finite charges and the infinite-charge closure

For a fixed input charge (s\ge-1), let (J_s) be the smallest integer
satisfying

\[
 J_s>N,
 \qquad J_s\ge\lceil s/2\rceil,
 \qquad J_s+s\equiv0\pmod3.
\tag{3.1}
\]

Every monomial of charge (s) and degree above (N) then has
(j\ge J_s).  For (s+q\ne0), rewrite the norm factor in (2.3) as

\[
 \frac{i+j}{i+j-1}
 \left|\frac{is}{j}-q\right|
 \frac{|s-q|}{3|s+q|}.
\tag{3.2}
\]

Both (1/j) and ((i+j)/(i+j-1)) decrease with (j).  Thus every degree
in the fixed charge column obeys

\[
 B_{i,q;s}^{\mathrm{fin}}
 =
 \frac{i+J_s}{i+J_s-1}
 \left(|q|+\frac{i|s|}{J_s}\right)
 \frac{|s-q|}{3|s+q|}.
\tag{3.3}
\]

If (s+q=0), the active-cone restrictions leave only
((q,s)=(-1,1),(0,0),(1,-1)).  The middle case vanishes, and the other two
are bounded by

\[
 B_{i,q;s}^{\mathrm{fin}}
 =\frac{i+J_s}{3(i+J_s-1)}.
\tag{3.4}
\]

Equations (3.3)--(3.4) treat the 242 charges

\[
 -1\le s\le240
\tag{3.5}
\]

with exact rational column bounds.

It remains to close all (s\ge241).  Write (x=s/j\).  Monomial
admissibility gives (0\le x\le2).  For every base charge (q\ge0),

\[
 \frac{|s-q|}{s+q}\le1,
 \qquad
 |ix-q|\le\max\{q,|2i-q|\}.
\tag{3.6}
\]

For the only negative base charge (q=-1),

\[
 \frac{s+1}{s-1}\le\frac{242}{240},
 \qquad
 |ix+1|\le2i+1.
\tag{3.7}
\]

Finally (j\ge N+1) gives

\[
 \frac{i+j}{i+j-1}\le\frac{i+N+1}{i+N}.
\tag{3.8}
\]

Combining (3.6)--(3.8) produces one explicit rational bound for the entire
infinite sector (s\ge241).  Define (Z_N(r)) as the maximum of the 242
finite column bounds and this final sector bound.  Then (2.4) becomes the
all-order estimate

\[
 \boxed{
 \|D\Phi(p_N)h\|_{\mathcal B_r}
 \le Z_N(r)\|h\|_{\mathcal B_r}.
 }
\tag{3.9}
\]

No finite degree cutoff is used for (h) in (3.9).

## 4. Exact degree-80 restart at (397/2000)

Take (N=80) and (r_*=397/2000).  The 242 finite charge columns and the
large-charge sector give

\[
 Z_{80}(r_*)
 \approx0.68960111886114510073<1.
\tag{4.1}
\]

The maximum certified column is the input-charge (s=162) sector.  The
single analytic sector (s\ge241) is bounded by

\[
 0.47394349392419015391.
\tag{4.2}
\]

At the same radius, the R0.38 scalar tail estimate is

\[
 2.0387664799903112732>1.
\tag{4.3}
\]

Thus the new radius does not follow from the previous charge-blind theorem.

The exact degree-80 residual contains 6345 terms in degrees 81 through 160,
and

\[
 Y=\|F(p_{80})\|_{\mathcal B_{r_*}}
 \approx1.7707144350063116838\times10^{-51}.
\tag{4.4}
\]

Let (m=1-Z_{80}(r_*)), and choose the exact rational ball radius

\[
 \varepsilon=\frac{m}{10^6}
 \approx3.1039888113885489927\times10^{-7}.
\tag{4.5}
\]

The residual satisfies

\[
 Y<m\varepsilon-3\varepsilon^2,
\tag{4.6}
\]

the ball-image bound is approximately

\[
 2.1405170476899816430\times10^{-7}<\varepsilon,
\tag{4.7}
\]

and the Lipschitz constant is

\[
 Z_{80}(r_*)+6\varepsilon
 \approx0.68960298125443193386<1.
\tag{4.8}
\]

Banach's theorem therefore gives a unique high-degree correction.  The
triangular recurrence identifies the resulting fixed point with the
canonical active formal series.

## 5. The transport estimate is also charge resolved

The normalized fields satisfy

\[
 (\mathcal L-1)F=\{a,F\}.
\tag{5.1}
\]

For a base monomial ((i,q)) and an arbitrary transport monomial ((j,s)),
the induced norm factor is

\[
 \frac{i+j}{i+j-1}
 \frac{|is/j-q|}{3}.
\tag{5.2}
\]

Here an arbitrary bivariate monomial has (-1\le s/j\le2), while the active
base has (-1\le q\le2i).  Hence

\[
 \frac{i+j}{i+j-1}\le\frac{i+1}{i},
 \qquad
 |is/j-q|\le\max\{i+q,2i-q\}.
\tag{5.3}
\]

Define

\[
 \tau(i,q)
 =\frac{i+1}{i}
 \frac{\max\{i+q,2i-q\}}{3}.
\tag{5.4}
\]

For the exact polynomial center,

\[
 \|T_{p_{80}}\|
 \le\sum_{i,q}\tau(i,q)A_{i,q}r_*^i
 \approx0.99940981015356436590.
\tag{5.5}
\]

The unknown correction is controlled by the general R0.37 estimate
(|T_h|\le2\|h\|\).  Therefore

\[
 \boxed{
 \|T_{p_{80}+h}\|
 \le0.99941043095132664361<1.
 }
\tag{5.6}
\]

The Neumann inverse constructs the canonical normalized fields (U,V) on
the same polydisc.  In contrast, the old scalar estimate gives

\[
 2(\|p_{80}\|+\varepsilon)
 \approx1.3348287296357404907>1.
\tag{5.7}
\]

Both charge-resolved estimates are needed at (r_*).

## 6. A nearby exact negative control

At

\[
 r_{\mathrm{probe}}=\frac{199}{1000}=0.199,
\tag{6.1}
\]

the all-order active-tail bound still passes:

\[
 Z_{80}(r_{\mathrm{probe}})
 \approx0.69200469968322433898<1.
\tag{6.2}
\]

However, the refined transport sufficient condition becomes

\[
 \|T_{p_{80}+h}\|_{\mathrm{bound}}
 \approx1.0025428645146803446>1.
\tag{6.3}
\]

This is a boundary of the present proof, not evidence that (U,V) are
nonanalytic at (0.199), and not evidence of a singularity.

## 7. Finite exact regressions

The certificate records the following implementation checks separately from
the all-order proof:

1. 2209 ordered monomial pairs through degree 10 match
   (1.5)--(1.6) exactly;
2. all 242 finite charge bounds and the analytic large-charge bound are
   stored as exact rationals and covered by a SHA-256 digest;
3. exact degree-81, 82, 160, and 241 column scans stay below (3.9);
4. the largest scanned ratios are approximately (0.33905), (0.45497),
   (0.45149), and (0.45026), respectively;
5. the recurrence residual vanishes through degree 80 and contains every
   term through degree 160;
6. all 18 formal checks pass without a floating-point sign decision.

The finite scans do not prove (3.9); equations (3.3)--(3.8) provide the
infinite-degree closure.

## 8. Value and remaining distance

Within the reduced edge model, the change from (0.118) to (0.1985) is a
substantial certified enlargement.  It also identifies the next obstruction
cleanly: at the new endpoint the active-tail margin is still about (0.3104),
whereas the transport margin is only about (5.90\times10^{-4}).

The finite R0.32 transport-candidate scale remains at least about 95.82 times
the newly certified fixed-charge radius.  More importantly, no theorem here
shows that the reduced edge system controls all three-dimensional critical
Navier--Stokes interactions.  The result should therefore be read as a
rigorous theorem about one derived generating system, not as progress of the
same magnitude on the Millennium problem itself.

## 9. Next mathematical question

R0.40 should replace the termwise transport supremum in (5.3) by an
input-slope or charge-resolved positive kernel.  The exact negative control
at (0.199) supplies a sharp acceptance test: a new theorem must reduce the
transport norm without weakening the all-order coverage.  Finite transport
columns may design the partition, but the final criterion must include every
degree and every charge.

## Reproduction

Run `research/edge_charge_resolved_audit.py` from the repository root.  The
formal certificate pins its clean source commit and the SHA-256 digest of the
R0.38 input certificate.  The computation uses exact GMP rationals, an
append-only progress log, and a process-tree resource log.  It has no random
seed, GPU dependency, or floating-point sign decision.

## References

1. R0.29, *Canonical transport reduction and the infinite charge ladder*.
2. R0.30, *An all-order analytic majorant for the canonical edge system*.
3. R0.37, *A weighted-Wiener restart beyond the R0.31 radius*.
4. R0.38, *A tail-aware Newton restart beyond the R0.37 radius*.
