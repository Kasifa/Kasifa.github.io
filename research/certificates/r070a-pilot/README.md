# R0.70A local scale-ratio pilot

This archive contains the five-point, single-worker diagnostic run described in
`research/r070a_scale_ratio_robustness_note.md`.  It is an audited diagnostic
archive, not an end-to-end producer archive or a formal certificate.

- Ratios: `3.8, 3.9, 4.0, 4.1, 4.2`
- Grid: raw-moment P14, 64 cutoff cells, distance-moment P14, 28 radial cells
  per ratio, 128-bit Arb endpoints
- Workers: one local worker; no DGX execution
- Setup time: `4.062272541981656` seconds
- Sum of ratio integration times: `330.44844549903064` seconds
- Result status: `diagnostic`
- Exact command: `command.txt`
- Captured software environment: `environment.txt`
- Unmodified program output: `raw-result.json`

Each fixed-ratio interval encloses its coefficient at the selected coarse grid,
but the widths are far too large to certify any sign.  Coefficient midpoints,
the discriminant recomputed from those midpoints, and all secant slopes are
diagnostics only.  They do not bound the derivative between ratio nodes and do
not certify a numerical open interval.

`result.json` was post-processed without reintegration.  Relative to
`raw-result.json`, the post-processing added the correctly defined discriminant
from coefficient midpoints, replaced the corresponding diagnostic secant, and
added the `provenance` object.  The test suite compares the raw and processed
files field by field and confirms that every coefficient interval, rigorous
discriminant interval, endpoint interval, timing, and integration audit is
unchanged.

One provenance limitation cannot be repaired retrospectively: the exact byte
state of the script that generated `raw-result.json` was not archived before
the diagnostic-field correction.  The current
`research/r070a_scale_ratio_robustness.py` is a rerun-compatible companion that
generates the corrected schema directly, but its hash is not represented as
the hash of the original producer state.  Likewise, the exact one-off
post-processing command was not retained.  The raw output and the fieldwise
verification make the data transformation auditable, but not byte-for-byte
replayable from the original producer.

Baseline repository HEAD before the pilot was
`155b21437337d69f42938699f0afcdd9e820f56c`; the published R0.69W producer
remains `2b3141a333d3dea0c4b7a241c11f9adbca31d1b4`.  This pilot does not modify
or supersede the R0.69W certificate.

The current companion script and the unchanged R0.69W interval integrator are
both hash-locked in `SHA256SUMS`.

The pilot did not record periodic CPU or memory telemetry.  Its elapsed times
are preserved in `result.json`, but it is intentionally classified as a
diagnostic rather than a formal monitored certificate.
