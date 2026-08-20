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

where (L_{j,i}) is the exact cube supremum of the affine first derivative
and (Q_{j,ik}) is the exact absolute mixed second derivative.  All carrier
coefficients lie in (\mathbb Q), so every coefficient of every (F_j) is a
nonnegative rational number.

Exact integration over the seven-simplex gives

\[
 \sum_{m=0}^{11}\frac{T^{m+7}}{(m+7)!}
 h_m(F_1,\ldots,F_7).
\]

After expansion through spatial degree eleven, multiplication by
(\alpha!\) gives an upper bound for each
(\lVert\partial^\alpha K\rVert_\infty), (|\alpha|=11).

## 3. Rational enclosure of time

The identity

\[
 \frac{\log 2}{2}=\operatorname{atanh}(1/3)
 =\sum_{n\ge0}\frac{(1/3)^{2n+1}}{2n+1}
\]

has positive terms.  Truncating after (N) terms gives a rational lower
endpoint, while the omitted tail is bounded by

\[
 \frac{(1/3)^{2N+1}}{(2N+1)(1-1/9)}.
\]

Because every coefficient of the derivative majorant is nonnegative,
substituting this rational upper endpoint for (T) gives a rigorous upper
bound.  No directed floating-point rounding assumption is used.

## 4. Acceptance criterion

The formal run must enumerate all (4368) multiindices for all (35)
shuffles, prove every resulting coefficient positive, locate the exact
maximum, and verify the rational inequality

\[
 \max_{|\alpha|=11}\lVert\partial^\alpha K\rVert_\infty
 < 2.567\times10^{-6}.
\]

The exact rational vector is represented by a canonical SHA-256 digest, and
the exact maximum is stored as a reduced numerator and denominator.

## 5. Scope boundary

Even after this component passes, the sign argument remains open until the
moment lift, heat jet, defect, dominant root, and resolvent arithmetic receive
compatible enclosures.  This fixed invariant parallel-shear calculation does
not establish global regularity for general three-dimensional Navier--Stokes
solutions.
