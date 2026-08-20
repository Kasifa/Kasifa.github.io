# R0.68B-2h guarded corrected dominant-heat certificate

This directory archives the source-locked guarded binary128 certificate for
the complete degree-ten spatial Taylor defect and resolvent correction of one
fixed reachable dominant component in the R0.68B eighth-order construction.

- Source commit: `efd0d828678ce99fcc5d0f40d751b1883d32f740`
- Engine source SHA-256:
  `487947432d9d4de172004ee4ebbb8ebdc8d1a4ac86d13b657af4da7b3c4336e4`
- Defect payload manifest SHA-256:
  `edfb110c8cd7f8369be4d5748cb798d9ca72864a8e35b1146c790662f2acacfc`
- Certified centred-moment radius SHA-256:
  `437a8f18234fb8c07ea23661a77e3413eee4dbb674e4dcefd83a17d386a268bf`
- Certified heat-coefficient radius SHA-256:
  `ab121c7f974542d42652d823410d23f2bda2502c5960479463206fed80b6432e`
- Signature classes: 44,514, covering all `16^6 = 16,777,216` shifts
- Absolute-path cycle: 695,808 nonzeros; maximum row sum 54,210,304
- Observable defect upper bound: `30.2344865053562053`
- Resolvent observable upper bound: `0.00469566611238897251`
- Derivative correction upper bound: `1.20506130214380835e-08`
- Corrected dominant-heat interval:
  `[-2.69744373399132142e-08, -2.87321129703704757e-09]`
- Runtime: 16.407 s (16.47 s including `/usr/bin/time`)
- Average CPU utilization: 1,779%
- Peak resident set size: 475,148 KiB
- Host: NVIDIA DGX Spark, `aarch64`, GCC 13.3.0, 20 CPU cores

The source-unlocked audit and source-locked formal run agree after removing
only the source-commit and elapsed-time fields.  The independent verifier
checks every defect payload hash and byte size, the source and upstream
certificate hashes, exact compression metadata, Decimal resolvent relations,
the explicitly budgeted binary64 serialization envelope, and the strict sign
of the final upper endpoint.

The no-cancellation tail uses the product of four entrywise-absolute digit
transfer matrices.  Taking the entrywise absolute value only after composing
the signed cycle would retain path cancellation and is not a valid majorant.

## Reproduction outline

1. At the source commit, generate a new empty defect bundle with
   `research/prepare_eighth_order_signature_defect.py`.
2. Verify all twelve payload hashes and byte sizes and the payload-manifest
   SHA-256 recorded above.
3. Compile on GCC with 16-byte, 113-bit `_Float128`, OpenMP, and no fast-math:

       g++ -O3 -std=gnu++20 -fopenmp -Wall -Wextra -Wconversion \
         research/eighth_order_signature_defect_engine.cpp -o engine

4. Run the engine against the R0.68B-2f full moment arrays and R0.68B-2g heat
   arrays, passing the source commit and all three provenance hashes.
5. Run `research/verify_eighth_order_signature_defect_output.py` over the
   formal summary, defect bundle, upstream hash lists, source, and audit run.

## Claim boundary

This certificate proves a strict corrected sign for one explicitly fixed
eighth-order coefficient inside a globally smooth parallel-shear invariant
class.  It does not control an infinite family of Picard orders, construct a
finite-time singularity, control arbitrary three-dimensional perturbations,
or prove general three-dimensional Navier--Stokes regularity.  It is not a
solution of the Millennium problem.
