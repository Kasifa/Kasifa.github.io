# R0.72Y deterministic full-row and forced-transfer certificate

This bundle is a **draft** finite-algebra certificate. It is deterministic,
but it is not formally sealed to a clean source commit. The draft checks:

- the two Fourier modes of the heat shear and the identity `W_d=W_xx`;
- the sign of `div_j grad_j=-L` and the two equal pressure sources giving
  `L*pi=2*i*c*W_x*u_2`;
- the Bloch/Leray divergence cancellation;
- the Orr--Sommerfeld commutator coefficients, pressure cancellation, and
  Squire lift sign for `mu>0`;
- velocity reconstruction and its exact Gram-matrix energy identity for
  `mu>0`;
- the zero-coupling lift-up residual and exact norm formula, including its
  strict-growth witness at `xi=0`;
- the causal kernel's geometric sum and zero-damping algebra;
- the pointwise standard/semiclassical `H^{-1}` Fourier-weight comparison;
- Young's identity and the distinction between the energy exponent and norm
  exponent in the damping-gap estimate;
- explicit finite-certified, analytic-only, negative-result, and open claim
  keys.

The certificate does **not** machine-check infinite-series convergence,
Duhamel or duality arguments, Galerkin/variational limits, endpoint traces,
sharpness constructions, or nonautonomous evolution. Those arguments remain
`analytic-not-finitely-certified`. It also does not prove the complete
linearized shear subsystem, nonlinear Navier--Stokes closure, or the Clay
Millennium problem.

Run the source checks without writing outputs:

```sh
python3 research/certificates/r072y/independent_recompute.py --self-test
python3 research/certificates/r072y/generate_certificate.py --self-test
```

Regenerate and validate the deterministic draft:

```sh
python3 research/certificates/r072y/generate_certificate.py --draft
python3 research/certificates/r072y/validate_certificate.py --require-draft
```

Draft regeneration refuses to overwrite a manifest marked `formal`.

After the analytic report, the full-row audit, forced-transfer audit,
comprehensive audit, literature audit, gap matrix, release manifest, release
and translation scripts, complete figure-source package, and four R0.72Y tests
have all been frozen in one clean commit, seal the certificate with:

```sh
SOURCE_COMMIT=$(git rev-parse HEAD)
python3 research/certificates/r072y/generate_certificate.py \
  --formal --formal-source-commit "$SOURCE_COMMIT"
python3 research/certificates/r072y/validate_certificate.py --require-formal
```

Formal generation requires a lowercase 40-character commit equal to the
current clean `HEAD`. Every bound source must exist in that commit, and its Git
blob must equal the working file. The formal manifest and crosscheck set
`temporaryUnsealedSourceAllowed=false` and `formalSourceReady=true`; the
certificate and independent recomputation both carry the same `sourceCommit`.
Strict formal validation re-resolves the Git object and every blob, verifies
the SHA-256 and byte counts, and requires the source commit to be the current
`HEAD` or its ancestor. Twenty-nine bound sources may never change. The bound
source-commit blob, SHA-256, and byte count of `research/release-manifest.json`
also remain permanently checked; only its current publication-state copy may
advance, and only in a completely clean descendant publication commit. While
validation still runs at the source `HEAD`, only the five certificate outputs
created by sealing may be dirty. This keeps validation usable after formal
publication without weakening the frozen source snapshot. An existing formal
bundle is never overwritten.
