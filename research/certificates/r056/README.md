# R0.56 exact Leray polarization-channel certificate

## Scope

This directory archives the deterministic exact regression attached to the
R0.56 note. The analytic note works in the triad-adapted Craya--Herring frame
and proves four pointwise statements for noncollinear Fourier frequencies
\(p+q=k\):

1. the ordered critical Fourier--Leray symbol has exactly two transverse
   output channels;
2. its normal-channel gain is
   \[
   g_N=\frac{|p\times q|}{|p||k|}=\sin\angle(p,k),
   \]
   and is the exact operator norm;
3. its in-plane gain obeys
   \[
   g_T\le\frac{|q|}{2|p|}\le\frac{1+\rho}{2}<1
   \quad\text{when }|k|/|p|\le\rho<1;
   \]
4. the normal channel still attains one at arbitrary high--high-to-low
   separation and its positive angular moments have no shell decay.

The two-polarization Fourier decomposition is classical prior art. R0.56 does
not claim to invent the Craya--Herring or helical basis. Its narrower result is
the exact critical channel norm, equality classification, strict planar gap,
and surviving one-channel obstruction.

The displayed proofs in
`research/leray_polarization_channel_note.md` establish the all-frequency
statements. The finite loops archived here are exact implementation
regressions, not substitutes for those proofs.

The result does not construct a closed anisotropic Banach algebra, control
cancellation between different normal-channel triads, connect arbitrary data
to the R0.54 charge-degree generator, or prove a large-data estimate. No claim
about three-dimensional Navier--Stokes regularity or singularity is made.

## Pinned source

The formal run is pinned to

    1b736121127e91727b8ab7ff1b2fd90c2ee873f6

The audit source is
`research/leray_polarization_channel_audit.py`.

## Exact run

From the repository root:

    tmp/r024-venv/bin/python research/run_with_monitor.py \
      --output research/certificates/r056/resources.csv \
      --interval 0.25 \
      -- \
      tmp/r024-venv/bin/python \
      research/leray_polarization_channel_audit.py \
      --cube-radius 5 \
      --max-family-index 200000 \
      --source-commit 1b736121127e91727b8ab7ff1b2fd90c2ee873f6 \
      --progress \
      --progress-log research/certificates/r056/progress.ndjson \
      --check \
      --pretty \
      --output research/certificates/r056/leray-polarization-channels.json

The run passed 21 checks. It verified:

- 1,764,912 noncollinear ordered integer triads in the radius-five cube;
- 4,096 direct exact projections for each ordered channel;
- 4,096 direct exact projections for the symmetrized channel formula;
- 400,000 instances across the two all-index high--high-to-low families;
- 24,984 exact normal-channel saturations in the finite cube;
- 120 ordered triads with \(|k|/|p|\le1/8\), whose largest observed planar
  squared gain was exactly \(25/99\), below the formal upper bound
  \((9/16)^2=81/256\).

The exact finite-regression digests stored inside the certificate are:

    exhaustive cube  42e2b7ec860148f4b1a0139eec11d1b55932d39f2ee231cd21b596eac7ad6034
    two families      0fce3686152bc148336ff3ae8e91acae5ee6e0e6c06da0c0ca7553901163719e

## Monitoring

The scientific audit reported 14.488241 seconds of wall time. The independent
process-tree monitor recorded 55 samples over 14.582162 seconds, with peak CPU
usage 100.0%, peak resident memory 23.625 MiB, and no GPU process. The run used
Python 3.12.13 with exact integers and `fractions.Fraction`. It used no
randomness and no floating-point sign decision.

## Files

- `leray-polarization-channels.json`: machine-readable theorem
  classification, exact regressions, digests, checks, and provenance;
- `progress.ndjson`: append-only stage log;
- `resources.csv`: process-tree resource samples;
- `SHA256SUMS`: hashes of the archived files.

## Literature boundary

The polarization frames and helical triad decomposition are prior work:

- F. Waleffe, *The nature of triad interactions in homogeneous turbulence*,
  Physics of Fluids A 4 (1992), 350--363,
  <https://doi.org/10.1063/1.858309>.
- C. Cambon, *L'héritage de Craya, pour une approche statistique à points
  multiples de la turbulence homogène anisotrope*, C. R. Mécanique 345
  (2017), 627--641, <https://doi.org/10.1016/j.crme.2017.05.004>.

R0.56 records the narrower critical-norm channel theorem stated above and
does not present the underlying polarization decomposition as new.
