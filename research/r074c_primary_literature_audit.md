# R0.74C — bounded primary-source literature collision audit

**Audit date:** 2026-09-01

**Status:** `EXACT_HIT_NOT_LOCATED / DIRECT_MECHANISM_COLLISIONS_FOUND / BOUNDED_NON_HIT`

**Claim class:** primary-source literature boundary; not a novelty or priority
claim

**Related analytic note:** `r074c_advected_shear_large_payment_obstruction.md`

This note records a bounded primary-source search for collisions with the
R0.74C fixed-centre obstruction.  Three outcomes are kept separate:

1. **Exact hit:** the same frozen R0.74B functionals and pressure gauge, the
   same smooth periodic advected derivative-of-heat-kernel family, and the
   same unbounded ratio theorem.
2. **Direct mechanism collision:** a primary source explicitly uses
   Galilean changes of frame, flow-following or skewed parabolic cylinders,
   local mean subtraction, a large torus mean velocity, or exact shear-wave
   solutions, or retains a fixed-centre mean-free entrance-flux term, but
   does not prove the R0.74C theorem.
3. **Bounded non-hit:** no exact hit was located within the search boundary.
   This is not an exhaustive bibliometric conclusion.

The exact theorem audited here fixes \(\nu=\theta=1\), retains the R0.74B
quantities

\[
 X_R=\mathcal U_{\rm ext}^{\infty}+\mathcal D_{\rm ext},
 \qquad
 P_R=\mathcal E(z_0,8R)^{3/2}
     +\mathcal A_{\rm ext}(z_0,2R;1),
\tag{0.1}
\]

and proves

\[
 \sup_{\substack{0<R<\pi/16\\
 (u,p)\ {\rm smooth\ periodic\ NSE}}}
 \frac{X_R}{P_R^{2/3}}=\infty.
\tag{0.2}
\]

The witnessing family is

\[
 u_{A,R,m}(t,x)
 =A R^2\partial_2K_{t+R^2}^{\rm per}
   \bigl(x_2-q_*-V_m(t-R^2)\bigr)e_1+V_me_2,
 \qquad p=0,
\tag{0.3}
\]

with the exact R0.74C parameter sequence and the frozen local/harmonic
pressure gauge.  A paper discussing only Galilean invariance, shear flows,
or moving cylinders is therefore a component collision, not an exact hit.

---

## 1. Search scope and stopping rule

The search had two waves.

### Wave 1 — provenance of the mechanism

I followed primary sources for:

1. Galilean changes of frame in classical incompressible Navier--Stokes;
2. blow-up arguments along mollified flow trajectories;
3. skewed parabolic cylinders and their maximal functions;
4. local zero-mean reductions for the velocity or convective velocity;
5. suitable weak-solution estimates built from those reductions;
6. large average velocity on a periodic domain;
7. exact plane, unidirectional, or transverse shear solutions;
8. mean-free local-energy inequalities with an explicit transport flux; and
9. local pressure projections and fixed spatial cylinders.

### Wave 2 — exact and synonymous negative statements

I then searched formula and terminology variants for:

- a failure or counterexample to a fixed-centre local-energy estimate under
  Galilean boosts;
- a travelling or advected shear/heat packet escaping a fixed parabolic
  cylinder;
- deletion of a large-payment term from a local-energy closure;
- a ratio of exterior annular energy to a \(2/3\)-power local payment;
- the same construction on \(\mathbb T^3\), including a derivative of the
  periodic heat kernel and a constant transverse drift; and
- synonymous combinations of fixed Eulerian cylinder, large mean flow,
  pressure payment, annular tail, and moving/skewed cylinder.

I stopped when exact queries returned the same moving-frame papers, broad
exact-solution papers, unrelated engineering moving-cylinder literature, or
unrelated uses of “drift” and “travelling bump.”  The search inspected
original journal articles, official publisher pages, official arXiv records,
and author or institutional manuscripts.  It did not exhaust monographs,
theses, every citation chain, inaccessible full texts, every language, or an
unanticipated notation.

---

## 2. Three-level collision result

### 2.1 Exact hit

**No exact hit was located.**

In particular, I did not locate a primary source that simultaneously:

- freezes the R0.74B quantities in (0.1), including the lifted Gaussian
  annular weights and the \(2R\)-scale pressure payment;
- keeps the spatial centre fixed while allowing an arbitrary constant mean
  velocity;
- uses the periodic family (0.3), whose fluctuating shear has zero spatial
  mean while the total velocity has mean \(V_me_2\), including all periodic
  copies and the frozen pressure gauge;
- makes the explicit \((M_m,R_m,A_m)\) choice from R0.74C; and
- proves the quantified divergence (0.2).

### 2.2 Direct mechanism collisions

The broad obstruction mechanism has strong direct precedents:

- Vasseur explicitly moves to another local frame along a mollified flow to
  overcome the transport term;
- Choi--Vasseur combine Galilean invariance, trajectories, and a scaling that
  gives zero mean to the velocity and convective velocity, and explicitly
  warn that a fast flow can cross a fixed cylinder before viscosity has time
  to regularize it;
- Yang builds maximal functions on skewed cylinders following mollified
  trajectories, states that the purpose is to remove mean velocity, and
  identifies uncontrolled flux as an obstruction to parabolic smoothing;
- Vasseur--Yang use those skewed cylinders in suitable-solution derivative
  estimates;
- Choe--Yang retain the transport flux in a fixed-centre local-energy
  inequality after subtracting a weighted spatial mean;
- Kwon--Ożański use Galilean invariance and a zero local mean in the
  hypodissipative analogue;
- Cyranka--Zgliczyński treat large average velocity on a torus through
  Galilean transformation; and
- Singh--Sridhar construct arbitrary-profile exact plane transverse waves;
  the zero-shear specialization followed by a Galilean boost already covers
  the PDE witness class used by R0.74C.

These sources mean that R0.74C must not claim the first use of a moving
frame, the first skewed cylinder, the first zero-mean Galilean reduction, the
first recognition that mean transport matters, or a new class of exact shear
solutions in broad terms.  It also cannot claim the first fixed-centre
mean-free entrance-flux formulation.

### 2.3 Bounded non-hit

The bounded non-hit concerns only the exact quantitative theorem (0.2) for
the frozen R0.74B ledger.  An equivalent negative result may be hidden in a
remark, exercise, different functional language, or literature outside the
search boundary.

---

## 3. Primary-source provenance

### 3.1 Local change of frame along a mollified flow

**Source.** Alexis F. Vasseur, “Higher derivatives estimate for the 3D
Navier--Stokes equation,” *Annales de l'Institut Henri Poincare C, Analyse
non lineaire* **27** (2010), no. 5, 1189--1204, DOI
10.1016/j.anihpc.2010.05.002.
[Official journal page](https://ems.press/journals/aihpc/articles/4076951)
and [official archival PDF](https://www.numdam.org/article/AIHPC_2010__27_5_1189_0.pdf)

**Supported.** Vasseur identifies the transport term
\((u\cdot\nabla)\nabla u\) as the main obstruction to a direct parabolic
estimate and says that the solution is considered “in another frame,
locally.”  The paper mollifies \(u\), defines the flow

\[
 \partial_sX(s,t,x)=u_\varepsilon(s,X(s,t,x)),
 \qquad X(t,t,x)=x,
\tag{3.1}
\]

and performs the local blow-up along that trajectory.  Its abstract
explicitly attributes the resulting estimates to Galilean invariance of the
transport part.

**Boundary.** The result is a positive higher-derivative estimate on
\(\mathbb R^3\).  It does not give the fixed-centre negative theorem (0.2),
the periodic heat-kernel witness, or the R0.74B annular ledger.

**Collision class:** `DIRECT_MECHANISM_COLLISION`.

### 3.2 Galilean trajectory scaling and local mean removal

**Source.** Kyudong Choi and Alexis F. Vasseur, “Estimates on fractional
higher derivatives of weak solutions for the Navier--Stokes equations,”
*Annales de l'Institut Henri Poincare C, Analyse non lineaire* **31**
(2014), no. 5, 899--945, DOI 10.1016/j.anihpc.2013.08.001.
[Official archival PDF](https://www.numdam.org/item/AIHPC_2014__31_5_899_0.pdf)
and [official arXiv record](https://arxiv.org/abs/1105.1526)

**Supported.** The paper states that its blow-up construction uses Galilean
invariance.  At each point and scale it follows an incompressible flow and
defines a transformed velocity by subtracting a mollified velocity along
the trajectory.  The authors state that the designed scaling gives the
mean-zero property to both the velocity and the convective velocity.  More
directly for the present collision, the introduction observes that a fast
flow through a fixed \(Q(1)\) can leave the region before viscosity completes
the local regularization.  This is the closest qualitative precursor located
for the R0.74C fixed-cylinder escape mechanism.

**Boundary.** This is a positive regularization theorem in whole space.
The local observable, scale-optimal inputs, and conclusion differ from
(0.1)--(0.2).  It neither states nor needs the R0.74C advected heat packet.

**Collision class:** `DIRECT_MECHANISM_COLLISION`.

### 3.3 Skewed cylinders generated by incompressible flows

**Source.** Jincheng Yang, “Construction of maximal functions associated
with skewed cylinders generated by incompressible flows and applications,”
*Annales de l'Institut Henri Poincare C, Analyse non lineaire* **39**
(2022), no. 4, 793--818, DOI 10.4171/aihpc/20.
[Official journal PDF](https://ems.press/content/serial-article-files/28646)
and [official arXiv record](https://arxiv.org/abs/2008.05588)

**Supported.** Yang defines a skewed cylinder as a tubular neighbourhood of
a mollified-flow trajectory, proves weak \((1,1)\) and strong \((p,p)\)
bounds for the subordinate maximal function, and applies it to 3D
Navier--Stokes derivative estimates.  The introduction explicitly says that
the advantage is to take out mean velocity and work in a neighbourhood
following the flow rather than in a fixed parabolic cylinder.  It also
states that, without flux control, parabolic regularization cannot overcome
the nonlinearity.  That statement is a direct precursor to the proposed
entrance-flux repair, not merely to the moving-cylinder repair.

**Boundary.** The paper supplies the moving geometry and covering theory,
not a counterexample to a fixed-centre annular inequality.  Its cylinders
track a mollified nonlinear flow, whereas the first R0.74C remedy to test is
the simpler constant-mean path.

**Collision class:** `DIRECT_MECHANISM_COLLISION`.

### 3.4 Suitable solutions and the local-to-global skewed-cylinder step

**Source.** Alexis F. Vasseur and Jincheng Yang, “Second derivatives
estimate of suitable solutions to the 3D Navier--Stokes equations,”
*Archive for Rational Mechanics and Analysis* **241** (2021), no. 2,
683--727, DOI 10.1007/s00205-021-01661-4.
[Official publisher page](https://link.springer.com/article/10.1007/s00205-021-01661-4)
and [official arXiv record](https://arxiv.org/abs/2009.14291)

**Supported.** The paper proves local Lorentz-space estimates for second
derivatives of suitable weak solutions.  Its local-to-global step uses the
maximal function for skewed cylinders, while the local analysis uses a
zero-mean reduction and vorticity estimates without an a priori pressure
bound.

**Boundary.** This establishes that moving-frame technology is already part
of classical 3D suitable-solution analysis.  It does not prove (0.2), use a
periodic large-payment ledger, or decide whether the R0.74B \(+P\) term is
sharp.

**Collision class:** `DIRECT_MECHANISM_COLLISION`.

### 3.5 Zero local mean in a Galilean-invariant fractional analogue

**Source.** Hyunju Kwon and Wojciech S. Ożański, “Local regularity of weak
solutions of the hypodissipative Navier--Stokes equations,” *Journal of
Functional Analysis* **282** (2022), no. 7, article 109370, DOI
10.1016/j.jfa.2021.109370.
[Official journal page](https://www.sciencedirect.com/science/article/pii/S0022123621004523)
and [official arXiv record](https://arxiv.org/abs/2010.12105)

**Supported.** For fractional dissipation \(s\in(3/4,1)\), the authors use
Galilean invariance to reduce the local regularity theorem to solutions with
zero \(\psi\)-mean velocity at every time.  The proof then restores the
general situation by a flow map for the mollified velocity.

**Boundary.** The equation is hypodissipative, not the classical \(s=1\)
system frozen in R0.74C.  It is therefore corroborating mechanism evidence,
not an exact collision.

**Collision class:** `DIRECT_MECHANISM_COLLISION / DIFFERENT_DISSIPATION`.

### 3.6 Large average velocity on a torus

**Source.** Jacek Cyranka and Piotr Zgliczyński, “Stabilizing effect of
large average initial velocity in forced dissipative PDEs invariant with
respect to Galilean transformations,” *Journal of Differential Equations*
**261** (2016), no. 8, 4648--4708, DOI 10.1016/j.jde.2016.07.007.
[Official journal page](https://www.sciencedirect.com/science/article/pii/S0022039616301723)
and [official arXiv record](https://arxiv.org/abs/1407.1712)

**Supported.** The paper treats dissipative PDEs on a torus and converts a
large average initial velocity, by Galilean transformation, into rapidly
oscillating forcing.  It includes forced incompressible 2D Navier--Stokes
and establishes a local attracting solution statement for the forced 3D
system.

**Boundary.** The problem is forced and dynamical; its large mean velocity
has a stabilizing averaging role.  It does not study fixed-centre local
energy functionals or prove their failure.  Its stabilization framework
illustrates that torus mean velocity remains dynamically visible to an
observable that is not Galilean invariant; this is an inference here, not a
theorem stated by the authors.

**Collision class:** `DIRECT_MECHANISM_COLLISION / DIFFERENT_OBJECTIVE`.

### 3.7 Exact plane transverse shearing waves

**Source.** Nishant K. Singh and S. Sridhar, “Plane shearing waves of
arbitrary form: exact solutions of the Navier--Stokes equations,”
*European Physical Journal Plus* **132** (2017), article 403, DOI
10.1140/epjp/i2017-11659-5.
[Official arXiv record](https://arxiv.org/abs/1101.5507)

**Supported.** The paper constructs exact incompressible Navier--Stokes
solutions in a background linear shear and superposes parallel Kelvin modes
to obtain plane transverse shearing waves of arbitrary profile, including
shear-periodic settings.  When the background shear is set to zero, this
class reduces to a one-dimensional transverse profile undergoing viscous
heat evolution, and shear-periodicity reduces to ordinary periodicity.  A
standard Galilean boost then adds a constant transverse drift.  Thus the
paper already covers the PDE witness class of (0.3), although not the
particular frozen functional test.

**Boundary.** The paper does not introduce the R0.74B annular quantities,
the frozen pressure gauge, the R0.74C parameter sequence, or the divergence
of (0.2).  The collision is therefore with the exact witness class, not with
the quantitative no-go theorem.

**Collision class:** `DIRECT_WITNESS_CLASS_COLLISION`.

### 3.8 Local pressure projections

**Source.** Jörg Wolf, “On the local pressure of the Navier--Stokes
equations and related systems,” *Advances in Differential Equations* **22**
(2017), nos. 5--6, 305--338, DOI 10.57262/ade/1489802453.
[Official DOI record](https://doi.org/10.57262/ade/1489802453)
and [official arXiv record](https://arxiv.org/abs/1611.01482)

**Supported.** Wolf constructs a local pressure distribution with harmonic
and force-dependent pieces, providing primary-source provenance for local
pressure projections in suitable local-energy analysis.

**Boundary.** The paper does not address a large uniform drift or the
R0.74C pressure-gauge estimate.  In the R0.74C witness the physical pressure
is zero; the nonzero frozen gauge arises solely because the R0.74B local
projection is retained.  That exact ledger remains outside Wolf's result.

**Collision class:** `STRUCTURAL_COMPONENT_COLLISION`.

### 3.9 Fixed-centre mean-free energy with retained flux

**Source.** Hi Jun Choe and Minsuk Yang, “Local kinetic energy and
singularities of the incompressible Navier--Stokes equations,” *Journal of
Differential Equations* **264** (2018), no. 2, 1171--1191, DOI
10.1016/j.jde.2017.09.036.
[Official journal page](https://www.sciencedirect.com/science/article/pii/S0022039617305211)
and [official arXiv record](https://arxiv.org/abs/1705.04561)

**Supported.** Lemma 6 keeps a fixed nonnegative spatial cutoff \(\varphi\)
normalized by \(\int\varphi\,dx=1\), and defines the weighted spatial mean
and fluctuation

\[
 [v]_r(t)=\int v(x,t)\varphi(x)\,dx,
 \qquad v^\circ=v-[v]_r,
\tag{3.2}
\]

and proves a mean-free localized energy inequality which retains the exact
transport-flux row

\[
 \int v\cdot\nabla\varphi\,|v^\circ|^2\theta\,dx\,dt,
\tag{3.3}
\]

along with the pressure row
\(2\int p\,v^\circ\cdot\nabla\varphi\,\theta\,dx\,dt\).  The paper attributes
this average-free modification to earlier work including
[Seregin's Lemma 2.1](https://www.mathnet.ru/eng/znsl2201); the genealogy
therefore predates 2018.

**Boundary.** This is a direct fixed-centre, local-mean-subtracted
entrance-flux precedent.  It neither uses the lifted annular observables in
(0.1) nor proves that the particular R0.74B ratio is unbounded.  It does,
however, rule out presenting “fixed centre plus a retained transport flux”
as a new repair architecture.

**Collision class:**
`DIRECT_MECHANISM_COLLISION / FIXED_CENTRE_FLUX_PRECEDENT`.

---

## 4. Precise difference matrix

| Literature family | What the source establishes | Difference from R0.74C | Why it is not an exact hit |
|---|---|---|---|
| Vasseur (2010), Choi--Vasseur (2014) | Galilean blow-up along a mollified trajectory; local mean removal; explicit warning that fast flow can cross a fixed cylinder before viscous regularization | Positive whole-space regularity estimates versus a negative periodic fixed-centre endpoint theorem | No frozen annular tail, no R0.74B pressure payment, and no divergence of \(X_R/P_R^{2/3}\) |
| Yang (2022), Vasseur--Yang (2021) | Skewed cylinders following mollified flow, covering/maximal estimates, local derivative bounds, and an explicit flux-control motivation | Nonlinear moving geometry and local-to-global regularity versus a frozen fixed-centre ledger | They motivate both flow-following and flux repairs but do not falsify the R0.74B inequality |
| Kwon--Ożański (2022) | Galilean transform and zero local mean for scale-optimal local regularity | Fractional dissipation \(s<1\), different inputs and conclusion | Different PDE and no periodic large-payment theorem |
| Cyranka--Zgliczyński (2016) | Large torus mean velocity converted into oscillatory forcing by Galilean transformation | Forced dynamical stabilization rather than unforced local-energy escape | No fixed-centre functional or endpoint ratio |
| Singh--Sridhar (2017) | Arbitrary-profile exact transverse waves; zero shear plus a Galilean boost covers the heat-evolved advected witness class | Same broad PDE witness class, different quantitative objective | No R0.74B quantities, gauge, parameter sequence, or no-go theorem |
| Choe--Yang (2018) | Fixed-centre weighted-mean subtraction with the exact \(v\cdot\nabla\varphi|v^\circ|^2\) transport flux retained | Positive mean-free local-energy inequality versus a negative test of one annular ledger | No lifted Gaussian exterior functional, frozen gauge, or unbounded endpoint ratio |
| Wolf (2017) | General local pressure projection and harmonic component | Pressure provenance only | Does not couple the gauge to the advected packet or the payment ledger |

---

## 5. Research-value boundary after the collision audit

The literature changes the interpretation of R0.74C in a useful way.

### Established before R0.74C

The following broad principles are established in the cited literature:

- transport can be handled by changing to a local moving frame;
- local mean velocity should be removed in scale-optimal estimates;
- skewed cylinders following mollified trajectories support a rigorous
  maximal-function and covering theory;
- a fast flow can traverse a fixed observation cylinder before viscosity
  supplies the desired local regularization;
- arbitrary-profile transverse heat-evolved waves and their Galilean boosts
  already supply the broad exact PDE witness class; and
- fixed-centre mean-free local energy can be written with an explicit
  transport-flux row retained.

### What R0.74C adds, if the proof and certificate remain valid

R0.74C supplies a narrower quantitative statement:

1. it tests one completely frozen annular-tail/payment inequality rather
   than a generic regularity slogan;
2. it deploys a particular exact smooth periodic representative of the known
   transverse-wave/Galilean class against that frozen ledger;
3. it retains the declared local pressure gauge even though the physical
   pressure is zero;
4. it pays every local-energy, exterior-cubic, harmonic, periodic-copy, and
   background-velocity row; and
5. it proves that the specific ratio in (0.2) is unbounded.

The remaining potentially original content is therefore the narrow
conjunction of the frozen R0.74B ledger, its specified local pressure gauge,
the explicit parameter sequence, and the unbounded ratio theorem.  This is a
rigorous branch-closing result and a design constraint, but not yet a
standalone high-level resolution.  The strongest publication direction is to
pair it with a positive co-moving closure or a broader classification theorem
for admissible transport/entrance-flux payments.

---

## 6. Safe attribution boundary

A research note may say:

> Flow-following Galilean reductions, local mean subtraction, skewed
> parabolic cylinders, exact transverse heat-wave witnesses, and fixed-centre
> mean-free flux inequalities have direct primary-source precedents.  In the
> bounded search described here, I did not locate the exact R0.74C
> conjunction: the frozen R0.74B ledger and pressure gauge, the explicit
> parameter sequence, and divergence of \(X_R/P_R^{2/3}\) after every declared
> payment row is retained.

It must not say “first moving-frame argument,” “first skewed cylinder,”
“first Galilean obstruction,” “first exact shear counterexample,” or “the
literature contains no such negative estimate.”  It also must not say “new
exact advected heat/shear solution family” or “first fixed-centre
entrance-flux formulation.”

The next positive question should cite the Vasseur--Choi--Yang line explicitly
and distinguish between:

1. a constant-mean co-moving centre;
2. a mollified-flow trajectory and admissible skewed cylinder; and
3. a fixed centre supplemented by a quantitatively specified entrance-flux
   payment, explicitly distinguished from the Choe--Yang mean-free local
   energy inequality.

**bounded non-hit is not novelty/priority proof**
