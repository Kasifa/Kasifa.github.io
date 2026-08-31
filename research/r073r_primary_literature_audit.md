# R0.73R primary-literature audit: caloric Besov norms and phase coherence

**Status:** bounded primary-source and collision pass complete; the analytic
core has a direct classical collision; no novelty or priority claim is made
for the local certificate package

**Access date:** 2026-08-31

## 1. Audit question and evidence rule

This pass asks which parts of R0.73R are already established harmonic
analysis, which parts are exact calculations made in this release, which
parts only follow after importing R0.73Q, and which claims remain open.
Every claim is assigned one of four classes:

- `VERIFIED_CLASSICAL`: an inspected research source contains the same
  mathematical ingredient, with its domain and indices retained;
- `INTERNAL_EXACT`: the claim follows from a displayed finite identity or a
  self-contained proof in R0.73R and still requires the release certificate;
- `INTERNAL_COROLLARY`: the claim additionally depends on an earlier proved
  result in this project, especially the fixed-orbit radius from R0.73Q;
- `OPEN`: neither the cited literature nor the internal proof establishes the
  claim.

The scope is deliberately narrow.  I checked the periodic heat-semigroup
description of negative Besov spaces, the dyadic heat estimate, stability of
global Navier--Stokes data in critical Besov topologies, the even-exponent
Fourier majorant principle, and the Rudin--Shapiro recursion.  I also ran a
targeted collision search for the same divergence-free
Dirichlet/Rudin--Shapiro tensor pair.  Failure to find that exact packaging is
not evidence of priority.

## 2. Main verdict

```text
periodicHeatBesovBMinusHalf64=VERIFIED_CLASSICAL
periodicDyadicHeatDecay=VERIFIED_CLASSICAL
criticalBesovGlobalDataOpenness=VERIFIED_CLASSICAL
evenExponentFourierMajorantAtP6=VERIFIED_CLASSICAL
rudinShapiroRecursionAndSquareRootBound=VERIFIED_CLASSICAL
sexticConvolutionCertificate=INTERNAL_EXACT
modalAndAdditiveMultiplicityBounds=INTERNAL_EXACT
exactDirichletSixthMomentAndCarrierIdentity=INTERNAL_EXACT
matchedDivergenceFreeTensorPair=INTERNAL_EXACT
fixedOrbitAllRestartEntrance=INTERNAL_COROLLARY
uniformL2OnlyStrongEntrance=OPEN
arbitraryDataClayConclusion=OPEN
noveltyOrPriority=NOT_CLAIMED
```

The release therefore cannot present the equivalence

\[
 \|e^{t\Delta}f\|_{L^4_tL^6_x}
 \asymp
 \left(\sum_j2^{-2j}\|P_jf\|_6^4\right)^{1/4}
 \tag{2.1}
\]

as a new theorem.  Its defensible value is an auditable interface: exact
shellwise Fourier data are converted into the already-classical caloric
Besov norm and then, by R0.73Q, into a sufficient perturbative entrance around
one fixed known global orbit.

## 3. Direct collision: the periodic heat/Besov equivalence

**Source.** Jean-Yves Chemin and Isabelle Gallagher, *On the Global
Wellposedness of the 3-D Navier--Stokes Equations with Large Initial Data*,
Annales Scientifiques de l'École Normale Supérieure 39 (2006), 679--698,
[primary Numdam PDF](https://www.numdam.org/article/ASENS_2006_4_39_4_679_0.pdf),
[DOI 10.1016/j.ansens.2006.07.002](https://doi.org/10.1016/j.ansens.2006.07.002).

**Inspected statements.** The paper works on
\(\mathbb T^3=(\mathbb R/2\pi\mathbb Z)^3\), takes mean-free fields, and
sets \(S(t)=e^{t\Delta}\).  Definition 1.1 defines, for \(s>0\),

\[
 \|u\|_{B^{-s}_{p,q}}
 =\left\|t^{s/2}\|S(t)u\|_{L^p}\right\|_{L^q(dt/t)}.
 \tag{3.1}
\]

With \(s=1/2\), \(p=6\), and \(q=4\), the fourth power of (3.1) is exactly

\[
 \int_0^\infty\|e^{t\Delta}u\|_6^4\,dt.
 \tag{3.2}
\]

Definitions 2.1--2.2 introduce periodic Littlewood--Paley blocks and state
that the negative heat definition is equivalent to the dyadic Besov norm.
At the same indices this is

\[
 \left(\sum_j2^{-2j}\|\Delta_ju\|_6^4\right)^{1/4}.
 \tag{3.3}
\]

Lemma 4.2 records the uniform localized heat decay

\[
 \|\Delta_je^{t\Delta}a\|_{L^p}
 \le C e^{-c2^{2j}t}\|\Delta_ja\|_{L^p}.
 \tag{3.4}
\]

Thus (2.1), the annular decay used in its upper bound, the mean-zero
condition, and the \(\ell^4\) shell exponent are `VERIFIED_CLASSICAL`.
R0.73R's direct inverse-multiplier proof is still useful for an explicit
two-sided certificate, but it does not create a new function-space theorem.

**Notation boundary.** Chemin--Gallagher write the mean-free periodic space
as \(B^{-1/2}_{6,4}(\mathbb T^3)\), using an inhomogeneous low block.  R0.73R
also uses \(j\ge0\) with all low nonzero modes in \(P_0\).  A dot over the
Besov symbol is therefore a convention after removing the zero mode, not a
separate theorem.  Public text should say “the mean-zero periodic
\(B^{-1/2}_{6,4}\) caloric norm” or explain this convention once.

**Corroborating source.** Xiao Xiong, Quanhua Xu, and Zhi Yin,
*Sobolev, Besov and Triebel--Lizorkin Spaces on Quantum Tori*, Memoirs of the
American Mathematical Society 252 (2018), no. 1203,
[arXiv primary manuscript](https://arxiv.org/pdf/1507.01789),
[DOI 10.1090/memo/1203](https://doi.org/10.1090/memo/1203).
Theorem 3.15 gives Littlewood--Paley/Poisson/heat-semigroup
characterizations for all real smoothness indices; the usual torus is the
commutative case \(\theta=0\).  This source confirms that the caloric
characterization belongs to general torus function-space theory.  The release
does not need its noncommutative generality.

## 4. Critical Navier--Stokes stability is also classical in principle

**Source.** Isabelle Gallagher, Drago\c{s} Iftimie, and Fabrice Planchon,
*Asymptotics and Stability for Global Solutions to the Navier--Stokes
Equations*, Annales de l'Institut Fourier 53 (2003), 1387--1424,
[primary Numdam PDF](https://www.numdam.org/item/10.5802/aif.1983.pdf),
[DOI 10.5802/aif.1983](https://doi.org/10.5802/aif.1983).

Theorem 3.1 proves openness and stability around an a priori global solution
in the whole-space critical classes
\(\dot B^{3/p-1}_{p,q}(\mathbb R^3)\), with the theorem's finite-index and
solution-branch hypotheses.  The choice \(p=6,q=4\) gives
\(\dot B^{-1/2}_{6,4}\).  This is a direct collision with any broad claim that
critical-Besov openness around a global orbit is new.

The domain is \(\mathbb R^3\), not the torus, and the theorem does not give
the explicit R0.73Q all-restart radius.  Hence the R0.73R entrance condition
around the fixed R0.73Q orbit is `INTERNAL_COROLLARY`, while the underlying
stability mechanism is `VERIFIED_CLASSICAL`.

Chemin--Gallagher 2006 also constructs explicit periodic data that may be
large in a critical norm and nevertheless generate a unique global smooth
solution under a nonlinear structural condition.  R0.73R must therefore
avoid any general novelty claim of the form “spectral structure or phase
permits large safe data.”

## 5. Phase sensitivity at the sixth moment is classical

**Source.** Ben Green and Imre Z. Ruzsa, *On the Hardy--Littlewood Majorant
Problem*, Mathematical Proceedings of the Cambridge Philosophical Society
137 (2004), 511--517,
[author manuscript](https://arxiv.org/pdf/math/0303244),
[DOI 10.1017/S0305004104007911](https://doi.org/10.1017/S0305004104007911).

Equation (1) in the introduction records the classical even-exponent
majorant inequality: for fixed frequency support and \(|a_n|\le1\), replacing
the coefficients by \(+1\) cannot decrease the \(L^p\) norm when
\(p\in2\mathbb N\).  At \(p=6\), this follows directly by expanding the third
power and applying Parseval.  The paper attributes the observation to
G. H. Hardy and J. E. Littlewood, *Notes on the Theory of Series (XIX): A
Problem Concerning Majorants of Fourier Series*, Quarterly Journal of
Mathematics 6 (1935), 304--315,
[DOI 10.1093/qmath/os-6.1.304](https://doi.org/10.1093/qmath/os-6.1.304).

Consequently, the fact that coefficient phases can change a sixth moment,
and that the all-positive Dirichlet choice is a majorant for fixed
magnitudes, is `VERIFIED_CLASSICAL`.  R0.73R's exact formula

\[
 \|f_j\|_6^6
 =\sum_{m=1}^3\left\|
   \sum_{r=1}^3A_{j,r}*\widetilde A_{j,r}*A_{j,m}
  \right\|_{\ell^2}^2
 \tag{5.1}
\]

is the vector-valued finite-convolution form of that even-moment expansion.
It is `INTERNAL_EXACT` as a certificate implementation, not a new majorant
principle.

## 6. Rudin--Shapiro provenance and the safe claim

**Original source record.** Walter Rudin, *Some Theorems on Fourier
Coefficients*, Proceedings of the American Mathematical Society 10 (1959),
855--859,
[official AMS scan](https://www.ams.org/journals/proc/1959-010-06/S0002-9939-1959-0116184-5/S0002-9939-1959-0116184-5.pdf),
[DOI 10.1090/S0002-9939-1959-0116184-5](https://doi.org/10.1090/S0002-9939-1959-0116184-5).
The official bibliographic record was verified; automated extraction of the
1959 scan was not available in this pass, so no page-specific claim is
reconstructed from it.

**Inspected accessible source.** Paul Balister, *Bounds on Rudin--Shapiro
Polynomials of Arbitrary Degree* (2019),
[author PDF](https://www.memphis.edu/msci/people/pbalistr/shapiro.pdf),
[arXiv:1909.08777](https://arxiv.org/abs/1909.08777).
Proposition 4 records the complementary identity and its square-root
supremum consequence for dyadic Rudin--Shapiro polynomials.  In the notation
of R0.73R this is

\[
 |P_m(e^{ix})|^2+|Q_m(e^{ix})|^2=2m,
 \qquad \|P_m\|_\infty\le\sqrt{2m}.
 \tag{6.1}
\]

The recursion, \(\pm1\) coefficients, common support, and bound (6.1) are
therefore `VERIFIED_CLASSICAL`; they also follow by a short induction from
the displayed recursion.  The exact carrier construction, its normalization,
the sixth-moment constant, and its embedding as a divergence-free torus field
are not attributed to these sources.

## 7. What remains an internal exact package

The following claims are established, if the independent certificate seals
the displayed calculations, by finite algebra rather than by a promoted
literature theorem:

1. the component-safe triple-convolution identity (5.1);
2. the support-cardinality and triple-additive-multiplicity bounds;
3. the exact Dirichlet value
   \(\|D_m\|_6^6=(11m^5+5m^3+4m)/20\);
4. the carrier identity
   \(\|W_{R,m}\|_6^6=(5/(2m^6))\|R_m\|_6^{12}\);
5. the matched real divergence-free fields with identical support,
   coefficient magnitudes, and every quadratic Fourier-weighted norm;
6. their \(m^{2/3}\) heat-trace ratio and the scaled separation;
7. the exact cancellation
   \((e_3g(x_1,x_2)\cdot\nabla)e_3g=0\).

These are `INTERNAL_EXACT`.  They form a useful reproducible example and
certificate hierarchy.  They do not establish that the packaging is new.

The targeted searches included the exact pairs “Rudin--Shapiro” with
“Navier--Stokes,” “divergence-free torus,” “heat flow,” and
“Dirichlet/Rudin--Shapiro Besov.”  No source containing the same
Navier--Stokes tensor pair surfaced.  The search did surface extensive
classical literature on Rudin--Shapiro norms and the Hardy--Littlewood
majorant problem.  The correct release statement is therefore “local exact
construction; no direct collision found in this bounded pass; no novelty or
priority claim.”

## 8. Open boundary and stop rule

The [Clay Mathematics Institute's current Navier--Stokes problem
page](https://www.claymath.org/millennium/Navier-Stokes-Equation/) still
states that the basic three-dimensional existence and uniqueness question
has no proof.  R0.73R does not change that status.

In particular, the following remain `OPEN` in this release:

- deriving the R0.73Q entrance from \(L^2\) smallness alone, uniformly over
  arbitrary three-dimensional data;
- removing the fixed a priori global reference orbit;
- arbitrary-data global regularity or a Clay conclusion.

Failure of the sufficient certificate is a different matter: it cannot, by
itself, imply blow-up or instability, because the `INTERNAL_EXACT` matched
family has zero nonlinearity and remains globally smooth even on the branch
that stays outside a small heat ball.  This is a proved exclusion, not an
open research claim.

The broad search stops here because the three consequential classical slots
have direct sources: caloric Besov characterization, critical-space
stability, and even-exponent phase majorization/Rudin--Shapiro bounds.  A
further search would be justified only by a precise priority claim, a journal
referee's requested comparison, or a concrete mathematical collision not
covered by the sources above.
