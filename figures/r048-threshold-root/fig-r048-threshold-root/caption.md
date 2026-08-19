# Figure R0.48-1

**Exact threshold root and full-window dominance certificate.** (a) The true
active column `C_r(81,162)` is shown across the adjacent millionth window as
its signed margin from one in parts per million.  The 101 plotted points are
exact rational presentation samples of the explicit degree-80 polynomial;
the exact root bracket, not the sampling grid, locates the crossing.  (b) At
the two adjacent decimal endpoints of the width-`10^-18` bracket, the exact
polynomial values have opposite signs.  The 81-polynomial exact Sturm
sequence has 40 and 39 sign variations, respectively, and no zero endpoint
values, so the bracket contains exactly one root.  Coefficient positivity
also gives `P'(r)>0` for every positive `r`, making this the globally unique
positive root.  (c) Every one of the 243 competitor bounds lies strictly
below the active column throughout `[0.376932,0.376933]`.  The ranked gaps are
exact monotone-sandwich gaps; the closest competitor is `s=164`, still lower
by approximately `9.9933786489298977945e-05`.  (d) The active column at the
window left and the seven closest competitors at the window right show the
same sandwich on a focused parts-per-million scale.  Comparing competitors
at the right endpoint with the active column at the left endpoint is the
deliberately stronger full-window comparison.

Every sign, root count, and ordering decision uses GMP rationals.  The result
is a sharp local threshold theorem for the reduced canonical edge generating
system and this induced two-block weighted-l1 norm.  It is not a PDE
singularity theorem and does not establish or refute three-dimensional
Navier--Stokes regularity.
