# R0.72Z Orr--Sommerfeld threshold and Squire-payment figure

This package is the reproducible source for a three-panel, double-column
journal figure. It visualizes only formulas proved or explicitly delimited in
the bound R0.72Z report:

1. the signed relative-form sufficient threshold and the sharp high-mode
   exponent `g ~ |c|^(2/5)`, equivalently `g ~ alpha^(-2)`;
2. the exact low-mode instantaneous-growth witness and the abstract gapless
   heat-tangent solution; and
3. kinetic orientation `chi <= 1` together with the explicit `|Lambda|`-paid
   Squire history multipliers.

All plotted rows are direct evaluations of closed expressions. There is no
PDE time-stepper, eigenvalue solver, optimization, regression, random seed, or
fitted exponent. The high-mode points are a deterministic sequence testing
the exact limit in report equation (7.6); they are not simulation output.

The tangent curve belongs to the abstract mean-zero `beta=mu=0`
Orr--Sommerfeld space. It is not a physical zero-frequency velocity row and
does not disprove a projected positive-`mu` theorem. The Squire panel is
conditional on a declared `Q`-history norm and retains the unavoidable
background payment `|Lambda|`.

The renderer is deterministic and refuses to certify formal output without a
clean two-commit source/certificate lineage plus explicit visual inspection.
The source stage creates no PDF, PNG, or SVG. Blue and gold are the only
chromatic roots; line style, markers, open fill, direct labels, and panel
structure provide grayscale redundancy.
