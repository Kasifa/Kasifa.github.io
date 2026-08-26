# Figure contract -- R0.72D dynamical ledger

## Analytical question

Does translating a Rudin--Shapiro carrier block from low frequencies to
\([M,2M)\) preserve its phase-flat \(\sqrt M\) multiplier scale while
compressing its thermal exposure to \(M^{-2}\), and does the exact interior
root retain an \(aM\) target-row slope at the resulting critical coupling?

## Intended takeaway

After the natural normalizations, the heat-weighted multiplier curves collapse
on the time variable \(s=M^2x\).  The exact-root slope approaches a positive
constant, the mixed exposure remains of order \(M^{-2}\), and the normalized
numerator and full-charge proxies stay order one.  The figure is a finite
diagnostic of the analytic theorem, not its proof.

## Chart family and variants

- Family: two-panel static journal figure.
- Panel A: normalized heat-weighted multiplier envelope against scaled time
  \(s=M^2x\), with one line for each dyadic carrier count.
- Panel B: dimensionless root/ledger diagnostics against \(M\) on a logarithmic
  horizontal axis.
- Variants: archival color figure and grayscale QA rendering.

## Data sufficiency

- The multiplier envelope is computed directly from the shifted
  Rudin--Shapiro coefficients on a declared uniform phase grid.
- The root adjustment and slope come from the independently assembled finite
  lattice ODE at \(\tau_M=M^{-3}\).
- Algebraic ledger proxies use the exact moment
  \(K_s=M(2M-1)(7M-1)/6\) and declared coupling
  \(\delta a=\gamma M^{3/2}\).
- Every plotted row is preserved in `data.csv`; no value is read from a
  screenshot or manually transcribed from the report.

## Renderer and publication surface

- Renderer: Python/Matplotlib static vector workflow.
- Target: mathematical-analysis journal and project research note.
- Final width: 178 mm double column.
- Exports: vector PDF, SVG, and 600 dpi PNG.
- QA: final-size raster, PDF raster, and grayscale rendering.

## Visual encoding

- Neutral descriptive title; no claim word such as “proof” or “breakthrough”.
- Restrained navy, rust, teal, and gray palette.
- Line style and marker shape duplicate color distinctions.
- Panel A uses a linear scaled-time axis and logarithmic vertical axis only if
  the sampled dynamic range requires it.
- Panel B uses log base 2 on \(M\); the vertical axis is linear because every
  diagnostic is dimensionless and expected to approach a finite constant.
- Direct labels or a compact legend are used; no decorative gradients or 3D
  effects.

## Required annotations

- State \(r_j=M+j\), \(M=2^n\), and \(\tau_M=M^{-3}\).
- State the finite phase-grid and lattice-truncation resolutions in the
  caption/manifest.
- Mark the asymptotic reference levels without presenting a fitted line as an
  analytic proof.
- Caption must state that numerical root residuals and slope ratios corroborate
  but do not prove the infinite-lattice theorem.

## Output and QA criteria

1. No clipped labels, legend, or panel tags at 178 mm width.
2. PNG metadata reports approximately 600 dpi.
3. SVG and PDF remain vector outputs.
4. All series remain distinguishable in grayscale.
5. Axis labels include every normalization and no ambiguous unit.
6. Source data, configuration, environment, command, manifest, checksums, and
   validation report are archived in this package.

