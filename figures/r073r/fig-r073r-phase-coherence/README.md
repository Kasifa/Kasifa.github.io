# R0.73R phase-coherence scaling figure

This two-stage package defines a paper-ready three-panel figure for the
matched Dirichlet/Rudin--Shapiro tensor family in R0.73R. It is an analytic
formula diagnostic. It is not a numerical simulation, a fitted scaling law,
or a regularity certificate.

The analytical question is whether matched Fourier support, coefficient
moduli, and quadratic Sobolev data can coexist with a growing phase-sensitive
heat-flow separation. The one-sentence takeaway is that the explicit phase
choice alone changes the normalized heat-flow scaling by a factor
\(m^{2/3}\), while after the shared amplitude scaling the Dirichlet heat
guide stays order one and the Rudin--Shapiro heat guide tends to zero.

- Panel A draws the common positive Fourier packet for \(m=8\), \(N=8m\).
  Both fields occupy the same sites and every displayed coefficient has
  modulus \(1/(\sqrt2m)\). Only the signs differ. The omitted negative packet
  is the complex-conjugate reflection required by reality.
- Panel B draws the unscaled analytic guides
  \(\|W_{D,m}\|_{\mathfrak X}\asymp m^{1/6}\),
  \(\|W_{P,m}\|_{\mathfrak X}\asymp m^{-1/2}\), and their
  \(m^{2/3}\) ratio.
- Panel C draws the analytic guides after
  \(\alpha_m=\sqrt8\,m^{-1/6}\): common \(L^2\) size
  \(m^{-1/6}\), Dirichlet heat-flow size \(1\), Rudin--Shapiro
  heat-flow size \(m^{-2/3}\), and common \(\dot H^{1/2}\) size
  \(m^{1/3}\).

Panels B and C are normalized at \(m=1\). Their vertical values suppress the
fixed constants hidden by \(\asymp\); only the stated exponents and common
normalization are encoded. No regression or PDE trajectory is used.

The source writes `source-data.csv` together with vector SVG and PDF, a
600-dpi PNG, independent PDF/final-size/grayscale QA rasters, environment and
monitoring records, and sealing metadata. The static Matplotlib surface is 178 mm
double-column width. Thirteen analytic observations spanning twelve dyadic
steps are sufficient to display the predetermined powers; there is no
statistical estimation. The palette uses at most two non-neutral roots plus
neutrals, and marker fill, marker shape, and line style preserve meaning in
grayscale. Final QA must inspect the 178 mm print-size and grayscale exports.
A scratch output directory keeps data-only test renders outside the source tree:

```text
PYTHON=/Users/kasifa/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3
DEPS=/tmp/r073r-figure-deps
$PYTHON -m pip install --target $DEPS -r requirements.txt
$PYTHON plot.py --deps $DEPS --data-only --output-dir /tmp/r073r-phase-coherence-data
```

`plot.py --render-preseal` creates the raw package on local CPU. `validate.py`
reconstructs all 141 CSV rows without importing plotting code, checks the
178 by 94 mm one-page vector surfaces, and creates a source-unsealed preseal.
Formal status requires a later immutable source commit: `--final
--source-commit <40_HEX>` verifies all ten committed source blobs byte for
byte before writing the final manifest. Raw assets and formal metadata are
committed only in the second stage.
