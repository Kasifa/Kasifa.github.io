# R0.71D independent mathematical audit

**Date:** 2026-08-25

**Scope:** independent reconstruction of a pointwise-material shear ledger,
its parabolic-time equality case, an additional embedded two-dimensional
Fourier stress check, and the bottom Littlewood--Paley cutoff commutator.

The checker imports no project audit module. It derives the field and every
local integral from the stated formulas. Exact identities use SymPy. A separate
\(48\times48\) midpoint rule uses ordinary floating-point trigonometry and does
not call the symbolic integration routine.

## 1. Verdict

All requested identities pass. The primary material-shear calculation gives

\[
 Y_\pm
 =\frac{A^2e^{-2\nu k^2t}(2\pm\rho)}8,
 \qquad
 D_\pm
 =\frac{A^2k^2e^{-2\nu k^2t}(2\mp\rho)}8,
 \tag{1.1}
\]

\[
 \beta_\pm
 =\mp\frac{\nu A^2k^2\rho e^{-2\nu k^2t}}4.
 \tag{1.2}
\]

The parent signed flux is zero. The positive child has

\[
 \delta
 =\frac{\nu^2A^2k^2\rho^2e^{-2\nu k^2t}}{2(2+\rho)}>0,
 \qquad
 \frac{\delta}{Y_++Y_-}
 =\frac{\nu^2k^2\rho^2}{2+\rho}.
 \tag{1.3}
\]

The weights in this calculation are pointwise material. On a parabolic
interval, the signed-box lower bound is an equality and the integrated
normalized cost is \(\nu\theta\rho^2/(2+\rho)\), independent of \(k\).

As an additional stress check, the cellular embedded-2D family gives

\[
 Y_\pm=C^2\left(\frac12\pm\frac\rho4\right),
 \qquad
 D_\pm=\frac{C^2N^2}{2},
 \qquad
 \beta_\pm=\mp\frac{\nu\rho C^2N^2}{4}.
 \tag{1.4}
\]

and leaves the exact positive-child defect

\[
 \delta=\frac{(\beta_-^+)^2}{D_-}
 =\frac{\nu^2\rho^2C^2N^2}{8}>0,
 \qquad
 \frac{\delta}{Y_++Y_-}
 =\frac{\nu^2\rho^2N^2}{8}.
 \tag{1.5}
\]

The second family also saturates its signed-box lower bound. Thus neither
calculation supplies a hidden negative power of frequency.

This is a narrow obstruction. It is not a proof of three-dimensional
regularity or singularity, and it is not a no-go theorem for every possible
flow-adapted localization.

## 2. Primary pointwise-material shear

Set

\[
 u(t,x)=\left(
 0,\frac Ak e^{-\nu k^2t}\sin(kx_1),0
 \right),
 \qquad
 \omega(t,x)=\left(
 0,0,Ae^{-\nu k^2t}\cos(kx_1)
 \right).
 \tag{2.1}
\]

Direct differentiation gives

\[
 \nabla\cdot u=0,\qquad
 (u\cdot\nabla)u=0,\qquad
 u\cdot\nabla\omega=0,\qquad
 \omega\cdot\nabla u=0.
 \tag{2.2}
\]

Also \(\partial_tu-\nu\Delta u=0\), so this is an exact smooth shear
Navier--Stokes solution with constant pressure.

Use the smooth positive partition

\[
 \phi_\pm(x)=\frac{1\pm\rho\cos(2kx_1)}2,
 \qquad 0<\rho<1.
 \tag{2.3}
\]

The weights depend only on \(x_1\), while \(u\) has only an \(x_2\) component.
Hence

\[
 (\partial_t+u\cdot\nabla)\phi_\pm=0
 \tag{2.4}
\]

pointwise. With normalized spatial measure, direct integration gives
(1.1)--(1.3), and each child satisfies

\[
 \frac12Y_\pm'+\nu D_\pm=\beta_\pm,
 \qquad
 \beta_\pm=\frac{\nu}{2}
 \int(\Delta\phi_\pm)|\omega|^2.
 \tag{2.5}
\]

For

\[
 \tau=\frac{\theta}{\nu k^2},
 \tag{2.6}
\]

the positive child obeys

\[
 B=\int_0^\tau\beta_-\,dt
 =\frac{A^2\rho(1-e^{-2\theta})}{8},
 \qquad
 \overline D=\int_0^\tau D_-\,dt
 =\frac{A^2(2+\rho)(1-e^{-2\theta})}{16\nu}.
 \tag{2.7}
\]

Consequently,

\[
 \boxed{
 \frac{B^2}{\overline D}
 =\int_0^\tau\frac{\beta_-^2}{D_-}\,dt
 =\frac{\nu A^2\rho^2(1-e^{-2\theta})}{4(2+\rho)}.}
 \tag{2.8}
\]

The Cauchy step is an exact equality. The normalized integral is

\[
 \int_0^\tau\frac{\delta}{Y_++Y_-}\,dt
 =\frac{\nu\theta\rho^2}{2+\rho},
 \tag{2.9}
\]

which is independent of \(k\). After the natural viscous normalization by
\(\nu\), the dimensionless cost is \(\theta\rho^2/(2+\rho)\). This is the
pointwise-material, scale-critical obstruction used in the R0.71D conclusion.

## 3. Additional embedded-2D Navier--Stokes stress check

Write \(X=Nx_1\), \(Y=Nx_2\), and set

\[
 \psi(t,x)=a(t)(\cos X+\cos Y),
 \qquad
 a'(t)=-\nu N^2a(t).
 \tag{3.1}
\]

The velocity and vorticity are

\[
 u=(\partial_2\psi,-\partial_1\psi,0)
 =(-aN\sin Y,aN\sin X,0),
 \tag{3.2}
\]

\[
 \omega=\nabla\times u
 =(0,0,C(t)(\cos X+\cos Y)),
 \qquad C(t)=a(t)N^2.
 \tag{3.3}
\]

Direct differentiation gives

\[
 \nabla\cdot u=0,
 \qquad
 u\cdot\nabla\omega=0,
 \qquad
 \omega\cdot\nabla u=0.
 \tag{3.4}
\]

There is a wording point worth keeping explicit. The velocity advection is not
pointwise zero. Instead,

\[
 (u\cdot\nabla)u
 =\nabla\bigl(a^2N^2\cos X\cos Y\bigr).
 \tag{3.5}
\]

Its Leray projection is zero and it is absorbed by
\(p=-a^2N^2\cos X\cos Y\). Together with
\(\partial_tu-\nu\Delta u=0\), this proves that the field is an exact smooth
two-dimensional Navier--Stokes solution embedded in the three-torus. The
vanishing nonlinearities in (3.4) are the vorticity transport and stretching
terms.

## 4. Additional embedded-2D local ledger

Use normalized phase-space measure \((2\pi)^{-2}\,dX\,dY\) and

\[
 \phi_\pm=\frac{1\pm\rho\cos(X-Y)}2,
 \qquad 0<\rho<1.
 \tag{4.1}
\]

These weights form a smooth positive partition. They are static, not
pointwise material. Nevertheless,

\[
 \frac12\int (u\cdot\nabla\phi_\pm)|\omega|^2=0
 \tag{4.2}
\]

exactly, because \(u\cdot\nabla\omega=0\) and \(u\) is divergence-free. The
remaining cutoff term is the vertical heat flux

\[
 \beta_\pm
 =\frac12\int
 (u\cdot\nabla\phi_\pm+\nu\Delta\phi_\pm)|\omega|^2.
 \tag{4.3}
\]

Direct phase integration gives (1.4), and each child satisfies

\[
 \frac12Y_\pm'+\nu D_\pm=\beta_\pm.
 \tag{4.4}
\]

Since \(\beta_++\beta_-=0\), the parent signed-before-square ledger is zero.
Equation (1.5) shows that the positive child ledger is strictly positive. The
defect is an internal heat flux: summing the children cancels it, while taking
the positive part before squaring retains it.

## 5. Additional embedded-2D parabolic equality

Let

\[
 C(t)=mN^2e^{-\nu N^2t},
 \qquad
 \tau=\frac{\theta}{\nu N^2}.
 \tag{5.1}
\]

For the positive child \(\phi_-\), exact time integration gives

\[
 \overline D
 =\int_0^\tau D_-\,dt
 =\frac{m^2N^4(1-e^{-2\theta})}{4\nu},
 \tag{5.2}
\]

\[
 B=\int_0^\tau\beta_-\,dt
 =\frac{\rho m^2N^4(1-e^{-2\theta})}{8}.
 \tag{5.3}
\]

Therefore

\[
 \boxed{
 \frac{B^2}{\overline D}
 =\int_0^\tau\frac{\beta_-^2}{D_-}\,dt
 =\frac{\nu\rho^2m^2N^4(1-e^{-2\theta})}{16}.}
 \tag{5.4}
\]

The signed-time Cauchy estimate is saturated. The corresponding normalized
instantaneous coefficient is
\(\nu^2\rho^2N^2/8\), so its integral over a parabolic interval is of critical
size rather than \(N^{-\varepsilon}\).

## 6. Bottom LP--cutoff commutator

I use the convention

\[
 [T_j,\phi]f=T_j(\phi f)-\phi T_jf.
 \tag{6.1}
\]

Assume the radial symbol satisfies

\[
 m_j(N)=m,
 \qquad
 m_j(\sqrt5N)=0.
 \tag{6.2}
\]

Multiplying \(\cos X+\cos Y\) by \(\phi_+\) creates the low modes at radius
\(N\) and the two high cosine modes \((2,-1)\), \((1,-2)\) at radius
\(\sqrt5N\). A signed Fourier-coefficient reconstruction gives

\[
 [T_j,\phi_+]\omega
 =-\frac{\rho m C}{4}
 \left[\cos(2X-Y)+\cos(X-2Y)\right].
 \tag{6.3}
\]

Thus the requested high-mode cosine coefficient, relative to the vorticity
amplitude \(C\), is exactly

\[
 -\frac{\rho m}{4}.
 \tag{6.4}
\]

Reversing the commutator convention reverses this sign; the checker records
the convention in its JSON output.

## 7. Independent quadrature

The checker also evaluates \(Y_\pm\), \(D_\pm\), the cutoff-transport terms,
and \(\beta_\pm\) on a \(48\times48\) midpoint grid in \((X,Y)\). It uses
\(C=1.3\), \(N=3\), \(\nu=0.7\), and \(\rho=0.6\). This finite trigonometric
polynomial is resolved exactly by the grid up to floating-point roundoff. The
maximum absolute discrepancy is required to be below \(2\times10^{-13}\).
The optional --output PATH argument writes the same canonical JSON with one
terminal newline while the ordinary invocation continues to print it.

## 8. Claim boundary

The certificate proves an exact pointwise-material scale-critical heat-flux
defect for the shear, an additional embedded-2D stress check, and the stated
LP--cutoff commutator. It does not prove any of the following:

- unconditional regularity for the three-dimensional Navier--Stokes equations;
- divergence of the local ledger for every material or parabolic tent family;
- failure of every compact, adjoint, or flow-adapted localization;
- absence of an NSE-specific nonlinear sign or depletion cancellation.

The example is therefore evidence against closing the route by telescoping or
time-box Cauchy alone. It leaves a genuinely PDE-specific cancellation or
depletion mechanism open.
