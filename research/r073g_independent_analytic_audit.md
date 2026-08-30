# R0.73G independent analytic audit

**Date:** 2026-08-30
**Audited source:** research/r073g_nonlinear_shadowing_proof.md
**Audited source SHA-256:** e3b5ae75eaa4a6d59a6fc79de0dab0c658e515293148e777bb953af5349c306c
**Scope:** physical scaling, planar invariance, top-vector regularity, the
\(H^3\) Riccati estimate, the all-mode remainder, the seed ceiling, and
double-row noncancellation
**Evidence class:** independent analytic recomputation, conditional on the
R0.73F moving-bundle lower bound

## 0. Verdict

All seven requested gates pass.  No correction obligation was found in the
audited source.

| Gate | Verdict | Decisive check |
|---|---|---|
| Physical-time and amplitude normalization | **PASS** | \(d=4t\), \(R=2\), \(K_z=1\), and background amplitude \(2\Lambda\) reproduce \(\widetilde B_{\Lambda^{-1}}(d)\) with no missing factor |
| Exact planar invariance and global continuation | **PASS** | the class \(U_1=0,\ \partial_{x_1}U=0\) is invariant and is exactly periodic two-dimensional Navier--Stokes |
| Frozen top-vector regularity and launch cost | **PASS** | two elliptic lifts give \(H^4_x=O(\Lambda^2)\); the velocity lift is order zero and \(L^2\)-isometric |
| Fixed-window \(H^3\) Riccati bootstrap | **PASS** | \(Y'\le a\Lambda Y+bY^2\) and the stated threshold keep the denominator at least \(3a\Lambda/4\) |
| All-mode quadratic remainder | **PASS** | the estimate is made before any Fourier-row projection and gives the stated \(C_De^{M_D\Lambda}Y(0)^2\) bound |
| Seed ceiling and half-gain | **PASS** | the two terms in the minimum respectively close the Riccati bound and make the nonlinear remainder at most one half of the linear lower signal |
| Double-row noncancellation | **PASS** | zero Leray output would force a two-frequency profile, which is incompatible with the nonzero \(W_2\) coefficient in the frozen eigenvalue equation |

The conclusion remains a relative-amplification theorem inside an exact
globally regular planar subsystem.  This audit does not upgrade it to an
order-one departure statement or to a result for general three-dimensional
data.

## 1. Physical normalization

Set

\[
 \overline U_\Lambda(t,y)
 =\bigl(0,0,2\Lambda W(4t,2y)\bigr),
 \qquad
 W_d=W_{xx}.
 \tag{1.1}
\]

Direct differentiation gives

\[
 \partial_t\overline U_{\Lambda,3}
 =8\Lambda W_d(4t,2y),
 \qquad
 \Delta\overline U_{\Lambda,3}
 =8\Lambda W_{xx}(4t,2y).
 \tag{1.2}
\]

The background is independent of \(z\), so
\(\overline U_\Lambda\cdot\nabla\overline U_\Lambda=0\).  Thus (1.1) is an
exact unforced viscosity-one Navier--Stokes solution.

For the physical row \(K_z=1\) and shear frequency \(R=2\), put

\[
 x=2y,\qquad d=4t,\qquad
 L=-\partial_x^2+\frac14.
 \tag{1.3}
\]

Then

\[
 \Delta_{y,z}=4\partial_x^2-1=-4L.
 \tag{1.4}
\]

After the physical linearized row equation is divided by the factor \(4\)
coming from \(\partial_t=4\partial_d\), its shear coefficient is
\(2\Lambda/4=\Lambda/2\), its coupling coefficient has the same normalized
factor, and its viscous term is \(-L\).  More explicitly, for

\[
 u(y,z)=\bigl(0,v(2y),2iv'(2y)\bigr)e^{iz},
 \tag{1.5}
\]

the perturbation vorticity is \(-4iLv\,e^{iz}\), while
\(\partial_y^2\overline U_{\Lambda,3}=8\Lambda W_{xx}\).  The linearized
vorticity equation therefore reduces to

\[
 L\partial_tv
 =-2i\Lambda\bigl(WLv+W_{xx}v\bigr)-4L^2v.
 \tag{1.6}
\]

After \(d=4t\), this is

\[
 L\partial_dv
 =-\frac{i\Lambda}{2}\bigl(WLv+W_{xx}v\bigr)-L^2v.
 \tag{1.7}
\]

Thus, for \(q=Lv\), the normalized kinetic equation is

\[
 \partial_dq
 =\Lambda\widetilde A(d)q-Lq.
 \tag{1.8}
\]

With

\[
 \varepsilon=\Lambda^{-1},
 \qquad
 \theta=\Lambda d,
 \tag{1.9}
\]

equation (1.5) becomes

\[
 \partial_\theta q
 =\left[\widetilde A(\varepsilon\theta)-\varepsilon L\right]q
 =\widetilde B_\varepsilon(\varepsilon\theta)q,
 \tag{1.10}
\]

which is precisely the R0.73F fast-time evolution.  A profile endpoint
\(d_D\) therefore occurs at

\[
 T_D=\frac{d_D}{4}
 \tag{1.11}
\]

in physical time and at \(\theta=d_D/\varepsilon=d_D\Lambda\) in fast
time.  Consequently the R0.73F factor

\[
 \exp\!\left((\alpha+\eta)\frac{d_D}{\varepsilon}\right)
 =e^{\kappa_D\Lambda},
 \qquad
 \kappa_D=(\alpha+\eta)d_D,
 \tag{1.12}
\]

has exactly the exponent used in the nonlinear proof.  The physical time,
background amplitude, row frequency, and fast-time exponent are mutually
consistent.

**Verdict: PASS.**

## 2. Exact planar invariance

Let

\[
 \mathcal S_{2D}
 =\{U=(0,U_2(y,z),U_3(y,z)):
   \partial_yU_2+\partial_zU_3=0\}.
 \tag{2.1}
\]

Fourier modes of a field in this class have first wave-number component
zero and first velocity component zero.  The three-dimensional Leray
symbol

\[
 P(k)=I-\frac{k\otimes k}{|k|^2}
 \tag{2.2}
\]

cannot create a first component when \(k_1=0\).  The Laplacian and the
quadratic convolution also preserve \(k_1=0\).  Therefore
\(\mathcal S_{2D}\) is invariant under the full three-dimensional equation,
not merely under a row-truncated model.

Equivalently, within this class the only vorticity component is

\[
 \omega=\partial_yU_3-\partial_zU_2,
 \tag{2.3}
\]

and it obeys

\[
 \partial_t\omega+U_2\partial_y\omega+U_3\partial_z\omega
 =\Delta_{y,z}\omega.
 \tag{2.4}
\]

The usual enstrophy identity and periodic two-dimensional regularity give
global smoothness for smooth data.  Since both the background and the real
conjugate-pair seed lie in \(\mathcal S_{2D}\), the theorem's nonlinear
orbit is global independently of the quantitative bootstrap.

**Verdict: PASS.**

## 3. Top-vector regularity and kinetic-to-velocity lift

At \(d=0\), choose an \(L^2_x\)-normalized eigenvector in the finite
R0.73F top space:

\[
 \bigl(\widetilde A(0)-\varepsilon L\bigr)h_\varepsilon
 =\lambda_\varepsilon h_\varepsilon.
 \tag{3.1}
\]

The common contour keeps \(\lambda_\varepsilon\) uniformly bounded, and
\(\widetilde A(0)\) is bounded on every fixed \(H^m_x\).  Rearranging (3.1)
and applying the elliptic estimate for \(L\) gives, for fixed \(m\),

\[
 \begin{aligned}
 \|h_\varepsilon\|_{H^{m+2}}
 &\le C_m\bigl(\|Lh_\varepsilon\|_{H^m}
                  +\|h_\varepsilon\|_{H^m}\bigr)\\
 &\le C_m'\varepsilon^{-1}
       \|h_\varepsilon\|_{H^m},
 \end{aligned}
 \tag{3.2}
\]

for sufficiently small \(\varepsilon\).  The iterations \(m=0\) and
\(m=2\) yield

\[
 \|h_\varepsilon\|_{H^2}\le C\varepsilon^{-1},
 \qquad
 \|h_\varepsilon\|_{H^4}\le C\varepsilon^{-2}
 =C\Lambda^2.
 \tag{3.3}
\]

Thus the claimed \(\Lambda^2\) cost is sufficient; no third elliptic lift
is needed.

For

\[
 \mathcal Eh
 =\left(
 0,\frac12(L^{-1/2}h)(2y),
 i(\partial_xL^{-1/2}h)(2y)
 \right)e^{iz},
 \tag{3.4}
\]

the divergence is zero.  On the \(x\)-Fourier coefficient \(n\), the
kinetic-to-velocity multiplier satisfies

\[
 \frac{1/4}{n^2+1/4}
 +\frac{n^2}{n^2+1/4}=1.
 \tag{3.5}
\]

The change \(x=2y\) preserves the normalized periodic mean, so (3.5)
proves the asserted \(L^2\) isometry.  The multipliers in (3.4) are of
orders \(-1\) and \(0\); hence

\[
 \|\mathcal Eh_\varepsilon\|_{H^3}
 \le C\|h_\varepsilon\|_{H^3}
 \le C\Lambda^2.
 \tag{3.6}
\]

The positive and negative \(K_z\) rows are orthogonal, so the real
conjugate-pair normalization preserves unit \(L^2\) norm.  Standard
elliptic bootstrapping of (3.1) also makes the selected vector smooth.

**Verdict: PASS.**

## 4. The \(H^3\) Riccati estimate

Let \(Y=\|w\|_{H^3}\).  The background satisfies

\[
 \|\overline U_\Lambda\|_{W^{4,\infty}}
 \le C\Lambda
 \tag{4.1}
\]

uniformly on the fixed window.  After applying derivatives of order at
most three, incompressibility cancels the highest background transport
term.  The commutators and \(w\cdot\nabla\overline U_\Lambda\) are bounded
by

\[
 C\Lambda Y^2.
 \tag{4.2}
\]

On \(\mathbb T^3\),

\[
 H^3\hookrightarrow W^{1,\infty},
 \tag{4.3}
\]

so the standard nonlinear transport estimate is bounded by \(CY^3\).
The Leray projector is harmless because it is an \(H^m\)-bounded
orthogonal multiplier commuting with derivatives.  Consequently

\[
 \frac12\frac d{dt}Y^2+\|\nabla w\|_{H^3}^2
 \le A\Lambda Y^2+BY^3
 \tag{4.4}
\]

and, by scalar comparison,

\[
 Y'\le a\Lambda Y+bY^2.
 \tag{4.5}
\]

The exact solution of the comparison equation is

\[
 Y(t)\le
 \frac{a\Lambda Y(0)e^{a\Lambda t}}
 {a\Lambda-bY(0)(e^{a\Lambda t}-1)}.
 \tag{4.6}
\]

If

\[
 Y(0)\le
 \rho_\Lambda
 =\frac{a\Lambda}{4b}e^{-a\Lambda T_D},
 \tag{4.7}
\]

then, for \(0\le t\le T_D\),

\[
 bY(0)(e^{a\Lambda t}-1)
 \le \frac{a\Lambda}{4},
 \tag{4.8}
\]

so the denominator in (4.6) is at least \(3a\Lambda/4\).  This gives

\[
 Y(t)\le\frac43e^{a\Lambda t}Y(0)
 <2e^{a\Lambda t}Y(0).
 \tag{4.9}
\]

The constants can be chosen independently of \(\Lambda\ge1\).

**Verdict: PASS.**

## 5. The all-mode remainder

Let \(z\) solve the complete linearized problem with \(z(0)=w(0)\), and
write \(r=w-z\).  Then

\[
 r_t=L_\Lambda(t)r
 -\mathbb P\nabla\cdot(w\otimes w),
 \qquad r(0)=0.
 \tag{5.1}
\]

This identity is formed in physical space before any Fourier-row
projection.  It therefore includes the \(K_z=0,\pm2\) modes created at
quadratic order and every later convolution.

The background transport cancels in the \(L^2\) identity, while

\[
 \left|\langle r\cdot\nabla\overline U_\Lambda,r\rangle\right|
 \le C\Lambda\|r\|_2^2.
 \tag{5.2}
\]

Integration by parts, incompressibility, and Young's inequality give

\[
 \begin{aligned}
 \left|\left\langle
 \mathbb P\nabla\cdot(w\otimes w),r
 \right\rangle\right|
 &=|\langle w\otimes w,\nabla r\rangle|\\
 &\le C\|w\|_\infty\|w\|_2\|\nabla r\|_2\\
 &\le\frac12\|\nabla r\|_2^2+CY^4.
 \end{aligned}
 \tag{5.3}
\]

Thus

\[
 \frac d{dt}\|r\|_2^2
 \le c\Lambda\|r\|_2^2+CY^4.
 \tag{5.4}
\]

Using (4.9),

\[
 \begin{aligned}
 \|r(T_D)\|_2^2
 &\le C\int_0^{T_D}
 e^{c\Lambda(T_D-s)}Y(s)^4\,ds\\
 &\le16CT_D
 e^{(c+4a)\Lambda T_D}Y(0)^4.
 \end{aligned}
 \tag{5.5}
\]

Taking the square root gives exactly

\[
 \|r(T_D)\|_2
 \le C_De^{M_D\Lambda}Y(0)^2,
 \tag{5.6}
\]

with

\[
 C_D=4(CT_D)^{1/2},
 \qquad
 M_D=\left(\frac c2+2a\right)T_D.
 \tag{5.7}
\]

No finite-row closure is used.

**Verdict: PASS.**

## 6. Seed ceiling and half-gain

For \(w(0)=\delta\phi_\Lambda\), the top-vector bound gives

\[
 Y(0)\le C_{\rm top}\Lambda^2\delta.
 \tag{6.1}
\]

The first term in the seed ceiling implies

\[
 C_{\rm top}\Lambda^2\delta
 \le\frac{a\Lambda}{4b}e^{-a\Lambda T_D}
 =\rho_\Lambda,
 \tag{6.2}
\]

so the Riccati bootstrap closes.

The remainder estimate gives

\[
 \|r(T_D)\|_2
 \le C_DC_{\rm top}^2\Lambda^4
 e^{M_D\Lambda}\delta^2.
 \tag{6.3}
\]

The second term in the seed ceiling implies

\[
 \begin{aligned}
 C_DC_{\rm top}^2\Lambda^4
 e^{M_D\Lambda}\delta
 &\le\frac1{2K_{\rm F}}
 e^{[M_D-(M_D-\kappa_D)_+]\Lambda}\\
 &\le\frac1{2K_{\rm F}}e^{\kappa_D\Lambda},
 \end{aligned}
 \tag{6.4}
\]

because

\[
 M_D-(M_D-\kappa_D)_+
 =\min\{M_D,\kappa_D\}\le\kappa_D.
 \tag{6.5}
\]

Therefore

\[
 \|r(T_D)\|_2
 \le\frac1{2K_{\rm F}}e^{\kappa_D\Lambda}\delta.
 \tag{6.6}
\]

R0.73F supplies, for every unit vector in the frozen top space,

\[
 \|z(T_D)\|_2
 \ge K_{\rm F}^{-1}e^{\kappa_D\Lambda}\delta.
 \tag{6.7}
\]

The reverse triangle inequality then yields

\[
 \|w(T_D)\|_2
 \ge\frac1{2K_{\rm F}}e^{\kappa_D\Lambda}\delta.
 \tag{6.8}
\]

Thus the stated seed ceiling really does retain one half of the certified
linear lower signal.  The positive-part exponent is also correct in both
cases \(M_D\ge\kappa_D\) and \(M_D<\kappa_D\).

This ceiling may be substantially smaller than
\(e^{-\kappa_D\Lambda}\); it proves relative gain, not order-one terminal
amplitude.

**Verdict: PASS.**

## 7. Double-row noncancellation

Write a positive physical row as

\[
 u_v(y,z)=\bigl(0,v(2y),2iv'(2y)\bigr)e^{iz}.
 \tag{7.1}
\]

Direct differentiation gives

\[
 (u_v\cdot\nabla)u_v
 =\left(0,0,
 4i\bigl(vv''-(v')^2\bigr)(2y)\right)e^{2iz}.
 \tag{7.2}
\]

For a field \((0,0,g(2y))e^{2iz}\), the Leray projection vanishes if and
only if the field is a gradient.  Its zero \(y\)-component forces the
potential to be independent of \(y\), so this occurs exactly when \(g\) is
constant.  Hence cancellation of the projected \(K_z=2\) forcing would
require

\[
 vv''-(v')^2=C.
 \tag{7.3}
\]

Differentiation gives

\[
 vv'''-v'v''=0.
 \tag{7.4}
\]

On an interval on which \(v\ne0\),

\[
 \left(\frac{v''}{v}\right)'=0.
 \tag{7.5}
\]

The frozen viscous eigenvalue equation is an elliptic fourth-order
ordinary differential equation with analytic coefficients and nonzero
leading coefficient \(\varepsilon\).  Its eigenfunctions are analytic.
Thus the local identity \(v''=cv\) extends around the circle.  Periodicity
then forces

\[
 v=Ae^{inx}+Be^{-inx}
 \tag{7.6}
\]

for an integer \(n\ge0\), including the constant case.

Such a nonzero \(v\) cannot solve the frozen wall-normal eigenvalue
equation

\[
 \sigma Lv
 =-\frac i2\bigl(WLv+W_{xx}v\bigr)
 -\varepsilon L^2v.
 \tag{7.7}
\]

Indeed, let \(W_2\ne0\) be the \(e^{2ix}\) coefficient of \(W(0,x)\).  If
\(A\ne0\), the \(n+2\) coefficient created by the two multiplication terms
on the right of (7.7) is, up to the common nonzero factor \(-i/2\),

\[
 W_2\left(n^2+\frac14-4\right)A
 =W_2\left(n^2-\frac{15}{4}\right)A.
 \tag{7.8}
\]

It is nonzero for every integer \(n\).  Neither \(\sigma Lv\) nor
\(-\varepsilon L^2v\) has an \(n+2\) coefficient.  For \(n\ge1\), the
\(Be^{-inx}\) term cannot contribute to that coefficient, so no
cancellation is possible.  If \(A=0\), the symmetric \(-(n+2)\)
coefficient generated from \(B\) gives the same contradiction.  When
\(n=0\), a nonzero constant directly generates nonzero \(\pm2\)
coefficients.  Therefore

\[
 \mathbb P\bigl[(u_v\cdot\nabla)u_v\bigr]\ne0.
 \tag{7.9}
\]

For the real pair \(u_v+\overline{u_v}\), the first quadratic convolution
has only \(K_z=0,+2,-2\).  It does not return to \(K_z=\pm1\) at quadratic
order.  The source correctly distinguishes these two facts: the double row
is genuinely generated, while feedback to the launching pair starts no
earlier than the next, cubic-order interaction.

**Verdict: PASS.**

## 8. Claim boundary and correction obligations

| Boundary proposition | Status after audit |
|---|---|
| The physical realization matches the R0.73F normalization | **PASS** |
| The constructed nonlinear orbit stays in a globally smooth planar class | **PASS** |
| The selected top vector has sufficient \(H^3\) cost \(O(\Lambda^2)\) | **PASS** |
| The explicit seed ceiling closes the fixed-window bootstrap | **PASS** |
| The full nonlinear solution retains at least half the R0.73F linear lower signal | **PASS** |
| The selected single row is a nonlinear invariant subsystem | **FALSE; the audited source correctly rejects it** |
| The selected row has nonzero quadratic leakage into the double row | **PASS** |
| The present estimates give order-one departure from a natural \(e^{-\kappa_D\Lambda}\) seed | **OPEN; the audited source explicitly leaves it open** |
| The result addresses general three-dimensional global regularity | **OPEN; the audited source explicitly disclaims such a conclusion** |

**Correction obligations:** none for the seven audited gates.

The FALSE and OPEN entries are boundary tests, not failed audit gates.  They
record why the proved theorem must remain labeled as a conditional nonlinear
relative-amplification result inside a planar barrier.
