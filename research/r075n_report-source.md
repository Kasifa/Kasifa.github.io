# R0.75N primary-source boundary -- radial projection and Fourier decay

**Audience:** analysts reviewing the averaged radial-collar Wiener row.
**Date:** 2026-09-03.
**Scope:** Fourier projection/slicing, radial averaging, curvature-driven
Fourier decay, and the discrete coefficient row in R0.75N.
**Exclusion:** no dynamical flux, local Version-M payment, E.24,
regularity, novelty, or priority claim.

## Direct answer

R0.75N is a local proof. It combines the exact rescaling of a smooth thin
radial shell, elementary cross-sectional area bounds, Fubini, and a
low/high split of sampled one-dimensional Fourier transforms. The
coefficientwise `x_3` supremum is taken before summation, so ordinary
pointwise slice statements are not silently promoted to the required
Wiener row.

The primary literature confirms that integration along transverse
directions is naturally represented by Fourier projection/slice formulas,
that radial averaging is governed by Abel-type transforms, and that
curvature controls Fourier decay of convex boundaries. None of the
inspected sources states the project-specific estimate

`sum_l ||i l Xi_l||_(L^infinity_(x_3)) <= C L`

for a smooth `O(R)` spherical collar with radius `(32/63)LR`, nor its
fully averaged `CL^2R` companion. Those bounds are proved directly in the
frozen main note.

## Evidence used and boundary

### Fourier projection and slicing

Garces, Rhodes, and Peña formulate the projection-slice theorem in two
and three dimensions. This supports the identification of a Fourier
coefficient after transverse physical integration with a slice of the
higher-dimensional transform. Their paper is a notation and imaging
result; it does not estimate an absolute Fourier-coefficient sum or the
thin-collar scaling used here.

### Radial dimension reduction

Rux, Quellmalz, and Steidl study slicing of radial functions through
averaging, rotation, one-dimensional Fourier transforms, and Abel-type
relations. This is close to the radial dimension-reduction architecture.
Their theorem does not include the R0.75N discrete sampling split,
coefficientwise `x_3` supremum, or frozen `R,L` normalization.

### Curved-boundary Fourier decay

Herz's classical paper studies Fourier transforms associated with convex
sets and is a primary reference for curvature-dependent decay. R0.75N
does not import a stationary-phase or sharp convex-body asymptotic from
that work: the smooth shell estimate follows from two integrations by
parts and physical support measure. In particular, spherical tangencies
are paid by the exact cross-sectional area bound rather than a pointwise
chord estimate.

## Claim-to-source ledger

| claim checked | primary source | date / identifier | URL | access and boundary |
|---|---|---|---|---|
| Projection along a physical direction has a Fourier-slice representation | Daissy H. Garces, William T. Rhodes, and Nestor M. Peña, *Projection-slice theorem: a compact notation* | JOSA A 28 (2011), 766--769 | https://doi.org/10.1364/JOSAA.28.000766 | Abstract and article metadata inspected 2026-09-03; no Wiener or collar estimate |
| Radial dimension reduction can be expressed using averaging, Abel-type relations, and one-dimensional Fourier transforms | Nicolaj Rux, Michael Quellmalz, and Gabriele Steidl, *Slicing of radial functions: a dimension walk in the Fourier space* | 2025, DOI 10.1007/s43670-025-00100-9 | https://doi.org/10.1007/s43670-025-00100-9 | Main setup, Radon-transform remark, and Fourier formulas inspected 2026-09-03; different estimate and normalization |
| Curvature of convex boundaries is a source of Fourier-transform decay | Carl S. Herz, *Fourier Transforms Related to Convex Sets* | Ann. of Math. 75 (1962), 81--92, DOI 10.2307/1970421 | https://doi.org/10.2307/1970421 | Bibliographic record and scope inspected 2026-09-03; no smoothed thin-shell discrete Wiener row |

## Gap matrix

| question | inspected evidence | R0.75N conclusion |
|---|---|---|
| Is transverse averaging compatible with Fourier analysis? | Projection-slice and radial-slicing sources | Yes, as neighboring architecture |
| Does an inspected theorem give the coefficientwise-supremum Wiener row? | Bounded search | No matching statement found |
| Is sharp stationary phase required for N.2? | Local proof N.6--N.13 | No; two integrations by parts and support area suffice |
| Are spherical tangencies omitted? | Exact slice-area split N.12 | No; the tangency disk is bounded by `4 pi a delta` |
| Does N.2 yield a vertically diffusing or nonconstant-shear flux theorem? | Main claim boundary | No |
| Does any inspected source close E.24? | Bounded search | No matching theorem found |

## Search record and stopping rule

The search combined terms for thin radial annuli, convex-body Fourier
decay, projection-slice formulas, radial slicing, sampled Fourier
coefficients, and Wiener norms. It was stopped after the directly relevant
projection/radial/curvature mechanism classes were represented and no
source contained the frozen coefficientwise-supremum row. More generic
tomography, oscillatory-integral, or Wiener-algebra references would not
determine the project-specific `R,L` scaling, which is already proved by
the local support calculation.

## Frozen conclusion

**Established locally:** the canonical radial outer-collar representative
has `x_1`-averaged Wiener row `O(L)` and fully averaged row `O(L^2R)`.

**Literature boundary:** projection, radial slicing, and curvature decay
are established mechanism classes; no inspected primary source supplies
the exact frozen estimate.

**Open:** vertical diffusion, nonconstant shear, local cubic payment,
inter-packet and low-difference control, E.24, complete clock, fixed
deletion, suitable-weak transfer, regularity, and singularity.
**NOT CLAY.**
