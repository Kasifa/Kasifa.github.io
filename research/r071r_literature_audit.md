# R0.71R bounded primary-source audit

**Search date:** 2026-08-26  
**Question:** does an existing parabolic Carleson, local-energy,
unique-continuation, flux, or nodal-set theorem force every positive entry of a
localized NSE observable to carry a uniform amount of tent mass?

## 1. Claim filters

A theorem was relevant only if it controlled at least one of the following:

1. a lower mass in a parabolic cylinder caused by one event;
2. the cardinality or packing of temporal zeros of a forced Hilbert-valued
   parabolic observable;
3. overlap of forward windows associated with repeated zeros;
4. a tent/source budget paid by Leray energy and uniform across observables;
5. a signed NSE-specific flux packet that could survive before componentwise
   positive parts.

Spatial nodal measure, a cover of singular points, a regularity interval, or an
upper Carleson norm was not treated as an entry-count theorem without an
event-to-tent lower implication.

## 2. Wave one: NSE local-energy and Carleson sources

### Caffarelli--Kohn--Nirenberg (1982)

- Source: [DOI 10.1002/cpa.3160350604](https://doi.org/10.1002/cpa.3160350604).
- Suitable weak solutions satisfy the local energy inequality.
- The epsilon-regularity mechanism says that a scale-normalized local
  space--time quantity below a universal threshold implies regularity.
- The singular set has zero one-dimensional parabolic Hausdorff measure.

**Interface:** at a singular point the epsilon-smallness criterion cannot hold
on all sufficiently small cylinders; its contrapositive supplies a limsup, or
a sequence-of-scales, lower charge for the singular-set covering argument.

**Gap:** an R0.71P entry can occur on a completely classical interval and need
not be singular.  The theorem gives no implication from
\(C_{j,Q}(t_0)=0\) with positive right jet to a lower local-energy mass.
Parabolic Hausdorff measure zero also does not control the cardinality of a
smooth temporal event set.

### Lei--Ren (2024)

- Sources: [arXiv:2210.01783](https://arxiv.org/abs/2210.01783),
  [DOI 10.1016/j.aim.2024.109654](https://doi.org/10.1016/j.aim.2024.109654).
- The paper proves a logarithmic improvement of the CKN partial-regularity
  measure and quantitative regular epochs in terms of the local
  scale-invariant quantity built from \(|u|^3+|p|^{3/2}\).

**Interface:** this supplies an actual NSE quantitative parabolic-window
scale, not merely qualitative smoothness.

**Gap:** the theorem neither excludes nor controls repeated zeros of one
filtered observable inside a regular epoch.  It packages
singularity/regularity, not filtered-entry incidence, and gives no lower tent
mass per entry.

### Koch--Tataru (2001)

- Sources: [author PDF](https://math.berkeley.edu/~tataru/papers/nas.pdf),
  [DOI 10.1006/aima.2000.1937](https://doi.org/10.1006/aima.2000.1937).
- The \(BMO^{-1}\) norm is defined through the caloric extension by the
  parabolic square average

  \[
   \sup_{x,R}\left(
   |B_R|^{-1}
   \int_0^{R^2}\int_{B_R(x)}|e^{t\Delta}u_0|^2\,dy\,dt
   \right)^{1/2}.
  \]

- Small \(BMO^{-1}\) data give a unique global solution in the corresponding
  parabolic solution space; the bilinear Duhamel map is controlled from its
  source space to the solution space.

**Interface:** this is the closest checked theorem to a genuine parabolic
Carleson total budget.

**Gap:** it is an upper tent norm in a small-data well-posedness class.  It
does not say that a zero/entry of a localized filtered field consumes a fixed
fraction of that norm, and it does not pay the degree-zero component union.

### Dascaliuc--Grujić (2013)

- Sources: [arXiv:1107.0058](https://arxiv.org/abs/1107.0058),
  [DOI 10.1007/s00220-012-1595-8](https://doi.org/10.1007/s00220-012-1595-8).
- Under vorticity-direction coherence, Kraichnan-scale separation, and a
  modulation assumption, the paper proves positive ensemble-averaged
  enstrophy flux across an inertial range and scale-locality bounds.

**Interface:** among the checked NSE sources, this is closest to retaining a
signed physical-scale precursor before taking componentwise positive parts.

**Gap:** the paid quantity is a space--time cover average under additional
structural hypotheses.  A temporal point atom may be invisible to that
average.  No lower signed flux packet is assigned to every filtered entry.

## 3. Wave two: zero sets and unique continuation

### Angenent (1988)

- Sources: [DOI 10.1515/crll.1988.390.79](https://doi.org/10.1515/crll.1988.390.79),
  [hosted scan](https://math.jhu.edu/~js/Math745/angenent.par1.pdf).
- For a one-dimensional scalar homogeneous parabolic equation

  \[
   v_t=a(x,t)v_{xx}+b(x,t)v_x+c(x,t)v,
  \]

  under uniform parabolicity, coefficient regularity, the paper's boundary
  hypotheses, and positive time, the spatial zero number is finite and
  nonincreasing; it drops at multiple zeros.

**Interface:** this is the closest checked theorem to an actual cardinality
law.

**Gap:** it uses one-dimensional order, scalarity, and a closed homogeneous
equation.  The R0.71R observable is a three-dimensional Hilbert-valued field
with the nonzero forcing (2.3), so the Sturm mechanism does not apply.

### Lin (1991)

- Source: [DOI 10.1002/cpa.3160440303](https://doi.org/10.1002/cpa.3160440303).
- Lin develops quantitative analytic-geometric and frequency-function control
  for nodal sets of heat-equation solutions.

### Huang--Jiang (2024 preprint)

- Source: [arXiv:2406.05877](https://arxiv.org/abs/2406.05877).
- Huang--Jiang estimate fixed-time-slice nodal sets for parabolic equations
  with Lipschitz principal coefficients and exhibit higher-dimensional
  examples in which nodal-set measure is not monotone.

**Gap:** R0.71P asks for times at which the whole localized spatial field is
zero, not the size of \(\{x:C(x,t)=0\}\) at a fixed time.  Spatial nodal
measure and temporal vector-zero count are different objects.

### Escauriaza--Seregin--Šverák (2003)

- Source: [DOI 10.1007/s00205-003-0263-8](https://doi.org/10.1007/s00205-003-0263-8).
- Backward uniqueness is proved for a closed parabolic differential
  inequality in an exterior domain, with Gaussian growth control and full
  terminal-field vanishing.

**Gap:** \(C_{j,Q}=0\) only says that one localized filtered operator output is
zero.  The operator has a large kernel, and (2.2) contains the forcing
\(G_{j,Q}\).  The theorem supplies neither a zero spacing nor a repeated-entry
count.

## 4. Claim-to-source comparison

| Source | Parabolic total budget | Event lower charge | Temporal cardinality | Forced Hilbert observable | All-component union | Leray arbitrary data |
|---|---:|---:|---:|---:|---:|---:|
| CKN | yes, local energy | failure of epsilon gate at singular points | no | no | no | suitable solutions |
| Lei--Ren | yes, quantitative local energy | singular/regularity gate | no | no | no | suitable solutions |
| Koch--Tataru | yes, square-Carleson | no | no | no | no | small critical data |
| Dascaliuc--Grujić | signed cover-averaged flux | no per entry | no | no | ensemble average | conditional Leray |
| Angenent | not the NSE budget | multiple spatial zero drop | yes, 1D spatial | no forcing, scalar 1D | no | no |
| Lin / Huang--Jiang | spatial nodal measure | frequency/doubling based | no temporal count | scalar parabolic | no | no |
| Escauriaza et al. | not a packing budget | full-field terminal vanishing | identity only | closed inequality | no | criterion-level |

## 5. Bounded conclusion

The sources identify the standard architecture of a successful packing
argument: a total parabolic budget plus a lower amount of that budget forced by
each bad object.  For R0.71P only the first half is presently available.
R0.71R proves that the \(\rho=2\) energy-matched source-square total budget is
paid by Leray energy (and that \(\rho=2\) is the minimal paid exponent on the
normalized zero-mean torus).  Covariant NSE scaling gives the optimal
\(\rho=2\) certificate two powers of scale weight, while the explicit
high-frequency family verifies the same \(K^2\) pressure only for its initial
Taylor-jet surrogate.  The scale-covariant \(\rho=0\) alternative requires an
\(L^2\)-Lamb and palinstrophy budget.  The checked literature supplies neither

\[
 A_{\beta,+}\lesssim
 \kappa_j^{-2}\frac{\|C_\alpha(t_\beta+h_\beta)\|_2^2}
 {\sup_{I_\beta}Y}
\]

nor a uniform overlap bound for the forward windows, and it does not remove
this exact two-derivative mismatch.

No primary theorem found in the two bounded waves controls the full distinct
positive-entry measure from Leray data.  This is a bounded negative finding
only.  It is not a claim that no such theorem exists, and it is not a novelty
or priority claim for R0.71R.
