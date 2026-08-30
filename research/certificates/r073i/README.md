# R0.73I exact and finite-boundary certificate

This package separates three evidence classes.

1. Exact rational arithmetic checks the inherited-endpoint chain, the
   constants in the continuum upper action, and two finite-dimensional
   logical counterexamples.
2. The analytic proofs remain in `research/r073i_*.md`; this package binds
   their hashes but does not replace their operator arguments.
3. `experiments/r073i` is a binary64 Fourier--Galerkin diagnostic.  Its
   action and WKB values are copied only as finite evidence and never used to
   certify a continuum branch or a matching action.

Formal build order:

```text
python3 generate_certificate.py --root ../../.. --source-commit COMMIT --write
python3 independent_recompute.py --directory . --write
python3 validate_certificate.py --directory . --root ../../.. --write
python3 seal_package.py --directory . --source-commit COMMIT --write
python3 validate_certificate.py --directory . --root ../../..
```

The formal package must be rebuilt after the source commit is frozen.
