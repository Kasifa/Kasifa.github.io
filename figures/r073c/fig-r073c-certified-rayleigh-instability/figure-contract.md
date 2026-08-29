# Figure contract

The formal figure must fit a 178 mm double-column width, retain vector text in
PDF/SVG, and provide a 600 dpi PNG.  Endpoint sign markers in Panel B must be
read from the interval JSON, not typed constants.  Panel C must retain the
labels `finite diagnostic` and `certified sigma bracket`.  Panel D must show
C5 as OPEN and C6 as CONDITIONAL in the same visual field as the closed C4
claim.

The figure fails closed if either endpoint sign changes, the interval source
hash differs between the two primary runs, the finite validation is not
passed, or any claim-boundary boolean is promoted beyond the evidence.

