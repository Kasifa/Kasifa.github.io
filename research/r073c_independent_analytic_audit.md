# R0.73C independent analytic audit

**Date:** 2026-08-30  
**Scope:** exact cubic neutral spectrum, periodic monodromy bridge,
source-locked endpoint signs, and the fast-time claim boundary  
**Decision:** C3 and C4 pass; C5 remains open; C6 remains conditional

## 1. Audit method

This audit does not promote Fourier-cutoff convergence to an
infinite-dimensional theorem.  It checks the analytic identities directly,
then reads the two primary interval outputs and the separately implemented
Decimal output as source-locked evidence.  The finite Fourier and sampled
Fredholm calculations are used only as falsification diagnostics.

## 2. Exact cubic neutral spectrum

For

\[
 W_0(x)=-\frac12\sin x+\frac14\sin 2x
       =-2\sin^3(x/2)\cos(x/2),
\]

direct differentiation away from the zeros gives

\[
 \frac{W_0''}{W_0}=-4+\frac{3}{2\sin^2(x/2)}.
\]

Let \(\phi_0\) be \(\sin^3(x/2)\) on \((0,2\pi)\), periodically joined as
\(|\sin(x/2)|^3\).  The join is \(C^2\cap H^2_{\rm per}\), so its second
distributional derivative has no delta mass.  Direct substitution gives

\[
 \left(-\partial_x^2+\frac{W_0''}{W_0}\right)\phi_0
 =-\frac74\phi_0.
\]

With \(t=x/2\), the Friedrichs operator is

\[
 4H_0=-\partial_t^2+6\csc^2t-16.
\]

The inverse-square coefficient \(6>3/4\) makes both endpoints limit point.
The standard \(l=2\) Pöschl--Teller eigenvalues therefore give

\[
 \sigma(H_0)=\left\{\frac{(n+3)^2-16}{4}:n\ge0\right\}
 =\left\{-\frac74,0,\frac94,5,\ldots\right\}.
\]

Thus \(-7/4\) is the unique negative singular threshold and
\(A_{\sqrt7/2}(0)\) has the exact neutral Sobolev mode.  This verifies C3.
It does not provide a regular perturbation theorem through \(c=0\).

## 3. Exact monodromy bridge

At \(\gamma=1/2\), take \(c=i\eta\), \(\eta>0\), and write

\[
 \phi''=Q_\eta\phi,
 \qquad Q_\eta=\frac14+\frac{W_0''}{W_0-i\eta}.
\]

The denominator is separated from zero, so the fundamental matrix
\(Y_\eta\) and monodromy \(M(\eta)=Y_\eta(2\pi)\) depend continuously on
\(\eta>0\).  The first-order system has zero trace, hence
\(\det M(\eta)=1\).

The reflection identities

\[
 W_0(2\pi-x)=-W_0(x),\qquad
 W_0''(2\pi-x)=-W_0''(x)
\]

give \(Q_\eta(2\pi-x)=\overline{Q_\eta(x)}\).  With
\(S=\operatorname{diag}(1,-1)\), reflection and conjugation imply

\[
 M^{-1}=S\overline M S.
\]

Because a determinant-one two-by-two matrix satisfies
\(\operatorname{tr}M^{-1}=\operatorname{tr}M\), the trace is real.  Also

\[
 \det(M-I)=2-\operatorname{tr}M.
\]

Consequently a nonzero periodic Rayleigh solution exists exactly when
\(F(\eta):=\operatorname{tr}M(\eta)-2=0\).  The phase-speed convention is

\[
 \sigma=-i\gamma c=\gamma\eta,
\]

so a positive root produces a positive real time eigenvalue.

## 4. Three source-locked endpoint enclosures

The primary producer was run with two different partitions and Taylor
orders.  Both outputs have `status=passed`, use no Fourier truncation, and
resolve the same strict signs:

| run | configuration | \(F(0.3407)\) | \(F(0.3410)\) |
|---|---|---|---|
| A | 1024 steps, order 10, 40 dps | \([-0.00385423231958435,-0.00385423231956409]\) | \([0.00611428610471889,0.00611428610473897]\) |
| B | 768 steps, order 12, 55 dps | \([-0.00385423231957440,-0.00385423231957403]\) | \([0.00611428610472875,0.00611428610472911]\) |

The independent validator imports neither the primary producer nor mpmath.
It reimplements directed interval arithmetic with Python Decimal, encloses
\(\pi\) by Machin's identity, and independently integrates the same
twelve-dimensional real system.  Its wider enclosures are

\[
\begin{aligned}
 F(0.3407)&\in[-0.00386324924767544,-0.00384521504531674],\\
 F(0.3410)&\in[0.00610533905153514,0.00612323350467374].
\end{aligned}
\]

Its fail-closed checks also require finite endpoints, zero contained in the
trace-imaginary intervals, \(1+0i\) contained in determinant sentinels,
clear critical Decimal flags, the pinned runtime, and a stable source hash.
The formal JSON reproduced byte for byte.

The exact bridge in Section 3 and the intermediate value theorem now give

\[
 \exists\eta_*\in(0.3407,0.3410),\qquad
 \sigma_*=\frac{\eta_*}{2}\in(0.17035,0.17050),\qquad
 \sigma_*\in\sigma_p(A_{1/2}(0)).
\]

This verifies C4 as an infinite-dimensional periodic-ODE statement.

## 5. Independent finite diagnostic

The separately implemented finite Fourier validator agrees with the primary
finite screen near

\[
 \sigma\approx0.170407976920434.
\]

It passes eigenvalue, embedded residual, finite-rank, projector-condition,
and sampled-winding crosschecks.  Its own claim boundary explicitly records
that an infinite-dimensional spectral result, a continuous contour
enclosure, and nonautonomous transfer are not proved.  These rows are useful
diagnostics but are not used in the proof of C4.

## 6. Why C5 does not follow

After \(\theta=|\Lambda|d\), the viscous generator contains

\[
 -|\Lambda|^{-1}L_{1/4}.
\]

This is an unbounded sectorial operator in the physical kinetic space; its
small scalar coefficient does not make it a bounded perturbation.  A valid
fast-time transfer still needs all of the following uniformly as
\(\varepsilon=|\Lambda|^{-1}\downarrow0\):

1. persistence of a viscous unstable eigenvalue;
2. a common Riesz contour and uniformly bounded projections;
3. a complementary exponential dichotomy;
4. graph-domain-compatible Kato transport along the moving profile.

None of the interval or finite computations supplies this package.  Hence
C5 is OPEN and the super-polynomial complete-row no-go C6 remains
CONDITIONAL.

## 7. Final ledger

```text
exactCubicNeutralSpectrum=CLOSED
infiniteDimensionalFrozenRayleighInstability=CLOSED
rootUniqueness=OPEN
algebraicSimplicity=OPEN
frozenInstabilityFastTimeTransfer=OPEN
superPolynomialCompleteRowNoGo=CONDITIONAL
sharpLargeLambdaGrowthLaw=OPEN
completeOSSquireA2DirectSum=OPEN
nonlinearNavierStokes=OPEN
Clay=OPEN
```

The audit therefore approves public release of C3 and C4 only with the C5,
C6, nonlinear, and Clay boundaries displayed in the same direct-decision
block.
