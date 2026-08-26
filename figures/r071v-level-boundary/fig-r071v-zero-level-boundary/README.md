# Figure R0.71V-1: fixed-target zero-level boundary layer

This directory is the reproducible journal-figure package for the R0.71V
fixed-target high-frequency family. It evaluates the exact first derivative
of the (N=2) implicit recurrence curve at

\[
q=8,16,32,64,128,256,
\]

without integrating the nonlinear trajectory.

## What the figure tests

The target, multiplier, annular shell scale, and macroscopic audit window are
fixed. Only the auxiliary shear frequencies grow. The plotted atom is the
atom at the **second prescribed root**, not the sum of both roots. This is the
quantity needed for the repeated-root no-go statement: the first root may be
paid separately, yet the second-root comparison with the same target-shell
first-time-jet row still diverges.

The constants are fully restored:

\[
K_y=K_z=\kappa_*=m_*=1,\qquad \rho^2=2.
\]

Relative to the reduced scalar ledger used for cross-checking,

\[
J=2j_{\rm red},\quad
\mathcal B_1^{(*)}=8b_{1,\rm red},\quad
\mathcal B_2^{(*)}=8b_{2,\rm red},\quad
H_E^2=8h_{E,\rm red}^2,
\]

while (D_E) is unchanged. The producer and independent validator both check
these prefactors explicitly.

## Reading the four panels

- **A:** (q^2\gamma_q(r/q^2)) approaches the two-root limiting profile.
- **B:** the second-root atom, the theorem-weighted singleton target-shell
  first and second rows, and the terminal excursion charge have orders
  (q^{-4},q^{-6},q^{-2},q^{-8}).
- **C:** the second-root atom divided by the first row grows like (q^2);
  division by the second row decays like (q^{-2}); division by terminal
  (H_E^2) grows like (q^4).
- **D:** the internal and terminal non-collapse factors decay like (q^{-2})
  and (q^{-4}).

The tail-four fitted powers are descriptive finite-(q) checks of analytic
orders, not regression proofs.

## Reproduce

From the repository root, use the commands in `command.txt`. The calculation
uses the local research virtual environment and is deterministic; no random
seed, GPU, DGX, PDE time stepper, or DNS is involved. `progress.ndjson` and
`resource-log.ndjson` provide process-stage and resource monitoring.

The package writes:

- `data.csv` and `data.json`: lossless panel data;
- `results.json`: complete cases, roots, atoms, jet rows, excursions, and
  asymptotic fits;
- `figure-data-metadata.json`: schema, hashes, evidence map, and claim boundary;
- `validation.json`: standalone 80-digit interpolation and independent
  quadrature/artifact validation;
- `figure.pdf`, `figure.svg`, and 600-dpi `figure.png`;
- final-size color, grayscale, and Poppler-rendered QA previews;
- a release `manifest.json` and `SHA256SUMS` ledger.

## Claim boundary

This figure is finite corroboration of the analytic R0.71V construction. It
does not prove the implicit-function theorem, a uniform nonlinear remainder,
the sharp coefficient of the second-time row, a continuation criterion, or
Navier--Stokes global regularity. It is a fixed-target multiscale family, not
a covariant Navier--Stokes dilation.

A source-tree build is **provisional** until its immutable Git source and
certificate hashes are known. Release certification rebuilds the manifest as
**formal**, records those hashes, and verifies the complete checksum ledger;
the computational claims and numerical payload do not change in that step.
