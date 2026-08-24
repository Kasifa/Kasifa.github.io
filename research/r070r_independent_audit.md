# R0.70R independent mathematical audit

**Verdict:** conditional **PASS** for the locked snapshot below.  There is no
remaining blocker or major mathematical, scope, citation, or reproducibility
defect in the canonical report.

The condition is substantive: R0.70R proves a sharp pointwise estimate for the
diffusion part of the covariance-residual ledger.  It does not prove that the
required near-rank-one condition or palinstrophy term propagates under the
Navier--Stokes equation.

## 1. Locked snapshot and scope

The final audit used:

- `research/r070r_report-source.md`, SHA-256
  `0c96025a07a61bbeb22becd8fa78705e4a5bf9f113620db9881aa17dd684b208`;
- `research/r070r_exact_audit.py`, SHA-256
  `6658a1d88cb75af970415a8973571aaf56acab372a03e6a520fea39b42f9c2d8`;
- `research/certificates/r070r/result.json`, SHA-256
  `c83bffb27fb0cafbf60468526e8ead154a1f79eeffa070d5afcb8b1f9d4387f7`;
- `tests/r070r-near-rank-diffusion-gate.test.mjs`, SHA-256
  `6b3e0cee039f9884e9c2b689fe89cbf697ddf6e72dc6de383face0b5a46edea8`.

The audit independently checked:

1. the finite or countable coefficient-space theorem and all convergence
   requirements;
2. the reduced-resolvent, synthesis-operator, and direct-sum estimates;
3. the scalar sum-of-squares identity and optimal constant;
4. the abstract sharp jet and its exact realization by the fixed R0.70P frame;
5. the global shear heat-flow realization and positive-time tuning;
6. the residual-ratio form, including the threshold (c_\eta<1);
7. the precise limitation of Section 7 to the diffusion part of the ledger.

## 2. Infinite-frame theorem

At one point, let

\[
 Q=\sum_\alpha\Omega_\alpha\otimes\Omega_\alpha,
 \qquad
 \lambda_1>\lambda_2\geq\lambda_3\geq0,
\]

and let (v_1,L,P) have the meanings fixed in the report.  For a finite or
countable index set, the final theorem assumes

\[
 (\Omega_\alpha)_\alpha\in\ell^2(\mathcal I;\mathbb R^3),
 \qquad
 (\partial_k\Omega_\alpha)_\alpha
 \in\ell^2(\mathcal I;\mathbb R^3),
 \quad k=1,2,3.
\]

These assumptions are sufficient.  The covariance series converges in trace
and Frobenius norm, while

\[
 \sum_\alpha
 \bigl(
  \partial_k\Omega_\alpha\otimes\Omega_\alpha
  +\Omega_\alpha\otimes\partial_k\Omega_\alpha
 \bigr)
\]

converges absolutely in Frobenius norm by Cauchy--Schwarz.  Thus no implicit
exchange of a conditionally convergent infinite frame sum is used.

Define

\[
 a_\alpha=v_1\cdot\Omega_\alpha,
 \quad b_\alpha=P\Omega_\alpha,
 \quad c_{\alpha k}=v_1\cdot\partial_k\Omega_\alpha,
 \quad h_{\alpha k}=P\partial_k\Omega_\alpha.
\]

Then

\[
 \sum_\alpha a_\alpha^2=\lambda_1,
 \qquad
 \sum_\alpha b_\alpha\otimes b_\alpha=PQP.
\]

The synthesis map (z\mapsto\sum_\alpha z_\alpha b_\alpha) therefore has
operator norm (sqrt{\lambda_2}).  Direct differentiation gives the exact
identity

\[
 y_k:=P(\partial_kQ)v_1
 =\sum_\alpha
  \left(a_\alpha h_{\alpha k}+c_{\alpha k}b_\alpha\right).
\]

Writing

\[
 \mathcal D_P=\sum_{\alpha,k}|h_{\alpha k}|^2,
 \qquad
 \mathcal D_L=\sum_{\alpha,k}|c_{\alpha k}|^2,
\]

Cauchy--Schwarz and the triangle inequality in the direct-sum Hilbert space
give

\[
 \left(\sum_k|y_k|^2\right)^{1/2}
 \leq
 \sqrt{\lambda_1\mathcal D_P}
 +\sqrt{\lambda_2\mathcal D_L}.
\]

Finally,

\[
 0\leq\mathcal R_Q
 \leq(\lambda_1-\lambda_2)^{-1}P
\]

proves

\[
 \mathcal K_Q
 \leq
 \frac{
  \left(
   \sqrt{\lambda_1\mathcal D_P}
   +\sqrt{\lambda_2\mathcal D_L}
  \right)^2}
 {\lambda_1-\lambda_2}.
\]

This proof is valid for the report's half-curvature convention
(\mathcal K_Q), not for the doubled variable (K=2\mathcal K_Q) used
internally by the older R0.70Q certificate.

## 3. Exact scalar optimization

Put

\[
 s=\sqrt\rho,
 \qquad
 X=\sqrt{\mathcal D_P},
 \qquad
 Y=\sqrt{\mathcal D_L}.
\]

The independently expanded sum-of-squares identity is

\[
 \mathcal D_P
 +\frac{s}{1-s}(\mathcal D_P+\mathcal D_L)
 -\frac{(X+sY)^2}{1-s^2}
 =\frac{s(X-Y)^2}{1-s^2}\geq0.
\]

Consequently

\[
 \boxed{
 \mathcal D_P-\mathcal K_Q
 \geq
 -\frac{\sqrt\rho}{1-\sqrt\rho}
  (\mathcal D_P+\mathcal D_L).}
\]

The same coefficient is the largest eigenvalue of

\[
 \frac1{1-\rho}
 \begin{pmatrix}
  \rho&\sqrt\rho\\
  \sqrt\rho&\rho
 \end{pmatrix}.
\]

Its maximizing vector has (X=Y), which is admissible.  Hence this is an
attained optimum, not merely a convenient majorant.  For $\rho=0$, the
coefficient is zero and the result reduces to the R0.70Q rank-one absorption.
The equation tags in the final report are unique and the SOS, matrix, and
eigenvalue formulas are mutually consistent.

## 4. Abstract and numerical sharpness jets

Let (v,w) be orthonormal and choose (A>\beta>0).  With one spatial
derivative, take

\[
 \Omega_1=Av,
 \quad \Omega_2=\beta w,
 \quad \partial\Omega_1=pw,
 \quad \partial\Omega_2=qv.
\]

Then

\[
 (\lambda_1,\lambda_2,\lambda_3)=(A^2,\beta^2,0),
 \quad
 \mathcal D_P=p^2,
 \quad
 \mathcal D_L=q^2,
\]

and

\[
 \mathcal K_Q=\frac{(Ap+\beta q)^2}{A^2-\beta^2}.
\]

Taking (p=q\ne0) attains every inequality above.  In particular, the exact
rational jet

\[
 \Omega_1=3e_1,
 \quad \Omega_2=e_2,
 \quad \partial\Omega_1=2e_2,
 \quad \partial\Omega_2=2e_1
\]

has

\[
 Q=\operatorname{diag}(9,1,0),
 \quad
 \mathcal D_P=\mathcal D_L=4,
 \quad
 \mathcal K_Q=8,
 \quad
 c(1/9)=\frac12,
\]

so

\[
 \mathcal D_P-\mathcal K_Q=-4
 =-\frac12(\mathcal D_P+\mathcal D_L).
\]

## 5. Fixed-frame and Navier--Stokes realization

The sharpness is realized by the fixed R0.70P scalar frame, not only by
independent abstract blocks.  Because its symbol is compactly supported in an
annulus, integers (k,\ell) can be chosen far enough apart that their active
index sets are disjoint.  Real-evenness ensures that each sine/cosine pair is
multiplied by the same real coefficient, and tightness gives coefficient
square sum one in each group.

For orthonormal (v,w\perp e_1), let

\[
 \omega_0
 =A\cos(kx_1)v+\frac pk\sin(kx_1)w
 +\beta\cos(\ell x_1)w+\frac q\ell\sin(\ell x_1)v.
\]

At (x_1=0), the two disjoint filter groups give exactly

\[
 Q=A^2v\otimes v+\beta^2w\otimes w,
 \quad
 \mathcal D_P=p^2,
 \quad
 \mathcal D_L=q^2,
 \quad
 \mathcal K_Q=\frac{(Ap+\beta q)^2}{A^2-\beta^2}.
\]

The field is smooth, mean zero, and divergence free.  The periodic
Biot--Savart velocity

\[
 u_0=\nabla\times(-\Delta)^{-1}\omega_0
\]

is transverse to (e_1) and depends only on (x_1).  Therefore
((u_0\cdot\nabla)u_0=0), and (e^{\nu t\Delta}u_0) is a smooth global
unforced Navier--Stokes shear solution.

The positive-time tuning in the report is also correct.  At a prescribed
(t_*>0),

\[
 p_*=pe^{-\nu k^2t_*},
 \qquad
 q_*=qe^{-\nu\ell^2t_*}.
\]

For (\ell>k), choosing

\[
 \frac pq=e^{-\nu(\ell^2-k^2)t_*}
\]

gives (p_*=q_*).  Since (A>\beta), the top eigenvalue remains the
(k)-frequency branch.  Thus equality can be arranged at any chosen positive
time.  Different heat-decay rates prevent one fixed nontrivial datum from
maintaining the equality relation for every time.

This construction proves optimality even in the class of snapshots from the
fixed LP frame and smooth global NSE solutions.  It does not prove persistence
or propagation of the sharp geometry.

## 6. Residual-ratio form

If (E>0) and (eta=r/E<1/2), then

\[
 \lambda_1=(1-\eta)E,
 \qquad
 \lambda_2\leq\eta E,
 \qquad
 \rho\leq\frac\eta{1-\eta}.
\]

Monotonicity of (c(\rho)) yields

\[
 c_\eta
 =\frac{\sqrt\eta}
        {\sqrt{1-\eta}-\sqrt\eta},
 \qquad
 \mathcal D_P-\mathcal K_Q\geq-c_\eta\mathcal G.
\]

The example with (lambda_3=0) attains this coefficient, since then
$\rho=\eta/(1-\eta)$.  Direct expansion gives

\[
 c_\eta=\sqrt\eta+O(\eta)
 \quad(\eta\downarrow0).
\]

Moreover, on (0\leq\eta<1/2),

\[
 c_\eta<1
 \iff
 2\sqrt\eta<\sqrt{1-\eta}
 \iff
 \eta<\frac15.
\]

The condition is pointwise.  A bound on the spatial residual
(R=\int r) does not imply it, particularly on low-(E) regions.

## 7. Diffusion-only scope

The R0.70Q residual equation contains

\[
 -2\nu\mathcal D_P+2\nu\mathcal K_Q,
\]

so R0.70R proves only

\[
 -2\nu\mathcal D_P+2\nu\mathcal K_Q
 \leq2\nu c_\eta\mathcal G.
\]

For (Phi_\mu=r+\mu E), the notation
(operatorname{Diff}(\mathscr L_\nu\Phi_\mu)) in the final report is
explicitly limited to the gradient-covariance and spectral-curvature source
terms.  Hence

\[
 \operatorname{Diff}(\mathscr L_\nu\Phi_\mu)
 \leq-2\nu(\mu-c_{\eta_0})\mathcal G
\]

states coercivity of this diffusion part only.  Stretching, transport/filter
commutators, and the propagation of the ratio remain outside the estimate.

After spatial integration, tightness gives

\[
 \int_{\mathbb T^3}\mathcal G\,dx
 =\sum_\alpha\|\nabla T_\alpha\omega\|_2^2
 =\|\nabla\omega\|_2^2.
\]

Thus the error is palinstrophy, one derivative above kinetic energy.  Adding
(\mu E) cannot be called an energy-level closure, because a uniform bound on
(int\Phi_\mu) already contains the target enstrophy bound.

The next-gate integral is correctly restricted to
({E>0, r/E\leq\eta_0}).  The report separately identifies (E=0) and
the non-simple top-spectrum set as requiring an extension or regularization
rule, so no undefined (0/0) ratio is silently used.

## 8. Corrections closed during audit

The following issues found in an earlier snapshot were corrected before this
verdict:

1. Theorem 4.1 now states the full countable-frame (ell^2) hypotheses and
   the norm-convergent derivative series;
2. the next-gate domain excludes (E=0) and routes spectral degeneracy
   separately;
3. the Rayleigh-quotient sentence and equation references are syntactically
   unambiguous;
4. positive-time equality includes the exact heat-decay tuning;
5. the accidental symbol (Phi_\beta) was corrected to (Phi_\mu);
6. Section 7 now defines `Diff` and states only diffusion-part coercivity.

No additional blocker or major issue appeared after these corrections.

## 9. Reproducibility and final boundary

The exact producer was independently rerun to a temporary path.  The result
was byte-identical to the archived `result.json`, with SHA-256
`c83bffb27fb0cafbf60468526e8ead154a1f79eeffa070d5afcb8b1f9d4387f7`.
All five entries in `research/certificates/r070r/SHA256SUMS` verified, and the
focused Node gate passed 8/8 tests.

The finite certificate verifies the algebraic candidate, the scalar SOS, the
rational sharp jet, and a finite disjoint-frame realization.  The analytic
argument in the report supplies the countable-frame extension and global shear
heat-flow interpretation.  Neither component proves covariance-PDE closure,
propagation of (R\in L_t^2), a continuation theorem, blow-up, or global
regularity for arbitrary three-dimensional Navier--Stokes data.
