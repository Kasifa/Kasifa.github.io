# R0.74W — bounded primary-literature collision audit for the remote adjacent-inward threshold

## 0. Verdict and claim boundary

This audit asks a narrow question: does a screened primary source already state
the complete R0.74W mechanism for the frozen common-shear packet family?

The mechanism being screened is the conjunction of the following six items.

1. One exact smooth periodic **unforced** Navier--Stokes solution contains a
   deterministic saturated common shear and inversion-paired derivative-heat
   packets.
2. The observation set is an explicit fixed strip in the **adjacent inward
   physical-space shell**, remote from the transported packet centre.
3. Exact all-winding Feynman--Kac disintegration reduces the comparison with
   the free packet to a conditional Brownian-bridge saturation deficit with
   logarithmic rate

   \[
    q(\ell)=\frac{(1/\lambda)^2}{4\ell},
    \qquad \ell=\tau_m/R^2\in[64,65].
    \tag{L.W.1}
   \]

4. The rate separates a uniform survival regime from a uniform shear-sweeping
   regime:

   \[
    \limsup\frac{\log(1/R)}{L^2}<q_{65}
    \quad\Longrightarrow\quad G_m^+/H_m\to1,
    \tag{L.W.2}
   \]

   whereas

   \[
    \liminf\frac{\log(1/R)}{L^2}>q_{64}
    \quad\Longrightarrow\quad G_m^+/H_m\to0
    \tag{L.W.3}
   \]

   on that fixed free-comparator strip.
5. Periodic windings, the inversion partner, the other packet, amplitudes, and
   the shell weight are retained quantitatively rather than suppressed in a
   one-packet model.
6. The R0.74U reserve places packet 2 in the survival regime and yields the
   weighted endpoint obstruction

   \[
    \frac{K_{k_2-1,R}(\tau_2)}{T_*}
    \ge cL_2^{-1/2}e^{\chi(65)L_2^2-CL_2}\longrightarrow\infty,
    \tag{L.W.4}
   \]

   disproving the matching all-shell \(O(T_*)\) upper bound for this frozen
   placement.

**Bounded-search verdict (3 September 2026):** no exact collision with this
six-part conjunction was found in the finite primary-source screen below.
The screen found established neighboring work on exact Navier--Stokes shear
waves, enhanced dissipation and hypoellipticity for passive scalars, scalar
large deviations in shear flows, Brownian-bridge functionals for random shear,
and Fourier--helical residence-time compression.  Those works overlap with
individual ingredients or vocabulary, but not with the R0.74W object,
quantifiers, physical-space shell, or endpoint consequence.

This is a **finite primary-source non-hit**, not a proof of novelty,
nonexistence, priority, correctness, or publishability.  It does not assess
the correctness of any screened source.  **LITERATURE BOUNDARY. NOT CLAY.**

<!-- R074W_LITERATURE_FINITE_NON_HIT -->
<!-- R074W_LITERATURE_NO_NOVELTY_CLAIM -->
<!-- R074W_LITERATURE_NOT_CLAY -->

## 1. Search scope and reproducible query families

The screen used exact-title searches, author-title searches, exact-phrase
searches, and mechanism combinations over arXiv, DOI/publisher metadata, and
ordinary scholarly-web indexing.  Representative query families were:

- `shear flow Brownian bridge passive scalar Feynman--Kac`;
- `enhanced dissipation hypoellipticity shear flow passive scalar`;
- `Navier--Stokes exact solutions background linear shear Kelvin modes`;
- `shear flow large deviations passive scalar periodic flows`;
- `random passive scalar linear shear Brownian bridge`;
- `adjacent inward shell Navier--Stokes`;
- `remote strip shear packet`;
- `packet sweeping conditional Brownian bridge`;
- the exact titles and author combinations listed in Sections 3--8.

The exact-phrase families `adjacent inward shell`, `remote strip`, and the
combined packet-sweeping phrases returned no relevant mathematical match in
this screen.  Search-engine non-return is weak evidence: terminology can vary,
indexing can be incomplete, and inaccessible or future work is not excluded.
The substantive comparison therefore rests on the primary records actually
opened, not on phrase absence alone.

The screen is bounded rather than systematic-review complete.  It did not
claim exhaustive coverage of books, theses, non-indexed proceedings, patents,
private manuscripts, or every citation descendant of the sources below.

## 2. Collision matrix

| Primary source | Main object | Main method/conclusion checked | Genuine overlap with R0.74W | Decisive non-collision |
|---|---|---|---|---|
| Singh--Sridhar (2011/2017) | exact plane shearing waves for incompressible Navier--Stokes | Kelvin-mode construction and parallel-wave-vector superposition | exact Navier--Stokes evolution in a prescribed linear shear geometry | no saturated localized shear, derivative-heat packet, remote physical shell, conditional-bridge threshold, or weighted endpoint obstruction |
| Bedrossian--Coti Zelati (2015) | passive scalar in periodic/channel shear flows | semigroup decay, enhanced dissipation, hypoelliptic/Gevrey regularization | rigorous shear-induced decay and small-diffusivity scaling | global norm/semigroup estimates, not a pointwise adjacent-shell bridge survival threshold inside an exact nonlinear Navier--Stokes family |
| Albritton--Beekie--Novack (2021) | passive scalar with boundary conditions | Hörmander viewpoint and enhanced-dissipation timescales | rigorous hypoelliptic transport-diffusion mechanism | no two-packet inversion architecture, all-winding remote strip, or completed-clock endpoint lower bound |
| Haynes--Vanneste (2014) | passive-scalar dispersion in periodic and shear flows | large-deviation rate functions for far scalar tails | rate-function treatment of remote shear-flow tails | long-time/high-Péclet concentration dispersion, not the R0.74W conditional deficit rate or its shell-weighted Navier--Stokes consequence |
| Camassa--Kilic--McLaughlin (2018/2019) | passive scalar under random white-noise linear shear | exact/random Green functions, Brownian motion/bridge functionals, pointwise PDFs | the closest stochastic-technique overlap: bridge functionals in shear transport | random Majda-model shear and PDF/moment statistics, not deterministic saturated common shear, adjacent-shell packet survival, or (L.W.4) |
| Inage (2026) | coherent same-scale Fourier--helical triads in 3D Navier--Stokes | claimed residence-time compression for low-drift coherent regimes | closest vocabulary-level overlap: Navier--Stokes, dyadic shells, residence time | frequency shells and phase drift, not a physical-space inward annulus, conditional bridge displacement, or a counterexample to a frozen shell-clock upper bound |

The matrix separates an ingredient-level precedent from a theorem-level
collision.  R0.74W makes no novelty claim for Feynman--Kac, Brownian bridges,
large-deviation estimates, Kelvin modes, enhanced dissipation, or dyadic
shells individually.

## 3. Singh--Sridhar: exact plane shearing waves

**Source.** N. K. Singh and S. Sridhar,
[*Plane shearing waves of arbitrary form: exact solutions of the
Navier--Stokes equations*](https://arxiv.org/abs/1101.5507),
arXiv:1101.5507 (2011); later *European Physical Journal Plus* **132**
(2017), 403, DOI
[10.1140/epjp/i2017-11659-5](https://doi.org/10.1140/epjp/i2017-11659-5).

The abstract and construction describe exact incompressible Navier--Stokes
solutions in a background linear shear.  Kelvin modes with parallel,
time-dependent wave vectors can be superposed, and the resulting plane
transverse shearing wave admits unbounded or shear-periodic boundary
conditions.

This is an important exact-flow precedent.  It is not the R0.74W collision:
the R0.74W shear is a deterministic heat-evolved saturation profile, the
packet is spatially tested on an adjacent inward annulus, and the conclusion
is the rate dichotomy (L.W.2)--(L.W.3) followed by the weighted endpoint
obstruction (L.W.4).  None of those four objects is stated in the screened
Singh--Sridhar record.

**Comparison confidence:** high for the object distinction; no correctness
or priority judgment is made.

## 4. Enhanced dissipation and hypoellipticity

### 4.1 Bedrossian--Coti Zelati

**Source.** J. Bedrossian and M. Coti Zelati,
[*Enhanced dissipation, hypoellipticity, and anomalous small noise inviscid
limits in shear flows*](https://arxiv.org/abs/1510.08098),
arXiv:1510.08098 (2015).

The paper studies two-dimensional drift--diffusion equations in which a
passive scalar is advected by a shear flow and dissipated by full or partial
diffusion.  It obtains enhanced semigroup decay and instantaneous
hypoelliptic/Gevrey regularization in periodic and bounded-channel settings.

The overlap is genuine: shear can change the effective dissipation scale of a
passive component.  The theorem type is different.  Its principal observables
are norm decay and regularization of a linear evolution, rather than a
conditional central bridge pinned at a remote physical strip.  It does not
state the rate \(q(\ell)\), retain the R0.74W packet interactions and windings,
or derive (L.W.4).

### 4.2 Albritton--Beekie--Novack

**Source.** D. Albritton, R. Beekie, and M. Novack,
[*Enhanced dissipation and Hörmander's
hypoellipticity*](https://arxiv.org/abs/2105.12308),
arXiv:2105.12308 (2021).

This work treats a passive scalar in a shear flow on a periodic direction and
a bounded transverse direction, including periodic, Dirichlet, and Neumann
conditions.  It relates enhanced-dissipation timescales to the order of
vanishing of the shear derivative through Hörmander-type hypoellipticity.

Again, the overlap is the rigorous shear--diffusion mechanism.  The source
does not test a derivative-heat lobe in an adjacent inward three-dimensional
shell, establish a conditional probability asymptotic of the form (L.W.1),
or convert packet survival into a weighted exterior velocity-cubic endpoint
obstruction.

**Comparison confidence for Section 4:** high for the theorem-object and
observable distinctions.

## 5. Haynes--Vanneste: large-deviation scalar tails

**Source.** P. H. Haynes and J. Vanneste,
[*Dispersion in the large-deviation regime. Part I: shear flows and periodic
flows*](https://arxiv.org/abs/1401.6665), arXiv:1401.6665 (2014),
DOI [10.1017/jfm.2014.64](https://doi.org/10.1017/jfm.2014.64).

The paper develops a large-deviation theory for passive-scalar concentration
tails at distances of order time, using one-parameter eigenvalue problems and
probabilistic methods, with explicit high-Péclet asymptotics for shear flows.
This is the strongest screened precedent for treating remote scalar mass by a
rate function rather than by effective diffusivity alone.

R0.74W nevertheless asks a different conditioned question.  Its rate is the
cost of the saturation-deficit event under a bridge already pinned to a
specific remote packet observation point, over a short scale-dependent time
\(t=\ell R^2\).  Its comparison is relative to a derivative-heat packet and
then inserted into an exact Navier--Stokes shell clock.  The screened
Haynes--Vanneste result does not state that conditional bridge event or the
endpoint consequence (L.W.4).

**Comparison confidence:** high for the regime and downstream-observable
distinctions.

## 6. Camassa--Kilic--McLaughlin: Brownian-bridge functionals in random shear

**Source.** R. Camassa, Z. Kilic, and R. M. McLaughlin,
[*On the symmetry properties of a random passive scalar with and without
boundaries, and their connection between hot and cold
states*](https://arxiv.org/abs/1802.03340), arXiv:1802.03340 (2018),
later *Physica D* **400** (2019), 132124, DOI
[10.1016/j.physd.2019.05.004](https://doi.org/10.1016/j.physd.2019.05.004).

The paper studies deterministic scalar data advected by a Gaussian
white-noise fluctuating linear shear in the Majda model.  It uses exact random
Green functions and Brownian motion/bridge functionals to study pointwise
probability distributions and scalar moments, with free-space and channel
comparisons and Monte Carlo verification.

This is the closest screened technique-level collision because both analyses
use bridge functionals for a shear-transport problem.  The probability spaces
are not the same.  In the Camassa--Kilic--McLaughlin model the velocity shear
itself is random and the observable is the distribution of the random scalar.
In R0.74W the common shear is deterministic; the bridge arises from the heat
kernel conditioned on endpoints, and the random variable is used to estimate
a deterministic Feynman--Kac integral.  The source does not state the adjacent
inward strip geometry, the survival/sweeping threshold (L.W.1), or the
all-component shell-clock obstruction (L.W.4).

**Comparison confidence:** high for the stochastic-model distinction; medium
for the non-hit because the broader random-shear literature was not exhaustively
enumerated.

## 7. Inage: residence-time compression in Fourier--helical shells

**Source.** S.-i. Inage,
[*Structural Reduction Framework and Residence-Time Compression of Coherent
Same-Scale Triadic Interactions in the 3D Navier--Stokes
Equations*](https://doi.org/10.3390/math14091410), *Mathematics* **14**
(2026), article 1410.

The publisher record describes a Fourier--helical decomposition of the
three-dimensional Navier--Stokes nonlinearity into scale-interaction channels.
Its stated main result is a residence-time compression estimate for
amplitude-active, low-phase-drift coherent same-scale triadic families.  The
paper itself disclaims a structural exclusion of the global regularity
problem.

The lexical overlap is unusually close, so the shell distinction is essential:

- Inage's shell is a **Fourier frequency shell**, and the selected time set is
  defined by phase-drift behavior of helical triads.
- R0.74W's shell is a **physical-space annulus**, and the selected strip is
  fixed relative to a free heat-packet comparator.
- Inage's advertised direction is compression of a coherent-triad time set.
- R0.74W proves a scale-dependent survival/sweeping dichotomy and then a lower
  endpoint obstruction for one frozen all-shell upper bound.

Frequency-shell residence does not imply physical-annulus packet survival,
and the latter does not imply a Fourier--helical phase-drift estimate.  The
match is therefore terminological and thematic, not theorem-level.

**Comparison confidence:** high for the shell and state-variable distinction;
this audit makes no claim about the validity of the source's reductions.

## 8. What the screen does and does not support

The sources establish that all of the following are prior themes or tools:

- exact Navier--Stokes solutions in shear geometries;
- passive-component reductions and shear-enhanced dissipation;
- probabilistic and large-deviation analysis of remote scalar tails;
- Brownian motion/bridge functionals in shear transport;
- dyadic shells, coherent interactions, and residence-time language.

Accordingly, none of those phrases should carry an isolated novelty claim in
a future manuscript.  The potentially distinctive unit is only the fully
quantified combination in Section 0, and even for that combination this audit
supports no more than a dated, reproducible, finite non-hit.

The following remain outside the collision result:

1. no exhaustive citation graph or all-database systematic review was run;
2. no claim of novelty, priority, or patentability is made;
3. no peer-review judgment is made;
4. no verification of R0.74W's proof follows from literature non-collision;
5. no fixed-deletion obstruction is obtained merely from (L.W.4);
6. no conclusion for arbitrary suitable weak solutions follows;
7. no Navier--Stokes regularity or singularity theorem follows.

## 9. Audit conclusion

Within this bounded primary-source screen, the nearest stochastic precedent is
Camassa--Kilic--McLaughlin's use of Brownian-bridge functionals for a random
linear shear, the nearest rate-function precedent is Haynes--Vanneste's
large-deviation treatment of scalar dispersion, the nearest exact-flow
precedent is Singh--Sridhar's Kelvin-wave construction, and the nearest
vocabulary collision is Inage's Fourier--helical residence-time compression.

None states the R0.74W conjunction of deterministic saturated common shear,
explicit adjacent-inward physical strip, conditional-bridge deficit threshold
\(q(\ell)\), two-scale survival/sweeping dichotomy, all-winding and cross-packet
control, and the weighted endpoint divergence (L.W.4).

That conclusion is a **bounded non-hit only**.  The mathematical status of
R0.74W must be decided by the primary proof audit and reproducible
certificates, not by this search.  **NOT CLAY.**
