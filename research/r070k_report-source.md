# R0.70K — Normalized vorticity anisotropy: exact evolution, source alignment, and the missing compensator

**Status:** internal canonical research report; not a public theorem chapter
**Release:** R0.70K
**Date:** 2026-08-24
**Scope:** a trace-normalized, spatially localized filtered-vorticity
covariance; its exact transport, strain, diffusion, cutoff, and subfilter
evolution; the signed correlation with a resolved symmetric trace-free source;
exact frozen-source and Navier--Stokes witnesses; and the resulting route
decision

---

## 1. Result in one page

R0.70J showed that trace freedom, incompressibility, fixed helicity, angular
averaging, and a physical cutoff do not annihilate the deviatoric diagonal
pairing between an exterior strain and a high-frequency vorticity square. It
left a narrower possibility: normalize the vorticity covariance by its local
trace, derive its equation, and ask whether the resulting *shape* variable has
a favorable source-aware evolution.

This release carries out that test. For a nonnegative cutoff \(\chi\), filtered
vorticity \(\Omega\), and

\[
 Q=\int\chi\,\Omega\otimes\Omega\,dx,
 \qquad E=\operatorname{tr}Q>0,
 \qquad A=\operatorname{dev}Q,
 \tag{1.1}
\]

define the trace-one shape and normalized anisotropy

\[
 R=\frac QE,
 \qquad
 \boxed{B=R-\frac13I=\frac AE.}
 \tag{1.2}
\]

The raw tensor \(A\) in R0.70J, equation (12.1), is dimensional. The object
actually normalized in R0.70K is \(B=A/E\). If \(F=\dot Q\), then

\[
 \boxed{
 \dot B=\mathcal T_B(F)
 :=\frac{\operatorname{dev}F-B\operatorname{tr}F}{E}.}
 \tag{1.3}
\]

Formula (1.3) removes pure amplitude changes exactly:
\(F=\lambda Q\Rightarrow\dot B=0\). It also gives sharp kinematic bounds,

\[
 -\frac13\le\lambda_i(B)\le\frac23,
 \qquad
 0\le |B|_F^2\le\frac23.
 \tag{1.4}
\]

These bounds are useful but not smallness. Rank-one vorticity attains the
upper endpoint.

The decisive calculation concerns a constant symmetric trace-free source
\(\Sigma\). Its contribution to the raw covariance equation is

\[
 F_\Sigma=\Sigma Q+Q\Sigma.
 \tag{1.5}
\]

Writing \(q=\Sigma:B=\Sigma:R\), the induced shape equation is

\[
 \dot R\big|_\Sigma
 =\Sigma R+R\Sigma-2qR.
 \tag{1.6}
\]

For a frozen source, the signed source--shape correlation satisfies the exact
variance law

\[
 \boxed{
 \dot q\big|_\Sigma
 =2\{\operatorname{tr}(R\Sigma^2)-q^2\}
 =2\operatorname{tr}\!\left[R(\Sigma-qI)^2\right]
 \ge0.}
 \tag{1.7}
\]

Thus the resolved strain contribution does not damp the normalized
correlation. It aligns the covariance with a source eigenspace and reinforces
or preserves the correlation. Equality holds exactly when the support of
\(R\) lies inside one eigenspace of \(\Sigma\).

For

\[
 \Sigma_0=\operatorname{diag}(-1/2,-1/2,1),
 \quad
 R(p)=\operatorname{diag}((1-p)/2,(1-p)/2,p),
 \tag{1.8}
\]

one obtains

\[
 q=\frac{3p-1}{2},
 \qquad
 \dot p=3p(1-p),
 \qquad
 \dot q=(1+2q)(1-q).
 \tag{1.9}
\]

Starting from isotropy, \(p(0)=1/3\),

\[
 p(t)=\frac{e^{3t}}{e^{3t}+2},
 \qquad
 q(t)=\frac{e^{3t}-1}{e^{3t}+2},
 \qquad
 |B(t)|_F^2=\frac23q(t)^2.
 \tag{1.10}
\]

The correlation increases from zero to the maximal extensional value one.
Normalization therefore converts amplitude growth into a bounded shape
dynamics, but that dynamics can still move monotonically toward maximal
anisotropy.

The complete filtered equation has an exact compensator ledger. Split its raw
flux as \(F=F_\Sigma+F_{\rm err}\), allowing \(\Sigma=\Sigma(t)\). Then

\[
 \boxed{
 \dot q
 =\dot\Sigma:B
 +2\operatorname{tr}\!\left[R(\Sigma-qI)^2\right]
 +\Sigma:\mathcal T_B(F_{\rm err}).}
 \tag{1.11}
\]

All possible damping must come from the source evolution or the residual
transport, nonconstant strain, diffusion, cutoff, and subfilter terms. This
release assigns no favorable sign to that combined residual. Even viscosity
loses its matrix order after trace normalization. On the periodic
three-torus, the exact Navier--Stokes solution

\[
 u(t,z)=\left(
 \frac{D}{2}e^{-4\nu t}\sin2z,
 -C e^{-\nu t}\sin z,
 0\right)
 \tag{1.12}
\]

has zero nonlinearity. Its normalized vorticity shape is
\(R=\operatorname{diag}(p,1-p,0)\), where

\[
 p=\frac{C^2e^{-2\nu t}}
 {C^2e^{-2\nu t}+D^2e^{-8\nu t}},
 \tag{1.13}
\]

and

\[
 \boxed{
 \frac d{dt}|B|_F^2
 =12\nu p(1-p)(2p-1).}
 \tag{1.14}
\]

At \(p=4/5\) the derivative is \(+144\nu/125\); at \(p=1/5\) it is
\(-144\nu/125\). Both signs occur in exact solutions driven only by unequal
heat decay of two modes.

An exact Burgers vortex supplies the complementary self-consistent
Navier--Stokes boundary. Its vorticity shape is the maximal rank-one state,
its axial source correlation is positive, and \(B\) is stationary because the
complete PDE balance compensates the raw positive stretching. The classical
vortex is not a finite-energy Leray field, so it is a structural witness, not
a regularity counterexample.

The R0.70K conclusion is therefore:

> **Trace normalization produces a bounded and scale-transparent shape
> variable, but not a dissipative one. The frozen resolved source contributes
> a nonnegative variance and drives alignment; normalized viscosity also has
> no universal sign. Any successful source-aware route must identify and
> estimate an equation-specific compensator involving source evolution,
> pressure, cutoff/subfilter flux, or a scale sum. Normalization alone cannot
> provide the missing Leray-to-critical estimate.**

This closes one proposed mechanism. It does not prove blow-up, global
regularity, or any part of the Millennium theorem.

## 2. Conventions and the normalization correction

Let \(u\) be a smooth incompressible Navier--Stokes solution on the time
interval under consideration, let \(U=\varphi_\ell*u\), and let

\[
 \Omega=\nabla\times U=\varphi_\ell*(\nabla\times u).
 \tag{2.1}
\]

The filter is smooth, normalized, and commutes with spatial derivatives.
Let \(0\le\chi=\chi(x,t)\in C_c^\infty\). The moving-cutoff option is retained
because \(\partial_t\chi\) appears explicitly below. Define

\[
 Q_{ij}(t)=\int_{\mathbb R^3}\chi(x,t)
             \Omega_i(x,t)\Omega_j(x,t)\,dx.
 \tag{2.2}
\]

Because \(\chi\ge0\), \(Q\) is symmetric and positive semidefinite. Assume

\[
 E(t)=\operatorname{tr}Q(t)=\int\chi|\Omega|^2dx>0.
 \tag{2.3}
\]

The raw deviatoric moment is

\[
 A=\operatorname{dev}Q
 =Q-\frac E3I.
 \tag{2.4}
\]

It has the same physical dimension and Navier--Stokes scale as \(Q\). Calling
\(A\) “normalized” would be imprecise. The dimensionless shape variables are

\[
 R=\frac QE,
 \qquad
 B=R-\frac13I=\frac AE.
 \tag{2.5}
\]

This correction does not alter the hashed R0.70J report. It fixes the object
used from this release onward.

The notation

\[
 X:Y=\operatorname{tr}(X^{\mathsf T}Y),
 \qquad |X|_F^2=X:X
 \tag{2.6}
\]

is used throughout. Every source tensor \(\Sigma\) is symmetric and
trace-free unless stated otherwise.

## 3. Exact filtered covariance ledger

R0.70H derived the filtered vorticity equation

\[
 \partial_t\Omega_i+U_a\partial_a\Omega_i
 =\Omega_a\partial_aU_i+\nu\Delta\Omega_i
 +\partial_aC_{ai},
 \tag{3.1}
\]

where

\[
 C_{ai}
 =\bigl[(\omega_a u_i)_\ell-\Omega_aU_i\bigr]
 -\bigl[(u_a\omega_i)_\ell-U_a\Omega_i\bigr].
 \tag{3.2}
\]

Since the antisymmetric part of \(\nabla U\) annihilates its own vorticity,

\[
 (\Omega\cdot\nabla)U=S(U)\Omega,
 \qquad
 S(U)=\frac12(\nabla U+\nabla U^{\mathsf T}).
 \tag{3.3}
\]

Applying the tensor identity from R0.70H gives

\[
 \dot Q=F_\chi+F_S+F_\nu+F_C,
 \tag{3.4}
\]

with

\[
 \begin{aligned}
 F_\chi
 &=\int(\partial_t\chi+U\cdot\nabla\chi+\nu\Delta\chi)
       \Omega\otimes\Omega\,dx,\\
 F_S
 &=\int\chi\bigl[(S(U)\Omega)\otimes\Omega
              +\Omega\otimes(S(U)\Omega)\bigr]dx,\\
 F_\nu
 &=-2\nu\int\chi\sum_a
       \partial_a\Omega\otimes\partial_a\Omega\,dx,\\
 (F_C)_{ij}
 &=-\int\left[C_{ai}\partial_a(\chi\Omega_j)
              +C_{aj}\partial_a(\chi\Omega_i)\right]dx.
 \end{aligned}
 \tag{3.5}
\]

This is an identity for smooth filtered solutions. A minimal suitable-weak or
Leray formulation requires mollification and convergence checks for each
localized term. No such endpoint passage is claimed in R0.70K.

The four terms have distinct roles.

- \(F_\chi\) contains cutoff motion, resolved transport through the cutoff,
  and the diffusion of the cutoff.
- \(F_S\) is the resolved stretching source.
- \(F_\nu\preceq0\) as a raw matrix when \(\chi\ge0\); this order is not
  inherited by \(B\).
- \(F_C\) is the exact subfilter exchange. It is not an eddy-viscosity model.

The trace of (3.4) reproduces the localized filtered-enstrophy ledger. This is
an internal consistency check: the tensor equation does not create a new
scalar balance.

## 4. Master trace-normalized identity

Let \(F=\dot Q\). Differentiating \(R=Q/E\) gives

\[
 \dot R=\frac FE-\frac Q{E^2}\dot E
 =\frac{F-R\operatorname{tr}F}{E}.
 \tag{4.1}
\]

Since \(B=R-I/3\), and since the right side of (4.1) is trace-free,

\[
 \begin{aligned}
 \dot B
 &=\frac{F-R\operatorname{tr}F}{E}\\
 &=\frac{\operatorname{dev}F-B\operatorname{tr}F}{E}
 =:\mathcal T_B(F).
 \end{aligned}
 \tag{4.2}
\]

The operator \(\mathcal T_B\) is linear in its flux argument for fixed
\((B,E)\). Therefore (3.4) yields the exact decomposition

\[
 \boxed{
 \dot B
 =\mathcal T_B(F_\chi)
 +\mathcal T_B(F_S)
 +\mathcal T_B(F_\nu)
 +\mathcal T_B(F_C).}
 \tag{4.3}
\]

The scalar anisotropy variance

\[
 \alpha=|B|_F^2
 =\frac{\operatorname{tr}(Q^2)}{E^2}-\frac13
 \tag{4.3a}
\]

satisfies the independent check

\[
 \boxed{
 \frac12\dot\alpha
 =\frac1E\sum_X
 \left[B:X-(\operatorname{tr}X)\alpha\right],}
 \tag{4.3b}
\]

where the sum runs over the four fluxes in (3.4). Equivalently,

\[
 \frac12\dot\alpha
 =\frac{Q:\dot Q}{E^2}
 -\frac{\operatorname{tr}(Q^2)\dot E}{E^3}.
 \tag{4.3c}
\]

Every flux must carry its own denominator correction in (4.3b). Keeping only
\(\operatorname{dev}X/E\) would miss the second term.

If \(F=\lambda Q\), then

\[
 \operatorname{dev}F=\lambda A=\lambda EB,
 \qquad
 \operatorname{tr}F=\lambda E,
 \tag{4.4}
\]

so \(\mathcal T_B(F)=0\). This is the exact benefit of normalization: a
spatial profile whose covariance changes only in amplitude has constant
shape.

That benefit has a precise limitation. Matrix sign does not commute with
\(\operatorname{dev}\), and the subtraction
\(-B\operatorname{tr}F\) depends on the current shape. Hence
\(F_\nu\preceq0\) does not imply a sign for \(\dot B\), \(B:\dot B\), or a
source contraction \(\Sigma:\dot B\).

The normalization is undefined at \(E=0\), and its \(1/E\) factor can be
large when the cutoff contains little filtered-vorticity mass. Boundedness of
\(B\) does not provide a positive lower bound for \(E\).

## 5. Realizability geometry

Diagonalize the positive semidefinite trace-one matrix \(R\):

\[
 R=O\operatorname{diag}(p_1,p_2,p_3)O^{\mathsf T},
 \qquad
 p_i\ge0,
 \qquad
 \sum_ip_i=1.
 \tag{5.1}
\]

The eigenvalues of \(B\) are \(p_i-1/3\), proving

\[
 -\frac13\le\lambda_i(B)\le\frac23.
 \tag{5.2}
\]

Moreover,

\[
 |B|_F^2
 =\sum_i\left(p_i-\frac13\right)^2
 =\sum_ip_i^2-\frac13.
 \tag{5.3}
\]

Since \(1/3\le\sum_ip_i^2\le1\),

\[
 \boxed{0\le|B|_F^2\le\frac23.}
 \tag{5.4}
\]

The lower endpoint is isotropy \(R=I/3\); the upper endpoint is any rank-one
state \(R=e\otimes e\). Thus the energy trace normalizes the size but gives no
small anisotropy defect.

If \(\Sigma\in\operatorname{Sym}_0(3)\), then

\[
 q:=\Sigma:B=\Sigma:R.
 \tag{5.5}
\]

Because \(q\) is an \(R\)-weighted average of the eigenvalues of \(\Sigma\),

\[
 \lambda_{\min}(\Sigma)
 \le q\le
 \lambda_{\max}(\Sigma).
 \tag{5.6}
\]

Cauchy--Schwarz and (5.4) also give

\[
 |q|\le\sqrt{\frac23}\,|\Sigma|_F.
 \tag{5.7}
\]

Bounded shape is not bounded raw work. The original stretching pairing is

\[
 \Sigma:A=E(\Sigma:B)=Eq.
 \tag{5.8}
\]

and the local enstrophy trace \(E\) remains outside the normalized bound.

## 6. Frozen-source variance law

Fix a spatially constant source \(\Sigma\). The corresponding part of the
stretching flux is

\[
 F_\Sigma
 =\int\chi\bigl[(\Sigma\Omega)\otimes\Omega
                   +\Omega\otimes(\Sigma\Omega)\bigr]dx
 =\Sigma Q+Q\Sigma.
 \tag{6.1}
\]

Its trace is

\[
 \operatorname{tr}F_\Sigma=2\Sigma:Q=2Eq.
 \tag{6.2}
\]

Substituting (6.1)--(6.2) into (4.1),

\[
 \boxed{
 \dot R\big|_\Sigma
 =\Sigma R+R\Sigma-2qR.}
 \tag{6.3}
\]

For fixed \(\Sigma\),

\[
 \begin{aligned}
 \dot q\big|_\Sigma
 &=\Sigma:\dot R\big|_\Sigma\\
 &=2\operatorname{tr}(R\Sigma^2)-2q^2\\
 &=2\operatorname{tr}\!\left[R(\Sigma-qI)^2\right].
 \end{aligned}
 \tag{6.4}
\]

The last quantity is nonnegative because both \(R\) and
\((\Sigma-qI)^2\) are positive semidefinite and

\[
 \operatorname{tr}(R H)
 =\operatorname{tr}(R^{1/2}HR^{1/2})\ge0
 \quad(H\succeq0).
 \tag{6.5}
\]

Equality in (6.4) holds exactly when

\[
 \operatorname{ran}R\subseteq\ker(\Sigma-qI),
 \tag{6.6}
\]

that is, when the covariance is supported inside one eigenspace of the
source. Equation (6.4) is a variance identity: it is twice the variance of
the source eigenvalue under the probability weights supplied by \(R\).

This sign is the opposite of a damping law. A non-eigenstate covariance is
driven toward stronger correlation with the extensional eigenspaces.

## 7. Exact axisymmetric flow on covariance space

Take

\[
 \Sigma_0=\operatorname{diag}(-1/2,-1/2,1)
 \tag{7.1}
\]

and the axisymmetric trace-one family

\[
 R(p)=\operatorname{diag}\left(\frac{1-p}{2},
                                \frac{1-p}{2},p\right),
 \qquad0\le p\le1.
 \tag{7.2}
\]

Direct substitution gives

\[
 q=\Sigma_0:R=\frac{3p-1}{2},
 \tag{7.3}
\]

\[
 \operatorname{tr}(R\Sigma_0^2)-q^2
 =\frac94p(1-p),
 \tag{7.4}
\]

and

\[
 \dot p=3p(1-p),
 \qquad
 \dot q=\frac92p(1-p)=(1+2q)(1-q).
 \tag{7.5}
\]

The exact solution with initial value \(p_0\in(0,1)\) is

\[
 p(t)=\frac{p_0e^{3t}}{1-p_0+p_0e^{3t}}.
 \tag{7.6}
\]

For the isotropic initial shape \(p_0=1/3\), (1.10) follows. The anisotropy
norm is

\[
 |B|_F^2=\frac23q^2.
 \tag{7.7}
\]

Three endpoints clarify the geometry.

- \(p=0\) is the compressive two-plane state, with \(q=-1/2\). It is
  stationary under the source-only shape equation because the plane is an
  eigenspace.
- \(p=1/3\) is isotropic, with \(q=0\), but it is not stationary.
- \(p=1\) is the axial rank-one state, with \(q=1\), and is stationary at the
  maximal anisotropy vertex.

This finite exact model is the minimal obstruction to interpreting
normalization as isotropization.

## 8. The complete source-correlation ledger

Choose a spatially constant reference source \(\Sigma(t)\), and decompose the
resolved strain as

\[
 S(U)(x,t)=\Sigma(t)+\widetilde S(x,t)
 \tag{8.1}
\]

on the cutoff support. This is an exact add-and-subtract operation; it does
not assume that the actual strain is constant. Let \(F_{\widetilde S}\) be
the analogue of \(F_S\) with \(S(U)\) replaced by \(\widetilde S\), and put

\[
 F_{\rm err}=F_\chi+F_{\widetilde S}+F_\nu+F_C.
 \tag{8.2}
\]

Then \(F=F_\Sigma+F_{\rm err}\). Differentiating
\(q=\Sigma:B\), using (6.4), yields

\[
 \boxed{
 \dot q
 =\dot\Sigma:B
 +2\operatorname{tr}\!\left[R(\Sigma-qI)^2\right]
 +\Sigma:\mathcal T_B(F_{\rm err}).}
 \tag{8.3}
\]

Equation (8.3) identifies the exact missing mechanism. A favorable estimate
cannot come from frozen resolved stretching, because that term is
nonnegative. It must come from one or more of

\[
 \dot\Sigma:B,
 \quad
 \Sigma:\mathcal T_B(F_\chi),
 \quad
 \Sigma:\mathcal T_B(F_{\widetilde S}),
 \quad
 \Sigma:\mathcal T_B(F_\nu),
 \quad
 \Sigma:\mathcal T_B(F_C).
 \tag{8.4}
\]

For an actual low-frequency or exterior-strain source, \(\dot\Sigma\) is not
free. Its velocity-gradient equation contains strain self-amplification,
vorticity terms, the deviatoric pressure Hessian, viscosity, and subfilter
terms. Pressure therefore enters the source-aware problem indirectly through
the evolution of \(\Sigma\), even though it is absent from the vorticity
equation itself.

No term in (8.4) is assigned a sign in this release. An eddy-viscosity closure
or an isotropic pressure closure would be an additional model, not an exact
Navier--Stokes identity.

## 9. Exact Burgers-vortex boundary

The classical Burgers vortex provides a self-consistent stationary solution
of the three-dimensional incompressible Navier--Stokes equations. Let
\(\gamma>0\), \(\rho=(x_1^2+x_2^2)^{1/2}\), and

\[
 \Sigma_\gamma
 =\gamma\operatorname{diag}(-1/2,-1/2,1).
 \tag{9.1}
\]

The background strain velocity is \(u_s=\Sigma_\gamma x\). For circulation
\(\Gamma\), the axial vorticity and azimuthal velocity are

\[
 \omega_B(\rho)
 =\frac{\Gamma\gamma}{4\pi\nu}
   e^{-\gamma\rho^2/(4\nu)}e_3,
 \tag{9.2}
\]

\[
 u_B(\rho)
 =\frac{\Gamma}{2\pi\rho}
   \left(1-e^{-\gamma\rho^2/(4\nu)}\right)e_\theta.
 \tag{9.3}
\]

The total velocity \(u=u_s+u_B\) is stationary. Its scalar axial-vorticity
balance is

\[
 -\frac{\gamma\rho}{2}\,\partial_\rho\omega_B
 =\gamma\omega_B
 +\nu\left(\partial_\rho^2\omega_B
            +\frac1\rho\partial_\rho\omega_B\right).
 \tag{9.4}
\]

The exact producer verifies (9.4) and verifies that the curl of (9.3) is
(9.2). The complete velocity-pressure verification is classical and is not
reduced to finite symbolic algebra in the certificate.

Any even spatial filter preserves the axial direction of the vorticity. For
any nonnegative cutoff on which the filtered vorticity is nonzero,

\[
 R=e_3\otimes e_3,
 \qquad
 B=\operatorname{diag}(-1/3,-1/3,2/3),
 \tag{9.5}
\]

\[
 |B|_F^2=\frac23,
 \qquad
 q=\Sigma_\gamma:B=\gamma>0.
 \tag{9.6}
\]

The shape is stationary. The source-only variance in (6.4) vanishes because
the vorticity already occupies an eigenspace. At the same time, the raw
stretching trace is

\[
 \operatorname{tr}F_{\Sigma_\gamma}=2\gamma E>0.
 \tag{9.7}
\]

The complete stationary PDE balances this positive stretching through
transport and viscosity; filtering and localization add the corresponding
subfilter and cutoff ledgers. This is exactly the kind of compensation that
the frozen-source subsystem cannot see.

The boundary is essential. The linear background velocity and the infinite
axial tube have infinite energy on \(\mathbb R^3\). The Burgers vortex is not
a Leray finite-energy solution and is not a counterexample to regularity. It
is an exact structural witness showing that positive source correlation and
maximal anisotropy are compatible with the full stationary equations. The
formulas and this boundary are consistent with
[Gallay--Wayne's treatment of Burgers vortices](https://arxiv.org/abs/math/0503354).

## 10. Exact periodic shear: normalized diffusion has both signs

The raw diffusion flux is negative semidefinite when \(\chi=1\), but this
does not produce a monotone normalized anisotropy. On \(\mathbb T^3\), set

\[
 u(t,x)=\left(
 \frac D2e^{-4\nu t}\sin(2x_3),
 -Ce^{-\nu t}\sin x_3,
 0\right).
 \tag{10.1}
\]

The field is divergence-free, depends only on \(x_3\), and has zero third
component. Therefore

\[
 (u\cdot\nabla)u=0.
 \tag{10.2}
\]

Its vorticity also has zero third component, so
\((\omega\cdot\nabla)u=0\). Thus the covariance evolution in this example
isolates diffusion.

Each component solves the heat equation, so (10.1), with constant pressure,
is an exact Navier--Stokes solution. Its vorticity is

\[
 \omega(t,x)=\left(
 Ce^{-\nu t}\cos x_3,
 De^{-4\nu t}\cos2x_3,
 0\right).
 \tag{10.3}
\]

Orthogonality on the torus makes the normalized covariance diagonal:

\[
 R=\operatorname{diag}(p,1-p,0),
 \quad
 p=\frac{C^2e^{-2\nu t}}
 {C^2e^{-2\nu t}+D^2e^{-8\nu t}}.
 \tag{10.4}
\]

Direct differentiation gives

\[
 \dot p=6\nu p(1-p),
 \tag{10.5}
\]

\[
 |B|_F^2=2p^2-2p+\frac23,
 \tag{10.6}
\]

and the sign-changing identity (1.14). At \(t=0\), choosing \(C=2D\)
gives \(p=4/5\) and positive derivative; choosing \(D=2C\) gives \(p=1/5\)
and negative derivative.

No nonlinearity, pressure Hessian, cutoff, or subfilter exchange is available
to explain the sign pair. It is caused solely by relative diffusion of the
two Fourier modes. This rules out any universal claim that viscosity alone
monotonically reduces the trace-normalized anisotropy magnitude.

The example is periodic rather than finite-energy on \(\mathbb R^3\). Its
role is exact algebraic diagnosis of the normalized diffusion term, not a
Leray-space obstruction.

## 11. Finite-energy initial-face compatibility

R0.70J constructed a smooth compact divergence-free source/core profile with
strictly positive raw correlation at the initial face. Fix the same physical
filter, cutoff, and exterior-strain functional, and define whenever \(E[u]>0\)

\[
 \mathcal K[u]=\Sigma[u]:B[u]
 =\frac{\Sigma[u]:A[u]}{E[u]}.
 \tag{11.1}
\]

For the compact witness \(F\), \(\mathcal K[F]>0\). Under amplitude scaling,

\[
 \Sigma[\varepsilon F]=\varepsilon\Sigma[F],
 \quad
 A[\varepsilon F]=\varepsilon^2A[F],
 \quad
 E[\varepsilon F]=\varepsilon^2E[F],
 \tag{11.2}
\]

so

\[
 \mathcal K[\varepsilon F]=\varepsilon\mathcal K[F]>0.
 \tag{11.3}
\]

Choosing \(\varepsilon\) in a standard small-data regime gives a smooth mild
Navier--Stokes solution, and continuity preserves the strict inequality on a
possibly short initial interval. This transfers the sign from a function
space comparator to one genuine finite-energy trajectory near its initial
face.

It does not give a common fixed positive terminal time for a refining family.
Under Navier--Stokes rescaling the persistence interval shrinks
parabolically. This is the same boundary recorded in R0.70J and must not be
reported as a cascade, blow-up, or regularity theorem.

## 12. Navier--Stokes scaling and amplitude homogeneity

For

\[
 u^{(r)}(x,t)=r^{-1}u(x/r,t/r^2),
 \tag{12.1}
\]

with the cutoff and filter rescaled consistently,

\[
 \Omega^{(r)}\sim r^{-2},
 \qquad
 Q^{(r)},E^{(r)},A^{(r)}\sim r^{-1},
 \tag{12.2}
\]

whereas

\[
 R^{(r)}\sim1,
 \qquad B^{(r)}\sim1.
 \tag{12.3}
\]

A strain source scales as \(\Sigma^{(r)}\sim r^{-2}\), so

\[
 q^{(r)}=\Sigma^{(r)}:B^{(r)}\sim r^{-2},
 \qquad
 r^2q^{(r)}\sim1.
 \tag{12.4}
\]

The raw work remains

\[
 \Sigma^{(r)}:A^{(r)}\sim r^{-3},
 \tag{12.5}
\]

and its integral over a parabolic time window scales like \(r^{-1}\). The
critical zeroth moment is \(rQ\), not \(Q\) itself.

Amplitude homogeneity tells the same story:

\[
 \Sigma[\varepsilon u]\sim\varepsilon,
 \quad
 Q[\varepsilon u],A[\varepsilon u],E[\varepsilon u]\sim\varepsilon^2,
 \quad
 B[\varepsilon u]\sim1,
 \tag{12.6}
\]

\[
 \Sigma[\varepsilon u]:B[\varepsilon u]\sim\varepsilon,
 \qquad
 \Sigma[\varepsilon u]:A[\varepsilon u]\sim\varepsilon^3.
 \tag{12.7}
\]

Normalization separates shape from amplitude but cannot remove the
enstrophy factor in the physical cubic work.

## 13. Position relative to the literature

The bounded R0.70K literature audit retains ten primary sources. Its main
finding is negative but specific: established work supplies exact filtered
identities, conditional scale locality, averaged enstrophy-flux theorems, and
statistical or modeled anisotropy mechanisms, but not a deterministic signed
estimate for the cutoff-localized normalized vorticity covariance used here.

Three connections are especially direct.

1. [Germano's filtering identity](https://doi.org/10.1017/S0022112092001733)
   is the correct algebraic ledger for nested filter stresses, but carries no
   sign and does not absorb a physical cutoff.
2. [Eyink--Aluie's smooth coarse-graining theorem](https://arxiv.org/abs/0909.2386)
   proves conditional ultraviolet and infrared locality from velocity
   increment hypotheses. Those hypotheses are stronger than a bare Leray
   energy inequality and do not determine a fixed-center sign.
3. [Johnson's exact multiscale decomposition](https://doi.org/10.1103/PhysRevLett.124.104501)
   explicitly retains local and nonlocal strain, vorticity, and mixed
   cross-scale covariance contributions. It supports the need for the full
   residual ledger in (8.3), not a one-term closure.

The filtered velocity-gradient equation also contains the deviatoric pressure
Hessian and SGS Hessian explicitly; this is the correct starting point for
evolving an actual low-frequency source. The corresponding statistical DNS
analysis does not give a deterministic sign for (8.4).

The absence found in a bounded search is not a theorem of nonexistence. It
sets the novelty boundary for the next derivation.

## 14. What is closed and what remains open

### Proved or exactly derived here

- The correction from raw \(A\) to dimensionless \(B=A/E\).
- The master normalized evolution (4.2) and the four-part exact ledger (4.3).
- Sharp realizability bounds for \(B\) and \(\Sigma:B\).
- The frozen-source covariance flow and nonnegative variance identity (6.4).
- The exact axisymmetric replicator solution (7.6).
- The complete correlation-compensator identity (8.3).
- The scalar Burgers-vortex balance and its rank-one normalized geometry.
- The exact periodic two-mode Navier--Stokes shear with both signs in
  \(d|B|_F^2/dt\).
- The scaling and amplitude-homogeneity ledgers.

### Closed route

The branch “trace normalization alone creates a dissipative anisotropy
Lyapunov quantity” is closed. Frozen resolved stretching reinforces its own
source correlation, and viscosity does not monotonically reduce the
normalized anisotropy magnitude.

### Still open

- A rigorous weak-solution version of the complete localized tensor identity.
- Control of the denominator near times or cutoffs where \(E_k\) is small,
  or a formulation that retains \((E_k,B_k)\) jointly.
- Evolution of one precisely defined adjacent-scale or exterior source
  \(\Sigma_k\), including its deviatoric pressure Hessian.
- A compensator \(\mathcal C_k\) such that a combination of
  \(q_k\), \(\mathcal C_k\), and neighboring scales has a favorable time or
  scale sum.
- An energy-controlled estimate for the raw factor \(E_k\) paired with that
  compensated shape law.
- A mechanism surviving cutoff terms, subfilter exchange, positive parts, and
  summation over a refining scale tree.
- A common fixed positive terminal time for one finite-energy solution.

### Route decision

R0.70L should not search for another algebraic sign of \(B\) alone. Its
smallest meaningful gate is the **source-evolution compensator problem**:

1. define \(\Sigma_k\) as an actual filtered/exterior strain functional;
2. derive \(\dot\Sigma_k\) in the same filter and cutoff convention as
   \(\dot B_k\);
3. isolate the deviatoric pressure-Hessian, local strain, vorticity, viscous,
   and SGS terms;
4. test whether one exact combination cancels or dominates the positive
   variance in (8.3) after an adjacent-scale sum;
5. if the sign fails, build a finite exact NSE or initial-face witness before
   any large computation.

This ordering avoids spending simulation time on a quantity already excluded
by exact algebra. DNS can later estimate the surviving compensator terms, but
cannot replace their derivation.

## 15. Reproduction and claim boundary

The exact producer is
`research/r070k_anisotropy_evolution_audit.py`. With pinned SymPy arithmetic it
checks six groups:

1. normalization and amplitude cancellation;
2. the source-induced shape equation and variance identity;
3. the axisymmetric replicator model and exact solution;
4. sharp realizability examples;
5. the Burgers scalar vorticity balance and swirl curl;
6. the exact periodic shear equation and both diffusion signs.

The identities are stated for smooth solutions, a fixed derivative-commuting
filter, a smooth cutoff, and times at which \(E>0\). A time-varying filter
scale, a sharp cutoff, or a Leray weak-solution passage requires additional
terms or limiting arguments.

The producer does not computer-prove positivity for arbitrary
positive-semidefinite \(R\), the integration-by-parts derivation of the full
filtered tensor ledger, the complete Burgers velocity-pressure solution,
small-data Navier--Stokes theory, weak-solution passage, or completeness of
the literature search. Those inputs are stated analytically and bounded
separately.

The exact outputs establish no energy-only control of \(E\), no favorable
sign for source evolution or pressure, and no term-by-term sign theorem for
the cutoff or commutator contributions. They do establish that diffusion and
normalization alone have no universal anisotropy monotonicity. They establish
no finite-energy fixed-terminal-time cascade, singularity, global regularity
theorem, or solution of the Millennium problem.
