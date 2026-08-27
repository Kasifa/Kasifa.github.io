# R0.72O gap matrix

**Date:** 2026-08-27
**Scope:** physical reinsertion of the R0.72N one-carrier cubic theorem and
the finite/common-band superposition interface inherited from R0.72L.

| Claim or interface | Status | Exact evidence | Boundary |
|---|---|---|---|
| R0.72N \(\mathcal C_{\rm diss}\) equals R0.72L raw \(\mathcal C_\times\) | Proved | \(y=R^2x\), row formulas, \(|\delta|a/R^2=\varepsilon\) | one carrier |
| Correct normalized ED numerator is \(\varepsilon^{11/6}\) | Proved | multiply by \(\Theta\), divide by \(D^{1/3}\) | not \(\varepsilon^{1/2}\) |
| ED bound survives \(\zeta e_0\) exact-root correction | Proved | full semigroup operator norm plus bounded coordinate functionals | fixed \(\mu\), one carrier |
| Improved one-carrier ledger (0.6) | Proved | R0.72L ledger plus new direct branch | declared exact-corrected family |
| Window \(\sqrt\varepsilon\lesssim R^{2/3}L_{R,\varepsilon}\) | Proved | divide ED numerator by local floor \(Z\) | upper scale gives boundedness |
| Little-o window gives normalized decay | Proved | all three ledger rows tend to zero | along the declared scaling ray |
| Fixed \(R\), arbitrary strong coupling is closed | Open | available ED envelope is \(O(\sqrt\varepsilon/\log\varepsilon)\) | sharper cubic or denominator needed |
| Full-superposition IED implies all-cross cubic bound | Proved conditionally | \(\rho^2\|V\|E\), no carrierwise expansion | assumes (0.13) with uniform constants |
| Conditional \(N\)-carrier numerator \(\varepsilon^{11/6}p^{4/3}\) | Proved conditionally | exact normalization after (0.14) | not an unconditional theorem |
| Conditional multi-carrier window (0.16) | Proved conditionally | divide by common-band local floor | uniform IED constants are part of the hypothesis |
| Carrierwise tensorization is sufficient | Disproved as a proof route | R0.72J triangle-rich \(N^2\) cubic | does not disprove full IED |
| Common band implies uniform Morse shape | Disproved | exact two-carrier degenerate critical point | theorem-applicability obstruction |
| Uniform full-superposition IED from \((R,N,B,p)\) | Open | no current theorem or project proof | needs shape parameter or rowwise route |
| Logarithmic one-carrier cubic | Open | finite diagnostics only | would address fixed geometry |
| Multiscale physical absorption | Open | R0.72L Schur ledger remains | no global payment |
| General 3D continuation criterion | Open | no endpoint bridge | Clay problem untouched |

## Earliest unresolved implication

The one-carrier physical reinsertion is closed through the window

\[
 \sqrt\varepsilon\lesssim R^{2/3}L_{R,\varepsilon}.
\]

The earliest structural gap is now the full-superposition estimate, with a
constant uniform over the compared carrier and geometry family,

\[
 \int_0^1E(y)\,dy\lesssim\varepsilon^{-1/2}E(0),
\]

or, more narrowly, the rowwise cubic bound

\[
 |\delta|\int|P_0VF\,P_0V^2F|\,dx
 \lesssim a^2N^2\varepsilon^{1/2}.
\]

Neither follows from common-band support without a quantitative shear-shape
input.
