# R0.72I certificate bundle

This bundle records the finite producer and independent audits for the
physical normalization ledger and the all-odd parity repair of the residual
cubic row.

## Authoritative claims

The theorem, proof, and audit boundary are in:

- `research/r072i_report-source.md`
- `research/r072i_gap_matrix.md`
- `research/r072i_independent_audit.md`
- `research/r072i_literature_audit.md`

The numerical files corroborate finite cases only.

## Producer route

- source: `research/r072i_exact_audit.py`
- sign construction: Rudin--Shapiro polynomial recurrence
- state representation: original complex Fourier lattice
- integrator: SciPy DOP853 in the rescaled variable \(y=M^2x\)
- quadrature: Simpson after \(y=z^3\)
- truncation radius: \(8M\)
- finite sizes: \(M=4,8,16,32,64,128\)
- result: `result.json`
- raw table: `producer-data.csv`
- monitor/progress/resources: `producer-monitor.log`,
  `producer-progress.ndjson`, `producer-resource.ndjson`

The producer result has status `passed`; all 10 declared checks are true.
At \(M=128\), its recorded values are

- `criticalQ = 99.88231697316388`;
- `deltaIntegralAbsHB = 0.3880135382491635`;
- `ratioGenericB = 8.69825769204549`;
- `measuredBvLiftedRatio = 0.003563151907706173`;
- `genericBToMeasuredHB = 206158376.83253548`;
- `evolvedRootResidual = 6.765421556309548e-17`.

## Independent route

- source: `research/r072i_independent_audit.py`
- sign construction: parity of overlapping adjacent binary `11` blocks
- state representation: exact all-odd real gauge
- integrator: SciPy RK45 in the rescaled variable \(y=M^2x\)
- quadrature: 280-point Gauss--Legendre after \(y=z^3\)
- truncation radius: \(9M\)
- finite sizes: \(M=4,8,16,32,64\)
- result: `independent-result.json`
- raw table: `independent-data.csv`
- monitor/progress/resources: `independent-monitor.log`,
  `independent-progress.ndjson`, `independent-resource.ndjson`

The independent result has status `passed`; all 14 declared checks are true.
At its largest size \(M=64\), its recorded values are

- `criticalAction = 57.330231441283466`;
- `deltaAbsHbIntegral = 0.16464089647057176`;
- `mixedRow = 4095.7772685990744`;
- `rootH = 68.00844164037157`;
- `liftedGenericBRatio = 5.555618885438757`;
- `liftedMeasuredCubicRatio = 1.1269362911973388e-7`;
- `evolvedRootResidual = 1.1254018550399536e-16`.

## Cross-route audit

The CSV rows reproduce their corresponding JSON case objects exactly after
numeric parsing. Across the five common sizes, using the producer value as
the relative-error denominator, the largest cross-route discrepancies are:

| Shared quantity | Maximum relative discrepancy | Size attaining it |
|---|---:|---:|
| critical action \(Q_*\) | `1.5620882395583527e-6` | 4 |
| \(\delta\int |hb|\) | `1.6036921699227625e-4` | 16 |
| mixed row \(\int |hQF|\) | `9.573777252374204e-10` | 4 |
| exact-root \(|h|\) | `3.6093568825426533e-9` | 4 |

Thus the largest discrepancy among these four shared observables is
`1.6036921699227625e-4`. The two routes intentionally use different gauges,
integrators, quadratures, and truncation radii.

## Reproduction

Run the commands in `command.txt` from the repository root with the declared
research Python environment. Rebuild `SHA256SUMS` only after all other bundle
files are final.

## Boundaries

The computations do not prove an asymptotic estimate, certify the complete
temporal root set, enclose floating-point and truncation errors by intervals,
cover mixed-parity carriers, or establish any general three-dimensional
Navier--Stokes regularity result.
