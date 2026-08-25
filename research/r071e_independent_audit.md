# R0.71E independent mathematical audit

**Date:** 2026-08-25

**Scope:** independent real-space reconstruction of the projected-Lamb
identity, the minimal six-mode phase pair, the separated-radius heat trace,
and the whole-space scaling check.

The checker deliberately imports no project audit module.  It starts from
trigonometric functions, differentiates them directly, and evaluates all
periodic averages by exact symbolic integration.  A separate
\(96\times96\) midpoint rule uses ordinary floating-point trigonometry.

## 1. Verdict

All requested identities pass.

For

\[
 u_\sigma
 =\left(
 0,-2\cos x,
 2\sigma\sin(x+y)-2\cos y
 \right),
 \qquad \sigma=\pm1,
 \tag{1.1}
\]

the checker obtains

\[
 \omega_\sigma
 =\left(
 2\sigma\cos(x+y)+2\sin y,
 -2\sigma\cos(x+y),
 2\sin x
 \right).
 \tag{1.2}
\]

Direct normalized integration gives

\[
 \|u_\sigma\|_2^2=6,
 \qquad
 \|\omega_\sigma\|_2^2=8,
 \qquad
 \|\nabla\omega_\sigma\|_2^2=12,
 \tag{1.3}
\]

and

\[
 \left\langle\omega_\sigma,
 \omega_\sigma\cdot\nabla u_\sigma
 -u_\sigma\cdot\nabla\omega_\sigma
 \right\rangle=2\sigma.
 \tag{1.4}
\]

Thus the two phases have identical quadratic spectra and opposite cubic
work.  The projected Lamb field reconstructed independently in physical
space satisfies

\[
 \nabla\times L_\sigma
 =\omega_\sigma\cdot\nabla u_\sigma
 -u_\sigma\cdot\nabla\omega_\sigma,
 \tag{1.5}
\]

while \(u_\sigma\times\omega_\sigma-L_\sigma\) is curl free.

The separated low-radius positive block gives

\[
 \frac{(b_{\rm lo}(s)^+)^2}{D_{\rm lo}(s)}
 =a^4K^6e^{-2K^2s}.
 \tag{1.6}
\]

Hence

\[
 q_{\rm lo}(0)
 =2K^2\int_0^\infty q_{\rm lo}(s)\,ds,
 \tag{1.7}
\]

and, with the physical bottom enstrophy \(8a^2K^4\),

\[
 A_{\rm bottom}=\frac{a^2K^2}{8},
 \qquad
 \mathcal V_{\rm bulk}=\frac{a^2}{16}.
 \tag{1.8}
\]

This confirms the exact two-derivative bottom-trace loss used in the main
report.

## 2. Real-space vorticity equation

The field (1.1) is independent of \(z\), and its first component vanishes.
The checker computes

\[
 \nabla\cdot u_\sigma=0
 \tag{2.1}
\]

and evaluates separately

\[
 \mathcal S_\sigma=(\omega_\sigma\cdot\nabla)u_\sigma,
 \qquad
 \mathcal T_\sigma=(u_\sigma\cdot\nabla)\omega_\sigma.
 \tag{2.2}
\]

No Fourier convolution routine is called.  The exact averages are

\[
 \langle\omega_\sigma,\mathcal S_\sigma\rangle=2\sigma,
 \qquad
 \langle\omega_\sigma,\mathcal T_\sigma\rangle=0.
 \tag{2.3}
\]

The global transport cancellation in (2.3) does not hold separately at the
two output radii.  Write

\[
 \omega_{\rm lo}=(2\sin y,0,2\sin x),
 \tag{2.4}
\]

\[
 \omega_{\rm hi}
 =(2\sigma\cos(x+y),-2\sigma\cos(x+y),0).
 \tag{2.5}
\]

Then

\[
 \begin{array}{c|ccc}
 &\langle\omega_*,\mathcal S\rangle
 &\langle\omega_*,\mathcal T\rangle
 &\langle\omega_*,\mathcal S-\mathcal T\rangle\\ \hline
 \mathrm{lo}&0&2\sigma&-2\sigma\\
 \mathrm{hi}&2\sigma&-2\sigma&4\sigma.
 \end{array}
 \tag{2.6}
\]

This independently confirms that the transport--filter commutator is an
essential part of the filtered shell work.

## 3. Independent projected-Lamb reconstruction

The horizontal velocity in (1.1) is the shear

\[
 v=(0,-2\cos x).
 \tag{3.1}
\]

Its nonlinear advection vanishes pointwise.  The third component

\[
 w=2\sigma\sin(x+y)-2\cos y
 \tag{3.2}
\]

is a passive scalar driven by this shear.  Therefore

\[
 L_\sigma=(0,0,-v\cdot\nabla w)
 \tag{3.3}
\]

at the initial trace.  Explicitly,

\[
 \boxed{
 L_\sigma
 =\left(
 0,0,
 4\cos x\,[\sigma\cos(x+y)+\sin y]
 \right).}
 \tag{3.4}
\]

Direct differentiation proves (1.5).  The checker also forms

\[
 R_\sigma=u_\sigma\times\omega_\sigma-L_\sigma
 \tag{3.5}
\]

and obtains

\[
 \nabla\times R_\sigma=0.
 \tag{3.6}
\]

On the periodic torus, after fixing the zero mean, this is exactly the
gradient part of the Lamb vector.  This independently verifies the Hodge
split used in the report without solving for the pressure.

The same decomposition also establishes the smooth NSE status.  The
horizontal shear decays by the heat equation, and the third component solves
a linear parabolic equation with smooth time-dependent coefficients.  Both
phases therefore produce global smooth 2D3C periodic NSE solutions.

## 4. Independent heat-trace calculation

Scale (1.1) by

\[
 u_{\sigma,a,K}(x)=aK u_\sigma(Kx).
 \tag{4.1}
\]

For \(\sigma=-1\), the low-radius block has

\[
 b_{\rm lo}(s)=2a^3K^6e^{-2K^2s},
 \qquad
 D_{\rm lo}(s)=4a^2K^6e^{-2K^2s}.
 \tag{4.2}
\]

The checker derives (1.6) directly and evaluates

\[
 \int_0^\infty q_{\rm lo}(s)\,ds
 =\frac12a^4K^4.
 \tag{4.3}
\]

Equations (1.7)--(1.8) follow.  On a finite vertical box,

\[
 \frac1{8a^2K^4}
 \int_0^{\theta/K^2}q_{\rm lo}(s)\,ds
 =\frac{a^2}{16}(1-e^{-2\theta}),
 \tag{4.4}
\]

which is independent of \(K\).  This is a heat-variable trace calculation,
not a numerical time evolution.

## 5. Whole-space scaling check

Near the origin of the compactly supported construction in the main report,
the checker uses

\[
 u=(x,-y-z,0),
 \qquad \omega=(1,0,0).
 \tag{5.1}
\]

It obtains

\[
 (\omega\cdot\nabla)u-(u\cdot\nabla)\omega=(1,0,0),
 \tag{5.2}
\]

\[
 u\times\omega=(0,0,y+z),
 \qquad
 \nabla\times(u\times\omega)=(1,0,0).
 \tag{5.3}
\]

Hence the projected Lamb field is nonzero.  Under

\[
 u_\lambda(x)=\lambda u(\lambda x),
 \tag{5.4}
\]

the squared kinetic, enstrophy, and Lamb norms scale as

\[
 \lambda^{-1},\qquad\lambda,\qquad\lambda^3,
 \tag{5.5}
\]

respectively.  The quotient \(\|L\|_2^2/\|\omega\|_2^2\) therefore scales
like \(\lambda^2\), while its parabolic-time integral is invariant.

This is a comparison among different smooth data.  It is not evidence for a
singular trajectory.

## 6. Floating-point sanity check

A separate midpoint sum evaluates the phase \(\sigma=1\) on a
\(96\times96\) grid.  Against the exact target

\[
 (\|u\|_2^2,Y,D,\mathfrak S,\mathfrak T,\mathfrak S-\mathfrak T)
 =(6,8,12,2,0,2),
 \tag{6.1}
\]

the maximum absolute error is below \(3\times10^{-14}\).  The floating-point
calculation is only a transcription check; every deciding statement uses
exact symbolic arithmetic.

## 7. Claim boundary

The independent reconstruction confirms:

- the projected-Lamb curl identity;
- the curl-free gradient complement;
- the phase-pair sign reversal with identical quadratic norms;
- the two-radius stretching/transport redistribution;
- the exact factor \(2K^2\) between bottom trace and heat bulk;
- the whole-space critical scaling.

It does not prove that \(A_{\rm sb,+}\in L^1_t\), that every adaptive trace
estimate fails, that pressure is unimportant in a strain ledger, or that a
regular or singular Millennium-problem solution has been constructed.
