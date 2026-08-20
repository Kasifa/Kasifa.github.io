# R0.68B-2d — Exact all-multiindex derivative majorant

## 1. Purpose

R0.68B-2c evaluated all (4368) eleventh-order multiindices, but its
coefficients and the time (T=\log(2)/2) were binary64 numbers.  This audit
removes floating-point arithmetic from that entire derivative gate.

It does not yet enclose the dominant moment lift, the heat coefficient, or the
observable defect.  Therefore this is one strict component of a future sign
certificate, not the final sign theorem.

## 2. Exact positive polynomial

For each of the seven heat rates and each shuffle, let

\[
 F_j(z)=\sum_i L_{j,i}z_i+
 \frac12\sum_{i,k}Q_{j,ik}z_i z_k,
\]

where \(L_{j,i}\) is the exact cube supremum of the affine first derivative
and \(Q_{j,ik}\) is the exact absolute mixed second derivative.  All carrier
coefficients lie in \(\mathbb Q\), so every coefficient of every \(F_j\) is a
nonnegative rational number.

Exact integration over the seven-simplex gives

\[
 \sum_{m=0}^{11}\frac{T^{m+7}}{(m+7)!}
 h_m(F_1,\ldots,F_7).
\]

After expansion through spatial degree eleven, multiplication by
\(\alpha!\) gives an upper bound for each
\(\lVert\partial^\alpha K\rVert_\infty\), \(|\alpha|=11\).
The omitted factor \(\exp(-\sum_j s_jr_j(x))\) is at most one because every
heat rate \(r_j\) is a sum of squares.

## 3. Rational enclosure of time

The identity

\[
 \frac{\log 2}{2}=\operatorname{atanh}(1/3)
 =\sum_{n\ge0}\frac{(1/3)^{2n+1}}{2n+1}
\]

has positive terms.  Truncating after \(N\) terms gives a rational lower
endpoint, while the omitted tail is bounded by

\[
 \frac{(1/3)^{2N+1}}{(2N+1)(1-1/9)}.
\]

Because every coefficient of the derivative majorant is nonnegative,
substituting this rational upper endpoint for \(T\) gives a rigorous upper
bound.  No directed floating-point rounding assumption is used.

## 4. Acceptance criterion

The formal run must enumerate all \(4368\) multiindices for all \(35\)
shuffles, prove every resulting coefficient positive, locate the exact
maximum, and verify the rational inequality

\[
 \max_{|\alpha|=11}\lVert\partial^\alpha K\rVert_\infty
 < 2.567\times10^{-6}.
\]

The exact rational vector is represented by a canonical SHA-256 digest, and
the exact maximum is stored as a reduced numerator and denominator.

## 5. Formal result

The monitored 120-term run passed all five declared checks. Its time
enclosure has width

\[
 4.81851363704637445\times10^{-118}.
\]

All \(4368\) multiindices were present in every shuffle. Exact comparison of
their rational upper bounds gives

\[
 \boxed{
 \max_{|\alpha|=11}\lVert\partial^\alpha K\rVert_\infty
 \le 2.56632663673508065521\times10^{-6},
 \quad \alpha=(0,0,0,11,0,0).
 }
\]

This upper bound is strictly smaller than \(2.567\times10^{-6}\). The
canonical exact-vector digest is
`2b742828cfa00097b2ea1dc2203cae4da8c30164d9422a734bd12da8d6a468ee`.

The formal run took 137.84 seconds; the external monitor sampled a peak RSS
of 200.203 MiB.

## 6. Scope boundary

Even after this component passes, the sign argument remains open until the
moment lift, heat jet, defect, dominant root, and resolvent arithmetic receive
compatible enclosures.  This fixed invariant parallel-shear calculation does
not establish global regularity for general three-dimensional Navier--Stokes
solutions.
