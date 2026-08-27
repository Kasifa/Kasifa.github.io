# R0.72K directional-root finite-audit bundle

This bundle supports the analytic directional zero-sampling theorem and its
complete complex-target application in the perturbative common-band
triangular class.  It does not prove those theorems numerically.  The finite
work checks exact sharpness identities, complex directional projections, the
transformation of two separately archived R0.72J lineages, and the resulting
physical normalization.

No new PDE evolution is performed in R0.72K.

## Producer route

- source: `research/r072k_exact_audit.py`;
- inherited input: SHA-verified `research/certificates/r072j/result.json`;
- sharpness arithmetic: exact rational formulas at seven values
  \(\epsilon=2^{-1},\ldots,2^{-7}\);
- complex checks: scalar circles and two-component complex vectors;
- common sizes: \(R=4,8,16,32,64\).

Every declared producer check passes.  At \(R=64\),

- `measuredUpperOverN2 = 4.008195953738801`;
- `theoremProxyOverN2 = 16.40124033210622`;
- `rootAtomOverN2 = 1.5364293621591198`;
- `normalizedMeasuredCompleteUpper = 4.927062979997985e-4`;
- `normalizedTheoremCompleteProxy = 2.016117600013836e-3`.

The all-size diagnostic slopes are `-0.7169243421462232` for the measured
normalized upper and `-0.6734750701519232` for the theorem-level proxy.

## Independent route

- source: `research/r072k_independent_audit.py`;
- inherited input: SHA-verified
  `research/certificates/r072j/independent-result.json`;
- implementation: Python standard-library quadrature, explicit norming
  functionals, bracketing, and bisection;
- sharpness parameterization: \(\epsilon=1/n\),
  \(n=4,8,\ldots,1024\);
- producer R0.72K source and artifacts are neither imported nor read.

Every declared independent check passes.  At \(R=64\), its values become

- measured complete upper divided by \(N^2\):
  `4.008195953733489`;
- analytic complete proxy divided by \(N^2\):
  `16.401246589632697`;
- exact root lower divided by \(N^2\):
  `1.536429362159221`;
- normalized measured upper: `4.927062962001006e-4`;
- normalized analytic proxy: `2.016118361796778e-3`.

The inherited exact-root residual is at most
`3.0102575009625416e-13` on the five sizes.

## Cross-route agreement

`crosscheck.json` compares only quantities produced independently in the two
routes.  Its largest relative discrepancies are:

| Quantity | Maximum relative discrepancy |
|---|---:|
| measured complete upper | `1.9858870324333152e-12` |
| theorem-level complete proxy | `6.344126605891297e-7` |
| normalized measured upper | `7.280138297493951e-9` |
| normalized theorem proxy | `6.271336973172109e-7` |
| exact root atom | `1.26026927930635e-11` |
| mixed row, including factor two | `3.972163143457586e-12` |
| true cubic row, including factor two | `2.9406301718957877e-12` |

The shared exact sharpness ratios and complex-scalar theorem ratios also
agree within `2e-12`.

## Boundary

The proof is in `research/r072k_report-source.md`.  Binary64 agreement does
not enumerate all complex roots, prove the extended root inequality, prove
the asymptotic common-band estimates, or provide an interval certificate.
The archived R0.72J model choices, amplitude lift, and reference payment are
inherited explicitly.  This bundle does not establish a theorem for general
three-dimensional Navier--Stokes solutions and does not resolve the Clay
Millennium Problem.

Run `command.txt` from the repository root.  Rebuild `SHA256SUMS` only after
every other file in this directory is final.
