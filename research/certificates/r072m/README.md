# R0.72M phase-mixing finite-audit bundle

This bundle supports the analytic R0.72M scalar danger-window theorem and the
complete one-carrier zero-diffusion benchmark. The proof is in
research/r072m_report-source.md; the finite artifacts have narrower jobs:

1. classify the exact scalar superlevel interval for declared parameter cases;
2. corroborate the full-lattice Bessel mass and gradient-moment identities;
3. evaluate the complete negative-norm action by two independent routes;
4. approach the proved frozen true-cubic coefficient 16/pi^2; and
5. compare two independently implemented finite dissipative diagnostics.

The producer uses differentiated Bessel functions, Gauss quadrature, and an
angular FFT phase split. The independent route uses Bessel recurrences,
angular Parseval sampling, separate quadrature, and a finite-chain
diagonal/Cayley split. crosscheck.json compares common observables with
field-specific tolerances.

The zero-diffusion reference deletes the relative diagonal heat operator and
is not the dissipative triangular PDE. The dissipative CSV files are finite
binary64 diagnostics, not interval certificates or continuum asymptotic
proofs. Nothing in this bundle proves general three-dimensional
Navier--Stokes regularity or a finite-time singularity.

Run command.txt from the repository root. The producer and independent
configs record the source commit. Rebuild SHA256SUMS only after every other
file in this directory is final.
