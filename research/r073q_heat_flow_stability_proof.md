# R0.73Q analytic proof: a periodic \(L^4_tL^6_x\) heat-flow tube

**Status:** analytic proof passed independent readback; finite formula
certificate awaiting immutable source binding

**Dependencies:** R0.73P finite orbit actions and relative-energy theorem;
periodic heat-kernel bounds; one-dimensional Hardy--Littlewood--Sobolev;
the classical Serrin continuation criterion

## 1. Setting and theorem

Work on \(\mathbb T^3=[0,2\pi]^3\) with normalized Haar measure, viscosity
one, zero spatial mean, and the Leray projector \(P\).  Let

\[
 u\in C([0,\infty);H^3_{\sigma,0})
 \cap L^2_{\rm loc}([0,\infty);H^4_{\sigma,0})
 \tag{1.1}
\]

be an a priori global solution of the unforced incompressible
Navier--Stokes equations.  Define

\[
 E(I):=L^4(I;L^6(\mathbb T^3)),
 \qquad
 \|f\|_{\mathfrak X}:=\|e^{t\Delta}f\|_{E(0,\infty)}.
 \tag{1.2}
\]

For mean-zero periodic distributions, \(\mathfrak X\) is the heat-semigroup
realization of \(\dot B^{-1/2}_{6,4}\).

### Theorem 1.1: uniform critical heat-flow stability

There exists a number \(\rho_{\mathfrak X}[u]>0\), depending only on the
fixed reference orbit through

\[
 M[u]:=\|u\|_{E(0,\infty)},
 \tag{1.3}
\]

such that the following statement holds for every \(t_0\ge0\).  If
\(v_0\in H^3_{\sigma,0}\) and

\[
 \|v_0-u(t_0)\|_{\mathfrak X}<\rho_{\mathfrak X}[u],
 \tag{1.4}
\]

then the solution starting from \(v_0\) is a unique global strong solution

\[
 v\in C([t_0,\infty);H^3_{\sigma,0})
 \cap L^2_{\rm loc}([t_0,\infty);H^4_{\sigma,0}).
 \tag{1.5}
\]

Putting \(w(t)=v(t)-u(t)\), one also has

\[
 \|w\|_{E(t_0,\infty)}
 \le 2K[u]\|w(t_0)\|_{\mathfrak X},
 \tag{1.6}
\]

for the explicit finite inverse bound \(K[u]\) in (4.12).  Moreover, the
R0.73P relative-energy estimate gives

\[
 \|w(t)\|_2
 \le e^{\mathcal L[u]}e^{-(t-t_0)}\|w(t_0)\|_2,
 \qquad t\ge t_0.
 \tag{1.7}
\]

The same radius works at every \(t_0\); no lower bound on \(t_0\) is used.

## 2. Finiteness of the reference \(E\)-action

R0.73P proved

\[
 \mathcal A_{1/2}[u]
 :=\int_0^\infty |u(t)|_1^4\,dt<\infty.
 \tag{2.1}
\]

The normalized periodic Sobolev inequality \(\|z\|_6\le C_S|z|_1\)
therefore yields

\[
 M[u]^4
 =\int_0^\infty\|u(t)\|_6^4\,dt
 \le C_S^4\mathcal A_{1/2}[u]<\infty.
 \tag{2.2}
\]

For the translated tail \(U_{t_0}(s)=u(t_0+s)\),

\[
 \|U_{t_0}\|_{E(0,\infty)}^4
 =\int_{t_0}^\infty\|u(t)\|_6^4\,dt
 \le M[u]^4.
 \tag{2.3}
\]

This single inequality is what makes every constant below independent of the
restart time.

## 3. The periodic bilinear estimate

For causal functions define

\[
 \mathcal B(a,b)(t)
 :=\int_0^t e^{(t-s)\Delta}P\nabla\!\cdot(a\otimes b)(s)\,ds.
 \tag{3.1}
\]

### Lemma 3.1

There is a periodic constant \(C_B<\infty\) such that

\[
 \|\mathcal B(a,b)\|_{E(0,\infty)}
 \le C_B\|a\|_{E(0,\infty)}\|b\|_{E(0,\infty)}.
 \tag{3.2}
\]

The same constant works after translating time or restricting the causal
integral and the output to any interval.

### Proof

The periodic heat semigroup, the \(L^p\)-bounded Leray projector, and the
spectral gap on mean-zero fields give

\[
 \|e^{\tau\Delta}P\nabla\!\cdot F\|_6
 \le C_O k(\tau)\|F\|_3,
 \tag{3.3}
\]

where one may take

\[
 k(\tau)=\tau^{-3/4}{\bf1}_{(0,1]}(\tau)
          +e^{-c\tau}{\bf1}_{(1,\infty)}(\tau).
 \tag{3.4}
\]

For \(0<\tau\le1\), the exponent is the sum of one derivative,
\(\tau^{-1/2}\), and the \(L^3_x\to L^6_x\) heat gain,
\(\tau^{-1/4}\).  For \(\tau>1\), factor the semigroup at a fixed positive
time and use the first nonzero eigenvalue.

Set

\[
 g(s):=\|a(s)\|_6\|b(s)\|_6.
 \tag{3.5}
\]

Then \(g\in L^2(0,\infty)\) and

\[
 \|g\|_2\le\|a\|_E\|b\|_E.
 \tag{3.6}
\]

After extending \(g\) by zero to \(\mathbb R\), (3.3) gives a short-time
fractional integral plus a long-time ordinary convolution.  The
one-dimensional Hardy--Littlewood--Sobolev inequality with order \(1/4\)
gives

\[
 \left\|
  \int_0^t(t-s)^{-3/4}{\bf1}_{t-s\le1}g(s)\,ds
 \right\|_{L^4_t}
 \le C_{\rm HLS}\|g\|_2.
 \tag{3.7}
\]

For the long-time part,
\(e^{-c\tau}{\bf1}_{\tau>1}\in L^{4/3}(\mathbb R_+)\), so Young's
inequality gives the same \(L^2_t\to L^4_t\) map.  Combining these bounds
with (3.6) proves (3.2), with

\[
 C_B=C_O\left(C_{\rm HLS}
 +\|e^{-c\tau}{\bf1}_{\tau>1}\|_{4/3}\right).
 \tag{3.8}
\]

The proof is causal and invariant under time translation, which proves the
last assertion.  \(\square\)

### Endpoint warning

Replacing (3.7) by ordinary Young convolution would require
\(\tau^{-3/4}\in L^{4/3}(0,1)\), which is false by a logarithm.  The HLS
step is essential.  This also records why a naive endpoint Kato estimate
cannot simply be promoted to the \(BMO^{-1}\) setting.

## 4. Uniform inversion of the large linearized cross term

Fix \(t_0\ge0\), write \(U=U_{t_0}\), and set

\[
 \mathcal L_Uz:=\mathcal B(U,z)+\mathcal B(z,U).
 \tag{4.1}
\]

The operator norm \(2C_B\|U\|_E\) need not be less than one.  The Volterra
structure nevertheless makes \(I+\mathcal L_U\) invertible with a bound
depending only on \(M[u]\).

Choose

\[
 \varepsilon_B:={1\over4C_B}.
 \tag{4.2}
\]

Partition \([0,\infty)\) into consecutive intervals
\(I_j=[\tau_{j-1},\tau_j)\), \(1\le j\le N\), so that

\[
 \|U\|_{E(I_j)}\le\varepsilon_B,
 \qquad
 N\le N_*[u]
 :=1+\left({M[u]\over\varepsilon_B}\right)^4.
 \tag{4.3}
\]

Such a partition follows by cutting the absolutely continuous action
\(\int\|U(t)\|_6^4dt\) into pieces of size at most
\(\varepsilon_B^4\).

Consider

\[
 z+\mathcal L_Uz=f,
 \qquad f\in E(0,\infty).
 \tag{4.4}
\]

Suppose \(z\) has already been constructed on
\([0,\tau_{j-1})\).  On \(I_j\), split the causal integral into its history
and local parts.  The local equation is

\[
 (I+\mathcal L^{I_j}_{U_j})z_j=f_j-h_j,
 \tag{4.5}
\]

where \(U_j={\bf1}_{I_j}U\), \(z_j={\bf1}_{I_j}z\), and \(h_j\) is the
output on \(I_j\) generated by the already known inputs before
\(\tau_{j-1}\).  More explicitly,

\[
 h_j={\bf1}_{I_j}\bigl[
 \mathcal B(U_{<j},z_{<j})+\mathcal B(z_{<j},U_{<j})\bigr].
 \tag{4.5a}
\]

There are no mixed-time products such as \(U_jz_{<j}\), because both factors
in the Duhamel integrand are evaluated at the same integration time.
Lemma 3.1 and (4.2) give

\[
 \|\mathcal L^{I_j}_{U_j}\|_{E(I_j)\to E(I_j)}
 \le2C_B\varepsilon_B={1\over2}.
 \tag{4.6}
\]

Thus the local inverse exists and has norm at most two.  The history term
satisfies

\[
 \|h_j\|_{E(I_j)}
 \le2C_BM[u]\|z\|_{E(0,\tau_{j-1})}.
 \tag{4.7}
\]

Consequently,

\[
 \|z_j\|_{E(I_j)}
 \le2\|f_j\|_{E(I_j)}
 +4C_BM[u]\|z\|_{E(0,\tau_{j-1})}.
 \tag{4.8}
\]

Put \(Z_j=\|z\|_{E(0,\tau_j)}\).  Since the fourth-power action is
additive on disjoint intervals and \((a^4+b^4)^{1/4}\le a+b\),

\[
 Z_j\le(1+4C_BM[u])Z_{j-1}+2\|f_j\|_{E(I_j)},
 \qquad Z_0=0.
 \tag{4.9}
\]

Iteration and Hölder's inequality for the finite sequence of interval norms
give

\[
 \begin{aligned}
 Z_N
 &\le2(1+4C_BM[u])^{N-1}
       \sum_{j=1}^N\|f_j\|_{E(I_j)}\\
 &\le2N^{3/4}(1+4C_BM[u])^{N-1}\|f\|_E.
 \end{aligned}
 \tag{4.10}
\]

The same recursion with \(f=0\) proves injectivity, while the recursive
Neumann construction proves surjectivity.  Since \(N\le N_*[u]\), define

\[
 \widehat N[u]:=\max\{1,\lceil N_*[u]\rceil\}
 \tag{4.11}
\]

and

\[
 \boxed{
 K[u]
 :=2\widehat N[u]^{3/4}
 (1+4C_BM[u])^{\widehat N[u]-1}.}
 \tag{4.12}
\]

Then, for every restart time,

\[
 \|(I+\mathcal L_{U_{t_0}})^{-1}\|_{E\to E}\le K[u].
 \tag{4.13}
\]

The bound is deliberately crude but finite, explicit, and uniform in
\(t_0\).

## 5. Quadratic fixed point

Let

\[
 R_U:=(I+\mathcal L_U)^{-1},
 \qquad
 S(t):=e^{t\Delta},
 \qquad
 \delta:=\|Sw_0\|_E=\|w_0\|_{\mathfrak X}.
 \tag{5.1}
\]

The difference mild equation is equivalent to

\[
 w=R_USw_0-R_U\mathcal B(w,w)=:\Phi(w).
 \tag{5.2}
\]

Take the closed ball in \(E\) of radius

\[
 r:=2K[u]\delta.
 \tag{5.3}
\]

For \(w,z\) in this ball, Lemma 3.1 and (4.13) give

\[
 \|\Phi(w)\|_E
 \le K[u]\delta+K[u]C_Br^2,
 \tag{5.4}
\]

and

\[
 \|\Phi(w)-\Phi(z)\|_E
 \le2K[u]C_Br\|w-z\|_E.
 \tag{5.5}
\]

Define

\[
 \boxed{
 \rho_{\mathfrak X}[u]
 :={1\over8C_BK[u]^2}.}
 \tag{5.6}
\]

If \(\delta<\rho_{\mathfrak X}[u]\), then

\[
 4C_BK[u]^2\delta<{1\over2}.
 \tag{5.7}
\]

Equations (5.4)--(5.7) show that \(\Phi\) maps the ball strictly into itself
and has Lipschitz constant less than \(1/2\).  Banach's theorem produces a
global \(w\in E\) and gives (1.6).

Uniqueness in the full \(E\) mild class follows by applying the same causal
small-interval argument to the difference of two solutions, partitioning
the finite \(L^4L^6\) actions of \(U,w_1,w_2\).  This statement is used only
inside the Serrin/mild class; it is not a \(BMO^{-1}\) endpoint claim.

## 6. Strong continuation from \(H^3\) data

Assume \(w_0\in H^3_{\sigma,0}\).  Classical local theory gives an \(H^3\)
solution on a maximal interval \([t_0,T_*)\).  On every compact subinterval
it belongs to \(L^4_tL^6_x\), so the preceding \(E\)-uniqueness identifies it
with the global mild solution \(u+w\).

Moreover,

\[
 u+w\in L^4_{\rm loc}([t_0,\infty);L^6),
 \qquad {2\over4}+{3\over6}=1.
 \tag{6.1}
\]

If \(T_*<\infty\), this identification and the global bounds give the full
critical norm up to the putative endpoint:

\[
 \|v\|_{L^4((t_0,T_*);L^6)}
 \le M[u]+2K[u]\delta<\infty.
 \tag{6.2}
\]

The classical Serrin continuation criterion therefore extends the solution
past \(T_*\), a contradiction.  Thus \(T_*=\infty\), and parabolic
propagation gives (1.5).  Finally, both solutions are strong and have finite
energy, so the already proved R0.73P relative-energy inequality applies and
yields (1.7).  This completes the proof of Theorem 1.1.  \(\square\)

## 7. Relation to \(H^{1/2}\) and strictness

Let \(\Delta_j\) be a periodic dyadic decomposition.  Bernstein gives

\[
 2^{-j/2}\|\Delta_jf\|_6
 \le C\,2^{j/2}\|\Delta_jf\|_2.
 \tag{7.1}
\]

Taking the \(\ell^4_j\) norm on the left, the \(\ell^2_j\) norm on the
right, and using \(\ell^2\hookrightarrow\ell^4\), one obtains

\[
 \|f\|_{\mathfrak X}
 \le C_X|f|_{1/2}.
 \tag{7.2}
\]

Hence the heat-flow tube contains the \(H^{1/2}\)-ball of radius
\(\rho_{\mathfrak X}[u]/C_X\).  This statement does not compare that radius
numerically with the independently obtained R0.73P radius
\(R_{1/2}[u]\).

To prove strictness inside smooth data, define

\[
 w_N(x)=N^{-1/4}e_2\sin(Nx_1).
 \tag{7.3}
\]

This field is smooth, mean zero, and divergence free.  With normalized Haar
measure,

\[
 \|\sin(Nx_1)\|_2={1\over\sqrt2},
 \qquad
 \|\sin(Nx_1)\|_6=\left({5\over16}\right)^{1/6}=:c_6.
 \tag{7.4}
\]

Since \(e^{t\Delta}w_N=e^{-N^2t}w_N\),

\[
 \begin{aligned}
 \|w_N\|_{\mathfrak X}^4
 &=c_6^4N^{-1}\int_0^\infty e^{-4N^2t}\,dt\\
 &={c_6^4\over4}N^{-3},
 \end{aligned}
 \tag{7.5}
\]

and therefore

\[
 \|w_N\|_{\mathfrak X}={c_6\over4^{1/4}}N^{-3/4}\to0.
 \tag{7.6}
\]

On the other hand,

\[
 \|w_N\|_2={1\over\sqrt2}N^{-1/4}\to0,
 \qquad
 |w_N|_{1/2}={1\over\sqrt2}N^{1/4}\to\infty.
 \tag{7.7}
\]

Also \((w_N\cdot\nabla)w_N=0\), although the proof of Theorem 1.1 does not
use this cancellation and does control its cross interaction with the
arbitrary fixed orbit \(u\).

Given any \(R>0\) and \(H>0\), (7.6)--(7.7) provide an integer \(N\) for
which

\[
 \|w_N\|_{\mathfrak X}<R,
 \qquad
 |w_N|_{1/2}>H.
 \tag{7.8}
\]

Taking \(R=\rho_{\mathfrak X}[u]\) proves that the heat-flow tube reaches
outside every fixed \(H^{1/2}\)-ball.  To state strict set inclusion without
silently ordering two unrelated radii, define

\[
 \mathcal D_Q[u]
 :=\{f:|f|_{1/2}<R_{1/2}[u]\}
 \cup\{f:\|f\|_{\mathfrak X}<\rho_{\mathfrak X}[u]\}.
 \tag{7.9}
\]

Both pieces are stable by R0.73P and Theorem 1.1, respectively, and (7.8)
gives

\[
 \mathcal D_Q[u]
 \supsetneq\{f:|f|_{1/2}<R_{1/2}[u]\}.
 \tag{7.10}
\]

This does not prove an unrestricted \(L^2\)-only theorem: (7.8) certifies one
controlled heat-flow geometry, while arbitrary \(L^2\) data need not have
small \(\mathfrak X\)-norm.

## 8. Literature boundary

The whole-space analogue of the finite-index stability mechanism is already
present in Gallagher--Iftimie--Planchon, Theorem 3.1, for global solutions in
critical Besov spaces.  The Auscher--Dubois--Tchamitchian publisher abstract
reports whole-space \(BMO^{-1}\)-topology openness for the corresponding
global Cauchy-data set; no unavailable theorem formula or uniqueness class is
imported.  These are collision sources, not periodic black boxes used in
Sections 2--7.

The endpoint boundary is now especially important: Coiculescu--Palasek
construct \(BMO^{-1}(\mathbb T^3)\) initial data giving two distinct global
solutions smooth for every positive time.  R0.73Q therefore stops at the
finite-index \(\dot B^{-1/2}_{6,4}\) Serrin/mild class and makes no
nonperturbative-endpoint uniqueness assertion.

## 9. What is new in this release and what is not

The self-contained result proved here is the fixed-torus, uniform-in-restart
corollary for one given global \(H^3\) orbit, with a concrete heat norm, an
explicit finite inverse recursion, and an exact smooth strictness sequence.
The bilinear estimate, critical Besov small-data mechanism, Serrin
continuation, and whole-space openness results are classical ingredients.

Accordingly, Theorem 1.1 is not a new solution of the global-regularity
problem, not a new \(BMO^{-1}\) theorem, and not evidence for regularity from
arbitrary \(L^2\)-small data.  Its value is to close a precise entrance that
R0.73P left open: some perturbations can be simultaneously small in
\(L^2\) and in the heat-flow trace, arbitrarily large in \(H^{1/2}\), and
still lie in one all-time strong stability tube about the fixed orbit.
