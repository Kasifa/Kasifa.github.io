# Figure contract: R0.71V fixed-target zero-level boundary

## Analytical question

For the exact two-root 2.5D recurrence tangent, can auxiliary frequencies
of size \(q\) drive one fixed low target so that the atom at the **second**
prescribed root is not uniformly paid by the target-shell first-time-jet row,
even after the first root is separately paid? How rapidly do the corresponding
excursion height charges lose the root slope?

## Evidence and decision

The figure evaluates closed response functions and deterministic
one-dimensional quadratures for

\[
q\in\{8,16,32,64,128,256\}.
\]

It must let a reader distinguish four facts: convergence of the rescaled
target profile, the four principal \(q\)-orders, the diverging or vanishing
ratios, and the failure of a uniform excursion non-collapse factor. The
figure is a finite corroboration of the analytic asymptotics. It is not the
proof of the implicit-function theorem or its nonlinear remainder estimate.

## Data grain

- Panel A: 601 scaled-time samples for each of six \(q\)-values and the
  limiting profile; the printed figure displays \(q=8,32,256\) and the limit.
- Panels B-D: six exact parameter cases, one row per plotted metric and \(q\).
- Every quantity uses the same fixed target, multiplier, target-shell scale
  \(\kappa_*=1\), multiplier \(m_*=1\), target wave number \(\rho^2=2\), viscosity, macroscopic
  window, background, and two scaled root locations.
- No stochastic samples, fitted physical parameters, or external data occur.

## Visual encoding

- Static 2 by 2 figure, 178.05 mm by 134.11 mm.
- Near-white paper, dark ink, muted blue and ochre; no rainbow palette.
- Line style, marker shape, and open versus filled markers duplicate all color
  distinctions for grayscale use.
- All magnitude panels use logarithmic axes and show explicit power-law
  guides. The guides are descriptive comparisons, not regression evidence.
- A small locked top-right blossom carries no data encoding.

## Required labels and boundaries

- Neutral title: "Fixed-target zero-level boundary layer".
- Subtitle: \(\nu=0.02\), \(K_y=K_z=1\), \(d=8\), roots
  \((0.1,0.2)/q^2\), \(\ell=0.5\), and the background mode.
- Panel B's atom is the second prescribed root only. Its rows are the selected
  singleton target-shell quantities \((2/\ell)\mathcal B_{1,q}^{(*)}\) and
  \((7\ell/3)\mathcal B_{2,q}^{(*)}\), with the theorem coefficients shown.
- The sum of both atoms may remain in machine-readable results as an auxiliary
  check, but it is not a plotted no-go quantity.
- Restore every fixed singleton-shell constant. With
  \(\rho^2=2\) and \(m_*=\kappa_*=K_z=1\), the producer and independent
  validator must check \(J=2j_{\rm red}\),
  \(\mathcal B_1^{(*)}=8b_{1,\rm red}\),
  \(\mathcal B_2^{(*)}=8b_{2,\rm red}\), and
  \(H_E^2=8h_{E,\rm red}^2\), while \(D_E\) is unchanged.
- Footer states that the target and window are fixed, that the calculation is
  not a covariant dilation, and that no nonlinear time integration or DNS is
  used.

## Outputs and QA

- vector PDF and SVG;
- 600 dpi archival PNG;
- color, true-grayscale, and independent Poppler PDF-render previews;
- inspection at final 178 mm print width;
- independent high-precision reconstruction, output checks, and checksums.
