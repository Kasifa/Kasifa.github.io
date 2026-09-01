# R0.74M independent figure-package audit

## Result

I audited the sealed package at
`research/figures/r074m/fig-r074m-nearest-inward-expulsion/` from a stable
snapshot. I did not use the package's recorded validation result as evidence.
The result is

\[
 \boxed{\text{INDEPENDENT FIGURE-PACKAGE AUDIT: PASS; NOT CLAY.}}
\]

This result concerns the reproducibility, data binding, typography, rendering,
and claim boundary of one formal figure. It does not extend the scope of the
R0.74M analytic theorem and gives no universal Navier--Stokes regularity or
singularity result.

## 1. Stable snapshot binding

The package stopped changing before this audit began. The following sizes,
timestamps, and hashes were checked at the start and again after every
read-only reconstruction and visual inspection. They did not drift.

| file | SHA-256 |
|---|---|
| `figure.svg` | `bfe895023513c536e6bc1fca07531560d932f5e30bd3acc7e1c106e1d756c2de` |
| `figure.pdf` | `1773da1a48e7bd0086d035261beb9647074af1e5ee3f63d53d34d4805b217d31` |
| `figure.png` | `aa91000e5c529cd48b176500571a7155f494582e794e7888119f63f1774da0a8` |
| `manifest.json` | `78c89ee287c0f3d5b20625eac7869a749dec137e11ba4878617d8907a8f6446c` |
| `validation.json` | `dba5b7ce493d73ca8750ea4fb093ab153a7c3fa384848767a46660b96f1a5d5b` |
| `SHA256SUMS` | `acb5b41c73af70245e468996411d221866b39e274dda2d5594077c330573f3cb` |

I copied the package and its five external inputs into a separate temporary
repository-shaped directory and ran `validate.py` there. It returned 49/49
PASS. Its regenerated `manifest.json`, `validation.json`, and `SHA256SUMS`
were byte-identical to the sealed originals. I then checked all 23 lines of
`SHA256SUMS` independently; every line matched.

The manifest contains 22 package entries and five external bindings. I
recomputed every byte count and SHA-256 value. The five bindings include the
problem freeze, current proof source, finite certificate, independent analytic
audit, and certificate generator. In particular, the analytic-audit binding is

`research/r074m_nearest_inward_independent_audit.md`

with SHA-256

`6e81954068dbcf588c857a6ebb1e1dcc80c70d6c926f8631aba8b2bff84c281c`.

It binds the current proof source SHA-256

`0077326ca97cfe40a0a43019caf0118504cf9ed770979595d63bf9d2ec281ef0`.

## 2. Exact-data reconstruction

I parsed all 18 rows of `source-data.csv` with exact rational arithmetic and
compared them with the current proof source. Every exact and decimal field
agreed. The independently reconstructed identities include

\[
 \frac35-\frac{32}{63}-\frac1{16}=\frac{149}{5040},
\]

\[
 \frac1{320}-\frac1{640}=\frac1{640},
\]

and

\[
 \frac1{16}-\frac1{320}-\frac2{1323}
 =\frac{24497}{423360}.
\]

The table also agrees with the proof's segment length \(1/64\), displacement
prefactor \(1/32768\), tail distance \(\Sigma_L/2\), denominator \(1056\),
and raw \(R\)-power ledger \(4,3,5\).

## 3. Earlier fail-closed findings and their repair

The first audit attempt stopped before PASS. Four defects or insufficiently
bound statements were reported. The final package closes all four.

| item | first finding | final check |
|---|---|---|
| F1 | `caption.md` contained a tab in `\to\infty` and lost backslashes in `\ge`, `\mathbb P`, and `\le`. | The commands are intact, the caption has no forbidden control byte, and all displayed relations parse as intended. |
| F2 | The SVG named local font families without embedding them; macOS Quick Look substituted a serif font. | The SVG contains two valid base64 TTF payloads. Their decoded bytes exactly equal DejaVu Sans regular and bold. An independent Quick Look render has no serif substitution or missing glyph. |
| F3 | The figure said `PENDING AUDIT` although the analytic audit had passed, and the package did not bind that audit. | Footer, metadata, config, results, manifest, README, and caption now distinguish `ANALYTIC AUDIT PASS` from the separately reported figure-package audit. The analytic-audit file is one of the five external hash bindings. |
| F4 | The caption stated the unpadded gap without the actual \(R/8\) collar padding or its large-\(L\) condition. | It now states \(r_-=(32L/63+1/8)R\) and \(32/63+1/16+1/(8L)\le3/5\), and says that the positive gap absorbs the padding for sufficiently large \(L\). |

## 4. Vector, font, and physical-size checks

The SVG has 40 text nodes, 29 path-or-rectangle vector nodes, and no raster
image node. Its two decoded font payloads are:

| embedded family | decoded bytes | decoded SHA-256 |
|---|---:|---|
| `R074M-Regular` | 757076 | `7da195a74c55bef988d0d48f9508bd5d849425c1770dba5d7bfc6ce9ed848954` |
| `R074M-Bold` | 705684 | `e6476c1b80502924294eed40894c5b18e06c181444ca953e5334262df9c27724` |

These byte streams exactly match the pinned DejaVu Sans regular and bold TTF
files used by the generator.

The PDF is one unencrypted vector page. Its measured media box is
\(177.9999897\,\mathrm{mm}\times100.0000117\,\mathrm{mm}\), consistent with
the declared \(178\,\mathrm{mm}\times100\,\mathrm{mm}\) double-column size.
It has no image XObject. All 40 text-show operations use the embedded subset
DejaVu Sans regular or bold fonts. ReportLab's unembedded built-in Helvetica
and Times resources occur only in empty font-initialization operators and show
no glyph.

The raster master is \(4205\times2363\) RGB pixels with 600-dpi metadata.
The final-size and grayscale checks are \(1402\times788\) at 200 dpi, and the
independent PDF raster is \(2103\times1182\) at 300 dpi.

## 5. Independent visual inspection

I inspected these five surfaces at their native resolution:

1. `figure.png`;
2. `qa-final-size.png`;
3. `qa-grayscale.png`;
4. `qa-pdf.png`; and
5. `qa-svg-quicklook.png`.

I also rendered the final SVG again with macOS Quick Look. The regenerated
pixel array was exactly equal to the archived Quick Look QA image. Its square
thumbnail canvas retains the full \(178{:}100\) artwork without cropping, and
the text remains DejaVu Sans rather than the serif fallback seen in the failed
first audit.

There is no clipping, overlap, broken arrow, missing glyph, or unreadable
final-size label. The endpoint collar, dashed path tube, heat-defect window,
kernel tail, and good/bad payment boxes remain distinguishable in grayscale
by position, border, dash pattern, and text. The SVG, PDF, and PNG carry the
same constants and status footer.

## 6. Claim and simulation boundary

The generator contains no random-number or numerical-path sampling code. The
curve in panel A is labeled as an analytic schematic. The package consistently
sets `simulation: false` and states `no DNS` and `no sampled stochastic path`.

The final status is precise:

- the nearest-inward source theorem has an independent analytic audit with
  result PASS;
- this note independently passes the sealed figure package;
- the remaining shell synthesis and the full R0.74K condition remain open;
- the figure is not a simulation result; and
- no Clay problem claim is made.

\[
 \boxed{\text{R0.74M FIGURE PACKAGE: PASS; NOT CLAY.}}
\]
