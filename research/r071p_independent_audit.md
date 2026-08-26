# R0.71P independent audit

**Date:** 2026-08-26  
**Implementation:** standalone NumPy arrays, sampled-sign/Brent root
detection, SciPy quadrature, and a \(32^3\) NumPy FFT.  The checker imports
neither the exact producer nor prior release code.

## 1. Random finite overlap ledgers

The checker generated 64 deterministic trials with seed `71071`.  Each trial
used a 48-dimensional real field, eight width-9 cells with stride 5, support
overlap two, and independently sampled supported directions.

For every cell it verified

\[
 \frac{(\langle F,c_Q\rangle^+)^2}{Y\|c_Q\|^2}
 \le\frac{\|1_{S_Q}F\|^2}{Y},
\]

and for every trial it verified

\[
 \sum_QA_{Q,+}
 \le\sum_Q\frac{\|1_{S_Q}F\|^2}{Y}
 \le2\frac{\|F\|^2}{Y}.
\]

The largest observed cellwise ratio was
`0.6780322243731772`; the largest entry-sum/overlap-budget ratio was
`0.14346621968093287`.  These seeded tests detect indexing, support, and
normalization errors; the general theorem is proved by Cauchy--Schwarz and
bounded overlap, not by random sampling.

## 2. Sequential-entry detection

For

\[
 C_N(t)=N^{-1}\sin(Nt)e,\qquad F=e,\qquad Y=1,
\]

on the half-open window \([0,2\pi)\), the independent checker sampled signs,
used Brent roots where needed, included the zero observation boundary at
\(t=0\), and excluded \(2\pi\).  For
\(N=1,2,4,8,16,32,64\), it detected exactly \(N\) positive entries; the
maximum count error was `0.0`.

With \(\varepsilon_N=N^{-4}\), independent quadrature of every rising soft
layer reproduced

\[
 V^+(a_{N,\varepsilon_N})=\frac{N}{1+N^{-2}}
\]

with maximum relative error `1.1796119636642288e-16`.  At \(N=64\), the hard
entry mass is `64`, the soft mass is `63.98437881376617`, and the denominator
mass is `0.0007669903939428206`; the \(C_t\) and \(F\) square masses remain
\(\pi\) and \(2\pi\).

## 3. Standalone NSE initial-jet FFT

The checker sampled

\[
 u_0=(0,\cos x_1,\cos x_2)
\]

on a \(32^3\) periodic grid, rebuilt vorticity, the Leray-projected Lamb field,
the radius-\(\sqrt2\) filter, and the leading denominator direction without
importing the symbolic implementation.  It also checked that the initially
filtered vorticity and its filtered viscous jet both vanish.  It obtained

\[
 Y_0=1,\qquad\|F\|_2^2=\frac14,\qquad
 \|c\|_2^2=1,\qquad\langle F,c\rangle=\frac12,
\]

and hence

\[
 A_+=\frac14=\frac{\|F\|_2^2}{Y_0}.
\]

All recorded binary64 residuals, including the Cauchy residual and sharpness
ratio, were `0.0` on this run.

## 4. Boundary

The audit corroborates finite overlap bookkeeping, the abstract temporal
packing separation, and one sharp NSE initial face.  It is not interval
arithmetic, a PDE time integration, an internal NSE face-count theorem, an
infinite-frame estimate, or a regularity result.
