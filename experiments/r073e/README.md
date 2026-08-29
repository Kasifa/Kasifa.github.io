# R0.73E exploratory finite complement diagnostic

This directory tests the complement left after removing only the selected
R0.73D viscous cluster.  The computation uses the exact kinetic-space
isometry

\[
 U_\mu=\mu^{-1/2}L_\mu^{-1/2}:X_\mu\to L^2,
 \qquad \mu=1/4,
\]

and dense Fourier compressions on modes \(-N,\ldots,N\).  Hence the reported
Euclidean 2-norms are the physical kinetic norms for each finite compression.

## Stage finding

The moving complement

\[
 Q_\varepsilon=I-P_\varepsilon
\]

is not stable in these finite matrices.  At the largest cutoff \(N=96\), it
contains a conjugate pair with positive real part for every sampled viscosity:

| \(\varepsilon\) | cluster real part | \(Q_\varepsilon\) spectral abscissa | pair imaginary part |
|---:|---:|---:|---:|
| \(10^{-2}\) | 0.1563164070 | 0.0079765069 | \(\pm0.1681643423\) |
| \(10^{-3}\) | 0.1689437514 | 0.0373262063 | \(\pm0.1752195941\) |
| \(10^{-4}\) | 0.1702610052 | 0.0402177675 | \(\pm0.1760459306\) |
| \(10^{-5}\) | 0.1703932743 | 0.0405072256 | \(\pm0.1761284978\) |
| \(10^{-6}\) | 0.1704065066 | 0.0405361741 | \(\pm0.1761367541\) |

The largest \(N=48\) versus \(N=96\) discrepancy in this spectral abscissa
is \(1.24\times10^{-7}\) on the frozen grid.  This is strong finite evidence
for an additional unstable pair, but it is not a proof that the continuum
operator has that pair.

The immediate analytic consequence is negative but useful: an exponential
decay theorem on this rank-one complement is incompatible with the computed
finite spectra.  The next proof should instead do one of the following:

1. enlarge the unstable Riesz projection after separately certifying every
   right-half-plane inviscid cluster; or
2. retain the rank-one projection and prove a growth-gap estimate
   \(\|e^{tB_\varepsilon}Q_\varepsilon\|\le C e^{\beta t}\) with
   \(0.0406<\beta<\operatorname{Re}\lambda_\varepsilon\).

The second route is numerically compatible with a vertical line such as
\(\operatorname{Re}z=0.08\), but no uniform continuum resolvent bound or
no-pollution theorem has been proved here.

## Resolvent and semigroup sentinels

For \(N=96\), \(\varepsilon=10^{-6}\), the maximum sampled/refined intrinsic
\(Q_\varepsilon\)-resolvent norms are

| vertical line | maximum norm | peak \(|\operatorname{Im}z|\) |
|---:|---:|---:|
| 0.05 | 378.4782 | 0.1758830 |
| 0.08 | 56.2998 | 0.1730535 |
| 0.12 | 21.2573 | 0.1677321 |

The intrinsic complement semigroup at the same row has

\[
 \|e^{200B_{\varepsilon,Q}}\|_2=1.68367\times10^4,
\]

and its largest refined value of
\(e^{-t\alpha_Q}\|e^{tB_{\varepsilon,Q}}\|_2\) on \(0\le t\le200\) is
5.07968.  The least-squares slope of \(\log\|e^{tB_{\varepsilon,Q}}\|_2\)
on \(120\le t\le200\) is 0.0405522, close to the finite spectral abscissa
0.0405362.  These are sampled binary64 observations, not continuous-time
bounds.

The fixed inviscid complement is also unsuitable for long-time evolution
without transport.  At \(N=96\), \(\varepsilon=10^{-6}\),

\[
 \|P_\varepsilon-P_0\|_2=3.09050\times10^{-4},
 \qquad \|P_\varepsilon Q_0\|_2=3.08062\times10^{-4}.
\]

Despite the small projector error,
\(\|e^{200B_\varepsilon}Q_0\|_2\approx1.94966\times10^{11}\), whereas the
moving-complement value is approximately \(1.68851\times10^4\).  The gap is
caused by the small fixed-complement leakage into the faster leading cluster;
it is not evidence for a continuum transient estimate.

## Audit and files

- `complement_diagnostic.json`: 15 primary rows, full time grids, residuals,
  cutoff comparisons, parameters, environment, and wall times;
- `progress.ndjson`: timestamped row-level progress and ETA events;
- `independent_validate.py`: an independent matrix construction using the
  explicit Fourier coefficients of \(W_0\) and \(W_0''\), 64-node Riesz
  contour projectors, inverse-based resolvent norms, and direct semigroup
  recomputation;
- `independent_validation.json`: all independent checks pass;
- `environment.json`, `command.txt`, `requirements.txt`, and `SHA256SUMS`:
  reproduction metadata.

The maximum primary algebraic residual is \(6.25\times10^{-14}\).  The
independent recomputation agrees to at most \(2.34\times10^{-15}\) in the
selected eigenvalue, \(8.45\times10^{-15}\) in the complement spectral
abscissa, \(1.71\times10^{-13}\) relatively in the resolvent peak, and
\(2.38\times10^{-13}\) relatively in the intrinsic semigroup sentinels.

## Claim boundary

Everything in this directory is a finite, dense, IEEE-754 binary64
diagnostic.  It supplies no interval enclosure, Fourier-tail bound, continuum
spectral classification, continuous-time semigroup estimate, moving-profile
uniformity, nonautonomous transfer, nonlinear Navier--Stokes estimate, or
Clay-problem conclusion.
