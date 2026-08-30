# R0.73G report source: nonlinear relative amplification and the exact planar barrier

**Date:** 2026-08-30  
**Parent input:** R0.73F moving-profile fixed-window lower law  
**Physical realization:** viscosity one,
\(\overline U_\Lambda(t,y)=(0,0,2\Lambda W(4t,2y))\),
\(K_x=0\), \(K_z=\pm1\)  
**Evidence:** exact nonlinear proof, independent operator derivation,
adversarial audit, primary-source literature boundary, symbolic identities,
and a separate finite Fourier diagnostic

## 0. Direct decision

R0.73G closes a deliberately limited nonlinear theorem and an equally
important negative boundary.

Let

\[
 W(d,x)=-\frac12e^{-d}\sin x+\frac14e^{-4d}\sin2x,
 \qquad W_d=W_{xx},
 \tag{0.1}
\]

and, for fixed \(D>0\), define

\[
 d_D=\min\{D,d_0\},
 \qquad T_D=\frac{d_D}{4},
 \qquad \kappa_D=(\alpha+\eta)d_D.
 \tag{0.2}
\]

There is an \(L^2\)-unit real top-vector launch \(\phi_\Lambda\) with

\[
 \|\phi_\Lambda\|_{H^3}\le C_{\rm top}\Lambda^2
 \tag{0.3}
\]

and an explicit exponentially small ceiling \(\delta_\Lambda^{\max}>0\)
such that every \(0<\delta\le\delta_\Lambda^{\max}\) produces a global
smooth exact solution whose perturbation satisfies

\[
 \boxed{
 \|w(T_D)\|_2
 \ge \frac1{2K_{\rm F}}e^{\kappa_D\Lambda}\|w(0)\|_2.}
 \tag{0.4}
\]

This is nonlinear **relative amplification**.  The sufficient seed can be
much smaller than \(e^{-\kappa_D\Lambda}\), so the final perturbation can
still tend to zero.  The theorem does not prove order-one departure.

The same launch lies in an exact planar invariant subspace.  Its nonlinear
orbit is a periodic two-dimensional Navier--Stokes solution embedded in
three dimensions, is globally smooth, and has no three-dimensional vorticity
stretching.  Direct nonlinear continuation of the R0.73F row therefore
cannot be a singularity mechanism.

## 1. Exact physical perturbation equation

The background

\[
 \overline U_\Lambda(t,y)
 =\bigl(0,0,2\Lambda W(4t,2y)\bigr)
 \tag{1.1}
\]

is an exact unforced solution on the standard three-torus with viscosity
one.  For \(U=\overline U_\Lambda+w\), subtraction and the full Leray
projector give

\[
 \partial_tw=L_\Lambda(t)w
 -\mathbb P\nabla\cdot(w\otimes w),
 \tag{1.2}
\]

\[
 L_\Lambda(t)w
 =\Delta w-\mathbb P\left(
 \overline U_\Lambda\cdot\nabla w
 +w\cdot\nabla\overline U_\Lambda
 \right).
 \tag{1.3}
\]

The quadratic term in (1.2) is not projected back to the selected Fourier
row.  All convolution-generated modes remain present.

The scaling ledger is

\[
 x=2y,qquad d=4t,qquad
 \theta=\Lambda d=4\Lambda t,qquad
 \varepsilon=\Lambda^{-1}.
 \tag{1.4}
\]

Thus the R0.73F fast endpoint \(d_D/\varepsilon\) is exactly the physical
endpoint \(T_D=d_D/4\), with exponent \(\kappa_D\Lambda\).  No factor of
two or four is omitted.

## 2. The exact planar invariant barrier

Define

\[
 \mathcal S_{2D}
 =\left\{(0,u_2(y,z),u_3(y,z)):
 \partial_yu_2+\partial_zu_3=0\right\}.
 \tag{2.1}
\]

The background, the R0.73F OS launch, the pressure, the Laplacian, and the
quadratic term preserve \(\mathcal S_{2D}\).  On this subspace the equation
is precisely periodic two-dimensional Navier--Stokes.  Its scalar vorticity

\[
 \omega=\partial_yU_3-\partial_zU_2
 \tag{2.2}
\]

obeys

\[
 \partial_t\omega+U_2\partial_y\omega+U_3\partial_z\omega
 =\Delta_{y,z}\omega,
 \tag{2.3}
\]

and

\[
 \frac12\frac d{dt}\|\omega\|_2^2
 +\|\nabla_{y,z}\omega\|_2^2=0.
 \tag{2.4}
\]

Every smooth orbit constructed in this section is therefore global.  Its
three-dimensional vorticity has only a first component and
\((\Omega\cdot\nabla)U=\Omega_1\partial_{x_1}U=0\).

## 3. One smooth unstable launch

On the normalized cell set

\[
 L=-\partial_x^2+\frac14,
 \qquad
 \widetilde B_\varepsilon(0)
 =\widetilde A(0)-\varepsilon L.
 \tag{3.1}
\]

Choose an \(L^2_x\)-unit eigenvector \(h_\varepsilon\) in the finite
nonzero top spectral block.  The fixed contour bounds its eigenvalue and
\(\widetilde A(0)\) is order zero on every fixed \(H^m_x\).  Two elliptic
iterations yield

\[
 \|h_\varepsilon\|_{H^{m+2}_x}
 \le C_m\varepsilon^{-1}\|h_\varepsilon\|_{H^m_x},
 \quad m=0,2,
 \tag{3.2}
\]

and hence

\[
 \|h_\varepsilon\|_{H^4_x}\le C\Lambda^2.
 \tag{3.3}
\]

The exact physical row map is

\[
 \mathcal Eh(y,z)=
 \left(
 0,\frac12(L^{-1/2}h)(2y),
 i(\partial_xL^{-1/2}h)(2y)
 \right)e^{iz}.
 \tag{3.4}
\]

It is divergence free and an isometry between the kinetic and physical
velocity \(L^2\) norms.  Therefore

\[
 \phi_\Lambda=2^{-1/2}
 \left(\mathcal Eh_\varepsilon+
 \overline{\mathcal Eh_\varepsilon}\right)
 \tag{3.5}
\]

is real, \(L^2\)-unit, planar, and satisfies (0.3).  R0.73F applies to every
vector in the frozen top space, so

\[
 \|\mathcal U_\Lambda(T_D,0)\phi_\Lambda\|_2
 \ge K_{\rm F}^{-1}e^{\kappa_D\Lambda}.
 \tag{3.6}
\]

## 4. Strong-norm lifespan and bootstrap

For \(Y(t)=\|w(t)\|_{H^3}\), standard periodic commutator estimates and
\(H^3(\mathbb T^3)\hookrightarrow W^{1,\infty}\) give constants
\(a,b>0\), independent of \(\Lambda\), such that

\[
 Y'\le a\Lambda Y+bY^2.
 \tag{4.1}
\]

If

\[
 Y(0)\le\rho_\Lambda
 :=\frac{a\Lambda}{4b}e^{-a\Lambda T_D},
 \tag{4.2}
\]

scalar comparison closes the whole physical window:

\[
 Y(t)\le2e^{a\Lambda t}Y(0),
 \qquad0\le t\le T_D.
 \tag{4.3}
\]

This is a sufficient, deliberately coarse envelope.  It is not a sharp
transition threshold.

## 5. Complete quadratic remainder

Let \(z_t=L_\Lambda(t)z\), \(z(0)=w(0)\), and \(r=w-z\).  Then

\[
 r_t=L_\Lambda(t)r
 -\mathbb P\nabla\cdot(w\otimes w),
 \qquad r(0)=0.
 \tag{5.1}
\]

The \(L^2\) energy identity gives

\[
 \frac d{dt}\|r\|_2^2
 \le c\Lambda\|r\|_2^2+CY^4.
 \tag{5.2}
\]

Using (4.3) yields constants \(C_D,M_D>0\), independent of \(\Lambda\),
such that

\[
 \boxed{
 \|r(T_D)\|_2
 \le C_De^{M_D\Lambda}\|w(0)\|_{H^3}^2.}
 \tag{5.3}
\]

This is an all-mode estimate.  It controls the zero row, doubled rows, and
all later modes together; it does not assume nonlinear row invariance.

## 6. Explicit sufficient seed ceiling

Define

\[
 \begin{aligned}
 \delta_\Lambda^{\max}:=\min\Bigg\{&
 \frac{a}{4bC_{\rm top}}\Lambda^{-1}e^{-a\Lambda T_D},\\
 &\frac{1}{2K_{\rm F}C_DC_{\rm top}^2}
 \Lambda^{-4}e^{-(M_D-\kappa_D)_+\Lambda}
 \Bigg\}.
 \end{aligned}
 \tag{6.1}
\]

For \(w(0)=\delta\phi_\Lambda\) with
\(0<\delta\le\delta_\Lambda^{\max}\), the first term closes (4.3).  The
second term makes the nonlinear error at most half of the linear lower
signal:

\[
 \|r(T_D)\|_2
 \le\frac1{2K_{\rm F}}e^{\kappa_D\Lambda}\delta.
 \tag{6.2}
\]

The reverse triangle inequality and (3.6) give (0.4).  If
\(M_D<\kappa_D\), the positive-part convention in (6.1) is conservative
but still sufficient.

## 7. Exact row leakage and parity

For a positive physical row written in normalized shear coordinate,

\[
 u_v(y,z)=\left(0,v(2y),2iv'(2y)\right)e^{iz},
 \tag{7.1}
\]

direct multiplication gives

\[
 (u_v\cdot\nabla)u_v
 =\left(0,0,4i\bigl(vv''-(v')^2\bigr)(2y)\right)e^{2iz}.
 \tag{7.2}
\]

The Leray projection vanishes only for the exceptional profiles satisfying
\(vv''-(v')^2=\text{constant}\).  Periodicity then forces

\[
 v(x)=Ae^{inx}+Be^{-inx}.
 \tag{7.3}
\]

Such a two-column profile cannot be a frozen top eigenvector: the nonzero
second harmonic of \(W(0)\) creates an extreme column with coefficient
proportional to

\[
 n^2+\frac14-4=n^2-\frac{15}{4}\ne0
 \tag{7.4}
\]

for every integer \(n\).  The viscous term is diagonal and cannot cancel
that sideband.  Thus the selected top vector has nonzero projected
\(K_z=2\) self-interaction.

For a real \(K_z=\pm1\) pair, the first quadratic generation has only
\(K_z=0,\pm2\).  A correction in the original odd pair starts no earlier
than the next interaction and is cubic in the seed.  This parity statement
identifies the sharper missing estimate, but does not itself bound it.

## 8. Three exact no-go results

1. **The selected linear row is not nonlinearly invariant.**  Equation
   (7.2) and the noncancellation argument give a nonzero doubled row.
2. **Kinetic \(L^2\) alone cannot close the quadratic term.**  A bounded
   sequence of divergence-free two-mode inputs can have
   \(\|\mathbb P[(u\cdot\nabla)u]\|_2\gtrsim N\).  A strong topology or
   parabolic derivative recovery is essential.
3. **Exponential linear growth does not imply nonlinear blow-up.**  The
   quadratic system

   \[
   \dot x=\lambda x-xy,
   \qquad \dot y=x^2
   \tag{8.1}
   \]

   has a linearly growing direction but conserves
   \(x^2+(y-\lambda)^2\), so every trajectory is global.

The third example is a logical counterexample, not evidence about the
Navier--Stokes row.  The actual selected row has the stronger exact planar
global-regularity barrier.

## 9. What remains open

The natural linear launch would have coefficient

\[
 \delta_\Lambda^{\rm nat}asymp e^{-\kappa_D\Lambda},
 \tag{9.1}
\]

which makes the linear endpoint order one.  The coarse remainder exponent
in (5.3) does not prove that this scale closes.  The next missing object is a
harmonic-resolved propagation estimate for the even second-order response
and the odd third-order feedback, with constants uniform in \(\Lambda\).

A useful target is a cubic target-row estimate of the form

\[
 \|\Pi_{\rm odd}
 [w_\delta(T_D)-\delta\mathcal U_\Lambda(T_D,0)\phi_\Lambda]\|_2
 \le C\delta^3e^{3\kappa_D\Lambda}.
 \tag{9.2}
\]

Even a proof of order-one departure within \(\mathcal S_{2D}\) would still
be a nonlinear instability theorem for an exact decaying shear, not a
singularity theorem.  A genuinely three-dimensional next gate must add
\(K_x\ne0\) or a nonzero first velocity component and control its Squire,
pressure, and triad coupling to the growing planar orbit.

## 10. Literature boundary

Friedlander--Pavlović--Shvydkoy prove nonlinear instability from unstable
spectrum for a **steady autonomous** Navier--Stokes linearization using
analytic-semigroup smoothing
([CMP 264 (2006)](https://doi.org/10.1007/s00220-006-1526-7),
[arXiv](https://arxiv.org/abs/math/0508173)).  Their theorem is a template,
not a black box for the present moving \(\Lambda\)-dependent family.

Grenier's high-order expansions and the Desjardins--Grenier viscous
boundary-layer theorem make the extra obligations explicit: interaction
algebra, correctors, resolvent control, and a residual smaller than the
growing signal
([Grenier 2000](https://doi.org/10.1002/1097-0312%28200009%2953%3A9%3C1067%3A%3AAID-CPA1%3E3.0.CO%3B2-Q),
[Desjardins--Grenier 2003](https://numdam.org/item/AIHPC_2003__20_1_87_0/)).

Grenier--Nguyen give the closest published heat-evolving instability
precedent located, but in a no-slip half-plane Prandtl-layer setting with
analyticity, a simple Rayleigh mode, singular sublayers, and an arbitrarily
small forcing
([Annals of PDE 5 (2019)](https://doi.org/10.1007/s40818-019-0074-3)).
Bedrossian--Vicol--Wang instead prove nonlinear stability for exact
heat-evolving near-Couette shears in another geometry
([JNS 28 (2018)](https://doi.org/10.1007/s00332-016-9330-9)).

The current periodic long-wave preprint of
Colombo--Dolce--Montalto--Ventura explicitly notes that a controlled
unstable eigenvalue does not automatically give nonlinear instability when
the remaining spectrum is not dominated
([arXiv:2509.18070](https://arxiv.org/abs/2509.18070)).

These sources calibrate the proof obligations.  None directly contains the
nonlinear lower law (0.4) for the present unforced periodic moving family.  The bounded
search supports a non-collision statement only.  No originality or priority
claim is made.

## 11. Claim ledger

```text
exactDecayingShearPerturbationEquation=CLOSED
selectedSeedPlanarInvariantClass=CLOSED
selectedNonlinearOrbitGlobalSmoothness=CLOSED
topEigenvectorPolynomialH3Cost=CLOSED
fixedWindowH3Bootstrap=CLOSED
allModeQuadraticRemainderBound=CLOSED
nonlinearRelativeAmplification=CLOSED
topEigenvectorDoubleRowLeakage=CLOSED

singleLinearRowNonlinearInvariant=FALSE
kineticL2QuadraticRemainderBound=FALSE
selectedRowCanCreateThreeDimensionalVortexStretching=FALSE
oneRowGainAloneImpliesOrderOneDeparture=FALSE_AS_INFERENCE
oneRowGainAloneImpliesFiniteTimeSingularity=FALSE

naturalSeedOrderOneDeparture=OPEN
targetedCubicModeConvolutionEstimate=OPEN
harmonicResolvedEvenOddPropagation=OPEN
transverseThreeDimensionalTriadClosure=OPEN
singleBackgroundSingleOrbitInstability=OPEN
completeOSSquireA2DirectSum=OPEN
Clay=OPEN
```

## 12. Evidence boundary

The continuum theorem comes from the exact perturbation equation, Sobolev
energy estimates, the inherited R0.73F lower law, and two independent
analytic audits.  A finite Fourier computation may diagnose the top-vector
Sobolev cost, doubled-row leakage, parity channels, and cutoff stability.  It
does not prove the continuum top cluster, the nonlinear theorem, global 3D
regularity, or a singularity.

R0.73G advances the chain from a one-row linear theorem to a genuine exact
nonlinear relative-amplification theorem.  It also proves that this direct
route is trapped inside a globally regular two-dimensional subsystem.  Its
direct value for the Clay alternative is therefore negative and structural:
the next viable test must be genuinely transverse and must replace the crude
strong-norm exponent by a harmonic-resolved nonlinear estimate.
