# R0.73B kinetic shear-form proof

**Date:** 2026-08-29

**Status:** analytic pass after independent audit; deterministic certificate
and release gates pending.

## 1. Two-dimensional physical row

Use the normalized periodic inner product
\(\langle f,g\rangle_0=(2\pi)^{-1}\int\overline f g\), so
\(\|1\|_2=1\).

Take

\[
 \beta=\xi=0,
 \qquad \mu=\gamma^2>0,
 \qquad c=\gamma\Lambda,
 \qquad \mathcal L_\mu=-\partial_x^2+\mu.
 \tag{1.1}
\]

Let \(v=\mathcal L_\mu^{-1}q\).  The Orr--Sommerfeld equation is

\[
 \mathcal L_\mu v_d
 =-\mathcal L_\mu^2v
 -icW\mathcal L_\mu v-icW_{xx}v.
 \tag{1.2}
\]

Define the OS physical kinetic energy

\[
 E_\mu(v)=\frac1\mu\langle\mathcal L_\mu v,v\rangle
 =\|v\|_2^2+\mu^{-1}\|v_x\|_2^2.
 \tag{1.3}
\]

Taking the real inner product of (1.2) with \(v/\mu\), and integrating the
imaginary part of the active term by parts, gives

\[
 \boxed{
 \frac12E_\mu'(v)
 +\mu^{-1}\|\mathcal L_\mu v\|_2^2
 =\frac{c}{\mu}\operatorname{Im}
 \int_{\mathbb T}W_xv_x\overline v\,dx.}
 \tag{1.4}
\]

The sign in (1.4) follows the inner-product convention used in the R0.72Y
row.  Every conclusion below uses the absolute value, so it is invariant
under the opposite convention.

Since

\[
 \mu^{-1}\|\mathcal L_\mu v\|_2^2\ge\mu E_\mu(v),
 \tag{1.5}
\]

and

\[
 \|v_x\|_2\|v\|_2
 \le\frac{\sqrt\mu}{2}E_\mu(v),
 \tag{1.6}
\]

(1.4), \(c=\sqrt\mu\operatorname{sgn}(\gamma)\Lambda\), and Gronwall
recover the physical kinetic bound in the report.

## 2. Best relative shear coefficient

Define

\[
 \rho_\mu(d)=\frac1{\sqrt\mu}
 \sup_{v\ne0}
 \frac{\left|\operatorname{Im}
 \int W_xv_x\overline v\,dx\right|}{E_\mu(v)}.
 \tag{2.1}
\]

Then (1.4) gives the sharper logarithmic-norm estimate

\[
 \|U_{\rm OS}(d,s)\|_{\mathcal K_\mu\to\mathcal K_\mu}
 \le
 \exp\!\left[-\mu(d-s)+|\Lambda|
 \int_s^d\rho_\mu(\tau)\,d\tau\right].
 \tag{2.2}
\]

Equation (1.6) proves

\[
 \boxed{\rho_\mu(d)\le\frac12\|W_x(d)\|_\infty.}
 \tag{2.3}
\]

Let

\[
 S(d)=-i\left(W_x\partial_x+\frac12W_{xx}\right).
 \tag{2.4}
\]

Periodic integration by parts shows that \(S(d)\) is self-adjoint and that
its quadratic form is the signed expression in (2.1).  Therefore

\[
 \boxed{
 \rho_\mu(d)=\sqrt\mu\left\|
 \mathcal L_\mu^{-1/2}S(d)\mathcal L_\mu^{-1/2}
 \right\|_{2\to2}.}
 \tag{2.5}
\]

In the Fourier basis \(e^{inx}\),

\[
 \boxed{
 (T_\mu)_{kn}
 =\sqrt\mu\,
 \frac{(k+n)\widehat{W_x}(k-n)}
 {2\sqrt{(k^2+\mu)(n^2+\mu)}}.}
 \tag{2.6}
\]

It is Hermitian and banded to \(|k-n|\in\{1,2\}\).

## 3. Exact low-gap limit

For \(k,n\ne0\), each entry in (2.6) tends to zero as
\(\mu\downarrow0\).  More importantly, if \(Q_0\) denotes the nonzero-mode
projection, the mean-zero form estimate in Section 4 gives

\[
 \|Q_0T_\mu Q_0\|_{2\to2}
 \le \|W_x\|_\infty\sqrt{\frac\mu{1+\mu}}
 \longrightarrow0.
 \tag{3.1}
\]

For \(k\ne0,n=0\),

\[
 (T_\mu)_{k0}\longrightarrow
 \frac{\operatorname{sgn}(k)}2\widehat{W_x}(k).
 \tag{3.2}
\]

The transpose-conjugate entries have the corresponding limit.  Thus the
entrywise limit is the rank-two star operator

\[
 T_0=
 \begin{pmatrix}
 0&a^*\\
 a&0
 \end{pmatrix},
 \qquad
 a_k=\frac{\operatorname{sgn}(k)}2\widehat{W_x}(k),
 \quad k\ne0.
 \tag{3.3}
\]

For finite \(\mu\), the carrier column is

\[
 (a_\mu)_k=\frac{k}{2\sqrt{k^2+\mu}}\widehat{W_x}(k),
 \qquad k\ne0,
 \tag{3.4}
\]

and, with \(a=e^{-d}\), \(b=e^{-4d}\),

\[
 \|a_\mu\|_{\ell^2}^2
 =\frac{a^2}{32(1+\mu)}
 +\frac{b^2}{8(4+\mu)}.
 \tag{3.5}
\]

The carrier column has only the four entries \(\pm1,\pm2\), so
\(a_\mu\to a\) in \(\ell^2\), while (3.1) controls the complete infinite
mean-zero block.  Hence the convergence is in operator norm, not merely
entrywise.  Parseval gives

\[
 \|a\|_{\ell^2}=\frac12\|W_x\|_2,
 \qquad \|T_0\|=\|a\|_{\ell^2}.
 \tag{3.6}
\]

Hence

\[
 \boxed{
 \lim_{\mu\downarrow0}\rho_\mu(d)
 =\frac12\|W_x(d)\|_2
 =\frac{\sqrt{e^{-2d}+e^{-8d}}}{4\sqrt2}.}
 \tag{3.7}
\]

The limiting integrated logarithmic coefficient is

\[
 \boxed{
 \int_0^\infty\lim_{\mu\downarrow0}\rho_\mu(d)\,dd
 =\frac1{4\sqrt2}\int_0^1\sqrt{1+y^6}\,dy
 =0.188106027072\ldots.}
 \tag{3.8}
\]

This is smaller than the elementary all-row coefficient \(5/16=0.3125\).
It is an OS low-gap logarithmic-norm limit, not the exact maximum transient
gain of the nonautonomous propagator.  Since
\(\rho_\mu\le\|W_x\|_\infty/2\in L^1([0,\infty))\), dominated convergence
also justifies interchanging the low-gap limit and the time integral in
(3.8).

## 4. Explicit finite-\(\mu\) block bound

Write \(v=h+z\), \(\Pi_0z=0\), and normalize \(E_\mu(v)=1\).  The
constant--mean-zero cross form is bounded by

\[
 \frac12\|W_x\|_2\,2|h|
 \left(\mu^{-1}\|z_x\|_2^2+\|z\|_2^2\right)^{1/2}.
 \tag{4.1}
\]

On the mean-zero block, Poincare and (1.6) give the diagonal bound

\[
 \delta_\mu(d)=\sqrt{\frac\mu{1+\mu}}\|W_x(d)\|_\infty.
 \tag{4.2}
\]

Using the exact carrier-column norm in (3.5), the largest eigenvalue of the
resulting \(2\times2\) comparison matrix is

\[
 \frac12\left(
 \delta_\mu+\sqrt{\delta_\mu^2+4\|a_\mu\|_{\ell^2}^2}
 \right).
 \tag{4.3}
\]

Since \(2\|a_\mu\|_{\ell^2}\le\|W_x\|_2\), the following simpler relaxed
form is an explicit upper bound:

\[
 \boxed{
 \rho_\mu(d)\le
 \min\left\{
 \frac12\|W_x\|_\infty,
 \frac{\delta_\mu+
 \sqrt{\delta_\mu^2+\|W_x\|_2^2}}2
 \right\}.}
 \tag{4.4}
\]

The first term is better away from the low-gap regime; the second converges
to the exact limit (3.7).

## 5. Exact near-carrier instantaneous-growth witness

Fix one time \(d\), and put

\[
 a=e^{-d},\qquad b=e^{-4d},
 \tag{5.1}
\]

\[
 A=\|W_x\|_2^2=\frac{a^2+b^2}{8},
 \qquad
 D=A+\mu\|W\|_2^2,
 \tag{5.2}
\]

\[
 B=\|\mathcal L_\mu W\|_2^2
 =\frac{a^2(1+\mu)^2}{8}
 +\frac{b^2(4+\mu)^2}{32}.
 \tag{5.3}
\]

Assume \(\Lambda\ne0\), and let

\[
 \sigma=\operatorname{sgn}(\gamma),
 \qquad \tau=\operatorname{sgn}(\Lambda),
 \tag{5.4}
\]

and consider the real two-parameter carrier--tangent trial plane

\[
 u_1=0,
 \qquad
 v=h+i\sigma\tau\sqrt\mu\,\varepsilon W,
 \qquad
 u_3=-\tau\varepsilon W_x.
 \tag{5.5}
\]

Indeed \(v_x+i\gamma u_3=0\).  Its kinetic metric is

\[
 \|u\|_2^2=h^2+D\varepsilon^2.
 \tag{5.6}
\]

The viscous quadratic form is

\[
 \|u_x\|_2^2+\mu\|u\|_2^2
 =\mu h^2+B\varepsilon^2,
 \tag{5.7}
\]

and the shear-production cross term is \(|\Lambda|Ah\varepsilon\).
Consequently the largest instantaneous logarithmic growth on this plane is

\[
 \boxed{
 \lambda_{\rm trial}
 =-\frac12\left(\mu+\frac BD\right)
 +\frac12\sqrt{
 \left(\mu-\frac BD\right)^2
 +\frac{\Lambda^2A^2}{D}}.}
 \tag{5.8}
\]

It is positive exactly when

\[
 \boxed{\Lambda^2A^2>4\mu B.}
 \tag{5.9}
\]

For every fixed \(\Lambda\ne0\) and every fixed time, (5.9) holds for all
sufficiently small \(\mu\).  Thus prefactor-one physical kinetic
contraction is false even on the bounded-\(\Lambda\) physical path: the
positive norm derivative produces strict growth on a sufficiently short
future interval.  At finite \(\mu\), the nonzero vorticity direction is
\(\sqrt\mu\,\mathcal L_\mu W\); it is only asymptotic, up to sign, to
\(-\sqrt\mu W_{xx}\) as \(\mu\downarrow0\).  The dangerous direction is a
complex-phase carrier--tangent mixture, not the bare unscaled tangent line.
