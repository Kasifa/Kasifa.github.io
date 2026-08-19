# R0.31: an improved common analytic domain for the canonical edge system

## Status and boundary

R0.30 proved that the reduced two-variable edge series are genuinely
analytic, but it used the deliberately coarse convolution estimate

\[
 H_L<32.
\]

This note replaces it by

\[
 H_2=8,
 \qquad
 H_L\le\frac{27}{4}\quad(L\ge3),
\tag{0.1}
\]

and improves the majorant constant from $96$ to $81/4$.  It also observes
that the quotient tails are already smaller than one throughout the full
majorant polydisc, so the canonical logarithms need no smaller auxiliary
domain.

The result is an all-order theorem for the reduced edge system.  A finite GMP
run checks the implementation independently.  Neither part locates the actual
nearest singularity or proves regularity or singularity for the full
three-dimensional Navier--Stokes equation.

## 1. The kernel to be improved

R0.30 established the layer inequalities

\[
 A_L\le\frac32\sum_{i+j=L}\min(i,j)A_iA_j,
\qquad
 F_L\le\sum_{i+j=L}\min(i,j)A_iF_j,
\tag{1.1}
\]

where $A_L$ is the coefficient ℓ¹ norm of the active field and $F_L$
is the corresponding norm for either normalized transport field.  Define

\[
 H_L=L^3\sum_{i+j=L}
 \frac{\min(i,j)}{i^3j^3}.
\tag{1.2}
\]

The old proof used $H_L<32$.  The numerical values suggested that the true
uniform behavior is much smaller, but a finite table alone would not improve
an all-order theorem.

## 2. A certified split estimate

By symmetry, with the middle term counted twice when $L$ is even,

\[
 H_L\le
 2\sum_{1\le i\le L/2}
 \frac1{i^2}\left(\frac{L}{L-i}\right)^3.
\tag{2.1}
\]

Split this sum at $i=L/10$.  In the first range,

\[
 \left(\frac{L}{L-i}\right)^3\le\left(\frac{10}{9}\right)^3.
\tag{2.2}
\]

An elementary rational certificate gives

\[
 \sum_{n=1}^{\infty}\frac1{n^2}<\frac53.
\tag{2.3}
\]

Indeed, convexity of $x^{-2}$ gives

\[
 \sum_{n=6}^{\infty}\frac1{n^2}
 \le\int_{11/2}^{\infty}\frac{dx}{x^2}=\frac2{11},
\]

and hence

\[
 \sum_{n=1}^{5}\frac1{n^2}+\frac2{11}
 =\frac{65159}{39600}
 <\frac53.
\tag{2.4}
\]

In the second range, $i>L/10$, so $i^{-2}<100/L^2$, while
$L/(L-i)\le2$.  There are at most $2L/5+1$ integers in that range.
Consequently

\[
 H_L<
 \frac{10000}{2187}
 +\frac{640}{L}
 +\frac{1600}{L^2}.
\tag{2.5}
\]

The right side is decreasing in $L>0$, and at $L=297$ it equals

\[
 \frac{1785040}{264627}<\frac{27}{4}.
\tag{2.6}
\]

Thus (0.1) holds for every $L\ge297$ by analysis.  Exact GMP rational
evaluation of (1.2) covers $3\le L\le296$; its maximum is $H_3=27/4$.
The exceptional first value is $H_2=8$.  The finite calculation and the
analytic tail have disjoint, explicit responsibilities.

## 3. Improved all-order coefficient bounds

Set

\[
 K=\frac{81}{4}.
\tag{3.1}
\]

The degree-two active layer is checked directly:

\[
 A_2=3<\frac{2K}{2^3}=\frac{81}{16}.
\tag{3.2}
\]

For $L\ge3$, assume the bound below degree $L$.  Equations (1.1) and
(0.1) give

\[
 A_L
 \le\frac{6K^{L-2}}{L^3}H_L
 \le\frac{81K^{L-2}}{2L^3}
 =\frac{2K^{L-1}}{L^3}.
\tag{3.3}
\]

The transport estimate has more slack because $2H_L\le16<K$, including
the exceptional degree-two kernel.  Therefore, for every $L\ge1$,

\[
 \boxed{
 A_L\le\frac{2(81/4)^{L-1}}{L^3},
 \qquad
 \|U_L\|_1,\|V_L\|_1
 \le\frac{(81/4)^{L-1}}{L^3}.
 }
\tag{3.4}
\]

It follows that all three series converge absolutely on

\[
 \boxed{\max(|Z|,|W|)<\frac4{81}.}
\tag{3.5}
\]

This is a strict factor $128/27\approx4.7407$ improvement over the R0.30
radius $1/96$.

## 4. The logarithms occupy the same polydisc

The ideal invariance from R0.30 gives $U=Z\widetilde U$ and
$V=W\widetilde V$, with both quotient series equal to one at the origin.
Let $x=Kr<1$.  From (3.4),

\[
 |\widetilde U-1|,|\widetilde V-1|
 \le\sum_{L\ge2}\frac{x^{L-1}}{L^3}
 <\sum_{L\ge2}\frac1{L(L-1)}=1.
\tag{4.1}
\]

Both quotients are therefore nonzero throughout the full open polydisc
(3.5).  Their analytic logarithms exist there, and so do

\[
 \phi=\frac12[\log(U/Z)+\log(V/W)]
\]

and the R0.29 exponential factorization.  R0.30 used the smaller radius
$1/192$ for this step; the separate shrinkage was unnecessary.

## 5. What this changes and what it does not

The new domain is a rigorously improved lower bound, not an estimate of the
actual convergence radius.  It closes the first acceptable R0.31 outcome:
the improvement is all-order and the finite kernel calculation is only the
bounded part of a proof with an analytic tail.

The nearest singular variety remains unidentified.  A separate continuation
stage must now construct a candidate and attach a validated error enclosure;
finite coefficient ratios, Padé poles, or root plots without such an enclosure
remain diagnostics rather than singularity theorems.
