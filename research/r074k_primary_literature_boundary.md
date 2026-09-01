# R0.74K bounded primary-literature boundary

## Question screened

Does an existing primary result directly imply the signed finite-window
collar estimate

\[
 \sup_{\tau\in I_{R_j}}[\mathcal I_j(\tau)]_+
 \lesssim \Gamma_jL_jR_j^5
\]

for the frozen, time-dependent, \(R_j\)-dependent R0.74F shear and its
periodic inward bridges?

The answer from this bounded screen is **no direct implication found**.  It
is not a systematic novelty search and is not evidence of priority.

## Primary sources

1. **Bedrossian--Coti Zelati (2017), _Enhanced dissipation,
   hypoellipticity, and anomalous small noise inviscid limits in shear
   flows_.**  The paper proves quantitative semigroup decay and
   hypoelliptic regularization for passive scalars advected by autonomous
   shear profiles, mode by mode in the streamwise variable.  Its localized
   spectral-gap and hypocoercive framework is prior art for the general
   shear-enhanced-dissipation mechanism.  It does not state a signed radial
   collar-flux estimate for the calibrated time-dependent family used here.
   Primary source: <https://arxiv.org/abs/1510.08098>.

2. **Albritton--Beekie--Novack (2022), _Enhanced dissipation and
   Hoermander's hypoellipticity_.**  This work obtains enhanced-dissipation
   time scales from bracket and subelliptic estimates for autonomous shear
   advection, including periodic and bounded transverse geometries.  It
   controls global semigroup decay and regularization, not the signed
   finite-time annular trace in R0.74K.  Primary source:
   <https://arxiv.org/abs/2105.12308>.

3. **Villringer (2024/2025), _Enhanced Dissipation via the Malliavin
   Calculus_.**  The stochastic integration-by-parts proof recovers
   enhanced dissipation and streamwise hypoelliptic regularization for
   smooth autonomous shears with finite-order critical points.  Its
   Malliavin covariance mechanism is relevant to preserving shear--Brownian
   dependence, but its theorem is not the weighted periodic-bridge estimate
   (4.3).  Primary source: <https://arxiv.org/abs/2405.12787>.

4. **Gardner--Liss--Mattingly (2024), _A pathwise approach to the enhanced
   dissipation of passive scalars advected by shear flows_.**  The paper
   uses Girsanov control and gives global and streamline-local decay,
   including profiles with infinite-order degeneracy.  This is the closest
   methodological prior art for exceptional-path control.  The stated
   results concern autonomous shear semigroups and total-variation/decay
   estimates; they do not directly preserve the signed radial-collar
   observable or the R0.74F time calibration.  Primary source:
   <https://arxiv.org/abs/2410.05657>.

5. **Liss--Luan (2026), _Uniform-in-diffusivity mixing by shear flows:
   stochastic and dynamical perspectives_.**  This recent preprint proves
   sharp uniform-in-diffusivity mixing rates using a stochastic
   representation and integration by parts under the regularity required
   by the zero-diffusion problem.  It concerns mixing norms for parallel
   shear flows, not the finite calibrated signed collar flux here.  Primary
   source: <https://arxiv.org/abs/2603.09238>.

## Collision matrix

| Mechanism | Established in sources | Needed for R0.74K (4.3) | Directly supplied? |
|---|---:|---:|---:|
| Autonomous shear semigroup decay | Yes | No, by itself | No |
| Hypocoercive or subelliptic smoothing | Yes | Potential ingredient | No |
| Malliavin covariance/integration by parts | Yes | Potential ingredient | No |
| Girsanov exceptional-path control | Yes | Potential ingredient | No |
| Streamline-local decay | Yes | Related but differently normalized | No |
| Time-dependent \(R_j\)-dependent plateau shear | Not in screened theorem statements | Yes | No |
| Periodic bridge conditioned across \(O(L_jR_j)\) | Not in screened theorem statements | Yes | No |
| Signed smooth radial collar trace | Not in screened theorem statements | Yes | No |
| Exact \(\Gamma_jL_jR_j^5\) scale | Not in screened theorem statements | Yes | No |

## Claim boundary

The sources show that shear-enhanced mixing is mature prior art and offer
several possible proof technologies.  The bounded non-hit only says that no
quoted theorem can be imported verbatim to close (4.3).  It does not show
that the prospective lemma is new, publishable, or correctly posed, and it
does not change the OPEN or NOT CLAY status.
