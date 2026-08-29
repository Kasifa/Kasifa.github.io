# QA report

Status: passed after explicit visual inspection on 2026-08-30.

- The 1100 by 816 final-size preview preserves all four panel titles, labels,
  legends, tick labels, boundary notes, and annotations without clipping.
- Logarithmic axes are identified by their tick spacing and mathematical axis
  labels. The reversed viscosity axis is stated explicitly.
- The grayscale preview preserves all comparisons through markers and line
  styles: circle/square/triangle in panel B, solid/dashed in panels C and D,
  and star/circle/cross in panel A.
- The red finite/sampled boundary notes remain legible in color and become
  neutral gray without losing meaning.
- The 180 dpi PDF raster has the same panel geometry and text placement as the
  PNG preview. The SVG contains vector text and no embedded raster image.
- Panel A reports only the six rightmost complementary finite values. Panel B
  reports stored line maxima rather than an unsampled resolvent curve. Panel C
  says that only the stored time grid is shown. Panel D labels fixed-projection
  leakage as a finite lesson. No continuum conclusion is encoded visually.
