# R0.73U formal figure source

This directory is the reproducible source and artifact package for
`fig-r073u-tensor-heat-hierarchy`.

The figure contains three distinct evidence types: an exact continuum
schematic, an exact four-site Fourier diagnostic with integer matrix entries,
and a plotted analytic function.  It contains no Navier--Stokes time
integration, random sample, regression, fitted scaling law, GPU result, or
DGX result.  Ordinary translation metadata is fixed to
`LOCAL_DIRECT_NO_DGX`.

Panel B compares tensor time tangents of the two sign-related initial fields
at the same initial time `t=0`.  It is not a claim that their subsequent
Navier--Stokes trajectories remain sign-related.  The viscous tensor
coefficient is
`V = Delta T - 2 sum_l partial_l u tensor partial_l u`.

## Reproduce

Use Python 3.12 with the exact versions in `requirements.txt`.  Either
activate that environment or pass its package directory through `--deps`:

```text
python3 plot.py --deps <python-packages> --render-preseal
python3 validate.py --deps <python-packages> --confirm-visual-qa
python3 validate.py --deps <python-packages> --verify-only
```

The publication seal binds the three frozen analytic sources to the
authoritative immutable commit
`84e808dae473f6381cbf9df55a71f5fe81a1cfce`:

```text
python3 validate.py --deps <python-packages> --source-commit 84e808dae473f6381cbf9df55a71f5fe81a1cfce --confirm-visual-qa
```

That source-commit pass upgrades the local artifact seal to the publication
seal.  The superseded commit
`72493751370aa948947000df169e21199fc5c95d` is rejected.  The ten figure-source
files and all generated artifacts are separately sealed by the manifest's
SHA-256 inventory, avoiding a metadata hash cycle.

The seal also emits the repository-wide `research-figure-manifest-v1`
compatibility fields while retaining the stricter R0.73U source seal.  The
figure, analytic, and certificate inputs must be committed and clean in their
declared scope before the write pass.  After sealing, verify both contracts:

```text
python3 validate.py --deps <python-packages> --verify-only
python3 ../../../validate_figure_package.py .
```

The CPU and memory fields are an explicitly labelled same-host post-run
metadata backfill; the original exact run's wall time and resource samples
remain bound to `progress.ndjson` and `resource-log.ndjson`.
