# R0.75R bounded primary-source report

## Report frame

- Audience: analysts reviewing the outer-cap concentration obstruction
- Date: 2026-09-04
- Question: do standard uncertainty, observability, or heat-kernel results
  contradict the concentrated high-band packet in R0.75R, and which parts of
  R use imported theory?
- Scope: primary records for torus Logvinenko--Sereda inequalities, heat
  observability from restricted sets, and Gaussian off-diagonal heat bounds
- Exclusions: an exhaustive priority search, a claim that no related
  counterexample exists, nonlinear turbulence, E.24, and every
  Navier--Stokes regularity conclusion

## Direct answer

The inspected spectral and observability literature does not contradict R.
Quantitative observation of band-limited functions requires a geometric
hypothesis on the observation set and carries constants depending on the
set's scale, density, and spectral complexity.  R deliberately observes only
the shrinking plateau shell while placing a coherent high-band packet in a
separated outer cap.  The resulting loss is computed directly from an
explicit normalized Dirichlet kernel.

The only general analytic ingredient used in R is short-time Gaussian
off-diagonal decay for the ordinary heat semigroup.  On the circle, that
estimate also follows immediately from the periodized Gaussian kernel, so no
external theorem is needed for the proof.  The cited heat-kernel literature
records the broader Davies--Gaffney framework and supports the terminology.

The bounded search did not find a theorem with R's exact combination of a
radial derivative cross-section, a separated shrinking plateau shell, an
explicit high-band Dirichlet packet, a local cubic atom, and the frozen
two-thirds normalization.  This is a search boundary, not a novelty or
priority claim.

## Primary evidence

### Spectral inequalities on the torus

Egidi and Veselic prove scale-free unique-continuation and
Logvinenko--Sereda estimates on tori for functions whose Fourier support lies
in spectral parallelepipeds.  Their constants depend on quantitative density
and scale data for the observation set, as well as the relevant spectral
description.  This is compatible with R: the plateau projection is separated
from the packet center and is not used with a uniform thick-set hypothesis at
the packet scale.

- Michela Egidi and Ivan Veselic, “Scale-free unique continuation estimates
  and Logvinenko--Sereda Theorems on the torus,” arXiv:1609.07020,
  https://arxiv.org/abs/1609.07020.

### Heat observability and thickness

Wang, Wang, Zhang, and Zhang characterize observable sets for the heat
equation on Euclidean space by a quantitative thickness condition and relate
observability, interpolation, and spectral inequalities.  They also study
weaker observations on balls.  Their results explain why the geometry and
cost of a restricted observation cannot be erased.  R does not invoke their
theorem and does not infer a torus statement from the Euclidean one.

- Gengsheng Wang, Ming Wang, Can Zhang, and Yubiao Zhang, “Observable set,
  observability, interpolation inequality and spectral inequality for the
  heat equation in `R^n`,” *Journal de Mathematiques Pures et Appliquees* 126
  (2019), 144--194, arXiv:1711.04279,
  https://arxiv.org/abs/1711.04279,
  https://doi.org/10.1016/j.matpur.2019.04.009.

### Gaussian off-diagonal heat decay

Coulhon and Sikora formulate Davies--Gaffney `L^2` estimates and show how
on-diagonal bounds yield Gaussian off-diagonal kernel bounds for broad
analytic families.  The circle Laplacian is a standard, simpler instance.
R uses only the elementary periodized-Gaussian case over times
`t<=K^(-2)` and separations comparable to `R`.

- Thierry Coulhon and Adam Sikora, “Gaussian heat kernel upper bounds via
  Phragmen--Lindelof theorem,” *Proceedings of the London Mathematical
  Society* 96 (2008), 507--544, arXiv:math/0609429,
  https://arxiv.org/abs/math/0609429,
  https://doi.org/10.1112/plms/pdm050.

## Claim-to-source gap matrix

| claim family | evidence | confidence | mismatch with R | treatment |
|---|---|---:|---|---|
| band-limited functions obey quantitative observation on suitable torus sets | Egidi--Veselic 2016 | high | constants require quantitative observation geometry; R's atom is a separated shrinking plateau | context only |
| heat observability on `R^n` is tied to thickness | Wang--Wang--Zhang--Zhang 2019 | high | different domain and norm; R computes one explicit torus family | context only |
| separated heat propagation is Gaussian-small on short times | Coulhon--Sikora 2008 | high | far broader framework than needed | R proves the circle case from the explicit kernel |
| the radial average is `-2pi y vartheta` | direct polar-coordinate calculation | exact local proof | none | proved locally |
| the packet lies in `[K,2K]` | exact finite Fourier support | exact local proof | none | proved locally |
| the plateau mass has the power `(nR)^(-6m)` | pointwise Dirichlet tail plus heat kernel | exact local proof | depends on the selected packet and shell | proved locally |
| every multimode payment must fail | no source or local proof | none | full-support and signed alternatives remain | explicitly excluded |
| R disproves E.24 | no source or local domination | none | Version-M sees more than the plateau atom | explicitly excluded |

## Search record and stopping rule

The first pass combined `torus`, `spectral inequality`,
`Logvinenko--Sereda`, `heat observability`, `thick set`, and
`high-frequency concentration`.  A second pass checked primary records for
Davies--Gaffney and pointwise Gaussian heat-kernel bounds.  The sources
resolved the relevant collision: quantitative uncertainty principles do not
give a geometry-free constant for the shrinking, separated observation used
in R.

The search stopped after primary representatives covered the three imported
concepts: torus spectral observation, restricted-set heat observation, and
off-diagonal heat propagation.  The central construction and all frozen
exponents are local calculations.  No citation graph or subscription-only
exhaustive priority review was attempted.

## Frozen conclusion

**Established locally:** an explicit real high-band packet remains in the
positive outer cap for one diffusive time, creates a positive signed flux,
and leaves only a quantified algebraic heat tail on the plateau.  Its
normalized flux-to-plateau-mass quotient diverges at an exact positive rate.

**Literature-supported context:** spectral observation and heat
observability require quantitative geometry, while ordinary heat propagation
across a fixed multiple of `R` is exponentially small on the `K^(-2)` time
scale used here.

**Open:** full-support payment, Version-M aggregation, general signed
multimode cancellation, E.24, complete-clock extraction, fixed deletion,
suitable-weak transfer, regularity, and singularity.  **NOT CLAY.**
