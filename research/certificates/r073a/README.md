# R0.73A finite-Fourier certificate

This source-stage package independently audits four finite-dimensional shadows
of `research/r073a_transient_proof.md`:

1. the exact Fourier-mode mean cancellation;
2. entrywise similarity of the raw-q matrix and the `(h,r)` matrix;
3. the hidden-mean derivative in (5.2), including its `mu -> 0` limit;
4. a deterministic direct propagator crosscheck against
   `exp[-mu(d-s)+|c|J(s,d)]`.

The producer uses exact rational coefficient ledgers plus an `(h,r)` RK4
crosscheck. A genuinely separate producer, `independent_recompute.py`, starts
from the raw-q matrix and writes
`experiments/r073a/xmu_propagator_certificate.csv`. The validator does **not**
import either producer: it reconstructs the raw-q matrix, checks the diagonal
change of variables, integrates the raw-q system, and compares every CSV row.

The L2 normalization used in the constant audit is `dx/(2*pi)`. No random
numbers are used. `SHA256SUMS` covers every flat regular file, while
`manifest.json` binds the canonical report, analytic audits, experiment
producer/validator/manifests, figure sources, release sources, and theorem
tests by byte count and SHA-256.

The supporting exact ledger also checks the orthogonal projection-speed
identity, all four Fourier coefficients of `G`, the `c != 0` two-mode leakage
and its kernel line, and rational samples of the normalized `B*` constant
coefficient `1/g`. These remain algebraic support only: the actual OS off-block
carries the coupling factor `|c|`, and no operator-norm discontinuity or full
operator theorem is inferred from the coefficient ledger.

## Two-stage lifecycle

`--source-stage` records exact working-tree bytes and writes `pending` into the
CSV commit columns. It is reproducible but unsealed.

`--formal --source-commit <40hex>` first verifies that the commit exists and
that every bound source is byte-for-byte identical to its blob in that commit.
Only then may it write `status=formal` and the fixed `sourceCommit`. Any missing,
untracked, or stale bound source fails closed before certificate outputs are
rewritten.

There is intentionally no self-referential certificate commit. The formal CSV
keeps `certificateCommit=pending` (or the later figure workflow may describe it
as `bound-by-figure-manifest`). A separate clean certificate commit `C` is bound
by the formal figure manifest after this package is committed; the certificate
is not endlessly regenerated to contain its own future hash.

## Boundary

This certificate checks finite Fourier matrices and the stated algebraic
constants. The numerical grid is only a crosscheck. It does **not** prove the
infinite-dimensional propagator theorem, an enhanced-dissipation rate, a
physical kinetic-energy estimate, an Orr--Sommerfeld/Squire direct sum, a
nonlinear Navier--Stokes theorem, or the Clay Millennium problem.

The present manifest remains `source-stage` until a real frozen source commit
exists. Neither lifecycle stage asserts website publication.
