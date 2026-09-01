# R0.73Y formal certificate archive

This directory is the self-contained formal-certificate archive for the
frozen R0.73Y research commit
`1ecc6fe20a921db9d0876dbd4484a3aa4ca7ec66`.

The archive binds eight frozen research inputs by SHA-256.  The executable
producer is the frozen certificate script with only its three filesystem
path declarations relocated from the repository layout to this flat archive.
`seal_package.py` reverses that relocation in memory and requires the exact
frozen source-script hash before it accepts the package.

## Reproduce

Run from this directory:

```bash
python3 exact-shear-producer.py --check-only
python3 seal_package.py --check-only
```

To repeat the producer check with two interpreters without writing package
files, pass the commands explicitly:

```bash
python3 seal_package.py --check-only --python python3 --python "$R073Y_ALT_PYTHON"
```

`--check-only` is read-only: the seal script snapshots size, modification
time, and change time for every package file and fails if any changes.

## Inventory and self-exclusion

The package has thirteen regular files.  `manifest.json` inventories and
hashes the eleven non-seal-output files.  `SHA256SUMS` then hashes those
eleven files plus `manifest.json`; it excludes itself.  Thus neither generated
seal output claims to hash itself.  The exact counts are derived and checked
by `seal_package.py`, not inferred from prose.

## Scope

The producer is an exact Fourier/structural audit of one single-sine shear
witness with a dependency-free numerical convolution cross-check.  The wider
orthogonal-shear theorem is analytic and lies outside executable coverage.
The independent re-audit is included byte-for-byte from the frozen commit.

This archive certifies a literature-calibrated obstruction to the specified
production-only coercive bridge.  It does not certify a general Navier--Stokes
regularity theorem, an epsilon-regularity refutation, novelty or priority, or
the Clay Millennium problem.

**NOT CLAY.**
