# Final visual QA

**Date:** 2026-08-30  
**Status:** passed

The archival PDF was rasterized with Poppler at 180 dpi and compared with the
direct 600 dpi PNG. A reduced final-size preview and a grayscale conversion
were inspected at original resolution.

Checks passed:

- the PDF is one 178 by 132 mm page and the PNG is 4204 by 3118 pixels at
  600 dpi;
- the figure title and all four panel titles are separate and fully visible;
- axes, units, legends, markers, status fields, and the precedent sentence are
  inside the page without overlap;
- Panel B labels the curves as finite compression only and Panel C labels them
  as diagnostics rather than a continuum proof;
- curve markers and line styles remain distinguishable in grayscale;
- the closed fixed-cluster claims and the open simplicity, complement,
  fast-time, nonlinear, and Clay gates remain visually separate;
- no missing glyphs, black squares, clipped equations, or raster artifacts
  were observed.

The visual pass initially found a collision between the figure title and the
A/B panel titles. The plotting source now reserves a dedicated title band, and
the PDF and grayscale views were rerendered and reinspected after that repair.

