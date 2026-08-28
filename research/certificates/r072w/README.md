# R0.72W deterministic exact-periodic certificate

This bundle is presently at **source stage**. No certificate JSON, manifest,
or hash ledger is generated or sealed at this stage.

The future formal certificate records only exact finite algebra:

- the heat-polynomial series through \(H_9\), including
  \(-\tfrac14H_3+\tfrac1{16}H_5-\tfrac1{160}H_7+
  \tfrac{17}{48384}H_9\), and the corresponding scaled coefficients;
- the identities \(\partial_tH_n=\partial_x^2H_n\) for
  \(n=3,5,7,9\), and the exact derivative scales of the trigonometric
  potential;
- the scaled probe on \(J_\ell=(-\ell/2,\ell/2)\), with
  \(\mu_2=\ell^2/44\), \(\mu_4=3\ell^4/2288\), and
  \(\mu_4-\mu_2^2=5\ell^4/6292\);
- the common-zero algebra for the bounded-chart limit, the determinant-three
  finite-type matrix, and
  \(\min_z(\cos^2z+\cos^22z)=7/16\);
- the far-translation no-go powers, the local absorption threshold
  (R=o(\kappa^{2/25})), the elementary torus-cell length inequality, and
  the energy ratio (C^2/(T+C^2)).

The bound analytic report proves the uniform exact-periodic unit-chart and
torus graph theorems and the scalar energy contraction. This finite
certificate does **not** machine-check compactness, scalar endpoint traces,
the varying-cell graph-space passage, the torus (H^{-1}) direct sum, or
nonautonomous evolution theory. It does not prove a short-time-uniform
constant, nonlinear Navier--Stokes closure, or any Clay-level statement.

Source-only checks, which write no outputs:

```sh
python3 research/certificates/r072w/independent_recompute.py --self-test
python3 research/certificates/r072w/generate_certificate.py --self-test
```

After every bound source has been committed, the later formal stage is:

```sh
SOURCE_COMMIT=$(git rev-parse HEAD)
python3 research/certificates/r072w/generate_certificate.py \
  --formal --source-commit "$SOURCE_COMMIT"
python3 research/certificates/r072w/validate_certificate.py --require-formal
```

Formal generation requires a completely clean repository, a full
40-character source commit equal to `HEAD`, and byte-identical working copies
of every bound source. The binding covers the research, audit, certificate,
figure, release-page, translation, manifest, and release-gate sources. It
refuses to overwrite any formal output.
