# R0.73T finite diagnostic certificate and formal-figure audit

**Audit date:** 2026-08-31

**Status:** **FINAL SEAL PASS — NOT CLAY**

**Scope:** the exact dynamic-autocorrelation no-go witnesses, including the
six-mode pressure pairing, heat-weighted grouping, ordinary shear, rotating
shear, dilation laws, and the associated 25-file journal-figure package.

**Verdict:** the exact producer, canonical check-only reconstruction,
fail-closed source seal, source-commit bindings, checksums, figure validator,
vector/raster outputs, and visual QA pass. Both packages bind their immutable
sources to commit `05c55d21f060a17a0a4db04c12e89e7271b03d30`; the
scientific artifacts are preserved in commit
`29d01625731d1c611f927c2852dbddf05967c6cb`. A metadata-only figure reseal at
`b17c45013cc9a3f6f09efa146bcbc2ef8ab043f9` adds the wall-time and bracketed
same-host runtime record required by the publication archive. It changes only
`environment.json`, the source figure manifest, and `SHA256SUMS`; all exact
data, validation, PDF, SVG, and PNG bytes remain unchanged. These packages certify exact
finite Fourier identities, instantaneous formulas, finite witnesses, and
artifact identity only. They are not a Navier--Stokes simulation, a continuum
PDE certificate, a new regularity criterion, a singularity construction, or
a solution of the Clay Millennium problem.

## 1. Exact finite contract

For normalized Haar probability measure on \(\mathbb T^3\), the certificate
reconstructs

\[
 C_h=\widehat{|u|^2}(h),\qquad
 Q=\sum_h|C_h|^2=\|u\|_4^4,
\]

and checks every declared coefficient and instantaneous derivative with exact
rational arithmetic.

For the six-mode field

\[
 u=(6\sin x_2-4\sin(x_1+x_2),
    4\sin x_1+4\sin(x_1+x_2),0),
\]

the package independently reconstructs the scalar autocorrelation by shifted
autocorrelation and product convolution, reconstructs pressure from the full
velocity tensor, and certifies

\[
 \mathcal E=42,\quad Q=2918,\quad A=164,\quad D_C=15,
\]

\[
 X^2=4296,\quad Y=1986,\quad
 \mathcal N_4=-384.
\]

For \(u_L(x)=u(Lx)\), it checks

\[
 Q'(u_L;0)=-16536\nu L^2-384L,\qquad
 Q'(-u_L;0)=-16536\nu L^2+384L.
\]

The pair has identical complete scalar autocorrelation, identical
\(u_L\otimes u_L\), and identical pressure; its signed derivative difference
isolates velocity phase in the pressure pairing. The separate pressure formula
still shows why scalar \(C\), which retains only the trace of the quadratic
velocity tensor, cannot reconstruct the pressure term in general.

The heat-weighted calculation is grouped exactly by \(m=|h|^2\), with no
floating approximation to an exponential. It certifies

\[
 Q_\tau'(u)-Q_\tau'(-u)=-768e^{-8\tau},
\]

and after dilation, \(-768L e^{-8\tau L^2}\). The ordinary shear checks the
pure viscous law, while the rotating shears
\(v_N=(0,\cos Nx_1,\sin Nx_1)\) have the same complete scalar
autocorrelation \(C=\delta_0\) for every \(N\), but

\[
 \dot C_0(0)=-2\nu N^2,\qquad Q'(0)=-4\nu N^2.
\]

This is an exact information-loss witness for autonomous evolution of the
unweighted scalar autocorrelation, not a dangerous-flow or blow-up witness.

## 2. Exact certificate and final seal

`research/certificates/r073t` contains nine files: six source files and three
generated files. The fixed checklist contains 55 exact expectations, including
the complete six-mode velocity, pressure, and autocorrelation tables rather
than aggregate totals alone.

The producer passes 55/55 checks. Check-only mode recomputes the complete
canonical object and requires byte identity with `results.json`. The final
sealer re-reads all six declared source blobs from the immutable source commit
and fails closed on an absent, stale, abbreviated, non-commit, or byte-different
binding.

The final manifest state is:

```text
status=sealed
allPrerequisiteChecksPass=true
exactChecks=55/55
sourceCommitAssigned=true
sourceCommit=05c55d21f060a17a0a4db04c12e89e7271b03d30
finalSeal=true
```

Selected certificate hashes:

| File | SHA-256 |
| --- | --- |
| `results.json` | `3a673f127d11fa63516182855ee0fd1dfecce98c06bc314c662ebd4fbfe41163` |
| `manifest.json` | `3ca0c0d6dad5bd88faad032e0dd93f1b74fd6338d99b0bb05f2454fac40e6134` |

## 3. Commit ledger

The seal separates immutable sources from generated artifacts so that neither
package makes a self-referential commit claim.

| Role | Commit | Audited content |
| --- | --- | --- |
| analytic and package sources | `05c55d21f060a17a0a4db04c12e89e7271b03d30` | exact-certificate sources, formal-figure sources, and the bound analytic proof |
| scientific artifacts | `29d01625731d1c611f927c2852dbddf05967c6cb` | final-sealed exact certificate plus the validated figure data, validation, PDF, SVG, and PNG |
| figure metadata reseal | `b17c45013cc9a3f6f09efa146bcbc2ef8ab043f9` | same-host runtime metadata backfill and the resulting figure `manifest.json` / `SHA256SUMS`; no mathematical or visual artifact changed |

The exact sealer and figure validator re-read their declared sources from the
source commit. The generated-artifact commit contains the byte-identical files
reported here.

## 4. Formal figure package

`research/figures/r073t/fig-r073t-dynamic-autocorrelation` contains 25 files:
ten source files, eleven raw outputs, and four package-metadata files. The
validator passes 106/106 checks and reconstructs all 28 exact source rows:
four analytic rows, eight carrier-loss rows, and sixteen signed-pair rows.

The panels show:

1. the one-sided dynamic inequality derived from the exact quartic balance,
   periodic pressure estimate, and the R0.73S static certificate;
2. carrier-scale information loss for rotating shears with identical complete
   scalar autocorrelation;
3. the viscous-centered signed derivative pair for \(u_L\) and \(-u_L\) at
   \(t=0\).

The final-size color surface, exact grayscale surface, and independently
rasterized PDF surface were visually inspected and passed. Equations, labels,
legends, and panel boundaries do not clip; the signed series remain
distinguishable in grayscale. The master outputs are a one-page 178 mm by
100 mm PDF, an SVG, and a 600 dpi PNG at 4,204 by 2,362 pixels.

Master-output hashes:

| Output | SHA-256 |
| --- | --- |
| `figure.pdf` | `cb2c4a213d7bb798b0717905be5a38d62e769837f3845128b4c596945998be62` |
| `figure.svg` | `d5ada2c4dd716ec878b38474d7fdda267b7edfc8367e6653ea62126b1425d90f` |
| `figure.png` | `9dbaedbfbf6370ca88612913dfe94b216df7d71142bbce248fb21f7f8a8fb060` |
| original `manifest.json` at scientific-artifact commit | `29d34366e2715819e08f1c6f1dc77bff5fcb089a2e2c2e6ce33616825fccae1d` |
| current metadata-resealed `manifest.json` | `bfa5c468ecb43a287239fd5e368c66d0eefad6ffe09dff241e828e806279a10e` |
| current metadata-resealed `environment.json` | `259de2eebb7179336b41f060b57068319873cb03a0dce1324e1c95388e9bf50e` |
| `validation.json` | `f440eac3f16edb5be2f35bc63f0c4464467256516b2c76537239d5646effb95f` |

## 5. Evidence boundary

The finite certificate verifies exact Fourier coefficients, conjugate reality,
incompressibility, pressure convolution, scalar-autocorrelation reconstruction,
moment identities, instantaneous derivative formulas, dilation laws,
heat-weighted coefficient groupings, carrier-scale loss, source provenance,
and output identity. The formal figure additionally verifies exact source-row
reconstruction, dimensions, palette, raster/vector consistency, and rendering
QA.

The continuum one-sided estimate and its pressure bound remain supported by
the separate analytic proof and primary-source audit. The finite package does
not prove time-integrability of \(A(t)\), close an autonomous evolution for
\(C\), improve a known regularity criterion, integrate a generic nonlinear
solution, certify instability, produce a finite-time singularity, or establish
global regularity. A failure of scalar-autocorrelation closure is an
information-loss result, not evidence of blow-up.

Every exact-certificate calculation and every figure-production step ran
locally. The exact producer imports only the Python standard library, and all
mathematical pass/fail decisions use `fractions.Fraction`; it uses no floating
tolerance, network request, simulation, GPU, or DGX computation. Figure
rendering also used no network, GPU, or DGX. Ordinary translation is performed
directly on the local workstation and is never routed through DGX.

No novelty, priority, singularity, global-regularity, or Clay claim follows
from these finite checks.

## 6. Machine ledger

```text
finiteFormulaDiagnosticValidation=PASS
finiteFormulaDiagnosticPackage=CLOSED
finiteFormulaDiagnosticChecks=55
finiteFormulaDiagnosticRequiredChecks=55
finiteFormulaDiagnosticFiles=9
finiteFormulaDiagnosticSourceFiles=6
finiteFormulaDiagnosticGeneratedFiles=3
finiteFormulaDiagnosticResultsSha256=3a673f127d11fa63516182855ee0fd1dfecce98c06bc314c662ebd4fbfe41163
finiteFormulaDiagnosticManifestSha256=3ca0c0d6dad5bd88faad032e0dd93f1b74fd6338d99b0bb05f2454fac40e6134
sourceCommitAssigned=TRUE
sourceCommit=05c55d21f060a17a0a4db04c12e89e7271b03d30
scientificArtifactCommit=29d01625731d1c611f927c2852dbddf05967c6cb
figureMetadataResealCommit=b17c45013cc9a3f6f09efa146bcbc2ef8ab043f9
figureMetadataBackfill=SAME_HOST_BRACKETED_NOT_ORIGINAL_RUN_EMISSION
originalFormalFigureManifestSha256=29d34366e2715819e08f1c6f1dc77bff5fcb089a2e2c2e6ce33616825fccae1d
currentFormalFigureManifestSha256=bfa5c468ecb43a287239fd5e368c66d0eefad6ffe09dff241e828e806279a10e
finalSeal=TRUE
formalFigurePackage=PASS
formalFigureChecks=106
formalFigureRows=28
formalFigureFiles=25
formalFigureWidthMm=178
formalFigureHeightMm=100
formalFigurePngWidthPx=4204
formalFigurePngHeightPx=2362
formalFigureColorQa=PASS
formalFigureGrayscaleQa=PASS
formalFigurePdfQa=PASS
formalFigureClipping=FALSE
dgxUsed=FALSE
networkUsed=FALSE
navierStokesSimulationRun=FALSE
ordinaryTranslationPath=LOCAL_DIRECT_NO_DGX
finiteFormulaDiagnosticIsNavierStokesSimulation=FALSE
finiteFormulaDiagnosticCertifiesContinuumPdeProof=FALSE
regularityCriterionImproved=FALSE
singularityConstructed=FALSE
globalRegularityEstablished=FALSE
clayConclusion=OPEN
noveltyOrPriorityClaim=FORBIDDEN
NOT CLAY
```
