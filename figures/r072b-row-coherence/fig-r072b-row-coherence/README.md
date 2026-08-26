# R0.72B-1 formal figure

This package contains the 178 mm three-panel figure for the target-row
coherence refinement.

- Panel A compares three sufficient power-law phase boundaries.
- Panel B records the exact-launch equal-carrier factors
  \(\chi_M\), \(\Omega^2/K_v\), and their combined gain relative to the
  previous dimension-free constants.
- Panel C records three one-carrier Bessel short-layer indicators. They explain
  why a frozen-profile enhanced-dissipation comparison does not remove slope
  mass accumulated before a positive burn-in.

`build_figure.py` reads both R0.72B machine certificates, writes `data.csv`,
and exports vector PDF/SVG plus a 600 dpi PNG. `qa_images.py` creates the
final-size color, grayscale, and PDF-render surfaces. `validate.py` checks the
data identities, independent agreement, dimensions, DPI, and PDF structure.

The analytic report is the source of the proof. The figure is not an interval
certificate, DNS, normalized lower construction, or NSE regularity claim.
