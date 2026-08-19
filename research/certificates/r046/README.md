# R0.46 exact certificate

This directory archives the formal exact-rational audit for the R0.46
zero/nonzero-charge two-block weighted-column theorem.

## Certified statement

Split a tail series into its charge-zero and nonzero-charge parts and set

\[
\|f\|_{r,\kappa}
=\kappa\|P_0f\|_{B_r}+\|P_{\ne0}f\|_{B_r},
\qquad \kappa=\frac34.
\]

For every input monomial, the output block weight is applied before taking
the column supremum.  This retains the correlation between the exceptional
zero-charge output and the remaining output from the same input column.

The proof covers five disjoint sectors:

1. `s=0`: the zero-charge output vanishes identically, and the nonzero output
   is maximized at the exact lattice endpoint `j=81`;
2. `s=-1`: only the `q=1` center terms land in charge zero.  Their negative
   derivative is multiplied by `kappa`, so
   \[
   G'_r(t)\ge 3r-\kappa\widehat Q_r(1/82)>0,
   \]
   and the exact maximum is the true endpoint `j=82`;
3. `s=1`: a uniform all-degree termwise bound treats the exceptional `q=-1`
   output with weight `kappa`;
4. `2<=s<241`: the R0.41 all-order fixed-charge endpoints apply unchanged;
5. `s>=241`: the R0.44 common-slope theorem applies unchanged.

At `r=0.376`, the five certified sector bounds are

- `s=0`: 0.76674139886755508747;
- `s=-1`: 0.98067636538355528460;
- `s=1`: 0.20295065666640586388;
- largest finite positive charge, `s=162`: 0.99520480590228934501;
- `s>=241`: 0.99770647568583198433.

The complete two-block tail bound is therefore
0.99770647568583198433, and the fixed-point and canonical-stretch gates both
close.  The unweighted R0.45 bound at the same radius is
1.0165018805421294014, so the block correlation is essential.

At the adjacent probe `r=0.377`, the inherited common-slope large-charge
bound is 1.0030411177094620525.  This fails the present sufficient inequality
while the polynomial stretch bound remains below one.  It does not prove
failure of the exact operator, failure of every block norm, a singularity of
the reduced system, or a Navier--Stokes singularity.

The audit also records a deliberately coarser entrywise `2x2` matrix of
separate block suprema.  That matrix has Perron display value
1.0753987917062369 at `r=0.376` and fails.  The successful theorem is not this
matrix estimate: it combines both output blocks from each input column before
taking the supremum.

## Files

- `edge-two-block-weight.json`: machine-readable GMP certificate;
- `progress.ndjson`: append-only scientific stage log;
- `resources.csv`: 0.125-second process-tree resource samples;
- `SHA256SUMS`: hashes for every archived file except itself.

## Pinned source

- source commit: `a521a84f01b748e3c138ecb785c1b21907dc0e28`;
- R0.45 input certificate SHA-256:
  `abc588fb80a140cf78f0558119f50e7a15dce9b2d3fa5219a8b0f9456c8d0b7b`.

## Exact reproduction command

```sh
PYTHONPATH=research tmp/r024-venv/bin/python research/run_with_monitor.py \
  --output research/certificates/r046/resources.csv \
  --interval 0.125 -- \
  tmp/r024-venv/bin/python research/edge_two_block_weight_audit.py \
  --max-total-degree 80 \
  --entry-radius 371/1000 \
  --rescued-radius 372/1000 \
  --target-radius 376/1000 \
  --failure-probe-radius 377/1000 \
  --zero-charge-weight 3/4 \
  --charge-cutoff 241 \
  --regression-charges=-1,0,1,2,162,240,241,300 \
  --regression-degree-offsets 0,3,18 \
  --ball-divisor 1000000 \
  --source-commit a521a84f01b748e3c138ecb785c1b21907dc0e28 \
  --progress \
  --progress-log research/certificates/r046/progress.ndjson \
  --check --pretty \
  --output research/certificates/r046/edge-two-block-weight.json
```

## Successful-run summary

- 31/31 formal checks passed;
- scientific wall time: 39.158856 seconds;
- monitored wall time: 39.282190 seconds;
- resource samples: 264;
- maximum observed CPU: 100.0%;
- maximum observed resident memory: 47.047 MiB;
- GPU: not used;
- randomness: none;
- threshold arithmetic: `gmpy2.mpq`, with no floating-point decision.

Environment:

- macOS Darwin 25.6.0 arm64;
- Apple M5 Max, 36 GiB memory;
- Python 3.12.13;
- gmpy2 2.3.1;
- GMP 6.3.0.
