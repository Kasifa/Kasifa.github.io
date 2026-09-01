# R0.73W formal figure source: independent re-audit

**Date:** 2026-09-01

**Figure:** `fig-r073w-signed-production`

**Package:** `figures/r073w/fig-r073w-signed-production/`

## Verdict

**PASS — ready for the R0.73W public release transaction.**

No blocker remains inside the formal figure package.  The 21 source/raw files
are immutable at `ac6293ac4d0c46c696d2ec8e29d3fb1350e341f1`; the four metadata
files are sealed in its direct child
`60b0e869bbaa3a0ace185bf450e067d79fcd79b3`; and every current package file is
byte-identical to that package commit.  `publicationStatus=staged` is the
correct hand-off state before HTML/PDF/site publication and is not an
incomplete source seal.

This re-audit was read-only.  It did not regenerate or edit the figure package.

## Independent checks

### 1. Git and checksum lifecycle — PASS

- The package-seal commit has exactly the figure-source commit as its parent.
- The first commit binds 10 source files and 11 raw artifacts.
- The second commit adds exactly four metadata files.
- All 21 manifest source bindings match current bytes, SHA-256 values, byte
  lengths, and Git blob object IDs.
- All 25 current package files match the package-seal commit.
- All 24 `SHA256SUMS` records verify.
- The scoped figure-package working tree is clean.

### 2. Validators and exact inputs — PASS

- Figure validator: 49/49 checks.
- Generic figure-package validator: zero errors and zero warnings.
- Source-data rows: 1,416.
- Primary exact producer: PASS, 56 checks.
- Independent trigonometric producer: PASS, 56 checks.
- Certificate source-commit seal check: `SEALED_COMMIT_BOUND`.
- Complete two-path `commonCore` objects: byte-identical.

### 3. Display and visual QA — PASS

- PDF/SVG size: 178 mm by 126 mm.
- PNG: 4,204 by 2,976 pixels at 600 dpi.
- PDF: one page, with all five referenced fonts embedded.
- Stored final-size, grayscale, and PDF-raster inspections report no clipped
  titles, equations, labels, axes, annotations, or footer.
- Solid/dashed strokes and filled/open markers preserve comparisons in
  grayscale.

### 4. Scope boundary — PASS

The figure package consistently records `navierStokesSimulation=false`,
`fittedScalingLaw=false`, `ordinaryTranslationPath=LOCAL_DIRECT_NO_DGX`, and
`dgxUsed=false`.  Its curves are deterministic coordinates of displayed
identities, upper bounds, and finite formulas.  They are not DNS output, a
numerical Navier--Stokes solution, generic-turbulence evidence, a singularity,
or a blow-up candidate.

The seal also does not promote any finite calculation into a PDE theorem.  In
particular, localized scale-critical control, arbitrary-data three-dimensional
global regularity, and the Clay problem remain open.  `NOT CLAY`.

## Release hand-off

```text
formalFigurePackage=SEALED_COMMIT_BOUND
figureSourceCommit=ac6293ac4d0c46c696d2ec8e29d3fb1350e341f1
figurePackageCommit=60b0e869bbaa3a0ace185bf450e067d79fcd79b3
publicReleaseTransaction=READY
ordinaryTranslationPath=LOCAL_DIRECT_NO_DGX
dgxUsed=false
```

The next transaction must preserve the sealed figure bytes while producing
synchronized HTML/PDF, cumulative recap, route/accounting updates, and the
GitHub Pages publication checks.  Those remaining release tasks are distinct
from the already completed figure seal.
