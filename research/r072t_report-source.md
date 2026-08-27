# R0.72T report source: the exact \(A_2\) spacetime germ and its unresolved global model estimate

**Date:** 2026-08-28

**Status:** exact local normal form, unique four-term scaling, inviscid mixing
estimate, weighted bracket calculation, and drift-only calibration are proved.
The quantitative contraction for the full nonautonomous cubic model, transfer
back to the periodic heat path, and every nonlinear or Clay-level consequence
remain open.

**Keywords:** time-dependent shear, critical-point collision, enhanced
dissipation, heat polynomial, cubic phase, Hörmander bracket, bounded-chart
normal form

---

## 0. What this section decides

R0.72S located the symmetry-restricted collision

\[
 y_*=\log 2,
 \qquad \phi_*=\frac\pi2
 \tag{0.1}
\]

on the exact heat path.  The first purpose of R0.72T is to identify the PDE
seen at that collision without confusing the derivative of the shear with the
shear itself.

Put

\[
 d=y-y_*,\qquad x=\phi-\phi_*.
 \tag{0.2}
\]

The exact physical shear in these coordinates is

\[
 \boxed{
 W(d,x)=\frac12e^{-d}
 \left[-\sin x+\frac12e^{-3d}\sin 2x\right].}
 \tag{0.3}
\]

It satisfies

\[
 \boxed{W_d=W_{xx}.}
 \tag{0.4}
\]

I prove below that the first nonzero parabolic jet of \(W\) is the heat
polynomial

\[
 -\frac14H_3(d,x)=-\frac14(x^3+6dx),
 \tag{0.5}
\]

not a quadratic potential plus a function of time.  This gives one unique
four-term balance.  For coupling \(\varepsilon_c>0\), define

\[
 \kappa=\frac{\varepsilon_c}{4},\qquad
 X=\kappa^{1/5}x,\qquad S=\kappa^{2/5}d.
 \tag{0.6}
\]

On every fixed bounded \((S,X)\)-chart, the rescaled equation tends to

\[
 \boxed{
 u_S=u_{XX}+i\sigma H_3(S,X)u,
 \qquad H_3(S,X)=X^3+6SX,
 \qquad \sigma\in\{-1,1\}.}
 \tag{0.7}
\]

The calculations in this note do **not** prove a uniform \(L^2\) contraction
for (0.7).  The labels used in the release inventory are therefore

\[
 \boxed{
 \texttt{blockContraction=OPEN},\quad
 \texttt{periodicTransfer=OPEN},\quad
 \texttt{Clay=OPEN}.}
 \tag{0.8}
\]

This is a closed normal-form result and an explicit analytic barrier, not an
enhanced-dissipation theorem for the collision.

---

## 1. Exact heat-polynomial expansion

At \(d=0\), (0.3) becomes

\[
 W(0,x)=\frac12\left[-\sin x+\frac12\sin2x\right].
 \tag{1.1}
\]

For \(n\ge0\), define the heat polynomial

\[
 H_n(d,x):=e^{d\partial_x^2}x^n
 =n!\sum_{j=0}^{\lfloor n/2\rfloor}
 \frac{d^j x^{n-2j}}{j!(n-2j)!}.
 \tag{1.2}
\]

Then \(\partial_dH_n=\partial_x^2H_n\), and the entire Taylor series in
(1.1) evolves term by term under (0.4).  The resulting exact series is

\[
 W(d,x)=\sum_{j=1}^{\infty}
 \frac{(-1)^j(2^{2j}-1)}{2(2j+1)!}
 H_{2j+1}(d,x).
 \tag{1.3}
\]

The first three nonzero terms are

\[
 \boxed{
 W(d,x)=-\frac14H_3(d,x)
 +\frac1{16}H_5(d,x)
 -\frac1{160}H_7(d,x)+R_9(d,x),}
 \tag{1.4}
\]

where

\[
 H_3=x^3+6dx,
 \tag{1.5}
\]

\[
 H_5=x^5+20dx^3+60d^2x,
 \tag{1.6}
\]

\[
 H_7=x^7+42dx^5+420d^2x^3+840d^3x.
 \tag{1.7}
\]

Here \(R_9\) is the tail of the exact series (1.3), beginning at parabolic
weight nine when \(x\) has weight one and \(d\) has weight two.  In
particular, for every fixed \(R>0\), there is \(C_R<\infty\) such that

\[
 |R_9(d,x)|\le C_R
 (|x|+|d|^{1/2})^9
 \tag{1.8}
\]

whenever \(|x|+|d|^{1/2}\le R\) in a sufficiently small neighborhood of
the origin.  Equation (1.4) records both the variable placement and the
remainder location: every displayed \(H_j\) is evaluated at \((d,x)\), and
the remainder starts after \(H_7\).

Differentiating (1.4) gives the fold already detected in R0.72S:

\[
 W_x(d,x)=-\frac32d-\frac34x^2
 +O(d^2+|d|x^2+x^4).
 \tag{1.9}
\]

Thus the derivative germ is a fold, while its primitive is the spacetime
cubic \(x^3+6dx\).  Replacing the primitive by a quadratic changes the PDE
and its scale.

---

## 2. Unique four-term balance

The local Fourier-row equation, after removing scalar damping already
separated in the preceding sections, has the form

\[
 v_d=v_{xx}-i\sigma\varepsilon_c W(d,x)v.
 \tag{2.1}
\]

Use the general rescaling

\[
 X=\kappa^a x,\qquad S=\kappa^b d.
 \tag{2.2}
\]

The four leading weights in (2.1) are

\[
 \partial_d:\ \kappa^b,
 \qquad
 \partial_x^2:\ \kappa^{2a},
 \qquad
 \kappa x^3:\ \kappa^{1-3a},
 \qquad
 \kappa dx:\ \kappa^{1-a-b}.
 \tag{2.3}
\]

Requiring all four terms to survive gives

\[
 b=2a=1-3a=1-a-b.
 \tag{2.4}
\]

This linear system has the unique solution

\[
 \boxed{a=\frac15,\qquad b=\frac25.}
 \tag{2.5}
\]

Therefore (0.6) is not a guessed scaling.  It is the unique scaling that
retains the time derivative, diffusion, cubic spatial phase, and collision
drift at the same order.

Substituting (1.4) into (2.1), dividing by \(\kappa^{2/5}\), and using the
parabolic homogeneity of the heat polynomials gives

\[
 \begin{aligned}
 u_S={}&u_{XX}+i\sigma\Bigl[
 H_3(S,X)
 -\frac{\kappa^{-2/5}}4H_5(S,X)
 +\frac{\kappa^{-4/5}}{40}H_7(S,X)
 +\mathcal R_\kappa(S,X)
 \Bigr]u,
 \end{aligned}
 \tag{2.6}
\]

with, on every fixed bounded chart \(|S|+|X|\le R\),

\[
 \sup_{|S|+|X|\le R}|\mathcal R_\kappa(S,X)|
 \le C_R\kappa^{-6/5}.
 \tag{2.7}
\]

This is the precise bounded-chart statement behind (0.7).  It is not yet a
global-in-\(X\) perturbation theorem: the polynomial corrections grow at
infinity, and (2.7) alone cannot be inserted into a global semigroup bound.

---

## 3. Why scalar gauges and real translations do not freeze the model

A potential of the incorrect form

\[
 A(S)+bX^2
 \tag{3.1}
\]

loses all of its \(A(S)\) dependence under the scalar phase

\[
 u(S,X)=e^{i\sigma\int_0^S A(r)\,dr}\,z(S,X).
 \tag{3.2}
\]

If \(b=0\), the remaining evolution is the heat equation composed with a
unitary scalar phase, so there is no collision-driven \(L^2\) decay.  More
precisely, for
\[
 z_t+ik[A(t)+bx^2]z=\nu z_{xx},
 \tag{3.3}
\]
the function \(A(t)\) is removed completely by a scalar phase.  If \(b=0\),
the remaining \(L^2\) norm is that of the heat semigroup.  If \(b\ne0\), a
unitary dilation balances \(\nu\partial_x^2\) against \(ikbx^2\) and gives
the complex-harmonic-oscillator time scale
\[
 \boxed{T_{\rm quad}\asymp(\nu|kb|)^{-1/2}.}
 \tag{3.4}
\]
The semigroup theory for the non-self-adjoint harmonic oscillator is treated,
for example, by J. Viola
(<https://arxiv.org/abs/1512.02558>,
<https://doi.org/10.1007/s00020-016-2303-4>).  This calibration concerns the
incorrect quadratic model alone and says nothing about the combined
spacetime-cubic model (0.7).

For the correct model, let \(X=Y+c(S)\) with \(c(S)\in\mathbb R\).  Then

\[
 H_3(S,Y+c)=Y^3+3cY^2+(3c^2+6S)Y
 +(c^3+6Sc).
 \tag{3.5}
\]

A scalar gauge can remove only the last, \(Y\)-independent term.  Removing
the quadratic term forces \(c=0\), after which the coefficient \(6S\) of
\(Y\) remains.  A real translation plus a scalar gauge therefore cannot
turn (0.7) into a stationary cubic-potential equation.  A space-dependent
phase would also create a first-order differential term, so it is not a
scalar-gauge reduction of the same operator.

---

## 4. Exact inviscid propagator and a uniform mixing estimate

Discard diffusion in (0.7).  For \(S_1>S_0\), direct integration gives

\[
 \boxed{
 U_0(S_1,S_0)f(X)=
 \exp\!\left{i\sigma\left[
 (S_1-S_0)X^3+3(S_1^2-S_0^2)X
 \right]\right}f(X).}
 \tag{4.1}
\]

On the symmetric block \(S_0=-T/2\), \(S_1=T/2\), the accumulated
linear-in-\(X\) phase cancels exactly:

\[
 U_0(T/2,-T/2)f=e^{i\sigma TX^3}f.
 \tag{4.2}
\]

This is the symmetric-block cancellation used here.  It removes the
spacetime-linear contribution from the accumulated phase; it does not remove
the cubic phase.

The third derivative of the phase in (4.1) is

\[
 \partial_X^3\left[(S_1-S_0)X^3
 +3(S_1^2-S_0^2)X\right]=6(S_1-S_0),
 \tag{4.3}
\]

independent of the starting time.  The order-three van der Corput lemma,
applied by duality, therefore yields the uniform estimate

\[
 \boxed{
 \|U_0(S_0+T,S_0)f\|_{H^{-1}(\mathbb R)}
 \le C\min(1,T^{-1/3})
 \|f\|_{H^1(\mathbb R)}.}
 \tag{4.4}
\]

For completeness, take \(f,g\in C_c^\infty(\mathbb R)\) and put
\(a=f\overline g\).  A standard order-three van der Corput estimate gives

\[
 \left|\int_{\mathbb R}e^{i\Phi(X)}a(X)\,dX\right|
 \le C T^{-1/3}
 \bigl(\|a\|_\infty+\|a'\|_{L^1}\bigr).
 \tag{4.5}
\]

The one-dimensional Sobolev inequality and Cauchy--Schwarz bound the last
factor by \(C\|f\|_{H^1}\|g\|_{H^1}\).  The \(T\le1\) bound follows directly
from unitarity on \(L^2\).  Density and \(H^{-1}\)-\(H^1\) duality prove
(4.4).

Estimate (4.4) is genuine inviscid mixing.  It is not, by itself, the
required viscous block contraction.  In particular, the abstract theorem of
Coti Zelati--Delgadino--Elgindi converts a mixing power \(p\) into

\[
 q=\frac{2}{2+p}.
 \tag{4.6}
\]

Putting \(p=1/3\) gives \(q=6/7\), not the collision scale \(3/5\).  Their
method also uses a strictly positive operator with compact-resolvent Hilbert
scale, while the global line model in (0.7) has neither a Poincaré gap nor a
compact \(H^1(\mathbb R)\hookrightarrow L^2(\mathbb R)\) embedding.  Thus
(4.4) identifies a useful mechanism and an explicit method barrier, not a
shortcut to the desired estimate.

---

## 5. Weighted Hörmander bracket at the collision

Introduce an auxiliary periodic coordinate \(\theta\) and regard the fixed
\(\theta\)-Fourier mode of

\[
 \partial_SF-\partial_X^2F-H_3(S,X)\partial_\theta F=0.
 \tag{5.1}
\]

Set

\[
 X_1=\partial_X,
 \qquad
 X_0=\partial_S-H_3(S,X)\partial_\theta.
 \tag{5.2}
\]

Successive brackets are

\[
 [X_1,X_0]=-(3X^2+6S)\partial_\theta,
 \tag{5.3}
\]

\[
 [X_1,[X_1,X_0]]=-6X\partial_\theta,
 \tag{5.4}
\]

\[
 \boxed{
 [X_1,[X_1,[X_1,X_0]]]=-6\partial_\theta,
 \qquad
 [X_0,[X_1,X_0]]=-6\partial_\theta.}
 \tag{5.5}
\]

The second identity uses
\(X_0(3X^2+6S)=6\) and the fact that all coefficients are independent of
\(\theta\).  Assign parabolic weight two to \(X_0\) and weight one to
\(X_1\).  The missing direction appears by either of two weighted brackets:

\[
 \boxed{2+1+1+1=5,\qquad 2+(1+2)=5.}
 \tag{5.6}
\]

This calculation is consistent with the fifth-root scaling in (0.6).  The
qualitative bracket condition does not supply the quantitative, global
Poincaré/observability inequality needed for a semigroup contraction.  That
inequality is the next analytic target.

---

## 6. Characteristic action and the exact drift-only calibration

The linear spacetime part can be solved exactly.  Consider

\[
 z_t+i a(t-t_*)xz=\nu z_{xx},
 \qquad a\in\mathbb R.
 \tag{6.1}
\]

Fourier transformation in \(x\) turns (6.1) into transport along frequency
characteristics with viscous action

\[
 \nu\int_I \xi(t)^2\,dt.
 \tag{6.2}
\]

Let \(I=[m-T/2,m+T/2]\) after translating \(t_*=0\).  Optimization over the
incoming frequency gives the exact variance

\[
 \inf_{\xi_{\rm in}}\int_I\xi(t)^2\,dt
 =a^2\left(\frac{m^2T^3}{12}+\frac{T^5}{720}\right).
 \tag{6.3}
\]

Consequently the exact \(L^2\)-operator norm of the drift-only propagator is

\[
 \boxed{
 \|P_a(m+T/2,m-T/2)\|_{2\to2}
 =\exp\!\left[-\nu a^2
 \left(\frac{m^2T^3}{12}+\frac{T^5}{720}\right)\right].}
 \tag{6.4}
\]

The symmetric collision block \(m=0\) retains the sharp action

\[
 \boxed{\nu a^2T^5/720.}
 \tag{6.5}
\]

The same constant has a fixed-function magnetic-form identity.  For
\(r\in[-T/2,T/2]\), put

\[
 Q(r)=\frac a2\left(r^2-\frac{T^2}{12}\right),
 \qquad \int_{-T/2}^{T/2}Q(r)\,dr=0.
 \tag{6.6}
\]

For every \(f\in H^1(\mathbb R)\), expansion of the square and cancellation
of the time-mean cross term give

\[
 \boxed{
 \int_{-T/2}^{T/2}
 \|\bigl(\partial_x-iQ(r)\bigr)f\|_2^2\,dr
 =T\|f'\|_2^2+\frac{a^2T^5}{720}\|f\|_2^2.}
 \tag{6.7}
\]

For a block centered at \(m\), the centered magnetic shift is
\(a[mr+(r^2-T^2/12)/2]\), and the last coefficient becomes the quantity in
(6.3).

Equations (6.4)--(6.7) are an exact calibration.  They show that the
time-linear spatial drift alone acts on the fifth-root timescale.  They do
not prove the same norm identity after adding the cubic potential, because
the corresponding Fourier equation is no longer a first-order transport
equation.

For the physical heat path, write the leading velocity germ as
\[
 A\nu(t-t_*)x+Bx^3
 \tag{6.8}
\]
with \(A\ne0\), and take horizontal Fourier mode \(k\ne0\).  The drift-only
coefficient in (6.1) is then
\[
 a=kA\nu.
 \tag{6.9}
\]
The symmetric-block action \(\nu a^2T^5/720\) becomes order one when
\[
 \boxed{
 T\asymp |kA|^{-2/5}\nu^{-3/5}.}
 \tag{6.10}
\]
This recovers the physical \(3/5\) collision scale without treating the
cubic term as a perturbation.

There is also an exact fixed-function identity for the combined inviscid
potential
\[
 V(S,X)=aSX+bX^3.
 \tag{6.11}
\]
Center an interval of length \(T\) at \(S=c\), write local time
\(r\in[-T/2,T/2]\), and define the accumulated magnetic coefficient
\[
 A_r(X)=(ac+3bX^2)r+\frac a2r^2,\qquad
 A_{\rm av}=\frac{aT^2}{24},
 \tag{6.12}
\]
\[
 D_r=\partial_X-iA_r(X),\qquad
 D_{\rm av}=\partial_X-iA_{\rm av}.
 \tag{6.13}
\]
For every fixed \(f\in H^1(\mathbb R)\),
\[
 \boxed{
 \begin{aligned}
 \int_{-T/2}^{T/2}\|D_rf\|_2^2\,dr
 ={}&T\|D_{\rm av}f\|_2^2\\
 &+\int_{\mathbb R}\left[
 \frac{(ac+3bX^2)^2T^3}{12}
 +\frac{a^2T^5}{720}\right]|f(X)|^2\,dX.
 \end{aligned}}
 \tag{6.14}
\]
Indeed, \(A_r-A_{\rm av}\) is the sum of an odd linear function of \(r\)
and the centered even function
\(a(r^2-T^2/12)/2\); their cross term vanishes after time integration.
Equation (6.14) is persistent coercivity for one fixed \(f\).  An evolving
solution changes with \(r\), so (6.14) is **not** the missing observability
estimate and does not prove `blockContraction`.

---

## 7. What the present argument does not close

The next theorem cannot be claimed from the calculations above:

\[
 \|U(S_0+T,S_0)\|_{L^2(\mathbb R)\to L^2(\mathbb R)}
 \le \rho<1
 \tag{7.1}
\]

for one fixed \(T\), uniformly in \(S_0\), for the full model (0.7).  Three
specific gaps remain.

1. A global-in-\(X\), quantitative subelliptic Poincaré or observability
   inequality must turn the weighted bracket calculation into fixed-time
   \(L^2\) loss.
2. Time cutoffs and the unbounded polynomial potential must be controlled
   without assuming the solution is supported in a bounded chart.
3. The \(H_5,H_7,R_9\) terms must be transferred from bounded charts to the
   periodic equation with a uniform weighted remainder estimate.

One useful precise gate is the following cutoff subelliptic estimate, with a
constant independent of the interval center \(S_0\):
\[
 \|\chi u\|_{L^2_SL^2_X}
 \le C\left[
 \|\partial_X(\chi u)\|_{L^2_SL^2_X}
 +\|(\partial_S-i\sigma H_3)(\chi u)\|_{L^2_SH^{-1}_X}
 \right],
 \tag{7.2}
\]
for suitable unit-length time cutoffs \(\chi\), together with endpoint
control strong enough to imply the solution observability estimate
\[
 \|u(S_0)\|_2^2
 \le C\int_{S_0}^{S_0+T_0}\|\partial_Xu(S)\|_2^2\,dS
 \tag{7.3}
\]
for one fixed \(T_0\) and every start \(S_0\).  For solutions of (0.7), the
second term on the right of (7.2) is controlled in \(L^2_SH^{-1}_X\) by the
diffusive derivative, but the time cutoff, endpoints, and unbounded-\(X\)
tails must all be handled.

I record the minimal next target as R0.72U: prove (7.2)--(7.3) globally in
\(X\), uniformly for all start times, and then prove a tail/localization
transfer that absorbs the weighted \(H_5,H_7,R_9\) remainder in (2.6).
Until those parts are complete, neither `blockContraction` nor
`periodicTransfer` is closed.

Nothing in this note addresses the nonlinear vortex-stretching estimates
required for three-dimensional Navier--Stokes regularity.  The relation to
the Clay problem remains only the long-range motivation.
