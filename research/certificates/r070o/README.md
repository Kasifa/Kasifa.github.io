# R0.70O exact certificate

This directory locks the exact symbolic payload for the spectral rank-strata
and filtered-to-unfiltered bridge gate.

The producer verifies five groups:

1. simple-spectrum eigenvalue, eigenvector, projector, trace, and normalized
   residual evolution;
2. exact finite-frame best-plane and best-line sum-of-squares certificates;
3. an explicit Bessel-filtered smooth global Navier--Stokes shear whose
   observed best-line residual tends to zero while its unfiltered critical
   transverse norm stays fixed, plus compact-band dyadic finite
   approximants;
4. coercive, near-plane, and near-line partition samples and exact gap
   certificates;
5. fixed-projection Fourier lower-frame and blind-frequency reconstruction
   checks.

Run the command in `command.txt` from the repository root.  The regenerated
result must be byte-identical to `result.json` before SHA verification.

The producer checks finite symbolic and rational identities.  The
arbitrary-measure Rayleigh--Ritz theorem, the infinite compact-band
Leray--Hopf endpoint example, and the arbitrary-filter lower-frame theorems
are proved analytically in the canonical report.  Neither the producer nor
the report proves a new regularity criterion, finite-time blow-up, global
smoothness, or the Millennium problem.
