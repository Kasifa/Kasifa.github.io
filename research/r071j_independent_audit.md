# R0.71J independent mathematical audit

**Date:** 2026-08-26

**Status:** release-grade adversarial audit of
`research/r071j_report-source.md`.  The audit verifies the hard and soft
positive-defect identities, the fixed parent frame, the exact Fourier
constants, the fixed-window limit, the full-frame scaling argument, the
quantifiers, and the claim boundary.  It is not a peer-review report or an
originality determination.

## 1. Independence design

The release uses two computational paths and one manual proof pass.

1. `research/r071j_exact_audit.py` uses SymPy and the repository's exact
   finite-Fourier primitives.  It produces canonical sorted JSON for the
   hard/soft defect identities, the broad-parent datum, the pure-heat limit,
   and the full-frame creation/heat separation.
2. `research/r071j_independent_audit.py` imports neither the producer nor the
   project Fourier helper.  It uses only the Python standard library.  It
   implements its own curl, convolution, Leray projection, parent filter,
   Parseval sums, direct heat evolution of every initial Fourier coefficient,
   and scaling checks.
3. The manual pass checks the algebraic factors, the Duhamel quantifiers, the
   frame support estimate, and every excluded claim.  In particular, it
   distinguishes a fixed parent frame from its later low/high child
   refinement and a global cell from a matched spatial partition.

No audit time-steps the finite-\(K\) PDE.  The finite-window conclusion uses
an analytic perturbation estimate; the reconstructed curves are the exact
pure-heat limit.

## 2. Hard and soft all-shell identities

For one positive-denominator component, R0.71I gives

\[
 a_t+2\nu\kappa^2a=2z^+\mathcal J.
 \tag{2.1}
\]

Write \(w=\kappa^{-2}\) and
\(\mathcal J=\mathcal J^+-\mathcal J^-\).  Multiplication by \(w\) gives

\[
 2wz^+\mathcal J^+
 =wa_t+2\nu a+2wz^+\mathcal J^-.
 \tag{2.2}
\]

Hence, for a finite fixed family \(\Gamma\),

\[
 \boxed{
 2\mathcal Z_+
 =\partial_t\mathcal A_w
 +2\nu\sum_{\gamma\in\Gamma}a_\gamma
 +2\mathcal Z_-.}
 \tag{2.3}
\]

The symbolic residual is exactly zero.  The independent checker uses 257
deterministic samples with \(a=z^2\) and mutually exclusive positive and
negative parts of one signed source.  Its maximum binary64 residual is
\(8.54\times10^{-16}\).

For the fixed-\(\varepsilon\) soft equation,

\[
 (a_\varepsilon)_t
 +2\nu\kappa^2(1+\theta_\varepsilon)a_\varepsilon
 =2z_\varepsilon^+\mathcal J_\varepsilon,
 \tag{2.4}
\]

the same multiplication adds

\[
 2\nu\sum_\gamma
 \theta_{\varepsilon,\gamma}a_{\varepsilon,\gamma}\ge0
 \tag{2.5}
\]

to the right side of (2.3).  The symbolic residual is again zero, and the
independent maximum residual is \(8.54\times10^{-16}\).

After time integration, only \(\mathcal A_w(T_+)-\mathcal A_w(T_-)\)
telescopes.  The viscous amplitude mass and the negative-source term are
nonnegative.  Hard zero-denominator faces and refresh jumps are outside the
hypotheses and are not cancelled by (2.3).

**Verdict:** PASS for a finite fixed family between refreshes.

## 3. What the tight frame does and does not cancel

For the global cell, heat height zero, and a real-even scalar tight frame,

\[
 \sum_jB_j
 =\langle L,-\Delta u\rangle
 =\frac12Y_t+\nu\|\Delta u\|_2^2,
 \tag{3.1}
\]

\[
 \sum_jd_j=\|\Delta u\|_2^2,
 \qquad
 \sum_j\|F_j\|_2^2=\|L\|_2^2.
 \tag{3.2}
\]

These are signed, linear Parseval identities.  They imply the instantaneous
sandwich

\[
 \frac{((\sum_jB_j)^+)^2}{\sum_jd_j}
 \le \sum_j\frac{(B_j^+)^2}{d_j}
 \le \sum_j\|F_j\|_2^2,
\tag{3.3}
\]

Here a shell with \(d_j=0\) contributes zero, since then \(C_j=0\) and
\(B_j=0\); if \(\sum_jd_j=0\), all three quantities in (3.3) are zero.
Otherwise the quotients are taken only over \(d_j>0\).

But differentiating (3.3) does not preserve the order needed for the
one-sided time source.  Also, antisymmetric signed transfers do not cancel
after termwise positive parts: \(\tau^++(-\tau)^+=|\tau|\).

Thus the report's “no cancellation” statement is correctly restricted to
the exact nonnegative defect in (2.3).  It is not a claim that signed NSE
interactions have no cancellation.

**Verdict:** PASS; ordinary tightness does not pay the target source.

## 4. Fixed broad-parent witness and exact initial constants

The frame used in the witness is the parent-only log-radius frame declared in
R0.71E.  Its multiplier is one on normalized squared radii \([16,32]\) at
the selected scale \(\kappa=4K\).  The frame is fixed before the R0.71J
datum; only its index shifts with the dyadic frequency \(K=2^J\).

At \(K=1\), the real 2D3C datum contains:

- two shear modes \((\pm1,0)\) of amplitude one;
- four driver modes \((0,\pm4)\), \((0,\pm5)\) of amplitudes
  \(\pm i/4\), \(\mp i/5\);
- eight target modes \((\pm1,\pm4)\), \((\pm1,\pm5)\) of amplitude one.

The kinetic energy can be checked without convolution:

\[
 2+8+2\left(\frac1{16}+\frac1{25}\right)
 =\frac{2041}{200}.
 \tag{4.1}
\]

The enstrophy is

\[
 2+4+4(1+4^2)+4(1+5^2)=178.
 \tag{4.2}
\]

Independent direct convolution and Leray projection give

\[
 \boxed{
 \|u_0\|_2^2=\frac{2041}{200},\quad
 Y(0)=178K^2,\quad
 \|F_{4K}(0)\|_2^2=500K^2,\quad
 d_{4K}(0)=3942K^4,\quad B_{4K}(0)=0.}
 \tag{4.3}
\]

The maximum residual against these constants is zero in binary64.  Resolving
the pairing by absolute horizontal Fourier index gives

\[
\begin{array}{c|ccc}
|m|&\|F\|_2^2/K^2&d/K^4&B/K^3\\ \hline
0&328&82&36\\
1&8&3860&-36\\
2&164&0&0.
\end{array}
\tag{4.4}
\]

Thus the exact zero entry is a checked \(36-36\) cancellation, not a
missing-mode artifact.  All initial Lamb modes lie in the parent flat top.
Their squared radii are
\(16,17,20,25,26,29\), while the selected curl-denominator radii are
\(16,17,25,26\).  The only vertical Lamb channels are \(|\xi_2|=4K,5K\).

The datum has the invariant form
\(u=(0,V(x_1,t),w(x_1,x_2,t))\).  The shear solves heat and \(w\) solves a
linear passive advection--diffusion equation with a global smooth
coefficient.  This proves global smoothness of the witness family; it does
not invoke a general three-dimensional regularity theorem.

**Verdict:** PASS for the fixed parent-only frame.

## 5. Direct pure-heat Fourier reconstruction

The independent checker does not insert the displayed profiles as its
Fourier data.  At each of 22 sample times it first multiplies every initial
coefficient by \(e^{-|k|^2\theta}\), then rebuilds curl, convolution, Leray
projection, the broad-parent Lamb field, and the broad-parent denominator.
The resulting four quantities agree with

\[
 B_0=4(e^{-34\theta}-e^{-52\theta}),
 \tag{5.1}
\]

\[
 D_0=32e^{-32\theta}+1156e^{-34\theta}
     +50e^{-50\theta}+2704e^{-52\theta},
 \tag{5.2}
\]

\[
 Y_0=2e^{-2\theta}+2e^{-32\theta}+68e^{-34\theta}
     +2e^{-50\theta}+104e^{-52\theta},
 \tag{5.3}
\]

\[
 F_0^2=4e^{-34\theta}+192e^{-36\theta}
      +4e^{-52\theta}+300e^{-54\theta}.
 \tag{5.4}
\]

The maximum absolute residual is \(2.27\times10^{-13}\).  This comparison
includes \(\theta=0\), \(\theta_*=(\log2)/18\), and twenty additional
points.

Consequently

\[
 A_0(\theta)
 =\frac{16(e^{-34\theta}-e^{-52\theta})^2}{D_0(\theta)Y_0(\theta)},
 \tag{5.5}
\]

and exact symbolic simplification at \(\theta_*\) gives

\[
 A_*=
 \frac{4}{
 57(2^{1/9}+44)(3\,2^{1/9}+4\,2^{7/9}+120)}
 =1.1965465392386773\times10^{-5}.
 \tag{5.6}
\]

Both \(B_0(0)\) and \(A_0(0)\) vanish, while \(D_0\) is strictly positive.

**Verdict:** PASS.

## 6. Fixed-window perturbation and quantifiers

With \(\theta=\nu K^2t\), each vertical channel satisfies a diagonal heat
equation plus a bilateral shift whose coefficient is \(1/(\nu K)\).  The
shift is bounded on polynomially weighted \(\ell_s^2\); the diagonal part
generates an analytic contraction semigroup; and the initial data have finite
support.  Duhamel's formula, applied also two weights higher before
differentiation, gives for fixed

\[
 \nu>0,\qquad M<\infty,\qquad s<\infty
 \tag{6.1}
\]

the estimate

\[
 \max_{n=4,5}
 \|c_{\cdot,n}^{(K)}-c_{\cdot,n}^{(0)}\|_
 {C^1([0,M];\ell_s^2)}
 \le \frac{C_{M,s,\nu}}K.
 \tag{6.2}
\]

The constant is allowed to depend on \(M,s,\nu\), but not on \(K\).  Smooth
bounded parent multipliers preserve convergence of the displayed quadratic
quantities.  Since \(D_0\) stays positive on a fixed compact window, the
parent denominator is positive there for all sufficiently large dyadic
\(K\).  In particular,

\[
 a_{4K}\!\left(\frac{\theta_*}{\nu K^2}\right)
 \ge\frac{A_*}{2}.
 \tag{6.3}
\]

The audit therefore supports a fixed-\(\nu\), fixed-window, sufficiently-large
dyadic-\(K\) statement.  It does not turn (5.1)--(5.5) into exact finite-\(K\)
PDE formulas.

**Verdict:** PASS with the stated quantifier order.

## 7. Complete-frame heat upper bound

For the parent support,

\[
 W(\xi)=\sum_j2^{-2j}|m_j(\xi)|^2\le4|\xi|^{-2}.
 \tag{7.1}
\]

The exact 2D3C Lamb vector is
\(L=(0,0,-V\partial_2w)\).  Its vertical channel is unchanged, so every
Lamb mode satisfies \(|\xi|\ge|\xi_2|\ge4K\), and

\[
 \frac{\|L\|_2^2}{Y}\le\|V\|_\infty^2=4e^{-2\theta}.
 \tag{7.2}
\]

Combining the constants \(4\), \((4K)^{-2}\), and \(4e^{-2\theta}\)
gives the independently checked density bound

\[
 \sum_j2^{-2j}\frac{\|T_jL\|_2^2}{Y}
 \le\frac{e^{-2\theta}}{K^2}.
 \tag{7.3}
\]

Since \(dt=d\theta/(\nu K^2)\),

\[
 \boxed{
 \mathcal H_K^{\rm frame}
 \le\frac{1-2^{-1/9}}{2\nu K^4}.}
 \tag{7.4}
\]

This is a sum over every parent in the fixed frame, not only the selected
parent.

**Verdict:** PASS.

## 8. Positive-creation lower bound and scaling

On the selected parent, \(\kappa=4K\) and
\(a(0)=0\).  Integrating the scalar identity and retaining its nonnegative
damping and negative-source rows yields

\[
 \int_{I_K}z_{4K}^+\mathcal J_{4K}^+dt
 \ge\frac{a_{4K}(\sup I_K)}2
 \ge\frac{A_*}{4}.
 \tag{8.1}
\]

After the frame weight \((4K)^{-2}\),

\[
 \boxed{
 \mathcal Z_K^{\rm frame}\ge\frac{A_*}{64K^2}.}
 \tag{8.2}
\]

Together with (7.4),

\[
 \boxed{
 \frac{\mathcal Z_K^{\rm frame}}{\mathcal H_K^{\rm frame}}
 \ge
 \frac{\nu A_*}{32(1-2^{-1/9})}K^2.}
 \tag{8.3}
\]

At \(\nu=1\), the independent lower ratios for
\(K=8,16,32,64,128\) are

\[
 0.0003228444, 0.0012913774, 0.0051655097,
 0.0206620388, 0.0826481552.
 \tag{8.4}
\]

Every successive ratio is exactly four up to the recorded binary64
arithmetic.  The small numerical coefficient does not affect the
quantifier: for fixed \(\nu>0\), the lower ratio is unbounded as dyadic
\(K\to\infty\).

**Verdict:** PASS; no constant independent of \(K\) can give the declared
full-frame heat payment.

## 9. Scope and quantifier audit

The supported statement has the following exact scope:

1. the parent-only smooth tight frame already declared in R0.71E;
2. one global cell \(\chi=1\) and heat height \(s=0\);
3. fixed viscosity \(\nu>0\);
4. the stated global-smooth fixed-energy 2D3C family;
5. all sufficiently large dyadic \(K\);
6. a constant in the proposed payment that is independent of \(K\).

The following extensions are not supported:

- the later R0.71E low/high child refinement;
- a matched spatial cell partition, collars, or movement terms;
- hard denominator faces, soft-to-hard passage, or refresh atoms;
- a different NSE-specific right side not bounded by the heat endpoint;
- an infinite frame--cell compactness theorem;
- failure of the complete face-paid weighted-BV target;
- a continuation criterion, singularity, or global regularity theorem.

The claim flags in the independent JSON enforce these boundaries:
`parentOnlyFrameChecked=true`, `matchedSpatialCellsChecked=false`,
`facePaidWeightedBVRejected=false`, `regularityTheoremClaimed=false`, and
`originalityClaimed=false`.

**Verdict:** PASS.

## 10. Literature and originality boundary

Smooth Germano telescopes, Littlewood--Paley energy flux identities,
shell-to-shell transfer notation, smooth frame decompositions, and
conditional critical-space regularity criteria are established literature.
The bounded source search found close conceptual precedent for the loss of
cancellation under an absolute value or positive part.  It did not locate a
theorem for the complete normalized source used here.

That negative search result is not evidence of originality, priority, or
nonexistence.  The present audit checks internal correctness only.  A novelty
claim would still require broader database coverage, citation tracing, and
expert review.

**Verdict:** PASS with no originality claim.

## 11. Final release verdict

The following rows are independently supported:

1. exact hard and soft all-shell positive-defect identities;
2. separation of the signed tight-frame telescope from shellwise positive
   creation;
3. exact fixed-energy broad-parent Fourier constants and zero-entry
   cancellation;
4. direct heat evolution and reconstruction of all four limiting profiles;
5. fixed-window \(C^1\) asymptotics with the correct order of quantifiers;
6. the complete-parent-frame heat upper bound;
7. the selected-parent creation lower bound and resulting \(K^2\) gap;
8. the parent-only, global-cell, non-regularity, non-originality boundary.

With these boundaries retained, the mathematical audit verdict is
**PASS**.  R0.71J rejects automatic all-shell cancellation after positive
parts and rejects payment by the same full-frame physical-time heat endpoint
for the declared parent frame.  It does not close the full
temporal-residence route.
