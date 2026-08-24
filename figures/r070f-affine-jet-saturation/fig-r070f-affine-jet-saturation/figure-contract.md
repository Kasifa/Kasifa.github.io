# Figure contract — R0.70F affine-jet saturation

## Supported claim

The figure supports the exact Taylor work powers, the exact linear growth of
the bounded--bounded triangular convolution for every fixed power, and the
geometry of the compact initial-face constant/linear jet witness.

## Source data

- taylor-gap-data.csv: evaluations of
  \(2^{-m},2^{-2m},2^{-3m},2^{-4m}\);
- triangular-sum-data.csv: evaluations of the exact closed form
  \(N/(2^\beta-1)-(1-2^{-\beta N})/(2^\beta-1)^2\);
- recurrence-factor-data.csv: the exact geometric factor
  \(b_n^2=[(1-\Lambda^{-4n})/(1-\Lambda^{-4})]^2\) at \(\Lambda=16\).

## Visual encoding

Panel A uses a logarithmic vertical axis. Panel B uses the exact cumulative
sums, not fitted lines. Panel C deliberately exaggerates the radius ratio so
that the source annulus, harmonic core, and off-centre vorticity lobe remain
legible.

## Claim boundary

This is an explanatory analytic figure. It is not a fluid simulation, a
Navier--Stokes trajectory, evidence of blow-up, or a numerical proof that the
initial-face recurrence persists on nested backward cylinders with one common
positive terminal time.
