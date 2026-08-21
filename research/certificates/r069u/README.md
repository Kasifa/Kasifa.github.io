# R0.69U dyadic affine-core saturation certificate

This archive locks the exact dyadic core-carrier saturation theorem from
`research/affine_core_dyadic_saturation_note.md` to source commit
`9748c451e9d1cc8d6e7e2bcd732f79691b1c13ca`.

## Reproduce

From the repository root:

    tmp/r068b-venv/bin/python research/run_with_monitor.py \
      --output research/certificates/r069u/resources.csv --interval 0.05 -- \
      tmp/r068b-venv/bin/python research/affine_core_dyadic_saturation_audit.py \
      --source-commit 9748c451e9d1cc8d6e7e2bcd732f79691b1c13ca \
      --output research/certificates/r069u/affine-core-dyadic-saturation.json

The certificate contains 19 checks, all passed.  It verifies the declared
trace-free affine matrix and unit vertical vorticity, the exact angular
moment, the radial factor in the transition vorticity, the beta-density mass
and squared norm, Young's rational transition-energy bound, both limiting
annular coefficients, the positive `1/42` outer-share margin, exact core
production, and the full-space `R^3` dyadic scaling.

The monitored run took 0.249074 seconds, with four running samples, a maximum
observed CPU utilization of 43.4%, and a peak resident set size of 66.031 MiB.
It was an exact, deterministic, CPU-only symbolic audit and exited with code
zero.

## Decision boundary

The result proves eventual exact saturation of the **core-restricted**
boundary carrier and proves that pure self-similar dilation leaves the
full-space annular cancellation ratio unchanged.  It does not prove
full-space saturation, a dynamically propagated depletion mechanism, global
regularity, finite-time singularity, or the Millennium Problem.
