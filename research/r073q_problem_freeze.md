# R0.73Q problem freeze: a critical heat-flow tube beyond the \(H^{1/2}\) ball

**Status:** scope frozen; primary-source collision audit and analytic proof
complete

**Parent result:** R0.73P all-time weak relative stability, the periodic
\(H^{1/2}\) strong tube, and the unresolved unrestricted \(L^2\)-only entrance

**Equation:** unforced incompressible Navier--Stokes on the normalized standard
three-torus \([0,2\pi]^3\), viscosity one, in the mean-zero divergence-free
phase space

## 0. The question that is actually being tested

Let

\[
 u\in C([0,\infty);H^3_{\sigma,0})
 \cap L^2_{\rm loc}([0,\infty);H^4_{\sigma,0})
 \tag{0.1}
\]

be a fixed a priori global unforced strong orbit.  R0.73P constructed a
uniform all-starting-time strong stability tube when the initial difference
is small in \(H^{1/2}\).  R0.73Q asks whether adjoining a tube in a strictly
weaker, still well-posed critical topology produces a strictly enlarged
stable domain without crossing into the unresolved \(L^2\)-only problem or
the non-unique nonperturbative \(BMO^{-1}\) endpoint.

The candidate is the concrete heat-flow trace norm

\[
 \|f\|_{\mathfrak X}
 :=\|e^{t\Delta}f\|_{L^4((0,\infty);L^6(\mathbb T^3))}.
 \tag{0.2}
\]

On mean-zero periodic distributions, \(\mathfrak X\) is an equivalent
realization of the homogeneous critical Besov space
\(\dot B^{-1/2}_{6,4}(\mathbb T^3)\).  Equation (0.2), rather than an
unspecified Littlewood--Paley cutoff, is the release's audited norm.

The release tests four statements.

1. The periodic Oseen bilinear map closes on
   \(E:=L^4_tL^6_x\).
2. The linearized Volterra operator about the possibly large reference orbit
   is invertible on \(E\) after a finite partition controlled by the orbit's
   \(L^4_tL^6_x\) action.
3. The resulting radius is uniform for every restart time \(t_0\ge0\).
4. The \(\mathfrak X\)-tube contains a small \(H^{1/2}\)-ball but also smooth
   perturbations whose \(H^{1/2}\) norm is arbitrarily large.

## 1. The finite reference action

R0.73P proved

\[
 \mathcal A_{1/2}[u]
 :=\int_0^\infty |u(t)|_1^4\,dt<\infty.
 \tag{1.1}
\]

The periodic Sobolev inequality gives

\[
 M[u]
 :=\|u\|_{L^4((0,\infty);L^6)}
 \le C_S\mathcal A_{1/2}[u]^{1/4}<\infty.
 \tag{1.2}
\]

For every restart time,

\[
 \|u\|_{L^4((t_0,\infty);L^6)}\le M[u].
 \tag{1.3}
\]

This monotone tail bound is the source of the uniform quantifier in \(t_0\).
No time-translation compactness or unverified periodic scaling argument is
needed.

## 2. Target P1: the critical periodic bilinear estimate

For causal functions on \((0,\infty)\), define

\[
 \mathcal B(a,b)(t)
 :=\int_0^t e^{(t-s)\Delta}P\nabla\!\cdot(a\otimes b)(s)\,ds.
 \tag{2.1}
\]

The target estimate is

\[
 \boxed{
 \|\mathcal B(a,b)\|_E
 \le C_B\|a\|_E\|b\|_E.}
 \tag{2.2}
\]

The proof must use the periodic Oseen bound

\[
 \|e^{\tau\Delta}P\nabla\!\cdot F\|_6
 \le C K(\tau)\|F\|_3,
 \qquad
 K(\tau)\lesssim
 \begin{cases}
 \tau^{-3/4},&0<\tau\le1,\\
 e^{-c\tau},&\tau\ge1,
 \end{cases}
 \tag{2.3}
\]

together with the one-dimensional Hardy--Littlewood--Sobolev map
\(I_{1/4}:L^2_t\to L^4_t\).  Ordinary Young convolution at the short-time
endpoint is not admissible, because \(\tau^{-3/4}\notin L^{4/3}(0,1)\).

## 3. Target P2: inversion of the large-orbit cross term

After a restart at \(t_0\), put \(U(t)=u(t_0+t)\) and define

\[
 \mathcal L_U z:=\mathcal B(U,z)+\mathcal B(z,U).
 \tag{3.1}
\]

The global norm of \(\mathcal L_U\) need not be small.  Choose
\(\varepsilon_B>0\) with \(2C_B\varepsilon_B<1\) and partition time into
finitely many consecutive intervals on which

\[
 \|U\|_{L^4L^6}\le\varepsilon_B.
 \tag{3.2}
\]

The number of intervals is bounded uniformly by

\[
 N[u]\le 1+\left({M[u]\over\varepsilon_B}\right)^4.
 \tag{3.3}
\]

Causality and interval-by-interval Neumann inversion should then give

\[
 (I+\mathcal L_U)^{-1}:E\to E,
 \qquad
 \|(I+\mathcal L_U)^{-1}\|_{E\to E}\le K[u]<\infty,
 \tag{3.4}
\]

where the same \(K[u]\) works for every \(t_0\ge0\).  The proof must display
one valid finite recursion for \(K[u]\); the mere phrase "subdivide time" is
not sufficient.

## 4. Target P3: a uniform heat-flow stability radius

Let \(w_0=v(t_0)-u(t_0)\in H^3_{\sigma,0}\).  The difference equation is

\[
 w=e^{t\Delta}w_0-\mathcal L_Uw-\mathcal B(w,w).
 \tag{4.1}
\]

Using (3.4), it becomes a quadratic fixed-point problem on \(E\).  A target
radius of the form

\[
 \rho_{\mathfrak X}[u]
 :={1\over c_B C_BK[u]^2}>0
 \tag{4.2}
\]

with a displayed numerical safety factor \(c_B\) should imply, uniformly for
every \(t_0\ge0\),

\[
 \|w_0\|_{\mathfrak X}<\rho_{\mathfrak X}[u]
 \quad\Longrightarrow\quad
 v\in C([t_0,\infty);H^3_{\sigma,0})
 \cap L^2_{\rm loc}([t_0,\infty);H^4_{\sigma,0}).
 \tag{4.3}
\]

The constructed difference also satisfies

\[
 \|w\|_{L^4((t_0,\infty);L^6)}
 \le 2K[u]\|w_0\|_{\mathfrak X}.
 \tag{4.4}
\]

Because \(u+w\in L^4_{\rm loc}L^6\), the Serrin criterion propagates the
initial \(H^3\) regularity.  The R0.73P relative-energy theorem remains
available and yields exponential synchronization in \(L^2\); (4.3) is not a
replacement for that theorem.

## 5. Target P4: strict enlargement beyond the \(H^{1/2}\) tube

Periodic Bernstein and dyadic summation give

\[
 H^{1/2}=B^{1/2}_{2,2}
 \hookrightarrow B^{-1/2}_{6,2}
 \hookrightarrow B^{-1/2}_{6,4}\simeq\mathfrak X.
 \tag{5.1}
\]

Thus a sufficiently small \(H^{1/2}\)-ball lies inside the new tube.  The
inclusion is strict even when the perturbations are restricted to smooth,
mean-zero, divergence-free fields.  With normalized Haar measure, set

\[
 w_N(x):=N^{-1/4}e_2\sin(Nx_1),
 \qquad N\in\mathbb N.
 \tag{5.2}
\]

Since \((w_N\!\cdot\nabla)w_N=0\), this is also a heat-decaying shear mode.
Writing

\[
 c_6:=\|\sin x_1\|_6=\left({5\over16}\right)^{1/6},
 \tag{5.3}
\]

direct integration gives

\[
 \|w_N\|_{\mathfrak X}
 ={c_6\over4^{1/4}}N^{-3/4}\longrightarrow0,
 \tag{5.4}
\]

whereas

\[
 \|w_N\|_2={1\over\sqrt2}N^{-1/4}\longrightarrow0,
 \qquad
 |w_N|_{1/2}={1\over\sqrt2}N^{1/4}\longrightarrow\infty.
 \tag{5.5}
\]

Consequently, for every positive heat-flow radius and every prescribed
\(H^{1/2}\) threshold, some smooth \(w_N\) lies in the former and outside
the latter.  This is a topological and dynamical entrance result, not a claim
that arbitrary \(L^2\)-small data are safe.

The two independently proved radii need not be ordered.  Therefore the
strict set enlargement to be published is

\[
 \mathcal D_Q[u]
 :=\{w_0:|w_0|_{1/2}<R_{1/2}[u]\}
 \cup
 \{w_0:\|w_0\|_{\mathfrak X}<\rho_{\mathfrak X}[u]\}.
 \tag{5.6}
\]

Both pieces are stable, and (5.4)--(5.5) imply

\[
 \mathcal D_Q[u]
 \supsetneq\{w_0:|w_0|_{1/2}<R_{1/2}[u]\}.
 \tag{5.7}
\]

No claim is made that the heat-flow ball alone contains the entire numerical
\(R_{1/2}[u]\)-ball from R0.73P.

## 6. Collision boundary that must remain visible

The primary-source audit must separate the following domains and solution
classes.

- Kato's \(L^3\) and Koch--Tataru's small \(BMO^{-1}\) theorems are whole-
  space critical small-data results.
- Gallagher--Iftimie--Planchon prove openness and Lipschitz stability around
  a priori global solutions in whole-space critical Besov spaces
  \(\dot B^{3/p-1}_{p,q}\), for finite indices in the stated range.
- The Auscher--Dubois--Tchamitchian publisher abstract reports whole-space
  \(BMO^{-1}\)-topology openness for the corresponding Cauchy-data set; the
  unavailable theorem formulas are not reconstructed here.
- Coiculescu--Palasek construct nonperturbative
  \(BMO^{-1}(\mathbb T^3)\) data with two distinct global finite-\(X_{KT}\)
  solutions smooth for positive time.  This is not a quantitative lower
  bound on the datum norm, and the endpoint cannot be promoted to
  unrestricted uniqueness.
- R0.73Q works on the fixed torus, at the finite-index
  \(B^{-1/2}_{6,4}\) level, and proves the needed periodic estimate rather
  than importing a whole-space scaling statement verbatim.

## 7. Explicit exclusions

R0.73Q will not claim any of the following.

1. A global strong solution for every smooth periodic datum.
2. A radius depending only on the \(L^2\) norm.
3. Uniqueness for arbitrary nonperturbative \(BMO^{-1}\) data.
4. A rough-data uniqueness theorem outside the \(L^4_tL^6_x\) mild/Serrin
   class.
5. A new version of the whole-space Gallagher--Iftimie--Planchon or
   Auscher--Dubois--Tchamitchian theorem.
6. Progress resolving the Clay global-regularity alternative.

The mathematical contribution tested here is narrower: a self-contained
periodic, uniform-in-restart heat-flow tube around one fixed global strong
orbit, together with an exact smooth sequence proving that adjoining this
tube strictly enlarges the previously published \(H^{1/2}\) stable domain.

## 8. Required closeout evidence

The section cannot be released until all of the following are present.

- a primary-source theorem ledger with exact domains and quantifiers;
- a full proof of the periodic Oseen/HLS bilinear estimate;
- an explicit causal interval recursion proving (3.4);
- a quadratic fixed-point and Serrin-continuation proof;
- an independent analytic audit;
- a finite exact-arithmetic certificate for (5.3)--(5.5);
- a formal vector figure, source data, checksums, and final-size/grayscale QA;
- synchronized Chinese/English HTML and PDF, recap, index, literature, and
  publication gates.
