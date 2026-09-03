# R0.75F primary-source boundary -- phase identities versus genuine shear coercivity

**Audience:** analysts reviewing the R0.75F route-pruning result.

**Search date:** 2026-09-03.

## Scope and direct answer

This bounded primary-source screen asks what the shear-flow literature adds
beyond the exact modal-product identity in R0.75F. The decisive distinction
is between an algebraic substitution and an estimate with genuinely new
information.

The closest primary literature supports three neighboring facts:

1. after streamwise Fourier transform, each shear mode evolves separately,
   but enhanced decay for nonzero modes is obtained through resolvent or
   hypocoercive information rather than the energy identity alone;
2. pathwise shear estimates use stochastic trajectories and local shear
   structure, thereby adding residence-time/mixing information;
3. physical localization of drift diffusion retains a boundary or cutoff
   flux whose control depends on the drift and geometry.

No searched source supplies the frozen R0.75F statement for the exact
three-dimensional spherical-collar Toeplitz form, nor a Version-M
payment-sensitive estimate closing E.24. This is a finite non-hit, not
evidence of novelty or priority. F.1--F.23 are locally derived and
independently audited.

## Evidence reconciliation

### Resolvent information is more than phase substitution

Siming He writes the shear advection-diffusion equation mode by mode after
Fourier transformation in the streamwise variable. The zero mode follows
ordinary diffusion, whereas the nonzero-mode enhanced-dissipation result is
obtained through resolvent estimates and a semigroup argument. This
supports the R0.75F boundary: rewriting `i ell b g_nm` with the product
equation cannot by itself create the coercivity that a resolvent estimate
must prove. The paper does not treat the frozen spherical collar, its
off-diagonal cutoff convolution, or the Version-M payment.

### Pathwise methods add trajectory information

Gardner, Liss, and Mattingly develop a pathwise approach to passive scalars
advected by shear flows. Their stochastic representation and local shear
analysis distinguish streamline averages from fluctuating modes and obtain
enhanced decay from trajectory separation across streamlines. That is
additional dynamical information, not an algebraic rearrangement of the
localized energy identity. Their locality follows streamlines rather than
the stationary three-dimensional collar used here, so the paper does not
yield E.24 directly.

### Localization retains a drift flux

Albritton and Dong's localized drift-diffusion energy calculation contains
a drift boundary contribution involving the scalar energy and the normal
component of the divergence-free drift. Their quantitative estimates use
drift integrability and geometric slicing. This supports retaining the
R0.75E/R0.75F signed collar flux: global skew-adjointness cannot simply be
reused after physical localization. It does not provide a positivity-only
comparison with the Fourier-diagonal part.

## Claim-to-source ledger

| Claim supported | Primary source | Date/version | URL | Access note |
|---|---|---|---|---|
| Streamwise Fourier modes evolve separately under a shear; actual enhanced decay for nonzero modes is obtained by resolvent/semigroup estimates | Siming He, *Enhanced dissipation, hypoellipticity for passive scalar equations with fractional dissipation* | arXiv:2103.07906v2, revised 2021-10-22 | https://arxiv.org/abs/2103.07906 | arXiv abstract and HTML equations 1.8--1.9 inspected 2026-09-03; URL rechecked HTTP 200 |
| A pathwise stochastic method uses local shear and trajectory information; the streamline average decouples from fluctuating modes | Victor Gardner, Kyle L. Liss, Jonathan C. Mattingly, *A pathwise approach to the enhanced dissipation of passive scalars advected by shear flows* | arXiv:2410.05657v1, submitted 2024-10-08 | https://arxiv.org/abs/2410.05657 | arXiv abstract and HTML equations 1.4--1.5 inspected 2026-09-03; URL rechecked HTTP 200 |
| Local energy estimates for divergence-free drift retain a drift boundary flux and require quantitative drift/geometric control | Dallas Albritton, Hongjie Dong, *Regularity properties of passive scalars with rough divergence-free drifts* | arXiv:2107.12511v1, submitted 2021-07-26 | https://arxiv.org/abs/2107.12511 | arXiv HTML discussion and equation 1.6 inspected 2026-09-03; URL rechecked HTTP 200 |

## Gap matrix

| Question | Evidence status | Consequence |
|---|---|---|
| Does the modal equation preserve streamwise wave number? | Established in primary literature and rederived locally | Modal invariance is standard structure, not a novelty claim |
| Does the product equation alone imply enhanced dissipation? | No; the cited result uses additional resolvent/semigroup control | F.17--F.18 correctly identify the direct substitution as tautological |
| Can pathwise residence information produce decay beyond energy algebra? | Yes in the cited shear setting | A pathwise collar-residence route remains viable but unproved here |
| Does physical localization retain drift flux? | Established in local drift-diffusion theory | The off-diagonal collar flux cannot be deleted by global skew-adjointness |
| Does positivity of a bounded cutoff control the localized form by its diagonal average? | Refuted locally by the exact finite F.20 family | Any successful comparison must add geometry, dynamics, frequency cost, or payment input |
| Does an existing theorem close the frozen E.24 payment target? | No matching theorem found in the bounded search | The arbitrary-real cross-mode gate remains open |

## Search boundary and stopping rule

Searches covered arXiv primary papers on shear Fourier modes, enhanced
dissipation, pathwise passive-scalar estimates, and localized
drift-diffusion energy. Follow-up inspection reached the modal equations,
the resolvent/pathwise mechanisms, the streamline-average statement, and
the localized drift flux. The search stopped once the method boundary was
stable: each successful neighboring theorem adds information absent from
the direct F.8 substitution, but none states the frozen collar/payment
estimate.

**Literature-established:** modal invariance for coordinate-independent
shears, enhanced decay from resolvent or pathwise mechanisms, decoupling of
the streamline average, and persistence of drift flux under localization.

**Locally proved:** the exact cancellation F.17--F.18 and the finite
positivity-only no-go F.19--F.23.

**Open:** the arbitrary-real estimate E.24, a quantitative collar
uncertainty/residence-time estimate, complete-clock extraction, fixed
deletion, suitable-weak transfer, and all Navier--Stokes regularity or
singularity conclusions. **NOT CLAY.**
