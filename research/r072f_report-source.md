# R0.72F -- the critical-log initial-layer repair and its admissible window

**Date:** 2026-08-27
**Status:** analytic screening theorem.  The result identifies the minimal
regularly varying initial-layer weight that is simultaneously not
contradicted by the selected R0.72E Bessel roots and payable by the Leray
energy inequality.  It does not prove the complete-root estimate with that
weight.

**Keywords:** Navier--Stokes regularity, projected Lamb vector, negative
Sobolev action, initial layer, weighted energy, temporal roots, Bessel
functions, exact triangular flows

---

## 0. Direct decision

R0.72E disproved the unweighted candidate

\[
 \mathcal J_{\rm all}(I)
 \le C D^{1/3}\Lambda_1(I;u)
 \tag{0.1}
\]

inside an exact globally smooth triangular Navier--Stokes class.  That
release left three possible repairs: an initial-layer frequency charge, a
time-weighted rotational action, or an explicit coupling-scale data term.

This report separates them.

For an interval \(I=[a,a+T]\), put

\[
 Y(t)=\|\omega(t)\|_2^2,
 \qquad
 L(t)=\mathbb P(u(t)\times\omega(t)),
 \tag{0.2}
\]

and, for \(0\le\beta<1\) and \(\gamma\ge0\), define

\[
 w_{\beta,\gamma}(s)
 :=s^{-\beta}[1+\log(1/s)]^\gamma,
 \qquad0<s\le1,
 \tag{0.3}
\]

and the dimensionless initial-layer action

\[
 \mathscr A_{\beta,\gamma}(I;u)
 :=\frac1T\int_a^{a+T}
 w_{\beta,\gamma}\!\left(\frac{t-a}{T}\right)
 \frac{\|L(t)\|_{\dot H^{-1}}^2}{Y(t)}\,dt.
 \tag{0.4}
\]

The quotient is set equal to zero where \(Y=0\).  On intervals where the
enstrophy contrast is finite, let

\[
 \Lambda_{1,\beta,\gamma}(I;u)
 :=\mathcal R_Y(I)\,[\nu^2+\mathscr A_{\beta,\gamma}(I;u)].
 \tag{0.5}
\]

Thus \(\Lambda_{1,0,0}=\Lambda_1\).  I omit \(\gamma=0\) from the
subscript when no logarithmic factor is present.

The two exact thresholds are different.

1. **Counterfamily threshold.**  For the selected positive roots in the
   R0.72E family,

   \[
    \frac{\mathcal J_{{\rm sel},R}}
    {D_R^{1/3}\Lambda_{1,\beta,\gamma}([0,T];u_R)}
   \asymp_{\beta,\gamma,T,q_0}
    \delta_R^{1/3-\beta}
    (\log\delta_R)^{1-\gamma},
    \qquad 0<\beta<1.
    \tag{0.6}
   \]

   Consequently every \(0<\beta<1/3\) still fails, for every fixed
   \(\gamma\).  At \(\beta=1/3\), every \(\gamma<1\) also fails.  The plain
   power endpoint \((\beta,\gamma)=(1/3,0)\) fails logarithmically, whereas
   \((1/3,1)\) exactly saturates the certified selected obstruction.
   The separate endpoint \(\beta=0\) also fails for every fixed \(\gamma\),
   by the logarithmic upper bound in (3.9), rather than by (0.6).

2. **Leray-payment threshold.**  Every mean-zero Leray--Hopf solution on
   the normalized torus obeys, at every admissible restart time \(a\),

   \[
    \boxed{
    \mathscr A_{\beta,\gamma}([a,a+T];u)
    \le
    C_{\mathbb T^3}\|w_{\beta,\gamma}\|_{L^2(0,1)}
    \frac{\|u(a)\|_2^2}{\sqrt{2\nu T}},
    \qquad 0\le\beta<\frac12.}
    \tag{0.7}
   \]

   This uses only Sobolev duality, interpolation, and the Leray energy
   inequality.  The exponent \(1/2\) is sharp for that information class:
   an arbitrary nonnegative \(Y\in L^1_t\) need not make
   \(t^{-\beta}Y^{1/2}\) integrable when \(\beta\ge1/2\).

It follows that the admissible regularly varying region is

\[
 \boxed{
 \left\{\frac13<\beta<\frac12,\ \gamma\ge0\right\}
 \ \cup\
 \left\{\beta=\frac13,\ \gamma\ge1\right\}.}
 \tag{0.8}
\]

The asymptotically smallest member of this region is the critical-log
weight

\[
 \boxed{
 w_*(s)=s^{-1/3}[1+\log(1/s)],
 \qquad
 \int_0^1w_*(s)^2\,ds=75.}
 \tag{0.9}
\]

It grows more slowly near launch than every power \(s^{-1/3-\varepsilon}\),
but it closes the exact logarithm left by the plain \(s^{-1/3}\) weight.
I therefore select \(w_*\), not an arbitrary interior exponent, as the next
concrete candidate.

This is not yet a proof of

\[
 \mathcal J_{\rm all}(I)
 \stackrel{?}{\le}
 C D^{1/3}\Lambda_{1,*}(I;u),
 \qquad
 \Lambda_{1,*}:=\Lambda_{1,1/3,1}.
 \tag{0.10}
\]

Equation (0.10) remains the next trace-packing question.  The current result
proves that its new action is energy-payable and that the selected R0.72E
obstruction is exactly saturated.  It does not control possible additional
complete roots.

---

## 1. Scale and solution class

Work first on the normalized three-torus with mean-zero divergence-free
velocity.  The mean-zero condition is harmless for the exact family and
allows the homogeneous Sobolev estimates below to be written without an
additional zero-mode term.

Under the whole-space Navier--Stokes rescaling, with the spatial domain
rescaled together with the solution,

\[
 u_\lambda(x,t)=\lambda u(\lambda x,\lambda^2t),
 \tag{1.1}
\]

both \(Y=\|\omega\|_2^2\) and
\(\|\mathbb P(u\times\omega)\|_{\dot H^{-1}}^2\) scale by \(\lambda\).
For the integer covering scaling on a fixed normalized torus they instead
both scale by \(\lambda^4\).
The quotient in (0.4), the relative time \((t-a)/T\), its normalized time
average, and \(\mathcal R_Y\) are therefore all dimensionless.  The
weighted factor does not break parabolic scaling when the observation
interval is scaled with the solution.

This invariance belongs to the new action, not to the entire proposed
right-hand side.  The inherited data size
\(D=\|u_0\|_2^2+\|\omega_0\|_2^2\) is nonhomogeneous: under whole-space
rescaling its two terms scale as \(\lambda^{-1}\) and \(\lambda\), while
under the fixed-torus integer covering they scale as \(\lambda^2\) and
\(\lambda^4\).  Thus (0.10) remains a normalized-domain candidate rather
than a scale-covariant whole-space estimate.

For the exact lower family, retain the R0.72E normalization

\[
 u_R=(f_R(y,z,t),0,v_R(y,t)),
 \qquad
 v_R=P_Re^{-q_0^2t}(e^{iq_0y}+e^{-iq_0y}),
 \tag{1.2}
\]

where \(q_0>R_*\) is fixed and

\[
 \widehat f_R(q_0r,1,t)=S_RF_{R,r}(q_0^2t).
 \tag{1.3}
\]

With \(x=q_0^2t\), \(\mu=q_0^{-2}\), and

\[
 (D_\mu F)_r=-(r^2+\mu)F_r,
 \qquad
 (V(x)F)_r=-ie^{-x}(F_{r-1}+F_{r+1}),
 \tag{1.4}
\]

the active sector solves

\[
 F_x=D_\mu F+\delta V(x)F,
 \qquad F(0)=ie_{-1}.
 \tag{1.5}
\]

The amplitudes are

\[
 \delta_R=R^4,
 \qquad
 P_R=q_0^2\delta_R,
 \qquad
 S_R^2=\frac{\delta_R}{\log(2+\delta_R)}.
 \tag{1.6}
\]

Every member is an exact smooth global unforced three-dimensional
Navier--Stokes solution.  In particular, no conclusion below is a blow-up
construction.

---

## 2. Energy payment for the weighted projected-Lamb action

### Lemma 2.1 -- pointwise energy-level bound

For almost every regular time of a mean-zero divergence-free velocity,

\[
 \boxed{
 \frac{\|\mathbb P(u\times\omega)\|_{\dot H^{-1}}^2}
 {\|\omega\|_2^2}
 \le C_{\mathbb T^3}\|u\|_2\|\omega\|_2.}
 \tag{2.1}
\]

#### Proof

The Leray projection is bounded on \(\dot H^{-1}\).  Sobolev duality,
Holder, and the periodic Gagliardo--Nirenberg inequality give

\[
\begin{aligned}
 \|\mathbb P(u\times\omega)\|_{\dot H^{-1}}
 &\le C\|u\times\omega\|_{6/5}\\
 &\le C\|u\|_3\|\omega\|_2\\
 &\le C\|u\|_2^{1/2}\|\omega\|_2^{3/2}.
\end{aligned}
 \tag{2.2}
\]

Square and divide by \(\|\omega\|_2^2\).  If the latter vanishes, the
mean-zero velocity and the projected Lamb vector both vanish.  This proves
(2.1).  \(\square\)

### Theorem 2.2 -- Leray payment for regularly varying weights

Let \(u\) be a mean-zero Leray--Hopf solution, and let \(a\) be a time from
which the strong energy inequality holds.  Then (0.7) holds for every
\(0\le\beta<1/2\) and every fixed \(\gamma\ge0\).

#### Proof

Energy monotonicity and Lemma 2.1 give

\[
 \mathscr A_{\beta,\gamma}
 \le
 \frac{C\|u(a)\|_2}{T}
 \int_a^{a+T}
 w_{\beta,\gamma}\!\left(\frac{t-a}{T}\right)
 Y(t)^{1/2}\,dt.
 \tag{2.3}
\]

Cauchy--Schwarz with normalized time measure yields

\[
\begin{aligned}
 \mathscr A_{\beta,\gamma}
 &\le C\|u(a)\|_2
 \left(\int_0^1w_{\beta,\gamma}(s)^2\,ds\right)^{1/2}
 \left(\frac1T\int_a^{a+T}Y(t)\,dt\right)^{1/2}\\
 &\le
 C\|w_{\beta,\gamma}\|_{L^2(0,1)}
 \|u(a)\|_2
 \left(\frac{\|u(a)\|_2^2}{2\nu T}\right)^{1/2}.
\end{aligned}
 \tag{2.4}
\]

The last step is the Leray energy inequality.  This is (0.7).  \(\square\)

For the critical-log weight,

\[
\begin{aligned}
 \|w_*\|_2^2
 &=\int_0^1s^{-2/3}[1+\log(1/s)]^2\,ds\\
 &=3+18+54=75.
\end{aligned}
 \tag{2.5}
\]

Thus the endpoint repair has an explicit finite energy-payment constant.

### Proposition 2.3 -- sharpness of the energy-only endpoint

The restriction \(\beta<1/2\) cannot be improved using only
\(Y\in L^1(0,T)\).

For \(\beta>1/2\), choose

\[
 Y(t)=t^{-p},
 \qquad
 2(1-\beta)\le p<1,
 \tag{2.6}
\]

near zero.  Then \(Y\in L^1\), but
\(t^{-\beta}Y^{1/2}\notin L^1\).  At \(\beta=1/2\), take

\[
 Y(t)=\frac1{t[\log(e/t)]^2}
 \tag{2.7}
\]

on a sufficiently short interval.  Again \(Y\in L^1\), whereas
\(t^{-1/2}Y^{1/2}=1/[t\log(e/t)]\) is not integrable.

These are scalar budget profiles, not claimed Navier--Stokes enstrophy
trajectories.  They prove sharpness only for the information used in
Theorem 2.2.

---

## 3. Exact weighted action of the R0.72E family

For fixed \(X>0\), \(0\le\beta<1\), and \(\gamma\ge0\), define

\[
 Q_{\beta,\gamma,\delta,q_0}(X)
 :=\int_0^X
 w_{\beta,\gamma}\!\left(\frac{x}{X}\right)
 \|V(x)F_\delta(x)\|_{A_q^{-1}}^2\,dx,
 \qquad
 A_q=q_0^{-2}-\partial_\theta^2.
 \tag{3.1}
\]

### Theorem 3.1 -- two-sided regularly varying initial-layer asymptotic

For every fixed \(q_0\), \(X>0\), \(0<\beta<1\), and \(\gamma\ge0\), there
are positive constants \(c_{\beta,\gamma,X,q_0}\),
\(C_{\beta,\gamma,X,q_0}\), and \(\delta_0\) such
that

\[
 \boxed{
 c_{\beta,\gamma,X,q_0}\delta^{\beta-1}(\log\delta)^\gamma
 \le Q_{\beta,\gamma,\delta,q_0}(X)
 \le C_{\beta,\gamma,X,q_0}\delta^{\beta-1}(\log\delta)^\gamma,
 \qquad \delta\ge\delta_0.}
 \tag{3.2}
\]

The constants are not uniform as \(\beta\downarrow0\), \(\beta\uparrow1\),
or \(q_0\to\infty\).

#### Upper bound

R0.72E proved the pointwise estimate

\[
 \|V(x)F_\delta(x)\|_{A_q^{-1}}^2
 \le C_{X,q_0}
 \min\left\{1,\frac1{\delta x}\right\},
 \qquad 0<x\le X.
 \tag{3.3}
\]

Split the integral at \(x=\delta^{-1}\).  The standard endpoint estimate
for a regularly varying factor gives, for fixed \(\beta>0\) and \(\gamma\),

\[
\begin{aligned}
 Q_{\beta,\gamma,\delta,q_0}(X)
 &\le C X^\beta
 \left[
 \int_0^{\delta^{-1}}x^{-\beta}[1+\log(X/x)]^\gamma\,dx
 +
 \delta^{-1}\int_{\delta^{-1}}^X
 x^{-1-\beta}[1+\log(X/x)]^\gamma\,dx
 \right]\\
 &\le C_{\beta,\gamma,X,q_0}
 \delta^{\beta-1}(\log\delta)^\gamma.
\end{aligned}
 \tag{3.4}
\]

#### Lower bound

Let \(F_0=ie_{-1}\).  The diagonal semigroup is contractive, \(V(x)\) is
uniformly bounded on \(\ell_2\), and \(F_0\) lies in the domain of
\(D_\mu\).  The mild equation gives, for \(0\le x\le c/\delta\),

\[
 \|F_\delta(x)-F_0\|_2
 \le Cx+C\delta x.
 \tag{3.5}
\]

Also \(\|[V(x)-V(0)]F_0\|_2\le Cx\).  Since
\(\|V(0)F_0\|_{A_q^{-1}}>0\), choose \(c>0\) sufficiently small,
independently of \(\delta\), to obtain

\[
 \|V(x)F_\delta(x)\|_{A_q^{-1}}^2\ge c_0>0,
 \qquad 0\le x\le c/\delta.
 \tag{3.6}
\]

Integrate only over \([c/(2\delta),c/\delta]\), where
\(1+\log(X/x)\asymp\log\delta\).  Therefore

\[
 Q_{\beta,\gamma,\delta,q_0}(X)
 \ge c_{\beta,\gamma,X,q_0}
 \delta^{\beta-1}(\log\delta)^\gamma.
 \tag{3.7}
\]

This proves (3.2).  \(\square\)

At \(\beta=0\), R0.72E gives the different upper law

\[
 Q_{0,0,\delta,q_0}(X)
 \le C_{X,q_0}\frac{1+\log(2+\delta)}{\delta}.
 \tag{3.8}
\]

The same split with a fixed logarithmic power gives

\[
 Q_{0,\gamma,\delta,q_0}(X)
 \le C_{\gamma,X,q_0}
 \frac{[1+\log(2+\delta)]^{\gamma+1}}{\delta},
 \qquad \gamma\ge0.
 \tag{3.9}
\]

Indeed, the initial piece is
\(O(\delta^{-1}(\log\delta)^\gamma)\), while after the pointwise
\((\delta x)^{-1}\) factor is inserted the second piece is an elementary
logarithmic integral of order
\(\delta^{-1}(\log\delta)^{\gamma+1}\).  With the physical amplitude in
(1.6), this implies
\(\mathscr A_{0,\gamma}=O((\log\delta_R)^\gamma)\).  Therefore the selected
ratio is bounded below by
\(c\delta_R^{1/3}/(1+(\log\delta_R)^\gamma)\), which still diverges for
every fixed \(\gamma\).

The nonuniform transition at \(\beta=0\) is why the endpoint must be kept
separate in every exponent audit.

---

## 4. The exact one-third obstruction

For the physical family (1.2)--(1.6), R0.72E proved

\[
 D_R\asymp_{q_0}\delta_R^2,
 \qquad
 \mathcal R_{Y_R}([0,T])\asymp_{T,q_0}1,
 \tag{4.1}
\]

and the exact Fourier identity for the full projected Lamb vector.  The
upper and lower enstrophy bounds in that release turn Theorem 3.1 into

\[
 \mathscr A_{\beta,\gamma}([0,T];u_R)
 \asymp_{\beta,\gamma,T,q_0}
 S_R^2\delta_R^{\beta-1}(\log\delta_R)^\gamma
 \asymp
 \delta_R^\beta(\log\delta_R)^{\gamma-1},
 \qquad 0<\beta<1.
 \tag{4.2}
\]

The first \(R\) exact roots satisfy

\[
 c k\le\delta_Rq_0^2t_{k,R}\le Ck,
 \qquad
 c k^{-1}\le |h_{k,R}|^2\le Ck^{-1},
 \qquad 1\le k\le R,
 \tag{4.3}
\]

with constants independent of \(R\).  Their physical atom sum therefore
obeys the two-sided estimate

\[
 \mathcal J_{{\rm sel},R}
 \asymp_{q_0}S_R^2\sum_{k=1}^R|h_{k,R}|^2
 \asymp S_R^2\log R
 \asymp\delta_R.
 \tag{4.4}
\]

Equations (4.1), (4.2), and (4.4) prove (0.6).  In particular,

\[
 \frac{\mathcal J_{{\rm sel},R}}
 {D_R^{1/3}\Lambda_{1,1/3,0}}
 \asymp\log\delta_R\longrightarrow\infty.
 \tag{4.5}
\]

Because the selected roots form a subset of the complete positive root
measure, (4.5) disproves the complete-root candidate at the endpoint as
well.

For the critical-log weight,

\[
 \frac{\mathcal J_{{\rm sel},R}}
 {D_R^{1/3}\Lambda_{1,*}}
 \asymp1.
 \tag{4.6}
\]

For every fixed \(\beta>1/3\), the selected ratio in (0.6) tends to zero.
Equation (4.6) makes \(w_*\) the minimal regularly varying saturation of the
known obstruction.  Neither statement is an upper bound for the complete
root measure.

---

## 5. Why a fixed initial frequency profile does not repair the estimate

At launch, the R0.72E family has Fourier support in a fixed finite set:
the shear lies at \((\pm q_0,0)\), and the active seed lies at the conjugate
pair generated by \((-q_0,1)\).  Only the amplitudes change with \(R\).

For each fixed \(s\ge0\), define the normalized initial frequency moment

\[
 \kappa_s(u_0)
 :=\frac{\|u_0\|_{\dot H^s}}{\|u_0\|_2}.
 \tag{5.1}
\]

The exact launch norms have the form

\[
 \|u_R(0)\|_{\dot H^s}^2
 =2P_R^2q_0^{2s}
 +2S_R^2(q_0^2+1)^s.
 \tag{5.2}
\]

Since \(S_R^2/P_R^2=O((\delta_R\log\delta_R)^{-1})\),

\[
 \kappa_s(u_R(0))\longrightarrow q_0^s.
 \tag{5.3}
\]

Consequently, for any finite list \(s_1,\ldots,s_m\) and any function
\(\Psi\) locally bounded near
\((q_0^{s_1},\ldots,q_0^{s_m})\),

\[
 \Psi(\kappa_{s_1}(u_R(0)),\ldots,\kappa_{s_m}(u_R(0)))=O(1).
 \tag{5.4}
\]

Multiplying the failed R0.72E payment by such a factor leaves its
\(\delta_R^{1/3}\) divergence unchanged.  A repair that sees only a finite
number of amplitude-normalized initial spatial frequency moments is
therefore impossible for this family.  The missing information is the fast
amplitude-driven time scale, not an unresolved launch wave number.

This statement does not cover frequency envelopes with infinitely many
independent coordinates, positive-time moments, or amplitude-sensitive
functionals.

---

## 6. A unified selected-family frontier

The three repairs above can be placed on one exponent ledger.  Keep the
R0.72E shear coupling and root dynamics, but now leave the active amplitude

\[
 X_\delta:=S_\delta^2
 \tag{6.1}
\]

free.  The roots are independent of \(X_\delta\).  For
\(X_\delta=O(\delta)\), the active enstrophy estimate inherited from
R0.72E is \(O(X_\delta\delta^{2/3})=o(\delta^2)\), so the shear still gives
\(D\asymp\delta^2\) and bounded enstrophy contrast.  For \(0<\beta<1\),
Theorem 3.1 gives

\[
 \mathcal J_{{\rm sel},0}\asymp X_\delta\log\delta,
 \qquad
 \mathscr A_{\beta,\gamma}
 \asymp X_\delta\delta^{\beta-1}(\log\delta)^\gamma.
 \tag{6.2}
\]

Let \(a,c\ge0\).  Let \(\mathfrak C_\delta\asymp\delta^2\) be a declared
squared-amplitude data coordinate, and let
\(\Gamma_\delta\asymp\delta\) be a declared coupling coordinate.  For
\(0<\beta<1\), test a right-hand side proportional to
\(\mathfrak C_\delta^a\Gamma_\delta^c
[\nu^2+\mathscr A_{\beta,\gamma}]\).  Choosing

\[
 X_\delta=\delta^{1-\beta}(\log\delta)^{-\gamma}
 \tag{6.3}
\]

keeps the action of order one and preserves shear dominance.  The selected
raw-ledger ratio is then

\[
 \asymp
 \delta^{1-\beta-2a-c}(\log\delta)^{1-\gamma}.
 \tag{6.4}
\]

Hence a necessary selected-family condition is

\[
 \boxed{2a+c+\beta>1,
 \quad\hbox{or}\quad
 2a+c+\beta=1\ \hbox{and}\ \gamma\ge1.}
 \tag{6.5}
\]

This is a no-go frontier, not a sufficient complete-root theorem.  It also
shows that replacing \(\nu^2+\mathscr A\) by a fixed higher power cannot
improve the polynomial frontier: the free amplitude can still be chosen so
that \(\mathscr A=O(1)\).  Any finite list of the normalized launch moments
in Section 5 contributes zero to this exponent ledger.

The endpoint \(\beta=0\) is separate.  From (3.9), choosing

\[
 X_\delta=\delta(\log\delta)^{-(\gamma+1)}
 \tag{6.6}
\]

keeps \(\mathscr A_{0,\gamma}=O(1)\) and makes the raw selected ratio at
least a constant multiple of
\(\delta^{1-2a-c}(\log\delta)^{-\gamma}\).  Thus the endpoint only forces
the polynomial condition \(2a+c\ge1\); it does not inherit the equality
clause in (6.5).

For the historical data exponent \(a=1/3\), the augmented polynomial
frontier has three distinguished vertices:

\[
 (c,\beta,\gamma,\alpha)
 = (0,1/3,1,0),\quad(1/3,0,0,0),\quad(0,0,0,4/9).
 \tag{6.7}
\]

They are respectively the critical-log action, the explicit coupling
repair, and the atom-weight repair of Section 8.  The first lies on (6.5),
the second uses the separate endpoint law (3.8)--(3.9), and the third changes
the left-hand side as well as using that endpoint law.

---

## 7. Explicit coupling-scale payment

In the normalized target geometry \(K_z=\nu=1\), the exact scalar coupling
is

\[
 \Gamma_R:=P_R/q_0^2=\delta_R.
 \tag{7.1}
\]

Let \(\theta\ge0\).  Suppose a candidate repair multiplies the old right-hand side by
\(1+\Gamma^\theta\).  The selected R0.72E ratio then has the lower scaling

\[
 \frac{\mathcal J_{{\rm sel},R}}
 {D_R^{1/3}\Lambda_1(1+\Gamma_R^\theta)}
 \gtrsim
 \delta_R^{1/3-\theta}.
 \tag{7.2}
\]

Thus every \(\theta<1/3\) fails, while a coupling factor must grow at least
as \(\Gamma^{1/3}\) to block this selected obstruction.  Since
\(D_R^{1/2}\asymp\Gamma_R\), the endpoint is equivalent on this family to
raising the total data factor from \(D^{1/3}\) to \(D^{1/2}\):

\[
 D^{1/3}\Gamma^{1/3}\asymp D^{1/2}.
 \tag{7.3}
\]

For transported target geometry the covariant model parameter is instead
\(\Gamma=P|K_z|/(\nu q_0^2)\).  The normalized formula \(P/q_0^2\) is
therefore both target-specific and nonintrinsic as a functional of a
general velocity field.  Replacing it by an intrinsic amplitude norm would
require a separate definition and a separate PDE payment.  Equation (7.2)
is a necessity test, not a general positive theorem.

---

## 8. Weighting the root ledger itself is a different problem

For comparison, define a selected time-weighted root measure

\[
 \mathcal J_{{\rm sel},\alpha}
 :=\sum_{k=1}^R
 \left(\frac{t_{k,R}}T\right)^\alpha J_*(t_{k,R}),
 \qquad \alpha>0.
 \tag{8.1}
\]

Using (4.3),

\[
\begin{aligned}
 \mathcal J_{{\rm sel},\alpha}
 &\asymp S_R^2\delta_R^{-\alpha}
 \sum_{k=1}^Rk^{\alpha-1}\\
 &\asymp
 \frac{\delta_R^{1-3\alpha/4}}{\log\delta_R}.
\end{aligned}
 \tag{8.2}
\]

Therefore

\[
 \frac{\mathcal J_{{\rm sel},\alpha}}
 {D_R^{1/3}\Lambda_1}
 \asymp
 \frac{\delta_R^{1/3-3\alpha/4}}{\log\delta_R}.
 \tag{8.3}
\]

The selected divergence survives for \(0<\alpha<4/9\) and disappears at
\(\alpha=4/9\).  This does not repair the original raw root measure; it
changes the quantity being controlled.  Such a change would need a new
argument showing that the weighted measure is still sufficient for the
intended continuation step.

---

For \(0<\beta<1\), inserting (6.3) into this weighted ledger gives the
necessary polynomial condition

\[
 \boxed{2a+c+\beta+\frac{3\alpha}{4}\ge1,
 \qquad \alpha>0.}
 \tag{8.4}
\]

At the historical unweighted-action vertex \(a=1/3\), the first passing
atom exponent is \(\alpha=4/9\), with the extra inherited logarithm making
the finite-family ratio decay there.

At \(\beta=0\), use (6.6), not (6.3).  The weighted selected ratio is then
bounded below by a constant multiple of
\(\delta^{1-2a-c-3\alpha/4}(\log\delta)^{-(\gamma+1)}\).  It gives the same
polynomial condition (8.4), while equality already has logarithmic decay.

---

## 9. Literature boundary

The pointwise projected-Lamb identity and its negative-Sobolev role are
consistent with Lerner--Vigneron, *On Some Properties of the Curl Operator
and Their Consequences for the Navier--Stokes System*, Communications in
Mathematical Research 38 (2022), 449--497,
[DOI 10.4208/cmr.2021-0106](https://doi.org/10.4208/cmr.2021-0106).
Equation (2.1) and the weighted estimate (0.7) are elementary consequences
derived here; they are not quoted as theorems from that paper.

Foias--Guillope--Temam, *New a priori estimates for Navier--Stokes equations
in dimension 3*, Communications in Partial Differential Equations 6 (1981),
329--359,
[DOI 10.1080/03605308108820180](https://doi.org/10.1080/03605308108820180),
proves a higher-derivative time-integrability hierarchy.  Its one-third
exponent concerns \(\int H_2^{1/3}\,dt\), not the initial-layer weight
\(\beta=1/3\) or the data factor \(D^{1/3}\) used here.

The quantitative action input (3.3) is inherited from R0.72E.  Its external
density theorem remains Kusuoka--Stroock, *Applications of the Malliavin
calculus, Part II*, Corollary (3.25) and inequality (3.27),
[DOI 10.15083/00039520](https://doi.org/10.15083/00039520).

The checked sources do not state Theorems 2.2 or 3.1, the exact threshold
(4.5), the critical-log saturation (4.6), or a complete-root estimate in
the admissible region (0.8).  This is a bounded
non-collision statement, not a claim of novelty, priority, or exhaustive
coverage.

---

## 10. Claim--evidence boundary

### Proved

1. The action \(\mathscr A_{\beta,\gamma}\) is dimensionless under parabolic
   rescaling.
2. For \(0\le\beta<1/2\) and finite \(\gamma\ge0\), the added action is
   bounded by the Leray energy inequality as in (0.7).
3. The exponent \(1/2\) is sharp for the abstract information
   \(Y\in L^1_t\).
4. For every fixed \(0<\beta<1\) and \(\gamma\ge0\), the R0.72E scaled
   weighted action obeys the two-sided law
   \(Q_{\beta,\gamma}\asymp
   \delta^{\beta-1}(\log\delta)^\gamma\).
5. The selected R0.72E roots disprove every \(0\le\beta<1/3\), and at
   \(\beta=1/3\) they disprove every \(\gamma<1\).
6. The critical-log weight \(w_*=s^{-1/3}[1+\log(1/s)]\) exactly saturates
   the selected obstruction and has squared \(L^2\) norm \(75\).
7. The admissible regularly varying region is exactly (0.8) for the two
   finite tests performed here.
8. Every repair depending only on finitely many amplitude-normalized
   initial frequency moments remains blind to the R0.72E coupling scale.
9. An explicit coupling factor \(\Gamma^\theta\) needs
   \(\theta\ge1/3\) on this family.
10. Weighting the root atoms themselves has a different selected threshold
   \(\alpha=4/9\).
11. Allowing the active amplitude to vary gives the unified necessary
   selected-family frontier (6.5), and (8.4) after the target atoms are
   weighted.

### Not proved

1. The complete-root candidate (0.10), even in the exact triangular class.
2. An upper bound on additional roots outside the selected Bessel
   neighborhoods under the new weight.
3. A trace theorem converting \(\mathscr A_{1/3,1}\) into the complete raw
   root ledger for arbitrary three-dimensional solutions.
4. A new continuation criterion.
5. Propagation into nontriangular dynamics with feedback from \(f\) to
   \(v\).
6. Finite-time singularity or global regularity for general three-dimensional
   Navier--Stokes.
7. Originality, priority, or an exhaustive literature claim.

---

## 11. Research value and next finite gate

R0.72E showed that the unweighted complete-root payment fails.  The current
result prevents an arbitrary repair from being inserted without a scale
audit.  Fixed launch frequencies are blind to the strong coupling.  A direct
coupling term needs at least an additional factor \(D^{1/6}\), raising the
data exponent from \(1/3\) to \(1/2\) on this family.  A
time-weighted action has two independently forced endpoints, leaving the
strict interval \((1/3,1/2)\).

The mathematical value is a viable-candidate theorem, not a regularity
theorem.  It reduces the next question to one concrete critical-log weight.
R0.72G should test \(w_*\) against the complete-root BV/trace mechanism.  It
must either prove a sampling inequality with all roots included or construct
an exact family that still makes the complete ratio diverge.
