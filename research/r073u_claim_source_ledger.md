# R0.73U claim--source ledger

**Status:** parent derivation, independent analytic audit, exact-certificate
final seal, formal-figure QA, and immutable source pins passed; bilingual
rendering and public deployment remain release gates

**Ordinary translation path:** `LOCAL_DIRECT_NO_DGX`

## Claim ledger

| ID | Claim | Evidence class | Exact source or proof | Release use and boundary |
|---|---|---|---|---|
| U1 | The local product tensor \(T^{\rm loc}_{ij}(h)=\widehat{u_i u_j}(h)\) is not the classical two-point K\'arm\'an--Howarth--Monin tensor \(R_{ij}(r)=\int u_i(x)u_j(x+r)\,d\mu(x)\). The first has cross-wave-number convolution data; the second has same-wave-number covariance data. | `INTERNAL_EXACT` | Direct Fourier calculation in [problem freeze](r073u_problem_freeze.md), Section 2, and [primary-literature audit](r073u_primary_literature_audit.md), Section 1 | Binding scope rule. No statement about one object may be transferred silently to the other. |
| U2 | The exact KHM/structure-function hierarchy advances from second-order statistics to signed third-order moments and then to higher orders; it is not a finite autonomous closure. | `VERIFIED_CLASSICAL` | von K\'arm\'an--Howarth 1938 [DOI](https://doi.org/10.1098/rspa.1938.0013); Hill 2001 [DOI](https://doi.org/10.1017/S0022112001003949); [primary-literature audit](r073u_primary_literature_audit.md), Section 2 | Classical comparison only. It does not prove the R0.73U local-tensor witness. |
| U3 | With the stated periodic Riesz convention, the full local product tensor reconstructs the mean-zero pressure at the same heat scale: \(p_s=R_iR_j\Theta_{s,ij}=R_iR_j(v_{s,i}v_{s,j}+\tau_{s,ij})\). | `VERIFIED_CLASSICAL` | Pressure Poisson equation and commutation of \(P_s\) with periodic Riesz transforms; [analytic proof](r073u_tensor_heat_hierarchy.md), Sections 1 and 3; independent sign audit in [independent audit](r073u_independent_analytic_audit.md), Sections 1--2 | Instantaneous pressure sufficiency is not dynamic closure. The scalar trace alone generally does not contain this polarization. |
| U4 | \(\Theta_s=P_s(u\otimes u)\) and \(\tau_s=\Theta_s-v_s\otimes v_s\) are symmetric positive semidefinite pointwise. | `INTERNAL_EXACT` | Nonnegative heat kernel, Jensen, and the heat-covariance formula; [analytic proof](r073u_tensor_heat_hierarchy.md), Proposition 2.1; [independent audit](r073u_independent_analytic_audit.md), Section 2 | Positivity is exact, but it does not make \(-\tau_s:\nabla v_s\) sign-definite. |
| U5 | The heat covariance obeys \((\partial_s-\Delta)\tau_s=2\sum_\ell\partial_\ell v_s\otimes\partial_\ell v_s\), \(\tau_0=0\), with the corresponding Duhamel representation in \(s\). | `INTERNAL_EXACT` | Direct semigroup/product differentiation in [analytic proof](r073u_tensor_heat_hierarchy.md), (2.1)--(2.2); independent derivation in [independent audit](r073u_independent_analytic_audit.md), Section 2 | This is an exact equation in the filter parameter \(s\), not a closed physical-time constitutive equation. No novelty claim is made. |
| U6 | The two-level identity \(\tau_{s+r}(u)=P_r\tau_s(u)+\tau_r(P_su)\) holds. | `INTERNAL_EXACT` | Heat-semigroup algebra in [analytic proof](r073u_tensor_heat_hierarchy.md), (2.6); nearest filtering framework: Germano 1992 [DOI](https://doi.org/10.1017/S0022112092001733) | Organizes filter levels but does not determine \(\tau_s\) from the single resolved field \(v_s\). |
| U7 | Exact filtering gives \(\partial_tv_s+\mathbb P\nabla\!\cdot(v_s\otimes v_s+\tau_s)=\nu\Delta v_s\), with the stated primitive-variable and resolved-energy identities. | `VERIFIED_CLASSICAL_RECONSTRUCTION` | Filtered Navier--Stokes algebra; [analytic proof](r073u_tensor_heat_hierarchy.md), (3.2)--(3.4); Germano 1992 [DOI](https://doi.org/10.1017/S0022112092001733) | The stress is exact but unresolved; this is not an LES closure model. |
| U8 | If \(u\in E(I)=L_t^4L_x^6(I)\), then uniformly in \(s\ge0\), \(\|\Theta_s\|_{L_t^2L_x^3}\le\|u\|_E^2\), \(\|\tau_s\|_{L_t^2L_x^3}\le\|u\|_E^2\), and \(\|p_s\|_{L_t^2L_x^3}\le C_R\|u\|_E^2\). | `INTERNAL_COROLLARY` | PSD trace bound, heat contraction, H\"older, and periodic Riesz boundedness; [analytic proof](r073u_tensor_heat_hierarchy.md), (4.2)--(4.4); [independent audit](r073u_independent_analytic_audit.md), Section 3 | Exact critical-exponent compatibility, conditional on the classical strong norm already being finite. It is circular for arbitrary-data regularity. |
| U9 | The R0.73Q causal Stokes map sends the stress row back to \(E\): \(\sup_s\|\mathcal S_\nu\tau_s\|_E\le C_{B,\nu}\|u\|_E^2\). | `INTERNAL_CONDITIONAL` | U8 plus the previously audited periodic Stokes--HLS estimate; [analytic proof](r073u_tensor_heat_hierarchy.md), (4.5)--(4.7) | Reuses the R0.73Q exponent mechanism. It creates no new arbitrary-data bound. |
| U10 | At every fixed \(s>0\), energy alone yields \(\|\tau_s\|_{L_t^2L_x^3}^2\le C_S^2H_3(s)E_0^2/(2\nu)\), hence the short-scale cost \(\|\tau_s\|_{L_t^2L_x^3}\lesssim E_0(\nu s)^{-1/2}\) for \(0<s\le1\). | `INTERNAL_COROLLARY` | Energy inequality, periodic Sobolev, heat smoothing, and time interpolation; [analytic proof](r073u_tensor_heat_hierarchy.md), (4.8)--(4.12); [independent audit](r073u_independent_analytic_audit.md), Section 3 | A genuine positive-scale estimate. It is not uniform as \(s\downarrow0\) and does not imply continuation. On a smooth branch it is read on its interval of existence; the notation must not presuppose a global smooth solution. |
| U11 | Centering pressure by \(\bar p_w=(\int wp)/(\int w)\) gives, for \(0<\vartheta\le2\), \(Q'+4\nu Y+(2-\vartheta)\nu X^2\le4\mathcal P_*/(\vartheta\nu)\), where \(\mathcal P_*=\int w(p-\bar p_w)^2\). | `INTERNAL_COROLLARY` | Gauge invariance, the classical quartic balance, weighted Cauchy, and Young; [analytic proof](r073u_tensor_heat_hierarchy.md), (5.1)--(5.6); [independent audit](r073u_independent_analytic_audit.md), Section 4 | A centered sharpening of the local inequality, not a new regularity criterion. |
| U12 | \(\mathcal P_*\le\int wp^2\le C_R^2AQ\), so \(\beta_*=\mathcal P_*/Q\le C_R^2A\) when \(Q>0\). | `INTERNAL_COROLLARY` | Periodic Riesz and H\"older estimates in [analytic proof](r073u_tensor_heat_hierarchy.md), (5.7); direct weighted-pressure collision: Tran--Yu--Dritschel 2021 [DOI](https://doi.org/10.1017/jfm.2020.1033) | The centered quantity can be strictly smaller, but the formula has a strong classical collision. Novelty and priority wording are forbidden. |
| U13 | The condition \(\beta_*\in L_t^1\) controls \(Q\) by Gronwall and enters the classical \(L_t^\infty L_x^4\) continuation route. | `INTERNAL_CONDITIONAL` | U11 with \(\vartheta=1\) or \(2\), followed by the classical \(L^4\) continuation argument; Tran--Yu--Dritschel 2021 [DOI](https://doi.org/10.1017/jfm.2020.1033) | This is a conditional restatement of a classical-strength pressure criterion. R0.73U does not prove \(\beta_*\in L_t^1\) from arbitrary energy data. |
| U14 | The exact tensor heat-plane law contains an even gradient-product term and odd cubic and pressure--velocity terms, as displayed in (6.2) of the proof. | `VERIFIED_CLASSICAL_RECONSTRUCTION` | Product equation for \(u_i u_j\), followed by \(P_s\); [analytic proof](r073u_tensor_heat_hierarchy.md), Section 6; independent index/sign derivation in [independent audit](r073u_independent_analytic_audit.md), Section 1 | Repairs instantaneous pressure reconstruction but exposes the missing signed third-order tangent. Exact KHM and Onsager/filtering hierarchies are conceptual collisions, not identical objects. |
| U15 | The even quadratic state \(\mathcal H(u)=\{\Theta_s,\tau_s,p_s:s\ge0\}\) satisfies \(\mathcal H(-u)=\mathcal H(u)\), while a nonzero nonlinear tensor tangent reverses sign. Therefore this state alone cannot have a single-valued autonomous law recovering the signed tensor tangent for every smooth divergence-free field. | `INTERNAL_EXACT` | Parity applied to U14, made non-vacuous by U16; [problem freeze](r073u_problem_freeze.md), Section 4; [analytic proof](r073u_tensor_heat_hierarchy.md), Section 7 | Restricted no-go for an equality based only on even quadratic data. It does not apply once the signed velocity \(v_s\), an odd/cubic state, or the full initial velocity is included. It does not exclude upper bounds. |
| U16 | At the initial time \(t=0\), the four-site field \(u=(2\sin(x+y),2\sin x-2\sin(x+y),0)\) has, at \(h_*=(1,2,0)\), \(\widehat T(h_*)=0\), zero viscous tensor coefficient, and nonlinear tensor tangent \(K=\begin{psmallmatrix}-2&1&0\\1&0&0\\0&0&0\end{psmallmatrix}\), \(|K|_F=\sqrt6\). Its sign pair has initial tensor-tangent separation \(2e^{-5s}K\). | `INTERNAL_EXACT` | Two independent sparse-Fourier calculations reported in [analytic proof](r073u_tensor_heat_hierarchy.md), (7.1)--(7.7), and [independent audit](r073u_independent_analytic_audit.md), Section 5; sealed exact package under `research/certificates/r073u/`, 75/75 checks | The rational certificate is release-bound to the analytic and certificate-source commits. This is an initial-state separation, not a trajectory symmetry. The planar smooth initial field is not a singularity, near-singularity, blow-up solution, vortex-stretching example, or simulation. |
| U17 | Under integer dilation \(u_L(x)=u(Lx)\), the coefficient separation is \(2Le^{-5sL^2}K\); at \(s=\theta L^{-2}\), its Frobenius size is \(2\sqrt6Le^{-5\theta}=2\sqrt{6\theta}e^{-5\theta}s^{-1/2}\). | `INTERNAL_EXACT_SCALING` | Exact dilation and heat multiplier calculation; [analytic proof](r073u_tensor_heat_hierarchy.md), Section 8; [independent audit](r073u_independent_analytic_audit.md), Section 5 | One-derivative cost for this coefficient at a fixed parabolic heat slice. It is not a universal lower bound against time integration, signed augmentation, one-sided estimates, or other cancellations. |
| U18 | The bounded primary-source search did not locate an existing theorem with the same heat-covariance PDE, critical tensor row, four-site parity witness, and coefficient-level parabolic separation package. | `NOT_ESTABLISHED` | [Primary-literature audit](r073u_primary_literature_audit.md), Sections 6--7 | Non-detection is not proof of novelty, priority, non-existence, or first authorship. The permitted description is “local auditable synthesis.” |
| U19 | Arbitrary-data three-dimensional global regularity and the Clay Millennium problem remain open. | `OPEN` | U8--U10 retain either a classical strong-norm hypothesis or an \(s^{-1/2}\) short-scale loss; U15--U17 are restricted information no-go statements | No affirmative global-regularity or Clay conclusion is licensed. `NOT CLAY`. |

## Release-binding ledger

```text
parentAnalyticDerivation=PASS
independentAnalyticAudit=PASS
localProductTensorDistinctFromKHM=TRUE
instantaneousPressureFromLocalProductTensor=VERIFIED_CLASSICAL
quadraticTensorOnlyDynamicClosure=NOT_ESTABLISHED
exactHigherMomentHierarchy=VERIFIED_CLASSICAL
heatCovariancePSD=INTERNAL_EXACT
heatCovarianceScalePDE=INTERNAL_EXACT
filteredEquation=VERIFIED_CLASSICAL_RECONSTRUCTION
criticalTensorStressRow=INTERNAL_COROLLARY
criticalTensorStressRowAssumesL4tL6x=TRUE
energyOnlyFixedScaleStress=INTERNAL_COROLLARY
energyOnlyUniformAsSToZero=FALSE
centeredPressureVariance=INTERNAL_COROLLARY
centeredPressureVarianceDirectClassicalCollision=TRUE
fourSiteParityWitness=INTERNAL_EXACT
formalFiniteCertificate=PASS
formalFiniteCertificateChecks=75
formalFigurePackage=PASS
formalFigureChecks=325
sourceCommitAssigned=TRUE
sourceCommit=84e808dae473f6381cbf9df55a71f5fe81a1cfce
certificateSourceCommit=6c79f23152116f5d420be6ff03653500ab02ef0e
finitePackageCommit=044bfb3f7e5af98e2615f60747c9e5109ef12d7c
figurePackageCommit=6c20af03a21488fea3f060738084fa9048437984
finalSeal=TRUE
publicReleaseTransaction=PENDING
navierStokesSimulation=NOT_RUN
finiteWitnessIsSimulation=FALSE
ordinaryTranslationPath=LOCAL_DIRECT_NO_DGX
dgxUsed=FALSE
arbitraryThreeDimensionalGlobalRegularity=OPEN
clayConclusion=OPEN
noveltyOrPriorityClaim=FORBIDDEN
NOT CLAY
```

## Evidence rules

1. `VERIFIED_CLASSICAL` and `VERIFIED_CLASSICAL_RECONSTRUCTION` are
   attribution classes, not novelty classes.
2. `INTERNAL_EXACT` means the displayed identity or finite calculation has a
   self-contained derivation and independent analytic readback.  The finite
   witness is now release-bound by its formal seal, but neither the label nor
   the seal certifies priority or the continuum PDE proof.
3. The local product tensor and the two-point KHM tensor are different data
   structures.  KHM literature supplies a closure comparison, not the proof
   of the R0.73U four-site local-tensor witness.
4. Positive semidefiniteness of \(\tau_s\) does not give a sign to the
   transfer \(-\tau_s:\nabla v_s\).
5. The \(L_t^2L_x^3\) critical row is either conditional on
   \(u\in L_t^4L_x^6\), or energy-only at fixed \(s>0\) with the explicit
   \(s^{-1/2}\) loss.  These alternatives must not be merged into a uniform
   energy-class theorem.
6. The centered pressure-variance inequality has a direct classical
   weighted-pressure collision.  It may be called an internal centered
   corollary, never a new criterion.
7. The four-site parity witness rules out a single-valued signed-tangent
   equality for the even quadratic state.  It does not rule out one-sided or
   absolute estimates, signed/cubic augmentation, time integration, or the
   original velocity state.
8. The finite witness is an exact sparse-convolution diagnostic, not a
   Navier--Stokes simulation and not a certificate of the continuum proof.
9. The word “critical” refers to the local/Euclidean parabolic exponent line;
   it is not literal invariance under normalized fixed-torus covering maps.
10. Ordinary Chinese--English translation is performed directly on the local
    workstation.  DGX is not used for translation or for this analytic/finite
    release.
11. Bounded collision search cannot establish novelty, priority, or
    non-existence.  Arbitrary-data global regularity and the Clay Millennium
    problem remain open.
