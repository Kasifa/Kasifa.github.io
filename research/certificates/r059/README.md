# R0.59 exact certificate

This directory archives the deterministic audit for the all-index theorem in
`research/multi_output_critical_saturation_note.md`.

## Successful source-locked run

- formal source commit: `f80788625f97a3038c492a6697832a7653bb8b82`
- audit result: 24/24 checks passed
- packet modes checked: 4,190,209
- ordered positive interaction pairs checked: 29,822,521
- tensor prefixes checked: 16,760,836
- wall time inside the scientific audit: 72.990616 seconds
- monitored elapsed time: 73.048608 seconds
- resource samples: 271
- peak CPU: 100.0 percent
- peak resident memory: 1,112.469 MiB
- GPU memory: 0 MiB
- randomness: none
- floating-point mathematical decisions: none

Reproduction command:

```text
python3 research/run_with_monitor.py --output research/certificates/r059/resources.csv --interval 0.25 -- python3 research/multi_output_critical_saturation_audit.py --maximum-level 10 --maximum-exhaustive-level 6 --maximum-prefix-level 10 --source-commit f80788625f97a3038c492a6697832a7653bb8b82 --progress --progress-log research/certificates/r059/progress.ndjson --check --pretty --output research/certificates/r059/multi-output-critical-saturation.json
```

## Retained failed source-lock attempt

The two files prefixed `failed-source-lock-` record an earlier run in which
all 24 mathematical checks passed, but the program correctly refused to emit
a certificate because the supplied 40-character commit hash did not equal the
checked-out HEAD.  They are retained as provenance for the monitoring record;
they are not the successful certificate run.

The finite computation is a regression of exact formulas.  The proof of the
all-index theorem is the symbolic argument in the research note.  Neither the
proof nor this certificate claims norm inflation, control of higher Picard
iterates, large-data regularity, or resolution of the three-dimensional
Navier--Stokes Millennium problem.
