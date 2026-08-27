# R0.72M gap matrix

**Date:** 2026-08-27
**Scope:** the row-aligned one-carrier full Fourier lattice, with the
diagonal passive heat removed only in the analytic benchmark.

| Claim or interface | Status | Exact evidence | Boundary |
|---|---|---|---|
| One-carrier parabolic rescaling gives \(\sigma=\varepsilon\) | Proved | phase rotation and \(y=R^2x\) | fixed one-carrier geometry |
| Zero-diffusion convolution remains full lattice | Proved | \(e^{sB}\) acts on \(\ell^2(\mathbb Z)\) | diagonal heat is removed |
| \(f_n=\sqrt2J_n'(2s)\) | Proved | Bessel recurrence | declared launch only |
| \(\sum n^2|f_n|^2=1+s^2\) | Proved | exact generating function and Parseval | frozen chain |
| \(K_{\rm fr}\asymp\sigma^2\) | Proved | evaluate at \(y=1\) with fixed background | benchmark enstrophy, not dissipative PDE |
| Complete frozen action is \(A_0\sigma^{-2/3}\log\sigma\) before the lift | Proved | stationary-phase \(H^{-1}\) bound, change of variables, dominated convergence | fixed positive target diagonal |
| Lifted action is \(\asymp\sigma^{4/3}\log\sigma\) | Proved | inherited \(\Theta\asymp\sigma^2\) | zero-diffusion reference |
| Frozen true cubic is \((16/\pi^2)a^2\log\sigma+O(a^2)\) | Proved | fixed-order Bessel asymptotics and periodic mean | frozen diagonal only |
| Exact superlevel set of \(\min\{U,Vx\}/(K+x)\) | Proved | two monotone rational branches | scalar ledger only |
| Frozen chain enters the optimized \(U\)-branch | Disproved | \(x/H\to0\) | family actually stays on \(Vx\)-branch |
| Frozen scalar cubic ratio decays | Proved | \(Vx/K\asymp\sigma^{-1/3}\log\sigma\) | zero-diffusion one carrier |
| Sublinear cubic branch occurs | Proved in benchmark | cubic divided by \(\sigma a^2\) tends to zero | one carrier, row-aligned launch |
| Dissipative finite solver agrees across two methods | Finite corroboration | refined FFT split and finite-chain Cayley split | binary64; no interval enclosure |
| Dissipative cubic is logarithmic | Open | finite data are compatible | needs uniform BV or flux proof |
| Common-band multi-carrier sublinear cubic | Open | no phase-uniform estimate | signed full convolution required |
| Multiscale physical absorption | Open | inherited R0.72L shell moments | no global payment |
| General 3D continuation criterion | Open | no bridge to an accepted endpoint | Clay problem untouched |

## Earliest unresolved implication

The first unavailable statements are either

\[
 \mathcal C_{\rm diss}(\sigma)=o(\sigma a^2)
\]

or

\[
 \sigma^{1/3}x_{\rm diss}=o(K_{\rm diss})
\]

for the exact dissipative one-carrier chain, uniformly as
\(\sigma\to\infty\).  Semigroup decay does not by itself control the
absolute time variation in the first statement or the action/enstrophy
comparison in the second.
