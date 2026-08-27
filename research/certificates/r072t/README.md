# R0.72T deterministic exact certificate

This bundle records only finite identities for the exact heat profile near the
pure-second collision, the unique four-term scaling balance, and the exactly
solvable linear time-drift calibration. It does not certify a block
contraction, a periodic transfer, an all-start semigroup estimate, the combined
cubic/drift model, or any statement about the Clay problem.

Run:

```sh
python3 research/certificates/r072t/independent_recompute.py
SOURCE_COMMIT=$(git rev-parse HEAD)
python3 research/certificates/r072t/generate_certificate.py --formal --source-commit "$SOURCE_COMMIT"
python3 research/certificates/r072t/validate_certificate.py --require-formal
```

`independent_recompute.py` is the separate Fraction route. The certificate
generator invokes it again and compares its exact Taylor, scaling, centered
moments, canonical brackets, and claim boundary with the producer payload.
The validator is fail-closed archive and lineage validation; it is not the
independent producer.
