# R0.70Q independent mathematical audit

**Verdict:** conditional **PASS** for the audited snapshot.  No blocking or
major mathematical, scope, citation, or reproducibility defect remains in the
canonical report.

This verdict is deliberately narrower than a Navier--Stokes regularity result.
It accepts the exact covariance and spectral identities, the explicit
counterexample, and the conditional continuation implication.  It does not
accept any unproved propagation statement for the quantities appearing in that
criterion.

## 1. Locked snapshot and audit scope

The final read-only pass used:

- `research/r070q_report-source.md`, SHA-256
  `75cbe17c56188572e5146236756180c8d35fafd3312b9078406cbebcc6614c24`;
- `research/r070q_exact_audit.py`, SHA-256
  `46e170c4b036cd86e6dc67be6bb85113baabb6c889205d8f27b8d8fc81c87cb5`;
- `research/certificates/r070q/result.json`, SHA-256
  `5716f52df687ca7d7337f8096ac75b1c70f6e81173df0090168f980488bd8b40`;
- the R0.70P frame bridge and projector proof in
  `research/r070p_report-source.md` and
  `research/r070p_projector_miller_audit.md`.

The audit independently re-derived the row-gradient vorticity convention, the
filtered covariance equation, the largest-eigenvalue curvature terms, the new
rank-one absorption proposition, every general-amplitude Beltrami constant,
the no-go quantifiers, and the complete logical chain in Theorem 8.1.

## 2. Covariance and spectral calculus

With

\[
 B_{ij}=\partial_i u_j,
 \qquad
 \mathscr L_\nu=\partial_t+u\mathbin\cdot\nabla-\nu\Delta,
\]

the stretching term is (B^{\mathsf T}\omega), not (B\omega).  For

\[
 \mathscr L_\nu\Omega_\alpha
 =B^{\mathsf T}\Omega_\alpha+\mathcal E_\alpha,
\]

direct product differentiation gives

\[
 \mathscr L_\nu Q
 =B^{\mathsf T}Q+QB+\mathcal F_Q-2\nu\mathcal H_Q.
\]

In particular, the viscous gradient-covariance sign is negative and its
coefficient is two.  Taking the trace gives the report's equation for (E).

At a simple top eigenvalue, set (L=v_1\otimes v_1), (P=I-L), and
(r=\operatorname{tr}(PQ)).  The report defines the half-curvature

\[
 \mathcal K_Q
 =\sum_{k,b>1}
 \frac{|v_b^{\mathsf T}(\partial_kQ)v_1|^2}
      {\lambda_1-\lambda_b}.
\]

The exact certificate instead denotes (K=2\mathcal K_Q).  Thus the two
conventions are equivalent, and the correct identities in report notation are

\[
 \Delta r=P:\Delta Q-2\mathcal K_Q,
 \qquad
 \mathscr L_\nu r=P:\mathscr L_\nu Q+2\nu\mathcal K_Q.
\]

There is no factor-two or sign mismatch between the report and certificate.
The expanded residual equation follows by using (PQ=QP).

## 3. Sharp rank-one diffusion absorption

Suppose (Q=EL) at the point under consideration, with (E>0).  Positivity
of the summands in (Q=\sum_\alpha\Omega_\alpha\otimes\Omega_\alpha) forces

\[
 \Omega_\alpha=a_\alpha v_1,
 \qquad
 \sum_\alpha a_\alpha^2=E.
\]

Writing (h_{\alpha k}=P\partial_k\Omega_\alpha), differentiation gives

\[
 P(\partial_kQ)v_1=\sum_\alpha a_\alpha h_{\alpha k}.
\]

Because both lower eigenvalues are zero,

\[
 \mathcal K_Q
 =\frac1E\sum_k\left|\sum_\alpha a_\alpha h_{\alpha k}\right|^2
 \leq\sum_{\alpha,k}|h_{\alpha k}|^2.
\]

This proves the nonpositive net diffusion contribution asserted in
Proposition 4.1.  The coefficient one is sharp: for the rotating Beltrami
family, (h_{\alpha k}) is proportional to (a_\alpha), so equality holds.
The proposition is pointwise and does not, by itself, provide a quantitative
near-rank-one estimate when (r>0).

## 4. General-amplitude Beltrami check

For

\[
 a_N(t)=\varepsilon_Ne^{-\nu N^2t},
 \qquad
 u_N=-a_N(0,\cos Nx_1,\sin Nx_1),
\]

the independently recomputed identities are

\[
 \omega_N=-Nu_N,
 \qquad
 B^{\mathsf T}\omega_N=0,
 \qquad
 E_N=\varepsilon_N^2N^2e^{-2\nu N^2t},
\]

\[
 Q_N=E_NL_N,
 \qquad
 R_N=0,
 \qquad
 \frac{\lambda_1-\lambda_2}{E_N}=1,
 \qquad
 |\nabla P_N|_F=\sqrt2N,
\]

and

\[
 \mathcal H_{Q_N}=E_NN^2w_N\otimes w_N,
 \qquad
 \mathcal K_{Q_N}=E_NN^2.
\]

Consequently

\[
 -2\nu P_N:\mathcal H_{Q_N}+2\nu\mathcal K_{Q_N}=0.
\]

The exact commutator square also vanishes.  With normalized Haar measure, the
weighted direction cost is

\[
 \mathfrak W_{L_N}(0,T)
 =\frac{\varepsilon_N^4N^2}{2\nu}
   \left(1-e^{-4\nu N^2T}\right),
\]

including at (T=\infty).  All powers of (N), factors of two, and
dependences on (\varepsilon_N) in the report are correct.

## 5. No-go boundary

For the Bessel-potential convention,

\[
 \|u_N(0)\|_{H^m}^2
 =\varepsilon_N^2(1+N^2)^m.
\]

Thus (\varepsilon_N=(1+N^2)^{-m/2}) gives the exact value one.  The choice
(\varepsilon_N=e^{-N}) sends the initial data to zero in every fixed smooth
seminorm while leaving ( |\nabla P_N|_F=\sqrt2N).  Theorem 7.1 therefore
correctly rules out a bound whose right-hand side is locally bounded in any
fixed finite collection of amplitude-sensitive Sobolev inputs, the residual,
and the relative gap near this sequence.

It does **not** rule out an estimate containing an absolute covariance floor,
an absolute gap, a frequency moment, an initial direction norm, an infinite
analytic/Gevrey-type input, or another structure-sensitive quantity.  It also
does not exhibit dynamic projector growth or a singular solution.  The final
report states these limitations explicitly.

## 6. Theorem 8.1 dependency audit

The conditional theorem follows from two already audited R0.70P components.
First, the complete-frame identity gives

\[
 \|P\omega\|_{L_t^4L_x^2}
 \leq a_0^{-1/2}
 \left(
  \|R\|_{L_t^2}^{1/2}
  +\|\mathfrak C_P\|_{L_t^2}^{1/2}
 \right).
\]

Second, the orientation-free integration-by-parts argument gives

\[
 Z_L^2
 \leq\frac18\|P\omega\|_2^4
 +2\|u_*\|_2^2\|\nabla u\|_2^2
    \|\nabla L\|_\infty^2.
\]

The stated assumptions therefore imply (Z_L\in L^2_t).  The middle positive
strain eigenvalue then lies in (L_t^4L_x^2); the periodic strain estimate,
Gagliardo--Nirenberg and Young inequalities, Gronwall, and the periodic
(H^1) blow-up alternative yield continuation.  The argument uses only
spatial weak derivatives of (L) and no time derivative or global orientation.

Theorem 8.1 is consequently valid for the stated maximal (H^1) mild/strong
solution class.  It is not a theorem about arbitrary Leray--Hopf solutions.
Its weighted hypothesis is the weaker condition already isolated in the
R0.70P projector audit, rather than an unannounced consequence of mere local
boundedness of (\nabla L).

## 7. Corrections closed during audit

Four scope or notation issues found in earlier snapshots were corrected before
this verdict:

1. the universal-sounding `Energy-only propagation: FAIL` was narrowed to
   failure of direct Leray-energy closure for the displayed covariance ledger;
2. the stretching-defect prose was changed from (B\omega) to
   (B^{\mathsf T}\omega), matching the fixed row-gradient convention;
3. the no-go conclusion now quantifies the required local boundedness of the
   proposed right-hand side;
4. criticality of the weighted cost is described as formal criticality under
   the usual (\mathbb R^3) scaling, rather than literal scale invariance of a
   fixed torus.

An independent second cross-check of the final snapshot found no remaining
blocker or major issue in Proposition 4.1, Theorem 7.1, or Theorem 8.1.

## 8. Reproducibility replay

The producer was rerun independently to a temporary output.  That output was
byte-identical to the archived `result.json`, with SHA-256
`5716f52df687ca7d7337f8096ac75b1c70f6e81173df0090168f980488bd8b40`.
All five entries in `research/certificates/r070q/SHA256SUMS` verified.  The
focused Node gate
`tests/r070q-covariance-evolution-gate.test.mjs` passed 8/8 tests.

The finite producer checks matrix, differential-polynomial, spectral, and
explicit-mode identities.  It does not computer-prove the infinite
Littlewood--Paley theorem, covariance-PDE propagation, the external periodic
continuation machinery, or global Navier--Stokes regularity.

## 9. Final boundary

The current R0.70Q snapshot passes as a rigorous route gate and conditional
theorem package.  The unresolved mathematical task is exactly the one the
report retains: derive (R\in L_t^2), the exact commutator-square bound, and
the weighted direction cost from genuinely subcritical or structural
Navier--Stokes information without reintroducing the target continuation norm.
Until that propagation step is proved, R0.70Q is not progress resolving the
Millennium problem in the sense of a regularity theorem.
