# R0.70M — Pullback by the strain-only propagator, noncommutative holonomy, and the affine-rank boundary

**Status:** internal canonical research report; not a public theorem chapter
**Release:** R0.70M
**Date:** 2026-08-24

## 1. Result in one page

R0.70L left one exact history-dependent construction open. If the localized
filtered-vorticity covariance satisfies

\[
 \dot Q=\Sigma Q+Q\Sigma+F,
 \qquad \Sigma\in\operatorname{Sym}_0(3),
 \tag{1.1}
\]

and

\[
 \dot G=\Sigma G,
 \qquad G(t_0)=I,
 \tag{1.2}
\]

then the pullback by the strain-only propagator

\[
 \widehat Q=G^{-1}QG^{-\mathsf T}
 \tag{1.3}
\]

obeys

\[
 \boxed{\dot{\widehat Q}=G^{-1}FG^{-\mathsf T}.}
 \tag{1.4}
\]

The constant resolved strain has disappeared from (1.4). R0.70M determines
exactly what this cancellation does and does not buy.

The terminology needs one strict boundary. The matrix \(G\) in (1.2) is a
**strain-only propagator**. It is not the physical deformation gradient of the
flow map, which solves

\[
 \dot D=(\Sigma+W)D
 \tag{1.4a}
\]

with the full velocity gradient. “Pullback” below always refers to the
auxiliary propagator (1.2), not to a Cauchy formula for the physical flow map.

First, for

\[
 \widehat E=\operatorname{tr}\widehat Q,
 \qquad
 \widehat R=\frac{\widehat Q}{\widehat E},
 \qquad
 \widehat B=\widehat R-\frac13I,
 \tag{1.5}
\]

there is a condition-number-free estimate only in the already pulled metric:

\[
 \boxed{
 |\widehat B(t)-\widehat B(s)|_F
 \le(1+\sqrt2)\int_s^t\rho_G(r)\,dr,}
 \tag{1.6}
\]

where

\[
 \rho_G
 =\inf_{\lambda\in\mathbb R}
 \frac{
 |G^{-1}(F-\lambda Q)G^{-\mathsf T}|_F
 }{
 \operatorname{tr}(G^{-1}QG^{-\mathsf T})
 }.
 \tag{1.7}
\]

If the residual is first measured in the original Euclidean frame,

\[
 \rho_0
 =\inf_{\lambda\in\mathbb R}
 \frac{|F-\lambda Q|_F}{\operatorname{tr}Q},
 \tag{1.8}
\]

then

\[
 \boxed{\rho_G\le\kappa_2(G)^2\rho_0.}
 \tag{1.9}
\]

The exponent two is sharp. For

\[
 G_k=\operatorname{diag}(k,k^{-1},1),
 \quad
 Q_\varepsilon=\operatorname{diag}(1,\varepsilon,\varepsilon),
 \quad
 F=e_2\otimes e_2,
 \tag{1.10}
\]

the amplification of \(|F|_F/\operatorname{tr}Q\) is

\[
 \frac{k^4(1+2\varepsilon)}
 {1+\varepsilon(k^4+k^2)}
 \longrightarrow k^4=\kappa_2(G_k)^2.
\tag{1.11}
\]

The same sharp limit holds after both frames optimize over the scalar
amplitude subtraction in (1.7)--(1.8):

\[
 \lim_{\varepsilon\downarrow0}
 \frac{\rho_G}{\rho_0}
 =k^4=\kappa_2(G_k)^2.
 \tag{1.11a}
\]

Second, signed cancellation of the strain history does not control the
time-ordered exponential. Let

\[
 A=(\log3)
 \begin{pmatrix}1&0\\0&-1\end{pmatrix},
 \qquad
 C=(\log3)
 \begin{pmatrix}0&1\\1&0\end{pmatrix}.
 \tag{1.12}
\]

Apply the four strains \(A,C,-A,-C\) in chronological order, using either
piecewise-constant unit intervals or disjoint smooth unit-mass pulses. Then

\[
 \int\Sigma(t)\,dt=0,
 \qquad F\equiv0,
 \tag{1.13}
\]

but

\[
 G_*=e^{-C}e^{-A}e^Ce^A
 =
 \begin{pmatrix}
 -119/9&-160/81\\
 160/9&209/81
 \end{pmatrix},
 \tag{1.14}
\]

with

\[
 \det G_*=1,
 \qquad
 \operatorname{tr}G_*=-\frac{862}{81}<-2.
 \tag{1.15}
\]

Thus the monodromy is hyperbolic even though the signed matrix integral is
zero. With \(Q_0=I\) and \(F=0\), the pullback remains exactly

\[
 \widehat Q(t)=I,
 \tag{1.16}
\]

while the physical covariance after one loop is

\[
 Q_*=G_*G_*^{\mathsf T}
 =\frac1{6561}
 \begin{pmatrix}
 1172641&-1575680\\
 -1575680&2117281
 \end{pmatrix}.
 \tag{1.17}
\]

After embedding this block in three dimensions,

\[
 \operatorname{tr}B_*^2
 =\frac{6553600}{9889449}
 =\frac23-\frac{13122}{3296483}.
 \tag{1.18}
\]

One zero-integral, zero-residual loop therefore drives the physical
covariance close to the rank-one anisotropy boundary while the pulled
covariance does not move.

Third, there is a genuine condition-number-free formulation on the positive
definite cone. If \(Q\succ0\), put

\[
 \mathfrak a(Q,F)^2
 =\operatorname{tr}[(Q^{-1}F)^2]
 -\frac13[\operatorname{tr}(Q^{-1}F)]^2.
 \tag{1.19}
\]

For the determinant-one pulled shape

\[
 \widehat{\mathcal C}
 =(\det\widehat Q)^{-1/3}\widehat Q,
 \tag{1.20}
\]

the affine-invariant speed is exactly

\[
 \boxed{
 |\dot{\widehat{\mathcal C}}|_{\widehat{\mathcal C}}
 =\mathfrak a(Q,F),}
 \tag{1.21}
\]

and hence

\[
 d_{\rm AI}
 (\widehat{\mathcal C}(s),\widehat{\mathcal C}(t))
 \le\int_s^t\mathfrak a(Q,F)\,dr.
 \tag{1.22}
\]

No \(G\) or \(\kappa_2(G)\) appears in (1.21)--(1.22). This is an application
of standard affine-invariant geometry of symmetric positive-definite
matrices, not a claim that the metric itself is new.

The boundary is decisive. The exact periodic shear

\[
 u(x,t)=A_0e^{-\nu N^2t}\sin(Ny)e_1
 \tag{1.23}
\]

is a smooth unforced periodic Navier--Stokes solution, but its filtered
vorticity is everywhere parallel to \(e_3\). Every nonzero weighted
covariance \(Q\) therefore has rank one. The inverse in (1.19) is undefined.
Adding \(\varepsilon E I\) does not repair the route uniformly: its effective
residual contains

\[
 -2\varepsilon E\Sigma,
 \tag{1.24}
\]

whose relative size remains order one in the null eigenspace as
\(\varepsilon\downarrow0\).

The conclusion is narrow but firm:

> Pullback by the strain-only propagator is an exact coordinate cancellation, not an
> energy-controlled regularity mechanism. In Euclidean normalized variables
> it pays a sharp \(\kappa_2(G)^2\) factor. Affine-relative geometry removes the
> factor only when \(Q\) is positive definite, a hypothesis violated by
> elementary smooth periodic NSE solutions. Any continuation of this route
> must prove a scale-frame coercivity estimate before taking an inverse or
> returning to the physical metric.

This release does not prove a Leray-to-critical estimate, a regularity
criterion stronger than existing strain criteria, finite-time blow-up,
global smoothness, or the Millennium problem.

## 2. Conventions

Let \(u\) be a smooth incompressible Navier--Stokes solution on the time
interval under consideration. As in R0.70K, let \(U=\varphi_\ell*u\),
\(\Omega=\nabla\times U\), and let \(0\le\chi\in C_c^\infty\). Define

\[
 Q(t)=\int\chi(x,t)\Omega(x,t)\otimes\Omega(x,t)\,dx,
 \qquad E=\operatorname{tr}Q>0.
 \tag{2.1}
\]

The exact R0.70K decomposition is

\[
 S(U)=\Sigma(t)+\widetilde S(x,t),
 \tag{2.2}
\]

\[
 \dot Q=\Sigma Q+Q\Sigma+F_{\rm err},
 \tag{2.3}
\]

where

\[
 F_{\rm err}
 =F_\chi+F_{\widetilde S}+F_\nu+F_C.
 \tag{2.4}
\]

The source \(\Sigma\) is spatially constant on the covariance ledger. It may
be a pointwise resolved strain along a chosen path, an exterior source, or an
exact add-and-subtract reference. Every theorem below is an ODE consequence
of (2.3); PDE claims are made only where the four residuals are explicitly
identified.

For matrices,

\[
 X:Y=\operatorname{tr}(X^{\mathsf T}Y),
 \qquad |X|_F^2=X:X,
 \qquad \kappa_2(G)=\|G\|_{\rm op}\|G^{-1}\|_{\rm op}.
 \tag{2.5}
\]

All strain-propagator matrices begin at \(G(t_0)=I\). Since
\(\operatorname{tr}\Sigma=0\),

\[
 \det G(t)=1.
 \tag{2.6}
\]

This determinant identity follows from the auxiliary trace-free generator.
It must not be identified with the full Eulerian--Lagrangian deformation
gradient. In the inviscid physical flow map, the latter evolves with
\(\nabla U=\Sigma+W\); in viscous Eulerian--Lagrangian formulations additional
diffusive commutators also appear.

## 3. Exact pullback ledger

For brevity, set \(F:=F_{\rm err}\) and \(M:=G^{-1}\). Then

\[
 \dot M=-M\Sigma.
 \tag{3.1}
\]

Differentiating \(\widehat Q=MQM^{\mathsf T}\) and using (2.3) gives

\[
\begin{aligned}
 \dot{\widehat Q}
 &=-M\Sigma QM^{\mathsf T}
   +M(\Sigma Q+Q\Sigma+F)M^{\mathsf T}
   -MQ\Sigma M^{\mathsf T}\\
 &=MFM^{\mathsf T}=:\widehat F.
\end{aligned}
\tag{3.2}
\]

The integrated identity is

\[
 \boxed{
 Q(t)=G(t)
 \left[Q(t_0)+\int_{t_0}^t
 G(r)^{-1}F(r)G(r)^{-\mathsf T}\,dr\right]
 G(t)^{\mathsf T}.}
 \tag{3.3}
\]

For the normalized variables (1.5),

\[
 \dot{\widehat E}=\operatorname{tr}\widehat F,
 \tag{3.4}
\]

\[
 \dot{\widehat R}
 =\frac{\widehat F
 -\widehat R\operatorname{tr}\widehat F}{\widehat E},
 \tag{3.5}
\]

\[
 \boxed{
 \dot{\widehat B}
 =\frac{\operatorname{dev}\widehat F
 -\widehat B\operatorname{tr}\widehat F}{\widehat E}.}
 \tag{3.6}
\]

Consequently,

\[
 \frac12\frac d{dt}|\widehat B|_F^2
 =\frac{
 \widehat B:\widehat F
 -|\widehat B|_F^2\operatorname{tr}\widehat F
 }{\widehat E}.
 \tag{3.7}
\]

Congruence preserves positive semidefiniteness. Hence

\[
 -\frac13\le\lambda_i(\widehat B)\le\frac23,
 \qquad
 |\widehat B|_F^2\le\frac23.
 \tag{3.8}
\]

It does not cure the denominator:

\[
 \widehat E=0\quad\Longleftrightarrow\quad E=0.
 \tag{3.9}
\]

## 4. The exact pulled-shape BV estimate

Equation (3.6) is unchanged if a scalar multiple of \(\widehat Q\) is
subtracted from \(\widehat F\). Indeed, for any \(\lambda\in\mathbb R\),

\[
 \mathcal T_{\widehat B}
 (\widehat F-\lambda\widehat Q)
 =\mathcal T_{\widehat B}(\widehat F).
 \tag{4.1}
\]

For any symmetric \(X\),

\[
 |\operatorname{dev}X
 -\widehat B\operatorname{tr}X|_F
 \le(1+\sqrt2)|X|_F,
 \tag{4.2}
\]

because \(|\widehat B|_F\le\sqrt{2/3}\) and
\(|\operatorname{tr}X|\le\sqrt3|X|_F\). Equations (4.1)--(4.2) prove
(1.6).

This is a genuine conditionally closed statement:

> If \(\rho_G\in L^1(t_0,T)\), then \(\widehat B\) has bounded variation on
> \([t_0,T]\), and it has a terminal limit whenever \(T<\infty\).

No Grönwall factor has been inserted. The unresolved point is whether the
NSE residual controls \(\rho_G\) from energy-level information.

## 5. Returning to the Euclidean frame: a sharp square loss

For \(X=F-\lambda Q\),

\[
 |MXM^{\mathsf T}|_F
 \le\|M\|_{\rm op}^2|X|_F,
 \tag{5.1}
\]

whereas

\[
 \widehat E
 =\operatorname{tr}(MQM^{\mathsf T})
 \ge\|G\|_{\rm op}^{-2}E.
 \tag{5.2}
\]

Taking the infimum over \(\lambda\) proves (1.9).

For symmetric \(\Sigma\), define the accumulated spectral spread

\[
 \Gamma(t)
 =\int_{t_0}^t
 \left[
 \lambda_{\max}(\Sigma(r))
 -\lambda_{\min}(\Sigma(r))
 \right]dr.
 \tag{5.3}
\]

The extremal singular-value inequalities give

\[
 \|G(t)\|_{\rm op}
 \le\exp\int_{t_0}^t\lambda_{\max}(\Sigma(r))\,dr,
 \tag{5.4}
\]

\[
 \|G(t)^{-1}\|_{\rm op}
 \le\exp\int_{t_0}^t-\lambda_{\min}(\Sigma(r))\,dr,
 \tag{5.5}
\]

and therefore

\[
 \boxed{\kappa_2(G(t))\le e^{\Gamma(t)}.}
 \tag{5.6}
\]

Combining (1.6), (1.9), and (5.6),

\[
 \boxed{
 |\widehat B(t)-\widehat B(s)|_F
 \le(1+\sqrt2)
 \int_s^t e^{2\Gamma(r)}\rho_0(r)\,dr.}
 \tag{5.7}
\]

The diagonal family (1.10) proves that neither the square on \(\kappa\) nor
the exponent \(2\Gamma\) can be removed for a general symmetric residual.
For

\[
 \Sigma=\operatorname{diag}(a,-a,0),
 \qquad G(T)=\operatorname{diag}(e^{aT},e^{-aT},1),
 \tag{5.8}
\]

one has

\[
 \kappa_2(G)=e^{2aT}=e^\Gamma.
 \tag{5.9}
\]

At a rank-one limiting state \(Q=e_1\otimes e_1\), with
\(F=e_2\otimes e_2\),

\[
 \frac{|\dot{\widehat B}|_F}{|F|_F/E}
 =\sqrt2e^{4aT}
 =\sqrt2\kappa_2(G)^2.
 \tag{5.10}
\]

The positive-definite family (1.10) gives the same sharpness by a limit and
avoids using a singular \(Q\) inside the proof. Exact least-squares
minimization over \(\lambda\) verifies (1.11a), so the sharpness is for the
actual quotient \(\rho_G/\rho_0\), not only for an unoptimized residual norm.

## 6. Zero-integral strain holonomy

### Theorem 6.1

There exists a smooth compactly time-supported path

\[
 \Sigma:\mathbb R\to\operatorname{Sym}_0(2)
 \tag{6.1}
\]

such that

\[
 \int_{\mathbb R}\Sigma(t)\,dt=0,
 \tag{6.2}
\]

but the solution of \(\dot G=\Sigma G\), \(G(-\infty)=I\), has the
hyperbolic terminal value (1.14).

### Proof

Choose four nonnegative functions

\[
 \phi_j\in C_c^\infty(I_j),
 \qquad \int\phi_j=1,
 \tag{6.3}
\]

with strictly ordered, disjoint intervals

\[
 I_1<I_2<I_3<I_4.
 \tag{6.4}
\]

Set

\[
 \Sigma(t)=\phi_1(t)A+\phi_2(t)C
 -\phi_3(t)A-\phi_4(t)C.
 \tag{6.5}
\]

Equation (6.2) is immediate. On each support only one fixed generator is
active, so its ordered exponential depends only on the pulse mass. Thus

\[
 G(+\infty)=e^{-C}e^{-A}e^Ce^A.
 \tag{6.6}
\]

Since

\[
 e^A=
 \begin{pmatrix}3&0\\0&1/3\end{pmatrix},
 \qquad
 e^C=
 \begin{pmatrix}5/3&4/3\\4/3&5/3\end{pmatrix},
 \tag{6.7}
\]

direct multiplication gives (1.14). Its characteristic roots are

\[
 \frac{-431\pm160\sqrt7}{81},
 \tag{6.8}
\]

one of which has modulus greater than one. This proves hyperbolicity.

The terminal matrix is also strongly non-normal:

\[
 G_*^{\mathsf T}G_*-G_*G_*^{\mathsf T}
 =\frac{2048000}{6561}
 \begin{pmatrix}1&1\\1&-1\end{pmatrix}.
 \tag{6.9}
\]

This is a time-ordering effect, not a signed-integral effect. Repeating the
loop produces exponential physical stretching while

\[
 \int_{\text{each loop}}\Sigma=0.
 \tag{6.10}
\]

The theorem is a matrix-ODE statement. Each generator, embedded in three
dimensions, is separately realizable as the strain at the origin of a smooth
periodic divergence-free field. For example,

\[
 u_A=a(\sin x\cos y,-\cos x\sin y,0),
 \tag{6.11}
\]

and

\[
 u_C=a(\sin y,\sin x,0).
 \tag{6.12}
\]

The prescribed four-stage history has not been embedded in one unforced
finite-energy periodic NSE trajectory. It is exact for a forced realization,
but R0.70M does not use that fact as an unforced NSE theorem.

## 7. The stretching has moved into the metric

Define the evolving material metric

\[
 \mathcal G=G^{\mathsf T}G.
 \tag{7.1}
\]

Then

\[
 Q=G\widehat QG^{\mathsf T},
 \qquad
 E=\mathcal G:\widehat Q,
 \tag{7.2}
\]

and

\[
 \dot{\mathcal G}=2G^{\mathsf T}\Sigma G.
 \tag{7.3}
\]

Consequently,

\[
 \boxed{
 \dot{\mathcal G}:\widehat Q
 =2\Sigma:Q=2E\,q.}
 \tag{7.4}
\]

Thus (1.4) does not destroy vortex stretching. It transfers the complete
constant-source work into the metric with which \(\widehat Q\) is read.

There is a particularly transparent hidden-deformation example. Let

\[
 \Sigma=\operatorname{diag}(a,-a,0),
 \qquad F=0,
 \qquad Q=e_3\otimes e_3.
 \tag{7.5}
\]

Then

\[
 q=0,
 \qquad
 \operatorname{tr}[R(\Sigma-qI)^2]=0,
 \tag{7.6}
\]

and \(Q,B,\widehat B\) all remain constant, while

\[
 \kappa_2(G(t))=e^{2at}.
 \tag{7.7}
\]

Therefore no universal function of

\[
 E,\quad B,\quad q,\quad
 \operatorname{tr}[R(\Sigma-qI)^2]
 \tag{7.8}
\]

can control the propagator condition number. The R0.70K shape variables do
not observe metric stretching in covariance-null directions.

## 8. The affine-relative SPD theorem

Assume now \(Q\succ0\). Jacobi's formula and (2.3) give

\[
\begin{aligned}
 \frac d{dt}\log\det Q
 &=\operatorname{tr}
 \left[Q^{-1}(\Sigma Q+Q\Sigma+F)\right]\\
 &=2\operatorname{tr}\Sigma+\operatorname{tr}(Q^{-1}F)\\
 &=\boxed{\operatorname{tr}(Q^{-1}F)}.
\end{aligned}
\tag{8.1}
\]

Thus incompressible constant-source stretching preserves the covariance
determinant. It can still increase the trace without bound by making the
covariance anisotropic.

Normalize the pulled covariance by determinant:

\[
 \widehat{\mathcal C}
 =(\det\widehat Q)^{-1/3}\widehat Q,
 \qquad \det\widehat{\mathcal C}=1.
 \tag{8.2}
\]

The affine-invariant metric on the SPD cone is

\[
 |X|_P
 =|P^{-1/2}XP^{-1/2}|_F.
 \tag{8.3}
\]

Using \(\dot{\widehat Q}=\widehat F\),

\[
 |\dot{\widehat{\mathcal C}}|_{\widehat{\mathcal C}}^2
 =\operatorname{tr}[(\widehat Q^{-1}\widehat F)^2]
 -\frac13[\operatorname{tr}(\widehat Q^{-1}\widehat F)]^2.
 \tag{8.4}
\]

But

\[
 \widehat Q^{-1}\widehat F
 =G^{\mathsf T}Q^{-1}FG^{-\mathsf T},
 \tag{8.5}
\]

which is similar to \(Q^{-1}F\). The two traces in (8.4) are therefore
similarity invariants, proving (1.21).

For the standard affine-invariant distance

\[
 d_{\rm AI}(P_0,P_1)
 =\left|
 \log(P_0^{-1/2}P_1P_0^{-1/2})
 \right|_F,
 \tag{8.6}
\]

the distance is bounded by curve length. This proves (1.22).

The theorem identifies the only direct way to remove \(\kappa_2(G)\): measure
the residual relative to the current covariance itself. It does not provide
an NSE estimate for

\[
 Q^{-1/2}FQ^{-1/2}.
 \tag{8.7}
\]

That relative residual can diverge when the smallest covariance eigenvalue
approaches zero, even if \(|F|_F/E\) is small.

## 9. Rank defect and non-uniform regularization

The SPD hypothesis is not a harmless technical restriction. Take the exact
periodic shear (1.23). It satisfies

\[
 \partial_tu=\nu\Delta u,
 \qquad
 (u\cdot\nabla)u=0,
 \qquad p=0,
 \tag{9.1}
\]

and

\[
 \omega
 =-A_0Ne^{-\nu N^2t}\cos(Ny)e_3.
 \tag{9.2}
\]

A translation-invariant scalar filter changes only the mode amplitude, not
its direction. Hence for every nonnegative cutoff,

\[
 Q=E\,(e_3\otimes e_3)
 \tag{9.3}
\]

whenever the filtered mode is not annihilated and the cutoff contains
nonzero vorticity. Thus

\[
 \operatorname{rank}Q=1,
 \qquad \det Q=0.
 \tag{9.4}
\]

The affine-relative diagnostic is undefined on this smooth solution.

Consider the natural isotropic regularization

\[
 Q_\varepsilon=Q+\varepsilon E I.
 \tag{9.5}
\]

Since

\[
 Q_\varepsilon'
 =\Sigma Q_\varepsilon+Q_\varepsilon\Sigma
 +F_\varepsilon,
 \tag{9.6}
\]

its effective residual is

\[
 \boxed{
 F_\varepsilon
 =F+\varepsilon\dot E I-2\varepsilon E\Sigma.}
 \tag{9.7}
\]

The last term is the source that the unregularized pullback had removed.
It is not small in the relative metric near a null eigenspace. For the exact
matrix state

\[
 Q=e_3\otimes e_3,
 \qquad
 \Sigma=
 \begin{pmatrix}0&1&0\\1&0&0\\0&0&0\end{pmatrix},
 \qquad F=0,
 \tag{9.8}
\]

one has \(\Sigma Q+Q\Sigma=0\), but

\[
 \operatorname{tr}
 \left[
 (Q_\varepsilon^{-1}(-2\varepsilon\Sigma))^2
 \right]=8
 \tag{9.9}
\]

for every \(\varepsilon>0\). The regularization error has no vanishing
\(\varepsilon\downarrow0\) limit in the affine-relative shape speed.

## 10. Pulled form of the complete NSE residual

Because \(M(t)=G(t)^{-1}\) is spatially constant, define

\[
 \widehat\Omega=M\Omega,
 \qquad
 \widehat S=M\widetilde S G,
 \qquad
 \widehat C_a=MC_a.
 \tag{10.1}
\]

Then

\[
 \widehat Q=\int\chi
 \widehat\Omega\otimes\widehat\Omega\,dx.
 \tag{10.2}
\]

The four exact pulled residuals are

\[
 \widehat F_\chi
 =\int a_\chi
 \widehat\Omega\otimes\widehat\Omega\,dx,
 \qquad
 a_\chi=\partial_t\chi+U\cdot\nabla\chi+\nu\Delta\chi,
 \tag{10.3}
\]

\[
 \widehat F_{\widetilde S}
 =\int\chi\left[
 (\widehat S\widehat\Omega)\otimes\widehat\Omega
 +\widehat\Omega\otimes(\widehat S\widehat\Omega)
 \right]dx,
 \tag{10.4}
\]

\[
 \widehat F_\nu
 =-2\nu\int\chi\sum_a
 \partial_a\widehat\Omega\otimes
 \partial_a\widehat\Omega\,dx,
 \tag{10.5}
\]

and

\[
 (\widehat F_C)_{ij}
 =-\int\left[
 (\widehat C_a)_i\partial_a(\chi\widehat\Omega_j)
 +(\widehat C_a)_j\partial_a(\chi\widehat\Omega_i)
 \right]dx.
 \tag{10.6}
\]

Set

\[
 A_\chi
 =\inf_{c\in\mathbb R}
 \|a_\chi-c\|_{L^\infty(\operatorname{supp}\chi)},
 \tag{10.7}
\]

\[
 S_G=\|\widehat S\|_{L^\infty},
 \tag{10.8}
\]

\[
 D_G
 =\nu\frac{
 \int\chi|\nabla\widehat\Omega|^2dx
 }{\widehat E},
 \tag{10.9}
\]

\[
 C_G
 =\frac{
 \sum_a\int|\widehat C_a|
 |\partial_a(\chi\widehat\Omega)|dx
 }{\widehat E}.
 \tag{10.10}
\]

The amplitude part of \(a_\chi\) is removed by the infimum in (1.7), while
the other three terms are bounded directly. Therefore

\[
 \boxed{
 |\dot{\widehat B}|_F
 \le(1+\sqrt2)
 \left(A_\chi+2S_G+2D_G+2C_G\right).}
 \tag{10.11}
\]

This is the strongest direct pulled-metric inequality obtained in R0.70M.
Returning each term to the original frame gives

\[
 S_G\le\kappa_2(G)\|\widetilde S\|_\infty,
 \tag{10.12}
\]

\[
 D_G\le\kappa_2(G)^2
 \nu\frac{\int\chi|\nabla\Omega|^2dx}{E},
 \tag{10.13}
\]

and

\[
 C_G\le\kappa_2(G)^2
 \frac{
 \sum_a\int|C_a||\partial_a(\chi\Omega)|dx
 }E.
 \tag{10.14}
\]

The cutoff oscillation \(A_\chi\) has no condition-number loss, the
nonconstant-strain term pays one power, and diffusion/SGS generally pay two.

## 11. Scaling and the critical boundary

Use the equivalent Navier--Stokes scaling

\[
 u_\lambda(x,t)=\lambda u(\lambda x,\lambda^2t),
 \tag{11.1}
\]

with filter and cutoff scaled consistently. Then

\[
 \Sigma_\lambda(t)=\lambda^2
 \Sigma(\lambda^2t),
 \qquad
 Q_\lambda(t)=\lambda Q(\lambda^2t),
 \qquad
 F_\lambda(t)=\lambda^3F(\lambda^2t).
 \tag{11.2}
\]

The strain-only propagator and normalized shape scale as

\[
 G_\lambda(t)=G(\lambda^2t),
 \qquad
 \widehat B_\lambda(t)=\widehat B(\lambda^2t).
 \tag{11.3}
\]

Consequently,

\[
 \Gamma_\lambda(t)=\Gamma(\lambda^2t),
 \tag{11.4}
\]

and every term in

\[
 \int
 \left(A_\chi+S_G+D_G+C_G\right)dt
 \tag{11.5}
\]

is scaling critical. This is necessary but not sufficient. Leray energy does
not control (11.5), does not give a positive lower bound for
\(\widehat E\), and does not bound the spectral-spread history uniformly as
the filter scale tends to zero.

In particular, using only the fixed-scale Bernstein estimate gives a bound
of the form

\[
 \|\Sigma_\ell\|_\infty
 \lesssim\ell^{-5/2}\|u_0\|_2.
 \tag{11.6}
\]

Over a parabolic time interval of length \(O(\ell^2)\), this permits

\[
 \Gamma_\ell
 \lesssim\ell^{-1/2}\|u_0\|_2,
 \tag{11.7}
\]

which diverges as \(\ell\downarrow0\). Passing through (5.7) therefore
recreates the critical-strain exponential rather than closing it.

## 12. Position relative to the literature

The exact filtered velocity-gradient and SGS ledger used here is anchored in
[Tom--Carbone--Bragg](https://arxiv.org/abs/2005.04300). The present release
does not treat their statistical observations as pointwise estimates.

The physical Euler flow map and the auxiliary \(G\) are distinct.
[Constantin's Eulerian--Lagrangian formulation](https://arxiv.org/abs/math/0004059)
uses the full flow map and the Cauchy formula. Its viscous counterpart
contains a nontrivial diffusion commutator
([Constantin 2001](https://arxiv.org/abs/math/0005116)), while the stochastic
Navier--Stokes representation of
[Constantin--Iyer](https://arxiv.org/abs/math/0511067) includes Brownian flow
and expectation. None of these results identifies a strain-only propagator
with the physical deformation gradient.

Deformation-history closures are established turbulence models. In
[Chevillard--Meneveau](https://doi.org/10.1103/PhysRevLett.97.174501), recent
fluid deformation is used to model pressure and viscous terms in the
Lagrangian velocity-gradient equation. It is a stochastic closure, not an
exact NSE regularity inequality. R0.70M uses no modeled pressure or viscosity.

The affine-invariant SPD metric, congruence invariance, and geodesic distance
in Section 8 are standard matrix geometry; see
[Moakher](https://doi.org/10.1137/S0895479803436937),
[Bhatia--Holbrook](https://doi.org/10.1016/j.laa.2005.08.025), and
[Pennec--Fillard--Ayache](https://doi.org/10.1007/s11263-005-3222-z).
R0.70M's contribution is the exact placement of the localized vorticity
covariance residual in this geometry and the explicit NSE rank boundary, not
the invention of the metric.

Classical regularity criteria already show that critical velocity-gradient
or vorticity control prevents breakdown. The
[Beale--Kato--Majda criterion](https://doi.org/10.1007/BF01212349) is the
canonical Euler example; Navier--Stokes strain/gradient criteria occupy the
corresponding critical scale. In particular,
[Ponce's strain criterion](https://doi.org/10.1007/BF01205787) shows why an
assumption at the level of time-integrated maximum strain is already a
continuation hypothesis. Therefore a proof that first assumes finite
\(\Gamma\) and then applies (5.7) would not advance the Millennium problem.

No audited source found the exact zero-signed-integral strain loop
(1.12)--(1.18) in this localized covariance setting, the sharp
\(\kappa_2(G)^2\) quotient (1.9)--(1.11a), or the periodic-shear rank obstruction
to the affine-relative diagnostic. This is a bounded-search novelty statement,
not a universal claim that no related result exists.

## 13. What is closed and what remains open

### Proved or exactly derived here

- The complete strain-only pullback ledger (3.2)--(3.7).
- The pulled-shape BV estimate (1.6)--(1.7).
- The Euclidean return estimate with a sharp \(\kappa_2(G)^2\) loss.
- The sharp spectral-spread bound \(\kappa_2(G)\le e^\Gamma\).
- A smooth zero-signed-integral, zero-residual noncommutative strain loop
  with exact hyperbolic monodromy.
- The exact transfer of stretching into the material metric (7.4).
- The affine-relative SPD shape identity (1.19)--(1.22).
- Rank failure on an exact smooth periodic shear solution.
- Failure of isotropic covariance regularization to vanish uniformly.
- The pulled versions of all four R0.70K residuals and their critical
  conditional estimate (10.11).

### Closed route

The branch

> pull back the covariance, estimate the pulled residual in ordinary
> Euclidean norms, and obtain a universal energy-controlled anisotropy bound

is closed. The conversion costs a sharp \(\kappa_2(G)^2\), and controlling that
factor requires the same accumulated strain information the construction was
intended to avoid.

The branch

> use an inverse-covariance affine metric on every smooth NSE solution

is also closed without an additional coercivity hypothesis, because smooth
periodic shear gives rank-one covariance.

### Still open

- A scale-frame coercivity inequality of the form
  \[
  \sum_{j\in J(k)}Q_j\succeq c
  \operatorname{tr}\left(\sum_{j\in J(k)}Q_j\right)I
  \tag{13.1}
  \]
  with \(c>0\) controlled from NSE quantities.
- An adjacent-scale viscosity/SGS telescoping identity proved before applying
  \(\kappa_2(G)^2\).
- A positive-semidefinite Gramian using several directions, times, or scales
  that remains invertible on periodic shear without importing the source.
- A finite-energy unforced periodic NSE realization of the sharp
  strain-propagator amplification.
- A weak-solution passage for the pulled covariance and the moving metric.

### Route decision

R0.70N should test the smallest possible **multi-scale frame coercivity
gate**:

1. replace a single possibly rank-deficient \(Q_k\) by a finite adjacent-scale
   Gramian \(\mathcal Q_k=\sum_{j=k-m}^{k+m}w_jQ_j\);
2. derive its exact source and residual ledger without assuming isotropy;
3. determine whether \(\lambda_{\min}(\mathcal Q_k)\) can be bounded below by
   localized enstrophy, or construct an exact shear/Beltrami counterexample;
4. only if a coercive frame survives, apply the affine-relative estimate
   before any Euclidean norm conversion;
5. do not run large DNS until this algebraic gate is passed.

## 14. Reproduction and claim boundary

The exact symbolic producer is

```text
research/r070m_deformation_holonomy_audit.py
```

It verifies the rational monodromy, algebraic eigenvalues, non-normality,
physical covariance, three-dimensional anisotropy, sharp
\(\kappa_2(G)^2\) family, affine-relative congruence invariants, and the
non-uniform regularization example.

The zero-integral loop is a rigorous matrix-ODE theorem and a smooth
time-history construction. The rank-defect boundary is a rigorous property
of an exact unforced periodic NSE solution. The report does not claim that
the four-pulse loop has been realized along one unforced finite-energy NSE
trajectory.

No numerical trajectory is used as proof. No closure model, empirical
pressure sign, or DNS statistic enters the theorem. The result is an
auditable structural obstruction and a conditional pulled-metric estimate,
not a regularity theorem or a solution of the Millennium problem.
