# R0.73Y formal figure-source audit

**Figure:** `fig-r073y-exact-shear-obstruction`

**Audit date:** 2026-09-01

**Verdict:** `FORMAL PASS / TWO-COMMIT SOURCE SEAL VERIFIED`

**DGX used:** `false`

This is the source-owner's read-only audit of the final 25-file figure package.
It checks the commit topology, all immutable source/raw bindings, current
package bytes, checksum inventory, executable validators, deterministic
reconstruction, visual evidence, portability boundary, and mathematical scope.
It is not a new proof of the underlying theorem. `NOT DNS`. `NOT CLAY`.

## 1. Commit topology and exact inventory

```text
frozen analytic source       1ecc6fe20a921db9d0876dbd4484a3aa4ca7ec66
21-file source/raw commit    e37bf12cb5c2a8eb975e5097229dbc48fa597b35
25-file metadata child       05fdbc717a02be9f88fafc2b67a658e706b40be4
```

The source/raw commit contains exactly 10 source files and 11 raw/result
artifacts. The later package commit adds only `SHA256SUMS`, `manifest.json`,
`qa-report.md`, and `validation.json`. The final directory contains exactly 25
regular files, with no subdirectory, symlink, hidden extra, or special file.

The manifest contains exactly 21 source bindings. For every binding, the
current bytes, SHA-256, byte count, source-commit blob bytes, and Git blob OID
agree. All 25 current files also equal their package-commit blobs.

## 2. Formula and source-data binding

The renderer binds three frozen research sources at `1ecc6fe2...`:

```text
2574f2caf19248a17d25f811488db1c7b30295efd07e59852c3afa17cf8f69e4  research/r073y_exact_shear_no_go.md
fe6bb0e8bb4674f63a579f6b2db92c12f75235c4d293594e115c7b49599ef4df  research/r073y_exact_shear_certificate.json
668177c61721600880cd85651f8481249c8f9a972d631dd4f5a3383bbb07c6aa  research/r073y_exact_shear_certificate_report.md
```

All 6,372 data rows are reconstructed from the frozen closed formulas. The
largest formula discrepancy is `1.1102e-16`; the largest stored-statistic
discrepancy is `5.5511e-17`. These are binary64 reconstruction checks. The
universal zero identities and strict positivity come from the analytic proof,
not from plotted samples.

## 3. Executable and deterministic checks

The final package validator in `--verify-only` mode passes without writes. The
repository-wide generic validator returns:

```text
errors=[]
warnings=[]
```

Two fresh builds reproduce all 18 deterministic-core files byte-for-byte.
The negative suite confirms that runtime-version drift, frozen-source drift,
and inventory drift each fail closed. `SHA256SUMS` covers every package file
except itself and independently verifies every listed digest.

The source correction also makes the zero-amplitude endpoint literal:
production vanishes for every real \(A\), strict gradient covariance holds for
\(A\ne0\), and the trivial \(A=0\) member has \(D_{ii,s}=0\). The plotted
covariance panels use the normalized nonzero witness \(A=1\), so no numeric or
visual output changed during resealing.

## 4. Output and visual QA

| Output | Formal property | SHA-256 |
|---|---|---|
| `figure.pdf` | synchronized one-page vector PDF | `abce445fc6409bf8b412fab47620aeca5b748499cf953b9a40aa7d1fc8a46df5` |
| `figure.png` | 4204 x 1464 px, 600 dpi | `7fd3b52f152e6fbc2d17325f6b1fc6f16172b7e5c3b0dcd72e7028624125e6f6` |
| `figure.svg` | synchronized vector output | `9403d5f042b17b8903a9c6cc1a0d51456412c09652b799ad3e75f794b2f86240` |

The final-size color image, grayscale image, and independently rendered PDF
show no clipping, label collision, lost panel marker, or ambiguous line style.
The SVG/PNG low-resolution structural correlation is `0.9905`; the stored
PDF/PNG mean absolute pixel difference is `5.8041`. These metrics supplement,
but do not replace, visual inspection.

## 5. Portability and scope

No real temporary directory, user-home directory, or host-specific source path
appears in the sealed outputs. The package records its certified runtime while
verification depends on pinned package versions rather than literal equality
with the original host path. No network, GPU, DGX, simulation, or DNS result
supports the figure.

The figure visualizes an analytic exact shear witness with
\(\Pi_s=\mathscr S_s=Q_s=0\) for every real amplitude,
\(A\ne0\Rightarrow D_{ii,s}>0\), \(A=0\Rightarrow D_{ii,s}=0\), and cubic
amplitude homogeneity. It rules out only the declared zero-preserving
production-only modulus. It does not establish or refute an
associated-pressure estimate, epsilon regularity, arbitrary-data global
regularity, blow-up, or a Clay conclusion.

**Final verdict:** `FORMAL PASS`. `ANALYTIC EXACT WITNESS / NOT DNS`.
`NOT CLAY`.
