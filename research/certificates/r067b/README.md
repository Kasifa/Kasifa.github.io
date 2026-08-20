# R0.67B publication certificate

This directory certifies the exact mass-plus-four-first-moment lift and the
strict zero-affine resolvent gap for the repeated-0100 sixth-order cycle.

## Source lock

- Source commit: d0347369ae6ba564d4275d0cd720ba1cd4b91615
- Exact audit: research/sixth_order_affine_moment_audit.py
- Mathematical note: research/sixth_order_affine_moment_note.md
- Regression test: tests/sixth-order-affine-moment.test.mjs
- Parent certificate: research/certificates/r067/sixth-order-cycle-audit.json

## Formal command

    python3 research/sixth_order_affine_moment_audit.py \
      --max-direct-level 7 --progress \
      --source-commit d0347369ae6ba564d4275d0cd720ba1cd4b91615 \
      --r067a-certificate research/certificates/r067/sixth-order-cycle-audit.json \
      --output research/certificates/r067b/sixth-order-affine-moment-audit.json

The standard-output log is a byte-for-byte duplicate of the JSON certificate.
Progress and /usr/bin/time -lp measurements are isolated in the standard-error
log; process-tree samples are stored in resources.csv.

## Certified result

The finite normalized lift has 1600 coordinates and the exact equations

    m' = W m,
    ell'_j = (W ell_j + E_j m)/16,  1 <= j <= 4.

Direct five-polynomial convolution agrees with the mass and all four first
moments in every one of the 320 states through seven binary levels.  The
canonical lift defect annihilates constants and all four affine coordinates.
The finite and infinite-dimensional scales obey

    26 < 256 < 300 < mu.

Hence the zero-affine C^{1,1}-dual resolvent at mu exists with norm at most
1/(mu-256), and every vector in the finite mu-eigenspace lifts to a genuine
eigen-distribution of the full affine operator.

All 13 formal checks pass.

## Resources

The source-locked run took 2.04 wall seconds and reached 54,067,200 bytes
maximum resident set size according to /usr/bin/time -lp.  The process-tree
monitor observed at most 52.516 MiB RSS, no GPU, and zero swaps.

## Claim boundary

This certificate does not evaluate the pairing of that eigen-distribution
with the complete heat-weighted five-simplex observable.  It therefore does
not yet prove a nonzero sixth-order heat projection.  It makes no statement
about all higher Picard orders, norm inflation, singularity, global regularity,
or the three-dimensional Navier--Stokes Millennium problem.
