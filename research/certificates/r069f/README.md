# R0.69F fractional-Volterra endpoint certificate

This archive locks the source commit and the exact/high-precision checks for
the endpoint-scaling no-go theorem in
research/critical_resolvent_endpoint_scaling_note.md.

## Reproduce

From the repository root, with the pinned R0.68B virtual environment:

    tmp/r068b-venv/bin/python research/run_with_monitor.py \
      --output research/certificates/r069f/resources.csv --interval 0.05 -- \
      tmp/r068b-venv/bin/python \
      research/critical_resolvent_endpoint_scaling_audit.py \
      --source-commit c3f3d94620f6852e48e07525cc81f2c94ee1511d \
      --output \
      research/certificates/r069f/critical-resolvent-endpoint-scaling.json \
      --pretty --check

The certificate contains 22 checks, all passed.  Symbolic checks cover the
geometric endpoint partition, the Bielecki stationarity cubic, and the exact
shell-threshold inverse.  One-hundred-digit calculations compare the
Mittag--Leffler series with the complementary-error-function identity at
eight points, optimize six Bielecki scenarios, and check four shell
recurrences.

The monitored reproduction completed in about 0.5 seconds and reached a peak
resident set of about 117.4 MiB.  The calculation is CPU-only because the
problem is a small high-precision symbolic audit; a DGX run would add transfer
and container overhead without improving time to result.

## Decision boundary

The certificate proves that optimizing the scalar positive-time resolvent
can force at most a type-I shell lower bound.  Classical local continuation
already gives the stronger every-late-shell statement.  The archive does not
assign sharp values to the universal kernel constants, prove that a singular
time exists, exclude a singularity, or solve the Navier--Stokes Millennium
problem.
