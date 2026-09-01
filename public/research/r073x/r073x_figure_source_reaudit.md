# Independent final re-audit of the R0.73X exterior-tail figure package

**Audit date:** 2026-09-01
**Repository inspected:** `/private/tmp/r073x-release-958b6b4`
**Package:** `figures/r073x/fig-r073x-exterior-tail-ledger/`
**Source/raw commit:** `161fd9d5ca3ebea55e34567188a0e152ee39ecfb`
**Metadata package commit:** `d11025bb124357c45c2f333bde1b21569b373aa5`

## 1. Conclusion

**PASS for the stated release scope.** I found no byte-integrity, Git-binding,
inventory, checksum, validator, format, runtime-provenance, plotted-data, or
claim-boundary discrepancy in the clean repository at the two pinned commits.

This conclusion is limited to the formal staged figure package and the claims
it actually makes. It does not independently prove a Navier-Stokes theorem,
an associated-pressure counterexample, epsilon regularity, global regularity,
or a Clay/Millennium conclusion. It also does not attest that the package has
been published to a remote Site; the manifest itself says
`publicationStatus=staged`.

## 2. Repository and two-commit topology

- `HEAD` was `d11025bb124357c45c2f333bde1b21569b373aa5` and `git status --short` was empty.
- `d11025bb124357c45c2f333bde1b21569b373aa5` has exactly one parent:
  `161fd9d5ca3ebea55e34567188a0e152ee39ecfb`.
- At the package path, the source/raw commit contains exactly 21 regular files:
  the 10 source files and 11 raw artifacts listed below. None of the four
  metadata files is present in that commit.
- The direct-child diff adds exactly the four metadata files and changes no
  source/raw file.
- The current package directory contains exactly 25 regular, non-symlink files.
  All 25 current byte streams equal the corresponding blobs at the package
  commit.

### Exact 10 source files

1. `README.md`
2. `caption.md`
3. `chart-contract-and-source-data.md`
4. `command.txt`
5. `config.json`
6. `contract.json`
7. `plot.py`
8. `qa-protocol.md`
9. `requirements.txt`
10. `validate.py`

### Exact 11 raw artifacts

1. `environment.json`
2. `figure.pdf`
3. `figure.png`
4. `figure.svg`
5. `progress.ndjson`
6. `qa-final-size.png`
7. `qa-grayscale.png`
8. `qa-pdf.png`
9. `resource-log.ndjson`
10. `results.json`
11. `source-data.csv`

### Exact 4 metadata files

1. `manifest.json`
2. `qa-report.md`
3. `validation.json`
4. `SHA256SUMS`

## 3. Independent reconciliation of all 21 manifest bindings

All paths in this table have the common prefix
`figures/r073x/fig-r073x-exterior-tail-ledger/`. For every row I separately
recomputed the current file size and SHA-256, resolved the source-commit Git
blob object ID, read the blob with `git show <commit>:<path>`, and compared the
blob bytes with the current bytes. `Manifest/current bytes` therefore shows
both values explicitly. Every row passed all four comparisons.

| Class | Path under package | Manifest/current bytes | SHA-256 (manifest = current) | Source-commit Git blob | Blob bytes = current |
|---|---|---:|---|---|---|
| source | `README.md` | 3328 / 3328 | `41df488eb0a8b75ac25d3d1f3a35e9d477e6cd16f51676329385f056d4b01b0c` | `7a37c96f644e0ef35eab9fa0a609d9fb5bc54e0c` | PASS |
| source | `caption.md` | 1184 / 1184 | `4e5d73b2d26a5573cefdebc947acbf9e3f1c2f6217a4aad5d5a9a7837071f806` | `7a09e4cea5712278a66c0226e6de1d88a02b9af9` | PASS |
| source | `chart-contract-and-source-data.md` | 2576 / 2576 | `086e4bf8c39a9e4664957128f7d984d84261c613eaf7dede06a9480c3d3f7110` | `cfdc01d3992ad932bd41af3c6c9aa41fd9743340` | PASS |
| source | `command.txt` | 1170 / 1170 | `a98fbc8ab25edafac9a82441776861183c79a977d2f0e523d1a1c2403b2819c5` | `9ba39d78c3347f93c21ac2ae67f51354a420e258` | PASS |
| source | `config.json` | 942 / 942 | `d46e9961cb1b94c73c1433bbbac00c36d6a83d58b880841ba84f673e4b9bca4f` | `012ef2ed00b57adf2bbae77e13ef6aff02ce14d4` | PASS |
| source | `contract.json` | 3420 / 3420 | `b3a58032639a8572785c55f82b8f40f9ff579252c4574251926f8ca1c8704ed3` | `54ef48ec1edd88910041e37fb60642ff28496e85` | PASS |
| raw | `environment.json` | 1066 / 1066 | `67902f4f1955fbdf150846b5e1cddd67c41345e61588e0bf4420ccfc191c95f0` | `121887ba0a2822d1d9112c498fa427df5ad6349c` | PASS |
| raw | `figure.pdf` | 36704 / 36704 | `19363b82c12ead447af6aac57a070d2f7accea99c3f3210b81b093ed532170db` | `8483eec6f066ce16f1fc4a962b023f95ae4c66e9` | PASS |
| raw | `figure.png` | 490622 / 490622 | `e5678bf73f52ffe67ab5838030632136ba91bef58e38024539af268f1fa200f4` | `2a6b1f2a2c49e9716df4bebfcab1b54b8d79122a` | PASS |
| raw | `figure.svg` | 100869 / 100869 | `60712de0c9cb8ae672086fe721c2f9d40a064aa0c71b2218f6ef7e90bd6b057e` | `e134871734d6854d6ebec4ab45d60a2887cc2e0a` | PASS |
| source | `plot.py` | 27308 / 27308 | `bb959a49209b5e5afacff0ad6fa8195c7114652b0ff0a5fe429a85307ea58303` | `4812a7ee8bba42383b93663c1d5b77707662a6f2` | PASS |
| raw | `progress.ndjson` | 602 / 602 | `c067e3bbc4cc5ec1ce82f1b45bd862e7078b09fc739fd85c4c36b80823ddbc01` | `2d75de46b353fda7f8efd6e0a6ceef0dd49bd7cb` | PASS |
| raw | `qa-final-size.png` | 383043 / 383043 | `7744db259e54c80bbc09b7a6ff2bf88bf0a953db5df5257982859d629b857a78` | `70b851cb5181ffd04ae1e02c26f6836797344a8c` | PASS |
| raw | `qa-grayscale.png` | 311701 / 311701 | `5f9a6f83c43fee8809fb7ba70b8de8b55591b44bc219bebe900f3bc9ea11c5e5` | `13a46e4e5190ad20b159442383d973ccc82529fa` | PASS |
| raw | `qa-pdf.png` | 214095 / 214095 | `aa5c33ed772f14bfea462cd8faa306785f523bcdf6d01dd2d2f0610e14ae5ede` | `5b94b7a16ce17dd851d744c117cfe7fb73d83b07` | PASS |
| source | `qa-protocol.md` | 2583 / 2583 | `be4fdb3efeef92793db66dcd4748d139f9da40fbff1c141b140f21c84dc5868c` | `62e9ac7cba786de3105ac3c304ee9523fbe594ef` | PASS |
| source | `requirements.txt` | 79 / 79 | `c0dfebb8e4ce0a39b1565a51b94cb2ad8adf09d7910be44490446710102cf92f` | `e7173c3a8a9d00bcbd2408a88d033594453fbf70` | PASS |
| raw | `resource-log.ndjson` | 102 / 102 | `3e1972608917f84f7e82c74d05e9c38c424d15c4b29ef00233cf98d805702546` | `fd4cec68c63412524b91e70c55feab4a1466226b` | PASS |
| raw | `results.json` | 1518 / 1518 | `83673eadfe0bddd39ee6cebeab9248287bf02fd7f867560671a5ce49994059f7` | `c30f9267fa6c58e9e2e0b290ab78ef9dd938b41a` | PASS |
| raw | `source-data.csv` | 15349 / 15349 | `564796804f6942a474c7e89e6bcb42498b95a025fe0c70d114098338da2cb911` | `3c6f4783513c7cef4903f573fff258ad969f9ef0` | PASS |
| source | `validate.py` | 38170 / 38170 | `75d8240aca91172ca69a5353dcc6135cbaa6b0be33d792203a042d8b3e0fce46` | `86174f08897bc6f54acae19fff8761b4687ae8f8` | PASS |

The manifest binding path set is exactly the 10-source plus 11-raw set above;
there are no duplicate, omitted, or extra binding paths.

## 4. Package-commit equality and metadata blobs

The 21 source/raw blob IDs at the package commit are inherited unchanged from
the direct parent. The following four current metadata files equal the four
new package-commit blobs. Together with the 21 rows above, this establishes
current-byte equality for all 25 files.

| Metadata path | Current bytes | Current SHA-256 | Package-commit Git blob | Blob bytes = current |
|---|---:|---|---|---|
| `manifest.json` | 16078 | `5151a8382e27ade9e54a884081c65d2d8f18f6c7654285152229f16e45ac164b` | `ff817eb57e440813fddc87441ba478f2ee6755f8` | PASS |
| `qa-report.md` | 2186 | `98e93ad21af2054dd3368d02b1904dcd3919581126ddf05276a62f4281603ab4` | `fa7c5a144f54764a32c9afaf46cad0f74c94d2c8` | PASS |
| `validation.json` | 10922 | `4d1b9ef364a2316caf4a9bf0057756cb6ec9f39673f40ea3bdb17e6c5c3350e0` | `7e6275b4c7f31430c70270a505f3d53f130a26cf` | PASS |
| `SHA256SUMS` | 1933 | `28e5b3124e8cc085ab0d5834f7389e0c107e80688c1748485e8073cba21c9ead` | `50b5e1093b186e138ac642d4257e250658228ef9` | PASS |

## 5. `SHA256SUMS`

I parsed 24 unique, lowercase SHA-256 entries. Their path set is exactly every
package file except `SHA256SUMS` itself: the 21 source/raw files plus
`manifest.json`, `qa-report.md`, and `validation.json`. There are no duplicate,
missing, extra, or self-referential entries. Independent recomputation matched
all 24 digests, and `shasum -a 256 -c SHA256SUMS` returned `OK` for every
entry.

## 6. Validators and portability check

The required verify-only invocation used the fixed certified dependency path:

```text
PYTHONPATH=/Users/kasifa/.cache/codex-runtimes/r073s-figure-python \
/Users/kasifa/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
-B figures/r073x/fig-r073x-exterior-tail-ledger/validate.py \
--repository /private/tmp/r073x-release-958b6b4 --verify-only
```

It exited 0 with `status=PASS`, `checks=50`, 21 figure-source bindings, 24
checksum entries, 13 manifest hash records, and four source-evidence bindings.

I separately changed the verifier's `PYTHONPATH` string to
`/private/tmp/r073x-portability-sentinel:/Users/kasifa/.cache/codex-runtimes/r073s-figure-python`.
That invocation also exited 0 with the same 50/50 result. This confirms that
verify-only no longer requires literal equality between the live verifier's
absolute path string and the certified-run path string. This is a focused
portability test, not a claim that every possible host environment was tested.

The repository-wide command
`research/validate_figure_package.py figures/r073x/fig-r073x-exterior-tail-ledger`
exited 0 and returned `errors=[]` and `warnings=[]`.

## 7. Runtime provenance

`environment.json`, `manifest.json`, and the reconstructed validation record
agree on the certified run:

- Python 3.12.13, recorded executable
  `/Users/kasifa/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`.
- Recorded `PYTHONPATH`:
  `/Users/kasifa/.cache/codex-runtimes/r073s-figure-python`.
- Recorded imports for Matplotlib and NumPy are absolute paths under that
  recorded `PYTHONPATH` root.
- Pinned and live versions both equal: Matplotlib 3.10.6, NumPy 2.5.2,
  Pillow 12.3.0, pypdf 6.10.0, and pypdfium2 5.13.0.
- The fixed verifier resolved the executable to `python3.12` and imported
  Matplotlib and NumPy from the recorded dependency root.
- The provenance record declares one process, one thread per process, no GPU,
  no network, `dgxUsed=false`, and `ordinaryTranslationPath=LOCAL_DIRECT_NO_DGX`.

The last item is a recorded run declaration; this re-audit did not reconstruct
historical OS telemetry. The static internal path checks, live package-version
checks, bound environment bytes, and successful alternate-path verification
are the evidence available in this package.

## 8. PDF, PNG, SVG, fonts, hashes, and visual inspection

| Output | Dimensions | Font result | Bytes | SHA-256 |
|---|---|---|---:|---|
| `figure.pdf` | 1 page; MediaBox 504.5669291339 x 260.7874015748 pt = 178 x 92 mm | 3/3 referenced Type0 fonts embedded: subset DejaVu Sans, DejaVu Sans Oblique, DejaVu Sans Bold | 36704 | `19363b82c12ead447af6aac57a070d2f7accea99c3f3210b81b093ed532170db` |
| `figure.png` | 4204 x 2173 px; RGBA; 599.9988 x 599.9988 dpi metadata | raster output; no embedded-font resource concept | 490622 | `e5678bf73f52ffe67ab5838030632136ba91bef58e38024539af268f1fa200f4` |
| `figure.svg` | 504.566929 x 260.787402 pt; viewBox `0 0 504.566929 260.787402` | text references DejaVu Sans families; no remote HTTP(S) links | 100869 | `60712de0c9cb8ae672086fe721c2f9d40a064aa0c71b2218f6ef7e90bd6b057e` |

I rendered the one-page PDF independently with Poppler and inspected that
raster together with `qa-final-size.png` and `qa-grayscale.png`. I found no
clipped title, panel label, axis label, tick, legend, annotation, formula, or
footer; no visible collision; and no PDF/PNG layout discrepancy. The
solid/dashed lines, filled/open markers, and circle/square/triangle distinctions
remain legible in grayscale. Panels A and B visibly include the `10^0` major
tick. Panel A retains the prefactor values above one; Panel B is normalized at
`m=1`. The stored validator also independently reproduces the final-size,
grayscale, and PDF QA rasters exactly and reports no artist-bounds failure.

## 9. Source evidence and independent data reconstruction

The four evidence files are byte-identical between source-evidence commit
`958b6b4216f6914a5d42f7712b6bc9b218caf801` and the current clean tree, and
their independently recomputed hashes and sizes match both `contract.json` and
the four manifest `sourceData` records:

| Evidence path | Bytes | SHA-256 |
|---|---:|---|
| `research/r073x_exterior_tail_freeze.md` | 29534 | `f16b610b9d264ed912bbeeb70df36b6ccd50dbfbda52f7fdc2344f8869a78a20` |
| `research/r073x_gaussian_tail_certificate.json` | 24832 | `136b40fb6d30d4fd671e5dc3049817266986f595da46e9a6b6a31a409fe3f836` |
| `research/r073x_gaussian_tail_independent_audit.md` | 14075 | `9ecbc927a25eb95c23604bfbe85c1c633a83cd4765d1405d626ea006ef9a706a` |
| `research/r073x_pressure_tail_independent_audit.md` | 24912 | `ac1cb3c26f2d51ecf529dd29d180b6c40af911f6fbe665577d9be574c3cb241b` |

I reconstructed all 46 `source-data.csv` records independently from those
bound sources and obtained exact binary64 equality:

- **Panel A:** 21 analytic-formula coordinates, for
  $\theta\in\{1,1/2,1/4\}$ and $m=1,\ldots,7$, from
  $\gamma_m(\theta)=\theta^{-2}\exp[-4^{m-1}/(32\theta)]$.
- **Panel B:** 14 analytic-formula coordinates. The $\theta=1$ Gaussian row
  and $(2^mR)^{-4}$ pressure-tail row were each divided by their value at
  $m=1$. The $R$ factor cancels in the normalized pressure shape. Both rows
  start at one, but the package correctly says they pay different quantities
  and are not interchangeable.
- **Panel C:** 10 normalized series points plus one ratio annotation, read from
  all five certificate `packet_concentration.numeric_rows` without
  interpolation. Weighted $L^3$ was divided by its $\delta=1/4$ value and the
  weighted-$L^2$-to-$3/2$ proxy by its own $\delta=1/4$ value. The smallest
  stored ratio is exactly `299.3965269759089`.

The certificate records limiting powers $3$, $9/2$, and $-3/2$ for weighted
$L^3$, the weighted-$L^2$ proxy, and their ratio. Its last finite slopes are
approximately `2.9998571`, `4.4997821`, and `-1.4999250`. These are static
packet quadrature diagnostics, not fitted measurements and not a time-stepped
PDE computation.

## 10. Claim-boundary audit

The visual itself says `analytic formula` on Panels A and B, `static functional
diagnostic` and `NOT DNS` on Panel C, `not interchangeable` for the Panel B
comparison, and `NOT CLAY` in the footer. The caption, README, contract,
manifest, results, QA report, and certificate are consistent with those labels.

In particular, the package claims only an unconstrained static,
velocity-functional obstruction for Panel C. It does **not** claim:

- DNS or any Navier-Stokes simulation;
- that the packet is an unforced NSE trajectory;
- an associated-pressure counterexample or an NSE-trajectory counterexample;
- compact-cutoff absorption or signed-to-absolute coercivity;
- epsilon regularity or global regularity; or
- a Clay/Millennium solution.

The machine-readable boundary has `associatedPressureCounterexample=false`,
`navierStokesSimulation=false`, `dns=false`, `epsilonRegularity=false`,
`globalRegularity=false`, `clayProblemSolved=false`, and `notClay=true`.
Accordingly, I accept Panel A and Panel B as frozen analytic-formula displays
and Panel C only as the declared static functional diagnostic, not as DNS or a
Navier-Stokes counterexample.

## 11. Final assessment

Within the local clean repository and pinned commits, the package is a
coherent formal figure-source seal: exact 10/11/4 inventory, direct parent-child
split, 21/21 source/raw Git bindings, 25/25 package-commit byte equality,
24/24 checksum entries, 50/50 verify-only checks under both tested environment
strings, zero generic-validator errors or warnings, internally consistent
runtime provenance, verified output dimensions/fonts/hashes, exact plotted-data
reconstruction, and an appropriately narrow claim boundary.

**FINAL_REAUDIT_VERDICT=PASS_WITHIN_DECLARED_FIGURE_SCOPE**
