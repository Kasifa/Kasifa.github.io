# R0.28 exact rational edge factorization and finite ratio separation

## Status

R0.27 reduced the negative two-generator edge to a nonlinear scalar series
\(A\) and a linear sharp series \(S\).  Its dual-precision window suggested
that the charge-one sharp coordinate approaches unit modulus, but all
coefficients still contained the radical generator (t), and the observed
parity pattern was only an MPFR statement at one parameter center.

This note removes those two weaknesses.  A change of variables factors every
coefficient into a known leaf monomial times one of three rational arrays.
The sharp array is exactly linear in the root parameters \((p,q)\).  Exact GMP
rational arithmetic then certifies the endpoint signs and consecutive-ratio
inequalities on the entire radius-\(10^{-6}\) R0.20 root box through \(N=40\).

The rationalization is an all-order identity.  The sign and ratio statements
are finite, \(N\leq40\), and are not a dominant-singularity theorem.  No
Navier--Stokes regularity or singularity conclusion is claimed.

## Radical-free normalization

Start with the R0.27 series

\[
 A(z,w)=\sum\alpha_{n,k}z^nw^k,
 \qquad
 S(z,w)=\sum s_{n,k}z^nw^k.
\]

Their first layers are

\[
 A_1=-6\sqrt2z+3\sqrt2t w,
 \qquad
 S_1=\frac p{\sqrt2}z-\sqrt2qtw.
\]

Set

\[
 Z=-6z,\qquad W=3tw,
\]

and define

\[
 A(z,w)=\sqrt2\,a(Z,W),
 \qquad
 S(z,w)=\sqrt2\,d(Z,W),
 \qquad
 d=p u+q v.
\tag{2.1}
\]

The initial data become rational:

\[
 a_1=Z+W,
 \qquad
 u_1=-\frac{Z}{12},
 \qquad
 v_1=-\frac W3.
\tag{2.2}
\]

All occurrences of \(t\) have moved into the variable \(W\).  Consequently
the coefficients of \(a,u,v\) are rational and the actual sharp coefficient
depends on \((p,q)\) only through the exact linear combination \(d=pu+qv\).

## Exact rational recurrences

For a split \((n,k)=(n_1,k_1)+(n_2,k_2)\), write

\[
 L=n+k,\qquad Q=3k-L,
 \qquad
 \Delta=n_1k_2-k_1n_2.
\]

After (2.1), the R0.27 recurrences become

\[
 (L-1)a_{n,k}
 =\begin{cases}
 \displaystyle
 \frac1Q\sum\Delta Q_2a_{n_1,k_1}a_{n_2,k_2},&Q\ne0,\\[1.2ex]
 \displaystyle
 \frac1L\sum\Delta L_2a_{n_1,k_1}a_{n_2,k_2},&Q=0,
 \end{cases}
\tag{3.1}
\]

and

\[
 (L-1)u_{n,k}=\sum\Delta a_{n_1,k_1}u_{n_2,k_2},
 \qquad
 (L-1)v_{n,k}=\sum\Delta a_{n_1,k_1}v_{n_2,k_2}.
\tag{3.2}
\]

Equivalently, the rational generating equations are

\[
 (\mathcal L-1)a
 =(I-\Pi_0)\mathcal Q^{-1}\{a,\mathcal Qa\}
 +\Pi_0\mathcal L^{-1}\{a,\mathcal La\},
\tag{3.3}
\]

\[
 (\mathcal L-1)u=\{a,u\},
 \qquad
 (\mathcal L-1)v=\{a,v\}.
\tag{3.4}
\]

The separate zero-charge term in (3.1) and (3.3) is retained exactly.  Thus
the rationalization does not discard the resonant \(Q=0\) coupling.

## Fixed-charge coefficients

Introduce the normalized charge variables

\[
 R=Z^2W,\qquad \Xi=Z^{-1}.
\]

Then

\[
 Z^nW^k=R^k\Xi^Q,
 \qquad
 R=108t\,r,
 \qquad
 \Xi=-\frac{\xi}{6}.
\]

Write the charge-one endpoints as

\[
 a_N=[R^N\Xi]a,
 \qquad
 u_N=[R^N\Xi]u,
 \qquad
 v_N=[R^N\Xi]v,
 \qquad
 d_N(p,q)=pu_N+qv_N.
\tag{4.1}
\]

Because (2N-1) pump leaves give a negative known leaf monomial, the R0.27
sharp coordinate is exactly

\[
 \sigma_{B,N}
 =-\frac{d_N}
 {\sqrt{d_N^2+a_N^2/12}+\sqrt2(3N-1)|a_N|}.
\tag{4.2}
\]

The generator \(t\), and hence the root parameter \(x\), cancels completely
from (4.2).  Only the linear root-box dependence of \(d_N(p,q)\) remains.

## Root-box interval certificate

Let \((p_*,q_*)\) be the rational center stored in the R0.20 certificate and
let

\[
 |p-p_*|\leq10^{-6},\qquad |q-q_*|\leq10^{-6}.
\]

Since \(u_N,v_N\) are rational, the inclusion

\[
 d_N(p,q)\in
 d_N(p_*,q_*)
 \mathbin{\pm}10^{-6}(|u_N|+|v_N|)
\tag{5.1}
\]

is exact.  It uses no floating-point interval operations.  Every endpoint
fraction and every interval endpoint in the certificate is a GMP rational.

The computation proves the following finite statements.

1. \(a_N>0\) for every \(1\leq N\leq40\).
2. For every point in the R0.20 root box and every \(8\leq N\leq40\),

   \[
   (-1)^{N+1}d_N(p,q)>0.
   \tag{5.2}
   \]

3. The smallest ratio of the center magnitude to the root-box uncertainty in
   (5.1), over \(N=8,\ldots,40\), is \(62214.5105\ldots\).  Thus the finite
   sign certificate is far from an interval boundary.

The center values reconstructed from the rational arrays agree with every
R0.27 \(\sigma_{B,N}\) and \(d_N/((3N-1)a_N)\) through \(N=25\) at the stored
precision.

## Consecutive-ratio separation

Define the normalized coefficient-radius proxies

\[
 \rho^A_N=\left|\frac{a_{N-1}}{a_N}\right|,
 \qquad
 \rho^D_N(p,q)=\left|\frac{d_{N-1}(p,q)}{d_N(p,q)}\right|,
\tag{6.1}
\]

and the relative block factor

\[
 \Gamma_N(p,q)
 =\frac{|d_N/d_{N-1}|}{|a_N/a_{N-1}|}
 =\frac{\rho^A_N}{\rho^D_N(p,q)}.
\tag{6.2}
\]

Independent exact interval division of the numerator and denominator boxes is
used in (6.1)--(6.2).  This loses correlation between the two occurrences of
\((p,q)\), so the resulting bounds are conservative but rigorous.

For every root-box point and every \(18\leq N\leq40\), the certificate gives

\[
 \rho^D_N(p,q)<\rho^A_N,
 \qquad
 \Gamma_N(p,q)>1.
\tag{6.3}
\]

The smallest lower bound in this complete finite window is

\[
 \Gamma_{19}>1.0294319301.
\]

On the tighter tail \(29\leq N\leq40\), all exact intervals lie in

\[
 0.9476601412\leq\rho^A_N\leq0.9515829735,
\tag{6.4}
\]

\[
 0.7490597436\leq\rho^D_N(p,q)\leq0.7786147490,
\tag{6.5}
\]

\[
 1.2221486618\leq\Gamma_N(p,q)\leq1.2697040505.
\tag{6.6}
\]

Selected certified decimal enclosures are:

| \(N\) | \(\rho^A_N\) | root-box interval for \(\rho^D_N\) | root-box interval for \(\Gamma_N\) |
|---:|---:|---:|---:|
| 18 | 0.961819600 | [0.601415743, 0.601422719] | [1.599240551, 1.599259101] |
| 19 | 0.960275087 | [0.932809901, 0.932820384] | [1.029431930, 1.029443498] |
| 25 | 0.954063379 | [0.804582260, 0.804591294] | [1.185773928, 1.185787243] |
| 30 | 0.951084191 | [0.749059744, 0.749068183] | [1.269689747, 1.269704051] |
| 35 | 0.949085365 | [0.764359333, 0.764367932] | [1.241660365, 1.241674334] |
| 40 | 0.947660141 | [0.757364740, 0.757373265] | [1.251245833, 1.251259916] |

## Exact implication and missing theorem

There is a simple all-order implication.  Suppose that for some
\(\varepsilon>0\) and all sufficiently large \(N\),

\[
 \Gamma_N(p,q)\geq1+\varepsilon.
\tag{7.1}
\]

Then iteration of (6.2) gives

\[
 \left|\frac{d_N}{a_N}\right|
 \geq C(1+\varepsilon)^N.
\]

Consequently \(|d_N|/((3N-1)|a_N|)\to\infty\), and (4.2) implies

\[
 |\sigma_{B,N}|\longrightarrow1.
\tag{7.2}
\]

If (5.2) also persists, the sign of \(\sigma_{B,N}\) is \((-1)^N\).

Equations (7.1)--(7.2) are an elementary conditional theorem.  The exact
certificate verifies its hypotheses only on \(18\leq N\leq40\).  A finite
window, however wide or well separated, does not prove an eventual uniform
gap.  In particular, the bands in (6.4)--(6.6) are coefficient-ratio proxies,
not certified convergence radii.

## Interpretation

The R0.27 trend is not caused by MPFR cancellation, the quadratic generator,
or selection of one rounded stationary point.  It survives exact
rationalization and the full certified \((p,q)\) root box.  The finite ratio
separation also identifies a precise analytic mechanism: the sharp series
behaves as if it has a closer negative \(R\)-singularity than the positive
in-plane series.

That interpretation remains conditional.  Singularity analysis transfers a
proved local expansion at a dominant singularity into coefficient
asymptotics; it does not turn a finite ratio table into a singularity theorem.
The nonlocal zero-charge projector in (3.3) and the infinite charge coupling
in (3.4) still prevent direct use of a standard transfer theorem.

## Next theorem target

R0.29 should seek an infinite-dimensional invariant cone after the parity
twist.  A successful cone must simultaneously prove, for all sufficiently
large (N),

\[
 a_N>0,
 \qquad
 (-1)^{N+1}d_N(p,q)>0,
 \qquad
 \Gamma_N(p,q)\geq1+\varepsilon
\]

uniformly on the root box.  The cone must include the \(Q=0\) slice and enough
neighboring charge sectors to close (3.1)--(3.2).  If such a cone fails, the
next acceptable result is a validated interval counterexample at a later
index.  Continuing to fit finite ratios without one of these two outcomes
would not advance the theorem.

The exact audit is implemented in
`research/edge_rational_asymptotic_audit.py`.  Its certificate preserves all
endpoint fractions, root-box intervals, ratio bounds, regression checks,
software versions, progress records, and resource monitoring.
