# R0.74M final source-rebind audit

## Result

This note checks the proof-source edit made after the independent analytic
PASS in r074m_nearest_inward_independent_audit.md.

\[
 \boxed{\text{FINAL SOURCE REBIND: PASS}.}
\]

The previously audited proof bytes had SHA-256

\[
 \texttt{5832c742000f1879874de7170403b2d1a78f44c2c511b6f65a1dd25c5c84deca}.
\]

The current r074m_final_segment_expulsion.md has SHA-256

\[
 \texttt{0077326ca97cfe40a0a43019caf0118504cf9ed770979595d63bf9d2ec281ef0}.
\]

## Byte-level reconstruction

The current proof source is untracked at the worktree base, so an ordinary
Git diff cannot supply an earlier blob. I therefore tested the declared
edit fail-closed at the byte level.

I applied exactly two inverse text transformations to the current proof
stream:

1. remove the new Status paragraph which records the completed independent
   analytic audit; and
2. restore the former first open item in Section 6,
   “an independent reconstruction of every support, exponent, and power in
   this proof,” then restore the former numbering \(2,\ldots,7\).

The transformed stream has SHA-256

\[
 \texttt{5832c742000f1879874de7170403b2d1a78f44c2c511b6f65a1dd25c5c84deca},
\]

exactly the hash independently audited before the state update. This
identity proves that there is no third, hidden byte change between the old
audited source and the current source.

## Mathematical-content comparison

The two changed blocks contain only audit status and the open-item ledger.
They contain no numbered equation, displayed mathematical formula,
definition, hypothesis, constant, exponent, support condition, stochastic
identity, estimate, theorem statement, or proof step.

In particular, the following audited content is byte-identical across the
rebind:

1. the theorem (0.1) and Theorem 5.1;
2. the corrected interval \(R^2\le t\le65R^2\) in (0.3);
3. the Jensen and common-forward formulae (1.5)--(1.7);
4. the caloric-defect bounds (2.1)--(2.9);
5. the Brownian event and displacement bounds (3.1)--(3.15);
6. the good/bad power and exponent ledgers (4.1)--(4.10); and
7. the factor-four return to the original signed row (5.1)--(5.5).

All numbered formulas and all displayed mathematics are unchanged. The
analytic reasoning audited under the old hash therefore transfers without
alteration to the current hash.

## Rebind conclusion and boundary

The source chain is now

\[
\begin{aligned}
 &\texttt{5832c742000f1879874de7170403b2d1a78f44c2c511b6f65a1dd25c5c84deca}\\
 &\qquad\xrightarrow{\text{two status-only edits}}\\
 &\texttt{0077326ca97cfe40a0a43019caf0118504cf9ed770979595d63bf9d2ec281ef0}.
\end{aligned}
\]

The independent analytic PASS is rebound to the current proof bytes. Its
scope is unchanged: it certifies only the complete nearest-inward
\(k=j-1\) row for the frozen smooth periodic family.

It does not prove the remaining shell synthesis, the full R0.74K signed
condition, a universal endpoint theorem, regularity or singularity for
arbitrary three-dimensional Navier--Stokes data, novelty, or priority.

\[
 \boxed{\text{CURRENT R0.74M SOURCE: PASS; NOT CLAY.}}
\]
