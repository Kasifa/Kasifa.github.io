# R0.74H collar-flux finite compatibility certificate report

## Result

The exact-arithmetic certificate returns **PASS: 25/25**.

This is a finite compatibility check.  It verifies the rational powers of
\(R\), \(B\), \(L\), and the outer \(2/3\) and inner \(3/2\) exponents
used in R0.74H.  It also records the elementary monotonicity reductions
behind the repaired payment and the small-payment corollary.

It does not prove the weighted energy identity or any analytic estimate.

## Quadratic-cutoff normalization

The parabolic time interval contributes \(R^2\), a three-dimensional
shell contributes \(R^3\), and hence the weighted support measure has
power

\[
 2+3=5.
\]

Weighted Hölder contributes its one-third power \(R^{5/3}\).  The outer
energy normalization and a time or Laplacian cutoff supply \(R^{-3}\), so

\[
 -3+\frac53=-\frac43.
\]

This agrees exactly with

\[
 \left(R^{-2}S_3\right)^{2/3}:
 \qquad -2\cdot\frac23=-\frac43.
\]

Thus the finite powers in R0.74H (4.3)--(4.4) are dimensionally
compatible.

## Inner and outer payment powers

Each quantity inserted into the payment with exponent \(3/2\) becomes
linear after the outer \(2/3\) power:

\[
 \frac32\cdot\frac23=1.
\]

This applies separately to the buffered local energy, the Version-F
acceleration moment, and the cubicized positive collar flux.

For nonnegative \(P\) and \(C\), put

\[
 S=P+C^{3/2}.
\]

Since \(P\le S\) and \(C^{3/2}\le S\), monotonicity gives

\[
 P^{2/3}\le S^{2/3},
 \qquad
 C\le S^{2/3}.
\]

Adding proves the deliberately non-sharp but sufficient algebraic row

\[
 P^{2/3}+C\le2(P+C^{3/2})^{2/3}.
\]

For \(0\le P\le1\), the exponent ordering \(2/3<1\) gives
\(P\le P^{2/3}\), which is exactly the extra algebra in Corollary 6.3.

## R0.74G diagnostic scale

Under

\[
 \mathfrak a=B\gamma^{-1/2},
\]

the shell factor in \(\mathfrak a^2\gamma\) cancels exactly.  The target
lower scale is therefore

\[
 X_*\sim B^2LR^2.
\]

The frozen old-payment upper ledger gives only

\[
 (B^3R^3)^{2/3}=B^2R^2,
\]

so the ratio retains one uncancelled power of \(L\).  By contrast,

\[
 (B^2LR^2)^{3/2}=B^3L^{3/2}R^3.
\]

Thus the cubicized collar flux has precisely the denominator scale required
to become linear after the outer \(2/3\) power.  This is exponent
compatibility, not a proof of the analytic lower bound.

The certificate also checks that with \(B\asymp R^{-2}\), the reference
upper scale \(B^3R^3\) is \(R^{-3}\).  This exponent computation is not a
lower bound for the actual payment.  The fact that the R0.74G family lies
in the large-payment regime is instead derived analytically in R0.74H
(7.5a), using Theorem 6.2 and the target lower bound.

## Shell-tail finite marker

At shell index \(j=4\), the exponent decrement in the ratio of the
polynomial shell-volume majorants is

\[
 \frac{3\cdot4^3}{32}=6.
\]

This is recorded only as a finite marker for the super-Gaussian tail.
Convergence of the infinite shell sum and the lattice-point bound remain
analytic inputs.

## Scope boundary

The certificate does **not** prove:

1. the finite-shell energy identities, their signs, or the terminal limit;
2. \(C^2\) convergence, unfolding, or absolute convergence of the shell
   sum;
3. Hölder, Calderón--Zygmund, harmonic-pressure, or residual-transport
   estimates;
4. the Version-F acceleration moment bound;
5. the R0.74F--G packet lobe or positive collar-flux lower bound;
6. a lower bound for the actual payment;
7. the R0.74H two-regime theorem, epsilon regularity, or continuation; or
8. any singularity, global-regularity, or Clay claim.

**NOT CLAY.**

## Reproduction

From the repository root, run

    python3 scripts/r074h_collar_flux_certificate.py

The standard output must be byte-for-byte identical to
`research/r074h_collar_flux_certificate.json`.
