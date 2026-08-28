# R0.72Z deterministic finite certificate

This bundle has two genuinely separate routes.  `generate_certificate.py`
uses exact rational ledgers, explicit formulas, and direct symmetric Fourier
sums.  `independent_recompute.py` does **not** import the producer; it instead
uses direct Fourier action, paired lattice enumeration, Poisson summation,
polynomial convolution, and deterministic Simpson quadrature.

The fail-closed validator checks the commutator and Fourier matrix, the exact
`M3` formula and sampled `s` bound, the strong-row alpha power, low- and
high-mode witnesses, the gapless tangent residual, the collision-scaled
cubic coefficients, kinetic orientation and lattice identities, causal
kernel integrals, the damping-gap `J` formula, source hashes, and the complete
claim ledger.

The certificate **does not** machine-check an infinite-dimensional low-gap
Orr--Sommerfeld propagator, a collision-scale limiting absorption theorem,
equality of a finite truncation with the full operator norm, a Bloch-uniform
physical velocity direct sum, a complete linearized shear subsystem, any
nonlinear Navier--Stokes estimate, or the Clay Millennium problem.  Those
boundaries are mandatory false booleans and OPEN claim keys; deleting or
flipping one makes validation fail.

The formal figure is sealed separately through Git ancestry and visual QA.
Its displayed high-mode range includes the complete declared sequence,
including the (n=1) witness; the certificate does not treat the figure as
analytic proof.

Run the commands in `command.txt` from the repository root.  All outputs are
deterministic for fixed source bytes and the bundled Python runtime.
