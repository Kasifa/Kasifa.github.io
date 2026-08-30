# R0.73N theorem-relevant finite diagnostic

This two-stage package independently checks the elementary finite-strain quantities
used by the R0.73N fixed-background feasibility/obstruction gate.  It is a
reproducibility and error-detection package, not a proof substitute.

The package checks:

1. the normalized exact strain envelope
   \(s(t)=e^{-4t}+e^{-16t}\), including the equality witness
   \(y=\pi/2\);
2. \(j(T)=\int_0^T s(t)\,dt\) and the exact limit
   \(j(\infty)=5/16\);
3. the high-precision value of \(j_*=j(1/1800)\);
4. the exact strict chain
   \(j_*>359/324000>173/450000>\mathcal A_*\), where only the last
   comparison uses the already sealed R0.73M continuum action upper bound;
5. finite exponent-factor curves across the marked background family.

The first inequality is validated against the analytic lower witness

\[
j_* > \frac{D_*}{2}-\frac{5D_*^2}{8}
     =\frac{359}{324000},\qquad D_*=\frac1{450},
\]

which follows from \(1-e^{-x}>x-x^2/2\) for \(x>0\).  Floating-point
evaluation is not used to prove that inequality.

## Evidence boundary

The inherited interval
\(167/450000<\mathcal A_*<173/450000\) is copied as an immutable theorem
input and is never recomputed or upgraded by this package.  The plotted
exponent factors are illustrative evaluations of exact formulas.  They do
not certify the sharp local flow-map modulus, arbitrary fixed-background Lyapunov
instability theorem, full three-dimensional FPS \((H^3,L^2)\) stability,
critical-norm growth, finite-time singularity, or the Clay problem.

Run the commands in `command.txt` from the repository root.  `--verify-only`
is fail-closed and performs no writes.  Before an immutable theorem-source
commit is assigned, the manifest status is `hash-bound-uncommitted`; after
successful commit/blob verification, it is `sealed`.

## Two-stage provenance seal

Running `seal_package.py` without `--source-commit` produces the pre-seal
`hash-bound-uncommitted` state.  After the nine package source files have
been committed, run `seal_package.py --source-commit <40-hex>` and then its
`--verify-only` form.  Final sealing succeeds only if that commit exists and
contains byte-identical regular blobs for all nine source bindings.  The
sealer never substitutes the current `HEAD` for an explicit commit.
