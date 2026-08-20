# R0.68B-2e exact dominant-mass certificate

This directory records the formal monitored exact-rational reconstruction of
all 1,792 coordinates of the reachable dominant mass vector.

- Source commit: b80c0f197e91da00673e1b4fd04f0801fe51be2d
- Status: strict-passed
- Exact recurrence degree: 33
- Exact root bisections: 192
- Root interval width:
  4.078315292499077829193933818285342222313228e-69
- Maximum mass-coordinate width:
  2.176879811830441074604718149855523460813868e-69
- Exact interval vector SHA-256:
  bf424dfb3c9ce85d1e47d2270b329f6cb4af51e32e665663949d6c53cf6f0e53
- Runtime: 7.01 s (7.2 s including the monitor)
- Peak sampled RSS: 177.688 MiB

All nine checks passed. The mass intervals follow from exact integer reachable
vectors, exact recurrence residuals, exact quartic signs, and rational
interval residue evaluation. Binary64 is used only for non-certifying
cross-checks.

Reproduction command:

    PYTHONPATH=research tmp/r068b-venv/bin/python \
      research/run_with_monitor.py \
      --output resources.csv --interval 0.1 -- \
      tmp/r068b-venv/bin/python \
      research/eighth_order_dominant_mass_exact_audit.py \
      --output eighth-order-dominant-mass-exact.json \
      --source-commit b80c0f197e91da00673e1b4fd04f0801fe51be2d \
      --bisections 192 --progress
