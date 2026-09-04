# R0.75L primary-source boundary -- modal shear diffusion and signed local flux

**Audience:** analysts reviewing the R0.75L single-harmonic diffusive
signed-flux gain.  
**Date:** 2026-09-03.  
**Scope:** horizontal Fourier modes of passive shear equations, ordinary
heat decay, enhanced dissipation, and exact shear-dispersion solutions.  
**Exclusion:** no E.24, complete-clock, regularity, novelty, or priority
claim.

## Direct answer

R0.75L proves its `k^(-2/3)` factor by an elementary exact solution of the
constant-shear passive equation.  The literature confirms that
mode-by-mode analysis and additional shear-induced decay are standard and
substantive, but none of the inspected primary sources proves the local
signed spherical-collar estimate E.24 or pays the frozen Version-M ledger.

The theorem should therefore be read as a controlled benchmark.  It shows
that, after the horizontal diagonal cancels, ordinary heat decay already
gives a favorable high-frequency factor for one real harmonic.  Extending
that factor to many interacting differences, nonconstant shear, and a
collar-localized cubic atom remains a separate theorem.

## Evidence used and boundary

### Mode-by-mode enhanced dissipation

Siming He studies passive scalars under shear with fractional dissipation,
derives estimates one horizontal Fourier mode at a time, and then sums the
modes under the paper's hypotheses.  This supports the high/low horizontal
frequency architecture proposed after L.17.  R0.75L does not import those
resolvent estimates, and the paper does not supply the local signed-flux
payment required here.

### Pathwise shear estimates

Gardner, Liss, and Mattingly derive enhanced-dissipation information from
the stochastic trajectories associated with shear drift diffusion and
obtain local-in-space streamline estimates under their assumptions.  This
supports reserving pathwise information for the low difference-frequency
sector.  Their result is not a Version-M collar estimate.

### Exact shear-dispersion solutions

Jimenez-Urias and Haine construct exact modal solutions for passive scalar
dispersion by a periodic shear using Mathieu functions and describe
different wavenumber/Peclet regimes.  This confirms that exact Fourier
benchmarks can distinguish propagation and decay regimes.  Their geometry,
closure observable, and scaling differ from R0.75L.

## Claim-to-source ledger

| claim checked | primary source | date / identifier | URL | access and boundary |
|---|---|---|---|---|
| Passive shear equations admit mode-by-mode enhanced-dissipation estimates that are subsequently summed under stated hypotheses | Siming He, *Enhanced dissipation, hypoellipticity for passive scalar equations with fractional dissipation* | submitted 2021-03-14, arXiv:2103.07906 | https://arxiv.org/abs/2103.07906 | Abstract, theorem-proof setup, and k-by-k reduction inspected 2026-09-03; no local signed collar payment |
| Pathwise stochastic control yields enhanced-dissipation and local streamline information for specified shear classes | Victor Gardner, Kyle L. Liss, and Jonathan C. Mattingly, *A pathwise approach to the enhanced dissipation of passive scalars advected by shear flows* | submitted 2024-10-08, arXiv:2410.05657 | https://arxiv.org/abs/2410.05657 | Abstract, main-result, and control-reduction sections inspected 2026-09-03; different target and geometry |
| Periodic shear dispersion has exact Fourier/Mathieu representations with wavenumber-dependent regimes | Miguel A. Jimenez-Urias and Thomas W. N. Haine, *An exact solution to dispersion of a passive scalar by a periodic shear flow* | submitted 2021-01-14, arXiv:2101.05406 | https://arxiv.org/abs/2101.05406 | Exact modal setup and closure sections inspected 2026-09-03; not an E.24 or Version-M theorem |

## Gap matrix

| question | evidence | R0.75L conclusion |
|---|---|---|
| Does one real constant-shear harmonic have a favorable diffusive flux/payment factor? | Exact local proof L.4--L.13 | Yes, `k^(-2/3)` for `k^2T>=1` |
| Is the factor an imported enhanced-dissipation theorem? | Exact local proof and source comparison | No; it is ordinary horizontal heat decay after diagonal cancellation |
| Can one sum arbitrary real cross modes with the same local cubic payment? | Main theorem boundary; literature mismatch | Not proved |
| Does a source localize the full-torus cubic mass to the frozen spherical collar with no leakage? | Bounded primary-source search | No matching theorem found |
| Is E.24 closed? | Frozen reduction and L.15 boundary | No |

## Search record and stopping rule

The bounded search used the mechanism terms `passive scalar`, `shear`,
`enhanced dissipation`, `horizontal Fourier mode`, `exact solution`, and
`pathwise`.  It prioritized arXiv primary papers, inspected the relevant
mode-by-mode, pathwise, and exact-solution sections, and stopped when the
three neighboring mechanism classes and their mismatch with E.24 were
established.  Further generic enhanced-dissipation references were unlikely
to prove the missing collar-localized Version-M conversion.

## Frozen conclusion

**Established locally:** a one-real-harmonic physical signed flux gains
`k^(-2/3)` relative to the two-thirds power of its full-torus spacetime
cubic mass once `k^2T>=1`.

**Supported context:** horizontal mode decompositions, resolvent estimates,
pathwise control, and exact shear-dispersion formulas are legitimate next
mechanisms, but their hypotheses and outputs must be translated rather
than cited as E.24.

**Open:** multimode summation, collar localization, background payment,
nonconstant shear, the low difference-frequency sector, E.24, complete
clock, fixed deletion, suitable-weak transfer, regularity, and singularity.
**NOT CLAY.**
