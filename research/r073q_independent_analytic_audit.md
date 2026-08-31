# R0.73Q independent analytic audit

**Audited file:** `research/r073q_heat_flow_stability_proof.md`

**Audit mode:** independent line-by-line reconstruction of the exponents,
Volterra history decomposition, fixed point, continuation bridge, and Fourier
witness; no reliance on the proof author's intended conclusion

**Final verdict:** `PASS_AFTER_TWO_EXPLICIT_REVISIONS`

The first draft had no fatal analytic error.  It required (i) an explicit
Serrin norm bound up to a hypothetical finite maximal time and (ii) a union
of the old and new stable tubes before asserting strict inclusion of the
previously published R0.73P domain.  Both changes are now present in the
audited proof.

## 1. Verdict matrix

| Item | Verdict | Audit conclusion |
| --- | --- | --- |
| Periodic Stokes/Oseen estimate | `PASS` | Short-time exponent \(3/4\) and long-time spectral-gap decay are correct |
| One-dimensional HLS step | `PASS` | \(I_{1/4}:L^2_t\to L^4_t\) is exactly the required endpoint map |
| Product-time exponent | `PASS` | \(L^4_tL^6_x\cdot L^4_tL^6_x\subset L^2_tL^3_x\) |
| Causal interval decomposition | `PASS` | History contains only old-time same-time products; no cross-time factors occur |
| Local inverse and recursion | `PASS` | Local norm \(1/2\), inverse norm \(2\), and the displayed \(K[u]\) are valid crude bounds |
| Quadratic contraction | `PASS` | \(\rho_{\mathfrak X}=1/(8C_BK[u]^2)\) gives ball invariance and contraction factor below \(1/2\) |
| Mild/Serrin/\(H^3\) bridge | `PASS_AFTER_REVISION` | The proof now displays finiteness of \(L^4((t_0,T_*);L^6)\) at a hypothetical endpoint |
| Heat-flow/Besov trace | `PASS` | Mean-zero semigroup characterization has the correct negative index and time measure |
| Exact shear constants | `PASS` | \(c_6=(5/16)^{1/6}\), heat exponent \(-3/4\), and Sobolev exponent \(+1/4\) all recompute exactly |
| Strict comparison with the R0.73P domain | `PASS_AFTER_REVISION` | Strict inclusion is claimed for the union \(\mathcal D_Q\), not by silently ordering unrelated radii |

## 2. Bilinear estimate reconstruction

The periodic heat estimate from \(L^3\) tensors to \(L^6\) vector fields has
short-time exponent

\[
 {1\over2}+{3\over2}\left({1\over3}-{1\over6}\right)
 ={3\over4}.
 \tag{2.1}
\]

For \(g(t)=\|a(t)\|_6\|b(t)\|_6\),

\[
 \|g\|_2\le\|a\|_{L^4L^6}\|b\|_{L^4L^6}.
 \tag{2.2}
\]

The kernel \(t^{-3/4}\) is the one-dimensional fractional-integration
kernel of order \(1/4\), and

\[
 I_{1/4}:L^2(\mathbb R)\to L^4(\mathbb R).
 \tag{2.3}
\]

The long-time kernel belongs to \(L^{4/3}\), for which Young's indices obey

\[
 1+{1\over4}={3\over4}+{1\over2}.
 \tag{2.4}
\]

The output of a periodic divergence has zero mean, so using the spectral gap
at long times is legitimate.

## 3. Volterra reconstruction

On an interval \(I_j=[\tau_{j-1},\tau_j)\), the Duhamel time integral splits
at \(\tau_{j-1}\).  Because both factors in every product are evaluated at
the same integration time, the history is exactly

\[
 h_j={\bf1}_{I_j}\bigl[
 \mathcal B(U_{<j},z_{<j})+
 \mathcal B(z_{<j},U_{<j})\bigr].
 \tag{3.1}
\]

There are no terms \(U_jz_{<j}\) or \(U_{<j}z_j\).  With
\(\varepsilon_B=(4C_B)^{-1}\),

\[
 \|\mathcal L^{I_j}_{U_j}\|\le{1\over2},
 \qquad
 \|(I+\mathcal L^{I_j}_{U_j})^{-1}\|\le2.
 \tag{3.2}
\]

Thus

\[
 Z_j\le(1+4C_BM[u])Z_{j-1}+2\|f_j\|_{E(I_j)}.
 \tag{3.3}
\]

The fourth-power action is additive, so at most

\[
 1+(M[u]/\varepsilon_B)^4
 \tag{3.4}
\]

pieces are needed.  Finite-sequence Hölder then produces the proof's
\(N^{3/4}\) factor.  The recursive construction proves surjectivity; the
same recursion at \(f=0\) proves injectivity.

## 4. Fixed point and continuation reconstruction

If \(R_U=(I+\mathcal L_U)^{-1}\) and
\(\delta=\|e^{t\Delta}w_0\|_E\), the ball radius is

\[
 r=2K[u]\delta.
 \tag{4.1}
\]

Both ball invariance and the Lipschitz estimate reduce to

\[
 4C_BK[u]^2\delta<{1\over2},
 \tag{4.2}
\]

which follows from
\(\delta<1/(8C_BK[u]^2)\).

For smooth initial data, the global fixed point has
\(w\in L^4(t_0,\infty;L^6)\).  If \(T_*<\infty\) were the maximal classical
time, mild uniqueness on compact subintervals would identify the classical
solution with the global fixed point and give

\[
 \|v\|_{L^4((t_0,T_*);L^6)}
 \le M[u]+2K[u]\delta<\infty.
 \tag{4.3}
\]

Since \(2/4+3/6=1\) and \(6>3\), Serrin continuation contradicts finite
\(T_*\).

## 5. Exact strictness witness reconstruction

For

\[
 w_N=N^{-1/4}e_2\sin(Nx_1),
 \tag{5.1}
\]

normalized Haar integration gives

\[
 \|\sin(Nx_1)\|_2={1\over\sqrt2},
 \qquad
 \|\sin(Nx_1)\|_6=\left({5\over16}\right)^{1/6}.
 \tag{5.2}
\]

Therefore

\[
 \|w_N\|_{\mathfrak X}
 ={(5/16)^{1/6}\over4^{1/4}}N^{-3/4},
 \quad
 \|w_N\|_2={1\over\sqrt2}N^{-1/4},
 \quad
 |w_N|_{1/2}={1\over\sqrt2}N^{1/4}.
 \tag{5.3}
\]

The heat-flow ball contains a matched smaller \(H^{1/2}\)-ball by the
continuous embedding, but the audit found no proved ordering between
\(\rho_{\mathfrak X}[u]/C_X\) and the separate R0.73P radius
\(R_{1/2}[u]\).  The corrected stable domain is consequently

\[
 \mathcal D_Q[u]
 =\{f:|f|_{1/2}<R_{1/2}[u]\}
 \cup\{f:\|f\|_{\mathfrak X}<\rho_{\mathfrak X}[u]\},
 \tag{5.4}
\]

and (5.3) proves the strict inclusion of the first set in (5.4).

## 6. Final claim boundary

The audit authorizes the following labels:

```text
periodicOseenHLS=PASS
volterraHistoryDecomposition=PASS
uniformInverseRecursion=PASS
globalEmildFixedPoint=PASS
H3SerrinBridge=PASS
periodicHeatBesovEquivalence=PASS
singleModeExactConstants=PASS
strictExtensionOfPublishedDomainByUnion=PASS
heatBallContainsEntirePublishedH12Ball=NOT_PROVED
uniformL2OnlyStrongRadius=OPEN
nonperturbativeBMOInverseUniqueness=FALSE_IN_GENERAL
clayConclusion=OPEN
```
