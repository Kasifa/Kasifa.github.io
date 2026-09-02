# R0.74N final source rebind audit

## 1. Final binding and verdict

This rebind was performed after the original shell reconstruction, the
cross-note implication audit, the complete-cutoff clarification, and the
correction of the initial source-diff invariant.

| Object | Final SHA-256 |
|---|---|
| research/r074n_problem_freeze.md | 4b2df724cf81cf28d0c9b89636ae166ade11746f623ca2a3466f08e4e1adfacc |
| research/r074n_all_shell_synthesis.md | ca1ddabb6ea931b2f1a96b5cb000e955492c6852b0ea3b2aaa6148c6f3fa9e1e |
| research/r074n_gap_matrix.md | 986a2ddc20318f6f70a968f80fd972c671e7ae43fe769e2acd00d4230d08fb06 |
| research/r074n_crossnote_implication_independent_audit.md | 7c289055939cdbf21780337e7da2a1d91109172d89a6c168258703124b50be8a |
| research/r074n_all_shell_independent_audit.md | 5173ac954ca82e2abc0371258527ddd8b6bc372e43de6c3a2aeea2a9f2b187e9 |

The shell theorem and the cross-note consequence both have verdict
**PASS**.  Their logical roles remain distinct: Theorem 6.1 proves the K
collar hypothesis, while Corollary 6.2 combines that new collar bound with
the pre-existing F/H/J results to obtain the exact-family endpoint law.

## 2. Unique equation-tag inventory

The final proof contains exactly 61 equation tags, all 61 unique:

\[
\begin{gathered}
 0.1,\ 0.2,\ 0.3,\ 0.4,\ 0.5,\ 0.6;\\
 1.1,\ 1.2,\ 1.3,\ 1.4;\\
 2.1,\ 2.2,\ 2.3,\ 2.4,\ 2.5,\ 2.6,\ 2.7,\ 2.8,\ 2.9,\ 2.10,\ 2.11;\\
 3.1,\ 3.2,\ 3.3,\ 3.4,\ 3.5,\ 3.6,\ 3.7,\ 3.8,\ 3.9,\ 3.10,\
 3.11,\ 3.12,\ 3.13,\ 3.14,\ 3.15,\ 3.16,\ 3.17;\\
 4.1,\ 4.2;\\
 5.1,\ 5.2,\ 5.3,\ 5.4,\ 5.5,\ 5.6,\ 5.7,\ 5.8,\ 5.9,\ 5.10;\\
 6.1,\ 6.2,\ 6.3,\ 6.4,\ 6.5;\\
 6.6,\ 6.7,\ 6.8,\ 6.9,\ 6.10,\ 6.11.
\end{gathered}
\]

The split is 55 pre-existing tags and six new cross-note tags.  The final
source has 86 opening and 86 closing inline-math delimiters, 61 opening and
61 closing display-math delimiters, no duplicate tags, no tabs, no carriage
returns, and no other ASCII control characters.

## 3. Fail-closed source-diff correction

The prior proof bound before the cross-note revision had SHA-256

    946f3e100944f3dc1e71dbf1b5389e1f3fd1db15e4f4f30f08675e43c4c9df62.

An initial rebind proposal said that all 55 old displays were unchanged.  The
independent check rejected that sentence before any audit file was saved.
After explicit authorization of the accurate invariant, the final comparison
is:

1. 53/55 pre-existing displays are verbatim unchanged;
2. old display (0.3) is extended to summarize the independently audited
   exact-family \(X_j\) consequence;
3. old display (0.6) is expanded from its abbreviated window line to the
   complete inherited R0.74H cutoff system;
4. all 49 shell-body displays (1.1)--(6.5) are verbatim unchanged; and
5. (6.6)--(6.11) are six newly added cross-note displays.

It would therefore be false to record “55/55 old displays unchanged.”  The
two controlled changes are mathematically substantive only in the following
limited senses: (0.3) updates the summary after Corollary 6.2, and (0.6)
removes cutoff ambiguity.  Neither changes an inward, target, outer, or
infinite-shell estimate.

## 4. Classification of the new corollary

The new source block after Theorem 6.1 does four things:

1. aliases the already frozen endpoint components
   \(\mathcal U_{\rm ext}^{\infty,\alpha,R_j}\) and
   \(\mathcal D_{\rm ext}^{\alpha,R_j}\);
2. applies the separate R0.74H (5.1a)--(5.1b) component bounds;
3. inserts the R0.74J payment upper law and the new N/K collar upper law; and
4. inserts the R0.74F lower bound for the endpoint exterior-energy component.

The independently checked result is

\[
 cT_j\le\mathcal U_j\le X_j\le CT_j,
 \qquad 0\le\mathcal D_j\le CT_j,
 \qquad T_j=B_j^2L_jR_j^2.
\]

No lower bound is asserted for \(\mathcal D_j\) alone.  The shell estimate by
itself does not imply this endpoint result; the implication is explicitly
cross-note and non-circular.

## 5. Final boundary

The final source proves matching \(X_j\) and \(\mathfrak C_j\) laws only on
the frozen exact family.  It does not prove a universal endpoint estimate,
an arbitrary-flow collar theorem, payment-to-admissibility, core-from-shell
control, singularity exclusion, or global regularity.  **NOT CLAY.**

\[
 \boxed{\text{FINAL SOURCE REBIND: PASS; 61/61 UNIQUE TAGS; NOT CLAY.}}
\]
