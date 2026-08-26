# Figure contract: R0.72C-1

## Analytical question

How much exact-launch carrier suppression is lost under arbitrary physical
phases, and how does that loss change the sufficient coupling--layer region?

## Supported takeaway

For \(r_l=l\) with equal moduli, the coherent family has geometric prefactor
\(M^{-10/3}\), while the odd-generation Rudin--Shapiro sign family has the
sharp phase-uniform order \(M^{-8/3}\). A fixed positive observation time has
tail prefactor \(M^{-3}\). The corresponding sufficient coupling boundaries
are

\[
\alpha<\min\{5/2,(10+3\beta)/7\},
\]

\[
\alpha<\min\{2,(8+3\beta)/7\},
\]

and

\[
\alpha<\min\{9/4,(9+3\beta)/7\},
\]

respectively.

## Data sufficiency

- Panel A uses exact formulas at ten odd Rudin--Shapiro generations
  \(M=2^n\), \(n=1,3,\ldots,19\).
- Panel B uses 161 analytic points on \(0\le\beta\le4\) for each boundary.
- No random samples or fitted maxima enter the displayed claims.
- The producer and independent checker must both pass before rendering is
  marked release-ready.

## Static renderer

- Matplotlib
- 178 mm x 86 mm
- white background
- deep ink, muted blue, ochre, and neutral gray
- solid, dashed, and dotted lines plus filled/open markers
- PDF, SVG, and 600 dpi PNG

## Panels

- **A:** exact coherent and Rudin--Shapiro prefactors against carrier count,
  with analytic \(-10/3\) and \(-8/3\) references.
- **B:** sufficient \((\beta,\alpha)\) boundaries for coherent exact launch,
  arbitrary-phase exact launch, and a fixed-positive-time tail.

## Claim boundary

Panel A concerns the algebraic coefficient in a complete-root upper bound.
It does not show that the actual root ledger reaches that bound. Panel B shows
strict sufficient regions, not converses. The fixed-positive curve controls
only roots observed after burn-in; it cannot subtract the pre-ledger. No DNS,
general NSE endpoint, regularity theorem, or blow-up theorem is claimed.
