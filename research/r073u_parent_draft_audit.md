# R0.73U parent-draft reader audit

**Audit date:** 2026-09-01

**Scope:** independent reader-facing audit of the current R0.73U report,
claim--source ledger, evidence/gap matrix, and bilingual dictionary against the
four frozen analytic sources, the sealed exact certificate, the sealed formal
figure, and the public-writing rules in AGENTS.md

**Verdict:** PASS_WITH_ONE_NONMATHEMATICAL_ERRATUM

The mathematical identities, constants, finite witness, and narrow no-go scope
agree across the analytic proof, independent audit, exact certificate, figure
data, and the four reader-facing files. The draft does not support a global
regularity or Clay claim.

Seven reader corrections found in the first pass were applied and read back
during this audit. The title now names the proved obstruction: a signed tensor
time tangent from an even quadratic state. It no longer conflates that
obstruction with the resolved subfilter energy flux, which is computable once
the signed filtered velocity is retained but has no fixed sign.

## 1. Evidence read back in this audit

The following bindings and checks were verified rather than inferred from
prose:

| Evidence item | Verified value |
|---|---|
| Analytic source commit | 84e808dae473f6381cbf9df55a71f5fe81a1cfce |
| Certificate source commit | 6c79f23152116f5d420be6ff03653500ab02ef0e |
| Finite package commit | 044bfb3f7e5af98e2615f60747c9e5109ef12d7c |
| Figure package commit | 6c20af03a21488fea3f060738084fa9048437984 |
| Exact certificate | PASS, 75/75 checks |
| Certificate final seal | PASS |
| Certificate SHA-256 inventory | PASS |
| Formal figure | PASS, 325/325 checks |
| Figure final seal | PASS |
| Figure SHA-256 inventory | PASS |
| Ordinary translation path | LOCAL_DIRECT_NO_DGX |
| DGX used | FALSE |
| Navier--Stokes simulation | NOT_RUN |

The exact-certificate producer was rerun in check-only mode. The final seal was
then read back with the assigned certificate-source commit. The figure
validator was rerun in verify-only mode with the recorded Python 3.12 package
set. Both package trees are byte-identical to the commits listed above, and
every line in both SHA256SUMS inventories passed.

I also inspected the archival PNG directly. The matrices, peak, parity
separation, and coefficient-level qualifier are legible. The plot is visibly
an exact analytic/finite diagnostic rather than a PDE simulation or fitted
scaling law.

The stale PENDING values present at the start of this audit were corrected
while the audit was in progress. The current report and ledgers now record the
75-check finite seal, the 325-check figure seal, the immutable source/package
commits, and the still-pending bilingual/public transaction consistently.

## 2. Closed corrections and one nonblocking erratum

### Corrections closed during the audit

| ID | Read-back result |
|---|---|
| R1 | PASS. The English and Chinese titles now say that the even quadratic state is not dynamically closed. The subfilter energy flux and the signed tensor tangent are no longer conflated. |
| R2 | PASS. Report equation (2.3) now states \(h\ne0\) and \(\widehat p(0)=0\). |
| R3 | PASS. The report now defines \(C_S\), the R0.73T Wiener quantity \(A=\sum_h|\widehat{|u|^2}(h)|\), and \(C_R\), and it treats \(u\equiv0\) separately before defining \(\bar p_w\). |
| R4 | PASS. The report defines \(V=\Delta T-2\partial_\ell u\otimes\partial_\ell u\), and it marks the witness tangents as \(t=0\) Navier--Stokes vector-field tangents rather than a trajectory symmetry. |
| R5 | PASS. The bilingual dictionary distinguishes analytic-proof equation (6.2) from reader-report equation (7.2). |
| R6 | PASS. The report now says explicitly that matching \(s^{-1/2}\) exponents do not prove a sharp constant or a universal optimal order. |
| R7 | PASS. Public Chinese terminology is standardized to 四站点; the dictionary says that both positive and negative Fourier sites are counted. |
| R8 | PASS. The resealed stand-alone figure defines \(V=\Delta T-2\sum_\ell\partial_\ell u\otimes\partial_\ell u\), labels both tangents at the same initial time \(t=0\), and states that the comparison is not a trajectory symmetry. The new figure gate passes 325/325 checks. |

The final English title uses “but” and is both grammatical and mathematically
aligned with the Chinese title.

### Nonblocking residual E1: frozen analytic cross-reference

Section 9 of the frozen analytic proof says the higher-moment facts agree with
(5.2), while the intended tensor heat-plane formula is (6.2). The formula
itself is correct, and neither the reader report nor the bilingual dictionary
repeats the wrong reference.

Because the file is bound to the immutable analytic source commit, this can
remain a recorded non-mathematical erratum unless the parent deliberately
creates a new analytic source commit and reseals both dependent packages.

## 3. Mathematical consistency matrix

| Item | Result | Reader boundary |
|---|---|---|
| Local product tensor versus KHM tensor | PASS | The report correctly places cross-wave-number convolution beside same-wave-number covariance and transfers no theorem silently between them. |
| Pressure sign and same-scale reconstruction | PASS | The periodic Riesz sign and zero mode agree with the mean-zero pressure Poisson equation. Instantaneous pressure sufficiency is not called time closure. |
| PSD of \(\Theta_s\) and \(\tau_s\) | PASS | Jensen/covariance reasoning is correct. The report separately states that PSD gives no sign to \(-\tau_s:\nabla v_s\). |
| Heat-covariance scale PDE and Duhamel law | PASS | The factor 2, sign, initial value, and semigroup placement agree. The variable is the filter parameter \(s\), not physical time. |
| Two-level Germano/heat identity | PASS | It is described as scale organization, not a one-scale constitutive closure. |
| Filtered NSE and resolved energy law | PASS | The stress-divergence and \(+\tau_s:\nabla v_s\) signs are correct; \(\Pi_s=-\tau_s:\nabla v_s\) is not sign-definite. |
| Conditional critical stress row | PASS | Each tensor norm is bounded by \(\|u\|_{L_t^4L_x^6}^2\); the combined displayed sum has the correct factor 2. The circular strong-norm hypothesis remains in view. |
| Energy-only fixed-scale row | PASS | \(\|\tau_s\|_{L_t^2L_x^3}^2\le C_S^2H_3(s)E_0^2/(2\nu)\), \(H_3(s)\lesssim s^{-1}\), and the resulting \(E_0/\sqrt{\nu s}\) norm cost agree. The time constant is uniform only inside the stated smooth lifespan. |
| Centered pressure variance | PASS | The coefficients \(4\nu Y\), \((2-\vartheta)\nu X^2\), and \(4/(\vartheta\nu)\) agree. The comparison \(\beta_*\le C_R^2A\) is not turned into an a priori time budget. |
| Classical collision | PASS | Tran--Yu--Dritschel (2021) is named beside the centered formula; novelty and priority language is explicitly forbidden. |
| Tensor heat-plane law | PASS | The even gradient-product term and the odd cubic and pressure--velocity terms have the correct signs. |
| Four-site witness | PASS | The field, four coefficients, selected mode, \(\widehat T=0\), zero viscous coefficient, \(K=[[-2,1,0],[1,0,0],[0,0,0]]\), and \(\|K\|_F=\sqrt6\) agree with the sealed certificate. |
| Dilation and heat factor | PASS | The sign-pair separation is \(2Le^{-5sL^2}K\); its Frobenius norm at \(s=\theta L^{-2}\) is \(2\sqrt6Le^{-5\theta}=2\sqrt{6\theta}e^{-5\theta}s^{-1/2}\). |
| Profile maximum | PASS | The normalized \(\theta\)-profile peaks at \(\theta=1/10\), equivalently the figure's \(z\)-profile peaks at \(z=1/\sqrt{10}\). |
| Minimality boundary | PASS | The four-site lower boundary is restricted to a real, mean-zero, no-mean-mode finite Fourier witness for this parity mechanism. No universal closure minimality is claimed. |
| No-go scope | PASS | It excludes only a single-valued signed-tangent equality from the even quadratic state. It leaves one-sided/absolute estimates, time integration, cancellation, \(v_s\), and odd/cubic augmentation open. |
| Clay/global-regularity boundary | PASS | The report states OPEN and NOT CLAY; the finite diagnostic is not presented as a simulation or singularity. |

## 4. Title, sections, next route, and public voice

The nine Chinese section headings match the bilingual heading table in order.
The English release title and Chinese public title are synchronized across the
report and dictionary and now state the proved quadratic-state closure
boundary.

The next-route language remains inside what the results allow. An explicitly
odd third-order lift can evade the parity no-go because it keeps signed data.
The tensor-only envelope route asks only for one-sided or absolute control and
is therefore also not excluded. Neither route is described as already
solvable.

The prose follows AGENTS.md: it uses first-person singular for choices and
plans, neutral language for mathematics, and no collective 我们, campaign
slogan, novelty claim, or unsupported importance claim. Classical results,
internal corollaries, finite calculations, open gaps, and the bounded negative
literature search are separated. The primary-source links are adjacent to the
claims they support.

Ordinary translation is consistently locked to
ordinaryTranslationPath=LOCAL_DIRECT_NO_DGX. The certificate, figure, report,
claim ledger, gap matrix, and bilingual dictionary all state that DGX was not
used and that no Navier--Stokes simulation was run for this release.

## 5. Release recommendation

The reader draft passes analytic readback and may enter the local
Chinese--English HTML/PDF rendering gate. The single frozen cross-reference
erratum in Section 2 does not alter a formula, claim class, or public theorem
boundary.

The eventual publication test should assert:

| Required publication token | Required value |
|---|---|
| headlineDistinguishesFluxFromSignedTensorTangent | TRUE |
| pressureZeroModeConventionVisible | TRUE |
| weightedPressureZeroSolutionHandled | TRUE |
| witnessViscousCoefficientDefined | TRUE |
| witnessTangentsMarkedAsInitialState | TRUE |
| reportEquationReferencesMatch | TRUE |
| parabolicExponentDoesNotClaimSharpness | TRUE |
| ordinaryTranslationPath | LOCAL_DIRECT_NO_DGX |
| dgxUsed | FALSE |
| navierStokesSimulation | NOT_RUN |
| publicReleaseTransaction | PASS |
| Clay boundary | NOT CLAY |
