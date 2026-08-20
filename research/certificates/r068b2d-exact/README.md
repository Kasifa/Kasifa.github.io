# R0.68B-2d exact derivative-majorant certificate

This directory records the formal monitored GMP rational run of
`research/eighth_order_heat_derivative_exact_audit.py`.

- Source commit: `516768bc5dbdbb557e156af5e7141ca2374327c3`
- Status: strict-passed
- Backend: gmpy2 2.3.1 / GMP 6.3.0
- Time enclosure: 120 terms, width
  `4.818513637046374450105764779644351260425e-118`
- Shuffles: 35
- Eleventh-order multiindices: 4,368 per shuffle
- Exact maximum upper:
  `2.566326636735080655209837298880261917219e-6`
- Maximising multiindex: `(0, 0, 0, 11, 0, 0)`
- Exact vector SHA-256:
  `2b742828cfa00097b2ea1dc2203cae4da8c30164d9422a734bd12da8d6a468ee`
- Runtime: 137.84 s (138.1 s including the monitor)
- Peak sampled RSS: 200.203 MiB

All five declared checks passed. The maximum is compared in exact rational
arithmetic with \(2.567\times10^{-6}\), so this archive strictly certifies
the complete eleventh-derivative majorant. It does not yet certify the
dominant moment lift, heat jet, observable defect, or combined sign gap.

Reproduction command:

    PYTHONPATH=research tmp/r068b-venv/bin/python \
      research/run_with_monitor.py \
      --output resources.csv --interval 0.1 -- \
      tmp/r068b-venv/bin/python \
      research/eighth_order_heat_derivative_exact_audit.py \
      --output eighth-order-heat-derivative-exact.json \
      --source-commit 516768bc5dbdbb557e156af5e7141ca2374327c3 \
      --time-terms 120 --progress
