# Independent primary analytic audit of R0.75A

## 0. Frozen object and verdict

Audited file: research/r075a_spectral_persistence_payment_dichotomy.md.
Frozen SHA-256:
f8117a7ff6380676d2ed05e749119579cc3f6972463834dcc6ad2a0b03026388.

**Verdict: PASS. Blocker count: 0. Minor corrections required: 0.**

The moving-cutoff identity, exhaustive dichotomy, spacetime Hölder
normalization, scale-\(2R\) weight, and frozen exponential rate all
recompute correctly.

This update is a **citation/framing rebind only**. The new paragraph after
(A.22) identifies the nested inner-ball/outer-ball heat estimate in
Wang--Wang--Zhang--Zhang, arXiv:1711.04279, Section 3.2, as a methodological
precedent and immediately distinguishes the residual shear, moving
periodic strip, and Version-M weighted cubic payment used here. It is not
invoked as a proof step, changes no hypothesis or formula, and does not
alter the verdict below.

## 1. Geometry and time interval

The frozen reciprocal is

\[
 p=(63/32)^{-1}=32/63,\qquad pL=2^{k_2}.
\]

Thus \(A_{k_2-1}(R)\) has inner and outer radii \(pLR/2\) and \(pLR\).
At the worst outer corner of \(\mathcal S_+(t_2)\), the squared-radius
slack is

\[
 (pLR)^2-|x|^2
 \ge R^2\left(\frac{15}{16}pL-\frac52\right)>0.
\]

The inner margin follows from \(x_3>pLR-R>pLR/2\). The faces of
\(\Omega_0\) are strictly inside those of \(\mathcal S_+\): the normalized
\(x_2\) interval changes from \((20/16,24/16)\) to
\((21/16,23/16)\), while the \(x_3-pLR\) interval changes from
\((-1,-8/16)\) to \((-15/16,-9/16)\). Hence a nested cutoff with
\(R^{-1}\) first derivatives and \(R^{-2}\) second derivatives exists.

For \(t\in[t_2-c_0R^3,t_2]\),
\[
 |Q_2(t)|\le c_0R/96,\qquad Q_2(t)\le0.
\]
After decreasing \(c_0\), \(x_2=z+Q_2(t)\) stays positive and its square
only decreases. The fixed radial buffer is preserved. The inherited
\(O(R^2)\) padding from \(\overline I_R\) to \(I_{2R}\) contains this
\(O(R^3)\) backward interval. Therefore (A.11) legitimately follows from
Z.12a--Z.12b:
\[
 J\subset I_{2R},\qquad
 \mathcal S_+(t)\subset A_{k_2-1}(R)=A_{k_2-2}(2R).
\]

The strip volume is exactly
\[
 \left(\frac12\sqrt{pL}R\right)
 \left(\frac14R\right)\left(\frac12R\right)
 =\frac1{16}\sqrt{pL}\,R^3.
\]

## 2. Shear and local-energy identity

The platform estimate on the calibration interval gives
\[
 D_1\ge64(1-\varepsilon_1)R^2,\qquad
 B=\frac1{2D_1}
 \le\frac1{128(1-\varepsilon_1)R^2}
 \le\frac1{96R^2}.
\]
The bound \(D_1\le64R^2\) also gives \(B\ge1/(128R^2)\), so (A.8) is
correct.

With \(z=x_2-Q_2(t)\) and \(c=b-Q_2'\), the chain rule gives
\[
 \partial_t\widetilde F=\Delta_{z3}\widetilde F-c\partial_z\widetilde F.
\]
Multiplication by \(\phi\widetilde F\) yields exactly
\[
 \frac12E'+\int\phi|\nabla_{z3}\widetilde F|^2
 =\frac12\int(c\partial_z\phi+\Delta_{z3}\phi)|\widetilde F|^2.
\]
The transport sign is plus because
\[
 -\int\phi c\widetilde F\partial_z\widetilde F
 =\frac12\int c\partial_z\phi|\widetilde F|^2,
\]
using that \(c\) is independent of \(z\).

Localizing in \(x_1\) is sound: \(F\) is \(x_1\)-independent, the passive
operator contains only \(\Delta_{23}\), and no \(x_1\) integration by
parts occurs. The \(x_1\) cutoff contributes only the \(\sqrt L R\)
volume factor.

Since \(|b|+|Q_2'|\le2B\le1/(48R^2)\),
\[
 |c\partial_z\phi|\le(C_\phi/48)R^{-3}.
\]
Also \(|\Delta_{z3}\phi|\le C_\phi R^{-2}\le C_\phi R^{-3}\) for
\(R\le1\). Thus the \(R^{-3}\) error in (A.21)--(A.22) is correct and
needs no plateau-mismatch estimate.

## 3. Exhaustive dichotomy

Let \(E_*=E(t_2)\), \(X=\int_JM(t)\,dt\). Because
\(0\le\phi\le1\) and \(\operatorname{supp}\phi\subset\mathcal S_+\),
\(E(t)\le M(t)\).

If \(E(t)\ge E_*/2\) throughout \(J\), then
\[
 X\ge(c_0/2)E_*R^3.
\]
Otherwise some \(t_0\in J\) has \(E(t_0)<E_*/2\), and integrating
\(E'\le K_\phi R^{-3}M\) gives
\[
 X>E_*R^3/(2K_\phi).
\]
These cases are exhaustive, so \(X\ge c_1E_*R^3\). No favorable
Dirichlet term has been discarded with the wrong sign.

## 4. Hölder, weight, and powers

The spacetime measure satisfies
\[
 |J|\sup_t|\mathcal S_+(t)|\le C L^{1/2}R^6.
\]
Therefore
\[
 \int_J\int_{\mathcal S_+(t)}|F|^3
 \ge\frac{X^{3/2}}{(CL^{1/2}R^6)^{1/2}}
 \ge cE_*^{3/2}R^{3/2}L^{-1/4}.
\]
Here \(X^{3/2}\) supplies \(R^{9/2}\), while the volume square root
supplies \(R^3L^{1/4}\).

On
\(A_{k_2-1}(R)=A_{k_2-2}(2R)\),
\[
 W_{2R}\ge\gamma_{k_2-2}
 =\gamma_{k_2-1}^{1/4}=\omega^{1/4}.
\]
Since \(|u|^3=(F^2+b^2)^{3/2}\ge|F|^3\), the exterior row gives
\[
 P_R^M\ge
 c\omega^{1/4}E_*^{3/2}R^{-1/2}L^{-1/4}.
\]
Using \(E_*\ge2Rh_{\rm rem}/\omega\) yields
\[
 P_R^M\ge
 ch_{\rm rem}^{3/2}R\omega^{-5/4}L^{-1/4},
\]
and hence
\[
 (P_R^M)^{2/3}\ge
 ch_{\rm rem}R^{2/3}\omega^{-5/6}L^{-1/6}.
\]
Every \(R,L,\omega\) power in (A.28)--(A.31) is correct.

## 5. Exponent and claim audit

With
\(\omega=\exp[-(c_\gamma/4)L^2]\) and
\(\log(1/R)=(\rho/4)L^2\), the exponential rate is
\[
 \frac5{24}c_\gamma-\frac\rho6
 =\frac5{24}\frac8{3969}-\frac16\frac9{10000}
 =\frac{64279}{238140000}>0.
\]
There is no remaining persistence fraction. The drop case covers critical
and shorter smooth endpoint focusing for the stated W remote kinetic
witness.

The main file correctly restricts the conclusion to the exact smooth
common-shear family, its total passive first component, and a
positive-volume endpoint core. It does not turn a strip lower bound into a
whole-shell upper bound, does not upper-bound the completed clock, and
does not prove fixed deletion or any statement for arbitrary suitable weak
solutions.

The theorem is phrased for finite correction families although the local
identity applies to any smooth periodic \(F\) solving the same equation.
This is a harmless restriction, not an overclaim. The fixed
\(\sqrt p\) factor is legitimately absorbed into the absolute constant.

\[
\boxed{
\begin{gathered}
\textbf{ANALYTIC VERDICT: PASS;}\\
\textbf{BLOCKERS: 0;}\\
\textbf{MINOR CORRECTIONS REQUIRED: 0.}
\end{gathered}}
\]

This audit makes no novelty determination and proves no Navier--Stokes
regularity or singularity result. \(\mathbf{NOT\ CLAY}\).
