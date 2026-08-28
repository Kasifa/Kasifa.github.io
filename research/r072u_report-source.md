# R0.72U report source: center-uniform graph coercivity on a bounded \(A_2\) chart

**Date:** 2026-08-28

**Status:** the uncut graph-coercivity estimate on every fixed bounded spatial
chart is proved with a constant independent of the time-interval center.  The
proof includes both bounded centers and centers escaping to infinity, without
temporal or spatial trace conditions.  The estimate gives local solution
observability and, conditional on a valid energy identity, a bounded-chart
dissipative contraction.  Whole-line tails,
periodic transfer, and every Clay-level consequence remain open.

**Keywords:** time-dependent cubic shear, graph coercivity, scalar moments,
weighted Poincare inequality, endpoint traces, local observability, tails

---

## 0. What this section closes

R0.72T reduced the collision chart to

\[
 H_3(S,X)=X^3+6SX.
 \tag{0.1}
\]

This section asks whether the graph norm of

\[
 \partial_S-i\sigma H_3(S,X),
 \qquad \sigma\in\{-1,1\},
 \tag{0.2}
\]

controls the spacetime \(L^2\) norm on every fixed bounded chart, uniformly
over the center of the time interval.

The answer is affirmative on a fixed bounded spatial interval, with no trace
condition on the tested function.  The precise release labels are

\[
 \boxed{
 \begin{aligned}
 \texttt{centerUniformLocalGraphCoercivity}&=\texttt{CLOSED},\\
 \texttt{localSolutionObservability}&=\texttt{CLOSED},\\
 \texttt{wholeLineBlockContraction}&=\texttt{OPEN},\\
 \texttt{periodicTransfer}&=\texttt{OPEN},\\
 \texttt{Clay}&=\texttt{OPEN}.
 \end{aligned}}
 \tag{0.3}
\]

No numerical value for the coercivity constant is claimed.  The proof is a
compactness and scalar-moment argument.  Its center-uniform part depends on an
explicit endpoint calculation.

---

## 1. Literal spatial-cutoff Poincare-trivial audit

There is a simple way to write a true but uninformative version of the target
estimate.  If a spatial cutoff forces

\[
 v\in H_0^1((-R,R)),
 \tag{1.1}
\]

then ordinary Poincare already gives

\[
 \|v\|_{L^2_X}
 \le C_R\|\partial_Xv\|_{L^2_X}.
 \tag{1.2}
\]

After integration in time, (1.2) implies the proposed graph inequality without
using the operator, the cubic phase, or the \(A_2\) collision.  Moreover, if

\[
 v=\eta(X)u,
 \tag{1.3}
\]

then

\[
 \partial_Xv=\eta\partial_Xu+\eta'u.
 \tag{1.4}
\]

The zero-order term \(\eta'u\) can carry the whole right-hand side.  Such a
proof does not establish collision-driven observability.

The theorem below therefore allows arbitrary \(H^1\) functions on the spatial
chart.  It imposes no spatial trace condition.  It also uses the whole fixed
time interval and imposes no temporal trace condition.

---

## 2. Geometry, graph space, and theorem

Fix

\[
 T>0,\qquad R>0,
 \tag{2.1}
\]

and set

\[
 I=(-T,T),\qquad J=(-R,R),\qquad Q=I\times J.
 \tag{2.2}
\]

Here \(I\) is the time interval and \(J\) is the spatial chart.  For a time
center \(c\in\mathbb R\), write

\[
 S=c+t,
 \qquad
 V_c(t,X)=X^3+6(c+t)X,
 \tag{2.3}
\]

and define

\[
 P_c=\partial_t-i\sigma V_c(t,X),
 \qquad \sigma\in\{-1,1\}.
 \tag{2.4}
\]

Use the Dirichlet negative Sobolev space

\[
 H_D^{-1}(J):=(H_0^1(J))^*.
 \tag{2.5}
\]

The graph space is

\[
 \mathcal G_c
 :=\left\{
 v\in L^2(I;H^1(J)):
 P_cv\in L^2(I;H_D^{-1}(J))
 \right\}.
 \tag{2.6}
\]

No value of \(v\) is prescribed at \(t=\pm T\) or \(X=\pm R\).

### Theorem 2.1: center-uniform local graph coercivity

There is a finite constant \(C_{R,T}\), depending on the fixed chart but not
on \(c\), such that every \(c\in\mathbb R\), every
\(\sigma\in\{-1,1\}\), and every \(v\in\mathcal G_c\) satisfy

\[
 \boxed{
 \|v\|_{L^2(Q)}
 \le C_{R,T}
 \left(
 \|\partial_Xv\|_{L^2(Q)}
 +
 \|P_cv\|_{L^2(I;H_D^{-1}(J))}
 \right).}
 \tag{2.7}
\]

The theorem asserts existence and center-uniformity.  It does not assert an
explicit formula for \(C_{R,T}\), nor uniformity as \(R\) or \(T\) degenerates.

---

## 3. Weighted Poincare lemma

Choose once and for all

\[
 q_0\in C_c^\infty(J),
 \qquad q_0\ge0,
 \qquad q_0(-X)=q_0(X),
 \qquad \int_Jq_0(X)\,dX=1.
 \tag{3.1}
\]

Set

\[
 q_1(X)=Xq_0(X),
 \tag{3.2}
\]

and define

\[
 m_2:=\int_JX^2q_0(X)\,dX>0,
 \qquad
 m_4:=\int_JX^4q_0(X)\,dX>0.
 \tag{3.3}
\]

The parity relations are

\[
 \int_JXq_0=\int_JX^3q_0=\int_Jq_1=0,
 \tag{3.4}
\]

while

\[
 \int_JXq_1=m_2,
 \qquad
 \int_JX^3q_1=m_4.
 \tag{3.5}
\]

### Exact rational-probe calibration

The smooth choice in (3.1) is convenient, but the proof uses only

\[
 q_0,\;Xq_0\in H_0^1(J)
 \tag{3.6}
\]

together with normalization, parity, and finite second and fourth moments.
If the chart \(J\) contains \([-1,1]\), the rational probe

\[
 \rho(X)=
 \frac{315}{256}(1-X^2)^4\mathbf 1_{[-1,1]}(X)
 \tag{3.7}
\]

is admissible.  Its exact ledger is

\[
 \int_J\rho=1,
 \qquad
 \mu_2:=\int_JX^2\rho(X)\,dX=\frac1{11},
 \qquad
 \mu_4:=\int_JX^4\rho(X)\,dX=\frac3{143}.
 \tag{3.8}
\]

For \(T=1\), the sufficient escaping-center threshold used in Section 6 is

\[
 2T+\frac{\mu_4}{3\mu_2}
 =2+\frac1{13}
 =\frac{27}{13}.
 \tag{3.9}
\]

These rational identities provide a finite exact certificate target.  Such a
ledger checks the normalization, moments, and threshold arithmetic.  It does
not machine-check the compactness argument, the graph-space trace theorem, or
the functional-analytic passage to the limit.

### Lemma 3.1: weighted Poincare inequality

For \(w\in H^1(J)\), define

\[
 a=\int_Jw(X)q_0(X)\,dX.
 \tag{3.10}
\]

Then there is a fixed constant \(C_P\) such that

\[
 \|w-a\|_{L^2(J)}
 \le C_P\|w_X\|_{L^2(J)}.
 \tag{3.11}
\]

#### Proof

Let

\[
 \bar w=\frac1{|J|}\int_Jw.
 \tag{3.12}
\]

Ordinary mean-zero Poincare gives

\[
 \|w-\bar w\|_2\le C_J\|w_X\|_2.
 \tag{3.13}
\]

Since \(\int q_0=1\),

\[
 |a-\bar w|
 =\left|\int_J(w-\bar w)q_0\right|
 \le\|q_0\|_2\|w-\bar w\|_2.
 \tag{3.14}
\]

Combining (3.13) and (3.14) proves (3.11).  No boundary value of \(w\) was
used.  \(\square\)

For \(v\in\mathcal G_c\), put

\[
 A(t)=\int_Jv(t,X)q_0(X)\,dX,
 \qquad
 r(t,X)=v(t,X)-A(t),
 \tag{3.15}
\]

and

\[
 B(t)=\int_Jv(t,X)q_1(X)\,dX.
 \tag{3.16}
\]

Lemma 3.1 gives

\[
 \|r\|_{L^2(Q)}
 \le C_P\|v_X\|_{L^2(Q)}.
 \tag{3.17}
\]

Because \(\int q_1=0\),

\[
 B(t)=\int_Jr(t,X)q_1(X)\,dX,
 \tag{3.18}
\]

and hence

\[
 \|B\|_{L^2(I)}
 \le C_B\|v_X\|_{L^2(Q)}
 \tag{3.19}
\]

for a fixed \(C_B\).  Finally,

\[
 \sqrt{|J|}\,\|A\|_{L^2(I)}
 \le\|v\|_{L^2(Q)}+C_P\|v_X\|_{L^2(Q)},
 \tag{3.20}
\]

and

\[
 \|v\|_{L^2(Q)}
 \le\sqrt{|J|}\,\|A\|_{L^2(I)}
 +C_P\|v_X\|_{L^2(Q)}.
 \tag{3.21}
\]

---

## 4. The two scalar moment equations and graph-space traces

Let

\[
 g=P_cv.
 \tag{4.1}
\]

Then

\[
 \partial_tv=g+i\sigma V_cv
 \in L^2(I;H_D^{-1}(J)).
 \tag{4.2}
\]

Thus \(v\in H^1(I;H_D^{-1}(J))\), and therefore \(v\) has an
\(H_D^{-1}(J)\)-valued representative continuous up to \(t=\pm T\):

\[
 v\in C(\overline I;H_D^{-1}(J)).
 \tag{4.3}
\]

No \(L^2(J)\) endpoint trace is used or claimed.  Pairing (4.2) with the
fixed functions \(q_0,q_1\in H_0^1(J)\) shows that

\[
 A,B\in H^1(I).
 \tag{4.4}
\]

The endpoint values used below are therefore legitimate scalar traces.

Pairing (4.2) with \(q_0\), using (3.4), gives

\[
 A'
 =i\sigma\int_JV_c(t,X)r(t,X)q_0(X)\,dX
 +G_0(t),
 \tag{4.5}
\]

where

\[
 G_0(t)=\langle g(t),q_0\rangle.
 \tag{4.6}
\]

Consequently, for a fixed constant \(D_A\),

\[
 \|A'\|_{L^2(I)}
 \le D_A\left[
 (1+|c|)\|v_X\|_{L^2(Q)}
 +\|g\|_{L^2(I;H_D^{-1}(J))}
 \right].
 \tag{4.7}
\]

Pairing with \(q_1\), using (3.5), gives the second exact equation

\[
 B'=i\sigma K_c(t)A+E,
 \tag{4.8}
\]

where

\[
 K_c(t)=m_4+6(c+t)m_2,
 \tag{4.9}
\]

and

\[
 E(t)=i\sigma\int_JV_c(t,X)r(t,X)q_1(X)\,dX
 +\langle g(t),q_1\rangle.
 \tag{4.10}
\]

For another fixed constant \(D_E\),

\[
 \|E\|_{L^2(I)}
 \le D_E\left[
 (1+|c|)\|v_X\|_{L^2(Q)}
 +\|g\|_{L^2(I;H_D^{-1}(J))}
 \right].
 \tag{4.11}
\]

Only the fixed test functions \(q_0,q_1\) are inserted into the negative
Sobolev pairing.  No unproved multiplication property for \(H_D^{-1}\) is
used.

---

## 5. Proof of Theorem 2.1: bounded centers

Assume that (2.7) is false.  There are centers \(c_n\in\mathbb R\) and
functions \(v_n\in\mathcal G_{c_n}\) such that

\[
 \|v_n\|_{L^2(Q)}=1,
 \tag{5.1}
\]

while

\[
 \delta_n:=\|(v_n)_X\|_{L^2(Q)}\longrightarrow0,
 \qquad
 \varepsilon_n:=\|P_{c_n}v_n\|_{L^2H_D^{-1}}
 \longrightarrow0.
 \tag{5.2}
\]

Equations (3.17), (3.20), and (3.21) imply

\[
 \|r_n\|_{L^2(Q)}\le C_P\delta_n\longrightarrow0,
 \tag{5.3}
\]

and

\[
 \sqrt{|J|}\,\|A_n\|_{L^2(I)}
 \ge1-C_P\delta_n.
 \tag{5.4}
\]

First suppose that \(c_n\) is bounded.  Pass to a subsequence with

\[
 c_n\longrightarrow c_\infty.
 \tag{5.5}
\]

By (4.7),

\[
 \|A_n'\|_{L^2(I)}
 \le C(\delta_n+\varepsilon_n)
 \longrightarrow0.
 \tag{5.6}
\]

The sequence \(A_n\) is bounded in \(H^1(I)\).  After taking a further
subsequence,

\[
 A_n\longrightarrow a
 \quad\text{strongly in }L^2(I),
 \tag{5.7}
\]

where \(a\) is a constant.  By (3.19),

\[
 B_n\longrightarrow0
 \quad\text{strongly in }L^2(I).
 \tag{5.8}
\]

It follows that

\[
 B_n'\longrightarrow0
 \quad\text{in }H^{-1}(I),
 \tag{5.9}
\]

because for every \(\varphi\in H_0^1(I)\),

\[
 |\langle B_n',\varphi\rangle|
 =\left|\int_IB_n\varphi'\right|
 \le\|B_n\|_2\|\varphi'\|_2.
 \tag{5.10}
\]

At the same time, (4.8), (4.11), and (5.7) imply in distributions that

\[
 B_n'
 \longrightarrow
 i\sigma\left[m_4+6(c_\infty+t)m_2\right]a.
 \tag{5.11}
\]

Hence

\[
 \left[m_4+6(c_\infty+t)m_2\right]a=0
 \quad\text{for almost every }t\in I.
 \tag{5.12}
\]

The affine factor in (5.12) has nonzero slope \(6m_2\).  It cannot vanish on
an interval.  Therefore \(a=0\), contradicting the lower bound (5.4).

---

## 6. Proof of Theorem 2.1: centers escaping to infinity

It remains to exclude a subsequence for which

\[
 C_n:=|c_n|\longrightarrow\infty.
 \tag{6.1}
\]

Suppress the index temporarily and write

\[
 C=|c|,
 \qquad
 \delta=\|v_X\|_{L^2(Q)},
 \qquad
 \varepsilon=\|P_cv\|_{L^2H_D^{-1}},
 \qquad
 \|v\|_2=1.
 \tag{6.2}
\]

Choose

\[
 C_*=2T+\frac{m_4}{3m_2}.
 \tag{6.3}
\]

If \(C\ge C_*\), then \(K_c(t)\) has one sign throughout \(I\), and

\[
 |K_c(t)|\ge3m_2C
 \qquad(t\in I).
 \tag{6.4}
\]

Multiply (4.8) by \(\overline A\), integrate on \(I\), and integrate the
term containing \(B'\) by parts without deleting its endpoints.  This gives

\[
 \begin{aligned}
 3m_2C\|A\|_{L^2(I)}^2
 \le{}&|B(T)A(T)|+|B(-T)A(-T)|\\
 &+\|B\|_{L^2(I)}\|A'\|_{L^2(I)}
 +\|E\|_{L^2(I)}\|A\|_{L^2(I)}.
 \end{aligned}
 \tag{6.5}
\]

There is no assumption that \(A\) or \(B\) vanishes at either endpoint.

For normalized \(v\), equations (3.20), (4.7), and (4.11) give fixed
constants \(A_*,D_A,D_E\) such that, once \(\delta,\varepsilon\le1\),

\[
 \|A\|_2\le A_*,
 \tag{6.6}
\]

\[
 \|A'\|_2\le D_A[(1+C)\delta+\varepsilon],
 \tag{6.7}
\]

and

\[
 \|E\|_2\le D_E[(1+C)\delta+\varepsilon].
 \tag{6.8}
\]

Equation (4.8) then implies, for a fixed \(D_B\),

\[
 \|B'\|_2\le D_BC
 \tag{6.9}
\]

when \(C\ge C_*\).

For every scalar \(h\in H^1(-T,T)\), the endpoint trace inequality

\[
 |h(\pm T)|^2
 \le\frac1{2T}\|h\|_2^2
 +2\|h\|_2\|h'\|_2
 \tag{6.10}
\]

follows by averaging the fundamental theorem of calculus over the other
endpoint variable.  Apply it first to \(B\).  Equations (3.19) and (6.9)
give

\[
 |B(\pm T)|
 \le D_{B,0}\delta+D_{B,1}\sqrt{C\delta}.
 \tag{6.11}
\]

Apply (6.10) to \(A\).  Equations (6.6) and (6.7) give

\[
 |A(\pm T)|
 \le D_{A,0}+D_{A,1}\sqrt{C\delta+\delta+\varepsilon}.
 \tag{6.12}
\]

Consequently,

\[
 \begin{aligned}
 \frac{|B(\pm T)A(\pm T)|}{C}
 \le D_0\bigg(&
 \delta+\sqrt{\frac\delta C}
 +\sqrt{\frac{\delta\varepsilon}{C}}\\
 &+\frac{\delta+\sqrt\varepsilon}{C}
 \bigg).
 \end{aligned}
 \tag{6.13}
\]

This estimate allows \(C\delta\) to be arbitrarily large.  It requires only

\[
 C\to\infty,
 \qquad \delta\to0,
 \qquad \varepsilon\to0.
 \tag{6.14}
\]

The two interior terms in (6.5) satisfy

\[
 \frac{\|B\|_2\|A'\|_2}{C}
 \le D_1\left(
 \delta^2+\frac{\delta^2}{C}
 +\frac{\delta\varepsilon}{C}
 \right),
 \tag{6.15}
\]

and

\[
 \frac{\|E\|_2\|A\|_2}{C}
 \le D_2\left(
 \delta+\frac\delta C+\frac\varepsilon C
 \right).
 \tag{6.16}
\]

Divide (6.5) by \(C\) and insert (6.13)--(6.16).  Along the alleged
counterexample sequence,

\[
 \|A_n\|_{L^2(I)}\longrightarrow0.
 \tag{6.17}
\]

This contradicts (5.4).  The cases of bounded centers and escaping centers
exhaust every sequence.  Theorem 2.1 follows.

---

## 7. Exact inviscid gauge calibration

The exact kernel of \(P_c\) gives an independent check on the mechanism.  If

\[
 P_cv=0,
 \tag{7.1}
\]

then

\[
 v(t,X)=f(X)
 \exp\left\{
 i\sigma\left[tX^3+6ctX+3t^2X\right]
 \right\}.
 \tag{7.2}
\]

For each fixed \(X\), set

\[
 q_{c,X}(t)=
 \sigma\left[3t(X^2+2c)+3t^2\right].
 \tag{7.3}
\]

Its time mean is \(\sigma T^2\).  Expanding around that mean gives the exact
identity

\[
 \begin{aligned}
 &\frac1{2T}\int_{-T}^{T}
 \left|f_X(X)+iq_{c,X}(t)f(X)\right|^2dt\\
 &\quad=
 \left|f_X(X)+i\sigma T^2f(X)\right|^2\\
 &\qquad+
 \left[
 3T^2(X^2+2c)^2+\frac45T^4
 \right]|f(X)|^2.
 \end{aligned}
 \tag{7.4}
\]

Equivalently, optimization over an arbitrary initial phase gradient gives

\[
 \begin{aligned}
 &\min_{a\in\mathbb R}
 \frac1{2T}\int_{-T}^{T}
 \left|
 a+\sigma\left[3t(X^2+2c)+3t^2\right]
 \right|^2dt\\
 &\hspace{34mm}
 =3T^2(X^2+2c)^2+\frac45T^4.
 \end{aligned}
 \tag{7.5}
\]

The minimizer is \(a=-\sigma T^2\).  The odd term

\[
 3\sigma t(X^2+2c)
 \tag{7.6}
\]

and the centered even term

\[
 \sigma(3t^2-T^2)
 \tag{7.7}
\]

are orthogonal in \(L^2(-T,T)\).  Therefore every exact inviscid solution
satisfies

\[
 \boxed{
 \|v_X\|_{L^2(Q)}^2
 \ge\frac45T^4\|v\|_{L^2(Q)}^2.}
 \tag{7.8}
\]

Thus no exact gauge, large-center wave packet, or endpoint-free inviscid mode
can violate Theorem 2.1.

The dependence on the fixed time length is essential.  At \(c=0\), set

\[
 v_T(t,X)=
 \exp\left\{
 i\sigma(tX^3+3t^2X-T^2X)
 \right\}.
 \tag{7.9}
\]

Then \(P_0v_T=0\), while direct integration on
\((-T,T)\times(-R,R)\) gives

\[
 \frac{\|(v_T)_X\|_2^2}{\|v_T\|_2^2}
 =\frac35T^2R^4+\frac45T^4.
 \tag{7.10}
\]

Hence no constant can remain uniform as \(T\downarrow0\).  The theorem fixes
the positive block length before claiming center-uniformity.

---

## 8. Local dissipative-solution observability

Consider a dissipative solution on the same chart satisfying

\[
 P_cu=u_{XX}
 \tag{8.1}
\]

in \(L^2(I;H_D^{-1}(J))\).  Since

\[
 \|u_{XX}\|_{H_D^{-1}(J)}
 \le\|u_X\|_{L^2(J)},
 \tag{8.2}
\]

Theorem 2.1 applied directly to \(u\), without a time cutoff, yields

\[
 \boxed{
 \|u\|_{L^2(I\times J)}
 \le2C_{R,T}\|u_X\|_{L^2(I\times J)}.}
 \tag{8.3}
\]

This is the closed local solution-observability statement.

If the bounded-chart evolution also has an energy identity

\[
 E(T)^2
 +2\int_{-T}^{T}\|u_X(t)\|_{L^2(J)}^2dt
 =E(-T)^2,
 \qquad
 E(t)=\|u(t)\|_{L^2(J)},
 \tag{8.4}
\]

then \(E\) is nonincreasing and

\[
 \|u\|_{L^2(I\times J)}^2
 \ge2T E(T)^2.
 \tag{8.5}
\]

Combining (8.3)--(8.5) gives a strict bounded-chart contraction

\[
 E(T)
 \le\rho_{R,T}E(-T),
 \qquad
 \rho_{R,T}:=
 \frac{C_{R,T}}{\sqrt{T+C_{R,T}^2}}<1.
 \tag{8.6}
\]

Formula (8.6) uses the finite constant supplied by Theorem 2.1.  It is not an
explicit numerical contraction rate because this section does not quantify
that constant.

The inviscid equation \(P_cu=0\) remains unitary in \(L^2\).  Thus graph
coercivity alone is not a contraction theorem.  The energy identity in (8.4)
is the step that converts accumulated spatial gradient into norm loss.

---

## 9. Whole-line tail and block boundary

For a whole-line solution, restriction to \(J=(-R,R)\) gives

\[
 \|u\|_{L^2(I\times J)}
 \le2C_{R,T}\|u_X\|_{L^2(I\times J)}.
 \tag{9.1}
\]

The global energy identity controls the right-hand side from above.  It does
not provide the lower bound

\[
 \|u\|_{L^2(I\times J)}^2
 \ge2T\|u(T)\|_{L^2(\mathbb R)}^2
 \tag{9.2}
\]

used in the bounded-chart argument.  The mass may lie in
\(\mathbb R\setminus J\).

A spatial cutoff does not remove this problem.  For \(v=\eta u\),

\[
 v_X=\eta u_X+\eta'u,
 \tag{9.3}
\]

and rewriting \(P_c(\eta u)\) through the diffusive equation introduces the
annular terms

\[
 2\eta'u_X+\eta''u.
 \tag{9.4}
\]

These terms require an independent tail or nested-cutoff estimate.  The local
theorem does not absorb them by itself.

To close a whole-line block contraction, a later section must prove a bound of
the schematic form

\[
 \int_{-T}^{T}\int_{|X|>R}|u|^2\,dXdt
 \le \eta_R
 \int_{-T}^{T}\int_{\mathbb R}|u|^2\,dXdt
 +\text{controlled dissipation},
 \tag{9.5}
\]

with \(\eta_R<1\), uniformly in the interval center, together with absorption
of (9.4).  No such estimate is proved here.  All-start whole-line semigroup
iteration and transfer to the periodic heat path therefore remain open.

---

## 10. Exact boundary of the result

The closed statement is the center-uniform graph inequality on every fixed
bounded spatial chart, with arbitrary \(H^1\) spatial traces and arbitrary
graph-space temporal traces.  It yields uncut local solution observability and
a conditional bounded-chart dissipative contraction through the energy
identity.

It does not provide whole-line tightness, cutoff-commutator absorption,
periodic remainder control, nonlinear Navier--Stokes estimates, or a global
regularity theorem.  The release labels remain exactly those in (0.3).
