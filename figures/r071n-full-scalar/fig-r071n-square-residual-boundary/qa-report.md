# Visual QA report

Status: passed

The regenerated 178 mm by 118 mm figure was inspected at final size in
color, in true grayscale, and after rendering the vector PDF at 180 dpi.
All four panel titles, axes, direct labels, formulas, zero lines, legends,
arrows, and the scope footer are legible and remain inside the figure. No
text collision, detached label, or clipped mark remains after the final
layout revision.

Panel B uses one honest linear signed scale with an explicit zero line. Its
square and residual values, component-sum diamonds, and signed labels agree
with `data.csv`. Panel C separates the scales of `z` and `J`, so the small
positive normalized pairings are not visually compared as if they shared
units with the signed scalar source. Panel D displays the exact exponents
5, 2, 3, and 0 and keeps the R0.71O face gate as a route annotation rather
than a proved estimate.

The blue solid and orange open-hatched encodings remain distinct in
grayscale. Filled circles, an open square, and an open diamond preserve the
scaling distinctions without color. The visible wording labels the witness
signs as deterministic diagnostics rather than interval theorems and states
that the figure contains no no-go, continuation, regularity, or singularity
claim. The final exports were cross-checked against `validation.json` and
`independent-validation.json` after the last rerender.
