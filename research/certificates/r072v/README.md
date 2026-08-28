# R0.72V deterministic unit-chart globalization certificate

This bundle is presently at **source stage**.  No certificate JSON, manifest,
or hash ledger is generated or sealed in this stage.

The future formal certificate records only exact finite algebra:

- the unit-chart probe
  \(q_0=(315/128)(1-4y^2)^4\mathbf 1_{[-1/2,1/2]}\);
- \(\mu_2=1/44\), \(\mu_4=3/2288\),
  \(\mu_4-\mu_2^2=5/6292\), and \(\kappa_0=5/6292\);
- \(\ell_{\alpha,\beta}(t)=\beta(\mu_4+6t\mu_2)\), the unit-block
  bound \(L_1=315/2288\), and the sufficient escaping-pair threshold
  \(\lambda\ge693/2\);
- the exact spatial translation coefficients
  \(a=3k\), \(b=3k^2+6c\), and the removable scalar term;
- the energy rearrangement giving the squared contraction ratio
  \(C^2/(T+C^2)\);
- the exact small-time scaling obstruction to a constant uniform as
  \(T\downarrow0\).

The bound analytic report proves the coefficient-uniform unit-chart theorem,
the whole-line graph theorem, the all-\(L^2\)-data energy evolution,
actual-solution observability, and block contraction for the exact scalar
model.  This finite certificate does **not** machine-check the
compactness argument, scalar endpoint traces, the countable
\(H^{-1}\) direct sum, or nonautonomous evolution existence.  It does not
prove periodic transfer, nonlinear Navier--Stokes closure, or any Clay-level
statement.  Time-length uniformity is false.

Source-only checks, which write no outputs:

```sh
python3 research/certificates/r072v/independent_recompute.py --self-test
python3 research/certificates/r072v/generate_certificate.py --self-test
```

After every bound source has been committed, the later formal stage is:

```sh
SOURCE_COMMIT=$(git rev-parse HEAD)
python3 research/certificates/r072v/generate_certificate.py \
  --formal --source-commit "$SOURCE_COMMIT"
python3 research/certificates/r072v/validate_certificate.py --require-formal
```

The producer has no unsealed output mode.  Formal generation requires a
completely clean repository, a full 40-character source commit equal to
`HEAD`, and byte-identical working copies of every bound source.  It refuses
to overwrite any pre-existing formal output.
