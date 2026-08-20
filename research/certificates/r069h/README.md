# R0.69H pressure-Hessian pointwise-obstruction certificate

This archive locks the source commit and exact symbolic/Fourier checks for
the pointwise pressure-Hessian sign obstruction in
research/pressure_hessian_pointwise_obstruction_note.md.

## Reproduce

From the repository root, with the pinned research virtual environment:

    tmp/r068b-venv/bin/python research/run_with_monitor.py \
      --output research/certificates/r069h/resources.csv --interval 0.05 -- \
      tmp/r068b-venv/bin/python \
      research/pressure_hessian_pointwise_obstruction_audit.py \
      --source-commit 86ac684e2a2564f56d42d9c216918ed659652846 \
      --output \
      research/certificates/r069h/pressure-hessian-pointwise-obstruction.json \
      --pretty --check

The certificate contains 15 checks, all passed. It verifies the strain
matrix identities, the quadrupole angular geometry, the mean-zero selector
duality, and two exact smooth periodic divergence-free witness families. The
witnesses have the same local strain and vorticity at the origin but pressure
components

    H11_minus = -1 - (54/85)t^2,
    H11_plus  = -1 + (54/85)t^2.

Their signs differ when t^2 > 85/54.

The monitored reproduction completed in about 0.3 seconds and reached a peak
resident set of about 66.5 MiB. The audit is small, exact, deterministic, and
CPU-only; a DGX run would add overhead without improving the evidence.

## Decision boundary

The certificate rules out only pointwise pressure-Hessian sign or closure
rules based solely on the local pair (S, omega). It does not rule out nonlocal
or integrated pressure mechanisms, does not prove regularity or singularity,
and does not solve the Millennium Problem.
