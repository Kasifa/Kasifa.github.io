# R0.74D — bounded primary-source literature collision audit

**Audit date:** 2026-09-01

**Status:** `EXACT_HIT_NOT_LOCATED / DIRECT_COMPONENT_COLLISIONS_FOUND /
BOUNDED_NON_HIT / NOT_NOVELTY_PROOF`

**Claim class:** primary-source prior-art boundary; not a novelty, priority,
or publication-clearance opinion

**Related analytic note:** `r074d_zero_mean_local_transport_obstruction.md`

This note audits the literature boundary of R0.74D without changing or
rechecking its proof.  It keeps four questions separate:

1. Is the zero-mean exact family outside known Navier--Stokes invariant
   classes?
2. Are removal of a global mean, removal of a local or mollified mean, and
   flow-following/skewed cylinders new repair ideas?
3. Is retaining a transport or pressure flux in a fixed-centre local-energy
   inequality new?
4. Was the exact frozen Version-A ratio theorem located?

The answers furnished by the bounded primary-source search are:

- **No:** the family is a coordinate-permuted specialization of the classical
  2D3C/passive-scalar invariant class, and time-dependent decaying sinusoidal
  shear is already a direct passive-scalar model in the literature.
- **No:** all three frame/mean-removal architectures have direct precedents.
- **No:** fixed-centre mean-free local-energy inequalities retaining both
  transport and pressure flux rows have direct precedents.
- **No exact hit was located** for the entire R0.74D quantitative conjunction.
  This last statement is only a bounded non-hit.  It is not evidence sufficient
  to claim novelty or priority.

---

## 1. Exact object audited

The search target is not a generic assertion that transport matters.  It is
the exact Version-A statement

\[
 X_R^A=\mathcal U_{\rm ext}^{\infty,A}+\mathcal D_{\rm ext}^A,
 \qquad
 P_R^A=\mathcal E^A(z_0,8R)^{3/2}
       +\mathcal A_{\rm ext}^A(z_0,2R;1),
\tag{1.1}
\]

and

\[
 \sup_{\substack{0<R<\pi/16\\
       (u,p)\ {\rm smooth\ periodic\ NSE}\\
       \overline u=0}}
 \frac{X_R^A}{(P_R^A)^{2/3}}=\infty.
\tag{1.2}
\]

The witness used in the analytic note is

\[
 u(t,x)=\bigl(AF(t,x_2,x_3),B_Re^{-t}\cos x_3,0\bigr),
 \qquad p=0,
\tag{1.3}
\]

where

\[
 \partial_tF+B_Re^{-t}\cos x_3\,\partial_2F
   =(\partial_2^2+\partial_3^2)F,
\tag{1.4}
\]

the initial scalar is a derivative of a periodic heat packet localized in
both active variables, and the parameters \((A,R,M_m,B_R)\) are coupled as in
R0.74D.  The theorem also retains the declared local/harmonic pressure gauge,
all lifted periodic annuli, all background and packet rows, and the explicit
Version-A exponent \(2/3\).

For this audit an **exact hit** would need to match, up to transparent changes
of notation, all of the following:

1. a smooth unforced periodic NSE family with zero global spatial mean;
2. the local coherent drift mechanism represented by (1.3)--(1.4);
3. the fixed Version-A centre, annular weights, standard clocks, and local
   pressure gauge;
4. the same numerator and full payment denominator in (1.1);
5. an explicit parameter sequence proving the unbounded ratio (1.2).

A source matching only the invariant class, shear equation, moving frame,
local-mean subtraction, flux architecture, or pressure decomposition is a
component collision, not an exact hit.

---

## 2. Search scope, source hierarchy, and stopping rule

### 2.1 Primary-source hierarchy

The audit prioritized, in order:

1. the article or author manuscript itself;
2. an official journal page or DOI record;
3. the official arXiv record and full text; and
4. a primary paper's own citation trail when the earlier paper could be
   inspected directly.

Review articles, search snippets, citation aggregators, and informal web pages
were used only as discovery aids and do not support a collision classification
below.

### 2.2 Search waves

The first wave traced the mechanisms:

- “two-dimensional three-component” / `2D3C` Navier--Stokes and passive
  scalar;
- periodic and time-dependent shear advection-diffusion, including decaying
  trigonometric shears;
- periodic mean velocity and Galilean removal;
- local or mollified mean subtraction;
- flow trajectories and skewed parabolic cylinders;
- fixed spatial cutoffs with mean-free transport and pressure fluxes; and
- local pressure projections and harmonic pressure components.

The second wave used exact and synonymous combinations:

- zero-global-mean local drift obstruction;
- 2D3C derivative-of-heat-kernel packets;
- fixed-centre annular tails versus local-energy payment;
- lifted Gaussian annular weights and periodic copies;
- Version-A or co-moving global-mean removal;
- entrance flux, pressure flux, and local weighted mean; and
- divergence of an exterior-energy/payment ratio with exponent \(2/3\).

The search stopped when exact and synonymous queries recycled the sources
below, returned general enhanced-dissipation or local-regularity literature,
or produced unrelated annular-domain and engineering results.  This stopping
rule did not exhaust books, theses, all citation chains, inaccessible full
texts, all languages, or results written in an unanticipated functional
notation.

---

## 3. Collision verdict

### 3.1 Exact hit

**No exact hit was located.**

In particular, none of the inspected primary sources simultaneously states
the frozen quantities (1.1), uses the zero-mean family (1.3) with the R0.74D
parameter sequence, retains every declared pressure/harmonic and periodic-copy
row, and proves (1.2).

### 3.2 Direct component collisions

The following collisions are strong and should control attribution:

- `DIRECT_INVARIANT_CLASS_COLLISION`: Biferale--Buzzicotti--Linkmann write the
  periodic 2D3C decomposition in which the planar velocity solves 2D
  Navier--Stokes and the perpendicular component solves a passive-scalar
  equation.  After permuting coordinates, (1.3)--(1.4) lies inside this class.
- `DIRECT_TIME_DEPENDENT_SHEAR_COLLISION`: Coble--He study the same
  time-dependent shear passive-scalar equation on \(\mathbb T^2\) and
  explicitly use a heat-evolving sinusoidal shear \(e^{-\nu t}\sin y\).
  With \(\nu=1\), a phase shift, and an amplitude factor, this contains the
  coefficient shape \(B_Re^{-t}\cos x_3\).
- `DIRECT_GLOBAL_MEAN_GALILEAN_COLLISION`: Galilean removal of a torus average
  velocity is explicit in Cyranka--Zgliczyński and is also an operative tool
  in the Vasseur--Choi line.  R0.74D cannot claim this algebraic repair.
- `DIRECT_LOCAL_FRAME_COLLISION`: Vasseur and Choi--Vasseur follow mollified
  trajectories and subtract a local/mollified convective velocity;
  Yang and Vasseur--Yang develop the corresponding skewed-cylinder geometry.
- `DIRECT_FIXED_CENTRE_FLUX_COLLISION`: Choe--Yang subtract a weighted spatial
  mean under a fixed cutoff while retaining both the convective transport flux
  and the pressure flux.  The architecture “fixed centre plus explicit flux
  payment” is therefore prior art.
- `STRUCTURAL_PRESSURE_COMPONENT_COLLISION`: Wolf gives general primary-source
  provenance for local pressure distributions with harmonic and
  force-dependent pieces.  This does not match the exact R0.74D gauge, but it
  prevents a broad novelty claim for local/harmonic pressure splitting.

### 3.3 Bounded non-hit

The only non-hit recorded here concerns the **whole quantitative
conjunction** in Section 1.  A mathematically equivalent result could still
occur as a lemma, remark, exercise, unpublished note, thesis result, or theorem
using different observables.  `EXACT_HIT_NOT_LOCATED` must not be silently
upgraded to “the theorem is new.”

---

## 4. Primary-source provenance and collision boundaries

### 4.1 Periodic 2D3C as 2D Navier--Stokes plus a passive scalar

**Source.** L. Biferale, M. Buzzicotti, and M. Linkmann, “From
two-dimensional to three-dimensional turbulence through two-dimensional
three-component flows,” *Physics of Fluids* **29** (2017), article 111101,
DOI 10.1063/1.4990082.
[Official arXiv record](https://arxiv.org/abs/1706.02371),
[primary full text](https://arxiv.org/html/1706.02371), and
[DOI record](https://doi.org/10.1063/1.4990082)

**Supported.** Section II starts with a periodic solenoidal velocity having
three components but depending on two coordinates.  It writes the exact split

\[
 \partial_tu^{2D}=-(u^{2D}\!\cdot\nabla)u^{2D}-\nabla P+\nu\Delta u^{2D},
 \qquad
 \partial_t\theta=-(u^{2D}\!\cdot\nabla)\theta+\nu\Delta\theta.
\tag{4.1}
\]

Taking the active plane to be \((x_2,x_3)\), the planar field
\((u_2,u_3)=(B_Re^{-t}\cos x_3,0)\), and the perpendicular component
\(u_1=AF\), equation (4.1) becomes precisely the PDE structure of
(1.3)--(1.4).  The assertion that R0.74D is a specialization is an elementary
coordinate identification made in this audit, not a theorem about the
Version-A functionals stated by those authors.

**Boundary.** The article studies 2D3C structure, invariants, cascades, and
2D-to-3D transition.  It does not use the R0.74D localized packet, annular
ledger, pressure gauge, parameter sequence, or ratio theorem.

**Collision class:** `DIRECT_INVARIANT_CLASS_COLLISION`.

### 4.2 The same time-dependent shear/passive-scalar equation

**Source.** Daniel Coble and Siming He, “A Note on Enhanced Dissipation and
Taylor Dispersion of Time-dependent Shear Flows,” *Communications in
Mathematical Sciences* **22** (2024), no. 6, 1685--1700, DOI
10.4310/CMS.2024.v22.n6.a10.
[Official arXiv record](https://arxiv.org/abs/2309.15738),
[primary full text](https://arxiv.org/html/2309.15738), and
[DOI record](https://doi.org/10.4310/CMS.2024.v22.n6.a10)

**Supported.** The paper studies

\[
 \partial_tf+V(t,y)\partial_xf=\nu\Delta_\sigma f
\tag{4.2}
\]

on domains including \(\mathbb T^2\).  Remark 1.1 explicitly selects the
heat-equation solution \(V(t,y)=e^{-\nu t}\sin y\) on the torus.  For
\(\nu=1\), replacing \(y\) by \(y+\pi/2\), and multiplying by \(B_R\), the
coefficient shape is the one in (1.4).  This is a direct collision with the
passive PDE mechanism, including its time dependence; it is stronger and more
specific than a generic citation to stationary shear dispersion.

**Boundary.** Coble--He prove enhanced-dissipation and Taylor-dispersion
estimates under structural hypotheses.  They do not embed the scalar as the
perpendicular component of the exact NSE witness, do not claim estimates
uniform in the R0.74D large amplitude \(B_R\), and do not define or test the
Version-A ratio.

**Collision class:** `DIRECT_TIME_DEPENDENT_SHEAR_COLLISION`.

### 4.3 Global average velocity and Galilean removal on a torus

**Source.** Jacek Cyranka and Piotr Zgliczyński, “Stabilizing effect of large
average initial velocity in forced dissipative PDEs invariant with respect to
Galilean transformations,” *Journal of Differential Equations* **261**
(2016), no. 8, 4648--4708, DOI 10.1016/j.jde.2016.07.007.
[Official arXiv record](https://arxiv.org/abs/1407.1712) and
[DOI record](https://doi.org/10.1016/j.jde.2016.07.007)

**Supported.** The paper treats dissipative equations on a torus and removes a
large average initial velocity by a Galilean transformation, converting it to
rapidly oscillating forcing.  Its examples include forced incompressible 2D
Navier--Stokes, with a related locally attracting statement for the forced 3D
system.

**Boundary.** The objective is forced dynamical stabilization, not an
unforced local-energy obstruction.  It does not state the exact Version-A
coordinate convention or the ratio (1.2).  The broader point—torus average
velocity and its Galilean removal are established tools—is nevertheless a
direct collision.

**Collision class:**
`DIRECT_GLOBAL_MEAN_GALILEAN_COLLISION / DIFFERENT_OBJECTIVE`.

### 4.4 Mollified trajectories and local mean removal

**Source 1.** Alexis F. Vasseur, “Higher derivatives estimate for the 3D
Navier--Stokes equation,” *Annales de l'Institut Henri Poincare C, Analyse
non lineaire* **27** (2010), no. 5, 1189--1204, DOI
10.1016/j.anihpc.2010.05.002.
[Official journal page](https://ems.press/journals/aihpc/articles/4076951) and
[official archival PDF](https://www.numdam.org/article/AIHPC_2010__27_5_1189_0.pdf)

**Source 2.** Kyudong Choi and Alexis F. Vasseur, “Estimates on fractional
higher derivatives of weak solutions for the Navier--Stokes equations,”
*Annales de l'Institut Henri Poincare C, Analyse non lineaire* **31** (2014),
no. 5, 899--945, DOI 10.1016/j.anihpc.2013.08.001.
[Official archival PDF](https://www.numdam.org/item/AIHPC_2014__31_5_899_0.pdf)
and [official arXiv record](https://arxiv.org/abs/1105.1526)

**Supported.** Vasseur identifies transport as the obstruction to a direct
parabolic estimate, mollifies the velocity, and performs the local blow-up
along the associated flow.  Choi--Vasseur make the Galilean/trajectory
scaling explicit and design it so the velocity and convective velocity have
zero weighted mean.  They also explain qualitatively why a fast flow may cross
a fixed cylinder before viscosity completes local regularization.

**Boundary.** These are positive whole-space derivative estimates.  Their
local means and observables are not the global torus mean or frozen Version-A
ledger.  They therefore supply the established repair architecture and the
qualitative transport warning, not (1.2).

**Collision class:** `DIRECT_LOCAL_FRAME_COLLISION`.

### 4.5 Flow-following and skewed cylinders

**Source 1.** Jincheng Yang, “Construction of maximal functions associated
with skewed cylinders generated by incompressible flows and applications,”
*Annales de l'Institut Henri Poincare C, Analyse non lineaire* **39** (2022),
no. 4, 793--818, DOI 10.4171/aihpc/20.
[Official journal PDF](https://ems.press/content/serial-article-files/28646)
and [official arXiv record](https://arxiv.org/abs/2008.05588)

**Source 2.** Alexis F. Vasseur and Jincheng Yang, “Second derivatives
estimate of suitable solutions to the 3D Navier--Stokes equations,” *Archive
for Rational Mechanics and Analysis* **241** (2021), no. 2, 683--727, DOI
10.1007/s00205-021-01661-4.
[Official publisher page](https://link.springer.com/article/10.1007/s00205-021-01661-4)
and [official arXiv record](https://arxiv.org/abs/2009.14291)

**Supported.** Yang defines skewed cylinders as tubular neighbourhoods of
trajectories of a mollified incompressible flow and proves the associated
covering and maximal-function estimates.  The paper says the geometry takes
out mean velocity and explains that uncontrolled flux prevents a naive
parabolic regularization argument.  Vasseur--Yang then use this machinery in
suitable-solution derivative estimates.

**Boundary.** These sources make a local/mollified trajectory, not the
constant global-mean path of Version A.  They do not prove that the
fixed-centre Version-A ledger fails, nor do they decide which transport-aware
repair controls the R0.74D family.

**Collision class:** `DIRECT_LOCAL_FRAME_COLLISION / SKEWED_CYLINDER_PRECEDENT`.

### 4.6 Fixed-centre local mean with transport and pressure flux retained

**Source.** Hi Jun Choe and Minsuk Yang, “Local kinetic energy and
singularities of the incompressible Navier--Stokes equations,” *Journal of
Differential Equations* **264** (2018), no. 2, 1171--1191, DOI
10.1016/j.jde.2017.09.036.
[Official journal page](https://www.sciencedirect.com/science/article/pii/S0022039617305211)
and [official arXiv record](https://arxiv.org/abs/1705.04561)

**Supported.** For a fixed normalized spatial cutoff \(\varphi\), Lemma 6
defines a weighted mean and fluctuation

\[
 [v]_r(t)=\int v(x,t)\varphi(x)\,dx,
 \qquad v^\circ=v-[v]_r,
\tag{4.3}
\]

and retains in the resulting mean-free local-energy inequality both

\[
 \int v\cdot\nabla\varphi\,|v^\circ|^2\theta\,dx\,dt
 \quad\hbox{and}\quad
 2\int p\,v^\circ\cdot\nabla\varphi\,\theta\,dx\,dt.
\tag{4.4}
\]

Thus fixed centre, weighted local-mean subtraction, convective transport
flux, and pressure flux already coexist in a primary-source inequality.  The
term “entrance-flux payment” is R0.74D's design language; the mathematical
architecture in (4.4) is the collision.

**Boundary.** Choe--Yang do not use the lifted Gaussian annuli, the exact
pressure gauge, or the numerator/denominator in (1.1), and they do not assert
the unbounded ratio (1.2).  Their paper cites
[earlier Seregin work](https://www.mathnet.ru/eng/znsl2201) for the
average-free modification.  Because this audit verified only the earlier
paper's metadata and not an identical formula, Seregin is recorded here as a
genealogical pointer rather than promoted to an independent direct collision.

**Collision class:** `DIRECT_FIXED_CENTRE_FLUX_COLLISION`.

### 4.7 Local pressure distribution and harmonic component

**Source.** Joerg Wolf, “On the local pressure of the Navier--Stokes
equations and related systems,” *Advances in Differential Equations* **22**
(2017), nos. 5--6, 305--338, DOI 10.57262/ade/1489802453.
[Official DOI record](https://doi.org/10.57262/ade/1489802453) and
[official arXiv record](https://arxiv.org/abs/1611.01482)

**Supported.** Wolf constructs a local pressure distribution by representing
the relevant distribution as
\(\partial_t\nabla p_h+\nabla p_0\), with a harmonic/local component and a
force-dependent component.  This supplies direct provenance for the broad
local-pressure decomposition used in local-energy analysis.

**Boundary.** Wolf does not use the R0.74D cutoff gauge, whose nonzero frozen
quantity must be retained even when the physical representative is \(p=0\).
It also does not couple a local pressure payment to the 2D3C packet or prove
(1.2).

**Collision class:** `STRUCTURAL_PRESSURE_COMPONENT_COLLISION`.

---

## 5. Precise difference matrix

| Literature family | Directly established component | R0.74D specialization or difference | Why not an exact hit |
|---|---|---|---|
| Biferale--Buzzicotti--Linkmann (2017) | Periodic 2D3C NSE splits into planar 2D NSE plus a passive perpendicular component | R0.74D takes the planar field to be one decaying shear and the passive component to be a localized derivative packet | No Version-A ledger, pressure gauge, parameter sequence, or ratio theorem |
| Coble--He (2024) | Time-dependent shear passive-scalar PDE on \(\mathbb T^2\); explicit heat-evolving sinusoidal shear | Same coefficient shape after phase, amplitude, coordinate, and \(\nu=1\) choices | Enhanced-dissipation objective; no NSE embedding or frozen ratio |
| Cyranka--Zgliczyński (2016) | Large torus average removed through Galilean transformation | Direct precedent for the global-mean operation tested and defeated by a zero-mean witness | Forced stabilization problem; no fixed-centre annular functional |
| Vasseur (2010), Choi--Vasseur (2014) | Mollified trajectory, Galilean blow-up, local weighted mean removal, fast-flow/fixed-cylinder warning | Candidate repairs left open by R0.74D use a genuinely local flow, not a constant global mean | Positive whole-space regularity estimates; no periodic no-go ratio |
| Yang (2022), Vasseur--Yang (2021) | Skewed cylinders following mollified flow, covering/maximal estimates, flux motivation | Supplies rigorous geometry for the next transport-aware branch | Does not test or falsify the frozen Version-A ledger |
| Choe--Yang (2018) | Fixed cutoff, weighted local mean, retained convective and pressure fluxes | Direct precedent for either local-mean or fixed-centre flux repair architecture | Different local-energy functional; no Gaussian annular exterior quantity or divergence theorem |
| Wolf (2017) | Local pressure distribution with harmonic and force pieces | Broad provenance for pressure splitting; R0.74D's exact cutoff gauge is narrower | No 2D3C witness and no quantitative annular ledger |

The matrix has an important asymmetry.  The **family and every proposed
transport-aware repair architecture have substantial prior art**.  The
bounded search failed to locate only the exact quantitative conjunction of
the frozen Version-A observables, every retained payment row, the chosen
parameter sequence, and (1.2).  The latter remains a non-hit, not a novelty
finding.

---

## 6. Claim-to-source ledger

| Claim used in the audit | Primary source | Verification level | Limitation |
|---|---|---|---|
| Periodic 2D3C gives 2D NSE plus passive scalar | Biferale--Buzzicotti--Linkmann (2017), Section II, equations (1)--(2) | Full primary text inspected | Turbulence article, not a theorem about Version-A functionals |
| The passive PDE allows a time-dependent decaying sinusoidal shear on \(\mathbb T^2\) | Coble--He (2024), equation (1.1), Remark 1.1 | Full primary text inspected | No uniform claim for R0.74D's scale-dependent amplitude |
| A torus average velocity may be removed by Galilean transformation | Cyranka--Zgliczyński (2016) | Primary abstract/full-record claim inspected | Forced and different objective |
| Mollified flow and local mean-zero reductions are established in classical 3D NSE estimates | Vasseur (2010); Choi--Vasseur (2014) | Primary papers inspected; exact construction/remarks checked in R0.74C audit and reused here | Positive regularity, not the negative endpoint |
| Skewed cylinders follow mollified incompressible trajectories | Yang (2022); Vasseur--Yang (2021) | Primary article and journal/arXiv records inspected | Different observables and conclusion |
| Fixed-centre mean-free energy retains transport and pressure flux | Choe--Yang (2018), Lemma 6 | Primary formula inspected in the R0.74C audit and reused here | Different cutoff and payment ledger |
| Local pressure admits harmonic and force pieces | Wolf (2017) | Primary abstract and article provenance inspected | Structural only; not the exact R0.74D gauge |
| An exact Version-A theorem identical to (1.2) exists | **Not established** | `EXACT_HIT_NOT_LOCATED` in a bounded search | Cannot support novelty or priority |

All URLs above were checked on 2026-09-01.  A working link verifies access and
metadata, not the truth of any claim beyond the specific inspected passage.

---

## 7. Safe attribution and forbidden claims

A safe description is:

> The R0.74D witness lies in the classical periodic 2D3C/passive-scalar
> invariant class, and its decaying sinusoidal shear coefficient has a direct
> time-dependent passive-scalar precedent.  Galilean/global-mean removal,
> local or mollified mean subtraction, flow-following/skewed cylinders, and
> fixed-centre transport/pressure-flux inequalities are also established
> architectures.  In the bounded primary-source search reported here, no
> theorem was located with the entire frozen R0.74D Version-A conjunction:
> its exact annular ledger and local pressure gauge, its explicit parameter
> sequence, every retained payment row, and divergence of
> \(X_R^A/(P_R^A)^{2/3}\).

The project must not claim any of the following on the basis of this audit:

- “the first 2D3C Navier--Stokes/passive-scalar construction”;
- “a new decaying periodic shear/passive-scalar equation”;
- “the first zero-mean shear witness” or “the first Galilean obstruction”;
- “the first local-mean, flow-following, or skewed-cylinder repair”;
- “the first fixed-centre entrance-flux or pressure-flux formulation”;
- “the first local/harmonic pressure decomposition”;
- “no equivalent theorem exists in the literature”; or
- “R0.74D is original/new” without a substantially broader, independently
  reviewed novelty search.

No “first,” priority, or originality wording is warranted here.  The proper
research-value statement is narrower: R0.74D, if its analytic proof survives
independent proof audit, closes one precisely frozen estimate and identifies
which already-established transport-aware architectures must be tested next.

---

## 8. Residual research boundary

After the collision audit, the remaining mathematical program is not to
market the 2D3C family.  It is to decide, with precisely frozen quantities,
whether any of the established repair architectures can yield a positive
closure:

1. a cylinder following an admissible local or mollified trajectory;
2. a scale-local weighted mean subtraction;
3. a fixed centre with a quantitatively defined signed transport-flux
   payment, separated from its pressure-flux row; or
4. a theorem classifying which transport-aware payments control the exterior
   annular ledger and with what optimal large-payment exponent.

Any future paper should cite the primary sources above at the point where the
invariant class or repair architecture is introduced, then state exactly what
new quantitative claim—if any—survives a fresh literature audit.

**BOUNDED NON-HIT IS NOT NOVELTY OR PRIORITY PROOF.**
