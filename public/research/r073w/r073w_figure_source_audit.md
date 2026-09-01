# R0.73W independent figure-source and claim-boundary audit

**Audit date:** 2026-09-01

**Figure ID:** `fig-r073w-signed-production`

**Ordinary translation path:** `LOCAL_DIRECT_NO_DGX`

**DGX used:** `false`

**Verdict:** PASS.  The formal figure source and raw artifacts are immutable,
the metadata package is sealed in the immediately following commit, all 49
figure checks pass, and the package is byte-identical to the sealed Git blobs.
This verdict certifies the rendering and its finite inputs.  It is not a
Navier--Stokes time simulation, a numerical PDE solution, a singularity
witness, a regularity theorem, or a Clay conclusion.

## 1. Immutable source chain

The figure has two consecutive commits:

| Layer | Commit | Independent result |
|---|---|---|
| ten source files plus eleven raw artifacts | `ac6293ac4d0c46c696d2ec8e29d3fb1350e341f1` | 21/21 current files equal their Git blobs and manifest hashes |
| four-file metadata package seal | `60b0e869bbaa3a0ace185bf450e067d79fcd79b3` | parent is exactly the source commit; all 25 package files equal the current package |

The four files added by the second commit are `manifest.json`,
`validation.json`, `qa-report.md`, and `SHA256SUMS`.  The manifest records

```text
figureSourceCommit=ac6293ac4d0c46c696d2ec8e29d3fb1350e341f1
figureSourceCommitAssigned=true
sealState=formal-figure-source-seal
requiresFigureSourceCommitFinalReseal=false
requiresParentFigureSourceCommitFinalReseal=false
```

All 24 records in `SHA256SUMS` verify.  The checksum file correctly excludes
itself.  Scoped Git status for the figure package is clean.

The source `README.md` describes the preseal-to-reseal procedure because it is
one of the immutable source blobs.  Current seal state is carried by the four
later metadata files and their package commit; the historical workflow prose
does not override those machine-readable records.

## 2. Exact certificate pins

The figure is bound to the R0.73W two-path certificate:

```text
certificateSourceCommit=b9f3b3943df1e2abf6abc2f51c1fb25d1f1e8440
certificatePackageCommit=68893eccd7f5b6047bf2b00c5262913e23fadbc3
primarySha256=0ce95b6e7175e841e265fdd10bb08ed978844c1ec22305811ade2f55547af912
independentSha256=6e8e7dc46874ad62b74bbda3c2aef460e07d1e9e221704451647147cc8f76774
commonCoreSha256=4c72251bde4bf12bb5cfe8c3c6b15c0e049dc440a2c41daa751eb0a5da9460f2
```

Read-only reruns of the sparse complex-Fourier producer and the independent
real-trigonometric producer passed.  Both report Fourier-support rank three,

\[
 {\langle\Pi_s\rangle\over A^3}
 ={1\over4}q^2(1-q^2),
 \qquad
 {\langle D_{ii,s}\rangle\over A^2}
 ={1\over2}(1-q^2)(13+12q^2+10q^4+4q^6).
\]

The final certificate seal check passed with 56 exact checks per path and
byte-identical `commonCore` objects.

## 3. Figure inventory and reproduction

`source-data.csv` contains 1,416 data rows, partitioned as follows:

| Panel | Rows |
|---|---:|
| A | 327 |
| B | 362 |
| C | 484 |
| D | 243 |
| **Total** | **1,416** |

The package validator reconstructed all source rows from the analytic and
certificate inputs.  Its verify-only result was 49/49 checks.  The generic
repository validator returned zero errors and zero warnings.

The archived outputs are a 178 mm by 126 mm vector PDF and SVG plus a 600 dpi
PNG.  The PNG is 4,204 by 2,976 pixels.  The PDF has one page and all five
referenced fonts are embedded.  The final-size, grayscale, and independent PDF
raster checks passed the stored visual-QA protocol.

## 4. Claim boundary

Panel A is a signed spatial-mean heat-characteristic identity.  Panel B shows
normalized analytic upper-bound shapes, not measurements or sharpness
evidence.  Panels C and D render exact finite Fourier formulas.  The sign
counterexample disproves a universal one-sided statement; amplitude scaling
disproves only the declared same-time, amplitude-independent quadratic
absorption inequality.

Nothing in the figure proves local scale-critical control, a continuation
criterion, a singular solution, arbitrary-data global regularity, or the Clay
Millennium conclusion.  `NOT CLAY`.

## 5. Machine-readable audit result

```text
formalFigurePackage=SEALED_COMMIT_BOUND
formalFigureChecks=49
formalFigureRows=1416
figureSourceCommit=ac6293ac4d0c46c696d2ec8e29d3fb1350e341f1
figurePackageCommit=60b0e869bbaa3a0ace185bf450e067d79fcd79b3
navierStokesSimulation=false
numericalPdeSolution=false
ordinaryTranslationPath=LOCAL_DIRECT_NO_DGX
dgxUsed=false
arbitraryThreeDimensionalGlobalRegularity=OPEN
clayConclusion=OPEN
```
