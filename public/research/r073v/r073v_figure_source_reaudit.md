# R0.73V formal figure source: independent re-audit

Date: 2026-09-01  
Figure: `fig-r073v-signed-third-order-interface`  
Package: `figures/r073v/fig-r073v-signed-third-order-interface/`

## Verdict

**PASS — ready for the R0.73V release transaction.**

No figure-package release blocker remains.  The source/raw-artifact commit and
the subsequent metadata reseal are both present, immutable, byte-identical to
the working tree, and clean in the figure-package scope.  The remaining
`publicationStatus=staged` value is the intended hand-off state before the
release transaction copies/publishes the package; it is not evidence that the
figure source seal is incomplete.

This re-audit did not edit or regenerate the figure package.

## Independent checks

### 1. Git blob immutability and seal lifecycle — PASS

- Exact-certificate source commit:
  `7c445c522a241bdc8b867b6fce0f0fed9b82e97d`.
- Exact-certificate package commit:
  `b34d91ea96c257b943f11d134e8024138e5f3cb0`.
- Figure source/raw-artifact commit:
  `f94915332ff405ae723711e8041acc2af07e896b`.
- Figure metadata reseal commit at the time of this re-audit:
  `ae679d5afa5f3cfacfe79c4d7b8a462baca2c195`.
- All 21 `seal.figureSourceBindings` were independently read with
  `git cat-file blob` from `f949153...`.  Every blob equals the current file
  byte for byte and has the SHA-256 recorded in the manifest.
- All 25 package files were independently read from `ae679d5...`; every blob
  equals the current working-tree file.
- `git status --porcelain=v1 --untracked-files=all -- <package>` returned no
  output.
- The manifest correctly records:
  `figureSourceCommitAssigned=true`,
  `requiresParentFigureSourceCommitFinalReseal=false`, and
  `seal.state=formal-figure-source-seal`.
- Commit ancestry is correct: the metadata reseal `ae679d5...` has figure
  source commit `f949153...` as its parent.

The two certificate outputs are also immutable at `b34d91e...`:

| Certificate output | Current SHA-256 | Git-blob SHA-256 | Result |
|---|---|---|---|
| `results.json` | `e024ea767ff146ee2e53455522e6c0ab2c59608e74038673cc8a6fca0271b0c4` | same | PASS |
| `independent-results.json` | `0c40808136b532b536a871184a9937b7a29c436e04ef0235e607964b0ebec1d0` | same | PASS |

Their complete `commonCore` objects are equal.

### 2. Package hashes and inventories — PASS

- Package files: 25.
- `SHA256SUMS` records: 24; the checksum file correctly excludes itself.
- `shasum -a 256 -c SHA256SUMS`: 24/24 `OK`.
- `source-data.csv`: 158 data rows plus one header row.
- Figure validator: 147/147 checks passed.
- `validation.json`, `results.json`, and `manifest.json` agree on the 147
  checks and 158 source-data rows.
- The evidence-aware CSV check keeps 57 certificate-derived rows string-exact;
  across the 101 renderer rows it keeps every non-`y` field exact, keeps the
  zero sample exact, and admits a remaining `y` value only when both the
  `2e-16` absolute bound and the 256-ULP bound hold against the closed formula.
- No `__pycache__`, subdirectory, unexpected file, or untracked figure-package
  entry is present.

### 3. Validator independence — PASS

The package validator was run read-only:

```text
python3 -B figures/r073v/fig-r073v-signed-third-order-interface/validate.py \
  --deps /Users/kasifa/.cache/codex-runtimes/r073s-figure-python \
  --verify-only
```

Result: `PASS`, 147 checks.

The repository-generic validator was also run independently:

```text
python3 -B research/validate_figure_package.py \
  figures/r073v/fig-r073v-signed-third-order-interface
```

Result: no errors and no warnings.

In addition, a standalone audit script that did not import `plot.py` or
`validate.py` independently checked the two certificate objects, CSV row
count, media dimensions, raster equality, scope flags, resource log, and seal
fields.  Result: `PASS`.

### 4. PDF, SVG, PNG, grayscale, and PDF-raster QA — PASS

- PNG: `4204 x 2787` pixels, RGBA, recorded DPI
  `(599.9988, 599.9988)`, consistent with the requested 600 dpi export.
- PDF: one page; independent media-box conversion gives
  `178.0000000000147 x 118.00000000000779 mm`.
- SVG: `504.566929 pt x 334.488189 pt` with matching view box and no remote
  HTTP(S) image/link dependency.
- `qa-final-size.png` is pixel-identical to an independently reconstructed
  thumbnail of the 600 dpi PNG.
- `qa-grayscale.png` is pixel-identical to an independent luminance conversion
  of that final-size raster.
- `qa-pdf.png` is pixel-identical to an independent 3x PDFium rasterization of
  `figure.pdf`.
- Manual inspection of the stored color, grayscale, final-size, and PDF QA
  rasters found no clipped titles, equations, matrices, axes, annotations, or
  claim-boundary footer.  Blue/gold distinctions remain legible in grayscale
  through fill, outline, position, and direct labels.

### 5. Panel B active-block disclosure — PASS

Both `README.md` and `caption.md` explicitly state that Panel B prints only the
active 2 by 2 block and that the omitted third row and third column are exactly
zero in the sealed 3 by 3 tensor coefficients.  Thus the compact matrix display
cannot reasonably be read as silently dropping unknown or numerical entries.

### 6. Scope and compute-policy boundary — PASS

The contract, results, manifest, figure footer, caption, and resource log are
consistent on the following boundaries:

- `navierStokesSimulation=false`;
- `fittedScalingLaw=false`;
- `analyticCurveIsRendererSampleNotFit=true`;
- `coefficientwiseNonRecoveryOnly=true`;
- `quarticStatementSelectedCoefficientOnly=true`;
- `fourthOrderNonClosureEstablished=false`;
- `finiteHierarchyNoGoEstablished=false`;
- `globalRegularityEstablished=false`;
- `clayProblemSolved=false`;
- `dgxUsed=false`;
- `gpu=not used`;
- `ordinaryTranslationPath=LOCAL_DIRECT_NO_DGX`.

All five resource-log rows carry the same local/no-DGX policy.  Nothing in the
figure package presents the deterministic analytic profile as a simulation or
fit.

## Release blockers

**None inside the formal figure package.**

The release transaction must still preserve the sealed files and advance the
archive/site publication metadata from `staged` to the appropriate published
state.  That is a normal release step, not a request to rerender, recompute, or
reseal the figure source.  Any post-seal change to one of the 21 bound
source/raw files would invalidate this verdict and require a new source commit
and metadata reseal.
