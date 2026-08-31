# R0.73T formal figure source

This directory contains the immutable source and generated artifacts for
`fig-r073t-dynamic-autocorrelation`.

The figure is based only on the exact analytic R0.73T identities and the
standard-library `Fraction` certificate in
`research/certificates/r073t/`.  It uses no simulation, regression, network
service, GPU, or DGX.

## Reproduce

Use an isolated Python environment satisfying the exact versions in
`requirements.txt`.  The repository does not vendor those packages.  Either
activate that environment or pass its site-packages directory as `--deps`:

```text
python3 plot.py --deps <python-packages> --render-preseal
python3 validate.py --deps <python-packages> --source-commit <full-commit> --confirm-visual-qa
python3 validate.py --deps <python-packages> --source-commit <full-commit> --verify-only
```

The tested local run used interpreter
`/Users/kasifa/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`
with package directory
`/Users/kasifa/.cache/codex-runtimes/r073s-figure-python`; the generated
`environment.json` records the actual interpreter and five package versions.
This machine-specific pair is not required when an equivalent isolated
Python 3.12 environment is active.

The source commit must contain byte-identical copies of the ten declared
figure-source files and the external analytic proof.  Validation reruns the
exact certificate producer and its source-commit seal, and fails closed on
inventory, data reconstruction, dimensions, palette, PDF/PNG/SVG integrity,
certificate drift, or claim-boundary drift.
