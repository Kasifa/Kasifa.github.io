# R0.72H certificate bundle

This bundle records the finite producer and independent audits for the
critical-log mixed-row theorem and the all-odd Rudin--Shapiro sharpness
family.

## Authoritative claims

The theorem and its proof are in:

- research/r072h_report-source.md
- research/r072h_gap_matrix.md
- research/r072h_independent_audit.md
- research/r072h_literature_audit.md

The numerical files corroborate finite cases only.

## Producer route

- source: research/r072h_exact_audit.py
- sign construction: Rudin--Shapiro polynomial recurrence
- state representation: original complex Fourier lattice
- integrator: DOP853 in \(y=M^2x\)
- quadrature: Simpson after \(y=z^3\)
- result: result.json
- raw table: producer-data.csv
- monitor/progress/resources: producer-monitor.log,
  producer-progress.ndjson, producer-resource.ndjson

## Independent route

- source: research/r072h_independent_audit.py
- sign construction: binary adjacent-\(11\) parity
- state representation: exact all-odd real gauge
- integrator: RK45
- quadrature: Gauss--Legendre after \(y=z^3\)
- result: independent-result.json
- raw table: independent-data.csv
- monitor/progress/resources: independent-monitor.log,
  independent-progress.ndjson, independent-resource.ndjson

Both final results have status "passed". The maximum relative discrepancy
between the two routes is \(3.31\times10^{-6}\).

## Preserved failed attempts

- producer-attempt1-failed-*: an overstrict small-\(M\) root-slope and
  finite-profile pass contract returned "failed".
- producer-attempt2-failed-*: the extended sweep completed but the final
  monotonicity check used an invalid strict pairwise iterator.

These files are retained so that the acceptance contract remains auditable.

## Reproduction

Run the commands in command.txt from the repository root with the declared
research Python environment. Rebuild SHA256SUMS only after all other bundle
files are final.

## Boundaries

The computations do not prove an asymptotic theorem, an infinite-lattice
error estimate, a physical \(D^{1/3}\Lambda_{1,*}\) counterexample, or any
general three-dimensional Navier--Stokes statement.
