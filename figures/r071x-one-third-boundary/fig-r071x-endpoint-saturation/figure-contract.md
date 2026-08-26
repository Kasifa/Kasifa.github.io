# Figure contract: R0.71X fixed-small-coupling endpoint scaling

## Analytical question

For the exact triangular recurrence family with

\[
A_q=\delta q^2,
\]

do the source certificates show the endpoint bookkeeping

\[
D_q\asymp q^6,\qquad \text{atomProxy}_q\asymp q^2,
\qquad \frac{\text{atomProxy}_q}{D_q^{1/3}}\asymp q^0,
\]

and the predicted \(\delta^{4/3}\) collapse? The figure must keep the exact
high-precision algebra and the finite retained-coset corroboration visually
separate.

## Data grain

- Panel A: five deterministic retained-coset cases, one at each
  \(q=256,512,1024,2048,4096\), indexed to the first case so the two powers
  are comparable on one axis.
- Panel B: seven high-precision fixed-\(\delta\) cases and five separate
  retained-coset cases. Four quantities are shown as distinct evidence layers;
  they are not added or treated as interchangeable.
- Panel C: five deliberate high-precision \(\delta\)-sweep cases at
  \(q=2048\). The inset shows three truncation-radius comparisons against
  \(R=40\) at \(q=1024\).
- No stochastic sample, fitted physical parameter, or DNS trajectory occurs.

## Visual encoding

- Static 178.05 mm double-column output; Panel A spans the top row.
- Near-white paper, dark ink, muted blue and ochre; no gradient.
- Solid/dashed/dotted line styles and filled/open marker shapes duplicate every
  color distinction.
- Logarithmic axes are used only for positive scale comparisons.
- Power guides are descriptive references, not proofs.

## Required evidence boundaries

- `atomProxy` is written exactly as a proxy, never as \(J_*\). The numerical
  certificates do not lock the compact multiplier value or the associated
  \(\kappa_*\) factor.
- The complete-ledger-normalized analytic proxy and the finite full-retained
  charge are plotted as separate layers, with no claim that they are the same
  quantity.
- The finite retained Fourier-coset calculation is not DNS and is not a
  spectral-convergence theorem.
- The continuum implicit-function radius is existential. The plotted
  \(\delta=1/128\) has not been proved to be inside that radius.
- No universal \(D^{1/3}\) inequality or Navier--Stokes regularity result is
  claimed.

## Outputs and QA

- vector PDF and SVG;
- 600 dpi archival PNG;
- final-size color, true-grayscale, and independent Poppler PDF previews;
- source/data/hash validation and package-level checksum ledger;
- manual inspection at final size, including grayscale and PDF clipping.
