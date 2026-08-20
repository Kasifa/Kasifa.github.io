# R0.68B-2g guarded degree-ten heat-jet certificate

This directory archives the source-locked guarded binary128 evaluation of all
8,008 centred heat coefficients through spatial degree ten and their pairing
with the certified R0.68B-2f dominant moments.

- Source commit: `014a9e604c65b405ebc7684cf3913c74ef19a55e`
- Engine SHA-256:
  `752dd737b364c2de6efd94d475cccbff75ffdd9ff65f27f25afdfea8d3815bdc`
- Independent verifier SHA-256:
  `322f6a45a3843a914680b272d5b4f7deeed293453884f227daf1552c39199937`
- Heat payload manifest SHA-256:
  `7fe9ffa660701c3f2314c32cbad803b3973ce33a0e26f475802260c583cf91f0`
- Certified centred-moment centre SHA-256:
  `0e1dd04f4811ca91d966ab4a48a156645e9f5a08f732c1612046a24f108fe29b`
- Certified centred-moment radius SHA-256:
  `437a8f18234fb8c07ea23661a77e3413eee4dbb674e4dcefd83a17d386a268bf`
- Uniform infinite time-series tail upper bound:
  `2.62605089342894371e-25`
- Degree-ten heat-jet centre:
  `-1.49238243184751323e-08`
- Degree-ten heat-jet interval radius upper bound:
  `1.07451892110713391e-25`
- Status: strict negative finite-jet sign
- Runtime: 41.642 s (41.70 s including `/usr/bin/time`)
- Average CPU utilization: 1,211%
- Peak resident set size: 469,596 KiB
- Host: NVIDIA DGX Spark, `aarch64`, GCC 13.3.0, 20 CPU cores

The two coefficient arrays are small enough to archive directly.  The
independent verifier rescanned all 8,008 coefficient intervals and recomputed
the moment pairing from the separately certified moment arrays.  A binary64
architecture reference agrees with the binary128 coefficient centres within
`4.05059535468908282e-22`.

## Reproduction outline

1. At the source commit, run
   `research/prepare_eighth_order_heat_coefficient.py` into a new empty
   directory.
2. Verify all seven payload hashes and sizes and the manifest SHA-256 above.
3. Compile `research/eighth_order_heat_coefficient_engine.cpp` with GCC,
   OpenMP, and no fast-math.
4. Run the engine with the heat data, the R0.68B-2f full binary128 output
   directory, an empty output directory, and the recorded provenance hashes.
5. Hash the coefficient arrays and run
   `verify_eighth_order_heat_coefficient_output.cpp`.

## Claim boundary

This certificate proves a strict negative sign only for the dominant spatial
Taylor jet through degree ten.  The signature-compressed Taylor defect and
its resolvent correction remain open, so the final dominant heat sign is not
yet established.  This is not a result on all Picard orders and does not solve
the Navier--Stokes Millennium problem.
