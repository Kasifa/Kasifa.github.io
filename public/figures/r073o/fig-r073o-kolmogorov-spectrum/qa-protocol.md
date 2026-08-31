# R0.73O figure visual QA protocol

Inspect all three surfaces before confirming:

1. `qa-final-size.png`: labels, legends, annotations, whitespace, and clipping;
2. `qa-grayscale.png`: distinguish the solid finite curve, dotted target,
   dashed zero line, and critical marker without hue;
3. `qa-pdf.png`: verify parity with the PNG master after independent PDF
   rasterization.

Panel A must display the critical interval as below plot resolution and keep
the target and finite crossing labels separated.  Panel B must show the finite
\(M=120\) value, physical growth conversion, and residual.  The two-line
footer must retain the finite/illustrative evidence boundary.  Only then run
`validate.py --confirm-visual-qa`.
