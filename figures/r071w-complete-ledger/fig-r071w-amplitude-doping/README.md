# Figure R0.71W-1: amplitude-doped complete-ledger test

This directory is the reproducible journal-figure package for the R0.71W
amplitude-doped route. It combines three already generated, independently
identified certificate files:

- `research/certificates/r071w/result.json`;
- `research/certificates/r071w/independent-result.json`;
- `research/certificates/r071w/truncated-coset-result.json`.

The package does not alter those source certificates.

## Reading the panels

- **A:** the certified leading atom/complete-ledger proxy and its asymptotic
  \(q^{+1}\) guide.
- **B:** nonlinear retained-coset atom proxy and full retained
  \(\dot H^{-1}\) rotational charge, with predicted powers \(+1\) and \(-1\).
- **C:** normalized second-root slope and the \(q=1024\) truncation comparison
  against \(R=40\).

The analytic and nonlinear-truncation evidence classes remain separate in
`data.csv`, `data.json`, `results.json`, the caption, and the plot labels.

## Reproduce

Run the commands in `command.txt` from the repository root. The pipeline
produces source-derived data, vector and raster figures, final-size QA images,
an independent validation report, a formal manifest, and SHA-256 ledger.

The formal source/certificate provenance is
`a9e2009565ca06672383da38fa9359874190481a`. The clean-run flag refers to the
tracked research inputs at that commit; the generated figure files are
downstream outputs and are not misclassified as source dirtiness.

## Claim boundary

The nonlinear calculation is a finite retained Fourier-coset integration with
DOP853 and a nonlinear least-squares root solve. It is computation
corroboration only, not DNS. It does not prove continuum IFT uniformity,
spectral-truncation convergence, singularity formation, or global regularity.
The initial-data size is unbounded along the amplitude-doped sequence.
