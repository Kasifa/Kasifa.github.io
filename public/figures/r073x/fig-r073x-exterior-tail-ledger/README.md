# R0.73X exterior-tail ledger figure

This directory is the reproducible 178 mm by 92 mm three-panel journal figure
package for `fig-r073x-exterior-tail-ledger`.

Panels A and B are sampled directly from the frozen analytic formulas for the
Gaussian heat tail and the algebraic harmonic-pressure tail.  Panel C reads
the five deterministic packet-quadrature rows from the independently audited
Gaussian certificate.  The renderer refuses source-hash drift, missing formula
tokens, a widened claim boundary, or a stale certificate payload.

The figure is a formula/evidence ledger.  It is not DNS, an NSE trajectory, a
fit, or an empirical turbulence result.  The packet in Panel C is a smooth
static divergence-free functional diagnostic; it does not carry associated
pressure and is not asserted to solve unforced Navier--Stokes.

## Reproduce

Use the exact Python packages in `requirements.txt`:

```text
python3 -B plot.py --repository /path/to/repository --render-preseal
python3 -B validate.py --repository /path/to/repository --confirm-visual-qa
python3 -B validate.py --repository /path/to/repository --verify-only
python3 -B /path/to/repository/research/validate_figure_package.py .
shasum -a 256 -c SHA256SUMS
```

After committing exactly the ten source files and eleven raw artifacts (and no
metadata files), upgrade the prepublication seal to the immutable figure-source
seal with that commit's full lowercase 40-hex object name:

```text
python3 -B validate.py --repository /path/to/repository \
  --figure-source-commit <full-40-hex-figure-source-commit> \
  --confirm-visual-qa
python3 -B validate.py --repository /path/to/repository --verify-only
```

The formal command fails unless all 21 bound files are byte-identical to their
Git blobs and their exact scoped status is clean.  It changes only
`validation.json`, `manifest.json`, `qa-report.md`, and `SHA256SUMS`; those four
metadata files belong in a separate reseal commit.  `--verify-only` reads the
stored seal, independently reconstructs every binding from Git, and then
reconstructs the complete validation-check list before accepting the package.

`environment.json` records the Python executable, the `PYTHONPATH` used for
the certified run, and the resolved matplotlib and NumPy import locations.
`command.txt` preserves that exact local invocation.  On another machine,
install `requirements.txt` into a clean environment and point
`R073X_FIGURE_PYTHON` at its Python; set `R073X_FIGURE_PYTHONPATH` only when
the dependencies live outside that environment's ordinary import path.

Before the final reseal, the staged metadata is a hash-bound prepublication
artifact.  Source evidence is bound to immutable research commit
`958b6b4216f6914a5d42f7712b6bc9b218caf801`; the 21 figure source/raw files
then receive their own immutable commit.  The current lifecycle state is
carried by `manifest.json`, `validation.json`, `qa-report.md`, and
`SHA256SUMS`, which are intentionally written only after that source commit.
A final seal has `schemaVersion=research-figure-manifest-v1`,
`figureSchemaVersion=r073x-exterior-tail-ledger-manifest-v1`, `release=R0.73X`,
`status=formal`, `publicationStatus=staged`, and
`seal.state=formal-figure-source-seal`.  No public mirror is created by this
package.

No GPU, network service, or DGX was used.  `NOT CLAY`.
