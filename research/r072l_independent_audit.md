# R0.72L independent analytic audit

**Verdict:** PASS WITH QUALIFICATIONS
**Date:** 2026-08-27

The independent derivation found no fatal exponent or inequality-direction
error in the R0.72L positive route.  It imposed five publication conditions.

1. In strong coupling, use only
   \(\mathcal J_{\rm all}\lesssim\Theta G_{\rm all}^{\rm ex}\).
   A two-sided equivalence is not available because enstrophy at a root can
   exceed its launch scale.
2. The inequality \(\Lambda_{1,*}\gtrsim K+x\) uses two different facts:
   the fixed background gives \(\inf Y\gtrsim E_{\rm phys}\) for the root
   upper lift, while \(\inf Y\le Y(0)\lesssim E_{\rm phys}\) gives the
   action lower lift.
3. The exact root and local action floor require a phase-aligned,
   row-aligned, exactly corrected launch and the fixed background.  They are
   not statements about every launch.
4. The upper edge
   \(\varepsilon\lesssim p^{2/3}R^{2/3}L_R\) gives a bounded normalized
   ledger.  Decay requires the corresponding little-o hypothesis.
5. Define \(\varepsilon=gB/R^2\) as the common-band exposure scale.  The
   operator hypothesis proves only
   \(|\delta|\int\|V_w(x)\|\,dx\lesssim\varepsilon\), not a reverse
   inequality; the actual Duhamel exposure may be smaller.

The audit recomputed

\[
 U_0=\varepsilon^{4/3}p^{4/3},\quad
 W=\varepsilon^{1/3}p^{1/3}R^{-1/3}L_R^{-1/2},
\]

\[
 U=\varepsilon^{7/3}p^{4/3},\quad
 V=\varepsilon^{1/3}p^{1/3}R,\quad
 H=\varepsilon^2p/R,
\]

and verified the scalar optimizations in (0.8).  With
\(p\gtrsim R^{-1/2}\), the first-root and mixed-row terms vanish across the
declared window, while the cubic term is bounded at its upper edge and
vanishes in the little-o subwindow.

The finite Galerkin theorem and the full-lattice non-embedding proposition
were audited separately from the positive theorem.  They constrain a proof
route; they do not supply a full-PDE counterexample.
