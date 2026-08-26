# Figure contract: R0.72B-1

## Analytical question

How much extra many-carrier suppression follows from the exact target-row
norm, and do one-carrier Bessel roots occur before the adjacent frozen-profile
enhanced-dissipation scale?

## Supported takeaway

For the canonical exact-launch profile \(r_l=l,z_l=1\), the target-row factor
is \(\chi_M=1/(2M)\) and \(\Omega^2/K_v\sim12/M\). Together with
\(M/K_s\sim3M^{-2}\), the normalized geometric prefactor is
\(M^{-10/3}\). The sufficient phase boundary becomes
\(\alpha<\min\{5/2,(10+3\beta)/7\}\). The one-carrier Bessel layer still
satisfies \(L_R\Gamma_{\mathrm{fr},R}\to0\), vanishing heat-freezing error,
and vanishing analytic energy-loss upper bound before burn-in.

## Static renderer

- Matplotlib
- 178 mm x 86 mm
- white background
- deep ink, muted blue, ochre, and neutral gray
- solid/dashed/dotted lines and filled/open/distinct markers
- PDF, SVG, and 600 dpi PNG

## Panels

- **A:** old \(M^{-2}\), target-participation \(M^{-3}\), and coherent
  \(M^{-10/3}\) sufficient boundaries against \(\beta\).
- **B:** exact equal-carrier \(\chi_M\), \(\Omega^2/K_v\), and the combined
  gain relative to the old uniform multiplier constant.
- **C:** \(\Theta_R=L_R\Gamma_{\mathrm{fr},R}\), heat-freezing
  \(\Xi_R\), and the analytic energy-loss upper bound.

## Claim boundary

Panel A and the equal-carrier curves are analytic formulas. Panel C evaluates
analytic comparison formulas at SciPy/mpmath Bessel zeros. The two machine
paths are not interval arithmetic. Enhanced dissipation after a burn-in can
control only the remaining tail; it cannot subtract the nonnegative
pre-burn-in ledger. No normalized lower family, three-dimensional DNS,
regularity theorem, or blow-up theorem is claimed.
