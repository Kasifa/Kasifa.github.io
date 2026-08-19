# R0.33 exact moment-structure obstruction certificate

This directory archives the formal R0.33 run from clean source commit
`c717fc1e8ae16bedc88f639ca35bebe38de51801`.

## Classification

The principal result is an **all-order function-class exclusion from exact
low-order witnesses**, accompanied by finite degree-49 diagnostics.

For

```text
B_U(x) = hat U_1(-x),     B_V(x) = -hat V_1(-x),
H_U(x) = B_U'(x)/B_U(x),  H_V(x) = B_V'(x)/B_V(x),
```

the following exact negative moment witnesses are certified:

```text
B_U ordinary Hankel order 2:  -437/24192
B_V shifted  Hankel order 2:  -43522897/685843200
H_U shifted  Hankel order 1:  -32/63
H_V ordinary Hankel order 2:  -29699111/12700800
```

Therefore none of the four series is the direct moment generating function
`integral dmu(t)/(1-x*t)` of a nonnegative measure on `[0,infinity)`.  A
negative principal minor cannot be changed by later coefficients, so this
exclusion applies to the infinite exact formal series, not only the 50
coefficients used to discover it.

The result does not exclude other Padé convergence classes, a transformed or
background-subtracted Stieltjes form, or signed and complex measures.  It
neither proves nor disproves the R0.32 candidate near `R=-0.7495`, and it has
no direct three-dimensional Navier--Stokes regularity consequence.

## Pinned input

The audit reads
`research/certificates/r032/edge-singularity-candidates.json` and requires
its SHA-256 to be

```text
bd70ed05779631b729e89c269f82d287da361fdcea34e3c42703a712222f5575
```

The input contains 50 exact endpoint records through total degree 149.

## Formal command

Run from the repository root inside the research Python environment:

```text
python research/run_with_monitor.py \
  --output /tmp/r033-resources.csv --interval 0.02 -- \
  python research/edge_moment_structure_audit.py \
  --maximum-hankel-order 12 \
  --progress --progress-log /tmp/r033-progress.ndjson \
  --check --pretty --output /tmp/r033-edge-moment-structure.json
```

## Files

- `edge-moment-structure.json`: input provenance, definitions, four exact
  theorem witnesses, all 50/49 coefficient signs, 96 local Turán records,
  96 ordinary/shifted Hankel determinants through order 12, theorem
  boundary, checks, environment, and clean source state.
- `progress.ndjson`: append-only stage log.
- `resources.csv`: 0.02-second process-tree resource samples.
- `SHA256SUMS`: hashes of the archived files.

## Run summary

- Scientific wall time: 0.0672 seconds.
- Monitored wall time: 0.3 seconds.
- Maximum sampled CPU: 45.9%.
- Maximum sampled RSS: 70.016 MiB.
- GPU: not used; the exact determinant audit is too small to benefit from a
  remote accelerator.
- Random seed: none.
- Exact backend: Python `Fraction` and SymPy rational determinants.
- All 10 formal checks passed.
- Finite local Turán failures: 13 of 48 for `B_U`, 20 of 48 for `B_V`.
