# R0.74O — independent formal-figure package audit

## Verdict

**INDEPENDENT FIGURE-PACKAGE AUDIT: PASS.**

The audited object is
`research/figures/r074o/fig-r074o-amplitude-endpoint/` in the R0.74O
worktree.  I did not use the package's internal `Manual status: PASS` as
evidence of visual correctness.  I independently recomputed the exact source
data, rebound every external SHA-256, inspected the renderer and validator,
rebuilt the package in an isolated copied repository tree, compared the
outputs byte for byte, and inspected every publication/QA surface.

An earlier intermediate state was rejected because five edited files were
not yet rebound by `manifest.json` and `SHA256SUMS`.  That intermediate state
is not the object audited here.  The final regenerated package below is
sealed consistently and passes the independent checks.

This audit is a figure-package audit, not a new proof of the underlying
Navier--Stokes theorem, not a novelty or priority determination, and not a
claim about the Millennium problem.  **NOT CLAY.**

## 1. Frozen package and inventory

The final directory contains exactly 26 regular files.  `manifest.json`
contains 24 package entries and 15 external bindings; it intentionally omits
itself and `SHA256SUMS`.  `SHA256SUMS` contains 25 lines and seals every other
file, including `manifest.json`.  Independent recomputation gave:

- `shasum -a 256 -c SHA256SUMS`: 25/25 PASS;
- manifest entry byte counts and hashes: 24/24 PASS;
- external manifest hashes: 15/15 PASS;
- internal validator: 72/72 unique checks PASS;
- package physical inventory: 26 files.

The exact package inventory is:

| File | Bytes | SHA-256 |
|---|---:|---|
| `README.md` | 1211 | `72f3a9ee8dacde4155800d273e456d46082126ba1d58f93e2f2e8f0f42ad9cd1` |
| `SHA256SUMS` | 2019 | `63d2e352b49988bca779703008b4a24697dcc2ba41b4d0c1b80eb868ed4fc1e9` |
| `caption.md` | 1488 | `f65b0c8b52617193f15abe06cb09d0b25278d1bde2cd03e4c446c14fe9f9746a` |
| `chart-contract-and-source-data.md` | 2136 | `ec8b03b88563eddab3e205e8be1527de0316f1819248fd200f7d6c81efd3f262` |
| `command.txt` | 253 | `00966697891bbf574179d3c10385d5b5898f1da1e3df5c9b24d397042e0d33a2` |
| `config.json` | 413 | `1bdcc9dab54c46b7303bfedf79c38d8c7b1a3f1125bf4ce8719ff93beb8a6d8d` |
| `contract.json` | 1479 | `0094d590bb5fbabf24ca094db1983aedcfa6467cdf254d760c2c0669975faec8` |
| `environment.json` | 290 | `1260c0d58525b65b6558c74726bab3eb79d0882c01d6f40cdf994949f42f1a29` |
| `figure.pdf` | 47647 | `3ed235968190c828ed1dfbc3b97c2201ea32902a3a180caa3b11ef6bf0a8a5da` |
| `figure.png` | 383312 | `e5578383c4f982f6f2aed74397dbe80ea8369f987d97b058db20b40fcc7ff3b1` |
| `figure.svg` | 1967166 | `aab4bca1d44fa248d9e108312dfdfb933b835d524fe86b915beaf4f22f7475de` |
| `layout-bounds.json` | 269 | `15034bebe7e4fd45fb9170779b8e3f7cc420fbd33ca3ef963378af640e6d4258` |
| `manifest.json` | 6419 | `97aa60ceb42807c14d8325d37df1b7214e33e4ea10bf12af77178265b2eea2d2` |
| `plot.py` | 21996 | `2e568afc1a885f53efaa746db2f38505b959933fd66aa0fc5da1292e7d4f7918` |
| `progress.ndjson` | 454 | `2bb339341e80f76ae521df69b60dad528a3e6bb56161679632667b1af9f30640` |
| `qa-final-size.png` | 273796 | `47354a290de84d208f9db13b67a2cc2f68241f66adb83a2e6076f173c55fb450` |
| `qa-grayscale.png` | 109328 | `942a73f68ca439e28fc5274e7f55783b983a1d749359154971baee6ce47d724b` |
| `qa-pdf.png` | 219860 | `db89b9ae7ca155f4e33f5795484fa1bced84c2fabe2986c8f97283d293eb2bd4` |
| `qa-protocol.md` | 1083 | `409a75ae6c55e58df9a4f01d967143ef7bdbd2341999754dc4d59c63c07d5474` |
| `qa-report.md` | 1211 | `46574d494449c43e1dc91f18ff3129968181058c75a5fdaeec68ea82cd0201d0` |
| `qa-svg-quicklook.png` | 294701 | `872532e61707c751a3040fa769923813655335dbf3359631836b9b049d0bd57f` |
| `requirements.txt` | 46 | `71085db0ee325c2bc2ea2a7aaa8272b4a7a3c06170c50b76aa19ea6c259a124e` |
| `results.json` | 847 | `66b761a3ad005a651e63ef25659ec0c77f9c900074e17827631ea5bb7ec8b2bb` |
| `source-data.csv` | 1792 | `513bb7a6961b68bc7ec30e4dcc46314eb58924c0bd4eccb023c42911130b1e07` |
| `validate.py` | 30784 | `1369d62ec197448245e140355149e47e089d401d7f71b80a9ddf042386505e4d` |
| `validation.json` | 9236 | `00ff7b024f9bfc8ec181c98551e2d0382cf7ace7fddd93a8aefe37ee1f8a61c8` |

The 15 external bindings were independently recomputed from the repository,
not copied from the manifest:

| Bound source | SHA-256 |
|---|---|
| `research/r074o_problem_freeze.md` | `c461b85425e58ad0bb371bf7e1e6fe79301fd200912c67a15d4d8ebefb9ec54f` |
| `research/r074o_amplitude_endpoint_counterexample.md` | `471158de1db718ac96f38adc729464d8717006f47c8c6bb57834cc4e159bd9bb` |
| `research/r074o_amplitude_endpoint_independent_audit.md` | `44ad81c0623bbba006eac0aabc8fb9a77dccde4229c50061d78e59590c6bea22` |
| `research/r074o_final_source_rebind_audit.md` | `403dfe8e0b7c7cd74b68b23d74bb0da9f9d2064719a5a168eac5042868429484` |
| `research/r074o_gap_matrix.md` | `11aaae9308056cb2afa5b8d3166fbeecf9713aeb77e05bd5128fc3835231cdcd` |
| `research/r074o_amplitude_endpoint_certificate.json` | `30fd77ae3b4c88628e2d84207fc9b1728b1ab2343bf187fcd1141b080d6c5a5b` |
| `research/r074o_amplitude_endpoint_certificate_report.md` | `308453e68ec9ce2ef7b1e2a16d6faacbdc333fdfd5604417929fbca634db10fa` |
| `research/r074o_certificate_independent_audit.md` | `3ddc0e06ca8622c546a8e184f56efcc9bf7ca836b9cb476f11ef4e9e63476d47` |
| `scripts/r074o_amplitude_endpoint_certificate.py` | `3a01ab8659ed5a96bce92aa15df8190437f98522e935858d4e5840e629358671` |
| `scripts/r074o_amplitude_endpoint_certificate_independent.rb` | `562a13ebd3f66438919bccdd842fb2d2c5348f2c313fa071d39e878dd39d4062` |
| `research/r074o_report-source.md` | `c4e6363293e1a11d35d826a24b9d7bbf00e202ff9b31f1609e0ff99eb82330c3` |
| `research/r074o_bilingual_dictionary.md` | `9dfecf5ccfef88bf7ad2b63532c825078af5665aae0862679323a63a78424e87` |
| `research/r074o_reader_source_independent_audit.md` | `8bdcb2916c955fb9ae7e49d1156323271f38bb007c2933b5d2037721195cb07c` |
| `research/r074o_primary_literature_boundary.md` | `2925a699299b45d2d84da8ae182fdddbf94aac02195a6e7a02b93b37efce0708` |
| `research/r074o_primary_literature_independent_audit.md` | `85072caeb8c23fa17d163b8ab793d105541547f2e5c575f5cbdba4e7d1b08c14` |

The audit-chain text independently contains the current source hashes in all
14 expected source-to-audit edges: analytic proof/freeze/gap, final
rebind proof/freeze/gap, certificate/producer/independent checker, reader
proof/analytic-audit/report/dictionary, and literature boundary.  Their PASS
sentinels also preserve `FINITE ONLY`, the bounded non-hit rule, no novelty
inference, and `NOT CLAY`.

## 2. Independent exact-arithmetic reconstruction

I parsed all 24 CSV rows with exact rational arithmetic.  The row names are
unique, every decimal column agrees with its exact rational within
`5e-15`, and every declared proof location occurs exactly once as a tagged
equation in the bound proof.  The independent reconstruction gave 24/24
rows and 18/18 derived identities PASS.  In particular,

\[
 e_E=d_E-c_\gamma
 =\frac{98}{29475}-\frac8{3969}
 =\frac{17018}{12998475},
\]

\[
 m=\rho-\frac32c_\gamma
 =\frac{43}{423360}>0,
 \qquad
 \frac m3=\frac{43}{1270080},
\]

and

\[
 e_E-\frac{2m}{3}=\frac{1171}{943200}>0.
\]

For the velocity-cubic packet/background row, the independent power ledger
is

\[
 3\left(\frac23\right)-2=0,
 \qquad
 3\left(\frac m3\right)-\rho+\frac32c_\gamma=0,
\]

so the ratio is exactly one.  Replacing (L^{-2}) by (L^{-7/2})
gives the harmonic ratio (L^{-3/2}).  The payment exponents are
(B^3R^3), while the observable ledger is
(\varkappa^2B^2LR^2).

Finally,

\[
 \delta_*=\frac{2m}{9\rho}=\frac{86}{11907},
 \qquad
 q_*=\frac23+\delta_*=\frac{8024}{11907},
\]

\[
 3\rho\delta_*=\frac{2m}{3},
 \qquad
 2\left(\frac23\right)+1=\frac73,
 \qquad
 \frac{7/3}{2}=\frac76,
 \qquad
 \frac76-\frac12=\frac23.
\]

These are precisely the energy reserve, G/H payment rows, realized scalar
frontier, and endpoint-ratio exponents displayed by Panels A--D.  No fitted
exponent or finite-precision asymptotic inference is present.

## 3. Renderer and validator audit

`plot.py` uses deterministic ReportLab vector primitives with
`rl_config.invariant = 1`, exact `Fraction` checks, fixed geometry, fixed
palette, and locally resolved DejaVu Sans regular/bold fonts.  It contains no
random generator, NumPy/SciPy solver, FFT, mesh, time step, sampled path, or
numerical fit.  The SVG builder embeds the exact two TTF payloads as data URLs;
the PDF builder records the narrow scope in metadata.  The displayed formulas
are literal analytic ledger statements, and I cross-checked every hard-coded
display string against the 24 exact rows, the proof tags, and the caption.

`validate.py` has 72 distinct check identifiers.  Inspection confirms that
they cover required inputs, the narrow claim boundary, independent analytic,
reader and literature prerequisites, exact rationals, raster dimensions and
modes, PDF/SVG vector structure and fonts, four-panel semantics, the caption,
all 15 external sources, finite certificate/audit chains, and forbidden
control bytes.  It explicitly leaves
`figure_package_independent_audit = EXTERNAL_SEPARATE_NOT_CLAIMED`; it does not
self-certify this file.  The internal `manual_visual_gate` is only a package
record, so I did not treat it as evidence; Section 5 below supplies the actual
independent visual inspection.

No code path widens the result beyond a scalar-payment-only no-go on the
frozen smooth exact family.

## 4. Isolated deterministic rebuild

I created a fresh temporary repository-shaped tree, copied the 26-file
package and only the 15 manifest-bound external inputs into their original
relative paths, and ran, in order,

```text
/Users/kasifa/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 plot.py
/Users/kasifa/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 validate.py
```

The isolated run reported `PASS 72/72; 24 package entries`.  The regenerated
tree had the same 26-file inventory, and every one of the 26 files compared
byte for byte with the sealed source package.  This includes the three
publication masters, all four QA derivatives, the runtime/progress records,
the validation/layout records, `manifest.json`, and `SHA256SUMS`.  The master
hashes reproduced exactly as

- SVG: `aab4bca1d44fa248d9e108312dfdfb933b835d524fe86b915beaf4f22f7475de`;
- PDF: `3ed235968190c828ed1dfbc3b97c2201ea32902a3a180caa3b11ef6bf0a8a5da`;
- PNG: `e5578383c4f982f6f2aed74397dbe80ea8369f987d97b058db20b40fcc7ff3b1`.

Thus the current outputs are reproducible under the recorded local runtime,
not merely compatible at the level of decoded pixels.

## 5. Independent vector, raster, and visual inspection

I inspected `figure.png`, `qa-final-size.png`, `qa-grayscale.png`,
`qa-pdf.png`, and `qa-svg-quicklook.png` directly.

### Raster surfaces

- publication PNG: 4205 by 2363 px, RGB, 599.9988 dpi;
- final-size QA: 1402 by 788 px, RGB, 199.9996 dpi;
- grayscale QA: 1402 by 788 px, mode `L`, 199.9996 dpi;
- independent PDF raster: 2103 by 1182 px, RGB, 299.9994 dpi;
- Quick Look SVG raster: 2103 by 2103 px, RGB.

The color master, final-size raster, grayscale raster, PDF raster, and SVG
Quick Look raster all retain Panels A--D, complete labels, exact rational
values, solid/dashed distinctions, and the two-root-plus-neutral hierarchy.
There is no clipping, overlap, missing glyph, detached label, broken outline,
or color-only distinction.  The Quick Look renderer places the landscape SVG
at the top of a square canvas and therefore leaves blank space below; the
complete 178 by 100 mm figure is intact, so this is a QA-renderer canvas
choice rather than a publication-master defect.

The previously borderline Panel-C boundary sentence is now 3.60 pt in the
PDF and is readable at actual final size and in grayscale:

> X lower comes from endpoint energy • no separate dissipation lower

The caption states the stronger full-language boundary: the lower bound for
(X_*) comes from endpoint energy, and no separate lower bound is proved for
its dissipation component.  Thus neither the panel nor the caption converts
the available dissipation upper bound into a false matching lower bound.

### PDF structure

The PDF is one unencrypted, unrotated PDF 1.4 page with identical MediaBox
and CropBox,

\[
 504.5669\times 283.4646\ {\rm pt}
 =177.99999\times100.00001\ {\rm mm}.
\]

An independent recursive resource walk found zero image XObjects and zero
form XObjects.  The content stream has zero `Do` calls and zero inline-image
`BI/ID/EI` operators; it contains live text and vector line/curve operators.
All 1282 visible characters use the embedded DejaVu Sans or DejaVu Sans Bold
subsets, each backed by an embedded `FontFile2`.  The unused Helvetica and
Times setup resources draw no visible character.  Visible text has about
14 pt left/right and 10--11 pt top/bottom clearance.  Metadata records the
title and author, deterministic 2000 timestamps, and the exact scope:
analytic schematic, no simulation or DNS, independent figure audit separate,
and `NOT CLAY`.

### SVG structure

The SVG declares 504.5669 by 283.4646 units with viewBox `0 0 504 283`.  It
contains 53 live text nodes, vector paths/rectangles/circles/polygons, zero
image nodes, two embedded TTF `@font-face` payloads, and zero external hrefs.
The two decoded font payload hashes match the recorded local DejaVu Sans
regular and bold files.  Quick Look renders both faces without substitution
or missing glyphs.

## 6. Claim-boundary inspection

The visible PDF and SVG each contain `varkappa` five times and contain no
standalone `kappa`.  The inherited proof's separate geometric constant
`\kappa=16` is not reused as the amplitude symbol.  Panel C and the caption
both preserve the endpoint-energy/dissipation boundary described above.

The figure footer and caption explicitly say:

- analytic schematic, not to scale;
- no DNS, simulation, fitted data, or sampled trajectory/path;
- `SCALAR-PAYMENT-ONLY NO-GO` on a smooth exact family;
- no singularity or universal replacement theorem is asserted; and
- `NOT CLAY`.

The bound proof explicitly leaves novelty and priority open, and the bounded
literature non-hit is not used as novelty evidence.  The figure therefore
does not inflate a narrow scalar-payment obstruction into a general
Navier--Stokes regularity, blow-up, priority, or Millennium-problem claim.

## Final disposition

The final R0.74O formal figure package is internally consistent,
cryptographically bound, exactly reproducible in the recorded environment,
visually legible at final size and in grayscale, vector-clean, and faithful
to the frozen mathematical boundary.  It is suitable for freezing and
publication as an analytic proof figure.

**PASS; SCALAR-PAYMENT-ONLY SCOPE; NO DNS OR SIMULATION; NO SEPARATE
DISSIPATION LOWER; NO NOVELTY OR PRIORITY CLAIM; NOT CLAY.**
