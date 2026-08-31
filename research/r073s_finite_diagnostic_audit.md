# R0.73S finite formula certificate and formal-figure audit

**Audit date:** 2026-08-31

**Status:** **FINAL SEAL PASS — NOT CLAY**

**Scope:** the quadratic-autocorrelation upper certificate, the fixed-quartic
difference-support obstruction, the selected-shift and low-summary no-go
families, the matched R0.73R phase-pair transfer, and the associated 25-file
journal-figure package.

**Verdict:** the producer, independent reconstruction, structural validation,
source-commit bindings, checksums, vector/raster outputs, and visual QA pass.
Both exact packages bind their sources to immutable commit
`72e4c12760dc3b837dec328ee96a29736fe93c99`; their generated artifacts are
preserved in commit `4bb49ecc380e4b41d33e3102af4f47de016b5653`.
These packages certify finite identities and artifact identity only. They are
not a Navier--Stokes simulation, a continuum PDE certificate, a complexity
lower bound, or a global-regularity theorem.

## 1. Exact finite contract

For normalized Haar measure and a finite Fourier vector field, the package
checks

\[
 C(h)=\widehat{|f|^2}(h),\qquad
 Q=\sum_h|C(h)|^2=\|f\|_4^4,
\]

and the sufficient chain

\[
 \|f\|_6^6\le \|C\|_1Q
 \le Q\min\{M\|f\|_2^2,\sqrt{D_CQ}\}.
\]

It also checks the fixed-quartic spike family with
\(\Gamma=5/3\), \(D_C=4m-1\), and sextic concentration growing like
\(D_C^{1/2}\); the real divergence-free annular lift; the exact
\(311/323\) low-summary seed; its no-carry lacunary amplification; and the
matched Dirichlet/Rudin--Shapiro proxy formulas.

The real annular lift is independently enumerated. It has \(2m+2\) Fourier
modes, \(D_C=4m-1\), \(D_\Delta=10m-1\), support in
\(32m\le |k|<36m\), and zero convective nonlinearity. It is therefore a
sharpness witness for the certificate, not a dangerous flow.

## 2. Independent certificate paths

`research/certificates/r073s` contains 19 files: nine source files and ten
generated files. Its source table contains 43 rows spanning generic exact
fields, the bounded-quartic spike, matched phase pairs, the real annular lift,
and the lacunary no-go family.

The direct producer passes 226 checks. The independent validator passes 54
checks without importing or invoking the producer. The fail-closed structural
validator passes 289 checks. Thus the declared inventory is
`226 + 54 + 289 = 569` passing checks. The finite-record SHA-256 is
`e25f71da5a9e72ce7a44300d4b965d8a4389c7d7d7b1502c11a0fc569c305718`.

The final manifest state is:

```text
status=sealed
allPrerequisiteChecksPass=true
sourceCommitAssigned=true
sourceCommit=72e4c12760dc3b837dec328ee96a29736fe93c99
finalSeal=true
```

Selected certificate hashes:

| File | SHA-256 |
| --- | --- |
| `source-data.csv` | `640beee60959e23e2b9877e7b0ae8f8790dcf2c7b37b162746da64a520f1680c` |
| `manifest.json` | `ac85441e327d2c8c839473e96ce9fe88ef410eddc9766bcfcd6e720f01ae55f6` |
| `certificate.json` | `d4e7ae0d5cf479d1a607ca2d67cc2e735f4ef9551f5d28736e1860940c1df3c9` |
| `validation.json` | `b3a026ea1dc0fdfac42e5f5f5354d08dea2caa1d6864b9cd0e119d866fcda3c4` |
| `independent_validation.json` | `7aced7487e21a353d6af65fc3d24d9e586a7694674244d21809ba03b4dcc6eb5` |
| `diagnostic.json` | `8bd9176b7f2696c2b3ef9c99a3037e902777aa3012b5b02b9d0e4d5c60ba7d7e` |

## 3. Commit ledger

The seal separates immutable sources from generated artifacts to avoid a
self-referential commit claim.

| Role | Commit | Audited content |
| --- | --- | --- |
| analytic and package sources | `72e4c12760dc3b837dec328ee96a29736fe93c99` | certificate and figure sources plus the analytic R0.73S source set |
| generated exact artifacts | `4bb49ecc380e4b41d33e3102af4f47de016b5653` | final-sealed certificate and formal-figure packages |

The final certificate sealer and figure validator re-read their declared
source blobs from the source commit. The artifact commit contains the
byte-identical generated files reported here.

## 4. Formal figure package

`research/figures/r073s/fig-r073s-quadratic-certificate` contains 25 files:
ten source files and fifteen generated files. The final validator passes
236/236 checks and reconstructs all 179 source-data rows: 18 sharpness rows,
32 matched-pair rows, and 129 no-go rows.

The panels show:

1. the sharp \(D_C^{1/2}\) growth at fixed quartic concentration;
2. the exact R0.73R matched-pair values and the quadratic proxy;
3. exact low-summary non-identifiability under no-carry amplification.

The final-size color surface, grayscale surface, and independently rasterized
PDF surface were visually inspected. The master outputs are a one-page
178 mm by 96 mm vector PDF, a vector SVG, and a 600 dpi PNG at
4,204 by 2,267 pixels. The PDF contains no raster image objects and the SVG
contains no embedded image element.

Master-output hashes:

| Output | SHA-256 |
| --- | --- |
| `figure.pdf` | `f236997829207c4c5b8b948be3a46b8871de4c251dadda780f530b9590d07fda` |
| `figure.svg` | `168e5063e9c75d7d44231f66fa6ffd53b74c8e488ca2240c03fb412857872c35` |
| `figure.png` | `9879ebb3c4d74bffa3aa2c1180ee416402e8453dffba5b9a1250289cc8f9deae` |
| `manifest.json` | `cae1d77095554beda5c3bffee77f1551112d638fd3c50c02a010dd50470f2e97` |
| `validation.json` | `f3901c2e8b0abbc2a6646d7fd1b7a1aa8e2a0522e5b026f8ce81630c56eca1a6` |
| `results.json` | `ee83109cc01c926dcc756dd13535c3f6d2b32c8d9659ba6654b34634ed41cd9c` |

## 5. Evidence boundary

The finite packages verify exact coefficient data, autocorrelation-support
counts, even-moment identities, no-carry factorization, theoretical exponent
bookkeeping, output identity, physical figure dimensions, and rendering QA.
The continuum Littlewood--Paley and heat-semigroup estimates remain supported
by the separate analytic proof and source audit.

The certificate performs no continuous heat-flow quadrature, interval
arithmetic, or nonlinear PDE simulation. It does not certify necessity,
instability, finite-time singularity, arbitrary-data regularity, or a
universal runtime lower bound. Failure of a sufficient entrance test is not a
dynamical diagnosis. The displayed annular witnesses have zero convection
and globally smooth heat evolution.

All finite calculations and figure rendering ran locally. GPU and DGX were
not used. Ordinary bilingual release translation will be performed directly
on the local workstation and will never be routed through DGX. No novelty or
priority claim follows from these finite checks.

## 6. Machine ledger

```text
formulaDiagnosticValidation=PASS
formulaDiagnosticPackage=CLOSED
formulaDiagnosticPrimaryChecks=226
formulaDiagnosticIndependentChecks=54
formulaDiagnosticStructuralChecks=289
formulaDiagnosticRows=43
sourceCommitAssigned=TRUE
sourceCommit=72e4c12760dc3b837dec328ee96a29736fe93c99
generatedArtifactCommit=4bb49ecc380e4b41d33e3102af4f47de016b5653
finalSeal=TRUE
formalFigurePackage=PASS
formalFigureChecks=236
formalFigureRows=179
dgxUsed=FALSE
ordinaryTranslationPath=LOCAL_DIRECT_NO_DGX
finiteFormulaDiagnosticIsNavierStokesSimulation=FALSE
finiteFormulaDiagnosticCertifiesContinuumPdeProof=FALSE
universalRuntimeLowerBound=NOT_PROVED
clayConclusion=OPEN
noveltyOrPriorityClaim=FORBIDDEN
NOT CLAY
```
