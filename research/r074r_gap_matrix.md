# R0.74R gap matrix — terminal-window coercion and arbitrary-clock extraction

## Scope

This matrix covers R0.74R Step 1, R0.74R Step 2, their finite certificates,
and the bounded primary-literature screen completed on 2026-09-02.  It keeps
separate: analytic proofs, inherited inputs, finite checks, conditional
implications, functional counterexamples, literature boundaries, and open
Navier--Stokes statements.  **NOT CLAY.**

| ID | Statement | Evidence | Status | Exact boundary |
|---|---|---|---|---|
| R1 | The R0.74Q target lobes are measurable, pairwise disjoint, lie in the required weighted doubled-radius annuli, and share the interval \(J=(65R^2-R^3,65R^2)\). | `r074r_persistent_lobe_cubic_packing.md`, (R.102)--(R.107); inherited R0.74Q geometry | INHERITED / PROVED | Frozen chart \(L=(63/32)2^j\), \(R=e^{-L^2/320}\), \(N=j\). |
| R2 | The realized window-averaged lobe energies \(E_\ell\) are detected by the corresponding clock variations: \(v_{k_\ell,R}\ge E_\ell\), hence \(Y_{2,R}^{\rm sf}\ge(\sum E_\ell^2)^{1/2}\). | Step 1, Proposition 2.1, (R.108)--(R.112) | PROVED | Lower bound only; maximizing times may depend on the shell and off-target clocks are not controlled above. |
| R3 | Restricting the nonnegative exterior velocity-cubic row to all lobe cylinders gives \(P_R^M\ge2\sqrt2R\sum\Gamma_\ell^{-5/4}L_\ell^{-1/2}E_\ell^{3/2}\). | Step 1, Proposition 3.1, (R.113)--(R.118) | PROVED | Uses the inherited Version-M exterior row and frozen doubled-radius weights. |
| R4 | Weighted Hölder and the exact reciprocal-weight geometric sum yield \((P_R^M)^{2/3}\ge2^{2/3}(2L)^{-1/3}e^{\kappa_2L^2}U\), \(\kappa_2=8831/1905120>0\). | Step 1, Sections 4--5 | PROVED / FINITE CERTIFICATE | Applies to the Step 1 terminal-window lobe energies, not arbitrary completed clocks. |
| R5 | Bounded normalized payment forces the normalized target distribution exponentially close in \(\ell^1\) to the first lobe. | Step 1, main theorem and corollary | PROVED | First-shell concentration is within the frozen target family; it is not a universal shell theorem. |
| R6 | Step 1 constants, exponent margins, tags, source bindings, deterministic regeneration, and the negative sentinel pass. | `r074r_persistent_lobe_certificate.*`; Step 1 independent audit | FINITE / INDEPENDENT AUDIT | Finite checks do not prove inherited stochastic/PDE inputs. |
| R7 | Every completed shell clock splits as \(K=E+D=Q+F\), with \(D\) nondecreasing, \(K\ge0\), and terminal-inclusive variation controlled by the \(Q,F\) total variations. | Step 2, (R.200)--(R.205); inherited R0.74P | INHERITED / PROVED | At local-energy good times; total variation uses the canonical absolutely continuous representatives. |
| R8 | A large terminal clock has an exact three-way alternative: at least half is accumulated dissipation, or at least one quarter appears as preceding-window averaged kinetic energy, or at least one quarter is recent \(Q/F\) variation. | Step 2, Corollary 2.2, (R.207) | PROVED | Algebraic triage; it does not estimate the dissipation or upcrossing branches at the desired quadratic scale. |
| R9 | For a padded shell and measurable preterminal set \(J\subset(s_R,t_0)\), spatial Hölder gives the cutoff-weighted persistence-to-payment coefficient \(2^k\gamma_k^{1/3}(\Theta^\eta)^{-2/3}\). | Step 2, Proposition 3.1, (R.208)--(R.214) | PROVED | The factor \(\eta_R^{3/2}\) makes the estimate valid on the full cutoff interval; on \(I_R\) it reduces to the unweighted row.  The stronger hard-annulus \(\gamma^{5/6}\) coefficient is not used here. |
| R10 | Hölder across shells cubes that coefficient to \(2^{3k}\gamma_k\Lambda_k^3(\Theta_k^\eta)^{-2}\), while all selected shell payments remain bounded by the complete Version-M payment. | Step 2, (R.211), (R.215) | INHERITED / PROVED | The selected time sets may depend on \(k\); the coefficient sum itself is not shown finite for arbitrary solutions. |
| R11 | If, outside at most \(N_0\) terminal exceptions and at every good \(\tau\in(s_R,t_0)\), clock-to-endpoint errors are quadratically summable and the persistence coefficients obey (R.217), then the all-time best-terminal tail and fixed-scale inequality (Q.1) follow. | Step 2, Theorem 4.1, (R.216)--(R.220) | PROVED IMPLICATION / CONDITIONAL INPUT | Good-time bounds extend to all terminal times by coordinatewise continuity of the canonical clocks and lower semicontinuity of the nonnegative best-\(N_0\) tail.  \(N_0,C_q,C_*\) must be universal; their existence is not proved. |
| R12 | Completed-clock algebra alone cannot force a kinetic window. | Step 2, Proposition 5.1 | PROVED ABSTRACT WITNESS | Scalar smooth clock model; not a Navier--Stokes solution. |
| R13 | A fixed endpoint slice can have arbitrarily small time thickness and spacetime cubic mass. | Step 2, Proposition 5.2 | PROVED FUNCTIONAL WITNESS | Smooth divergence-free time spike; not a Navier--Stokes solution. |
| R14 | A fixed amount of gradient dissipation cannot be bounded below by velocity-cubic mass using only a functional inequality. | Step 2, Proposition 5.3 | PROVED FUNCTIONAL WITNESS | Smooth high-frequency divergence-free fields; not a Navier--Stokes evolution. |
| R15 | Step 2 rational constants, exponent ledgers, terminal-inclusive variation, cutoff-weighted full-interval scope, all-time-tail closure sentinels, tags, deterministic regeneration, and a negative exponent mutation pass. | `r074r_arbitrary_clock_gate_certificate.*` | FINITE / PRIMARY AUDIT | The certificate does not prove local-energy identities, inherited support sums, lower semicontinuity, or the conditional hypotheses. |
| R16 | Suitable weak Navier--Stokes dynamics universally construct \(S_\tau,q_k,\Lambda_k,J_k\) satisfying (R.216)--(R.217). | None | OPEN / NOT CLAIMED | This is the exact arbitrary-clock extraction gap. |
| R17 | Dissipation-dominated terminal clocks can be paid or reduced to finitely many exceptions at scale \((P_R^M)^{2/3}\). | None | OPEN / NOT CLAIMED | The functional no-go prevents a proof from using Sobolev/Hölder alone; a dynamical mechanism is required. |
| R18 | Recent positive clock upcrossings admit an all-shell signed stopping-time bound at the square-function scale. | None | OPEN / NOT CLAIMED | Absolute total variation only gives the already-known \(\ell^1\) ledger.  Leakage, backscatter, and sign cancellation remain unresolved. |
| R19 | Mature literature proves singularity-centred all-late-time \(L^3\) concentration under singular-point or Type-I hypotheses. | Neustupa (2013); Barker--Prange (2020, 2021) | LITERATURE-ESTABLISHED / DIFFERENT HYPOTHESES | These results do not start from arbitrary prescribed-centre completed clocks and do not yield (R.216)--(R.217). |
| R20 | Recent preprints rigorously isolate finite-chain signed work or endpoint-atom pressure response. | Yu, arXiv:2606.25322v1; Huang, arXiv:2608.30715v1 | PRIMARY PREPRINT / ADJACENT | Neither preprint supplies the arbitrary-clock observability/persistence packing.  Peer review not established. |
| R21 | The bounded literature screen found an identical completed-clock persistence-packing theorem. | `r074r_primary_literature_boundary.md` | FINITE NON-HIT | A finite non-hit is not evidence of novelty, priority, or correctness. |
| R22 | The unconditional fixed-scale inequality \(\mathfrak C_R^M\le C[(P_R^M)^{2/3}+Y_{2,R}^{\rm sf}]\) holds for arbitrary suitable weak solutions. | None | OPEN | Step 2 proves only a sufficient conditional theorem. |
| R23 | R0.74R supplies scale contraction, a nested good-scale sequence, regularity, singularity formation, or a Clay alternative. | None | OPEN / NOT CLAIMED | Additional PDE and iteration inputs remain absent. **NOT CLAY.** |

## Route consequence

Step 1 has closed the convex-payment side for a terminal window: any broad
target distribution is exponentially expensive.  Step 2 has shown exactly
why that result cannot simply be evaluated at an arbitrary terminal clock:
the missing information is split between endpoint kinetic comparability,
time thickness, accumulated dissipation, and recent signed upcrossing.

The next theorem should not attempt another abstract \(\ell^1\)-to-\(\ell^2\)
compression.  It should instead target either a stopping-time signed-work
identity that retains leakage/backscatter, or a dynamical dissipation-to-
persistence alternative.  Until one of those bridges is proved, (Q.1),
regularity, and the Millennium problem remain **OPEN**.  **NOT CLAY.**
