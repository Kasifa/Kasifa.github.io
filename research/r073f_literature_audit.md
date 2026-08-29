# R0.73F primary-source literature boundary audit

**Date:** 2026-08-30  
**Scope:** persistence of exponential dichotomies under a small bounded
nonautonomous perturbation, adiabatic transport of nonselfadjoint spectral
subspaces, and the distinction between frozen spectra and dynamical growth  
**Evidence class:** bounded primary-source audit; not an originality or
priority claim

## 1. Audit rule

The R0.73F proof is self-contained at the decisive roughness step.  The
literature is used for three narrower purposes:

1. verify that the definition of an infinite-dimensional exponential
   dichotomy allows a noninvertible stable evolution and only requires
   invertibility on the unstable fiber;
2. identify established roughness and slow-variation precedents;
3. prevent an instantaneous Riesz projection or a pointwise spectral gap from
   being mistaken for a dynamical lower bound.

Only original papers, author manuscripts, books, and official publisher pages
are used.  The search is bounded to the operator theory needed for this
section.  It is not an exhaustive survey of nonautonomous parabolic equations.

## 2. Claim-to-source ledger

| Claim needed for interpretation | Primary source | What the source actually supplies | What R0.73F proves itself |
|---|---|---|---|
| the correct Banach-space definition of exponential dichotomy | Latushkin--Schnaubelt (1999), Definition 2.1 and Theorem 2.7 | a strongly continuous projection field, forward decay on the stable fiber, invertibility and backward decay only on the unstable fiber; equivalence with hyperbolicity of the evolution semigroup | the projection field and both estimates for the exact moving Fourier row |
| roughness of an already existing dichotomy | Latushkin--Schnaubelt (1999), Corollary 2.10; Coppel (1978), Chapter 4 | persistence under sufficiently small perturbations of the cocycle or coefficient, in their stated classes | a direct Lyapunov--Perron graph proof with one conservative radius \(\nu/(16K^2)\), including rank preservation and the noninvertible stable case |
| frozen analytic dichotomies plus slow coefficient variation can imply a moving dichotomy | Schnaubelt (1999), Theorem 3.7 | under hypotheses (P1) and (ED), plus the quantitative condition \(L\|\phi\|_1<1\), a nonautonomous analytic-semigroup equation has an exponential dichotomy | the exact family has the stronger small-**amplitude** estimate \(\|\widetilde A(d)-\widetilde A(0)\|\le(49/4)d\), so the theorem is background rather than a black box |
| Kato-type transport of a separated spectral subspace | Schmid (2019), Proposition 2.17 and Theorem 3.1 | Proposition 2.17 assumes the comparison evolution exists and proves exact intertwining; Theorem 3.1 obtains adiabatic approximation under Condition 2.9 with \(\omega=0\), \(P\in W_*^{2,1}\), and a uniform gap | R0.73F does not invoke this theorem; it constructs the dynamical graph directly and leaves unscaled \(H^2\) Kato transport open |
| nonselfadjoint instantaneous eigenprojectors may fail to be the right transported objects | Joye (2007), Theorem 2.1 and the discussion of eigen-nilpotents | superadiabatic projectors for analytic nonselfadjoint families; eigen-nilpotents can obstruct direct following of instantaneous projectors | the lower bound follows from a uniform backward estimate on the entire top block, without selecting or transporting one instantaneous eigenline |
| a positive instantaneous spectral abscissa is not a dynamical lower bound | no external theorem is needed | the literature above does not license this implication | an exact diagonal \(4\times4\) crossing example has positive instantaneous spectral abscissa at every time but exponential decay over the full window |

## 3. Latushkin--Schnaubelt: dichotomy and evolution semigroups

**Primary source.** Yuri Latushkin and Roland Schnaubelt, *Evolution
semigroups, translation algebras, and exponential dichotomy of cocycles*,
Journal of Differential Equations 159 (1999), 321--369,
[DOI 10.1006/jdeq.1999.3668](https://doi.org/10.1006/jdeq.1999.3668),
[author manuscript](https://wwwalt.math.kit.edu/iana3/~schnaubelt/media/aht.pdf).

Definition 2.1 does not require the complete evolution to be invertible.  It
requires forward exponential decay on one projected fiber and invertibility,
with backward exponential decay, on the complementary fiber.  Theorem 2.7
identifies this dichotomy with hyperbolicity of the induced evolution
semigroup.  Corollary 2.10 proves persistence under a sufficiently small
fixed-time cocycle perturbation.

R0.73F follows exactly this noninvertible-stable convention.  Negative time is
used only on the finite-dimensional frozen top block.  The paper is a
precedent for the framework, not a black-box proof of the model-specific
smallness condition.

## 4. Coppel and Schnaubelt: roughness and slow variation

**Primary sources.** W. A. Coppel, *Dichotomies in Stability Theory*,
Lecture Notes in Mathematics 629, Springer, 1978,
[DOI 10.1007/BFb0067780](https://doi.org/10.1007/BFb0067780); Roland
Schnaubelt, *Sufficient conditions for exponential stability and dichotomy of
evolution equations*, Forum Mathematicum 11 (1999), 543--566,
[author manuscript](https://iana.math.kit.edu/downloads/iana3/schnaubelt/Paper/ed.pdf).

Coppel's discussion on pp. 28--37 establishes the classical roughness
principle for finite-dimensional linear ordinary differential equations with
matrix coefficients.  It is historical precedent, not a theorem covering the
present unbounded Banach-space generator.

Schnaubelt's Theorem 3.7 is genuinely infinite-dimensional but has a much more
structured hypothesis set than a bare small bound in \(\mathcal L(X)\).  Its
conditions (P1) and (ED) include a common domain, invertible generators of a
common analytic type, uniform control of \(A(t)A(s)^{-1}\), relative
graph-domain Hölder control, and frozen exponential dichotomies with common
constants.  The theorem then requires the quantitative condition
\(L\|\phi\|_1<1\).  These assumptions must not be compressed into the claim
that arbitrary small coefficient oscillation alone suffices.  The paper also
warns that pointwise spectral conditions can fail dramatically in a
nonautonomous problem.

R0.73F needs less abstract machinery because all profile dependence is a
bounded perturbation on \(H\), while the unbounded term
\(-\varepsilon L\) remains frozen.  Sections 3--4 of the proof give the two
Lyapunov--Perron equations, their contraction constant, complementary graph
spaces, rank preservation, and uniform rates.  No unverified numerical
roughness threshold is imported.

## 5. Schmid: common-domain adiabatic theory

**Primary source.** Jochen Schmid, *Adiabatic theorems for general linear
operators with time-independent domains*, Reviews in Mathematical Physics 31
(2019), no. 5, 1950014,
[arXiv:1804.11213](https://arxiv.org/abs/1804.11213),
[DOI 10.1142/S0129055X19500144](https://doi.org/10.1142/S0129055X19500144).

Schmid works with a common dense domain, Kato stability, operator regularity,
and associated spectral projections.  Proposition 2.17 does **not** construct
the comparison evolution: it assumes that the comparison evolution exists,
and then proves its exact intertwining relation for the projection.  Theorem
3.1 gives an adiabatic approximation under Condition
2.9 with stability exponent \(\omega=0\), the regularity
\(P\in W_*^{2,1}\), and a uniform spectral gap.  In particular, the
\(\omega=0\) hypothesis supplies uniform boundedness that a bare common-domain
statement does not provide.

This matters negatively for R0.73F: setwise equality
\(D(\widetilde B_\varepsilon(d))=H^2\) does not by itself prove a uniform
graph-domain transport theorem as \(\varepsilon\downarrow0\).  The natural
viscous graph norm contains \(\varepsilon\|Lu\|\), not an unscaled uniform
\(H^2\) bound.  R0.73F therefore does not cite adiabaticity as the reason for
the lower bound.

## 6. Joye: nonselfadjoint gaps and eigen-nilpotents

**Primary source.** Alain Joye, *General Adiabatic Evolution with a Gap
Condition*, Communications in Mathematical Physics 275 (2007), 139--162,
[arXiv:math-ph/0608059](https://arxiv.org/abs/math-ph/0608059),
[DOI 10.1007/s00220-007-0299-y](https://doi.org/10.1007/s00220-007-0299-y).

Joye assumes a common dense domain and analyticity in a complex neighborhood
of the real parameter interval.  The isolated part of the spectrum consists
of finitely many spectral values of constant finite algebraic multiplicity,
separated by uniform gaps; hypothesis H3 also imposes a contraction-semigroup
shift on the complementary block.  Under these conditions, Theorem 2.1
constructs superadiabatic projectors close to the instantaneous projectors.
The paper emphasizes that eigen-nilpotents can prevent the true evolution from
directly following the instantaneous eigenprojectors.

The source gives an important warning but not the precise R0.73F conclusion.
An operator-norm approximation or upper bound does not automatically provide a
conorm lower bound on a whole nonnormal top block.  R0.73F instead starts from
the R0.73E backward group estimate for that complete block and preserves it by
a small-amplitude graph transform.

## 7. What is and is not new in this section

The abstract fact that small bounded perturbations preserve exponential
dichotomies is established theory.  No priority claim is made for Lemma 3.1.
The model-specific contribution is the verified splice:

\[
 \text{R0.73E uniform frozen top dichotomy}
 +\|\widetilde A(d)-\widetilde A(0)\|\le\frac{49}{4}d
 \Longrightarrow
 \text{exact-profile fixed-window exponential gain}.
\]

The splice retains constants uniform in the singular viscosity parameter and
over a fast interval of length \(O(\varepsilon^{-1})\).  It also identifies
the correct logical boundary: frozen spectrum alone is insufficient, while a
uniform frozen semigroup dichotomy plus a small bounded profile amplitude is
sufficient.

The audit does not establish novelty of the final model-specific theorem.
Before journal submission, a broader search of slow nonselfadjoint
hydrodynamic-instability literature and an expert check of the R0.73E input are
still required.
