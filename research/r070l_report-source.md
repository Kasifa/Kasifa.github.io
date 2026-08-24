# R0.70L — Resolved source evolution and the pressure-blindness obstruction

**Status:** internal canonical research report; not a public theorem chapter
**Release:** R0.70L
**Date:** 2026-08-24
**Scope:** exact filtered strain-source evolution; coupling to the normalized
vorticity covariance of R0.70K; an indefinite local quadratic; a general
initial-face obstruction for instantaneous local source compensators; and an
explicit smooth periodic Navier--Stokes sign pair

---

## 1. Result in one page

R0.70K proved that the frozen resolved source produces the normalized
correlation

\[
 q=\Sigma:B,
 \qquad B=\frac{Q}{\operatorname{tr}Q}-\frac13I,
\]

at the nonnegative rate

\[
 2\operatorname{tr}[R(\Sigma-qI)^2].
 \tag{1.1}
\]

The only credible next step was therefore to evolve an actual source
\(\Sigma\), rather than freeze it. R0.70L takes

\[
 \Sigma(t)=S(U)(X(t),t),
 \qquad \dot X(t)=U(X(t),t),
 \tag{1.2}
\]

where \(U\) is a filtered velocity and \(S(U)\) its symmetric gradient. If

\[
 \tau=\overline{u\otimes u}-U\otimes U,
\]

then the exact resolved source equation is

\[
\boxed{
 \dot\Sigma
 =-(\Sigma^2)^\circ
 -\frac14(\Omega_*\otimes\Omega_*)^\circ
 -H_*^\circ
 +\nu(\Delta S)_*
 -K_{\tau,*}^\circ,}
 \tag{1.3}
\]

where \(\Omega_*=\nabla\times U(X,t)\), \(H=\nabla^2P\), and

\[
 (K_\tau)_{ij}
 =\frac12\partial_a(\partial_j\tau_{ia}
                         +\partial_i\tau_{ja}).
 \tag{1.4}
\]

Coupling (1.3) to the R0.70K covariance equation gives

\[
\boxed{
\begin{aligned}
 \dot q={}&
 \underbrace{B:\Sigma^2+\frac23|\Sigma|_F^2-2q^2}_{\mathcal Q(\Sigma,R)}
 -\frac14B:(\Omega_*\otimes\Omega_*)
 -B:H_*\\
 &+\nu B:(\Delta S)_*
 -B:K_{\tau,*}
 +\Sigma:\mathcal T_B(F_{\rm err}).
\end{aligned}}
 \tag{1.5}
\]

Every coefficient and sign in (1.3)--(1.5) was checked independently. The
first hoped-for cancellation already fails:

\[
 \mathcal Q\bigl(\operatorname{diag}(2,-1,-1),e_1\otimes e_1\bigr)=-2,
\]

but

\[
 \mathcal Q\bigl(\operatorname{diag}(2,-1,-1),e_2\otimes e_2\bigr)=1.
 \tag{1.6}
\]

The deeper obstruction is pressure. R0.70J proved a support-separated
realization of an arbitrary symmetric trace-free center pressure Hessian by
compact exterior velocity packets. Those packets vanish on a buffered core.
Consequently they leave the core source \(\Sigma\), the cutoff covariance
\(B\), the cutoff motion, and the pressure-free vorticity evolution of \(B\)
unchanged, while changing \(H_*^\circ\) arbitrarily.

This yields a local-functional no-go statement. For any \(C^1\) instantaneous
scalar \(\Phi(\Sigma,B)\), the pressure contribution is

\[
 \dot\Phi\big|_H=-D_\Sigma\Phi:H_*^\circ.
 \tag{1.7}
\]

At every source/shape state reachable by a buffered core, a universal
one-sided sign for \(\dot\Phi\) over all smooth initial data forces

\[
 \boxed{D_\Sigma\Phi=0.}
 \tag{1.8}
\]

Thus no nontrivial instantaneous compensator depending only on the local
source and the normalized core covariance can have a universal Lyapunov sign.
The conclusion does not cover a functional that also contains nonlocal
pressure information, spatial integrals, history, SGS state, or adjacent
scales.

There is also a completely explicit periodic witness. On \(\mathbb T^3\), set

\[
\begin{aligned}
 \psi_-&=-\sin x\sin y
 +2(1-\cos x)(1-\cos2y),\\
 \psi_+&=-\sin x\sin y
 +2(1-\cos2x)(1-\cos y),\\
 u_\pm&=(-\partial_y\psi_\pm,
 \partial_x\psi_\pm+\sqrt{120}(\cos z-1),0),
 \qquad \nu=1.
\end{aligned}
 \tag{1.9}
\]

Both smooth initial data have the same kinetic energy and generate genuine
short-time smooth Navier--Stokes solutions. At the origin and at the initial
time they have identical

\[
 \Sigma=\operatorname{diag}(1,-1,0),
 \quad
 R=\operatorname{diag}(1/2,0,1/2),
 \quad
 B=\operatorname{diag}(1/6,-1/3,1/6),
 \quad q=1/2.
 \tag{1.10}
\]

Their local quadratic, source-viscous, and covariance-evolution contributions
to \(\dot q\) are also identical. Only the pressure contraction changes, and
exact Fourier inversion gives

\[
 \boxed{
 \dot q_- =\frac{3901}{2040}>0,
 \qquad
 \dot q_+ =-\frac{1283}{2040}<0.}
 \tag{1.11}
\]

The R0.70L conclusion is:

> **Evolving the actual resolved strain does not close the R0.70K sign gate.
> The local quadratic is indefinite, and pressure makes every nontrivial
> instantaneous local source/shape compensator pressure-blind or unsigned.
> Any surviving route must retain genuinely nonlocal, spatially integrated,
> historical, or adjacent-scale pressure information.**

This is a rigorous structural no-go result and a route reduction. It is not a
Leray-to-critical estimate, a blow-up result, a global-regularity theorem, or
any part of a solution of the Millennium problem.

## 2. Conventions

Use

\[
 A_{ij}=\partial_jU_i,
 \qquad
 S=\frac12(A+A^{\mathsf T}),
 \qquad
 W=\frac12(A-A^{\mathsf T}).
 \tag{2.1}
\]

The resolved vorticity is

\[
 \Omega=\nabla\times U,
 \qquad
 W_{ij}=-\frac12\varepsilon_{ijk}\Omega_k,
\]

so

\[
 W^2=\frac14(\Omega\otimes\Omega-|\Omega|^2I),
 \qquad
 (W^2)^\circ=\frac14(\Omega\otimes\Omega)^\circ.
 \tag{2.2}
\]

For a symmetric matrix \(M\),

\[
 M^\circ=M-\frac13\operatorname{tr}(M)I.
 \tag{2.3}
\]

The covariance convention remains that of R0.70K. For a nonnegative cutoff
\(\chi(x,t)\),

\[
 Q=\int\chi\,\Omega\otimes\Omega\,dx,
 \qquad E=\operatorname{tr}Q>0,
 \qquad R=Q/E,
 \qquad B=R-I/3.
 \tag{2.4}
\]

When the source is followed along \(X(t)\), the cutoff may also depend on
\(X(t)\). Its complete time derivative remains in \(F_\chi\); no transported
cutoff identity is silently assumed.

## 3. Exact filtered strain equation

Let the spatial filter be linear, normalized, and commuting with the spatial
derivatives used below. The filtered momentum equation is

\[
 \partial_tU_i+U_a\partial_aU_i
 =-\partial_iP+\nu\Delta U_i-\partial_a\tau_{ia},
 \tag{3.1}
\]

where

\[
 \tau_{ia}=\overline{u_i u_a}-U_iU_a.
 \tag{3.2}
\]

Differentiate (3.1). Since

\[
 \partial_j(U_a\partial_aU_i)
 =U_a\partial_aA_{ij}+A_{aj}A_{ia},
\]

one obtains

\[
 D_t^U A_{ij}
 =-(A^2)_{ij}-\partial_i\partial_jP
 +\nu\Delta A_{ij}-\partial_j\partial_a\tau_{ia}.
 \tag{3.3}
\]

The symmetric part of \(A^2\) is

\[
 \operatorname{sym}(A^2)=S^2+W^2.
 \tag{3.4}
\]

Define

\[
 (K_\tau)_{ij}
 =\frac12(\partial_j\partial_a\tau_{ia}
          +\partial_i\partial_a\tau_{ja}).
 \tag{3.5}
\]

Because \(\operatorname{tr}S=0\), the trace-free equation is

\[
 \boxed{
 D_t^US
 =-(S^2)^\circ-(W^2)^\circ-(\nabla^2P)^\circ
 +\nu\Delta S-K_\tau^\circ.}
 \tag{3.6}
\]

Equations (2.2) and (3.6), evaluated along (1.2), prove (1.3). The sign of the
vorticity dyad is negative. Writing the equation with \(+WW^{\mathsf T}\) is
equivalent because \(WW^{\mathsf T}=-W^2\).

For the identity filter, \(\tau=0\) and (3.6) reduces to the classical
unfiltered strain equation. For a general filter, pressure and SGS Hessians
must remain separate in the exact ledger even if a model later combines
their statistics.

## 4. Coupling to the normalized covariance

On the cutoff support decompose

\[
 S(U)(x,t)=\Sigma(t)+\widetilde S(x,t).
 \tag{4.1}
\]

R0.70K gives

\[
 \dot q
 =\dot\Sigma:B
 +2\operatorname{tr}[R(\Sigma-qI)^2]
 +\Sigma:\mathcal T_B(F_{\rm err}),
 \tag{4.2}
\]

where

\[
 F_{\rm err}=F_\chi+F_{\widetilde S}+F_\nu+F_C.
 \tag{4.3}
\]

Substituting (1.3) into (4.2) leaves one algebraic simplification. Since

\[
 R=B+I/3,
 \qquad
 q=\Sigma:R=\Sigma:B,
\]

\[
\begin{aligned}
 &-B:\Sigma^2
 +2\{\operatorname{tr}(R\Sigma^2)-q^2\}\\
 &\qquad
 =B:\Sigma^2+\frac23|\Sigma|_F^2-2q^2.
\end{aligned}
 \tag{4.4}
\]

This proves (1.5). Notice that viscosity appears in two distinct places:
\(\nu B:(\Delta S)_*\) evolves the point source, while
\(\Sigma:\mathcal T_B(F_\nu)\) evolves the normalized covariance. Combining
them without derivation would lose the denominator correction.

## 5. The local quadratic has both signs

Define

\[
 \mathcal Q(\Sigma,R)
 =B:\Sigma^2+\frac23|\Sigma|_F^2-2(\Sigma:B)^2.
 \tag{5.1}
\]

Take

\[
 \Sigma_0=\operatorname{diag}(2,-1,-1).
\]

At \(R=e_1\otimes e_1\), one has \(q=2\),
\(B:\Sigma_0^2=2\), and hence

\[
 \mathcal Q=2+4-8=-2.
 \tag{5.2}
\]

At \(R=e_2\otimes e_2\), one has \(q=-1\),
\(B:\Sigma_0^2=-1\), and hence

\[
 \mathcal Q=-1+4-2=1.
 \tag{5.3}
\]

Thus source self-amplification can either overcompensate or reinforce the
frozen-source variance. No choice of sign for the local quadratic is valid on
the realizability simplex.

## 6. Pressure-blindness theorem for instantaneous local compensators

The theorem is stated at the smooth initial face, where every term is
classical.

### Theorem 6.1

Let \(u_c\in C_{c,\sigma}^\infty(\mathbb R^3)\) be a core velocity, let
\(0\le\chi\in C_c^\infty\) be supported inside a buffer on which exterior
packets vanish, and suppose \(E_\chi[u_c]>0\). Let

\[
 \Sigma=S(u_c)(0),
 \qquad B=B_\chi[u_c].
\]

Use either the identity filter or a compactly supported radial convolution
filter whose support remains inside the buffer. Assume the cutoff motion at
\(t=0\) depends only on the core velocity and its chosen center trajectory.

For every \(C^1\) scalar

\[
 \Phi:\operatorname{Sym}_0(3)\times\mathcal B\to\mathbb R,
\]

where

\[
 \mathcal B=\{B\in\operatorname{Sym}_0(3):B+I/3\ge0\},
\]

the following implication holds at the reachable pair \((\Sigma,B)\): if
\(\dot\Phi\) has one fixed sign for every smooth finite-energy initial datum
formed by adding support-separated exterior pressure packets to \(u_c\), then

\[
 D_\Sigma\Phi(\Sigma,B)=0.
 \tag{6.1}
\]

### Proof

R0.70J constructs, for every \(H\in\operatorname{Sym}_0(3)\), a finite sum of
compact divergence-free exterior packets whose additional center pressure
Hessian is exactly \(H\). The packet velocities vanish in the buffered core.
Their supports are disjoint from the core and from one another, so the
quadratic pressure sources have no cross terms.

Consequently, on the cutoff support and at \(t=0\):

1. the velocity, vorticity, strain, and every local spatial derivative remain
   those of \(u_c\);
2. the center velocity and therefore the prescribed cutoff motion remain
   fixed;
3. \(Q,E,R,B\) remain fixed;
4. \(\dot B\) remains fixed because the vorticity equation is local and
   pressure-free;
5. the only arbitrarily variable source term is
   \(\dot\Sigma|_H=-H\).

For a radial convolution filter, the exterior pressure is harmonic in the
core, and the mean-value property preserves its center Hessian exactly. Thus

\[
 \dot\Phi=C-D_\Sigma\Phi:H,
 \tag{6.2}
\]

where \(C\) is independent of the chosen exterior pressure packet. If
\(D_\Sigma\Phi\ne0\), choose

\[
 H=\pm\lambda D_\Sigma\Phi
\]

and let \(\lambda\) exceed \(|C|/|D_\Sigma\Phi|_F^2\). The two derivatives in
(6.2) have opposite signs. Hence a universal one-sided sign forces (6.1).
\(\square\)

### Boundaries of Theorem 6.1

The conclusion does not automatically extend to:

- a Gaussian or strict Littlewood--Paley filter with noncompact spatial tail;
- a source defined by a spatial average rather than a point value;
- a cutoff whose acceleration is allowed to depend on pressure;
- a functional containing \(H\), SGS state, a spatial pressure integral,
  past history, or neighboring scales;
- a sign claimed only on a fixed, quantitatively restricted energy class;
- global independence of \(\Phi\) from \(\Sigma\) without a reachability
  theorem for all pairs \((\Sigma,B)\).

These are genuine escape routes, not technical footnotes.

## 7. An explicit periodic sign pair

The abstract pressure realization proves a class no-go. The following finite
Fourier pair gives a transparent independent witness for \(q=\Sigma:B\).

Work on \(\mathbb T^3=(\mathbb R/2\pi\mathbb Z)^3\) with normalized spatial
average \(\langle\cdot\rangle\). Define (1.9). Since

\[
 u_\psi=(-\psi_y,\psi_x+\sqrt{120}(\cos z-1),0),
\]

each field is divergence-free and

\[
 \omega=(\sqrt{120}\sin z,0,\Delta_{x,y}\psi).
 \tag{7.1}
\]

At the origin,

\[
 u_\pm(0)=0,
 \quad
 \nabla u_\pm(0)=\operatorname{diag}(1,-1,0),
 \quad
 \omega_\pm(0)=0.
 \tag{7.2}
\]

The two perturbations are obtained from one another by swapping \(x\) and
\(y\), so their velocity norms agree. Fourier orthogonality gives

\[
 \langle(\Delta\psi_\pm)^2\rangle=60,
 \qquad
 Q_\pm=\operatorname{diag}(60,0,60).
 \tag{7.3}
\]

Equations (7.2)--(7.3) prove the common data in (1.10).

## 8. Exact pressure inversion

For a two-dimensional stream function embedded as above,

\[
 -\Delta p
 =\operatorname{tr}(\nabla u)^2
 =2(\psi_{xy}^2-\psi_{xx}\psi_{yy}).
 \tag{8.1}
\]

The \(z\)-dependent shear contributes neither a self pressure source nor a
cross pressure source. Exact Fourier inversion of (8.1) gives

\[
 H^-:=\nabla^2p_-(0)=
 \begin{pmatrix}
 -301/85&-152/65&0\\
 -152/65&131/85&0\\
 0&0&0
 \end{pmatrix},
 \tag{8.2}
\]

\[
 H^+:=\nabla^2p_+(0)=
 \begin{pmatrix}
 131/85&-152/65&0\\
 -152/65&-301/85&0\\
 0&0&0
 \end{pmatrix}.
 \tag{8.3}
\]

In particular,

\[
 H_{11}^-=-1-\frac{216}{85},
 \qquad
 H_{11}^+=-1+\frac{216}{85}.
 \tag{8.4}
\]

Since \(B=\operatorname{diag}(1/6,-1/3,1/6)\),

\[
 -H^-:B=\frac{563}{510},
 \qquad
 -H^+:B=-\frac{733}{510}.
 \tag{8.5}
\]

## 9. Complete derivative ledger

At the initial face, \(u_\pm(0)=0\), so the Eulerian and resolved-material
derivatives at the origin agree. All exact contributions are

| contribution to \(\dot q\) | \(u_-\) | \(u_+\) |
|---|---:|---:|
| local gradient, \(-\operatorname{sym}(A^2):B\) | \(1/6\) | \(1/6\) |
| pressure, \(-H:B\) | \(563/510\) | \(-733/510\) |
| source viscosity, \((\Delta S):B\) | \(-1\) | \(-1\) |
| covariance transport | \(0\) | \(0\) |
| total covariance stretching | \(0\) | \(0\) |
| normalized covariance viscosity, \(\Sigma:\dot B\) | \(197/120\) | \(197/120\) |
| SGS for the identity filter | \(0\) | \(0\) |

The raw covariance viscous matrix is

\[
 F_\nu=\operatorname{diag}(-120,0,-514),
 \tag{9.1}
\]

and the normalization correction gives

\[
 \dot B
 =\operatorname{diag}(197/120,0,-197/120).
 \tag{9.2}
\]

The complete common nonpressure subtotal is

\[
 \frac16-1+\frac{197}{120}=\frac{97}{120}.
 \tag{9.3}
\]

Adding (8.5) proves (1.11). Moreover,

\[
 \dot q_--\dot q_+
 =\frac{216}{85}
 =(-H^-:B)-(-H^+:B).
 \tag{9.4}
\]

Thus pressure is not merely one differing term; it is exactly the entire
difference in the signed derivative ledger.

In the R0.70K split, the frozen-source alignment contribution is \(+1/2\)
and the spatial strain-fluctuation contribution is \(-1/2\). They cancel in
this pair before the pressure-driven source evolution is inserted.

The publication-quality rendering, exact CSV ledger, contract, caption,
validation, and manifest are archived under
figures/r070l-source-compensator/fig-r070l-source-compensator/.

## 10. Why simple compensators fail

### 10.1 \(q\) itself

Equation (1.11) gives opposite signs at identical \((\Sigma,B,q)\), identical
energy, and identical nonpressure scalar ledger. Hence no autonomous ODE
\(\dot q=f(\Sigma,B,q)\) can represent the NSE evolution.

### 10.2 Source-direction normalization

Let

\[
 c=\frac{\Sigma:B}{|\Sigma|_F},
 \qquad |\Sigma|_F>0.
\]

Writing \(N=\Sigma/|\Sigma|_F\), its pressure contribution is

\[
 \dot c\big|_H
 =-\frac1{|\Sigma|_F}H:(B-cN).
 \tag{10.1}
\]

Unless \(B=cN\), the arbitrary exterior pressure realization gives both
signs. Normalizing the source magnitude therefore does not evade Theorem 6.1.

### 10.3 Spectral-gap diagnostic

Let \(\lambda_+(\Sigma)\) be a simple largest eigenvalue with projector
\(P_+\), and define

\[
 d=\lambda_+(\Sigma)-q\ge0.
 \tag{10.2}
\]

For a frozen source,

\[
 \dot d=-2\operatorname{tr}[R(\Sigma-qI)^2]\le0.
 \tag{10.3}
\]

This is the strongest natural local diagnostic found in this release. For
the amplitude-free \(\delta=d/|\Sigma|_F\), however, the pressure coefficient
is

\[
 -\frac1{|\Sigma|_F}
 \left(P_+-R-\frac{d}{|\Sigma|_F^2}\Sigma\right):H.
 \tag{10.4}
\]

It is arbitrary unless the displayed coefficient vanishes. The exact
pressure no-go therefore excludes even this otherwise favorable candidate.

### 10.4 Low-order polynomial corrections

Any polynomial or smooth invariant correction depending only on
\(\Sigma,B\) remains inside Theorem 6.1. Adding
\(|\Sigma|^2\), \(\operatorname{tr}\Sigma^3\),
\(\operatorname{tr}(B\Sigma^2)\), or a smooth function of their ratios cannot
remove the arbitrary linear pressure direction unless the final functional
loses all source dependence at that state.

### 10.5 Modeled pressure closures

Restricted Euler, Gaussian conditional closures, and recent-fluid-deformation
models can stabilize finite-dimensional dynamics. They do not replace the
exact pressure Hessian in a deterministic regularity argument.

### 10.6 The deformation pullback survives

There is one exact history-dependent construction that is not covered by
Theorem 6.1. If

\[
 \dot Q=\Sigma Q+Q\Sigma+F_{\rm err},
\]

let

\[
 \dot G=\Sigma G,\qquad G(t_0)=I,
 \qquad
 \widehat Q=G^{-1}QG^{-\mathsf T}.
 \tag{10.5}
\]

Direct differentiation cancels the complete constant-source stretching:

\[
 \boxed{
 \dot{\widehat Q}
 =G^{-1}F_{\rm err}G^{-\mathsf T}.}
 \tag{10.6}
\]

For

\[
 \widehat B
 =\frac{\widehat Q}{\operatorname{tr}\widehat Q}-\frac13I,
 \qquad
 \widehat F_{\rm err}=G^{-1}F_{\rm err}G^{-\mathsf T},
\]

\[
 \frac12\frac d{dt}|\widehat B|_F^2
 =
 \frac{
 \widehat B:\widehat F_{\rm err}
 -|\widehat B|_F^2\operatorname{tr}\widehat F_{\rm err}
 }{\operatorname{tr}\widehat Q}.
 \tag{10.7}
\]

This is the strongest surviving candidate because it removes source
stretching at the matrix level, not by assigning pressure a sign. Its cost is
history:

\[
 \det G=1,
 \qquad
 \|G\|\,\|G^{-1}\|
 \le
 \exp\left(2\int_{t_0}^t\|\Sigma(s)\|_{\rm op}\,ds\right).
 \tag{10.8}
\]

Controlling the condition number may therefore require essentially the
critical accumulated-strain information one hoped to prove. R0.70L records
(10.6) as a live candidate, not a closed estimate.

## 11. What survives the no-go theorem

The result deliberately leaves five classes open.

1. **Spatial integration.** On a periodic domain,
   \(\int S:\nabla^2p\,dx=0\). A useful localization must quantify the exact
   pressure commutator rather than assign a pointwise sign.
2. **Nonlocal pressure variables.** A functional may retain a pressure
   singular integral, a harmonic/exterior multipole, or a pressure flux.
3. **Scale coupling.** Germano and Gaussian semigroup identities can place
   pressure and SGS terms into one adjacent-scale ledger.
4. **History.** A Lagrangian time integral can remember pressure rotation,
   provided its growth can be estimated from energy or dissipation.
5. **Deformation pullback.** Equations (10.5)--(10.7) cancel the local source
   exactly, but require a condition-number estimate for the history matrix.

These routes are harder because they add state rather than remove it. They
are also the only routes not excluded by exact algebra.

## 12. Filter dependence of the pressure/SGS split

Pressure and SGS are not individually invariant under a change of filter.
An auxiliary two-mode Beltrami family makes this explicit. Let

\[
 v_N=(\sin Nz,\ \sin Nx+\cos Nz,\ \cos Nx),
 \qquad
 u(t)=Ae^{-\nu N^2t}v_N.
 \tag{12.1}
\]

Then

\[
 \nabla\times v_N=Nv_N,
 \qquad
 \Delta v_N=-N^2v_N,
 \qquad
 (v_N\cdot\nabla)v_N=\nabla(1+\sin Nx\cos Nz),
 \tag{12.2}
\]

so (12.1) is an exact periodic NSE solution with the corresponding pressure.
For a filter that fixes the \(N\)-shell velocity modes and multiplies the
mixed pressure mode by \(\theta\), the relevant pressure and SGS
contributions split as

\[
 -\theta C,
 \qquad
 -(1-\theta)C,
 \tag{12.3}
\]

while their sum is always \(-C\). Thus a proposed compensator that uses only
one of the two terms is filter-convention dependent. R0.70L uses the complete
pair in every route decision.

## 13. Scaling and energy boundary

Under Navier--Stokes scaling

\[
 u^{(r)}(x,t)=r^{-1}u(x/r,t/r^2),
\]

the ledgers scale as

\[
 \Sigma^{(r)},q^{(r)}\sim r^{-2},
 \qquad
 B^{(r)}\sim1,
 \qquad
 H^{(r)},\dot q^{(r)}\sim r^{-4}.
 \tag{13.1}
\]

The pressure obstruction is therefore scale-consistent. It is not a bound on
the exterior energy required to realize an arbitrary Hessian at a fixed
core. The periodic pair separately shows opposite \(\dot q\) at equal finite
energy, but only for this particular correlation, not for every
\(C^1\) functional.

## 14. Position relative to the literature

The bounded eleven-source audit is archived in
research/r070l_literature_audit.md. Its direct conclusions are:

- [Tom--Carbone--Bragg](https://arxiv.org/abs/2005.04300) provides the exact
  filtered velocity-gradient ledger and statistical evidence that pressure
  and SGS matter across scales;
- [Wilczek--Meneveau](https://arxiv.org/abs/1401.3351) separates exact
  pressure nonlocality from Gaussian conditional closure;
- [Germano](https://doi.org/10.1017/S0022112092001733) and
  [Johnson](https://arxiv.org/abs/1912.00293) provide exact adjacent-filter
  and Gaussian scale identities without a time sign;
- [Yang--Xu--Pumir--He](https://doi.org/10.1017/jfm.2024.143) gives a
  strong-vorticity asymptotic pressure cancellation supported by DNS, not a
  global deterministic error bound.

No audited source gives the R0.70L local-functional theorem or the explicit
matched \((\Sigma,B,q)\) opposite-derivative pair. This is a bounded novelty
statement, not a universal literature nonexistence claim. Pressure-Hessian
nonlocality itself is established and is not claimed as new.

## 15. What is closed and what remains open

### Proved or exactly derived here

- The resolved source equation (1.3), including pressure and SGS Hessians.
- The complete correlation ledger (1.5).
- The indefinite local quadratic (1.6).
- The pressure-blindness theorem for instantaneous local
  \(\Phi(\Sigma,B)\) under its explicit buffer/filter assumptions.
- The exact periodic matched-data pair (1.9)--(1.11).
- The complete derivative ledger showing pressure is the sole sign switch.
- The filter dependence of separate pressure and SGS contributions.

### Closed route

The branch “an instantaneous scalar depending nontrivially only on the local
resolved strain and the normalized local covariance has a universal NSE
Lyapunov sign” is closed at the smooth initial face under Theorem 6.1.

### Still open

- A compensator containing an exact nonlocal pressure variable.
- An energy-controlled bound for the deformation pullback (10.5).
- A localized version of global pressure orthogonality with an estimable
  commutator.
- An adjacent-scale pressure-plus-SGS identity compatible with the R0.70K
  denominator correction.
- A formulation for noncompact Gaussian or Littlewood--Paley filters with
  quantified tails.
- An energy-controlled estimate for the raw factor \(E_k\).
- A weak-solution passage and one-solution fixed-positive-time scale sum.

### Route decision

R0.70M should not enumerate more local polynomials in \((\Sigma,B)\). The
smallest surviving gate is the **deformation-pullback residual problem**:

1. derive (10.6) for the complete filtered/cutoff residual at every scale;
2. test whether positivity of \(Q\), \(\det G=1\), and neighboring scales can
   control the congruence without an a priori bound on \(\kappa(G)\);
3. run exact axisymmetric, Burgers, and periodic-shear witnesses against the
   normalized pullback;
4. if condition-number growth is fatal, couple the pullback to a localized
   pressure or adjacent-scale pressure-plus-SGS variable;
5. identify every boundary, harmonic, filter-tail, and denominator term
   before any DNS.

Large DNS is not yet justified. It becomes useful only after one nonlocal
combination survives exact algebra.

## 16. Reproduction and claim boundary

The producer research/r070l_source_compensator_audit.py uses exact SymPy
Fourier, matrix, polynomial, and rational arithmetic. It checks:

1. the gradient-square and vorticity-dyad identities;
2. the coupled local quadratic and its opposite signs;
3. divergence freedom and common local data of the periodic pair;
4. the exact covariance and normalized shape;
5. the complete pressure Hessians;
6. the identical nonpressure derivative ledger;
7. the opposite exact derivatives (1.11);
8. the finite-dimensional pressure duality behind Theorem 6.1.

The program certifies finite calculations. The continuum filtered equation,
support-separated no-go proof, local smooth NSE existence from the periodic
initial data, and bounded literature interpretation are analytic arguments.

R0.70L does not claim a nonlocal compensator, a regularity criterion, a
singularity, global regularity, or a solution of the Millennium problem.
