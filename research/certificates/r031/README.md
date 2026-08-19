# R0.31 optimized-majorant certificate

This directory archives the exact finite regressions accompanying the R0.31
improved analytic-domain theorem.  The proof is recorded in
`research/edge_optimized_majorant_note.md`.

The all-order kernel proof has two explicit parts:

- exact GMP rational evaluation gives (H_L\le27/4) for
  (3\le L\le296), with equality only at (L=3);
- for (L\ge297), the decreasing rational bound
  (10000/2187+640/L+1600/L^2) is already below (27/4).

Together with the direct degree-two value (A_2=3), this closes the layer
majorants with (K=81/4):

\[
 A_L\le \frac{2(81/4)^{L-1}}{L^3},
 \qquad
 \|U_L\|_1,\|V_L\|_1\le \frac{(81/4)^{L-1}}{L^3}.
\]

The common guaranteed analytic domain for (a,U,V), the canonical
logarithms, and the R0.29 exponential factorization is therefore
(max(|Z|,|W|)<4/81).

The degree-119 recurrence is an independent implementation regression.  It is
not the proof of the all-order estimate, does not locate the nearest singular
variety, and does not imply a Navier--Stokes regularity or singularity result.

## Source state

- repository: Kasifa/Kasifa.github.io
- source commit: dfdf19ae3706d376deae02b9ff804060bf37d626
- source working tree at audit start: clean
- arithmetic: gmpy2 2.3.1 over GMP 6.3.0 exact rationals
- finite kernel range: total degrees 2 through 296
- maximum checked recurrence degree: 119

## Reproduction

Install the pinned research environment, then run from the repository root
with fresh output paths:

    python research/run_with_monitor.py \
      --output /tmp/r031-resources.csv \
      --interval 2 -- \
      python research/edge_optimized_majorant_audit.py \
        --max-total-degree 119 \
        --progress \
        --progress-log /tmp/r031-progress.ndjson \
        --check \
        --pretty \
        --output /tmp/r031-edge-optimized-majorant.json

The archived run took 29.09 seconds on an Apple M5 Max.  Its maximum observed
CPU use was 100% of one core and its maximum resident memory was 32.188 MiB.
It evaluated 5,484,501 ordered recurrence interactions.  The append-only
progress log and two-second resource log are archived here and in the formal
figure package.  SHA-256 digests are listed in `SHA256SUMS`.
