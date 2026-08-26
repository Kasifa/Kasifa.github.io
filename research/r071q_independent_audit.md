# R0.71Q independent audit

**Status:** PASS  
**Scope:** finite complex-analysis geometry and analytic counterfamilies; no
Navier--Stokes time integration

## 1. Independence boundary

`research/r071q_independent_audit.py` imports neither the exact producer nor
any prior release module.  It reconstructs all numerical values directly
from the displayed formulas using NumPy.  The exact producer separately uses
rational arithmetic from Python's `Fraction`.

## 2. Finite Blaschke products

For each (N=1,2,4,8,16,32,64), the checker sampled 8,192 points on the
unit circle for

\[
 B_N(z)=\prod_{k=1}^N\frac{z-a_{N,k}}{1-a_{N,k}z},
 \qquad a_{N,k}=\frac{2N^2-k}{4N^2}.
\]

Results:

- maximum error in (|B_N(e^{i\theta})|=1):
  (1.2212453271\times10^{-14});
- maximum residual at the prescribed zeros: (0.0);
- maximum discrepancy between the direct log-anchor sum and the evaluated
  center product: (0.0);
- positive derivative counts: (lceil N/2\rceil) in every case;
- the squared family (B_N^2e) has (N) even-order positive entries in
  every case.

At (N=64), the distinct zero count is (64), while the Jensen bound for
the unsquared family is (64.3672744732).  This independently confirms the
near-sharp anchor logarithm.

## 3. Extracted Temam disk

With fixed seed `71072`, the checker sampled 200,000 uniformly distributed
points in (D(1/4,1/64)).  For the normalized lobe inequality

\[
 x^3-(x^2+y^2)^2>0,
\]

the minimum sampled residual was (0.0098575758).  The proof does not rely
on sampling: the exact certificate separately verifies the rational worst
bounds.  This numerical test is only a second implementation.

## 4. Component-union tax

For (Q=1,2,4,8,16,32,64), the checker constructed distinct
(b_q\in(1/4,1/2)) and (g_q(z)=z-b_q).  Every case passed:

- individual outer-disk bound (M_q<3/2);
- individual center anchor (a_q>1/4);
- distinct union count exactly (Q);
- positive derivative count exactly (Q).

Thus the component-union growth is not caused by a deteriorating individual
radius, norm, or anchor.

## 5. Local window-cover tax

For

\[
 C_N(z)=\left(\frac{\sin(\pi Nz)}{\pi N}\right)^2e,
\]

the checker sampled 16,384 points on every representative outer window
circle.  The maximum relative complex growth was

\[
 28.3316904452,
\]

matching the theoretical (cosh^2(3\pi/4)) bound to floating-point
precision.  The ratio is independent of (N), while the owned entry and
window counts both equal (N).

## 6. Covering-scale ledger

The independent table evaluated

\[
 T_1=(1+Y)^{-2},
 \qquad r_i=T_1/256
\]

for (Y=0,1/4,1,4,16,64,256).  At (Y=256), the inverse normalized scale
is (66049).  This is a scale audit only: it does not assert that the sampled
values form an NSE trajectory.

## 7. Conclusion

All independent checks pass.  They corroborate the finite theorem inputs
and the three abstract obstructions (anchor, component union, and covering).
They do not establish a uniform NSE zero count, an internal repeated-face
solution, a continuation criterion, or global regularity.
