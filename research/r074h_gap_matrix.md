# R0.74H evidence and gap matrix

The status labels in this matrix have the following meanings.

- **PROVED**: established analytically in the R0.74H derivation, possibly
  using an explicitly identified inherited theorem.
- **FINITE**: checked by exact finite arithmetic only; not an analytic proof.
- **OPEN**: not established by R0.74H.
- **NOT CLAIMED**: deliberately excluded from the release claim set.

The analytic source audited here has SHA-256

    14ec43c55d833ea498d9ccd1a9e4514b015d8db41194615360af7376ccc433fe.

| ID | Claim | Evidence | Status | Boundary |
|---|---|---|---|---|
| H1 | The terminally anchored Version-M and Version-F fields satisfy the displayed moving-frame equations and share the periodic pressure source identity. | R0.74H (1.2)--(1.5a), inherited R0.74E transformation algebra | **PROVED** | Smooth periodic unforced solutions only; Version F retains its constant acceleration force. |
| H2 | The finite periodized shell weights converge in \(C^2(\mathbb T^3)\), and unfolding recovers the complete lifted shell sum. | R0.74H (2.3)--(2.7), lattice counting and super-Gaussian summability | **PROVED** | Depends on the frozen super-Gaussian weights and the stated padded shell cutoffs. |
| H3 | The finite-shell weighted energy identities hold in both frames, including the residual Version-M drift, pressure flux, and Version-F acceleration moment. | R0.74H (3.1)--(3.7) | **PROVED** | Classical smooth integration by parts; no weak-solution passage is included. |
| H4 | The time-cutoff and Laplacian-cutoff quadratic row obeys \(\mathfrak Q_R^\alpha\lesssim(P_{0,R}^\alpha)^{2/3}\). | R0.74H (4.1)--(4.8) | **PROVED** | Uses weighted Holder, shell-volume summability, radius shift, and the frozen local/exterior cubic ledger. |
| H5 | The Version-F acceleration contribution is already paid linearly after the outer \(2/3\) power. | R0.74H (3.7), (5.4), and definition (1.11) | **PROVED** | This does not remove the acceleration or reinterpret it as periodic pressure. |
| H6 | Adding the positive cumulative collar flux linearly gives \(X_R^\alpha\lesssim(P_R^\alpha)^{2/3}+\mathfrak C_R^\alpha\). | R0.74H Theorem 5.1, equations (5.1), (5.1a), and (5.1b) | **PROVED** | The flux is tied to the same weighted energy identity; it is not independently payable. |
| H7 | The corrected payment \(\widehat P_R^\alpha=P_R^\alpha+(\mathfrak C_R^\alpha)^{3/2}\) yields \(X_R^\alpha\lesssim(\widehat P_R^\alpha)^{2/3}\). | R0.74H (5.2)--(5.5) | **PROVED** | Identity-level repair only; it is not an epsilon-regularity criterion. |
| H8 | The absolute collar flux is bounded by the existing pre-acceleration ledger: \(\sup|\mathfrak F_R^M|\lesssim P_R^M\), \(\sup|\mathfrak F_R^F|\lesssim P_{0,R}^F\). | R0.74H Lemma 6.1, equations (6.1)--(6.6) | **PROVED** | Uses the full velocity-pressure cubic ledger and, in Version M, the residual-drift payment. |
| H9 | Every smooth periodic solution in scope satisfies the two-regime estimates (6.7)--(6.8). | R0.74H Theorem 6.2 from H6 and H8 | **PROVED** | This is an arbitrary-smooth-solution size theorem, not a weak-solution theorem or scale iteration. |
| H10 | If \(P_R^\alpha\le1\), then \(X_R^\alpha\lesssim(P_R^\alpha)^{2/3}\) for both frames. | R0.74H Corollary 6.3, equation (6.9) | **PROVED** | A one-scale size implication only; it does not show that smallness propagates or absorbs another budget. |
| H11 | On the R0.74F--G family, the collar flux reduces exactly to the packet-energy transport by the odd shear. | R0.74H (7.1)--(7.2), using \(p=a_R=a_R'=0\) and the parity cancellations | **PROVED** | Special explicit smooth 2D3C family only. |
| H12 | The explicit family lies in the large-payment regime, with \(P_R\gtrsim B^2LR^2\to\infty\). | R0.74H (7.5a), deduced from Theorem 6.2 and the inherited target lower bound | **PROVED** | No matching lower bound \(P_R\gtrsim B^3R^3\) is asserted; the R0.74G statement \(P_R\lesssim B^3R^3\) remains an upper bound. |
| H13 | The explicit family forces \(\mathfrak C_R\gtrsim B^2LR^2\), hence \(\mathfrak C_R^{3/2}\gtrsim B^3L^{3/2}R^3\). | R0.74H (7.4), (7.6)--(7.8), exact weighted identity | **PROVED** | Lower bound only; no matching upper bound or asymptotic equivalence. |
| H14 | The 25-row exact-arithmetic certificate checks the shell-volume powers, \(3/2\)-to-\(2/3\) compatibility, small-payment exponent ordering, and diagnostic family scales. | `scripts/r074h_collar_flux_certificate.py`, JSON and report | **FINITE** | It does not prove convergence, energy identities, pressure estimates, acceleration control, two-regime closure, or the flux lower bound. |
| H15 | The positive collar flux is controlled by a weaker quantity not already tied to the local energy identity. | No such estimate in R0.74H | **OPEN** | Required before treating the flux as an independently useful regularity budget. |
| H16 | The smooth two-regime theorem extends stably to suitable weak or local-energy solutions. | No compactness, lower-semicontinuity, or moving-trajectory limit theorem | **OPEN** | The cumulative positive flux and terminally anchored path both require a weak-limit analysis. |
| H17 | The small-payment estimate closes a scale iteration or absorption argument. | No iteration theorem in R0.74H | **OPEN** | One-scale smallness does not by itself propagate to smaller scales. |
| H18 | R0.74H gives an epsilon-regularity, continuation, or singularity-exclusion theorem. | No such argument | **OPEN** | The proved result is a size estimate only. |
| H19 | R0.74H proves global smoothness, constructs blow-up, or resolves the Navier--Stokes Millennium problem. | Explicit scope exclusions in Sections 0 and 9 | **OPEN** | **NOT CLAY.** |
| H20 | The flux lower bound has a reverse comparison or a two-sided asymptotic formula on the explicit family. | R0.74H states “No reverse comparison is claimed.” | **NOT CLAIMED** | Only the lower direction (7.7)--(7.8) is proved. |
| H21 | A logarithmic frontier such as \(P^{2/3}\sqrt{1+\log_+P}\) is a theorem of R0.74H. | No logarithmic estimate appears in the analytic source | **NOT CLAIMED** | It remains, at most, a separate scaling-screen candidate. |
| H22 | The R0.74H result is novel, exhaustive, or has publication priority. | Bounded literature comparison only | **NOT CLAIMED** | No exhaustive collision search or priority claim is made. |

## Route decision

R0.74H repairs the frozen large-payment failure at the level of exact smooth
energy accounting and proves that the original \(2/3\) size estimate remains
valid in the small-payment regime.  The next mathematical gate is not a
stronger claim about the same identity-level flux.  It is either an
independent payment for that flux or a stable weak-solution and scale-iteration
bridge.  Until such a bridge is proved, no regularity or Millennium conclusion
follows.

**NOT CLAY.**
