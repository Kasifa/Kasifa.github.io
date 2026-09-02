# R0.74Q, Step 2 — relaxed multipacket geometry and the cubic-payment obstruction

## 0. Status and exact claim boundary

Step 1 showed that finitely many passive packets may be re-evolved under one
common heat shear to give an exact smooth periodic Navier--Stokes solution,
but that the old frozen terminal-angle calibration cannot be shared across
two dyadic shells.  This note tests the relaxed calibration left open in
R0.74Q (Q.62)--(Q.63).

The result has two distinct parts.

1. **Geometry passes.**  An explicit family with
   \(N=\lfloor\log _2L\rfloor\to\infty\) has one common shear, one common
   terminal interval, uniform packet survival, and \(N\) terminal lobes in
   \(N\) distinct physical shells.  For equal-target amplitudes, the full
   amplitude-weighted packet sum is dominated by the intended packet on
   every target lobe.  Thus the no-cancellation hypothesis in Step 1,
   Proposition 7.2, is proved for this family.
2. **The intended low-payment scaling fails.**  If every target shell is
   assigned the same terminal scale \(T\), the outermost lobe alone forces
   the complete Version-M payment to satisfy

   \[
    \frac{(P_R^{M,(N)})^{2/3}}{NT}\longrightarrow\infty.
   \tag{Q.100}
   \]

The terminal clock lower bounds proved here do **not** establish a signed
cumulative-flux estimate of order \(NT\), and they do not give the matching
all-shell upper bound
\(Y_{2,R}^{\rm sf}\lesssim\sqrt N\,T\).  Consequently, (Q.100) closes the
canonical equal-target, low-payment stress test; it does not prove the
fixed-scale inequality (Q.1), an effective-shell theorem for arbitrary
suitable weak solutions, regularity, blow-up, or the Millennium problem.
**NOT CLAY.**

No simulation, numerical fit, or asymptotic floating-point calculation is
used.

<!-- R074Q_STEP2_STATUS_GEOMETRY_PROVED -->
<!-- R074Q_STEP2_STATUS_CUBIC_PAYMENT_PROVED -->
<!-- R074Q_STEP2_STATUS_SIGNED_FLUX_OPEN -->

## 1. The explicit relaxed common-shear family

Retain the rational constants

\[
 \lambda=\frac{63}{32},\qquad
 c_h=\frac{15}{16},\qquad
 \alpha=\frac{14}{15},\qquad
 q_*=\frac12,
\tag{Q.101}
\]

\[
 \rho=\frac1{320},\qquad
 a_D=\frac{49}{14625},\qquad
 a_S=\frac{75}{22528},\qquad
 c_\gamma=\frac8{3969}.
\tag{Q.102}
\]

For an integer \(j\to\infty\), set

\[
 L=\lambda2^j,\qquad
 R=e^{-\rho L^2},\qquad
 N=\lfloor\log _2L\rfloor,
\tag{Q.103}
\]

and, for \(1\le\ell\le N\),

\[
 L_\ell=2^{\ell-1}L,\qquad
 k_\ell=j+\ell-1,\qquad
 h_\ell=c_hL_\ell R.
\tag{Q.104}
\]

Since \(1<\lambda<2\), one has \(N=j\) exactly.  Therefore

\[
 \boxed{
 L_N=\frac{L^2}{2\lambda}=\frac{16}{63}L^2,}
 \qquad
 \frac{L^2}{4}<L_N\le\frac{L^2}{2}.
\tag{Q.105}
\]

In particular,

\[
 L_NR\le\frac12L^2e^{-\rho L^2}\longrightarrow0.
\tag{Q.106}
\]

Use the saturation shear from Step 1,

\[
 g_R(x_3)=\sigma\!\left(\frac{\sin x_3}{16R}\right),
 \qquad
 \theta_R(t,x_3)=e^{t\partial_3^2}g_R(x_3),
\tag{Q.107}
\]

where \(\sigma\in C^\infty(\mathbb R;[-1,1])\) is odd and equals
\(\operatorname {sgn}s\) for \(|s|\ge1\).  Define

\[
 D_\ell=\int_{R^2}^{65R^2}\theta_R(t,h_\ell)\,dt,
 \qquad
 B=\frac{q_*}{D_1},
 \qquad
 b(t,x_3)=B\theta_R(t,x_3),
\tag{Q.108}
\]

and use the relaxed horizontal calibration

\[
 q_\ell=BD_\ell-q_*,
\tag{Q.109}
\]

\[
 q_{{\rm pre},\ell}
 =-q_*-B\int_0^{R^2}\theta_R(t,h_\ell)\,dt,
 \qquad
 Q_\ell(t)
 =q_{{\rm pre},\ell}
  +B\int_0^t\theta_R(s,h_\ell)\,ds.
\tag{Q.110}
\]

These definitions give the exact identities

\[
 Q_\ell(R^2)=-q_*,
 \qquad
 Q_\ell(65R^2)=q_\ell.
\tag{Q.111}
\]

Let \(K_t=K_t^{\rm per}\) be the one-dimensional periodic heat kernel and
put

\[
\begin{aligned}
 G_{\ell,0}^+(x_2,x_3)
 &=R^3\partial_2K_{R^2}(x_2-q_{{\rm pre},\ell})
       K_{R^2}(x_3-h_\ell),\\
 G_{\ell,0}^-(x_2,x_3)
 &=R^3\partial_2K_{R^2}(x_2+q_{{\rm pre},\ell})
       K_{R^2}(x_3+h_\ell).
\end{aligned}
\tag{Q.112}
\]

Re-evolve every packet under the same shear:

\[
 (\partial_t+b\partial_2-\Delta_{23})G_\ell^\pm=0,
 \qquad G_\ell^\pm(0)=G_{\ell,0}^\pm,
 \qquad G_\ell=G_\ell^++G_\ell^-.
\tag{Q.113}
\]

Define the target-shell weight and the equal-target amplitude by

\[
 \Gamma_\ell=\gamma_{k_\ell}
 =e^{-c_\gamma L_\ell^2},
 \qquad
 \mathfrak a_\ell
 =A_*(\Gamma_\ell L_\ell)^{-1/2},
 \qquad A_*=A_*(L)>0.
\tag{Q.114}
\]

Finally set

\[
 U_N=\sum_{\ell=1}^N\mathfrak a_\ell G_\ell,
 \qquad
 u^{(N)}=(U_N,b,0),
 \qquad p^{(N)}=0.
\tag{Q.115}
\]

For every \(j\), this is a finite sum.  Step 1, Proposition 1.1, therefore
applies verbatim: (Q.115) is an exact smooth periodic mean-zero unforced
Navier--Stokes solution.  Full inversion oddness and the even frozen
mollifier give

\[
 X_R=a_R=a_R'=0.
\tag{Q.116}
\]

The scale assigned to each target packet is independent of \(\ell\):

\[
 \boxed{
 T:=\Gamma_\ell\mathfrak a_\ell^2L_\ell R^2
   =A_*^2R^2.}
\tag{Q.117}
\]

The common factor \(A_*\) may depend on \(L\).  It cancels from every
amplitude ratio and from the normalized conclusion (Q.100).

## 2. Uniform relaxed calibration, survival, and annular placement

### 2.1 Calibration and terminal paths

The two-parameter platform lemma, Step 1 (Q.48a)--(Q.49), applies uniformly
to every \(L_\ell\), because \(L_\ell\ge L\) and (Q.106) places even the
outermost height in the central chart.  Write

\[
 D_\ell=64R^2-\delta_\ell.
\tag{Q.118}
\]

Then

\[
 0\le\delta_\ell
 \le256R^2e^{-a_DL_\ell^2}.
\tag{Q.119}
\]

Consequently,

\[
 B=\frac1{128R^2}
   \left(1+O(e^{-a_DL^2})\right),
 \qquad
 q_1=0,
\tag{Q.120}
\]

and, without assuming any unproved monotonicity of \(D_R(h)\),

\[
 \sup_{1\le\ell\le N}|q_\ell|
 \le Ce^{-a_DL^2}.
\tag{Q.121}
\]

The exact exponent reserve is

\[
 a_D-\rho
 =\frac{211}{936000}>0.
\tag{Q.122}
\]

Hence

\[
 \sup_{1\le\ell\le N}\frac{|q_\ell|}{R}
 \le Ce^{-(a_D-\rho)L^2}
 \longrightarrow0.
\tag{Q.123}
\]

Set

\[
 t_0=65R^2,
 \qquad
 J=(t_0-R^3,t_0).
\tag{Q.124}
\]

Since \(BR^2\to1/128\), for all sufficiently large \(j\), uniformly in
\(\ell\) and \(t\in J\),

\[
 |Q_\ell(t)-q_\ell|
 \le B(t_0-t)
 \le BR^3
 \le\frac R{64}.
\tag{Q.125}
\]

Thus all packets use the same terminal interval.

### 2.2 Uniform bridge survival

The R0.74F all-winding Brownian-bridge proof depends on the packet index
only through the positive-platform and vertical-separation estimates.  The
horizontal translations in (Q.110)--(Q.112) commute with (Q.113).  Applying
that proof with \(L_\ell\) in place of \(L\), and using Step 1's
two-parameter platform lemma, is uniform because
\[
 \frac{R^{-1}}{L_N}
 =\frac{e^{\rho L^2}}{L_N}\longrightarrow\infty.
\]
In particular, the inherited comparison \(R^{-1}\ge L_\ell\) holds for
every \(\ell\le N\) once \(j\) is large.  The bridge proof then gives the
uniform error majorant

\[
 E_\ell
 \le\frac C R
 \left(e^{-a_DL_\ell^2}+e^{-a_SL_\ell^2}\right)
 +Ce^{-c/R^2}.
\tag{Q.126}
\]

Here \(C,c>0\) are independent of \(j,N,\ell\).  The second exact reserve is

\[
 a_S-\rho
 =\frac{23}{112640}>0.
\tag{Q.127}
\]

It follows that

\[
 \sup_{1\le\ell\le N}E_\ell
 \le C e^{-(a_S-\rho)L^2}
    +Ce^{-ce^{2\rho L^2}}
 \longrightarrow0.
\tag{Q.128}
\]

Therefore there are fixed \(c_0>0\) and \(j_0\) such that, for all
\(j\ge j_0\), all \(1\le\ell\le N\), and all

\[
 t\in J,\qquad
 \frac54R<x_2-Q_\ell(t)<\frac32R,\qquad
 |x_3-h_\ell|<R,
\tag{Q.129}
\]

the direct positive packet has one fixed sign and

\[
 |G_\ell^+(t,x_2,x_3)|\ge2c_0.
\tag{Q.130}
\]

This is a reuse of the already proved periodic bridge theorem with a
uniform parameter substitution, not a new stochastic assumption.

### 2.3 One lobe in each of \(N\) distinct shells

Put \(r_\ell=L_\ell R\) and define

\[
\begin{aligned}
 \Omega_{\ell,+}(t)
 :=\{x\in\mathbb T^3:
 &|x_1|<r_\ell/16,\\
 &5R/4<x_2-Q_\ell(t)<3R/2,\\
 &|x_3-h_\ell|<R\},
 \qquad
 \Omega_{\ell,-}(t)=-\Omega_{\ell,+}(t).
\end{aligned}
\tag{Q.131}
\]

Because

\[
 2^{k_\ell}R=\frac{r_\ell}{\lambda},
 \qquad
 2^{k_\ell+1}R=\frac{2r_\ell}{\lambda},
\tag{Q.132}
\]

the inner annular inequality follows, uniformly for large \(j\), from

\[
 |x|\ge|x_3|
 \ge r_\ell\left(c_h-\frac1{L_\ell}\right)
 >\frac{r_\ell}{\lambda}.
\tag{Q.133}
\]

Equations (Q.123) and (Q.125) give \(|x_2|\le2R\).  The outer inequality is
therefore controlled by

\[
 \frac{|x|^2}{r_\ell^2}
 \le\frac1{256}
    +\left(c_h+\frac1{L_\ell}\right)^2
    +\frac4{L_\ell^2}.
\tag{Q.134}
\]

The right side decreases with \(L_\ell\) and has the strict limiting
margin

\[
 c_h^2+\frac1{256}
 =\frac{113}{128}
 <\left(\frac{64}{63}\right)^2
 =\left(\frac2\lambda\right)^2.
\tag{Q.135}
\]

Thus, after increasing \(j_0\) once,

\[
 \boxed{
 \Omega_{\ell,\pm}(t)\subset A_{k_\ell}(R)}
\tag{Q.136}
\]

for every \(j\ge j_0\), every \(\ell\le N\), and every \(t\in J\).  All
annular margins are uniform in \(N\).

## 3. Amplitude-weighted all-packet dominance

Section 2 controls each target packet separately.  This section proves that
the other \(N-1\) packets cannot cancel it after the exponentially growing
equal-target amplitudes (Q.114) are inserted.

Set

\[
 a_\times=\frac{\alpha^2}{264}=\frac{49}{14850},
 \qquad
 q=\frac{c_\gamma}{2}=\frac4{3969}.
\tag{Q.137}
\]

### Lemma 3.1 — uniform vertical packet tails

For \(0\le t\le65R^2\), the stochastic representation of (Q.113), followed
by the uniform bound on the horizontal derivative kernel, gives

\[
 |G_m^\pm(t,x)|
 \le CRK_{R^2+t}^{\rm per}(x_3\mp h_m).
\tag{Q.138}
\]

Indeed, the vertical stochastic coordinate is ordinary Brownian motion,
while the shear changes only the horizontal coordinate.  Taking the
horizontal factor in (Q.112) in \(L^\infty\) leaves \(CR\), and the
semigroup law convolves its vertical heat kernel to \(K_{R^2+t}^{\rm per}\).

On the positive \(\ell\)-th lobe, \(|x_3-h_\ell|<R\).  Since

\[
 c_h|L_m-L_\ell|-1
 \ge\alpha|L_m-L_\ell|
\tag{Q.139}
\]

for \(m\ne\ell\) and all sufficiently large \(L\), (Q.138) and
\(4(R^2+t)\le264R^2\) yield

\[
 |G_m^+|
 \le C e^{-a_\times(L_m-L_\ell)^2}
      +Ce^{-3/(22R^2)},
\tag{Q.140}
\]

\[
 |G_m^-|
 \le C e^{-a_\times(L_m+L_\ell)^2}
      +Ce^{-3/(22R^2)}.
\tag{Q.141}
\]

The same calculation with \(m=\ell\) gives

\[
 |G_\ell^-|
 \le Ce^{-4a_\times L_\ell^2}
      +Ce^{-3/(22R^2)}.
\tag{Q.142}
\]

The constant \(3/22\) comes from the nonzero vertical windings: the lifted
central-chart reserve is
\[
 2h_N+R
 \le2c_h\frac5{144}+\frac1{32}
 =\frac{37}{384}<\frac1{10}.
\]
Thus their distance is at least \(6|n|\), while the Gaussian denominator is
at most \(264R^2\).  Equations (Q.130) and (Q.142) imply, uniformly on every target
lobe,

\[
 |G_\ell|\ge c_0
\tag{Q.143}
\]

for all sufficiently large \(j\).  Negative lobes obey the same bounds by
full inversion parity.

### Lemma 3.2 — outer packets cannot cancel an inner target

Let \(m=\ell+d>\ell\), \(r=2^d\ge2\), and \(x=L_\ell\).  The direct-packet
part of the relative tail is

\[
 \frac{\mathfrak a_m}{\mathfrak a_\ell}
 e^{-a_\times(L_m-L_\ell)^2}
 =r^{-1/2}e^{-\Phi(r)x^2},
\tag{Q.144}
\]

where

\[
 \Phi(r)=a_\times(r-1)^2-q(r^2-1).
\tag{Q.145}
\]

The adjacent outer packet is the worst case.  Its exact exponent margin is

\[
 \boxed{
 \delta_\times
 =a_\times-3q
 =a_\times-\frac32c_\gamma
 =\frac{67}{242550}>0.}
\tag{Q.146}
\]

For every \(r\ge2\),

\[
 \Phi(r)-\delta_\times(r-1)^2
 =2q(r-1)(r-2)\ge0.
\tag{Q.147}
\]

The geometric dyadic sum is therefore bounded by

\[
 \sum_{m>\ell}
 \frac{\mathfrak a_m|G_m|}
      {\mathfrak a_\ell|G_\ell|}
 \le C_{c_0}e^{-\delta_\times L_\ell^2}
     +\mathcal R_{\rm per}.
\tag{Q.148}
\]

The negative partners have strictly larger vertical separation and are
absorbed in the same bound.

### Lemma 3.3 — inner packets cannot cancel an outer target

Let \(m=\ell-d<\ell\), \(s=2^{-d}\), and \(x=L_\ell\).  Then

\[
 \frac{\mathfrak a_m}{\mathfrak a_\ell}
 e^{-a_\times(L_\ell-L_m)^2}
 =2^{d/2}e^{-\psi_d x^2},
\tag{Q.149}
\]

where

\[
 \psi_d
 =a_\times(1-2^{-d})^2+q(1-4^{-d}).
\tag{Q.150}
\]

The adjacent inner exponent is

\[
 \mu_{\rm in}
 =\frac14a_\times+\frac34q
 =\frac{4601}{2910600}>0.
\tag{Q.151}
\]

Moreover,

\[
 \psi_{d+1}-\psi_d
 \ge\frac{5a_\times}{8}2^{-d}.
\tag{Q.152}
\]

Since \(2^{-d}x=L_m\ge L\), consecutive terms after the adjacent one have
ratio at most
\(\sqrt2\exp[-(5a_\times/8)xL]\), which is below \(1/2\) for large \(L\).
Thus

\[
 \sum_{m<\ell}
 \frac{\mathfrak a_m|G_m|}
      {\mathfrak a_\ell|G_\ell|}
 \le C_{c_0}e^{-\mu_{\rm in}L_\ell^2}
     +\mathcal R_{\rm per}.
\tag{Q.153}
\]

### Lemma 3.4 — periodic remainders remain negligible

The exact ratio identity is
\[
 \frac{\mathfrak a_m}{\mathfrak a_\ell}
 =\sqrt{\frac{L_\ell}{L_m}}\,
  e^{q(L_m^2-L_\ell^2)}.
\]
For \(m>\ell\), it is at most \(e^{qL_N^2}\).  For \(m<\ell\), it is at
most one once \(L\) is large, because
\(x^{-1/2}e^{qx^2}\) is then increasing.  All amplitude ratios and the
number of packets therefore give the coarse uniform bound

\[
 \mathcal R_{\rm per}
 \le CN\exp\!\left(qL_N^2-\frac3{22R^2}\right).
\tag{Q.154}
\]

The exact relations (Q.103), (Q.105), and (Q.137) give

\[
 qL_N^2=\frac{1024}{15752961}L^4,
 \qquad
 R^{-2}=e^{L^2/160}.
\tag{Q.155}
\]

Hence

\[
 \mathcal R_{\rm per}
 \le CN\exp\!\left[
   \frac{1024}{15752961}L^4
   -\frac3{22}e^{L^2/160}
 \right]
 \longrightarrow0.
\tag{Q.156}
\]

### Proposition 3.5 — uniform all-lobe dominance

There is a deterministic \(\varepsilon_L\to0\), independent of
\(A_*,N,\ell\), such that

\[
\begin{aligned}
 &\sup_{1\le\ell\le N}
  \sup_{t\in J}
  \sup_{x\in\Omega_{\ell,+}(t)\cup\Omega_{\ell,-}(t)}
 \frac{\sum_{m\ne\ell}|\mathfrak a_mG_m(t,x)|}
      {|\mathfrak a_\ell G_\ell(t,x)|}\\
 &\qquad\le\varepsilon_L,
\end{aligned}
\tag{Q.157}
\]

with the explicit majorant

\[
 \varepsilon_L
 \le C\left[
 e^{-\frac{67}{242550}L^2}
 +e^{-\frac{4601}{2910600}L^2}
 +N\exp\!\left(
   \frac{1024}{15752961}L^4
   -\frac3{22}e^{L^2/160}
  \right)
 \right].
\tag{Q.158}
\]

In particular, for all sufficiently large \(j\),

\[
 \sum_{m\ne\ell}|\mathfrak a_mG_m|
 \le\frac12|\mathfrak a_\ell G_\ell|,
\tag{Q.159}
\]

and therefore

\[
 \boxed{
 |U_N|\ge\frac12|\mathfrak a_\ell G_\ell|
 \ge\frac{c_0}{2}\mathfrak a_\ell}
\tag{Q.160}
\]

throughout every target lobe.  This removes the no-cancellation premise of
Step 1, Proposition 7.2, for the explicit family (Q.103)--(Q.115).

## 4. What the terminal clocks do prove

Let \(\eta_R\), \(\Psi_k^R\), and \(K_{k,R}\) be the frozen cutoff and
defect-completed clock of R0.74P (2.6)--(2.10), with terminal time
\(t_0=65R^2\).  The solution is smooth, so the total dissipation measure is
\(|\nabla u^{(N)}|^2\,dx\,dt\).  The cutoff satisfies \(\eta_R=1\) on
\(I_R=(t_0-R^2,t_0)\), and \(J\subset I_R\).

For any \(\tau\in J\), (Q.136) and the defining cutoff property give
\(\Psi_{k_\ell}^R=1\) on \(\Omega_{\ell,+}(\tau)\).  Since the dissipation
part of the clock is nonnegative, (Q.160) gives

\[
\begin{aligned}
 K_{k_\ell,R}(\tau)
 &\ge\frac{\Gamma_\ell}{2R}
       \int_{\Omega_{\ell,+}(\tau)}|u^{(N)}(\tau,x)|^2\,dx\\
 &\ge c\Gamma_\ell\mathfrak a_\ell^2L_\ell R^2.
\end{aligned}
\tag{Q.161}
\]

Here

\[
 |\Omega_{\ell,+}(t)|=\frac1{16}L_\ell R^3.
\tag{Q.162}
\]

Using (Q.117), one obtains the simultaneous terminal lower bounds

\[
 \boxed{
 K_{k_\ell,R}(\tau)\ge c_KT,
 \qquad 1\le\ell\le N,}
\tag{Q.163}
\]

where \(c_K>0\) is independent of \(j,N,\ell,A_*\).  Because the target
indices are distinct and
\(v_{k,R}=\operatorname {Var}^+K_{k,R}\ge K_{k,R}(\tau)\), this proves only
the lower bound

\[
 \boxed{
 Y_{2,R}^{\rm sf}\ge c_K\sqrt N\,T.}
\tag{Q.164}
\]

It does not prove the matching upper bound.  Off-target shell clocks,
quadratic cross terms, and positive variation accumulated before \(J\)
remain uncontrolled at that level.

## 5. The outermost lobe forces supercritical cubic payment

Let \(P_R^{M,(N)}\) be the complete Version-M payment in Step 1 (Q.74),
equivalently R0.74E (3.10), for the exact solution (Q.115).  Its nonnegative
exterior velocity-cubic row at radius \(2R\) is

\[
 \mathcal G_u^{(N)}
 =(2R)^{-2}\int_{I_{2R}}\!\int_{\mathbb T^3}
 W_{2R}(x)|u^{(N)}(t,x)|^3\,dx\,dt.
\tag{Q.165}
\]

The outermost lobe lies in

\[
 A_{k_N}(R)=A_{k_N-1}(2R).
\tag{Q.166}
\]

The exact payment weight on that annulus is therefore

\[
 \gamma_{k_N-1}
 =e^{-(c_\gamma/4)L_N^2}
 =\Gamma_N^{1/4}.
\tag{Q.167}
\]

Since \(J\subset I_{2R}\), (Q.160)--(Q.162), applied to the outermost lobe,
give

\[
\begin{aligned}
 P_R^{M,(N)}
 &\ge\mathcal G_u^{(N)}\\
 &\ge c\mathfrak a_N^3\Gamma_N^{1/4}L_NR^4\\
 &=cA_*^3R^4\Gamma_N^{-5/4}L_N^{-1/2}.
\end{aligned}
\tag{Q.168}
\]

Taking the \(2/3\) power and dividing by \(NT=NA_*^2R^2\) yields

\[
 \boxed{
 \frac{(P_R^{M,(N)})^{2/3}}{NT}
 \ge\frac cN R^{2/3}L_N^{-1/3}
       e^{(5/6)c_\gamma L_N^2}.}
\tag{Q.169}
\]

The amplitude \(A_*\) cancels exactly.  By (Q.103) and (Q.105),

\[
\begin{aligned}
 \log\frac{(P_R^{M,(N)})^{2/3}}{NT}
 \ge{}&
 \frac{5c_\gamma}{6}L_N^2
 -\frac{2\rho}{3}L^2
 -\frac13\log L_N
 -\log N-O(1)\\
 \ge{}&
 \frac{5c_\gamma}{96}L^4
 -\frac1{480}L^2
 -\frac23\log L
 -O(\log\log L).
\end{aligned}
\tag{Q.170}
\]

The leading coefficient is the positive rational number

\[
 \frac{5c_\gamma}{96}=\frac5{47628}>0.
\tag{Q.171}
\]

Thus the right side of (Q.170) tends to \(+\infty\), proving (Q.100).
Using the exact identity \(L_N=(16/63)L^2\) gives the slightly stronger
leading coefficient \(5120/47258883\); the coarser rational lower bound in
(Q.170) is sufficient.

The inherited inner bridge reserve remains valid simultaneously, because

\[
 R^{-1}e^{-a_SL^2}
 =e^{-(a_S-\rho)L^2}\longrightarrow0.
\tag{Q.172}
\]

Hence the divergence in (Q.100) is not caused by loss of packet survival.
It is forced by the combination of the outer physical-shell weight and the
equal-target amplitude.

For comparison, the adjacent-two-shell exponent conflict inherited from
Step 1, rather than the actual outermost \(L_N\sim L^2\) exponent of the
present construction, is measured by

\[
 5c_\gamma-a_S
 =\frac{603445}{89413632}>0.
\tag{Q.173}
\]

## 6. Why this does not yet give signed flux

Equation (Q.163) implies

\[
 \sum_{\ell=1}^NK_{k_\ell,R}(\tau)\ge c_KNT.
\tag{Q.174}
\]

However, the exact shell balance is

\[
 K_{k,R}=Q_{k,R}+F_{k,R}.
\tag{Q.175}
\]

The inherited absolute ledger controls the sum of the cutoff-source terms
only by

\[
 \sum_k\operatorname {TV}Q_{k,R}
 \le C(P_R^{M,(N)})^{2/3}.
\tag{Q.176}
\]

Consequently the presently available lower estimate is merely

\[
 \sum_kF_{k,R}(\tau)
 \ge c_KNT-C(P_R^{M,(N)})^{2/3}.
\tag{Q.177}
\]

Equation (Q.100) makes the error on the right much larger than \(NT\), so
(Q.177) has no positive content.  It would be circular to claim from the
terminal clock lower bound that

\[
 \mathfrak C_R^{M,(N)}\asymp NT.
\tag{Q.178}
\]

Statement (Q.178) remains **OPEN** for this family.  Conditionally, if a
separate signed-flux analysis established (Q.178), then (Q.100) would imply

\[
 \frac{(P_R^{M,(N)})^{2/3}}
      {\mathfrak C_R^{M,(N)}}\longrightarrow\infty,
\tag{Q.179}
\]

so this equal-target family could not refute (Q.1).  The conditional sentence
is not used in the proved route-closing statement.

## 7. Decision after Step 2

The relaxed common-shear route passes more of the construction than the
frozen-angle route:

1. the common-shear PDE is exact for every finite \(N\);
2. \(N\to\infty\) target lobes fit simultaneously in distinct physical
   shells;
3. the bridge, inversion, and all periodic-copy estimates are uniform in
   \(N\);
4. equal-target amplitudes preserve pointwise target dominance on every
   lobe;
5. every target clock has a simultaneous terminal lower bound of order
   \(T\).

The same equal-target normalization then forces the outer velocity-cubic
payment to exceed the total terminal target scale after the \(2/3\) power by
an exponentially diverging factor.  Therefore this explicit architecture
cannot realize the intended low-payment condition

\[
 (P_R^{M,(N)})^{2/3}=o(NT).
\tag{Q.180}
\]

This is a quantitative obstruction for one canonical smooth stress-test
architecture.  It is not a theorem that every common-shear family fails,
and it does not exclude a different amplitude distribution, time schedule,
shear profile, packet geometry, or a direct PDE estimate for arbitrary
suitable weak solutions.

The next mathematically justified branch is no longer to add more identical
equal-target packets.  It is to ask whether the convex exterior payment can
be linked directly to the number and strength of effective terminal shells,
with all off-target clocks and signed source terms retained.  That is a new
estimate, not a consequence asserted in this note.

## 8. Claim matrix and source ledger

| Statement | Status | Evidence | Boundary |
|---|---|---|---|
| Exact \(N\)-packet common-shear NSE family | INHERITED / PROVED | Step 1, Proposition 1.1; (Q.107)--(Q.116) | Finite \(N\) for each \(j\) |
| Uniform relaxed calibration and terminal paths | PROVED | (Q.118)--(Q.125) | No sign claim for \(q_\ell\) |
| Uniform all-winding bridge survival | INHERITED + PARAMETER-CLOSED | (Q.126)--(Q.130); R0.74F bridge theorem; Step 1 platform lemma | Uses the stated saturation shear |
| \(N\) distinct terminal shell lobes | PROVED | (Q.131)--(Q.136) | Explicit geometry only |
| Amplitude-weighted all-lobe dominance | PROVED | Lemmas 3.1--3.4 and Proposition 3.5 | Equal-target amplitudes (Q.114) |
| \(K_{k_\ell,R}(\tau)\gtrsim T\) for all targets | PROVED | (Q.161)--(Q.163) | Terminal lower bound only |
| \(Y_{2,R}^{\rm sf}\gtrsim\sqrt N\,T\) | PROVED | (Q.164) | Matching upper bound open |
| \((P_R^{M,(N)})^{2/3}/(NT)\to\infty\) | PROVED | (Q.165)--(Q.173) | Explicit equal-target family |
| \(\mathfrak C_R^{M,(N)}\asymp NT\) | OPEN | (Q.174)--(Q.178) | Cannot be inferred from terminal clocks |
| Fixed-scale inequality (Q.1) | OPEN | Not decided here | No regularity or Clay claim |

The inherited inputs are located in the following frozen notes.

- R0.74F: exact all-winding Brownian-bridge identity, packet survival,
  inversion suppression, and periodic-copy estimates.
- R0.74E: physical-shell weights, central and exterior payment definitions,
  and the Version-M fixed-scale question.
- R0.74P: defect-completed shell clock, positive variation, and absolute
  cutoff-source ledger.
- R0.74Q, Step 1: exact finite-\(N\) common-shear superposition and the
  two-parameter saturation-platform lemma.

The accompanying finite certificate checks the exact rational constants,
the source-text bindings, and deterministic report generation.  It does not
replace the stochastic representation, bridge argument, annular geometry,
all-packet estimates, terminal-clock proof, or payment lower bound.

<!-- R074Q_STEP2_END -->
