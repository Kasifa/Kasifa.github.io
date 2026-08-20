# R0.68A certificate package

This package archives the exact all-order target-tail reduction for the
periodic invariant-shear packet at quartic-critical amplitude.

## Certified statement

For `L=1`, `M_r=16^r`, `m_r=(2M_r+13)/15`, and
`epsilon_r^2=(16/lambda)^r`, where the R0.66 root satisfies `lambda>25`,
the complete sum of target terms of order at least ten obeys

    |R_{>=10,r}| / |A_r^2 Ghat_2(0,m_r,t_H)|
      < (1/30000) (43/64)^r.

The proof uses the exact invariant-shear Dyson chain, the tensor
Rudin--Shapiro heat envelope, the strict ninth-order support gap, and the
positive quadratic coefficient. It leaves the complete eighth-order heat
term as the only finite-order obstruction. It does not prove a result for
general three-dimensional Navier--Stokes solutions.

## Reproduction

Run from the repository root:

    python3 research/all_order_tail_reduction_audit.py \
      --output /tmp/r068a-audit.json --progress

The archived JSON and captured standard output are byte-identical.

## Files

- `all-order-tail-reduction-audit.json`: machine-readable formal report.
- `all-order-tail-reduction-audit.stdout.log`: byte-identical report.
- `all-order-tail-reduction-audit.stderr.log`: progress and monitor log.
- `resources.csv`: independent process resource samples.
- `SHA256SUMS`: integrity manifest for this package.
