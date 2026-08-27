# R0.72K -- directional zero sampling and the complete complex-target ledger

**Date:** 2026-08-27

**Status:** a sharp zero-count-independent sampling lemma for real or complex
Banach-valued curves, and a complete complex-target root theorem for the
finite triangular 2.5D Navier--Stokes class.  In the perturbative common-band
regime of R0.72J, the complete raw root mass has order \(a^2N^2\), while its
full physical critical-log normalization tends to zero.  This is not a
theorem for general three-dimensional Navier--Stokes solutions.

**Keywords:** Navier--Stokes regularity, complex temporal zeros, Banach-valued
curve, directional projection, Rolle theorem, complete root ledger,
critical-log action, triangular 2.5D flow

---

## 0. Direct decision

R0.72J left one logical gap in the common-band mixed-parity analysis.  It
constructed an exact complex target root and bounded both continuous row
integrals

\[
 \mathcal E_Q(I)=\int_I|hQF|\,dx,
 \qquad
 \mathcal C_\times(I)
 =|\delta|\int_I|hP_0V^2F|\,dx,
 \tag{0.1}
\]

but did not pack all roots because the target coordinate was not confined to
one real line.

The missing step does not require a complex Rolle theorem.  Let \(B\) be a
real or complex Banach space, let \(X\in W^{2,1}(I;B)\), and let

\[
 t_1<\cdots<t_m,
 \qquad X(t_j)=0.
 \tag{0.2}
\]

Then

\[
 \boxed{
 \sum_{j=2}^m\|X'(t_j)\|_B^2
 \le2\int_I\|X'(t)\|_B\,\|X''(t)\|_B\,dt.}
 \tag{0.3}
\]

The proof chooses, on each gap, a norming functional for the derivative at
the right endpoint.  The real part of that functional applied to \(X'\) has
zero average and therefore has a zero.  The complex or vector derivative
itself need not vanish.

The first selected root must be paid separately.  The factor \(2\) in (0.3)
is optimal in the stated regularity class.

For the exact triangular target equations

\[
 F_0'+\lambda_0F_0=\delta h,
 \qquad
 h'+\lambda_0h=QF+\delta b,
 \qquad b=P_0V^2F,
 \tag{0.4}
\]

the integrating factor and (0.3) give, for every finite root subset and hence
for the complete extended root mass,

\[
 \boxed{
 G_{\rm all}^{\rm ex}(I)
 \le E_A\rho_A^2+2\mathcal E_Q(I)+2\mathcal C_\times(I).}
 \tag{0.5}
\]

Here \(I=[A,A+X]\), \(E_A=\|F(A)\|_2^2\), and
\(\rho_A=\|P_0V(A)\|\).  Formula (0.5) requires \(\delta\ne0\), but it
requires no real gauge, root count, root separation, holomorphic extension,
or lower analytic anchor.

Combining (0.5) with R0.72H and R0.72J gives the finite-carrier theorem

\[
\boxed{
\begin{aligned}
G_{\rm all}^{\rm ex}(I)
\le{}&E_A\rho_A^2
+12\sqrt\nu\,d|K_z|
[\lambda_0E_A m_*(A,X)Q_*^I]^{1/2}\\
&+2\min\left\{
|\delta|\sqrt{\lambda_0}B_AQ_*^I,
|\delta|E_A\int_I\rho(x)^2\|V(x)\|\,dx
\right\}.
\end{aligned}}
\tag{0.6}
\]

In the common frequency band of R0.72J,

\[
 R\le|r_l|\le C_0R,
 \qquad |w_l|\asymp a,
 \qquad \|V(x)\|\le CaB e^{-cR^2x},
 \tag{0.7}
\]

\[
 g=|\delta|a,
 \qquad
 \varepsilon=\frac{gB}{R^2}\le\gamma_0,
 \qquad
 \|F(0)\|_2^2=N,
 \tag{0.8}
\]

equation (0.6) and the exact root constructed in R0.72J yield

\[
 \boxed{G_{\rm all}^{\rm ex}\asymp a^2N^2.}
 \tag{0.9}
\]

After the exact physical amplitude balance,

\[
 \boxed{
 \mathcal J_{\rm all}\asymp\frac{g^2N}{R^2},
 \qquad
 \frac{\mathcal J_{\rm all}}
 {D^{1/3}\Lambda_{1,*}}
 \le
 CR^{-4/9}(1+\log R)^{-2/3}\longrightarrow0.}
 \tag{0.10}
\]

Thus the common-band no-go now covers the complete complex root ledger, not
only the cubic row.  The multiscale and strong-coupling regimes remain open.

---

## 1. Directional zero sampling in a Banach space

I use the canonical absolutely continuous representative of \(X'\) when
\(X\in W^{2,1}(I;B)\).  All endpoint derivatives below refer to this
representative.

### Theorem 1.1 -- complete directional root-slope packing

Let \(B\) be a real or complex Banach space and \(I=[a,b]\).  Suppose
\(X\in W^{2,1}(I;B)\).  For every finite ordered set

\[
 a\le t_1<\cdots<t_m\le b,
 \qquad X(t_j)=0,
 \tag{1.1}
\]

one has

\[
 \boxed{
 \sum_{j=1}^m\|X'(t_j)\|_B^2
 \le \|X'(t_1)\|_B^2
 +2\int_a^b\|X'(t)\|_B\,\|X''(t)\|_B\,dt.}
 \tag{1.2}
\]

If \(Z=\{t\in I:X(t)=0\}\), its extended nonnegative derivative mass,
defined as the supremum over all finite subsets, satisfies

\[
 \sum_{t\in Z}^{\rm ex}\|X'(t)\|_B^2
 \le \sup_{t\in Z}\|X'(t)\|_B^2
 +2\int_a^b\|X'(t)\|_B\,\|X''(t)\|_B\,dt.
 \tag{1.2a}
\]

The supremum is finite because the canonical representative of \(X'\) is
continuous on the compact interval.  If \(Z\) has a least element \(t_*\),
the supremum term in (1.2a) may instead be replaced by
\(\|X'(t_*)\|_B^2\).

#### Proof

Fix \(j\ge2\), put \(\alpha=t_{j-1}\), \(\beta=t_j\), and set

\[
 v=X'(\beta).
 \tag{1.3}
\]

If \(v=0\), the desired estimate on this gap is trivial.  Otherwise the real
or complex Hahn--Banach theorem gives a functional

\[
 \ell_j\in B^*,
 \qquad \|\ell_j\|=1,
 \qquad \ell_j(v)=\|v\|_B>0.
 \tag{1.4}
\]

In the complex case, multiply a norming functional by a unit phase so that
the last value is positive real.  Define the real absolutely continuous
function

\[
 \phi_j(t)=\operatorname{Re}\ell_j(X'(t)).
 \tag{1.5}
\]

Because both endpoints are roots,

\[
 \int_\alpha^\beta\phi_j(t)\,dt
 =\operatorname{Re}\ell_j(X(\beta)-X(\alpha))=0.
 \tag{1.6}
\]

Continuity therefore supplies \(c_j\in[\alpha,\beta]\) with
\(\phi_j(c_j)=0\).  At the right endpoint,

\[
 \phi_j(\beta)=\|X'(\beta)\|_B.
 \tag{1.7}
\]

The one-dimensional chain rule gives

\[
\begin{aligned}
 \|X'(\beta)\|_B^2
 &=\phi_j(\beta)^2-\phi_j(c_j)^2\\
 &=2\int_{c_j}^{\beta}\phi_j(t)\phi_j'(t)\,dt\\
 &\le2\int_\alpha^\beta
 \|X'(t)\|_B\,\|X''(t)\|_B\,dt.
\end{aligned}
\tag{1.8}
\]

The root gaps are disjoint.  Summing (1.8) for \(j=2,\ldots,m\) and
adding the first root proves (1.2).  The inequality applies to every finite
root subset, even if other roots are skipped.  Its first-root term is bounded
uniformly by the supremum in (1.2a), so taking the supremum proves that
statement.  If \(Z\) has a least root, adjoining it to each finite subset
before applying (1.2) gives the sharper fixed-first-root version. \(\square\)

### 1.1 What vanishes and what does not

For

\[
 X(t)=e^{2\pi it}-1,
 \qquad0\le t\le1,
 \tag{1.9}
\]

the endpoint values agree, but \(X'(t)\ne0\) for every \(t\).  Literal
complex Rolle is false.  In Theorem 1.1, the scalar projection

\[
 \operatorname{Re}\ell(X'(t))
 \tag{1.10}
\]

does vanish.  The functional may change from one root gap to the next.  No
global phase or common real line is asserted.

### 1.2 The first-root term is necessary

Take \(B=\mathbb R\) and \(X(t)=t\) on \([0,1]\).  The only root is at zero,

\[
 |X'(0)|^2=1,
 \qquad
 \int_0^1|X'||X''|\,dt=0.
 \tag{1.11}
\]

Thus no theorem of the form (1.2) can remove the first-root payment without
additional boundary information.

### 1.3 Sharpness of the factor two

Let \(0<\epsilon<1/3\) and put

\[
 L_\epsilon=\frac{2\epsilon}{1+\epsilon}.
 \tag{1.12}
\]

Define a continuous piecewise-linear derivative \(v_\epsilon\) on
\([0,1]\) by

\[
 v_\epsilon(t)=
 \begin{cases}
 -\epsilon,&0\le t\le1-L_\epsilon,\\
 -\epsilon+\dfrac{1+\epsilon}{L_\epsilon}
 (t-1+L_\epsilon),&1-L_\epsilon<t\le1.
 \end{cases}
 \tag{1.13}
\]

The plateau and ramp areas cancel exactly:

\[
 \int_0^1v_\epsilon(t)\,dt=0.
 \tag{1.14}
\]

With

\[
 X_\epsilon(t)=\int_0^tv_\epsilon(s)\,ds,
 \tag{1.15}
\]

both endpoints are roots, \(X_\epsilon'(1)=1\), and direct calculation gives

\[
 \int_0^1|X_\epsilon'||X_\epsilon''|\,dt
 =\frac{1+\epsilon^2}{2}
 \longrightarrow\frac12
 \qquad(\epsilon\downarrow0).
 \tag{1.16}
\]

Therefore the coefficient in front of the integral in (1.2) cannot be
smaller than two in the full \(W^{2,1}\) class.

### 1.4 The theorem controls mass, not root count

Let

\[
 f_N(t)=N^{-3}(e^{2\pi iNt}-1),
 \qquad0\le t\le1.
 \tag{1.17}
\]

It has \(N+1\) roots, while

\[
 \sum_{f_N(t)=0}|f_N'(t)|^2
 \asymp N^{-3}\longrightarrow0.
 \tag{1.18}
\]

Thus no positive-homogeneous slope action should be expected to bound the
raw number of roots.  The derivative-mass ledger is stable precisely because
many small-slope roots are inexpensive.  This scalar family is an abstract
method check, not a triangular Navier--Stokes trajectory.

---

## 2. Exact triangular target equations

I retain the finite-carrier triangular class of R0.72H--J.  The active
Fourier lattice satisfies

\[
 \partial_xF=D_qF+\delta V_w(x)F,
 \qquad
 (D_qF)_r=-\lambda_{q,r}F_r,
 \tag{2.1}
\]

where

\[
 \lambda_{q,r}
 =\nu\left[\left(dr+\frac{K_y}{q}\right)^2
 +\frac{K_z^2}{q^2}\right],
 \qquad \lambda_0=\lambda_{q,0}>0,
 \tag{2.2}
\]

and

\[
 (V_w(x)F)_r=-iK_z\sum_{l=1}^N e^{-\kappa r_l^2x}
 \left(w_lF_{r-r_l}+\overline{w_l}F_{r+r_l}\right),
 \qquad \kappa=\nu d^2.
 \tag{2.3}
\]

The conjugate pairing makes \(V_w(x)\) skew-adjoint.  Hence

\[
 \frac12\frac d{dx}\|F(x)\|_2^2
 =-\sum_r\lambda_{q,r}|F_r(x)|^2,
 \qquad
 \|F(x)\|_2^2\le E_A:=\|F(A)\|_2^2
 \tag{2.4}
\]

for \(x\ge A\).

Set

\[
 z=V_wF,
 \qquad h=P_0z,
 \qquad b=P_0V_wz=P_0V_w^2F,
 \tag{2.5}
\]

\[
 \mathfrak q=\langle A_q^{-1}z,z\rangle,
 \qquad A_q=-D_q,
 \qquad \rho(x)=\|P_0V_w(x)\|.
 \tag{2.6}
\]

Then

\[
 |h|^2\le\lambda_0\mathfrak q,
 \qquad
 |h(x)|^2\le\rho(x)^2E_A.
 \tag{2.7}
\]

The target coordinate and its differentiated row are exactly

\[
 F_0'+\lambda_0F_0=\delta h,
 \tag{2.8}
\]

\[
 h'+\lambda_0h=QF+\delta b,
 \qquad
 Q=P_0[V_w'+V_w(D_q+\lambda_0)].
 \tag{2.9}
\]

No phase or real-gauge assumption appears in these identities.

---

## 3. Complete complex-target root theorem

Let \(I=[A,A+X]\).  For \(\delta\ne0\), define the complete extended raw
root mass by

\[
 G_{\rm all}^{\rm ex}(I)
 :=\sup_{\mathcal T}
 \sum_{\tau\in\mathcal T}|h(\tau)|^2,
 \tag{3.1}
\]

where the supremum runs over all finite subsets

\[
 \mathcal T\subset\{\tau\in I:F_0(\tau)=0\}.
 \tag{3.2}
\]

### Theorem 3.1 -- complex target row packing

Every finite-carrier solution of (2.1)--(2.3) with \(\delta\ne0\) satisfies

\[
 \boxed{
 G_{\rm all}^{\rm ex}(I)
 \le E_A\rho(A)^2
 +2\int_I|hQF|\,dx
 +2|\delta|\int_I|hb|\,dx.}
 \tag{3.3}
\]

#### Proof

Take an arbitrary finite ordered root subset

\[
 A\le\tau_1<\cdots<\tau_m\le A+X.
 \tag{3.4}
\]

Use the integrating-factor target

\[
 X_0(x)=e^{\lambda_0(x-A)}F_0(x).
 \tag{3.5}
\]

Equations (2.8)--(2.9) give

\[
 X_0'(x)=\delta e^{\lambda_0(x-A)}h(x),
 \tag{3.6}
\]

\[
 X_0''(x)
 =\delta e^{\lambda_0(x-A)}[Q(x)F(x)+\delta b(x)].
 \tag{3.7}
\]

Apply the one-gap estimate from Theorem 1.1 on
\([\tau_{j-1},\tau_j]\).  After division by
\(|\delta|^2e^{2\lambda_0(\tau_j-A)}\),

\[
\begin{aligned}
 |h(\tau_j)|^2
 &\le2\int_{\tau_{j-1}}^{\tau_j}
 e^{-2\lambda_0(\tau_j-x)}
 |h(x)|\,|QF+\delta b|\,dx\\
 &\le2\int_{\tau_{j-1}}^{\tau_j}
 \left(|hQF|+|\delta||hb|\right)\,dx.
\end{aligned}
\tag{3.8}
\]

The last inequality uses \(\lambda_0\ge0\) and \(x\le\tau_j\).  The gaps
are disjoint.  The first root satisfies

\[
 |h(\tau_1)|^2\le\rho(\tau_1)^2E_A
 \le\rho(A)^2E_A,
 \tag{3.9}
\]

because the shear row decays and the energy contracts.  Summing and taking
the supremum proves (3.3). \(\square\)

### 3.1 Comparison with the real Rolle corollary

R0.72H (6.5) required a fixed real target gauge.  Between two real target
roots it produced an actual zero of \(h\), then integrated \(hh'\).  That
route introduced a positive \(2\lambda_0^2Q_*^I\) term through
\(h'=-\lambda_0h+QF+\delta b\).

Theorem 3.1 works for arbitrary complex phases and applies the integrating
factor before the directional projection.  The nonnegative kernel in (3.8)
is at most one, so there is no exponential loss and no separate
\(\lambda_0^2Q_*^I\) term.  The improvement is structural, not a consequence
of a complex derivative zero.

### 3.2 The zero-coupling boundary

Division by \(\delta\) is essential.  At \(\delta=0\), the physical target
slope \(F_0'\) at a target root does not contain \(h\).  If the uncoupled
target coordinate vanishes identically, the raw \(h\)-ledger can be unrelated
to a physical root-slope measure.  Theorem 3.1 is therefore stated only for
\(\delta\ne0\).

---

## 4. Carrier-free finite-row corollary

R0.72H proved

\[
 \mathcal E_Q(I):=\int_I|hQF|\,dx
 \le6\sqrt\nu\,d|K_z|
 [\lambda_0E_A m_*(A,X)Q_*^I]^{1/2},
 \tag{4.1}
\]

where

\[
 Q_*^I=\int_A^{A+X}
 w_*\!\left(\frac{x-A}{X}\right)\mathfrak q(x)\,dx,
 \qquad
 w_*(s)=s^{-1/3}[1+\log(1/s)],
 \tag{4.2}
\]

and \(m_*\) is the reciprocal-weight carrier moment.

R0.72J proved the hybrid true-cubic bound

\[
 \mathcal C_\times(I)
 \le\min\left\{
 |\delta|\sqrt{\lambda_0}B_AQ_*^I,
 |\delta|E_A\int_I\rho(x)^2\|V(x)\|\,dx
 \right\}.
 \tag{4.3}
\]

Substitution in Theorem 3.1 gives (0.6).  Its constants are independent of
the number and locations of finite carriers.  Carrier geometry remains in the
explicit moments and the joint heat exposure; no unweighted coefficient
\(\ell^1\) norm is introduced by the root-sampling step.

---

## 5. Complete common-band theorem

I now impose the exact common-band assumptions of R0.72J.  The carrier
frequencies and coefficients satisfy

\[
 R\le|r_l|\le C_0R,
 \qquad c_0a\le|w_l|\le C_0a,
 \qquad l=1,\ldots,N,
 \tag{5.1}
\]

and the heat multiplier obeys

\[
 \|V(x)\|\le C_1aB e^{-c_1R^2x},
 \qquad \sqrt N\lesssim B\lesssim N.
 \tag{5.2}
\]

Let

\[
 g=|\delta|a,
 \qquad
 \varepsilon=\frac{gB}{R^2}\le\gamma_0,
 \tag{5.3}
\]

and take the row-aligned launch, including the exact complex root correction,
with energy \(E_0=N\).

The estimates proved in R0.72J are

\[
 \rho(0)^2\asymp a^2N,
 \tag{5.4}
\]

\[
 Q_*\asymp
 a^2N^2R^{-4/3}(1+\log R),
 \tag{5.5}
\]

\[
 m_*\le
 Ca^2NR^{4/3}(1+\log R)^{-1},
 \tag{5.6}
\]

\[
 \mathcal C_\times
 \le C\varepsilon a^2N^2.
 \tag{5.7}
\]

Consequently

\[
 E_0\rho(0)^2\asymp a^2N^2,
 \tag{5.8}
\]

and

\[
 [E_0m_*Q_*]^{1/2}\le Ca^2N^2.
 \tag{5.9}
\]

### Theorem 5.1 -- complete complex common-band roots

Under (5.1)--(5.3), for sufficiently small fixed \(\gamma_0\),

\[
 \boxed{G_{\rm all}^{\rm ex}([0,X])\asymp a^2N^2.}
 \tag{5.10}
\]

The constants are independent of (R,N,B,a,g) inside the declared class.

#### Proof

Equations (3.3) and (5.7)--(5.9) give the upper bound.  R0.72J Lemma 5.3
constructs an exact complex root at \(\tau=R^{-3}\) and proves

\[
 |h(\tau)|\ge caN.
 \tag{5.11}
\]

That one atom gives the lower bound. \(\square\)

The theorem determines the order of the complete extended root mass without
enumerating the root set.  Any additional hidden complex roots must fit
inside the same \(a^2N^2\) budget.

---

## 6. Full physical normalization

Under the exact amplitude balance of R0.72I--J, the canonical root lift is

\[
 \Theta\asymp\frac{g^2}{a^2NR^2}.
 \tag{6.1}
\]

At every target root, the projected-Lamb identity and the uniform enstrophy
comparison give

\[
 J_*(t_\tau)\asymp\Theta|h(\tau)|^2.
 \tag{6.2}
\]

Therefore Theorem 5.1 yields

\[
 \boxed{
 \mathcal J_{\rm all}
 \asymp\Theta G_{\rm all}^{\rm ex}
 \asymp\frac{g^2N}{R^2}.}
 \tag{6.3}
\]

The physical scales already proved in R0.72J are

\[
 D\asymp g^2NR^2,
 \tag{6.4}
\]

\[
 \mathscr A_*\asymp
 g^2NR^{-10/3}(1+\log R),
 \qquad
 \Lambda_{1,*}\asymp1+\mathscr A_*.
 \tag{6.5}
\]

Put

\[
 Z=g^2NR^{-10/3}(1+\log R).
 \tag{6.6}
\]

Then

\[
\begin{aligned}
 \frac{\mathcal J_{\rm all}}
 {D^{1/3}\Lambda_{1,*}}
 &\asymp
 \frac{g^{4/3}N^{2/3}R^{-8/3}}{1+Z}\\
 &=R^{-4/9}(1+\log R)^{-2/3}
 \frac{Z^{2/3}}{1+Z}.
\end{aligned}
\tag{6.7}
\]

Since \(Z^{2/3}/(1+Z)\) is uniformly bounded,

\[
 \boxed{
 \sup_{N,B,g}
 \frac{\mathcal J_{\rm all}}
 {D^{1/3}\Lambda_{1,*}}
 \le
 CR^{-4/9}(1+\log R)^{-2/3}\longrightarrow0,}
 \tag{6.8}
\]

where the supremum is restricted to the declared common-band assumptions.

### 6.1 The coherent mixed-parity block

For

\[
 S_R=\{R,R+1,\ldots,3R-1\},
 \qquad N=2R,
 \qquad g=\gamma R,
 \tag{6.9}
\]

R0.72J proved a raw true-cubic mass of order \(R^2\).  Theorem 5.1 now gives
the complete raw root mass

\[
 G_{\rm all}^{\rm ex}\asymp R^2.
 \tag{6.10}
\]

Its full physical root ledger and normalized ratio satisfy

\[
 \mathcal J_{\rm all}\asymp R,
 \qquad
 \frac{\mathcal J_{\rm all}}
 {D^{1/3}\Lambda_{1,*}}
 \asymp R^{-2/3}.
 \tag{6.11}
\]

The previous cubic no-go is therefore not hiding an unbounded collection of
additional complex roots.

---

## 7. Finite audit contract

The proof of Theorems 1.1 and 3.1 is analytic.  The finite audit has a
narrower role.

The producer route:

1. checks the mean-zero directional projection on exact rational
   piecewise-linear derivative families;
2. verifies the sharpness ratio approaching one for the factor-two theorem;
3. checks a genuinely complex periodic curve whose derivative never
   vanishes;
4. derives the new measured and theorem-level complete-root upper ledgers
   from the archived R0.72J producer rows;
5. records the inherited input SHA-256 and all transformed quantities.

The independent route:

1. uses a different parameterization of the sharpness family;
2. samples complex two-component trigonometric curves and reconstructs the
   directional zeros numerically;
3. derives the complete-root ledgers from the independently generated
   R0.72J rows;
4. shares no producer outputs or code.

The cross-check compares only common declared quantities.  No new PDE time
evolution is needed: the new mathematical step is the analytic sampling
lemma, while the finite \(h,QF,b,Q_*\) data were already evolved twice and
archived in R0.72J.  The R0.72K certificate preserves this lineage rather
than silently duplicating it.

Finite agreement does not enumerate all roots and does not prove the
asymptotic theorem.

---

## 8. Literature boundary

The literature audit compares the directional lemma with Opial-type
inequalities, Hilbert-valued endpoint inequalities, Banach indicatrix
theorems, scattered-zero Sobolev estimates, complex Rolle frameworks, and
Navier--Stokes time analyticity.

These neighboring results have different targets:

1. Opial inequalities control integrals involving a function and its
   derivative, not a discrete squared derivative mass at every zero.
2. Indicatrix theorems average crossing information over levels, while zero
   is fixed here.
3. Scattered-zero estimates pay an externally imposed fill distance.
4. Complex Rolle and Voorhoeve theories count analytic zeros through complex
   growth or differential-equation structure.
5. Time analyticity isolates nontrivial temporal zeros but supplies no
   mixed-row or true-cubic payment.

The bounded primary-source search found no source directly stating (0.3) or
its project-specific consequence (0.5).  I do not infer originality,
priority, or nonexistence from that search.  The proof is included in full so
the result does not depend on the literature search outcome.

---

## 9. What is proved and what is not

### Proved

1. A zero-count- and separation-free derivative-mass inequality for roots of
   real or complex Banach-valued \(W^{2,1}\) curves.
2. Necessity of the first-root payment and sharpness of the factor two.
3. A complete complex-target root theorem for every finite triangular shear
   configuration with \(\delta\ne0\).
4. Removal of the real-gauge condition and of the extra
   \(2\lambda_0^2Q_*\) term from the earlier Rolle corollary.
5. The scale \(G_{\rm all}^{\rm ex}\asymp a^2N^2\) in the perturbative
   common-band class.
6. The complete physical scale
   \(\mathcal J_{\rm all}\asymp g^2N/R^2\).
7. Uniform decay of the fully normalized complete ledger at the rate in
   (6.8).
8. Closure of the entire complex-root ledger for the triangle-rich coherent
   block of R0.72J.

### Not proved

1. A multiscale version when carriers occupy several separated heat windows.
2. A strong-coupling version beyond \(gB/R^2\le\gamma_0\).
3. A uniform physical inequality for every finite triangular solution.
4. A corresponding root ledger for arbitrary full three-dimensional
   Navier--Stokes solutions.
5. A new continuation criterion, exclusion of finite-time singularities, a
   singular solution, or global regularity.
6. Novelty or priority of the abstract directional lemma.

---

## 10. Exact conclusion and next gate

R0.72J correctly refused to use real Rolle theory on a complex target.  The
repair is not to force the trajectory onto a real line and not to count its
complex zeros.  Each root gap has its own real direction: the direction of
the derivative at the right endpoint.  Its projected derivative has zero
mean, which is enough to charge that endpoint slope to one continuous
weighted variation integral.

That single observation converts the mixed-row and true-cubic estimates
already proved in R0.72H--J into a complete root theorem.  It also shows that
the common-band coherent construction cannot conceal a large uncounted
complex-root ledger.

The next finite gate should return to the part not touched by the sampling
lemma: the continuous row bounds outside one heat scale.  A valid R0.72L
route must either

1. sum joint exposures across separated carrier scales without an
   uncontrolled cross-shell factor; or
2. analyze strong coupling without using the perturbative Duhamel closeness
   that produced the exact common-band lower and upper scales.

Until one of those gates closes, the result remains a rigorous structural
theorem in an exact globally smooth test class.  The Clay Millennium Problem
remains unsolved.
