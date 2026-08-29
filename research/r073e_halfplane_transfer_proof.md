# R0.73E proof: fixed-positive-half-plane splitting and logarithmic profile transfer

**Date:** 2026-08-30
**Scope:** the periodic row \(\gamma=1/2\), the exact collision profile, and
the singular limit \(\varepsilon\downarrow0\)
**Evidence class:** exact operator theorem, conditional only on the certified
R0.73C inviscid eigenvalue

## 1. Operators and theorem

Let

\[
 W(d,x)=-\frac12e^{-d}\sin x+\frac14e^{-4d}\sin2x,
 \qquad
 L=-\partial_x^2+\frac14,
 \tag{1.1}
\]

and let \(X=X_{1/4}\) be the physical kinetic vorticity space from R0.73D.
The fast-time inviscid row is

\[
 A(d)=-\frac i2\left(M_{W(d)}+M_{W_{xx}(d)}L^{-1}\right)
 \in\mathcal B(X).
 \tag{1.2}
\]

Under the unitary map

\[
 U=2L^{-1/2}:X\longrightarrow H:=L^2(\mathbb T_{2\pi}),
 \tag{1.3}
\]

the frozen family at \(d=0\) becomes

\[
 B_\varepsilon:=UA(0)U^{-1}-\varepsilon L
 =M+K-\varepsilon L,
 \tag{1.4}
\]

where

\[
 M=-\frac i2M_{W(0)},
 \tag{1.5}
\]

is bounded and skew-adjoint, and

\[
 K=-\frac i2\left(
 L^{-1/2}[M_{W(0)},L^{1/2}]
 +L^{-1/2}M_{W_{xx}(0)}L^{-1/2}
 \right)
 \tag{1.6}
\]

is compact.  The domains are

\[
 D(B_\varepsilon)=H^2_{\rm per}\quad(\varepsilon>0),
 \qquad
 B_0=A_0:=M+K\in\mathcal B(H).
 \tag{1.7}
\]

R0.73C and R0.73D supply an eigenvalue

\[
 \sigma_*\in(0.17035,0.17050)
 \cap\sigma_p(A_0).
 \tag{1.8}
\]

Define

\[
 a:=\max_{z\in\sigma(A_0)}\operatorname{Re}z.
 \tag{1.9}
\]

Then \(a\ge\sigma_*>0.17035\).  The conclusions proved below are:

1. in every fixed positive half-plane whose boundary avoids
   \(\sigma(A_0)\), all viscous spectrum is contained in the continuations
   of the finitely many inviscid clusters, with no extra spectral pollution;
2. the corresponding total Riesz projection and finite spectral block
   converge in operator norm, and the reduced half-plane resolvent is
   uniformly bounded;
3. the complete inviscid top cluster has a viscous continuation with a
   uniform relative exponential dichotomy;
4. the exact heat-profile drift transfers a top viscous eigenmode through
   every fixed logarithmic fast-time interval;
5. for every fixed \(d_*>0\) and \(p>0\),

   \[
    \lim_{|\Lambda|\to\infty}
    \frac{G_{1/2}(\Lambda;d_*)}{|\Lambda|^p}=\infty.
    \tag{1.10}
   \]

The theorem does not identify the top cluster, prove that the certified
\(\sigma_*\) is rightmost, or give a fixed-window exponential lower law.

## 2. Base resolvents on compact subsets

Put

\[
 H_\varepsilon=M-\varepsilon L,
 \qquad
 R_\varepsilon(z)=(z-H_\varepsilon)^{-1}.
 \tag{2.1}
\]

For \(\operatorname{Re}z>0\), the dissipativity argument from R0.73D gives

\[
 \|R_\varepsilon(z)\|
 \le(\operatorname{Re}z)^{-1}
 \qquad(\varepsilon\ge0).
 \tag{2.2}
\]

On every compact set \(\mathcal Z\Subset\{\operatorname{Re}z>0\}\),

\[
 R_\varepsilon(z)\longrightarrow R_0(z)
 \tag{2.3}
\]

strongly and locally uniformly in \(z\), and the same is true for the
adjoints.  Since \(K\) is compact,

\[
 \sup_{z\in\mathcal Z}
 \|(R_\varepsilon(z)-R_0(z))K\|\longrightarrow0,
 \tag{2.4}
\]

and

\[
 \sup_{z\in\mathcal Z}
 \|K(R_\varepsilon(z)-R_0(z))\|\longrightarrow0.
 \tag{2.5}
\]

For the full resolvent

\[
 G_\varepsilon(z)=(z-B_\varepsilon)^{-1},
 \tag{2.6}
\]

the Fredholm factorization is

\[
 z-B_\varepsilon
 =(z-H_\varepsilon)F_\varepsilon(z),
 \qquad
 F_\varepsilon(z)=I-R_\varepsilon(z)K.
 \tag{2.7}
\]

Thus \(F_\varepsilon\to F_0\) in operator norm on compact subsets of the
right half-plane.  On any compact subset of
\(\rho(A_0)\cap\{\operatorname{Re}z>0\}\), the inverses
\(F_\varepsilon(z)^{-1}\) and the full resolvents are uniformly bounded.

## 3. Uniform high-frequency resolvents

The preceding compact-set argument must not be applied directly to an
unbounded half-plane.  Let \(z=x+i\tau\), \(x>0\).  Since \(L\) is positive
self-adjoint,

\[
 \|(z+\varepsilon L)^{-1}\|
 =\sup_{n\in\mathbb Z}
 \frac1{|x+\varepsilon(n^2+1/4)+i\tau|}
 \le\frac1{|\tau|}.
 \tag{3.1}
\]

The factorization

\[
 z-H_\varepsilon
 =(z+\varepsilon L)
 \bigl[I-(z+\varepsilon L)^{-1}M\bigr]
 \tag{3.2}
\]

therefore gives

\[
 \|R_\varepsilon(z)\|
 \le\frac1{|\tau|-\|M\|}
 \qquad(|\tau|>\|M\|),
 \tag{3.3}
\]

uniformly in \(\varepsilon\ge0\).  If

\[
 |\tau|>\|M\|+2\|K\|,
 \tag{3.4}
\]

then \(\|R_\varepsilon(z)K\|<1/2\), so (2.7) gives

\[
 \|G_\varepsilon(z)\|
 \le\frac2{|\tau|-\|M\|}.
 \tag{3.5}
\]

There is also a uniform high-real-part bound.  From (2.2),

\[
 \|R_\varepsilon(z)K\|
 \le\frac{\|K\|}{\operatorname{Re}z}.
 \tag{3.6}
\]

Hence \(G_\varepsilon(z)\) exists and is uniformly bounded whenever
\(\operatorname{Re}z>2\|K\|\).  Equations (3.5)--(3.6) leave only a fixed
compact rectangle to be controlled by Section 2.

## 4. Fixed-positive-half-plane no-pollution theorem

Fix \(b>0\) such that

\[
 \sigma(A_0)\cap\{\operatorname{Re}z=b\}=\varnothing.
 \tag{4.1}
\]

Because \(K\) is compact and \(\sigma(M)\subset i\mathbb R\),

\[
 \Sigma_b:=\sigma(A_0)\cap\{\operatorname{Re}z>b\}
 \tag{4.2}
\]

is a finite set of isolated eigenvalues of finite algebraic multiplicity.
Indeed, the boundary line is disjoint from the compact inviscid spectrum,
so the two have positive separation in every bounded rectangle.  Analytic
Fredholm theory allows accumulation away from the essential spectrum only
at that essential spectrum, which lies on the imaginary axis.  Hence no
infinite sequence of inviscid eigenvalues can remain in the fixed half-plane
\(\operatorname{Re}z>b\).  Choose pairwise disjoint closed disks
\(D_1,\ldots,D_J\) whose interiors
contain exactly these spectral points, whose boundaries
\(\Gamma_j=\partial D_j\) lie in \(\{\operatorname{Re}z>b\}\), and whose
closures are contained in the right half-plane.

The compact-Fredholm argument on each \(\Gamma_j\) shows that, for all
sufficiently small \(\varepsilon>0\),

\[
 \Gamma_j\subset\rho(B_\varepsilon)
 \tag{4.3}
\]

with a common contour-resolvent bound.  Set

\[
 \Pi_{\varepsilon,b}
 =\frac1{2\pi i}\sum_{j=1}^J
 \int_{\Gamma_j}G_\varepsilon(z)\,dz,
 \qquad
 Q_{\varepsilon,b}=I-\Pi_{\varepsilon,b}.
 \tag{4.4}
\]

As in R0.73D,

\[
 G_\varepsilon-R_\varepsilon
 =G_\varepsilon K R_\varepsilon.
 \tag{4.5}
\]

For completeness, on every fixed contour
\(G_\varepsilon K=F_\varepsilon^{-1}R_\varepsilon K\) converges in
operator norm and has compact limit.  Therefore

\[
 G_\varepsilon K R_\varepsilon-G_0KR_0
 =(G_\varepsilon K-G_0K)R_\varepsilon
  +G_0K(R_\varepsilon-R_0)\longrightarrow0
 \tag{4.5a}
\]

in operator norm: the first term uses the uniform base-resolvent bound, and
the second uses adjoint-strong resolvent convergence against the compact
operator \(G_0K\).  The convergence is uniform on the finitely many
contours.  The base resolvent is analytic inside each disk, so

\[
 \int_{\Gamma_j}R_\varepsilon(z)\,dz=0.
 \tag{4.6}
\]

Consequently

\[
 \|\Pi_{\varepsilon,b}-\Pi_{0,b}\|\longrightarrow0.
 \tag{4.7}
\]

The ranks and total algebraic multiplicities inside every disk are
preserved.

To exclude all other viscous spectrum in the half-plane, choose the
high-frequency and high-real-part cutoffs from Section 3.  In the remaining
compact rectangle, remove the interiors of the disks \(D_j\).  The result is
a compact subset of \(\rho(A_0)\), so Section 2 gives a uniform full
resolvent there.  Therefore

\[
 \sigma(B_\varepsilon)\cap\{\operatorname{Re}z\ge b\}
 \subset\bigcup_{j=1}^J\operatorname{int}D_j.
 \tag{4.8}
\]

This is no-pollution only in the fixed half-plane.  Its constants need not
remain bounded as \(b\downarrow0\).

## 5. Uniform reduced resolvent and spectral-block convergence

Outside the disks, Sections 2--4 already give

\[
 \sup_{0<\varepsilon<\varepsilon_b}
 \sup_{\substack{\operatorname{Re}z\ge b\\
 z\notin\cup_jD_j}}
 \|G_\varepsilon(z)\|<\infty.
 \tag{5.1}
\]

Because \(\Pi_{\varepsilon,b}\) is a spectral projection, the Riesz
decomposition satisfies

\[
 H=\Pi_{\varepsilon,b}H\oplus Q_{\varepsilon,b}H,
 \qquad
 Q_{\varepsilon,b}D(B_\varepsilon)\subset D(B_\varepsilon),
 \qquad
 B_\varepsilon Q_{\varepsilon,b}
 =Q_{\varepsilon,b}B_\varepsilon
 \quad\text{on }D(B_\varepsilon).
 \tag{5.2a}
\]

Let \(C_{\varepsilon,b}\) be the part of \(B_\varepsilon\) in
\(Q_{\varepsilon,b}H\), and define the extended reduced resolvent

\[
 \widehat G_{\varepsilon,b}(z)
 =(z-C_{\varepsilon,b})^{-1}Q_{\varepsilon,b}.
 \tag{5.2b}
\]

It agrees with \(G_\varepsilon(z)Q_{\varepsilon,b}\) wherever the full
resolvent exists and is analytic through every eigenvalue assigned to the
finite Riesz block.  On the disk boundaries it is uniformly bounded by
(5.1), (4.7), and the resulting uniform projection bound.  The
Banach-valued maximum principle, applied after pairing against unit vectors,
gives

\[
 \boxed{
 \sup_{0<\varepsilon<\varepsilon_b}
 \sup_{\operatorname{Re}z\ge b}
 \|\widehat G_{\varepsilon,b}(z)\|<\infty.}
 \tag{5.2}
\]

At points where the full resolvent exists, (5.2) is equivalently the stated
bound for \(G_\varepsilon(z)Q_{\varepsilon,b}\).

The finite spectral block is also norm-convergent.  Functional calculus
gives

\[
 B_\varepsilon\Pi_{\varepsilon,b}
 =\frac1{2\pi i}\sum_j
 \int_{\Gamma_j}zG_\varepsilon(z)\,dz.
 \tag{5.3}
\]

The base spectrum lies in the closed left half-plane, whereas every disk is
in the open right half-plane.  Thus

\[
 \int_{\Gamma_j}zR_\varepsilon(z)\,dz=0.
 \tag{5.4}
\]

Subtracting the analytic base term and using the same compact-sandwich norm
convergence as in (4.5) yields

\[
 \boxed{
 \|B_\varepsilon\Pi_{\varepsilon,b}
   -A_0\Pi_{0,b}\|\longrightarrow0.}
 \tag{5.5}
\]

Equations (4.7), (4.8), (5.2), and (5.5) prove the fixed-positive-half-plane
theorem.

## 6. The inviscid top cluster

The spectrum of the bounded operator \(A_0\) is compact.  Equation (1.8)
shows that its spectral abscissa \(a\) is positive.  Every spectral point in
the open right half-plane is discrete, so

\[
 \Sigma_{\rm top}
 =\{z\in\sigma(A_0):\operatorname{Re}z=a\}
 \tag{6.1}
\]

is nonempty and finite.  Let \(\Pi_0^{\rm top}\) be its total Riesz
projection and \(Q_0^{\rm top}=I-\Pi_0^{\rm top}\).  The complementary
spectral bound

\[
 \beta:=\max\{\operatorname{Re}z:
 z\in\sigma(A_0|_{Q_0^{\rm top}H})\}
 \tag{6.2}
\]

is attained and satisfies \(\beta<a\).  Indeed, the complementary spectrum
is compact, while every top point is isolated and has been removed with its
entire Riesz block; the complement therefore cannot approach the finite top
set.  Choose

\[
 \max\{\beta,0\}<b<c<a.
 \tag{6.3}
\]

The half-plane theorem with boundary \(b\) has
\(\Pi_{\varepsilon,b}=\Pi_\varepsilon^{\rm top}\) for all sufficiently
small \(\varepsilon\).  In particular,

\[
 \|\Pi_\varepsilon^{\rm top}-\Pi_0^{\rm top}\|\longrightarrow0,
 \qquad
 \sup_\varepsilon\|Q_\varepsilon^{\rm top}\|<\infty.
 \tag{6.4}
\]

All viscous top-cluster eigenvalues converge to \(\Sigma_{\rm top}\).
Hence one may choose

\[
 \lambda_\varepsilon\in\sigma_p(B_\varepsilon),
 \qquad
 B_\varepsilon v_\varepsilon
 =\lambda_\varepsilon v_\varepsilon,
 \qquad
 \|v_\varepsilon\|=1,
 \tag{6.5}
\]

such that

\[
 \operatorname{Re}\lambda_\varepsilon\longrightarrow a.
 \tag{6.6}
\]

No simplicity or common eigenvector is asserted.

## 7. Uniform complementary semigroup bound

Let \(C_\varepsilon\) be the part of \(B_\varepsilon\) in
\(Q_\varepsilon^{\rm top}H\).  Riesz invariance gives

\[
 D(C_\varepsilon)
 =D(B_\varepsilon)\cap Q_\varepsilon^{\rm top}H.
 \tag{7.1}
\]

The operator \(H_\varepsilon=M-\varepsilon L\) is maximally dissipative, so
its semigroup is contractive.  Since \(K\) is bounded,

\[
 \|e^{tB_\varepsilon}\|
 \le e^{\|K\|t}.
 \tag{7.2}
\]

Together with (6.4), this supplies a common crude short-time bound for
\(e^{tC_\varepsilon}\).

By (5.2), the reduced resolvents are uniformly bounded on the line
\(b+i\mathbb R\).  Equation (3.5) strengthens this to

\[
 \|(b+i\tau-C_\varepsilon)^{-1}\|
 \le\frac{C}{1+|\tau|}.
 \tag{7.3}
\]

For every \(\varepsilon>0\), the operator \(-\varepsilon L\) generates an
analytic semigroup and \(M+K\) is bounded.  Hence \(B_\varepsilon\), and its
invariant part \(C_\varepsilon\), generate analytic semigroups.  Start the
inverse Laplace formula for \(t>0\) on a common vertical line
\(\operatorname{Re}z=\omega>\|K\|\), to the right of the growth bound in
(7.2), and move it to \(b+i\mathbb R\).  The horizontal sides of the
truncating rectangles vanish because the Section 3 high-frequency estimate
holds uniformly throughout the strip
\(b\le\operatorname{Re}z\le\omega\), together with the uniform projection
bound in (6.4).  On the new line, integrate once by parts.  Since

\[
 \frac d{d\tau}(b+i\tau-C_\varepsilon)^{-1}
 =-i(b+i\tau-C_\varepsilon)^{-2},
 \tag{7.4}
\]

one obtains, for \(t>0\),

\[
 e^{tC_\varepsilon}
 =\frac{e^{bt}}{2\pi t}
 \int_{\mathbb R}e^{i\tau t}
 (b+i\tau-C_\varepsilon)^{-2}\,d\tau,
 \tag{7.5}
\]

The boundary term vanishes by the \(O(|\tau|^{-1})\) resolvent estimate.
The integral is absolutely and uniformly convergent because the square
resolvent is bounded on compact \(\tau\)-intervals and is
\(O(|\tau|^{-2})\) at infinity.  Thus for
\(t\ge1\),

\[
 \|e^{tB_\varepsilon}Q_\varepsilon^{\rm top}\|
 \le C_b e^{bt}.
 \tag{7.6}
\]

For \(0\le t\le1\), combine (7.2) and (6.4).  Since \(b>0\), enlarging
\(C_b\) gives (7.6) for every \(t\ge0\).

Choose fixed top-cluster contours whose closures lie in
\(\{\operatorname{Re}z>c\}\).  Functional calculus on the finite spectral
block gives

\[
 e^{-tB_\varepsilon}\Pi_\varepsilon^{\rm top}
 =\frac1{2\pi i}\sum_j
 \int_{\Gamma_j}e^{-tz}G_\varepsilon(z)\,dz.
 \tag{7.7}
\]

The uniform contour-resolvent bound yields

\[
 \|e^{-tB_\varepsilon}\Pi_\varepsilon^{\rm top}\|
 \le C_c e^{-ct},
 \qquad t\ge0.
 \tag{7.8}
\]

For any \(b<\alpha<c\), the shifted generator
\(B_\varepsilon-\alpha I\) therefore has a uniform exponential dichotomy,
with forward stable rate \(\alpha-b\) on the complement and backward stable
rate \(c-\alpha\) on the finite top block.  The unshifted complement is not
claimed to decay at a fixed negative rate.

## 8. Frozen full-semigroup bound at the spectral abscissa

For every fixed \(\delta>0\), choose the top-cluster contours to lie in

\[
 \{z:\operatorname{Re}z<a+\delta\}.
 \tag{8.1}
\]

Forward functional calculus on the top block gives

\[
 \|e^{tB_\varepsilon}\Pi_\varepsilon^{\rm top}\|
 \le C_\delta e^{(a+\delta)t}.
 \tag{8.2}
\]

The complement estimate (7.6), with \(b<a\), is smaller after enlarging the
constant.  Hence

\[
 \boxed{
 \|e^{tB_\varepsilon}\|
 \le C_\delta e^{(a+\delta)t},
 \qquad t\ge0,}
 \tag{8.3}
\]

uniformly for all sufficiently small \(\varepsilon\).  The constant may
depend on \(\delta\); no estimate is asserted at \(\delta=0\).

## 9. Explicit bounded heat-profile drift

Define the bounded operator on \(H\)

\[
 \widetilde A(d):=UA(d)U^{-1}.
 \tag{9.0}
\]

The unitary formula used in R0.73D gives, for
\(\Delta W=W(d)-W(0)\),

\[
 \begin{aligned}
 \|\widetilde A(d)-\widetilde A(0)\|
 \le\frac12\bigl(&\|\Delta W\|_\infty
 +2\sum_k|k|\,|\widehat{\Delta W}(k)|\\
 &+4\|\Delta W_{xx}\|_\infty\bigr).
 \end{aligned}
 \tag{9.1}
\]

The elementary inequalities \(1-e^{-d}\le d\) and
\(1-e^{-4d}\le4d\) give

\[
 \|\Delta W\|_\infty\le\frac32d,
 \qquad
 \sum_k|k|\,|\widehat{\Delta W}(k)|\le\frac52d,
 \qquad
 \|\Delta W_{xx}\|_\infty\le\frac92d.
 \tag{9.2}
\]

Consequently

\[
 \boxed{
 \|\widetilde A(d)-\widetilde A(0)\|
 \le\frac{49}{4}d.}
 \tag{9.3}
\]

In fast time, \(d=\varepsilon\theta\), so the exact moving generator is

\[
 B_\varepsilon+E_\varepsilon(\theta),
 \qquad
 E_\varepsilon(\theta)
 =\widetilde A(\varepsilon\theta)-\widetilde A(0),
 \qquad
 \|E_\varepsilon(\theta)\|
 \le C_A\varepsilon\theta,
 \qquad C_A=\frac{49}{4}.
 \tag{9.4}
\]

The entire unbounded term \(-\varepsilon L\) remains inside
\(B_\varepsilon\).  Only the profile drift is treated as bounded forcing.

## 10. Logarithmic fast-time Volterra transfer

Fix \(M>0\) and set

\[
 T_\varepsilon=M\log(1/\varepsilon).
 \tag{10.1}
\]

Let \(v_\varepsilon\) and \(\lambda_\varepsilon\) be chosen as in (6.5).
The common-domain bounded-perturbation theorem gives a unique evolution
family for

\[
 q'(t)=[B_\varepsilon+E_\varepsilon(t)]q(t),
 \qquad q(0)=v_\varepsilon.
 \tag{10.2}
\]

Take

\[
 \delta=\frac1{4M}.
 \tag{10.3}
\]

Write \(S_\varepsilon(t)=e^{tB_\varepsilon}\).  From (8.3), Duhamel's
formula and weighted Gronwall,

\[
 \|q(t)\|
 \le C_\delta e^{(a+\delta)t}
 \exp\left(\frac12C_\delta C_A\varepsilon t^2\right).
 \tag{10.4}
\]

Since

\[
 S_\varepsilon(t)v_\varepsilon
 =e^{\lambda_\varepsilon t}v_\varepsilon,
 \tag{10.5}
\]

the difference

\[
 r(t):=q(t)-e^{\lambda_\varepsilon t}v_\varepsilon
 \tag{10.6}
\]

satisfies

\[
 \|r(t)\|
 \le\frac12C_\delta^2C_A\varepsilon t^2
 \exp\left[
  (a+\delta)t+\frac12C_\delta C_A\varepsilon t^2
 \right].
 \tag{10.7}
\]

Let

\[
 \eta_\varepsilon
 =|\operatorname{Re}\lambda_\varepsilon-a|\longrightarrow0.
 \tag{10.8}
\]

At \(t=T_\varepsilon\), the error relative to the frozen eigenmode is at
most

\[
 C\varepsilon T_\varepsilon^2
 \exp\left[
  (\delta+\eta_\varepsilon)T_\varepsilon
  +C\varepsilon T_\varepsilon^2
 \right].
 \tag{10.9}
\]

For sufficiently small \(\varepsilon\),
\(M\eta_\varepsilon<1/4\).  Since \(M\delta=1/4\), (10.9) is bounded by a
constant times

\[
 \varepsilon^{1/2}
 \log^2(1/\varepsilon)
 \exp\bigl(C\varepsilon\log^2(1/\varepsilon)\bigr),
 \tag{10.10}
\]

which tends to zero.  Therefore

\[
 \boxed{
 \|q(T_\varepsilon)\|
 \ge\frac12
 e^{\operatorname{Re}\lambda_\varepsilon T_\varepsilon}}
 \tag{10.11}
\]

for every sufficiently small \(\varepsilon\).  Equivalently, the
logarithmic growth rate satisfies the unambiguous bound

\[
 \liminf_{\varepsilon\downarrow0}
 \frac{\log\|U_\varepsilon(T_\varepsilon,0)\|}
      {\log(1/\varepsilon)}
 \ge Ma\ge M\sigma_*>0.17035M.
 \tag{10.12}
\]

This proof does not introduce a moving spectral projection and does not
commute an inviscid projection through \(L\).

## 11. Physical-time consequence and both signs

Return to \(\varepsilon=|\Lambda|^{-1}\) and physical time

\[
 d_\Lambda
 =\varepsilon T_\varepsilon
 =M\frac{\log|\Lambda|}{|\Lambda|}.
 \tag{11.1}
\]

For every fixed \(d_*>0\), eventually \(d_\Lambda<d_*\).  The sign
\(s=-1\) is obtained by complex conjugating the top eigenvalue and
eigenvector because the profile and \(L\) are real.  The initial vector may
depend on \(|\Lambda|\) and on its sign, which is permitted in the operator
norm.

Recall that the exact row gain is the observation-window supremum

\[
 G_{1/2}(\Lambda;d_*)
 =\sup_{0\le d\le d_*}
 \|U_{1/2,\Lambda}(d,0)\|_{\mathcal K_{1/4}\to\mathcal K_{1/4}}.
 \tag{11.1a}
\]

Thus the lower bound at the earlier time \(d_\Lambda<d_*\) is a lower bound
for \(G_{1/2}(\Lambda;d_*)\).

Fix \(p>0\) and choose \(M>p/0.17035\).  By the spectral-abscissa lower
bound \(a\ge\sigma_*>0.17035\), (6.6), and (10.11),

\[
 \frac{G_{1/2}(\Lambda;d_*)}{|\Lambda|^p}
 \longrightarrow\infty
 \qquad(|\Lambda|\to\infty).
 \tag{11.2}
\]

For the selected complete Fourier row,

\[
 \beta=\xi=0,
 \qquad \gamma=\frac12,
 \qquad \mu=\gamma^2=\frac14.
 \tag{11.3}
\]

The exact Orr--Sommerfeld--Squire system is triangular, and its Squire
forcing coefficient \(i\xi\Lambda\) vanishes.  Therefore initial Squire
vorticity \(\eta(0)=0\) remains zero.  The physical kinetic identity is

\[
 \|u\|_2^2
 =\mu^{-1}\bigl(\|L^{-1/2}q\|_2^2+\|\eta\|_2^2\bigr).
 \tag{11.4}
\]

The map \(U=2L^{-1/2}\) is unitary from the OS kinetic space at
\(\mu=1/4\) to \(H\).  The OS lower bound therefore embeds isometrically in
this complete row.  Every complete-row polynomial upper bound required to
cover all rows must dominate it and is excluded.  This does not prove the
still-open complete OS--Squire \(A_2\) direct-sum estimate.

## 12. Why the R0.73D local data alone are insufficient

For \(N\ge1\), let

\[
 D_N=
 \begin{pmatrix}
 a&0&0\\
 0&-N&N^2\\
 0&0&-N
 \end{pmatrix},
 \qquad a>0.
 \tag{12.1}
\]

The Riesz projection around \(a\) is constant, its local contour resolvent
is uniformly bounded, and the complementary spectrum equals \(\{-N\}\).
Nevertheless,

\[
 e^{tD_N}|_{\rm complement}
 =e^{-Nt}
 \begin{pmatrix}1&N^2t\\0&1\end{pmatrix},
 \tag{12.2}
\]

whose norm is at least \(N/e\) at \(t=N^{-1}\).  Thus a local Riesz theorem,
a spectral gap, and memberwise analyticity do not imply a family-uniform
complementary semigroup bound.  Sections 3--7 use additional structure
specific to \(M+K-\varepsilon L\).

## 13. Exact boundary

The proved statements are:

```text
fixedPositiveHalfPlaneNoPollution=CLOSED
allModesRightOfBProjectionNormPersistence=CLOSED
topInviscidClusterExists=CLOSED
topViscousClusterPersistence=CLOSED
topReducedHalfPlaneResolventUniform=CLOSED
frozenTopClusterRelativeDichotomy=CLOSED
fixedFrozenGeneratorVolterraTransfer=CLOSED
logFastTimeTransfer=CLOSED
superPolynomialCompleteRowNoGo=CLOSED
```

The following remain open:

```text
certifiedSigmaStarIsRightmost=OPEN
selectedSigmaStarComplementDichotomy=OPEN
uniformHalfPlaneBoundAtBEqualsZero=OPEN
globalRightHalfPlaneNoPollution=OPEN
absoluteUniformComplementDecay=OPEN
explicitHalfPlaneGap=OPEN
explicitViscosityThreshold=OPEN
quantitativeEigenvalueRate=OPEN
movingProfileUniformContour=OPEN
graphDomainKatoTransport=OPEN
movingProfileEvolutionDichotomy=OPEN
inviscidRootUnique=OPEN
inviscidEigenvalueSimple=OPEN
completeOSSquireA2DirectSum=OPEN
fixedWindowExponentialLowerLaw=OPEN
nonlinearNavierStokes=OPEN
Clay=OPEN
```

The new route makes moving-profile Riesz continuation and graph-domain Kato
transport unnecessary for the logarithmic norm lower bound.  It does not
prove those separate operator statements.  It also does not turn a linear
large-coupling result into a nonlinear Navier--Stokes or Clay conclusion.
