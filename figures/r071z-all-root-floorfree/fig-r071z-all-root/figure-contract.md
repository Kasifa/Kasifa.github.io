# Figure contract: R0.71Z all-root suppression and launch retention

## Analytical question

How do the complete squared-slope mass, the exact integer-lattice cost,
growth of the observation coupling, and launch retention change the normalized
endpoint envelope in the R0.71W-Y real-shear triangular class?

The one-sentence takeaway is fixed before rendering:

> At bounded observation coupling, complete-root BV sampling removes the
> selected-root factor (N), changing the exact lattice law from (M^{-1})
> to (M^{-2}); the same certified upper envelope becomes asymptotically
> (M^{-5/6}) for η (=M^{1/2}) and nonvanishing for
> η (=M^{6/7}), while a window excluding launch can lose enstrophy by
> θ (=exp(-2νd^2A_0R^2)) whereas launch-inclusive retention is one.

## Data grain

- Panel A extracts all 30 committed minimum-lattice rows
  (M=2^j+1), (j=1,…,30), and plots (M/K_s) with
  (K_s=\sum_{l=1}^M l^2), together with the analytic bound (3/M^2).
- Panel B uses the certified fixed-η row at η (=1). The complete-root
  envelope is proportional to (M/K_s). The neutral comparator multiplies
  the same row by (N=(M-1)/2), reproducing the older selected-root payment.
  Both share the same (M=3), (N=1) normalizer.
- Panel C reconstructs the exact declared formula
  
  \[
  \frac{M}{K_s}\,η^{4/3}
  e^{2\lambda_0L}(4+C_\kappaη),
  \]
  
  up to common fixed geometry constants, for η (=1),
  η (=M^{1/2}), and η (=M^{6/7}). Each curve is divided by its
  own (M=3) value so that the comparison concerns scaling rather than
  arbitrary fixed constants.
- Panel D evaluates the exact heat-shear retention formula at integer
  (R=1,…,32), using the certified ν (=0.02), (d=8), and
  (A_0=0.05). The eight dyadic certificate points are independently
  cross-checked; no interpolation of simulated output occurs.

There is no random sample, physical fit, PDE time stepping, or DNS.

## Visual encoding

- Static 178 mm double-column output in a two-by-two panel layout.
- Near-white paper, dark ink, one muted blue root, an ochre focus series, and
  neutral gray scaffolding. No gradient or decorative chart background.
- Every color distinction is duplicated by line style, marker shape, and
  marker fill.
- Positive (M)- and retention-scaling comparisons use logarithmic axes.
- The old selected-root result is always neutral and dashed; it is never
  styled as new R0.71Z evidence.

## Required evidence boundaries

- Panels A-C are theorem/certificate envelopes, not observations of a
  constructed growing-root solution.
- The all-root theorem controls squared slope mass, not raw zero count.
- The (M^{-2}) result uses real shear, a fixed target, distinct positive
  integer carriers, unit launch phases, and fixed (A_0>0).
- The floor cancellation is mixed-window: roots stay on (I_t=[a,b]), while
  the common payment is computed on (K_t=[σ_q,b]), which includes launch.
- The η (=M^{6/7}) curve is a diagnostic for saturation of this upper
  bound. It is not a strong-coupling root construction.
- Panel D disproves automatic fixed-window retention from launch data. The
  displayed heat shear has no nonzero target-root atom, so it is not a
  counterexample to every fixed-window floor-free atom inequality.
- No universal endpoint estimate, singularity construction, or
  Navier-Stokes regularity result is asserted.

## Outputs and QA

- vector PDF and SVG;
- 600 dpi archival PNG;
- final-size color, true-grayscale, and independent Poppler PDF previews;
- independent formula, source-hash, package-hash, and page-size validation;
- manual final-size inspection in color, grayscale, and the PDF render.
