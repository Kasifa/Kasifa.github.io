# R0.29 canonical transport certificate

This directory archives the exact finite regression accompanying the R0.29
all-order formal theorem.  The theorem itself is proved in
`research/edge_canonical_transport_note.md`; it does not depend on truncating
the series.

The GMP audit reconstructs the rational formal series \(a,u,v,e^{-a}\) through
total degree 119 and checks, coefficient by coefficient,

\[
 \{u,v\}=uv,
 \qquad
 4Wu=Zv e^{-a}.
\]

It also checks that every nonzero coefficient of the active series has charge
at least \(-1\).  In total, the run performed 14,514 coefficient checks and
16,176,149 exact convolution interactions, with no failure.

The finite regression checks the implementation.  It does not prove endpoint
coefficient signs, locate a dominant singularity, or imply a Navier--Stokes
regularity result.

## Source state

- repository: Kasifa/Kasifa.github.io
- source commit: e4486837dd232228cafab39651eb41955621faab
- source working tree at audit start: clean
- arithmetic: gmpy2 2.3.1 over GMP 6.3.0 exact rationals
- maximum checked total degree: 119

## Reproduction

Install the pinned research environment, then run from the repository root
with fresh temporary output paths:

    python research/run_with_monitor.py \
      --output /tmp/r029-resources.csv \
      --interval 5 -- \
      python research/edge_canonical_transport_audit.py \
        --max-total-degree 119 \
        --progress \
        --progress-log /tmp/r029-progress.ndjson \
        --check \
        --pretty \
        --output /tmp/r029-edge-canonical-transport.json

The archived run took 81.32 seconds on an Apple M5 Max.  Its maximum observed
CPU use was 100% of one core and its maximum resident memory was 33.422 MiB.
The SHA-256 digest of the certificate is listed in `SHA256SUMS`.
