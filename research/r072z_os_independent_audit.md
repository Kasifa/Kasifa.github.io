# Independent audit: R0.72Z Orr--Sommerfeld lane

**Date:** 2026-08-28

**Method:** independent derivation from the frozen row equation, followed by
Fourier-pair witnesses and asymptotic cross-checks.  No conclusion was
accepted merely because it appeared in the candidate report.

## 1. Exact energy identity

**Decision: PASS.**

With

\[
 D_\beta=-i(\partial_x+i\beta),\qquad
 \mathcal L=D_\beta^2+\mu,
\]

the two commutators are

\[
 [D_\beta,W_{xx}]=-iW_{xxx},
\]

\[
 [\mathcal L,W_{xx}]
 =-i(D_\beta W_{xxx}+W_{xxx}D_\beta).
\]

The independently recomputed pressure contribution is

\[
 -c\langle r,Hr\rangle,
 \qquad r=\mathcal L^{1/2}q,
\]

with

\[
 H=\frac12\mathcal L^{-3/2}
 (D_\beta W_{xxx}+W_{xxx}D_\beta)\mathcal L^{-3/2}.
\]

The sign in the report agrees with this convention.  The operator is
self-adjoint and compact for \(g>0\).

## 2. Operator bound and sufficient threshold

**Decision: PASS.**

The direct factorization gives

\[
 \|H\|\le\|W_{xxx}\|_\infty g^{-5/2}.
\]

The refined factor

\[
 \|H\|\le \|W_{xxx}\|_\infty
 g^{-3/2}s_{\beta,\mu}
\]

is also correct.  Consequently \(|c|\|H\|<1\) is ensured by

\[
 g>(|c|\|W_{xxx}\|_\infty)^{2/5}.
\]

For \(|c|=4\alpha^{-5}\), the exponent becomes \(\alpha^{-2}\).

## 3. Low-gap and high-gap witnesses

**Decision: PASS WITH SCOPE CORRECTION.**

For \(\beta=0\), the compression to
\(\operatorname{span}\{e_n,e_{n+1}\}\) has off-diagonal entry

\[
 a_n=
 \frac{(2n+1)\widehat{W_{xxx}}_1}
 {2(n^2+\mu)^{3/2}((n+1)^2+\mu)^{3/2}}.
\]

Since \(\widehat{W_{xxx}}_1=e^{-d}/4\), this equals the report's
formula.  The low-mode asymptotic is \(a_0\asymp\mu^{-3/2}\), not
\(\mu^{-5/2}\).  The report does not claim otherwise.

For \(\mu=2n^2\), direct asymptotics give

\[
 a_n\mu^{5/2}\to\frac{\sqrt2}{27}e^{-d}.
\]

An independently optimized choice \(n\asymp\sqrt{\mu/5}\) gives a different
positive constant but the same \(\mu^{-5/2}\) power.  Hence the \(2/5\)
gap exponent is necessary for unweighted instantaneous \(L^2_q\)
coercivity.  It is not proved necessary for every possible weighted,
transient, spectral, or enhanced-dissipation theorem.  The frozen report
states this narrower scope.

## 4. Exact tangent mode

**Decision: PASS.**

On the mean-zero \(\beta=\mu=0\) abstract OS space,

\[
 q_*=W_{xx},\qquad \mathcal L_0^{-1}q_*=-W
\]

has zero imaginary residual and evolves by heat.  This refutes a uniform
strict scalar-style block factor on that abstract row.  The report correctly
states that the physical \(\mu=0\) velocity coordinates degenerate, so the
witness is not promoted to a physical full-row theorem.

## 5. Forced estimates

**Decision: PASS.**

The exponential kernel integrals \(\Phi_a\) and \(\Psi_a\), the exact
negative-norm embedding

\[
 \ell_s^2=\max\left\{s^2,
 \frac{1+s^2\rho^2}{g}\right\},
\]

and the resulting spacetime/endpoint powers were recomputed.  They reproduce
the R0.72Y \(L^2\), standard \(H^{-1}\), and semiclassical
\(H^{-1}\) ledger on \(g\gtrsim\alpha^{-2}\).

## 6. Audit boundary

The audit does not certify low-gap limiting absorption, a transient
low-gap propagator, a physical kinetic-energy direct sum, or any nonlinear
estimate.  Those items remain OPEN in the frozen source.
