# R0.73A hidden-mean, transient-envelope, and frozen-spectrum figure

This package is the reproducible source for a three-panel, double-column
journal figure. It keeps three kinds of evidence visually and logically
separate:

1. the exact normalized hidden-mean bracket and its path-sensitive limit;
2. the proved analytic `X_mu` transient envelope; and
3. independently validated finite Fourier--Galerkin frozen-time diagnostics.

Panel B does not currently contain a certified nonautonomous `X_mu`
propagator-gain grid because no such upstream artifact exists. The reserved
overlay is visibly labelled `PENDING - NOT PLOTTED`. Draft rendering may retain
that dependency label; formal rendering must fail until a certificate CSV with
the declared schema and provenance is supplied.

Panel C reads the validated `N=40` target rows from
`experiments/r073a/target_dynamics.csv`. These values are finite-dimensional
counterexample-screening evidence only. They do not prove the spectrum,
pseudospectrum, or semigroup behavior of the infinite-dimensional frozen
operator, and they do not prove the nonautonomous propagator.

All analytic curves are direct closed-form evaluations. No regression, random
seed, interpolation, or fitted exponent is used. Blue and gold are the only
chromatic roots; stroke pattern, open/filled markers, direct labels, zero
references, and panel structure preserve meaning in grayscale.

Panel A plots `h_d/(i c_mu)`, not an unconditional limit of `h_d`. Its bracket
has a nonzero `mu -> 0` limit along `c_mu -> c0 != 0`, equivalently the scaling
`Lambda_mu ~ 1/gamma`. At fixed `Lambda`, one has `c_mu -> 0`; this figure does
not decide the resulting limit of `h_d`.
Moreover, for every positive gap the instantaneous lifted line is not invariant;
the normalized bracket is a diagnostic identity, not a closed positive-gap
one-dimensional dynamics.
