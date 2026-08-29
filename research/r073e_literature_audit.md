# R0.73E primary-source literature boundary audit

**Date:** 2026-08-30

**Scope:** fixed-positive-half-plane spectral splitting, a family-uniform
complementary semigroup estimate, and logarithmic-time transfer for the exact
drifting profile

**Evidence class:** bounded primary-source audit; not an originality or priority
claim

## 1. Audit rule

This note asks three separate questions for each source:

1. What does the cited source actually prove, in its own operator class and
   topology?
2. Which step is instead proved inside R0.73E for the specific family
   \(B_\varepsilon=M+K-\varepsilon L\)?
3. What conclusion is not licensed by either comparison?

Only original papers, author manuscripts, books, and official publisher pages
are used.  The search is deliberately bounded to the operator-theoretic and
hydrodynamic-stability precedents needed to interpret R0.73E.  It is not an
exhaustive search of all vanishing-viscosity, pseudospectral, or nonautonomous
semigroup literature.

The central boundary is this.  Literature precedent can identify the correct
kind of theorem, but it does not supply the uniform constants for this singular
family.  Those constants must come from the model-specific high-frequency
resolvent estimate, compact Fredholm reduction, contour argument, and Volterra
calculation written in `research/r073e_halfplane_transfer_proof.md`.

This file audits attribution and scope, not the correctness of that internal
proof.  “R0.73E proves” below means “the R0.73E proof manuscript supplies this
step rather than importing it from the cited source”; final theorem status still
depends on the separate analytic audit and certificate gate.

## 2. Audit matrix

| Source family | What the primary source supplies | What R0.73E must supply itself | Forbidden inference |
|---|---|---|---|
| Shvydkoy--Friedlander | inviscid-limit convergence of unstable eigenvalues, algebraic multiplicities, and spectral subspaces beyond the Euler essential spectrum | operator-norm convergence of the total fixed-half-plane Riesz projection and a no-pollution result for this \(M+K-\varepsilon L\) family | treating their projection statement as an explicit operator-norm theorem, or importing their torus PDO theorem without verifying its hypotheses |
| Kato perturbation theory | the general contour and separated-spectrum framework under an appropriate operator-convergence hypothesis | the actual compact-sandwich norm convergence despite the singular change \(D(B_\varepsilon)=H^2\to H\) | saying that abstract perturbation theory automatically proves norm-resolvent convergence here |
| Engel--Nagel | memberwise spectral mapping and spectral-bound/growth-bound facts for analytic semigroups | constants uniform in \(\varepsilon\), including the complementary prefactor | inferring a family-uniform estimate from the fact that every fixed viscous member is analytic |
| Gearhart--Prüss | a Hilbert-space stability criterion based on resolvent control on a complete half-plane or vertical line | the uniform reduced resolvent on \(b+i\mathbb R\), its \(O(|\tau|^{-1})\) tail, and a common short-time bound | replacing a full-line uniform estimate by a local contour bound or a spectral gap |
| Li--Lin | unstable oscillatory shears, slow Navier--Stokes drift, and frozen Orr--Sommerfeld eigenvalue convergence | a genuine evolution-family lower bound for the exact drifting profile on \(M\log(1/\varepsilon)\) fast time | reading a frozen eigenvalue as a moving-profile amplification theorem |
| Grenier--Nguyen | an inviscid-uniform semigroup estimate for a stationary no-slip half-space shear in boundary-layer norms | the periodic kinetic-vorticity-space estimate and its compact-plus-dissipative proof | transferring their boundary-layer result to the present periodic row or moving profile |
| Kato--Schmid adiabatic theory | transport of spectral subspaces under slow variation, subject to spectral, regularity, well-posedness, and domain assumptions | the bounded-drift Duhamel argument that avoids a moving Riesz projection | assuming slow coefficient drift alone gives adiabatic transport for this singular dissipative family |
| Latushkin--Schnaubelt; Popescu | characterizations and roughness of an already defined exponential dichotomy for an evolution family or cocycle | the frozen relative dichotomy and the direct finite-time Volterra transfer used here | deriving a nonautonomous dichotomy from pointwise frozen spectra alone |

## 3. Shvydkoy--Friedlander: inviscid spectral convergence

**Primary source.** Roman Shvydkoy and Susan Friedlander, *The unstable
spectrum of the Navier--Stokes operator in the limit of vanishing viscosity*,
Annales de l'Institut Henri Poincaré C 25 (2008), 713--724,
[DOI 10.1016/j.anihpc.2007.05.004](https://doi.org/10.1016/j.anihpc.2007.05.004),
[publisher-hosted full text](https://ems.press/journals/aihpc/articles/4076495).

### What the source actually proves

The paper studies linearized Euler and Navier--Stokes operators on the torus.
Its high-/low-frequency decomposition is used to show precise convergence of
viscous eigenvalues to inviscid eigenvalues beyond the essential spectral
radius.  Theorem 2.1 preserves total algebraic multiplicity inside a small
circle and states convergence of the associated sum of Riesz projections.

The topology needs careful wording.  In the proof, the semigroups and the
relevant resolvents are first shown to converge in the strong operator
topology.  Formula (4.17) is then inserted into the contour formula (4.18), and
dominated convergence is invoked.  Neither Theorem 2.1 nor that step explicitly
labels the projection limit as operator-norm convergence.  The safe citation is
therefore: spectral-subspace/Riesz-projection convergence with preservation of
algebraic multiplicity, based on strong convergence plus uniform contour
bounds.  This audit does not upgrade that statement to norm topology.

### What R0.73E proves for its own family

R0.73E does not cite the paper as a black-box proof.  For the one-dimensional
family \(B_\varepsilon=M+K-\varepsilon L\), it writes

\[
G_\varepsilon(z)-R_\varepsilon(z)
  =G_\varepsilon(z)K R_\varepsilon(z),
\]

uses compactness of \(K\) and strong convergence of the base resolvents and
their adjoints, and obtains operator-norm convergence of the compact sandwich
on each contour.  The analytic base-resolvent integral vanishes.  This gives

\[
\|\Pi_{\varepsilon,b}-\Pi_{0,b}\|\to0
\]

for the total spectrum in every fixed admissible positive half-plane.  Separate
high-imaginary and high-real-part estimates then exclude additional viscous
spectrum outside the continued inviscid clusters.

### What cannot be inferred

- The 2008 paper is not evidence that every singular viscous perturbation has
  norm-convergent Riesz projections.
- Its theorem does not provide the reduced half-plane resolvent bound used in
  R0.73E, nor a family-uniform complementary semigroup prefactor.
- Neither result is a statement at the boundary
  \(\operatorname{Re}z=0\), and neither is uniform as \(b\downarrow0\).

## 4. Kato: separated spectra under operator perturbation

**Primary source.** Tosio Kato, *Perturbation Theory for Linear Operators*,
2nd ed., Springer, 1995,
[DOI 10.1007/978-3-642-66282-9](https://doi.org/10.1007/978-3-642-66282-9).

### What the source actually proves

Kato develops the general Riesz-projection calculus and stability of separated
parts of the spectrum under suitable perturbations of bounded or closed
operators.  In the closed-operator setting, graph/gap or resolvent convergence
is the substantive input: once a separating contour remains in the resolvent
set with the required convergence, spectral projections and finite spectral
blocks can be compared.

### What R0.73E proves for its own family

The viscous operators have domain \(H^2_{\rm per}\), while the inviscid limit is
bounded on all of \(H\).  R0.73E therefore verifies the needed convergence on
the chosen contours directly.  It combines dissipative base-resolvent bounds,
compactness of \(K\), Fredholm factorization, and explicit control of the
unbounded part of the half-plane.  It also proves

\[
\|B_\varepsilon\Pi_{\varepsilon,b}
  -A_0\Pi_{0,b}\|\to0
\]

by integrating \(zG_\varepsilon(z)\) after subtracting the analytic base term.

### What cannot be inferred

- The formal expression \(-\varepsilon L\to0\) does not itself imply
  operator-norm convergence because \(L\) is unbounded.
- Kato's general framework does not by itself control the whole unbounded
  half-plane or give a semigroup estimate uniform in viscosity.
- No moving-domain or graph-norm transport theorem has been verified for the
  exact time-dependent family in R0.73E; that remains outside the claim.

## 5. Engel--Nagel: analytic semigroups and growth bounds

**Primary source.** Klaus-Jochen Engel and Rainer Nagel, *One-Parameter
Semigroups for Linear Evolution Equations*, Springer, 2000,
[DOI 10.1007/b97696](https://doi.org/10.1007/b97696),
[author-hosted text](https://www.math.uni-tuebingen.de/de/forschung/agfa/members/engel-nagel_one-parameter-semigroups.pdf).

### What the source actually proves

Corollary IV.3.12 gives spectral mapping and equality of spectral and growth
bounds for several memberwise regularity classes, including analytic
semigroups.  This is a theorem about a fixed semigroup.  The growth bound is an
asymptotic infimum over admissible exponents; the result does not supply one
prefactor that is uniform across a singular parameter family.

### What R0.73E proves for its own family

R0.73E first obtains a common crude estimate

\[
\|e^{tB_\varepsilon}\|\le e^{\|K\|t}
\]

from maximal dissipativity of \(M-\varepsilon L\) and bounded perturbation by
\(K\).  It then derives a uniform reduced resolvent on an entire vertical line,
shifts the inverse-Laplace contour, and integrates once by parts.  This yields a
common complementary prefactor \(C_b\) in

\[
\|e^{tB_\varepsilon}Q_\varepsilon^{\rm top}\|
  \le C_b e^{bt}.
\]

### What cannot be inferred

- Analyticity of every \(e^{tB_\varepsilon}\) does not imply
  \(\sup_\varepsilon C_{b,\varepsilon}<\infty\).
- Equality of spectral and growth bounds does not rule out parameter-dependent
  transient growth.
- A spectral gap without a uniform resolvent bound is insufficient for the
  family estimate required here.

## 6. Gearhart--Prüss: resolvent control must cover the full line

**Primary sources.** Larry Gearhart, *Spectral theory for contraction
semigroups on Hilbert space*, Transactions of the AMS 236 (1978), 385--394,
[DOI 10.1090/S0002-9947-1978-0461206-1](https://doi.org/10.1090/S0002-9947-1978-0461206-1);
Jan Prüss, *On the spectrum of \(C_0\)-semigroups*, Transactions of the AMS
284 (1984), 847--857,
[DOI 10.1090/S0002-9947-1984-0743749-9](https://doi.org/10.1090/S0002-9947-1984-0743749-9),
[AMS issue page](https://www.ams.org/journals/tran/1984-284-02/).

### What the sources actually prove

The Hilbert-space Gearhart--Prüss criterion links uniform exponential
stability to resolvent control on the whole right half-plane; equivalently,
after shifting the generator, one controls a complete vertical line.  The
Engel--Nagel formulation makes the nonlocal requirement explicit:

\[
\sup_{\operatorname{Re}\lambda>0}
\|R(\lambda,A)\|<\infty.
\]

Prüss also studies the spectrum of general \(C_0\)-semigroups and dichotomic
projections through solution and resolvent properties.  The relevant lesson is
not a citation shortcut but a hypothesis check: local information near one
eigenvalue is not enough.

### What R0.73E proves for its own family

For each fixed admissible \(b>0\), R0.73E proves

\[
\sup_{0<\varepsilon<\varepsilon_b}
\sup_{\tau\in\mathbb R}
\|(b+i\tau-C_\varepsilon)^{-1}\|<\infty
\]

for the complementary generator \(C_\varepsilon\), and strengthens the tail to
\(O(|\tau|^{-1})\).  The proof covers the unbounded line by three distinct
regions: high imaginary frequency, high real part, and a remaining compact
rectangle.  R0.73E then performs the inverse-Laplace argument directly, rather
than merely naming the abstract theorem.

### What cannot be inferred

- A bounded resolvent on one small Riesz contour cannot replace the complete
  line.
- Pointwise-in-\(\varepsilon\) Gearhart--Prüss bounds do not give a common
  semigroup constant unless the resolvent and short-time estimates are uniform.
- The result is not uniform as the line approaches the essential-spectrum
  boundary \(b=0\).

## 7. Li--Lin: oscillatory shears and the frozen Orr--Sommerfeld limit

**Primary source.** Y. Charles Li and Zhiwu Lin, *A Resolution of the
Sommerfeld Paradox*, SIAM Journal on Mathematical Analysis 43 (2011),
1923--1954,
[DOI 10.1137/100794912](https://doi.org/10.1137/100794912),
[arXiv:0904.4676](https://arxiv.org/abs/0904.4676).

### What the source actually proves

Li--Lin constructs oscillatory shears that approach Couette flow in kinetic
energy but not in enstrophy and proves inviscid linear instability for the
relevant class.  The paper also observes that these shears drift slowly under
Navier--Stokes evolution.  When the slowly drifting shear is frozen, unstable
Orr--Sommerfeld eigenvalues converge to the corresponding inviscid eigenvalues
as Reynolds number tends to infinity.  The paper also treats nearby
three-dimensional shears at the level stated there.

### What R0.73E proves for its own family

R0.73E starts from its separately certified inviscid eigenvalue and proves the
full fixed-positive-half-plane continuation.  It then selects a viscous
eigenvalue from the complete inviscid top cluster.  For the exact heat-decaying
profile, it proves the bounded drift estimate

\[
\|A(d)-A(0)\|\le \frac{49}{4}d
\]

in the unitarily transformed kinetic space and applies Duhamel's formula on
\(T_\varepsilon=M\log(1/\varepsilon)\).  The resulting evolution-family lower
bound is not a frozen-flow statement.

### What cannot be inferred

- Frozen Orr--Sommerfeld eigenvalue convergence does not prove that the exact
  moving profile follows a moving eigenspace.
- Slow drift by itself does not control nonnormal transient amplification or
  the complementary semigroup.
- Li--Lin does not supply the arbitrary-\(M\) logarithmic-time lower bound or
  the super-polynomial operator-norm conclusion of this particular row.

## 8. Grenier--Nguyen: a genuine uniform semigroup precedent in another geometry

**Primary source.** Emmanuel Grenier and Toan T. Nguyen, *Sharp bounds for the
resolvent of linearized Navier Stokes equations in the half space around a
shear profile*, Journal of Differential Equations 269 (2020), 9384--9403,
[DOI 10.1016/j.jde.2020.06.046](https://doi.org/10.1016/j.jde.2020.06.046),
[arXiv:1703.00881](https://arxiv.org/abs/1703.00881).

### What the source actually proves

For a stationary smooth shear layer in a half-plane or half-space, with
Dirichlet no-slip boundary conditions and an unstable Euler eigenvalue,
Theorem 1.1 proves a semigroup bound of the form

\[
\|e^{tL_{\alpha,\nu}}\omega_0\|_{\beta,\gamma}
 \le C_\tau e^{(\operatorname{Re}\lambda_0+\tau)t}
 \|\omega_0\|_{\beta,\gamma},
\]

uniformly for \(0<\nu\le1\) in the paper's boundary-layer norm.  The proof uses
Orr--Sommerfeld Green functions, Evans-function information, resolvent bounds,
and a Laplace-contour representation.  This is a genuine example where the
uniform prefactor is proved rather than inferred from the spectrum.

### What R0.73E proves for its own family

The present periodic row has no no-slip wall and is measured in a kinetic
vorticity Hilbert space.  R0.73E uses the different structure
\(M+K-\varepsilon L\): a skew multiplication operator, a compact perturbation,
and diagonal dissipation.  It derives the vertical-line resolvent and semigroup
bound directly in that setting, then treats the profile drift as bounded
forcing.

### What cannot be inferred

- The half-space boundary-layer estimate does not transfer unchanged to a
  periodic kinetic norm.
- Its stationary generator estimate is not a theorem for the exact moving
  heat profile in R0.73E.
- The source does not identify the present top cluster or prove this row's
  super-polynomial lower law.

## 9. Kato and Schmid: adiabatic transport is not automatic slow drift

**Primary sources.** Tosio Kato, *On the Adiabatic Theorem of Quantum
Mechanics*, Journal of the Physical Society of Japan 5 (1950), 435--439,
[DOI 10.1143/JPSJ.5.435](https://doi.org/10.1143/JPSJ.5.435);
Jochen Schmid, *Adiabatic theorems for general linear operators with
time-independent domains*, Reviews in Mathematical Physics 31 (2019), 1950014,
[DOI 10.1142/S0129055X19500144](https://doi.org/10.1142/S0129055X19500144),
[arXiv:1804.11213](https://arxiv.org/abs/1804.11213);
Jochen Schmid, *Adiabatic theorems for general linear operators with
time-dependent domains*, 2018 preprint,
[arXiv:1804.11255](https://arxiv.org/abs/1804.11255).

### What the sources actually prove

Kato's 1950 argument gives geometric transport of separated spectral
subspaces in the quantum adiabatic setting.  Schmid extends adiabatic results to
general, typically dissipative, operators, including versions with and without
a spectral gap and versions allowing time-dependent domains.  The hypotheses
remain substantive: well-posed evolution, appropriate stability, regularity of
operators or resolvents, and associated spectral projections are part of the
theorem, not consequences of the phrase “slowly varying.”

The bibliographic distinction matters.  The peer-reviewed 2019 article with
DOI 10.1142/S0129055X19500144 is the **time-independent-domain** paper.  The
time-dependent-domain item cited here is arXiv:1804.11255; this audit does not
misassign the journal DOI to that separate preprint.

### What R0.73E proves for its own family

R0.73E does not construct or differentiate a moving Riesz projection.  It
keeps the full unbounded viscous term inside the frozen generator and estimates
only the bounded profile drift:

\[
\|E_\varepsilon(t)\|\le \frac{49}{4}\varepsilon t.
\]

A direct Duhamel--Volterra estimate compares the exact evolution with one
frozen viscous eigenmode on logarithmic fast time.  Thus the proof avoids any
unverified commutator such as \([L,\Pi_0]\) and any graph-domain adiabatic
transport claim.

### What cannot be inferred

- Slow variation does not alone verify Schmid's regularity, stability, or
  projection hypotheses for this singular family.
- Kato's self-adjoint quantum theorem is not a direct theorem for a nonnormal
  Orr--Sommerfeld generator.
- R0.73E does not prove a moving-profile uniform contour theorem, a
  graph-domain Kato transport theorem, or adiabatic following on a fixed
  physical-time interval.

## 10. Latushkin--Schnaubelt and Popescu: nonautonomous dichotomy

**Primary sources.** Yuri Latushkin and Roland Schnaubelt, *Evolution
Semigroups, Translation Algebras, and Exponential Dichotomy of Cocycles*,
Journal of Differential Equations 159 (1999), 321--369,
[DOI 10.1006/jdeq.1999.3668](https://doi.org/10.1006/jdeq.1999.3668),
[author manuscript](https://wwwalt.math.kit.edu/iana3/~schnaubelt/media/aht.pdf);
Liviu Horia Popescu, *Exponential dichotomy roughness and structural stability
for evolution families without bounded growth and decay*, Nonlinear Analysis
71 (2009), 935--947,
[DOI 10.1016/j.na.2008.11.009](https://doi.org/10.1016/j.na.2008.11.009).

### What the sources actually prove

Latushkin--Schnaubelt studies an exponentially bounded, strongly continuous
cocycle over a flow.  Exponential dichotomy is characterized by hyperbolicity
of its associated evolution semigroup and by the imaginary axis lying in the
resolvent of that evolution-semigroup generator.  The paper also proves
persistence under suitable small perturbations of the cocycle.

Popescu starts from an evolution operator that is already exponentially
dichotomic and proves roughness/structural stability for the perturbed Volterra
equation under a smallness condition, without assuming the bounded growth and
decay condition used in earlier roughness results.

### What R0.73E proves for its own family

R0.73E first proves a **frozen relative dichotomy** after shifting by
\(b<\alpha<c<a\): the complement is forward stable relative to the shift, and
the finite top block is backward stable.  It then uses only the full frozen
semigroup upper bound and a single top eigenmode in a finite-time Volterra
comparison.  It does not claim that the exact moving evolution family has a
global exponential dichotomy.

### What cannot be inferred

- A family of frozen spectral gaps does not define an exponential dichotomy for
  a nonautonomous evolution family.
- A roughness theorem cannot create the initial dichotomy or its uniform
  constants; those are hypotheses to be verified.
- R0.73E's logarithmic-time lower bound is not a structural-stability theorem on
  the whole time axis.

## 11. Claim-to-source ledger

| Claim used in this audit | Primary source | Exact use here | Confidence |
|---|---|---|---|
| unstable inviscid eigenvalues, multiplicities, and spectral subspaces persist beyond the essential spectrum | Shvydkoy--Friedlander 2008 | precedent only; projection topology kept conservative | high |
| separated spectral parts are compared through contour resolvents under an adequate operator-convergence hypothesis | Kato 1995 | abstract framework, not a substitute for the model proof | high |
| analytic semigroups satisfy memberwise spectral mapping and \(s(A)=\omega_0\) | Engel--Nagel 2000, Cor. IV.3.12 | explains why memberwise analyticity is insufficient for family uniformity | high |
| Hilbert-space semigroup stability requires complete half-plane/vertical-line resolvent control | Gearhart 1978; Prüss 1984; Engel--Nagel Thm. V.1.11 | hypothesis benchmark for the R0.73E reduced resolvent | high |
| oscillatory Navier--Stokes shears drift slowly, while frozen Orr--Sommerfeld eigenvalues converge inviscidly | Li--Lin 2011 | closest shear-flow motivation; no moving transfer imported | high |
| stationary no-slip half-space shear admits an inviscid-uniform semigroup bound in boundary-layer norms | Grenier--Nguyen 2020, Thm. 1.1 | genuine uniform-semigroup precedent in a different geometry and norm | high |
| adiabatic transport needs spectral, regularity, stability, and evolution hypotheses | Kato 1950; Schmid 2018/2019 | boundary against a shortcut from “slow drift” | high |
| exponential dichotomy is an evolution-family/cocycle property and is rough under suitable small perturbations | Latushkin--Schnaubelt 1999; Popescu 2009 | boundary against pointwise frozen-spectrum inference | high |

## 12. Resulting citation boundary for R0.73E

The sources support the following restrained description:

> R0.73E uses established ideas from inviscid spectral convergence, Riesz
> projection perturbation, resolvent--semigroup theory, and nonautonomous
> stability.  Its fixed-positive-half-plane norm projection theorem, uniform
> reduced-resolvent estimate, relative top-cluster dichotomy, and
> logarithmic-time transfer are proved for the specific periodic family
> \(M+K-\varepsilon L\) inside this project.  No originality or priority claim
> follows from this bounded audit.

The following statements must not appear as literature consequences:

```text
ShvydkoyFriedlanderProjectionNormTopology=NOT_CLAIMED
abstractKatoAutomaticallyHandlesDomainCollapse=FALSE
memberwiseAnalyticityImpliesUniformFamilyPrefactor=FALSE
localContourBoundImpliesComplementSemigroupBound=FALSE
frozenEigenvalueImpliesMovingProfileGrowth=FALSE
halfSpaceBoundaryLayerEstimateTransfersToPeriodicRow=FALSE
slowDriftAloneImpliesAdiabaticFollowing=FALSE
frozenSpectralGapImpliesNonautonomousDichotomy=FALSE
literatureAuditEstablishesPriority=FALSE
literatureAuditClosesNavierStokesMillenniumProblem=FALSE
```

## 13. Search stop condition

The search stopped after each consequential comparison had an original paper,
book, official publisher page, or author manuscript; the projection-topology
ambiguity in Shvydkoy--Friedlander had been checked against the theorem and its
proof; and the uniformity assumptions in the semigroup and nonautonomous
sources had been made explicit.  Further broad searching would be an
originality survey, which is outside this note and would require a separate,
systematic protocol.
