# R0.72U visual QA protocol

The source stage performs structural tests only and records no visual approval.
For a later formal build, inspect all of the following before passing
`--visual-inspected`:

1. View the PDF at final 178 mm width and confirm every label, fraction, line,
   marker, and panel letter is legible and unclipped.
2. Compare the PDF render, SVG, and 600 dpi PNG; confirm their curves, labels,
   dimensions, and panel order agree.
3. Inspect `qa-grayscale.png`; all three centre curves and the two probe curves
   must remain distinguishable without colour through stroke style, direct
   labels, or markers. Confirm that no semantic distinction relies on hue.
4. Confirm Panel A displays `mu2=1/11` and `mu4=3/143` and that the probe
   vanishes at both endpoints.
5. Confirm Panel B displays `K_c=3/143+6(c+s)/11`, the threshold `27/13`, and
   the negative threshold edge `-81/143` at \(s=1\).
6. Confirm Panel C labels `4/5` as a fixed-gauge inviscid floor, not as a
   viscous contraction or as the Panel B moment floor.
7. Confirm the phrase `whole-line block contraction: OPEN` is visible.
8. Confirm no formal public copy is accepted unless its bytes equal the package
   master and the strict validator passes.
9. Confirm the only chromatic roots are blue `#285f8f` and gold `#a6781f`
   (neutral ink/muted/grid/paper and the pale gold surface are allowed), with
   blue used for primary curves and gold for comparators, floor, and OPEN.
10. Confirm the subtle five-petal research blossom remains locked to the
    top-right header, is unclipped, overlaps no title or panel, and encodes no
    data.
