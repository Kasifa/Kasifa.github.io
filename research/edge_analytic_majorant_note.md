# R0.30: an all-order analytic majorant for the canonical edge system

## Status and boundary

R0.29 showed that the normalized transport coordinates

\[
U=-12u,\qquad V=-3v
\]

obey the formal identities

\[
\{U,V\}=UV,
\qquad
\frac UV=\frac ZW e^{-a}.
\]

It also showed that no fixed finite upper charge cutoff closes.  The bare leaf
term in the charge recurrence is \(k f_{k,q+1}\).  That observation is correct
as a closure obstruction, but it is not a growth obstruction: after the
recurrence is solved, its normalized coefficient is

\[
\frac{k}{3k-q-1}\le 1.
\]

The correct next object is therefore an infinite weighted estimate.  This note
proves one in the simpler and stronger total-degree form.  The result gives an
explicit common domain of absolute analyticity for \(a,U,V\), and an explicit
smaller domain on which the logarithms in the R0.29 factorization are analytic.

The theorem concerns the reduced two-variable edge system derived in R0.28.
It is not a theorem for the full three-dimensional Navier--Stokes equation, it
does not locate a dominant singularity, and it does not prove endpoint
coefficient asymptotics.

## 1. Layer norms

Write a homogeneous series as

\[
f=\sum_{L\ge1}\sum_{k=0}^L f_{L,k}Z^{L-k}W^k
\]

and define

\[
A_L=\sum_{k=0}^L|a_{L,k}|,
\qquad
F_L=\sum_{k=0}^L|f_{L,k}|.
\tag{1.1}
\]

For an index \((L,k)\), set its charge to

\[
Q=3k-L.
\tag{1.2}
\]

The exact active recurrence has two forms.  If the output charge is nonzero,

\[
a_{L,k}=\frac1{Q(L-1)}
\sum_{\substack{i+j=L\\r+s=k}}
(is-rj)(3s-j)a_{i,r}a_{j,s}.
\tag{1.3}
\]

For zero output charge,

\[
a_{L,k}=\frac1{L(L-1)}
\sum_{\substack{i+j=L\\r+s=k}}
(is-rj)j\,a_{i,r}a_{j,s}.
\tag{1.4}
\]

The transport recurrence is

\[
f_{L,k}=\frac1{L-1}
\sum_{\substack{i+j=L\\r+s=k}}
(is-rj)a_{i,r}f_{j,s}.
\tag{1.5}
\]

## 2. Symmetrization removes the apparent charge loss

Let

\[
Q_1=3r-i,
\qquad
Q_2=3s-j,
\qquad
Q=Q_1+Q_2.
\]

The support theorem from R0.29 gives \(Q_1,Q_2\ge-1\) whenever the two active
coefficients are nonzero.  If \(Q\ne0\), pairing each ordered term with its
swap gives

\[
\sum (is-rj)Q_2a_{i,r}a_{j,s}
=\frac12\sum(is-rj)(Q_2-Q_1)a_{i,r}a_{j,s}.
\tag{2.1}
\]

For integers \(Q_1,Q_2\ge-1\) with \(Q_1+Q_2\ne0\),

\[
|Q_2-Q_1|\le3|Q_1+Q_2|.
\tag{2.2}
\]

If both charges are nonnegative the constant is one.  If one is \(-1\), the
largest allowed ratio occurs for the other charge equal to two, where it is
exactly three.  This exhausts the cases.

For zero output charge, the same swap in (1.4) gives

\[
\sum(is-rj)j\,a_{i,r}a_{j,s}
=\frac12\sum(is-rj)(j-i)a_{i,r}a_{j,s}.
\tag{2.3}
\]

Using

\[
|is-rj|\le ij,
\qquad |j-i|\le L,
\qquad \frac{ij}{L-1}\le\min(i,j),
\]

both charge cases are covered by the single all-order inequality

\[
\boxed{
A_L\le\frac32\sum_{i+j=L}\min(i,j)A_iA_j.
}
\tag{2.4}
\]

Equation (1.5) gives, without charge division,

\[
\boxed{
F_L\le\sum_{i+j=L}\min(i,j)A_iF_j.
}
\tag{2.5}
\]

These are estimates for the entire charge ladder at once.  A finite charge
cutoff is unnecessary.

## 3. The convolution lemma

Define

\[
H_L=L^3\sum_{i+j=L}
\frac{\min(i,j)}{i^3j^3}.
\tag{3.1}
\]

By symmetry, and because \(L/(L-i)\le2\) for \(1\le i\le L/2\),

\[
H_L
\le 2\sum_{1\le i\le L/2}
\frac1{i^2}\left(\frac L{L-i}\right)^3
\le16\sum_{i\ge1}\frac1{i^2}
<32.
\tag{3.2}
\]

The last strict inequality is elementary:
\(1/i^2<1/[i(i-1)]\) for \(i\ge2\), and the latter series telescopes.

## 4. Explicit all-order majorants

Set

\[
K=96.
\tag{4.1}
\]

Since \(A_1=2\), induction in (2.4) and (3.2) gives

\[
\boxed{
A_L\le\frac{2K^{L-1}}{L^3}
\quad(L\ge1).
}
\tag{4.2}
\]

Indeed, if the bound holds below \(L\), the right side of (2.4) is at most

\[
\frac{6K^{L-2}}{L^3}H_L
<\frac{192K^{L-2}}{L^3}
=\frac{2K^{L-1}}{L^3}.
\]

The normalized fields have \(\|U_1\|_1=\|V_1\|_1=1\).  Applying (2.5) with
(4.2) gives

\[
\boxed{
\|U_L\|_1,\ \|V_L\|_1
\le\frac{K^{L-1}}{L^3}.
}
\tag{4.3}

Here \(K=96\) is deliberately conservative.  No optimization of the radius is
claimed.

## 5. From formal series to analytic identities

If \(\max(|Z|,|W|)\le r\), every homogeneous monomial of degree \(L\) has
absolute value at most \(r^L\).  Equations (4.2)--(4.3) therefore prove
absolute convergence of \(a,U,V\) on

\[
\boxed{\max(|Z|,|W|)<\frac1{96}.}
\tag{5.1}
\]

The transport equations preserve the principal ideals \((Z)\) and \((W)\).
Thus \(U=Z\widetilde U\) and \(V=W\widetilde V\), with both quotient series
equal to one at the origin.  Put \(x=Kr\).  For \(x\le1/2\),

\[
|\widetilde U-1|,\ |\widetilde V-1|
\le\sum_{L\ge2}\frac{x^{L-1}}{L^3}
\le\frac{x}{8(1-x)}
\le\frac18.
\tag{5.2}
\]

Consequently the two quotient series do not vanish on the closed polydisc of
radius \(1/192\), and their analytic logarithms are defined there.  Hence

\[
\phi=\frac12\left[\log(U/Z)+\log(V/W)\right]
\tag{5.3}
\]

is analytic on

\[
\boxed{\max(|Z|,|W|)<\frac1{192}.}
\tag{5.4}
\]

The all-order formal identities from R0.29 are identities of convergent power
series in this domain.  In particular,

\[
U=Ze^{\phi-a/2},
\qquad
V=We^{\phi+a/2},
\]

and the sharp-field exponential factorization hold as analytic identities,
not only as formal ones.

## 6. What remains open

The estimate proves existence of a nonzero common analytic polydisc.  It does
not identify the actual radius, the nearest singular variety, or the
singularity controlling the endpoint coefficient sequence.  The next useful
step is therefore not a larger finite charge cutoff.  It is one of:

1. improve the scalar majorant using the exact kernel rather than the uniform
   constant 32;
2. analytically continue the canonical map beyond the conservative polydisc
   and identify candidate singular varieties;
3. prove that one candidate singularity controls the endpoint extraction and
   determine whether the exponential factors preserve or change its sign.

The exact degree-119 computation archived with R0.30 only checks the recurrence
implementation, the layer bounds, and finite growth diagnostics.  It is not
used in the all-order proof above.
