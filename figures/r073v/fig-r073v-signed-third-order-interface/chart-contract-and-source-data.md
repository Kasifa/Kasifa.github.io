# R0.73V chart contract and source data

## Analytical question

How does the pressure-aware signed third-order heat lift expose an exact scale
interface, and where do coefficientwise pressure and fourth-order terms enter?

## One-sentence takeaway

The two-path exact certificate resolves the signed lift explicitly, separates
an order-s-squared cumulant-flux coefficient from order-s pressure
coefficients, and exhibits both a pressure-strain-only zero mode and a selected
nonzero quartic tangent under parabolic dilation.

## Visual and delivery contract

- **Surface:** standalone static journal figure for the R0.73V HTML note and
  synchronized PDF.
- **Panel A:** exact pressure-aware compressed interface at
  \(h_*=(1,2,0)\): raw \(\mathcal C_s\), resolved
  \(v_s\odot N_s\), and signed residual \(\chi_s\).
- **Panel B:** exact four-site Germano-mode decomposition, retaining every
  displayed active-block entry and the certified small-s orders. The omitted
  third row and third column are exactly zero in the sealed 3 by 3 tensors. The
  \(s^{-1}\) comparison is coefficientwise, not a whole-field theorem.
- **Panel C:** exact six-site zero-mode witness: contracted cumulant flux and
  pressure diffusion vanish while pressure strain remains nonzero.
- **Panel D:** exact selected \(\kappa_{112}\) quartic q-polynomial,
  its finite-\(\varepsilon\) cross-check, and its parabolic dilation.
  The line is a deterministic rendering of the displayed closed formula.
- **Renderer:** reproducible local Matplotlib; SVG, one-page PDF, and 600 dpi
  PNG.
- **Palette:** hard two-root cap (blue and gold) plus neutrals. Filled/open
  boxes, solid/dashed strokes, direct labels, and matrix layout preserve
  meaning in grayscale.
- **Footprint:** 178 mm by 118 mm.
- **Final QA:** exact two-path equality, source-row reconstruction, certificate
  commit bindings, SVG/PDF/PNG integrity, final-size raster, independent PDF
  raster, exact grayscale conversion, and visual inspection.

## Source-data schema and sufficiency

`source-data.csv` records every diagram identity, every displayed exact matrix
entry, every q-polynomial coefficient, every certified small-s order and
leading coefficient, the six-site exact zeros, the finite-perturbation
cross-check, and deterministic samples of the Panel D closed profile. Each row
retains its primary and independent JSON paths, evidence class, normalization,
and the hashes of both producer outputs.

The two producer objects are required to be identical before rows are emitted:

```text
primary.commonCore == independent.commonCore
commonCoreSha256 = 24519dec8a70d0ebe1e0ba3ea1899569ca3dbfabc1b11691990387c628731fa2
```

The plotted Panel D profile is

\[
 g(\theta)=2e^{-2\theta}(1-e^{-2\theta})^2,
 \qquad
 \left.\partial_t\widehat\kappa_{112,s}(0,2L,0)\right|_{\rm nl}
 = iL\,g(\theta),
 \quad s=\theta L^{-2}.
\]

Its sampled points are only rendering coordinates. Exact nonvanishing for
\(\theta>0\), the q-polynomial, and the factor \(L\) are read from the
certificate, not fitted from the curve.

## Interpretation boundary

The figure certifies exact finite Fourier coefficients. It does not establish
information-theoretic minimality, whole-field non-recovery, finite-order PDE
nonclosure, generic Navier--Stokes integration, a singular solution, improved
regularity, global regularity, or the Clay conclusion. No GPU, network
service, simulation, or DGX result supports the figure.
