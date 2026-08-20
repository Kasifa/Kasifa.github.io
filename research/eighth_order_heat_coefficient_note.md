# R0.68B-2g — A guarded negative degree-ten heat jet

## Result

For the fixed reachable dominant component of the 1,792-state eighth-order
construction, the complete centred Taylor jet through spatial degree ten has
a strictly negative heat pairing.  The source-unlocked audit run gives centre

\[
 -1.49238243184751323\times10^{-8}
\]

with an internal binary128 interval radius at most

\[
 1.07451892110713391\times10^{-25}.
\]

This is a strict sign for the finite degree-ten jet only.  The
signature-compressed spatial Taylor defect and its resolvent correction are
still separate gates.

## Exact heat-rate input

The 35 order-preserving shuffles contribute seven quadratic heat rates each.
All 245 rates are generated in exact GMP rational arithmetic.  Together they
contain 6,055 nonzero monomial terms.  Their centred coefficient \(L^1\) norms
obey the exact common bound

\[
 Q=\frac{605}{16}.
\]

The only transcendental parameter is

\[
 T=\frac{\log 2}{2}=\operatorname{atanh}(1/3).
\]

A positive rational series with 120 terms encloses \(T\).  Every weight
\(T^{n+7}/(n+7)!\), \(0\le n\le64\), is converted from exact rational
endpoints to a binary64 double-double centre and outward radius before the
guarded binary128 recurrence begins.

## Infinite time-series tail

For seven rate polynomials, the coefficient \(L^1\) norm of the complete
homogeneous polynomial satisfies

\[
 \|h_n\|_1\le {n+6\choose6}Q^n.
\]

After summing all 35 shuffles, the first omitted term at \(n=65\) is bounded
by \(2.11177082063804\times10^{-25}\).  Its successive majorant ratio is at
most \(0.195837816425328\) and decreases thereafter.  Thus every omitted
spatial coefficient is covered by the uniform exact-rational bound

\[
 2.626050893428943\times10^{-25}.
\]

This tail is added to every coefficient radius.  The finite recurrence uses
unit roundoff \(2^{-113}\), widened dot-product bounds, and a factor
\(1+2^{-100}\) after positive radius calculations.  Final interval endpoints
are rounded outward explicitly.

## Cross-checks and boundary

An independent binary128 scanner recomputes the pairing from the stored heat
coefficient and centred-moment arrays.  The coefficient centres also agree
with the old binary64 architecture pilot to within
\(4.051\times10^{-22}\).  Neither check substitutes for the interval proof;
they detect ordering and implementation mistakes.

This result does not yet prove the final dominant heat sign, does not control
all Picard orders, and does not solve the Navier--Stokes Millennium problem.
