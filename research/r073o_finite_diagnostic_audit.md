# R0.73O finite spectral diagnostic audit

**Audit date:** 2026-08-31

**Status:** **FINAL SEAL PASS — NOT CLAY**

**Scope:** the finite Fourier spectral diagnostic at \(R=3.012\), its
independent generalized-pencil recomputation, the sealed 19-file certificate,
and the associated 25-file journal-figure package.

**Verdict:** the finite diagnostic, independent recomputation, provenance
bindings, checksums, figure formats, and visual QA pass. Both archival packages
are sealed to immutable source commit
f139c5e707ffdfe855ca114faac669d12e431e59. This audit supports a reproducible
finite-dimensional consistency check only. It does not turn the finite
calculation into an infinite-dimensional spectral theorem or a nonlinear
instability proof.

## 1. Question and fixed parameters

The diagnostic uses the planar Kolmogorov spectral reduction with

\[
 \alpha=0.7,\qquad R=3.012,
\]

and the standard-cube embedding

\[
 A=30.12,\qquad N=10,\qquad k_x=7,\qquad \nu=1.
\]

The dimensionless eigenvalue is denoted by \(\sigma\).  The recorded physical
growth conversion is

\[
 \lambda=A\,N\,\sigma=301.2\,\sigma.
\]

The interval

\[
 [\,3.011528364444,\ 3.011528364446\,]
\]

is an external computer-assisted input attributed in the package to Nagatou
2004 and its later restatement. Neither the producer nor the independent
script recomputes or replaces that rigorous interval.

## 2. Primary finite calculation

The primary truncation is \(N_{\mathrm{trunc}}=120\), giving a matrix
dimension of 241. Its leading finite eigenvalue at \(R=3.012\) is

\[
 \sigma_{\mathrm{fin}}
 =3.7327236415731776\times10^{-5}
 +1.2646397392119195\times10^{-16}i.
\]

The reported relative generalized residual is
\(3.4214202985369127\times10^{-18}\), and the tail spread from truncation 20
is \(1.93374775827454\times10^{-14}\). The corresponding finite crossing and
physical scaling are

\[
 R_{\mathrm{cross,fin}}=3.011528364444171,
\]

\[
 \lambda_{\mathrm{fin}}
 =0.011242963608418411,
 \qquad
 \lambda_{\mathrm{fin}}^{-1}
 =88.94451986407111.
\]

The source-data table contains 131 rows: 121 sweep rows and 10 convergence
rows. Its SHA-256 is
4065d44e461e6e8b89d8ddaa1544e083ba393e8180eb0d0e6be5b1800b532927.
These samples make the finite calculation reproducible and test its numerical
stability. They do not supply a continuum enclosure.

## 3. Independent recomputation

The independent path assembles and equilibrates the generalized eigenvalue
pencil separately and does not import the producer code. At the target it
returns

\[
 \sigma_{\mathrm{ind}}
 =3.7327236439186274\times10^{-5},
\]

\[
 R_{\mathrm{cross,ind}}
 =3.0115283644441178,
\qquad
 \lambda_{\mathrm{ind}}
 =0.011242963615482906.
\]

The two implementations differ by

| Quantity | Absolute difference |
| --- | ---: |
| leading dimensionless eigenvalue | \(2.345449816353387\times10^{-14}\) |
| finite critical crossing | \(5.3290705182007514\times10^{-14}\) |
| physical growth rate | \(7.064494822461853\times10^{-12}\) |

The independently equilibrated relative residual at the target is
\(1.1266123964451373\times10^{-17}\). Across the tested truncations, the
largest equilibrated relative generalized residual is
\(5.211599776279684\times10^{-16}\). All 11 checks internal to the independent
recomputation pass.

The aggregate certificate validator passes all 24 fail-closed checks. These
include exact parameter identities, locked dependencies and runtime versions,
source-data counts and hashes, positivity on both finite paths, agreement
within tolerance, preservation of every exclusion flag, and confirmation that
the producer was not imported by the independent implementation.

The independent run was executed on the local workstation with one process,
no GPU, and a recorded wall time of 5.708457999979146 seconds. Timestamped
progress and resource logs remain in the package.

## 4. Certificate package and provenance

research/certificates/r073o contains exactly 19 files: 9 source files and 10
generated files. Its SHA256SUMS ledger binds the other 18 files. A fresh
SHA-256 readback of all 18 entries passed during this audit.

Final certificate state:

- status = sealed;
- allPrerequisiteChecksPass = true;
- sourceCommitAssigned = true;
- sourceCommit = f139c5e707ffdfe855ca114faac669d12e431e59;
- finalSeal = true.

The sealer binds byte-identical copies of all nine source files to the stated
commit. It does not substitute the current repository HEAD.

Selected certificate hashes:

| File | SHA-256 |
| --- | --- |
| manifest.json | 0a88b96e265d317274c43c5c704c24bf78cfae7be304997ff6c569f7aee47ea7 |
| certificate.json | e5a3ec184563891dd227730369b78a33193d904c52d2a5661dbb5ab51e14b19b |
| validation.json | df80edecf8678d26ccce762cc4fb7b7e8c826ced0d810b72cb349243ea8c4261 |
| independent_validation.json | 8f19b1042ac8e263f2525be6a60ade7d02ae6c6a2765ed8a02784bb98bd00c56 |
| diagnostic.json | 128994c97f2e2ee9cd4fad5fae2788c4a884f852b9170d61d52e599adc7a4eae |

## 5. Formal figure package

research/figures/r073o/fig-r073o-kolmogorov-spectrum contains exactly 25
files: 10 source files and 15 generated files. Its SHA256SUMS ledger binds the
other 24 files, and a fresh readback of every entry passed.

The master figure has the following checked properties:

- one-page vector PDF, \(178.0000000000147\) mm by
  \(82.00000000000361\) mm, with zero raster image XObjects;
- vector SVG with preserved text and zero embedded raster images;
- 600 dpi PNG, 4204 by 1937 pixels, with recorded density
  \(599.9988\times599.9988\) dpi;
- final-size color, final-size grayscale, and independently rasterized PDF
  QA surfaces;
- 27 programmatic checks passed and visualQaConfirmed = true;
- sourceCommitAssigned = true at the same immutable source commit.

The final-size color rendering is legible and unclipped. The grayscale
rendering preserves line-style and marker distinctions. The PDF raster agrees
with the PNG layout. The finite/illustrative boundary remains visible.

Master-output hashes:

| Output | SHA-256 |
| --- | --- |
| figure.pdf | aad3b7de6682627913bd4fe2c47d89fa96cf45643c6356247d32a727d0ee7710 |
| figure.svg | 2cca630f673f2442dc08b77a58e5bb23c43958c7cb2907335e49a4afc035d312 |
| figure.png | 5cee46fc764ad763f2f227d076411bc5070800b916716ff7cd01aa7b7a977de6 |
| manifest.json | 20c1bf33ad3b7b177509135aa3e6a830f0d959e9668cd4a236bfb7f770117740 |
| validation.json | d9e8424ea0ce50452c9f47172d3f0017688c36a1ce1d6820c361b829754f1af7 |
| results.json | 7867c25c6f0fac972d3a3fe68795985b4b8a9530b13119a48523d1b672a0fefc |

Publication-contract audit found that the first sealed figure environment
snapshot preceded the final byte of `independent_validation.json`: it recorded
12,554 bytes and an obsolete SHA-256 even though the figure validation facts
already read the final 12,555-byte file.  The figure was therefore rendered
again from the final sealed certificate, visually reinspected, revalidated,
and resealed.  The environment input now binds
`independent_validation.json` to SHA-256
`8f19b1042ac8e263f2525be6a60ade7d02ae6c6a2765ed8a02784bb98bd00c56`.
This correction changes archival metadata and the timestamp-bearing vector
exports; it does not change the finite spectral values or their evidence
class.  The corrected generated figure package is frozen at repository commit
`6f24e989746056c3ca9d470ddd36b812d4d5c4d1`.

## 6. Evidence boundary

This audit establishes that the archived finite matrices were assembled and
solved reproducibly, that an independently implemented finite calculation
agrees to the stated tolerances, and that the figure reports those finite
values faithfully.

It does not establish an infinite-dimensional positive eigenvalue. The
infinite-dimensional spectral statement in the analytic report must stand on
its separate literature and operator-theoretic chain. It does not replace
Nagatou's computer-assisted critical-interval certificate. It does not
establish nonlinear escape, an essentially three-dimensional unstable mode,
finite-time singularity, or any conclusion for the unforced three-dimensional
Clay problem.

The proper label is:

**finite Fourier diagnostic with independent recomputation — NOT CLAY**

No novelty or priority conclusion is made.

## 7. Machine ledger

    finiteDiagnosticValidation=PASS
    finiteDiagnosticPackage=CLOSED
    sourceCommitAssigned=TRUE
    finalSeal=TRUE
    formalFigurePackage=PASS
