# Figure R0.71X-1: fixed-small-coupling endpoint scaling

This directory is the reproducible journal-figure package for the R0.71X
one-third endpoint audit. It extracts data only from these committed source
certificates:

- `research/certificates/r071x/result.json`;
- `research/certificates/r071x/independent-result.json`;
- `research/certificates/r071x/truncated-coset-result.json`.

The source/certificate provenance commit is
`45691a4bc1b562f305cd8f7b79d2c8c50957fb73`. The package never rewrites or
reruns those source calculations.

## Reading the panels

- **A:** fixed-\(\delta\) retained-coset \(D\) and complete prescribed
  two-root atomProxy sum, indexed to \(q=256\), with \(q^6\) and \(q^2\)
  guides.
- **B:** high-precision endpoint proxies and two visibly separate finite
  retained-coset layers: atomProxy sum divided by \(D^{1/3}\), and the full
  retained rotational-charge upper bound.
- **C:** the high-precision \(\delta^{4/3}\) sweep and the \(q=1024\)
  truncation-radius comparison against \(R=40\).

`data.csv`, `data.json`, `results.json`, and
`figure-data-metadata.json` retain raw values, formulas, source paths, and
evidence classes. The figure uses indexed values only in Panel A; the raw
source quantities remain archived in every Panel A row.

## Reproduce

Run `command.txt` from the repository root. The pipeline produces the source
extraction, figure exports, color/grayscale/PDF QA assets, independent
validation, formal manifest, and SHA-256 ledger.

## Claim boundary

`atomProxy` is not \(J_*\): the multiplier and \(\kappa_*\) factors are not
numerically locked. The nonlinear calculation is a finite retained Fourier
coset, not DNS. It does not establish spectral convergence. The analytic
continuum implicit-function theorem has an existential smallness radius, but
the plotted \(\delta=1/128\) has not been proved to satisfy that radius. This
package makes no universal \(D^{1/3}\) or regularity claim.
