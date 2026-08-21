# R0.69Q — Vorticity-direction diffusion is already inside enstrophy dissipation

## 1. Result

R0.69P shows that incompressibility alone permits sharp positive vortex
stretching on an open set.  R0.69Q tests the next possible escape: perhaps the
diffusion of the vorticity direction automatically pays for that stretching in
space-time.

Let a smooth three-dimensional Navier--Stokes solution satisfy

\[
 (\partial_t+u\cdot\nabla)\omega-\nu\Delta\omega=S\omega,
 \qquad \nu>0,                                                \tag{1.1}
\]

and, on the open set where \(\rho=|\omega|>0\), write

\[
 \omega=\rho\xi,\qquad |\xi|=1,\qquad
 \alpha=\xi\cdot S\xi.                                      \tag{1.2}
\]

There are three exact identities:

\[
 \boxed{
 (\partial_t+u\cdot\nabla-\nu\Delta)\rho
 =\rho\alpha-\nu\rho|\nabla\xi|^2,}                        \tag{1.3}
\]

\[
 \boxed{
 (\partial_t+u\cdot\nabla)\xi
 =(I-\xi\otimes\xi)S\xi
 +\nu(I-\xi\otimes\xi)\Delta\xi
 +2\nu\nabla\log\rho\cdot\nabla\xi,}                       \tag{1.4}
\]

and

\[
 \boxed{
 \frac12(\partial_t+u\cdot\nabla-\nu\Delta)\rho^2
 +\nu|\nabla\rho|^2+\nu\rho^2|\nabla\xi|^2
 =\rho^2\alpha.}                                             \tag{1.5}
\]

The two positive terms in (1.5) are not new dissipation.  They are exactly
the polar decomposition

\[
 \boxed{
 |\nabla\omega|^2
 =|\nabla\rho|^2+\rho^2|\nabla\xi|^2.}                       \tag{1.6}
\]

More decisively, the sharp affine core from R0.69P has

\[
 \rho=w,\qquad \xi=e_3,\qquad \nabla\rho=\nabla\xi=0,
 \qquad
 \rho^2\alpha=\sqrt{\frac23}\,s w^2>0                       \tag{1.7}
\]

on a ball.  Thus the direction part and the entire interior enstrophy
dissipation vanish exactly where positive stretching saturates its sharp
pointwise bound.

This obstruction persists for genuine Navier--Stokes dynamics.  The compactly
supported affine-core field is smooth initial data for a local classical
solution.  On a smaller core ball \(B\), define

\[
 \begin{aligned}
 P(T)&=\int_0^T\!\int_B(\omega\cdot S\omega)_+\,dx\,dt,\\
 D_\xi(T)&=\nu\int_0^T\!\int_B\rho^2|\nabla\xi|^2\,dx\,dt,\\
 D_\omega(T)&=\nu\int_0^T\!\int_B|\nabla\omega|^2\,dx\,dt.
 \end{aligned}                                                \tag{1.8}
\]

Then

\[
 \boxed{
 \frac{P(T)}{T}\longrightarrow
 |B|\sqrt{\frac23}\,s w^2,
 \qquad
 \frac{D_\xi(T)}{T}\longrightarrow0,
 \qquad
 \frac{D_\omega(T)}{T}\longrightarrow0}                    \tag{1.9}
\]

as \(T\downarrow0\).  Consequently, no universal constant can absorb local
positive stretching by either interior direction dissipation or interior
enstrophy dissipation alone on every sufficiently short cylinder.

The route decision is therefore strict: an unconditional argument must retain
at least one term that the affine core does not erase--for example cutoff
flux, nonlocal magnitude--direction coupling, or a dynamically accumulated
defect with an initial trace.  R0.69Q does not prove or disprove global
regularity and does not solve the Millennium Problem.

## 2. Exact magnitude equation

Put \(D_t=\partial_t+u\cdot\nabla\).  Since \(|\xi|=1\),

\[
 \xi\cdot\partial_j\xi=0,
 \qquad
 \xi\cdot\Delta\xi=-|\nabla\xi|^2.                           \tag{2.1}
\]

Expanding the Laplacian gives

\[
 \Delta(\rho\xi)
 =\xi\Delta\rho+2\nabla\rho\cdot\nabla\xi+\rho\Delta\xi. \tag{2.2}
\]

Taking the scalar product of (1.1) with \(\xi\), the mixed term vanishes by
(2.1), while the final term contributes
\(-\rho|\nabla\xi|^2\).  This proves (1.3).  The negative sign is favorable,
but it is weighted by the same amplitude whose growth is driven by
\(\alpha\).

## 3. Exact direction equation and its zero-set boundary

Subtract \(\xi D_t\rho\) from the expanded vector equation and divide by
\(\rho\).  One obtains the equivalent unprojected formula

\[
 D_t\xi
 =(I-\xi\otimes\xi)S\xi
 +2\nu\nabla\log\rho\cdot\nabla\xi
 +\nu\bigl(\Delta\xi+|\nabla\xi|^2\xi\bigr).                \tag{3.1}
\]

Because of (2.1),

\[
 (I-\xi\otimes\xi)\Delta\xi
 =\Delta\xi+|\nabla\xi|^2\xi,                              \tag{3.2}
\]

so (3.1) is (1.4).  Every term is tangent to the unit sphere.

Equation (1.4) is useful only on \(\{\rho>0\}\).  Its drift contains
\(\nabla\log\rho\), which is not controlled near vorticity zeros by the
energy inequality.  Any global argument using (1.4) must either localize away
from the zero set or rewrite the calculation in nonsingular variables such as
\(\omega\) itself.  Treating the direction equation as a globally regular
parabolic equation would silently assume away this difficulty.

## 4. The polar enstrophy identity

Multiplying (1.3) by \(\rho\) and using

\[
 \rho\Delta\rho
 =\frac12\Delta\rho^2-|\nabla\rho|^2                        \tag{4.1}
\]

proves (1.5).  Independently,

\[
 \partial_j\omega
 =(\partial_j\rho)\xi+\rho\partial_j\xi.                    \tag{4.2}
\]

The two summands are orthogonal by (2.1), hence

\[
 |\partial_j\omega|^2
 =|\partial_j\rho|^2+\rho^2|\partial_j\xi|^2.               \tag{4.3}
\]

Summing over \(j\) proves (1.6).  After spatial integration, (1.5) is exactly
the ordinary enstrophy balance, not a stronger inequality.  In particular,
the angular term \(\rho^2|\nabla\xi|^2\) cannot be counted once in (1.5) and
again as an independent geometric gain.

## 5. A sharp local obstruction

For \(s,w>0\), set

\[
 S_+=\frac{s}{\sqrt6}\operatorname{diag}(-1,-1,2),
 \qquad
 \Omega x=\frac12w e_3\times x,
 \qquad A=S_++\Omega.                                       \tag{5.1}
\]

Let

\[
 B_A(x)=-\frac13x\times(Ax),
 \qquad
 v_A=\nabla\times(\chi B_A),                                \tag{5.2}
\]

where \(\chi\in C_c^\infty(B_2)\) equals one on \(B_1\).  The calculation in
R0.69P gives \(v_A=Ax\) on \(B_1\).  Therefore, throughout that ball,

\[
 S[v_A]=S_+,
 \qquad \omega[v_A]=w e_3.                                  \tag{5.3}
\]

Equations (1.7) follow immediately.  In particular, for every finite
\(C\), both proposed pointwise absorptions

\[
 (\omega\cdot S\omega)_+
 \le C\nu\rho^2|\nabla\xi|^2,
 \qquad
 (\omega\cdot S\omega)_+
 \le C\nu|\nabla\omega|^2                                  \tag{5.4}
\]

fail on the whole core ball, not merely at one exceptional point.

There is also a global scaling warning.  For any fixed compactly supported
solenoidal field \(v\), define

\[
 v_{a,L}(x)=aL\,v(x/L).                                      \tag{5.5}
\]

Writing

\[
 P_+(v)=\int(\omega[v]\cdot S[v]\omega[v])_+\,dx,
 \qquad D(v)=\int|\nabla\omega[v]|^2\,dx,                   \tag{5.6}
\]

one has exactly

\[
 P_+(v_{a,L})=a^3L^3P_+(v),
 \qquad D(v_{a,L})=a^2L D(v).                               \tag{5.7}
\]

Whenever \(P_+(v)>0\), their ratio is multiplied by \(aL^2/\nu\).  Thus no
scale-independent global positive-part absorption by \(\nu D\) is possible
without another controlling norm or flux.  This statement concerns the
positive part; it does not assign a sign to the globally integrated Betchov
production.

## 6. Short-time obstruction for genuine solutions

Take \(u_0=v_A\) from Section 5.  Standard local well-posedness for smooth
finite-energy data supplies a classical solution on some interval
\([0,T_*]\).  Fix a closed ball \(B\Subset B_1\).  At time zero,

\[
 (\omega_0\cdot S_0\omega_0)_+
 =\sqrt{\frac23}\,s w^2,
 \qquad \nabla\omega_0=0,
 \qquad \nabla\xi_0=0                                      \tag{6.1}
\]

uniformly on \(B\).  Smooth time continuity also gives
\(|\omega(x,t)|\ge w/2\) there for all sufficiently small \(t\), so \(\xi\)
is well defined on the cylinder.

The three integrands in (1.8) are continuous up to \(t=0\).  Therefore the
elementary time-average limit

\[
 \frac1T\int_0^T f(t)\,dt\longrightarrow f(0)               \tag{6.2}
\]

proves (1.9).  If a universal \(C\) satisfied

\[
 P(T)\le C D_\xi(T)
 \quad\hbox{or}\quad
 P(T)\le C D_\omega(T)                                     \tag{6.3}
\]

for every such solution and all small \(T\), division by \(T\) and passage
to the limit would give a positive number bounded by zero.  This is the
claimed contradiction.

The conclusion is local and deliberately excludes boundary-flux and initial-
trace terms.  It does not contradict localized regularity criteria: those
criteria retain cutoff flux, the nonlocal Biot--Savart coupling, high-vorticity
localization, or an assumed modulus of direction coherence.

## 7. What is established and what remains open

R0.69Q establishes:

1. the exact magnitude and direction equations away from vorticity zeros;
2. the exact radial--angular split of enstrophy dissipation;
3. a smooth compactly supported local equality case with positive maximal
   stretching and zero radial and angular dissipation on an open set;
4. a short-time Navier--Stokes obstruction to any universal interior-only
   absorption of positive stretching by direction or full enstrophy
   dissipation.

It does **not** establish:

1. failure of a localized inequality that includes cutoff flux or initial
   trace terms;
2. failure of a magnitude-weighted nonlocal geometric criterion;
3. failure of the classical conditional vorticity-direction criteria;
4. global regularity, finite-time blow-up, or a solution of the Millennium
   Problem.

The next viable target is therefore not another pointwise angular estimate.
R0.69R will keep the nonlocal difference

\[
 \omega(x)\times\omega(x+z)
 =\omega(x)\times\bigl(\omega(x+z)-\omega(x)\bigr)           \tag{7.1}
\]

inside the signed Biot--Savart kernel and determine whether the resulting
near/far-scale split gives any exponent beyond the classical enstrophy
estimate.  Acceptance requires a genuine scale gain after optimizing the
split radius; reproducing the classical supercritical power will close that
branch.

## 8. Relation to known results

The polar decomposition and the vorticity-direction equation are classical.
Constantin and Fefferman use direction coherence together with the nonlocal
vortex-stretching representation; Beir\~ao da Veiga and Berselli weaken the
direction regularity assumptions; Gruji\'c localizes geometric depletion to
arbitrarily small space-time cylinders.  R0.69Q does not strengthen those
conditional regularity theorems.  Its contribution to this project is the
sharp affine-core and short-time audit showing precisely why direction
diffusion, taken by itself, cannot supply the missing unconditional estimate.

Primary references:

1. P. Constantin and C. Fefferman, *Direction of Vorticity and the Problem of
   Global Regularity for the Navier--Stokes Equations*, Indiana Univ. Math. J.
   42 (1993), 775--789.  Published result.
2. H. Beir\~ao da Veiga and L. C. Berselli, *On the regularizing effect of the
   vorticity direction in incompressible viscous flows*, Differential and
   Integral Equations 15 (2002), 345--356,
   doi:10.57262/die/1356060864.  Published result.
3. Z. Gruji\'c, *Localization and Geometric Depletion of Vortex-Stretching in
   the 3D NSE*, Comm. Math. Phys. 290 (2009), 861--870,
   doi:10.1007/s00220-008-0726-8.  Published result.

