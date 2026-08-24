# Figure contract — R0.70J deviatoric helical symbol

## Analytical question and takeaway

The figure asks whether helicity or angular averaging supplies a null
structure for an exterior symmetric trace-free tensor paired with the
deviatoric high--high vorticity square.  The exact answer is negative at a
fixed direction: for

\[
 S_0=\operatorname{diag}(1/2,1/2,-1),\qquad
 \omega_\sigma=\sqrt2(e_1\cos\theta-\sigma e_2\sin\theta),
\]

the contraction is one at every phase and for both helicities.  Complete
second-order isotropy cancels the signed angular quadrupole, but its positive
part has normalized mean \(\sqrt{3}/9\).  The critical source square norm and
core dual square norm scale as \(r\) and \(r^{-1}\), respectively, leaving a
scale-invariant Cauchy product and signed pairing.

## Chart contract

- **Panel A:** 73-point phase sweep on \([0,2\pi]\). The two pure-helicity
  witnesses both equal one. The signed control
  \(2\cos(2\theta)\), obtained from a different STF tensor, has zero phase
  mean but is not pointwise zero. The control is included to distinguish
  signed averaging from a true null identity.
- **Panel B:** 49-point evaluation of
  \(K_{S_0}(z)=(3z^2-1)/2\), where \(z=\xi_3\). Positive and negative
  regions are distinguished by rust and open blue fills, with zeros at
  \(z=\pm1/\sqrt{3}\). Exact annotations record signed mean zero and
  positive-part mean \(\sqrt{3}/9\).
- **Panel C:** base-two log--log ledger at
  \(r=2^{-k}\), \(k=1,\ldots,12\), for amplitude \(a=1\), after factoring
  out the fixed profile constants, time integrals, and
  \(\Lambda^{-2}\) geometry. Source norm squared is \(r\), core dual norm
  squared is \(r^{-1}\), and the normalized geometric mean and signed
  pairing are one.
- **Renderer and footprint:** static Matplotlib; 178 mm double-column width;
  vector PDF and SVG plus a 600 dpi PNG.
- **Palette:** hard two-root cap. Rust marks pointwise-positive or focal
  pairing quantities; blue marks the opposite helicity or signed reference.
  Stroke styles, open versus filled markers, signed fills, direct labels, and
  panel separation preserve the distinctions without color.

## Source data

`data.csv` is a 145-row long-form table: 73 phase rows, 49 direction-cosine
rows, 12 critical-scale rows, and 11 exact-summary rows. Every plotted value
is an evaluation of a displayed closed formula. The table contains no fit,
DNS state, sampled NSE trajectory, or extrapolation from simulation.

## Claim boundary

This is **exact analytic tensor and scale data, not DNS and not a blow-up or
regularity result**.  Panel A disproves a universal helicity-based algebraic
null structure for an arbitrary external STF source. It does not show that
the chosen source is the wave's own pressure Hessian. Panel B assumes an
isotropic diagonal directional covariance before the positive part; a
physical cutoff can introduce coherent cross terms. Panel C records critical
monomial covariance, not nonlinear persistence to one fixed positive
terminal time. The figure establishes no Millennium-problem result.
