# R0.72X independent analytic audit

**Date:** 2026-08-28

**Audit outcome:** **PASS** for the compact-physical-time all-center graph
theorem, the arbitrary-start exact-family semigroup estimate, the integrated
central-layer estimate, the uniform Bloch-twisted formulation, the strong-row
direct sum, the fixed-margin A1 estimate, and the exact A1--A2--A1
factorization for the periodic representative \(\beta=0\).  **PASS as
negative results** for three deliberately excluded
claims: a prefactor-one exponential at every time gap, uniform fixed-shape A1
hypotheses at the shrinking interface, and strict contraction of every
physical Fourier row.  Forced negative-Sobolev transfer, the complete
linearized subsystem, nonlinear Navier--Stokes closure, and the Clay problem
remain open.

---

## 0. Statement under audit

For

\[
 V_\alpha(S,X)=\alpha^{-3}
 \left[2e^{-\alpha^2S}\sin(\alpha X)
 -e^{-4\alpha^2S}\sin(2\alpha X)\right],
 \qquad 0<\alpha\le1,
\]

the audit checks whether the R0.72W centered-block graph estimate can be
translated to every block whose physical center
\(D_0=\alpha^2S_0\) remains in a fixed compact interval
\(K\Subset\mathbb R\), uniformly in the spatial cell and in the Bloch twist.
It then checks the passage from a strict block contraction to an
arbitrary-start semigroup estimate and to a physical-time integrated bound.

The exact scalar row in physical variables is

\[
 \partial_dv=v_{xx}-i\sigma\varepsilon_c W(d,x)v,
 \qquad
 W(d,x)=\frac12e^{-d}
 \left[-\sin x+\frac12e^{-3d}\sin2x\right],
\]

with \(\alpha=(\varepsilon_c/4)^{-1/5}\),
\(S=\alpha^{-2}d\), and \(X=\alpha^{-1}x\).

---

## 1. Shifted-center compactness audit

At a translated block and spatial-cell center, put
\(D=\alpha^2S_0\) and
\(\theta=\alpha X_0\pmod{2\pi}\).  The constant and linear coefficients
relevant to the R0.72W compactness alternative are

\[
 b=2\alpha^{-2}
 \left(e^{-D}\cos\theta-e^{-4D}\cos2\theta\right),
\]

\[
 a=\alpha^{-1}
 \left(-e^{-D}\sin\theta+2e^{-4D}\sin2\theta\right).
\]

Their simultaneous zero equations are

\[
 e^{3D}\cos\theta=\cos2\theta,
 \qquad
 e^{3D}\sin\theta=2\sin2\theta.
\]

If \(\sin\theta=0\), the only solution is
\((D,\theta)=(0,0)\pmod{2\pi}\).  If
\(\sin\theta\ne0\), eliminating \(e^{3D}\) would require

\[
 4\cos^2\theta=2\cos^2\theta-1,
\]

which is impossible.  Thus the collision is the unique common zero for all
real \(D\).

For

\[
 f=e^{-D}\cos\theta-e^{-4D}\cos2\theta,
 \qquad
 g=-e^{-D}\sin\theta+2e^{-4D}\sin2\theta,
\]

the Jacobian at the common zero is \(\operatorname{diag}(3,3)\), and

\[
 f=3D+\frac32\theta^2
 +O(D^2+|D|\theta^2+\theta^4),
\]

\[
 g=3\theta+O(|D\theta|+|\theta|^3).
\]

Consequently bounded \((a,b)\) forces
\(\theta=O(\alpha)\) and \(D=O(\alpha^2)\).  After taking the canonical
cell residue, both translated centers stay bounded and the limiting phase is
a translate of \(H_3=X^3+6SX\), exactly the model already closed in R0.72V.

**Verdict:** PASS.

---

## 2. Escaping-cell branch and uniformity on compact physical time

On every fixed compact enlargement \(K_T=K+[-T,T]\), exact differentiation
gives

\[
 V_{\alpha,XXX}=O_{K,T}(1),
 \qquad
 V_{\alpha,XXXX}=O_{K,T}(\alpha).
\]

These are precisely the uniform derivative bounds used by the R0.72W
endpoint ledger.  If the lower coefficients escape rather than stay bounded,
that ledger supplies the same coercive alternative.  The preceding
common-zero calculation is the only new bounded branch.  Sequential
compactness therefore rules out failure of one graph constant on any fixed
physical-time compact set.

The compactness restriction is essential: the audit does not claim a
constant uniform as \(D\to+\infty\), where the shear amplitude vanishes.

**Verdict:** PASS with the stated compact-time boundary.

---

## 3. Bloch-twist audit

For a physical Fourier residue \(\beta\), the scaled diffusion is
\((\partial_X+i\alpha\beta)^2\).  The gauge

\[
 w(S,X)=e^{i\alpha\beta X}u(S,X)
\]

converts it to the ordinary Laplacian and changes periodicity to

\[
 w(X+2\pi/\alpha)=e^{2\pi i\beta}w(X).
\]

Cellwise \(H^1_0\) extensions belong to every such twisted global
\(H^1\) space, and their direct sum has constant one.  In the energy
identity the two endpoints have equal modulus, so the twisted boundary term
cancels.  No estimate depends on \(\beta\).

**Verdict:** PASS for uniformTwistedPeriodicGraph at the exact \(A_2\)
family rate.  This step does not extend the later fixed-margin \(A_1\)
black-box estimate to arbitrary twists.

---

## 4. Strict block contraction and arbitrary starts

The uniform shifted graph estimate and the exact energy identity give one
strict contraction \(q_{K,T}<1\) on every block of scaled length \(2T\),
independently of the block center, spatial cell, sign, and twist.  Tiling an
arbitrary physical interval \([d_1,d_2]\subset K\) by full blocks and using
energy contraction on the terminal remainder gives

\[
 \|U_\alpha(d_2,d_1)\|_{2\to2}
 \le q_{K,T}^{\lfloor(d_2-d_1)/(2T\alpha^2)\rfloor}.
\]

Since \(\lfloor y\rfloor\ge y-1\),

\[
 \|U_\alpha(d_2,d_1)\|_{2\to2}
 \le q_{K,T}^{-1}
 \exp\!\left[-\frac{|\log q_{K,T}|}{2T\alpha^2}
 (d_2-d_1)\right].
\]

The factor \(q^{-1}\) cannot be removed: strong continuity gives
\(\|U(d_1+h,d_1)\|\to1\) as \(h\downarrow0\), whereas a positive-rate
prefactor-one exponential is strictly below one at every positive gap.

Summing the squared norm on successive blocks yields

\[
 \int_{d_1}^{d_2}\|v(d)\|_2^2\,dd
 \le \frac{2T\alpha^2}{1-q_{K,T}^2}\|v(d_1)\|_2^2.
\]

Thus the exact-family decay rate is \(\alpha^{-2}=\kappa^{2/5}\), and the
integrated scale is \(\alpha^2=\kappa^{-2/5}\).

**Verdict:** PASS for allStartExactPathSemigroup and
allStartIntegratedA2Scale.  prefactorOneAllGapExponential is FALSE.

---

## 5. Forced-transfer boundary

The semigroup kernel has \(L^1\) time mass \(O(\alpha^2)\).  Young's
inequality therefore gives the stated \(L_d^2L_x^2\)-to-\(L_d^2L_x^2\)
Duhamel estimate, and an \(L_d^\infty L_x^2\) forcing gives an endpoint
\(O(\alpha^2)\) gain.  By contrast, endpoint-concentrated
\(L_d^1L_x^2\) forcing has only the energy-scale \(L^1\)-to-\(L^\infty\)
bound and need not gain \(\alpha^2\).

None of these calculations proves the transfer needed for the coupled
physical system when the forcing is only controlled in \(H^{-1}_x\), nor
does an integrated \(L_d^2\) estimate automatically give an endpoint
estimate.

**Verdict:** PASS for the stated \(L_d^2L_x^2\) convolution estimate and
its explicit forcing-class boundary.  forcedHMinusOneTransfer remains OPEN.

---

## 6. Fixed-margin A1 audit for the periodic representative

For the periodic representative \(\beta=0\), on the physical heat path

\[
 K_*=[-\log2,1-\log2],
\]

fix \(\delta=1/8\).  On
\([-\log2,-\delta]\cup[\delta,1-\log2]\), the critical points have fixed
count, fixed separation, a uniform nonzero Hessian, and a uniform
away-from-critical gradient floor.  All required derivatives are bounded by
compactness.

With fast time \(t=\varepsilon_cd\) and
\(\eta=\varepsilon_c^{-1}\), the time derivative of the shear is
\(O(\eta)\).  If its constant is \(C_\delta\), then
\(C_\delta\eta\le\eta^{3/4}\) for
\(0<\eta\le\min\{1,C_\delta^{-4}\}\), which verifies the cited slowly
varying-shear condition.  The fixed-margin theorem therefore
gives

\[
 \|U(d_2,d_1)\|_{2\to2}
 \le C_\delta e^{-c_\delta\sqrt{\varepsilon_c}(d_2-d_1)}
\]

and an integrated \(O(\varepsilon_c^{-1/2})\) scale, uniformly for
subintervals of either outer segment.  The constants depend on the fixed
margin and are not asserted to survive as \(\delta\downarrow0\).

**Verdict:** PASS for fixedMarginA1EnhancedDissipation.

---

## 7. Shrinking-interface no-go audit

Put \(h_\alpha=T\alpha^2\).  Before the collision the two critical points
satisfy

\[
 x_\pm=\pm\sqrt{2T}\,\alpha+O_T(\alpha^3),
\]

so their separation and the relevant Hessian scale vanish like
\(O(\alpha)\).  After the collision,

\[
 W_x(T\alpha^2,0)
 =-\frac32T\alpha^2+O_T(\alpha^4).
\]

Hence a black-box A1 theorem requiring fixed-radius critical
neighborhoods, fixed Morse constants, and a fixed away-gradient floor cannot
be applied uniformly down to the \(O(\alpha^2)\) interface.  This is a
failure of those hypotheses, not evidence against enhanced dissipation.

The two heuristic local rates both match \(\alpha^{-2}\): before collision,
\((\varepsilon_c\alpha)^{1/2}\asymp\alpha^{-2}\); after collision,
\((\varepsilon_c\alpha^2)^{2/3}\asymp\alpha^{-2}\).  These rate balances
are diagnostics, not separate theorems.

**Verdict:** shrinkingInterfaceFixedShapeA1Hypotheses is FALSE.

---

## 8. Exact A1--A2--A1 factorization

The fixed-margin \(A_1\) input has been audited only for the periodic
representative \(\beta=0\).  The factorization below has that scope.  The
Bloch-uniform result from Section 3 remains available separately for the
exact \(A_2\) family.

For \(T=1/4\), \(\delta=1/8\), and sufficiently small \(\alpha\) so that
\(h=T\alpha^2\le\delta\), the exact evolution factors as

\[
\begin{aligned}
 U(1-\log2,-\log2)
 ={}&U(1-\log2,\delta)U(\delta,h)U(h,-h)\\
 &\times U(-h,-\delta)U(-\delta,-\log2).
\end{aligned}
\]

The two outer factors are controlled by fixed-margin A1, the central factor
by the exact all-center A2 contraction, and the shoulders by energy
contraction or by further all-center blocks.  This gives the fixed-history
terminal estimate

\[
 \|U(1-\log2,-\log2)\|_{2\to2}
 \le C e^{-c\sqrt{\varepsilon_c}}
\]

and an \(O(\varepsilon_c^{-1/2})\) integrated bound from the left endpoint;
the compact range of remaining \(\varepsilon_c\) is absorbed into the
constant.  For this fixed launch, pre-collision A1 plus energy monotonicity
already gives the terminal rate.  The genuinely new R0.72X content is the
arbitrary-start exact A2 semigroup control through the collision layer.

**Verdict:** PASS for exactA1A2A1TimeConcatenation on the periodic
representative \(\beta=0\), with the novelty and Bloch-scope boundaries
stated explicitly.

---

## 9. Fourier normalization, damping, and row sum

Using the unitary Fourier convention on the physical circle makes Parseval
exact.  A scalar damping term \(-\mu G\) contributes
\(e^{-\mu(d_2-d_1)}\) to the norm estimate and its square to the energy
estimate.  Strong rows with a common positive coupling floor therefore sum
in \(\ell^2\) without a row-count loss.

The actual row coupling is

\[
 \varepsilon_j=\frac{2|\delta K_{z,j}|a}{R^2}.
\]

There is no common positive floor over all rows.  In particular, the row
\(K_z=0\), \(\beta=0\), \(\mu=0\) has an exact constant nondecaying mode.
Thus a strict contraction statement for every physical row is false.

**Verdict:** PASS for strongRowDirectSumNoCountLoss.
allPhysicalRowsUniformContraction is FALSE, and
completeLinearizedShearSubsystem remains OPEN.

---

## 10. Numerical diagnostic boundary

The accompanying center scan evaluates finite-resolution transfer norms for
the full exact potential over the full physical heat path, several values of
\(\alpha\), several centers, and several resolution levels.  Its numerical
row uses the periodic representative; sign invariance follows exactly by
complex conjugation, while Bloch-twist uniformity remains an analytic claim
rather than a numerical scan.  The calculation is a reproducible stress test
for implementation errors and adverse centers.  It does not replace the
compactness proof and it does not certify the infinite-dimensional operator
norm.

**Verdict:** PASS as diagnostic evidence only, conditional on the sealed
artifact and deterministic certificate reproducing the recorded hashes.

---

## 11. Final claim ledger

| Claim | Audit status |
|---|---|
| allCenterExactFamilyGraphCoercivity | CLOSED |
| allStartExactPathSemigroup | CLOSED |
| allStartIntegratedA2Scale | CLOSED |
| uniformTwistedPeriodicGraph | CLOSED |
| strongRowDirectSumNoCountLoss | CLOSED |
| fixedMarginA1EnhancedDissipation | CLOSED |
| exactA1A2A1TimeConcatenation | CLOSED |
| shrinkingInterfaceFixedShapeA1Hypotheses | FALSE |
| prefactorOneAllGapExponential | FALSE |
| allPhysicalRowsUniformContraction | FALSE |
| forcedHMinusOneTransfer | OPEN |
| completeLinearizedShearSubsystem | OPEN |
| nonlinearNavierStokes | OPEN |
| Clay regularity problem | OPEN |

The audited result is a rigorous scalar enhanced-dissipation theorem for one
exact collision family on compact physical-time intervals.  It is not a
regularity proof for three-dimensional Navier--Stokes.
