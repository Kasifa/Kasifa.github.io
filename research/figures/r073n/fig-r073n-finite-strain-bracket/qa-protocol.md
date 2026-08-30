# Visual QA protocol

Before sealing, inspect all three surfaces:

1. `qa-final-size.png` for labels, legend separation, whitespace, and clipping;
2. `qa-grayscale.png` for line-style and fill distinguishability without hue;
3. `qa-pdf.png` for vector-PDF rasterization parity.

Confirm that panel B marks both \(T_*=1/1800\) and \(5/16\), panel C says
that its curves are formula factors at different marked basepoints, no label
collides with another, and the footer retains the finite/illustrative evidence
boundary.  Only after this manual inspection may `validate.py` be run with
`--confirm-visual-qa`.
