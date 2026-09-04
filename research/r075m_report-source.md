# R0.75M primary-source boundary -- dyadic shear packets and modal aggregation

**Audience:** analysts reviewing the R0.75M dyadic-packet signed-flux
estimate.  
**Date:** 2026-09-03.  
**Scope:** mode-by-mode shear diffusion, packet summation, cutoff Fourier
regularity, and local/full-torus payment boundaries.  
**Exclusion:** no E.24, complete-clock, regularity, novelty, or priority
claim.

## Direct answer

R0.75M is a local derivation using the exact constant-shear semigroup,
Schur's test, Parseval, Holder, and a Fourier-space Sobolev estimate.  It
proves that arbitrary finite interference inside one dyadic horizontal
packet retains the `K^(-2/3)` gain found for one harmonic in R0.75L,
provided the cutoff derivative is measured in its Wiener norm.

The primary literature supports horizontal mode decomposition and
mode-dependent shear decay as serious tools.  It does not identify the
R0.75M Wiener row with an affordable frozen spherical-collar atom, perform
the inter-packet summation, or prove E.24.

## Evidence used and boundary

### Mode-by-mode and summed shear estimates

Siming He proves mode-by-mode estimates for passive shear equations with
fractional dissipation and then sums horizontal modes under the paper's
hypotheses.  This supports the overall dyadic architecture, but R0.75M's
specific Schur/Wiener kernel and Version-M boundary are not imported from
that paper.

### Pathwise control under nonconstant shears

Gardner, Liss, and Mattingly use stochastic trajectories and quantitative
control to recover enhanced-dissipation behavior for several shear
classes.  Their work remains relevant to the nonconstant-shear and low
difference-frequency sectors left open here.  It does not pay the frozen
cutoff Wiener norm or local cubic atom.

### Exact modal shear dispersion

Jimenez-Urias and Haine construct exact modal representations for periodic
shear dispersion and identify wavenumber-dependent regimes.  This supports
the use of exact modal benchmarks, while their Mathieu setting and averaged
closure observable differ from the R0.75M local signed flux.

## Claim-to-source ledger

| claim checked | primary source | date / identifier | URL | access and boundary |
|---|---|---|---|---|
| Passive shear enhanced-dissipation analysis can be organized mode by mode and then summed under stated hypotheses | Siming He, *Enhanced dissipation, hypoellipticity for passive scalar equations with fractional dissipation* | submitted 2021-03-14, arXiv:2103.07906 | https://arxiv.org/abs/2103.07906 | Abstract and k-by-k proof reduction inspected 2026-09-03; no M.2 or Version-M conclusion |
| Pathwise quantitative control yields shear-diffusion decay information for specified nonconstant shear classes | Victor Gardner, Kyle L. Liss, and Jonathan C. Mattingly, *A pathwise approach to the enhanced dissipation of passive scalars advected by shear flows* | submitted 2024-10-08, arXiv:2410.05657 | https://arxiv.org/abs/2410.05657 | Main-result and control-reduction sections inspected 2026-09-03; different target and payment |
| Periodic shear dispersion admits exact mode-dependent representations | Miguel A. Jimenez-Urias and Thomas W. N. Haine, *An exact solution to dispersion of a passive scalar by a periodic shear flow* | submitted 2021-01-14, arXiv:2101.05406 | https://arxiv.org/abs/2101.05406 | Modal and closure sections inspected 2026-09-03; not a local collar theorem |

## Gap matrix

| question | evidence | R0.75M conclusion |
|---|---|---|
| Does arbitrary finite interference inside one dyadic packet destroy the `K^(-2/3)` factor? | Local proof M.7--M.16 | No, if the cutoff derivative Wiener norm is retained |
| Is the packet mode count paid separately? | Schur estimate M.9--M.11 | No explicit count appears |
| What replaces that count? | M.1 and M.17 | The cutoff derivative Wiener norm |
| Is its frozen `R,L` size affordable? | Main theorem boundary | Not proved |
| Are inter-packet, collar-localized, and nonconstant-shear estimates available from the inspected sources? | Bounded primary-source search | No matching theorem found |
| Is E.24 closed? | M.19 boundary | No |

## Search record and stopping rule

The audit reused the primary mode-by-mode, pathwise, and exact-solution
sources verified for R0.75L.  A focused second pass checked whether their
outputs include a local signed collar flux, cutoff Wiener payment, or
Version-M cubic localization.  No matching theorem was found.  The search
stopped because the packet estimate is proved locally and additional
generic enhanced-dissipation references would not determine the frozen
cutoff or payment scaling.

## Frozen conclusion

**Established locally:** one constant-shear dyadic packet has a
mode-count-free `K^(-2/3)` signed-flux/cubic-mass gain when the cutoff
derivative Wiener norm is retained.

**New exact gate:** quantify that Wiener norm in the frozen spherical
geometry, localize the cubic mass, and sum packets without losing the
required `R` exponent.

**Open:** nonconstant shear, low differences, E.24, complete clock, fixed
deletion, suitable-weak transfer, regularity, and singularity.
**NOT CLAY.**
