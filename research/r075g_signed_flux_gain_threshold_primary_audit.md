# Independent primary audit of R0.75G

## 0. Frozen object and verdict

Audited file: `research/r075g_signed_flux_gain_threshold.md`.

Frozen SHA-256:
`f2b3424dddb7eee5938200c3433cd012a1820564e43ad446e0c88d8dfa39ff41`.

**Verdict: PASS. Mathematical blocker count: 0. Release blocker count: 0.**

The note proves a conditional exponent threshold. It does not prove the
positive correlation gain assumed in G.1, does not treat its threshold as
necessary for unrelated proof methods, and does not promote the
pure-transport benchmark to the diffusive passive equation.

The four frozen inputs recompute as

| input | SHA-256 |
|---|---|
| `research/r075c_background_shear_packing_false_positive.md` | `1f72f3c9d9d348f86188206690ce714df28aed661a9192c7b53bc1e5921f2f89` |
| `research/r075d_passive_gradient_route_screen.md` | `54bcd703aff9a55f8fff522ded2bf1c5b629ee2497bd4f2255a6224e4bb747f6` |
| `research/r075e_horizontal_cross_mode_flux_reduction.md` | `99529b8934412775e19a1b70784cddf3e62190b50c42669ccd34135a134c5049` |
| `research/r075f_modal_phase_integration_identity.md` | `f7a72ebfe0471e18c0d5d44bd3123491d7cd47a79293d1860c5d023c13acf440` |

## 1. Background atom, G.5--G.10

The normalized background atom has four independent scale factors:

\[
 R^{-2}\omega
 \times O(R^2)
 \times O(L^2R^3)
 \times O(R^{-6}).
\]

They are respectively the payment normalization, time length, collar
volume, and `|b|^3` bound. Their product is

\[
 p_b\le C L^2\omega R^{-3},
\]

and its cube root is

\[
 p_b^{1/3}\le C L^{2/3}\omega^{1/3}R^{-1}.
\]

No lower bound on `p_b` is used in the sufficient implication.

## 2. Gain threshold, G.11--G.15

Assuming G.1 and using `p_F <= C P_R^M` gives the coefficient

\[
 L^{2/3}\omega^{1/3}R^{\alpha-1}.
\]

Its exact exponential rate is

\[
 \frac{(1-\alpha)\rho}{4}-\frac{c_\gamma}{12}.
\]

Strict negativity is equivalent to

\[
 \alpha>1-\frac{c_\gamma}{3\rho}
 =1-\frac{80000}{107163}
 =\frac{27163}{107163}
 =0.253473680281\ldots.
\]

At equality the exponential rate vanishes while `L^(2/3)` grows, so the
strict inequality is necessary for this unrefined sufficient estimate.
Direct rational substitution gives

\[
 \begin{aligned}
 \alpha=\frac13&:\quad
 \frac\rho6-\frac{c_\gamma}{12}
 =-\frac{4279}{238140000},\\
 \alpha=\frac14&:\quad
 \frac{3\rho}{16}-\frac{c_\gamma}{12}
 =\frac{1489}{1905120000}.
 \end{aligned}
\]

The first closes E.24 conditionally; the second leaves an exponentially
growing coefficient and therefore does not close it by this route.

## 3. Amplitude homogeneity, G.16--G.17

For `A>0`, the positive signed flux is quadratic in `F`, while the passive
cubic atom is cubic:

\[
 \mathfrak X(AF,b)=A^2\mathfrak X(F,b),
 \qquad p_{AF}^{2/3}=A^2p_F^{2/3}.
\]

Thus the normalized correlation ratio is exactly amplitude invariant.
The note correctly concludes only that amplitude renormalization cannot
manufacture the missing `R^alpha` factor.

## 4. Residence exponent and kinematic benchmark, G.18--G.20

If an interaction atom is smaller than the full background atom by
`R^beta`, its cube root produces `R^(beta/3)`. Therefore

\[
 \beta_*=3\alpha_*
 =\frac{27163}{35721}
 =0.760421040844\ldots.
\]

During a single unwrapped passage, a monotone real lift with
`|q'| >= c R^(-2)` spends at most

\[
 O(R)/[cR^{-2}]=O(R^3)
\]

in an interval of width `O(R)`. Relative to the `O(R^2)` window this is
an `O(R)` fraction, formally corresponding to `beta=1` and
`alpha=1/3`. The main note explicitly says that this one-dimensional
kinematic count is not yet an interaction estimate for an arbitrary
diffusing field.

## 5. Pure transport sign, G.21--G.23

Multiplication of
`partial_t H + b(t) partial_2 H = 0` by `xi H` gives

\[
 \frac12\frac d{dt}\int\xi|H|^2
 =\frac12\int b(t)\partial_2\xi|H|^2.
\]

The sign and endpoint difference in G.22--G.23 are correct. With diffusion
restored, the dissipation reappears in the local identity, so using that
identity alone would reproduce the R0.75F circularity. The benchmark is
not used as a proof of G.24.

## 6. Structural and claim audit

- Equation tags G.1--G.24 are unique and consecutive.
- Every internal G-reference resolves to one of those tags.
- G.1 is consistently stated as an unproved sufficient hypothesis.
- G.15 closes only the frozen passive outer-dissipation row, conditionally.
- G.20 is limited to a single unwrapped monotone passage.
- The dynamic, diffusion, geometry, transition, and payment gates are all
  retained.
- G.24, E.24, complete clock, fixed deletion, suitable-weak transfer,
  regularity, and singularity remain open.
- No simulation, numerical fit, novelty, or priority claim is made.

The frozen R0.75G claims are mathematically consistent and ready for a
finite exact certificate. **NOT CLAY.**
