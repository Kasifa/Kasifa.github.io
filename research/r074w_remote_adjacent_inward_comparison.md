# R0.74W — remote adjacent-inward comparison for the common-shear packet

## 0. Result, status, and exact boundary

This note resolves the first endpoint part of R0.74V, Proposition V.0, for
the frozen two-packet common-shear family.  The answer is a scale dichotomy,
not a uniform reuse of the near-lobe estimate.

Write

\[
 p:=\frac1\lambda=\frac{32}{63},\qquad
 d:=c_h-p=\frac{433}{1008},\qquad
 q_{64}:=\frac{p^2}{4\cdot64}=\frac4{3969},
 \tag{W.1}
\]

and

\[
 q_{65}:=\frac{p^2}{4\cdot65}
 =\frac{256}{257985}<q_{64}.
 \tag{W.2}
\]

For packet \(m\), put \(L=L_m\), let \(t=\tau_m\), and write
\(\ell=t/R^2\in[64,65]\).  On a width-\(R\) strip just inside the outer
face of the adjacent inward shell, the exact conditional Brownian-bridge
calculation gives the horizontal displacement scale, in probability under
the central conditional bridge:

\[
 \boxed{
 \mathbb P_{0,y}^{\rm br}\!\left\{
 e^{-(q(\ell)+\eta)L^2}\le\mathfrak S_t
 \le e^{-(q(\ell)-\eta)L^2}\right\}\longrightarrow1
 \quad(\eta>0),
 \qquad
 q(\ell):=\frac{p^2}{4\ell}.}
 \tag{W.3}
\]

The total free heat age is \((\ell+1)R^2\), but the shear deficit in
(W.3) has age \(t=\ell R^2\).  Confusing those two ages changes the
threshold and is not allowed.

The rigorous consequences are as follows.

1. If

   \[
    \limsup\frac{\log(1/R)}{L^2}<q_{65},
    \tag{W.4}
   \]

   then, uniformly for every \(\tau_m\in[64R^2,65R^2]\), the direct
   common-shear packet is relatively asymptotic to its free
   derivative-heat comparator on the remote strip.

2. If

   \[
    \liminf\frac{\log(1/R)}{L^2}>q_{64},
    \tag{W.5}
   \]

   then, uniformly in the same time slab, the conditional displacement is
   much larger than the packet width and the direct packet on the fixed
   free-comparator strip is \(o(1)\) relative to that comparator.  The
   packet is swept in the negative \(x_2\)-direction.  This is a proved
   relative failure mechanism, not an absolute \(o(1)\) substitution.

3. The R0.74U reserve forces (W.4) for the outer packet \(m=2\).  Thus the
   free-comparator lower bound predicted in R0.74V (V.64) is a theorem for
   packet (2), including its inversion partner, the other packet,
   periodic windings, amplitudes, and the adjacent-shell weight.

4. On the original R0.74Q scale
   \(R=e^{-L_1^2/320}\), packet (1) satisfies (W.5), whereas packet (2)
   satisfies (W.4).  The two nominally similar adjacent-inward tests
   therefore have opposite outcomes.

The open interval \(q_{65}\le\log(1/R)/L^2\le q_{64}\), and especially
the critical equality at a fixed \(\ell\), requires a sharper transition
asymptotic and is recorded explicitly below.  This note proves no
whole-shell \(H^1\) occupation estimate, no positive-variation upper bound,
and no regularity or singularity theorem for arbitrary solutions.
**NOT CLAY.**

<!-- R074W_REMOTE_V0_SCALE_DICHOTOMY -->
<!-- R074W_PACKET2_RELATIVE_SURVIVAL -->
<!-- R074W_PACKET1_ORIGINAL_SCALE_SWEPT -->
<!-- R074W_NOT_CLAY -->

## 1. Frozen family and an explicit remote strip

Retain all notation and hypotheses of R0.74V:

\[
 \lambda=\frac{63}{32},\qquad c_h=\frac{15}{16},\qquad
 L_2=2L_1,\qquad h_m=c_hL_mR,
 \tag{W.6}
\]

\[
 L_1\ge9216,\qquad L_2R\le\frac5{144},\qquad
 R^{-1}e^{-a_SL_1^2}\longrightarrow0,
 \qquad a_S=\frac{75}{22528}.
 \tag{W.7}
\]

The common shear is

\[
 \theta_R(t,x_3)=e^{t\partial_3^2}g_R(x_3),\qquad
 b=B\theta_R,qquad
 B=\frac1{2D_1},
 \tag{W.8}
\]

where

\[
 g_R(x_3)=\sigma\!\left(\frac{\sin x_3}{16R}\right),
 \qquad
 D_1=\int_{R^2}^{65R^2}\theta_R(s,h_1)\,ds.
 \tag{W.9}
\]

The frozen saturation satisfies \(-1\le\sigma\le1\), is odd and smooth,
and equals \(\operatorname {sgn}\) outside \([-1,1]\).  No monotonicity of
\(\sigma\) is added in this note.

At the re-centring time \(t=\tau_m\), \(Q_m(t)=0\).  Put \(L=L_m\) and
define

\[
 \begin{aligned}
 \mathcal S_m:=\biggl\{x:\;&
 |x_1|<\frac14\sqrt{pL}\,R,\\
 &\frac54R<x_2<\frac32R,\\
 &pLR-R<x_3<pLR-\frac12R\biggr\}.
 \end{aligned}
 \tag{W.10}
\]

This is a width-\(R\) vertical core and a fixed horizontal derivative-kernel
interval.  Since the outer radius of \(A_{k_m-1}(R)\) is
\(2^{k_m}R=pL_mR\), elementary squaring gives, for \(L\ge9216\),

\[
 \boxed{\mathcal S_m\subset A_{k_m-1}(R),\qquad
 \Psi_{k_m-1}^R=1\quad\hbox{on }\mathcal S_m.}
 \tag{W.11}
\]

Indeed, \(x_3>pLR-R>pLR/2\), while at the worst outer corner

\[
 x_1^2+x_2^2+x_3^2
 \le \frac{pL}{16}R^2+\frac94R^2
      +(pLR-R/2)^2<(pLR)^2.
 \tag{W.12}
\]

Its volume is exact:

\[
 |\mathcal S_m|=\frac1{16}\sqrt{pL_m}\,R^3.
 \tag{W.13}
\]

For \(x\in\mathcal S_m\), set

\[
 z=x_2,\qquad y=x_3-h_m=-(dL+\delta)R,
 \qquad \frac12<\delta<1.
 \tag{W.14}
\]

The free derivative-heat comparator is

\[
 H_m(t,z,y)
 :=R^3\partial_zK_{R^2+t}^{\rm per}(z)
          K_{R^2+t}^{\rm per}(y).
 \tag{W.15}
\]

If \(a:=1+\ell\in[65,66]\), the central real copies and the fixed
horizontal interval imply

\[
 cR^{-2}\le|\partial_zK_{aR^2}^{\rm per}(z)|\le CR^{-2},
 \tag{W.16}
\]

\[
 cR^{-1}e^{-(dL+\delta)^2/(4a)}
 \le K_{aR^2}^{\rm per}(y)
 \le CR^{-1}e^{-(dL+\delta)^2/(4a)}.
 \tag{W.17}
\]

All noncentral terms in (W.16)--(W.17) are
\(O(e^{-c/R^2})\).  In particular, \(H_m\) has one fixed sign on the
strip and

\[
 |H_m(t,z,y)|\asymp
 e^{-(dL+\delta)^2/(4a)}.
 \tag{W.18}
\]

## 2. Exact all-winding stochastic representation

Let \(G_m^+\) denote the direct positive packet evolved under the common
shear, and use the frame centred at \(Q_m(t)\).  The R0.74F
time-reversed Feynman--Kac identity gives

\[
 G_m^+(t,Q_m(t)+z,h_m+y)
 =R^3\mathbb E_y\!\left[
  \partial_zK_T^{\rm per}(z+\mathfrak S_t^y)
  K_{R^2}^{\rm per}(Y_t^y)\right],
 \tag{W.19}
\]

where \(T=t+R^2=aR^2\), \(Y_s^y=y+\sqrt2W_s\pmod {2\pi}\), and

\[
 \mathfrak S_t^y
 =B\int_0^t
 \bigl[\theta_R(t-s,h_m)-
       \theta_R(t-s,h_m+Y_s^y)\bigr],ds.
 \tag{W.20}
\]

For clarity, we now disintegrate (W.19) over every vertical winding.  Put

\[
 w_n:=k_T(2\pi n-y),\qquad n\in\mathbb Z,
 \tag{W.21}
\]

and let \(\mathbb P_{n,y}^{\rm br}\) be the real Gaussian bridge, with
generator \(\partial_y^2\), from \(y\) at stochastic time (0) to
\(2\pi n\) at time \(T\).  Only its restriction to \(0\le s\le t<T\)
enters (W.20).  The exact all-copy identity is

\[
 \boxed{
 G_m^+(t,Q_m(t)+z,h_m+y)
 =R^3\sum_{n\in\mathbb Z}w_n
  \mathbb E_{n,y}^{\rm br}
  \bigl[\partial_zK_T^{\rm per}(z+\mathfrak S_t)\bigr].}
 \tag{W.22}
\]

In the same notation,

\[
 H_m(t,z,y)
 =R^3\partial_zK_T^{\rm per}(z)
  \sum_{n\in\mathbb Z}w_n.
 \tag{W.23}
\]

Thus relative comparison must be made after division by the full winding
sum.  It is not legitimate to estimate (W.19) by an absolute \(o(1)\).

For the central bridge \(n=0\), the one-time conditional law has mean and
heat variance

\[
 \mu_s=\frac{T-s}{T}y,
 \qquad
 v_s=\frac{s(T-s)}T.
 \tag{W.24}
\]

More explicitly, a real lift of the \(n\)-th bridge is

\[
 Y_s^{(n)}
 =\left(1-\frac{s}{T}\right)y+\frac{s}{T}2\pi n
 +\sqrt2\left(W_s-\frac{s}{T}W_T\right).
 \tag{W.24a}
\]

To derive (W.22), first use the Markov property and append the
\(R^2\)-heat interval carried by \(K_{R^2}^{\rm per}(Y_t)\).  Expanding
both periodic kernels and tiling the real line reduces each copy to

\[
 k_s(\xi-y)k_{T-s}(2\pi n-\xi)
 =k_T(2\pi n-y)k_{v_s}(\xi-\mu_{n,s}),
 \qquad
 \mu_{n,s}=\frac{T-s}{T}y+\frac{s}{T}2\pi n.
 \tag{W.24b}
\]

Conditioning the independent horizontal Brownian motion then convolves
the initial derivative kernel to
\(\partial_zK_T^{\rm per}(z+\mathfrak S_t)\).  Tonelli applies to the
nonnegative vertical bridge weights; the signed horizontal derivative is
conditioned only after this disintegration.  This proves (W.22) with every
winding retained.

The noncentral winding mass is relatively negligible:

\[
 \omega_{\rm per}
 :=\frac{\sum_{n\ne0}w_n}{w_0}
 \le C\exp\!\left[-\frac1{11R^2}\right]
 \le Ce^{-75L^2}=o(1).
 \tag{W.25}
\]

This follows directly from \(|y|=O(LR)\), \(T\le66R^2\), and the chart
condition \(L_2R\le5/144\): eventually \(|y|<1\), so
\((2\pi n-y)^2-y^2\ge24n^2\), while
\((11R^2)^{-1}\ge(144/5)^2L^2/11>75L^2\).
Together with the reserve in (W.7), the same estimate gives
\(R^{-1}\omega_{\rm per}\le Ce^{-70L^2}\) eventually.  Equation (W.25),
rather than deletion of the nonzero windings, will be used below.

## 3. The remote saturation deficit

Define the nonnegative deficit

\[
 A(r,x):=1-\theta_R(r,x)
 =e^{r\partial_x^2}(1-g_R)(x)\ge0.
 \tag{W.26}
\]

Let

\[
 \delta_R:=\arcsin(16R).
 \tag{W.27}
\]

For the present range, \(16R\le\delta_R\le32R\).  The nearest positive
plateau begins at \(\delta_R\).  The standard periodic Gaussian tail gives,
whenever \(x\) is in the positive central plateau,

\[
 A(r,x)\le4\exp\!\left[-
 \frac{(x-\delta_R)^2}{4r}\right]
 \tag{W.28}
\]

with the value at \(r=0\) understood by continuity.  This bound already
includes every lifted defect copy.

There is also a lower bound that does not require \(\sigma\) to be
monotone.  On the interval \([-2\delta_R,-\delta_R]\), one has
\(g_R=-1\), hence \(1-g_R=2\).  Retaining that interval and the central
real heat-kernel copy yields

\[
 A(r,x)\ge
 2\delta_R(4\pi r)^{-1/2}
 \exp\!\left[-\frac{(x+2\delta_R)^2}{4r}\right].
 \tag{W.29}
\]

The upper and lower bounds have the same \(L^2\)-scale exponent at
\(x=pLR+O(R)\), \(r=\ell R^2\):

\[
 -\frac1{L^2}\log A(\ell R^2,pLR+O(R))
 \longrightarrow\frac{p^2}{4\ell}=q(\ell).
 \tag{W.30}
\]

At the reference height \(h_m=c_hLR\), the corresponding uniform upper
exponent is strictly larger:

\[
 A(r,h_m)\le
 C\exp\!\left[-\frac{c_h^2}{260}L^2+CL\right],
 \qquad 0\le r\le65R^2,
 \tag{W.31}
\]

and

\[
 \frac{c_h^2}{260}-q_{64}
 =\frac{125357}{52835328}>0.
 \tag{W.32}
\]

This strict separation makes the remote deficit, rather than the deficit at
the reference height, the leading source of horizontal displacement.

## 4. Conditional bridge upper bound at the relative scale

The bridge conditioning provides more information than the absolute
near-lobe estimate.  For \(n=0\), the semigroup law and (W.24) give the
exact identity

\[
 \mathbb E_{0,y}^{\rm br}
  A(t-s,h_m+Y_s)
 =A(t-s+v_s,h_m+\mu_s).
 \tag{W.33}
\]

Put \(s=\varsigma R^2\).  From (W.14) and (W.24),

\[
 \frac{h_m+\mu_s}{R}
 =\left(p+\frac{d}{\ell+1}\varsigma\right)L
  -\left(1-\frac{\varsigma}{\ell+1}\right)\delta,
 \tag{W.34}
\]

whereas

\[
 \frac{t-s+v_s}{R^2}
 =\ell-\frac{\varsigma^2}{\ell+1}.
 \tag{W.35}
\]

For \(0\le\varsigma\le\ell\), set

\[
 f_\ell(\varsigma):=
 \frac{(p+d\varsigma/(\ell+1))^2}
 {4(\ell-\varsigma^2/(\ell+1))}.
 \tag{W.36}
\]

The elementary inequalities

\[
 f_\ell(\varsigma)
 \ge\frac{(p+d\varsigma/(\ell+1))^2}{4\ell}
 \ge q(\ell)+
 \frac{pd}{2\ell(\ell+1)}\varsigma
 \tag{W.37}
\]

show that the conditional leakage integral is localized to a
\(R^2/L^2\) stochastic-time layer at \(s=0\).  Applying (W.28) to
(W.33), keeping the \(O(R)\) strip and transition offsets explicitly as an
\(O(L)\) term in the exponent, and integrating (W.37) gives

\[
 \int_0^t\mathbb E_{0,y}^{\rm br}
  A(t-s,h_m+Y_s)\,ds
 \le CR^2L^{-2}e^{-q(\ell)L^2+CL}.
 \tag{W.38}
\]

Since

\[
 |\theta_R(r,h_m)-\theta_R(r,h_m+Y_s)|
 \le A(r,h_m)+A(r,h_m+Y_s),
 \tag{W.39}
\]

and \(B R^2\le1/96\), (W.31)--(W.38) imply

\[
 \boxed{
 \mathbb E_{0,y}^{\rm br}|\mathfrak S_t|
 \le CL^{-2}e^{-q(\ell)L^2+CL}
     +Ce^{-c_h^2L^2/260+CL}.}
 \tag{W.40}
\]

For every path and every winding,

\[
 |\mathfrak S_t|\le2Bt\le\frac{65}{48}.
 \tag{W.41}
\]

Combining (W.25), (W.40), and (W.41) therefore yields the full all-winding
conditional estimate

\[
 \frac{\sum_nw_n\mathbb E_{n,y}^{\rm br}|\mathfrak S_t|}
      {\sum_nw_n}
 \le CL^{-2}e^{-q(\ell)L^2+CL}
 +Ce^{-c_h^2L^2/260+CL}
 +C\omega_{\rm per}.
 \tag{W.42}
\]

No periodic winding has been discarded in (W.42).

## 5. A high-probability lower displacement and the sweeping mechanism

The matching lower mechanism also comes from the central conditional
bridge.  Fix \(0<\epsilon<\min\{p/4,d/4\}\), put

\[
 s_*:=\frac{R^2}{L^2},
 \tag{W.43}
\]

and let \(\mathcal E_\epsilon\) be the event, on the real central bridge,

\[
 \sup_{0\le s\le s_*}|Y_s-y|\le\epsilon LR.
 \tag{W.44}
\]

The mean bridge drift on this interval is \(O(R/L)\).  The reflection
bound for the centred Gaussian bridge, whose variance is at most \(2s\),
gives

\[
 \mathbb P_{0,y}^{\rm br}(\mathcal E_\epsilon^c)
 \le C e^{-c\epsilon^2L^4}.
 \tag{W.45}
\]

On \(\mathcal E_\epsilon\), (W.29),
\(t-s\ge(\ell-L^{-2})R^2\), and (W.14) give

\[
 A(t-s,h_m+Y_s)
 \ge c\exp\!\left[-
 \frac{(p+\epsilon)^2}{4\ell}L^2-CL\right]
 \qquad(0\le s\le s_*).
 \tag{W.46}
\]

The identity

\[
 \theta_R(r,h_m)-\theta_R(r,h_m+Y_s)
 =A(r,h_m+Y_s)-A(r,h_m)
 \tag{W.47}
\]

and nonnegativity of \(A\) also give the pathwise lower bound

\[
 A(r,h_m+Y_s)-A(r,h_m)\ge-A(r,h_m)
 \tag{W.48}
\]

outside the short interval.  Thus no unproved monotonicity of the
saturation is being used.  Equations (W.31), (W.43), and (W.46)--(W.48),
together with \(BR^2\ge1/128\), show that on
\(\mathcal E_\epsilon\), for all sufficiently large \(L\),

\[
 \boxed{
 \mathfrak S_t
 \ge cL^{-2}\exp\!\left[-
 \frac{(p+\epsilon)^2}{4\ell}L^2-CL\right]
 =:\Delta_{\epsilon,\ell}(L)>0.}
 \tag{W.49}
\]

Here the retained positive term before absorption is
\(cL^{-2}e^{-(p+\epsilon)^2L^2/(4\ell)-CL}\), whereas the entire
negative reference-height contribution is at most
\(Ce^{-c_h^2L^2/260+CL}\).  The choice
\(\epsilon<d/4\) gives
\((p+\epsilon)^2/256<c_h^2/260\), so their ratio tends to zero.  This is
the explicit comparison that justifies (W.49).

For every \(\eta>0\), choose \(\epsilon\) so small that
\((p+\epsilon)^2/(4\ell)<q(\ell)+\eta/2\).  Equation (W.49), with
(W.45), gives the lower half of (W.3).  Conversely, Markov's inequality
applied to (W.40) gives

\[
 \mathbb P_{0,y}^{\rm br}\!\left\{
 |\mathfrak S_t|>e^{-(q(\ell)-\eta)L^2}\right\}\longrightarrow0.
 \tag{W.49b}
\]

This gives the upper half.  Thus (W.3) is a probabilistic logarithmic
asymptotic, not a deterministic pathwise identity.

For a precise one-time statement, let
\((L_j,R_j,t_j)\) be a sequence with

\[
 \ell_j:=\frac{t_j}{R_j^2}\longrightarrow\ell_\infty\in[64,65],
 \qquad
 \rho_*:=\liminf_{j\to\infty}
 \frac{\log(1/R_j)}{L_j^2}>q(\ell_\infty).
 \tag{W.50}
\]

Choose a fixed \(\epsilon>0\) sufficiently small that

\[
 \frac{(p+\epsilon)^2}{4\ell_\infty}
 <\min\left\{
 \rho_*,
 \frac{c_h^2}{260}\right\}.
 \tag{W.51}
\]

After discarding finitely many indices, the same two strict inequalities
hold with \(\ell_j\) and
\(\log(1/R_j)/L_j^2\).  We suppress the index \(j\) in (W.49)--(W.53).
Then

\[
 \frac{\Delta_{\epsilon,\ell}(L)}R\longrightarrow\infty.
 \tag{W.52}
\]

Because \(z>0\), (W.41) and (W.49) give, on the good event,

\[
 \Delta_{\epsilon,\ell}(L)
 \le z+\mathfrak S_t
 \le \frac{3}{64}+\frac{65}{48}
 =\frac{269}{192}<\frac32<\frac\pi2.
 \tag{W.52a}
\]

Thus \(z+\mathfrak S_t\) stays in the central horizontal chart and its
distance to \(2\pi\mathbb Z\) is at least
\(\Delta_{\epsilon,\ell}(L)\).  Periodic
Gaussian derivative bounds therefore give

\[
 \frac{
  \left|\mathbb E_{0,y}^{\rm br}
   \partial_zK_T^{\rm per}(z+\mathfrak S_t)\right|}
 {|\partial_zK_T^{\rm per}(z)|}
 \le Ce^{-c\epsilon^2L^4}
   +C\exp\!\left[-c
       \left(\frac{\Delta_{\epsilon,\ell}(L)}R\right)^2\right].
 \tag{W.53}
\]

Adding the noncentral windings through (W.25) proves a super-exponential
relative loss.  The mechanism is geometric: paths reaching the remote
height see less shear than the reference centre, hence lag by
\(\mathfrak S_t\), and the derivative lobe is centred near
\(z=-\mathfrak S_t\), not near the free interval \(z\asymp R>0\).

## 6. Direct-packet scale dichotomy

We now combine the two bridge estimates with the exact representation.

### Proposition 6.1 — relative survival

If, with the fixed constant \(C_0\) in (W.40),

\[
 \frac1{RL^2}e^{-q(\ell)L^2+C_0L}\longrightarrow0
 \tag{W.54}
\]

then

\[
 \boxed{
 \sup_{x\in\mathcal S_m}
 \left|
 \frac{G_m^+(t,x_2,x_3)}
      {H_m(t,x_2,x_3-h_m)}-1
 \right|\longrightarrow0.}
 \tag{W.55}
\]

In particular, the uniform strict condition (W.4) implies (W.55) for all
\(\ell\in[64,65]\).

**Proof.**  The periodic heat-kernel derivative bounds on the normalized
compact box give

\[
 \frac{\|\partial_z^2K_T^{\rm per}\|_\infty}
 {|\partial_zK_T^{\rm per}(z)|}\le\frac CR.
 \tag{W.56}
\]

Subtract (W.23) from (W.22), apply the mean-value theorem, and then use
(W.42).  The \(c_h^2/260\) term is smaller by (W.32), and the winding term,
after the factor \(R^{-1}\) in (W.56), is negligible by the strengthened
form of (W.25).  This proves (W.55).  Notice that the comparison
is relative to \(H_m\); no absolute error replaces it. \(\square\)

### Proposition 6.2 — relative sweeping failure

Under (W.50),

\[
 \boxed{
 \sup_{x\in\mathcal S_m}
 \left|
 \frac{G_m^+(t,x_2,x_3)}
      {H_m(t,x_2,x_3-h_m)}
 \right|\longrightarrow0.}
 \tag{W.57}
\]

The convergence beats \(e^{-CL^2}\) for every fixed \(C>0\).  Under the
uniform condition (W.5), put
\(\delta_\rho:=\liminf\log(1/R)/L^2-q_{64}>0\) and choose one
\(\epsilon>0\) such that
\((p+\epsilon)^2/256<q_{64}+\delta_\rho/2\).  Since
\((p+\epsilon)^2/(4\ell)\le(p+\epsilon)^2/256\), the same \(\epsilon\)
works for every \(\ell\in[64,65]\); hence (W.57) is uniform on the slab.

**Proof.**  Choose \(\epsilon\) as in (W.51).  Divide the exact central
term in (W.22) by the free central derivative and use (W.53).  Its first
row is \(e^{-cL^4}\); its second is doubly exponential because of (W.52).
The winding ratio (W.25) is also super-exponential on the \(L^2\) scale
under the chart bound.  Finally use (W.23) and
\(\sum_nw_n=w_0(1+o(1))\). \(\square\)

Equations (W.55) and (W.57) are mutually exclusive strict-regime results.
At a fixed \(\ell\), the sharp logarithmic threshold is \(q(\ell)\).  The
uniform slab thresholds are \(q_{65}\) for survival and \(q_{64}\) for
sweeping.

## 7. Inversion partner and the other packet after amplitudes

The direct comparison alone is insufficient because the physical first
component is

\[
 U=\mathfrak a_1G_1+\mathfrak a_2G_2,
 \qquad G_i=G_i^++G_i^-.
 \tag{W.58}
\]

Here

\[
 \frac{\mathfrak a_2}{\mathfrak a_1}
 =2^{-1/2}e^{3q_{64}L_1^2},
 \qquad
 \frac{\mathfrak a_1}{\mathfrak a_2}
 =\sqrt2e^{-3q_{64}L_1^2}.
 \tag{W.59}
\]

The exact stochastic formula followed by a supremum in the horizontal
derivative factor gives the inherited vertical estimate

\[
 |G_j^\pm(t,x)|\le CRK_{R^2+t}^{\rm per}(x_3\mp h_j).
 \tag{W.60}
\]

This estimate is insensitive to \(q_{{\rm pre},j}\) and \(Q_j(t)\), and
contains every vertical winding.

For the inversion partner of packet \(m\), comparison with (W.18) yields

\[
 \frac{|G_m^-|}{|H_m|}
 \le C\exp\!\left[-\frac5{693}L_m^2+CL_m\right]
 +Ce^{-c/R^2+CL_m^2}.
 \tag{W.61}
\]

Indeed,

\[
 \frac{(c_h+p)^2-d^2}{4a}
 =\frac{c_hp}{a}\ge\frac{c_hp}{66}=\frac5{693}.
 \tag{W.62}
\]

For the other packet there are two different geometries.  On the packet-1
remote strip, the packet-2 positive centre has separation

\[
 (2c_h-p)L_1R+O(R),
 \tag{W.63}
\]

and amplitude-weighted comparison gives

\[
 \frac{\mathfrak a_2|G_2|}{\mathfrak a_1|H_1|}
 \le C e^{-\delta_{1\leftarrow2}L_1^2+CL_1}
    +Ce^{-c/R^2+CL_1^2},
 \tag{W.64}
\]

where the exact worst-age margin is

\[
 \boxed{
 \delta_{1\leftarrow2}
 :=\frac{(2c_h-p)^2-d^2}{264}-3q_{64}
 =\frac{100043}{29804544}>0.}
 \tag{W.65}
\]

On the packet-2 remote strip, write all heights in \(L_1\)-units.  The
packet-1 positive centre has separation

\[
 (2p-c_h)L_1R+O(R)
 =\frac{79}{1008}L_1R+O(R).
 \tag{W.66}
\]

Although this is a much smaller vertical separation, the packet-1
amplitude is exponentially smaller.  The exact comparison is

\[
 \frac{\mathfrak a_1|G_1|}{\mathfrak a_2|H_2|}
 \le C e^{-\delta_{2\leftarrow1}L_1^2+CL_1}
    +Ce^{-c/R^2+CL_1^2},
 \tag{W.67}
\]

with

\[
 \boxed{
 \delta_{2\leftarrow1}
 :=3q_{64}
 -\frac{4d^2-(2p-c_h)^2}{260}
 =\frac{3667}{17611776}>0.}
 \tag{W.68}
\]

The generic periodic remainders displayed in (W.61), (W.64), and (W.67)
are also quantitatively harmless after the largest amplitude ratio.  With
\(q=q_{64}=c_\gamma/2\), the all-copy vertical estimate gives

\[
 \mathcal R_{\rm per}
 \le C\exp\!\left(qL_2^2-\frac3{22R^2}\right)
 \le Ce^{-c_*L_2^2},
 \qquad
 c_*:=\frac3{22}\left(\frac{144}{5}\right)^2-q>0.
 \tag{W.68a}
\]

Here the last inequality is exactly the chart bound
\(L_2R\le5/144\); it does not appeal to an unspecified competition
between constants.

The negative partner of the other packet is farther away and is absorbed
in the same bounds.  Consequently, after the actual amplitudes have been
inserted,

\[
 \frac{\mathfrak a_{3-m}|G_{3-m}|
       +\mathfrak a_m|G_m^-|}
      {\mathfrak a_m|H_m|}\longrightarrow0
 \tag{W.69}
\]

on either remote strip.  This is the required quantitative noncancellation
statement.  It is stronger than an unweighted absolute \(o(1)\), and the
shell weight, being common to all terms at the same point, does not alter
the ratios (W.61), (W.64), and (W.67).

## 8. Which packet survives under the frozen hypotheses

### 8.1 The outer packet survives for every R0.74U-admissible sequence

For \(m=2\), \(L_2=2L_1\).  The strict identity

\[
 4q_{65}-a_S
 =\frac{3719797}{5811886080}>0
 \tag{W.70}
\]

and the inherited reserve in (W.7) give

\[
 \begin{aligned}
 &\frac1{RL_2^2}e^{-q_{65}L_2^2+CL_2}\\
 &\quad=\frac1{L_2^2}
 \left(R^{-1}e^{-a_SL_1^2}\right)
 e^{-(4q_{65}-a_S)L_1^2+2CL_1}
 \longrightarrow0.
 \end{aligned}
 \tag{W.71}
\]

Thus Proposition 6.1 and (W.69) prove, uniformly for every admissible
\(\tau_2\),

\[
 \boxed{
 \sup_{x\in\mathcal S_2}
 \left|
 \frac{U(t,x)}{\mathfrak a_2H_2(t,x_2,x_3-h_2)}-1
 \right|\longrightarrow0.}
 \tag{W.72}
\]

This is an unconditional theorem inside the frozen R0.74V family.

### 8.2 The inner packet is not decided by the generalized hypotheses

For \(m=1\), (W.7) permits both sides of the threshold.  Polynomially small
\(R\) satisfies the relative-survival condition, while an exponential scale
with rate strictly above \(q_{64}\) satisfies the sweeping condition.  There
is therefore no theorem with one common outcome for packet (1) under
(W.7) alone.

For the original R0.74Q choice

\[
 R=e^{-\rho L_1^2},\qquad \rho=\frac1{320},
 \tag{W.73}
\]

the exact margins are

\[
 \rho-q_{64}
 =\frac{2689}{1270080}>0,
 \qquad
 q_{65}-\frac\rho4
 =\frac{13939}{66044160}>0.
 \tag{W.74}
\]

Hence packet (1) is swept from its fixed free-comparator strip, while
packet (2) survives there:

\[
 \frac{U}{\mathfrak a_1H_1}\longrightarrow0
 \quad\hbox{on }\mathcal S_1,
 \qquad
 \frac{U}{\mathfrak a_2H_2}\longrightarrow1
 \quad\hbox{on }\mathcal S_2.
 \tag{W.75}
\]

Here and only in the shorthand (W.75),
\(H_m=H_m(t,x_2,x_3-h_m)\) on \(\mathcal S_m\).
The first convergence uses (W.57), (W.61), and (W.64); the second uses
(W.55), (W.61), and (W.67).  Thus both inversion and cross-packet effects
have been compared after amplitude insertion.

## 9. Adjacent-shell weight and the proved endpoint obstruction

Let

\[
 \Gamma_m=\gamma_{k_m}=e^{-c_\gamma L_m^2},
 \qquad
 \mathfrak a_m=A_*(\Gamma_mL_m)^{-1/2},
 \qquad T_*=A_*^2R^2.
 \tag{W.76}
\]

The adjacent inward weight ratio is exact:

\[
 \frac{\gamma_{k_m-1}}{\Gamma_m}
 =e^{(3/4)c_\gamma L_m^2}.
 \tag{W.77}
\]

Whenever relative survival holds, (W.11)--(W.18), (W.69), and the
nonnegative endpoint row of the completed clock give

\[
 \begin{aligned}
 K_{k_m-1,R}(\tau_m)
 &\ge\frac{\gamma_{k_m-1}}{2R}
       \int_{\mathcal S_m}|U(\tau_m,x)|^2\,dx\\
 &\ge cT_*L_m^{-1/2}
 \exp\!\left[
  \left(\frac34c_\gamma-\frac{d^2}{2a}\right)L_m^2
  -CL_m\right].
 \end{aligned}
 \tag{W.78}
\]

Since \(a\in[65,66]\),

\[
 \frac34c_\gamma-\frac{d^2}{2a}
 \ge\chi(65)
 =\frac{12191}{132088320}>0.
 \tag{W.79}
\]

For packet \(2\), relative survival is unconditional by (W.71).  Therefore

\[
 \boxed{
 \frac{K_{k_2-1,R}(\tau_2)}{T_*}
 \ge cL_2^{-1/2}e^{\chi(65)L_2^2-CL_2}
 \longrightarrow\infty.}
 \tag{W.80}
\]

Thus the matching all-shell \(O(T_*)\) upper bound contemplated in R0.74V
is false for the frozen placement.  This conclusion needs only packet \(2\),
and it remains valid for every generalized sequence satisfying (W.7).

For comparison, in the original-scale packet-1 sweeping regime, the
packet contribution from this particular fixed strip is negligible after
the same amplitude and weight are inserted.  Indeed, the free weighted
scale grows at most like \(e^{\chi(66)L_1^2+CL_1}\), whereas (W.57) is
super-exponential and

\[
 2\delta_{1\leftarrow2}-\chi(66)
 =\frac{221281}{33530112}>0,
 \tag{W.81}
\]

with the inversion margin still larger.  Hence

\[
 \frac{\gamma_{k_1-1}}{RT_*}
 \int_{\mathcal S_1}|U(\tau_1,x)|^2\,dx\longrightarrow0
 \tag{W.82}
\]

on that scale.  Equation (W.82) is a strip statement, not a whole-shell
upper bound: the swept packet may contribute at other horizontal radii.

The obstruction (W.80) concerns the shell \(k_2-1=k_1\).  It disproves an
all-shell matching upper estimate, but a fixed-deletion functional could
delete precisely that coordinate.  Since packet (1)'s second candidate
shell can be swept away, this note does not by itself disprove every
fixed-deletion upper theorem.  The target-coordinate duration problem and
R0.74V Proposition V.1 also remain open.

## 10. Exact blocker at the transition and next analytic input

The strict regimes above leave a narrow but genuine transition issue.
For a sequence with \(\tau_m/R^2\to\ell\), the logarithmic threshold is

\[
 \frac{\log(1/R)}{L_m^2}=q(\ell)
 =\frac{p^2}{4\ell}.
 \tag{W.83}
\]

At equality, the polynomial \(L^{-2}\), the \(O(L)\) transition-layer
correction, and the detailed fixed profile \(\sigma\) determine the law of
\(\mathfrak S_t/R\).  The upper conditional moment (W.40) and the lower
high-probability estimate (W.49) deliberately do not identify that critical
law.  Closing it requires a boundary Laplace asymptotic for

\[
 B\int_0^t
 \left[A(t-s,h_m+Y_s)-A(t-s,h_m)\right]ds
 \tag{W.84}
\]

under the central bridge, including the scaled transition profile of
\(1-g_R\).  This is the exact blocker; it is not a missing absolute
near-lobe estimate.

The proved boundary is therefore:

- exact all-winding Feynman--Kac disintegration: **proved**;
- conditional remote bridge localization and sharp \(L^2\)-exponent:
  **proved**;
- relative survival below the threshold: **proved**;
- relative sweeping above the threshold: **proved**;
- inversion and other-packet noncancellation after amplitudes: **proved**;
- packet-2 adjacent-inward weighted endpoint divergence: **proved**;
- critical transition law: **open**;
- whole-shell \(H^1\), time occupation, accumulated viscosity, and fixed
  deletion: **open**;
- arbitrary suitable weak solutions or Millennium regularity: **not
  addressed; NOT CLAY**.
