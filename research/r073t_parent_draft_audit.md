# R0.73T parent-draft analytic audit

**Files audited:**

- research/r073t_dynamic_autocorrelation_budget.md
- research/r073t_report-source.md

**Audit mode:** independent line-by-line reconstruction of coefficients,
scaling, Serrin comparison, componentwise nonlinear Bernstein coercivity,
Dini derivatives at zeros, heat-plane signs, claim boundaries, and equation
references

**Verdict:**
PASS_AFTER_ONE_SUBSTANTIVE_SHELL_ZERO_CORRECTION_AND_MINOR_REVISIONS

The full-field mathematics passes.  The pressure constant, exact quartic
balance, scaling law, Dini estimate for \(A\), \(Y_j=Q_j^{1/2}\) shell
transport, componentwise Bernstein deduction, and heat-plane law are
correct.  One shell statement is not valid as written: the
\(X_j=Q_j^{1/4}=\|v_j\|_4\) inequality cannot use the *instantaneous*
autocorrelation support count through a time at which \(v_j=0\), and its
Duhamel form cannot pull a time-dependent support count outside the
integral.  A fixed ambient annular difference-set count repairs both issues.

## 1. Verdict matrix

| Item | Verdict | Required action |
| --- | --- | --- |
| Haar/Fourier normalization | PASS | repair two missing TeX backslashes in the analytic draft |
| coefficient evolution | PASS_EXACT | none |
| quartic balance and factors \(4,2\) | PASS_EXACT | none |
| pressure/Riesz/Young constant | PASS_EXACT | none |
| \(AQ\) Gronwall implication | PASS | none |
| Navier--Stokes scaling of \(A\) | PASS | put corresponding time limits into the public report |
| Serrin comparison | PASS_WITH_WORDING_REVISION | say “at least as restrictive as”; state exponent convention |
| upper-Dini estimate for \(A\) | PASS | none |
| scalar componentwise Bernstein | PASS_WITH_CUTOFF_BOUNDARY | retain fixed-cutoff and low-shell qualification |
| \(Y_j=Q_j^{1/2}\) through zeros | PASS | none |
| \(X_j=Q_j^{1/4}\) through zeros | FAIL_AS_WRITTEN | replace instantaneous \(D_{C,j}\) by a fixed ambient count |
| \(X_j\) Duhamel form | FAIL_AS_WRITTEN | same replacement, or keep a valid time envelope inside the integral |
| forcing bounds | PASS | refine “critical norm” wording |
| heat-plane sign and dissipation | PASS_EXACT | none |
| non-autonomy examples | PASS_EXACT | none |
| novelty/Clay boundary | PASS_STRICT | none |
| equation tags and references | PASS | all tags unique and all explicit references resolve |

## 2. Full-field identities and normalization

With Haar probability measure and

\[
 \widehat f(h)=\int_{\mathbb T^3}f(x)e^{-ih\cdot x}\,d\mu,
 \tag{2.1}
\]

the local density equation is

\[
 \partial_t w
 =\nu\Delta w-2\nu|\nabla u|^2
  -\nabla\cdot\bigl(u(w+2p)\bigr).
 \tag{2.2}
\]

Therefore

\[
 \dot C_h
 =-\nu|h|^2C_h-2\nu\widehat{|\nabla u|^2}(h)
  -ih\cdot\widehat{u(w+2p)}(h),
 \tag{2.3}
\]

exactly as in both drafts.  Multiplication by \(2w\) gives

\[
 Q'+4\nu Y+2\nu X^2
 =4\int_{\mathbb T^3}p\,u\cdot\nabla w\,d\mu.
 \tag{2.4}
\]

The signs and factors agree with both the physical-space derivation and the
independent Fourier audit.  In particular, transport cancels but pressure
does not, and the second viscous term cannot be omitted from (2.3).

### TeX corrections

The analytic draft has two literal occurrences of
\(\int_{mathbb T^3}\) in its displayed equations (3.1) and (3.4).
Both must be \(\int_{\mathbb T^3}\).  This is a rendering error, not a
mathematical coefficient error.

The prose spellings Calderon--Zygmund and Holder may also be normalized to
Calderón--Zygmund and Hölder during copy editing.

## 3. Pressure estimate and exact constant

The chain

\[
 \|p\|_3\le C_R\|u\|_6^2
 \tag{3.1}
\]

and Hölder with exponents \((3,6,2)\) gives

\[
 4\left|\int p\,u\cdot\nabla w\right|
 \le4C_R\|u\|_6^3X.
 \tag{3.2}
\]

Completing the square,

\[
 0\le
 \left(\sqrt\nu X-{2C_R\over\sqrt\nu}\|u\|_6^3\right)^2,
 \tag{3.3}
\]

proves

\[
 4C_R\|u\|_6^3X
 \le\nu X^2+{4C_R^2\over\nu}\|u\|_6^6.
 \tag{3.4}
\]

Substitution in (2.4) leaves exactly

\[
 Q'+4\nu Y+\nu X^2
 \le {4C_R^2\over\nu}AQ.
 \tag{3.5}
\]

Thus \(4C_R^2/\nu\), \(4\nu Y\), and the surviving \(\nu X^2\) are all
correct.  No hidden \((2\pi)^3\) factor occurs under normalized Haar measure.

The \(Q\)-only fallback

\[
 Q'\le C(\nu^{-7}Q^3+\nu^{-1}Q^{3/2})
 \tag{3.6}
\]

also has the correct powers.  It follows from

\[
 \|u\|_6^3
 \lesssim Q^{3/8}(X+\|u\|_2^2)^{3/4}
 \tag{3.7}
\]

and Young exponents \(8/7,8\) and \(2,2\).  Its stated local-only boundary
is correct.

## 4. Scaling and Serrin comparison

For integer \(\lambda\) on the torus,

\[
 u^{[\lambda]}(x,t)=\lambda u(\lambda x,\lambda^2t)
 \tag{4.1}
\]

gives

\[
 C^{[\lambda]}_{\lambda h}(t)
 =\lambda^2C_h(\lambda^2t),
 \qquad
 A^{[\lambda]}(t)=\lambda^2A(\lambda^2t).
 \tag{4.2}
\]

Hence the analytic draft correctly writes

\[
 \int_0^{T/\lambda^2}A^{[\lambda]}(t)\,dt
 =\int_0^TA(s)\,ds.
 \tag{4.3}
\]

The public report's unbounded shorthand
\(\int A^{[\lambda]}(t)dt=\int A(t)dt\) should be replaced by (4.3).
Equality is between corresponding time intervals, not between the same
fixed interval before and after scaling.

Fourier inversion gives

\[
 \|u(t)\|_\infty^2
 =\||u(t)|^2\|_\infty\le A(t),
 \tag{4.4}
\]

so

\[
 A\in L_t^1\Longrightarrow u\in L_t^2L_x^\infty.
 \tag{4.5}
\]

This is the classical LPS equality pair with *time exponent* \(2\) and
*space exponent* \(\infty\): \(2/2+3/\infty=1\).  The drafts' convention
\((p,q)=(2,\infty)\) is correct because they use \(L_t^pL_x^q\), although
many sources reverse the letters.  The public text should state the
time/space convention explicitly and may note that this is not the delicate
\(L_t^\infty L_x^3\) endpoint.

The displayed implication proves that \(A\in L_t^1\) is **at least as
restrictive as** the classical \(L_t^2L_x^\infty\) hypothesis.  The words
“strictly stronger” or Chinese “还强” suggest a strict logical separation
that the displayed inequality alone does not prove.  Recommended wording:
“它至少具有经典 \(L_t^2L_x^\infty\) 端点条件的强度，并且直接蕴含该
条件。”

The continuation paragraph is otherwise correct.  Gronwall bounds
\(Q=\|u\|_4^4\), hence \(u\in L_t^\infty L_x^4\), which lies safely inside
the LPS region on a finite interval.

## 5. Upper-Dini derivative for \(A\)

At a nonzero coefficient,

\[
 {d\over dt}|C_h|
 =\operatorname{Re}{\overline{C_h}\dot C_h\over|C_h|}.
 \tag{5.1}
\]

At \(C_h=0\), its upper right derivative is \(|\dot C_h|\).  Splitting the
linear damping before applying the triangle inequality gives

\[
 D^+A+\nu\sum_h|h|^2|C_h|
 \le2\nu\sum_h|\widehat{|\nabla u|^2}(h)|
 +\sum_h|h|\,|\widehat{u(w+2p)}(h)|.
 \tag{5.2}
\]

Thus equation (6.1) of the analytic draft is correct, including its
zero-coefficient interpretation.  For a smooth solution the needed rapidly
weighted absolute convergence is available on every compact smooth
subinterval.  The conclusion that \((A,Q,\|u\|_2)\) does not close these
stronger Wiener norms is correctly bounded; it is not stated as a no-go for
all possible weighted hierarchies.

## 6. Componentwise nonlinear Bernstein deduction

Let \(v_j=P_ju\) be real and supported in the fixed annulus
\(|k|\asymp\lambda_j\).  The exact shell dissipation is

\[
 \mathcal D_j
 =\int |v_j|^2|\nabla v_j|^2
 +{1\over2}\|\nabla|v_j|^2\|_2^2.
 \tag{6.1}
\]

For every scalar component,

\[
 -\int(\Delta v_{j,i})v_{j,i}^3
 =3\int v_{j,i}^2|\nabla v_{j,i}|^2
 \ge c\lambda_j^2\|v_{j,i}\|_4^4.
 \tag{6.2}
\]

Moreover,

\[
 \mathcal D_j
 \ge\sum_i\int v_{j,i}^2|\nabla v_{j,i}|^2,
 \qquad
 |v_j|^4\le3\sum_i|v_{j,i}|^4.
 \tag{6.3}
\]

Combining (6.2)--(6.3), with the factors \(1/3\) absorbed twice into a
cutoff-dependent constant, proves

\[
 \mathcal D_j\ge c_B\lambda_j^2Q_j.
 \tag{6.4}
\]

The parent drafts' componentwise derivation is therefore correct.  The
qualification “fixed real annular cutoff, with finitely many low shells
handled in the constant” should remain.  The scalar theorem does not justify
an arbitrary annular multiplier with a universal cutoff-independent
constant.

## 7. Shell transport: coefficients that pass

The exact equation

\[
 {1\over4}Q_j'+\nu\mathcal D_j
 =-\int|v_j|^2v_j\cdot\mathcal F_j
 \tag{7.1}
\]

and

\[
 \left|\int|v_j|^2v_j\cdot\mathcal F_j\right|
 \le\|v_j\|_6^3F_j
 \le A_j^{1/2}Q_j^{1/2}F_j
 \tag{7.2}
\]

give, for \(Y_j=Q_j^{1/2}\),

\[
 D^+Y_j+2\nu c_B\lambda_j^2Y_j
 \le2A_j^{1/2}F_j.
 \tag{7.3}
\]

All coefficients in the drafts' equations (8.7)/(6.3) are correct.  The
upper-Dini interpretation through \(Y_j=0\) is also valid: if
\(v_j(t_0)=0\) and \(v_j\) is differentiable, then

\[
 Y_j(t_0+h)=\|v_j(t_0+h)\|_4^2=O(h^2),
 \tag{7.4}
\]

so \(D^+Y_j(t_0)=0\), while \(A_j(t_0)=0\).  The Duhamel coefficient \(2\)
and decay rate \(2\nu c_B\lambda_j^2\) are correct.

## 8. Substantive correction: the \(X_j\) branch at zeros

For \(X_j=Q_j^{1/4}=\|v_j\|_4>0\), the estimate

\[
 A_j\le D_{C,j}^{1/2}X_j^2
 \tag{8.1}
\]

and division of (7.1) by \(X_j^3\) correctly give

\[
 X_j'+\nu c_B\lambda_j^2X_j
 \le D_{C,j}^{1/4}F_j.
 \tag{8.2}
\]

This derivation does **not** extend with the instantaneous
\(D_{C,j}(t)=|\operatorname{supp}\widehat{|v_j(t)|^2}|\) through a zero of
\(v_j\).  At \(v_j(t_0)=0\), that support count equals zero, but

\[
 D^+X_j(t_0)=\|\partial_tv_j(t_0)\|_4
 =\|\mathcal F_j(t_0)\|_4
 \tag{8.3}
\]

can be positive.

This situation occurs in the actual projected Navier--Stokes equation.
Choose two high modes

\[
 p=(N,0,0),\qquad q=(-N+m,m,0),\qquad k=p+q=(m,m,0),
 \tag{8.4}
\]

with polarizations

\[
 a_p=(0,1,0),\qquad a_q=(m,N-m,0),
 \tag{8.5}
\]

and add their conjugate modes.  Both polarizations are divergence free.
Choose the \(j\)-shell to contain \(k\) but not \(p,q\).  Initially
\(v_j=0\), whereas

\[
 \mathbb P_kB_k=m(m-N)(1,-1,0)\ne0.
 \tag{8.6}
\]

Thus \(\mathcal F_j(t_0)\ne0\), proving failure of (8.2) with the
instantaneous \(D_{C,j}(t_0)=0\).

### Correct global formulation

Let

\[
 \Sigma_j=\{k:\text{the fixed symbol of }P_j\text{ is nonzero at }k\},
 \qquad
 \overline D_j=|\Sigma_j-\Sigma_j|.
 \tag{8.7}
\]

Both \(v_j\) and \(\mathcal F_j\) have support in \(\Sigma_j\).  The fixed
bound

\[
 A_j(t)\le\overline D_j^{1/2}X_j(t)^2
 \tag{8.8}
\]

holds for every time.  At a zero, finite-spectrum Nikolskii gives

\[
 \|\mathcal F_j\|_4
 \le\overline D_j^{1/4}\|\mathcal F_j\|_2.
 \tag{8.9}
\]

Therefore the corrected upper-Dini statement is

\[
 \boxed{
 D^+X_j+\nu c_B\lambda_j^2X_j
 \le\overline D_j^{1/4}F_j,}
 \tag{8.10}
\]

valid through zeros, with Duhamel form

\[
\boxed{
\begin{aligned}
 X_j(t)&\le e^{-\nu c_B\lambda_j^2(t-s)}X_j(s)\\
 &\quad+\overline D_j^{1/4}\int_s^t
 e^{-\nu c_B\lambda_j^2(t-r)}F_j(r)\,dr.
\end{aligned}}
 \tag{8.11}
\]

If the sharper instantaneous \(D_{C,j}(r)\) is retained on an interval
where \(X_j(r)>0\), its factor belongs **inside** the integral:

\[
 \int_s^t e^{-\nu c_B\lambda_j^2(t-r)}
 D_{C,j}(r)^{1/4}F_j(r)\,dr.
 \tag{8.12}
\]

A right-continuous support envelope or fixed \(\overline D_j\) is still
needed at zeros.  Accordingly:

- analytic-draft equations (8.8) and (8.10) require this correction;
- report-source equation (6.4) requires the same correction;
- downstream \(X_j\) final-time budgets must use \(\overline D_j\), or
  explicitly restrict themselves to a nonzero interval.

## 9. Forcing estimates and scaling language

The estimates

\[
 F_j=\|P_j\mathbb P\nabla\cdot(u\otimes u)\|_2
 \lesssim\lambda_j\|u\otimes u\|_2
 =\lambda_j\|u\|_4^2
 \tag{9.1}
\]

and

\[
 F_j\lesssim\lambda_j^{1+3/2}\|u\otimes u\|_1
 =\lambda_j^{5/2}\|u\|_2^2
 \tag{9.2}
\]

are correct.  The first uses \(L^2\to L^2\) annular multiplier control; the
second uses the three-dimensional \(L^1\to L^2\) Bernstein factor
\(\lambda_j^{3/2}\).

The phrase “the first branch reintroduces a strong critical norm” is too
compressed.  The instantaneous norm \(\|u(t)\|_4\) is not itself
scale-invariant.  The associated Serrin-critical spacetime budget is

\[
 u\in L_t^8L_x^4,
 \qquad {2\over8}+{3\over4}=1,
 \tag{9.3}
\]

or \(\|u\|_4^2\in L_t^4\).  Recommended wording is that the first forcing
bound reintroduces the full-field strong \(L_x^4\) quantity being
transported, whose critical Serrin time exponent is eight.  The second
branch's \(\lambda_j^{5/2}\) growth is correctly described as an energy-only
but high-frequency-supercritical barrier.

## 10. Heat-plane audit

With

\[
 v_s=e^{s\Delta}u,\qquad
 R_s=e^{s\Delta}\mathbb P\nabla\cdot(u\otimes u),
 \tag{10.1}
\]

the projected NSE gives

\[
 (\partial_t-\nu\partial_s)v_s=-R_s.
 \tag{10.2}
\]

Differentiating \(Q_s=\|v_s\|_4^4\) yields

\[
 \boxed{
 (\partial_t-\nu\partial_s)Q_s
 =-4\int|v_s|^2v_s\cdot R_s\,d\mu.}
 \tag{10.3}
\]

The heat derivative is

\[
 \partial_sQ_s
 =-2\|\nabla|v_s|^2\|_2^2
  -4\int|v_s|^2|\nabla v_s|^2\,d\mu\le0.
 \tag{10.4}
\]

All signs and factors in analytic-draft equations (9.2)--(9.3) and
report-source equation (6.6) pass.  The stated commutator boundary is also
correct:

\[
 e^{s\Delta}\mathbb P\nabla\cdot(u\otimes u)
 \ne\mathbb P\nabla\cdot(v_s\otimes v_s).
 \tag{10.5}
\]

No scalar heat weighting removes the signed velocity phase in the pressure
pairing exhibited by the sign pair.

## 11. Report self-containment and declaration boundary

The public report's Section 6 introduces \(v_j\) and \(F_j\), but then uses
\(Q_j,\mathcal D_j,A_j,D_{C,j}\) without defining them.  Before its equation
(6.1), add

\[
 Q_j=\|v_j\|_4^4,\quad
 A_j=\sum_h|\widehat{|v_j|^2}(h)|,\quad
 \mathcal D_j=\int|v_j|^2|\nabla v_j|^2
 +{1\over2}\|\nabla|v_j|^2\|_2^2,
 \tag{11.1}
\]

and use the fixed \(\overline D_j\) of (8.7), or define exactly which
support envelope replaces \(D_{C,j}\).

The non-autonomy witnesses, their quantified boundaries, and the signed
velocity-phase interpretation pass the independent exact audits.  The sign
pair has the same tensor and pressure, so the separate pressure-tensor barrier
comes from the general reconstruction formula, not from that pair alone.
The drafts correctly state that:

- the rotating shear only disproves autonomy of unweighted scalar \(C\);
- the six-mode sign pair is a smooth planar information witness, not a
  singularity mechanism;
- the one-sided \(AQ\) estimate is compatible with the stronger negative
  viscous \(L^2\)-scale term;
- bounded collision searches do not establish novelty or priority;
- tensor heat closure, arbitrary-data three-dimensional regularity, and the
  Clay problem remain open.

No prohibited novelty, blow-up, partial-Clay, or arbitrary-data regularity
claim appears in either draft.

The analytic draft's opening sentence should preferably say “finite Fourier
fields at a fixed time or Galerkin solutions” rather than “finite Fourier
solution”: a generic exact NSE solution does not preserve finite support.
This does not affect any displayed identity.

## 12. Formula-number and reference audit

Automated structural readback gives:

    dynamic_autocorrelation_budget:
      displayed_equations=45
      unique_tags=45
      duplicate_tags=0
      unresolved_explicit_references=0
      display_delimiter_balance=PASS

    report_source:
      displayed_equations=29
      unique_tags=23
      duplicate_tags=0
      unresolved_explicit_references=0
      display_delimiter_balance=PASS

The report contains six unnumbered displays by design; this creates no
collision.  Every explicit reference such as (1.2), (2.2), (4.4),
(8.9)--(8.10), and (9.2)--(9.3) resolves within its own file.

## 13. Required correction list

### Mathematical correction required before release

1. Replace the instantaneous-support version of analytic equations
   (8.8)/(8.10) and report equation (6.4) by the fixed ambient-support
   formulation (8.10)--(8.11), or explicitly restrict the sharper statement
   to \(X_j>0\) and keep a valid time-dependent envelope inside the integral.

### Precision/editorial corrections

2. Repair both \(\int_{mathbb T^3}\) strings in analytic equations
   (3.1)/(3.4).
3. Put corresponding time limits into report equation (4.1).
4. Replace “stronger than Serrin” by “at least as restrictive as and implies
   \(L_t^2L_x^\infty\),” and state the exponent convention.
5. Replace the unqualified phrase “strong critical \(L^4\) norm” by the
   precise \(L_t^8L_x^4\) Serrin-critical comparison.
6. Define all shell quantities in public-report Section 6.
7. Prefer “finite Fourier field/Galerkin solution” in the analytic opening
   sentence.

After item 1 and the minor repairs above, the parent drafts are
mathematically authorized for the next certificate and publication gates.
They still do not establish a critical shell closure or any arbitrary-data
global regularity theorem.
