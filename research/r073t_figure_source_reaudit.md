# R0.73T formal-figure source re-audit

**Audited directory:**
`research/figures/r073t/fig-r073t-dynamic-autocorrelation/`

**Audit mode:** independent, read-only review of the revised ten source files
and the current local rerender; exact row and pixel reconstruction in a
temporary directory; no figure-source edit, Git commit, network, GPU, or DGX

**Verdict:** `ONE_VISUAL_BLOCKER_REMAINS`

The mathematics, 28-row provenance split, 105-check arithmetic, 23/24 sealed
inventories, external analytic-proof binding logic, explicit certificate
sealer call, initial-time labels, and the implemented exact pixel comparisons
are now internally correct.  The old outer-edge clipping and the overclaiming
main title are repaired.  The render is nevertheless not ready for positive
visual confirmation: each panel title overlaps its subtitle, quantitatively
and visibly in both the PNG and PDF raster.  The provenance final-seal run is
not assessed as a failure here because the ten figure sources, analytic proof,
and certificate package have deliberately not yet received their source
commit.

## 1. Disposition of the three previous blockers

| Previous blocker | Second-round result | Evidence |
| --- | --- | --- |
| clipped/overclaiming visual language | **partly repaired; still blocked** | “one upper estimate” replaces “upper closure”; the Panel A box label fits; no text bounding box lies outside the canvas.  However all three title/subtitle pairs overlap. |
| Panel A falsely attributed to the finite certificate | **repaired** | the four Panel A rows use `source_origin=r073t-analytic-proof`; Panels B/C retain `r073t-exact-certificate-results`; the external analytic proof is a separately declared source-commit binding. |
| figure validator trusted certificate-manifest booleans | **repaired in source** | the validator invokes `seal_package.py --source-commit <same-commit> --check-only` and requires a zero return code after checking the certificate and figure share the same full commit. |

Thus two source/provenance blockers are closed.  The visual blocker has changed
from outer clipping to title/subtitle collision and has not disappeared.

## 2. Mathematical and claim-boundary readback

The displayed Panel A chain remains correct.  With

\[
 X^2=\|\nabla |u|^2\|_2^2,
 \qquad
 Y=\int |u|^2|\nabla u|^2,
\]

the exact balance is

\[
 Q'+4\nu Y+2\nu X^2
 =4\int p\,u\mathbin\cdot\nabla |u|^2.
\]

The periodic pressure estimate and Young choice

\[
 a=\sqrt\nu X,
 \qquad
 b=2C_R\nu^{-1/2}\|u\|_6^3
\]

give

\[
 4\left|\int p\,u\mathbin\cdot\nabla |u|^2\right|
 \le \nu X^2+{4C_R^2\over\nu}\|u\|_6^6.
\]

Combining this with \(\|u\|_6^6\le AQ\) yields exactly the plotted
one-sided inequality

\[
 Q'+4\nu Y+\nu X^2
 \le {4C_R^2\over\nu}AQ.
\]

For Panel B, the rotating shear has
\(C(h,0)=\delta_{h0}\) and
\(|\dot C_0(0)|/(2\nu)=N^2\).  For Panel C, the full initial derivatives
are

\[
 Q'(u_L;0)=-16536\nu L^2-384L,
 \qquad
 Q'(-u_L;0)=-16536\nu L^2+384L.
\]

The plotted centered values are therefore exactly \(-384L\) and \(+384L\).
The signs, factor 16536, and description “common viscosity removed” agree
across the figure, caption, contract, CSV, and analytic proof.

The revised language also respects the result boundary:

- the main title says “one upper estimate,” not “closure”;
- Panel C says “signed pairing phase,” which is what the sign pair detects;
- the caption says exact analytic/rational reconstruction, not simulation;
- the contract keeps simulation, fitting, singularity, improved criterion,
  global regularity, and Clay flags false;
- the footer explicitly says `NOT CLAY`.

## 3. Exact 28-row provenance reconstruction and initial time

The current CSV and a fresh temporary rerender agree byte for byte.  Its rows
split as

\[
 4\ \text{analytic-chain rows}
 +8\ \text{rotating-shear rows}
 +16\ \text{six-mode sign-pair rows}
 =28.
\]

The former provenance defect is repaired rather than relabelled cosmetically:

- Panel A's four rows are labelled `r073t-analytic-proof` and the contract
  points to `research/r073t_dynamic_autocorrelation_budget.md`;
- Panels B/C's 24 rows are labelled
  `r073t-exact-certificate-results` and the contract points to
  `research/certificates/r073t/results.json`;
- `validate.py` rebuilds the same split independently, field by field.

The initial-time scope also passes.  Panel B visibly says
`at t=0`, Panel C visibly says `same C at t=0`, its ordinate is
\(Q'(0)+16536\nu L^2\), and the caption states `at t=0` for both witness
families.  The chart contract and CSV formulas retain the same restriction.

## 4. The 105-check count

`EXPECTED_CHECK_COUNT = 105` is now enforced by a final check whose own
inclusion is pinned through `len(checks) + 1 == 105`.  Independent expansion
of every fixed and loop-generated check gives

| Check class | Count |
| --- | ---: |
| fixed source, certificate, schema, claim, result, and environment checks before dependencies | 22 |
| exact dependency-version checks | 5 |
| CSV schema and row-count checks | 2 |
| 28 exact-row checks plus 28 finite-coordinate checks | 56 |
| PNG format, dimensions, and color | 3 |
| three QA-image validity checks | 3 |
| grayscale mode and exact-pixel checks | 2 |
| regenerated PDF-raster exact-pixel check | 1 |
| PDF page and media-box checks | 2 |
| SVG root, title, default-palette exclusion, and required roots | 4 |
| three primary-output size checks | 3 |
| human visual confirmation gate | 1 |
| check-count pin itself | 1 |
| **Total** | **105** |

The IDs produced by these fixed and indexed loops are distinct.  A removed
check now changes the total and fails before validation metadata can be
sealed.

## 5. The 23/24 inventory pins

The final package arithmetic is now both declared and checked:

| Class | Pinned count |
| --- | ---: |
| ten source files | 10 |
| raw generated files | 11 |
| metadata files | 4 |
| complete package | 25 |
| manifest-bound files: source + raw + validation + QA report | 23 |
| SHA256SUMS lines: 23 files + `manifest.json` | 24 |

`validate.py` adds explicit checks for 23 manifest-bound files and 24 SHA
lines, and `main()` independently requires the generated sums text to contain
exactly 24 nonempty lines.  This closes the former unpinned-inventory gap.

The current local directory contains the ten sources and eleven raw outputs,
but not the four final metadata files.  That is the expected pre-seal state,
not a 23/24 failure; the final inventory can only be materialized after a
source commit is assigned.

## 6. External analytic proof and certificate-sealer binding

The revised validator requires a full lowercase 40-hex commit and checks that
the commit resolves.  It then obtains Git blob bytes for

1. all ten figure-source files; and
2. `research/r073t_dynamic_autocorrelation_budget.md`;

and requires every committed blob to equal the corresponding working-tree
bytes.  The returned source-binding inventory is pinned at eleven.  This is a
real byte binding of the external analytic proof, not merely a path recorded
in JSON.

The certificate path is also materially stronger.  The validator:

1. reruns `compute_exact_certificate.py --check-only`;
2. requires the certificate manifest to be final sealed;
3. requires the certificate and figure to name the same full source commit;
4. actually runs
   `seal_package.py --source-commit <same-commit> --check-only`; and
5. requires that subprocess to return zero.

The current certificate pre-seal independently passes 55/55 exact checks and
its no-commit `seal_package.py --check-only` pass.  Probes against current
`HEAD` fail nonzero because the new sources are not in that commit, as a
fail-closed validator should.  The final same-commit run is intentionally left
to the later source-commit/seal stage and is not represented here as already
executed.

One workflow clarification remains advisable: neither `README.md` nor
`command.txt` lists the command which first converts the certificate pre-seal
to its full-commit final seal.  The figure validator only checks that final
seal; it does not create it.  Adding the explicit certificate final-seal
command before figure validation would make the published reproduction order
self-contained.

## 7. Current rerender and exact pixel comparisons

A fresh temporary render from the revised source produced byte-identical
copies of the current

- `source-data.csv`;
- `figure.png`;
- `qa-final-size.png`;
- `qa-grayscale.png`; and
- `results.json`.

Its PDF raster was also pixel-identical to the current PDF raster.  Current
dimensions are

| Artifact | Dimensions |
| --- | ---: |
| 600 dpi PNG | 4204 x 2362 |
| final-size QA raster | 1800 x 1011 |
| grayscale QA raster | 1800 x 1011 |
| PDF QA raster at scale 2.5 | 1262 x 709 |

Independent readback gave all three relevant derivation results as true:

1. rebuilding the 1800 x 1011 thumbnail from `figure.png` exactly matches
   `qa-final-size.png`;
2. explicit luminance conversion of `qa-final-size.png` exactly matches the
   mode-`L` `qa-grayscale.png`;
3. rerasterizing `figure.pdf` at scale 2.5 exactly matches `qa-pdf.png`.

The revised validator implements checks 2 and 3.  It validates the final-size
raster but does not itself implement check 1.  The present artifact passes
that independent comparison; binding it automatically would be an additional
hardening check rather than a correction of the current data.

## 8. Remaining visual blocker: title/subtitle collision

No visible text is now outside the Matplotlib canvas, so the original hard
right-edge clipping is repaired.  The current render nevertheless violates
the QA protocol's no-collision requirement.  The subtitle is placed at axes
coordinate `y=1.01` while each axes title occupies the same vertical band.
Renderer bounding-box intersections at the native 100 dpi canvas are

| Panel | Vertical overlap | Horizontal overlap |
| --- | ---: | ---: |
| A | 4.52 px | 157.25 px |
| B | 8.52 px | 130.62 px |
| C | 7.52 px | 144.88 px |

These are not just conservative bounding boxes: the merged strokes are
visibly apparent in the 600 dpi PNG, the final-size raster, the grayscale
raster, and the PDF raster.  Panel C's subtitle is additionally only about
1.04 px from the right canvas edge at 100 dpi, although it is not presently
clipped.

The equations, axes, zero line, legends, bottom boundary statement, and footer
otherwise fit.  The filled-square/solid line and hollow-circle/dashed line
remain clearly distinguishable in grayscale.

The figure must therefore not be run with `--confirm-visual-qa` yet.  The
minimal repair is to place the subtitles on a separate line with a positive
gap below the titles (and retain a safer right margin for Panel C), rerender,
and repeat the bounding-box plus color/grayscale/PDF readback.

## 9. Secondary fail-closed hardening

`validate.py` now rejects symlinks for all source and raw files, but the
top-level inventory test uses `path.is_file()` for metadata entries.  A
symlink to a regular file satisfies that predicate, and seal mode would then
write through it.  Requiring every package entry, including the four metadata
paths, to be a regular nonsymlink file when present would make the stated
fail-closed boundary complete.  No such metadata symlink is present in the
current pre-seal directory.

## 10. Release gate

The revised source passes the mathematical, source-row, claim, count,
inventory, binding-logic, initial-time, and current-artifact pixel audits.  It
should move to source commit and provenance sealing only after this remaining
visual condition is met:

1. remove all three title/subtitle overlaps and give the Panel C subtitle a
   non-marginal right clearance;
2. rerender and repeat PNG, grayscale, and PDF visual readback;
3. only then give positive manual visual confirmation and run the final
   certificate/figure same-commit seals.

No new PDE regularity result or Clay conclusion is inferred by this source
audit.
