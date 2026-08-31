# R0.73U chart contract and source data

## Analytical question

Which information is recovered by the full local-product tensor heat
hierarchy, and which signed physical-time tangent remains unidentifiable from
an even quadratic state?

## One-sentence takeaway

The tensor hierarchy reconstructs pressure exactly, but an exact four-site
parity witness leaves a signed odd tangent unresolved and retains a
one-derivative \(s^{-1/2}\) cost on parabolic heat slices.

## Visual and delivery contract

- **Surface:** standalone static journal figure for the R0.73U HTML note and
  synchronized PDF.
- **Panel A:** exact continuum map, not a numerical chart: \(T\to p\), but
  the even quadratic state does not determine the signed cubic and
  pressure--velocity tangent.
- **Panel B:** exact finite Fourier diagnostic at the same initial time
  \(t=0\) and \(h_*=(1,2,0)\), displaying every entry of \(A+B=K\) and the
  \(u/-u\) initial-tangent separation.  This is not a trajectory-symmetry
  claim.
- **Panel C:** analytic line plot of \(f(z)=ze^{-5z^2}\), including its exact
  maximizer \(z_*=1/\sqrt{10}\) and the explicit parabolic
  \(s^{-1/2}\) boundary.
- **Renderer:** reproducible local Matplotlib; SVG, one-page PDF, and 600 dpi
  PNG.
- **Palette:** hard two-root cap (blue and gold) plus neutrals.  Filled versus
  open boxes, solid versus dashed arrows, direct labels, and matrix layout
  preserve meaning in grayscale.
- **Footprint:** 178 mm by 100 mm.
- **Final QA:** exact source-row reconstruction; source inventory; PDF, SVG,
  and PNG integrity; 600 dpi dimensions; independently regenerated PDF
  raster; exact grayscale conversion; and manual inspection.

## Source-data schema and sufficiency

`source-data.csv` contains four schematic claims for Panel A, twenty-two exact
finite records for Panel B, 111 samples of the exact Panel C function on
\(0\le z\le1.1\), and one separate exact peak record.  The curve rows are
renderer samples of a closed formula, not observations.  The table retains
component indices, exact integer values where applicable, formula,
normalization, evidence class, and source origin.

Panel B uses

\[
 A=\begin{pmatrix}-2&3\\3&-4\end{pmatrix},\qquad
 B=\begin{pmatrix}0&-2\\-2&4\end{pmatrix},\qquad
 K=A+B=\begin{pmatrix}-2&1\\1&0\end{pmatrix}.
\]

The viscous tensor coefficient is defined before use by

\[
 V=\Delta T-2\sum_\ell
   \partial_\ell u\otimes\partial_\ell u,
 \qquad \widehat T(h_*)=\widehat V(h_*)=0.
\]

The plotted separation is the Frobenius norm of the coefficient difference,
evaluated at \(t=0\); it is not a spatial norm and not a PDE trajectory.

## Interpretation boundary

The no-go concerns an autonomous **signed equality** based only on the even
quadratic heat state.  It does not exclude one-sided estimates, absolute
bounds, cancellations after time integration, or hierarchies augmented by
odd/cubic data or the signed velocity.  The witness is smooth and planar.
No numerical simulation, parameter fit, GPU, network service, or DGX supports
the figure.
