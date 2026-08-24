# R0.70L independent internal audit

**Audit status:** PASS after correction and scope narrowing
**Date:** 2026-08-24
**Audited objects:** resolved-strain derivation, coupled correlation ledger,
periodic Fourier witness, pressure-blindness theorem, and route decision

This is an independent internal mathematical audit. It is not external peer
review.

## 1. Strain-source equation

Starting from

\[
 D_t^UU_i=-\partial_iP+\nu\Delta U_i-\partial_a\tau_{ia},
\]

the audit independently recovered

\[
 D_t^US
 =-(S^2)^\circ-(W^2)^\circ-(\nabla^2P)^\circ
 +\nu\Delta S-K_\tau^\circ,
\]

\[
 (K_\tau)_{ij}
 =\frac12(\partial_j\partial_a\tau_{ia}
          +\partial_i\partial_a\tau_{ja}),
\qquad
 (W^2)^\circ=\frac14(\Omega\otimes\Omega)^\circ.
\]

The pressure, vorticity, viscosity, and SGS signs and coefficients agree with
R0.70L. A random trace-free matrix check gave maximum residual
\(5.3\times10^{-15}\).

## 2. Coupled \(q\) ledger

The audit independently obtained

\[
\begin{aligned}
\dot q={}&
B:\Sigma^2+\frac23|\Sigma|_F^2-2q^2
-\frac14B:(\Omega_*\otimes\Omega_*)
-B:(\nabla^2P)_*^\circ\\
&+\nu B:(\Delta S)_*
-B:K_{\tau,*}^\circ
+\Sigma:\mathcal T_B(F_{\rm err}).
\end{aligned}
\]

The local quadratic has both signs. The examples in the report were checked
exactly. No pressure, cutoff, or SGS sign was assumed.

## 3. Periodic sign pair

For

\[
\psi_-=-\sin x\sin y+2(1-\cos x)(1-\cos2y),
\]

\[
\psi_+=-\sin x\sin y+2(1-\cos2x)(1-\cos y),
\]

\[
u_\pm=(-\psi_{\pm,y},
\psi_{\pm,x}+\sqrt{120}(\cos z-1),0),
\qquad \nu=1,
\]

an independent finite-Fourier computation verified:

\[
u_\pm(0)=0,\quad
\Sigma_\pm(0)=\operatorname{diag}(1,-1,0),\quad
\omega_\pm(0)=0,
\]

\[
Q_\pm=\operatorname{diag}(60,0,60),\quad
B_\pm=\operatorname{diag}(1/6,-1/3,1/6),\quad
q_\pm=1/2.
\]

The pressure Hessians are

\[
H^-=
\begin{pmatrix}
-301/85&-152/65&0\\
-152/65&131/85&0\\
0&0&0
\end{pmatrix},
\qquad
H^+=
\begin{pmatrix}
131/85&-152/65&0\\
-152/65&-301/85&0\\
0&0&0
\end{pmatrix}.
\]

The independently checked derivative table is

| term | minus | plus |
|---|---:|---:|
| local gradient | \(1/6\) | \(1/6\) |
| source viscosity | \(-1\) | \(-1\) |
| normalized covariance evolution | \(197/120\) | \(197/120\) |
| pressure | \(563/510\) | \(-733/510\) |

Therefore

\[
\dot q_-=\frac{3901}{2040}>0,\qquad
\dot q_+=-\frac{1283}{2040}<0.
\]

The common nonpressure subtotal is \(97/120\), and the entire derivative
difference equals the pressure difference \(216/85\). The two initial fields
also have the same kinetic energy.

## 4. Pressure-blindness theorem

The theorem passes under the following minimal assumptions:

- pointwise resolved-Lagrangian source
  \(\Sigma=S(U)(X(t),t)\);
- identity filter, or a compactly supported radial filter inside a strict
  core buffer;
- a cutoff whose instantaneous motion depends only on local velocity and the
  chosen trajectory;
- the support-separated exterior pressure-Hessian realization already
  certified in R0.70J.

The exterior packet changes the center pressure Hessian while leaving
\(\Sigma,B,X'(0),\dot\chi(0)\), and the pressure-free \(\dot B(0)\) fixed.
Thus

\[
\dot\Phi=C-D_\Sigma\Phi:H
\]

for every \(C^1\) instantaneous \(\Phi(\Sigma,B)\). Since
\(H\in\operatorname{Sym}_0(3)\) is arbitrary and scalable, a universal
one-sided sign forces \(D_\Sigma\Phi=0\) at every reachable core state.

## 5. Required claim boundaries

The theorem does not presently cover:

- noncompact Gaussian or strict Littlewood--Paley filters;
- a spatially averaged source;
- pressure-dependent cutoff acceleration;
- functionals containing pressure, SGS state, global energy, history, or
  neighboring scales;
- a sign restricted to one fixed quantitative energy ball;
- a claim of source-independence on an abstract state space without a
  reachability theorem.

The R0.70L report includes all six boundaries. The earlier, broader wording
“every local compensator” was narrowed to the precise \(C^1\)
instantaneous-source class above.

## 6. Surviving candidate

The audit also checked the history-dependent deformation pullback

\[
\dot G=\Sigma G,\qquad
\widehat Q=G^{-1}QG^{-\mathsf T},
\]

\[
\dot{\widehat Q}=G^{-1}F_{\rm err}G^{-\mathsf T}.
\]

It cancels constant-source stretching exactly and lies outside the local
pressure no-go. Its unresolved obstruction is the condition number

\[
\|G\|\,\|G^{-1}\|
\le
\exp\left(2\int\|\Sigma\|_{\rm op}\,dt\right).
\]

The audit agrees that this is the narrowest justified R0.70M gate.

## 7. Final assessment

R0.70L proves a structural initial-face obstruction for a specified class of
local source/shape Lyapunov candidates and supplies an exact matched-data
Navier--Stokes sign pair. It does not prove a regularity criterion, singular
behavior, global regularity, or a Millennium-problem result.
