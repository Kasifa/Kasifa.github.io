# R0.72V visual QA protocol

The source stage performs structural checks only and records no visual
approval. For a later formal build, inspect all of the following before
passing --visual-inspected:

1. View the PDF at final 178 mm width. Confirm every label, fraction, marker,
   box, arrow, and panel letter is legible and unclipped.
2. Compare PDF, SVG, and 600 dpi PNG masters. Confirm identical panel order,
   analytic curves, labels, dimensions, and status statements.
3. Inspect qa-grayscale.png. The three \(c\)-curves and integer-cell markers
   must remain distinguishable through stroke styles, direct labels, and
   markers; no semantic distinction may rely only on hue.
4. Confirm Panel A displays the exact probe ledger, \(1/44\), \(3/2288\),
   \(5/6292\), and the positive floor \(5/6292\).
5. Confirm Panel B displays \(b=a^2/3+6c\), \(a=3k\), all three stated
   \(c\)-values, and integer-\(k\) markers.
6. Confirm Panel C states the full-\(H^1\)-norm direct-sum inequality and the
   graph-to-energy implication. If the ratio curve is shown, it must say
   formula only and must not display an inferred or fitted \(C_T\).
7. Confirm the exact visible statements
   whole-line block contraction: CLOSED (exact cubic energy model)
   and periodic / Clay: OPEN.
8. Confirm pdeSimulation=false: every curve is analytic presentation only.
9. Confirm the only chromatic roots are blue #285f8f and gold #a6781f;
   neutral ink, muted gray, grid gray, paper, and pale gold are allowed.
10. Confirm the five-petal blossom remains in the top-right header, overlaps
    no title or data, and carries no information.
11. Confirm formal public PDF/SVG/PNG copies are byte-identical to their
    package masters and that the strict validator passes.
