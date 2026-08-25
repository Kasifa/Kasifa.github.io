# Figure contract - fig-r071c-viscous-sign-creation

## Analytical question

Can an exactly cancelled signed packet sum at \(\tau=0\) remain nonpositive
under unequal viscous decay, and how is the latent fine-ledger mass
redistributed?

## Exact quantities

With dimensionless time \(\tau=\nu t\), the two selected output works are

\[
w_1(\tau)=2e^{-8\tau},\qquad
w_2(\tau)=-2e^{-14\tau},\qquad
W(\tau)=w_1(\tau)+w_2(\tau).
\]

The parent and fine signed-before-square ledgers, together with the refinement
defect, are

\[
E_{\rm root}(\tau)=
\frac{(W(\tau)^+)^2}{16e^{-8\tau}},\qquad
E_{\rm fine}(\tau)=
\frac{(w_1(\tau)^+)^2}{8e^{-8\tau}},\qquad
\delta(\tau)=E_{\rm fine}(\tau)-E_{\rm root}(\tau).
\]

At \(\tau=0\),

\[
W=0,\qquad E_{\rm root}=0,\qquad
E_{\rm fine}=\delta=\frac12.
\]

For every \(\tau>0\), \(W(\tau)>0\). At
\(\tau_*=\log 2/6\),

\[
E_{\rm root}=2^{-16/3},\qquad
E_{\rm fine}=2^{-7/3},\qquad
\delta=7\,2^{-16/3}.
\]

## Panel contract

- **A - Signed packet work.** Plot \(w_1\), \(w_2\), and their parent sum
  \(W\) on \(0\leq\tau\leq1/2\). Keep the zero line visible. Mark exact
  cancellation at \(\tau=0\) and state the strict sign \(W(\tau)>0\) for
  \(\tau>0\).
- **B - Ledger refinement identity.** Plot \(E_{\rm root}\),
  \(E_{\rm fine}\), and \(\delta\) on the same interval. Mark
  \(\tau_*=\log2/6\) and annotate the three exact values there.

## Data sufficiency and provenance

The source table contains 251 exact rational grid values
\(\tau=j/500\), \(0\leq j\leq250\), plus the exact irrational marker
\(\tau_*=\log2/6\). Each row retains the two child works, parent work,
parent dissipative denominator, both ledgers, and the refinement defect. The
display uses closed exact formulas and high-precision evaluation; there is no
random seed, fitted curve, DNS, or numerical time integration. A second script
recomputes every CSV row without importing the plotting module.

## Visual rules

- Static Matplotlib at double-column width, 178 by 92 mm.
- Vector PDF and SVG plus a 600 dpi PNG.
- Hard cap of two non-neutral color roots plus neutral parent quantities.
- Solid, dashed, and dash-dot strokes with distinct marker shapes preserve
  distinctions in grayscale.
- The visible zero line and linear axes preserve sign and magnitude honestly.
- Original-resolution, grayscale, and rendered-PDF QA surfaces are inspected.

## Claim boundary

The figure records an exact two-packet Stokes heat-semigroup witness and the
associated refinement identity. It does not prove time integrability for a
Navier--Stokes continuation coefficient. It is not a new continuation
criterion, a finite-time singularity result, a global-regularity result, or a
solution of the Millennium problem.
