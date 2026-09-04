# R0.75Q bounded primary-source report

## Report frame

- Audience: analysts reviewing the one-harmonic physical-collar payment
- Date: 2026-09-04
- Question: does existing passive-scalar or heat-observability theory already
  prove the R0.75Q collar-localized cubic conversion, and what part of the
  low-entrance branch remains after Q?
- Scope: primary journal and arXiv records for modal shear diffusion,
  streamline-wise enhanced dissipation, exact shear-dispersion solutions, and
  heat observation from restricted sets
- Assumptions: Q concerns one real horizontal harmonic transported by a
  constant shear, independent of `x_1,x_3`, with an explicitly selected radial
  plateau shell
- Exclusions: an exhaustive priority search, multimode nonlinear dynamics,
  numerical turbulence, E.24, and every Navier--Stokes regularity conclusion

## Direct answer

The inspected literature gives strong mode-by-mode and streamline-wise decay
theory for passive scalars, including a 2026 hypocoercive result with a
space-time weight adapted to local shear strength. It also gives observability
results from thick or positive-measure sets. None of those inspected theorems
has the same output as Q: an exact lower bound for the spacetime `L^3` mass of
one known harmonic inside a shrinking spherical shell, followed by payment of
the shell's signed cutoff flux with the two-thirds power of that same mass.

Q uses no enhanced-dissipation or observability theorem. The proof is
elementary after the exact harmonic is fixed: every sufficiently long
`x_2`-interval captures a phase-uniform amount of `|cos|^3`; a rectangular
subcollar has an explicit `x_1`-fibre length; and ordinary heat decay supplies
the time integral. The result is consequently a rigorous benchmark for one
spatially spread harmonic, not a solution of the general low-entrance branch.

The bounded search found no matching theorem with all of the spherical-shell
geometry, signed derivative cutoff, shrinking `R` scale, `L^3` atom,
`k^(-2/3)` conversion, and Version-M ledger alignment. This is a search
boundary, not a novelty or priority claim.

## Primary evidence

### Streamline-wise enhanced dissipation

Siming He's 2026 preprint studies the passive-scalar equation for shear flows
with finitely many nondegenerate critical points. Its main theorem uses a
space-time hypocoercive weight and gives streamline-dependent `L^2` decay,
interpolating between critical-layer and monotone-region rates. This is the
closest inspected literature collision with the word “localized.” Its
localization follows the shear profile and controls a weighted `L^2` norm; it
does not estimate Q's signed spherical-collar flux or its local `L^3` payment.

- Siming He, “Localized Enhanced Dissipation: A Hypocoercivity Approach,”
  arXiv:2603.14657v1, submitted 2026-03-15,
  https://arxiv.org/abs/2603.14657.

Gardner, Liss, and Mattingly use stochastic trajectories and Girsanov control
to obtain enhanced-dissipation estimates whose rates can depend on the local
shear geometry along streamlines. Again, the observable, geometry, and norm
differ from Q.

- Victor Gardner, Kyle L. Liss, and Jonathan C. Mattingly, “A pathwise
  approach to the enhanced dissipation of passive scalars advected by shear
  flows,” arXiv:2410.05657v1, submitted 2024-10-08,
  https://arxiv.org/abs/2410.05657.

### Mode-by-mode shear diffusion

Siming He's earlier work reduces the shear problem to nonzero horizontal
Fourier modes and derives enhanced-dissipation estimates before summing those
modes. This supports treating a one-mode calculation as a controlled
benchmark, but Q uses only the exact ordinary heat factor `e^(-k^2t)` after
constant transport is removed.

- Siming He, “Enhanced dissipation, hypoellipticity for passive scalar
  equations with fractional dissipation,” *Journal of Functional Analysis*
  282 (2022), 109319, arXiv:2103.07906,
  https://arxiv.org/abs/2103.07906.

Jimenez-Urias and Haine derive exact Mathieu-function representations and
wavenumber-dependent regimes for dispersion by a periodic shear. This
confirms the value of exact modal benchmarks, but its cross-channel averages
and closure operators are not Q's shrinking spherical collar.

- Miguel A. Jimenez-Urias and Thomas W. N. Haine, “An exact solution to
  dispersion of a passive scalar by a periodic shear flow,” arXiv:2101.05406,
  submitted 2021-01-14, https://arxiv.org/abs/2101.05406.

### Observation on restricted sets

Wang, Wang, Zhang, and Zhang characterize observable sets for the heat
equation in Euclidean space through thickness and establish related spectral
and interpolation inequalities. A single shrinking shell is not a uniform
thick-set hypothesis at the ambient scale. Q avoids an observability cost by
using the explicit periodic harmonic and integrating `|cos|^3` directly.

- Gengsheng Wang, Ming Wang, Can Zhang, and Yubiao Zhang, “Observable set,
  observability, interpolation inequality and spectral inequality for the
  heat equation in `R^n`,” *Journal de Mathematiques Pures et Appliquees* 126
  (2019), 144--194, DOI 10.1016/j.matpur.2019.04.009,
  https://doi.org/10.1016/j.matpur.2019.04.009.

## Claim-to-source gap matrix

| claim family | evidence | confidence | mismatch with Q | treatment |
|---|---|---:|---|---|
| shear diffusion can be analyzed one horizontal mode at a time | He 2022 | high | semigroup decay is not a signed collar payment | context only |
| enhanced dissipation can be localized along streamlines | Gardner--Liss--Mattingly 2024; He 2026 | high | weighted or pathwise `L^2` outputs, not spherical-shell `L^3` mass | promising for later nonconstant-shear work |
| periodic shear admits exact modal solutions | Jimenez-Urias--Haine 2021 | high | different shear, averages, and closure observable | context only |
| global heat observation requires quantitative geometric hypotheses | Wang--Wang--Zhang--Zhang 2019 | high | the shrinking shell is not inserted into those constants | no observability theorem imported |
| Q.18 is phase-uniform | direct period decomposition | exact local proof | none for one harmonic | proved locally |
| Q.19 follows from the rectangular subcollar | direct fibre geometry | exact local proof | depends on the selected radial plateau | proved locally |
| Q.26 holds for any Fourier projection of a larger velocity field | no supporting source or local domination | none | pointwise domination fails in general | explicitly excluded |
| Q closes arbitrary low-entrance packets | no supporting source or local proof | none | interference, vertical structure, and packet sums remain | explicitly open |

## Search record and stopping rule

The first pass combined `passive scalar`, `shear`, `single Fourier mode`,
`exact solution`, `local observation`, and `shrinking set`. A targeted second
pass checked the 2026 localized-hypocoercivity paper, the pathwise shear
paper, the earlier mode-by-mode result, the exact periodic-shear solution,
and the thick-set heat-observability theorem. The sources resolved the main
collision: “localized enhanced dissipation” means streamline-adapted decay,
not the project-specific spherical-collar cubic payment.

The search stopped because every consequential source class now has a
primary representative and a precise mismatch. A broader generic search was
unlikely to validate the missing multimode signed-collar theorem. No citation
graph or subscription-only exhaustive priority review was attempted.

## Frozen conclusion

**Established locally:** one spatially spread real harmonic has enough
phase-uniform mass in the explicit physical collar to pay its signed cutoff
flux with a favorable `k^(-2/3)` factor, under Q's stated geometry and time
conditions.

**Literature-supported context:** modal and streamline-wise decay theory is
well developed, including genuinely localized `L^2` estimates, but its output
cannot be substituted for Q.3--Q.4 without a new proof.

**Open:** two or more modes, destructive interference in the local cubic
mass, vertical structure, general low-entrance packets, nonconstant shear,
arbitrary-field E.24, complete-clock extraction, fixed deletion,
suitable-weak transfer, regularity, and singularity. **NOT CLAY.**
