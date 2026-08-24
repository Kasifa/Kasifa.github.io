# Figure contract — R0.70H core-moment gap

## Analytical question and takeaway

The figure asks which adjacent-scale core-moment coordinate detects the
persistent baseline in the R0.70F recurrence, and where the unresolved
spacetime amplification enters.  For the \(\Lambda=2\) algebraic sample,
ordinary adjacent increments decay and their total variation saturates,
whereas the instantaneous pairing-covariant increments remain order one and
accumulate linearly.  The actual spacetime source--core dual requirement adds
the stronger weight \(r_k^{-3}\).

## Chart contract

- **Panel A:** semilog ordered comparison over \(k=1,\ldots,12\) for the
  ordinary increment and the degree-zero/degree-one instantaneous
  pairing-covariant increments.
- **Panel B:** cumulative ordered comparison over \(N=1,\ldots,40\) for the
  degree-zero pairing \(\ell^1\) and square masses, with an inset showing the
  saturation of ordinary total variation at \(31/225\).
- **Panel C:** base-two logarithmic comparison over \(k=0,\ldots,8\) for the
  spacetime coordinate weight \(r_k^{-2}=2^{4k}\) and the focal dual weight
  \(r_k^{-3}=2^{6k}\), using \(r_0=1\) and \(\rho=1/4\).
- **Renderer and footprint:** static Matplotlib; 178 mm double-column width;
  vector PDF and SVG plus a 600 dpi PNG.
- **Palette:** hard two-root cap. Blue denotes ordinary differences or the
  contextual \(r_k^{-2}\) weight; rust denotes pairing-covariant quantities
  and the focal \(r_k^{-3}\) weight. Stroke style, marker fill, direct labels,
  and panels preserve the distinctions without color.

## Source data

`data.csv` contains 41 scale rows and evaluates the exact formulas

\[
 b_k=\frac{1-q^k}{1-q},\qquad g_k=b_k^2,
 \qquad q=\Lambda^{-4}=\frac1{16},
\]

the ordinary increment \(g_{k+1}-g_k\), the pairing increments
\(g_k-\rho^{n+2}g_{k+1}\) for \(n=0,1\), their finite cumulative masses, and
the weights \(r_k^{-2}\), \(r_k^{-3}\).  Every row is a closed-form
evaluation; no fitted parameter or trajectory sample is used.

## Claim boundary

This is an **algebraic diagnostic, not an NSE trajectory**.  The finite choice
\(\Lambda=2\) is an algebra sample only and does not verify the compact
support-separation geometry required by R0.70F.  The figure is not simulation
evidence or a numerical PDE proof, and it establishes no nonlinear time
persistence, parabolic Carleson estimate, regularity, or singularity result.
