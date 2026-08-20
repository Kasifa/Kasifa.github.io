# R0.68B-1 publication certificate

This directory certifies the exact zero-time eighth-order seven-carrier cycle
for the repeated-`0100` Rudin--Shapiro packet.  It is the algebraic half of
the remaining R0.68 obstruction.  The complete heat-weighted seven-simplex
projection is still open.

## Source lock

- Source commit: `3ddf6d30965837311c0b659d5fb21e41c3b80f14`
- Exact audit: `research/eighth_order_cycle_audit.py`
- Mathematical note: `research/eighth_order_cycle_note.md`
- Pinned dependencies: `research/requirements-r068b.txt`

## Formal command

```text
OPENBLAS_NUM_THREADS=18 OMP_NUM_THREADS=18 \
python research/run_with_monitor.py \
  --output research/certificates/r068b1/resources.csv \
  --interval 5 -- \
  python research/eighth_order_cycle_audit.py \
  --source-commit 3ddf6d30965837311c0b659d5fb21e41c3b80f14 \
  --max-direct-level 6 --sequence-terms 82 --progress \
  --output research/certificates/r068b1/eighth-order-cycle-audit.json
```

The standard-output log is byte-for-byte identical to the JSON certificate.
Scientific progress is isolated in the standard-error log, and process-tree
resources are sampled independently every five seconds.

## Certified result

The direct closure has 1792 states.  Both digit matrices have exact rational
rank 448.  Direct seven-fold convolution agrees with the digit transfer in
all 1792 states through six binary levels.

For the four-bit cycle `0100`,

```text
rank(W8) = 204,
rank(W8^2) = rank(W8^3) = 148.
```

The exact image characteristic polynomial is

```text
x^56 (x-4096)^14 q4_256(x)^14 q10_16(x)^6 q18(x).
```

All 205 integer coefficients match this factorization.  Their canonical
JSON SHA-256 is

```text
2a1ac6b6b2c0fc5b6939492425fd13709592b9eea14cae3d24a24f2bd248d75d
```

The reachable scalar satisfies

```text
Y8_r = C8,0 nu^r + O(4800^r),
nu = 256 lambda,
```

with

```text
6438.806869529984 < nu < 6438.806869530010
```

and the strict rational projection interval displayed as

```text
-0.0261267936340556992556756533777
  < C8,0 <
-0.0261267936270826862592782194400.
```

The certificate verifies the full 1792-coordinate identity
`P33(W8) W8 v0 = 0`, while `P33(W8) v0` is nonzero.  The generating function
is reduced, so the dominant quartic factor is genuinely reachable.  Exact
Schur transforms place every root of the degree-ten and degree-eighteen
factors inside radius 4800.

All 17 certificate checks pass.

## Resources

The formal audit took 228.56 solver wall seconds and 228.9 monitored wall
seconds.  The monitor recorded 47 samples, a peak process-tree resident set
of 649.312 MiB, peak sampled CPU of 100%, no NVIDIA GPU, and final status
`exited:0`.

## Claim boundary

This certificate proves a zero-time, fixed-order algebraic correlation
theorem for one explicit packet inside the globally smooth invariant-shear
class.  It does not evaluate the complete heat-weighted seven-simplex
observable.  It does not prove norm inflation, singularity, global
regularity, or the three-dimensional Navier--Stokes Millennium problem.
