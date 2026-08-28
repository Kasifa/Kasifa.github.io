# R0.72X report source: all-center exact-path propagation and exact A1--A2--A1 time concatenation

**Date:** 2026-08-28

**Status:** the exact-family unit-cell theorem of R0.72W is extended from a
single collision-centered block to every scaled block whose physical time
center lies in a fixed compact interval.  Consecutive exact blocks give an
all-start semigroup estimate at the uniform collision rate
\(\varepsilon_c^{2/5}\), an integrated-energy bound at scale
\(\varepsilon_c^{-2/5}\), and an exact Duhamel kernel for the declared
periodic scalar Fourier row.  On fixed pre- and post-collision margins, the
time-dependent nondegenerate-shear theorem gives the faster \(A_1\) rate
\(\varepsilon_c^{1/2}\).  The true propagator factors through the two outer
\(A_1\) pieces and the exact \(A_2\) family without any gauge or endpoint
loss.  The fixed-shape \(A_1\) hypotheses cannot be pushed uniformly to the
shrinking collision interface.  The complete linearized shear subsystem,
row-dependent coupling sum, nonlinear Navier--Stokes closure, and the Clay
problem remain open.

**Keywords:** time-dependent shear, fold collision, enhanced dissipation,
all-start semigroup, compact--escaping dichotomy, exact propagator cocycle,
Fourier-row normalization, A1--A2 concatenation

---

## 0. Exact decision and claim boundary

The physical scalar row isolated in R0.72T is

\[
 \partial_d v=\partial_x^2v-i\sigma\varepsilon_cW(d,x)v,
 \qquad x\in\mathbb T_{2\pi},\quad \sigma\in\{-1,1\},
 \tag{0.1}
\]

where

\[
 W(d,x)=\frac12e^{-d}
 \left[-\sin x+\frac12e^{-3d}\sin2x\right],
 \qquad W_d=W_{xx}.
 \tag{0.2}
\]

The collision is at \((d,x)=(0,0)\).  For

\[
 \kappa=\frac{\varepsilon_c}{4},\qquad
 \alpha=\kappa^{-1/5},\qquad
 S=\alpha^{-2}d,\qquad X=\alpha^{-1}x,
 \tag{0.3}
\]

R0.72W proved a strict contraction on one fixed block centered at \(S=0\).
The missing point was not the algebraic cocycle identity.  It was uniformity
of the graph constant when the scaled block center moves as far as
\(O(\alpha^{-2})\).

This section proves that uniformity.  For every compact physical-time interval
\(K\Subset\mathbb R\) and fixed \(T>0\), there is one
\(q_{K,T}\in(0,1)\) such that every exact block

\[
 [S_0-T,S_0+T],\qquad \alpha^2S_0\in K,
 \tag{0.4}
\]

contracts by \(q_{K,T}\).  Hence, for any \([d_1,d_2]\subset K\),

\[
 \boxed{
 \|U_{\alpha}(d_2,d_1)\|_{2\to2}
 \le q_{K,T}^{\left\lfloor
 (d_2-d_1)/(2T\alpha^2)\right\rfloor}
 \le q_{K,T}^{-1}
 e^{-c_{K,T}(d_2-d_1)/\alpha^2},}
 \tag{0.5}
\]

where

\[
 c_{K,T}=\frac{|\log q_{K,T}|}{2T}>0.
 \tag{0.6}
\]

For homogeneous solutions,

\[
 \boxed{
 \int_{d_1}^{d_2}\|v(d)\|_2^2\,dd
 \le \frac{2T\alpha^2}{1-q_{K,T}^2}
 \|v(d_1)\|_2^2.}
 \tag{0.7}
\]

The labels frozen at this gate are

\[
\boxed{
\begin{aligned}
\texttt{allCenterExactFamilyGraphCoercivity}&=\texttt{CLOSED},\\
\texttt{allStartExactPathSemigroup}&=\texttt{CLOSED},\\
\texttt{allStartIntegratedA2Scale}&=\texttt{CLOSED},\\
\texttt{uniformTwistedPeriodicGraph}&=\texttt{CLOSED},\\
\texttt{strongRowDirectSumNoCountLoss}&=\texttt{CLOSED},\\
\texttt{fixedMarginA1EnhancedDissipation}&=\texttt{CLOSED},\\
\texttt{exactA1A2A1TimeConcatenation}&=\texttt{CLOSED},\\
\texttt{shrinkingInterfaceFixedShapeA1Hypotheses}&=\texttt{FALSE},\\
\texttt{prefactorOneAllGapExponential}&=\texttt{FALSE},\\
\texttt{allPhysicalRowsUniformContraction}&=\texttt{FALSE},\\
\texttt{forcedHMinusOneTransfer}&=\texttt{OPEN},\\
\texttt{completeLinearizedShearSubsystem}&=\texttt{OPEN},\\
\texttt{nonlinearNavierStokes}&=\texttt{OPEN},\\
\texttt{Clay}&=\texttt{OPEN}.
\end{aligned}}
\tag{0.8}
\]

The `shrinkingInterfaceFixedShapeA1Hypotheses=FALSE` label concerns the
fixed-radius, fixed-Morse-margin hypotheses of
the nondegenerate \(A_1\) black box at a shrinking interface.  It does not
assert that enhanced dissipation itself fails there.  The
exactA1A2A1TimeConcatenation label is restricted to the periodic
representative \(\beta=0\); Bloch-uniformity at this gate belongs to the
exact \(A_2\) family, not to the imported fixed-margin \(A_1\) theorem.

---

## 1. The shifted exact family

The exact rescaled potential is

\[
 V_\alpha(S,X)=\alpha^{-3}\left[
 2e^{-\alpha^2S}\sin(\alpha X)
 -e^{-4\alpha^2S}\sin(2\alpha X)
 \right].
 \tag{1.1}
\]

It is periodic on

\[
 \mathbb T_\alpha=\mathbb R/(2\pi/\alpha)\mathbb Z
 \tag{1.2}
\]

and satisfies \(V_{\alpha,S}=V_{\alpha,XX}\).  For a scaled block center
\(S_0\), write

\[
 D_0=\alpha^2S_0,
 \qquad \tau=S-S_0\in(-T,T).
 \tag{1.3}
\]

The shifted potential is therefore

\[
 V_{\alpha,S_0}(\tau,X)=\alpha^{-3}\left[
 2e^{-D_0-\alpha^2\tau}\sin(\alpha X)
 -e^{-4D_0-4\alpha^2\tau}\sin(2\alpha X)
 \right].
 \tag{1.4}
\]

If \(D_0\in K\) and \(|\tau|\le T\), the first derivatives needed in the
R0.72W argument obey

\[
 |V_{XXX}|\le M_{3,K,T},\qquad
 |V_{XXXX}|\le\alpha M_{4,K,T},
 \tag{1.5}
\]

for finite constants depending only on the enlarged compact interval

\[
 K_T=K+[-T,T].
 \tag{1.6}
\]

The enlargement is safe because \(0<\alpha\le1\).  The heat identity gives

\[
 \partial_\tau V_X=V_{XXX},\qquad
 \partial_\tau(V_{XX}/2)=V_{XXXX}/2.
 \tag{1.7}
\]

Thus the slope changes by \(O_{K,T}(1)\) and the curvature by
\(O_{K,T}(\alpha)\) on every shifted scaled block, exactly as at the
collision-centered block.

---

## 2. The only bounded-coefficient center is the collision chart

At \(\tau=0\) and a spatial cell center \(X_0\), put

\[
 \theta=\alpha X_0\pmod{2\pi},\qquad
 \theta\in[-\pi,\pi],
 \tag{2.1}
\]

and

\[
 b=V_X(S_0,X_0)
 =2\alpha^{-2}\left(e^{-D_0}\cos\theta
 -e^{-4D_0}\cos2\theta\right),
 \tag{2.2}
\]

\[
 a=\frac12V_{XX}(S_0,X_0)
 =\alpha^{-1}\left(-e^{-D_0}\sin\theta
 +2e^{-4D_0}\sin2\theta\right).
 \tag{2.3}
\]

The common-zero calculation is global in \(D_0\).  Multiply both brackets
by \(e^{4D_0}\) and put \(r=e^{3D_0}>0\).  A common zero satisfies

\[
 r\cos\theta=\cos2\theta,
 \qquad
 r\sin\theta=2\sin2\theta.
 \tag{2.4}
\]

If \(\sin\theta=0\), positivity of \(r\) leaves only
\((r,\theta)=(1,0)\).  If \(\sin\theta\ne0\), the second equation gives
\(r=4\cos\theta\), while the first gives

\[
 4\cos^2\theta=2\cos^2\theta-1,
 \tag{2.5}
\]

which is impossible over the reals.  Therefore

\[
 \boxed{(D_0,\theta)=(0,0)\pmod{2\pi}}
 \tag{2.6}
\]

is the only common zero for all real physical times.

For the unscaled brackets

\[
 f(D,\theta)=e^{-D}\cos\theta-e^{-4D}\cos2\theta,
 \tag{2.7}
\]

\[
 g(D,\theta)=-e^{-D}\sin\theta+2e^{-4D}\sin2\theta,
 \tag{2.8}
\]

the Jacobian at the common zero is

\[
 D(f,g)(0,0)=
 \begin{pmatrix}3&0\\0&3\end{pmatrix}.
 \tag{2.9}
\]

Suppose \(\alpha_n\downarrow0\), \(D_{0,n}\in K\), and the corresponding
\(a_n,b_n\) remain bounded.  Then

\[
 f(D_{0,n},\theta_n)=O(\alpha_n^2),
 \qquad
 g(D_{0,n},\theta_n)=O(\alpha_n).
 \tag{2.10}
\]

Compactness and (2.6) first give \((D_{0,n},\theta_n)\to(0,0)\).  The local
inverse estimate from (2.9) gives \(D_{0,n},\theta_n=O(\alpha_n)\).  Expanding
one order more,

\[
 g(D,\theta)=3\theta+O(|D\theta|+|\theta|^3),
 \tag{2.11}
\]

\[
 f(D,\theta)=3D+\frac32\theta^2
 +O(D^2+|D|\theta^2+\theta^4),
 \tag{2.12}
\]

and using (2.10) yields the sharp bounded-center conclusion

\[
 \boxed{\theta_n=O(\alpha_n),\qquad
 D_{0,n}=O(\alpha_n^2).}
 \tag{2.13}
\]

Consequently the spatial residue \(X_{0,n}\) and the scaled center
\(S_{0,n}=D_{0,n}/\alpha_n^2\) stay bounded.  After a subsequence, every
bounded-coefficient chart converges smoothly on compact sets to a translate
of

\[
 H_3(S,X)=X^3+6SX.
 \tag{2.14}
\]

This is the new compactness step absent from the collision-centered R0.72W
statement.

---

## 3. All-center unit-cell graph coercivity

Let \(J_\ell=(-\ell/2,\ell/2)\), \(1\le\ell\le2\), and retain the normalized
R0.72W probe \(q_\ell\).  For a spatial cell centered at \(X_0\), subtract
the probe mean

\[
 m(\tau)=\int_{J_\ell}
 V_\alpha(S_0+\tau,X_0+y)q_\ell(y)\,dy
 \tag{3.1}
\]

by the time-only unitary phase whose value is one at \(\tau=-T\).  This
normalization makes every block gauge an internal proof device; no phase is
identified across adjacent physical blocks.

### Theorem 3.1: compact-physical-time, all-center cell theorem

For every compact interval \(K\Subset\mathbb R\) and fixed \(T>0\), there is
\(C_{K,T}^{\rm cell}<\infty\), independent of

\[
 0<\alpha\le1,\quad D_0=\alpha^2S_0\in K,
 \quad X_0\in\mathbb R,\quad1\le\ell\le2,
 \quad\sigma\in\{-1,1\},
 \tag{3.2}
\]

such that

\[
 \boxed{
 \|w\|_{L^2((-T,T)\times J_\ell)}
 \le C_{K,T}^{\rm cell}\left(
 \|w_y\|_2+
 \|Q_{\alpha,S_0,X_0,\sigma}w\|_{L^2H_D^{-1}}
 \right),}
 \tag{3.3}
\]

where

\[
 Q_{\alpha,S_0,X_0,\sigma}
 =\partial_\tau-i\sigma
 V_\alpha(S_0+\tau,X_0+y)
 \tag{3.4}
\]

and

\[
 H_D^{-1}(J_\ell)=
 (H_0^1(J_\ell),\|\cdot\|_{H^1(J_\ell)})^*.
 \tag{3.5}
\]

The graph class is maximal and distributional:

\[
 w\in L^2((-T,T);H^1(J_\ell)),qquad
 Qw\in L^2((-T,T);H_D^{-1}(J_\ell)).
 \tag{3.6}
\]

### Proof

Repeat the normalized contradiction of R0.72W.  At the center time define
\(\lambda=(a^2+b^2)^{1/2}\) using (2.2)--(2.3).

If \(\lambda\) remains bounded and \(\alpha\) stays away from zero, the
parameters \((\alpha,D_0,\theta,\ell)\) are compact and the limiting exact
trigonometric potential is not spatially constant.  If \(\alpha\to0\),
Section 2 forces \(D_0=O(\alpha^2)\) and
\(\theta=O(\alpha)\); the limit is a translated \(H_3\) chart.  The scalar
average of a normalized counterexample becomes constant in time, and the
nonconstant limiting centered potential forces that constant to vanish.

If \(\lambda\to\infty\), Taylor expansion on the cell gives

\[
 U(\tau,y)=\lambda p_{\gamma,\beta,\ell}(y)+h(\tau,y),
 \qquad \|h\|_\infty\le R_{K,T},
 \tag{3.7}
\]

because of (1.5)--(1.7).  The adaptive probe variance remains

\[
 \int p_{\gamma,\beta,\ell}^2q_\ell
 \ge\frac5{6292}.
 \tag{3.8}
\]

The endpoint ledger of R0.72W then applies verbatim: changes of the linear
coefficient are \(O_{K,T}(1)\), changes of the quadratic coefficient are
\(O_{K,T}(\alpha)\), and no assumption
\(\lambda\|w_y\|_2\to0\) is used.  Both alternatives contradict the unit
normalization.  This proves (3.3).

The finite certificate checks (2.4)--(2.13), the derivative scaling, and the
block arithmetic.  It does not machine-check this compactness argument or
the scalar endpoint trace passage.

---

## 4. Torus globalization, Bloch twists, and a shifted exact block

Partition \(\mathbb T_\alpha\) into

\[
 N_\alpha=\lfloor2\pi/\alpha\rfloor
 \tag{4.1}
\]

equal cells.  Their common length lies in \([1,2)\).  Zero extension of
\(H_0^1\) test functions gives the same constant-one negative-Sobolev
direct-sum inequality as in R0.72W.  Theorem 3.1 therefore yields

\[
 \boxed{
 \|w\|_{L^2((-T,T)\times\mathbb T_\alpha)}
 \le C_{K,T}^{\rm per}\left(
 \|w_X\|_2+
 \|Q_{\alpha,S_0,\sigma}w\|_{L^2H^{-1}}
 \right).}
 \tag{4.2}
\]

For every \(L^2\) datum, the exact energy solution of

\[
 (\partial_\tau-i\sigma V_\alpha)w=w_{XX}
 \tag{4.3}
\]

satisfies

\[
 E(\tau_2)+2\int_{\tau_1}^{\tau_2}\|w_X\|_2^2\,d\tau
 =E(\tau_1).
 \tag{4.4}
\]

Using \(\|w_{XX}\|_{H^{-1}}\le\|w_X\|_2\) in (4.2) gives

\[
 \boxed{
 \|w(T)\|_2\le q_{K,T}\|w(-T)\|_2,
 \qquad
 q_{K,T}=\frac{C_{K,T}^{\rm per}}
 {\sqrt{T+(C_{K,T}^{\rm per})^2}}<1.}
 \tag{4.5}
\]

The constant is uniform in the physical block center, \(\alpha\), and the
sign.  It is not uniform as \(T\downarrow0\), and no numerical value of the
nonconstructive \(q_{K,T}\) is claimed.

The same statement holds for every Bloch phase.  Let

\[
 H_\vartheta^1(\mathbb T_\alpha)
 =\{w:w(X+2\pi/\alpha)=e^{i\vartheta}w(X)\}.
 \tag{4.6}
\]

Every zero-extended \(H_0^1\) cell test belongs to the twisted global test
space, so the negative-norm direct sum still has constant one.  The local
cell theorem does not read the global boundary phase, and the two twisted
endpoint terms cancel in integration by parts.  Thus (4.2)--(4.5) hold with
the same constants for every \(\vartheta\in\mathbb R/(2\pi\mathbb Z)\).

---

## 5. Exact block tiling and the all-start semigroup

Let \(d_1<d_2\) lie in the compact physical interval \(K\), and set

\[
 L_S=\frac{d_2-d_1}{\alpha^2},qquad
 N=\left\lfloor\frac{L_S}{2T}\right\rfloor.
 \tag{5.1}
\]

Starting at \(S_1=d_1/\alpha^2\), place \(N\) consecutive full blocks of
length \(2T\); the terminal remainder has length less than \(2T\).  Each
full block contracts by \(q_{K,T}\), while the remainder is an energy
contraction.  The exact evolution cocycle gives

\[
 \|U_\alpha(d_2,d_1)\|_{2\to2}\le q_{K,T}^N.
 \tag{5.2}
\]

Since \(\lfloor z\rfloor\ge z-1\), (0.5) follows with the unavoidable
prefactor \(q_{K,T}^{-1}\).  Omitting that prefactor would contradict strong
continuity on intervals shorter than one block.

Monotonicity bounds the energy integral over the \(j\)-th full block by
\(2Tq_{K,T}^{2j}E(S_1)\).  The terminal remainder is bounded by the next
term of the same geometric series.  Hence

\[
 \int_{S_1}^{S_2}E(S)\,dS
 \le\frac{2T}{1-q_{K,T}^2}E(S_1).
 \tag{5.3}
\]

Multiplication by \(dd=\alpha^2dS\) proves (0.7).

The semigroup kernel also gives the exact later-use bounds

\[
 \sup_{s\in K}\int_s^{\sup K}
 \|U_\alpha(d,s)\|_{2\to2}\,dd
 \le C_{K,T}\alpha^2,
 \tag{5.4}
\]

and, for \(L^2_x\)-valued forcing, the Duhamel convolution estimate

\[
 \left\|\int_{d_1}^dU_\alpha(d,s)F(s)\,ds
 \right\|_{L_d^2L_x^2}
 \le C_{K,T}\alpha^2\|F\|_{L_d^2L_x^2}.
 \tag{5.5}
\]

Equation (5.5) is an \(L^2_x\)-forcing statement.  No \(H^{-1}\)-forcing
or complete linearized-system estimate is inferred from it.

---

## 6. Exact physical normalization and scalar damping

Write a shear-direction frequency as \(m=r+nR\), choose a residue
representative \(r\), and put \(\beta_r=r/R\).  Use the unitary row Fourier
transform

\[
 (\mathcal F_{\rm row}f)(x)
 =(2\pi)^{-1/2}\sum_{n\in\mathbb Z}f_ne^{inx},
 \qquad
 \|\mathcal F_{\rm row}f\|_{L^2(0,2\pi)}
 =\|f\|_{\ell^2}.
 \tag{6.1}
\]

After the carrier-cell rescaling used in R0.72P--T, an orthogonal target
frequency contributes a nonnegative scalar damping \(\mu\).  The exact
residue-row equation has the form

\[
 \partial_dG=((\partial_x+i\beta_r)^2-\mu)G
 -i\sigma\varepsilon_cW(d,x)G.
 \tag{6.2}
\]

Under the collision scaling this becomes

\[
 u_S=\left[(\partial_X+i\alpha\beta_r)^2-\alpha^2\mu\right]u
 +i\sigma V_\alpha u.
 \tag{6.2a}
\]

The unitary gauge \(w=e^{i\alpha\beta_rX}u\) restores the ordinary
Laplacian, leaves the scalar term \(-\alpha^2\mu\) unchanged, and changes
the boundary condition:

\[
 w(X+2\pi/\alpha)=e^{2\pi i\beta_r}w(X).
 \tag{6.2b}
\]

Section 4 therefore gives exactly the same block factor for every residue.

For an interval beginning at \(d_1\), set

\[
 v(d)=e^{\mu(d-d_1)}G(d).
 \tag{6.3}
\]

Then \(v\) solves the undamped covariant version of (0.1).  Applying the
Bloch gauge (6.2b) gives

\[
 \boxed{
 \|G(d_2)\|_2
 \le e^{-\mu(d_2-d_1)}
 q_{K,T}^{\lfloor(d_2-d_1)/(2T\alpha^2)\rfloor}
 \|G(d_1)\|_2.}
 \tag{6.4}
\]

The spatial scaling from \(x\) to \(X\) multiplies both endpoint norms by
the same factor \(\alpha^{-1/2}\); it cancels in every operator-norm ratio.
The cellwise scalar gauges in Section 3 are unitary and start at phase one
on each proof block.  They never alter (6.4), and no gauge phase is matched
across two physical blocks.

The constants in (6.4) are independent of \(\sigma\), \(\mu\ge0\), and the
row residue used in (6.1).  For an orthogonal family with
\(\varepsilon_j\ge\varepsilon_{\min}\ge4\), put
\(\alpha_{\max}=(\varepsilon_{\min}/4)^{-1/5}\) and

\[
 N_{\min}=\left\lfloor
 \frac{d_2-d_1}{2T\alpha_{\max}^2}\right\rfloor.
 \tag{6.4a}
\]

Parseval then gives the direct-sum estimate

\[
 \sum_j\|G_j(d_2)\|_2^2
 \le q_{K,T}^{2N_{\min}}
 \sum_je^{-2\mu_j(d_2-d_1)}\|G_j(d_1)\|_2^2,
 \tag{6.5}
\]

with no row-count factor.

The physical coupling must nevertheless be restored before claiming a full
system theorem.  In the triangular model it has the form

\[
 \varepsilon_j=\frac{2|\delta K_{z,j}|a}{R^2}.
 \tag{6.6}
\]

Weakly coupled rows need not contain a collision block on the same scale.
If \(K_z=0\), \(\beta_r=0\), and \(\mu=0\), the spatial constant is an exact
nondecaying mode.  Consequently a uniform strict contraction over all
physical rows is false without a projection or a coupling floor.  The
complete linearized subsystem remains open.

---

## 7. Fixed-margin nondegenerate A1 blocks for \(\beta=0\)

Take the physical heat history inherited from R0.72S,

\[
 K_*=[-\log2,1-\log2],
 \tag{7.1}
\]

and fix, for concreteness,

\[
 \delta=\frac18.
 \tag{7.2}
\]

Both outer intervals

\[
 K_-=[-\log2,-\delta],
 \qquad
 K_+=[\delta,1-\log2]
 \tag{7.3}
\]

have positive length.  Indeed \(\log2>1/4\) follows from
\(e^{1/4}<4/3<2\), and \(\log2<3/4\) follows from
\(e^{3/4}>1+3/4+(3/4)^2/2>2\).

R0.72S proved that (0.2) has four distinct critical points before the fold,
two after it, and no degeneracy except at \(d=0\).  On each compact interval
in (7.3), the critical count is fixed.  Analyticity, the implicit-function
theorem, and compactness give:

1. a positive lower bound for critical-point separation;
2. a positive lower bound for \(|W_{xx}|\) at every critical point;
3. a positive lower bound for \(|W_x|\) outside fixed critical
   neighborhoods;
4. uniform spatial derivative and physical-time derivative bounds.

Put \(t=\varepsilon_c d\) and \(\eta=\varepsilon_c^{-1}\).  Then (0.1)
becomes

\[
 \partial_tv=\eta\partial_x^2v
 -i\sigma W(\eta t,x)v.
 \tag{7.4}
\]

On either fixed outer interval, the actual shear can be used as its own
reference shear in the Coble--He time-dependent nondegenerate theorem.  The
shape constants above are fixed, and

\[
 \|\partial_{tx}W(\eta t)\|_\infty
 \le C_\delta\eta
 \le \eta^{3/4},
 \qquad 0<\eta\le\min\{1,C_\delta^{-4}\},
 \tag{7.5}
\]

once \(\eta\) is sufficiently small.  Thus there are
\(C_{A_1,\delta}\ge1\), \(c_{A_1,\delta}>0\), and
\(\varepsilon_{A_1,\delta}<\infty\) such that the exact outer propagators
satisfy

\[
 \boxed{
 \|U(d_2,d_1)\|_{2\to2}
 \le C_{A_1,\delta}
 e^{-c_{A_1,\delta}\sqrt{\varepsilon_c}(d_2-d_1)}}
 \tag{7.6}
\]

whenever \([d_1,d_2]\) is a subinterval of either fixed outer interval and
\(\varepsilon_c\ge\varepsilon_{A_1,\delta}\).  The corresponding integrated
bound is

\[
 \int_{d_1}^{d_2}\|U(d,d_1)f\|_2^2\,dd
 \le C_{A_1,\delta}\varepsilon_c^{-1/2}\|f\|_2^2.
 \tag{7.7}
\]

These are fixed-margin statements.  No constant in (7.6) is asserted to be
uniform as \(\delta\downarrow0\).

---

## 8. Why the shrinking-interface A1 black box is not uniform

Let the R0.72W collision interface be

\[
 h_\alpha=T\alpha^2=T\kappa^{-2/5}.
 \tag{8.1}
\]

On the pre-collision side \(d=-h_\alpha\), the fold expansion gives the two
colliding critical points

\[
 x_\pm=\pm\sqrt{2T}\,\alpha+O_T(\alpha^3),
 \tag{8.2}
\]

and

\[
 |W_{xx}(-h_\alpha,x_\pm)|\asymp_T\alpha.
 \tag{8.3}
\]

Their separation and the Morse curvature floor both vanish.  On the
post-collision side,

\[
 W_x(h_\alpha,0)
 =\frac12(e^{-4h_\alpha}-e^{-h_\alpha})
 =-\frac32T\alpha^2+O_T(\alpha^4).
 \tag{8.4}
\]

Thus the away-gradient floor also vanishes.  The fixed critical-neighborhood
radius, fixed Morse lower bound, and fixed exterior-gradient lower bound in
the standard nondegenerate \(A_1\) theorem cannot remain uniform at (8.1).

The expected local rates nevertheless match the collision rate at the
interface:

\[
 (\varepsilon_c|W_{xx}|)^{1/2}
 \asymp\varepsilon_c^{1/2}\alpha^{1/2}
 \asymp\alpha^{-2},
 \tag{8.5}
\]

on the pre side, and

\[
 (\varepsilon_c|W_x|)^{2/3}
 \asymp\varepsilon_c^{2/3}\alpha^{4/3}
 \asymp\alpha^{-2}
 \tag{8.6}
\]

on the post side.  Equations (8.5)--(8.6) are scaling diagnostics, not a
parameter-dependent \(A_1\) theorem.  The all-center exact-family theorem
supplies the rigorous \(\alpha^{-2}\) propagation across this region.

---

## 9. Exact A1--A2--A1 time concatenation for the periodic representative

The fixed-margin input in Section 7 has been invoked for the periodic
representative \(\beta=0\).  Accordingly, this section proves the fast
\(A_1\)--\(A_2\)--\(A_1\) history estimate only for that representative.
Sections 4--6 remain uniform in every Bloch twist at the \(A_2\)
exact-family rate; no Bloch-uniform extension of the fixed-margin
Coble--He input is inferred.

Keep \(T=1/4\) and \(\delta=1/8\).  When

\[
 h_\alpha=T\alpha^2\le\delta,
 \tag{9.1}
\]

the true ungauged propagator has the exact cocycle factorization

\[
\begin{aligned}
 U(1-\log2,-\log2)
 ={}&U(1-\log2,\delta)
 U(\delta,h_\alpha)
 U(h_\alpha,-h_\alpha)\\
 &\times U(-h_\alpha,-\delta)
 U(-\delta,-\log2).
\end{aligned}
\tag{9.2}
\]

The first and last factors are the fixed-margin \(A_1\) pieces.  The middle
factor is the exact R0.72W \(A_2\) collision block.  The two shoulders are
energy contractions; alternatively, Section 5 fills the whole middle
interval by exact-family blocks at rate \(\alpha^{-2}\).  Therefore, above a
fixed coupling threshold,

\[
\boxed{
\begin{aligned}
 \|U(1-\log2,-\log2)\|_{2\to2}
 \le{}&C_{A_1,\delta}^2q_{K_*,T}
 \exp\{-c_{A_1,\delta}(1-2\delta)
 \sqrt{\varepsilon_c}\}.
\end{aligned}}
\tag{9.3}
\]

The exact-family tiling also gives an additional valid middle factor of the
form \(C\exp(-c\delta/\alpha^2)\), but (9.3) records only what is needed for
the fixed-history \(A_1\) rate.

The pre-collision \(A_1\) estimate gives

\[
 \int_{-\log2}^{-\delta}\|v(d)\|_2^2\,dd
 \le C\varepsilon_c^{-1/2}\|v(-\log2)\|_2^2.
 \tag{9.4}
\]

At \(-\delta\), the remaining energy is exponentially small.  Energy
monotonicity over the rest of the unit physical interval then gives

\[
 \boxed{
 \int_{-\log2}^{1-\log2}\|v(d)\|_2^2\,dd
 \le C\varepsilon_c^{-1/2}\|v(-\log2)\|_2^2,}
 \tag{9.5}
\]

and

\[
 \boxed{
 \|v(1-\log2)\|_2
 \le Ce^{-c\sqrt{\varepsilon_c}}
 \|v(-\log2)\|_2.}
 \tag{9.6}
\]

Increasing \(C\) covers the compact coupling range
\(4\le\varepsilon_c<\varepsilon_{A_1,\delta}\).  With scalar damping
restored, the terminal estimates gain the appropriate exponential damping
factor, while the integrated estimates never worsen.

For this fixed heat history, (9.5)--(9.6) already follow from the existence
of a positive-length pre-collision \(A_1\) interval plus energy monotonicity.
The new mathematical content of Sections 2--6 is stronger: arbitrary data
may start inside or next to the collision region, and the exact family still
has the uniform all-start \(\varepsilon_c^{2/5}\) semigroup (0.5).

---

## 10. Numerical stress test and evidentiary boundary

A Fourier Strang-splitting calculation propagates the full exact potential
(1.1) on blocks centered at several physical times \(D_0\).  A deterministic
Lanczos--Ritz calculation is applied to the discrete Hermitian operator
\(U^*U\).  Every new Krylov vector is reorthogonalized twice against the full
existing basis.  Starting at dimension 8, the code checks every 4 dimensions
through dimension 32.  At each checkpoint it forms the Ritz vector in the
full discrete space, recomputes \(U^*Uv\), and requires

\[
 \frac{\|U^*Uv-\lambda v\|_2}{|\lambda|}\le10^{-10}.
 \tag{10.1}
\]

A configuration that does not meet (10.1) by dimension 32 fails rather than
emitting a norm estimate.  A Krylov breakdown before dimension 8 is also
rejected conservatively, even when it could represent an exact early closure.
The scan is designed to search for an outer-center
quasimode and to test the block-center uniformity proved in Section 4.

For the accepted Ritz vector the reported norm is evaluated directly as
\(\|Uv\|_2\), rather than inferred from \(\sqrt{\lambda}\).  Each row also
archives the relative consistency defect
\[
 \frac{|\,\|Uv\|_2-\sqrt{v^*U^*Uv}\,|}
 {\max\{\|Uv\|_2,\sqrt{v^*U^*Uv}\}},
 \tag{10.2}
\]
which must be finite and whose global maximum must not exceed \(10^{-10}\).
The norm, Ritz residual, adjoint defect, and relative-to-finest audit must all
be finite; the finest-to-itself audit is required to equal zero exactly.
The calculation uses one fixed deterministic starting vector.  Thus a small
actual Ritz residual certifies the returned Krylov-space eigenpair but does
not independently certify that it is the global largest eigenpair of the
finite matrix \(U^*U\).  In particular, a seed orthogonal to the top
eigenspace could converge with zero residual to a lower eigenpair.  The
reported \(\|Uv_{\rm Ritz}\|_2\) is therefore a finite-grid stress diagnostic,
not a certified finite-dimensional operator norm.

The computation is deterministic and archives its command, configuration,
Krylov dimension, actual Ritz residual, environment, progress log, resource
log, raw CSV data, and PDF/SVG/600 dpi PNG figure.  The global numerical QA
gate requires maximum actual Ritz residual at most \(10^{-8}\), in addition
to the stricter per-configuration stopping tolerance (10.1), and the global
Rayleigh-norm consistency gate is \(10^{-10}\).  It is not used
to prove Theorem 3.1, to evaluate
\(C_{K,T}^{\rm per}\), or to establish an infinite-dimensional operator
norm.

---

## 11. Literature boundary

Coble--He supplies the nondegenerate time-dependent shear theorem used only
on the fixed outer margins in Section 7.  Its fixed finite critical-point
count, separation, local Morse shape, and exterior-gradient hypotheses are
not uniform at the shrinking interface (8.1).

Stationary finite-type results explain the \(A_1\) and \(A_2\) benchmark
rates but do not prove a nonautonomous crossing theorem.  Abstract
mixing-to-dissipation results require a Hilbert-scale structure and do not
replace the exact expanding-torus graph argument.  Gluing arguments for a
time-dependent scalar multiple or rigid translation of one fixed spatial
profile do not cover a change in critical-point number.

The all-center compact--escaping proof and exact block tiling are derived in
this report rather than quoted from those sources.  The literature search is
bounded and is not evidence of novelty or priority.

---

## 12. Exact claim boundary and next gate

R0.72X closes the scalar-row outer-time gate in two senses:

1. every physical start time in a fixed compact interval has an exact-family
   semigroup at the uniform collision rate \(\varepsilon_c^{2/5}\);
2. for the periodic representative \(\beta=0\), the fixed heat history
   factors exactly into two fixed-margin \(A_1\) pieces and the exact
   \(A_2\) family, retaining scalar damping, Fourier normalization, endpoint
   norms, and all block constants; Bloch-uniformity is proved separately
   only for the \(A_2\) exact-family semigroup;
3. any orthogonal direct sum of rows sharing the same strong-coupling floor
   inherits the scalar estimate without a row-count loss.

It does not close:

1. a parameter-dependent \(A_1\) black box whose fixed-shape constants stay
   uniform all the way to \(|d|\asymp\varepsilon_c^{-2/5}\);
2. a uniform strict contraction over rows whose effective coupling varies
   with or vanishes at the row index; an exact zero-coupling counterexample
   prevents that statement;
3. the complete linearized shear system and its pressure coupling;
4. nonlinear convolution, vortex stretching, or a three-dimensional
   continuation criterion;
5. global smoothness or finite-time blow-up for general Navier--Stokes data.

The next finite gate is

\[
 \boxed{
 \text{R0.72Y: restore every Fourier row, scalar damping, and coupling
 weight, then test an }\ell^2\text{ direct-sum linearized estimate}.}
 \tag{12.1}
\]

The Clay Millennium problem remains open.

---

## Claim-to-source ledger

| Claim | Source or proof | Exact role | Remaining limitation |
|---|---|---|---|
| Time-dependent nondegenerate shear ED on fixed outer margins | Coble--He, Theorem 1.2 and Appendix A | Gives (7.6)--(7.7) after the exact slow-time rescaling | Shape constants depend on the fixed margin \(\delta\) |
| Stationary finite-type rates retain degeneracy information | Bedrossian--Coti Zelati; Coti Zelati--Gallay | Calibrates the \(A_1\) and finite-type rate hierarchy | Stationary profiles; no collision crossing |
| Abstract mixing-to-enhanced-dissipation transfer | Coti Zelati--Delgadino--Elgindi | Explains why an all-start evolution estimate is the relevant object | Its compact Hilbert-scale assumptions do not prove the present theorem |
| Exact all-center cell theorem and block tiling | Sections 2--5 of this report | Supplies the uniform \(A_2\)-scale semigroup through the collision | Compactness and endpoint traces remain analytic, not finite-certified |

## Primary references used at this gate

1. D. Coble and S. He, *A Note on Enhanced Dissipation and Taylor
   Dispersion of Time-dependent Shear Flows*, arXiv:2309.15738; published in
   *Communications in Mathematical Sciences* **22** (2024), 1663--1691.
2. J. Bedrossian and M. Coti Zelati, *Enhanced Dissipation,
   Hypoellipticity, and Anomalous Small Noise Inviscid Limits in Shear
   Flows*, *Archive for Rational Mechanics and Analysis* **224** (2017),
   1161--1204.
3. M. Coti Zelati and T. Gallay, *Enhanced Dissipation and Taylor
   Dispersion in Higher-dimensional Parallel Shear Flows*, *Journal of the
   London Mathematical Society* **108** (2023), 1358--1392.
4. M. Coti Zelati, M. G. Delgadino, and T. M. Elgindi, *On the Relation
   between Enhanced Dissipation Timescales and Mixing Rates*,
   *Communications on Pure and Applied Mathematics* **73** (2020),
   1205--1244.
