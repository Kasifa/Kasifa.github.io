# fig-r071k-matched-cell-gap

Formal double-column figure package for R0.71K.  It records four boundaries:

1. one fixed translated matched partition has bounded overlap and exact sum
   one;
2. the R0.71J global amplitude starts at zero and becomes positive on the
   fixed parabolic window, while the aligned cell sum preserves a positive
   endpoint;
3. the normalized positive-creation and local heat/payment bounds scale as
   \(K^{-2}\) and \(K^{-4}\);
4. cutoff--curl and viscous-collar rows are leading order, not discarded
   errors.

Run the commands in `command.txt` from this directory.  The output formats
are vector PDF, SVG, and a 600 dpi PNG at 178 mm width.  The producer uses
only closed formulas and the explicit smooth partition; there is no DNS,
PDE time stepping, fitted exponent, random seed, GPU, or DGX workload.

`validation.json` checks the producer path.  `independent-validation.json`
uses a separate standard-library/Decimal path and checks the archived output
headers.  The stronger independent Fourier and one-cell quadrature audit is
stored at `../../../research/r071k_independent_audit.py`.

Claim boundary: the theorem uses one fixed aligned scale-covariant partition
and the R0.71E parent-only broad frame.  It rejects the same local
heat/support endpoint as a uniform payment.  It does not reject an explicit
collar-, face-, shape-, or refresh-paid estimate; arbitrary or moving
partitions; an infinite frame--cell identity; a continuation theorem;
regularity; singularity; originality; or the Millennium problem.

