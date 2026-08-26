# R0.72D claim and gap matrix

**Release:** R0.72D  
**Date:** 2026-08-27

| Claim or route | Decision | Evidence | Boundary |
|---|---|---|---|
| The R0.72C phase-free \(M^{-8/3}\) coefficient may be only an algebraic artifact | Rejected | Shifted Rudin--Shapiro block plus row-aligned data produces an exact target root with slope \(\asymp aM\) | Internal to the triangular 2.5D class |
| A launch endpoint is required to saturate the first-root term | Rejected | A scalar launch adjustment gives an exact simple interior root at \(\tau_M=M^{-3}\) | The root approaches launch as \(M\to\infty\) |
| Spectral translation destroys Rudin--Shapiro phase flatness | Rejected | Prefix bound plus Abel summation is invariant under multiplication by \(z^M\) | Uses a contiguous dyadic block and standard RS signs |
| Unequal heat weights destroy the \(\sqrt M\) multiplier bound immediately | Rejected | Monotone heat weights and Abel summation give \(\|V_M(x)\|\lesssim a\sqrt M e^{-\kappa M^2x}\) | Depends on the common lower carrier scale \(r_j\ge M\) |
| Integrated multiplier exposure for the shifted block | Proved | \(\int\|V_M\|\lesssim aM^{-3/2}\), \(\int\|V_M\|^2\lesssim a^2M^{-1}\) | Constants depend on fixed \(\kappa,K_z\) |
| Critical strong coupling can coexist with bounded Dyson exposure | Proved | \(\delta a=\gamma M^{3/2}\) gives \(\eta\asymp\gamma M^2\) but \(\delta\int\|V_M\|=O(\gamma)\) | \(\gamma\) is fixed and sufficiently small in the root proof |
| Exact interior target root | Proved | Evolution-operator adjustment \(\zeta_M=-P_0U(\tau_M)G_M/P_0U(\tau_M)e_0\) | Finite-support launch data; \(|\zeta_M|=O(M^{-1/2})\) |
| Interior-root slope remains nonzero | Proved | Short-time Duhamel estimate gives \(|P_0V_M(\tau_M)F_M(\tau_M)|\ge caM\) | Large \(M\), fixed small \(\gamma\) |
| The complete root ledger has a genuine lower bound | Proved | One exact atom is nonnegative and belongs to the complete ledger | Additional roots are not counted or excluded |
| Enstrophy contrast can be kept uniform on a fixed physical interval | Proved | Weighted commutator estimate plus matched decoupled low-mode background | Background is included in \(D\) and \(Y\), but not in the target or Lamb vector |
| Full nonlinear rotational charge remains bounded | Proved | Exact identity \(\mathbb P(u\times\omega)=(-vf_z,0,0)\), all-frequency \(\dot H^{-1}\) estimate, and thermal \(L_t^2L_y^\infty\) bound | No target-shell proxy or discarded off-diagonal interactions |
| Nonvanishing normalized complete ledger | Proved | \(\mathcal J_{\rm all}/D^{1/3}\gtrsim\gamma^{4/3}\), \(\Lambda_1\lesssim\nu^2+\gamma^2\) | Positive finite lower constant; not divergence |
| The R0.72C upper scale is dynamically sharp | Proved for this family | Lower and upper ledgers are both order one at \(\eta\asymp M^2\) and \(\ell_\times\asymp M^{-2}\) | Does not prove a universal optimal constant |
| The candidate \(D^{1/3}\Lambda_1\) payment fails | Not established | The normalized ratio stays finite | A divergent family or a proof of a universal ceiling is still needed |
| A universal triangular-class payment theorem | Open | No compactness or structural theorem covers arbitrary carrier geometries and launch data | R0.72D is one exact lower family |
| General 3D Navier--Stokes regularity | Open | The construction is a globally regular invariant 2.5D subclass | No critical-norm bridge or continuation criterion |

## Decision ledger

1. The main positive route is the spectrally shifted RS block, not a new
   enhanced-dissipation estimate.
2. The root is placed at positive time so the result does not rely on a
   left-endpoint atom convention.
3. The low-frequency background is retained in both the data size and
   enstrophy.  It is omitted only from the target response and projected Lamb
   vector, where exact Fourier structure removes it.
4. The full nonnegative ledger is bounded below by one certified root.  No
   assertion is made about the total root count.
5. Static phase flatness, short thermal exposure, row alignment, exact root
   creation, and full-charge payment are all required before the section is
   publishable.
6. One admissible integer \(q=q_0\) is fixed independently of \(M\); hence
   \(t_M=q_0^{-2}M^{-3}\) is positive and lies in every fixed interval
   \([0,T]\) for all sufficiently large \(M\).

## Next finite gate

R0.72E should decide between two alternatives.

1. Construct a supercritical family for which the normalized ratio grows
   beyond the order-one R0.72D scale while \(\Lambda_1\) stays controlled.
2. Prove that the same full rotational charge or another exact NSE identity
   imposes a universal order-one ceiling in the triangular class.

Either route must retain a positive-time exact root, a fixed physical
observation interval, the complete charge, and the true data size.
