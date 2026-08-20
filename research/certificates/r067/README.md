# R0.67A publication certificate

This directory certifies the exact zero-time sixth-order five-carrier cycle
for the repeated-`0100` Rudin--Shapiro packet.  It is an intermediate
certificate: the complete heat-weighted five-simplex projection remains the
next R0.67 step.

## Source lock

- Source commit: `8da878e`
- Exact audit: `research/sixth_order_cycle_audit.py`
- Mathematical note: `research/sixth_order_cycle_note.md`
- Regression test: `tests/sixth-order-cycle.test.mjs`

## Formal command

```text
python3 research/sixth_order_cycle_audit.py \
  --max-direct-level 7 --sequence-terms 40 --progress \
  --output research/certificates/r067/sixth-order-cycle-audit.json
```

The standard-output log is a byte-for-byte duplicate of the JSON certificate.
Progress and `/usr/bin/time -lp` resource measurements are isolated in the
standard-error log.

## Certified result

The complete direct closure has 320 states.  Direct five-fold convolution
agrees with the digit transfer in every state through seven binary levels.
The four-bit cycle has image dimension 36 and image characteristic polynomial

```text
x^5 (x-256)^5 q4(x)^4 q10(x),
```

where the dominant root of `q4` satisfies

```text
402.425429345624 < mu < 402.4254293456256.
```

The reachable target scalar obeys

```text
Y_r = C_6,0 mu^r + O(300^r),
```

with the exact outward interval displayed by the certificate as

```text
-0.0130633968154241768578468
  < C_6,0 <
-0.0130633968151447883145673.
```

Consequently `|Y_r|/256^r` tends to infinity.  The absolute carry transfer
has exact eigenvalue 65536; after removing mass and four affine moments, the
formal `C^{1,1}` dual threshold is `65536/16^2 = 256 < mu`.

All 14 certificate checks pass.

## Resources

The formal run took 0.72 wall seconds and reached 45,760,512 bytes maximum
resident set size according to `/usr/bin/time -lp`; it reported zero swaps.

## Claim boundary

This certificate proves a zero-time, fixed-order algebraic correlation theorem
for one explicit packet family.  It does not yet certify a nonzero dominant
projection for the complete heat-weighted five-simplex observable.  It does
not prove norm inflation, singularity, global regularity, or the
three-dimensional Navier--Stokes Millennium problem.
