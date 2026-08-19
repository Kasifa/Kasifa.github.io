# R0.30 analytic-majorant certificate

This directory archives the exact finite regression accompanying the R0.30
all-order analytic-majorant theorem.  The proof is recorded in
`research/edge_analytic_majorant_note.md`; it does not depend on truncating the
formal series.

For each total degree through 119, the GMP audit reconstructs the exact
rational fields \(a,U=-12u,V=-3v\), checks the active charge support, verifies
the principal-ideal divisibility of the transport fields, and compares their
coefficient \(\ell^1\) layer norms with

\[
 A_L\le \frac{2\,96^{L-1}}{L^3},
 \qquad
 \|U_L\|_1,\|V_L\|_1\le \frac{96^{L-1}}{L^3}.
\]

The finite regression checks the implementation and records finite growth
diagnostics.  It is not the proof of the all-order bounds, does not locate a
dominant singularity, and does not imply a Navier--Stokes regularity result.

## Source state

- repository: Kasifa/Kasifa.github.io
- source commit: 641db99147d30f51bfc70c8881a70743f6bd063d
- source working tree at audit start: clean
- arithmetic: gmpy2 2.3.1 over GMP 6.3.0 exact rationals
- maximum checked total degree: 119

## Reproduction

Install the pinned research environment, then run from the repository root
with fresh temporary output paths:

    python research/run_with_monitor.py \
      --output /tmp/r030-resources.csv \
      --interval 2 -- \
      python research/edge_analytic_majorant_audit.py \
        --max-total-degree 119 \
        --progress \
        --progress-log /tmp/r030-progress.ndjson \
        --check \
        --pretty \
        --output /tmp/r030-edge-analytic-majorant.json

The archived run took 33.19 seconds on an Apple M5 Max.  Its maximum observed
CPU use was 100% of one core and its maximum resident memory was 32.250 MiB.
It evaluated 5,484,501 ordered recurrence interactions.  The append-only
progress log and the two-second resource log are archived with the certificate
and the formal figure package.  SHA-256 digests are listed in `SHA256SUMS`.
