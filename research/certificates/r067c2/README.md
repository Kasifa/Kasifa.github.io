# R0.67C-2 certificate package

This package archives the guarded sign audit for the dominant complete
sixth-order five-simplex heat projection in the periodic 0100 target family.

## Certified statement

The 320-state transfer is lifted through all 210 centred moments of total
degree at most six. Signed paths landing at the same affine shift are combined
before absolute values are taken. A global analytic majorant for every seventh
partial derivative of the complete ten-shuffle heat observable, together with
the exact zero-sixth-jet transfer scale 1/4096, gives

    -1.715485437712e-6
      < C_6,heat <
    -2.025145622883e-7.

The dominant complete sixth-order heat projection is therefore strictly
negative. This does not control all Picard orders, norm inflation, singularity,
or three-dimensional Navier--Stokes regularity.

## Reproduction

Run from the repository root:

    python3 research/sixth_order_heat_dominant_projection_audit.py \
      --output /tmp/r067c2-audit.json \
      --source-commit ed153f5919f040c7fc16b169685b05fc574f3d17 \
      --r067b-certificate \
        research/certificates/r067b/sixth-order-affine-moment-audit.json \
      --progress

The JSON report and captured stdout are byte-identical. The source commit is
ed153f5919f040c7fc16b169685b05fc574f3d17. The parent R0.67B certificate
SHA-256 is
6ca1af103c763d7ed6fa6296765bba891c4c080bc596d6679a9539fb9e94e1e0.

## Files

- sixth-order-heat-dominant-projection-audit.json: machine-readable report.
- sixth-order-heat-dominant-projection-audit.stdout.log: byte-identical report.
- sixth-order-heat-dominant-projection-audit.stderr.log: progress and macOS resource log.
- resources.csv: compact runtime and proof-size summary.
- SHA256SUMS: integrity manifest for the package.
