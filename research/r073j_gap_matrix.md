# R0.73J gap matrix

**Audit date:** 2026-08-30  
**Mathematical status:** J0--J11 are closed by the assembled analytic and
validated-computation evidence, with the numerical-independence limitation
stated below  
**Publication status:** source stage; no public release has been declared  
**Parent:** R0.73I  
**Frozen window:** \(0\le d\le1/450\)

This matrix separates three questions.  A claim can be mathematically closed
by a validated certificate, while a second computation still shares its raw
ODE grid, and while the publication inventory remains incomplete.  These are
not interchangeable statuses.

| ID | Claim | Current state | Decisive evidence and limitation |
|---|---|---|---|
| J0 | `rayleighKineticEquivalenceAndDiscreteness` | **CLOSED / PASS** | `r073j_analytic_proof.md` and its line-by-line audit prove the kinetic/ordinary generalized-root equivalence, compact-perturbation essential spectrum on \(i\mathbb R\), and discreteness with finite algebraic multiplicity in the open right half-plane. |
| J1 | `evansAnalyticInRightHalfPlane` | **CLOSED / PASS** | The analytic ODE construction and \(\lvert W_d-2i\lambda\rvert\ge2\operatorname{Re}\lambda\) give joint Evans analyticity on the required domains; the independent analytic audit passes the sign and analyticity checks. |
| J2 | `evansZeroOrderEqualsOperatorMultiplicity` | **CLOSED / PASS** | The exact operator-pencil factorization, periodic BVP/IVP analytic equivalence, partial-multiplicity argument, and kinetic/\(L^2\) Jordan bootstrap are all passed by the analytic audit. |
| J3 | `uniformHowardDisk` | **CLOSED / PASS** | The periodic Howard identity gives \(\lvert\lambda\rvert\le3\sqrt3/16<13/40\) for every right-half-plane eigenvalue.  This part is analytic and does not depend on a finite truncation or contour grid. |
| J4 | `basePositiveRealRoot` | **CLOSED / PASS** | R0.73C supplies the original interval sign bracket.  The present local base winding one, conjugation symmetry, and local disk \(\lvert\lambda-17/100\rvert<3/1000\) also give a positive real base root without relying on that earlier bracket. |
| J5 | `globalBaseWindingOne` | **CLOSED / PASS (formal certificate)** | The primary contour certificate gives exact positive-orientation winding one and a base homotopy lower bound \(>5.594985687\).  The independent reverse-order DCT/Clenshaw audit again gives winding one and a homotopy lower bound \(>5.642610414\). |
| J6 | `globalParameterBoundaryNonzero` | **CLOSED / PASS (formal certificate; independence qualified)** | A complete 56-panel, 7,168-cell cover gives primary \(\inf\lvert E\rvert>5.499484465\); the independent shared-grid post-processing gives \(>5.497398601\).  The second calculation does not independently regenerate the raw ODE values. |
| J7 | `localParameterBoundaryNonzero` | **CLOSED / PASS (formal certificate; independence qualified)** | A complete eight-panel, 4,096-cell cover gives primary \(\inf\lvert E\rvert>0.164355178\); the independent shared-grid post-processing gives \(>0.164339779\).  The natural-box audit described below is corroborative, not a theorem prerequisite. |
| J8 | `uniqueAlgebraicallySimpleRightRoot` | **CLOSED / PASS** | J0--J7, exact winding, parameter homotopy, nesting of the local disk in the global rectangle, conjugation symmetry, the multiplicity bridge, and the analytic implicit-function theorem give one real analytic, algebraically simple root in \((0.167,0.173)\) for every \(d\). |
| J9 | `explicitRightmostGap` | **CLOSED / PASS** | The Howard disk places every right-half-plane eigenvalue with real part \(>0.11\) inside the counted global rectangle.  Thus every other spectral point has real part at most \(0.11\), while \(\lambda_0>0.167\); the strict gap is \(>0.057>0.05=g_*\). |
| J10 | `kineticLeftRightOverlap` | **CLOSED / PASS (formal certificate; independence qualified)** | After J8 supplies the true root, the analytic overlap identity and the full auxiliary rectangle certificate give normalized overlap \(>0.585343766\).  A different centre-Lipschitz range proof on the shared 841-point grid gives \(>0.585009444>1/2\) and rechecks all 128 primary cells. |
| J11 | `fixedContinuumPhaseAnchor` | **CLOSED / PASS (formal certificate; independence qualified)** | The fixed bounded functional is \(\mathfrak a(h)=(L^{-1}h)(0)\).  The primary rectangle certificate gives \(\lvert M_{12}\rvert>1.841548895\); the independent centre-Lipschitz proof gives \(>1.841475104\).  J8 turns the auxiliary-rectangle statement into nonvanishing along the branch. |
| J12 | `finiteGalerkinBranch` | **FINITE DIAGNOSTIC ONLY — NO PROOF WEIGHT** | Cutoff sweeps may select contours and compare decimals.  In particular, the apparent weaker unstable conjugate pair near real part \(0.04\) remains a finite diagnostic.  It neither contradicts nor strengthens the theorem, whose uniqueness region is \(\operatorname{Re}\lambda>0.11\). |
| J13 | `uniformRankOneViscousBranch` | **OPEN** | Later R0.73K contract; no viscous persistence theorem is supplied here. |
| J14 | `matchingSelectedGainAction` | **OPEN** | Requires the later viscous and nonselfadjoint adiabatic estimates. |
| J15 | `transverseThreeDimensionalClosure` | **OPEN** | Requires nonzero transverse modes and nonlinear triad/vortex-stretching estimates. |
| J16 | `finiteTimeSingularity` | **OPEN** | No singularity mechanism has been proved in this planar linear problem. |
| J17 | `Clay` | **OPEN** | There is no global-regularity proof and no finite-time singularity construction for three-dimensional Navier--Stokes. |

## Evidence snapshot

The detailed cross-check is recorded in `research/r073j_adversarial_audit.md`.
The decisive audit-time hashes are:

| Artifact | SHA-256 |
|---|---|
| `research/r073j_continuum_branch_theorem.md` | `3f74be5cb9a217cb0559a85593767ec060698cba29d7db538f1ebcc8f53e297d` |
| `research/r073j_analytic_proof.md` | `81061d6f77e97fca33dafa0643820ab3860ae02b4042fe742eac1d91f1f108f0` |
| `research/r073j_analytic_audit.md` | `f134d4a828ed0f91c62899a41e9640b8e5ed211f375a4a92913e76a1f537de5e` |
| `research/r073j_overlap_analytic_proof.md` | `89c94e9d3ab9cd892f4f20ff8d2a3932b3f5fef6e82135ea2e64f39148c42f02` |
| `experiments/r073j/contour_certificate.json` | `60c770beaf0dc9a3da99ba6ab7bff234b506aa7d8bc72a0aad7b55471b571a38` |
| `experiments/r073j/independent_validation.json` | `203b7af48933cdb49c0a0b59751c0b0435cf26ae48ea01e08f203900ad554d57` |
| `experiments/r073j/overlap_certificate.json` | `12e1505cacb807d83a611b96d5b928bd4302c9faef16030566d3e178234180ab` |
| `experiments/r073j/independent_overlap_validation.json` | `a5f8e3267afbe2566ff260a064b1edcc889e37891fdbaad8212b05110404b7e0` |
| `experiments/r073j/natural_box_validation.json` | `2d92b6055ba847ffeda2a36a11d7c294df6d65925fd5e7dd00ec0cf6f7645c9a` |
| `experiments/r073j/natural_box_refinement.json` | `3ef584616bf0efc539ff20c1c734c057ac7b90874cd9a00ee25da2539a3679ab` |
| `experiments/r073j/natural_box_refinement_deep.json` | `269d0b3860d7961c73f262d91ee48d4ef24219f0e34f0f775b21c437f609782f` |

## Numerical-independence qualification

The two formal primary certificates are complete, parameter-uniform proof
inputs.  Their independent post-processing audits use different DCT and
range implementations, validate source ledgers and complete covers, and
recompute the decisive margins and winding numbers.  Both audits nevertheless
share the primary Arb/Acb raw ODE grids.  They can expose post-processing,
coverage, provenance, homotopy, and winding errors, but a common defect in raw
ODE integration or node labeling could survive both routes.  The passing
83-box direct ODE audit below checks selected locations with another kernel,
but it does not eliminate common-mode risk on the untested contour boxes.

The separate natural-parameter-box contour run tests part of that shared
layer with a new interval Taylor integrator.  At the frozen initial widths,
76 of 83 selected boxes passed and seven were Evans-wrapping-inconclusive;
all seven retained positive Rayleigh-denominator and Picard-tube margins.  A
complete depth-two dyadic refinement covered each of those seven boxes.  It
resolved all 16 leaves of `HASH-00-G-left-05-d3-s7`, but the other six parent
boxes retained 96 inconclusive leaves.  A preserved adaptive deep refinement
then split every one of those leaves until depth five.  Its final 2,896
adaptive leaves all passed, so all seven original parents and all 83 selected
natural boxes are now covered by direct passing enclosures.  The minimum final
Evans lower bound is \(0.007149506836327955\); the combined denominator and
tube lower bounds remain positive.  The initial and shallow inconclusive
records were enclosure-width failures, not detected Evans zeros or
counterexamples.  This direct ODE corroboration still covers only 83 selected
boxes.  It does not cover either contour and was never a prerequisite of
J5--J7.

The independent overlap audit also records three future natural
\((d,\lambda)\) boxes for a separate direct ODE recomputation.  That plan has
not been executed.  It is therefore incorrect to describe J10--J11 as backed
by two fully independent ODE calculations.

## Certificate and release rules

The accepted contour range is direct outward-rounded interval Clenshaw on a
complete dyadic cover.  The accepted overlap range is midpoint Bernstein with
direct coefficient-residual inflation; the independent overlap route uses a
cell-centre Lipschitz bound based on \(|T_n'|\le n^2\).  The two earlier
wrapping-prone range attempts remain in `failure_ledger.json`; neither is
silently reclassified as a spectral zero or a physical nonpositive energy.

Closing J0--J11 does not by itself release R0.73J.  The formal figure inventory,
synchronized HTML/PDF, cumulative recap, literature and bilingual assets,
release manifest, homepage counters/routes, and publication tests must all be
verified in one release cycle.  That complete publication check has not been
established by this audit.  Until it is, the public endpoint remains R0.73I.
