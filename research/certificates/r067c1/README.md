# R0.67C-1 certificate package

This package archives the exact first-cycle sign audit for the complete
sixth-order five-simplex heat observable.

## Certified statement

At `M=16`, `q=2`, and `T=log(2)/2`, the sum over all 34,690 valid carrier
tuples and all ten `(3,2)` time-order shuffles lies in the strict positive
interval recorded in `sixth-order-heat-one-cycle-audit.json`.  The Taylor
polynomial has degree 32 and the absolute omitted-series bound is below
`2e-12`.

This is a finite-scale sign certificate.  It does not certify the sign of the
dominant asymptotic heat projection, all higher Picard orders, singularity, or
three-dimensional Navier--Stokes regularity.

## Reproduction

Run from the repository root with the bundled or an equivalent Python runtime:

```sh
python3 research/sixth_order_heat_one_cycle_audit.py \
  --output /tmp/r067c1-audit.json \
  --order 32 \
  --source-commit b898179036990a352a6b73e04f2a733905f9dc32 \
  --progress
```

The JSON report and captured stdout are byte-identical.  The source commit is
`b898179036990a352a6b73e04f2a733905f9dc32`.  The parent R0.67B certificate
SHA-256 is
`6ca1af103c763d7ed6fa6296765bba891c4c080bc596d6679a9539fb9e94e1e0`.

## Files

- `sixth-order-heat-one-cycle-audit.json`: machine-readable exact report.
- `sixth-order-heat-one-cycle-audit.stdout`: byte-identical captured report.
- `sixth-order-heat-one-cycle-audit.stderr`: progress and macOS resource log.
- `resources.csv`: compact runtime summary.
- `SHA256SUMS`: integrity manifest for the package.
