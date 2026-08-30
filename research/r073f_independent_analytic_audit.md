# R0.73F independent analytic audit

**Date:** 2026-08-30

**Audit status:** **FINAL PASS**

**Evidence class:** independent analytic audit of a conditional operator theorem

## 1. Object and scope of the audit

This audit covers the two public R0.73F documents

- *R0.73F problem freeze: a moving-profile dichotomy on a fixed physical
  window*;
- *R0.73F proof: moving-profile dichotomy and fixed-window exponential gain*.

The question audited is narrow and precise.  Starting from the uniform frozen
dichotomy supplied by R0.73E, does the proof rigorously obtain

1. a fast-time exponential dichotomy for the exact moving Fourier row on a
   fixed positive physical interval;
2. an unstable bundle of the same finite positive dimension as the frozen top
   block;
3. a lower bound of order
   \(\exp(c_D/\varepsilon)=\exp(c_D|\Lambda|)\);
4. the stated interface with the R0.73B upper bound?

The audit checks logical sufficiency, quantifiers, constants, evolution
directions, graph complementarity, invariance, the common Riesz contour, the
clamped extension, and the conversion between fast and physical time.

The following inputs are treated exactly as hypotheses of R0.73F and are not
re-proved here:

- the certified R0.73C inviscid eigenvalue;
- the R0.73E uniform frozen semigroup dichotomy, including its uniform
  prefactors and finite-rank top projection;
- the R0.73B complete-row kinetic upper estimate.

Accordingly, FINAL PASS means that the R0.73F implication from those stated
inputs is analytically closed.  It is not an independent recertification of
R0.73B, R0.73C, or R0.73E.

## 2. Initial adversarial verdict: NOT PASS

The first audit did not identify a counterexample to the intended roughness
argument.  It did identify several places where the then-current exposition
did not yet support the public claim at theorem-proof standard.

### 2.1 Missing uniform estimate on the common contour

The earlier contour argument asserted separation on the line
\(\operatorname{Re}z=\alpha\), but did not display the uniform resolvent
estimate needed there.  Pointwise membership of the resolvent set is not
enough to obtain a contour bound uniform in \(\varepsilon\) and \(d\), nor
the uniform \(C^1\) bound for the Riesz projection.

This was a substantive closure gap because nonnormal generators can have a
large resolvent even when their spectra remain separated.

### 2.2 Graph invariance and unstable bijectivity were too compressed

The earlier Lyapunov--Perron discussion constructed candidate stable and
unstable graphs but did not spell out why

- the mild evolution maps each graph to the corresponding graph at the later
  base time;
- the unstable restriction is onto as well as one-to-one;
- the graph projections vary continuously in operator norm.

These points are necessary for a genuine evolution dichotomy, especially
because the parabolic stable semigroup is not invertible.

### 2.3 Endpoint argument contained an incorrect cross-reference

The exact identity placing the initial frozen top space in the moving
unstable fiber was cited by the wrong equation number.  Since the endpoint
lower bound depends on that identity, the reference had to be corrected even
though the intended argument was recoverable.

### 2.4 Instantaneous, dynamical, and graph-norm claims were not separated

The earlier claim boundary did not distinguish sharply enough among

- the instantaneous frozen-at-\(d\) Riesz projection;
- the dynamical projection of the nonautonomous evolution;
- a Kato transport statement in an unscaled \(H^2\) graph norm;
- continuation beyond the local interval \(0\le d\le d_0\).

Only the first two are constructed, and they are not proved equal.  The Kato
and global-continuation statements are not consequences of norm-\(C^1\)
control in \(\mathcal B(H)\).

### 2.5 The all-row boundary was too broad

The earlier wording could be read as supplying a complete all-row
OS--Squire direct-sum conclusion.  The proof concerns one exact invariant
row.  The boundary therefore had to say explicitly that neither a complete
all-row \(A_2\) closure nor a matching fixed-window lower bound across all
rows has been proved.

These five items produced the initial NOT PASS.  All five are corrected in
the audited version.

## 3. Verification of the corrected proof

### 3.1 Frozen input and the shift

The proof chooses

\[
 \max\{\beta,0.17035\}<\alpha<a,
 \qquad
 \max\{\beta,0\}<b<\alpha<c<a,
\]

and defines

\[
 \delta_s=\alpha-b,\qquad
 \delta_u=c-\alpha,\qquad
 \nu=\min\{\delta_s,\delta_u\}>0,
\]

\[
 K=\max\{1,C_b,C_c\}.
\]

After shifting by \(\alpha\), the R0.73E estimates become

\[
 \|e^{tC_\varepsilon}Q_\varepsilon\|
 \le Ke^{-\nu t},
 \qquad
 \|e^{-tC_\varepsilon}P_\varepsilon\|
 \le Ke^{-\nu t},
 \qquad t\ge0.
\]

The second expression is used only on the finite-dimensional unstable
block.  The proof never assumes that the stable parabolic semigroup has a
negative-time inverse.  Evaluating at \(t=0\) also gives the projection
bounds \(\|P_\varepsilon\|,\|Q_\varepsilon\|\le K\).

### 3.2 Lyapunov--Perron constants

Lemma 3.1 sets

\[
 \eta=\frac{\nu}{2},\qquad
 \rho=\sup_t\|V(t)\|,
\]

and obtains the contraction constant

\[
 \begin{aligned}
 q
 &=K\rho
 \left(\frac1{\nu-\eta}+\frac1{\nu+\eta}\right)\\
 &=\frac{8K\rho}{3\nu}.
 \end{aligned}
\]

Under the stated conservative radius

\[
 \rho<\frac{\nu}{16K^2},
\]

one has

\[
 q<\frac1{6K}\le\frac16<1.
\]

Thus both the forward stable and backward unstable fixed-point maps are
strict contractions with constants uniform in the base time and in the
length of the time interval.

The graph bounds are

\[
 \|\Phi_s\|,\ \|\Psi_s\|
 \le
 M:=
 \frac{K^2\rho}{(\nu+\eta)(1-q)}.
\]

The same inequalities give \(M<1/20\), hence
\(\|\Phi_s\|\,\|\Psi_s\|<1\) uniformly.  The constants therefore close with
ample margin; no hidden dependence on \(\varepsilon\) or on
\(d/\varepsilon\) enters the contraction.

### 3.3 The noninvertible stable semigroup is handled correctly

In the stable graph equation, the \(Q\) term is propagated only forward and
the negative-time integral uses only the group on \(P H\).  In the unstable
graph equation, the integral from \(-\infty\) to the observation time again
uses the forward \(Q\)-semigroup, while the other integral uses negative
time only on \(P H\).

At no point does the proof write or require \(e^{-tC}Q\).  This is the
correct one-sided formulation for a parabolic stable component.

### 3.4 Complementarity, invariance, and rank

For \(x=q_0+p_0\in QX\oplus PX\), the decomposition into the two graphs is
reduced to

\[
 (I-\Phi_s\Psi_s)\zeta=p_0-\Phi_s q_0,
 \qquad
 \xi=q_0-\Psi_s\zeta.
\]

Because \(\|\Phi_s\Psi_s\|<1\), the inverse exists by a uniform Neumann
series.  This proves both complementarity and uniform boundedness of the
graph projections.

The corrected proof then splits each fixed-point equation at an intermediate
time.  Fixed-point uniqueness shows that a stable solution restricted to a
later half-line is the stable graph solution based there, and likewise for
the unstable backward solution.  Conversely, the backward fixed point
through any vector in the later unstable fiber supplies its unique preimage.
This proves invariance and bijectivity of the unstable restriction without
asserting invertibility on the stable space.

Norm continuity of \(V\), uniform contraction, and dominated convergence in
the two integral equations give norm continuity of \(\Phi_s\), \(\Psi_s\),
and hence of the graph projections.  Since the unstable graph is the graph
of a bounded map over \(PX\), its dimension is exactly
\(\dim PX=m\) at every time.

The resulting estimates have one common prefactor \(K_1\) and rate
\(\eta=\nu/2\), depending only on the frozen constants and the selected
roughness radius.

### 3.5 Autonomous graph projection equals the local Riesz projection

For fixed \(d\), the perturbation

\[
 V(t)=\widetilde A(d)-\widetilde A(0)
\]

is constant and satisfies the same roughness bound.  The invariant graphs
therefore split the autonomous shifted generator into a stable part with
spectrum in
\(\{\operatorname{Re}z\le\alpha-\eta\}\) and a finite-dimensional
unstable part with spectrum in
\(\{\operatorname{Re}z\ge\alpha+\eta\}\).

The positive-time Laplace formula on the stable part and the negative-time
formula on the finite-dimensional unstable part give the complete resolvent
strip

\[
 \{z:|\operatorname{Re}z-\alpha|<\eta\}
 \subset\rho(\widetilde B_\varepsilon(d)).
\]

Consequently, the autonomous dichotomy projection is the unique spectral
projection onto the part to the right of \(\alpha\), hence it equals the
Riesz projection defined by the common contour.  This equality is only for
the autonomous frozen-at-\(d\) problem.  It does not identify that
projection with the dynamical projection of the moving problem.

The corrected proof now includes the missing uniform estimate on the left
side of the contour:

\[
 \sup_{\tau\in\mathbb R}
 \|(\alpha+i\tau-\widetilde B_\varepsilon(d))^{-1}\|
 \le\frac{2K_1}{\eta}.
\]

The other three sides are controlled uniformly by

\[
 z-\widetilde B_\varepsilon(d)
 =(z+\varepsilon L)
 \left[I-(z+\varepsilon L)^{-1}\widetilde A(d)\right],
\]

with the right and horizontal sides chosen beyond the common bound
\(M_A=\sup_{0\le d\le d_0}\|\widetilde A(d)\|\).  This gives one finite
contour independent of \(\varepsilon\) and \(d\).  Differentiating its
resolvent integral is then justified and yields the claimed uniform
operator-norm \(C^1\) estimate for
\(P_\varepsilon^{\rm inst}(d)\).

No unscaled \(H^2\) graph-norm estimate is inferred from this
\(\mathcal B(H)\) statement.

### 3.6 The clamped moving profile

For \(0<d\le d_0\), the extension

\[
 \chi_{\varepsilon,d}(t)=
 \begin{cases}
 0,&t\le0,\\
 \varepsilon t,&0\le t\le d/\varepsilon,\\
 d,&t\ge d/\varepsilon
 \end{cases}
\]

is continuous, and

\[
 D_{\varepsilon,d}(t)
 =\widetilde A(\chi_{\varepsilon,d}(t))
  -\widetilde A(0)
\]

is a norm-continuous bounded perturbation.  Since
\(C_A=49/4\), choosing

\[
 C_A d_0<\frac{\nu}{16K^2}
\]

puts the whole extended problem inside the same roughness ball:

\[
 \sup_t\|D_{\varepsilon,d}(t)\|
 \le C_A d\le C_A d_0.
\]

The unbounded operator \(-\varepsilon L\) remains in the fixed generator
with common domain \(H^2_{\rm per}\); only a bounded time-dependent
operator is perturbed.  The mild evolution is therefore supplied by the
bounded nonautonomous perturbation theorem or its Volterra series.

The extension agrees exactly with the physical coefficient on
\(0\le t\le d/\varepsilon\).  Its values after the endpoint are only a
device for applying a whole-line roughness lemma.  Because the perturbation
vanishes for all \(t\le0\), the unstable graph formula gives the exact
identity

\[
 \Psi_0=0,\qquad
 E^u_{\varepsilon,d}(0)=P_\varepsilon H.
\]

The corrected endpoint argument cites this identity as equation (4.14).

### 3.7 Fixed-window lower bound and time conversion

Let \(T=d/\varepsilon\) and take a unit vector in
\(P_\varepsilon H=E^u_{\varepsilon,d}(0)\).  Applying the inverse estimate
on the moving unstable fiber gives

\[
 \|V_{C,\varepsilon,d}(T,0)v_\varepsilon\|
 \ge K_1^{-1}e^{\eta T}.
\]

Undoing the shift by \(\alpha\) yields

\[
 \|U_\varepsilon(T,0)v_\varepsilon\|
 \ge K_1^{-1}e^{(\alpha+\eta)T}.
\]

The initial unit vector may depend on \(\varepsilon\), which is legitimate
for an operator-norm lower bound.  Indeed, the estimate holds for every unit
vector in the frozen top space.

For an arbitrary fixed physical window \(D>0\), set

\[
 d_D=\min\{D,d_0\}.
\]

Since \(d_D\) is an admissible observation time in the supremum defining the
gain, and since \(\varepsilon=|\Lambda|^{-1}\),

\[
 G_{1/2}(\Lambda;D)
 \ge K_1^{-1}
 \exp\!\left((\alpha+\eta)d_D|\Lambda|\right).
\]

When \(D>d_0\), this is a lower bound attained at the interior admissible
time \(d_0\); it is not an endpoint law at \(D\).  The row
\(\beta=\xi=0,\gamma=1/2\) has zero Squire forcing, the kinetic
identification is unitary, and complex conjugation handles the two signs of
\(\Lambda\).  These are the exact interfaces required to transfer the
moving scalar-row estimate to the stated complete invariant row.

### 3.8 Interface with the R0.73B upper bound

R0.73B supplies, in the same kinetic norm, the complete-row estimate

\[
 \|U(d,0)\|\le e^{5|\Lambda|/16}
\]

uniformly in \(d\ge0\).  Restricting it to the present row and taking the
supremum over \(0\le d\le D\) is legitimate.  Together with the lower bound,
division by \(|\Lambda|\) and passage to liminf and limsup give

\[
 (\alpha+\eta)d_D
 \le
 \liminf_{|\Lambda|\to\infty}
 \frac{\log G_{1/2}(\Lambda;D)}{|\Lambda|}
 \le
 \limsup_{|\Lambda|\to\infty}
 \frac{\log G_{1/2}(\Lambda;D)}{|\Lambda|}
 \le\frac5{16}.
\]

The constant \(\log K_1/|\Lambda|\) vanishes in this limit.  This proves
only \(\Theta(|\Lambda|)\) logarithmic gain; it neither proves existence of
the normalized limit nor identifies a sharp exponent.

## 4. Adversarial failure modes

The corrected proof explicitly records two exact finite-dimensional
counterexamples that delimit the theorem.

First, a stable nonnormal block

\[
 D_N=
 \begin{pmatrix}
 -N&N^2\\
 0&-N
 \end{pmatrix}
\]

has spectrum fixed at \(-N\) but
\(\|e^{D_N/N}\|\ge N/e\).  A spectral gap alone therefore does not provide
an \(\varepsilon\)-uniform dichotomy prefactor.

Second, a diagonal four-dimensional family with three phase-shifted cosine
rates has positive instantaneous spectral abscissa at every slow time, while
each of the three candidate growing components equals
\(\exp(-D/(4\varepsilon))\) after one complete window.  Pointwise positive
spectral abscissa therefore does not select a dynamically growing line.

These are exact analytic counterexamples to invalid inference patterns.
They are not evidence about the Navier--Stokes Fourier row itself.

## 5. Finite diagnostics are not part of the proof

No finite truncation, eigenvalue plot, sampled resolvent, or numerical
time-stepping experiment can replace the uniform operator estimates used
above.  Such computations may diagnose candidate constants, catch algebraic
errors, or motivate a contour, but they do not establish

- a resolvent bound over an entire unbounded vertical line;
- an \(\varepsilon\)-uniform semigroup prefactor;
- a whole-line evolution dichotomy;
- an infinite-dimensional Riesz projection identity;
- the fixed-window lower law.

The R0.73F proof is therefore conditional on the certified theorem inputs
from R0.73C and R0.73E, not on an uncertified finite diagnostic.  The
finite-dimensional systems in Section 4 of this audit are counterexamples
to shortcuts, not surrogate proofs of the target theorem.

## 6. Claim ledger

| Claim | Audit status | Exact boundary |
|---|---:|---|
| Uniform frozen dichotomy at \(d=0\) | inherited | R0.73E input, not re-proved here |
| Roughness under bounded norm-continuous perturbations | closed | permits a noninvertible stable semigroup |
| Moving fast-time stable/unstable bundle on \(0\le d\le d_0\) | closed | one exact invariant Fourier row |
| Positive finite unstable dimension, uniform in time and small \(\varepsilon\) | closed | equals the frozen top-block rank |
| Local instantaneous spectral strip and one common contour | closed | only \(0\le d\le d_0\) |
| Autonomous frozen-at-\(d\) dichotomy projection equals its Riesz projection | closed | does not identify the moving dynamical projection |
| Norm-\(C^1\) instantaneous Riesz projection in \(\mathcal B(H)\) | closed | no unscaled \(H^2\) graph-norm Kato theorem |
| Fixed-window lower gain \(e^{c_D|\Lambda|}\) for every fixed \(D>0\) | closed | for \(D>d_0\), uses the interior time \(d_0\) |
| Matching endpoint lower law at an arbitrary prescribed \(D>d_0\) | open | not claimed |
| Equality of instantaneous and dynamical projections | open | not claimed |
| Sharp normalized logarithmic exponent or existence of its limit | open | not claimed |
| Simplicity or rightmost status of the certified inviscid eigenvalue | open | not claimed |
| Complete all-row OS--Squire \(A_2\) direct-sum closure | open | not supplied by this one-row theorem |
| Matching fixed-window lower bound across all rows | open | not supplied |
| Nonlinear mode-convolution control | open | not supplied |
| Finite-time singularity of one Navier--Stokes solution | no claim | outside R0.73F |
| Failure of global regularity or resolution of the Clay problem | no claim | outside R0.73F |

## 7. Final verdict

All initially identified proof-closure and claim-boundary defects have been
repaired.  The constants are consistent, the Lyapunov--Perron construction
does not invert the stable semigroup, the graph splitting is complementary
and invariant, the autonomous dichotomy projection is correctly identified
with its local Riesz projection, the clamped extension is exact on the
physical interval, and the fast-time lower estimate is correctly converted
to the fixed physical-window gain.  The R0.73B upper-bound interface is
compatible and does not create a sharp-exponent claim.

**FINAL PASS.**

This verdict is restricted to the conditional, one-row linear theorem
stated above.  It is not an all-row theorem, a nonlinear Navier--Stokes
closure, a singularity theorem, or a solution of the Clay Millennium
problem.
