# R0.69R nonlocal-vorticity-difference certificate

This archive locks the exact near/far vorticity-difference split, optimal
radius, scaling uniqueness, and sextic Young endpoint from
`research/nonlocal_vorticity_difference_split_note.md` to source commit
`97cfa19f962309bb62ae3fab0e4dcaef9f9eca38`.

## Reproduce

From the repository root:

    tmp/r068b-venv/bin/python research/run_with_monitor.py \
      --output research/certificates/r069r/resources.csv --interval 0.05 -- \
      tmp/r068b-venv/bin/python research/nonlocal_vorticity_difference_split_audit.py \
      --source-commit 97cfa19f962309bb62ae3fab0e4dcaef9f9eca38 \
      --output research/certificates/r069r/nonlocal-vorticity-difference-split.json

The certificate contains 15 checks, all passed. It verifies the cross-product
difference identity, the linear near-kernel radial mass, the exact far-kernel
`L^2` norm, the optimized enstrophy radius, the unique homogeneous exponents
`p=q=3/2`, and the exact sextic Young remainder.

The monitored run took 0.37 seconds, with 5 running samples, a maximum
observed CPU utilization of 32.6%, and a peak resident set size of
67.062 MiB. It was an exact, deterministic, CPU-only symbolic audit.

## Decision boundary

The result closes only the norm-based route that combines the absolute
near-field vorticity difference with an energy-controlled far field. The
difference genuinely removes one singular order, but optimizing the split
returns the classical `A^(3/2) B^(3/2)` scale and hence an `A^6` remainder.
It does not exclude signed cross-scale cancellation or bounds containing an
additional critical quantity. It proves neither global regularity nor
finite-time blow-up and does not solve the Millennium Problem.
