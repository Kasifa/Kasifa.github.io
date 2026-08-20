# R0.68B-2f guarded degree-ten moment certificate

This directory archives the source-locked, monitored IEEE binary128
centre--radius enclosure of every raw and centred moment through total degree
ten for the fixed 1,792-state R0.68B construction.

- Engine source commit: `2d4c9e1c4150034b8204cea32d19238ca3013190`
- Engine source SHA-256:
  `a2ecd299bf3a08a7d157847aa301c6f7a3a8bc43bd719bea83831a478b4549e7`
- Sparse-payload manifest SHA-256:
  `e80e5224aba65c8493bd8b89d21b3413d96427caa7aa9db6d48ba3d0884cf3b1`
- Payload: 410 files, 58,913,830 bytes
- State dimension: 1,792
- Channels per state through degree ten: 8,008
- Values in each output array: 14,350,336
- Raw maximum radius upper bound:
  `7.91179658125257438e-22`
- Centred maximum radius upper bound:
  `1.88584884046089302e-20`
- Runtime: 512.856 s wall time
- Average CPU utilization: 1,763%
- Peak resident set size: 1,960,264 KiB
- Host: NVIDIA DGX Spark, `aarch64`, GCC 13.3.0, 20 CPU cores

The four binary128 arrays total 918,421,504 bytes and are not stored in Git.
`output-array-SHA256SUMS` and `output-array-sizes.txt` bind them exactly.  The
complete arrays remain in the DGX working archive and can be regenerated from
the locked source and payload manifest.  The independent streaming verifier
scanned every value after the formal run; all centres and radii were finite
and every radius was nonnegative.

The binary64 implementation in
`research/eighth_order_moment_interval_audit.py` is a rejected precision
baseline, not this certificate.

## Reproduction outline

1. From the source commit, generate a new empty sparse bundle with
   `research/prepare_eighth_order_quad_moment.py`.
2. Verify that the SHA-256 of `payload-manifest.sha256` is the value recorded
   above and verify every listed file hash and byte size.
3. On GCC with 16-byte, 113-bit `_Float128`, compile without fast-math:

       g++ -O3 -std=gnu++20 -fopenmp -Wall -Wextra -Wconversion \
         research/eighth_order_quad_moment_engine.cpp -o engine

4. Run with 20 OpenMP threads, passing the source commit and payload-manifest
   hash as the last two arguments:

       OMP_NUM_THREADS=20 ./engine DATA OUTPUT 10 \
         2d4c9e1c4150034b8204cea32d19238ca3013190 \
         e80e5224aba65c8493bd8b89d21b3413d96427caa7aa9db6d48ba3d0884cf3b1

5. Hash the four arrays and run
   `verify_eighth_order_quad_moment_output.cpp` over the output directory.

## Claim boundary

This certificate closes only the finite degree-ten moment-lift gate.  It does
not yet enclose the heat coefficients or the signature-compressed defect, so
it does not establish the final eighth-order heat sign.  It makes no claim
about general three-dimensional Navier--Stokes regularity and does not solve
the Millennium problem.
