# R0.71O standalone soft-face and Fourier audit

## Purpose

The file research/r071o_independent_audit.py checks the R0.71O face
calculation with an implementation that imports neither the exact symbolic
producer nor an earlier release checker. It uses standalone SciPy quadrature
for the finite-order and oscillatory profiles and a standalone \(32^3\) NumPy
FFT reconstruction for one smooth periodic Navier--Stokes initial jet.

The calculation uses ordinary binary64 arithmetic. It corroborates the exact
identities in the report but does not replace their proofs with a numerical
claim.

## Command

    PYTHONDONTWRITEBYTECODE=1 tmp/r068b-venv/bin/python \
      research/r071o_independent_audit.py \
      --output /tmp/r071o-independent-result.json

The command writes one JSON record containing every checked quadrature,
closed-form target, FFT scalar, and residual.

## Finite-order face profiles

For each order \(m=1,\ldots,8\), the checker integrates

\[
 k_m(s)=\frac{2m s^{2m-1}}{(1+s^{2m})^2},
 \qquad s\in(0,\infty),
\]

which is the outgoing derivative profile of
\(s^{2m}/(1+s^{2m})\). The exact mass is

\[
 \int_0^\infty k_m(s)\,ds=1.
\]

All eight adaptive quadratures pass. The maximum error of the computed mass
from one is \(2.22\times10^{-16}\). The script also integrates the additional
radial-damping profile

\[
 r_m(s)=\frac{s^{2m}}{(1+s^{2m})^2}.
\]

Its computed masses are positive for every tested order, from
\(0.7853981634\) at \(m=1\) to \(0.0629034089\) at \(m=8\).

## Raw logarithms and joint cancellation

On one active half-face the checker fixes \(\gamma=0.73\) and independently
integrates

\[
 S_\varepsilon(x)=\frac{\gamma^2}{x+\varepsilon},
 \qquad
 R_\varepsilon(x)=-\frac{\gamma^2x}{(x+\varepsilon)^2},
 \qquad 0<x<1.
\]

Their exact masses are

\[
 \int_0^1S_\varepsilon\,dx
 =\gamma^2\log\frac{1+\varepsilon}{\varepsilon},
\]

\[
 \int_0^1R_\varepsilon\,dx
 =\gamma^2\left(
 \frac1{1+\varepsilon}
 -\log\frac{1+\varepsilon}{\varepsilon}
 \right),
\]

so the separate logarithms cancel and

\[
 \int_0^1(S_\varepsilon+R_\varepsilon)\,dx
 =\frac{\gamma^2}{1+\varepsilon}.
\]

The numerical sweep uses
\(\varepsilon=10^{-1},10^{-2},10^{-4},10^{-6}\). At \(10^{-6}\), the source
mass is \(7.3622861092\), the radial mass is \(-6.8293866421\), and their sum
is \(0.5328994671\). The maximum relative error in the joint identity over
the sweep is \(3.33\times10^{-16}\). Thus the checker sees both separate
logarithmic growth and the finite combined face mass; it does not infer a
uniform measure bound for either raw term separately.

## Oscillatory path and bounded ordinary budgets

For \(N=1,2,4,8,16,32,64\), the script evaluates the smooth Hilbert path

\[
 C_N(t)=N^{-1}\sin(Nt)e,
 \qquad F_N=e,\qquad Y_N=1,\qquad
 \varepsilon_N=N^{-4}
\]

on \([0,2\pi]\), with \(\lambda=0.37\). Writing
\(\delta_N=N^2\varepsilon_N=N^{-2}\), the checked positive variation is

\[
 V^+(a_{N,\varepsilon_N})
 =\frac{N}{1+\delta_N}.
\]

The maximum relative error in this formula is
\(1.18\times10^{-16}\). It grows from \(0.5\) at \(N=1\) to
\(63.9843788138\) at \(N=64\).

The R0.71I extra radial mass is checked against

\[
 \int_0^{2\pi}
 2\lambda\theta_{N,\varepsilon_N}a_{N,\varepsilon_N}\,dt
 =\frac{\lambda\pi\sqrt{\delta_N}}
 {(1+\delta_N)^{3/2}}.
\]

It is \(0.0181556833\) at \(N=64\) and tends to zero as the face count grows.
The reported relative residuals for this identity are at most
\(6.94\times10^{-17}\).

At the same time the ordinary quadratic budgets are

\[
 \int_0^{2\pi}d_N\,dt=\frac{\pi}{N^2},
 \qquad
 \int_0^{2\pi}\|C_{N,t}\|^2dt=\pi,
\]

\[
 \int_0^{2\pi}\|C_{N,t}+\lambda C_N\|^2dt
 =\pi\left(1+\frac{\lambda^2}{N^2}\right),
 \qquad
 \int_0^{2\pi}\|F_N\|^2dt=2\pi.
\]

Thus the sampled variation grows like \(N\), while the derivative, source,
and field budgets remain bounded and the denominator mass decreases like
\(N^{-2}\). This is an abstract smooth-path separation, not an NSE face-count
example.

## Standalone \(32^3\) Fourier reconstruction

The FFT checker declares

\[
 u_0(x)=(0,\cos x_1,\cos x_2)
\]

on the normalized periodic torus. It reconstructs vorticity, computes
\(L=\mathbb P(u_0\times\omega_0)\), and retains only the shell
\(|k|^2=2\). The initial vorticity lies at \(|k|=1\), so the filtered
vorticity is zero, while the projected Lamb field has exactly four retained
modes \((\pm1,\pm1,0)\).

The independent FFT returns the exact target values

\[
 Y_0=1,\qquad
 \|F\|_2^2=\frac14,\qquad
 \|\operatorname{curl}F\|_2^2=\frac12,
\]

\[
 \|C_t(0)\|_2^2=1,\qquad
 B_t(0)=\frac12,\qquad
 \frac{B_t(0)^2}{Y_0\|C_t(0)\|_2^2}=\frac14.
\]

The recorded residuals for velocity divergence, filtered-Lamb divergence,
zero initial filtered vorticity, all five scalar targets, and the right-entry
trace are \(0.0\) in the reported binary64 run. The four-mode count is also
checked explicitly. These values describe an instantaneous NSE initial jet;
the program never advances the solution in time.

## Claim boundary

This checker performs no time stepping or DNS. It uses no interval
arithmetic and proves no sign statement on a time interval, no internal NSE
face-count theorem, no uniform frame--cell face budget, no continuation
criterion, and no Navier--Stokes regularity or singularity result. The
oscillatory family is an abstract Hilbert path, and the Fourier calculation
certifies only one smooth one-sided NSE initial face.
