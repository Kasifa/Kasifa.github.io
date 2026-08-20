# R0.62 quartic-correlation certificate

This directory archives the exact finite regression and the extended
deterministic computations used in R0.62.  The all-index three-carry identity
and the bound

```text
|R_{L,M,m}| <= C_4 (m/M)^2 sqrt(M),    C_4 < 7.9
```

are proved in `research/quartic_correlation_reduction_note.md`.  The integer
audit is a regression of that proof.  Positivity and the small numerical
values in the target scans remain finite evidence only.

## Source lock

- source commit: `f7159fe6e089af6207c18d6aee3ea081a2b8508f`
- exact regression: `research/quartic_correlation_reduction_audit.py`
- quartic scanner: `research/quartic_target_scan.cpp`
- sweep driver: `research/quartic_target_sweep.py`
- aggregate audit: `research/quartic_target_audit.py`
- workers per quartic target: 18
- arithmetic: C++ `long double` with compensated summation
- randomness: none

The integer regression checks 228,225 direct carrier triples in 16 dyadic
parameter boxes and verifies all four exact checks.  It reports the explicit
constant
`C_4 = 7.834243504443502291016914984711454558...`.

The three new all-target scans contain 3,584 evaluations:

| `L` | `M` | worst target | maximum ratio | scanner wall time |
|---:|---:|---:|---:|---:|
| 1 | 512 | 481 | 0.0009855702272829397 | 1.759 s |
| 1 | 1024 | 981 | 0.0012127996801718404 | 6.020 s |
| 1 | 2048 | 1912 | 0.0011457637853978923 | 35.779 s |

Combined with R0.61, the finite certificate now covers 4,042 distinct
`(L,M,m)` triples and 27,082,065,198 ordered quartic paths.  The overall
observed maximum remains `0.0013286562612066827` at `(4,64,64)`.

## Reproduction

Compile the scanner:

```sh
/usr/bin/clang++ -O3 -std=c++20 -pthread \
  research/quartic_target_scan.cpp \
  -o tmp/r062/quartic-target-scan
```

Run the exact correlation regression:

```sh
python3 research/run_with_monitor.py \
  --output research/certificates/r062/correlation-reduction-resources.csv \
  --interval 0.1 -- \
  python3 research/quartic_correlation_reduction_audit.py \
  --maximum-level 3 \
  --progress-log research/certificates/r062/correlation-reduction-progress.ndjson \
  --pretty --check \
  --output research/certificates/r062/correlation-reduction-audit.json
```

For `M=512`, replace `LEVEL_M` by `9`; for `M=1024`, use `10`; for
`M=2048`, use `11`:

```sh
python3 research/run_with_monitor.py \
  --output research/certificates/r062/m2048-all-resources.csv \
  --interval 0.1 -- \
  python3 research/quartic_target_sweep.py \
  --binary tmp/r062/quartic-target-scan \
  --pairs 0:LEVEL_M --threads 18 --target-mode all \
  --run-directory tmp/r062/m2048-all-runs \
  --progress-log research/certificates/r062/m2048-all-progress.ndjson \
  --output research/certificates/r062/m2048-all-summary.json
```

The summary JSON is a lossless aggregation of every raw scanner record and
adds the exact command used for each target.  It is therefore the archived
raw numerical record; the temporary per-target files are redundant.

Aggregate R0.61 and R0.62 finite scans:

```sh
python3 research/quartic_target_audit.py \
  --summary research/certificates/r061/scaling-summary.json \
  --summary research/certificates/r061/extended-summary.json \
  --summary research/certificates/r061/all-targets-summary.json \
  --summary research/certificates/r062/m512-all-summary.json \
  --summary research/certificates/r062/m1024-all-summary.json \
  --summary research/certificates/r062/m2048-all-summary.json \
  --high-precision research/certificates/r061/high-precision.json \
  --source-commit f7159fe6e089af6207c18d6aee3ea081a2b8508f \
  --check --pretty \
  --output research/certificates/r062/extended-quartic-exploration.json
```

## Monitoring boundary

Each sweep has an append-only progress log and a process-tree resource log.
The individual target scanners are shorter than the 0.1-second resource
sampling interval.  The resource records therefore certify liveness, wall
time, and absence of persistent memory growth, but they under-sample peak CPU
use.  The progress logs record every completed target, its ratio, condition
number, path count, elapsed time, and ETA.

`SHA256SUMS` pins every archived payload except the checksum file itself.
