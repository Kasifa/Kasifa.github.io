# R0.73K figure QA report

**Status:** passed.

Automated extraction and export checks passed. I inspected `figure.png`,
`qa-final-size.png`, `qa-grayscale.png`, and `qa-pdf.png` at original
resolution on 2026-08-31. The whitespace-only regeneration preserved all four
visual surfaces byte for byte.

Automated facts:

- source rows: 213 = 204 display-core rows + 5 cutoff summaries + 4
  cross-cutoff summaries;
- primary rows: 1,190; cross-cutoff rows: 952;
- displayed grid: `N=160`, 17 d nodes, and 12 core viscosity levels;
- largest-two-cutoff eigenvalue difference: 7.585809664112349e-15;
- largest-two-cutoff embedded projector difference: 5.6611745823103356e-14;
- largest-cutoff right/left embedded residuals:
  1.1732806350686037e-14 / 7.749893012666417e-15;
- independent maximum ordinary / difference-quotient absolute errors:
  5.218048215738236e-14 / 3.6637359812630166e-07, both within the frozen
  tolerances;
- PDF page: 504.566929 by 334.488189 points;
- 600 dpi PNG: 4,204 by 2,787 pixels;
- final-size QA: 1,261 by 836 pixels at 180 dpi;
- PDF/SVG raster-image count: zero;
- byte-identical visual hashes after whitespace normalization: figure PNG
  `064971bfd72c27dd5e7c98b03492d51c94a2541874fc17838acb992f2be4cb5d`,
  final-size QA `68adec3d1bcacd56ad7ecf8a33cb4e192e32ba878e83b0728b3854aa84666371`,
  grayscale QA `905bf6e2f85eea95086cb58260dab559655498f7cc29029ff154597852e920c6`,
  and PDF raster QA
  `11a9481897817e675a3ea832b0bab689b3622434a5fde3640508d68518d441c8`.

Manual inspection checklist:

- original 600 dpi PNG: passed; all four panels, both Panel C subpanels, the
  uncertainty bands, and the cutoff markers are sharp and fully inside the
  page;
- final-size raster: passed; titles, focused-scale note, axes, ticks,
  legends, annotations, source line, and scope sentence remain readable at
  178 by 118 mm;
- grayscale distinctions: passed; solid, dashed, dash-dot, and dotted lines
  remain distinct, and filled/open circles, squares, triangles, and diamonds
  remain identifiable;
- independently rasterized PDF: passed; it agrees visually with the direct
  raster and has no missing glyphs, black boxes, detached labels, or displaced
  marks;
- labels, uncertainty bands, blossom anchor, and claim boundary: passed; the
  blossom is locked to the top-right header, the focused scale is declared,
  and the boundary text identifies a finite-dimensional diagnostic rather
  than a continuum result.

Corrections made during QA:

- raised the lower panel row so both x-axis labels clear the provenance line
  at final publication size;
- normalized SVG trailing whitespace and CSV line endings without changing
  any visual surface.
