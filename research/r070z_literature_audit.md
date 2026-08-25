# R0.70Z literature and collision audit

**Audit date:** 2026-08-25
**Verdict:** PASS with a strict no-priority boundary

## 1. Question and source policy

The bounded literature question was:

1. Is a principal eigenvalue gap of a Littlewood--Paley/frame covariance
   already known to determine the sign or depletion of
   \(\int S:Q\)?
2. Is the normalized projector coefficient
   \(|\nabla Q|/(\lambda_1-\lambda_2)\) already recognizable as a standard
   geometric regularity input?
3. Does a response-index lift already remove the common-response channel of
   full vortex stretching?

Only original papers, journal records, and author-hosted or publisher-hosted
versions were used for substantive comparisons. Search-engine snippets were
used only for discovery.

## 2. Claim-to-source gap matrix

| Claim family | Primary evidence | What the source supports | Difference from R0.70Z | Confidence / remaining gap |
|---|---|---|---|---|
| Vorticity-direction coherence can deplete stretching | [Constantin--Fefferman, *Direction of Vorticity and the Problem of Global Regularity for the Navier--Stokes Equations* (1993)](https://iumj.org/article/3627/) | Regularity follows under geometric control of the physical vorticity direction in the high-vorticity region | R0.70Z concerns the top projector of a frame covariance \(Q\), and proves that an eigengap alone supplies no such coherence | High; hypotheses and geometric objects are different |
| A varying plane/direction requires derivative control | [Miller, *A locally anisotropic regularity criterion ...* (2020)](https://arxiv.org/abs/2002.02152) | A locally varying plane can enter a scale-critical criterion when the gradient of its normal is controlled | Consistent with \( |\nabla P_1|\le|\nabla Q|/g \); it does not derive projector control from a covariance gap | High; this is the closest conceptual neighbor |
| Strain eigenvalues constrain blow-up geometry | [Miller, *A regularity criterion ... middle eigenvalue of the strain tensor* (2017/2020)](https://arxiv.org/abs/1710.05569) | The positive part of the middle eigenvalue of the physical strain tensor gives critical continuation criteria | Eigenvalues of \(S\) are not eigenvalues of the analysis-frame covariance \(Q\); no \(Q\)-gap sign law follows | High |
| Div--curl products lie in Hardy space | Coifman--Lions--Meyer--Semmes, *Compensated compactness and Hardy spaces*, J. Math. Pures Appl. 72 (1993), 247--286; [zbMATH record](https://zbmath.org/0864.42009) | The div--curl compensation used for \(h_j=\omega\cdot\nabla u_j\) and \(\mathcal H^1\)-BMO pairing | Gives the classical common-channel endpoint, not a new response-chord gain | High; original journal metadata verified, direct publisher full text was not available in the search interface |
| Direct vorticity-BMO endpoint | [Kozono--Taniuchi, *Bilinear estimates in BMO and the Navier--Stokes equations* (2000)](https://doi.org/10.1007/s002090000130) | A classical BMO endpoint control for Navier--Stokes vorticity | Supplies one sufficient common-channel control; R0.70Z does not prove it necessary and does not exclude other compensation | High |
| Near-\(L^\infty\) Besov vorticity criteria | [Kozono--Ogawa--Taniuchi, *Navier--Stokes equations in the Besov space near \(L^\infty\) and BMO* (2003)](https://doi.org/10.2206/kyushujm.57.303) | Extension criteria reach \(\dot B^0_{\infty,\infty}\) and the established BMO/Besov endpoint family | R0.70Z's response lift does not improve these criteria; its sharp family only blocks inherited absolute chord decay | High |
| Exact frame-covariance eigengap sign pair | Bounded exact-phrase and concept search described below | No located primary source contained the same pointwise \(Q\), uniform-gap, opposite-\(\int S:Q\) construction | Possible paper-level lemma, subject to a broader specialist search and external review | Low-to-moderate novelty confidence; no priority claim |
| Two-channel operators \(H^+,H^-,H^\Delta\) | Bounded exact-phrase and structural search described below | No located source used this response trace lift for full/principal/defect stretching | Algebraically useful, but may be a repackaging of standard polarization | Low novelty confidence; treat as infrastructure |

## 3. Searches performed

The first wave used:

- “Geometric constraints on potentially singular solutions”;
- “Direction of Vorticity and the Problem of Global Regularity”;
- “Navier--Stokes strain middle eigenvalue regularity criterion”;
- “vorticity direction coherence regularity criterion eigenvector alignment”.

The collision wave used:

- “frame covariance vorticity Navier--Stokes eigenvalue gap”;
- “Littlewood--Paley covariance tensor vorticity stretching”;
- “principal eigenvalue gap covariance Navier--Stokes vorticity”;
- “spectral projector vorticity direction Navier--Stokes regularity”.

The endpoint wave used:

- “Compensated compactness and Hardy spaces”;
- “vorticity BMO regularity criterion Navier--Stokes”;
- “Navier--Stokes equations Besov space near \(L^\infty\) and BMO”.

The exact frame-covariance phrases returned unrelated numerical spectral
projectors, standard Littlewood--Paley estimates, recent unverified
manuscripts, and general turbulence papers. None was used as evidence for a
novelty claim.

## 4. Reconciliation

The sources agree on the main boundary:

- geometric depletion requires directional regularity, coherence, or
  alignment;
- a spectral statement about the physical strain can be powerful because it
  enters an exact strain evolution identity;
- BMO/div--curl control supplies a known critical endpoint for the common
  stretching channel, without being proved necessary by R0.70Z.

R0.70Z is compatible with all three. Its eigengap identifies a smooth top
covariance projector, but it neither controls that projector's spatial
variation nor its signed alignment with the physical strain.

No source located in the bounded search contradicts the exact sign pair.
Conversely, absence from these searches is not evidence of priority or
novelty.

## 5. Allowed wording

The following wording is supported:

- “R0.70Z proves an exact finite-Fourier no-go within the pinned complete
  frame.”
- “A true principal eigengap alone does not determine principal-work sign.”
- “The normalized derivative \(|\nabla Q|/g\) is a sharp sufficient upper
  majorant exposed by projector perturbation; the exact quantity is
  \(|\nabla P_1|\).”
- “Classical critical BMO/div--curl control supplies one sufficient endpoint
  for the common response channel; other compensation is not excluded.”

The following wording is not supported:

- “first proof” or “first counterexample”;
- “new Navier--Stokes regularity criterion”;
- “the eigengap route is useless in every strengthened form”;
- “the response lift improves the BMO criterion”;
- any claim of global regularity, blow-up, or resolution of the Millennium
  problem.

## 6. Stop decision

The bounded audit is sufficient for an internal research gate because the
closest primary-source families have been identified and the consequential
claims have an explicit boundary. Another broad search is unlikely to change
the R0.70Z mathematical conclusion.

A paper submission would require a wider MathSciNet/zbMATH citation search,
specialist review of covariance or structure-tensor terminology, and an
independent novelty assessment.
