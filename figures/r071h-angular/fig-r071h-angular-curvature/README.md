# fig-r071h-angular-curvature

This formal double-column figure records four exact boundaries from R0.71H:

1. a two-mode pure heat flow has an exact projective-curvature payment
   identity;
2. a fixed-energy global-smooth 2D3C Navier-Stokes family has initial
   pointwise angular speed proportional to \(K\), while the corresponding
   initial source density approaches a finite limit;
3. one nonconstant finite-Fourier cutoff has finite Rayleigh and projective
   source quotients for \(0\leq\delta\leq1\);
4. the direct Young estimate for the weighted-BV target asks for a frequency
   weight \(1\), while the available heat-bulk weight is \(K^{-2}\).

## Reproduction

Run the commands in command.txt from this directory. generate_data.py
evaluates only closed-form formulas. It does not integrate an ODE or step a
PDE. validate_data.py checks the producer formulas and exact balances.
independent_validate.py recomputes every row through a separate 60-digit
Decimal path and verifies the PDF, SVG, PNG, print size, and rasterization.

The formal outputs are figure.pdf, figure.svg, and the 600 dpi figure.png.
qa-original.png, qa-grayscale.png, and qa-report.md record the print-size
and non-color checks. manifest.json and SHA256SUMS bind the complete package.

## Compute boundary

The package uses one local CPU process. It needs no random seed, GPU, DGX,
DNS, fitting, or time-evolved three-dimensional simulation. Panel B is exact
initial-time Fourier algebra for a true global-smooth 2D3C Navier-Stokes
family; it is not a numerical trajectory.

## Claim boundary

The figure proves an exact finite-dimensional heat identity and one
pointwise energy-only no-go at \(t=0\). It does not disprove an integrated
angular-turning budget or a weighted-BV estimate. The cutoff panel shows
finite saturation in one fixed template, not a universal cutoff bound. The
scaling panel records what the direct Young inequality requires; it does not
prove that every deeper PDE cancellation is impossible. Nothing here proves
regularity, constructs a singularity, establishes originality, or resolves
the Millennium problem.
