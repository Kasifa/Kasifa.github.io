# R0.74L — independent analytic audit of the main-collar proof

## Binding and verdict

The independent reconstruction audited these exact source objects:

| File | SHA-256 |
|---|---|
| r074l_problem_freeze.md | 8d68f64afe53a45859c29a6e89e18725ec10ab8820ec756c0389645afcd26e28 |
| r074l_forward_bridge_bv_reduction.md, pre-promotion audited text | 33f7cac1ca1c2923fddce8ded1c5a3090a7d8d9125107bb6b0e5b57e7451de8e |

Verdict: **PASS.**  No substantive mathematical flaw or scale error was
found.  One earlier sentence incorrectly suggested that the \(n_3\)-lift
disjointness was unnecessary for the periodized slice bound.  The source
was corrected to use at most one nonzero \(n_3\)-lift and was then
re-audited successfully.

The later status-only promotion edits do not alter any displayed proof
formula.  The release manifest must bind the final promoted source hash
separately.

## Per-lemma reconstruction

| Row | Independent check | Verdict |
|---|---|---|
| A1 | Jensen contributes \(R^6K_T^2\), and \(u=z+\mathfrak S\) gives exactly \(M(Q-\mathfrak S+u,h+y)\). | PASS |
| A2 | Real-to-torus folding retains all kernel windings and all collar copies.  The \(n_2\)-sum unfolds, while at most one \(n_3\)-lift is active for a fixed torus \(x_3\). | PASS |
| A3 | The pointwise chord bound is \(O(L)\).  The \(R/16\)-thickened spherical collar projects to planar area \(O((LR)R)\), including tangency, hence its slice integral is \(O(LR)\). | PASS |
| A4 | \(C_{\rm pr}=65/63\) is valid, and an interval of length \(65/64<2\pi\) meets at most two periodic clock-support components of total length \(O(LR)\). | PASS |
| A5 | Symmetric periodic heat-kernel cylinder densities give the integrated bridge reversal (3.3). | PASS |
| A6 | Reversing \(t-s\) to \(s\) yields \(Q-\mathfrak S^\leftarrow=q_{\rm pre}+B\int_0^t\theta(s,h+X_s)\,ds\). | PASS |
| A7 | The good-event horizon is \(66R^2\) for generator \(\partial_x^2\), so the reflection denominator is \(264R^2\).  Both plateau endpoints retain \(32R\) clearance. | PASS |
| A8 | The bad-path exponent is \(A=4876875/1476395008\), with \(A-\rho=1315703/7381975040>0\), and the bad row scales as \(LR^5\). | PASS |
| A9 | The clipped clock equals the true clock on the good event.  Changing variables before dropping the good-event indicator is legitimate by nonnegativity. | PASS |
| A10 | The inverse-clock entry satisfies \(\{\sigma_\nu\le r\}=\{\widehat q(r)\ge a_\nu\}\); a component traversal lasts \(O(LR^3)\). | PASS |
| A11 | Strong Markov at the entry time and domination by a deterministic \(O(LR^3)\) interval yield modulus failure probability \(4e^{-c/(LR)}\). | PASS |
| A12 | Small oscillation permits the fixed thickened slice.  Its complement costs only \(CL^2R e^{-c/(LR)}\), so clock occupation is \(O(LR)\). | PASS |
| A13 | \(R^6B^{-1}R^{-1}R^{-3}(LR)\le CLR^5\) because \(B^{-1}\le128R^2\). | PASS |
| A14 | The positive packet gives (F.7); inversion, oddness of \(\theta\), and the inherited radial/even cutoff give the negative packet.  Then \(|F|^2\le2(|F^+|^2+|F^-|^2)\). | PASS |

## Promotion boundary

The audit supports promotion of

\[
 \sup_{\tau\in I_R}\mathscr B_j(\tau)\le C LR^5
\]

and its absolute main-target-collar consequence
\(C\Gamma_jLR^5\) from candidate to proved.

It does not audit or prove:

- nearest inward positive shear expulsion;
- the full signed packet estimate R0.74K (4.3);
- a matching upper bound for \(\mathfrak C_j\) or \(X_j\);
- a novelty or priority claim; or
- any universal endpoint, regularity, singularity, or Clay statement.

**NOT CLAY.**
