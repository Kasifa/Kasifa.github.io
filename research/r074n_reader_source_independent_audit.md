# R0.74N reader-source independent audit

## 1. Final binding and verdict

This audit compares the Chinese reader source and the locked bilingual
dictionary against the final mathematical proof and its independent
analytic reconstruction.

| Object | SHA-256 |
|---|---|
| research/r074n_all_shell_synthesis.md | ca1ddabb6ea931b2f1a96b5cb000e955492c6852b0ea3b2aaa6148c6f3fa9e1e |
| research/r074n_all_shell_independent_audit.md | 5173ac954ca82e2abc0371258527ddd8b6bc372e43de6c3a2aeea2a9f2b187e9 |
| research/r074n_crossnote_implication_independent_audit.md | 7c289055939cdbf21780337e7da2a1d91109172d89a6c168258703124b50be8a |
| research/r074n_final_source_rebind_audit.md | ea51805047a8dbb3e914f4f29c8f93fd117ff1a22d8320f832af1cab7002042c |
| research/r074n_report-source.md | b3a50fe4aaf9ca1b98d92fa4df3ab3ff3a461163fc9d857c0219cea3a29272c1 |
| research/r074n_bilingual_dictionary.md | d1418d676333293fab29c11d21da053e60f61241068d4b8aaf2565636c270755 |

**Verdict: PASS.** The final reader source preserves the shell theorem, all
required ledgers, the independently audited cross-note endpoint consequence,
and the exact familywise boundary without promoting the result to a universal
Navier--Stokes statement.

The first reader-source pass failed closed. It found five unrendered inline
math fragments, undefined \(c_\gamma,\rho\), and an absolute value applied
to a torus path without naming the selected lift. The final bound source
repairs all of them.  The later cross-note revision was reread independently,
including its component bounds and OPEN list, before this verdict.

## 2. Formula-by-formula correspondence

### A. Exact three-range decomposition

The reader source defines the same observable as the proof:

\[
 \mathcal I_j
 =\sum_{k\ge1}\mathcal J_{j,k}
 =\mathcal I_<+\mathcal I_=+\mathcal I_>,
\]

with the exact disjoint ranges

\[
 1\le k\le j-1,\qquad k=j,\qquad k\ge j+1.
\]

It states explicitly that no \(k\ge1\) shell is omitted. The inherited
R0.74L main-shell estimate is copied at the correct weighted scale
\(C\Gamma_jL_jR_j^5\).

### B. Combined inward chord

The reader source retains the shellwise positive part before summation,
including the weights \(\Gamma_k\). It records both geometric inputs

\[
 \operatorname{length}_{x_1}\le C2^kR_j,\qquad
 |\partial_2\psi_k^{R_j}|\le C/R_j,
\]

and therefore the correct uniform chord bound

\[
 D_<\le C\sum_{k\ge1}2^ke^{-4^{k-1}/32}=C_*.
\]

It also records the exact largest padded radius

\[
 r_-=\left(\frac{32}{63}L_j+\frac18\right)R_j
\]

and correctly distinguishes uniqueness of the compact support lift from
retention of every periodic packet and heat-kernel winding.

### C. Inherited expulsion and the inner ledger

The final reader source uses the selected lift both at the endpoint and
along the final Brownian segment. It reproduces

\[
 \mathbb P(\mathcal H_t^c)\le4e^{-L_j^2/16},
 \qquad
 \Sigma_{L_j}=2^{-15}e^{-L_j^2/640},
\]

\[
 \frac{\Sigma_{L_j}}{L_jR_j}
 =\frac{e^{L_j^2/640}}{32768L_j}\to\infty,
 \qquad
 \operatorname{dist}_{\mathbb T}(u,0)\ge\frac12\Sigma_{L_j}.
\]

The bad-path raw power is \(CR_j^4\), and the exact payment reserve is

\[
 \frac1{16}-\frac1{320}-\frac8{3969}
 =\frac{72851}{1270080}>0.
\]

The good-path line is also exact:

\[
 CR_j^3\exp\!\left[
 -\frac{e^{L_j^2/320}}{1056\cdot32768^2}\right],
\]

which pays \(\Gamma_jR_j^2\). The resulting inner estimate has the correct
positive part and target scale. The prose explicitly retains the
factor-four safe majorant for two packet self terms and the cross term,
without claiming packet cancellation.

### D. Maximum principle and the outer ledger

The reader source preserves the initial packet normalization
\(R_j^3\partial K_{R_j^2}K_{R_j^2}\) and the two heat-kernel powers
\(R_j^{-2}\) and \(R_j^{-1}\). Its maximum-principle conclusion is therefore
the correct uniform bound

\[
 \|F_j(t)\|_\infty\le C.
\]

It states that the collar has two radial faces and records their complete
Euclidean derivative mass

\[
 \int_{\mathbb R^3}|\partial_2\psi_k^{R_j}|\,dx
 \le C4^kR_j^2.
\]

With time length \(4R_j^2\), this gives the same absolute outer majorant as
the proof. The adjacent-term ratio, discrete tail, and family identities
are copied correctly:

\[
 4\exp\!\left(-\frac{3\cdot4^{k-1}}{32}\right),\qquad
 4^{j+1}=\frac{4096}{3969}L_j^2,\qquad
 \frac{\Gamma_{j+1}}{\Gamma_j}=e^{-3c_\gamma L_j^2}.
\]

The repaired constants block now explicitly defines
\(c_\gamma=8/3969\) and \(\rho=1/320\). Thus the displayed outer reserve

\[
 3c_\gamma-\rho=\frac{1237}{423360}>0
\]

is fully defined and agrees with the proof.

The prose says that the estimate is on the complete \(\mathbb R^3\) shell
against the periodic lift. It also states absolute convergence and the
legitimacy of \(N\to\infty\), matching the proof's uniform-Cauchy argument.

### E. Final theorem and scope

The reader theorem is exactly

\[
 \sup_{\tau\in I_{R_j}}[\mathcal I_j(\tau)]_+
 \le C\Gamma_jL_jR_j^5.
\]

It invokes R0.74K only as a sufficient implication to

\[
 \mathfrak C_j\le CB_j^2L_jR_j^2,
\]

then combines the separately inherited lower bound and scale identity to
state the familywise two-sided collar-flux law.  The reader does not pretend
that this shell implication alone proves an endpoint estimate.  It labels the
additional \(X_j\) result as a cross-note synthesis of R0.74F, H, J, and N.

### F. Cross-note endpoint consequence and components

The reader introduces the same scale as the proof,

\[
 T_j=B_j^2L_jR_j^2,
\]

and accurately copies the R0.74H closure

\[
 X_j\le C\left(P_j^{2/3}+\mathfrak C_j\right).
\]

It then uses the R0.74J payment law to obtain
\(P_j^{2/3}\asymp B_j^2R_j^2\le T_j\), and the completed N/K collar result
to obtain \(\mathfrak C_j\le CT_j\).  The resulting upper bound
\(X_j\le CT_j\) is therefore non-circular and at the correct normalization.

For the lower bound, the reader names the correct R0.74F component:

\[
 \mathcal U_{{\rm ext},j}^{\infty}\ge cT_j.
\]

It retains

\[
 X_j=\mathcal U_{{\rm ext},j}^{\infty}
 +\mathcal D_{{\rm ext},j},
 \qquad \mathcal D_{{\rm ext},j}\ge0,
\]

and consequently states exactly

\[
 cT_j\le\mathcal U_{{\rm ext},j}^{\infty}
 \le X_j\le CT_j,
 \qquad
 0\le\mathcal D_{{\rm ext},j}\le CT_j.
\]

The prose immediately says that no bound
\(\mathcal D_{{\rm ext},j}\ge cT_j\) has been proved.  It therefore does not
misattribute the endpoint-energy lower bound to dissipation.  The final
two-sided statement

\[
 X_j\asymp\mathfrak C_j\asymp B_j^2L_jR_j^2
 \asymp P_j^{2/3}\sqrt{1+\log_+P_j}
\]

is restricted throughout to the frozen exact family.

## 3. Evidence labels and terminology lock

The PROVED, INHERITED, FINITE, LITERATURE BOUNDARY, OPEN, and NOT CLAY
sections agree with the bilingual dictionary.

In particular:

- all-shell synthesis means precisely the three frozen index ranges;
- the positive chord and factor four are explicitly cancellation-free;
- the certificate is described as finite arithmetic only;
- the literature search is described as a bounded non-hit, not novelty
  evidence;
- square-root-log saturation for both \(X_j\) and \(\mathfrak C_j\) is
  restricted to the exact family;
- the \(X_j\) law is explicitly described as cross-note synthesis, not as a
  consequence of the shell estimate alone;
- the endpoint exterior-energy lower bound is kept distinct from the
  dissipation upper bound; and
- universal endpoint control, arbitrary-flow collar control,
  payment-to-admissibility, core-from-shell control, singularity control, and
  global regularity remain OPEN.

No terminology entry enlarges the mathematical theorem.

## 4. Source hygiene

For the final reader source:

- tab characters: \(0\);
- carriage returns and other control characters: \(0\);
- inline math delimiters: \(39\) opening and \(39\) closing;
- display math delimiters: \(42\) opening and \(42\) closing; and
- bare-command checks across the known TeX command stems used by this note:
  no unwrapped hit.

For the bilingual dictionary:

- tab characters: \(0\);
- carriage returns and other control characters: \(0\);
- inline math delimiters: \(32\) opening and \(32\) closing; and
- display math delimiters: none required.

\[
 \boxed{\text{R0.74N READER SOURCE: PASS; CROSS-NOTE BOUND; NOT CLAY.}}
\]
