# R0.73D problem freeze: static viscous persistence of the certified Rayleigh cluster

**Frozen:** 2026-08-30  
**Parent release:** R0.73C  
**One permitted target:** the fixed profile \(d=0\), row \(\gamma=1/2\),
sign \(s=+1\), and the singular limit \(\varepsilon\downarrow0\)

## 1. Input inherited from R0.73C

On \(\mathbb T_{2\pi}\), let

\[
 W_0(x)=-\frac12\sin x+\frac14\sin2x,
 \qquad L=L_{1/4}=-\partial_x^2+\frac14,
\]

and

\[
 A=-\frac i2\bigl(M_{W_0}+M_{W_0''}L^{-1}\bigr).
\]

R0.73C proved, by a validated infinite-dimensional periodic-ODE
certificate, that

\[
 \exists\,\sigma_*\in(0.17035,0.17050),
 \qquad \sigma_*\in\sigma_p(A).
 \tag{1.1}
\]

Existence is certified.  Uniqueness of the root in the bracket and algebraic
simplicity are not certified.

## 2. Frozen space and viscous family

Let \(X=X_{1/4}\) be the completion of \(L^2\) in the norm

\[
 \|q\|_X^2=4\langle L^{-1}q,q\rangle_{L^2}.
 \tag{2.1}
\]

The viscous frozen generator is

\[
 B_\varepsilon=A-\varepsilon L,
 \qquad D_X(B_\varepsilon)=H^1_{\rm per},
 \qquad \varepsilon>0.
 \tag{2.2}
\]

The domain is not allowed to be suppressed.  Although \(A\) is bounded on
\(X\), \(\varepsilon L\) is unbounded there for every \(\varepsilon>0\).

## 3. Exact R0.73D theorem contract

The section is complete only if it proves all of the following without a
Fourier-tail extrapolation:

1. \(\sigma_*\) is an isolated finite-algebraic-multiplicity eigenvalue of
   \(A\) on \(X\);
2. there is a fixed circle \(\Gamma_*\subset\{\operatorname{Re}z>0\}\)
   enclosing no inviscid spectral point other than \(\sigma_*\);
3. \(\Gamma_*\subset\rho(B_\varepsilon)\) for every sufficiently small
   \(\varepsilon>0\), with a contour resolvent bound uniform in
   \(\varepsilon\);
4. the fixed-cluster Riesz projections satisfy at least
   \(\sup_\varepsilon\|P_\varepsilon\|<\infty\) and
   \(P_\varepsilon\to P_0\) strongly;
5. the viscous spectral cluster is nonempty and converges to \(\sigma_*\).

The stronger candidate conclusion

\[
 \|P_\varepsilon-P_0\|_{\mathcal B(X)}\to0
 \tag{3.1}
\]

may be released only if the compact-sandwich argument and the adjoint strong
resolvent step pass an independent audit.  If (3.1) passes, total algebraic
multiplicity preservation follows and may also be released.

## 4. Permitted proof route

The kinetic-space isometry

\[
 U=2L^{-1/2}:X\to L^2
\]

must be checked on the completed space, including

\[
 ULU^{-1}=L,
 \qquad U D_X(L)=H^2_{\rm per}.
\]

The intended transformed decomposition is

\[
 UAU^{-1}=M+K,
 \qquad M=-\frac i2M_{W_0},
\]

with

\[
 K=-\frac i2\left(
 L^{-1/2}[M_{W_0},L^{1/2}]
 +L^{-1/2}M_{W_0''}L^{-1/2}
 \right).
\]

The proof must establish, rather than assume, that \(K\) is compact.  It
must also preserve the domain jump

\[
 D(M-\varepsilon L)=H^2\quad(\varepsilon>0),
 \qquad D(M)=L^2\quad(\varepsilon=0).
\]

No bounded-operator perturbation theorem may be applied directly to
\(-\varepsilon L\).

## 5. Evidence classes

The public report must keep the following classes separate:

- **Inherited validated theorem:** existence of \(\sigma_*\), from R0.73C.
- **Exact operator theorem:** compact-Fredholm and Riesz argument in R0.73D.
- **Prior general theorem:** Shvydkoy--Friedlander zero-viscosity unstable
  spectral convergence.
- **Finite diagnostic:** any Fourier eigenvalue or sampled projection-norm
  calculation.  It may illustrate convergence but cannot certify the
  continuum theorem or the inviscid cluster radius.
- **Open problem:** moving-profile continuation, complement dichotomy,
  fast-time transfer, the complete OS--Squire system, nonlinear control, and
  Clay.

## 6. Mandatory literature boundary

The release must cite Shvydkoy and Friedlander (2008) as the decisive general
precedent.  It may describe the present proof as a self-contained
profile-specific realization and, if independently verified, an
operator-norm projection strengthening for this special compact row.  It
must not claim the first general vanishing-viscosity persistence theorem.

Channel/no-slip Orr--Sommerfeld theorems may appear only as comparisons.  The
periodic cross-stream problem has neither a wall boundary layer nor a real
critical layer at \(c=i\eta_*\).

## 7. Explicitly excluded from R0.73D

The following are outside this section even if a finite experiment looks
favorable:

```text
inviscidRootUnique=OPEN
inviscidEigenvalueSimple=OPEN
quantitativeEigenvalueRate=OPEN
movingProfileUniformContour=OPEN
uniformComplementaryDichotomy=OPEN
graphDomainKatoTransport=OPEN
logFastTimeTransfer=OPEN
completeOSSquireA2DirectSum=OPEN
nonlinearNavierStokes=OPEN
Clay=OPEN
```

In particular, a fixed-cluster theorem does not produce a rank-one branch
unless algebraic simplicity is proved separately.

## 8. Publication gate

R0.73D may be published only after all of the following pass:

1. exact proof and independent analytic audit;
2. current primary-source literature audit;
3. a reproducible diagnostic with progress monitoring and explicit finite
   status;
4. formal SVG/PDF/600-dpi PNG figure package;
5. Chinese/English HTML note and synchronized PDF;
6. cumulative R0.61--R0.73D recap and homepage/index counters;
7. deterministic certificate and release tests;
8. GitHub Pages deployment and byte/behavior parity checks.
