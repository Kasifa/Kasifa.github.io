# R0.72U deterministic two-moment certificate

This bundle is presently at **source stage**. No certificate JSON, manifest,
or hash ledger is generated or sealed in this stage.

The future formal certificate records only exact finite algebra:

- \(\rho=(315/256)(1-X^2)^4\mathbf 1_{[-1,1]}\), normalized to mass one;
- \(\mu_2=1/11\) and \(\mu_4=3/143\);
- \(K_c(s)=3/143+6(c+s)/11\) on \([-1,1]\);
- the sufficient large-centre threshold \(|c|\ge27/13\);
- the independently optimized inviscid fixed-gauge floor \(4/5\).

The finite certificate does not machine-check the compactness and trace proof
of bounded-chart graph coercivity. It does not prove a whole-line block
contraction, periodic transfer, a nonlinear Navier–Stokes estimate, or any
statement about the Clay problem.

Source-only checks, which write no outputs:

```sh
python3 research/certificates/r072u/independent_recompute.py --self-test
python3 research/certificates/r072u/generate_certificate.py --self-test
```

After every bound source has been committed, the later formal stage is:

```sh
SOURCE_COMMIT=$(git rev-parse HEAD)
python3 research/certificates/r072u/generate_certificate.py \
  --formal --source-commit "$SOURCE_COMMIT"
python3 research/certificates/r072u/validate_certificate.py --require-formal
```

The producer has no unsealed output mode. Formal generation requires a clean
tracked tree, a full source commit equal to `HEAD`, and byte-identical working
copies of every bound source.
