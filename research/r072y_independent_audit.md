# R0.72Y independent synthesis audit

**Date:** 2026-08-28

**Files audited:**

- research/r072y_report-source.md
- research/r072y_full_row_independent_audit.md
- research/r072y_forced_transfer_independent_audit.md
- research/r072y_literature_audit.md

**Outcome:** **PASS** for the stated CLOSED identities and scalar forced
estimates; **PASS as negative results** for the exact lift-up obstruction,
the standard \(H^{-1}\) \(\alpha^2\) claim, and an endpoint
\(\alpha\)-gain; **OPEN** for the complete low-gap
Orr--Sommerfeld--Squire row, nonlinear Navier--Stokes, and the Clay problem.

The two mathematical recalculations were performed separately: one began
from the physical vector equations and one began from the R0.72X scalar
evolution family. This synthesis checks that their shared normalization,
claim names, and boundaries agree.

---

## 1. Normalization audit

The report retains

\[
 A_b=2\delta a,\qquad
 d=\nu R^2(t-t_*),\qquad
 x=Ry-\phi_*,
\]

\[
 \xi=K_x/R,\qquad
 \gamma=K_z/R,\qquad
 \Lambda=A_b/(\nu R),\qquad
 c=\gamma\Lambda.
\]

Direct dimensional substitution gives

\[
 \frac{K_zA_b}{\nu R^2}=c,\qquad
 \frac{A_bR}{\nu R^2}=\Lambda.
\]

**Verdict:** PASS. The advection coefficient and lift-up coefficient are
not conflated. Suppressing \(\nu\) is allowed only after stating
\(\nu=1\).

---

## 2. Pressure and Leray signs

Independent divergence calculation gives

\[
 \nabla\cdot(V\partial_{x_3}u)=iK_zV_yu_2,
\qquad
 \nabla\cdot(u_2V_ye_3)=iK_zV_yu_2.
\]

With \(+\nabla p\) on the left,

\[
 \Delta_Kp=-2iK_zV_yu_2.
\]

On the cell,

\[
 \operatorname{div}_j\nabla_j=-\mathcal L.
\]

Therefore

\[
 \mathbb P_j=I+\nabla_j\mathcal L^{-1}\operatorname{div}_j
\]

has the required plus sign and annihilates gradients.

**Verdict:** PASS.

---

## 3. Orr--Sommerfeld--Squire audit

Applying \(\mathcal L\) to the \(u_2\) equation and substituting the pressure
source cancels both \(W_xA_\beta u_2\) commutators. The remaining equation is

\[
 q_d=(-\mathcal L-icW)q
 -icW_{xx}\mathcal L^{-1}q.
\]

Taking \(i\gamma\) times the first velocity equation minus \(i\xi\) times
the third cancels pressure and gives

\[
 \eta_d=(-\mathcal L-icW)\eta
 +i\xi\Lambda W_x\mathcal L^{-1}q.
\]

The OS feedback sign is negative; the Squire forcing sign is positive.

**Verdict:** PASS for the exact equations. The report correctly leaves
their scale-sharp propagation OPEN.

---

## 4. Recovery and exceptional-row audit

Solving

\[
 \xi u_1+\gamma u_3=iA_\beta u_2,\qquad
 \gamma u_1-\xi u_3=-i\eta
\]

gives the displayed recovery formulas and

\[
 \|u\|_2^2
 =\|u_2\|_2^2
 +\mu^{-1}\left(\|A_\beta u_2\|_2^2+\|\eta\|_2^2\right).
\]

The inversion uses \(\mu>0\). At \(\mu=0,\beta=0\),
\(\mathcal L^{-1}\) is unavailable and the component lift-up equation
survives.

**Verdict:** PASS. The report does not use the recovery formula in the
degenerate row.

---

## 5. Exact lift-up counterexample

For \(\gamma=\beta=0\), constant cell input \(u_2(d_1)=v_0\), and
\(u_1(d_1)=u_3(d_1)=0\),

\[
 u_2(d_2)=e^{-\xi^2\tau}v_0,
\]

\[
 u_3(d_2)
 =-\Lambda\tau e^{-\xi^2\tau}W_x(d_2)v_0.
\]

Differentiation reduces the residual to

\[
 (W_x)_d-(W_x)_{xx}=0.
\]

The two cosine harmonics are orthogonal, so

\[
 \langle |W_x(d)|^2\rangle
 =\frac18(e^{-2d}+e^{-8d}).
\]

This reproduces the report's amplification formula. When \(\xi>0\), the
physical horizontal Fourier factor makes the perturbation spatially mean
zero.

**Verdict:** PASS as an exact negative result. It refutes a
background-uniform strict contraction based only on
\(\varepsilon_j=|\gamma\Lambda|\). It does not refute estimates with
explicit \(\Lambda\), orientation, damping, or transient-growth payments.

---

## 6. Causal-kernel audit

For

\[
 k_\mu(r)=\mathbf1_{r\ge0}e^{-\mu r}q^{\lfloor r/h\rfloor},
\qquad h=2T\alpha^2,
\]

direct summation over \([nh,(n+1)h)\) gives

\[
 \int_0^\infty k_\mu(r)^p\,dr
 =\frac{1-e^{-p\mu h}}
 {p\mu(1-q^pe^{-p\mu h})}.
\]

The \(\mu\downarrow0\) limit is \(h/(1-q^p)\). The \(L^1\) kernel norm
is \(A_q\alpha^2\); the \(L^2\) norm is
\(\sqrt{B_q}\alpha\).

**Verdict:** PASS for all four \(L_x^2\)-valued forcing maps stated in the
report.

---

## 7. Negative-Sobolev duality audit

The backward adjoint has

\[
 \|z\|_{L^2L^2}\le A_q\alpha^2\|g\|_{L^2L^2},
\qquad
 \|A_\beta z\|_{L^2L^2}
 \le\sqrt{A_q}\alpha\|g\|_{L^2L^2}.
\]

Consequently its standard \(H^1_\beta\) norm is \(O(\alpha)\), while its
semiclassical \(\mathcal H^1_{\alpha,\beta}\) norm is
\(O(\alpha^2)\). Transposition therefore yields exactly

\[
 H^{-1}_\beta\to L_d^2L_x^2:\ O(\alpha),
\]

\[
 \mathcal H^{-1}_{\alpha,\beta}\to L_d^2L_x^2:\
 O(\alpha^2).
\]

The report supplies the variational and Hilbert-triple trace step rather
than assuming a pointwise \(H^{-1}\to L^2\) propagator.

**Verdict:** PASS analytically.

---

## 8. Endpoint-constant audit

The endpoint proof defines

\[
 C_q'=\max\{r_q,\sqrt{2(C_q+r_q)}\}.
\]

It states

\[
 \max\{\|A_\beta G\|_{L^2L^2},\|G\|_{L^\infty L^2}\}
 \le C_q'\|F\|_{L^2H^{-1}},
\]

not an incorrect bound on the sum by the same maximum constant.

The terminal high-frequency pulse has unit asymptotic
\(L_d^2H_x^{-1}\) input norm and an order-one heat endpoint. The potential
error is \(O(M_\alpha/N^2)\), which can be made small after fixing
\(\alpha\).

**Verdict:** PASS. Standard endpoint \(\alpha\)-gain is FALSE.

---

## 9. Sharpness and direct-sum audit

The localized collision-chart witness is zero-initial and mean zero. Its
physical change of variables gives state norm squared \(O(\alpha^3)\),
standard forcing norm squared \(O(\alpha)\), and semiclassical forcing norm
squared \(O(\alpha^{-1})\). The two ratios are therefore
\(O(\alpha)\) and \(O(\alpha^2)\), respectively.

For invariant scalar rows, squaring before summing preserves the row weights
\(\alpha_j^2\) or \(\alpha_j^4\). Parseval introduces no row-count
factor.

**Verdict:** PASS. The scaling limit and infinite-sum passage are analytic,
not finite-certified. No off-diagonal pressure operator is included.

---

## 10. Weak/zero-row audit

The scalar energy identity gives finite-history bounds for every coupling
size. A genuine Bloch/damping gap yields a time-global coercive estimate.
At \(\varepsilon=\beta=\mu=0\), the spatial constant reduces to
\(a'=f\), and a unit \(L^2\) input over \([0,L]\) produces
\(\|a\|_{L^2}=L/\sqrt3\).

Mean zero is not invariant for \(\beta=0\) under multiplication by a
nonconstant \(W\).

**Verdict:** PASS. A common strong-scale gain for all rows is FALSE.

---

## 11. Literature and thesis boundary

The source audit confirms prior nonautonomous forced estimates and vector
Couette results. The report does not claim those topics as new. It also
records why the strictly monotone coordinate used near Couette fails at
\(\partial_yV=0\).

The supplied thesis supports the standard linearized starting equations and
steady normal-mode context only. It is not cited as proving the
time-dependent heat-shear, Bloch, collision, or forced-transfer results.

**Verdict:** PASS.

---

## 12. Final publication decision

The following may be published as proved:

- the complete row identities and their special-row split;
- the scalar invariant embedding;
- the full-row damping-dominated class;
- the exact lift-up formula and its negative consequence;
- the three strong scalar spacetime forcing scales;
- the standard and semiclassical endpoint bounds;
- the sharpness witnesses;
- the decoupled scalar direct sum;
- the weak/zero scalar finite-history ledger.

The following must remain visibly OPEN:

- collision-scale Orr--Sommerfeld pressure absorption;
- orientation-uniform Squire transfer;
- low-gap complete vector rows;
- the complete linearized shear subsystem;
- nonlinear Navier--Stokes;
- the Clay regularity problem.

**Final verdict:** R0.72Y is mathematically publishable with the exact
boundaries above. It is not a full-row enhanced-dissipation theorem and not
a Navier--Stokes regularity result.
