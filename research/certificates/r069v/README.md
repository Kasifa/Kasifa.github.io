# R0.69V exact two-scale decoupling certificate

This archive certifies the symbolic cubic production law and deterministic
regressions for the shape-changing family

    u_{epsilon,a} = a U_1 + (1-a) U_epsilon.

The executable source is locked to commit
`0e99dfbab767890839bca88bcf773b5889a8fa91`.  The accompanying mathematical
note proves the uniform annular decoupling theorem; this machine certificate
checks the algebra and deterministic building coefficients.

## Reproduce

From the repository root:

    tmp/r068b-venv/bin/python research/run_with_monitor.py \
      --output research/certificates/r069v/resources.csv --interval 0.05 -- \
      tmp/r068b-venv/bin/python research/two_scale_annular_decoupling_audit.py \
      --output research/certificates/r069v/two-scale-annular-decoupling.json \
      --source-commit 0e99dfbab767890839bca88bcf773b5889a8fa91

All 21 checks passed.  The monitored process exited with code zero after
0.748 seconds, reached 90.6% CPU and 136.219 MiB resident memory, and used no
NVIDIA GPU.

## Certified conclusions

The exact local-production identity is

    V(u_{epsilon,a})
      = V_q[a^3 + epsilon^3(1-a)^3]
        + epsilon^3 a(1-a)^2 C_q,

with no `a^2(1-a)` term.  Numerically, the deterministic references are
`V_q = 1.9568944233758179` and `C_q = -2.804629235509589`.

The mathematical note proves that pure copies separate in logarithmic scale
while all mixed annular `ell^1` mass is uniformly lower order.  Hence
`Gamma_ann(u_{epsilon,a})` converges uniformly in `a` to the one-profile ratio
as `epsilon` tends to zero.  Scale separation alone therefore cannot improve
the limiting full-space cancellation ratio.

## Claim boundary

This is an exact theorem for the declared static compactly supported family.
It neither proves a finite-separation sign obstruction for every amplitude nor
controls a time-dependent Navier--Stokes solution.  It does not solve global
regularity, finite-time singularity, or the Millennium Problem.
