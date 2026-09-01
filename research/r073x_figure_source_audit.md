# R0.73X formal figure-source audit

**Figure:** `fig-r073x-exterior-tail-ledger`

**Audit date:** 2026-09-01

**Audit target:** clean worktree `/private/tmp/r073x-release-958b6b4`

**Verdict:** `FORMAL PASS / PORTABLE TWO-COMMIT SEAL VERIFIED`

**DGX used:** `false`

This is the source-owner's read-only audit of the final 25-file figure package.
It verifies the two-commit transaction, all immutable source/raw bindings,
all current package bytes, the checksum inventory, executable validation,
portable runtime-provenance semantics, and the mathematical claim boundary.
It is not a new proof or a re-audit of the underlying R0.73X lemmas.
`NOT DNS`. `NOT CLAY`.

## 1. Formal commit graph

The final package has the required direct parent/child relation:

```text
source/raw commit  161fd9d5ca3ebea55e34567188a0e152ee39ecfb
package child      d11025bb124357c45c2f333bde1b21569b373aa5
```

Read-only Git inspection gives

```text
d11025bb124357c45c2f333bde1b21569b373aa5^
= 161fd9d5ca3ebea55e34567188a0e152ee39ecfb
```

The audited worktree has `HEAD` at the package child and an empty
`git status --short`. The parent freezes the 21 authored source/raw artifacts;
the child adds the four final metadata files: `validation.json`,
`manifest.json`, `qa-report.md`, and `SHA256SUMS`.

## 2. Immutable bindings and package bytes

`manifest.json.seal.figureSourceBindings` has exactly 21 entries. For every
entry this audit required:

1. current bytes equal the corresponding source/raw-commit blob;
2. current SHA-256 equals the stored binding digest;
3. the source/raw-commit Git blob ID equals the stored blob ID; and
4. the path belongs to the declared source/raw inventory.

All `21/21` bindings pass:

```text
README.md
caption.md
chart-contract-and-source-data.md
command.txt
config.json
contract.json
environment.json
figure.pdf
figure.png
figure.svg
plot.py
progress.ndjson
qa-final-size.png
qa-grayscale.png
qa-pdf.png
qa-protocol.md
requirements.txt
resource-log.ndjson
results.json
source-data.csv
validate.py
```

Every one of the 25 current files was also compared byte-for-byte with the
corresponding blob at package child `d11025bb...`; all `25/25` pass. The package
contains no extra, untracked, symlink, or special-file entries.

## 3. Checksums and executable validation

`SHA256SUMS` has exactly 24 entries, covering every package file except itself.
`shasum -a 256 -c SHA256SUMS` returns `OK` for all `24/24` entries.

The final executable checks return:

```text
validate.py --verify-only, certified PYTHONPATH    PASS, 50/50
validate.py --verify-only, altered PYTHONPATH      PASS, 50/50
figureSourceBindings                               21
manifestHashRecords                                13
sha256SumsEntries                                  24
sourceDataBindings                                 4
generic figure validator                           errors=[], warnings=[]
owner final-size visual review                     PASS
```

The two verify-only invocations used different literal `PYTHONPATH` strings;
the second prepended `/private/tmp/r073x-portable-audit` while retaining the
certified dependency directory. Both passed `50/50`. This confirms that
verification is not coupled to live equality with the original certified-run
absolute path string.

The authoritative child state is:

```text
status=formal
publicationStatus=staged
seal.state=formal-figure-source-seal
seal.figureSourceCommit=161fd9d5ca3ebea55e34567188a0e152ee39ecfb
seal.figureSourceCommitBound=true
seal.upgradeRequired=null
```

The README lifecycle text is no longer stale: it distinguishes the state
before the final reseal from the current lifecycle state carried by
`manifest.json` and `validation.json`.

## 4. Runtime provenance and portability boundary

The certified rendering run records:

```text
python=/Users/kasifa/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3
PYTHONPATH=/Users/kasifa/.cache/codex-runtimes/r073s-figure-python
matplotlib=/Users/kasifa/.cache/codex-runtimes/r073s-figure-python/matplotlib/__init__.py
numpy=/Users/kasifa/.cache/codex-runtimes/r073s-figure-python/numpy/__init__.py
```

The `runtime-provenance` validator checks the internal consistency of that
static certified-run record. It does not require a verifier on another machine
to reproduce those literal absolute paths. Live verification separately checks
the pinned Python-package versions through `dependency-versions`; that check
passes. The two-PYTHONPATH test above confirms the intended portability
boundary. No GPU, network service, or DGX result supports the figure.

## 5. Formula/source-data-to-glyph map

The 46-row `source-data.csv` is reconstructed from four frozen evidence
bindings at evidence commit
`958b6b4216f6914a5d42f7712b6bc9b218caf801`:

| Panel / glyph | Formula or audited source | Evidence class |
|---|---|---|
| A, three line/marker series | \(\gamma_m(\theta)=\theta^{-2}\exp[-4^{m-1}/(32\theta)]\), parsed from `r073x_exterior_tail_freeze.md` | `analytic formula` |
| B, blue solid circles | Gaussian factor normalized at \(m=1\) | `analytic formula` |
| B, gold dashed squares | \((2^mR)^{-4}\), normalized to \(2^{-4(m-1)}\) | `analytic formula` |
| B, boxed warning | Gaussian and harmonic-pressure rows pay different quantities | interpretation boundary |
| C, blue solid circles | audited `weighted_L3` packet rows, normalized at \(\delta=1/4\) | `static functional diagnostic` |
| C, gold open squares | audited `weighted_L2_to_three_halves` rows | `static functional diagnostic` |
| C, ratio annotation | certified smallest-scale ratio `299.3965269759089` | static annotation, not a fit |

The renderer parses the Gaussian denominator `32` and algebraic exponent `4`
from the proof text rather than trusting configuration alone. Panel C requires
certificate payload
`fcac97440dde87d00103f3a09b346bdd918c9fbb7360ee792edc2c8d0357e3b7`
and the independent verdict `PASS WITH THE ORIGINAL CLAIM BOUNDARY`.

Panels A and B explicitly show the \(10^0\) major tick. Panel A keeps
`yMaximum=40`, above the largest raw \(\theta^{-2}\)-weighted point
`14.119950441353527`; Panel B is explicitly normalized at \(m=1\). Final-size,
grayscale, and PDF QA show no clipping or collision. Solid/dashed/dotted lines
and filled/open circle/square/triangle markers remain distinguishable without
color. The owner visual review is `PASS`.

## 6. Mathematical claim boundary

The final manifest retains all required negative scope flags:

```text
associatedPressureCounterexample=false
navierStokesSimulation=false
dns=false
fittedScalingLaw=false
compactCutoffAbsorptionResolved=false
epsilonRegularity=false
globalRegularity=false
clayProblemSolved=false
panelBRowsInterchangeable=false
notClay=true
```

Panel B compares normalized decay shapes only; it does not identify or order
the complete Gaussian and harmonic-pressure functionals. Panel C is a smooth,
static, divergence-free velocity-packet diagnostic. It refutes only the stated
unconstrained velocity-only functional replacement of the critical weighted
\(L^3\) row by weighted \(L^2\) mass raised to \(3/2\). It is not an unforced
Navier--Stokes trajectory and does not provide its associated pressure.

No signed-to-absolute coercivity, compact-cutoff absorption, tent/Carleson
estimate, suitable-weak zero-scale endpoint, epsilon regularity, blow-up
exclusion, arbitrary-data global regularity, or Clay conclusion follows.

## 7. Final digests

The current formal child bytes have these principal SHA-256 digests:

```text
41df488eb0a8b75ac25d3d1f3a35e9d477e6cd16f51676329385f056d4b01b0c  README.md
a98fbc8ab25edafac9a82441776861183c79a977d2f0e523d1a1c2403b2819c5  command.txt
bb959a49209b5e5afacff0ad6fa8195c7114652b0ff0a5fe429a85307ea58303  plot.py
75d8240aca91172ca69a5353dcc6135cbaa6b0be33d792203a042d8b3e0fce46  validate.py
67902f4f1955fbdf150846b5e1cddd67c41345e61588e0bf4420ccfc191c95f0  environment.json
19363b82c12ead447af6aac57a070d2f7accea99c3f3210b81b093ed532170db  figure.pdf
e5678bf73f52ffe67ab5838030632136ba91bef58e38024539af268f1fa200f4  figure.png
60712de0c9cb8ae672086fe721c2f9d40a064aa0c71b2218f6ef7e90bd6b057e  figure.svg
5151a8382e27ade9e54a884081c65d2d8f18f6c7654285152229f16e45ac164b  manifest.json
4d1b9ef364a2316caf4a9bf0057756cb6ec9f39673f40ea3bdb17e6c5c3350e0  validation.json
98e93ad21af2054dd3368d02b1904dcd3919581126ddf05276a62f4281603ab4  qa-report.md
28e5b3124e8cc085ab0d5834f7389e0c107e80688c1748485e8073cba21c9ead  SHA256SUMS
```

The source audit itself is maintained outside the Site checkout and is not one
of the sealed package's 25 files. This audit did not alter the clean checkout.

The package is source/raw-commit-bound, metadata-child-sealed, reproducibly
verifiable under the declared dependency contract, visually reviewed, and
mathematically scoped. `FORMAL PASS`. `NOT DNS`. `NOT CLAY`.
