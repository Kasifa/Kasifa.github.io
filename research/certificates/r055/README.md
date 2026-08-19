# R0.55 critical Fourier bridge and scalar-charge certificate

## Scope

This directory archives the deterministic exact regression attached to the
R0.55 note. The analytic note proves three separate statements:

1. the Fourier--Leray estimate in the scale-critical
   \(\mathcal X^{-1}\) framework, with a finite heat-Duhamel bridge to a
   scalar degree majorant;
2. the exact high--high-to-low identity
   \[
   p_N=(N,0,0),\quad q_N=(-N,1,0),\quad p_N+q_N=(0,1,0),
   \]
   whose normalized critical symbol ratio is one for every positive integer
   \(N\);
3. every scalar charge that is additive under convolution and invariant
   under all rotations is zero, with the analogous result for the
   orientation-preserving cubic rotation group on \(\mathbb Z^3\).

The displayed proofs in
research/fourier_critical_charge_bridge_note.md establish the all-frequency
statements. The finite loops archived here are exact implementation
regressions and figure data, not substitutes for those proofs.

The result does not construct a bridge from arbitrary Fourier data to the
current nontrivial charge-degree generator. It rules out that direct bridge
only when the scalar charge itself is required to be both additive and
rotation invariant. Directional, vector-valued, and multi-frame interfaces
remain open. No claim about three-dimensional Navier--Stokes large-data
regularity or singularity is made.

## Pinned source

The formal run is pinned to

    640cf4ce9b97c2caa8d22f9159b4d0aa2e3a65a0

The audit source is
research/fourier_critical_charge_bridge_audit.py.

## Exact run

From the repository root:

    tmp/r024-venv/bin/python research/run_with_monitor.py \
      --output research/certificates/r055/resources.csv \
      --interval 0.25 \
      -- \
      tmp/r024-venv/bin/python \
      research/fourier_critical_charge_bridge_audit.py \
      --max-triad-index 200000 \
      --max-catalan-degree 256 \
      --rotation-radius 12 \
      --source-commit 640cf4ce9b97c2caa8d22f9159b4d0aa2e3a65a0 \
      --progress \
      --progress-log research/certificates/r055/progress.ndjson \
      --check \
      --pretty \
      --output research/certificates/r055/fourier-critical-charge-bridge.json

The run passed 17 checks. It verified:

- 200,000 exact integer high--high-to-low triads;
- 15,624 exact rational half-turn matrices in \(SO(3)\);
- the Catalan recurrence and closed formula through degree 256.

The exact finite-regression digests stored inside the certificate are:

    triads     80485297fb8199ad9ebbb4c6a4d1bd3b3ca0482a2185301cacc6950a8523e649
    rotations  86abf552bb72e14454774679ac22162c284bc9653fa235b0a9c0a107b7491a6d
    Catalan    3161637c9d50b1f48f12eb301e4afb518473d3f42e2fb631c55d03b97c56cf80

## Monitoring

The scientific audit reported 5.312455 seconds of wall time. The independent
process-tree monitor recorded 21 samples over 5.384576 seconds, with peak CPU
usage 100.0%, peak resident memory 40.000 MiB, and no GPU process. The run
used Python 3.12.13 with exact integers and fractions.Fraction. It used no
randomness and no floating-point sign decision.

## Files

- fourier-critical-charge-bridge.json: machine-readable theorem
  classification, exact regressions, digests, checks, and provenance;
- progress.ndjson: append-only stage log;
- resources.csv: process-tree resource samples;
- SHA256SUMS: hashes of the archived files.

## Literature boundary

The \(\mathcal X^{-1}\) small-data framework is prior work:

- Z. Lei and F.-H. Lin, *Global Mild Solutions of the Navier--Stokes
  Equations*, Communications on Pure and Applied Mathematics 64 (2011),
  1297--1304, <https://doi.org/10.1002/cpa.20361>,
  <https://arxiv.org/abs/1203.2699>.

R0.55 records that classical critical baseline and proves the narrower
scalar-charge interface obstruction stated above. It does not present the
Lei--Lin theorem as a new result.
