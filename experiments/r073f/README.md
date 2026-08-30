# R0.73F finite moving-profile diagnostic

This package evaluates finite Fourier compressions of the exact moving
profile on the declared row \(\gamma=1/2\), \(\beta=\xi=0\).  It is an
IEEE-754 binary64 implementation, convergence, and falsification diagnostic.
It is not an interval computation or a proof about the continuum operator.

The diagnostic endpoint is

\[
 d_{\mathrm{diag}}=0.01.
\]

It is deliberately **not** identified with the existential analytic
roughness window \(d_0\).  R0.73F does not provide a numerical value of
\(d_0\).

The primary grid uses the complete matrices on modes \(-96,\ldots,96\) and
the eight viscosities in `config.json`.  For each row it stores the full
propagator norm and the conorm obtained by propagating an orthonormal basis
of the finite leading Riesz cluster.  The kinetic-space conjugation makes
the Euclidean norm the finite physical kinetic norm.

Cutoffs \(24,48,96\), three fast-time step sizes, a separately written
Fourier-coefficient matrix constructor, sign conjugacy, the R0.73B
\(5/16\) upper sentinel, the exact \(49/4\) drift bound, and two exact
finite-dimensional counterexamples are checked independently.  Ordinary
cutoff agreement remains a reported diagnostic and is never treated as a
Fourier-tail enclosure.

## Reproduction

Use the pinned dependency directory named in `command.txt`.  The producer
writes progress continuously and uses only local dense CPU linear algebra.
The independent validator does not import the producer.

## Evidence boundary

Nothing here proves a continuum spectral gap, a continuum evolution
dichotomy, a continuous-time operator bound, an explicit analytic value of
\(d_0\), a nonlinear Navier--Stokes estimate, or the Clay problem.
