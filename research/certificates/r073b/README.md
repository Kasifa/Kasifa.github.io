# R0.73B physical-kinetic and Bloch-cancellation certificate

This package separates exact algebra from finite numerical evidence.

The exact rational ledger checks:

1. the general-Bloch near-carrier cancellation
   `Pi0(Wr+Wxx L^-1r)=g Pi0(WL^-1r)+2i beta Pi0(W_xL^-1r)`;
2. entrywise similarity of the raw-q finite matrix and the exact `(h,r)`
   near-carrier matrix for four rational `(beta,mu,c)` cases;
3. the sharp heat-profile identity
   `||W_x(d)||_infinity=(e^-d+e^-4d)/2` and its primitive;
4. the Young inequality producing the `|Lambda| K/2` physical-velocity norm
   exponent;
5. the formal block powers `(1-p)_+` for raw q and `(a/2-p)_+` for the
   diagonal weighted family;
6. the fixed-Lambda triangular h-column coefficient and the low-gap star
   coefficient for the sharpened kinetic shear form.

The finite crosscheck binds the independently validated experiment under
`experiments/r073b`: 280 propagators, 1,960 norm rows, targeted asymptotics,
step/mode refinement, and a direct kinetic-generator numerical-abscissa check.
The validator does not import the producer. It refits selected exponents from
CSV and recomputes the triangular singular value with a standalone scalar
power iteration. `independent_recompute.py` separately materializes those
scalar checks before either certificate stage is generated.

The source binding also covers the problem freeze, proof source, report source,
literature audit, gap matrix, and independent analytic audit. Any edit to one
of those files therefore requires regenerating the source-stage snapshot before
the source commit is sealed.

## Two-stage lifecycle

`--source-stage` writes a reproducible working-tree snapshot with `pending`
commit fields. It is unsealed.

`--formal --source-commit <40hex>` verifies that every bound source is exactly
the corresponding Git blob and only then emits a formal certificate. The
certificate commit is intentionally not self-referential; a later figure or
release manifest may bind it.

## Strict boundary

The rational checks certify only their displayed coefficient identities. The
CSV checks certify finite matrices at sampled parameters. This package does
not prove a Galerkin tail bound, an infinite-dimensional convergence theorem,
a complete Orr--Sommerfeld/Squire `A2` direct sum, nonlinear frequency
closure, global Navier--Stokes regularity, or the Clay Millennium problem.
