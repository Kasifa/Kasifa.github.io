# R0.75P bounded primary-source report

## Report frame

- Audience: analysts reviewing the buffered-collar entrance-concentration
  argument
- Date: 2026-09-03
- Question: is the R0.75P local-energy-to-collar-cubic mechanism already a
  standard heat-observability theorem, and does the literature supply the
  missing low-concentration branch?
- Scope: primary articles and open preprint records for heat observability,
  spectral inequalities, and passive-scalar evolution in shear flows;
  bounded searches for the project-specific moving-cutoff and
  entrance-concentration estimate
- Exclusions: exhaustive novelty review, turbulence numerics, nonlinear
  stability thresholds, and any Navier--Stokes regularity conclusion
- Local assumption: P is a finite constant-shear, single-packet statement
  with a total upper-frequency cap and a separate Version-M
  ledger-alignment hypothesis

## Direct answer

Heat observability from positive-measure or thick sets is a developed
theory.  Those theorems recover a global or terminal norm from observations
on a prescribed set, with constants that depend on time, geometry, and
spectral information.  R0.75P does not import such a theorem.  It assumes an
entrance fraction `E_in >= mu E_0`, differentiates a cutoff transported by
the constant shear, and retains half of that fraction for the explicit
forward time `c_0 mu K^(-2)`.  Holder's inequality and the exact radial
fibre length then produce the `mu^(5/2)` local cubic lower bound.

The inspected passive-scalar literature confirms that transverse diffusion
and nonconstant parallel shears lead to substantial semigroup and
hypocoercive effects.  It does not, on the inspected records, supply the
project-specific low-entrance-concentration estimate needed after P.  In
particular, a global heat-observability result cannot be inserted without
tracking its cost at the shrinking `R` geometry and the `K^(-2)` time scale.

The bounded search did not locate the exact combination of a moving
constant-shear cutoff, a spherical `x_1`-fibre lower bound, the power
`mu^(5/2)`, the frozen threshold
`sigma < 8558/178605`, and Version-M ledger inclusion.  This is only a
search boundary.  It is not evidence of novelty or priority.

## Primary evidence

### Observations from measurable subsets

Apraiz, Escauriaza, Wang, and Zhang prove heat-equation observability from
positive-measure subsets of space-time on bounded domains, together with a
spectral inequality under their geometric hypotheses.  This is relevant to
the general question of recovering heat energy from a restricted region.
It is not the one-sided forward persistence argument in P, and it does not
provide the frozen `mu,R,K` powers used there.

- Jone Apraiz, Luis Escauriaza, Gengsheng Wang, and Can Zhang,
  “Observability inequalities and measurable sets,” *Journal of the
  European Mathematical Society* 16 (2014), 2433--2475, DOI
  [10.4171/JEMS/490](https://doi.org/10.4171/JEMS/490).
- Open preprint record:
  [arXiv:1202.4876](https://arxiv.org/abs/1202.4876).

### Observable sets in the whole space

Wang, Wang, Zhang, and Zhang characterize observable sets for the heat
equation in Euclidean space through thickness and relate observability,
interpolation, and spectral inequalities.  A single shrinking collar or
entrance disk is not automatically a uniformly thick observation set at
the torus scale.  Their result therefore does not justify replacing P.1 by
an unconditional entrance lower bound.

- Gengsheng Wang, Ming Wang, Can Zhang, and Yubiao Zhang, “Observable set,
  observability, interpolation inequality and spectral inequality for the
  heat equation in `R^n`,” *Journal de Mathematiques Pures et Appliquees*
  126 (2019), 144--194, DOI
  [10.1016/j.matpur.2019.04.009](https://doi.org/10.1016/j.matpur.2019.04.009).
- Open preprint record:
  [arXiv:1711.04279](https://arxiv.org/abs/1711.04279).

### Dependence of heat-observability cost on geometry

Ervedoza and Zuazua derive observability-cost estimates whose dependence on
the geometry of the domain and observation region is explicit, and prove
sharpness in specified settings.  This reinforces the need to audit any
attempt to use observability on a collar whose width and time window shrink
with `R`.  R0.75P deliberately avoids that cost by retaining an assumed
entrance fraction through a direct local-energy inequality.

- Sylvain Ervedoza and Enrique Zuazua, “Sharp observability estimates for
  heat equations,” *Archive for Rational Mechanics and Analysis* 202
  (2011), 975--1017, DOI
  [10.1007/s00205-011-0445-8](https://doi.org/10.1007/s00205-011-0445-8).

### Higher-dimensional parallel shear

Coti Zelati and Gallay treat passive-scalar evolution in higher-dimensional
parallel shear flows and obtain decay estimates in enhanced-dissipation and
Taylor-dispersion regimes.  Their setting confirms that transverse
diffusion is not a removable detail.  Their public theorem description is
about decay across diffusivity and wave-number regimes, not the signed
collar flux or local entrance-fraction dichotomy required here.

- Michele Coti Zelati and Thierry Gallay, “Enhanced dissipation and Taylor
  dispersion in higher-dimensional parallel shear flows,” *Journal of the
  London Mathematical Society* 108 (2023), 1358--1392, DOI
  [10.1112/jlms.12782](https://doi.org/10.1112/jlms.12782).
- Open preprint record:
  [arXiv:2108.11192](https://arxiv.org/abs/2108.11192).

## Claim-to-source gap matrix

| claim family | evidence | confidence | gap | project treatment |
|---|---|---:|---|---|
| heat energy can be observed from suitable restricted sets | Apraiz--Escauriaza--Wang--Zhang 2014; Wang--Wang--Zhang--Zhang 2019 | high | constants and admissible sets differ from the shrinking collar | contextual only |
| observability cost depends materially on geometry and time | Ervedoza--Zuazua 2011 | high | no frozen `R,K,mu` insertion has been proved | no observability theorem imported |
| the transported-cutoff identity P.16 is valid | direct periodic integration by parts | high | constant shear is essential to the exact transport cancellation | proved locally |
| entrance persistence lasts `c_0 mu K^(-2)` | P.17--P.20 | local proof | requires the total-frequency cap and P.1 | proved conditionally |
| radial fibres and Holder give `mu^(5/2)` | P.10 and P.21--P.24 | local proof | requires the canonical plateau and space-time alignment | proved conditionally |
| every packet satisfies `mu >= c_mu R^sigma` below the frozen threshold | no source or local proof | none | spatially spread data can have much smaller entrance fraction | explicitly open |
| P.31 embeds every constant-shear packet or packet projection into the frozen inversion-paired family | unsupported | none | ledger inclusion requires the actual-component realization and is weaker than dynamical-family realization | explicitly not claimed |
| the low-concentration complement follows from standard enhanced dissipation | inspected shear literature | none | the target is a localized signed kernel with cancellation | explicitly open |

## Searches and stopping rule

The first pass checked journal and arXiv records for heat observability from
measurable or thick sets, sharp dependence of observability cost, and
parallel-shear advection--diffusion.  A second pass combined terms for
moving observations, transported cutoffs, local heat energy, shrinking
collars, band-limited entrance concentration, and signed shear flux.  The
results converged on the four mechanism families above and did not reveal a
matching project-specific theorem.

The search stopped because the immediate mathematical boundary is now
determinate.  P's high-entrance branch stands or falls on its local proof,
not on a literature black box.  The next branch requires a new localized
signed-kernel or near/far argument; further generic observability citations
would not determine its frozen exponent ledger.

## Limitations and use boundary

- Public article metadata, abstracts, accessible full text, and arXiv
  records were inspected; no exhaustive citation graph or subscription-only
  database review was attempted.
- Absence of an exact search match does not prove that no equivalent result
  exists.
- The literature sources do not validate P.1, P.5, the Version-M alignment,
  actual-component realization, or the arithmetic of P.29--P.31; those
  require local proof and independent audit.
- P remains constant-shear, single-packet, total-frequency capped, and
  conditional on entrance concentration and ledger alignment.
- No source or local result here proves E.24, complete-clock extraction,
  fixed deletion, suitable-weak transfer, regularity, or singularity.
  **NOT CLAY.**
