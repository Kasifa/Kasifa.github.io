# R0.73I independent analytic audit

**Date:** 2026-08-30  
**Scope:** line-by-line audit of the problem freeze, continuum upper proof,
zero-window tangent proof, fixed-window no-go, report source, and gap matrix  
**Evidence class:** independent source-stage analytic audit  
**Public status:** final analytic pass for the scoped R0.73I claims only

## 0. Decision

The corrected source set passes the independent mathematical audit.

The audit verifies:

- the factor \(2/4\) ledger between physical, profile, kinetic, and fast
  variables;
- the \(\gamma=1/2\) completion of the square;
- the strict dissipative factor \(e^{-D/4}\);
- every strict inequality in the \(d_0\) upper bound;
- the order and dependence of all four zero-window liminf/limsup limits;
- the diagonal and Jordan counterexamples at the level of the declared
  abstract operator outputs;
- the negative statement's restriction to logical non-implication;
- the separation of finite Fourier evidence from continuum PDE theorems.

The earlier transcription and evidence-label issues have been repaired in
the shared source:

- report equation (3.2) now contains \(\frac1{16c^2}\), with no control
  character;
- report equation (4.1) now uses \(\inf\) and \(\sup\);
- both WKB formulas now use \(\,\mathrm d d\);
- the report now identifies the comparison as an independent
  kinetic-coordinate RK4 implementation, not a physical-velocity
  formulation.

No shared source was modified by this audit.

## 1. Audited snapshot

The final audit used these hashes:

    8b6efb098fc88689d739d1293ea329f7cf177986d2b450d91d997e585f46b104  research/r073i_problem_freeze.md
    078d8a33099361ceb890d5cb56659a2e6971adcf3d917da6eeb27524d1cae347  research/r073i_continuum_upper_action_proof.md
    fb4ef3a64e91c8ebe1139cb3beab0995ab3222d343760d5e5ab7f361650b4500  research/r073i_zero_window_tangent_proof.md
    e069e144e58629d7bbebfb56007b90bbbfa19a2ad349c612c2c4643253e9ca3b  research/r073i_fixed_window_no_go.md
    295c00881bc0b7dc7b44fb0c1c3248805db46df4838506a175f413454515c091  research/r073i_report-source.md
    5284e6ab11c5f57d7c80e3ffecb3976244b1f32118bbe246d758816ba2d7f8ca  research/r073i_gap_matrix.md

## 2. Factor ledger

For the selected row,

\[
 \gamma=\frac12,
 \qquad
 L=-\partial_x^2+\frac14,
 \qquad
 B_\varepsilon(d)=\widetilde A(d)-\varepsilon L,
 \qquad
 \varepsilon=\Lambda^{-1}.
 \tag{2.1}
\]

The exact time changes are

\[
 d=4t_{\rm physical},
 \qquad
 \theta=\Lambda d.
 \tag{2.2}
\]

The physical row Laplacian becomes

\[
 \frac14(4\partial_x^2-1)
 =-\left(-\partial_x^2+\frac14\right)
 =-L
 \tag{2.3}
\]

after changing from physical time to \(d\).  Changing from \(d\) to
\(\theta\) then gives \(-\varepsilon L\).  Thus the fast endpoint is
\(\theta=D/\varepsilon=\Lambda D\), with no missing factor four.

For a streamfunction profile \(v\), define

\[
 E_{1/2}(v)=\|v'\|_2^2+\frac14\|v\|_2^2,
 \qquad
 F_d(v)=\frac12\operatorname{Im}
 \int_{\mathbb T}W_x(d)v'\overline v.
 \tag{2.4}
\]

Under the kinetic unitary, \(h=2L^{1/2}v\), one has

\[
 \|h\|_2^2=4E_{1/2}(v),
 \qquad
 \operatorname{Re}\langle\widetilde A(d)h,h\rangle
 =4F_d(v).
 \tag{2.5}
\]

Consequently,

\[
 \frac{\operatorname{Re}
 \langle\widetilde A(d)h,h\rangle}{\|h\|_2^2}
 =\frac{F_d(v)}{E_{1/2}(v)}.
 \tag{2.6}
\]

This closes the possible factor-two and factor-four ambiguity.

## 3. Square completion and numerical abscissa

Let

\[
 \mathscr H_d
 =-\partial_x^2+1-\frac94W_x(d)^2.
 \tag{3.1}
\]

The inherited exact certificate gives

\[
 \mathscr H_d\ge h(d)I,
 \qquad
 h(d)=\frac1{20}-\frac{45}{4}d,
 \qquad
 0\le d\le\frac1{450}.
 \tag{3.2}
\]

For \(c>0\) and \(\sigma=\pm1\),

\[
 \begin{aligned}
 cE_{1/2}(v)+\sigma F_d(v)
 ={}&
 c\left\|v'
 +\frac{i\sigma}{4c}W_x(d)v\right\|_2^2\\
 &+
 c\int_{\mathbb T}
 \left(\frac14-\frac{W_x(d)^2}{16c^2}\right)|v|^2.
 \end{aligned}
 \tag{3.3}
\]

The periodic gauge

\[
 v=e^{-i\sigma W(d)/(4c)}f
 \tag{3.4}
\]

is unitary on \(L^2\), preserves the periodic \(H^1\) form domain, and
reduces (3.3) to \(c\langle H_{c,d}f,f\rangle\), where

\[
 H_{c,d}
 =-\partial_x^2+\frac14-\frac1{16c^2}W_x(d)^2.
 \tag{3.5}
\]

For

\[
 \vartheta=\frac1{36c^2},
 \tag{3.6}
\]

coefficient comparison gives

\[
 H_{c,d}
 =\vartheta\mathscr H_d
 +(1-\vartheta)(-\partial_x^2)
 +\left(\frac14-\vartheta\right)I.
 \tag{3.7}
\]

Choosing

\[
 \vartheta(d)=\frac1{4(1-h(d))}
 \tag{3.8}
\]

makes the scalar lower bound zero and yields

\[
 c_H(d)
 =\frac13\sqrt{1-h(d)}
 =\frac13\sqrt{\frac{19}{20}+\frac{45}{4}d}.
 \tag{3.9}
\]

On the declared interval, \(0<\vartheta(d)<1\), so the discarded
\((1-\vartheta)(-\partial_x^2)\) term is nonnegative.  Both signs prove

\[
 |F_d(v)|\le c_H(d)E_{1/2}(v),
 \qquad
 \omega(\widetilde A(d))\le c_H(d).
 \tag{3.10}
\]

The form domain is \(H^1_{\rm per}\); the associated Schrödinger operator
domain is \(H^2_{\rm per}\).  No hidden domain assumption is used here.

## 4. Viscous factor and integrated action

For a classical solution of

\[
 u_\theta=B_\varepsilon(\varepsilon\theta)u,
 \tag{4.1}
\]

equation (3.10) and \(L\ge I/4\) give

\[
 \frac12\frac d{d\theta}\|u\|_2^2
 \le
 \left[c_H(\varepsilon\theta)-\frac{\varepsilon}{4}\right]
 \|u\|_2^2.
 \tag{4.2}
\]

Hence

\[
 \frac d{d\theta}\log\|u\|_2
 \le c_H(\varepsilon\theta)-\frac{\varepsilon}{4}.
 \tag{4.3}
\]

Integration to \(D/\varepsilon\) produces

\[
 \|U_\varepsilon(D/\varepsilon,0)\|
 \le
 \exp\left\{\frac{\Omega_H(D)}{\varepsilon}-\frac D4\right\},
 \tag{4.4}
\]

where

\[
 \Omega_H(D)
 =
 \frac8{405}
 \left[
 \left(\frac{19}{20}+\frac{45D}{4}\right)^{3/2}
 -\left(\frac{19}{20}\right)^{3/2}
 \right].
 \tag{4.5}
\]

The passage from squared norm to norm does not introduce another factor
two.  The \(-D/4\) term is correct.  The unbounded
\(-\varepsilon L\) remains in the fixed generator; only the profile drift
is treated as bounded.

## 5. Strict \(d_0\) chain

R0.73F uses

\[
 0<b<\alpha<c_F<a,
 \qquad
 \nu=\min\{\alpha-b,c_F-\alpha\},
 \qquad K\ge1.
 \tag{5.1}
\]

Therefore

\[
 2\nu
 \le(\alpha-b)+(c_F-\alpha)
 =c_F-b<a.
 \tag{5.2}
\]

The strictness follows from \(c_F<a\) and \(b>0\), so

\[
 \nu<\frac a2.
 \tag{5.3}
\]

Since

\[
 C_A d_0<\frac{\nu}{16K^2},
 \qquad C_A=\frac{49}{4},
 \tag{5.4}
\]

one obtains

\[
 d_0
 <\frac{\nu}{196K^2}
 \le\frac{\nu}{196}
 <\frac a{392}.
 \tag{5.5}
\]

At \(d=0\), spectral inclusion in the closure of the numerical range and
(3.9) give

\[
 a\le c_H(0)=\sqrt{\frac{19}{180}}.
 \tag{5.6}
\]

Thus

\[
 d_0<\frac{\sqrt{19/180}}{392}.
 \tag{5.7}
\]

Finally,

\[
 \left(\frac{450}{392}\right)^2\frac{19}{180}
 =\frac{21375}{153664}<1.
 \tag{5.8}
\]

Hence \(d_0<1/450\) strictly and the inherited endpoint is
\(D=d_0\).  The source correctly keeps \(d_0\) existential and shrinkable.

## 6. Four nested tangent limits

Let

\[
 \begin{aligned}
 m_\varepsilon(D)
 &=\inf_{\substack{v\in P_\varepsilon H\\\|v\|=1}}
 \|U_\varepsilon(D/\varepsilon,0)v\|,\\
 M_\varepsilon(D)
 &=\sup_{\substack{v\in P_\varepsilon H\\\|v\|=1}}
 \|U_\varepsilon(D/\varepsilon,0)v\|.
 \end{aligned}
 \tag{6.1}
\]

For each upper margin \(\rho>0\), the R0.73E frozen estimate and Volterra
Gronwall give

\[
 M_\varepsilon(D)
 \le C_\rho
 \exp\left\{
 \frac{(a+\rho)D+\frac12C_\rho C_A D^2}{\varepsilon}
 \right\}.
 \tag{6.2}
\]

For each lower accuracy \(\zeta>0\), first choose

\[
 \max\{\beta,0.17035,a-\zeta\}<\alpha_\zeta<a,
 \tag{6.3}
\]

then choose \(b_\zeta,c_\zeta,\nu_\zeta,K_\zeta\), and only afterward an
interval \(d_\zeta>0\) satisfying the R0.73F roughness conditions.  With

\[
 r_\zeta=\alpha_\zeta+\frac{\nu_\zeta}{2}>a-\zeta,
 \tag{6.4}
\]

R0.73F gives

\[
 m_\varepsilon(D)
 \ge K_{1,\zeta}^{-1}e^{r_\zeta D/\varepsilon},
 \qquad
 0<D\le d_\zeta.
 \tag{6.5}
\]

For each fixed \(D>0\), both the inner liminf and inner limsup as
\(\varepsilon\downarrow0\) lose the constant prefactors.  Sending
\(D\downarrow0\) next removes the \(O(D)\) Volterra correction.  Finally
\(\rho,\zeta\downarrow0\) gives

\[
 \begin{aligned}
 \lim_{D\downarrow0}\liminf_{\varepsilon\downarrow0}
 \frac{\varepsilon}{D}\log m_\varepsilon(D)
 &=
 \lim_{D\downarrow0}\limsup_{\varepsilon\downarrow0}
 \frac{\varepsilon}{D}\log m_\varepsilon(D)\\
 &=
 \lim_{D\downarrow0}\liminf_{\varepsilon\downarrow0}
 \frac{\varepsilon}{D}\log M_\varepsilon(D)\\
 &=
 \lim_{D\downarrow0}\limsup_{\varepsilon\downarrow0}
 \frac{\varepsilon}{D}\log M_\varepsilon(D)
 =a.
 \end{aligned}
 \tag{6.6}
\]

The dependence \(d_\zeta=d_\zeta(\alpha_\zeta,b_\zeta,c_\zeta,
\nu_\zeta,K_\zeta)\) is explicit in the source.  No positive lower bound
uniform in \(\zeta\) is asserted.  The source also correctly excludes a
fixed-\(D\) inner limit and a joint limit along \(D=D(\varepsilon)\).

## 7. Counterexample scope

The negative theorem concerns the abstract outputs currently isolated from
R0.73F--H:

1. bounded \(O(d)\) drift;
2. a finite complete frozen top block;
3. a uniformly separated complement;
4. an every-vector moving lower dichotomy on a small interval;
5. a noncanonical eigenvector choice in the top block;
6. a one-sided numerical-abscissa upper bound.

The diagonal example shows that these outputs do not force a
launch-independent action.  The Jordan example shows that even existence
of an action does not force a bounded compensated prefactor.

The no-go source explicitly says that these finite systems do not model the
detailed coefficients of the exact periodic operator.  The report and gap
matrix label the conclusions FALSE AS INFERENCE and keep the actual PDE
matching action open.  Therefore the negative conclusion does not cross its
logical boundary.

## 8. Finite/PDE boundary

The finite package was checked with the bundled runtimes:

    node --test tests/r073i-finite-diagnostic.test.mjs
      tests=2, pass=2

    python experiments/r073i/validate.py --directory experiments/r073i
      allChecksPass=true
      actionRows=18
      comparisonRows=36
      gainRows=36
      continuumConclusion=none

The independent RK4 comparison is a separate time integrator on the same
finite kinetic-coordinate generator.  It is not a physical-velocity
derivation, an independent spatial discretization, or a Fourier-tail
enclosure.  The corrected report no longer makes that stronger claim.

The three diagnostic windows remain clearly separated:

- \(D=10^{-4}\) is an explicit finite pilot;
- \(D=\sqrt{19/180}/392\) is a diagnostic at a strict upper bound for
  \(d_0\), not at \(d_0\);
- \(D=1/450\) is outside the inherited theorem endpoint.

No finite result is used to prove a continuum spectral branch, an
adiabatic law, or the value of the shrinkable \(d_0\).

## 9. Boundary retained after the pass

The pass covers only:

- the strict endpoint correction;
- the one-sided continuum upper action;
- the zero-window tangent theorem;
- the two scoped logical non-implications.

It does not close:

- a canonical rank-one rightmost continuum branch;
- a fixed positive action window;
- a fixed-window action or bounded prefactor for the exact PDE gain;
- a prescribed action-scale nonlinear seed;
- fixed-background instability;
- transverse three-dimensional closure;
- finite-time singularity or the Clay problem.

**MATHEMATICAL FINAL PASS**
