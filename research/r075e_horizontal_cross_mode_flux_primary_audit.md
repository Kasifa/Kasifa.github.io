# Independent primary audit of R0.75E

## 0. Frozen object and verdict

Audited file:
`research/r075e_horizontal_cross_mode_flux_reduction.md`.

Frozen SHA-256:
`99529b8934412775e19a1b70784cddf3e62190b50c42669ccd34135a134c5049`.

**Verdict: PASS. Mathematical blocker count: 0. Release blocker count: 0.**

The note proves a localized spectral identity and a strict invariant-sector
lemma. It does not claim the arbitrary-field cross-mode bound E.24. The
complex singleton is kept as an algebraic diagnostic and is not promoted
to a real Navier--Stokes velocity.

The three frozen inputs recompute as

| input | SHA-256 |
|---|---|
| `research/r075b_bulk_clock_outer_padding_gate.md` | `430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a` |
| `research/r075c_background_shear_packing_false_positive.md` | `1f72f3c9d9d348f86188206690ce714df28aed661a9192c7b53bc1e5921f2f89` |
| `research/r075d_passive_gradient_route_screen.md` | `54bcd703aff9a55f8fff522ded2bf1c5b629ee2497bd4f2255a6224e4bb747f6` |

## 1. Local energy sign and endpoint, E.6--E.8

For complex \(F\), taking the real part gives

\[
 \operatorname {Re}(\overline F\,\partial_tF)
 =\frac12\partial_t|F|^2,
 \qquad
 \operatorname {Re}(\overline F\,\partial_2F)
 =\frac12\partial_2|F|^2.
\]

Thus the time cutoff contributes the right-hand row
\(\frac12\int\eta_R'\xi|F|^2\). The diffusion integration by parts gives

\[
 -\operatorname {Re}\int\eta_R\xi\overline F\Delta_{23}F
 =\int\eta_R\xi|\nabla_{23}F|^2
 -\frac12\int\eta_R\Delta_{23}\xi|F|^2.
\]

The transport contribution on the left is

\[
 \operatorname {Re}\int\eta_R\xi b\overline F\partial_2F
 =-\frac12\int\eta_Rb\partial_2\xi|F|^2.
\]

Moving the last two signed cutoff rows to the right gives exactly E.6--E.8,
including the positive sign of E.7 on the right. Since
\(\eta_R(s_R)=0\) and \(\eta_R(t_2)=1\), only the terminal endpoint remains.
It is nonnegative and may be dropped only for the stated upper estimate.

## 2. Fourier normalization and the factor pi, E.9--E.11

With the \(1/(2\pi)\) convention in E.5,

\[
 F=\sum_nf_ne^{inx_2},\qquad
 |F|^2=\sum_{n,m}f_n\overline{f_m}e^{i(n-m)x_2},
\]

and

\[
 \partial_2\xi
 =\sum_{\ell}i\ell\widehat\xi_\ell e^{i\ell x_2}.
\]

The \(x_2\) integral is zero unless
\(\ell+n-m=0\), so \(\ell=m-n\), and the surviving period integral is
\(2\pi\). E.7 already contains \(1/2\); therefore

\[
 \frac12(2\pi)=\pi,
\]

which is exactly the prefactor in E.10. There is no missing second factor
of \(1/2\). Integrating \(\widehat\xi_{m-n}\) in \(x_1\) produces
\(\Xi_{m-n}\) because \(F\) and \(b\) are independent of \(x_1\). Taking
the real part is necessary for the complexified calculation and redundant
but harmless for a real field.

Every diagonal term has \(m-n=0\), hence multiplier zero. E.11 follows
without an estimate or a limiting argument: the localized transport row
is exactly off diagonal in horizontal frequency.

## 3. Invariance and the sharp zero-flux condition, E.9--E.13

Substitution of \(f_ne^{inx_2}\) into E.1 gives

\[
 \partial_tf_n-\partial_3^2f_n+(n^2+inb)f_n=0.
\]

No other horizontal index occurs because \(b=b(t,x_3)\). Uniqueness of
the smooth linear parabolic problem preserves every initially vanishing
mode. Consequently it is legitimate to use one fixed support set \(S\)
throughout the time interval.

The condition in E.12 is sufficient even though it is imposed only on the
\(x_1\)-averaged coefficient \(\Xi_\ell\). Indeed, after the \(x_1\)
integration in E.10 there is no remaining \(x_1\)-dependent factor from
the solution. Requiring the stronger pointwise condition
\(\widehat\xi_\ell(x_1,x_3)=0\) would be unnecessary.

When \(S=\{0\}\), the conclusion can also be checked before Fourier
expansion:

\[
 \int_{-\pi}^{\pi}\partial_2\xi(x_1,x_2,x_3)|f_0(x_3)|^2\,dx_2=0.
\]

This is a real invariant sector. If the frozen Version-M inversion pairing
is required, odd \(f_0(x_3)\), including arbitrarily high vertical sine
modes, supplies admissible examples.

For a complex singleton \(S=\{n\}\),
\(|f_ne^{inx_2}|^2=|f_n|^2\), and the same cancellation holds. The main
note correctly labels this only as a complexified scalar diagnostic.

## 4. Scaling audit, E.14--E.16

The outer collar has spatial volume \(O(L^2R^3)\), and the frozen interval
has length \(O(R^2)\), so the spacetime volume is \(O(L^2R^5)\). Hölder and
the definition of \(p_F\) give

\[
 \begin{aligned}
 \int_{I_{2R}}\!\int_{\operatorname {supp}\xi}|F|^2
 &\le C(L^2R^5)^{1/3}
 \left(R^2\omega^{-1}p_F\right)^{2/3}\\
 &=CL^{2/3}R^3\omega^{-2/3}p_F^{2/3}.
 \end{aligned}
\]

Multiplication by the time/Laplacian cutoff prefactor
\(\omega R^{-3}\) cancels every power of \(R\) and leaves

\[
 CL^{2/3}\omega^{1/3}p_F^{2/3}.
\]

The scale-\(2R\) exterior cubic row gives \(p_F\le CP_R^M\). Since
\(\omega=\exp[-(c_\gamma/4)L^2]\),

\[
 L^{2/3}\omega^{1/3}
 =L^{2/3}\exp[-(c_\gamma/12)L^2]\to0.
\]

Hence E.2 and E.15 are uniform for \(L\ge L_0\) and require no assumption
that \(P_R^M\le1\). This is the exact improvement over the general
R0.75D fallback within the zero-flux sector.

## 5. Real harmonic boundary, E.17--E.20

Reality imposes \(f_{-n}=\overline{f_n}\). Expanding
\(F=a\cos(nx_2)+c\sin(nx_2)\) gives exactly

\[
 F^2=\frac{a^2+c^2}{2}
 +\frac{a^2-c^2}{2}\cos(2nx_2)+ac\sin(2nx_2).
\]

Thus a nonzero real harmonic has difference frequencies \(\pm2n\), which
can couple to \(\Xi_{\pm2n}\). For an \(x_2\)-even cutoff,
\(\partial_2\xi\) is odd: the cosine row cancels, but the sine row need not.
So even radial parity does not create a universal real-single-harmonic
cancellation.

Direct differentiation gives

\[
 b\partial_2F=nb(c\cos(nx_2)-a\sin(nx_2)),
\]

and therefore the two signs in E.20, \(+nbc\) in the cosine equation and
\(-nba\) in the sine equation, are correct. A pure cosine phase is not
generally invariant under a nonzero shear.

## 6. Normalized remaining gate, E.21--E.24

E.10 contains

\[
 \mathcal T_\xi=\pi\operatorname {Re}\sum_{n\ne m}(\cdots).
\]

The dissipation target is the energy identity multiplied by \(\omega/R\).
Therefore its positive transport contribution is exactly

\[
 \frac{\omega}{R}[\mathcal T_\xi]_+
 =\frac{\pi\omega}{R}
 [\operatorname {Re}\sum_{n\ne m}(\cdots)]_+,
\]

which confirms the prefactor in E.21. Combining it with the already-paid
time/Laplacian rows proves E.22.

Using \(|\partial_2\xi|\le CR^{-1}\) yields

\[
 \mathfrak X_{\xi,R}
 \le C\omega R^{-2}\int|b||F|^2
 \le Cp_b^{1/3}p_F^{2/3},
\]

so E.23 has the correct powers and normalization. Cubing this last
quantity shows why the R0.75D sufficient gate is
\(p_bp_F^2\lesssim(P_R^M)^2\). The new signed quantity is strictly more
structured: it omits all diagonal modal mass, but no general estimate E.24
has yet been proved.

## 7. Structural and claim audit

- Equation tags E.1--E.24 are unique and consecutive.
- Every internal E-reference resolves to one of those tags.
- The spherical cutoff's \(x_2\) dependence and the \(x_1\) averaging are
  retained.
- The real zero mode, complex singleton, and real \(\pm n\) pair are not
  conflated.
- No simulation, DNS, exact counterexample, complete-clock estimate,
  suitable-weak transfer, regularity theorem, singularity theorem, novelty,
  or priority claim is made.
- E.24 and all downstream Clay implications remain explicitly open.

The frozen R0.75E claims are mathematically consistent and ready for a
finite certificate. **NOT CLAY.**
