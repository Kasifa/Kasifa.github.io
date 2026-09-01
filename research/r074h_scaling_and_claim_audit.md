# R0.74H — independent scaling and claim-boundary audit

## Verdict and source binding

**FINAL PASS.**  The cubicized collar-flux row, the two-regime estimates,
the small-payment corollary, and the explicit-family lower bounds have the
correct powers and claim directions.  No blocking scaling or claim-boundary
error was found.

This audit is bound to the complete analytic source

    research/r074h_collar_flux_two_regime_closure.md

with SHA-256

    14ec43c55d833ea498d9ccd1a9e4514b015d8db41194615360af7376ccc433fe.

The review is read-only with respect to that source.  It checks the specific
rows (5.2), (6.7)--(6.9), (7.5a), and (7.7)--(7.8), together with the nearby
statements about logarithmic repairs, reverse flux comparison, regularity,
novelty, and the Millennium problem.

---

## 1. Reference scaling

On the inherited R0.74F--G family,

\[
 R=e^{-c_RL^2},\qquad
 \gamma=e^{-c_\gamma L^2},\qquad
 BR^2\longrightarrow\frac1{128},\qquad
 \mathfrak a=B\gamma^{-1/2}.
\tag{1.1}
\]

The proved target lower scale is

\[
 X_* = B^2LR^2.
\tag{1.2}
\]

A quantity placed inside a payment and then subjected to the outer
\(2/3\) power must therefore have scale

\[
 X_*^{3/2}=B^3L^{3/2}R^3.
\tag{1.3}
\]

R0.74G supplies only the upper bound

\[
 P_R\le CB^3R^3,
 \qquad
 P_R^{2/3}\le CB^2R^2=o(X_*).
\tag{1.4}
\]

Nothing in this audit reverses the first inequality in (1.4) or promotes it
to a matching \(B^3R^3\) lower bound.

---

## 2. Audit of the cubicized flux, equation (5.2)

The analytic source defines

\[
 \widehat P_R^\alpha
 =P_R^\alpha+(\mathfrak C_R^\alpha)^{3/2}.
\tag{2.1}
\]

This is the correct exponent.  For nonnegative \(P,C\),

\[
 P^{2/3}+C
 \le 2(P+C^{3/2})^{2/3}.
\tag{2.2}
\]

Indeed, both \(P^{2/3}\) and \(C\) are bounded by
\((P+C^{3/2})^{2/3}\).  At the explicit-family lower scale
\(C\gtrsim X_*\), the new row satisfies

\[
 C^{3/2}\gtrsim B^3L^{3/2}R^3,
\tag{2.3}
\]

which is exactly (1.3).  Inserting \(C\) itself inside the payment would
have the wrong power; the source does not make that mistake.

The source also states the correct boundary: this correction is
**identity-level**.  It records positive cumulative work in the weighted
energy identity.  It is not claimed to be independently controlled by a
weaker regularity quantity.

**Decision for (5.2): PASS.**

---

## 3. Audit of the two-regime rows, equations (6.7)--(6.9)

The source proves

\[
 X_R^M\le C\bigl[(P_R^M)^{2/3}+P_R^M\bigr],
\tag{3.1}
\]

and

\[
 X_R^F
 \le C\bigl[(P_R^F)^{2/3}+P_{0,R}^F\bigr]
 \le C\bigl[(P_R^F)^{2/3}+P_R^F\bigr].
\tag{3.2}
\]

These formulas agree with the scaling screen.  The linear term is part of
the **outer two-regime response**; it is not inserted into a new payment and
then incorrectly raised to \(2/3\).  Version F correctly retains the
pre-acceleration quantity \(P_{0,R}^F\) in the sharper first inequality.
Since

\[
 P_R^F=P_{0,R}^F+(\mathcal J_{\rm acc}^{F,R})^{3/2},
\tag{3.3}
\]

this avoids charging the acceleration moment linearly twice.

When \(P_R^\alpha\le1\),

\[
 P_R^\alpha\le(P_R^\alpha)^{2/3},
 \qquad
 P_{0,R}^F\le P_R^F,
\tag{3.4}
\]

so (3.1)--(3.2) imply exactly

\[
 X_R^\alpha\le C(P_R^\alpha)^{2/3}.
\tag{3.5}
\]

The source labels (3.5) as a size implication only.  It does not infer
propagation, absorption, epsilon regularity, or singularity exclusion.

**Decision for (6.7)--(6.9): PASS.**

---

## 4. Audit of the large-payment conclusion, equation (7.5a)

The repaired source no longer infers a matching lower bound from the
R0.74G upper bound.  Its argument is instead:

1. the explicit family has
   \(X_R\ge cB^2LR^2\to\infty\);
2. if \(P_R\le1\), Corollary 6.3 would give
   \(X_R\le C P_R^{2/3}\le C\), a contradiction for large \(j\);
3. hence \(P_R>1\) eventually, and then
   \(P_R^{2/3}\le P_R\);
4. Theorem 6.2 consequently yields

\[
 P_R\ge cX_R\ge cB^2LR^2\longrightarrow\infty.
\tag{4.1}
\]

This proves the displayed lower conclusion in (7.5a).  It does **not** prove

\[
 P_R\gtrsim B^3R^3
\tag{4.2}
\]

and the source explicitly says that no matching \(B^3R^3\) claim is needed.
Thus the direction of the inherited upper bound is no longer reversed.

**Decision for (7.5a): PASS.**

---

## 5. Audit of the explicit-family flux lower bound, equations (7.7)--(7.8)

For terminal times in the R0.74F lobe interval, the weighted kinetic term in
the exact energy identity obeys

\[
 \frac1R\int\Theta_R|u_j(\tau)|^2
 \ge cB_j^2L_jR_j^2.
\tag{5.1}
\]

The quadratic time-and-Laplacian cutoff row satisfies

\[
 \mathfrak Q_{R_j}
 \le C P_{R_j}^{2/3}
 \le CB_j^2R_j^2.
\tag{5.2}
\]

The last expression is smaller than (5.1) by one factor of \(L_j\).
The dissipation on the left side of the exact identity is nonnegative.
Therefore the cumulative signed flux must be positive at one such terminal
time and

\[
 \mathfrak C_{R_j}^M=\mathfrak C_{R_j}^F
 \ge cB_j^2L_jR_j^2.
\tag{5.3}
\]

Taking the \(3/2\) power gives

\[
 (\mathfrak C_{R_j}^\alpha)^{3/2}
 \ge cB_j^3L_j^{3/2}R_j^3.
\tag{5.4}
\]

This is precisely the required lower scale.  The source does not claim an
upper bound of the same order, an asymptotic equivalence, or any reverse
comparison between the flux and the endpoint.  It says explicitly:
“No reverse comparison is claimed.”

**Decision for (7.7)--(7.8): PASS.**

---

## 6. Logarithmic and claim-boundary screen

The audited source contains no theorem involving

\[
 P^{2/3}\sqrt{1+\log_+P}
\tag{6.1}
\]

or any other logarithmic frontier.  A prior scaling screen may motivate
such a candidate, but R0.74H neither uses nor proves it.  No claim about a
minimal logarithmic repair is present.

The proved scope is every **smooth periodic unforced** solution satisfying
the interior-time hypothesis and using the two frozen local frames.  The
following remain outside the theorem:

- weak-solution stability or lower semicontinuity of the moving-frame flux;
- an independently payable bound for \(\mathfrak C_R^\alpha\);
- scale iteration, absorption, epsilon regularity, or continuation;
- singularity exclusion or global regularity;
- novelty or priority; and
- every Millennium-problem conclusion.

The source keeps these items open or not claimed and retains the label
**NOT CLAY**.

---

## 7. Final result

All requested scaling identities and claim directions agree with the exact
energy algebra and with the inherited R0.74F--G bounds.  The earlier
large-payment declaration gap has been removed: (7.5a) comes from the new
two-regime theorem and the target lower bound, not from reversing an upper
estimate.  No logarithmic-frontier theorem or two-sided flux comparison has
been introduced.

**FINAL PASS.**
