# fig-r071i-joint-volume-gap

This is a draft formal double-column figure package.  Its current
manifest.json uses schema version 1.0 and status `draft`; it is not a
published or certified figure release.  The package records four exact
R0.71I boundaries:

1. a two-eigenvalue common-heat path has a coefficient pulse with zero outer
   faces;
2. its weighted-BV to weighted-time-volume ratio is exactly proportional to
   \(K^2\);
3. a fixed-energy, global-smooth 2D3C Navier--Stokes family has an exactly
   zero entry coefficient and a positive limiting pulse for one fixed smooth
   radial two-ring multiplier;
4. one complementary two-cell partition has the exact refresh gap
   \(3U^2/28\).

## Reproduction

Run all package commands from this directory.  In the current checkout, the
manifest's repository-local Python entry point is
`../../../tmp/r068b-venv/bin/python`.  The numerical dependency lock is
`../../../research/requirements-r068b.txt`; the observed Python, NumPy,
Matplotlib, and Pillow versions are recorded in manifest.json and
environment.txt.  command.txt records the original workstation invocation as
additional provenance, including a host-local `/tmp` package path; that
absolute temporary path is not the portable entry point.

generate_data.py evaluates only closed-form formulas.  No ODE or PDE time
stepper, DNS, random sample, regression, or fitted exponent is used.
validate_data.py checks the producer formulas.  independent_validate.py
recomputes every CSV row with a separate 70-digit Decimal path and verifies
the archival outputs.

The archival figure outputs are figure.pdf, figure.svg, and the 600 dpi
figure.png.
qa-original.png, qa-grayscale.png, and qa-report.md record visual and
non-color checks.  manifest.json and SHA256SUMS bind the package.

Verify an unchanged package from this directory with
`shasum -a 256 -c SHA256SUMS`.  After changing any package asset, regenerate
manifest.json and SHA256SUMS with build_manifest.py before running that check;
a stale hash failure is expected until the ledger is rebuilt.

## Claim boundary

Panels A--B are a finite-dimensional common-heat model with \(Y=1\), not a
Navier--Stokes solution.  Panel C plots the rigorously derived
\(K\to\infty\), fixed-viscous-window profiles of an exact global-smooth 2D3C
NSE family; it is not a finite-\(K\) numerical trajectory.  Its multiplier is
a fixed smooth radial two-ring template, not the preselected broad dyadic
frame.  Panel D shows why an uncontrolled cutoff-refresh schedule cannot be
free; it does not reject a fixed or independently controlled transported
partition.  The package supplies a volume-only obstruction for the stated
models and multiplier.  It is not a full face-paid BV no-go.  It does not
reject every face-paid weighted-BV theorem, prove a continuation estimate,
construct a singularity, establish originality, or resolve the Millennium
problem.
