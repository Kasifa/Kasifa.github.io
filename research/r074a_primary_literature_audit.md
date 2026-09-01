# R0.74A — bounded primary-source literature collision audit

**Audit date:** 2026-09-01

**Status:** `COMPONENT_COLLISIONS_FOUND + EXACT_COMBINATION_NOT_LOCATED_IN_BOUNDED_SEARCH`

**Claim class:** literature boundary; not a priority proof

**Related analytic note:** `r074a_localized_kd_size_lemma.md`

This note records a bounded, two-wave search for primary-source collisions
with the R0.74A localized size lemma.  The object checked was

\[
 \mathcal K_D(z_0,R;\theta)
 =\frac\nu{R^2}\int_{I_R}\int_0^{\theta R^2}\int_{B_R}
 D_s\sqrt{k_s}\,dx\,ds\,dt,
\tag{0.1}
\]

where

\[
 D_s=P_s|\nabla u|_F^2-|\nabla P_su|_F^2,
 \qquad
 k_s=\frac12\left(P_s|u|^2-|P_su|^2\right).
\tag{0.2}
\]

The full combination also includes the core/exterior Gaussian
majorization and the paired annular controls

\[
 \mathop{\rm ess\,sup}_{t\in I_R}
 \frac1R\sum_{m\ge1}\gamma_m(\theta)
 \int_{A_m(R)}|u(t)|^2
\tag{0.3}
\]

and

\[
 \frac\nu R\int_{I_R}\sum_{m\ge1}\gamma_m(\theta)
 \int_{A_m(R)}|\nabla u(t)|^2\,dt.
\tag{0.4}
\]

The conclusion is narrow.  The components of this construction have strong
precedents.  I did not locate the exact complete combination in the bounded
search described below.  That negative search result is not evidence of
priority and is not a proof of novelty.

---

## 1. Search scope and stopping rule

I used at most two search waves.

### Wave 1 — component discovery

The first wave covered these source families:

1. positive covariance for nonnegative filters;
2. carré-du-champ and heat-semigroup variance identities;
3. Gaussian filter width as a heat-time variable;
4. exact subfilter-stress evolution and gradient-product representations;
5. heat-semigroup Besov and oscillation seminorms;
6. suitable local energy and localized dissipation;
7. weighted \(L^2\), uniformly local energy, and Wiener-amalgam local
   energy solutions;
8. Gaussian off-diagonal and annular localization;
9. subgrid kinetic-energy closures using \(\sqrt{k_{\rm sgs}}\).

### Wave 2 — exact-combination checks

The second wave used formula and terminology variants for:

- \(D_s\sqrt{k_s}\);
- heat or Gaussian gradient covariance multiplied by the square root of
  velocity covariance;
- gradient variance multiplied by subgrid or subfilter kinetic energy;
- \(\sqrt{k_{\rm sgs}}\) multiplied by gradient variance;
- a mixed heat-semigroup square function with the same heat time in both
  factors;
- Gaussian annuli combined with an
  \(L_t^\infty L_x^2\) exterior energy tail;
- a paired time-integrated annular \(H_x^1\) or gradient-energy tail;
- a local cylinder and scale integral carrying the same \(\nu/R^2\)
  normalization.

I stopped after the second wave because the remaining results repeated the
same component sources or moved to unrelated uses of the notation.  The
search did not exhaust monographs, all forward and backward citation chains,
doctoral theses, non-English literature, or every inaccessible full text.

Only original papers, official journal pages, arXiv records, and author or
institutional copies are used below.  No search-results page is cited.

---

## 2. Primary-source provenance

### 2.1 Positive filter covariance and realizability

**Source.** A. W. Vreman, B. J. Geurts, and J. G. M. Kuerten,
“Realizability conditions for the turbulent stress tensor in large-eddy
simulation,” *Journal of Fluid Mechanics* **278** (1994), 351--362,
DOI 10.1017/S0022112094003745.
[Institutional record](https://research.tue.nl/en/publications/realizability-conditions-for-the-turbulent-stress-tensor-in-large/)

**Supported.** The paper establishes realizability conditions for filtered
turbulent stress and identifies positivity of the filter as the relevant
condition.  Gaussian and top-hat filters belong to the positive-filter
class.  This directly precedes the nonnegativity of a trace covariance such
as \(k_s\).

**Not supported.** The paper does not state the mixed observable
\(D_s\sqrt{k_s}\), its heat-scale integral, the R0.74A local cylinder, or
the two exterior tails in (0.3)--(0.4).

**Collision class:** `DIRECT_COMPONENT_COLLISION`.

### 2.2 Carré du champ and diffusion-semigroup geometry

**Source.** Michel Ledoux, “The geometry of Markov diffusion generators,”
*Annales de la Faculté des sciences de Toulouse* **9** (2000), no. 2,
305--366.
[Official Numdam text](https://numdam.org/item/AFST_2000_6_9_2_305_0/)

**Supported.** The paper develops the Markov diffusion and carré-du-champ
framework in which semigroup variance, gradient estimates, and Poincaré-type
inequalities are standard objects.  It supplies the correct general setting
for quantities of the form
\(P_s(f^2)-(P_sf)^2\) and for comparing
\(\Gamma(P_sf)\) with \(P_s\Gamma(f)\).

**Not supported.** It does not identify the product of a velocity variance
and a gradient variance as a named seminorm, and it does not give the
Navier--Stokes localization or annular tail theorem in R0.74A.

**Collision class:** `DIRECT_COMPONENT_COLLISION`.

### 2.3 Exact Gaussian scale evolution of subfilter stress

**Source.** Perry L. Johnson, “Energy transfer from large to small scales
in turbulence by multi-scale nonlinear strain and vorticity interactions,”
submitted 1 December 2019; *Physical Review Letters* **124** (2020),
104501, DOI 10.1103/PhysRevLett.124.104501.
[arXiv record](https://arxiv.org/abs/1912.00293)
and [full HTML manuscript](https://arxiv.org/html/1912.00293v1).

**Supported.** Equations (7)--(10) use a Gaussian filter, identify squared
filter width as a diffusion-time variable, derive a forced diffusion
equation for the subfilter stress, and give an exact scale integral of
filtered velocity-gradient products.  The trace of the stress is subfilter
kinetic energy.  This is a direct collision with the Gaussian scale-flow
and gradient-product components used in R0.74A.

**Not supported.** Johnson's small-scale molecular dissipation is expressed
through strain covariance, whereas \(D_s\) in (0.2) is the full velocity-
gradient covariance.  The paper does not multiply that covariance by
\(\sqrt{k_s}\), integrate the product over the same positive heat scale, or
derive the R0.74A exterior tails.

**Collision class:** `DIRECT_COMPONENT_COLLISION`.

### 2.4 Generalized central moments and multiple filtering

**Source.** Massimo Germano, “Turbulence: the filtering approach,”
*Journal of Fluid Mechanics* **238** (1992), 325--336; received
16 July 1990 and revised 21 October 1991.
[Author-hosted/classic-paper copy](https://www.ams.jhu.edu/~eyink/Turbulence/classics/Germano92.pdf)

**Supported.** The paper defines generalized central moments and proves
exact identities for stresses at multiple filter levels.  It also explains
the local extraction of resolved energy, production, and dissipation across
filter levels.

**Not supported.** It does not give the positive four-block majorization,
the mixed covariance product, or the annular-tail bound in R0.74A.

**Collision class:** `DIRECT_COMPONENT_COLLISION`.

### 2.5 Heat-semigroup Besov classes

**Source.** Patricia Alonso-Ruiz, Fabrice Baudoin, Li Chen, Luke Rogers,
Nageswari Shanmugalingam, and Alexander Teplyaev,
“Besov class via heat semigroup on Dirichlet spaces I: Sobolev type
inequalities,” submitted 10 November 2018, revised 30 April 2020;
accepted for the *Journal of Functional Analysis*.
[arXiv:1811.04267](https://arxiv.org/abs/1811.04267)

**Supported.** The paper introduces heat-semigroup Besov classes on general
Dirichlet spaces, studies heat-kernel oscillation seminorms, and proves
quantitative regularization and \(L^p\) Sobolev-type estimates for
\(p\ge1\).  It is a strong structural precedent for measuring oscillation
through a heat semigroup.

**Not supported.** The standard construction uses one \(p\)-increment or
one semigroup oscillation with its scale weight.  It does not state a
product of two quadratic covariances, one applied to \(u\) and one to
\(\nabla u\), with the exponents in (0.1).  No direct norm equivalence with
\(D_s\sqrt{k_s}\) was located.

**Collision class:** `STRUCTURAL_COMPONENT_COLLISION`.

### 2.6 Suitable local energy

**Source.** Luis Caffarelli, Robert Kohn, and Louis Nirenberg,
“Partial regularity of suitable weak solutions of the Navier--Stokes
equations,” *Communications on Pure and Applied Mathematics* **35**
(1982), 771--831, DOI 10.1002/cpa.3160350604.
[Official DOI page](https://doi.org/10.1002/cpa.3160350604)

**Supported.** The suitable local energy inequality and its scale-critical
kinetic-energy and dissipation inputs are classical.  These are the
underlying local quantities used in the core--core estimate of R0.74A.

**Not supported.** Caffarelli--Kohn--Nirenberg does not contain the Gaussian
covariance observable, the heat-scale integral, or the paired annular
tails.  R0.74A is not a new local-energy principle; it is a particular
semigroup size estimate built from established local-energy inputs.

**Collision class:** `DIRECT_COMPONENT_COLLISION`.

### 2.7 Wiener-amalgam local energy

**Source.** Zachary Bradshaw and Tai-Peng Tsai, “Local energy solutions to
the Navier--Stokes equations in Wiener amalgam spaces,” submitted
20 August 2020.
[arXiv:2008.09204](https://arxiv.org/abs/2008.09204)

**Supported.** The paper constructs local-energy solutions in classes based
on \(L^2\) Wiener amalgam spaces.  These spaces interpolate between the
finite-energy Leray class and infinite-energy local-solution classes, and
they explicitly track spatially distributed local \(L^2\) energy.

**Not supported.** The paper does not use the precise super-exponential
Gaussian dyadic weight \(\gamma_m(\theta)\), and it does not pair an
essential time supremum of annular velocity energy with the specific
time-integrated annular gradient tail generated by (0.1).

**Collision class:** `STRONG_STRUCTURAL_NEIGHBOR`.

### 2.8 Weighted energy solutions

**Source.** Pedro Gabriel Fernández-Dalgo and
Pierre Gilles Lemarié-Rieusset, “Weighted energy estimates for the
incompressible Navier--Stokes equations and applications to axisymmetric
solutions without swirl,” submitted 2 October 2020.
[arXiv:2010.00868](https://arxiv.org/abs/2010.00868)

**Supported.** The paper develops suitable weak solutions and energy
estimates in weighted \(L^2\) spaces.  It confirms that weighted exterior
energy bookkeeping is an established Navier--Stokes technique.

**Not supported.** Its weights and theorems are not the Gaussian annular
pair in (0.3)--(0.4), and the paper does not derive those tails from the
mixed covariance observable.

**Collision class:** `STRONG_STRUCTURAL_NEIGHBOR`.

### 2.9 SGS kinetic-energy velocity scale

**Source.** Akira Yoshizawa and Kiyosi Horiuti,
“A Statistically-Derived Subgrid-Scale Kinetic Energy Model for the
Large-Eddy Simulation of Turbulent Flows,” *Journal of the Physical Society
of Japan* **54** (1985), 2834--2839; received 17 January 1985 and published
15 August 1985, DOI 10.1143/JPSJ.54.2834.
[Official J-STAGE page](https://www.jstage.jst.go.jp/article/jpsj1946/54/8/54_8_2834/_article/-char/en)

**Supported.** The paper derives a one-equation SGS kinetic-energy model in
which generalized SGS eddy viscosity is expressed using SGS kinetic energy
and a characteristic grid width.  This is the classical modeling precedent
for treating \(\sqrt{k_{\rm sgs}}\) as an unresolved velocity scale next to
gradient-based stress or dissipation terms.

**Not supported.** This is a closure model.  It does not use the exact full-
gradient covariance \(D_s\), and it does not prove a positive heat-scale
functional or a localized energy-class estimate.

**Collision class:** `MODEL_HEURISTIC_COLLISION`.

### 2.10 Dissipation conditioned on SGS kinetic energy

**Source.** Charles Meneveau and John O'Neil, “Scaling laws of the
dissipation rate of turbulent subgrid-scale kinetic energy,”
*Physical Review E* **49** (1994), 2866; published 1 April 1994,
DOI 10.1103/PhysRevE.49.2866.
[Official APS page](https://journals.aps.org/pre/abstract/10.1103/PhysRevE.49.2866)

**Supported.** The paper studies the dissipation term in the SGS kinetic-
energy transport equation, its moments, and the expected dissipation
conditioned on local SGS energy.  It is a close physical precedent for
placing subgrid energy and dissipation in the same analysis.

**Not supported.** It is a statistical and modeling analysis rather than a
deterministic Gaussian-semigroup identity.  It does not give the
\(D_s\sqrt{k_s}\) functional or the R0.74A tail theorem.

**Collision class:** `MODEL_HEURISTIC_COLLISION`.

---

## 3. Collision matrix

| R0.74A item | Collision assessment | Confidence | Precise boundary |
|---|---|---:|---|
| Nonnegative velocity covariance \(k_s\) | direct component collision | high | positive-filter stress realizability and semigroup variance are established |
| Nonnegative gradient covariance \(D_s\) | direct component collision | high | carré-du-champ and Gaussian gradient covariance are established |
| Gaussian heat-scale evolution | direct component collision | very high | Johnson gives the exact stress scale equation and integral representation |
| Local energy and integrated gradient energy | direct component collision | very high | suitable local energy is classical |
| Heat-kernel oscillation/Besov framework | structural collision | high | standard seminorms do not have the mixed product in (0.1) |
| \(\sqrt{k_{\rm sgs}}\) as a velocity scale | model-form collision | high | classical LES closure, not an exact analytic covariance theorem |
| Spatially distributed or weighted \(L^2\) energy | structural collision | high | Wiener-amalgam and weighted-energy theories are established |
| Gaussian dyadic annulus estimate | standard kernel component | high | off-diagonal Gaussian decay is standard; the frozen \(\gamma_m\) is bookkeeping |
| Exact \(D_s\sqrt{k_s}\) heat-scale functional | not located in the bounded search | medium-low | no priority inference is permitted |
| Exact pair (0.3)--(0.4) generated by the four-block proof | not located in the bounded search | medium-low | neighboring weighted/local-energy theories use different weights and pairings |
| Complete R0.74A theorem with local cylinder and \(\nu/R^2\) normalization | not located in the bounded search | medium-low | the search was not exhaustive |

---

## 4. Non-equivalences that must remain explicit

### 4.1 Full gradient versus symmetric strain

Johnson's small-scale molecular dissipation uses covariance of the
symmetric strain tensor.  R0.74A uses covariance of the full matrix
\(\nabla u\).  The two quantities are not pointwise identical.  A citation
to Johnson supports the Gaussian mechanism, not an identity with \(D_s\).

### 4.2 Exact covariance versus LES closure

The Yoshizawa--Horiuti construction models SGS stress using SGS kinetic
energy and a grid length.  R0.74A evaluates exact heat covariances of the
unfiltered field and then proves an inequality.  A closure formula cannot
be cited as the proof of that inequality.

### 4.3 Mixed quadratic covariances versus a cubic increment

In general,

\[
 \bigl(\mathbb E|X|^2\bigr)
 \bigl(\mathbb E|Y|^2\bigr)^{1/2}
 \ne \mathbb E\bigl(|X|^2|Y|\bigr)
\tag{4.1}
\]

and it is not a single third moment.  Therefore a \(p=3\) heat-Besov
seminorm is not algebraically identical to \(D_s\sqrt{k_s}\).  Hölder or
Cauchy--Schwarz may give inequalities when the required moments exist, but
that is not a direct norm equivalence.

### 4.4 Distributed local energy versus the frozen annular pair

Weighted \(L^2\) and Wiener-amalgam theories establish that spatially
distributed energy can be propagated.  They do not automatically give the
same Gaussian weight, the same essential time supremum, or the same
gradient-tail pairing as (0.3)--(0.4).

### 4.5 Component algebra versus the complete theorem

Standard covariance positivity, Gaussian kernel decay, ultracontractivity,
and local energy together explain all ingredients of the R0.74A proof.
Their existence does not by itself imply that the complete four-block
estimate has already appeared in the same form.  Conversely, failure to
locate that form does not establish that it has not appeared.

---

## 5. Exact-combination negative-search boundary

The second wave did not locate a primary source that simultaneously keeps
all of the following:

1. the same heat time \(s\) in both covariances;
2. the full-gradient covariance \(D_s\);
3. the velocity covariance to the power \(1/2\);
4. the \(dx\,ds\,dt\) integration over
   \(B_R\times(0,\theta R^2)\times I_R\);
5. the normalization \(\nu/R^2\);
6. a core/exterior decomposition of the Gaussian input;
7. an \(L_t^\infty L_x^2\) Gaussian annular velocity tail;
8. a time-integrated Gaussian annular gradient-energy tail;
9. the factorized local size bound proved in R0.74A.

This record means only that the exact combination was not found in the
declared search.  It does not mean that the combination is absent from the
literature.  It does not establish novelty, authorship priority, or a right
to use “first.”

---

## 6. Novelty-safe wording

The following wording is supported by this audit:

> R0.74A combines classical positive Gaussian covariances, standard heat-
> kernel off-diagonal estimates, and standard local-energy inputs into a
> localized four-block size bound.  Closely related LES models use the
> square root of subgrid kinetic energy as a velocity scale, while weighted
> and Wiener-amalgam Navier--Stokes theories track spatially distributed
> \(L^2\) energy.  In a bounded two-wave primary-source audit, I did not
> locate the same mixed covariance functional together with the same
> Gaussian annular velocity and gradient tails.  This is a limited
> non-collision finding, not a claim of novelty or priority.

The following statements are not supported:

- “This is the first mixed Gaussian covariance functional.”
- “No equivalent theorem exists.”
- “The annular tail pair is new.”
- “The literature search proves priority.”

---

## 7. Audit status

### `COMPONENT_COLLISIONS_FOUND`

All main analytic ingredients have primary-source precedents.

### `EXACT_COMBINATION_NOT_LOCATED_IN_BOUNDED_SEARCH`

No source with the full nine-part combination in Section 5 was located in
the two declared waves.

### `NOT_A_PRIORITY_PROOF`

The search was bounded and incomplete.  This note must not be used as a
novelty certificate.

### `NOT_CLAY`

This literature audit has no regularity implication.
