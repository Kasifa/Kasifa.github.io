# R0.73W signed-production figure source

This directory is the reproducible source and artifact package for
`fig-r073w-signed-production`, a 178 mm by 126 mm four-panel journal figure.

Panels A--B render audited analytic identities and upper-bound envelopes.
Panels C--D render the exact rank-three witness only after the primary
`results.json` and independently implemented `independent-results.json` have
identical complete `commonCore` objects and match the hashes frozen in
`contract.json`.  The finite certificate is sealed to source commit
`b9f3b394...` and package commit `68893ecc...`.  All sampled curves are
deterministic coordinates of displayed closed formulas.  They are not
observations and are never fitted.

The package is deliberately a **hash-bound prepublication artifact seal**.
The R0.73W finite certificate is immutable and commit-bound.  The new figure
sources and raw artifacts are not yet immutable Git blobs, and this task does
not create a commit.  `manifest.json` therefore stays truthfully at
`status=draft` while recording passed journal-output QA and the current
repository state.  A later release transaction may commit the figure
source/raw files, then reseal the figure metadata against that commit.

## Reproduce

Use Python 3.12 with the exact versions in `requirements.txt`.  The `--deps`
switch is optional when those packages are installed normally:

```text
python3 -B plot.py --deps <python-packages> --render-preseal
python3 -B validate.py --deps <python-packages> --confirm-visual-qa
python3 -B validate.py --deps <python-packages> --verify-only
python3 -B ../../../research/validate_figure_package.py .
shasum -a 256 -c SHA256SUMS
```

After committing exactly the ten source files and eleven raw artifacts (and no
metadata files), upgrade the prepublication seal to the immutable figure-source
seal with the resulting full lowercase 40-hex commit:

```text
python3 -B validate.py --deps <python-packages> \
  --figure-source-commit <full-40-hex-figure-source-commit> \
  --confirm-visual-qa
python3 -B validate.py --deps <python-packages> --verify-only
```

The final command fails unless all 21 bound files are byte-identical to their
Git blobs and their exact scoped status is clean.  It changes only
`validation.json`, `manifest.json`, `qa-report.md`, and `SHA256SUMS`; those four
metadata files belong in a separate reseal commit.

The local build used the bundled dependency directory recorded in
`environment.json`.  No GPU, network service, DGX system, or external
translation service is used.  Ordinary translation follows
`LOCAL_DIRECT_NO_DGX`; `dgxUsed=false`.

## Evidence boundary

Panel A is a signed spatial-mean endpoint identity.  Panel B shows only the
shape of unconditional energy-class upper bounds.  Panels C--D are exact finite
Fourier counterexamples.  None is a Navier--Stokes simulation, a genericity or
minimality claim, a singular solution, an improved regularity criterion, global
regularity, or a Clay conclusion.  `NOT CLAY`.
