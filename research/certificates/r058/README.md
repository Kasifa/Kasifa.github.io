# R0.58 exact Duhamel critical-saturation certificate

This directory archives the deterministic audit for
`research/duhamel_critical_saturation_note.md`.

## Supported formal statements

The analytic note proves, for every eligible shell index:

1. the exact first-Duhamel coefficient
   \(e^{-t}\sum_N(1-e^{-2N^2t})/(2N^2)\);
2. the all-index envelope \(1/(32L)\le d_L(t_L)\le1/(2L)\) at
   \(t_L=(\log2)/(2L^2)\);
3. normalized shell scalings \(L^{-2}\), \(L^{-1}\), and \(L^{-3}\) in
   the fixed-output block, Fourier \(\mathcal X^{-1}\), and
   \(\dot H^{1/2}\) tests;
4. a Rudin--Shapiro prefix and weighted-Abel estimate;
5. shell-uniform positive lower bounds for the heat-Besov and periodic
   \(BMO^{-1}\) bilinear quotients.

The finite run is an exact implementation regression, not the proof of these
all-index statements.

## Formal run

Source commit:

`35a817f00d8821e91f033764f6bd29fc1697ad56`

Command:

```text
python3 research/run_with_monitor.py \
  --output research/certificates/r058/resources.csv \
  --interval 0.25 \
  -- python3 research/duhamel_critical_saturation_audit.py \
  --maximum-shell 4096 \
  --maximum-rs-level 22 \
  --source-commit 35a817f00d8821e91f033764f6bd29fc1697ad56 \
  --progress \
  --progress-log research/certificates/r058/progress.ndjson \
  --check --pretty \
  --output research/certificates/r058/duhamel-critical-saturation.json
```

Result:

- status: passed;
- formal checks: 24;
- exact packet modes checked: 8,390,656;
- largest Rudin--Shapiro polynomial: 4,194,304 coefficients;
- scientific wall time: 25.760813 seconds;
- monitored elapsed time: 25.873088 seconds;
- monitor samples: 97;
- peak CPU: 100.0%;
- peak resident memory: 951.469 MiB;
- GPU samples: none;
- randomness: none;
- floating-point mathematical decisions: none.

## Boundary

The certificate does not establish norm inflation, unboundedness of the
Koch--Tataru bilinear map, a compactly supported Euclidean construction,
control of higher Picard iterates, large-data regularity, or a solution of the
three-dimensional Navier--Stokes Millennium problem.
