# R0.70P independent audit

**Audit date:** 2026-08-25

**Decision:** **CONDITIONAL PASS** for the theorem scope stated in the canonical
report

**Unresolved report defects:** none at BLOCKER, MAJOR, or MINOR level

**Public-release decision:** not made by this audit

The qualifier “conditional” has one precise meaning: the negative-one-order
square commutator uses the cited Calderón--Coifman--Meyer first-order
commutator theorem as an external analytic input.  R0.70P verifies the
uniform symbol hypotheses and derives the square estimate from that theorem,
but does not reprove the external theorem.  The qualifier does **not** hide a
remaining algebraic, zero-mode, time-exponent, continuation, or window-defect
gap in the current report.

## 1. Audited snapshot and method

The final read-only pass used the following canonical snapshot:

- `research/r070p_report-source.md`, SHA-256
  `31b7912fe45b3cea98b1e1e740e8fea20bde910fe6855be652875303bcd8cbbc`;
- `research/r070p_exact_audit.py`, SHA-256
  `96f55f413dd7c31af6bdd22e71de6c2b47af906ecc5f96a48b6c293c8ee09376`;
- `research/certificates/r070p/result.json`, SHA-256
  `a591393f937c107c1a19e2510c87861e8e2ea7194b01bedca6b17a3084c11d2f`.

The audit independently rederived, rather than merely pattern-matched, the
following chain:

1. completeness of the Euclidean and periodic scalar frames, including the
   periodic constant block;
2. the abstract lower-frame/commutator bridge and its time-norm conversion;
3. finite Rademacher randomization, uniform multiplier seminorms, and the
   first-order operator decomposition;
4. the separate periodic zero-mode commutator estimate;
5. the bounded-weight estimate and the normalized one-mode obstruction for
   unbounded weights;
6. the energy-level vorticity identity and Theorem 6.1's exact time
   exponents;
7. the spectral-projector gradient bound;
8. the periodic orientation-free projector continuation argument;
9. the combined finite-endpoint continuation theorem; and
10. the additional defect created by spatial covariance windows.

The report was also compared with
`research/r070p_commutator_audit.md`,
`research/r070p_projector_miller_audit.md`, and
`research/r070p_literature_audit.md`.  Formula labels in the canonical report
are unique; in particular, (4.10), (4.10a), (4.10b), and (4.11) do not
collide.

## 2. Complete-frame and zero-mode audit

For the normalized annular profile

\[
 d(\xi)^2=\sum_j|\eta(2^{-j}\xi)|^2,
 \qquad \varphi=\eta/d,
\]

finite overlap, positivity of \(d\) away from zero, and dyadic invariance
\(d(2^k\xi)=d(\xi)\) give

\[
 \sum_j|\varphi(2^{-j}\xi)|^2=1
 \qquad(\xi\ne0).
\]

Thus the homogeneous family is a tight frame on \(L^2(\mathbb R^3)\).  On
\(\mathbb T^3\), the nonzero-mode annular family alone is **not** complete on
the quantity to which the lower frame is applied.  The current report
correctly adjoins

\[
 T_\star=\Pi_0,
 \qquad
 \{T_\alpha\}_{\alpha\in\{\star\}\cup\mathbb Z},
\]

and obtains the full periodic Parseval identity.  Although
\(\Pi_0\omega=0\), generally

\[
 \Pi_0(P\omega)=[\Pi_0,P]\omega\ne0.
\]

Consequently the constant block contributes neither to \(Q\) nor directly to
\(R\), but it is indispensable in the lower-frame reconstruction of
\(P\omega\).  The current Theorem 4.2 includes this block, and the separate
estimate is valid: for zero-mean \(f\),

\[
 [\Pi_0,A]f=\Pi_0(Af),
\]

while homogeneous \(H^{-1}\)--\(H^1\) duality on the normalized torus gives

\[
 \|\Pi_0(Af)\|_2
 \lesssim_m
 \|f\|_{\dot H^{-1}_\#}\|\nabla A\|_{L^2}
 \lesssim_m
 \|f\|_{\dot H^{-1}_\#}\|\nabla A\|_\infty.
\]

This closes the formerly missing periodic zero mode without inserting an
\(L^2\)-vorticity norm on the right.

## 3. Abstract bridge and endpoint square commutator

The block identity

\[
 T_\alpha(Pf)=PT_\alpha f+[T_\alpha,P]f
\]

and the lower-frame inequality, followed by the triangle inequality in
\(\ell^2_\alpha(L^2_x)\), give exactly

\[
 \sqrt{a_0}\|Pf\|_2
 \le
 \left(\sum_\alpha\|PT_\alpha f\|_2^2\right)^{1/2}
 +\left(\sum_\alpha\|[T_\alpha,P]f\|_2^2\right)^{1/2}.
\]

There is no hidden synthesis assumption in this step.

For a finite set \(F\subset\mathbb Z\), the randomized operator

\[
 M_{\varepsilon,F}=\sum_{j\in F}\varepsilon_jT_j
\]

satisfies the exact identity

\[
 \mathbb E_\varepsilon
 \|[M_{\varepsilon,F},A]f\|_2^2
 =\sum_{j\in F}\|[T_j,A]f\|_2^2.
\]

Finite annular overlap gives symbol bounds uniform in \(F\) and the signs.
With \(\Lambda=|D|\), the operator identity

\[
 [M_{\varepsilon,F},A]\Lambda
 =[M_{\varepsilon,F}\Lambda,A]
 +M_{\varepsilon,F}[A,\Lambda]
\]

has the correct sign and no omitted term.  The first multiplier is uniformly
of order one and the second factor is uniformly of order zero.  Applying the
cited first-order commutator theorem and then monotone convergence proves the
annular square estimate.  The periodic constant block is added by the direct
duality argument in Section 2 above.

The external source boundary is stated accurately.  Coifman--Meyer Theorem 2
on pp. 179--180 supplies the order-one multilinear commutator estimate with
constants controlled by symbol bounds; its Section 5 supplies the Lipschitz
endpoint, and its introduction treats the compact-manifold localization.
The R0.70P square-function statement is not attributed verbatim to that
paper: it is the finite-randomization consequence proved in the report.

## 4. Weight boundary

For \(0\le w_j\le W\), pulling out \(\sqrt W\) from the square sum gives the
claimed bounded-weight estimate.

The counterexample is normalized correctly on the torus.  With
\(A=\cos x_1\),

\[
 f_J=n_Je^{in_Jx_1}e_2,
 \qquad 2^{-J}n_J\longrightarrow\rho,
\]

one has

\[
 \|\nabla A\|_\infty=1,
 \qquad
 \|f_J\|_{\dot H^{-1}_\#}=1.
\]

The two shifted Fourier modes are orthogonal and a first-order Taylor limit
gives

\[
 \|[T_J,A]f_J\|_2
 \longrightarrow
 \frac{\rho}{\sqrt2}|\partial_r\varphi(\rho e_1)|>0.
\]

Hence the weighted norm is at least \(c\sqrt{w_J}\).  The proposition proves
failure of a constant uniform over arbitrary nonnegative weight sequences;
it does not claim that every individual unbounded sequence defines a frame.

## 5. Energy-level and spectral bridge

For divergence-free velocity,

\[
 \|\omega\|_{\dot H^{-1}(\mathbb R^3)}=\|u\|_2,
 \qquad
 \|\omega\|_{\dot H^{-1}_\#(\mathbb T^3)}=\|u-\bar u\|_2.
\]

Therefore

\[
 \mathcal C(t)^{1/2}
 \lesssim
 \|\nabla P(t)\|_\infty\|u_*(t)\|_2.
\]

The time conversion in Theorem 6.1 is exact:

\[
 \|\mathcal C^{1/2}\|_{L_t^4}
 \le C
 \|u_*\|_{L_t^\infty L_x^2}
 \|\nabla P\|_{L_t^4L_x^\infty},
 \qquad
 \|R^{1/2}\|_{L_t^4}=\|R\|_{L_t^2}^{1/2}.
\]

No extra time-length factor and no \(L_t^4L_x^2\) vorticity norm is hidden on
the right side.

For a simple top eigenvalue of a weakly differentiable symmetric covariance,
diagonalizing \(Q\) shows

\[
 |\partial_iP|_F^2
 =2\sum_{b=2}^3
 \frac{|(\partial_iQ)_{1b}|^2}{(\lambda_1-\lambda_b)^2}
 \le
 \frac{|\partial_iQ|_F^2}{(\lambda_1-\lambda_2)^2}.
\]

Thus the Frobenius projector-gradient bound and the factor
\(\gamma^{-1}|\nabla Q|/\operatorname{tr}Q\) are correct.  The report also
correctly refuses to infer control at \(E=0\) without an additional projector
extension or zero-set lemma.

## 6. Periodic projector continuation theorem

Theorem 8.1 matches the separately derived projector audit.  Its assumptions
are for a maximal unforced periodic \(H^1\) mild/strong solution and include
endpoint-uniform spatial Lipschitz control of a rank-one projector.  Mere
local boundedness on compact subintervals of \([0,T_{\max})\) is correctly
excluded.

With the row-gradient convention \(B_{ij}=\partial_i u_j\), the
orientation-free pointwise identity is

\[
 \operatorname{tr}(LS^2)-\frac14|P\omega|^2
 =B_{ij}B_{ki}L_{jk}.
\]

Periodic integration by parts, performed after subtracting the conserved
velocity mean, gives

\[
 \int B_{ij}B_{ki}L_{jk}
 =-\int \widetilde u_j\,\partial_k u_i\,\partial_iL_{jk}.
\]

Consequently, for
\(Z_L=\int\operatorname{tr}(LS^2)\),

\[
 Z_L
 \le \frac14\|P\omega\|_2^2
 +C\|\widetilde u\|_2\|\nabla u\|_2\|\nabla L\|_\infty,
\]

and the energy equality yields \(Z_L\in L_t^2\).  If
\(\mu_1\le\mu_2\le\mu_3\) are the trace-free strain eigenvalues, then
\(|\mu_2|=\min_i|\mu_i|\), so

\[
 \|\mu_2^+(t)\|_2^2\le Z_L(t).
\]

The periodic strain identity, determinant inequality, zero-mean
Gagliardo--Nirenberg estimate, Young inequality, and Gronwall therefore give
a uniform \(H^1\) bound.  The periodic \(H^1\) blow-up alternative closes the
extension argument.  The proof uses neither a global oriented lift of \(L\)
nor a time derivative of \(L\), and it makes no claim for arbitrary
Leray--Hopf solutions or forced equations.

Theorem 9.1 now explicitly assumes \(T_{\max}<\infty\).  This is essential:
only on a finite interval does endpoint-uniform \(L_t^\infty\) control of
\(\nabla P\) imply the \(L_t^4\) hypothesis in Theorem 6.1.  With that
condition present, Theorems 4.2, 6.1, and 8.1 compose without a missing
endpoint step.

## 7. Spatial-window defect

For a windowed covariance, the report now distinguishes the observable

\[
 R_K=\int\operatorname{tr}(P Q_K)
\]

from the same-point residual \(R\).  For nonnegative normalized kernels,

\[
 P(y)\Omega_j(y)
 =P(x)\Omega_j(y)+(P(y)-P(x))\Omega_j(y)
\]

and \(|a+b|^2\le2|a|^2+2|b|^2\) give exactly

\[
 \sum_j\|P\Omega_j\|_2^2\le2R_K+2D.
\]

If the second kernel moment is \(O(2^{-2j})\), Lipschitz continuity of \(P\)
and annular support give

\[
 D
 \lesssim
 \|\nabla P\|_\infty^2
 \sum_j2^{-2j}\|T_j\omega\|_2^2
 \lesssim
 \|\nabla P\|_\infty^2\|u_*\|_2^2.
\]

The Euclidean/periodic kernel normalization and the periodic-distance
convention are now explicit.  The canonical R0.70P theorem uses the
same-point covariance, so this window term is a recorded future-model defect,
not a hidden hypothesis in Theorem 9.1.

## 8. Issues found and resolved during the audit

Three issues were blocking or materially weakening the earlier snapshot.
All three are resolved in the audited snapshot.

1. **Periodic zero-mode blocker — resolved.**  The annular frame originally
   omitted the constant block even though \(P\omega\) can have nonzero mean.
   The report now adjoins \(T_\star=\Pi_0\), uses the full lower frame, and
   proves the separate \(\dot H^{-1}_\#\)--\(\dot H^1_\#\) commutator bound.
2. **Finite-endpoint hypothesis — resolved.**  The combined continuation
   theorem originally did not state \(T_{\max}<\infty\), so uniform-in-time
   control did not imply an \(L_t^4\) bound on a possibly infinite interval.
   The finite-endpoint hypothesis is now explicit.
3. **Window residual mismatch — resolved.**  The window inequality originally
   reused the same-point symbol \(R\).  The report now defines \(R_K\) and
   proves the correct inequality \(\sum_j\|P\Omega_j\|_2^2\le2R_K+2D\).

The final cleanup also defines \(u_*\) on both domains, pins the integer
sequence and vector frequencies in the weight obstruction, states weak
spatial differentiability of \(Q\), specifies periodic kernel geometry, and
links the archived certificate.

## 9. Reproducibility result

The exact producer was rerun independently with the pinned environment and a
temporary output path.  The regenerated JSON was byte-identical to
`research/certificates/r070p/result.json`; its SHA-256 is

```text
a591393f937c107c1a19e2510c87861e8e2ea7194b01bedca6b17a3084c11d2f
```

All entries in `research/certificates/r070p/SHA256SUMS` pass when checked from
the certificate directory.  The producer covers finite symbolic projector
algebra, periodic integration by parts, Rademacher orthogonality, normalized
weight scaling, the periodic constant block, and finite-dimensional bridge
tests.  It does not computer-prove the infinite-dimensional commutator theorem
or the Navier--Stokes continuation argument, and the report does not claim
otherwise.

## 10. Remaining research boundary

R0.70P closes a conditional harmonic-analysis-to-continuation bridge.  It
does not propagate the bridge hypotheses from Navier--Stokes data.  A future
stage must still obtain, without using an equivalent of the desired critical
vorticity norm,

\[
 R\in L_t^2,
 \qquad
 \lambda_1-\lambda_2\ge\gamma\operatorname{tr}Q,
 \qquad
 \frac{|\nabla Q|}{\operatorname{tr}Q}
 \in L_t^4L_x^\infty,
\]

together with a legal projector extension across \(E=0\) and
endpoint-uniform control of \(\nabla P\).  Any derivation that requires
\(\|\omega\|_{L_t^4L_x^2}\), \(\|\nabla\omega\|_\infty\), or a comparable
regularity norm is circular and must stop.

Accordingly, this audit supports the canonical report's conditional theorem
scope.  It does not support a global-regularity claim, a singularity claim, a
novelty/priority claim, or a claim to have solved the Navier--Stokes
Millennium problem.
