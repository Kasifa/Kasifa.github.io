# R0.73Y exact-shear analytic figure archive

This directory is the formal 25-file archive for the R0.73Y exact-shear obstruction figure. The figure is a closed-form analytic witness, not DNS, not a turbulence-closure validation, and not a Navier-Stokes regularity result.

The sole mathematical authority is frozen research commit `1ecc6fe20a921db9d0876dbd4484a3aa4ca7ec66`: Theorem 1.1, equation (1.4), in `research/r073y_exact_shear_no_go.md`, together with the hash-sealed deterministic certificate whose payload is `51f721cf560df38fbeacdd093d4293adae10635e13dcaa6b9251616c4f7eca2c`.

## Reproduction

Create a Python 3.12.13 environment from `requirements.txt`. Set `R073Y_SOURCE_ROOT` to a clean checkout at the frozen commit. `MPLCONFIGDIR` may be set to an external writable directory; when it is absent, `plot.py` uses and removes a system temporary directory outside this package.

Run the commands in `command.txt`. The plotter checks the exact Python, NumPy, and Matplotlib versions and the frozen theorem/certificate hashes before it writes any output. The validator checks the exact 25-file inventory, reconstructs every CSV row, validates PDF/SVG/600-dpi PNG properties, checks all three QA renders, and runs negative source/runtime/inventory drift tests. Its manifest follows `research-figure-manifest-v1` and passes the project-wide `research/validate_figure_package.py` validator.

## Two-stage Git seal

The first seal is a prepublication metadata seal. It uses the pending figure-source sentinel and does not invent a commit. Commit exactly the 21 source/raw files in their final repository location. Then run the final reseal with `--repository`, the actual 40-hex `--figure-source-commit`, and `--confirm-visual-qa`. The validator reads every committed blob, requires byte identity with the current 21 files, requires their scoped Git status to be clean, reconstructs the bindings, and rewrites only `SHA256SUMS`, `manifest.json`, `qa-report.md`, and `validation.json`.

## Archive partition

The archive has exactly 10 immutable source files, 11 raw/result files, and 4 metadata files. `config.json` and `manifest.json` identify an 18-file deterministic core. UTC timestamps, process IDs, timing, resource observations, environment observations, sealing records, and their dependent checksums are explicitly isolated as nondeterministic observability.

No intermediate directory is created inside the package. `--verify-only` reconstructs the stored 21 blob bindings from Git rather than trusting serialized paths or hashes.
