# R0.73C certified frozen Rayleigh instability

This package binds two exact/validated results and keeps every later gate
explicit.

1. **C3 (exact singular neutral spectrum).**  For
   `W=-sin(x)/2+sin(2x)/4`, the periodic mode
   `phi0=|sin(x/2)|^3` belongs to `C2 cap H2_per` but not `C3`, and

   ```text
   (-d_x^2 + W''/W) phi0 = -(7/4) phi0.
   ```

   After the Pöschl--Teller transform the Friedrichs spectrum is
   `((n+3)^2-16)/4`, `n=0,1,...`; hence `-7/4` is the unique negative
   threshold.

2. **C4 (one infinite-dimensional frozen unstable row).**  At `gamma=1/2`,
   the periodic Rayleigh ODE has monodromy trace `F(eta)=tr(M(eta))-2`.
   Exact ODE lemmas give `det(M)=1`, real trace, and periodicity iff `F=0`.
   Two pinned `mpmath.iv` partitions and a separately implemented Decimal
   directed-rounding kernel certify

   ```text
   F(0.3407) < 0 < F(0.3410).
   ```

   Continuity therefore gives a point eigenvalue
   `sigma=eta/2 in (0.17035,0.17050)`.

The finite Fourier and sampled-contour files are bound as diagnostics only.
They are not used to prove the infinite-dimensional eigenvalue.

## Lifecycle

`generate_certificate.py --source-stage` records a deterministic SHA-256
snapshot with every commit field set to `pending`.  This stage is useful for
review but is not sealed.

After all bound sources have been committed, run

```text
python3 research/certificates/r073c/generate_certificate.py --formal --source-commit <40-hex-commit>
python3 research/certificates/r073c/validate_certificate.py --require-formal
```

The formal generator first verifies that every working-tree source is byte
identical to the specified Git blob.  It fails before rewriting certificate
outputs if any source is missing, modified, or absent from the commit.
`independent_recompute.py` first materializes a standalone standard-library
recomputation.  The validator also does not import the producer; it
independently redoes the rational coefficient identities, exact-binary
endpoint signs, Decimal sentinels, source bindings, and package inventory.
The Sturm--Liouville completeness and ODE continuity/Liouville lemmas remain
human-audited analytic arguments whose exact source bytes are bound; this
package does not mislabel those lemmas as machine-verified formal proofs.

For the current unsealed review stage use the first four commands in
`command.txt`.

## Boundary

The certificate proves existence, not uniqueness or algebraic simplicity of
the root.  It does not prove viscous eigenvalue persistence, a uniform Riesz
contour, complementary dichotomy, graph-domain Kato transport, nonautonomous
fast-time growth, a complete Orr--Sommerfeld/Squire `A2` direct sum, a
nonlinear Navier--Stokes estimate, or the Clay Millennium problem.  In
particular, C5 remains open and the complete-row super-polynomial consequence
remains conditional on C5.
