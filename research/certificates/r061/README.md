# R0.61 quartic-target exploration certificate

This directory archives the deterministic finite computation supporting
R0.61.  The exact all-index coefficient formula is proved in
`research/quartic_target_note.md`; the observed positivity and numerical bound
in this directory are **not** all-index theorems.

## Source lock

- source commit: `895543f44b3c83c777014eefc9594f95b3b9d829`
- scanner: `research/quartic_target_scan.cpp`
- sweep driver: `research/quartic_target_sweep.py`
- high-precision cross-check: `research/quartic_target_high_precision.py`
- aggregate audit: `research/quartic_target_audit.py`
- randomness: none

The source-locked audit reports 464 evaluations including three duplicates,
461 distinct `(L,M,m)` triples, 49 distinct `(L,M)` pairs, and
7,494,536,238 ordered quartic paths.  All ten finite consistency checks pass.
Every archived ratio is positive; the largest is
`0.0013286562612066827` at `(L,M,m)=(4,64,64)`.  A 60-decimal computation
gives
`0.00132865626120669002455277852263909423526774058180003694165188`.

## Reproduction commands

Compile the long-double scanner:

```sh
/usr/bin/clang++ -O3 -std=c++20 -pthread -Wall -Wextra -pedantic \
  research/quartic_target_scan.cpp \
  -o tmp/r061/quartic_target_scan-formal
```

Run the 30-pair baseline edge sweep:

```sh
python3 research/run_with_monitor.py \
  --output research/certificates/r061/scaling-resources.csv \
  --interval 0.10 -- \
  python3 research/quartic_target_sweep.py \
  --binary tmp/r061/quartic_target_scan-formal \
  --preset scaling --threads 16 --target-mode edge \
  --run-directory tmp/r061/formal-scaling-runs \
  --progress-log research/certificates/r061/scaling-progress.ndjson \
  --output research/certificates/r061/scaling-summary.json
```

Run the 18-pair extended edge sweep:

```sh
python3 research/run_with_monitor.py \
  --output research/certificates/r061/extended-resources.csv \
  --interval 0.10 -- \
  python3 research/quartic_target_sweep.py \
  --binary tmp/r061/quartic_target_scan-formal \
  --pairs 0:11,0:12,0:13,1:10,1:11,1:12,2:9,2:10,2:11,3:8,3:9,3:10,4:6,4:7,4:8,5:6,6:6,10:0 \
  --threads 16 --target-mode edge \
  --run-directory tmp/r061/formal-extended-runs \
  --progress-log research/certificates/r061/extended-progress.ndjson \
  --output research/certificates/r061/extended-summary.json
```

Run all targets in four representative families:

```sh
python3 research/run_with_monitor.py \
  --output research/certificates/r061/all-targets-resources.csv \
  --interval 0.10 -- \
  python3 research/quartic_target_sweep.py \
  --binary tmp/r061/quartic_target_scan-formal \
  --pairs 0:8,2:6,3:6,4:5 \
  --threads 16 --target-mode all \
  --run-directory tmp/r061/formal-all-target-runs \
  --progress-log research/certificates/r061/all-targets-progress.ndjson \
  --output research/certificates/r061/all-targets-summary.json
```

Run the 60-decimal cross-check at the observed maximum.  The Python
environment must provide `mpmath==1.3.0`.

```sh
python3 research/run_with_monitor.py \
  --output research/certificates/r061/high-precision-resources.csv \
  --interval 0.10 -- \
  python3 research/quartic_target_high_precision.py \
  --level-l 2 --level-m 6 --target 64 --precision 60 \
  --reference tmp/r061/formal-scaling-runs/l4-m64-t64.json \
  --source-commit 895543f44b3c83c777014eefc9594f95b3b9d829 \
  --progress-log research/certificates/r061/high-precision-progress.ndjson \
  --output research/certificates/r061/high-precision.json
```

Aggregate and check the archived records:

```sh
python3 research/quartic_target_audit.py \
  --summary research/certificates/r061/scaling-summary.json \
  --summary research/certificates/r061/extended-summary.json \
  --summary research/certificates/r061/all-targets-summary.json \
  --high-precision research/certificates/r061/high-precision.json \
  --source-commit 895543f44b3c83c777014eefc9594f95b3b9d829 \
  --check --pretty \
  --output research/certificates/r061/quartic-target-exploration.json
```

## Monitoring

The extended sweep reached 1,591.3% observed CPU and 15.062 MiB RSS over
11.73 seconds.  The high-precision check used one core, peaked at 265.719 MiB
RSS, and completed in 11.00 monitored seconds.  Every sweep has a separate
append-only progress log and process-tree resource log.  The all-target jobs
are shorter than the 0.10-second resource sampling interval, so that log is
useful for wall time and liveness but not a reliable peak-CPU estimate.

`SHA256SUMS` pins every archived payload other than the checksum file itself.
