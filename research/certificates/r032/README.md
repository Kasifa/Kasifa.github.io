# R0.32 exact finite singularity-candidate certificate

This directory archives the formal R0.32 run from clean source commit
`a973bc77915181a27158a475e75008e8bdb18d4a`.

## Classification

The result is a **finite exact diagnostic**, not a singularity theorem.

- Exact GMP recurrence: total degree 149, endpoint parameter 50.
- Exact ordered recurrence interactions: 13,518,749.
- Candidate table: diagonal D-log Padé cuts 30, 32, ..., 50.
- Exact root isolation: 22 transport approximants plus 11 sharp-combination
  zero diagnostics.
- Transport candidate hull:
  `[-0.749701196287094659..., -0.749433079639935448...]`.
- High-cut transport hull, cuts 42 through 50:
  `[-0.749499736288725517..., -0.749433079639935448...]`.
- All transport residues are strictly below `-1/2`.
- The closer sharp-combination object near `-0.723449` has positive residue
  near `+1` and is classified as a zero candidate.

The isolated roots are poles of finite rational approximants.  The files do
not prove analytic continuation to the cluster, convergence of the Padé
sequence, a dominant singularity, endpoint asymptotics, or a result for the
full three-dimensional Navier--Stokes equation.

## Formal command

Run from the repository root inside the research Python environment:

```text
python research/run_with_monitor.py \
  --output /tmp/r032-resources.csv --interval 2 -- \
  python research/edge_singularity_candidate_audit.py \
  --max-total-degree 149 --minimum-cut 30 --cut-step 2 \
  --checkpoint /tmp/r032-checkpoint.pkl.gz --checkpoint-interval 25 \
  --progress --progress-log /tmp/r032-progress.ndjson \
  --check --pretty --output /tmp/r032-edge-singularity-candidates.json
```

If interrupted, repeat the inner audit command with `--resume` and the same
checkpoint path.  The formal final checkpoint was 4,730,426 bytes with
SHA-256
`0e39f59b73dc80d190cc5fb4d662db975ca5e022538d92a02c57dcc1a34776ed`.
The checkpoint itself is an operational cache and is not committed.

## Files

- `edge-singularity-candidates.json`: exact endpoints, Padé polynomial
  digests, rational root and residue enclosures, dual-precision checks,
  theorem boundary, environment, and source provenance.
- `progress.ndjson`: append-only stage and checkpoint log.
- `resources.csv`: two-second process-tree resource samples.
- `resume-verification.json`: comparison of the first run with a second run
  restored from the final checkpoint.
- `SHA256SUMS`: hashes of the four archived files above.

## Run summary

- Scientific wall time: 176.395 seconds.
- Monitored wall time: 176.6 seconds.
- Maximum sampled CPU: 100.0%.
- Maximum sampled RSS: 216.203 MiB.
- GPU: not used; this exact rational workload is single-process and CPU-bound.
- Historical regression: every R0.28 endpoint through parameter 40 matched
  exactly.
- Checkpoint regression: a split run through degrees 12 and 18 matched a
  fresh degree-18 run coefficient for coefficient.
