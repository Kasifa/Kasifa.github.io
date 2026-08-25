# R0.71B independent mathematical audit

**Date:** 2026-08-25

**Scope:** independent checking of the two-shell common/chord formula, both
arbitrary-(N) fan constructions, the (N=8) Fourier reconstructions, the
positive-output Cauchy--Young inequality, the R0.71A sign test, and the exact
claim boundary.

The independent checker does not import the R0.71B producer.  No calculation
below treats a static Fourier field as a Navier--Stokes solution trajectory.

## 1. Audit verdict

The following claims pass.

1. The HHL polarizations are unit and divergence-free, the high radii are
   equal, and both are strictly separated from the low radius.
2. The common symbol tends to one, while the chord symbol is
   (-1/(2M^2)+o(M^{-2})).
3. The same-low fan has only the (12N) intended ordered resonances, fixed
   (L^2) mass (3/2), total common work tending to (1/4), and shell
   (ell^2) work tending to zero.
4. The shared-high frequencies are integral, all high radii are exactly
   equal, low response classes are strictly separated, and only the intended
   resonances remain.
5. The shared-high polarized work is exactly

   \[
    -\frac1{8\sqrt N}
    \sum_{j=1}^N\frac{M_j}{\sqrt{1+M_j^2}}.
   \]

6. Each high factor has (L^2) norm (1/\sqrt2), while every frame block
   of the low coefficient is bounded by one.
7. The positive-output coefficient satisfies the exact Cauchy--Young
   consumer.
8. Independent reconstruction gives (9/800) and (3/39940400) for the
   R0.71A positive field, and zero for the negative field.
9. A nonzero plane wave has zero positive-output coefficient, so that
   coefficient is not a BMO-equivalent norm.

No blocker or major mathematical inconsistency was found.  Two wording
restrictions are essential:

- the shared-high theorem concerns a **polarized three-field** estimate, not
  the established one-field Besov continuation theorem;
- the finite (N=8) enumerations are regression certificates, not proofs of
  the arbitrary-(N) resonance classifications.

## 2. Two-shell formula

Let

\[
 n=(1,1,0),quad
 p=(M,-M-1,0),quad
 q=(-M-1,M,0),
 \tag{2.1}
\]

and use the polarizations in the report.  Direct evaluation of the
symmetrized vorticity-to-strain multiplier gives

\[
 A_n=\frac{2M+1}{\sqrt2R},
 \tag{2.2}
\]

\[
 A_p=\frac{2M+1}{\sqrt2R}
 \left(1-\frac2{R^2}\right),
 \qquad
 A_q=-\frac{2M+1}{\sqrt2R},
 \tag{2.3}
\]

where (R^2=2M^2+2M+1).  The weighted identity is

\[
 2A_n+R^2A_p+R^2A_q=0.
 \tag{2.4}
\]

With high correlation one and low--high correlations zero,

\[
 \mathcal P=A_n,
 \qquad
 \mathcal F=A_n+A_p+A_q=A_p.
 \tag{2.5}
\]

Their half-sum and half-difference reproduce the report.  Differentiation
gives

\[
 \mathcal U'(M)
 =\frac{\sqrt2(5M^2+5M+1)}
 {(2M^2+2M+1)^{5/2}}>0.
 \tag{2.6}
\]

The limits are therefore genuine analytic statements, not numerical fits.

## 3. Same-low fan

### 3.1 Resonances

For every positive high mode (p_M) or (q_M), the sum of its first two
coordinates is (-1).  The low mode has coordinate sum (2).  Thus a
positive zero-sum triple must have one low and two high modes.  Directly,

\[
 p_M+q_L=-n
 \iff M=L.
 \tag{3.1}
\]

The other two-high combinations cannot equal (-n).  Negating all modes
gives the only other orientation.  Six permutations of each orientation
give (12N) ordered triples.

The independent checker reconstructs all 34 signed modes for (N=8) and
finds exactly 96 ordered triples.

### 3.2 Norm and work ledger

The low cosine contributes (1/2) to (L^2).  Each of the (2N) high
cosines has amplitude (N^{-1/2}) and contributes (1/(2N)).  Hence

\[
 \|\omega_N\|_2^2=\frac32.
 \tag{3.2}
\]

Since no cross-family resonance exists, the common work is the sum of the
individual real-cosine values (mathcal U_{M_j}/(4N)).  The independent
full-product and frame-covariance convolutions give

\[
 \frac{\mathfrak I_N+\mathfrak P_{Q,N}}2
 =0.2497261589308691\ldots
 \tag{3.3}
\]

at (N=8), matching the producer exactly.

## 4. Shared-high rational-circle fan

### 4.1 Integer and equal-radius arithmetic

Because (Q_N) is divisible by every (d_j=1+M_j^2), all coordinates in

\[
 p_j=\frac{Q_N}{d_j}(1-M_j^2,2M_j,0)
 \tag{4.1}
\]

and

\[
 n_j=-\frac{2Q_N}{d_j}(1,M_j,0)
 \tag{4.2}
\]

are integers.  The Pythagorean identity

\[
 (1-M^2)^2+(2M)^2=(1+M^2)^2
 \tag{4.3}
\]

proves (|p_j|=Q_N=|q|) exactly.  This is stronger than membership in the
same dyadic annulus and is exactly what makes every response correlation
equal to one.

### 4.2 Resonance audit

The largest low radius is less than (Q_N/8), and successive low radii
drop by more than a factor four.  The (q)-coefficient representation of
the high modes reduces every possible two-high resonance to a relation
among at most three low shifts.  Lacunarity excludes such relations unless
the intended indices coincide.

The independent checker again finds 34 signed modes and exactly 96 ordered
zero-sum triples for (N=8).

### 4.3 Direct Fourier work

The checker rebuilds

\[
 \widehat S_A(k)
 =\frac i2
 \left(k\otimes\widehat u_A(k)
 +\widehat u_A(k)\otimes k\right)
 \tag{4.4}
\]

and the polarized covariance convolution without calling the producer.  It
obtains

\[
 \mathfrak P_{\rm cr}
 =-0.3534669874150541\ldots
 \tag{4.5}
\]

at (N=8), with exact symbolic residual zero against the formula in the
report.

This result rejects

\[
 |\mathfrak P_{\rm cr}(A;B,C)|
 \lesssim
 \sup_\alpha\|T_\alpha A\|_\infty
 \|B\|_2\|C\|_2.
 \tag{4.6}
\]

It does not reject a one-field estimate in which the complete
Littlewood--Paley block norm and the full (L^2) mass are evaluated on the
same (omega).

## 5. Positive-output square

For a real field,

\[
 \mathfrak P_Q
 =\sum_{k\in K_+}w_k.
 \tag{5.1}
\]

The first inequality

\[
 (\mathfrak P_Q)_+
 \le\sum_{k\in K_+}w_k^+
 \tag{5.2}
\]

is one-sided and loses cancellation only after the sign is measured at each
output.  Cauchy--Schwarz uses the exact weights

\[
 2|k||\widehat S(k)|_F.
 \tag{5.3}
\]

For divergence-free (widehat\omega(k)), a coordinate rotation taking
(k/|k|) to (e_1) gives

\[
 \widehat S(k)
 =-\frac12
 \left[e_1\otimes(e_1\times\widehat\omega)
 +(e_1\times\widehat\omega)\otimes e_1\right],
 \tag{5.4}
\]

so

\[
 |\widehat S(k)|_F^2
 =\frac12|\widehat\omega(k)|^2.
 \tag{5.5}
\]

Summing one representative from each pair proves the gradient identity and
the Cauchy bound.  Completing the square proves the Young bound.

### 5.1 Independent R0.71A reconstruction

The checker independently rebuilds the six base cosine coefficients and the
four filler coefficients, including the imaginary Fourier phases of the
sine filler.  It finds:

| Field | covariance work | nonzero output count | \(\mathcal T_+^2\) | \(a_+\) |
|---|---:|---:|---:|---:|
| positive | \(3\sqrt2/40\) | 1 | \(9/800\) | \(3/39940400\) |
| negative | \(-3\sqrt2/40\) | 1 | \(0\) | \(0\) |

The result confirms that the coefficient sees strain phase even when the
pointwise covariance is identical.

## 6. Claim-boundary audit

The evidence proves static no-go results and one exact deterministic
consumer.  It does not prove:

- an (L_t^1) estimate for (a_+);
- a local tent or Carleson theorem for (a_+);
- that all signed common-response quantities reduce to BMO;
- failure of the established BMO, dyadic-BMO, or
  (dot B^0_{\infty,\infty}) continuation criteria;
- a Navier--Stokes singular solution or unconditional regularity.

The next-stage wording should therefore be “localize and propagate the
positive-output coefficient”, not “the common-response problem is solved”.
