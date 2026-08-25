# R0.70Y exact-certificate bundle

This directory archives the finite exact audit for the R0.70Y
response-slope, critical Besov, and top-eigenvalue gate.

## Decision locked by the bundle

The producer checks six finite groups:

1. response-chord, symmetric, metric/response, wedge-norm, and Gram-trace
   identities;
2. an actual \(M\ge4\) radial-frame family with zero affine response area
   and zero three-response Gram determinant but nonzero cyclic block;
3. the scale-separation arithmetic used by the \(q=3\) packet obstruction;
4. the 49/197 filler covariance algebra and the ledger supporting the uniform
   \(\lambda_1(Q)\ge1/41210\) lower bound;
5. exact curve residuals and an explicit point showing that the filler does
   not have a principal eigengap; and
6. a forty-mode Fourier/Parseval reconstruction with 376 defect outputs and
   signed work
   \[
   -81\Lambda^3(62+1639\kappa)/32780.
   \]

The coefficients at \(\Lambda^2\), \(\Lambda\), and \(1\) are all exactly
zero.  The gradient ledger is

\[
 \|\nabla\omega_\Lambda\|_2^2=1188\Lambda^2+20605.
\]

## Files

- `result.json` — canonical sorted JSON emitted by the producer;
- `command.txt` — exact reproduction command;
- `environment.txt` — pinned runtime and dependency record;
- `SHA256SUMS` — hashes for every archived payload and producer dependency;
- `../../r070y_exact_audit.py` — R0.70Y producer; and
- `../../r070x_exact_audit.py` — imported thirty-six-mode R0.70X dependency.

## Analytic boundary

The finite producer does not replace the periodic localized-kernel lemma or
the Littlewood--Paley sequence proof in `../../r070y_report-source.md`.  It
does not prove a general Coifman--Meyer endpoint theorem, a principal-eigengap
no-go result, control of \(\int S:Q\), an enstrophy closure, a continuation
criterion, global regularity, or a solution of the Millennium problem.

No DNS, stochastic search, GPU, or DGX resource is used.
