# R0.72N independent analytic audit

**Verdict:** PASS WITH QUALIFICATIONS
**Date:** 2026-08-27

The derivation was rebuilt from the dissipative lattice and the passive
scalar mode equation.  The following points are necessary for the public
claim.

1. The commutator is
   \[
   \langle N^2f,Bf\rangle
   =\sum_n(2n+1)f_nf_{n+1}.
   \]
   Splitting \(2n+1=n+(n+1)\) gives the factor
   \(2\sqrt{DE}\).  Together with \(D^2\le PE\), this yields the exact
   barrier \((2\sigma)^{2/3}\).  The index shift should first be made on
   Galerkin truncations and then passed to the parabolic limit.
2. Under \(s=\sigma(1-e^{-y})\), the dissipative coefficient is exactly
   \((\sigma-s)^{-1}\).  The non-autonomous evolution is an
   \(\ell^2\)-contraction, so the fixed-\(s\) Duhamel error is
   \(O_S(\sigma^{-1})\).
3. The first-layer density is strictly positive:
   \[
   q_{\rm fr}(0)=\frac2\mu+\frac1{\mu+4}.
   \]
   Since \(y\asymp s/\sigma\) and \(dy=ds/(\sigma-s)\), this gives
   \(\mathscr A_\sigma\gtrsim\sigma^{-2/3}\log\sigma\), not merely a
   numerical scaling.
4. With \(x\gtrsim\sigma^{4/3}\log\sigma\),
   \(K\lesssim\sigma^{2/3}\), \(U\asymp\sigma^{7/3}\), and
   \(V\asymp\sigma^{1/3}\), both reciprocal branches give
   \(T_\sigma\gtrsim\sigma^{1/3}\); \(T\le V\) gives the reverse bound.
   The action-poor route is therefore false for this launch.
5. The generating function satisfies
   \[
   F_y=F_{\theta\theta}+2i\sigma e^{-y}\sin\theta\,F.
   \]
   With \(t=\sigma y\), \(\nu=\sigma^{-1}\), this is the \(k=-2\)
   Fourier mode of the Coble--He passive-scalar equation with horizontal
   diffusion switch zero and \(V=e^{-\nu t}\sin\theta\).
6. Choosing the reference shear \(U=V\) avoids any ambiguity about moving
   critical points.  On \(0\le t\le\nu^{-1}\), the amplitude belongs to
   \([e^{-1},1]\), the two critical points are fixed and nondegenerate,
   and
   \[
   \|\partial_{t\theta}U\|_\infty\le\nu\le\nu^{3/4}.
   \]
   The structural and spectral constants in the proof are therefore
   uniform as \(\nu\downarrow0\).
7. The theorem controls the \(L^2\) norm of the mode.  Squaring its decay
   estimate and using
   \[
   |f_1(f_0-f_2)|\le\sqrt2\sum_n|f_n|^2
   \]
   gives an integrable envelope on the enhanced-dissipation time scale
   \(\nu^{-1/2}\).  The change of variables contributes no extra power:
   \(\sigma\,dy=dt\).  Hence
   \[
   \mathcal C_{\rm diss}\lesssim a^2\nu^{-1/2}
   =a^2\sigma^{1/2}.
   \]
8. This \(O(\sigma^{1/2})\) estimate is a project-specific corollary of a
   published semigroup theorem.  Coble and He do not state the cubic
   corollary.  Conversely, the corollary does not prove the finite-data
   suggestion \(O(\log\sigma)\).
9. The result is confined to the declared one-carrier launch and fixed
   geometry.  It does not control multi-carrier cross terms, complete the
   R0.72L physical absorption ledger, or give a continuation theorem for
   general three-dimensional Navier--Stokes solutions.

No exponent, Jacobian, sign, or inequality-direction error was found after
imposing these qualifications.
