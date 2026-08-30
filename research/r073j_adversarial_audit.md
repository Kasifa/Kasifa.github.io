# R0.73J adversarial evidence audit

**Audit date:** 2026-08-30  
**Decision:** PASS for the bounded computer-assisted spectral-branch theorem;
the shared-raw-grid limitation remains explicit  
**Release decision:** NOT READY; this is not a publication-gate approval  
**Scope:** J0--J12 on \(0\le d\le1/450\) for
\((\beta,\xi,\gamma)=(0,0,1/2)\)

## 1. What I checked

I read the assembled theorem, both analytic proof notes, the independent
analytic audit, both formal certificates, both independent numerical
validations, the initial natural-box run, its complete depth-two refinement,
its passing adaptive deep refinement, and the rejected-method ledger.  I
recomputed the file hashes below and
compared every current source-ledger entry with the corresponding workspace
file.  I also checked that the overlap certificate names the exact current
contour certificate as its prerequisite.

This is an evidence-chain audit.  It does not rerun the 21,632-point contour
grid or the 841-point overlap grid.  No frozen proof, certificate, checkpoint,
configuration, or grid file was edited in this audit.

## 2. Audit-time snapshot

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `research/r073j_continuum_branch_theorem.md` | 10,123 | `3f74be5cb9a217cb0559a85593767ec060698cba29d7db538f1ebcc8f53e297d` |
| `research/r073j_analytic_proof.md` | 19,204 | `81061d6f77e97fca33dafa0643820ab3860ae02b4042fe742eac1d91f1f108f0` |
| `research/r073j_analytic_audit.md` | 23,493 | `f134d4a828ed0f91c62899a41e9640b8e5ed211f375a4a92913e76a1f537de5e` |
| `research/r073j_overlap_analytic_proof.md` | 17,037 | `89c94e9d3ab9cd892f4f20ff8d2a3932b3f5fef6e82135ea2e64f39148c42f02` |
| `experiments/r073j/contour_certificate.json` | 8,025,975 | `60c770beaf0dc9a3da99ba6ab7bff234b506aa7d8bc72a0aad7b55471b571a38` |
| `experiments/r073j/contour_grid_checkpoint.json` | 16,367,233 | `f706eecf8318a72954ca5582dabd58cd56f200cec6f67aeeb4eb80f9c2fc3df9` |
| `experiments/r073j/config.json` | 607 | `168051f8915fda82e76037707e6c7f6a00f8ad31cd55697a5041e35bab4dd8c5` |
| `experiments/r073j/independent_validate.py` | 82,994 | `0fa6d54748746dadf13119903fa65a641a86f490077cb7a05b8c76f3a10ca7d0` |
| `experiments/r073j/independent_validation.json` | 51,672 | `203b7af48933cdb49c0a0b59751c0b0435cf26ae48ea01e08f203900ad554d57` |
| `experiments/r073j/overlap_certificate.json` | 167,433 | `12e1505cacb807d83a611b96d5b928bd4302c9faef16030566d3e178234180ab` |
| `experiments/r073j/overlap_grid_checkpoint.json` | 1,140,779 | `9e1d86f83a157b59386b8d7e36aa1b72a1a44af492ddf2d5ee80b8756caff3a8` |
| `experiments/r073j/overlap_config.json` | 362 | `14e8b1a58edab1a9affe741b0a196e05a0f3ba18701410cb679510f17f0ba927` |
| `experiments/r073j/independent_validate_overlap.py` | 63,741 | `30842ffbc4a5c343af38c01c7d41170531d75d94aae2188efd0ec40f1feb38e4` |
| `experiments/r073j/independent_overlap_validation.json` | 474,195 | `a5f8e3267afbe2566ff260a064b1edcc889e37891fdbaad8212b05110404b7e0` |
| `experiments/r073j/natural_box_validation.json` | 176,563 | `2d92b6055ba847ffeda2a36a11d7c294df6d65925fd5e7dd00ec0cf6f7645c9a` |
| `experiments/r073j/independent_natural_box_validate.py` | 40,216 | `de1bd217204681af133a3f7c0a1441d33267bb07104093980edde9b3fd959dad` |
| `experiments/r073j/natural_box_refinement.json` | 385,385 | `3ef584616bf0efc539ff20c1c734c057ac7b90874cd9a00ee25da2539a3679ab` |
| `experiments/r073j/independent_natural_box_refine.py` | 31,422 | `635e3b0aa4b3eac5a938fa7a645759a8d81b8f208c27c3963b0fd17e5e75c401` |
| `experiments/r073j/natural_box_refinement_deep.json` | 9,883,044 | `269d0b3860d7961c73f262d91ee48d4ef24219f0e34f0f775b21c437f609782f` |
| `experiments/r073j/independent_natural_box_refine_deep.py` | 38,631 | `9231aa0aecfd635fa64cb3574315dd02e0af07924cacc9f85594cfb26e633ad2` |
| `experiments/r073j/natural_box_refinement_deep_progress.ndjson` | 4,534,691 | `93f81060f5e066a1273f380aa542a059280894169f66ac7541ee4d36aad354db` |
| `experiments/r073j/natural_box_refinement_deep_resources.ndjson` | 13,620 | `7a331132e795e04509d956c28059f4870018000dcdde663cc32baee72cdfb1e9` |
| `experiments/r073j/failure_ledger.json` | 1,795 | `021d3a17cf40cf71e412090733658106256b0d3642af9b66ebb20d2209ebabd2` |

The contour certificate has source digest
`736ebbcdad0f0897a1be100352aec7163f0483a1f323e6a4f1466dd43d7353f8`;
its raw checkpoint has source digest
`f95fdac894a7ded9042c58950ea0f79603a5ef69341a01c91a36edc093de1729`.
The overlap certificate has source digest
`c50750d1253ee2e82aa9e6fe719f638811be034c9f1e992a528af528f0f191cc`;
its raw checkpoint has source digest
`2d08620d7e3c1f1067b34b7577e1a1e7a405d4bc47618c69020714b43a1c28cb`.

The overlap prerequisite records the contour artifact at exactly
`60c770be...b571a38` with source digest `736ebbcd...353f8` and all four
required contour decisions true.  The independent contour validation records
the current contour checkpoint, configuration, primary certificate, and
auditor hashes exactly.  The independent overlap validation records the
current 29 by 29 checkpoint, configuration, proof/source ledger, primary
analysis source, and auditor hash.  Every ledger hash I recomputed matched.

## 3. Claim-by-claim closure

| Claim | Decision | Reason |
|---|---|---|
| J0 | **PASS / CLOSED** | Essential spectrum, compact perturbation, right-half-plane discreteness, and kinetic/ordinary Jordan-chain equality are proved and independently audited. |
| J1 | **PASS / CLOSED** | The Rayleigh denominator is nonzero in the open right half-plane and the parameter-dependent Evans construction is analytic on the certified domains. |
| J2 | **PASS / CLOSED** | Analytic equivalences preserve partial multiplicities from the kinetic operator pencil to \(M-I\), so Evans zero order equals operator algebraic multiplicity. |
| J3 | **PASS / CLOSED** | The periodic Howard identity gives the uniform disk without numerical input. |
| J4 | **PASS / CLOSED** | The local base winding is one; symmetry forces its only zero to be real and the local disk is strictly positive. |
| J5 | **PASS / CLOSED** | Both primary and independent post-processing obtain exact positive-orientation global winding one. |
| J6 | **PASS / CLOSED, shared-grid qualification** | Both complete global range proofs have large positive margins. |
| J7 | **PASS / CLOSED, shared-grid qualification** | Both complete local range proofs have positive margins. |
| J8 | **PASS / CLOSED** | Counts, nesting, symmetry, multiplicity, and analytic continuation give one real analytic algebraically simple branch. |
| J9 | **PASS / CLOSED** | The outer analytic disk and global count imply the strict \(0.057\) gap, hence the conservative \(g_*=0.05\). |
| J10 | **PASS / CLOSED, shared-grid qualification** | J8 plus the analytic adjoint/pairing identity and the complete overlap rectangle prove the normalized lower bound. |
| J11 | **PASS / CLOSED, shared-grid qualification** | J8 plus the bounded point-evaluation functional and the complete anchor rectangle prove uniform nonvanishing. |
| J12 | **FINITE DIAGNOSTIC ONLY** | No cutoff root or apparent finite gap contributes to J0--J11. |

## 4. Decisive numerical cross-checks

| Quantity | Primary certificate | Independent post-processing | Audit reading |
|---|---:|---:|---|
| contour panels / raw ODE nodes | 64 / 21,632 | all 64 / all 21,632 validated | same frozen raw grid |
| global complete-cover cells | 7,168 | 7,168 | 56 panels, exact normalized area four per panel |
| local complete-cover cells | 4,096 | 4,096 | eight panels, exact normalized area four per panel |
| global boundary \(\inf\lvert E\rvert\) | \(>5.499484465806685\) | \(>5.497398601851467\) | both comfortably nonzero |
| local boundary \(\inf\lvert E\rvert\) | \(>0.164355178305153\) | \(>0.164339779846808\) | both comfortably nonzero |
| global base-homotopy lower bound | \(>5.594985687145022\) | \(>5.642610414201621\) | curve-to-polygon homotopy separated from zero |
| local base-homotopy lower bound | \(>0.164355201467909\) | \(>0.170178214674438\) | curve-to-polygon homotopy separated from zero |
| exact global/local winding | \(1/1\) | \(1/1\) | orientation and integer count agree |
| contour raw denominator lower | \(>0.218192850727718\) | same raw audit | not an independent ODE recomputation |
| contour raw Picard slack | \(>2.464473798851068\times10^{-10}\) | same raw audit | positive; maximum inflation attempt four |
| overlap grid | 841 nodes, \(29\times29\) | all 841 nodes and 3,364 output reconstructions | same frozen raw grid |
| overlap complete-cover cells | 128 | 128 | exact normalized area four |
| anchor \(\lvert M_{12}\rvert\) lower | \(>1.841548895632704\) | \(>1.841475104765145\) | uniform nonzero anchor |
| right energy lower | \(>86.71852876576329\) | \(>86.70795698498808\) | strictly positive |
| left energy lower | \(>141.3215874849568\) | \(>141.1927698605030\) | strictly positive |
| normalized overlap lower | \(>0.585343766721940\) | \(>0.585009444869089\) | both exceed \(1/2\) |
| independent strict margin over \(1/2\) | — | \(>0.085009444869089\) | decisive J10 margin |
| overlap raw denominator lower | \(>0.330796048110939\) | same raw audit | not an independent ODE recomputation |
| overlap raw Picard slack | \(>0.000616325805586756\) | same raw audit | positive; no inflation required |

The theorem's displayed refinement \(>0.5853\) comes from the primary
midpoint-Bernstein certificate.  The independent centre-Lipschitz route is
slightly wider and independently proves the release threshold \(>1/2\), not
the decimal \(>0.5853\).  It also replays all 128 primary boxes and confirms
that their serialized boxes and margins contain the replay.

## 5. Natural-box result

The initial independent raw-ODE run used 120 decimal digits, Taylor order 14,
2,048 global or 1,024 local steps, and 16 workers.  Its schema status is
`failed` because the frozen acceptance rule required all 83 boxes to pass.
The actual split was 76 pass and seven Evans-wrapping-inconclusive: two global
and five local.  Their exact identifiers were:

1. `HASH-00-G-left-05-d3-s7`
2. `HASH-01-G-left-06-d0-s27`
3. `HASH-03-L-circle-04-d5-s49`
4. `HASH-04-L-circle-00-d1-s18`
5. `HASH-09-L-circle-03-d4-s63`
6. `HASH-12-L-circle-06-d2-s31`
7. `HASH-25-L-circle-04-d6-s35`

Every one of the seven had a positive Rayleigh denominator and positive
Picard-tube slack.  Its final interval image of \(E\), not a computed point
value, contained zero.

The refinement then made a complete exact \(2\times2\) dyadic split at level
one and refined every inconclusive child once more.  All 28 first-level boxes
remained wrapping-inconclusive, so the final cover contained 112 level-two
leaves.  Sixteen leaves passed and 96 remained inconclusive.  All 16 leaves
of `HASH-00-G-left-05-d3-s7` passed, so one of the original seven parents was
resolved; the other six were not.  The minimum passing-leaf Evans lower bound
was \(2.242243436038458\).  Across all 140 refinement integrations, the
minimum Rayleigh-denominator lower bound was \(0.219096410720085\), the
minimum Picard-tube slack was \(1.285258619748844\times10^{-7}\), and there
was no denominator or tube failure.

The deep run preserved that shallow record and adaptively refined all 96
remaining leaves.  At depth three, 64 of 384 boxes passed; at depth four, 768
of 1,280 passed; at depth five, all 2,048 remaining boxes passed, so depth six
was not needed.  The resulting 2,896 adaptive leaves form an exact passing
cover of all seven original parents.  The final inconclusive-leaf count is
zero, and all original 83 selected natural boxes are now covered either
directly or by passing refined leaves.  The minimum final Evans lower bound is
\(0.007149506836327955\).  The combined minimum Rayleigh-denominator lower
bound is \(0.219096410720994754\), and the combined minimum Picard-tube slack
is \(0.000357397880846495\).

The correct final conclusion is **PASS on the 83 selected natural boxes**,
not a second complete contour proof.  The initial fail-closed and shallow
inconclusive artifacts remain part of the record and show why refinement was
needed.  The adaptive leaves do not cover either full contour.  The deep run
therefore strengthens raw-ODE corroboration without replacing the uniform
Clenshaw certificate used by J5--J7.

The overlap audit contains a design for three direct natural
\((d,\lambda)\) boxes, but no such direct overlap ODE run has been executed.

## 6. Strongest objections and answers

### Objection 1: both “independent” numerical audits reuse the primary raw grid

**Answer.** This objection is correct and remains material.  The contour
audit independently reconstructs coefficients, reverses the Clenshaw axis
order, proves complete dyadic ranges, and recomputes homotopies and exact
winding.  The overlap audit uses a direct tensor DCT, a different
cell-centre/derivative Lipschitz range, and a full replay of primary
midpoint-Bernstein boxes.  Neither regenerates its raw node values.  A common
ODE-integrator or node-labeling defect could survive.  The evidence must be
described as a formal primary proof with independent shared-grid
post-processing, not as two fully independent ODE proofs.  The passing
83-box direct ODE audit tests selected locations with another kernel and
reduces this concern locally, but it does not cover the full contours.

### Objection 2: seven natural boxes initially failed

**Answer.** The initial file's fail-closed status is real and must remain in
the record.  Its seven failures were interval wrapping after positive
denominator and tube checks.  Complete depth-two refinement resolved one
parent and left six parents with 96 inconclusive leaves.  The subsequent
adaptive full-cover refinement resolved all 96 by depth five, with a positive
final Evans lower bound and positive combined denominator/tube margins.  Thus
the final direct ODE decision passes for all 83 selected boxes.  Because those
boxes remain a selected spot audit rather than a complete contour cover, this
corroboration does not replace the passed uniform certificate.

### Objection 3: two range methods failed before replacements passed

**Answer.** The failure ledger records both cases.  Full-ball
Chebyshev-to-power-to-Bernstein conversion wrapped on the contour data, and
direct interval Clenshaw lost a shared-variable dependency for an overlap
energy.  The raw grids were preserved.  Replacement analyses have separate
source ledgers, complete covers, strict margins, and independent
post-processing replays.  These are rejected enclosure methods, not spectral
zeros or nonpositive physical energies.  The retained ledger prevents a
method change from being mistaken for a clean first attempt.

### Objection 4: a winding count could miss spectrum outside the rectangle

**Answer.** The numerical rectangle is not the only enclosure.  The analytic
Howard bound puts every right-half-plane eigenvalue inside
\(|\lambda|\le3\sqrt3/16<13/40\), which is strictly inside the rectangle's
top, bottom, and right sides.  Its left side is \(\operatorname{Re}\lambda=0.11\).
The essential spectrum lies on the imaginary axis.  Therefore every spectral
point with real part greater than \(0.11\) lies in the counted region.

### Objection 5: one Evans zero need not mean one simple operator eigenvalue

**Answer.** The analytic proof does not infer multiplicity from a numerical
kernel dimension.  It proves kinetic/ordinary Jordan-chain equivalence, an
exact analytic operator-pencil factorization, and analytic equivalence of the
periodic BVP pencil with \(M-I\).  Partial multiplicities and hence the Riesz
algebraic multiplicity are preserved.  The independent analytic audit passes
this bridge.  Winding one therefore gives algebraic multiplicity one.

### Objection 6: the local and global counts might refer to different roots

**Answer.** The local disk is contained in the global rectangle, and each has
zero count one for every parameter.  The local zero must therefore be the
global zero.  Both domains are invariant under conjugation.  A nonreal zero
would bring a distinct conjugate and force count at least two, so the root is
real.  Analytic simplicity then supplies local analytic continuation, and
uniqueness glues the branch across the closed parameter interval.

### Objection 7: finite matrices show other unstable roots

**Answer.** The frozen problem statement already records an apparent weaker
conjugate pair near real part \(0.04\).  J12 assigns it no continuum proof
weight.  It does not contradict the certified wording: the theorem says
“only spectral point with real part greater than \(0.11\),” not “only
unstable eigenvalue.”  No claim about the continuum existence, multiplicity,
or evolution of that weaker pair follows here.

### Objection 8: the overlap rectangle contains points that are not eigenvalues

**Answer.** Correct.  Away from an Evans zero, its four interval outputs are
auxiliary holomorphic quantities, not eigenvector data.  The overlap analytic
proof states this conditional structure.  J8 places the true real root in the
entire certified rectangle for every \(d\); only on that root are the right
solution, kinetic adjoint, numerator, and energies interpreted as eigenvector
quantities.  Positivity of both energy lower bounds and nonvanishing of the
numerator then give the normalized overlap.

### Objection 9: the fixed anchor may be a coordinate-dependent normalization

**Answer.** The functional itself is fixed:
\(\mathfrak a(h)=(L^{-1}h)(0)\).  Since \(L^{-1}:X\to H^1_{\rm per}\) and
one-dimensional point evaluation is bounded on \(H^1\), it is a bounded
functional on the kinetic space.  On the selected solution it equals
\(M_{12}\), whose uniform lower bound is positive.  Rescaling changes its
value but not nonvanishing; the normalized overlap is rescaling invariant.

### Objection 10: this advances the Clay problem

**Answer.** It does not close a Clay-level step.  The result concerns the
discrete spectrum of one planar periodic frozen Euler/Rayleigh linearization
over a short parameter interval.  It proves neither viscous branch
persistence nor a nonselfadjoint adiabatic remainder, transverse
three-dimensional nonlinear control, global regularity, or finite-time
singularity.  Other weak unstable roots are not continuum-certified here.

### Objection 11: mathematical closure is being confused with publication

**Answer.** J0--J11 can be closed as a bounded computer-assisted theorem
while R0.73J remains unreleased.  This audit does not verify the full formal
figure inventory, synchronized HTML/PDF, cumulative recap, release manifest,
homepage counters and routes, or publication tests.  Presence of some source
or figure files is not a release PASS.  The public endpoint remains R0.73I
until the complete publication inventory is checked together.

## 7. Final decision

I find the assembled implication for J0--J11 internally complete at the
stated mathematical scope.  The strongest certified conclusions are a unique
real analytic, algebraically simple spectral branch in
\((0.167,0.173)\), no other spectral point with real part above \(0.11\), a
strict real-part gap greater than \(0.057\), normalized kinetic overlap above
\(1/2\), and a fixed nonzero phase anchor.

The numerical evidence is not two independent ODE proofs.  It is a primary
validated computation, two independent shared-grid post-processing audits,
and a passing direct raw-ODE corroboration on 83 selected natural boxes.
Those boxes do not form a complete contour cover.
J12 remains finite diagnostic only.  J13--J17 remain open.  The publication
gate remains incomplete.
