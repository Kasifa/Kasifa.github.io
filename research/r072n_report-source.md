# R0.72N -- the dissipative action route is unsafe, but the true cubic is sublinear

**Date:** 2026-08-27

**Status:** a proof-grade one-carrier theorem inside the fixed-band,
row-aligned triangular class inherited from R0.72L--M.  The diagonal heat
operator lowers the actual enstrophy contrast to at most order
\(\sigma^{2/3}\), but the critical-log action already receives an
order-\(\sigma^{-2/3}\log\sigma\) contribution from the first coupling
layer.  After the physical lift, the exact R0.72M scalar screen is therefore
of order \(\sigma^{1/3}\), not a safety term.  Thus the action-poor route is
false for this launch.  A time-dependent nondegenerate-shear
enhanced-dissipation theorem nevertheless gives the true cubic bound
\(\mathcal C_{\rm diss}\lesssim a^2\sigma^{1/2}\).  The direct cubic route
is therefore sublinear in this one-carrier class, although the numerically
suggested logarithmic law remains unproved.

**Keywords:** Navier--Stokes regularity, triangular 2.5D flow, dissipative
Fourier chain, enstrophy moment, critical-log action, enhanced dissipation,
phase mixing, scalar danger window

---

## 0. Direct decision

Let \(f^\sigma=(f_n^\sigma)_{n\in\mathbb Z}\) solve the complete dissipative
one-carrier chain

\[
 \partial_y f_n^\sigma
 =-n^2f_n^\sigma+\sigma e^{-y}
 (f_{n-1}^\sigma-f_{n+1}^\sigma),
 \qquad 0\le y\le1,
 \tag{0.1}
\]

with the row-aligned launch

\[
 f_1^\sigma(0)=2^{-1/2},\qquad
 f_{-1}^\sigma(0)=-2^{-1/2},\qquad
 f_n^\sigma(0)=0\quad(n\ne\pm1).
 \tag{0.2}
\]

Fix \(\mu>0\), put \(A=\mu+N^2\), and let

\[
 (Bf)_n=f_{n-1}-f_{n+1},\qquad
 q_\sigma(y)=\langle A^{-1}Bf^\sigma(y),Bf^\sigma(y)\rangle.
 \tag{0.3}
\]

The normalized critical-log action is

\[
 \mathscr A_\sigma
 =\int_0^1 y^{-1/3}[1+\log(1/y)]e^{-2(1+\mu)y}
 q_\sigma(y)\,dy.
 \tag{0.4}
\]

For the fixed one-carrier geometry, the inherited physical lift obeys
\(\Theta_\sigma\asymp\sigma^2\), and

\[
 x_\sigma=\Theta_\sigma\mathscr A_\sigma.
 \tag{0.5}
\]

The first theorem is

\[
 \boxed{
 c\sigma^{-2/3}\log\sigma
 \le \mathscr A_\sigma\le C,
 \qquad
 c\sigma^{4/3}\log\sigma
 \le x_\sigma\le C\sigma^2.}
 \tag{0.6}
\]

If \(K_\sigma\) is the actual enstrophy contrast after adding the fixed
decoupled background used in R0.72L, then

\[
 \boxed{K_\sigma\le C(1+\sigma^{2/3}).}
 \tag{0.7}
\]

Consequently the proposed action-poor condition fails in the strong form

\[
 \boxed{
 \frac{\sigma^{1/3}x_\sigma}{K_\sigma}
 \ge c\sigma\log\sigma\longrightarrow\infty.}
 \tag{0.8}
\]

With the R0.72M scalar coefficients

\[
 U_\sigma\asymp\sigma^{7/3},\qquad
 V_\sigma\asymp\sigma^{1/3},
 \tag{0.9}
\]

the exact scalar term satisfies

\[
 \boxed{
 T_\sigma
 :=\frac{\min\{U_\sigma,V_\sigma x_\sigma\}}
 {K_\sigma+x_\sigma}
 \asymp\sigma^{1/3}.}
 \tag{0.10}
\]

Thus the actual dissipative action lies in the R0.72M danger window for
every fixed superlevel once \(\sigma\) is large.  The action denominator
cannot close this launch.

There is, however, a direct route that does not pass through that scalar
screen.  If

\[
 \mathcal F^\sigma(y,\theta)=\sum_{n\in\mathbb Z}
 f_n^\sigma(y)e^{in\theta},\qquad
 F^\sigma(t,\theta)=\mathcal F^\sigma(\nu t,\theta),
 \quad \nu=\sigma^{-1},
 \tag{0.11}
\]

then, with \(t=\sigma y\),

\[
 \partial_tF^\sigma
 =\nu\partial_\theta^2F^\sigma
 +2i e^{-\nu t}\sin\theta\,F^\sigma.
 \tag{0.12}
\]

This is the \(k=-2\), zero-horizontal-diffusion Fourier mode of a passive
scalar transported by the time-dependent shear
\(V(t,\theta)=e^{-\nu t}\sin\theta\).  The nondegenerate-shear theorem of
Coble and He applies uniformly on \(0\le t\le\nu^{-1}\) and gives

\[
 \|F^\sigma(t)\|_{L^2(\mathbb T)}
 \le C e^{-c\nu^{1/2}t}\|F^\sigma(0)\|_{L^2(\mathbb T)}.
 \tag{0.13}
\]

Consequently the actual first-row cubic satisfies

\[
 \boxed{
 \mathcal C_{\rm diss}(\sigma)
 \le C a^2\sigma^{1/2}
 =o(\sigma a^2).}
 \tag{0.14}
\]

Thus R0.72N gives both a negative and a positive decision: the
critical-action denominator is asymptotically unsafe, while the true cubic
is directly sublinear.  The latter closes the weaker one-carrier gate stated
in R0.72M.  It is not the sharper logarithmic estimate suggested by finite
curves.

---

## 1. Exact energy and moment ledger

Work on real \(\ell^2(\mathbb Z)\).  Define

\[
 E(y)=\sum_n|f_n^\sigma(y)|^2,\qquad
 D(y)=\sum_n n^2|f_n^\sigma(y)|^2,\qquad
 P(y)=\sum_n n^4|f_n^\sigma(y)|^2.
 \tag{1.1}
\]

The operator \(B\) is skew-adjoint.  The following differentiations and
index shifts may first be made on Galerkin truncations; parabolic smoothing
and the corresponding moment bounds then justify passage to the full chain.
Hence

\[
 \frac12E'(y)=-D(y),
 \qquad E(y)\le E(0)=1.
 \tag{1.2}
\]

Differentiating the second moment gives

\[
 D'(y)=-2P(y)+2g(y)S(y),
 \qquad g(y)=\sigma e^{-y},
 \tag{1.3}
\]

where the commutator sum is exactly

\[
 S(y)=\sum_{n\in\mathbb Z}(2n+1)f_n^\sigma(y)f_{n+1}^\sigma(y).
 \tag{1.4}
\]

Splitting \(2n+1=n+(n+1)\) and applying Cauchy--Schwarz twice gives

\[
 |S(y)|\le2\sqrt{D(y)E(y)}.
 \tag{1.5}
\]

Also \(D^2\le PE\), so \(P\ge D^2\) because \(E\le1\).  Therefore

\[
 D'(y)\le-2D(y)^2+4\sigma\sqrt{D(y)}.
 \tag{1.6}
\]

At \(D=(2\sigma)^{2/3}\) the right side is zero, and it is negative
above that value.  Since \(D(0)=1\), the scalar barrier argument yields

\[
 \boxed{
 \sup_{0\le y\le1}D(y)
 \le\max\{1,(2\sigma)^{2/3}\}.}
 \tag{1.7}
\]

This estimate uses the full infinite chain.  It is not a finite-support or
Galerkin argument.

---

## 2. From the modal moment to the physical enstrophy contrast

After restoring the common heat factor, the active one-carrier enstrophy
is bounded, up to fixed geometry constants, by

\[
 Y_{\rm act}(y)
 \lesssim e^{-2\mu y}[\mu E(y)+D(y)].
 \tag{2.1}
\]

The inherited decoupled background on \([0,1]\) has fixed positive lower
and upper bounds independent of \(\sigma\).  Thus

\[
 K_\sigma
 =\frac{\sup_{[0,1]}(Y_{\rm bg}+Y_{\rm act})}
 {\inf_{[0,1]}(Y_{\rm bg}+Y_{\rm act})}
 \le C[1+\sup_{[0,1]}D].
 \tag{2.2}
\]

Equation (1.7) proves (0.7).  No lower enstrophy-growth assertion is needed
for the no-go theorem.

---

## 3. The first coupling layer forces critical-log action

The upper bound in (0.6) is immediate.  Since
\(\|B\|_{\ell^2\to\ell^2}\le2\), \(A^{-1}\le\mu^{-1}\), and
\(E(y)\le1\),

\[
 0\le q_\sigma(y)\le\frac4\mu.
 \tag{3.1}
\]

The weight in (0.4) is integrable at zero, hence

\[
 \mathscr A_\sigma\le C_\mu.
 \tag{3.2}
\]

For the lower bound, introduce

\[
 s=\sigma(1-e^{-y}),\qquad
 y_\sigma(s)=-\log(1-s/\sigma),
 \tag{3.3}
\]

and write \(h^\sigma(s)=f^\sigma(y_\sigma(s))\).  On every fixed
\(0\le s\le S<\sigma\),

\[
 \partial_sh^\sigma
 =Bh^\sigma-\frac1{\sigma-s}N^2h^\sigma.
 \tag{3.4}
\]

Let \(\phi(s)=e^{sB}f(0)\) be the frozen full-lattice solution.  The
non-autonomous propagator generated by
\(B-(\sigma-s)^{-1}N^2\) is an \(\ell^2\) contraction.  Variation of
constants therefore gives

\[
 \sup_{0\le s\le S}\|h^\sigma(s)-\phi(s)\|_2
 \le\frac1{\sigma-S}
 \int_0^S\|N^2\phi(r)\|_2\,dr
 =O_S(\sigma^{-1}).
 \tag{3.5}
\]

The last integral is finite.  Indeed, the R0.72M full-lattice formula
\(\phi_n(s)=\sqrt2J_n'(2s)\) has finite weighted moments of every order on
compact \(s\)-intervals.  Since \(B\) and \(A^{-1}\) are bounded, (3.5)
also implies uniform convergence of the corresponding \(q\)-densities.

At \(s=0\),

\[
 (Bf(0))_0=-\sqrt2,\qquad
 (Bf(0))_{2}=(Bf(0))_{-2}=2^{-1/2},
 \tag{3.6}
\]

and all other entries vanish.  Hence

\[
 q_{\rm fr}(0)=\frac2\mu+\frac1{\mu+4}>0.
 \tag{3.7}
\]

Continuity and (3.5) give fixed \(0<s_0<s_1<\infty\) and \(c_0>0\)
such that

\[
 q_\sigma(y_\sigma(s))\ge c_0
 \qquad(s_0\le s\le s_1)
 \tag{3.8}
\]

for all sufficiently large \(\sigma\).  On this fixed interval,
\(y_\sigma(s)\asymp s/\sigma\) and
\(dy=ds/(\sigma-s)\).  Restricting (0.4) to \([s_0,s_1]\) yields

\[
 \mathscr A_\sigma
 \ge c\sigma^{-2/3}\log\sigma.
 \tag{3.9}
\]

Multiplying (3.2) and (3.9) by
\(\Theta_\sigma\asymp\sigma^2\) proves (0.6).

The logarithm in this lower bound is not a large-time mixing effect.  It
is already forced by the critical-log weight on the first nontrivial
coupling layer \(y\asymp\sigma^{-1}\).

---

## 4. Exact placement inside the R0.72M danger window

For positive \(U,V,K,x\),

\[
 T=\frac{\min\{U,Vx\}}{K+x}
 \quad\Longrightarrow\quad
 \frac1T
 =\max\left\{\frac{K+x}{U},\frac{K+x}{Vx}\right\}.
 \tag{4.1}
\]

Use (0.6)--(0.9).  The first reciprocal branch satisfies

\[
 \frac{K_\sigma+x_\sigma}{U_\sigma}
 \le C(\sigma^{-5/3}+\sigma^{-1/3}),
 \tag{4.2}
\]

while the second satisfies

\[
 \frac{K_\sigma+x_\sigma}{V_\sigma x_\sigma}
 =\frac1{V_\sigma}
 +\frac{K_\sigma}{V_\sigma x_\sigma}
 \le C\left(\sigma^{-1/3}
 +\frac1{\sigma\log\sigma}\right).
 \tag{4.3}
\]

Thus \(T_\sigma\ge c\sigma^{1/3}\).  Since always \(T\le V\), the
matching upper bound follows, proving (0.10).

Equivalently, for every fixed \(M>0\), the actual action eventually lies
in the exact R0.72M superlevel interval

\[
 \left(
 \frac{MK_\sigma}{V_\sigma-M},
 \frac{U_\sigma}{M}-K_\sigma
 \right).
 \tag{4.4}
\]

This is a no-go for the scalar action screen, not a lower bound for the
true cubic variation.  The scalar estimate discards the oscillatory sign
structure that the dissipative chain appears to retain.

---

## 5. Enhanced dissipation closes the sublinear true-cubic gate

For the first row, write

\[
 u(y)=f_1^\sigma(y),\qquad
 v(y)=f_0^\sigma(y)-f_2^\sigma(y).
 \tag{5.1}
\]

Then

\[
 u'(y)+u(y)=\sigma e^{-y}v(y).
 \tag{5.2}
\]

Up to the fixed physical weight, the true cubic is

\[
 \mathcal C_{\rm diss}(\sigma)
 =4a^2\int_0^1\sigma e^{-(3+2\mu)y}
 |u(y)v(y)|\,dy.
 \tag{5.3}
\]

Equation (5.2) also rewrites it as a weighted absolute variation of
\(u^2\):

\[
 \mathcal C_{\rm diss}(\sigma)
 =4a^2\int_0^1e^{-(2+2\mu)y}
 |u(y)[u'(y)+u(y)]|\,dy.
 \tag{5.4}
\]

The total-variation formulation is useful for a sharp logarithmic target,
but it is not necessary for sublinearity.  Define \(\mathcal F^\sigma\)
by (0.11).
The chain gives

\[
 \partial_y\mathcal F^\sigma
 =\partial_\theta^2\mathcal F^\sigma
 +2i\sigma e^{-y}\sin\theta\,\mathcal F^\sigma.
 \tag{5.5}
\]

With \(t=\sigma y\), \(\nu=\sigma^{-1}\), put

\[
 g_n(t)=f_n^\sigma(\nu t),\qquad
 F(t,\theta)=\sum_ng_n(t)e^{in\theta}.
 \tag{5.6}
\]

This is (0.12).  To match the notation of Coble--He, take the horizontal
Fourier number \(k=-2\), the horizontal diffusion switch equal to zero,
and

\[
 V_\nu(t,\theta)=U_\nu(t,\theta)
 =e^{-\nu t}\sin\theta.
 \tag{5.7}
\]

On \(0\le t\le\nu^{-1}\), the two critical points are fixed and
nondegenerate, the amplitude lies in \([e^{-1},1]\), and all shape and
\(W^{2,\infty}\) constants are uniform.  Moreover,

\[
 \|\partial_{t\theta}U_\nu\|_\infty
 \le\nu\le\nu^{3/4}\qquad(0<\nu\le1).
 \tag{5.8}
\]

Thus every hypothesis of their nondegenerate time-dependent shear theorem
holds with constants uniform in \(\nu\).  The theorem is stated with a
threshold \(\nu_0(U,V)\), but Section 3 and Appendix A construct that
threshold from the shape constants, a spectral inequality, fixed cutoff
derivatives, and \(\|\partial_{\theta\theta}U\|_\infty\).  Here the critical
points are fixed and the cutoffs can be chosen independently of \(\nu\).
Consequently there is one \(\nu_*>0\) and one decay constant valid for the
whole family \(0<\nu\le\nu_*\).  For the fixed mode \(|k|=2\), its
conclusion is (0.13).

With the Fourier convention in (5.6), exact Parseval is

\[
 E_g(t):=\sum_n|g_n(t)|^2
 =\frac1{2\pi}\|F(t)\|_{L^2(\mathbb T)}^2.
 \tag{5.9}
\]

Coordinate projection gives the sharper elementary bound

\[
 |g_1(t)[g_0(t)-g_2(t)]|
 \le\frac1{\sqrt2}
 \bigl(|g_1|^2+|g_0|^2+|g_2|^2\bigr)
 \le\frac1{\sqrt2}E_g(t).
 \tag{5.10}
\]

Under \(y=\nu t\), one has \(dy=\nu\,dt\) and
\(\sigma\,dy=dt\).  Thus (5.3) is exactly

\[
 \mathcal C_{\rm diss}
 =4a^2\int_0^{\nu^{-1}}
 e^{-(3+2\mu)\nu t}
 |g_1(t)[g_0(t)-g_2(t)]|\,dt.
 \tag{5.11}
\]

Dropping the physical weight bounded by one and applying (0.13) therefore
yields

\[
\begin{aligned}
 \mathcal C_{\rm diss}(\sigma)
 &\le Ca^2\int_0^{\nu^{-1}}
       e^{-2c\nu^{1/2}t}\,dt \\
 &\le Ca^2\sigma^{1/2}.
\end{aligned}
 \tag{5.12}
\]

For bounded \(\sigma\), the energy identity enlarges the same constant, so
(0.14) holds for all \(\sigma\ge1\).  This is a corollary obtained here from
the cited semigroup theorem; it is not a theorem stated in that paper.

Finite producer and independent curves remain compatible with the stronger

\[
 \mathcal C_{\rm diss}(\sigma)
 \lesssim a^2[1+\log(1+\sigma)],
 \tag{5.13}
\]

but no finite fit proves (5.13), and the enhanced-dissipation argument does
not recover it.

---

## 6. Claim boundary

R0.72N proves, in the declared fixed one-carrier class:

1. the exact full-chain energy identity (1.2);
2. the exact second-moment commutator identity (1.3)--(1.4);
3. the coupling-uniform moment barrier (1.7);
4. the enstrophy-contrast upper bound (0.7);
5. the first-layer critical-log action lower bound and the global action
   upper bound (0.6);
6. failure of the proposed action-poor inequality (0.8);
7. the sharp scalar-screen order \(T_\sigma\asymp\sigma^{1/3}\);
8. the direct true-cubic upper bound
   \(\mathcal C_{\rm diss}\lesssim a^2\sigma^{1/2}\), obtained by mapping
   the chain to a published time-dependent-shear enhanced-dissipation
   theorem.

It does not prove:

1. logarithmic growth of the true cubic variation;
2. a matching asymptotic for the dissipative enstrophy moment or action;
3. a multi-carrier or multiscale strong-coupling theorem;
4. a continuation criterion for arbitrary three-dimensional solutions;
5. finite-time singularity or global smoothness for general
   Navier--Stokes.

The Clay Millennium problem remains open.

---

## 7. Next exact gate

R0.72O should reinsert (0.14) into the normalized R0.72L physical ledger and
determine exactly which one-carrier strong-coupling window is now paid by
the direct cubic branch.  The next structural question is then whether the
same estimate survives finite or common-band multi-carrier superposition
without losing the \(\sigma^{1/2}\) gain to cross terms.

In parallel, (5.4) leaves a sharper optional target,

\[
 \operatorname{TV}_{[0,1]}(u^2)
 \lesssim1+\log(1+\sigma),
 \tag{7.1}
\]

which would match the finite one-carrier diagnostics.  That logarithmic
refinement is no longer required for the one-carrier sublinear decision,
but it may matter when summing many carriers.

---

## References used at this gate

1. Daniel Coble and Siming He, *A Note on Enhanced Dissipation of
   Time-Dependent Shear Flows*, *Communications in Mathematical Sciences*
   22(6) (2024),
   [DOI](https://doi.org/10.4310/CMS.2024.v22.n6.a10),
   [arXiv:2309.15738](https://arxiv.org/abs/2309.15738).  The published
   theorem supplies the semigroup estimate; (0.14) is the project-specific
   corollary proved above.
2. Johannes Benthaus and Camilla Nobili, *Enhanced Dissipation via
   Time-Modulated Velocity Fields*, *Evolution Equations and Control Theory*
   15 (2026),
   [DOI](https://doi.org/10.3934/eect.2025051),
   [arXiv:2501.16905](https://arxiv.org/abs/2501.16905).  This is supporting
   literature for time modulation, not the source of (0.14).
