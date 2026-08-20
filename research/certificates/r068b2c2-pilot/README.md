# R0.68B-2c2 complete mixed-derivative pilot archive

This directory records the formal monitored run of
`research/eighth_order_heat_defect_pilot.py` after the complete homogeneous
polynomial reduction was added.

- Source commit: `11c46ce8c111a3433767b0d4cfc623d125f131fa`
- Classification: exploratory binary64 pilot
- Jet degree: 10
- Moment channels per state: 8,008
- Total moment coordinates: 14,350,336
- Free shifts processed: 16,777,216
- Signature classes: 44,514
- Eleventh-order multiindices: 4,368 per shuffle
- Global derivative maximum: `2.56632663673508e-6`
- Maximising multiindex: `(0, 0, 0, 11, 0, 0)`
- Runtime: 132.51 s (132.8 s including the monitor)
- Peak sampled RSS: 1,828.219 MiB

The run passed all ten declared checks. It closes the mixed-derivative gate
at the binary64 majorant level. It does not yet provide outward-rounded
enclosures for the moment lift, heat jet, observable defect, or derivative
majorant, so it is not a strict sign certificate.

Reproduction command:

    PYTHONPATH=research tmp/r068b-venv/bin/python \
      research/run_with_monitor.py \
      --output resources.csv --interval 0.1 -- \
      tmp/r068b-venv/bin/python \
      research/eighth_order_heat_defect_pilot.py \
      --output eighth-order-heat-defect-pilot.json \
      --source-commit 11c46ce8c111a3433767b0d4cfc623d125f131fa \
      --progress
