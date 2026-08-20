# R0.68B-2h — A strict corrected dominant heat sign

## Result

For the fixed reachable dominant component of the 1,792-state eighth-order
parallel-shear construction, the degree-ten heat jet remains strictly
negative after the complete spatial Taylor defect and resolvent correction
are added.  The source-unlocked guarded run gives

\[
 B_{10}\in
 [-1.49238243184751323\times10^{-8},
  -1.49238243184751290\times10^{-8}]
\]

and a correction magnitude at most

\[
 1.20506130214380835\times10^{-8}.
\]

Consequently the corrected interval is

\[
 \boxed{
 [-2.69744373399132142\times10^{-8},
  -2.87321129703704757\times10^{-9}]<0.}
\]

This closes the finite dominant-heat gate for this one fixed eighth-order
coefficient.  It does not control all Picard orders.

## Exact signature compression

The full free-shift grid contains \(16^6=16{,}777{,}216\) points.  Carry
admissibility and Fourier signs compress it exactly to 44,514 classes.  Each
class stores a distance shell, an exact multiplicity, and a fourteen-entry
signature with at most seven nonzero entries, all in \(\{0,\pm1\}\).

The certified centred moments are paired with every class using guarded
binary128 arithmetic.  The resulting observable defect is bounded by

\[
 b_{\mathrm{obs}}^{(10)}
 \le 30.2344865053562053.
\]

## Absolute-path tail and resolvent

The no-cancellation tail must use the product of the four entrywise-absolute
digit transfer matrices.  It is **not** the entrywise absolute value of their
already-composed signed cycle; the latter would incorrectly retain path
cancellation.  The exact absolute-path cycle has 695,808 nonzeros, maximum
entry 134,512, and maximum row sum 54,210,304.

With the exact positive carry weight, the deliberately coarse bounds are

\[
 b_{\mathrm{obs,coarse}}\le4827.881115068729,
 \qquad
 \|b\|_w\le1.282496074405874\times10^{-6}.
\]

The block contraction is exactly \(16^{-5}\).  Combining the leading
observable term with the geometric weighted tail gives

\[
 Z_{\mathrm{obs}}le0.004695666112388973.
\]

The previously certified all-multiindex derivative majorant is

\[
 \max_{|\alpha|=11}\|\partial^\alpha K\|_\infty
 <2.5663266367350814\times10^{-6}.
\]

Their product is the correction bound displayed above.

## Boundary and value

This is a rigorous sign theorem for one explicitly constructed eighth-order
coefficient inside a globally smooth parallel-shear invariant class.  Its
research value is methodological and local: it joins exact combinatorics,
exact algebraic spectral data, outward-rounded high-precision moments, an
infinite heat-series tail, and a resolvent defect into one auditable sign
certificate.

It does not establish a sign at every Picard order, does not construct a
finite-time singularity, does not control arbitrary three-dimensional
perturbations, and does not solve the Navier--Stokes Millennium problem.
