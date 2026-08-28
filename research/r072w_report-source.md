# R0.72W report source: exact-tail periodic contraction through an $A_2$ shear collision

**Date:** 2026-08-28

**Status:** a global weighted but nonabsorbed remainder estimate and a growing
collision-core absorption theorem are proved.  Global term-by-term absorption
of $H_5,H_7,R_9$ is proved false.  By retaining the exact trigonometric tail,
a unit-cell graph theorem uniform in the collision parameter is proved and
globalized both to the whole line and to the expanding physical torus.  The
exact periodic scalar Fourier row therefore has a strict contraction on one
collision-scale block.  Short-time uniformity, concatenation with the outer
heat-time intervals, nonlinear Navier--Stokes closure, and every Clay-level
consequence remain open.

**Keywords:** critical-point collision, exact heat path, analytic remainder,
periodic enhanced dissipation, negative Sobolev graph norm, compact--escaping
cell dichotomy, nonperturbative cancellation

---

## 0. What this section decides

R0.72T identified the exact collision path

\[
 W(d,x)=\frac12e^{-d}
 \left[-\sin x+\frac12e^{-3d}\sin 2x\right],
 \qquad W_d=W_{xx},
 \tag{0.1}
\]

and the unique collision scaling.  Put

\[
 \kappa=\frac{\varepsilon_c}{4},\qquad
 \alpha=\kappa^{-1/5},\qquad
 X=\alpha^{-1}x,\qquad S=\alpha^{-2}d.
 \tag{0.2}
\]

For \(0<\alpha\le1\), the exact rescaled real potential is

\[
 \boxed{
 V_\alpha(S,X)=\alpha^{-3}\left[
 2e^{-\alpha^2S}\sin(\alpha X)
 -e^{-4\alpha^2S}\sin(2\alpha X)
 \right].}
 \tag{0.3}
\]

It is periodic on

\[
 \mathbb T_\alpha
 :=\mathbb R/(2\pi/\alpha)\mathbb Z
 \tag{0.4}
\]

and satisfies the exact heat identity

\[
 \partial_SV_\alpha=\partial_X^2V_\alpha.
 \tag{0.5}
\]

Its bounded-chart expansion is

\[
 V_\alpha
 =H_3-\frac{\alpha^2}{4}H_5
 +\frac{\alpha^4}{40}H_7+\mathcal R_\alpha,
 \tag{0.6}
\]

where the next coefficient is

\[
 \mathcal R_\alpha
 =-\frac{17}{12096}\alpha^6H_9+O(\alpha^8H_{11}).
 \tag{0.7}
\]

The central decision is that (0.6) must **not** be treated as one global
small perturbation of $H_3$.  On the periodic scale

\[
 |X|\asymp\alpha^{-1}=\kappa^{1/5},
 \tag{0.8}
\]

all displayed heat polynomials have the same size.  R0.72W proves that the
naive global absorption is false, then bypasses it by proving a uniform graph
theorem directly for (0.3).

For $I=(-T,T)$, define

\[
 P_{\alpha,\sigma}
 =\partial_S-i\sigma V_\alpha(S,X),
 \qquad \sigma\in\{-1,1\}.
 \tag{0.9}
\]

The release labels are

\[
 \boxed{
 \begin{aligned}
 \texttt{weightedNonabsorbedRemainderEstimate}&=\texttt{CLOSED},\\
 \texttt{growingCoreAbsorption}&=\texttt{CLOSED},\\
 \texttt{globalTermwiseRemainderAbsorption}&=\texttt{FALSE},\\
 \texttt{exactFamilyUnitCellCoercivity}&=\texttt{CLOSED},\\
 \texttt{exactWholeLineGraphCoercivity}&=\texttt{CLOSED},\\
 \texttt{exactPeriodicGraphCoercivity}&=\texttt{CLOSED},\\
 \texttt{exactPeriodicBlockContraction}&=\texttt{CLOSED},\\
 \texttt{outerTimeConcatenation}&=\texttt{OPEN},\\
 \texttt{nonlinearNavierStokes}&=\texttt{OPEN},\\
 \texttt{Clay}&=\texttt{OPEN}.
 \end{aligned}}
 \tag{0.10}
\]

The completed contraction is a theorem for one exact linear scalar Fourier
row on a collision-scale block.  It is not a nonlinear stability threshold
and not a solution of the three-dimensional regularity problem.

---

## 1. A global envelope for the exact analytic tail

For fixed $T>0$, define

\[
 \begin{aligned}
 W_{5,T}(X)&=|X|^5+20T|X|^3+60T^2|X|,\\
 W_{7,T}(X)&=|X|^7+42T|X|^5+420T^2|X|^3+840T^3|X|,
 \end{aligned}
 \tag{1.1}
\]

and

\[
 \Omega_{9,T}(X)
 =\sum_{n=0}^4
 \frac{T^{4-n}|X|^{2n+1}}
 {(4-n)!(2n+1)!}.
 \tag{1.2}
\]

### Lemma 1.1: exact-tail envelope

For \(0<\alpha\le1\) and \(|S|\le T\),

\[
 \boxed{
 |\mathcal R_\alpha(S,X)|
 \le
 2\bigl(e^T+256e^{4T}\bigr)\alpha^6
 \Omega_{9,T}(X).}
 \tag{1.3}
\]

This bound is global in $X$.  It is not the fixed-chart $O_R(\alpha^6)$
notation of R0.72T.

### Proof

Expand each sine through degree seven.  The ninth-order Lagrange remainders
satisfy

\[
 |R_9(\alpha X)|\le\frac{\alpha^9|X|^9}{9!},
 \qquad
 |R_9(2\alpha X)|\le
 \frac{2^9\alpha^9|X|^9}{9!}.
 \tag{1.4}
\]

After division by \(\alpha^3\), these give the $n=4$ term in (1.3).
For the coefficients of (X,X^3,X^5,X^7), expand respectively

\[
 2(e^{-a}-e^{-4a}),\quad
 \frac{4e^{-4a}-e^{-a}}3,\quad
 \frac{e^{-a}-16e^{-4a}}{60},\quad
 \frac{64e^{-4a}-e^{-a}}{2520},
 \qquad a=\alpha^2S,
 \tag{1.5}
\]

through orders (3,2,1,0).  The exponential remainder formula, together
with \(0<\alpha\le1\), gives the other four terms in (1.3).  The factors
\(1,4^4=256,16\cdot4^2=256\), and \(64\cdot4=256\) explain the common safe
constant.  The retained coefficients are exactly those of
\(H_3-\alpha^2H_5/4+\alpha^4H_7/40\).  This proves (1.3).

---

## 2. The strongest direct perturbative consequence of R0.72V

Let

\[
 P_{0,\sigma}=\partial_S-i\sigma H_3(S,X).
 \tag{2.1}
\]

On the weighted graph class for which the quantities below are finite,
R0.72V and

\[
 P_{0,\sigma}v
 =P_{\alpha,\sigma}v
 +i\sigma(V_\alpha-H_3)v
 \tag{2.2}
\]

give the following theorem.

### Theorem 2.1: weighted, nonabsorbed exact-tail estimate

For each fixed $T>0$,

\[
 \boxed{
 \begin{aligned}
 \|v\|_2\le C_T\bigg(&
 \|v_X\|_2
 +\|P_{\alpha,\sigma}v\|_{L^2_SH^{-1}_X}\\
 &+\frac{\alpha^2}{4}\|W_{5,T}v\|_2
 +\frac{\alpha^4}{40}\|W_{7,T}v\|_2\\
 &+2(e^T+256e^{4T})\alpha^6
 \|\Omega_{9,T}v\|_2\bigg).
 \end{aligned}}
 \tag{2.3}
\]

Here and below, unlabelled spacetime norms are over \(I\times\mathbb R\).
The use of the full nonhomogeneous negative norm is harmless because

\[
 \|f\|_{H^{-1}(\mathbb R)}\le\|f\|_{L^2(\mathbb R)}.
 \tag{2.4}
\]

The adjective `nonabsorbed` is essential: (2.3) records the weighted costs on
the right-hand side.  It does not claim that they are controlled by the two
unweighted graph terms.

---

## 3. Growing collision-core absorption and its exact scale

Suppose $v$ is supported in \(|X|\le R\).  Put

\[
 \begin{aligned}
 D_{\alpha,T}(R)
 :={}&\frac{\alpha^2}{4}W_{5,T}(R)
 +\frac{\alpha^4}{40}W_{7,T}(R)\\
 &+2(e^T+256e^{4T})\alpha^6\Omega_{9,T}(R).
 \end{aligned}
 \tag{3.1}
\]

If $C_TD_{\alpha,T}(R)<1$, (2.3) gives

\[
 \boxed{
 \|v\|_2\le
 \frac{C_T}{1-C_TD_{\alpha,T}(R)}
 \left(\|v_X\|_2
 +\|P_{\alpha,\sigma}v\|_{L^2H^{-1}}\right).}
 \tag{3.2}
\]

The leading restriction is

\[
 \alpha^2R^5\ll1.
 \tag{3.3}
\]

Since \(\alpha=\kappa^{-1/5}\), direct bounded-multiplier absorption therefore
allows

\[
 \boxed{R=o(\kappa^{2/25}).}
 \tag{3.4}
\]

At the critical choice \(R=r\kappa^{2/25}\), only the leading $H_5$ term
survives:

\[
 D_{\alpha,T}(R)=\frac{r^5}{4}+o(1).
 \tag{3.5}
\]

Thus a fixed sufficiently small $r>0$ remains admissible.  In the original
physical coordinate, this core has width

\[
 |x|\lesssim \alpha R
 =r\kappa^{-3/25}.
 \tag{3.6}
\]

This closes a genuine growing-core theorem, but the core is much smaller than
one physical period, whose rescaled radius is $O(\kappa^{1/5})$.

---

## 4. Why global term-by-term absorption is false

There are two independent obstructions.

### 4.1 The polynomial truncation is not relatively small on the whole line

Take a fixed smooth spacetime bump centered at $X=L$ and apply a time-only
phase that removes the value of $H_3$ at the cell center.  On the translated
coordinate $Y=X-L$,

\[
 H_3(S,L+Y)-H_3(S,L)
 =3L^2Y+3LY^2+Y^3+6SY,
 \tag{4.1}
\]

whereas

\[
 H_5(S,L+Y)-H_5(S,L)
 =5L^4Y+O_T(L^3).
 \tag{4.2}
\]

For a fixed bump with \(Y\phi\ne0\) in $H^{-1}$, the centered correction
therefore obeys

\[
 \frac{\|\alpha^2[H_5(S,X)-H_5(S,L)]v_L\|_{L^2H^{-1}}}
 {\|v_{L,X}\|_2+
 \|P_{0,\sigma}v_L\|_{L^2H^{-1}}}
 \asymp \alpha^2L^2.
 \tag{4.3}
\]

For fixed \(\alpha>0\), this ratio is unbounded as \(L\to\infty\).  Hence the
whole-line polynomial correction is not a relatively small perturbation of
the cubic graph operator.

### 4.2 Smallness already fails at one-period scale

On the growing torus choose a cell center

\[
 X_\alpha=\frac\pi\alpha-c,
 \qquad c\ne0\text{ fixed}.
 \tag{4.4}
\]

After removing cellwise scalar phases, the cubic slope is

\[
 H_{3,X}(0,X_\alpha)
 =3\pi^2\alpha^{-2}+O(\alpha^{-1}),
 \tag{4.5}
\]

while the exact slope is

\[
 V_{\alpha,X}(0,X_\alpha)
 =-4\alpha^{-2}+O(1).
 \tag{4.6}
\]

Therefore the centered spatial variation of \(V_\alpha-H_3\), relative to
that of $H_3$, tends to

\[
 -1-\frac{4}{3\pi^2}\ne0.
 \tag{4.7}
\]

Already the centered correction $\alpha^2H_5/4$ has relative slope ratio

\[
 \frac{5\pi^2}{12}+o(1)>4.
 \tag{4.8}
\]

For the combined (H_5,H_7) correction, the absolute limiting ratio is

\[
 \left|-\frac{5\pi^2}{12}+\frac{7\pi^4}{120}\right|
 \approx1.570.
 \tag{4.9}
\]

Thus even a relative constant smaller than one is impossible for these
termwise corrections on a whole expanding period; a fortiori, no (o(1))
bound can hold.
This is invariant under time-only scalar gauges and is not an artifact of a
large constant value of the potential.

The exact sine series remains bounded and periodic only because infinitely
many polynomial terms cancel.  Those cancellations must be retained.

---

## 5. Exact derivative ledger on a unit cell

The first four spatial derivatives of (0.3) are

\[
 V_{\alpha,X}
 =2\alpha^{-2}\left[
 e^{-\alpha^2S}\cos(\alpha X)
 -e^{-4\alpha^2S}\cos(2\alpha X)
 \right],
 \tag{5.1}
\]

\[
 V_{\alpha,XX}
 =2\alpha^{-1}\left[
 -e^{-\alpha^2S}\sin(\alpha X)
 +2e^{-4\alpha^2S}\sin(2\alpha X)
 \right],
 \tag{5.2}
\]

\[
 V_{\alpha,XXX}
 =-2e^{-\alpha^2S}\cos(\alpha X)
 +8e^{-4\alpha^2S}\cos(2\alpha X),
 \tag{5.3}
\]

\[
 V_{\alpha,XXXX}
 =\alpha\left[
 2e^{-\alpha^2S}\sin(\alpha X)
 -16e^{-4\alpha^2S}\sin(2\alpha X)
 \right].
 \tag{5.4}
\]

Consequently, on \(|S|\le T\),

\[
 |V_{XXX}|\le M_{3,T}:=2e^T+8e^{4T},
 \qquad
 |V_{XXXX}|\le\alpha M_{4,T},
 \tag{5.5}
\]

where

\[
 M_{4,T}:=2e^T+16e^{4T}.
 \tag{5.6}
\]

The heat identity adds the decisive time ledger

\[
 \partial_SV_{\alpha,X}=V_{\alpha,XXX},
 \qquad
 \partial_S\left(\frac12V_{\alpha,XX}\right)
 =\frac12V_{\alpha,XXXX}.
 \tag{5.7}
\]

Thus a possibly large cell slope changes at rate $O_T(1)$, and a possibly
large cell curvature changes at rate $O_T(\alpha)$.  An escaping coefficient
direction cannot rotate at its own large scale during one fixed $S$-block.

There is also an exact two-row finite-type identity.  Put

\[
 A=e^{-\alpha^2S}\cos(\alpha X),
 \qquad
 B=e^{-4\alpha^2S}\cos(2\alpha X).
 \tag{5.8}
\]

Then

\[
 \begin{pmatrix}
 \alpha^2V_X/2\\ V_{SX}/2
 \end{pmatrix}
 =
 \begin{pmatrix}1&-1\\-1&4\end{pmatrix}
 \begin{pmatrix}A\\B\end{pmatrix}.
 \tag{5.9}
\]

The matrix determinant is \(3\), and

\[
 \cos^2z+\cos^22z
 =4\cos^4z-3\cos^2z+1
 \ge\frac7{16}.
 \tag{5.10}
\]

Consequently, for every fixed \(T\), there is an explicit \(c_T>0\) such
that

\[
 \boxed{
 |\alpha^2V_X(S,X)|+|V_{SX}(S,X)|\ge c_T}
 \tag{5.11}
\]

for all \(0<\alpha\le1\), \(|S|\le T\), and \(X\in\mathbb R\).  No point can
have both a small scaled spatial slope and a small temporal sweep.  The
compact--escaping proof below is still required because (5.11) alone is not
the full negative-Sobolev graph estimate.

---

## 6. Uniform cell geometry and the normalized probe

Let \(1\le\ell\le2\),

\[
 J_\ell=(-\ell/2,\ell/2),
 \tag{6.1}
\]

and scale the exact R0.72V probe by

\[
 q_\ell(y)=\ell^{-1}q_0(y/\ell),
 \qquad
 q_0(y)=\frac{315}{128}(1-4y^2)^4
 \mathbf1_{[-1/2,1/2]}(y).
 \tag{6.2}
\]

Then \(q_\ell\ge0\), it is even, has unit integral, and all polynomial
multiples used below belong to $H_0^1(J_\ell)$.  Its moments are

\[
 \mu_{2,\ell}=\frac{\ell^2}{44},
 \qquad
 \mu_{4,\ell}=\frac{3\ell^4}{2288},
 \qquad
 \mu_{4,\ell}-\mu_{2,\ell}^2
 =\frac{5\ell^4}{6292}.
 \tag{6.3}
\]

Therefore, for \(\gamma^2+\beta^2=1\),

\[
 p_{\gamma,\beta,\ell}(y)
 =\gamma(y^2-\mu_{2,\ell})+\beta y
 \tag{6.4}
\]

satisfies

\[
 \int p_{\gamma,\beta,\ell}q_\ell=0,
 \tag{6.5}
\]

and

\[
 \int p_{\gamma,\beta,\ell}^2q_\ell
 =\gamma^2\frac{5\ell^4}{6292}
 +\beta^2\frac{\ell^2}{44}
 \ge\boxed{\frac5{6292}}=:\kappa_*.
 \tag{6.6}
\]

Weighted Poincare modulo constants and all relevant $H_0^1$ test norms are
uniform over the compact length interval \(1\le\ell\le2\).

Throughout the cell argument,

\[
 H_D^{-1}(J_\ell)
 :=\bigl(H_0^1(J_\ell),\|\cdot\|_{H^1(J_\ell)}\bigr)^*.
 \tag{6.7}
\]

Thus the local test space carries the full inherited, nonhomogeneous
\(H^1\) norm.  This convention is essential for the constant-one dual
direct-sum inequalities in Section 9.

---

## 7. The exact-family unit-cell theorem

For a cell center \(X_0\in\mathbb R\), set

\[
 \mathcal V_{\alpha,X_0}(S,y)
 =V_\alpha(S,X_0+y).
 \tag{7.1}
\]

The scalar mean

\[
 m_{\alpha,X_0,\ell}(S)
 =\int_{J_\ell}\mathcal V_{\alpha,X_0}(S,y)q_\ell(y)\,dy
 \tag{7.2}
\]

is removed by a time-only unitary phase.  Write the centered potential as

\[
 U_{\alpha,X_0,\ell}=\mathcal V_{\alpha,X_0}-m_{\alpha,X_0,\ell}.
 \tag{7.3}
\]

More explicitly, if

\[
 M_{\alpha,X_0,\ell}(S)=\int_0^S
 m_{\alpha,X_0,\ell}(s)\,ds,
 \qquad
 w=e^{-i\sigma M_{\alpha,X_0,\ell}}v,
 \tag{7.3a}
\]

then

\[
 (\partial_S-i\sigma U_{\alpha,X_0,\ell})w
 =e^{-i\sigma M_{\alpha,X_0,\ell}}
 (\partial_S-i\sigma\mathcal V_{\alpha,X_0})v.
 \tag{7.3b}
\]

The phase is independent of \(y\), so it preserves the spatial derivative,
the local negative norm, and every norm in (7.5).

### Theorem 7.1: uniform exact-family cell coercivity

For every fixed $T>0$, there is a finite \(C_T^{\rm cell}\), independent of

\[
 0<\alpha\le1,\quad X_0\in\mathbb R,\quad
 1\le\ell\le2,\quad\sigma\in\{-1,1\},
 \tag{7.4}
\]

such that (7.5) holds for every member of the maximal distributional graph
class

\[
 v\in L^2(I;H^1(J_\ell)),\qquad
 (\partial_S-i\sigma\mathcal V_{\alpha,X_0})v
 \in L^2(I;H_D^{-1}(J_\ell)).
 \tag{7.5a}
\]

Namely,

\[
 \boxed{
 \|v\|_{L^2(I\times J_\ell)}
 \le C_T^{\rm cell}\left(
 \|v_y\|_{L^2(I\times J_\ell)}
 +\|(
 \partial_S-i\sigma\mathcal V_{\alpha,X_0})v
 \|_{L^2(I;H_D^{-1}(J_\ell))}
 \right).}
 \tag{7.5}
\]

No spatial or temporal trace of \(v\) is prescribed.

---

## 8. Proof of Theorem 7.1: the compact--escaping dichotomy

Assume (7.5) fails.  After applying the scalar gauge and normalizing, there
are parameters and $v_n$ such that

\[
 \|v_n\|_2=1,
 \qquad
 \delta_n:=\|(v_n)_y\|_2\to0,
 \qquad
 \varepsilon_n:=\|g_n\|_{L^2H_D^{-1}}\to0,
 \tag{8.1}
\]

where

\[
 g_n=(\partial_S-i\sigma_nU_n)v_n.
 \tag{8.2}
\]

Define

\[
 A_n(S)=\int v_nq_{\ell_n},
 \qquad r_n=v_n-A_n.
 \tag{8.3}
\]

Uniform weighted Poincare gives

\[
 \|r_n\|_2\le C\delta_n.
 \tag{8.4}
\]

At the center time $S=0$, put

\[
 b_n=V_{\alpha_n,X}(0,X_{0,n}),
 \qquad
 a_n=\frac12V_{\alpha_n,XX}(0,X_{0,n}),
 \qquad
 \lambda_n=(a_n^2+b_n^2)^{1/2}.
 \tag{8.5}
\]

### 8.1 Bounded coefficients

Suppose \(\lambda_n\) is bounded.  If a subsequence has
\(\alpha_n\to\alpha_*>0\), periodicity, compactness of the phase center, and
\(\ell_n\to\ell_*\) give a smooth limiting centered trigonometric potential.
It is not spatially constant on an open interval.

Now suppose \(\alpha_n\to0\).  Write

\[
 \theta_n=\alpha_nX_{0,n}\pmod{2\pi},
 \qquad \theta_n\in[-\pi,\pi].
 \tag{8.6}
\]

At $S=0$,

\[
 b_n=2\alpha_n^{-2}
 (\cos\theta_n-\cos2\theta_n),
 \tag{8.7}
\]

\[
 a_n=\alpha_n^{-1}
 (-\sin\theta_n+2\sin2\theta_n).
 \tag{8.8}
\]

The common zeros of

\[
 \cos\theta-\cos2\theta
 =(1-\cos\theta)(2\cos\theta+1)
 \tag{8.9}
\]

and

\[
 -\sin\theta+2\sin2\theta
 =\sin\theta(4\cos\theta-1)
 \tag{8.10}
\]

consist only of \(\theta=0\pmod{2\pi}\).  Since the derivative of (8.10) at
zero is (3), boundedness of (8.7)--(8.8) gives

\[
 \theta_n=O(\alpha_n),
 \qquad X_{0,n}\pmod{2\pi/\alpha_n}=O(1).
 \tag{8.11}
\]

After a subsequence, the exact chart converges smoothly to a translate of

\[
 H_3(S,X)=X^3+6SX.
 \tag{8.12}
\]

In both bounded cases, $U_n$ is uniformly bounded.  Centering gives

\[
 \|A_n'\|_{L^2(I)}
 \le C(\delta_n+\varepsilon_n)\to0.
 \tag{8.13}
\]

Thus $A_n$ converges strongly to a time constant, and $v_n$ converges
strongly to the same spacetime constant.  Passing (8.2) to distributions
forces that constant times the nonconstant limiting centered potential to
vanish.  The constant is zero, contradicting (8.1).

### 8.2 Escaping coefficients

Now suppose \(\lambda_n\to\infty\).  Put

\[
 \gamma_n=a_n/\lambda_n,
 \qquad \beta_n=b_n/\lambda_n,
 \qquad p_n=p_{\gamma_n,\beta_n,\ell_n}.
 \tag{8.14}
\]

Taylor's theorem, (5.5), and (5.7) give the exact decomposition

\[
 \boxed{U_n(S,y)=\lambda_np_n(y)+h_n(S,y),}
 \tag{8.15}
\]

where

\[
 \|h_n\|_{L^\infty(I\times J_{\ell_n})}\le R_T
 \tag{8.16}
\]

with $R_T$ independent of $n$.  Indeed, the changes of the linear and
quadratic Taylor coefficients over $I$ are $O_T(1)$ and $O_T(\alpha_n)$,
while the cubic Taylor remainder is bounded by $M_{3,T}|y|^3/6$.

Define the adaptive scalar moment

\[
 B_n(S)=\int v_np_nq_{\ell_n}.
 \tag{8.17}
\]

Then

\[
 \|B_n\|_2\le C\delta_n,
 \tag{8.18}
\]

and direct pairing gives

\[
 B_n'
 =i\sigma_n
 [\lambda_n\kappa_n+\ell_n(S)]A_n+E_n,
 \tag{8.19}
\]

where

\[
 \kappa_n=\int p_n^2q_{\ell_n}\ge\kappa_*,
 \qquad
 |\ell_n(S)|\le C_TR_T,
 \tag{8.20}
\]

and

\[
 \|A_n'\|_2+\|E_n\|_2
 \le C_T[(1+\lambda_n)\delta_n+\varepsilon_n].
 \tag{8.21}
\]

For large \(n\), the real coefficient in (8.19) is at least
\(\lambda_n\kappa_*/2\).  Multiplying by \(\overline A_n\), integrating, and
keeping both scalar endpoints gives

\[
 \begin{aligned}
 \frac{\kappa_*}{2}\|A_n\|_2^2
 \le{}&
 \frac{|B_n(T)A_n(T)|+|B_n(-T)A_n(-T)|}{\lambda_n}\\
 &+\frac{\|B_n\|_2\|A_n'\|_2}{\lambda_n}
 +\frac{\|E_n\|_2\|A_n\|_2}{\lambda_n}.
 \end{aligned}
 \tag{8.22}
\]

The one-dimensional scalar trace inequality gives

\[
 |A_n(\pm T)|
 \le C_T\left[1+\sqrt{(1+\lambda_n)\delta_n+\varepsilon_n}\right],
 \tag{8.23}
\]

\[
 |B_n(\pm T)|
 \le C_T(\delta_n+\sqrt{\lambda_n\delta_n}).
 \tag{8.24}
\]

For completeness, put

\[
 \mathfrak h_n=(1+\lambda_n)\delta_n+\varepsilon_n.
 \tag{8.25}
\]

Expanding the endpoint product with (8.23)--(8.24) gives

\[
 \frac{|B_n(\pm T)A_n(\pm T)|}{\lambda_n}
 \le C_T\left(
 \sqrt{\frac{\delta_n}{\lambda_n}}+
 \delta_n+
 \frac{\delta_n^{3/2}}{\sqrt{\lambda_n}}+
 \sqrt{\frac{\delta_n\varepsilon_n}{\lambda_n}}+o(1)
 \right)\longrightarrow0.
 \tag{8.26}
\]

The two bulk terms satisfy

\[
 \frac{\|B_n\|_2\|A_n'\|_2}{\lambda_n}
 \le C_T\left(
 \delta_n^2+
 \frac{\delta_n^2+\delta_n\varepsilon_n}{\lambda_n}
 \right)\longrightarrow0,
 \tag{8.27}
\]

and

\[
 \frac{\|E_n\|_2\|A_n\|_2}{\lambda_n}
 \le C_T\left(
 \delta_n+
 \frac{\delta_n+\varepsilon_n}{\lambda_n}
 \right)\longrightarrow0.
 \tag{8.28}
\]

Thus every term on the right of (8.22) tends to zero.  In particular, no hypothesis \(\lambda_n\delta_n\to0\) is used.  Hence
\(A_n\to0\), contradicting (8.1) and (8.4).  Theorem 7.1 follows.

---

## 9. Whole-line and torus globalization

### 9.1 Whole line

Partition \(\mathbb R\) into unit intervals.  On each interval, translate to
$J_1$, apply the cellwise scalar gauge and Theorem 7.1.  For the restrictions
$g_j$ of $g\in H^{-1}(\mathbb R)$, zero extension gives

\[
 \sum_j\|g_j\|_{H_D^{-1}(J_j)}^2
 \le\|g\|_{H^{-1}(\mathbb R)}^2.
 \tag{9.1}
\]

Squaring and summing yields a constant independent of \(\alpha\):

\[
 \boxed{
 \|v\|_{L^2(I\times\mathbb R)}
 \le C_T^{\rm ex}\left(
 \|v_X\|_2
 +\|P_{\alpha,\sigma}v\|_{L^2H^{-1}(\mathbb R)}
 \right).}
 \tag{9.2}
\]

Here (9.2) is asserted for
\(v\in L^2(I;H^1(\mathbb R))\) with
\(P_{\alpha,\sigma}v\in L^2(I;H^{-1}(\mathbb R))\), with the operator
understood distributionally.

This theorem uses the exact periodic potential on the whole line.  It is not
a perturbation theorem for the polynomial truncation.

### 9.2 Expanding torus

Let \(L_\alpha=2\pi/\alpha\), \(N_\alpha=\lfloor L_\alpha\rfloor\), and

\[
 \ell_\alpha=L_\alpha/N_\alpha.
 \tag{9.3}
\]

For \(0<\alpha\le1\),

\[
 1\le\ell_\alpha<2.
 \tag{9.4}
\]

Partition \(\mathbb T_\alpha\) into \(N_\alpha\) equal cells.  Zero extension
of $H_0^1$ functions from the cells into $H^1(\mathbb T_\alpha)$ again
gives

\[
 \sum_{j=1}^{N_\alpha}
 \|g_j\|_{H_D^{-1}(J_{\ell_\alpha})}^2
 \le\|g\|_{H^{-1}(\mathbb T_\alpha)}^2.
 \tag{9.5}
\]

Therefore:

### Theorem 9.1: uniform exact-periodic graph coercivity

For every fixed $T>0$, there is \(C_T^{\rm per}<\infty\), independent of
\(0<\alpha\le1\) and \(\sigma\), such that

\[
 \boxed{
 \|v\|_{L^2(I\times\mathbb T_\alpha)}
 \le C_T^{\rm per}\left(
 \|v_X\|_{L^2(I\times\mathbb T_\alpha)}
 +\|P_{\alpha,\sigma}v\|_{L^2(I;H^{-1}(\mathbb T_\alpha))}
 \right).}
 \tag{9.6}
\]

The quantified graph class is
\(v\in L^2(I;H^1(\mathbb T_\alpha))\) with
\(P_{\alpha,\sigma}v\in
L^2(I;H^{-1}(\mathbb T_\alpha))\), again in the distributional sense.

The negative norm is the full nonhomogeneous dual

\[
 H^{-1}(\mathbb T_\alpha)=(H^1(\mathbb T_\alpha))^*.
 \tag{9.7}
\]

---

## 10. Exact periodic energy evolution and strict contraction

For every $u_-\in L^2(\mathbb T_\alpha)$, the smooth bounded real potential
\(V_\alpha\) gives a unique energy solution of

\[
 P_{\alpha,\sigma}u=u_{XX}
 \tag{10.1}
\]

in

\[
 u\in C(\overline I;L^2(\mathbb T_\alpha))
 \cap L^2(I;H^1(\mathbb T_\alpha)).
 \tag{10.2}
\]

It satisfies

\[
 \|u(S_2)\|_2^2
 +2\int_{S_1}^{S_2}\|u_X(S)\|_2^2\,dS
 =\|u(S_1)\|_2^2.
 \tag{10.3}
\]

Since

\[
 \|u_{XX}\|_{H^{-1}(\mathbb T_\alpha)}
 \le\|u_X\|_2,
 \tag{10.4}
\]

(9.6) yields

\[
 \|u\|_{L^2(I\times\mathbb T_\alpha)}
 \le2C_T^{\rm per}\|u_X\|_{L^2(I\times\mathbb T_\alpha)}.
 \tag{10.5}
\]

Let $E(S)=\|u(S)\|_2^2$.  Monotonicity and (10.3)--(10.5) give

\[
 T E(T)
 \le(C_T^{\rm per})^2[E(-T)-E(T)].
 \tag{10.6}
\]

Hence

\[
 \boxed{
 E(T)\le
 \frac{(C_T^{\rm per})^2}
 {T+(C_T^{\rm per})^2}E(-T).}
 \tag{10.7}
\]

Equivalently,

\[
 \boxed{
 \|u(T)\|_2\le q_T\|u(-T)\|_2,
 \qquad
 q_T:=\frac{C_T^{\rm per}}
 {\sqrt{T+(C_T^{\rm per})^2}}<1,}
 \tag{10.8}
\]

uniformly in \(0<\alpha\le1\) and \(\sigma\).

The existence of \(C_T^{\rm per}\) is nonconstructive.  The theorem does not
claim an optimal numerical value of $q_T$.

---

## 11. Exact return to the physical collision row

The declared physical Fourier row from R0.72T is

\[
 v_d=v_{xx}-i\sigma\varepsilon_cW(d,x)v,
 \qquad x\in\mathbb T_{2\pi}.
 \tag{11.1}
\]

With \(\varepsilon_c=4\kappa=4\alpha^{-5}\) and (0.2), direct substitution
gives

\[
 u_S=u_{XX}+i\sigma V_\alpha(S,X)u.
 \tag{11.2}
\]

Indeed,

\[
 V_\alpha(S,X)=-4\alpha^{-3}W(\alpha^2S,\alpha X),
 \tag{11.3}
\]

which is exactly (0.3).  No $H_5,H_7,R_9$ truncation occurs in this
conjugacy.

The \(L^2\) scaling factor is the same at both endpoints and cancels in the
ratio.  Therefore, for every \(\varepsilon_c\ge4\),

\[
 \boxed{
 \|v(T\kappa^{-2/5})\|_{L^2(\mathbb T_{2\pi})}
 \le q_T
 \|v(-T\kappa^{-2/5})\|_{L^2(\mathbb T_{2\pi})},}
 \tag{11.4}
\]

where $q_T<1$ is independent of \(\varepsilon_c\) and of the sign
\(\sigma\).

This closes the exact periodic collision-block transfer for the scalar row.
It does not yet concatenate the block with the pre-collision and
post-collision intervals.

---

## 12. Numerical stress test and its evidentiary role

A Fourier Strang-splitting calculation was used only as a stress test of the
analytic theorem.  It propagated the full exact potential (0.3), applied
power iteration to the discrete forward--adjoint product, and estimated the
largest singular value over \(S\in[-1,1]\).  Representative converged values
were

\[
 \begin{array}{c|c|c}
 \alpha&2\pi/\alpha&\|\mathcal U_\alpha(1,-1)\|_{2\to2}
 \\\hline
 1.00&6.2832&0.071285\\
 0.75&8.3776&0.119851\\
 0.50&12.5664&0.101230\\
 0.35&17.9520&0.080730\\
 0.25&25.1327&0.069833
 \end{array}
 \tag{12.1}
\]

For \(\alpha=0.25,0.35,0.50\), simultaneous refinement from
$(N,N_S)=(512,1000)$ to $(2048,4000)$ changed the reported norm by less
than \(1.3\times10^{-6}\).  These values support the absence of an obvious
numerical quasimode, but they are not used to prove (9.6) or (10.8), and they
do not evaluate the nonconstructive analytic constant \(C_T^{\rm per}\).

---

## 13. Literature boundary

Stationary finite-type shear theorems provide the expected enhanced-
dissipation scaling and localized spectral-gap mechanisms.  Time-dependent
theorems of Coble--He cover strictly monotone shears or a fixed finite family
of shared nondegenerate critical points whose neighborhoods remain separated.
Those assumptions fail at the present fold collision, where the number of
critical points changes and the two colliding points meet.

Static maximal estimates for imaginary polynomial potentials also do not
directly supply (9.6): their constants concern a fixed potential or a fixed
representation class, whereas R0.72W requires a nonautonomous family,
negative-Sobolev forcing, expanding domains, and uniformity as
\(\alpha\downarrow0\).

The closest references calibrate the context and methods.  None is invoked as
a black box for the compact--escaping proof above.  The bounded literature
search is not a proof of novelty or priority.

---

## 14. Exact claim boundary and next gate

R0.72W proves a stronger result than the initially proposed global weighted
absorption: the full analytic tail is retained, and the exact periodic
collision row contracts uniformly on its natural \(\kappa^{-2/5}\) time
block.  At the same time, the section proves why the tempting global
term-by-term route cannot work.

What remains open is substantial:

1. concatenate the collision block with uniform outer intervals where the
   exact shear has only ordinary nondegenerate critical points;
2. keep every Fourier normalization and scalar damping term in the return to
   the complete linearized shear subsystem;
3. sum the row estimates with constants compatible with the nonlinear
   convolution;
4. control pressure and vortex stretching in a three-dimensional bootstrap;
5. derive a genuinely unconditional continuation criterion.

The next finite gate is therefore:

\[
 \boxed{
 \text{R0.72X: outer }A_1\text{ blocks plus the }A_2
 \text{ collision block, with exact time concatenation}.}
 \tag{14.1}
\]

No statement in this report proves global smoothness or finite-time blow-up
for the three-dimensional incompressible Navier--Stokes equations.
