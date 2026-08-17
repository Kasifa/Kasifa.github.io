# R0.21 remainder certificate archive

This directory contains machine-readable outputs for the R0.21 finite-time
remainder study.  Each JSON file records its own clean source commit.

## Cone-frequency cancellation certificate

`cone-frequency-cancellation.json` comes from
`research/cone_frequency_cancellation_audit.py` at clean source commit
`3440e29c265e1289e0718b7cbd6c0ea39f264130`.  Exact rational arithmetic
certifies that the eight signed input labels are the vertices of a linearly
transformed cube.  Hence the exact `L`-leaf support has `(L + 1)^3` labels;
after the zero Fourier mode is removed, even leaf counts have one fewer mode.
The archived run verifies the support through 13 leaves and audits the
diagonal/transverse frequency decomposition on 11,024 generated labels.

The accompanying operator lemma proves that incompressibility and a
longitudinal seminorm remove the apparent shell factor mode by mode,
including charge-zero outputs.  This certificate does not yet close the
infinite analytic sequence norm or the Taylor remainder.

## Exact certificate

`viscous-target-order7.json` comes from
`research/viscous_target_taylor_audit.py`.  It uses exact signed-frequency
arithmetic, rational polynomial coefficients, and exact interval evaluation
on the radius-`1e-6` R0.20 root box.  It certifies:

- target absence through time order four;
- equality of the order-five viscous target and the R0.20 pure nonlinear
  target;
- absence of a seven-leaf target and hence of the pure nonlinear order-six
  term;
- the one-heat order-six interval
  `[-2.611276916335079, -2.6112696484122124]` relative to order five;
- the complete order-seven interval
  `[-2.8144704386643693, -2.814414371216345]` relative to order five,
  separated into two heat insertions and two classes of eight-leaf trees.

The exact run used Python 3.12.13 and completed in 23.98 seconds.  Its
finite-shell complex128 records are cross-checks, not part of the exact sign
proof.

## Exploratory tail diagnostic

`viscous-tail-order12-diagnostic.json` comes from
`research/viscous_tail_diagnostic.py`.  Three worker processes independently
computed levels 3, 4, and 5 through time order 12.  All three runs reached
4772 order-12 Fourier modes.  Their order-12 Fourier-l1 root indicators are
approximately 3.08898, 3.10146, and 3.10229.

This second file is floating-point evidence only.  It does not enclose the
infinite Taylor tail, prove convergence uniformly in shell level, or prove a
Navier--Stokes regularity, singularity, or cascade statement.

## Reproduction

```sh
PYTHONPATH=research python3.12 research/cone_frequency_cancellation_audit.py \
  --check --pretty --progress --maximum-leaves 13 \
  --output tmp/r021-cone-frequency-cancellation.json

PYTHONPATH=research python3.12 research/viscous_target_taylor_audit.py \
  --check --pretty --progress --output tmp/r021-viscous-target-order7.json

PYTHONPATH=research python3.12 research/viscous_tail_diagnostic.py \
  --check --pretty --progress --levels 3 4 5 --maximum-order 12 --workers 3 \
  --output tmp/r021-viscous-tail-order12.json
```

Verify the copied outputs against `SHA256SUMS` before using them as evidence.
