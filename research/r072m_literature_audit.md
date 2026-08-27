# R0.72M literature and claim-boundary audit

**Date:** 2026-08-27
**Method:** bounded search of primary papers, publisher records, and the
NIST Digital Library of Mathematical Functions.  The search is not a proof
of priority.

| Source | What it supports here | What it does not support |
|---|---|---|
| Waleffe, *Physics of Fluids A* 4 (1992), [DOI](https://doi.org/10.1063/1.858309) | triad transfer depends on exact geometry and polarization | large coupling forces positive full-lattice flux |
| Moffatt, *Journal of Fluid Mechanics* 741 (2014), [DOI](https://doi.org/10.1017/jfm.2013.637) | finite triad dynamics can differ from exact Fourier evolution | the frozen chain is an exact dissipative PDE solution |
| Bedrossian and Coti Zelati, *Archive for Rational Mechanics and Analysis* 224 (2017), [DOI](https://doi.org/10.1007/s00205-017-1099-y) | shear mixing can produce quantitative enhanced dissipation and hypoellipticity | their semigroup estimate bounds the absolute cubic variation used here |
| Coti Zelati and Gallay, *Journal of the London Mathematical Society* 108 (2023), [DOI](https://doi.org/10.1112/jlms.12782) | Morse shear profiles have sharp enhanced-dissipation time scales | the decaying-coupling chain satisfies the project-specific logarithmic cubic bound |
| Reddy and Henningson, *Journal of Fluid Mechanics* 252 (1993), [DOI](https://doi.org/10.1017/S0022112093003738) | non-normal operators can have large transient growth despite stable spectrum | every launch realizes an enstrophy lower bound |
| Aluie and Eyink, *Physics of Fluids* 21 (2009), [arXiv](https://arxiv.org/abs/0909.2451) | cascade statements require scale-localized sums rather than one largest triad | a positive flux lower bound for every smooth solution |
| Kishimoto and Yoneda, *Annals of Global Analysis and Geometry* 62 (2022), [DOI](https://doi.org/10.1007/s00021-022-00703-5) | genuinely nonlinear real finite-Fourier-support NSE evolution is structurally excluded | quantitative tail or cubic estimates for the infinite chain |
| Chernyshenko, Constantin, Robinson, and Titi (2007), [arXiv](https://arxiv.org/abs/math/0607181) | numerical approximations need residual control to certify a nearby strong solution | the present binary64 diagnostic is an a posteriori PDE proof |
| NIST DLMF Sections 10.6, 10.17, 10.19(iii), and 10.20(i), [recurrences](https://dlmf.nist.gov/10.6), [fixed-order asymptotics](https://dlmf.nist.gov/10.17), [transition region](https://dlmf.nist.gov/10.19.iii), [uniform large-order expansion](https://dlmf.nist.gov/10.20.i) | the Bessel derivative identity, fixed-order expansion, and uniform Airy control through the turning region | the project-specific row and physical normalization |

## Boundary decision

The primary literature does not support a statement of the form

\[
 \text{extreme coupling}\Longrightarrow
 K\gtrsim\varepsilon^{7/3}p^{4/3}
 \quad\text{or}\quad
 x\gtrsim\varepsilon^{7/3}p^{4/3}
\]

without additional phase, polarization, or flux hypotheses.  The exact
frozen one-carrier calculation is therefore used as a method screen, not as
a general cascade theorem.

The literature on enhanced dissipation supplies methods and comparison
scales for the next dissipative step.  It does not directly control the
absolute bounded-variation functional
\(\int|u u'|\), so citing semigroup decay cannot close R0.72N.

## Safe public wording

> R0.72M proves an exact action danger window and a sharp logarithmic cubic
> law in a complete one-carrier zero-diffusion reference.  That reference
> lies in the action-poor safe branch.  The corresponding dissipative
> action/enstrophy comparison and cubic upper bound remain open.

Unsafe wording includes:

- arbitrary strong coupling is closed;
- enhanced dissipation automatically proves the logarithmic cubic law;
- the frozen chain is a Navier--Stokes solution;
- a finite diagnostic is a full-lattice certificate;
- the Clay problem is solved or reduced to an existing theorem.
