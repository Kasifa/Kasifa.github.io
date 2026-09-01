# R0.74I evidence and gap matrix

The status labels in this matrix have the following meanings.

- **PROVED**: established analytically in the R0.74I derivation, possibly
  using an explicitly identified inherited or published theorem.
- **FINITE**: checked by exact finite arithmetic only; not an analytic proof.
- **OPEN**: not established by R0.74I.
- **NOT CLAIMED**: deliberately excluded from the release claim set.

The analytic source audited here has SHA-256

    70ff507704c6c7aed5ea8bc0250a96373113975e8e3f92edd53e3193d7cd8457.

| ID | Claim | Evidence | Status | Boundary |
|---|---|---|---|---|
| I1 | At each fixed \(R>0\), the spatially mollified periodic suitable-weak velocity has a Borel, spatially Lipschitz representative whose terminal Caratheodory problem has a unique absolutely continuous lift. | R0.74I (1.3)--(1.5), energy-class convolution bounds | **PROVED** | Per-solution and fixed-scale statement; no sequence-level path stability is asserted. |
| I2 | The nonnegative terminally moving test \(\eta_R(t)\Theta_{R,N}(x-X_R(t))\) is admissible in the suitable-weak local energy inequality after smooth path approximation. | R0.74I Lemma 2.1; `research/r074i_weak_extension_independent_audit.md` | **PROVED** | Version M only; the test is justified per solution, not by passing a family of trajectories through a compactness theorem. |
| I3 | The moving local-energy inequality has the displayed residual kinetic flux \(\frac12|v_R|^2(v_R-a_R)\), pressure flux, signs, and \(1/(2R),1/R\) factors. | R0.74I (2.2)--(2.4); independent weak-extension audit | **PROVED** | The smooth identity becomes an inequality in the favorable direction. |
| I4 | The R0.74H finite-shell cutoff and absolute-flux estimates require only the suitable-weak integrability ledger and remain valid in Version M. | R0.74I Lemma 2.2; inherited R0.74E/H estimates; independent weak-extension audit | **PROVED** | Uses \(u\in L^3\), \(p\in L^{3/2}\), the distributional pressure split, and the frozen shell weights. |
| I5 | Every periodic suitable weak solution in scope satisfies \(X_R^M\lesssim(P_R^M)^{2/3}+P_R^M\), and the pure \(2/3\) bound follows when \(P_R^M\le1\). | R0.74I Theorem 2.3; independent weak-extension audit | **PROVED** | A one-scale size estimate; it does not itself imply regularity. |
| I6 | Small moving energy bounds the mollified path displacement by \(CR\mathcal E_R^{1/2}\) over the terminal subinterval and places the fixed ball \(B_{R/2}(x_0)\) inside the moving ball \(X_R(t)+B_R\). | R0.74I Lemma 3.1 and (3.4)--(3.5); `research/r074i_epsilon_log_independent_audit.md` | **PROVED** | Depends on the frozen mollifier support and a chosen continuous torus lift. |
| I7 | Moving energy controls the fixed-cylinder cubic velocity quantity by \((R/2)^{-2}\int_{Q_{R/2}(z_0)}|u|^3\lesssim\mathcal E_R^{3/2}\). | R0.74I Lemma 3.2; Guevara--Phuc Lemma 2.6; independent epsilon/log audit | **PROVED** | Purely functional interpolation; it does not use the two-regime theorem. |
| I8 | Sufficiently small \(\mathcal E^{M,R}(z_0,8R)\) implies that \(z_0\) is regular. | R0.74I Theorem 3.3; Wang--Wu--Zhou Theorem 1.1 with \(\delta=1/2\); NSE rescaling (3.11a)--(3.11b) | **PROVED** | Conditional epsilon gate at one given scale; the theorem does not produce the smallness hypothesis. |
| I9 | Sufficiently small \(P_R^M\) implies regularity because \(\mathcal E_R^{3/2}\le P_R^M\). | R0.74I (3.9); nonnegativity of the exterior ledger | **PROVED** | Version M only.  No claim is made for the Version-F acceleration payment. |
| I10 | The exact R0.74F--H family satisfies \(2\rho\le\liminf \log P_j/L_j^2\le\limsup \log P_j/L_j^2\le3\rho\), with \(\rho=1/320\). | R0.74I (4.2)--(4.7); inherited payment upper/lower bounds | **PROVED** | Asymptotic sequence statement with unspecified analytic constants. |
| I11 | For both \(Y_j=X_j\) and \(Y_j=\mathfrak C_j\), \(\liminf Y_j/[P_j^{2/3}\sqrt{1+\log P_j}]>0\). | R0.74I Theorem 4.1; independent epsilon/log audit | **PROVED** | Lower frontier along the realized family; not an endpoint upper estimate. |
| I12 | Every universal payment \(P^{2/3}(1+\log_+P)^\gamma\) with fixed \(\gamma<1/2\) fails for both Version M and Version F. | R0.74I Corollary 4.2 | **PROVED** | Failure is witnessed along a highly lacunary smooth periodic sequence. |
| I13 | A hypothetical endpoint upper estimate at \(\gamma=1/2\) would force the missing matching family bound \(P_j\gtrsim B_j^3R_j^3\). | R0.74I (4.15)--(4.17) | **PROVED** | Conditional implication only; the premise and matching lower bound remain unproved. |
| I14 | The realized payment sequence is lacunary, with \(P_{j+1}/P_j\to\infty\). | R0.74I (4.18), using \(L_{j+1}=2L_j\) | **PROVED** | No pointwise constraint is obtained between successive realized payment values. |
| I15 | The exact certificate checks the NSE cubic scaling, threshold exponents, rational logarithmic window, lacunarity exponent, square-root-log power recovery, and endpoint algebra. | `scripts/r074i_tube_log_certificate.py`, frozen JSON/report, and independent Ruby reconstruction | **FINITE** | Does not prove the moving LEI, path confinement, interpolation, epsilon regularity, inherited packet bounds, or any continuum theorem. |
| I16 | The bounded primary-source comparison locates suitable-weak, one-scale velocity-only, skewed-cylinder, and logarithmic precedents without finding the same observable-level theorem. | `research/r074i_report-source.md` and independent literature audit | **NOT CLAIMED** | A finite non-hit is not a novelty or priority conclusion. |
| I17 | The Version-F two-regime theorem extends to suitable weak solutions. | No weak control of the acceleration row \(a_R'\) in R0.74I | **OPEN** | Version F is deliberately excluded from Sections 1--3. |
| I18 | \(P_R^M\) or \(\mathcal E_R\) is necessarily small at every point or at a possible singular point. | No such estimate in R0.74I | **OPEN** | This is the missing hypothesis needed to use the epsilon gate globally. |
| I19 | The square-root-logarithmic endpoint upper estimate holds universally. | The family screen gives only a positive lower ratio at \(\gamma=1/2\) | **OPEN** | \(1/2\) is the first exponent not rejected, not a proved positive theorem. |
| I20 | Smallness propagates from one moving scale to all smaller moving scales. | No comparison theorem for the scale-dependent trajectories \(X_R\) | **OPEN** | Fixed-cylinder CKN recurrences do not automatically compare distinct moving paths. |
| I21 | The cumulative moving pressure--velocity flux is stable under a suitable-weak approximation sequence. | No sequence-level theorem in R0.74I | **OPEN** | The per-solution fixed-\(R\) theorem does not require this stronger statement. |
| I22 | R0.74I excludes all singularities, proves global smoothness, constructs blow-up, or resolves the Navier--Stokes Millennium problem. | Explicit scope exclusions in Sections 0 and 6 | **OPEN** | **NOT CLAY.** |
| I23 | The exact moving-energy epsilon implication, logarithmic obstruction, or combined release is novel or has publication priority. | Bounded literature comparison only | **NOT CLAIMED** | Requires a broader professional collision and priority review. |

## Route decision

R0.74I closes two gates that were open after R0.74H: Version M now has a
per-solution suitable-weak two-regime theorem, and small moving energy now
enters an established velocity-only epsilon criterion.  The explicit family
also rules out every scalar logarithmic repair below exponent \(1/2\).

The next global obstacle is not the existence of a one-scale epsilon theorem.
It is the derivation or propagation of the required moving-energy smallness at
a possible singular point, together with the unresolved endpoint payment.
Until that obstacle is crossed, no global-regularity conclusion follows.

**NOT CLAY.**
