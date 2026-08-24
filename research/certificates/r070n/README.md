# R0.70N exact certificate

This directory locks the exact symbolic payload for the scalar multi-scale
vorticity-frame gate.

The producer verifies four groups:

1. the aggregate covariance ledger, common-source mismatch, moving weights,
   positive time windows, and common pullback;
2. the exact periodic shear NSE solution and its rank-one three-scale
   covariance;
3. the exact single-axis Beltrami rank-two obstruction and a two-axis
   positive control with the correct pressure;
4. failure of scale normalization and positive time aggregation, plus a
   full-rank whole-space Schwartz family whose optimal frame constant tends
   to zero.

Run the command in command.txt from the repository root.  The result must be
byte-identical to result.json before SHA verification.

The finite producer verifies exact exemplars.  The arbitrary scalar-filter
common-subspace theorem is proved in the canonical report.  Neither the
producer nor the report rules out conditional frame estimates, proves that
low rank is regularizing, establishes global smoothness or blow-up, or solves
the Millennium problem.
