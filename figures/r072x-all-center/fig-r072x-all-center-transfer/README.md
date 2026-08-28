# R0.72X all-center exact-path figure

This package is the paper-ready four-panel figure source for R0.72X.  It
combines exact finite-alpha interface arithmetic and exact block-count
arithmetic with a deterministic finite-grid diagnostic of the full shifted
two-harmonic potential.

The discrete norm estimate uses a fully double-reorthogonalized
Lanczos-Ritz method on \(U^*U\).  The deterministic policy begins at Krylov
dimension 8, checks every 4 dimensions, and stops no later than dimension 32
only when an actual-space recomputation of \(Av-\lambda v\) is at most
`1e-10` relative to \(\lambda\).  A configuration that misses that tolerance
fails the build instead of emitting a norm estimate.
An exact or near-exact Krylov breakdown before dimension 8 is also rejected
conservatively; the build does not reinterpret an early breakdown as a
passing configuration.

The archived `normEstimate` is computed directly as \(\|Uv_{\rm Ritz}\|_2\),
not inferred from the projected eigenvalue.  Every row also records the
relative discrepancy from \(\sqrt{v_{\rm Ritz}^*U^*Uv_{\rm Ritz}}\); the
global `rayleighNormDefect` QA gate is `1e-10`.  All numerical scalar fields
must be finite, and each fine-grid relative-to-fine value must be exactly zero.

The analytical question is whether the exact collision family remains
numerically stable as the physical block center ranges over the complete heat
history, and how the interface geometry and block ledger reflect the analytic
R0.72X theorem.  The numerical scan does not prove graph coercivity, compute
the nonconstructive constant, or certify an infinite-dimensional norm.  It
also does not independently certify the global largest singular value of the
finite propagator: a single fixed seed and a small actual Ritz residual certify
the returned Krylov-space Ritz pair, not that the seed saw the top eigenspace.

`--self-test` writes nothing.  A formal render requires the source-bound
R0.72X certificate, a distinct clean certificate commit, and an explicit
visual-inspection flag.  Existing formal outputs are never overwritten.
