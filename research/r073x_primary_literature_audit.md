# R0.73X primary-literature collision audit

**Audit date:** 2026-09-01

**Status:** `BOUNDED_COMPLETE`

**Claim class:** `PRIMARY_SOURCE_COLLISION_AUDIT / NO_NOVELTY_INFERENCE`

**Ordinary translation path:** `LOCAL_DIRECT_NO_DGX`

**DGX used:** `false`

## 1. Question and bounded-search rule

This audit asks how the localized R0.73X heat-characteristic ledger intersects
the primary literature on

1. localized coarse-grained energy balances;
2. the Duchon--Robert defect and suitable local energy inequality;
3. Gaussian or heat filtering as a continuous scale coordinate;
4. tent-space/Carleson control in the Koch--Tataru theory; and
5. Caffarelli--Kohn--Nirenberg-type epsilon regularity.

Only original papers, author-hosted manuscripts, official publisher records,
and official arXiv records are used as evidence.  The search was deliberately
bounded rather than bibliometrically exhaustive.  In particular, failure to
locate an identical formula or implication is **not** evidence of novelty,
priority, non-existence, or first authorship.

The local object being audited is
[`r073x_localized_heat_characteristic.md`](r073x_localized_heat_characteristic.md),
especially its fixed-cutoff identities (X3.3)--(X6.6) and open estimate
(X8.1).

## 2. Executive conclusion

The broad architecture is already occupied.  Exact spatially filtered
Navier--Stokes momentum and resolved-energy balances, Reynolds/subfilter
stress, signed interscale production, smooth-filter increment commutators,
and Gaussian continuous-scale stress identities are established.  The
Duchon--Robert defect is an established **zero-filter-scale distributional
limit** in the local energy equation.  Suitable weak solutions and modern
dissipative/local-suitable formulations already carry a nonnegative local
energy defect.  None of those results turns a signed finite-scale production
payment into local coercivity.

The Koch--Tataru interface is also established but different in kind.  Its
Carleson quantity is the local spacetime $L^2$ norm of a caloric extension,
paired with the $\sqrt tL^\infty$ component of the solution space and a
bilinear mild fixed-point argument.  It is not a theorem saying that a signed
coarse-grained production integral controls a tent norm of an arbitrary
suitable weak solution.

The closest direct collision found is Runlong Yu's 2026 arXiv preprint on
coarse-grained CKN resolution and pressure--flux work depletion.  It already
uses a localized resolved-energy balance with

\[
 \Pi^\ell=-R^\ell:\nabla U^\ell,
 \qquad
 G^\ell=\Pi^\ell+\nabla\!\cdot(P^\ell U^\ell),
\]

and explicitly leaves the resolved-CKN-badness-to-work-observability
implication unproved.  A companion preprint reduces a potential singular
branch to a conditional NS-realizable invisible defect cascade.  These
preprints substantially narrow any permissible originality claim for R0.73X:
the localized balance, signed-work depletion ledger, pressure/harmonic-tail
obstruction, and conditional detector interface cannot be presented as an
unoccupied framework.  Both 2026 items are arXiv preprints; this audit does
not represent them as peer-reviewed journal publications.

A third directly adjacent preprint by the same author, *Critical Ledgers and
Scale-Defect Cascades for Navier--Stokes* (arXiv:2606.13887), proves a
finite-scale supply--tax ledger and develops finite-window/conditional defect
tests.  It further occupies the general “critical ledger plus invisible
defect” architecture, while explicitly stopping short of an unconditional
regularity theorem.  It does not supply the heat-filtered absolute/tent
estimate in (2.1).

The bounded search did **not** locate a primary source proving the specific
bridge needed by R0.73X:

\[
 \text{energy-class signed heat-scale ledger}
 \quad\Longrightarrow\quad
 \text{local absolute/tent smallness}
 \quad\Longrightarrow\quad
 \text{a CKN epsilon scale}.
\tag{2.1}
\]

This is a bounded negative finding, not a novelty statement.  The missing
part is an estimate, not another exact identity.

## 3. Primary-source collision matrix

| Theme | Primary source and exact identifier | Established content relevant to R0.73X | Boundary for R0.73X |
|---|---|---|---|
| Suitable weak solutions and local energy inequality | L. Caffarelli, R. Kohn, and L. Nirenberg, “Partial regularity of suitable weak solutions of the Navier--Stokes equations,” *Comm. Pure Appl. Math.* **35** (1982), 771--831, [DOI](https://doi.org/10.1002/cpa.3160350604) | Suitable weak formulation, generalized/local energy inequality, and partial regularity with a scale-critical local smallness mechanism | The endpoint is a positive/absolute local criterion, not signed filtered production |
| Direct CKN proof and one-scale velocity/pressure formulation | F.-H. Lin, “A new proof of the Caffarelli--Kohn--Nirenberg theorem,” *Comm. Pure Appl. Math.* **51** (1998), 241--257, [DOI](https://doi.org/10.1002/(SICI)1097-0312(199803)51:3%3C241::AID-CPA2%3E3.0.CO;2-A) | Compactness/Campanato route to partial regularity using scale-invariant velocity and pressure control | No production-to-smallness implication is supplied |
| Dissipation epsilon criterion | A. Vasseur, “A new proof of partial regularity of solutions to Navier--Stokes equations,” *NoDEA* **14** (2007), 753--785, [DOI](https://doi.org/10.1007/s00030-007-6001-4), [author manuscript](https://web.ma.utexas.edu/users/vasseur/documents/preprints/NS2.pdf) | For a suitable solution, sufficiently small \(\limsup_{r\downarrow0}r^{-1}\int_{Q_r}|\nabla u|^2\) yields local boundedness; the proof also exposes the difficult local pressure term | This is a positive dissipation smallness criterion, not a signed flux criterion |
| Improved local energy and epsilon criteria | C. Guevara and N. C. Phuc, “Local energy bounds and epsilon-regularity criteria for the 3D Navier--Stokes system,” *Calc. Var. PDE* **56** (2017), article 68, [DOI](https://doi.org/10.1007/s00526-017-1151-7), [author manuscript](https://www.math.lsu.edu/~pcnguyen/papers_html/Guevara-Phuc-12-29-16.pdf) | Sharpens local energy estimates and several epsilon criteria; treats head pressure as a signed distribution but closes estimates through scale-invariant absolute quantities | “Signed distribution” here does not mean signed production alone is coercive |
| One-scale criterion without pressure | Y. Wang, G. Wu, and D. Zhou, “A regularity criterion at one scale without pressure for suitable weak solutions to the Navier--Stokes equations,” *J. Differential Equations* **267** (2019), 4673--4704, [DOI](https://doi.org/10.1016/j.jde.2019.05.003) | Gives velocity-only one-scale epsilon criteria for suitable weak solutions | Still assumes smallness of an absolute velocity norm; it does not follow from cancellation in \(\Pi_s\) |
| Dissipative/local-suitable equivalence and pressure-free interface | H. Kwon, “The role of the pressure in the regularity theory for the Navier--Stokes equations,” *J. Differential Equations* **357** (2023), 1--31, [DOI](https://doi.org/10.1016/j.jde.2023.01.049), [arXiv](https://arxiv.org/abs/2104.03160) | Proves equivalence of dissipative and local suitable weak formulations and epsilon/short-time regularity results allowing distributional pressure, using a local Leray projection and a harmonic component | Requires local velocity/initial-data smallness and structural decomposition, not merely a signed heat-characteristic payment |
| Local short-time smoothing | H. Jia and V. Šverák, “Local-in-space estimates near initial time for weak solutions of the Navier--Stokes equations and forward self-similar solutions,” *Invent. Math.* **196** (2014), 233--265, [DOI](https://doi.org/10.1007/s00222-013-0468-x), [arXiv](https://arxiv.org/abs/1204.0529) | Propagates local initial regularity for a short time modulo nonlocal harmonic pressure; controls energy entering a good region and then applies partial-regularity machinery | Needs local initial regularity and global/local-energy hypotheses; it is not a fixed-scale production criterion |
| Smooth filtering and generalized central moments | M. Germano, “Turbulence: the filtering approach,” *J. Fluid Mech.* **238** (1992), 325--336, [DOI](https://doi.org/10.1017/S0022112092001733), [publisher](https://www.cambridge.org/core/journals/journal-of-fluid-mechanics/article/abs/turbulence-the-filtering-approach/1B92D8CFAEEB0D6B4ADA6BB31282D378) | Generalized central moments, filtered equations, and the two-filter stress identity | Parent algebra for \(\tau_s\), \(k_s\), and filter composition; not a regularity theorem |
| Increment commutator | P. Constantin, W. E, and E. S. Titi, “Onsager's conjecture on the energy conservation for solutions of Euler's equation,” *Comm. Math. Phys.* **165** (1994), 207--209, [DOI](https://doi.org/10.1007/BF02099744) | Controls mollifier commutators through velocity increments and proves energy conservation above the Onsager threshold | Supplies commutator lineage, not an NS epsilon-regularity bridge at the energy level |
| Smooth coarse-grained local energy flux | G. L. Eyink and H. Aluie, “Localness of energy cascade in hydrodynamic turbulence. I. Smooth coarse-graining,” *Phys. Fluids* **21** (2009), 115107, [DOI](https://doi.org/10.1063/1.3266883), [arXiv](https://arxiv.org/abs/0909.2386) | Exact smooth-filter momentum/energy budgets and signed SGS transfer, with rigorous locality bounds under inertial-range scaling assumptions | Classical parent of the resolved local ledger; the scaling assumptions are not automatic for arbitrary suitable weak solutions |
| Duchon--Robert defect | J. Duchon and R. Robert, “Inertial energy dissipation for weak solutions of incompressible Euler and Navier--Stokes equations,” *Nonlinearity* **13** (2000), 249--255, [DOI](https://doi.org/10.1088/0951-7715/13/1/312), [primary PDF mirror](https://www.karlin.mff.cuni.cz/~prazak/uceni/431-20/lit/Jean_Duchon_2000_Nonlinearity_13_312.pdf) | \(D_\varepsilon(u)\) converges distributionally to a kernel-independent defect \(D(u)\), and the local energy equation contains \(D(u)\) | \(D(u)\) is a zero-scale distributional object; it is not pointwise equal to a fixed positive heat-scale \(\Pi_s\) or \(\mathscr S_s\) |
| Gaussian scale as heat time and exact stress/production | P. L. Johnson, “Energy Transfer from Large to Small Scales in Turbulence by Multiscale Nonlinear Strain and Vorticity Interactions,” *Phys. Rev. Lett.* **124** (2020), 104501, [DOI](https://doi.org/10.1103/PhysRevLett.124.104501), [arXiv](https://arxiv.org/abs/1912.00293); expanded in “On the role of vorticity stretching and strain self-amplification in the turbulence energy cascade,” *J. Fluid Mech.* **922** (2021), A3, [DOI](https://doi.org/10.1017/jfm.2021.490), [arXiv](https://arxiv.org/abs/2102.06844) | Exact spatially local Gaussian-filter stress and multiscale production decomposition; Gaussian variance is a continuous diffusion-scale variable | Strong formula-level collision for the heat covariance and production, but no suitable-weak local regularity theorem |
| Sign of local production | A. Alexakis and S. Chibbaro, “Local energy flux of turbulent flows,” *Phys. Rev. Fluids* **5** (2020), 094604, [DOI](https://doi.org/10.1103/PhysRevFluids.5.094604), [arXiv](https://arxiv.org/abs/2004.14453) | DNS with Gaussian and sharp filters shows local flux has both positive and negative values | Empirical evidence only, but it reinforces the analytic requirement to separate signed payment from absolute control |
| Carleson/tent-type mild solution space | H. Koch and D. Tataru, “Well-posedness for the Navier--Stokes equations,” *Adv. Math.* **157** (2001), 22--35, [DOI](https://doi.org/10.1006/aima.2000.1937), [author manuscript](https://math.berkeley.edu/~tataru/papers/nas.pdf) | Defines \(BMO^{-1}\) using the caloric extension and the scale-invariant cylinder norm, defines \(X\) with both \(\sup_t\sqrt t\|u(t)\|_\infty\) and the local spacetime \(L^2\) component, then proves small-data global and local mild well-posedness by a fixed point | This tent-like norm is an initial-data/mild-solution interface; no implication from signed SGS production to the full \(X\) norm is proved |
| Direct coarse-grained CKN collision | R. Yu, “Coarse-Grained Resolution and Pressure--Flux Work Depletion for Navier--Stokes CKN Badness,” arXiv:2606.25322v1 (2026), [arXiv DOI](https://doi.org/10.48550/arXiv.2606.25322), [record](https://arxiv.org/abs/2606.25322) | Proves a coarse/residual CKN resolution lemma and a fixed-chain localized pressure--flux work depletion identity; explicitly treats leakage, backscatter, pressure gauge, harmonic tails, and signed work | Closest collision.  The crucial coarse-badness-to-work-observability implication is explicitly conditional and unproved |
| Critical-ledger framework collision | R. Yu, “Critical Ledgers and Scale-Defect Cascades for Navier--Stokes,” arXiv:2606.13887v1 (2026), [arXiv DOI](https://doi.org/10.48550/arXiv.2606.13887), [record](https://arxiv.org/abs/2606.13887) | Proves a finite-scale supply--tax reduction and formulates PDE-realizable defect packages, finite-window quotient tests, and a conditional localized transfer program | Directly occupies the broader ledger/defect architecture; its finite-window and conditional results do not prove the R0.73X heat-filtered coercive bridge or global regularity |
| Conditional defect-cascade collision | R. Yu, “Invisible Defect Cascades for Navier--Stokes Regularity,” arXiv:2606.12756v1 (2026), [arXiv DOI](https://doi.org/10.48550/arXiv.2606.12756), [record](https://arxiv.org/abs/2606.12756) | Gives a conditional scale-critical reduction using coarse graining, pressure compatibility, flux, energy, trace, and NS-realizability | Does not exclude the remaining invisible cascade and does not prove global regularity |
| Global dyadic-flux title collision, not validated | R. D. C. dos Santos, “Energy Flux Criteria and Critical Besov Regularity for the 3D Navier--Stokes Equations,” Preprints.org v1 (2026), [DOI](https://doi.org/10.20944/preprints202604.1762.v1), [primary record](https://www.preprints.org/manuscript/202604.1762) | Claims a continuation criterion from an absolute weighted dyadic-flux bound plus an additional Besov hypothesis | The source is explicitly not peer reviewed, is global/frequency-localized rather than local/heat-filtered, and its printed proof has unresolved scaling and inference issues described below; it is not counted as an established theorem |

### 3.1 Source-integrity note on the global dyadic-flux preprint

The Santos preprint is a title-level collision and therefore cannot be
silently omitted.  It does not, however, verify the R0.73X bridge.  Its
assumptions include

\[
 u\in L^3(0,T^*;B^{1/3}_{3,\infty}),
 \qquad
 \sup_j2^{(1+\eta)j}\int_0^{T^*}|\Pi_j(t)|\,dt<\infty,
\tag{3.1}
\]

so the proposed criterion already contains an absolute high-frequency flux
decay and extra Besov regularity; it is neither energy-class only nor a
consequence of signed cancellation.

Direct readback also leaves at least three proof obligations unresolved:

1. under the Navier--Stokes scaling
   \(u_\lambda(x,t)=\lambda u(\lambda x,\lambda^2t)\), the homogeneous
   spatial norm \(\dot B^{s}_{3,\infty}\) scales as \(\lambda^s\), so
   \(s=0\), not \(s=1/3\), is the initial-data critical exponent for
   \(p=3\); the preprint's printed critical-scaling statement is inconsistent
   with this calculation;
2. its time-integrated flux hypothesis is used in the displayed proof as if
   it supplied a pointwise-in-time flux bound before integration; that step
   is not justified by the stated assumption; and
3. summing the weighted initial shell energies requires an
   \(\dot H^s\) initial trace, whereas the stated theorem assumes only the
   energy class and does not provide that trace in the written argument.

Some of these gaps might admit a repaired formulation, but no repair is made
in this audit.  The preprint is therefore recorded as an **unvalidated
neighbor**, not as literature-established support for a flux-to-regularity
theorem.

## 4. Formula-level attribution of the R0.73X ledger

### 4.1 Resolved localized balance: strong classical collision

For a smooth spatial filter,

\[
 \partial_tU-\nu\Delta U+\nabla\!\cdot(U\otimes U)+\nabla P
 =-\nabla\!\cdot R,
 \qquad
 \Pi=-R:\nabla U,
\tag{4.1}
\]

and the resulting pointwise resolved-energy balance are standard in the
Germano/Eyink--Aluie/Johnson line.  Multiplication by a cutoff and integration
by parts necessarily produce the resolved boundary flux.  Yu 2026 places
essentially this same localized signed work inside a CKN-facing fixed-chain
ledger.  Consequently, R0.73X (X3.3)--(X3.6) is best described as a
**heat-coordinate localized reconstruction**, not as a new local energy law.

### 4.2 Gaussian characteristic: established ingredients, narrower bounded finding

Johnson's Gaussian convention is equivalent to heat flow after a fixed
variance normalization.  The covariance formula, positivity of the Gaussian
stress, and exact production decomposition are therefore established
ingredients.  The bounded search did not locate the identical package

\[
 s'(t)=-\nu,
 \quad
 \frac{d}{dt}\int\chi e_{s(t)},
 \quad
 \frac{d}{dt}\int\chi k_{s(t)},
\tag{4.2}
\]

with the fixed cutoff, pressure covariance, centered cubic flux,
carré-du-champ, and suitable-weak defect all displayed simultaneously.
That non-detection supports only the label **local synthesis / explicit
bookkeeping**.  It does not support a first-result claim, because every major
ingredient and the neighboring localized work identity already have direct
precedents.

The sign convention must be frozen when comparing sources:

\[
 \tau_s=P_s(u\otimes u)-P_su\otimes P_su,
 \qquad
 \Pi_s=-\tau_s:\nabla P_su.
\tag{4.3}
\]

With this convention, positive production is a sink of resolved energy.
Johnson's 2020 PRL has a 2021
[erratum](https://doi.org/10.1103/PhysRevLett.126.029901) affecting part of
the strain/rotation decomposition; the Gaussian forced-stress evolution and
scale integral used here are not the corrected item.  The 2021 JFM paper is
the safer source for the expanded formula package.

### 4.3 Duchon--Robert versus fixed heat scale

Duchon--Robert define, for a standard mollifier,

\[
 D_\varepsilon(u)
 =\frac14\int \nabla\varphi_\varepsilon(\xi)\!\cdot\delta u(\xi)
       |\delta u(\xi)|^2\,d\xi,
\tag{4.4}
\]

and pass to a distributional limit as \(\varepsilon\downarrow0\).  The limit
is independent of the mollifier and enters the weak local energy equation.
This is conceptually adjacent to the centered cubic heat-scale term, but the
objects must not be identified without a proved limiting argument:

\[
 \mathscr S_s\quad(s>0)
 \ne
 D(u)\quad\text{as a pointwise identity}.
\tag{4.5}
\]

For suitable solutions, the nonnegative distribution generated by the local
energy inequality can be represented as a Radon measure and then heat-smoothed
by duality.  Kwon's dissipative/local-suitable equivalence confirms the
correct weak-solution neighborhood.  The particular characteristic testing in
R0.73X remains a local derivation; it is not a new defect theory.

### 4.4 Carleson/tent interface: exact mismatch

Koch--Tataru use the caloric extension \(w(t)=e^{t\Delta}u_0\) to define

\[
 \|u_0\|_{BMO^{-1}}
 =\sup_{x,R}
 \left(
  |B(x,R)|^{-1}\int_0^{R^2}\int_{B(x,R)}|w(t,y)|^2\,dy\,dt
 \right)^{1/2},
\tag{4.6}
\]

and their solution norm contains

\[
 \sup_{t>0}\sqrt t\,\|u(t)\|_\infty
 +\sup_{x,R}
 \left(
  |B(x,R)|^{-1}\int_0^{R^2}\int_{B(x,R)}|u(t,y)|^2\,dy\,dt
 \right)^{1/2}.
\tag{4.7}
\]

The theorem then closes the mild equation by bilinear estimates.  The
following substitutions are invalid without additional proof:

* replacing the positive square function in (4.6)--(4.7) by a signed cubic
  production integral;
* dropping the \(\sqrt tL^\infty\) component;
* applying the initial-data fixed-point theorem directly at an interior time
  slice of an arbitrary suitable weak solution; or
* inferring Carleson smallness from the global energy-class
  \(s^{-1/4}\) production bound.

Thus “tent space” is a plausible target geometry, not an already established
consequence of the heat characteristic.

### 4.5 Epsilon regularity: positive quantities remain the endpoint

CKN, Lin, Vasseur, Guevara--Phuc, Wang--Wu--Zhou, and Kwon provide several
different entrances to local regularity.  They share the relevant feature
that the small input is a positive or absolute scale-invariant velocity,
pressure, dissipation, or local-energy quantity.  Cancellation between
forward production and backscatter is not such an input.

At the Navier--Stokes scaling, two natural **candidate diagnostics** for a
heat-scale bridge would be

\[
 \mathcal F_{\theta}(z_0,r)
 =r^{-1}\int_{Q_r(z_0)}
   |\mathscr S_{\theta r^2}|\,dx\,dt,
 \qquad 0<\theta<1,
\tag{4.8}
\]

and

\[
 \mathcal T(z_0,r)
 =r^{-3}\int_{Q_r(z_0)}\int_0^{c r^2}
   |\mathscr S_s|\,ds\,dx\,dt.
\tag{4.9}
\]

The prefactors make the displays scale invariant.  Equations (4.8)--(4.9)
are proposed diagnostic normalizations only.  Their finiteness, smallness,
control by energy data, and implication for a CKN quantity are all unproved.
Pressure covariance, heat tails, cutoff leakage, and the defect measure must
remain in any honest localized version.

## 5. Direct-collision assessment for the open estimate (X8.1)

The open estimate in R0.73X seeks to absorb unsigned cubic and pressure
payments into localized dissipation plus an energy-level remainder.  The
primary-source audit gives the following decision table.

| Proposed step | Audit status | Reason |
|---|---|---|
| Exact fixed-cutoff resolved balance | `KNOWN / DIRECT_COLLISION` | Classical filtered energy balance; Yu 2026 gives a direct CKN-facing localized form |
| Exact Gaussian stress and heat-scale covariance | `KNOWN / DIRECT_COLLISION` | Johnson 2020/2021 after variance normalization |
| Zero-scale cubic defect in weak local energy equation | `KNOWN / DIRECT_COLLISION` | Duchon--Robert 2000 |
| Suitable/dissipative defect formulation with distributional pressure | `KNOWN / DIRECT_COLLISION` | CKN lineage and Kwon 2023 |
| Simultaneous descending-characteristic ledger with every R0.73X term displayed | `LOCAL_SYNTHESIS / NO_PRIORITY_CLAIM` | Identical package not located in the bounded search; ingredients and neighboring ledgers are established |
| Control of \(|\mathscr S_s|\), \(|Q_s\cdot\nabla\chi|\), and Gaussian tails by energy-level local data with an absorbable constant | `OPEN_IN_THIS_LINE` | No inspected source supplies this non-circular estimate |
| Signed characteristic payment implies local absolute/tent smallness | `OPEN_IN_THIS_LINE` | Sign cancellation and backscatter destroy direct coercivity |
| Local absolute/tent smallness implies a CKN epsilon scale | `OPEN_IN_THIS_LINE` | Would require a new quantitative comparison or compactness-rigidity theorem |
| Global regularity or singularity exclusion | `NOT ESTABLISHED` | No inspected result closes the missing implications |

Yu 2026 is particularly important here.  Its resolution lemma separates full
CKN badness into resolved badness and a subfilter residual, while its
depletion theorem pays forward combined work by energy, leakage, and
backscatter.  The paper states that the implication from resolved CKN badness
to observable work is a separate, unproved compactness/separation problem.
R0.73X (X8.1) encounters the same obstruction in heat-filter coordinates,
with the additional need to control Gaussian tails and pressure covariance.

## 6. Known / local / open boundary

### `LITERATURE_ESTABLISHED`

* suitable weak solutions, local energy inequality, and CKN partial
  regularity;
* epsilon criteria based on small positive/absolute scale-invariant
  quantities;
* spatially filtered momentum and resolved-energy equations;
* generalized central moments, Reynolds stress, and signed SGS production;
* Gaussian scale as a diffusion variable and the exact Gaussian stress
  integral;
* Duchon--Robert's zero-scale distributional defect;
* caloric Carleson characterization of \(BMO^{-1}\) and Koch--Tataru
  small-data mild well-posedness;
* localized coarse/residual CKN resolution and fixed-chain signed-work
  depletion in the 2026 arXiv preprint, with its stated conditional boundary.

### `LOCAL_DERIVATION / SYNTHESIS`

* the fixed-cutoff descending heat characteristic with \(s'(t)=-\nu\);
* the simultaneous ledger retaining \(K_s\), \(Q_s\), \(D_{ii,s}\), heat
  tails, time-cutoff payment, and the heat-smoothed suitable-weak defect;
* the exact cancellation converting
  \(\partial_sk_s+D_{ii,s}\) into \(P_s(|\nabla u|^2)\) inside that ledger.

These labels mean only that the formulas are derived in the local research
note and were not located verbatim as a single package.  They do not imply
novelty.

### `OPEN`

* a scale-invariant, non-circular estimate controlling the absolute centered
  cubic, pressure covariance, cutoff leakage, and Gaussian exterior tails at
  the suitable-weak energy level;
* an implication from signed endpoint/characteristic payment to absolute
  local or tent-space smallness;
* a comparison from such heat-scale smallness to a known CKN/Lin/Vasseur/Kwon
  epsilon criterion;
* removal of the positive lower heat-scale cutoff in the weak characteristic
  without hidden uniform integrability;
* exclusion of a residual or combined-invisible NS-realizable cascade.

## 7. Research decision

The next useful theorem should not be another rearrangement of the exact
balance.  It should target one falsifiable bridge and preserve its failure
alternatives.  A defensible sequence is:

1. freeze a scale ratio \(s=\theta r^2\) and define an **absolute**,
   scale-invariant local production-plus-pressure functional;
2. prove or disprove an energy-level localization estimate including
   Gaussian annular tails and harmonic pressure, with no Serrin, Hölder,
   \(L^\infty\), or already-regular norm on the right;
3. if the estimate survives, prove a compactness statement identifying every
   zero-diagnostic limit, rather than assuming production detects CKN
   badness;
4. only then attempt an implication to a published epsilon criterion;
5. retain a residual alternative if high-frequency velocity/pressure
   oscillation is invisible to the fixed heat scale.

The most likely immediate failure mode is not algebraic.  It is the absence
of coercivity caused by signed cancellation, pressure--flux cancellation,
harmonic/exterior pressure, or subfilter residual concentration.  A rigorous
negative result isolating one of these failure modes would still be a valid
research outcome.

## 8. Bounded negative finding and permissible wording

Permissible:

> A bounded primary-source search did not locate a theorem deriving local
> Carleson/tent smallness or a CKN epsilon scale from the R0.73X signed
> heat-characteristic ledger at the suitable-weak energy level.  The closest
> inspected preprints retain the analogous observability step as a condition.

Not permissible:

* “no such theorem exists”;
* “the heat characteristic is novel”;
* “the literature has not connected coarse graining to CKN”;
* “the signed production controls regularity”; or
* any claim of progress on the Clay Millennium problem.

## 9. Machine-readable conclusion

```text
auditStatus=BOUNDED_COMPLETE
sourcePolicy=PRIMARY_ONLY
finiteSearchNoveltyProof=false
localizedResolvedBalance=KNOWN_DIRECT_COLLISION
gaussianHeatStress=KNOWN_DIRECT_COLLISION
duchonRobertDefect=ZERO_SCALE_DISTRIBUTIONAL_NOT_FIXED_SCALE
suitableWeakDefect=KNOWN_FRAMEWORK
kochTataruCarleson=CALORIC_INITIAL_DATA_PLUS_MILD_FIXED_POINT
signedProductionImpliesTentSmallness=NOT_ESTABLISHED
tentSmallnessImpliesCKN=NOT_ESTABLISHED
closestDirectCollision=ARXIV_2606_25322
closestLedgerFramework=ARXIV_2606_13887
closestConditionalCascade=ARXIV_2606_12756
globalDyadicFluxPreprint=UNVALIDATED_NEIGHBOR_PREPRINTS202604_1762_V1
descendingCharacteristicFullLedger=LOCAL_SYNTHESIS_NO_PRIORITY_CLAIM
clayClaim=NONE
ordinaryTranslationPath=LOCAL_DIRECT_NO_DGX
dgxUsed=false
```
