# R0.73U figure-source audit: tensor heat hierarchy

**Audit date:** 2026-09-01

**Figure ID:** `fig-r073u-tensor-heat-hierarchy`

**Verdict:** PASS - PUBLICATION SEAL.  The corrected formal figure is
traceable to its analytic source, exact finite data, plotting source, three
publication formats, and visual QA assets.  It explicitly evaluates the
\(u/-u\) comparison at the same initial time \(t=0\), defines \(V\), and
states that the
comparison is not a trajectory symmetry.  The stored validator reports
325/325 passing checks with 325 distinct check identifiers and no failed
entry.

**Ordinary translation path:** `LOCAL_DIRECT_NO_DGX`

## 1. Source and package bindings

The final figure manifest binds three frozen analytic files to

```text
84e808dae473f6381cbf9df55a71f5fe81a1cfce
```

with these SHA-256 values:

| Analytic file | SHA-256 |
|---|---|
| `research/r073u_problem_freeze.md` | `1c7c4b0cf683bc91fc55022748a1c56ef843b0f50617e97fa8e2e57af57cbdc3` |
| `research/r073u_tensor_heat_hierarchy.md` | `733af2e677c1bff1eaecb2e80115dced98d9d9842b6960d0fef7b0968f5735ee` |
| `research/r073u_independent_analytic_audit.md` | `ac9531cf8fb48fba95f0562dace370337f3d6012cdb96a4c258797e24af3f389` |

The corrected figure package was resealed at
`6c20af03a21488fea3f060738084fa9048437984`.  Its final manifest has
SHA-256
`c48aa6b1185b0328efed10256fe7d012481cfeaa301ae5eb3dd7e444acf99fcb`.
Principal file bindings are:

| Artifact | SHA-256 |
|---|---|
| `plot.py` | `a7cd8e4bea046d82e241483db2e16524c11018767872e6d00c1a3fb80bb73970` |
| `validate.py` | `7638afbe892c4bd76756cf1cda0c91d98855141ec496a3ad9337f6e8cb3806ed` |
| `source-data.csv` | `75ecb2139bb8667a89a1bb3353f67afbaa236b9c6570c7b93b5ed3689847e4aa` |
| `figure.pdf` | `5377b2cdb32d7e8c65429d0d59b8d20c31128d9627c62b09f4f7fd92fba32088` |
| `figure.svg` | `18826213480a95ddf0bb6a515e9be6beebeaec77816abcc2c0e697709b162fe1` |
| `figure.png` | `f35bed77869d7ced9f5d27e1a0390d4c3d91f6d3a4f1b5fc6b52ced1d82ae4e8` |
| `validation.json` | `0d5a9005486e325a4c9b5fe70e4476edda486c37a720ce5c029abfab34747fec` |

The package records `finalSeal=true`, `sourceCommitAssigned=true`, and rejects
the superseded analytic commit
`72493751370aa948947000df169e21199fc5c95d`.

## 2. Source-data reconstruction

The CSV contains 138 data rows:

| Evidence class | Rows |
|---|---:|
| exact Panel A schematic records | 4 |
| exact Panel B finite diagnostic records | 22 |
| analytic samples of \(f(z)=ze^{-5z^2}\) | 111 |
| separate exact peak record | 1 |

The Panel B rows reconstruct

\[
 A=\begin{pmatrix}-2&3\\3&-4\end{pmatrix},\qquad
 B=\begin{pmatrix}0&-2\\-2&4\end{pmatrix},\qquad
 K=A+B=\begin{pmatrix}-2&1\\1&0\end{pmatrix},
\]

with \(\lVert K\rVert_F^2=6\).  The corrected package defines

\[
 V=\Delta T-2\sum_\ell\partial_\ell u\otimes\partial_\ell u
\]

before recording \(\widehat T(h_*)=\widehat V(h_*)=0\).  All Panel B
records are evaluated at the same initial time \(t=0\), not along a claimed
trajectory symmetry.  The tangent labels agree with

\[
 \left.\partial_t\widehat\Theta_s(h_*;u(t))\right|_{t=0}
 -\left.\partial_t\widehat\Theta_s(h_*;\widetilde u(t))\right|_{t=0}
 =2e^{-5s}K,
 \qquad
 \left\|\left.\partial_t\widehat\Theta_s(h_*;u(t))\right|_{t=0}
 -\left.\partial_t\widehat\Theta_s(h_*;\widetilde u(t))\right|_{t=0}
 \right\|_F
 =2\sqrt6e^{-5s}.
\]

Panel C uses the closed analytic formula

\[
 f(z)=ze^{-5z^2},\qquad
 f'(z)=e^{-5z^2}(1-10z^2),
\]

so its unique positive maximum is
\(z_*=1/\sqrt{10}\) with
\(f(z_*)=e^{-1/2}/\sqrt{10}\).  The curve rows are renderer samples of this
formula.  They are not observations, fitted data, or a numerical scaling
experiment.

## 3. Format, print-size, and visual QA

The archival footprint is 178 mm by 100 mm.  The outputs passed these checks:

- the PDF has one page and a media box of
  \(504.566929\times283.464567\) points, equivalent to 178 mm by 100 mm;
- the SVG has the matching view box, contains no remote drawable, and uses
  only the declared two-root palette plus neutrals;
- the 600 dpi PNG is \(4204\times2362\) pixels, within one pixel of the
  independently rounded 178 mm expectation and exact in height;
- `qa-final-size.png` is the exact stored 1800 by 1011 print-size readback;
- `qa-grayscale.png` is the exact luminance conversion of that readback;
- a fresh PDF raster is pixel-identical to the stored 1262 by 709
  `qa-pdf.png`.

I inspected the master color image, the grayscale image, and the independent
PDF raster.  Panel labels, matrix entries, arrows, the blocked signed-tangent
map, the exact peak label, and the coefficient-level \(s^{-1/2}\) statement
are legible.  Grayscale preserves the distinction through outlines, fills,
solid/dashed arrows, and direct labels.  I found no clipped text, collision,
or material discrepancy among the PDF, SVG, and PNG presentations.  The
corrected figure visibly labels both states and their separation at \(t=0\),
displays the definition of \(V\), and the caption explicitly says that this
is not a trajectory symmetry.

## 4. Read-only validation

I reran the final validator in `--verify-only` mode with Python 3.12 and the
five pinned package versions, then checked the complete checksum inventory:

```text
python3 -B research/figures/r073u/fig-r073u-tensor-heat-hierarchy/validate.py \
  --deps <python-packages> --verify-only
cd research/figures/r073u/fig-r073u-tensor-heat-hierarchy \
  && shasum -a 256 -c SHA256SUMS
```

The validator returned `status=PASS`, `finalSeal=true`; all 24 checksum lines
returned `OK`.  The stored validation contains 325/325 passing checks, 325
distinct identifiers, and zero failures.  This includes exact CSV row
reconstruction, matrices and peak, dependency pins, PDF/SVG/PNG integrity,
dimensions, palette, final-size raster, grayscale conversion, PDF
re-rasterization, source commit, visual confirmation, the initial-time scope,
the definition of \(V\), and the explicit rejection of a trajectory-symmetry
claim.

## 5. Interpretation boundary

The figure supports an exact continuum identity, an exact finite Fourier
diagnostic, and a plotted analytic function.  It does not show a PDE
simulation or trajectory.  The \(s^{-1/2}\) statement is a coefficient-level
cost for this witness at a fixed parabolic slice; it is not a universal lower
bound for every estimate, closure, or augmented hierarchy.  The witness is
smooth and planar, not singular or near-singular.  The figure establishes no
improved regularity criterion, no arbitrary-data global theorem, and no Clay
result: `NOT CLAY`.

The metadata consistently records `navierStokesSimulation=false`,
`fittedScalingLaw=false`, `dgxUsed=false`, and
`ordinaryTranslationPath=LOCAL_DIRECT_NO_DGX`.  No DGX computation supports
the figure; ordinary translation is local and direct.
