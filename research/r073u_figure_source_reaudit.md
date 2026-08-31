# R0.73U independent figure-source reaudit

**Reaudit date:** 2026-09-01

**Object:** `fig-r073u-tensor-heat-hierarchy`

**Verdict:** PASS.  A separate readback of the corrected sealed files, rather
than the prose QA conclusion alone, reproduces the 325/325 figure gate and
finds no manifest, checksum, data-label, format, semantic-boundary, or visual
inconsistency.  The corrected package explicitly fixes the comparison at the
same initial time \(t=0\), defines \(V\), and rejects a trajectory-symmetry
reading.

**Ordinary translation path:** `LOCAL_DIRECT_NO_DGX`

## 1. Reaudit method

I used five independent readbacks:

1. parsed `manifest.json`, `validation.json`, and `SHA256SUMS` and compared
   every stored byte count and digest with the current regular file;
2. reran `validate.py --verify-only` with the pinned Python 3.12 dependency
   set, without rewriting the seal;
3. parsed `source-data.csv` independently and rebuilt its row inventory and
   the Panel B matrices from component labels;
4. checked the PDF page box, SVG view box and remote-link boundary, 600 dpi
   PNG dimensions, and the stored color, grayscale, and PDF rasters;
5. visually read the master PNG, grayscale readback, and independently
   regenerated PDF readback at their delivered aspect ratios.

The validation file contains 325 checks, 325 distinct identifiers, 325 pass
flags, and zero failures.  The read-only validator returned
`finalSeal=true`, `status=PASS`.  Every one of the 24 checksum entries returned
`OK`.

## 2. Provenance and hash parity

The analytic source binding is
`84e808dae473f6381cbf9df55a71f5fe81a1cfce`; the package commit is
`6c20af03a21488fea3f060738084fa9048437984`.  The manifest digest is
`c48aa6b1185b0328efed10256fe7d012481cfeaa301ae5eb3dd7e444acf99fcb`.

The three publication formats are independently hash-bound:

```text
PDF  5377b2cdb32d7e8c65429d0d59b8d20c31128d9627c62b09f4f7fd92fba32088
SVG  18826213480a95ddf0bb6a515e9be6beebeaec77816abcc2c0e697709b162fe1
PNG  f35bed77869d7ced9f5d27e1a0390d4c3d91f6d3a4f1b5fc6b52ced1d82ae4e8
CSV  75ecb2139bb8667a89a1bb3353f67afbaa236b9c6570c7b93b5ed3689847e4aa
```

Format parity here means that the formats carry the same three-panel content,
physical footprint, equations, labels, and visual hierarchy.  It does not
mean that vector PDF/SVG bytes should equal raster PNG bytes.  The PDF was
independently rasterized and matched its stored QA raster exactly; the master
PNG generated the stored final-size and grayscale readbacks exactly.

## 3. Independent data and formula readback

The CSV has exactly 138 rows: four analytic schematic rows, twenty-two exact
finite rows, 111 samples of the stated analytic curve, and one exact peak
row.  Reordering the component-labelled entries gives

\[
 A=\begin{pmatrix}-2&3\\3&-4\end{pmatrix},\quad
 B=\begin{pmatrix}0&-2\\-2&4\end{pmatrix},\quad
 A+B=K=\begin{pmatrix}-2&1\\1&0\end{pmatrix}.
\]

The separate \(T\) and \(V\) component rows are all zero, and the source
defines

\[
 V=\Delta T-2\sum_\ell\partial_\ell u\otimes\partial_\ell u.
\]

Every Panel B data row carries \(t=0\); the separation-row normalization says
`same initial time t=0` and `not trajectory symmetry`.  The labels for
\(2e^{-5s}K\), \(2\sqrt6e^{-5s}\), and
\(D_L(s)=2\sqrt6Le^{-5sL^2}\) agree between the CSV, caption, plot, and frozen
analytic derivation.  Panel C consistently labels

\[
 f(z)=ze^{-5z^2},\qquad z=\sqrt{s}L,qquad
 z_*=1/\sqrt{10},\qquad f(z_*)=e^{-1/2}/\sqrt{10}.
\]

The exact derivative label
\(f'(z)=e^{-5z^2}(1-10z^2)\) confirms the unique positive maximum.  The curve
is an analytic formula sampled for rendering, not a fit.

## 4. PDF, SVG, PNG, print, and grayscale readback

- PDF: one page; 178 mm by 100 mm media box; stored PDF raster reproducible
  pixel for pixel.
- SVG: matching view box; no remote drawable; no undeclared color.
- PNG: 600 dpi archival master, \(4204\times2362\) pixels; the one-pixel
  horizontal rounding difference from 178 mm is within the explicit gate.
- Final-size QA: \(1800\times1011\) pixels and exactly regenerated from the
  master PNG.
- Grayscale QA: \(1800\times1011\) pixels and exactly equal to the prescribed
  luminance conversion.

The separate visual readback confirms that all matrix signs and entries are
readable in color, grayscale, and the PDF raster.  Dashed versus solid
connections remain distinct without color.  The peak marker and labels do not
collide.  Panel B visibly labels both states and the separation at \(t=0\),
and displays the definition of \(V\).  The caption explicitly says the
comparison is not a trajectory symmetry.  The footer says the object is
coefficient-level, not a simulation or fitted law, and `NOT CLAY`.

## 5. Reaudit boundary

This pass certifies the figure source chain and its faithful rendering.  It
does not independently prove the continuum Navier--Stokes identities; those
remain in the frozen analytic proof and analytic audit.  The finite witness is
not a PDE simulation and is not evidence of blow-up.  The plotted
\(s^{-1/2}\) behavior is not a universal lower bound.  It does not rule out
time integration, one-sided estimates, cancellations, signed/cubic
augmentation, or a state containing \(v_s\).  It has no global-regularity or
Clay implication.

No GPU, network service, DGX job, or Navier--Stokes simulation was used.
Routine translation is performed directly on the local workstation.
