# R0.73J continuum spectral-branch certificate figure

This package renders a 178 mm three-panel journal figure directly from the
formal R0.73J contour and kinetic-overlap certificates.

- Panel A records the exact contour geometry, the analytic Howard disk, the
  essential-spectrum axis, and the certified local root interval.
- Panel B plots one strict lower bound for every global and local contour
  panel.  The values are interval-certificate margins, not sampled moduli.
- Panel C shows the 128 certified lower bounds for the normalized kinetic
  left-right overlap on the complete ((d,\lambda)) rectangle.

The analytical question is whether one compact visual can show both the
spectral counting geometry and the quantitative margins that keep the
certificate separated from zero and from the overlap threshold (1/2).
The supported takeaway is limited: all certified contour panels avoid zero,
both exact base windings equal one, and every overlap cell exceeds (1/2).

The static renderer uses a hard two-root palette cap (blue and orange) plus
neutrals.  Line style, marker shape, open fill, and panel position preserve
the distinctions in grayscale.  `source-data.csv` contains every plotted
certificate row with its upstream path and SHA-256 digest.

Run `command.txt` from the repository root.  The archival outputs are vector
PDF, vector SVG, and a 600 dpi PNG.  The QA surfaces are a final-size raster,
a grayscale raster, and an independently rasterized PDF.

This figure certifies one planar periodic linearized spectral branch.  It
does not prove a viscous branch, an adiabatic theorem, transverse
three-dimensional closure, finite-time singularity, or the Clay problem.
