# R0.22 analytic-radius loss certificate

This archive records the full-space analytic-weight obstruction found after
the R0.21 cone-frequency cancellation lemma.

`analytic-radius-loss.json` was generated from clean source commit
`d32f2132a9e82dd2d0448e90c690526fc153a675` with Python 3.12.13 and NumPy
2.3.5.  It records exact rational checks for the family

```text
a_N = (N, -3N, 3N-2)
b_N = (-N+1, -3N+1, -3N+1)
```

and floating-point convergence checks for `N = 2, 3, 5, 8, 13, 21, 34,
55, 89`.

The exact proof establishes a shell-uniform upper bound with analytic-radius
loss

```text
1/(e eta) + 24/(e^2 eta^2).
```

The sharp family has exactly additive cube radius.  Its ordered interaction,
normalized by `N^2`, tends to `27/2`; the symmetrized quadratic interaction
tends to `27`.  Along `delta_N = 4^-N`, the dimensionless input heat rates
tend to `1/12` and the output rate tends to `1/3`, so the heat multiplier does
not provide a uniform `N^2` gain.

This rules out a one-radius estimate in the full Euclidean/longitudinal mode
space.  It does not rule out a smaller invariant coefficient subspace or
tree-level cancellations for the selected initial data.

## Reproduction

```sh
PYTHONPATH=research python3.12 research/analytic_radius_loss_audit.py \
  --check --pretty --progress \
  --output tmp/r022-analytic-radius-loss.json

cd research/certificates/r022
shasum -a 256 -c SHA256SUMS
```
