# R0.74B — bounded primary-source literature collision audit

**Audit date:** 2026-09-01

**Status:** `EXACT_HIT_NOT_LOCATED / STRONG_COMPONENT_COLLISIONS_FOUND / BOUNDED_NON_HIT`

**Claim class:** primary-source literature boundary; not a novelty or priority
claim

**Related analytic note:** `r074b_buffered_tail_closure.md`

This note records a bounded primary-source search for collisions with the
R0.74B buffered closure of Gaussian annular energy tails.  I separated the
outcome into three levels:

1. **Exact hit:** the same functionals, hypotheses, quantifiers, scale shift,
   buffered time window, pressure payment, and displayed conclusions.
2. **Strong component collision:** a primary source proves one or more of the
   main mechanisms, but not the complete R0.74B statement.
3. **Bounded non-hit:** no exact hit was located inside the stated search
   boundary.  This is not an exhaustive bibliometric conclusion.

The audit concerns a periodic suitable weak solution, lifted annuli

\[
 A_m(R)=\{2^mR\le |y-\widetilde x_0|<2^{m+1}R\},
 \qquad
 \gamma_m(\theta)=\theta^{-2}
 \exp\!\left(-\frac{4^{m-1}}{32\theta}\right),
\tag{0.1}
\]

the exact doubled-radius identity

\[
 A_k(R)=A_{k-1}(2R),\qquad k\ge2,
\tag{0.2}
\]

and the buffered payment

\[
 P^\square
 =\mathcal E^\square(z_0,8R)^{3/2}
 +\mathcal A_{\rm ext}^\square(z_0,2R;\theta).
\tag{0.3}
\]

The two conclusions checked in the literature search were

\[
 \mathcal U_{\rm ext}^{\infty,\square}
 +\mathcal D_{\rm ext}^{\square}
 \le C_{\nu,\square}
 \bigl[(P^\square)^{2/3}+P^\square\bigr]
\tag{0.4}
\]

and

\[
 \mathcal K_D^\square
 \le C_{\nu,\square}\theta^{1/4}
 \bigl[P^\square+(P^\square)^{3/2}\bigr].
\tag{0.5}
\]

The constants, both clock choices, the essential time supremum, and the
larger-radius pressure payment are part of the exact-hit criterion.  A paper
containing only the powers (2/3) and (3/2) is not an exact hit.

---

## 1. Search scope and stopping rule

I used two search waves.

### Wave 1 — component provenance

The first wave followed primary sources for:

1. suitable weak solutions and the local energy inequality on
   \(\mathbb T^3\);
2. uniformly local and weighted \(L^2\) energy estimates;
3. dyadic cube or Herz-type spatial energy bookkeeping;
4. local/remote and active/harmonic pressure decompositions;
5. backward-Gaussian test functions and annular cutoff errors;
6. nested cylinders, interior time windows, and radius-loss iterations; and
7. finite chains carrying annular leakage, pressure-tail, and
   pressure--flux--energy costs.

### Wave 2 — exact and synonymous formulations

The second wave checked formula and terminology variants for:

- `P^(2/3)+P`, `P^{2/3}+P`, and their local-energy variants;
- `P+P^(3/2)`, `P+P^{3/2}`, with and without a
  \(\theta^{1/4}\) factor;
- `U_gamma`, `D_gamma`, `U_ext`, `D_ext`, and `K_D` together with
  Navier--Stokes, local energy, and annular tails;
- Gaussian, exponential, and superexponential annular weights;
- weights containing \(\theta^{-2}\), \(4^m\), or
  \(\exp(-c4^m/\theta)\);
- buffered or interior time windows, doubled-radius closure, and exact
  dyadic-annulus shifts; and
- the semantic combination periodic suitable solution + weighted annular
  tail + harmonic pressure + scale doubling, without relying on the R0.74B
  notation.

I stopped after the second wave because exact queries had saturated in
repeated component sources or unrelated uses of the symbols.  Every required
component family had at least one inspected primary source, and the closest
2026 finite-chain preprint had been checked against its full arXiv text.

The search was limited to original papers, official publisher pages, official
arXiv records, and author or institutional manuscripts that were directly
accessible.  It did not exhaust monographs, theses, every language, every
forward and backward citation chain, inaccessible full texts, or results
written in an unanticipated notation.

---

## 2. Three-level collision result

### 2.1 Exact hit

**No exact hit was located.**

In particular, I did not locate a primary source containing all of the
following in one theorem or lemma:

- periodic suitability on \(\mathbb T^3\);
- the lifted dyadic annuli and the weight in (0.1);
- the exact shift (0.2);
- a larger interval supporting a cutoff that is one on the target interval;
- local pressure generated at the \(2R\) scale and paid by \(8R\) energy;
- the payment (0.3); and
- both (0.4) and (0.5), with the same functionals and quantifiers.

### 2.2 Strong component collisions

Strong component collisions were located for every broad ingredient:

- periodic suitability and suitable local-energy testing;
- uniformly local and polynomially weighted energy control;
- dyadic spatial classes with local/remote pressure estimates;
- backward-Gaussian localization with errors on an outer annulus;
- nested spatial cylinders and harmonic-pressure influence;
- explicit local/harmonic pressure decompositions; and
- finite-chain ledgers with annular leakage, pressure-tail, and PFE rows.

These precedents mean that R0.74B must not claim a new local-energy
principle, a first weighted energy estimate, a first Gaussian cutoff, or a
first local/harmonic pressure split.

### 2.3 Bounded non-hit

The bounded non-hit is only for the simultaneous R0.74B package.  It leaves
open at least three possibilities: an exact result may use different
notation; the closure may appear as an intermediate estimate rather than a
named theorem; or it may occur in literature outside the search boundary.

---

## 3. Primary-source provenance

### 3.1 Periodic suitability

**Source.** Jean-Luc Guermond, “Finite-element-based Faedo--Galerkin weak
solutions to the Navier--Stokes equations in the three-dimensional torus are
suitable,” *Journal de Mathématiques Pures et Appliquées* **85** (2006),
no. 3, 451--464, DOI 10.1016/j.matpur.2005.10.004.
[Official journal page](https://www.sciencedirect.com/science/article/pii/S0021782405001169)

**Supported.** Guermond proves suitability for a class of Faedo--Galerkin
weak solutions on the three-dimensional torus under discrete commutator and
inf--sup hypotheses.  This is a direct primary-source precedent for periodic
suitability and the local energy inequality in the geometry used by R0.74B.

**Boundary.** The paper is about construction and suitability.  It does not
state a lifted Gaussian annular tail, the exact doubled-radius shift, or the
buffered estimates (0.4)--(0.5).

**Collision class:** `STRONG_COMPONENT_COLLISION`.

### 3.2 Suitable local energy and nested-scale regularity

**Source.** Luis Caffarelli, Robert Kohn, and Louis Nirenberg, “Partial
regularity of suitable weak solutions of the Navier--Stokes equations,”
*Communications on Pure and Applied Mathematics* **35** (1982), no. 6,
771--831, DOI 10.1002/cpa.3160350604.
[Official DOI page](https://doi.org/10.1002/cpa.3160350604)

**Source.** Fang-Hua Lin, “A new proof of the Caffarelli--Kohn--Nirenberg
theorem,” *Communications on Pure and Applied Mathematics* **51** (1998),
no. 3, 241--257, DOI
10.1002/(SICI)1097-0312(199803)51:3<241::AID-CPA2>3.0.CO;2-A.
[Official DOI page](https://doi.org/10.1002/%28SICI%291097-0312%28199803%2951%3A3%3C241%3A%3AAID-CPA2%3E3.0.CO%3B2-A)

**Supported.** These papers establish the suitable local-energy framework
and the classical nested-cylinder iteration behind local scale estimates.

**Boundary.** Neither source contains the Gaussian annular sum in (0.1), the
periodic lift, the payment in (0.3), or either target closure.

**Collision class:** `STRONG_COMPONENT_COLLISION`.

### 3.3 Uniformly local energy

**Source.** Pierre Gilles Lemarié-Rieusset, “Solutions faibles d'énergie
infinie pour les équations de Navier--Stokes dans \(\mathbb R^3\),”
*Comptes Rendus de l'Académie des Sciences, Série I, Mathématique* **328**
(1999), no. 12, 1133--1138, DOI 10.1016/S0764-4442(99)80427-3.
[Official journal page](https://www.sciencedirect.com/science/article/pii/S0764444299804273)

**Supported.** The paper constructs suitable weak solutions for uniformly
locally square-integrable initial data with the stated vanishing-at-infinity
condition.  It is a foundational collision for infinite-energy
\(L^2_{\rm uloc}\) control.

**Boundary.** Uniform local control over translated balls is not the
centered, superexponentially weighted annular functional in R0.74B.

**Collision class:** `STRONG_COMPONENT_COLLISION`.

### 3.4 Weighted \(L^2\) suitable solutions

**Source.** Pedro Gabriel Fernández-Dalgo and Pierre Gilles
Lemarié-Rieusset, “Weak solutions for Navier--Stokes equations with initial
data in weighted \(L^2\) spaces,” *Archive for Rational Mechanics and
Analysis* **237** (2020), no. 1, 347--382, DOI
10.1007/s00205-020-01510-w.
[Author preprint and arXiv record](https://arxiv.org/abs/1906.11038)

**Supported.** The paper obtains global weak solutions with new weighted
energy controls for
\(w_\gamma(x)=(1+|x|)^{-\gamma}\), \(0<\gamma\le2\).  It directly
precedes suitable weighted exterior-energy bookkeeping.

**Boundary.** The weight is polynomial.  The theorem does not use the
superexponential dyadic sequence in (0.1), an exact radius-doubling shift, or
the R0.74B pressure payment.

**Collision class:** `STRONG_COMPONENT_COLLISION`.

**Source.** Pedro Gabriel Fernández-Dalgo and Pierre Gilles
Lemarié-Rieusset, “Weighted energy estimates for the incompressible
Navier--Stokes equations and applications to axisymmetric solutions without
swirl,” *Journal of Mathematical Fluid Mechanics* **23** (2021), no. 3,
article 76, DOI 10.1007/s00021-021-00603-0.
[Author preprint and arXiv record](https://arxiv.org/abs/2010.00868)

**Supported.** The paper develops weighted energy testing for weak suitable
solutions and treats a family of admissible weights, including the
polynomial axisymmetric examples stated in the paper.

**Boundary.** Its weight hypotheses and global weighted spaces are not the
discrete Gaussian annular tail in (0.1).  It does not provide the exact
buffered closure (0.4).

**Collision class:** `STRONG_COMPONENT_COLLISION`.

### 3.5 Dyadic spatial control and near/far pressure

**Source.** Zachary Bradshaw, Igor Kukavica, and Tai-Peng Tsai, “Existence
of global weak solutions to the Navier--Stokes equations in weighted
spaces,” *Indiana University Mathematics Journal* **71** (2022), no. 1,
191--212, DOI 10.1512/iumj.2022.71.8789.
[Author preprint and arXiv record](https://arxiv.org/abs/1910.06929)

**Supported.** The paper works with a scale-dependent cube family and the
weighted classes \(M_{\mathcal C}^{2,q}\).  Its pressure expansion splits a
Calderón--Zygmund near part from a remote kernel difference, and it estimates
the pressure in the same weighted spatial framework.  This is the closest
classical collision combining nonuniform spatial energy bookkeeping with a
local/remote pressure estimate.

**Boundary.** The geometry is \(\mathbb R^3\) and the bookkeeping uses cubes
whose size varies with position.  It is not a lifted annular sum on
\(\mathbb T^3\), does not use the sequence \(\gamma_m(\theta)\), and does
not derive (0.4)--(0.5) from a \(2R\)-to-\(8R\) payment.

**Collision class:** `STRONG_COMPONENT_COLLISION`.

### 3.6 Backward-Gaussian testing and annular cutoff loss

**Source.** Changxing Miao and Yanqing Wang, “Regularity conditions for
suitable weak solutions of the Navier--Stokes system from its rotation
form,” *Pacific Journal of Mathematics* **288** (2017), no. 1, 189--215,
DOI 10.2140/pjm.2017.288.189.
[Official journal PDF](https://msp.org/pjm/2017/288-1/pjm-v288-n1-p10-s.pdf)

**Supported.** The proof inserts the localized backward heat kernel

\[
 [4\pi(\mu^2-t)]^{-3/2}
 \exp\!\left[-\frac{|x|^2}{4(\mu^2-t)}\right]
\]

into the local energy inequality.  The derivative-of-cutoff energy error is
placed on \(Q(\rho)\setminus Q(\rho/2)\), and the resulting estimate is
iterated between nested scales.  This is a direct collision with Gaussian
localization, annular cutoff loss, and radius-buffered iteration.

**Boundary.** The paper uses one localized kernel and one annular cutoff at
a time.  It does not sum the fixed dyadic weight (0.1), use the periodic
annular identity (0.2), or prove the endpoint/dissipation closure (0.4).

**Collision class:** `STRONG_COMPONENT_COLLISION`.

### 3.7 Local-in-space estimates and harmonic pressure influence

**Source.** Hao Jia and Vladimír Šverák, “Local-in-space estimates near
initial time for weak solutions of the Navier--Stokes equations and forward
self-similar solutions,” *Inventiones Mathematicae* **196** (2014), no. 1,
233--265, DOI 10.1007/s00222-013-0468-x.
[Author preprint and arXiv record](https://arxiv.org/abs/1204.0529)

**Supported.** The paper derives local-in-space control on a smaller region
from assumptions on a larger region near the initial time.  It explicitly
identifies the harmonic part of the pressure as the remaining nonlocal
influence and repeatedly uses nested cylinders and interior losses.

**Boundary.** The main purpose is near-initial-time regularity and forward
self-similar existence on \(\mathbb R^3\).  It does not state the R0.74B
weighted tail, the arbitrary interior buffered interval, the exact
\(8R\to2R\to R\) ledger, or the powers in (0.4)--(0.5).

**Collision class:** `STRONG_COMPONENT_COLLISION`.

### 3.8 Explicit local/harmonic pressure decomposition

**Source.** Hi Jun Choe and Minsuk Yang, “Local kinetic energy and
singularities of the incompressible Navier--Stokes equations,” *Journal of
Differential Equations* **264** (2018), no. 2, 1171--1191, DOI
10.1016/j.jde.2017.09.036.
[Author preprint and arXiv record](https://arxiv.org/abs/1705.04561)

**Supported.** The paper writes \(p\psi=p_1+p_2+p_3\), where \(p_1+p_2\)
is generated from localized velocity and cutoff derivatives and \(p_3\) is
harmonic on the smaller ball.  It then estimates the harmonic part using an
outer annulus and an explicit radius gap.

**Boundary.** This is a local pressure and reverse-Hölder argument.  It does
not attach the pressure split to the Gaussian annular energy sum or the
specific \(8R\) energy payment in (0.3).

**Collision class:** `STRONG_COMPONENT_COLLISION`.

**Source.** Jörg Wolf, “On the local pressure of the Navier--Stokes
equations and related systems,” *Advances in Differential Equations* **22**
(2017), nos. 5--6, 305--338; preprint arXiv:1611.01482v1, submitted
4 November 2016.
[Author preprint and arXiv record](https://arxiv.org/abs/1611.01482)

**Supported.** Wolf constructs a local pressure distribution of the form
\(\partial_t\nabla p_h+\nabla p_0\), with a harmonic-pressure projection
and a force-dependent local part.  This is a general primary-source
foundation for local pressure projections in energy estimates.

**Boundary.** The abstract local pressure construction does not give the
R0.74B Gaussian weights, dyadic shift, or quantitative payment (0.3).

**Collision class:** `STRONG_COMPONENT_COLLISION`.

**Source.** Zachary Bradshaw and Tai-Peng Tsai, “On the local pressure
expansion for the Navier--Stokes equations,” arXiv:2001.11526v1 [math.AP],
submitted 30 January 2020.
[Official arXiv record](https://arxiv.org/abs/2001.11526)

**Supported.** The preprint characterizes when the pressure of a
distributional whole-space solution has a local expansion and gives an
explicit BMO solution of the associated Poisson equation.  It is a direct
structural precedent for separating locally generated pressure from the
nonlocal remainder.

**Boundary.** I did not verify a peer-reviewed journal version in this
bounded search.  The preprint does not state the R0.74B buffered annular
closure.

**Collision class:** `STRONG_COMPONENT_COLLISION`.

### 3.9 A 2026 finite-chain near-collision

**Source.** Runlong Yu, “Finite-Chain CKN-Bad Scale Counting for
Navier--Stokes: Standard PDE Closure and Canonical Detector Realization,”
arXiv:2606.21783v1 [math.AP], submitted 19 June 2026, arXiv-issued DOI
10.48550/arXiv.2606.21783.
[Official arXiv record](https://arxiv.org/abs/2606.21783)
and [full arXiv HTML](https://arxiv.org/html/2606.21783)

**Verified publication status.** This is an arXiv v1 preprint.  I did not
locate or verify a journal publication in this audit.

**Supported.** The abstract states a finite-chain counting theorem for CKN
bad scales of suitable weak solutions.  Its standard-cost ledger contains
vertical one-component concentration, annular leakage, pressure-tail terms,
and pressure--flux--energy residuals.  Section 3 defines annular leakage and
the active/harmonic split

\[
 P_k^{\rm act}=R_iR_j(\eta u_{k,i}u_{k,j}),
 \qquad
 P_k^{\rm harm}=p_k-P_k^{\rm act}.
\]

**Necessary qualification.** The paper does **not** prove that small annular
leakage, pressure-tail cost, or PFE residual alone forces CKN smallness.
Remark 5.2 says that the proved standard-PDE theorem closes through the
vertical one-component channel; the other rows are honest nonnegative costs
in the same ledger.  Remark 5.3 labels the stronger PFE closing as open.

**Boundary.** The paper does not use the periodic lifted annuli, the
superexponential weights in (0.1), the exact shift (0.2), or the payment and
powers in (0.3)--(0.5).  It is therefore a strong conceptual near-collision,
not an exact hit and not an independent proof of the R0.74B closure.

**Collision class:** `STRONG_COMPONENT_COLLISION / PREPRINT`.

---

## 4. Precise difference matrix

| Literature family | What the source establishes | Difference from R0.74B | Why it is not an exact hit |
|---|---|---|---|
| Bradshaw--Kukavica--Tsai (2022) | Suitable global weak solutions in position-dependent cube/weighted classes; a near/far pressure expansion using a local Calderón--Zygmund term and a remote kernel difference | Whole-space cube geometry and growth-at-infinity classes versus periodic lifted dyadic annuli; no \(\theta\)-dependent Gaussian sequence; no exact annular shift | It does not prove an endpoint-plus-dissipation Gaussian tail estimate from the \(8R\to2R\to R\) payment, nor (0.4)--(0.5) |
| Miao--Wang (2017) | A backward Gaussian multiplied by a compact cutoff is inserted into the suitable local energy inequality; cutoff errors live on an annular region; nested-scale iteration follows | One heat kernel and one annular collar at a time versus an infinite weighted annular sum with fixed \(\gamma_m(\theta)\); different regularity objective and geometry | No periodic lift, no identity \(A_k(R)=A_{k-1}(2R)\), no weighted essential-supremum tail, and no payment (0.3) |
| Jia--Šverák (2014) | Smaller-region local control near initial time; the nonlocal remainder is handled as harmonic pressure; nested spatial and temporal interiors are used | Near-initial-time whole-space regularity versus an arbitrary interior periodic suitable cylinder; qualitative radius loss versus the declared two-clock buffer and \(8R\) payment | No Gaussian dyadic tail or exact powers in (0.4)--(0.5) |
| Choe--Yang (2018), Wolf (2017), Bradshaw--Tsai (2020 preprint) | Explicit localized velocity-generated pressure plus a harmonic remainder, or an abstract local pressure projection/expansion | These papers supply the pressure mechanism only; R0.74B couples it to a fixed gauge, the \(2R\) exterior payment, the \(8R\) local energy, and the shifted Gaussian annuli | None states the complete quantitative pressure ledger or buffered tail closure used in R0.74B |
| Yu (2026 preprint) | A finite-chain standard-cost ledger containing annular leakage, pressure-tail, PFE, and a one-component channel; active/harmonic pressure coordinates | Finite CKN scale counting versus infinite Gaussian annular energy tails; its proved closing input is one-component compactness | The preprint expressly does not prove closing from leakage/pressure-tail/PFE alone and contains neither (0.1)--(0.3) nor (0.4)--(0.5) |

---

## 5. The target powers are not evidence of novelty

The exponents in (0.4)--(0.5) are not, by themselves, a novelty marker.
In R0.74B, \(P^\square\) already contains
\(\mathcal E^\square(z_0,8R)^{3/2}\).  Consequently,
\((P^\square)^{2/3}\) naturally returns a quadratic energy scale.  The
remaining \(3/2\) power is also compatible with standard interpolation,
Hölder, and Young inequalities applied after a cubic payment.  The same
algebraic exponents can therefore arise in unrelated estimates.

An exact-form search that fails to find the strings
\(P^{2/3}+P\) or \(P+P^{3/2}\) does not establish mathematical novelty.
Any defensible increment would have to lie in the uniform quantified
combination: the declared functionals, constants, clocks, infinite annular
summation, periodic lift, exact radius shift, endpoint time buffer, pressure
gauge, and \(8R\to2R\to R\) payment.

---

## 6. Safe attribution boundary

A research note may say:

> Periodic suitability, suitable local-energy testing, weighted and
> uniformly local energy control, dyadic spatial pressure estimates,
> backward-Gaussian localization, nested-cylinder buffering, and
> local/harmonic pressure decompositions all have direct primary-source
> precedents.  In the bounded search described here, I did not locate the
> exact simultaneous R0.74B package or either displayed closure with the
> same functionals and quantifiers.

It must not say “first,” “new weighted local energy method,” “new Gaussian
localization,” “new pressure decomposition,” or “the literature contains no
such estimate.”

The potentially distinguishable part is the exact integration of standard
components: a periodic lifted superexponential annular sum, its exact
doubled-radius shift, a suitable-weak endpoint buffer, and one quantitatively
declared pressure-payment ledger with constants uniform in the truncation
level.  Whether that integration is substantial enough for publication is a
separate mathematical and referee-level question.

**bounded non-hit is not novelty/priority proof**
