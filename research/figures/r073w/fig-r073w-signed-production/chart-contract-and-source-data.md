# R0.73W chart contract and source data

## Analytical question

What does the exact signed-production heat-plane identity control, what is the
energy-class scale loss, and why do neither the sign nor a same-time quadratic
absorption law hold universally?

## One-sentence takeaway

Heat-plane characteristics pay the signed spatial mean through endpoint energy,
the unconditional energy-class estimate has the integrable envelopes
\(s^{-1/4}\) and \(S^{3/4}\), and an exact rank-three Fourier-support witness
realizes both production signs while its amplitude-normalized absorption
coefficient starts at \(1/78\).

## Visual and delivery contract

- **Surface:** standalone static journal figure for the R0.73W research note and
  synchronized PDF; it is not copied into `public/` by this package build.
- **Panel A — exact heat-plane identity:** draw normalized characteristics
  \(s+\nu t=c\) in the \((t,s)\) plane, highlight one segment, and show the
  endpoint payment
  \[
    \int_{t_0}^{t_1}\langle\Pi_{s(t)}(t)\rangle\,dt
      =E_{s(t_0)}(t_0)-E_{s(t_1)}(t_1),\qquad s'(t)=-\nu.
  \]
  The diagram uses \(\nu=1\) only to set the drawing coordinates; the displayed
  identity retains general \(\nu>0\).
- **Panel B — upper-bound shapes, not observations:** display the two
  dimensionless shapes \(s^{-1/4}\) and \(S^{3/4}\), each normalized to one at
  unit scale.  The panel must say explicitly that these are analytic upper-bound
  envelopes, not measured, simulated, or fitted data.  No sharpness claim is
  encoded.
- **Panel C — exact signed witness:** for the frozen rank-three Fourier-support
  field \(u_A=\pm A R\), plot
  \[
    {\langle\Pi_s\rangle\over A^3}
      =\pm {1\over4}q^2(1-q^2),\qquad q=e^{-s}.
  \]
  Mark the exact extremum at \(s=\tfrac12\log 2\), whose magnitude is
  \(1/16\).  The minus branch is obtained by \(R\mapsto-R\).
- **Panel D — dimensionless absorption coefficient:** plot
  \[
    c_{\rm abs}(s)={q^2\over
      2(13+12q^2+10q^4+4q^6)},\qquad q=e^{-s},
  \]
  which is the coefficient of \(A/\nu\) in
  \(|\langle\Pi_s\rangle|/(\nu\langle D_{ii,s}\rangle)\).  Mark the exact
  endpoint \(\lim_{s\downarrow0}c_{\rm abs}(s)=1/78\).  The curve is not
  asserted to be monotone; its small interior maximum is retained faithfully.
- **Renderer:** reproducible local Matplotlib; SVG, one-page PDF, and 600 dpi
  PNG.
- **Palette:** near-white paper, deep-gray text, one blue and one orange root
  plus neutral grays.  Solid/dashed/dash-dot strokes and filled/open markers
  carry every comparison independently of hue.
- **Research mark:** retain the repository's locked, data-free five-petal
  blossom at the whole-figure header's far right; it carries no legend or data
  meaning and must not overlap the R0.73W header token.
- **Footprint:** 178 mm by 126 mm, arranged as a 2 by 2 panel grid.
- **Final QA:** exact two-path certificate equality, deterministic source-row
  reconstruction, closed-form spot checks, SVG/PDF/PNG integrity, 600 dpi
  metadata, exact final-size and grayscale QA rasters, independent PDF raster,
  label/legend inspection, clipping guard, and SHA-256 inventory.

## Source-data schema and sufficiency

`source-data.csv` is a tidy deterministic rendering table.  Its columns are:

```text
panel,series,record,x,y,x_name,y_name,formula,evidence_class,
source_primary_path,source_independent_path,normalization,note
```

The table contains every plotted polyline point and every exact landmark:

1. all Panel A characteristic coordinates, the highlighted segment endpoints,
   and its endpoint-payment annotation;
2. all Panel B envelope samples, with the rows permanently labelled
   `analytic-upper-bound-shape-not-data`;
3. both Panel C parity branches and the exact \((\tfrac12\log2,\pm1/16)\)
   landmarks read from the rank-three certificate;
4. all Panel D closed-form samples and the exact \((0,1/78)\) endpoint.

Renderer samples are generated from the displayed formulas on frozen decimal
grids.  They are coordinates for drawing, not numerical evidence for the exact
claims.  The exact rank-three formulas are accepted only if
`results.json.commonCore == independent-results.json.commonCore` byte-for-byte
after canonical JSON serialization and the two producer files match their
recorded SHA-256 hashes.

## Interpretation boundary

Panel A controls a signed spatially averaged characteristic integral, not
\(\int|\Pi_s|\), and assumes periodic or boundary-decaying transport.  Panel B
records an unconditional Leray--Hopf energy-class upper bound but neither a
uniform zero-scale estimate nor optimality.  Panels C and D are exact finite
Fourier counterexamples to universal sign and amplitude-independent same-time
quadratic absorption statements.  They are not Navier--Stokes trajectories,
DNS, fits, generic-turbulence claims, singular solutions, regularity criteria,
global-regularity results, or a Clay conclusion.  No GPU, network service, or
DGX result supports this figure; ordinary translation is local and direct.
