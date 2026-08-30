# R0.73L problem freeze: parameter-uniform nonselfadjoint adiabatic tracking

**Status:** contract fulfilled; continuum proof, independent analytic audit,
and adversarial audit PASS, with the exact open boundary in Section 6 retained

**Slow window:** \(0\le d\le D_*:=1/450\)

**Operator row:** \((\beta,\xi,\gamma)=(0,0,1/2)\)

## 0. Direct decision

R0.73K proves a uniformly conditioned, algebraically simple viscous branch
\(\lambda_\varepsilon(d)\) and a uniformly controlled frozen complement.
R0.73L asks whether the exact non-autonomous evolution follows that branch
for the full fast time \(D_*/\varepsilon\), with a multiplicative constant
that stays bounded as \(\varepsilon\downarrow0\).

The theorem may not be obtained by integrating the instantaneous eigenvalue
and declaring the remaining factor harmless.  R0.73I records finite-dimensional
counterexamples in which a Jordan block creates an unbounded prefactor.  The
present proof must use the rank-one branch, its uniform conditioning, and a
genuine relative decay estimate for the moving complement.

## 1. Frozen variables

On \(H=L^2(\mathbb T_{2\pi})\), let

\[
 B_\varepsilon(d)=\widetilde A(d)-\varepsilon L,
 \qquad D(B_\varepsilon(d))=H^2_{\rm per},
 \qquad 0<\varepsilon\le\varepsilon_K,
 \tag{1.1}
\]

where \(L=-\partial_x^2+1/4\) and

\[
 W_d(x)=-\frac12e^{-d}\sin x+\frac14e^{-4d}\sin2x.
 \tag{1.2}
\]

The fast and slow equations are equivalent:

\[
 \partial_\theta u=B_\varepsilon(\varepsilon\theta)u,
 \qquad
 \varepsilon\partial_d u=B_\varepsilon(d)u,
 \qquad d=\varepsilon\theta.
 \tag{1.3}
\]

Let \(U_\varepsilon(d,s)\) denote the slow-time evolution, so the physical
selected gain at fast time \(D/\varepsilon\) is

\[
 G_\varepsilon(D)
 :=\|U_\varepsilon(D,0)h_\varepsilon(0)\|,
 \qquad h_\varepsilon(0)\in P_\varepsilon(0)H,
 \quad \|h_\varepsilon(0)\|=1.
 \tag{1.4}
\]

Define the viscous and inviscid actions

\[
 \Phi_\varepsilon(d,s)
 :=\frac1\varepsilon\int_s^d\lambda_\varepsilon(r)\,dr,
 \qquad
 \mathcal A_0(D):=\int_0^D\lambda_0(r)\,dr.
 \tag{1.5}
\]

All selected eigenvalues in this section are real.

## 2. Inherited constants and hypotheses

After decreasing \(\varepsilon_K\) if needed, R0.73K gives constants
\(C_K,K_K,C_\lambda,C_P<\infty\), independent of \(d\) and
\(\varepsilon\), such that

\[
 0.167<\lambda_\varepsilon(d)<0.173,
 \qquad
 \|P_\varepsilon(d)\|<\frac95,
 \qquad
 \|P_\varepsilon'(d)\|\le C_P,
 \tag{2.1}
\]

\[
 |\lambda_\varepsilon(d)-\lambda_0(d)|
 \le C_\lambda\varepsilon,
 \tag{2.2}
\]

\[
 \|e^{tB_\varepsilon(d)}Q_\varepsilon(d)\|
 \le C_Ke^{0.12t},
 \qquad
 \|e^{tB_\varepsilon(d)}\|\le e^{K_Kt}.
 \tag{2.3}
\]

The profile dependence is a bounded drift:

\[
 \|B_\varepsilon(d)-B_\varepsilon(s)\|
 =\|\widetilde A(d)-\widetilde A(s)\|
 \le L_B|d-s|
 \tag{2.4}
\]

for a constant \(L_B\) independent of \(\varepsilon\).  The unbounded
viscous term cancels in this difference.

## 3. Target theorem

R0.73L is successful only if there are
\(\varepsilon_L\in(0,\varepsilon_K]\) and \(C_L\ge1\) such that every
\(0<\varepsilon\le\varepsilon_L\) and every \(D\in[0,D_*]\) satisfy

\[
 C_L^{-1}e^{\Phi_\varepsilon(D,0)}
 \le G_\varepsilon(D)
 \le C_Le^{\Phi_\varepsilon(D,0)}.
 \tag{3.1}
\]

Consequently, after enlarging \(C_L\),

\[
 C_L^{-1}\exp\!\left(\frac{\mathcal A_0(D)}\varepsilon\right)
 \le G_\varepsilon(D)
 \le C_L\exp\!\left(\frac{\mathcal A_0(D)}\varepsilon\right).
 \tag{3.2}
\]

The same constants must yield action-resolved backward localization:

\[
 \frac{\|U_\varepsilon(s,0)h_\varepsilon(0)\|}
      {\|U_\varepsilon(D,0)h_\varepsilon(0)\|}
 \le C_L\exp\!\left[-\frac1\varepsilon
       \int_s^D\lambda_0(r)\,dr\right]
 \tag{3.3}
\]

for \(0\le s\le D\le D_*\).

## 4. Proof obligations

| ID | Obligation | Admissible mechanism |
|---|---|---|
| L1 | existence of exact and Kato-corrected evolution on the common domain | bounded profile drift and bounded \([P',P]\) perturbation |
| L2 | exact Kato intertwining | differentiate \(P U^{\rm a}-U^{\rm a}P\) with the correct commutator sign |
| L3 | moving-complement relative stability | fixed fast-time blocks, frozen complement semigroup, bounded Duhamel drift |
| L4 | \(Q\)-component is \(O(\varepsilon)\) relative to the selected action | forward Volterra equation with the L3 kernel |
| L5 | selected amplitude has upper and lower bounded prefactors | rank-one Kato coordinate and Volterra absorption |
| L6 | transfer from \(\lambda_\varepsilon\) to \(\lambda_0\) | inherited uniform \(O(\varepsilon)\) eigenvalue estimate |
| L7 | backward localization | apply L5 at \(s\) and \(D\), then divide |
| L8 | theorem-boundary and literature audit | primary-source comparison plus explicit open ledger |

## 5. Forbidden shortcuts

- Do not apply a one-parameter adiabatic theorem without proving that its
  constants remain uniform for the singular family \(B_\varepsilon\).
- Do not use a uniform \(H^2\) graph-norm bound for \(P_\varepsilon\), its
  eigenvectors, or their derivatives; none is inherited.
- Do not assume a uniform bound for \(P_\varepsilon''\).  The target proof is
  deliberately organized so that only \(P_\varepsilon'\) is needed.
- Do not infer a non-autonomous complement bound from a spectral gap alone.
- Do not evolve the stable complement backward in time.
- Do not use a Fourier truncation to close any continuum obligation.
- Do not promote (3.2) to a two-term WKB expansion or an explicit prefactor
  limit.

## 6. Exact boundary

Even if L1--L8 close, R0.73L is a linear two-dimensional result for one
certified periodic shear row.  It does not establish nonlinear departure,
transverse three-dimensional instability, a bootstrap to arbitrary smooth
data, finite-time singularity, or the Clay regularity alternative.
