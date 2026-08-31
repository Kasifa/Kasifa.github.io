# R0.73T evidence and gap matrix

**Status:** primary-source audit, exact-certificate final seal, and formal-
figure QA closed; only the public HTML/PDF/deployment transaction remains

| Claim slot | Best current evidence | Confidence | Collision, contradiction, or unresolved gap | Release treatment / next query |
|---|---|---:|---|---|
| Exact coefficient law for \(C_h=\widehat{|u|^2}(h)\) | Two independent physical/Fourier derivations; it is the spatial Fourier transform of the classical local-energy identity displayed by Tran--Yu--Dritschel 2021 [DOI](https://doi.org/10.1017/jfm.2020.1033) | high | \(C\) is not autonomous because gradient correlation and the signed flux \(u(w+2p)\) remain; in general \(p=R_iR_j(u_i u_j)\) also requires the full tensor beyond its scalar trace; literal \(C_h\) packaging was not located | Label `VERIFIED_CLASSICAL_RECONSTRUCTION`; publish both distinct missing-variable mechanisms, not a novelty claim |
| Exact \(L^4\) balance | Direct integration by parts; Tran--Yu--Dritschel 2021 gives exact \(L^q\) balances and pressure-correlation criteria [DOI](https://doi.org/10.1017/jfm.2020.1033) | high | Direct formula-level classical collision; risk of presenting the identity as new | Label `VERIFIED_CLASSICAL_RECONSTRUCTION` |
| \(Q'+4\nu Y+\nu X^2\le4C_R^2\nu^{-1}AQ\) | Exact balance + periodic Riesz \(L^3\) bound + Young + R0.73S; constant checked independently by completing the square | high | No control of \(\int A\,dt\); Tran--Yu--Dritschel 2021 is the nearest direct \(L^4\)/pressure collision [DOI](https://doi.org/10.1017/jfm.2020.1033) | Label `INTERNAL_COROLLARY`, never a new \(L^p\) theorem |
| \(\int A\,dt\) is critical, at least as restrictive as, and directly implies \(L_t^2L_x^\infty\) | Exact integer-dilation scaling and \(\|u\|_\infty^2\le A\); Serrin 1962 gives the classical critical comparison | high | This destroys any claim that the \(AQ\) inequality bypasses Serrin | Put the comparison beside the positive theorem |
| Differentiating \(A\) does not close in \((A,Q,E)\) | Upper-Dini law introduces derivative Wiener norms of \(|\nabla u|^2\) and \(u(w+2p)\) | high | This is failure of this state vector, not a theorem that every weighted Wiener hierarchy fails | State exact missing terms; keep weighted/tensor variants open |
| Scalar \(C\) loses carrier scale | Rotating shear has \(C=\delta_0\) for every \(N\) but \(\dot C_0=-2\nu N^2\) | exact | A frequency-weighted \(C\) can restore scale, so no-go is only for unweighted scalar \(C\) | Label `CLOSED_EXACT`; include the quantified boundary |
| Scalar \(C\) loses the signed velocity phase entering the pressure pairing | Six-mode \(u_L,-u_L\) have identical complete \(C\), identical \(u\otimes u\), and identical mean-zero \(p\), while pressure work is \(\mp384L\); two independent Fraction reconstructions | exact | The sign change comes from the leading velocity factor, not from a change of pressure tensor or pressure; fields are planar smooth witnesses and omit 3D vortex stretching | Label `CLOSED_EXACT`; explicitly forbid using this pair alone as a pressure-tensor-polarization witness or using blow-up language |
| General pressure reconstruction requires tensor data beyond scalar \(C\) | \(p=R_iR_j(u_i u_j)\), whereas \(C=\widehat{\sum_i u_i^2}\) records only the tensor trace | exact / classical | This formula-level information barrier is distinct from the sign-pair certificate, whose tensor and pressure are unchanged | Keep the tensor route open; do not attribute this conclusion to the six-mode sign pair alone |
| No finite bound on \(|Q'|\) from \((E,Q,A,D_C)\) | Shear gives fixed summaries and \(|Q'|=(3/2)\nu L^2\) | exact | Does not contradict the one-sided upper inequality | State “absolute/two-sided no-go,” never “no upper estimate” |
| Heat weighting repairs carrier scale but not signed velocity phase | Exact heat-plane law; weighted sign pair differs by \(-768Le^{-8\tau L^2}\) despite identical \(u\otimes u\) and pressure | high | At fixed \(\tau\) the difference decays; at parabolic \(\tau\asymp L^{-2}\) one pays \(L\asymp\tau^{-1/2}\) | Keep scale cost explicit; next query is tensor heat commutator |
| Periodic shell coercivity \(\mathcal D_j\gtrsim2^{2j}Q_j\) | Li 2013 and Li--Sire 2023 scalar frequency-localized Bernstein; Li--Sire Theorem 4.2 at \(p=4,s=2\), followed by the local componentwise vector deduction [DOI](https://doi.org/10.1090/tran/8708) | high | Theorem 4.2 is stated for a real scalar; Remark 4.1 is not a literal frequency-localized vector theorem. Cutoff constants and low shells must remain explicit | Cite the scalar theorem and display the three-component deduction; `VERIFIED_CLASSICAL_WITH_ADAPTATION` |
| Shell Duhamel transport | Exact projected equation + shell coercivity + R0.73S | high | Forcing is not the shell's self-advection and is not controlled by shell statistics alone | Label `INTERNAL_CONDITIONAL`; preserve the Leray projector |
| Energy-only shell closure | Only \(F_j\lesssim2^{5j/2}\|u\|_2^2\) | contradicted at desired scaling | High-frequency factor is supercritical | Record as the exact unresolved flux barrier |
| Classical-strong shell closure | \(F_j\lesssim2^j\|u\|_4^2\) | valid but circular for the target | Reintroduces the strong norm being transported | Use only as a diagnostic comparison |
| Identical prior package | Bounded searches across autocorrelation, energy-density Fourier/Wiener, \(AQ\), \(L^4\)-pressure, and nonlinear Bernstein literature found related components but no identical package; velocity-Wiener near-neighbour Ambrose--Lopes Filho--Nussenzveig Lopes 2024 [DOI](https://doi.org/10.1090/proc/16615) | low / not required | Absence from a bounded search is not a novelty, priority, or non-existence proof | Say “local auditable synthesis”; `noveltyOrPriorityClaim=FORBIDDEN` |
| Exact finite diagnostic seal | Final certificate rerun and manifest seal passed `55/55`; source commit `05c55d21f060a17a0a4db04c12e89e7271b03d30`, scientific-artifact commit `29d01625731d1c611f927c2852dbddf05967c6cb` | exact package QA | Certifies finite rational reconstruction and package binding only; it is not a continuum proof or a Navier--Stokes simulation | `finiteFormulaDiagnosticValidation=PASS`; `finalSeal=TRUE` |
| Formal figure package | Formal figure QA passed `106/106` over 28 source rows. Figure data, validation, PDF, SVG, and PNG remain at scientific-artifact commit `29d01625731d1c611f927c2852dbddf05967c6cb`; metadata-only reseal `b17c45013cc9a3f6f09efa146bcbc2ef8ab043f9` adds wall time and bracketed same-host runtime fields | exact package QA | Certifies figure data lineage, hashes, render checks, and transparent metadata provenance only; it adds no theorem strength | `formalFigurePackage=PASS`; distinguish scientific artifacts from the metadata reseal |
| Ordinary translation route | User instruction fixes local direct translation | locked | Route is not evidence that translation/deployment has completed | `ordinaryTranslationPath=LOCAL_DIRECT_NO_DGX` |
| Public HTML/PDF/deployment transaction | Not yet completed | pending | A passed source, certificate, or figure gate is not proof of public delivery | Complete and verify the release transaction separately; `dgxUsed=FALSE` |
| Arbitrary 3D global regularity / Clay | No implication from the displayed estimates | open | Main public overclaim risk | `arbitraryThreeDimensionalGlobalRegularity=OPEN`; `NOT CLAY` |

## Primary-source backbone

1. James Serrin, *On the interior regularity of weak solutions of the
   Navier--Stokes equations*, Archive for Rational Mechanics and Analysis 9
   (1962), 187--195, [DOI](https://doi.org/10.1007/BF00253344).
2. Tosio Kato, *Strong \(L^p\)-solutions of the Navier--Stokes equation in
   \(\mathbb R^m\), with applications to weak solutions*, Mathematische
   Zeitschrift 187 (1984), 471--480,
   [DOI](https://doi.org/10.1007/BF01174182).
3. Tosio Kato, *Liapunov functions and monotonicity in the Navier--Stokes
   equation*, Lecture Notes in Mathematics 1450 (1990), 53--63,
   [Springer volume](https://link.springer.com/book/10.1007/BFb0084893).
4. Dong Li, *On a frequency localized Bernstein inequality and some
   generalized Poincaré-type inequalities*, Mathematical Research Letters 20
   (2013), 933--945,
   [DOI](https://doi.org/10.4310/MRL.2013.v20.n5.a9),
   [arXiv](https://arxiv.org/abs/1212.0183).
5. Dong Li and Yannick Sire, *Remarks on the Bernstein inequality for higher
   order operators and related results*, Transactions of the American
   Mathematical Society 376 (2023), 945--967, especially Theorem 4.2,
   Remark 4.1, and Lemma 4.4,
   [DOI](https://doi.org/10.1090/tran/8708),
   [arXiv:2109.07952](https://arxiv.org/abs/2109.07952).
6. C. V. Tran, X. Yu, and D. G. Dritschel, *Velocity--pressure correlation in
   Navier--Stokes flows and the problem of global regularity*, Journal of Fluid
   Mechanics 911 (2021), A18,
   [DOI](https://doi.org/10.1017/jfm.2020.1033).
7. Ch. V. Tran and X. Yu, *Pressure moderation and effective pressure in
   Navier--Stokes flows*, Nonlinearity 29 (2016), 2990--3005,
   [DOI](https://doi.org/10.1088/0951-7715/29/10/2990).
8. D. M. Ambrose, M. C. Lopes Filho, and H. J. Nussenzveig Lopes,
   *Existence and analyticity of the Lei--Lin solution of the Navier--Stokes
   equations on the torus*, Proceedings of the American Mathematical Society
   152 (2024), 781--795, a related velocity-Wiener/Gevrey branch,
   [DOI](https://doi.org/10.1090/proc/16615),
   [arXiv:2205.12383](https://arxiv.org/abs/2205.12383).

## Follow-up queries that remain live

1. Search pressure regularity criteria expressed through the full tensor
   \(\widehat{u_i u_j}\), not only scalar pressure norms.
2. Search signed heat-commutator estimates at the exact
   \(L_t^4L_x^6\)/LP weights used in R0.73Q--R0.73R.
3. Test whether a tensor heat hierarchy can retain polarization without
   paying a supercritical \(\tau^{-1/2}\) loss.
4. Treat every future “no collision found” statement as bounded-search
   evidence only, never a novelty certificate.
