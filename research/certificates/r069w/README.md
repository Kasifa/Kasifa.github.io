# R0.69W strict interval certificate

This archive is the complete, source-locked certificate for the static
scale-ratio-four family

\[
u_a=aU_1+(1-a)U_{1/4},\qquad 0\le a\le1.
\]

It certifies

\[
\mathcal A_0(u_a)<0\quad(0<a\le1),\qquad
\mathcal A_{-2}(u_0)<0.
\]

The claim is a rigorous obstruction for this declared one-parameter static
family.  It is not a propagation theorem, a critical-norm estimate, a global
regularity proof, or a finite-time singularity construction for the
three-dimensional Navier--Stokes equations.

## Certified decision intervals

The outward-rounded merged result is:

| Quantity | Certified interval |
| --- | --- |
| \(c_1\) | `[-0.0020421027908703103, -0.0008440552534174868]` |
| \(c_2\) | `[0.002393592617980337, 0.004933596141229829]` |
| \(c_3\) | `[-0.12676969700886406, -0.12489333880250154]` |
| \(\Delta=c_2^2-4c_1c_3\) | `[-0.0010297777226174903, -0.00039732714404764783]` |
| \(\mathcal A_{-2}(u_0)\) | `[-0.001947993537909744, -0.0019148502803584854]` |

Because the upper endpoints of \(c_3\) and \(\Delta\) are negative, the
quadratic \(c_1+c_2a+c_3a^2\) is negative on the whole real axis.  The
separate \(j=-2\) interval closes the algebraically degenerate endpoint
\(a=0\).

## Locked production configuration

- Producer source commit: `2b3141a333d3dea0c4b7a241c11f9adbca31d1b4`
- Raw bump moments: power 19, 524,288 cells
- Cutoff certificate: 2,048 cells
- Distance-moment primitives: power 22, 4,194,304 cells
- Radial grid: 512 transition cells, 128 core cells, 256 plateau cells
- Boundary refinement: 4
- Arb precision: 256 bits
- Execution: 20 disjoint radial-row workers on NVIDIA DGX Spark
- Longest worker elapsed time: 1,535.6651919609867 seconds
- Sum of worker elapsed times: 28,877.69878333574 seconds
- Sum of observed per-worker peak RSS: 67.2967841796875 GiB
- Every resource monitor terminated with `exited:0`

The true smooth convolution is certified directly.  No floating quadrature
node enters the formal result.  Cutoff endpoint distributions are retained
through order six.  Center derivative coefficients use a certified local
Taylor enclosure from exact rational cutoff nodes; box-wide remainders retain
the independent whole-cell derivative ranges.

## Archive layout

- `result.json`: outward-rounded merge of all 20 partial certificates.
- `verifier.json`: independent rational-endpoint decision and provenance
  verification; all checks passed.
- `workers/worker-00` through `worker-19`: each partial `result.json`, complete
  `progress.ndjson`, two-second `resources.csv`, and `worker.log`.
- `environment.txt`: source hashes, clean-tree check, system and package data.
- `resource-summary.json`: worker runtimes, terminal statuses, and memory peaks.
- `calibration-comparison.json`: rejected calibrations and the same-P18
  before/after midpoint-derivative comparison.  It is diagnostic evidence,
  not part of the formal interval sum.
- `formal-command.txt`: exact worker command template.
- `SHA256SUMS`: digest of every other archived payload.

## Independent reproduction checks

From repository root at the source commit, merge the partial results with:

```sh
python research/merge_two_scale_annular_intervals.py \
  --source-root . \
  --output result.json \
  research/certificates/r069w/workers/worker-*/result.json
```

Then verify the merged certificate with:

```sh
python research/verify_two_scale_annular_interval.py \
  research/certificates/r069w/result.json \
  --source-root . --require-head
```

The archived verifier was executed on the clean DGX source tree while HEAD was
the locked producer commit.  Later publication-only commits do not change that
producer provenance.
