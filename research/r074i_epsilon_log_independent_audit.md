# R0.74I — independent adversarial audit of the epsilon bridge and logarithmic obstruction

## Verdict and source binding

**CONDITIONAL PASS.**  I found no blocking mathematical error in the
moving-tube epsilon argument or in the square-root logarithmic lower screen.
The scale factors, inequality directions, and use of the velocity-only
one-scale theorem are correct.  Four repairs are required before freeze:

1. use \(1+\log_+P\), or explicitly restrict every generic logarithmic
   expression to \(P\geq1\);
2. write out the two-line derivation showing that an endpoint upper bound
   forces \(P_j\gtrsim B_j^3R_j^3\);
3. prove, rather than merely describe, the lacunarity of the realized
   sequence \((P_j)\); and
4. make the generic frame label in (4.10)--(4.13) explicit.

These are precision and completeness repairs.  None reverses the main
conclusions.  In particular, this audit does **not** promote the endpoint
\(\gamma=1/2\) to an upper theorem.

This review is read-only with respect to the analytic source

    research/r074i_suitable_weak_tube_and_log_obstruction.md

at SHA-256

    0ed6425884a841e1f8e42a1a3dfb3ee09a76732d0bf2bd9888a739e4d00570da.

The inherited sources checked were

    research/r074g_complete_payment_counterexample.md
    95548d6225389b9cfd1822a8abaf89e495e7f15ca5ff30c6b92aaa8ac5f2d6be

    research/r074h_collar_flux_two_regime_closure.md
    8c1d43f08d5a2c9299ae50ebdd10c8c184f064c6830f1d663524e03fa90d88f1

    research/r074h_scaling_and_claim_audit.md
    a6dd7f5e1efae508ed332acfb7b3af3170668a9b12e95a1eec167ee90cad3be2.

The audit covers only Sections 3--4 of the R0.74I source.  It does not audit
the moving local-energy test or weak finite-shell limit in Section 2.

---

## 1. Almost-everywhere drift control and path confinement

Write \(E=\mathcal E^{M,R}(z_0,8R)\).  The first term in the definition of
\(E\) gives, for almost every \(t\in I_{8R}\),

\[
 \int_{B_{8R}}|v_R(t,y)|^2\,dy\leq 8RE.
\tag{1.1}
\]

Because the frozen mollifier is supported in \(B_R\) and
\(\|\varphi_R\|_2=R^{-3/2}\|\varphi\|_2\), the trajectory equation gives

\[
\begin{aligned}
 |a_R(t)|
 &=\left|\int_{B_R}\varphi_R(-y)v_R(t,y)\,dy\right|\\
 &\leq \|\varphi\|_2R^{-3/2}
       \left(\int_{B_R}|v_R(t,y)|^2\,dy\right)^{1/2}\\
 &\leq \sqrt8\,\|\varphi\|_2R^{-1}E^{1/2}
\end{aligned}
\tag{1.2}
\]

for almost every time.  Thus (3.1) has the correct \(R^{-1}\) factor.
The almost-everywhere qualification is sufficient: the Caratheodory path
has an absolutely continuous lift, so, for every \(t\in I_{R/2}\),

\[
 |X_R(t)-X_R(t_0)|
 \leq\int_t^{t_0}|a_R(s)|\,ds
 \leq \frac{\sqrt8\,\|\varphi\|_2}{4}RE^{1/2}.
\tag{1.3}
\]

The factor \(1/4\) is exactly the time length
\(|I_{R/2}|=(R/2)^2=R^2/4\).  There is no illicit passage from an
almost-everywhere estimate to a pointwise derivative estimate; only the
integral identity of the absolutely continuous path is used.

For a completely literal periodic statement, the source should say that
\(X_R\) is represented by the continuous lift in \(\mathbb R^3\) anchored
at a chosen lift of \(x_0\).  Since the resulting displacement is at most
\(R/2\) and \(R<\pi/16\), no ambiguity from the torus cut locus occurs.

**Decision for Lemma 3.1: PASS, with the lift clarification required.**

---

## 2. Geometry of the moving and fixed balls

Under (3.4), if \(x\in B_{R/2}(x_0)\), then

\[
 |x-X_R(t)|
 \leq |x-x_0|+|x_0-X_R(t)|<R.
\tag{2.1}
\]

Therefore

\[
 B_{R/2}(x_0)\subset X_R(t)+B_R
\tag{2.2}
\]

for every \(t\in I_{R/2}\), exactly as claimed.  Translation by
\(X_R(t)\) then gives

\[
 \int_{B_{R/2}(x_0)}|u(t,x)|^3\,dx
 \leq \int_{B_R}|v_R(t,y)|^3\,dy.
\tag{2.3}
\]

This is a time-slice inclusion.  It does not assert that a moving
space-time tube is itself a standard parabolic cylinder.

**Decision for (3.4)--(3.5): PASS.**

---

## 3. Fixed-\(y\) interpolation and every scale factor

The relevant functional inequality is Guevara--Phuc, Lemma 2.6.  For an
arbitrary energy-class function on \(Q_\rho\), it states

\[
 r^{-2}\int_{Q_r}|f|^3
 \leq C\left(\frac\rho r\right)^3
 A_f(\rho)^{3/4}B_f(\rho)^{3/4}
 +C\left(\frac r\rho\right)^3A_f(\rho)^{3/2},
\tag{3.1}
\]

where

\[
 A_f(\rho)=\rho^{-1}\operatorname*{ess\,sup}_t
             \int_{B_\rho}|f|^2,
 \qquad
 B_f(\rho)=\rho^{-1}\int_{Q_\rho}|\nabla f|^2.
\tag{3.2}
\]

Apply this purely functional inequality to \(f=v_R\) in the fixed
\(y\)-coordinates, with \(r=R\) and \(\rho=8R\).  Both quantities in
(3.2) are bounded by \(E\).  Hence

\[
\begin{aligned}
 R^{-2}\int_{I_R}\int_{B_R}|v_R|^3
 &\leq C8^3E^{3/4}E^{3/4}
      +C8^{-3}E^{3/2}\\
 &\leq C_IE^{3/2}.
\end{aligned}
\tag{3.3}
\]

No Navier--Stokes equation for \(v_R\) is needed here.  This matters:
the residual drift in its moving-frame equation creates no missing term in
this step.  Combining (2.3), restricting from \(I_R\) to \(I_{R/2}\), and
using \((R/2)^{-2}=4R^{-2}\) gives exactly

\[
 (R/2)^{-2}\int_{I_{R/2}}\int_{B_{R/2}(x_0)}|u|^3
 \leq 4C_IE^{3/2}.
\tag{3.4}
\]

The source absorbs this fixed factor into its constant.  Its displayed
constant \(C_I\) should be understood as the post-restriction constant.

**Decision for Lemma 3.2: PASS.**

Primary source checked: C. Guevara and N. C. Phuc,
[Local energy bounds and epsilon-regularity criteria for the 3D
Navier--Stokes system](https://arxiv.org/abs/1702.00449), Lemma 2.6.

---

## 4. Velocity-only one-scale criterion and scaling

Wang--Wu--Zhou, Theorem 1.1, states that for every \(\delta>0\) a suitable
weak solution in \(Q(1)\) is bounded in \(Q(1/16)\) if

\[
 \int_{Q(1)}|u|^{5/2+\delta}\leq\varepsilon(\delta).
\tag{4.1}
\]

Taking \(\delta=1/2\) gives exponent \(3\) and removes pressure from the
smallness hypothesis.  If \(r=R/2\) and

\[
 U(s,\xi)=r\,u(t_0+r^2s,x_0+r\xi),
\tag{4.2}
\]

then

\[
 \int_{Q(1)}|U|^3\,d\xi\,ds
 =r^{-2}\int_{Q_r(z_0)}|u|^3\,dx\,dt.
\tag{4.3}
\]

Thus (3.11) is exactly the rescaled hypothesis of the cited theorem, not
a norm with a missing cube and not a condition requiring pressure
smallness.  The periodic solution restricts to a Euclidean suitable weak
solution on this interior cylinder; \(r<\pi/32\) is far below the torus
injectivity radius.  Boundedness on the smaller backward cylinder is the
standard local meaning that \(z_0\) is regular.

The theorem citation should use its exact title and published DOI:

- Y. Wang, G. Wu, and D. Zhou,
  [A regularity criterion at one scale without pressure for suitable weak
  solutions to the Navier--Stokes equations](https://doi.org/10.1016/j.jde.2019.05.003),
  *Journal of Differential Equations* 267 (2019), 4673--4704;
- [arXiv:1811.09927](https://arxiv.org/abs/1811.09927), Theorem 1.1.

The source's current arXiv title is close but not exact.  This is
bibliographic, not analytic.

**Decision for the external theorem and its use in Theorem 3.3: PASS.**

---

## 5. The small-\(P_R^M\) corollary

Every row in \(\mathcal A_{\rm ext}^{M,R}\) is nonnegative, so

\[
 E^{3/2}\leq P_R^M.
\tag{5.1}
\]

Consequently

\[
 P_R^M\leq\varepsilon_P
 \quad\Longrightarrow\quad
 E\leq\varepsilon_P^{2/3}.
\tag{5.2}
\]

Choosing \(\varepsilon_P\leq\varepsilon_{\rm tube}^{3/2}\) gives
\(E\leq\varepsilon_{\rm tube}\), so (3.9) follows.  The exponent and
inequality direction are correct.

It is also useful to state explicitly that Section 3 does not use the weak
two-regime closure in Section 2.  It uses only suitability, the mollified
path, the assumed moving energy, the interpolation inequality, and the
external one-scale theorem.  Therefore a later repair to Section 2 would
not by itself invalidate the epsilon bridge.

**Decision for (3.9): PASS.**

---

## 6. Inherited packet scales and the logarithmic window

The inherited results give, for all sufficiently large \(j\),

\[
\begin{gathered}
 P_j\leq AB_j^3R_j^3,
 \qquad
 P_j\geq a_PB_j^2L_jR_j^2,\\
 Y_j\geq a_YB_j^2L_jR_j^2,
 \qquad Y_j\in\{X_j,\mathfrak C_j\},
\end{gathered}
\tag{6.1}
\]

with

\[
 R_j=e^{-\rho L_j^2},
 \qquad b_j=B_jR_j^2\longrightarrow\frac1{128}.
\tag{6.2}
\]

The safe eventual bounds \(1/256\leq b_j\leq1/64\) follow from this
convergence.  They imply

\[
 B_j^3R_j^3=b_j^3e^{3\rho L_j^2},
 \qquad
 B_j^2L_jR_j^2=b_j^2L_je^{2\rho L_j^2}.
\tag{6.3}
\]

Taking logarithms in the two payment inequalities, using boundedness above
and below of \(b_j\), and dividing by \(L_j^2\) gives

\[
 2\rho+\frac{\log L_j+O(1)}{L_j^2}
 \leq\frac{\log P_j}{L_j^2}
 \leq3\rho+\frac{O(1)}{L_j^2}.
\tag{6.4}
\]

This proves (4.7), including \(P_j\to\infty\).  The lower bound is not
misused to control \(P_j^{2/3}\); only the upper bound is used for that.

**Decision for (4.2)--(4.7): PASS.**

---

## 7. Square-root logarithmic lower screen

For every fixed \(\delta>0\), the payment upper bound and (6.4) imply,
eventually,

\[
 P_j^{2/3}\leq A^{2/3}B_j^2R_j^2,
 \qquad
 1+\log P_j\leq(3\rho+\delta)L_j^2.
\tag{7.1}
\]

Therefore

\[
 P_j^{2/3}\sqrt{1+\log P_j}
 \leq A^{2/3}\sqrt{3\rho+\delta}\,
       B_j^2L_jR_j^2.
\tag{7.2}
\]

Dividing the lower bound for either \(Y_j\) by (7.2) gives

\[
 \liminf_{j\to\infty}
 \frac{Y_j}{P_j^{2/3}\sqrt{1+\log P_j}}
 \geq
 \frac{a_Y}{A^{2/3}\sqrt{3\rho+\delta}}>0.
\tag{7.3}
\]

One may fix, for example, \(\delta=\rho\); letting \(\delta\downarrow0\)
is valid but unnecessary.  Since \(P_j\to\infty\), every eventually
nonnegative function

\[
 \Phi(p)=o\!\left(p^{2/3}\sqrt{1+\log p}\right)
\tag{7.4}
\]

fails to dominate \(Y_j\) along the realized sequence.  This proves the
claimed obstruction for any positive universal constant \(K\).

For a fixed \(\gamma<1/2\), division by
\(P_j^{2/3}(1+\log P_j)^\gamma\) yields

\[
 \frac{Y_j}{P_j^{2/3}(1+\log P_j)^\gamma}
 \geq c(1+\log P_j)^{1/2-\gamma}\longrightarrow\infty.
\tag{7.5}
\]

Every inequality direction in this argument is correct.

**Decision for Theorem 4.1 and the \(\gamma<1/2\) conclusion: PASS on the
eventual large-\(P\) sequence.**

---

## 8. Endpoint implication

The sentence after (4.14) is mathematically correct, but its proof must be
shown.  Suppose, for either \(Y=X\) or \(Y=\mathfrak C\), that a universal
endpoint upper estimate holds:

\[
 Y_R\leq K P_R^{2/3}\sqrt{1+\log_+P_R}.
\tag{8.1}
\]

On the explicit family, (6.1) and the logarithmic upper bound in (7.1)
give

\[
 a_YB_j^2L_jR_j^2
 \leq Y_j
 \leq C K L_jP_j^{2/3}.
\tag{8.2}
\]

Cancel \(L_j>0\) and raise the result to the \(3/2\) power:

\[
 P_j\geq cK^{-3/2}(B_j^2R_j^2)^{3/2}
 =cK^{-3/2}B_j^3R_j^3.
\tag{8.3}
\]

Thus an endpoint upper theorem would indeed force the missing matching
lower bound.  It does not follow from the presently frozen results without
the hypothetical endpoint upper estimate.

**Decision for the endpoint sentence: CONDITIONAL PASS; insert
(8.1)--(8.3) into the source before freeze.**

---

## 9. Lacunarity and the exact claim boundary

The statement that the realized payment sequence is highly lacunary is
also derivable, but the derivation is absent.  Since
\(L_{j+1}=2L_j\), (6.1)--(6.3) give

\[
\begin{aligned}
 \log\frac{P_{j+1}}{P_j}
 &\geq 2\rho L_{j+1}^2-3\rho L_j^2
       +\log L_{j+1}+O(1)\\
 &=5\rho L_j^2+\log L_{j+1}+O(1)
 \longrightarrow\infty.
\end{aligned}
\tag{9.1}
\]

Hence \(P_{j+1}/P_j\to\infty\), so \((P_j)\) is eventually strictly
increasing and genuinely lacunary.  This justifies the source's caveat:
the family constrains an arbitrary comparison function only at the
realized values \(P_j\).  Without monotonicity, regular variation, or
another structural assumption on \(\Phi\), it gives no pointwise lower
bound for \(\Phi(p)\) at every sufficiently large real \(p\).

The source should also retain the following boundaries:

- \(\gamma=1/2\) is the first logarithmic power not rejected by this
  family, not a proved upper exponent;
- the argument supplies no estimate between successive \(P_j\);
- it supplies no smallness, scale propagation, continuation, or global
  regularity statement; and
- it is a route screen, not a novelty or Millennium-problem conclusion.

**Decision for the lacunarity boundary: CONDITIONAL PASS; add (9.1).**

---

## 10. Required source repairs

### Repair A — logarithm domain

The generic formulas in the opening summary and (4.13) contain
\((1+\log P_R)^\gamma\).  For \(0<P_R<e^{-1}\), the base is negative and a
noninteger power is not a real-valued quantity.  Replace every generic
formula by

\[
 P_R^{2/3}(1+\log_+P_R)^\gamma,
 \qquad \log_+p=\max\{\log p,0\},
\tag{10.1}
\]

or explicitly state that the formula is asserted only for \(P_R\geq1\).
The realized sequence is eventually larger than one, so this repair does
not alter Theorem 4.1.

### Repair B — frame notation

Equations (4.10) and (4.13) write \(X_R\) and \(\mathfrak C_R\) without a
frame superscript, although the generic observables have Version-M and
Version-F definitions.  State that each proposed inequality is rejected
separately for \(\alpha=M\) and \(\alpha=F\).  Equality of the two versions
on the explicit family is sufficient for both rejections.

### Repair C — endpoint and lacunarity proofs

Insert the derivations (8.2)--(8.3) and (9.1), rather than leaving them as
unsupported prose.

### Repair D — citation wording

Use the exact Wang--Wu--Zhou title and identify Theorem 1.1 with
\(\delta=1/2\).  State the rescaling (4.2)--(4.3) in the proof.  This makes
the absence of a pressure hypothesis auditable.

---

## 11. Claim-to-source ledger and stopping rule

| Claim checked | Primary or frozen evidence | Result |
|---|---|---|
| Fixed-cylinder cubic interpolation, including both energy terms and radius ratios | Guevara--Phuc, arXiv:1702.00449, Lemma 2.6 | PASS |
| Velocity-only one-scale criterion at exponent \(3\) | Wang--Wu--Zhou, arXiv:1811.09927 / JDE 267 (2019), Theorem 1.1 with \(\delta=1/2\) | PASS |
| Denominator upper scale \(P_j\lesssim B_j^3R_j^3\) | Frozen R0.74G (1.10), (7.2)--(7.4) | PASS / inherited |
| Endpoint and collar-flux lower scales \(X_j,\mathfrak C_j\gtrsim B_j^2L_jR_j^2\) | Frozen R0.74F survival and R0.74H (7.5a), (7.7) | PASS / inherited |
| Logarithmic window and \(\gamma<1/2\) obstruction | Direct algebra from the preceding frozen bounds | PASS |
| Endpoint upper would force matching denominator lower bound | Direct implication (8.1)--(8.3) | PASS only as a hypothetical implication |

The source search stopped after the exact two external ingredients were
located in their primary records and the inherited scales were checked
against the frozen R0.74G/H notes and audits.  Additional adjacent
epsilon-regularity or logarithmic-criterion papers would not change the
validity of these two derivations.  This audit makes no novelty claim.

---

## 12. Final decision table

| Item | Decision | Freeze condition |
|---|---|---|
| Drift bound and path integration | **PASS** | Specify the anchored torus lift. |
| Ball inclusion | **PASS** | None beyond the lift clarification. |
| Fixed-\(y\) interpolation | **PASS** | Keep both terms of Lemma 2.6 and absorb the factor \(4\) into \(C_I\). |
| Wang--Wu--Zhou theorem and NSE scaling | **PASS** | Give exact theorem citation and rescaling. |
| Small-\(P_R^M\) corollary | **PASS** | State nonnegativity of the exterior ledger. |
| Logarithmic window | **PASS** | None. |
| \(o(P^{2/3}\sqrt{\log P})\) and \(\gamma<1/2\) rejection | **PASS for the realized large-\(P_j\) sequence** | Use \(\log_+\) in generic formulas and explicit frame labels. |
| Endpoint forcing of \(P_j\gtrsim B_j^3R_j^3\) | **CONDITIONAL PASS** | Add the derivation. |
| Lacunarity claim | **CONDITIONAL PASS** | Add the ratio proof. |
| Endpoint upper bound, scale propagation, or global regularity | **OPEN / NOT PROVED** | Must remain outside the theorem. |

After the four repairs listed at the start, Sections 3--4 are suitable for
promotion from this audit's scope.  The overall release must still wait for
the independent Section-2 audit, certificate, literature boundary, figure,
and final-source rebind required by the project manifest.

**NOT CLAY.**
