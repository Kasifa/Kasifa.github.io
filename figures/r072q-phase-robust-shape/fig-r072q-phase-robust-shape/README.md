# R0.72Q formal figure source scaffold

This directory contains exactly the thirteen source files for the proposed
three-panel journal figure accompanying the R0.72Q fixed-mode,
phase-robust Morse contract. Formal data, results, masters, QA surfaces,
manifests, and hash ledgers are intentionally absent until the analytic source
and both audit routes are frozen.

The figure separates three statements:

- Panel A draws the exact 1:2 caustic
  `z(phi) = exp(-3 i phi)/8 - 3 exp(-i phi)/8`. The caustic-free disk
  `|z| < 1/4` contains every relative phase. The smaller disk `|z| <= 1/8`
  is the 1:2 slice of the general `Q2 <= 1/2` contract.
- Panel B records the unique radial wall `r_*(theta)` on every relative-phase
  ray. It is sampled only through the exact caustic parametrization and stays
  in `[1/4, 1/2]`; no fitted or interpolated wall is used.
- Panel C records the fixed-`M` analytic margins used by the proof: critical
  localization `pi/12`, curvature zone `pi/6`, and
  `mu = (sqrt(3)-1)/2`. The normalized profile `F` has away gap `>1/12`;
  for the formal Coble shear `W=e^{-y}F` on `0<=y<=1`, the declared contract
  is `(r,C0,C1)=(pi/12,81,36)`.

Every dense curve is a direct binary64 evaluation of an exact formula. The
figure runs no PDE simulation, continuation, regression, root fit, or
certificate interpolation. These samples illustrate formulas and cannot
replace the continuous inequalities in the analytic report. The result keeps
`M` fixed; it does not provide constants uniform as `M` grows and does not
cover arbitrary fast time-dependent phases.

The thirteen source files retain the prior fail-closed lineage contract. Formal plotting
requires the frozen analytic source, producer configuration and result,
independent configuration and result, and a passed formal crosscheck. Those
five runtime JSON files must come from the canonical flat directory
`research/certificates/r072q/` and must be covered exactly by its independently
verified `SHA256SUMS` ledger. Temporary or unsealed crosschecks are rejected.

The analytic report and audit programs are bound to the source commit. The
runtime certificate files and their ledger are bound to the certificate
commit. The formal figure build commit must equal the certificate commit.
Plotting and manifest sealing both reject tracked or staged drift, bind all
thirteen package sources to Git blobs, and allow only the declared untracked
generated outputs.

The intended masters are an editable-text SVG, a one-page PDF, and a 600 dpi
PNG at 177.8 x 82.55 mm. The formal workflow also creates final-size,
grayscale, and PDF-raster QA surfaces. Automatic checks run first. All three QA
surfaces then require explicit visual inspection before the visual gate may be
set. Source syntax checks are not visual QA.

No `data.csv`, `results.json`, figure master, QA image, manifest,
`SHA256SUMS`, or public asset belongs in this source-only scaffold. See
`command.txt` for the deferred formal workflow.
