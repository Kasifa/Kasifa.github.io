# R0.73D report source: static viscous persistence of the certified Rayleigh cluster

**Date:** 2026-08-30  
**Scope:** the frozen periodic profile \(d=0\), row \(\gamma=1/2\), and
\(\varepsilon\downarrow0\)  
**Evidence:** inherited validated inviscid eigenvalue, exact operator theorem,
independent analytic audit, primary-source literature audit, and separate
finite diagnostics

## 0. Direct decision

R0.73D closes the static singular-perturbation input left open by R0.73C.
For every positive inviscid eigenvalue

\[
 \sigma_*\in(0.17035,0.17050)
\]

supplied by the R0.73C interval-monodromy theorem, the frozen viscous operator

\[
 B_\varepsilon
 =A_{1/2}(0)-\varepsilon L_{1/4}
\]

has a nonempty spectral cluster converging to \(\sigma_*\) as
\(\varepsilon\downarrow0\).  More precisely, there is a fixed circle in the
open right half-plane on which the resolvents are uniformly bounded, the
cluster Riesz projections converge in the physical kinetic-space operator
norm, and the total algebraic multiplicity is preserved.

The strongest closed block is

```text
staticVanishingViscosityPersistence=CLOSED
fixedContourResolventUniform=CLOSED
fixedClusterRieszProjectionNormConvergence=CLOSED
fixedClusterAlgebraicMultiplicityPreserved=CLOSED
fixedClusterEigenvaluesConverge=CLOSED
```

The constants defining the contour and the viscosity threshold are
existential, not numerical.  The inviscid algebraic multiplicity is unknown,
so the theorem concerns a spectral cluster and not a unique rank-one branch.
The full right-half-plane complement, moving profile, logarithmic fast-time
transfer, complete Orr--Sommerfeld--Squire system, nonlinear Navier--Stokes
problem, and Clay problem remain open.

## 1. Frozen operator and physical space

On \(\mathbb T_{2\pi}\), set

\[
 W_0(x)=-\frac12\sin x+\frac14\sin2x,
 \qquad L=L_{1/4}=-\partial_x^2+\frac14,
 \tag{1.1}
\]

and

\[
 A=-\frac i2\bigl(M_{W_0}+M_{W_0''}L^{-1}\bigr).
 \tag{1.2}
\]

The kinetic vorticity space is the completion \(X=X_{1/4}\) of \(L^2\)
under

\[
 \|q\|_X^2=4\langle L^{-1}q,q\rangle_{L^2}.
 \tag{1.3}
\]

The viscous operator is

\[
 B_\varepsilon=A-\varepsilon L,
 \qquad D_X(B_\varepsilon)=H^1_{\rm per}.
 \tag{1.4}
\]

The term \(-\varepsilon L\) is unbounded on \(X\) for every positive
\(\varepsilon\).  The proof therefore cannot use bounded-operator norm
perturbation of \(A\).

R0.73C proved the existence of

\[
 A q_*=\sigma_*q_*,
 \qquad
 \sigma_*\in(0.17035,0.17050).
 \tag{1.5}
\]

The corresponding phase speed is \(c=i\eta_*\), \(\eta_*>0\).  Hence
\(|W_0-c|\ge\eta_*\), the periodic Rayleigh coefficient is smooth, and
elliptic bootstrapping makes \(q_*\) smooth.  In particular, it is a genuine
eigenvector in \(X\).

## 2. The theorem

### Theorem 2.1 (fixed-cluster viscous persistence)

Let \(\sigma_*\) be any eigenvalue in (1.5), and let \(m_*\ge1\) be its
algebraic multiplicity for \(A\) on \(X\).  There exist
\(r_*,\varepsilon_*>0\) such that

\[
 \Gamma_*:=\{z:|z-\sigma_*|=r_*\}
 \subset\{\operatorname{Re}z>0\}
 \tag{2.1}
\]

contains no other inviscid spectral point and, for every
\(0<\varepsilon<\varepsilon_*\):

\[
 \Gamma_*\subset\rho(B_\varepsilon),
 \qquad
 \sup_{0<\varepsilon<\varepsilon_*}
 \sup_{z\in\Gamma_*}\|(z-B_\varepsilon)^{-1}\|_{\mathcal B(X)}<\infty.
 \tag{2.2}
\]

If

\[
 P_\varepsilon=\frac1{2\pi i}
 \int_{\Gamma_*}(z-B_\varepsilon)^{-1}\,dz,
 \tag{2.3}
\]

then

\[
 \|P_\varepsilon-P_0\|_{\mathcal B(X)}\to0,
 \qquad
 \operatorname{rank}P_\varepsilon
 =\operatorname{rank}P_0=m_*.
 \tag{2.4}
\]

All viscous eigenvalues in this cluster, counted with algebraic
multiplicity, converge to \(\sigma_*\).

The full proof is in
`research/r073d_viscous_persistence_proof.md`; the independent audit is in
`research/r073d_independent_analytic_audit.md`.

## 3. Exact kinetic-space conjugation

For a fixed \(\mu>0\), define

\[
 U_\mu=\mu^{-1/2}L_\mu^{-1/2}:X_\mu\to L^2.
 \tag{3.1}
\]

This is an onto isometry, and Fourier coefficients give

\[
 U_\mu L_\mu U_\mu^{-1}=L_\mu,
 \qquad
 U_\mu D_X(L_\mu)=H^2_{\rm per}.
 \tag{3.2}
\]

After conjugation,

\[
 U_\mu A_\gamma U_\mu^{-1}=M+K,
 \qquad M=-i\gamma M_W,
 \tag{3.3}
\]

where

\[
 K=-i\gamma\left(
 L_\mu^{-1/2}[M_W,L_\mu^{1/2}]
 +L_\mu^{-1/2}M_{W''}L_\mu^{-1/2}
 \right).
 \tag{3.4}
\]

The singular domain jump is preserved:

\[
 D(M-\varepsilon L_\mu)=H^2_{\rm per}\quad(\varepsilon>0),
 \qquad D(M)=L^2\quad(\varepsilon=0).
 \tag{3.5}
\]

## 4. Why the Rayleigh correction is compact

Let \(\omega_n=(n^2+\mu)^{1/2}\).  The Fourier matrix of the commutator in
(3.4) is

\[
 W_{n-m}(\omega_m-\omega_n).
\]

Since

\[
 |\omega_m-\omega_n|\le|m-n|,
\]

Young's inequality gives

\[
 \|[M_W,L_\mu^{1/2}]\|_{2\to2}
 \le\sum_k|k||W_k|.
 \tag{4.1}
\]

For the double-harmonic \(W_0\), this sum is exactly one.  The periodic
multiplier \(L_\mu^{-1/2}\) is compact.  Both terms in (3.4) are therefore
compact.  Thus \(M+K\) is a compact perturbation of skew-adjoint
multiplication, and every positive-real-part eigenvalue is isolated with
finite algebraic multiplicity.

This compact single-row representation is the structural reason the proof is
shorter than a no-slip channel Orr--Sommerfeld analysis.

## 5. Dissipative base resolvents

Put

\[
 H_\varepsilon=M-\varepsilon L_\mu,
 \qquad R_\varepsilon(z)=(z-H_\varepsilon)^{-1}.
\]

For \(\operatorname{Re}z>0\), coercivity for \(H_\varepsilon\) and its
adjoint gives

\[
 \|R_\varepsilon(z)\|\le(\operatorname{Re}z)^{-1}.
 \tag{5.1}
\]

If \(u\in H^2\) and \(f=(z-M)u\), then

\[
 R_\varepsilon(z)f-u
 =-\varepsilon R_\varepsilon(z)L_\mu u.
 \tag{5.2}
\]

The image \((z-M)H^2\) is dense.  Hence \(R_\varepsilon(z)\to R_0(z)\)
strongly, and the same is true for the adjoints.  Resolvent equicontinuity
makes both convergences uniform on a compact right-half-plane contour.

If \(C\) is compact, strong plus adjoint-strong convergence implies

\[
 \|(R_\varepsilon-R_0)C\|\to0,
 \qquad
 \|C(R_\varepsilon-R_0)\|\to0,
 \tag{5.3}
\]

uniformly on that contour.

## 6. Compact Fredholm factor and the fixed contour

The transformed full operator is

\[
 \widetilde B_\varepsilon=H_\varepsilon+K.
\]

Factor

\[
 z-\widetilde B_\varepsilon
 =(z-H_\varepsilon)(I-R_\varepsilon(z)K).
 \tag{6.1}
\]

Because \(K\) is compact, (5.3) gives norm convergence of

\[
 F_\varepsilon(z)=I-R_\varepsilon(z)K
\]

to \(F_0(z)\), uniformly on \(\Gamma_*\).  Since \(F_0\) is invertible on
the contour, \(F_\varepsilon\) is uniformly invertible there for all
sufficiently small \(\varepsilon\).  Thus the full resolvents

\[
 G_\varepsilon(z)
 =(z-\widetilde B_\varepsilon)^{-1}
 =F_\varepsilon(z)^{-1}R_\varepsilon(z)
 \tag{6.2}
\]

exist and are uniformly bounded.

## 7. The projection-norm step

Strong full resolvent convergence alone would not yield (2.4).  The special
compact structure supplies the missing norm estimate:

\[
 G_\varepsilon-R_\varepsilon
 =G_\varepsilon K R_\varepsilon.
 \tag{7.1}
\]

Equations (5.3) and (6.2) imply

\[
 \sup_{z\in\Gamma_*}
 \|G_\varepsilon K R_\varepsilon-G_0KR_0\|\to0.
 \tag{7.2}
\]

Every \(H_\varepsilon\) has spectrum in the closed left half-plane, while
the disk bounded by \(\Gamma_*\) lies in the open right half-plane.  Hence

\[
 \int_{\Gamma_*}R_\varepsilon(z)\,dz=0.
 \tag{7.3}
\]

Integrating only the norm-convergent compact sandwich proves

\[
 \|P_\varepsilon-P_0\|\to0.
\]

When this norm is below one, the two finite-rank projections have equal rank.
Repeating the argument on nested circles forces the full enclosed viscous
cluster to converge to \(\sigma_*\).

## 8. Relation to prior work

General inviscid-to-viscous unstable spectral persistence is not new.
Shvydkoy and Friedlander proved convergence, algebraic multiplicity, and
Riesz spectral-subspace persistence beyond the inviscid essential spectral
threshold for a broad periodic class.  Their Theorem 2.1(ii)--(iii) is the
decisive precedent.

The present contribution is a self-contained specialization to the exact
double-harmonic Fourier row and physical kinetic space, including the domain
jump, an explicit compact Fourier commutator, and a complete operator-norm
projection argument.  No general priority claim is made.

Li gave an explicit periodic Kolmogorov-flow example.  Li and Lin proved a
channel Orr--Sommerfeld persistence theorem using Wasow asymptotics and
Rouche's theorem.  Grenier--Guo--Nguyen treated a different viscous
boundary-layer instability mechanism.  Beekie--Chen--Jia study the periodic
high-Reynolds stable side under assumptions excluding the discrete inviscid
eigenvalue present here.

The full source-by-source boundary is recorded in
`research/r073d_literature_audit.md`.

## 9. Finite diagnostic

The finite experiment conjugates every Fourier compression by the same
kinetic-space isometry used in the proof.  At \(N=128\), the leading finite
eigenvalue and rank-one finite projector diagnostics are:

| \(\varepsilon\) | \(\operatorname{Re}\lambda_{\varepsilon,N}\) | finite \(\|P_{\varepsilon,N}\|\) | finite \(\|P_{\varepsilon,N}-P_{0,N}\|\) |
|---:|---:|---:|---:|
| \(0\) | 0.170407976920433 | 1.68350420491750 | 0 |
| \(10^{-2}\) | 0.156316407014908 | 1.48660633256165 | \(5.6234861\times10^{-1}\) |
| \(10^{-4}\) | 0.170261005247709 | 1.67567944616625 | \(2.8188658\times10^{-2}\) |
| \(10^{-6}\) | 0.170406506600202 | 1.68342107704387 | \(3.0905009\times10^{-4}\) |
| \(10^{-8}\) | 0.170407962217171 | 1.68350337308649 | \(3.0937715\times10^{-6}\) |

The \(N=96\) and \(N=128\) eigenvalues agree within
\(2.9\times10^{-15}\) on the frozen viscosity grid.  The largest-cutoff
embedded residual is below \(6.5\times10^{-15}\).  An independently coded
Fourier-coefficient construction reproduces all 48 rows.

These are finite diagnostics only.  They do not certify the continuum
contour, algebraic simplicity, or a convergence rate.  The analytic theorem
does not use them.

## 10. What this section changes

R0.73C established one genuine infinite-dimensional inviscid unstable
eigenvalue.  R0.73D now proves that this instability is not immediately
destroyed by an arbitrarily small frozen viscosity.  It also replaces the
project-internal H1 assumption

```text
viscous eigenvalue exists + Riesz projection uniformly bounded
```

by a theorem with the stronger fixed-row conclusion

```text
viscous spectral cluster persists
+ Riesz projection converges in operator norm
+ total algebraic multiplicity is preserved.
```

This is a meaningful linear spectral advance.  It is not yet a fast-time
growth theorem, because a single local spectral cluster does not control the
whole complementary spectrum or semigroup.

## 11. Remaining gap and next section

The static proof does not exclude additional viscous spectrum elsewhere in
the right half-plane.  It therefore does not provide a uniform exponential
dichotomy on the complement of \(P_\varepsilon\).

The next section, R0.73E, should use the same compact-Fredholm decomposition
on a full right-half-plane strip rather than only one small circle.  The
target is:

1. capture all inviscid spectrum with \(\operatorname{Re}z>b>0\) in a
   finite collection of fixed clusters;
2. rule out viscous spectral pollution on the remaining strip uniformly in
   \(\varepsilon\);
3. obtain a reduced complementary resolvent or semigroup bound;
4. combine the fixed spectral splitting with the bounded profile drift
   \(A(\varepsilon\theta)-A(0)=O(\varepsilon\theta)\) by a Volterra
   argument.

This route may avoid moving Riesz projections and graph-domain Kato
transport, but it still requires a genuine whole-complement estimate.

## 12. Final boundary

```text
inviscidRootUnique=OPEN
inviscidEigenvalueSimple=OPEN
explicitContourRadius=OPEN
explicitViscosityThreshold=OPEN
quantitativeEigenvalueRate=OPEN
globalRightHalfPlaneNoPollution=OPEN
uniformComplementaryDichotomy=OPEN
movingProfileUniformContour=OPEN
logFastTimeTransfer=OPEN
superPolynomialCompleteRowNoGo=CONDITIONAL
completeOSSquireA2DirectSum=OPEN
nonlinearNavierStokes=OPEN
Clay=OPEN
```

No finite Fourier calculation, no one-row linear spectral theorem, and no
fixed-profile result is presented as a solution of the three-dimensional
Navier--Stokes regularity problem.
