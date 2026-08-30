# R0.73H derivation: exact quadratic leakage and cubic target return

**Date:** 2026-08-30  
**Coordinates:** \(x=2y\), profile time \(d=4t\), physical velocity
amplitude  
**Purpose:** fix every Leray factor and every ordered \(K_z\) path before
using finite Fourier diagnostics

## 1. Divergence-free row representation

Let \(D=\partial_x\).  For \(q\ne0\), a planar divergence-free row with
wall-normal profile \(f\) is

\[
 \mathbf u_q[f]
 =\left(0,f,\frac{2i}{q}Df\right)e^{iqz}.
 \tag{1.1}
\]

Indeed, \(\partial_y=2D\), so
\(\partial_yu_2+\partial_zu_3=2Df-2Df=0\).  Its physical kinetic norm is a
fixed multiple of

\[
 \|f\|_2^2+\frac4{q^2}\|Df\|_2^2.
 \tag{1.2}
\]

For an unprojected row

\[
 F_q=(0,A,C)e^{iqz},
 \tag{1.3}
\]

put

\[
 H_q=q^2-4D^2.
 \tag{1.4}
\]

Solving the scalar pressure equation gives the exact Leray formula

\[
 \boxed{
 \mathbb P F_q
 =\mathbf u_q\!\left[
 H_q^{-1}(q^2A+2iqDC)
 \right].}
 \tag{1.5}
\]

The inverse in (1.5) is unambiguous for \(q\ne0\).  The \(q=0\) row is
handled directly: its divergence-free, zero-mean part is a tangential
shear \((0,0,b(x))\).

Throughout this note,

\[
 \mathcal Q(f,g)=(f\cdot\nabla)g,
 \qquad
 \mathcal B(f,g)=-\frac14\mathbb P\mathcal Q(f,g).
 \tag{1.6}
\]

Thus the profile formulas below are first written for
\(\mathbb P\mathcal Q\); the slow-time Navier--Stokes forcing is always
\(-1/4\) times that profile.

## 2. Exact second-order rows

Take the positive carrier

\[
 u_+=\mathbf u_1[f]
 =(0,f,2iDf)e^{iz},
 \tag{2.1}
\]

and its real conjugate partner

\[
 u_-=\mathbf u_{-1}[\bar f].
 \tag{2.2}
\]

### 2.1 The doubled row

Direct differentiation gives

\[
 \mathcal Q(u_+,u_+)
 =\left(0,0,4i[fD^2f-(Df)^2]\right)e^{2iz}.
 \tag{2.3}
\]

Applying (1.5) with \(q=2\) gives

\[
 \boxed{
 \mathbb P\mathcal Q(u_+,u_+)
 =\mathbf u_2[\ell_2(f)],}
 \tag{2.4}
\]

where

\[
 \boxed{
 \ell_2(f)
 =-4D(1-D^2)^{-1}
 \bigl[fD^2f-(Df)^2\bigr].}
 \tag{2.5}
\]

The corresponding slow-time forcing profile in the \(b\) equation is
\(-\ell_2(f)/4\).

### 2.2 The mean row

The sum of the two ordered carrier--conjugate interactions is

\[
 \mathcal Q(u_+,u_-)+\mathcal Q(u_-,u_+)
 =\left(
 0,\,4D|f|^2,\,4i[\bar fD^2f-fD^2\bar f]
 \right).
 \tag{2.6}
\]

The wall-normal component is a derivative and is removed by the
\(q=0\) Leray projection.  Hence

\[
 \boxed{
 \mathbb P[
 \mathcal Q(u_+,u_-)+\mathcal Q(u_-,u_+)]
 =\left(0,0,4i[\bar fD^2f-fD^2\bar f]\right).}
 \tag{2.7}
\]

Its spatial mean is zero.  The row therefore evolves by the scalar heat
equation and causes no hidden constant mode.

Equations (2.4) and (2.7) prove the exact second-order support

\[
 K_z\in\{0,\pm2\}.
 \tag{2.8}
\]

## 3. Exact cubic return to \(K_z=1\)

At a fixed time, write the positive doubled-row coefficient as

\[
 u_2=\mathbf u_2[a]
 =(0,a,iDa)e^{2iz},
 \tag{3.1}
\]

and the mean coefficient as

\[
 u_0=(0,0,b(x)).
 \tag{3.2}
\]

Put \(g=\bar f\).  The complete unprojected positive target source is the
sum of the four ordered paths

\[
 (1,0),\quad(0,1),\quad(-1,2),\quad(2,-1).
 \tag{3.3}
\]

Its two nonzero components are

\[
 \begin{aligned}
 A_1={}&ibf+3gDa+6(Dg)a,\\
 C_1={}&2fDb-2bDf\\
 &+i\bigl[2gD^2a+2(Dg)(Da)-4aD^2g\bigr].
 \end{aligned}
 \tag{3.4}
\]

Therefore the Leray-projected wall-normal target profile is

\[
 \boxed{
 \mathfrak q_1(f,a,b)
 =(1-4D^2)^{-1}(A_1+2iDC_1).}
 \tag{3.5}
\]

The slow-time forcing in the \(c\) equation is
\(-\mathfrak q_1/4\).  Formula (3.5) contains both the mean-return and
double-return paths; either pair can be retained separately before their
sum is formed.

## 4. Exact cubic generation of \(K_z=3\)

The two ordered positive paths are \((1,2)\) and \((2,1)\).  Before Leray
projection they give

\[
 \begin{aligned}
 A_3={}&fDa-2(Df)a,\\
 C_3={}&i\bigl[2fD^2a+4aD^2f-6(Df)(Da)\bigr].
 \end{aligned}
 \tag{4.1}
\]

Hence

\[
 \boxed{
 \mathfrak q_3(f,a)
 =(9-4D^2)^{-1}(9A_3+6iDC_3),}
 \tag{4.2}
\]

and the slow-time forcing profile is \(-\mathfrak q_3/4\).

Together with the conjugate rows, (3.5) and (4.2) prove the cubic support

\[
 K_z\in\{\pm1,\pm3\}.
 \tag{4.3}
\]

## 5. Duhamel hierarchy and parity

Let \(S_q(d,s)\) be the exact linear evolution on the real row pair
\(K_z=\pm q\).  With \(a\) normalized by the exact endpoint gain, the
coefficient equations are equivalently

\[
 \begin{aligned}
 b(d)&=\int_0^dS_{\{0,2\}}(d,s)
 \mathcal B(a(s),a(s))\,ds,\\
 c(d)&=\int_0^dS_{\{1,3\}}(d,s)
 [\mathcal B(a(s),b(s))+\mathcal B(b(s),a(s))],ds.
 \end{aligned}
 \tag{5.1}
\]

For a launch-amplitude expansion

\[
 u(d;\rho)=\sum_{j\ge1}\rho^ju^{(j)}(d),
 \tag{5.2}
\]

Fourier-label addition proves by induction

\[
 \operatorname{supp}_{K_z}u^{(j)}
 \subset\{-j,-j+2,\ldots,j-2,j\}.
 \tag{5.3}
\]

Thus odd orders contain only odd \(K_z\), and even orders contain only
even \(K_z\).  In particular, the target \(K_z=\pm1\) has no quadratic or
quartic term.  Its first nonlinear correction is cubic and the next
possible correction is quintic.

The amplitude \(\rho\) in (5.2) must not be denoted by
\(\varepsilon\), because \(\varepsilon_\nu=\Lambda^{-1}\) already denotes
the singular viscosity parameter in fast time.

## 6. Independent algebra contract

The formal finite diagnostic must evaluate every retained source in two
independent ways:

1. the one-dimensional formulas (2.5), (2.7), (3.5), and (4.2);
2. generic physical-velocity Fourier convolution for
   \(\mathbb P\mathcal Q(u,v)\),
   \[
   i\mathbb P_k\sum_{\ell+m=k}
   (\widehat u(\ell)\cdot m)\widehat v(m),
   \tag{6.1}
   \]
   followed by row extraction.  Here \(m\) is the physical wavevector
   \((2m_x,m_z)\) associated with the normalized Fourier label
   \((m_x,m_z)\).  The slow-time bilinear forcing \(\mathcal B\) is
   \(-1/4\) times (6.1).

An alias-free physical-grid FFT implementation provides a third, independent
sentinel check.  Passing these finite comparisons validates the code path
and the displayed identities at the chosen cutoffs.  It does not prove a
continuum semigroup estimate, a Fourier-tail enclosure, a uniform Taylor
radius, or a three-dimensional result.
