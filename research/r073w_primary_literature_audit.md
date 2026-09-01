# R0.73W primary-literature audit

**Audit date:** 2026-09-01

**Status:** `BOUNDED_COMPLETE`

**Question:** which parts of the R0.73W signed-production package are already
established, which are direct reformulations, and which formulas were not
located verbatim in a bounded primary-source search?

**Ordinary translation path:** `LOCAL_DIRECT_NO_DGX`

**DGX used:** `false`

## 1. Audit conclusion

The Gaussian stress formula in R0.73W is not new.  It is exactly the
heat-semigroup normalization of Perry L. Johnson's 2020 and 2021 Gaussian
filter identities.  With Johnson's filter width \(\ell\), the conversion is

\[
 P_s=e^{s\Delta},\qquad s={\ell^2\over2}.
\tag{1.1}
\]

Under (1.1), Johnson's forced diffusion equation, exact stress integral, and
production \(-\tau:S\) agree term by term with the current formulas.

The local resolved-energy law is the standard coarse-grained energy balance
used by Eyink, Aluie, Johnson, and the LES literature.  The combined operator
\(\partial_t-\nu\partial_s\) is a one-step heat-coordinate rewrite of that
classical equation.  The bounded search did not locate the identical combined
display, but non-detection does not make it a new cascade theorem.

The centered-increment split is in the direct lineage of Germano generalized
central moments, Constantin--E--Titi increment commutators, and the
Duchon--Robert local energy defect.  The current finite-scale centering and
coefficient are derived explicitly and independently audited; no priority
claim is made.

The bounded search did not locate the exact \(s^{-1/4}\) energy-class estimate
or the exact \(s^{-1/2}\)-weighted production display.  Both are short
corollaries of established ingredients: Johnson's exact stress formula,
standard heat estimates, the heat representation of \(L^{-1/2}\), and the
classical critical \(H^{1/2}\) Navier--Stokes structure.  They are described
as current synthesis and corollaries, not as first results.

## 2. Direct formula collision with Johnson

Johnson uses

\[
 G_\ell(x)=(2\pi\ell^2)^{-3/2}
 e^{-|x|^2/(2\ell^2)},\qquad
 \widehat G_\ell(k)=e^{-|k|^2\ell^2/2}.
\tag{2.1}
\]

Thus \(\overline a^{\,\ell}=P_sa\) under (1.1).  Equation (10) of Johnson
2020 can be written

\[
 \sigma_{ij}^{\ell}
 =\int_0^{\ell^2}d\theta\,
 P_{(\ell^2-\theta)/2}\left[
 \partial_kP_{\theta/2}u_i\,
 \partial_kP_{\theta/2}u_j\right].
\tag{2.2}
\]

Set \(\theta=2r\).  Then

\[
 \sigma_{ij}^{\ell}
 =2\int_0^sP_{s-r}\left[
 \partial_kv_{r,i}\partial_kv_{r,j}
 \right]dr
 =\tau_{ij,s}.
\tag{2.3}
\]

Because the stress is symmetric,

\[
 -\tau_s:\nabla v_s=-\tau_s:S_s.
\tag{2.4}
\]

Equations (2.3)--(2.4) are an exact collision, not a merely analogous result.
The 2021 JFM paper supplies the fuller and corrected presentation and is the
preferred primary attribution.

## 3. Primary-source matrix

| Claim family | Primary source | Formula-level relevance | R0.73W treatment |
|---|---|---|---|
| Gaussian forced diffusion and exact stress integral | P. L. Johnson, “Energy Transfer from Large to Small Scales in Turbulence by Multiscale Nonlinear Strain and Vorticity Interactions,” *Physical Review Letters* **124** (2020), 104501, [DOI](https://doi.org/10.1103/PhysRevLett.124.104501), [accepted manuscript](https://link.aps.org/accepted/10.1103/PhysRevLett.124.104501) | Eqs. (7)--(10) give the Gaussian kernel, heat equation in \(\ell^2\), forced stress diffusion, and exact scale integral; Eq. (12) decomposes production into strain/vorticity mechanisms | `VERIFIED_CLASSICAL`; exact normalization shown in Section 2 |
| Corrected and expanded Gaussian stress, increments, and local energy law | P. L. Johnson, “On the role of vorticity stretching and strain self-amplification in the turbulence energy cascade,” *Journal of Fluid Mechanics* **922** (2021), A3, [DOI](https://doi.org/10.1017/jfm.2021.490), [arXiv](https://arxiv.org/abs/2102.06844) | Eqs. (20), (22)--(23), (38), and (43)--(47) cover generalized covariance, filtered NS/energy, increment covariance, Gaussian forced diffusion, and its exact integral | Preferred direct citation for stress, production, and deviatoric mechanism |
| General smooth-filter local energy flux | G. L. Eyink and H. Aluie, “Localness of energy cascade in hydrodynamic turbulence, I. Smooth coarse-graining,” *Physics of Fluids* **21** (2009), 115107, [DOI](https://doi.org/10.1063/1.3266883), [arXiv](https://arxiv.org/abs/0909.2386) | Eqs. (2)--(5) give filtered NS, stress, pointwise resolved-energy balance, and \(\Pi=-(\partial_j\bar u_i)\tau_{ij}\) for smooth kernels | Classical parent of the local energy equation |
| Generalized central moments and filter composition | M. Germano, “Turbulence: the filtering approach,” *Journal of Fluid Mechanics* **238** (1992), 325--336, [DOI](https://doi.org/10.1017/S0022112092001733), [publisher](https://www.cambridge.org/core/journals/journal-of-fluid-mechanics/article/abs/turbulence-the-filtering-approach/1B92D8CFAEEB0D6B4ADA6BB31282D378) | Generalized central moments and the two-filter identity; Gaussian widths compose by addition of variances | Algebraic lineage of \(\tau_{s+t}=P_t\tau_s+\tau_t(P_su)\) and \(K_s\) |
| Increment commutator and Onsager estimate | P. Constantin, W. E, and E. S. Titi, “Onsager's conjecture on the energy conservation for solutions of Euler's equation,” *Communications in Mathematical Physics* **165** (1994), 207--209, [DOI](https://doi.org/10.1007/BF02099744), [author PDF](https://web.math.princeton.edu/~weinan/papers/misc1.pdf) | Periodic mollifier stress is written and bounded through velocity increments | General increment/commutator lineage; no heat Duhamel attribution |
| Weak local energy defect | J. Duchon and R. Robert, “Inertial energy dissipation for weak solutions of incompressible Euler and Navier--Stokes equations,” *Nonlinearity* **13** (2000), 249--255, [DOI](https://doi.org/10.1088/0951-7715/13/1/312), [primary PDF mirror](https://www.karlin.mff.cuni.cz/~prazak/uceni/431-20/lit/Jean_Duchon_2000_Nonlinearity_13_312.pdf) | Defines the cubic increment defect with the kernel-gradient contraction and passes to the zero-filter-scale distributional limit | Zero-scale weak limit, not the fixed-\(s\) identity; supports the defect boundary |
| Early local energy flux | G. L. Eyink, “Local energy flux and the refined similarity hypothesis,” *Journal of Statistical Physics* **78** (1995), 335--351, [DOI](https://doi.org/10.1007/BF02183352) | Defines local coarse-grained subscale flux and its increment scaling | Historical attribution for signed local flux |
| Exact multiscale gradient expansion | G. L. Eyink, “Multi-Scale Gradient Expansion of the Turbulent Stress Tensor,” *Journal of Fluid Mechanics* **549** (2006), 159--190, [arXiv](https://arxiv.org/abs/nlin/0512022) | Convergent multiscale/gradient expansion of exact turbulent stress | Related but not identical to Johnson's one-parameter Gaussian Duhamel formula |
| Gaussian variance as scale time | F. Hamba, “Scale-space energy density for inhomogeneous turbulence based on filtered velocities,” *Journal of Fluid Mechanics* **931** (2022), A34, [publisher](https://www.cambridge.org/core/journals/journal-of-fluid-mechanics/article/scalespace-energy-density-for-inhomogeneous-turbulence-based-on-filtered-velocities/C026E5393FAFE310FD237720E77D31DE) | Gaussian variance is an additive scale coordinate satisfying a diffusion equation | Direct precedent for heat scale as a coordinate; its statistical energy density is a different object |
| Critical \(H^{1/2}\) Navier--Stokes structure | H. Fujita and T. Kato, “On the Navier--Stokes initial value problem. I,” *Archive for Rational Mechanics and Analysis* **16** (1964), 269--315, [DOI](https://doi.org/10.1007/BF00276188) | Classical fractional-power, critical small-data framework | The R0.73W \(s^{-1/2}\) average recovers this type of critical cubic balance; it does not extend it to arbitrary energy |
| Both signs of local energy flux in DNS | A. Alexakis and S. Chibbaro, “Local energy flux of turbulent flows,” *Physical Review Fluids* **5** (2020), 094604, [DOI](https://doi.org/10.1103/PhysRevFluids.5.094604) | Numerical/physical evidence for local forward transfer and backscatter | Context only; the exact finite certificate carries the universal counterexample |
| Carré-du-champ terminology | D. Bakry and M. Émery, “Diffusions hypercontractives,” *Séminaire de probabilités XIX* (1985), 177--206, [Numdam](https://numdam.org/item/SPS_1985__19__177_0/) | Foundational \(\Gamma\)-calculus language for diffusion generators | Terminology only; no claim that the paper prints the current turbulence formula verbatim |

## 4. Attribution of each R0.73W formula family

### 4.1 Heat covariance

For the Laplacian generator,

\[
 \Gamma(f,g)={1\over2}[\Delta(fg)-f\Delta g-g\Delta f]
 =\nabla f\cdot\nabla g.
\tag{4.1}
\]

The semigroup interpolation

\[
 P_s(fg)-P_sf\,P_sg
 =2\int_0^sP_{s-r}\Gamma(P_rf,P_rg)\,dr
\tag{4.2}
\]

is simultaneously the heat-semigroup covariance formula, the continuous
Gaussian specialization of Germano filter composition, and the exact
turbulence stress formula used by Johnson.  Turbulence-facing prose must cite
Johnson; mathematical prose may additionally use the \(\Gamma\) language.

### 4.2 Local heat-plane energy law

Eyink--Aluie 2009 and Johnson 2021 contain the classical filtered local-energy
equation.  The extra identity

\[
 \partial_s{|v_s|^2\over2}
 =\Delta{|v_s|^2\over2}-|\nabla v_s|^2
\tag{4.3}
\]

combines its two viscous terms into \(-\nu\partial_s\).  R0.73W therefore
labels the result `CLASSICAL_FILTERED_ENERGY_IN_HEAT_COORDINATES`, not a new
energy-cascade theorem.

### 4.3 Centered increments and weak defects

Germano owns the generalized-central-moment ledger, and
Constantin--E--Titi/Eyink own the increment commutator lineage.  The
Duchon--Robert defect is a zero-scale distributional limit of a cubic
kernel-gradient expression.  It must not be identified pointwise with a
fixed positive-scale \(\Pi_s\) or \(\mathscr S_s\).

For smooth fields, the centered split in R0.73W is a direct finite-scale
algebraic identity.  For suitable weak solutions, the local trace equation
may carry an additional nonnegative energy-defect measure.  This is why the
public theorem separates its smooth and weak statements.

### 4.4 The \(s^{-1/4}\) bound

No inspected primary source displayed

\[
 \|\Pi_s\|_{L^1_{t,x}}
 \lesssim s^{-1/4}
 \|u\|_{L_t^\infty L_x^2}
 \|\nabla u\|_{L^2_{t,x}}^2
\tag{4.4}
\]

verbatim.  It follows directly from Johnson's exact stress integral,

\[
 \|\tau_s(t)\|_1\le2s\|\nabla u(t)\|_2^2,
\tag{4.5}
\]

and the standard three-dimensional heat estimate

\[
 \|\nabla P_su(t)\|_\infty
 \le Cs^{-5/4}\|u(t)\|_2.
\tag{4.6}
\]

It is therefore an energy-class corollary built from established ingredients.
The negative search does not support novelty or optimality language.

### 4.5 The critical \(s^{-1/2}\) average

The identity

\[
 \int_0^\infty s^{-1/2}e^{-2sL}\,ds
 =\sqrt{\pi/2}\,L^{-1/2}
\tag{4.7}
\]

is the standard heat-semigroup representation of a fractional inverse.  When
applied to the spatial mean of production it yields a zero-order Riesz
trilinear form.  The bounded search did not locate that exact turbulence
display, but the operator identity and the critical \(H^{1/2}\) structure are
classical.  R0.73W may describe the display as a useful diagnostic synthesis,
not as a new critical theory.

## 5. Sign, convention, and erratum checks

1. Johnson, Eyink--Aluie, and R0.73W use
   \(\tau=\overline{u\otimes u}-\bar u\otimes\bar u\) and
   \(\Pi=-\tau:S\).  Positive \(\Pi\) is a forward/downscale sink of resolved
   energy.  Sources using the opposite stress convention require an explicit
   sign conversion.
2. Positive semidefiniteness of \(\tau_s\) does not fix the sign of its
   contraction with trace-free strain.
3. Johnson's 2020 PRL has a 2021 [Erratum](https://doi.org/10.1103/PhysRevLett.126.029901)
   concerning a sign/index in part of the later strain--rotation
   decomposition.  The Gaussian forced diffusion and exact stress equations
   (8)--(10) are unaffected.  The 2021 JFM version is preferred when quoting
   the full decomposition.
4. Hamba's Gaussian variance convention is twice the R0.73W heat parameter.
5. The public rank-three Fourier witness is exact finite algebra.  DNS papers
   supply physical context, not proof of its universal-sign conclusion.

## 6. Bounded negative findings

The search inspected the primary sources above and targeted combinations of
“Gaussian filter,” “heat equation/semigroup,” “subgrid stress,” “energy
flux,” “scale space,” \(L^{-1/2}\), and \(H^{1/2}\).  It did not locate a
source printing either of the following packages verbatim:

- the exact combined \((\partial_t-\nu\partial_s)\) local energy display
  together with its descending heat characteristic;
- the exact \(s^{-1/4}\) energy-class estimate or the exact
  \(s^{-1/2}\)-weighted production-to-Riesz display.

These are bounded negative findings only.  They do not prove novelty,
priority, non-existence, or first authorship.  The correct release labels are
“heat-coordinate reformulation,” “energy-class corollary,” and “critical
scale-weighted synthesis.”

## 7. Frozen attribution sentence

> The Gaussian covariance/stress identity is the heat-semigroup normalization
> of Johnson's exact Gaussian-filter formula (2020, 2021), equivalently the
> continuous-semigroup specialization of Germano's filtering identity and the
> standard carré-du-champ interpolation.  The local and integrated heat-plane
> balances are heat-coordinate reformulations of the classical coarse-grained
> Navier--Stokes energy balance.  The Duchon--Robert defect is the corresponding
> zero-filter-scale distributional object for weak solutions, not the
> finite-scale identity.

## 8. Machine-readable conclusion

```text
johnsonGaussianStressCollision=DIRECT_EXACT_AFTER_S_EQUALS_ELL2_OVER_2
germanoFilterComposition=VERIFIED_CLASSICAL
eyinkAluieLocalEnergyLaw=VERIFIED_CLASSICAL
centeredIncrementLineage=VERIFIED_CLASSICAL_CONTEXT
duchonRobertZeroScaleDefect=DISTINCT_FROM_FIXED_SCALE
heatPlaneCombinedDisplay=CLASSICAL_REFORMULATION_BOUNDED_NONDETECTION
energyClassSMinusQuarter=INTERNAL_COROLLARY_BOUNDED_NONDETECTION
criticalHalfScaleRiesz=INTERNAL_SYNTHESIS_BOUNDED_NONDETECTION
fujitaKatoCriticalStructure=VERIFIED_CLASSICAL
prl2020ErratumChecked=YES_CORE_STRESS_UNAFFECTED
noveltyOrPriorityClaim=FORBIDDEN
ordinaryTranslationPath=LOCAL_DIRECT_NO_DGX
dgxUsed=false
NOT CLAY
```
