# R0.49 exact certificate

This directory archives the formal exact-rational audit for the R0.49
multiplicative charge-character theorem.

## Certified statement

For a monomial `Z^m W^n`, define its degree and charge by

\[
i=m+n,\qquad q=2n-m,
\]

and equip the reduced canonical edge generating system with

\[
\|f\|_{r,c}=\sum_{m+n>0}(m+n)|f_{mn}|r^{m+n}c^{2n-m},
\qquad c=\frac45.
\]

The charge character `omega_s=c^s` is exactly multiplicative.  The scaling
`S_c[Z^mW^n]=c^q Z^mW^n` is therefore an algebra automorphism, commutes with
the nonlinear map, and conjugates this anisotropic norm to the ordinary
one-total-derivative Wiener norm.  Equivalently, the polyradii are

\[
\rho_Z=\frac r c,\qquad \rho_W=rc^2.
\]

The R0.47 all-order charge-degree theorem, applied after this exact
conjugacy, identifies the true active input column as charge `s=162` and
degree `j=81` throughout `[0.382618,0.382619]`.  Its value is a degree-80
polynomial `A_c(r)` with strictly positive nonconstant coefficients.  Hence
`P_c(r)=A_c(r)-1` has positive derivative for every positive `r` and at most
one positive root.

Exact GMP bisection and an independent exact Sturm sequence certify one root
in

\[
0.382618642388680778<r_*^{(4/5)}
                    <0.382618642388680779.
\]

At the adjacent millionth endpoints, the active column has exact decimal
values `0.99999692284203436108` and `1.0000017130264400588`.  The monotone
full-window sandwich covers all 243 competitors.  The nearest competitor is
the fixed charge `s=164` sector, with a positive certified dominance gap of
approximately `0.00014157274652028842093`.

At `r=0.382618`, the anisotropic Newton ball, Lipschitz gate, and conjugated
canonical-stretch construction all close.  The stretch bound is
`0.98796898781173256118`; the exact center residual norm is approximately
`1.6910402110013306773e-30`.  This residual includes the required total-degree
factor; the certificate explicitly excludes the smaller unweighted diagnostic
from the proof.

The geometry must be read anisotropically.  At the certified target,
`rho_Z=0.4782725` and `rho_W=0.24487552`, while

\[
\rho_Z^2\rho_W=r^3.
\]

Thus the certified disk radius in the fixed-charge variable `R=Z^2W` gains
a strict lower factor `1.0459367903514846826` relative to the upper endpoint
of the R0.48 threshold.  This is not an enlargement of the isotropic bidisc.
The certificate does not prove optimality of `c=4/5`, a theorem for arbitrary
three-dimensional velocity fields, Navier--Stokes global regularity, or
finite-time blow-up.

## Files

- `edge-charge-character-weight.json`: machine-readable GMP certificate;
- `progress.ndjson`: append-only scientific stage log;
- `resources.csv`: 0.125-second process-tree resource samples;
- `SHA256SUMS`: hashes for every archived file except itself.

## Pinned inputs

- source commit: `26ce6d7ffd636956fe7c95a2bbeb7e6ea6573728`;
- source SHA-256:
  `971e7bde1972028aedcda96756a9d0c5e4e91a3b838317f9664c3e18f6a7e9bd`;
- R0.48 input certificate SHA-256:
  `246bcfa6623b1050511554312c32e9973b42b620a20ff571a1b5f340041c9af0`;
- charge-scaled degree-80 polynomial SHA-256:
  `5f03a7cf2b083566b0360be1b442606b5a9355f64fe2f97fdbd3893a4822f2e9`;
- rational threshold-polynomial SHA-256:
  `3e2d58683a97c46290ae8d5ffc6b8beab38bb5763393aca4dcee5991cd7f5288`;
- primitive integer threshold-polynomial SHA-256:
  `590f711be8e843317ddf776dbb52268ea6d45d6f85d73adb804ff3825393c357`;
- active charge-contribution digest SHA-256:
  `8f62e4b3acd1f17f237d985d170a4326bc7a549221b7cae6b981b3b5f3f9f790`.

## Exact reproduction command

```sh
PYTHONPATH=research tmp/r024-venv/bin/python research/run_with_monitor.py \
  --output research/certificates/r049/resources.csv \
  --interval 0.125 -- \
  tmp/r024-venv/bin/python \
  research/edge_charge_character_weight_audit.py \
  --max-total-degree 80 \
  --charge-character 4/5 \
  --window-lower 382618/1000000 \
  --window-upper 382619/1000000 \
  --root-decimal-digits 18 \
  --charge-cutoff 241 \
  --ball-divisor 1000000 \
  --source-commit 26ce6d7ffd636956fe7c95a2bbeb7e6ea6573728 \
  --progress \
  --progress-log research/certificates/r049/progress.ndjson \
  --check --pretty \
  --output \
  research/certificates/r049/edge-charge-character-weight.json
```

## Successful-run summary

- 32/32 exact checks passed;
- exact Sturm sequence length: 81;
- exact root count in the isolated interval: 1;
- exact bisection decisions: 39;
- competitors covered: 243;
- finite exact regression columns: 30, used only as implementation checks;
- scientific wall time: 119.530144 seconds;
- monitored wall time: 120.581154 seconds;
- resource samples: 808;
- maximum observed CPU: 100.0%;
- maximum observed resident memory: 158.906 MiB;
- GPU: not used;
- randomness: none;
- threshold arithmetic: `gmpy2.mpq/mpz`, with no floating-point decision.

Environment:

- macOS Darwin 25.6.0 arm64;
- Apple M5 Max, 36 GiB memory;
- Python 3.12.13;
- gmpy2 2.3.1;
- GMP 6.3.0.
