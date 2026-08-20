# R0.68B-2c degree-ten defect pilot archive

This directory records the formal monitored run of
research/eighth_order_heat_defect_pilot.py.

- Source commit: d05886b831dc51b14abefe62f34f6340b141dc1d
- Classification: exploratory binary64 pilot
- Jet degree: 10
- Moment channels per state: 8,008
- Total moment coordinates: 14,350,336
- Free shifts processed: 16,777,216
- Signature classes: 44,514
- Runtime: 87.61 s
- Peak sampled RSS: 1,760.812 MiB

The run passed all eight declared checks. It does not certify all mixed
eleventh derivatives and therefore does not prove the final heat-projection
sign.

Reproduction command:

    PYTHONPATH=research tmp/r068b-venv/bin/python \
      research/run_with_monitor.py \
      --output resources.csv --interval 0.1 -- \
      tmp/r068b-venv/bin/python \
      research/eighth_order_heat_defect_pilot.py \
      --output eighth-order-heat-defect-pilot.json \
      --source-commit d05886b831dc51b14abefe62f34f6340b141dc1d \
      --progress
