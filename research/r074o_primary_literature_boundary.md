# R0.74O — primary-literature boundary for the arbitrary-flow collar endpoint

## Status and scope

This note records a bounded primary-source collision search completed on
2026-09-02.  It concerns the proposed arbitrary-solution estimate

\[
 \mathfrak C_R^\alpha
 \le C P_R^{2/3}\sqrt{1+\log_+P_R},
 \qquad \alpha\in\{M,F\},
\tag{0.1}
\]

for the frozen R0.74 local frames, complete payment, and positive cumulative
all-shell collar flux.

The search had three separate questions.

1. Does the literature validate the periodic smooth 2D3C class with an
   arbitrarily amplified passive third component?
2. Is there a published local-energy, weighted-energy, shell-flux,
   moving-cylinder, Carleson, or logarithmic endpoint theorem that already
   implies (0.1), or conflicts with an exact 2D3C counterexample?
3. Is there a published counterexample to the exact R0.74O observables and
   payment?

The answers found in this bounded search are:

- **yes** to the first question;
- **no direct hit found** for the second question; and
- **no previously stated identical counterexample found** for the third
  question.

The first answer concerns only the legitimacy of the solution class.  The
estimates for \(P_R\), \(X_R\), and \(\mathfrak C_R\), and the resulting
failure of (0.1), are internal mathematics.  None of the cited papers proves
those R0.74 estimates.

This finite non-hit is not evidence of novelty, priority, exhaustiveness, or
publishability.  No Millennium-problem conclusion follows.  **NOT CLAY.**

---

## 1. Exact 2D3C embedding and passive-amplitude freedom

### 1.1 Published exact embedding

L. Biferale, M. Buzzicotti, and M. Linkmann consider a solenoidal velocity on
the periodic cube \(V=[0,L)^3\), independent of \(x_3\), and write

\[
 u=u^{2D}+\theta e_3,
 \qquad
 u^{2D}=(u_1,u_2,0).
\tag{1.1}
\]

Their Section II, equations (1)--(2), states that the three-dimensional
Navier--Stokes equations split exactly into

\[
 \partial_t u^{2D}
 =-(u^{2D}\!\cdot\nabla)u^{2D}-\nabla p+\nu\Delta u^{2D},
\tag{1.2}
\]

and

\[
 \partial_t\theta
 =-(u^{2D}\!\cdot\nabla)\theta+\nu\Delta\theta.
\tag{1.3}
\]

Thus the planar velocity and pressure solve two-dimensional Navier--Stokes,
while the third velocity component solves a linear passive
advection--diffusion equation.  The same section identifies the passive
component energy as a separate quadratic invariant in the inviscid limit.

Primary source:

- L. Biferale, M. Buzzicotti, M. Linkmann,
  [*From two-dimensional to three-dimensional turbulence through
  two-dimensional three-component flows*](https://arxiv.org/abs/1706.02371),
  *Physics of Fluids* **29** (2017), 111101,
  DOI [10.1063/1.4990082](https://doi.org/10.1063/1.4990082).

### 1.2 Arbitrary amplitude is a direct consequence, not a quoted theorem

Equation (1.3) is linear and homogeneous in \(\theta\).  Consequently, if
\((u^{2D},\theta,p)\) is a smooth 2D3C solution, then for every constant
\(A\in\mathbb R\),

\[
 u_A=u^{2D}+A\theta e_3,
 \qquad p_A=p,
\tag{1.4}
\]

is again an exact smooth periodic three-dimensional Navier--Stokes solution.
The pressure is unchanged because the passive component does not enter the
planar equation and all fields are independent of \(x_3\).

This amplitude statement is an elementary consequence of the published
split equations.  Biferale--Buzzicotti--Linkmann do not state or analyze the
R0.74O payment or collar observables.  Their paper therefore validates
admissibility of the exact family, not the internal counterexample ledger.

### 1.3 Large smooth vertical-component precedent

M. Paicu and Z. Zhang prove global smoothness for a class of large,
anisotropic initial data on \(\mathbb R^3\).  Their Theorem 1.1 treats

\[
 u_0^\varepsilon
 =\left(
   \varepsilon^{1/2}v_0^h(x_h,\varepsilon x_3),
   \varepsilon^{-1/2}v_0^3(x_h,\varepsilon x_3)
  \right),
\tag{1.5}
\]

under small analytic-type norms of the unscaled profile.  The vertical
component becomes large as \(\varepsilon\downarrow0\), yet the resulting
solution is global and smooth.

Primary source:

- M. Paicu, Z. Zhang,
  [*Global Regularity for the Navier--Stokes equations with large, slowly
  varying initial data in the vertical direction*](https://arxiv.org/abs/0903.5194),
  Theorem 1.1.

This theorem is not the strict periodic 2D3C construction in (1.1)--(1.4).
It is only a separate precedent showing that a large vertical component is
compatible with global smooth Navier--Stokes dynamics in a structured class.

---

## 2. Local and weighted energy flux

### 2.1 Suitable local energy inequality

The Caffarelli--Kohn--Nirenberg suitable-weak-solution framework uses the
local energy inequality.  In the normalization used by later primary
sources, for every nonnegative smooth compactly supported spacetime cutoff
\(\phi\),

\[
 2\iint |\nabla u|^2\phi
 \le
 \iint |u|^2(\partial_t\phi+\Delta\phi)
 +\iint (|u|^2+2p)u\cdot\nabla\phi.
\tag{2.1}
\]

Primary source:

- L. Caffarelli, R. Kohn, L. Nirenberg,
  [*Partial regularity of suitable weak solutions of the Navier--Stokes
  equations*](https://onlinelibrary.wiley.com/doi/10.1002/cpa.3160350604),
  *Communications on Pure and Applied Mathematics* **35** (1982), 771--831.

Equation (2.1) contains exactly the velocity--pressure flux that appears
when a cutoff is differentiated.  It does not give a sublinear large-payment
bound for the positive part of that flux.

A moving cutoff \(\phi(x-X(t),t)\) is allowed as a smooth test function, but
its time derivative contains

\[
 -X'(t)\cdot\nabla\phi.
\tag{2.2}
\]

Thus the local energy inequality does not make trajectory motion free.  Any
moving-frame theorem must retain or estimate this row.

### 2.2 Weighted \(L^2\) energy

P. G. Fernández-Dalgo and P. G. Lemarié-Rieusset prove global weak solutions
for divergence-free data in

\[
 L^2_{w_\gamma}(\mathbb R^3),
 \qquad w_\gamma(x)=(1+|x|)^{-\gamma},
 \qquad 0<\gamma\le2.
\tag{2.3}
\]

Their Theorem 1 gives a suitable solution and a weighted energy inequality
whose cutoff terms include

\[
 -\int \nabla |u|^2\cdot\nabla w_\gamma
 +\int (|u|^2+2p)u\cdot\nabla w_\gamma.
\tag{2.4}
\]

Primary source:

- P. G. Fernández-Dalgo, P. G. Lemarié-Rieusset,
  [*Weak solutions for Navier--Stokes equations with initial data in weighted
  \(L^2\) spaces*](https://arxiv.org/abs/1906.11038), Theorem 1.

This is a direct precedent for keeping the weighted pressure flux in the
energy ledger.  Its closed a priori estimate uses polynomial energy terms
and Gronwall control.  It does not estimate a positive cumulative annular
flux by \(P^{2/3}\sqrt{\log P}\).

### 2.3 Local pressure is not collar-local

Z. Bradshaw and T.-P. Tsai define local energy solutions using a pressure
decomposition on a ball.  Their Definition 1.1 separates

1. a local Calderón--Zygmund term generated by
   \(u\otimes u\) inside a larger ball;
2. a far-field integral of differences of the pressure kernel; and
3. a time-dependent pressure gauge.

Primary source:

- Z. Bradshaw, T.-P. Tsai,
  [*Local energy solutions to the Navier--Stokes equations in Wiener amalgam
  spaces*](https://arxiv.org/abs/2008.09204), Definition 1.1 and Theorem 1.4.

This exact split shows why a payment based only on velocity inside one collar
cannot automatically control pressure flux: the far field contributes a
harmonic pressure on the local region.  This is a design constraint.  It is
not a counterexample to a frozen payment that already contains a genuine
pressure-tail or harmonic-pressure row.

---

## 3. The closest physical-space shell-flux theorem

R. Dascaliuc and Z. Grujić define the localized physical-space energy flux
through a ball or shell by

\[
 \Phi_{x_0,R}
 =\frac1T\iint
 \left(\frac{|u|^2}{2}+p\right)u\cdot\nabla\phi_{x_0,R}.
\tag{3.1}
\]

For suitable weak solutions they subtract the nonnegative anomalous flux
\(\Phi^\infty/T\) and use the modified flux

\[
 \Psi=\Phi-\frac{\Phi^\infty}{T}.
\tag{3.2}
\]

Their shell identity gives

\[
 \Psi
 =\nu E_{\rm shell}
 -\frac1{2T}\iint |u|^2(\partial_t\phi+\nu\Delta\phi),
\tag{3.3}
\]

and, under their cutoff/time-window setup, including

\[
 T\ge \frac{R_0^2}{\nu},
\]

but without the Taylor-scale hypothesis, the upper estimate

\[
 \Psi
 \le \nu E_{\rm shell}
 +C\nu\widetilde R^{-2}e_{\rm shell}.
\tag{3.4}
\]

Under the same cutoff/time-window setup and the additional local
Taylor-scale condition

\[
 \tau=(e/E)^{1/2}
 <\gamma C_0^{-1/2}\widetilde R,
\tag{3.5}
\]

their Theorem 5.1 proves

\[
 (1-\gamma^2)\nu E_{\rm shell}
 \le\Psi\le
 (1+\gamma^2)\nu E_{\rm shell}.
\tag{3.6}
\]

For regular solutions the anomalous term vanishes.  Their inertial-range
theorem additionally averages over optimal spatial coverings.

Primary source:

- R. Dascaliuc, Z. Grujić,
  [*Energy cascades and flux locality in physical scales of the 3D
  Navier--Stokes equations*](https://arxiv.org/abs/1101.2193),
  Theorem 4.1, shell identities in Section 5, and Theorem 5.1;
  *Communications in Mathematical Physics* **305** (2011), 199--220,
  DOI [10.1007/s00220-011-1219-8](https://doi.org/10.1007/s00220-011-1219-8).

This is the closest direct flux theorem found.  It does not give (0.1): it
uses time-averaged fixed-shell flux, energy/enstrophy payments, a
cutoff/time-window condition, and for the two-sided comparison a
Taylor-scale condition.  It does not take the
supremum of a positive cumulative short-window flux, follow the R0.74
terminal trajectory, sum the frozen all-shell weight, or produce a
square-root logarithm.

---

## 4. Moving and skewed cylinders

J. Yang constructs maximal functions subordinate to skewed cylinders that
are tubular neighborhoods of trajectories of a mollified incompressible
flow.  The main result proves weak type \((1,1)\) and strong type \((p,p)\)
for the associated maximal operator.

Primary source:

- J. Yang,
  [*Construction of Maximal Functions associated with Skewed Cylinders
  Generated by Incompressible Flows and Applications*](https://arxiv.org/abs/2008.05588),
  *Annales de l'Institut Henri Poincaré C, Analyse non linéaire* **39**
  (2022), 793--818.

A. Vasseur and J. Yang then use this moving geometry in a local-to-global
argument.  Corollary 1.2 applies to a global suitable weak solution on
\((0,\infty)\times\mathbb R^3\) with divergence-free finite-energy data
\(u_0\in L^2(\mathbb R^3)\), and proves

\[
 \nabla^2u\in L^{4/3,q}_{\rm loc},
 \qquad q>\frac43,
\tag{4.1}
\]

with related Lorentz estimates for higher vorticity derivatives of smooth
solutions.

Primary source:

- A. Vasseur, J. Yang,
  [*Second derivatives estimate of suitable solutions to the 3D
  Navier--Stokes equations*](https://arxiv.org/abs/2009.14291),
  *Archive for Rational Mechanics and Analysis* **241** (2021), 683--727,
  DOI [10.1007/s00205-021-01661-4](https://doi.org/10.1007/s00205-021-01661-4).

These papers validate the use of mollified-flow trajectories to remove a
large local mean while retaining scale-correct maximal estimates.  They do
not define or bound the R0.74 positive cumulative collar flux.

---

## 5. Carleson, dyadic, annular, and logarithmic endpoint precedents

### 5.1 Parabolic Carleson control

H. Koch and D. Tataru characterize \(BMO^{-1}\) through the heat extension
using the parabolic square function

\[
 \sup_{x,R}
 \frac1{|B(x,R)|}
 \int_0^{R^2}\int_{B(x,R)}|e^{t\Delta}u_0|^2.
\tag{5.1}
\]

Their solution space contains the analogous Carleson quantity for \(u\),
together with \(\sup_t\sqrt t\|u(t)\|_\infty\).  Their Theorem 2 gives a
unique global solution for sufficiently small divergence-free
\(BMO^{-1}\) data.

Primary source:

- H. Koch, D. Tataru,
  [*Well-posedness for the Navier--Stokes equations*](https://math.berkeley.edu/~tataru/papers/nas.pdf),
  *Advances in Mathematics* **157** (2001), 22--35,
  DOI [10.1006/aima.2000.1937](https://doi.org/10.1006/aima.2000.1937).

This is a genuine scale-invariant Carleson endpoint.  It is a small-data
mild-solution theorem based on the initial heat extension, not a
velocity--pressure collar-flux theorem.

### 5.2 Quantitative good annuli

Z. Lei and X. Ren prove the logarithmically improved partial-regularity
statement

\[
 \mathcal P^{r|\log r|}(\mathcal S)=0
\tag{5.2}
\]

for suitable weak solutions.  Their key bookkeeping uses nonoverlapping
hollow dissipation layers and a pigeonhole selection.  Theorem B finds a
regular interval in one spatial direction whose length is bounded below in
terms of the natural local quantities

\[
 \mathcal G=\int_{Q(1)}(|u|^3+|p|^{3/2}),
 \qquad
 \mathcal H=\int_{Q(1)}|\nabla u|^2.
\tag{5.3}
\]

Remark 8 states the analogous existence of one quantitative regular
annulus.

Primary source:

- Z. Lei, X. Ren,
  [*Quantitative partial regularity of the Navier--Stokes equations and
  applications*](https://arxiv.org/abs/2210.01783),
  Theorem A, Theorem B, and Remark 8;
  *Advances in Mathematics* **445** (2024), 109654,
  DOI [10.1016/j.aim.2024.109654](https://doi.org/10.1016/j.aim.2024.109654).

This theorem selects at least one favorable annulus.  It does not control a
predetermined collar, an all-shell weighted sum, or the positive cumulative
flux.  Its logarithm belongs to partial-regularity scale counting, not to
the right side of (0.1).

### 5.3 Recent stationary annular logarithm

W. Wu proves for smooth stationary solutions on \(\mathbb R^3\), vanishing
at infinity,

\[
 \omega\in L^{9/5,\infty}(\mathbb R^3)
 \quad\Longrightarrow\quad
 u\equiv0.
\tag{5.4}
\]

The proof first obtains finite Dirichlet energy, then combines the weak
\(L^{9/5}\) distribution bound with \(L^2\) control.  Its equation (3.6)
gives logarithmic growth of cumulative strong \(L^{9/5}\) vorticity mass.
Lemma 3.1 selects dyadic starting scales with controlled one-sided annular
blocks before a stationary blow-down and flux-vanishing argument.

Primary source:

- W. Wu,
  [*The Global Weak-Lorentz Vorticity Endpoint in the Stationary
  Navier--Stokes Liouville Problem*](https://arxiv.org/abs/2608.22471),
  Theorem 1.1 and Lemma 3.1, arXiv v1, submitted 23 August 2026.

This is a recent, unrefereed preprint.  It treats stationary whole-space
Liouville rigidity under a global weak-Lorentz hypothesis.  Its logarithm
and annular selection do not imply an unsteady periodic collar estimate.

### 5.4 Recent finite-chain CKN ledger

R. Yu considers a finite geometric scale chain and defines nonnegative
channels for a vertical component, annular leakage, pressure tails, and a
pressure--flux--energy residual.  Under a uniform full critical bound,
Theorem 6.3 states

\[
 \sum_{k\in\mathcal B}w_k
 \le
 \frac1{\varepsilon_{\rm close}(M)}
 \sum_k w_k
 \left(
 C_{3,k}+\mathcal L_k^{\rm ann}
 +\mathcal P_k^{\rm tail}
 +\mathcal R_k^{\rm PFE}
 \right).
\tag{5.5}
\]

Primary source:

- R. Yu,
  [*Finite-Chain CKN-Bad Scale Counting for Navier--Stokes: Standard PDE
  Closure and Canonical Detector Realization*](https://arxiv.org/abs/2606.21783),
  Theorem 6.3, arXiv v1, submitted 19 June 2026.

The paper states that the proved standard-PDE closure uses one-component
compactness through \(C_{3,k}\).  It explicitly does not claim that the
annular-leakage or pressure-tail channels independently force CKN
smallness.  It is a finite-chain counting theorem, not (0.1), and it contains
no square-root-logarithmic flux law.  It is also a recent unrefereed
preprint.

---

## 6. Limitations that must not be promoted into false counterexamples

### 6.1 Harmonic pressure in a local domain

J. Wolf gives the local potential-like example

\[
 u(x,t)=\nabla\phi(x)\eta(t),
 \qquad
 p=-\phi\eta'-\frac12|\nabla\phi|^2\eta^2,
\tag{6.1}
\]

where \(\phi\) is harmonic and \(\eta\) may have arbitrary time behavior.
His main representation separates a time derivative of harmonic pressure
from a pressure generated by the remaining force.

Primary source:

- J. Wolf,
  [*On the local pressure of the Navier--Stokes equations and related
  systems*](https://arxiv.org/abs/1611.01482), introduction example and the
  local-pressure representation in Section 6.

This example explains why a local velocity norm need not determine local
pressure.  It is not a counterexample on the global periodic torus: periodic
harmonic functions are constant.

### 6.2 Local energy inequality alone is insufficient

W. S. Ożański constructs spatially localized weak solutions of the
Navier--Stokes inequality that satisfy the strong and local energy
inequalities and approximate an arbitrary prescribed nonincreasing energy
profile.  Theorem 1.3 emphasizes that these fields need not solve the
Navier--Stokes equations.

Primary source:

- W. S. Ożański,
  [*Weak solutions to the Navier--Stokes inequality with arbitrary energy
  profiles*](https://arxiv.org/abs/1809.02109), Theorem 1.3;
  *Communications in Mathematical Physics* **374** (2020), 33--62,
  DOI [10.1007/s00220-019-03588-0](https://doi.org/10.1007/s00220-019-03588-0).

This shows that the local energy inequality by itself cannot supply all
Navier--Stokes dynamics needed for (0.1).  It is not a smooth NSE
counterexample and must not be cited as one.

For suitable weak solutions, anomalous local-energy defect is another
separate issue.  The modified flux in (3.2) records it.  The R0.74O 2D3C
family is smooth, so no anomalous defect is involved in the internal
counterexample.

---

## 7. Literature boundary versus the internal R0.74O counterexample

The primary literature establishes only the following external input:

\[
 \boxed{\text{arbitrarily amplified smooth periodic 2D3C passive components
 are exact 3D NSE solutions}.}
\tag{7.1}
\]

The proposed R0.74O disproof uses additional internal estimates.  In the
current frozen notation they have the schematic form

\[
 \kappa=L^{2/3}e^{mL^2/3},
 \qquad m=\frac{43}{423360}>0,
\tag{7.2}
\]

\[
 P\asymp B^3R^3,
 \qquad
 \log P=3\rho L^2+O(1),
\tag{7.3}
\]

and

\[
 X,\mathfrak C
 \gtrsim \kappa^2B^2LR^2.
\tag{7.4}
\]

Equations (7.2)--(7.4) are not literature results.  They must be justified
by the exact R0.74G payment estimates, the R0.74J shear-only payment lower
bound, and the R0.74F/H target and collar-flux lower bounds.

If those internal estimates pass their independent analytic audits, then

\[
 P^{2/3}\sqrt{1+\log_+P}
 \asymp B^2R^2L,
\tag{7.5}
\]

while

\[
 \frac{X}{P^{2/3}\sqrt{1+\log_+P}},
 \quad
 \frac{\mathfrak C}{P^{2/3}\sqrt{1+\log_+P}}
 \gtrsim\kappa^2\longrightarrow\infty.
\tag{7.6}
\]

Thus (0.1) is false for arbitrary smooth periodic solutions, conditional
only on completion of that internal proof ledger.  The bounded literature
search found no theorem that conflicts with (7.6).  In particular, the
Dascaliuc--Grujić estimate pays shell energy and dissipation directly and
does not perform the sublinear conversion in (0.1).

The stronger internal lower-growth formulation

\[
 X,\mathfrak C
 \gtrsim
 P^{8024/11907}(\log P)^{7/6},
 \qquad
 \frac{8024}{11907}>\frac23,
\tag{7.7}
\]

is likewise not supplied by any cited source.

The literature classification is therefore:

| Question | Bounded-search result |
|---|---|
| Is the arbitrary-amplitude periodic 2D3C family a legitimate exact smooth NSE class? | **YES.** Published split equations imply it directly. |
| Does a primary source prove the frozen \(P^{2/3}\sqrt{\log P}\) positive collar bound? | **NO DIRECT HIT FOUND.** |
| Does a primary source state the same \(P/X/\mathfrak C\) counterexample? | **NO IDENTICAL HIT FOUND.** |
| Does the literature prove the internal payment and flux asymptotics? | **NO.** They remain internal proof obligations. |
| Does the non-hit establish novelty, priority, exhaustiveness, or publishability? | **NO.** |

The correct R0.74O research target is therefore an impossibility theorem for
the arbitrary-solution endpoint, not another attempted proof of (0.1).  A
positive replacement would need an additional structural restriction or a
new nonnegative payment row that detects the amplified passive component.

**NOT CLAY.**

---

## 8. Primary-source ledger

The table records exactly how each source was used.  No survey, encyclopedia,
secondary citation database, or search-result summary is used as mathematical
evidence in this note.

| ID | Primary source | Verified statement or range | Collision classification |
|---|---|---|---|
| S1 | Biferale--Buzzicotti--Linkmann (2017), [arXiv:1706.02371](https://arxiv.org/abs/1706.02371) | Periodic 2D3C NSE splits into 2D NSE plus linear passive advection--diffusion, Section II (1)--(2). | **Direct admissibility hit** for arbitrary passive amplitude; no R0.74 payment theorem. |
| S2 | Paicu--Zhang (2009), [arXiv:0903.5194](https://arxiv.org/abs/0903.5194) | Theorem 1.1: global smooth solutions for structured large slowly varying data with a vertical component of size \(\varepsilon^{-1/2}\). | Large-smooth-vertical-component precedent only. |
| S3 | Caffarelli--Kohn--Nirenberg (1982), [DOI 10.1002/cpa.3160350604](https://onlinelibrary.wiley.com/doi/10.1002/cpa.3160350604) | Suitable weak local energy inequality and partial regularity. | Foundational flux identity; no positive collar endpoint. |
| S4 | Fernández-Dalgo--Lemarié-Rieusset (2019), [arXiv:1906.11038](https://arxiv.org/abs/1906.11038) | Theorem 1: global weighted-\(L^2\) suitable weak solutions for \(0<\gamma\le2\), with weighted velocity--pressure flux. | Weighted-energy method hit; no square-root log. |
| S5 | Bradshaw--Tsai (2020), [arXiv:2008.09204](https://arxiv.org/abs/2008.09204) | Definition 1.1: local Calderón--Zygmund pressure plus far-field kernel difference and time gauge; Theorem 1.4 gives local-energy control in Wiener amalgam spaces. | Pressure-tail design constraint. |
| S6 | Dascaliuc--Grujić (2011), [arXiv:1101.2193](https://arxiv.org/abs/1101.2193) | Under their cutoff/time-window setup, including \(T\ge R_0^2/\nu\), the time-averaged physical-shell modified flux has an upper estimate without the Taylor-scale hypothesis; Theorem 5.1 adds a Taylor-scale condition for the two-sided enstrophy comparison. | Closest flux theorem; different observable, payment, averaging, and hypotheses. |
| S7 | Yang (2020/2022), [arXiv:2008.05588](https://arxiv.org/abs/2008.05588) | Mollified-flow skewed-cylinder maximal operator is weak \((1,1)\) and strong \((p,p)\). | Moving-cylinder method hit only. |
| S8 | Vasseur--Yang (2020/2021), [arXiv:2009.14291](https://arxiv.org/abs/2009.14291) | Corollary 1.2: for a global suitable weak solution on \((0,\infty)\times\mathbb R^3\) with divergence-free \(u_0\in L^2\), a local \(L^{4/3,q}\), \(q>4/3\), second-derivative estimate follows from skewed-cylinder local-to-global analysis. | Moving local regularity under the finite-energy/global hypothesis, not collar flux. |
| S9 | Koch--Tataru (2001), [primary PDF](https://math.berkeley.edu/~tataru/papers/nas.pdf) | Theorem 2: small \(BMO^{-1}\) global well-posedness with parabolic Carleson solution norm. | Carleson endpoint precedent; no flux theorem. |
| S10 | Lei--Ren (2022/2024), [arXiv:2210.01783](https://arxiv.org/abs/2210.01783) | Theorem A: \(r|\log r|\) partial-regularity improvement; Theorem B and Remark 8: existence of one quantitative regular interval/annulus. | Logarithmic good-scale selection, not predetermined all-shell control. |
| S11 | Wu (2026), [arXiv:2608.22471](https://arxiv.org/abs/2608.22471) | v1 Theorem 1.1: stationary weak-Lorentz vorticity Liouville theorem; Lemma 3.1: dyadic good-scale selection after logarithmic cumulative mass control. | Recent stationary annular-log precedent only. |
| S12 | Yu (2026), [arXiv:2606.21783](https://arxiv.org/abs/2606.21783) | v1 Theorem 6.3: finite-chain weighted CKN-bad-scale counting under a full critical bound; proved closure uses the vertical-component channel. | Recent finite-chain ledger; explicitly no independent annular closure or square-root log. |
| S13 | Wolf (2016), [arXiv:1611.01482](https://arxiv.org/abs/1611.01482) | Local pressure representation and potential-like harmonic-pressure example. | Local pressure limitation; not a periodic counterexample. |
| S14 | Ożański (2018/2020), [arXiv:1809.02109](https://arxiv.org/abs/1809.02109) | Theorem 1.3: spatially localized Navier--Stokes-inequality fields approximating arbitrary nonincreasing energy profiles. | LEI-only limitation; fields need not solve NSE. |

Search boundary: local/suitable energy inequalities; weighted NSE energy;
pressure decomposition and harmonic tails; physical-space ball and shell flux;
dyadic/Carleson and logarithmic endpoints; quantitative good annuli; moving and
skewed cylinders; strict 2D3C/passive-component dynamics; large smooth vertical
components; and LEI/NSI limitations.  This is a bounded screen, not a systematic
review of every paper in those areas.
