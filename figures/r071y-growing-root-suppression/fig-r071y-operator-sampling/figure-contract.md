# Figure contract: R0.71Y growing-root operator sampling

## Analytical question

How do the number (N) of selected exact roots, the minimum scaled root
separation (h), and the conditioning of the equal-grid response matrix
jointly constrain the growing-dimensional continuation of the R0.71W
triangular family?

The one-sentence takeaway is fixed before rendering:

> At bounded observation coupling, the exact selected-root theorem envelope
> decays like (N^{-1}) without a separation hypothesis, improves to
> (N^{-2}) at fixed (h>0), and returns to (N^{-1}) for
> (h\asymp N^{-1}); the canonical equal-grid choice (r_l=l),
> (h=N^{-3}) simultaneously forces the certified inverse lower bound to
> grow rapidly.

## Data grain

- Panel A contains 21 deterministic powers-of-two values
  (N=1,2,\ldots,2^{20}). It plots the exact minimum-lattice factor
  (NM/K_s), with (M=2N+1) and
  (K_s=\sum_{j=1}^{M}j^2), against the theorem bound (3/(4N)).
- Panel B contains the same 21 values for each of three exact theorem
  envelopes, all normalized by their (N=1) value. The no-separation curve
  uses the committed fixed value \(\delta_{\rm obs}=1/8\). The separated
  curves use (M/(bhK_s)) with (h=0.05) and (h=N^{-1}).
- Panel C contains the five certified values (N=4,8,16,32,64) for
  \(\log_{10}\|\mathsf M^{-1}\|_2\)'s lower bound under
  (h=N^{-3}), (r_l=l), and (r_{\max}=N+1).
- There is no stochastic sample, physical fit, PDE time stepping, or DNS.

## Visual encoding

- Static 178.05 mm double-column output, with Panel A spanning the top row.
- Near-white paper, dark ink, muted blue and ochre, quiet gray grids, and no
  gradient.
- Every color distinction is duplicated by line style and marker fill/shape.
- Logarithmic axes are used for positive (N)-scaling comparisons. Panel C
  uses a linear vertical axis because the plotted quantity is already a
  base-ten logarithm.
- The coincident normalized (N^{-1}) laws in Panel B are labeled as such;
  no visual offset is introduced.

## Required evidence boundaries

- Panels A and B are theorem envelopes, not observations of constructed
  growing-root solutions.
- The (N^{-1}) conclusion uses unit-modulus carrier phases, real shear,
  fixed target, and full growing-dimensional data/root-time enstrophy floors.
- The atom sum is over selected exact roots. No all-root count or
  no-spurious-root theorem is asserted.
- The equal-grid inverse lower bound is not an upper bound on the true
  nonlinear implicit-function radius; forcing direction and derivative
  Lipschitz constants remain separate payments.
- No DNS, universal endpoint estimate, singularity construction, or
  Navier--Stokes regularity result is claimed.

## Outputs and QA

- vector PDF and SVG;
- 600 dpi archival PNG;
- final-size color, true-grayscale, and independent Poppler PDF previews;
- source/data/hash validation and a package checksum ledger;
- manual final-size inspection in color, grayscale, and PDF render.
