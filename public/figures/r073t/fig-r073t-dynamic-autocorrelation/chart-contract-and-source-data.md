# R0.73T chart contract and source data

## Analytical question

Which part of the scalar energy-density autocorrelation survives as a useful
Navier--Stokes estimate, and which information losses prevent an autonomous
evolution?

## One-sentence takeaway

The R0.73S quantity \(AQ\) gives a rigorous one-sided quartic budget, but
identical complete scalar autocorrelation can hide either arbitrarily different
carrier dissipation or opposite signed pressure work at the initial time.

## Visual and delivery contract

- **Surface:** standalone static journal figure embedded in the R0.73T HTML
  note and synchronized PDF.
- **Panel A:** analytic flow diagram, not a numerical chart.
- **Panel B:** ordered line with eight exact carrier-frequency observations at
  \(t=0\); \(|\dot C_0(0)|/(2\nu)=N^2\).
- **Panel C:** signed ordered lines with sixteen exact observations at
  \(t=0\); the common initial viscous part is subtracted and the remaining values are
  \(\mp384L\).
- **Renderer:** reproducible local Matplotlib; SVG, PDF, and 600 dpi PNG.
- **Palette:** hard two-root cap (blue and gold) plus neutrals.  Marker fill,
  line style, direct labels, and sign relative to a visible zero line preserve
  the distinction in grayscale.
- **Footprint:** 178 mm by 100 mm, one journal-width page figure.
- **Final QA:** source-row reconstruction, SVG/PDF/PNG integrity, 600 dpi
  dimensions, PDF raster comparison, grayscale inspection, and visual
  inspection in the note page.

## Source and sufficiency

Panel A is bound to the continuum derivation in
`research/r073t_dynamic_autocorrelation_budget.md`.  Panels B and C are bound
to `research/certificates/r073t/results.json`, itself rebuilt with Python
`fractions.Fraction`.  The figure validator requires the analytic proof, all
ten figure-source files, and the exact certificate to share one immutable
source commit; it also reruns the certificate's fail-closed seal.  There are
eight ordered points in Panel B and eight points for each of two signed series
in Panel C, enough to display the exact quadratic and linear laws.
No interpolation, regression, random sample, PDE integration, floating-point
simulation, GPU, or DGX result supports the claims.

## Interpretation boundary

Panel C plots the signed pressure-pairing contribution after subtracting the
common initial viscous term.  It is not the full \(Q'\).  The quadratic
viscous term dominates asymptotically for each fixed \(\nu>0\); no uniform
claim over arbitrarily small symbolic viscosity is made.  Both witness
families are smooth exact fields and are not singularity evidence.
