# R0.71J primary-source audit — what all-shell telescoping already means in the literature

**Date:** 2026-08-26

**Scope:** smooth coarse-graining and Germano telescopes, Littlewood--Paley
energy flux, shell-to-shell transfer, positive/absolute flux, smooth frames,
heat-flow/tent-space closure, and critical Navier--Stokes continuation
criteria.  The audit asks whether any source already proves an unconditional
Leray-level estimate for

\[
 \sum_{j,Q}K_j^{-2}\int z_{j,Q}^+
 \mathcal J_{j,Q}^+dt
 \tag{0.1}
\]

with the complete R0.71I source and face ledger.

## Claim-to-source ledger

| Material claim checked | Primary source and visible evidence | Scope match / collision risk | R0.71J boundary |
|---|---|---|---|
| Smooth filters admit nonnegative multiscale band energies and a flux-difference telescope. | G. L. Eyink and H. Aluie, *Localness of energy cascade in hydrodynamic turbulence, I. Smooth coarse-graining* (2009), [arXiv:0909.2386](https://arxiv.org/abs/0909.2386), especially the multiscale Germano construction and band budgets (13). | Direct collision with any claim of a first smooth all-band energy hierarchy or first ordinary flux telescope. | R0.71J claims neither.  Its variable is a normalized projected-Lamb quotient after shellwise positive parts. |
| Signed transfer can decorrelate while absolute transfer is immune to cancellation. | Eyink--Aluie (2009), [author/arXiv HTML](https://arxiv.org/html/0909.2386v1), discussion of mean absolute versus signed flux in Section III.C. | Strong conceptual precedent for the loss of cancellation after an absolute value or positive part. | The exact identity (3.1) is specific to the R0.71I scalar evolution and proves the remaining defect rather than importing a turbulence scaling law. |
| Filtered stresses at different levels satisfy exact algebraic identities. | M. Germano, *Turbulence: the filtering approach*, J. Fluid Mech. 238 (1992), [DOI](https://doi.org/10.1017/S0022112092001733). | Direct collision with any claim that filter nesting or the Germano identity is new. | Linear filter identities do not control per-shell denominators, \(Y_t/Y\), or \(z^+\mathcal J^+\). |
| Littlewood--Paley energy flux has classical commutator representations and critical Besov estimates. | A. Cheskidov, P. Constantin, S. Friedlander, R. Shvydkoy, *Energy conservation and Onsager's conjecture for the Euler equations*, [arXiv:0704.0759](https://arxiv.org/abs/0704.0759), [Nonlinearity DOI](https://doi.org/10.1088/0951-7715/21/6/005); P. Constantin, W. E, E. Titi, [Comm. Math. Phys. DOI](https://doi.org/10.1007/BF02099744). | Standard LP commutator/flux cancellation is not a new mechanism.  The estimates use Besov regularity. | Such regularity is an extra hypothesis, not a consequence of the Leray energy inequality or of the target BV estimate. |
| Mode-to-mode and shell-to-shell triadic energy transfer have a long formal literature. | G. Dar, M. K. Verma, V. Eswaran, *A new approach to study energy transfer in turbulence*, [arXiv:physics/0006012](https://arxiv.org/abs/physics/0006012). | Pairwise transfer antisymmetry and shell-transfer notation are not new. | Even exact antisymmetry gives \(\tau^++(-\tau)^+=|\tau|\) after positive parts; it does not pay (0.1). |
| Scale locality is not an unconditional property of arbitrary NSE solutions. | H. Aluie and G. L. Eyink, *Localness ... II. Sharp spectral filter*, [arXiv:0909.2451](https://arxiv.org/abs/0909.2451), [Phys. Fluids DOI](https://doi.org/10.1063/1.3266948). | Locality conclusions depend on inertial-range scaling assumptions. | Cascade locality cannot be inserted as a Leray-level theorem in R0.71J. |
| Smooth frame and atomic decompositions are classical linear harmonic analysis. | M. Frazier and B. Jawerth, *A discrete transform and decompositions of distribution spaces*, J. Funct. Anal. 93 (1990), [DOI](https://doi.org/10.1016/0022-1236(90)90137-A). | Smooth square partitions, frame reconstruction, and sequence norms are established tools. | The new calculation, if any, must come from the nonlinear normalized NSE quantity, not from the existence of a frame. |
| Heat-flow Carleson/tent control yields a small-data global NSE theory. | H. Koch and D. Tataru, *Well-posedness for the Navier--Stokes equations*, Adv. Math. 157 (2001), [author PDF](https://math.berkeley.edu/~tataru/papers/nas.pdf), [DOI](https://doi.org/10.1006/aima.2000.1937). | Direct precedent for critical heat-extension and Carleson norms, but in a small \(BMO^{-1}\) data class. | Importing this norm would make the route conditional; R0.71J does not derive it from Leray energy. |
| Critical Besov continuity/jump conditions imply regularity. | A. Cheskidov and R. Shvydkoy, *On the regularity of weak solutions of the 3D Navier--Stokes equations in \(B^{-1}_{\infty,\infty}\)*, [arXiv:0708.3067](https://arxiv.org/abs/0708.3067), [J. Stat. Phys. DOI](https://doi.org/10.1007/s00205-009-0265-2). | A known continuation interface with explicit extra shell-amplitude assumptions. | Those assumptions cannot be reused as proof of the unconditional weighted-BV target. |
| Weak all-scale energy balances can retain a defect. | J. Duchon and R. Robert, *Inertial energy dissipation for weak solutions of incompressible Euler and Navier--Stokes equations*, Nonlinearity 13 (2000), [DOI](https://doi.org/10.1088/0951-7715/13/1/312). | Warns against assuming that an infinite-scale limit telescopes without a defect. | R0.71J remains classical/finite before limits and explicitly leaves the Leray/soft/frame-cell passage open. |
| Static divergence-free fields can have persistent positive LP flux across large shells. | J. Burczak and G. Sattig, *Anomalous Energy Flux in Critical \(L^p\)-Based Spaces*, J. Fourier Anal. Appl. 29 (2023), [DOI](https://doi.org/10.1007/s00021-023-00770-2). | Refutes a purely LP-algebraic expectation that every positive flux must vanish after an all-shell organization; the constructed field is not an NSE trajectory. | R0.71J uses a genuine global-smooth NSE family for its own quotient, so it does not rely on this static example. |

## Reconciliation

Three statements are safe.

1. Ordinary smooth-frame energy decomposition and signed flux telescoping are
   established mathematics and are not a novelty claim here.
2. The closest literature itself separates signed cancellation from
   absolute/positive flux.  That distinction is consistent with the exact
   positive-defect identity proved in R0.71J.
3. Known heat-tent, Besov, locality, or energy-equality closures introduce
   regularity, scaling, smallness, or summability assumptions beyond the
   Leray energy inequality.  Reusing them would give a conditional route.

The bounded search found no source proving (0.1) with the complete
projected-Lamb acceleration \(N\), localized-direction acceleration \(M\),
enstrophy normalization \(Y_t/Y\), soft zero faces, matched moving cells,
collars, and refresh atoms.  This is a bounded negative finding, not proof of
originality or nonexistence.

## Search record and stopping reason

The search used exact paper titles, author pages, arXiv records, journal DOI
pages, and targeted combinations of “smooth coarse-graining,” “Germano,”
“Littlewood--Paley energy flux,” “shell-to-shell transfer,” “absolute flux,”
“heat flow Carleson,” and “Navier--Stokes Besov regularity.”  Follow-up reads
checked the claims most likely to collide with R0.71J: the multiscale energy
telescope, signed-versus-absolute cancellation, and conditional critical
closures.

The search stopped because each material claim slot had a primary source or
an explicit gap, later results repeated the same interfaces, and no further
targeted query was likely to change the claim boundary without access to a
formal MathSciNet/zbMATH citation graph and expert novelty review.
