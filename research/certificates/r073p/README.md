# R0.73P formula-diagnostic certificate

This 19-file package independently reproduces the three elementary formula
checks used by the R0.73P critical-frequency gate.  It is a reproducibility
and error-detection package, not a Navier--Stokes simulation or a PDE proof.

The package checks:

1. the normalized frequency thresholds (N^{-3}) and (N^{-1/2});
2. for the pure mode (a_N=cN^{-\gamma}), the homogeneous Sobolev powers

   \[
   \|a_Ne_N\|_{L^2}\sim cN^{-\gamma},\qquad
   \|a_Ne_N\|_{\dot H^{1/2}}\sim cN^{1/2-\gamma},\qquad
   \|a_Ne_N\|_{\dot H^3}\sim cN^{3-\gamma},
   \]

   and the open strip (1/2<\gamma<3), where the first two powers are
   negative and the last is positive;
3. on the configured grid (10^{-3}\le\tau\le10), the exact discrete
   maximum

   \[
   \max_{k\in\mathbb Z^3\setminus\{0\}}
   |k|^3e^{-\tau|k|^2}
   \]

   and the continuous radial upper bound

   \[
   \left(\frac{3}{2e\tau}\right)^{3/2}.
   \]

The lattice enumeration uses the cutoff (|k|^2\le4096).  This encloses the
global maximum for every configured time because

\[
4096>\frac{3}{2\tau_{\min}}=1500,
\]

and (r^3e^{-\tau r^2}) is strictly decreasing after its continuous radial
maximum.  The producer enumerates nonnegative integer triples directly.  The
independent validator instead enumerates admissible squared radii with
Legendre's three-square characterization and does not import or call the
producer.

Both paths compare their calculations with
`research/figures/r073p/fig-r073p-critical-frequency-gate/`.  The comparison
binds the figure configuration, source data, results, and validation by
SHA-256.  No PDF is read, written, rendered, or required by this package.

## Claim boundary

The checked statements are closed-form and finite-lattice formula diagnostics
only.  They are not:

- a Navier--Stokes simulation;
- a nonlinear entry certificate for an (H^{1/2}) or (H^3) tube;
- a necessary condition for a PDE solution;
- a proof of a global regularity theorem;
- a proof or partial proof of the Clay Millennium problem.

The exact machine-readable boundary is stored in `config.json` and copied
unchanged into every certificate layer.

## Reproduction and monitoring

Run the commands in `command.txt` from the repository root.  The calculation
uses only the Python standard library, one process, and no GPU.  Scientific
stages are recorded in `progress.ndjson`; wall time and peak resident memory
are recorded in `resource-log.ndjson`.

`validate_certificate.py --verify-only` and `seal_package.py --verify-only`
are fail-closed and perform no writes.

## Two-stage provenance seal

Running `seal_package.py` without `--source-commit` creates the required
`hash-bound-uncommitted` pre-seal.  It binds the nine source files and eight
pre-seal outputs by SHA-256, while explicitly leaving the immutable source
commit unassigned.

After a parent release commits the nine source files, it may run

```text
seal_package.py --source-commit <full-lowercase-40-hex>
```

to produce the final commit-bound seal.  The sealer never substitutes the
current `HEAD` for an explicit commit and rejects a commit whose source blobs
are not byte-identical to the current package sources.
