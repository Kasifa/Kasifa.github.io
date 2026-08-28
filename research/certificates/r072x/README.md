# R0.72X deterministic outer-time certificate

This bundle is presently at **source stage**.  No certificate JSON,
manifest, or hash ledger is generated or sealed at this stage.

The future formal certificate records only exact finite algebra and
bookkeeping:

- the unique common zero of the shifted slope/curvature brackets,
  \((D,\theta)=(0,0)\), including the \(\operatorname{diag}(3,3)\)
  Jacobian and the local Taylor coefficients used by the bounded-center
  reduction;
- the powers of \(\alpha\) and \(\kappa\) at the shrinking interface,
  including the matching \(\alpha^{-2}=\kappa^{2/5}\) diagnostic rates;
- the block floor inequality, its necessary \(q^{-1}\) exponential
  prefactor, and the geometric integrated-energy ledger;
- the Bloch gauge phase \(e^{2\pi i\beta}\), with complete cancellation of
  the scaling parameter from the boundary phase;
- the distinction between the scalar norm factor \(e^{-\mu L}\) and the
  squared-energy factor \(e^{-2\mu L}\);
- the exact spatially constant counterexample at zero coupling, zero
  residue, and zero scalar damping.

The bound analytic report proves the all-center exact-family graph theorem,
the all-start scalar semigroup, and the exact physical
\(A_1\)--\(A_2\)--\(A_1\) cocycle for the periodic representative
\(\beta=0\).  Bloch-uniform propagation is asserted only for the exact
\(A_2\) path and its strong-row direct sum; a Bloch-uniform fast \(A_1\)
concatenation is not proved.  This finite certificate does **not**
machine-check compactness, the bounded-center graph-limit passage, scalar
endpoint traces, twisted \(H^{-1}\) direct sums, endpoint integration by
parts, nonautonomous evolution, the Coble--He theorem, or the hypotheses of
its application.  It does not prove a uniform strict contraction for all
physical rows, a forced \(H^{-1}\) transfer, the complete linearized shear
subsystem, nonlinear Navier--Stokes closure, or any Clay-level statement.

Source-only checks, which write no outputs:

```sh
python3 research/certificates/r072x/independent_recompute.py --self-test
python3 research/certificates/r072x/generate_certificate.py --self-test
```

After every bound source has been committed, the later formal stage is:

```sh
SOURCE_COMMIT=$(git rev-parse HEAD)
python3 research/certificates/r072x/generate_certificate.py \
  --formal --source-commit "$SOURCE_COMMIT"
python3 research/certificates/r072x/validate_certificate.py --require-formal
```

Formal generation requires a completely clean repository, a full
40-character source commit equal to `HEAD`, and byte-identical working copies
of every bound source.  The binding covers the report, audits, certificate,
figure, release-page, translation, and release-gate sources.  Mutable site
publication state is validated separately by the release gate.  Formal
generation refuses to overwrite an existing output.
