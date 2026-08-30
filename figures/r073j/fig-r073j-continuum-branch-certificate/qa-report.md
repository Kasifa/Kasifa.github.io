# R0.73J figure QA report

**Status:** passed.

Automated certificate and export checks passed. I inspected `figure.png`,
`qa-final-size.png`, `qa-grayscale.png`, and `qa-pdf.png` at original
resolution on 2026-08-30.

Automated facts:

- source rows: 192 = 64 contour panels + 128 overlap cells;
- global minimum: 5.4994844658066855244780824076486877967115879986065100252929739009243097123937373 (G-left-09);
- local minimum: 0.16435517830515349406408224947203145697808610836036070848305708489081214602540829 (L-circle-00);
- overlap minimum: 0.58534376672194088497214965120823073782702694037082714926984657951506897826463322 at d-index 7, lambda-index 15;
- PDF page: 504.566929 by 294.803150 points;
- 600 dpi PNG: 4204 by 2456 pixels;
- final-size QA: 1261 by 737 pixels at 180 dpi;
- PDF/SVG raster-image count: zero.

Manual inspection checklist:

- original 600 dpi PNG: passed; all three panels, the local inset, and the
  minimum-cell marker are sharp and fully inside the page;
- final-size raster: passed; titles, axes, ticks, legends, annotations, and
  the scope sentence remain readable at 178 by 104 mm;
- grayscale distinctions: passed; global solid circles remain distinct from
  local dashed open squares, and the outlined minimum cell remains visible;
- independently rasterized PDF: passed; it agrees visually with the direct
  raster and has no missing glyphs, black boxes, or displaced marks;
- labels, inset, annotation attachment, blossom anchor, and claim boundary:
  passed; the blossom is locked to the top-right header and the boundary text
  makes no viscous, three-dimensional, singularity, or Clay claim.

Corrections made during QA:

- replaced the standard rasterized colorbar gradient with 48 vector strips;
- moved the panel labels into the titles, separated the Panel C subtitle, and
  moved the color scale inward so no visible element touches the page edge;
- removed the adjacent 56/57 tick-label collision and simplified the local
  inset ticks without changing any certificate value.
