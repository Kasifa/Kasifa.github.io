# R0.73D independent analytic audit

**Date:** 2026-08-30  
**Audited source:** `research/r073d_viscous_persistence_proof.md`  
**Decision:** PASS for one fixed inviscid spectral cluster and the qualitative
limit \(\varepsilon\downarrow0\)

## 1. Audit question

The audit did not assume that \(-\varepsilon L\) is a bounded perturbation
on \(X_{1/4}\).  It separately checked:

1. the completed kinetic space and the transformed domains;
2. the compactness of the conjugated Rayleigh correction;
3. strong and adjoint-strong convergence of the dissipative base
   resolvents;
4. norm convergence of the compact Fredholm factors;
5. the extra step from strong full resolvent convergence to operator-norm
   convergence of the Riesz projections;
6. algebraic multiplicity and spectral-pollution boundaries.

## 2. Corrections required during the audit

The first draft incorrectly assigned the \(H^2\) domain to the base operator
also at \(\varepsilon=0\).  That restriction of the bounded multiplication
operator would not be closed.  The proof now keeps the singular domain jump

\[
 D(H_\varepsilon)=H^2_{\rm per}\quad(\varepsilon>0),
 \qquad D(H_0)=L^2.
 \tag{2.1}
\]

The first draft also wrote the kinetic norm as an \(L^2\) inner product
without first defining the completion.  The final proof defines \(X\) as the
completion of \(L^2\) and interprets the extension through the
\(H^1\)--\(H^{-1}\) dual pairing.

Both corrections are material.  They are incorporated in the audited
source.

## 3. Kinetic-space and domain check

Let \(\mu=1/4\).  On Fourier coefficients,

\[
 \|q\|_X^2
 =\mu^{-1}\sum_{n\in\mathbb Z}
 \frac{|q_n|^2}{n^2+\mu}.
\]

Thus

\[
 U=\mu^{-1/2}L_\mu^{-1/2}
\]

is an onto isometry from \(X\) to \(L^2\).  If
\(q=U^{-1}u=\mu^{1/2}L_\mu^{1/2}u\), then

\[
 q\in D_X(L_\mu)
 \quad\Longleftrightarrow\quad
 \sum_n(n^2+\mu)^2|u_n|^2<\infty,
\]

so \(UD_X(L_\mu)=H^2\).  The domain statement in the proof is correct.

The R0.73C eigenmode has \(c=i\eta_*\), \(\eta_*>0\).  The periodic
Rayleigh coefficient is therefore smooth, elliptic bootstrapping gives a
smooth eigenfunction, and the certified eigenvector genuinely belongs to
\(X\).

## 4. Compact commutator check

For \(\omega_n=(n^2+\mu)^{1/2}\), the Fourier matrix of
\([M_W,L_\mu^{1/2}]\) is

\[
 W_{n-m}(\omega_m-\omega_n).
\]

The reverse triangle inequality in \(\mathbb R^2\) gives

\[
 |\omega_m-\omega_n|\le|m-n|.
\]

Young's inequality therefore proves boundedness with norm at most
\(\sum_k|k||W_k|\).  For \(W_0\), this sum equals one.  Left multiplication
by the compact diagonal \(L_\mu^{-1/2}\) makes the commutator contribution
compact.  The \(W_0''\) contribution has compact factors on both sides.
Hence the asserted \(K\) is compact.  The rough numerical check \(\|K\|\le4\)
is also correct and is not used as a sharp estimate.

## 5. Base and full resolvents

For \(\operatorname{Re}z>0\), coercivity for both \(H_\varepsilon\) and its
adjoint gives surjectivity and

\[
 \|(z-H_\varepsilon)^{-1}\|
 \le(\operatorname{Re}z)^{-1}.
\]

The identity

\[
 R_\varepsilon(z)(z-M)u-u
 =-\varepsilon R_\varepsilon(z)L_\mu u,
 \qquad u\in H^2,
\]

proves strong convergence on a dense set.  The same argument for the
adjoints is valid.  Resolvent equicontinuity upgrades both convergences to be
uniform on a compact contour.

Since \(K\) is compact,

\[
 \sup_{z\in\Gamma_*}
 \|(R_\varepsilon(z)-R_0(z))K\|\to0.
\]

Thus the Fredholm factors \(I-R_\varepsilon K\) converge in norm and remain
uniformly invertible on any sufficiently small fixed circle around the
isolated inviscid eigenvalue.  The full contour resolvent statement passes.

## 6. Projection-norm step

This is the strongest and least automatic part of the proof.  Strong
resolvent convergence alone would be insufficient.  Here, however,

\[
 G_\varepsilon-R_\varepsilon
 =G_\varepsilon K R_\varepsilon,
\]

and the compact sandwich converges in operator norm, uniformly on the
contour.  Adjoint-strong convergence is exactly what is needed for
\(K(R_\varepsilon-R_0)\to0\) in norm.

The circle and its interior lie in the right half-plane, while every base
operator \(H_\varepsilon\) has spectrum in the closed left half-plane.
Therefore

\[
 \int_{\Gamma_*}R_\varepsilon(z)\,dz=0.
\]

After subtracting this analytic base term, the contour integral contains
only the norm-convergent compact sandwich.  Hence

\[
 \|P_\varepsilon-P_0\|_{\mathcal B(X)}\to0.
\]

This step passes.

## 7. Multiplicity and spectral-pollution boundary

For \(\varepsilon>0\), the full viscous operator has compact resolvent.
Once \(\|P_\varepsilon-P_0\|<1\), each projection is injective on the range
of the other, so their finite ranks agree.  Repeating the argument on every
smaller circle proves that all eigenvalues of this fixed cluster converge to
\(\sigma_*\), counted with algebraic multiplicity.

This excludes spectral pollution inside the audited fixed disk.  It does
not exclude new viscous spectrum elsewhere in the right half-plane.  In
particular, it gives no uniform complementary semigroup bound.

## 8. Final permitted statement

For every inviscid eigenvalue \(\sigma_*\) supplied by R0.73C, there exist
non-explicit \(r_*,\varepsilon_*>0\) such that, for
\(0<\varepsilon<\varepsilon_*\):

```text
fixedContourResolventUniform=CLOSED
fixedClusterRieszProjectionNormConvergence=CLOSED
fixedClusterAlgebraicMultiplicityPreserved=CLOSED
fixedClusterEigenvaluesConverge=CLOSED
```

The audit does not identify \(m_*\), and therefore does not prove a unique
or rank-one viscous branch.  It supplies no eigenvalue convergence rate, no
global right-half-plane no-pollution theorem, no moving-profile contour, no
complementary dichotomy, and no C5 or nonlinear conclusion.
