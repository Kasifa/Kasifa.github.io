# R0.70B exact 3:4:5 triad audit

This archive checks the finite-dimensional symbolic arithmetic in Theorem 8.1
of `research/r070b_report-source.md`.

The producer derives the Euler-derivative and annular-target matrices from the
wavevectors, helical polarizations, Biot--Savart velocity symbol, Leray
projector, and strain symbol.  The two coefficient tables are not supplied as
producer inputs.  All decision quantities are exact SymPy rational
expressions; the result contains no floating-point decision.

The audit verifies:

- the divergence-free and helical eigenvector relations;
- the four derivative and target rows for the 3:4:5 interaction triad;
- rank two of the derivative matrix and its energy gauge;
- two exact left-null vectors and the necessary condition
  `16*g4 - 9*g3 - 7*g5 = 0`;
- cancellation of the quadratic Bessel term;
- the nonzero quartic coefficient `72/5` multiplying the positive moment
  `I4`.

The archive does **not** turn the analytic wave-packet limit or the
orthogonal-group averaging argument into a computer-assisted proof.  Those
parts remain proved in prose in the canonical report.  It also does not
exclude non-translation-invariant, nonquadratic, time-nonlocal normal forms,
or exact identities with an uncontrolled same-order remainder.  It proves no
Navier--Stokes regularity or singularity result.

## Reproduction

From the repository root, run the command recorded in `command.txt`.  The
expected producer environment is recorded in `environment.txt`.

## Payloads

- `result.json`: exact symbolic output and claim boundary;
- `command.txt`: reproduction command;
- `environment.txt`: baseline and interpreter versions;
- `SHA256SUMS`: hashes of the producer, result, command, environment, and this
  README.
