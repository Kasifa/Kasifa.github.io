# R0.70D exact fixed-scale cover-blindness audit

This archive checks the finite-dimensional arithmetic used in the R0.70D
fixed-resolution sign-obstruction theorem.

The producer verifies, with exact SymPy arithmetic:

- the negative-part integral of
  \(f_{\delta,N}=\delta+\sin(Nx_1)\) on the three-torus;
- its value at \(\delta=1/2\), its limit as \(\delta\downarrow0\), and the
  leading negative-to-signed ratio;
- the derivative that makes the negative mass monotone on the locked
  interval;
- the frequency-gate algebra giving the normalized interval
  \([\delta/2,3\delta/2]\).

The archive does **not** computer-prove the integration-by-parts estimate for
arbitrary \(W^{1,1}\) cutoffs, the optimal-cover definitions, or any
Navier--Stokes realization.  The witness is an abstract scalar density.  It
does not negate cascade results that use local PDE balances, geometric
hypotheses, or information over additional scales.  No regularity or
singularity claim is made.

## Reproduction

From the repository root, run the command recorded in `command.txt`.  The
expected producer environment is recorded in `environment.txt`.

## Payloads

- `result.json`: deterministic exact symbolic output and claim boundary;
- `command.txt`: reproduction command;
- `environment.txt`: baseline and interpreter versions;
- `SHA256SUMS`: hashes of the producer, result, command, environment, and this
  README.
