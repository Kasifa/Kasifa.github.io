# Independent primary audit of R0.75D

## 0. Frozen object and verdict

Audited file: research/r075d_passive_gradient_route_screen.md.

Frozen SHA-256:
54bcd703aff9a55f8fff522ded2bf1c5b629ee2497bd4f2255a6224e4bb747f6.

**Verdict: PASS. Mathematical blockers in the stated claims: 0. Release
blockers: 0.**

The note is a route screen, not a closure theorem. Its exact identities and
scale calculations are correct; frequency/cubic separation, localization
commutators, periodic-weight leakage, and the intermediate band are
expressly left conditional or OPEN. No exact counterexample or complete
clock estimate is claimed.

For context, the two immediately used frozen inputs also recompute as

| input | SHA-256 |
|---|---|
| research/r075b_bulk_clock_outer_padding_gate.md | 430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a |
| research/r075c_background_shear_packing_false_positive.md | 1f72f3c9d9d348f86188206690ce714df28aed661a9192c7b53bc1e5921f2f89 |

## 1. Low-frequency Hölder calculation, D.4--D.7

The spatial outer collar has radius \(r\asymp LR\), radial thickness
\(O(R)\), and hence volume \(O(r^2R)=O(L^2R^3)\). Since
\(\lvert I_{2R}\rvert=4R^2\), its spacetime volume is \(O(L^2R^5)\).
Therefore

\[
 \lvert I_{2R}\times {\rm out}\rvert^{1/3}
 \lesssim L^{2/3}R^{5/3},
\]

which is exactly the first factor in D.4. On this collar the frozen
scale-\(2R\) exterior row has \(W_{2R}\geq\omega\), so, provided the
selected piece has the separately stated cubic comparability,

\[
 \int |G|^3\lesssim R^2\omega^{-1}P_R^M.
\]

Raising this inequality to the \(2/3\) power and inserting it into Hölder
gives

\[
 \int |G|^2
 \lesssim L^{2/3}R^3\omega^{-2/3}(P_R^M)^{2/3}.
\]

The Rayleigh inequality D.3 and multiplication by \(\omega/R\) then give

\[
 \frac{\omega}{R}\int|\nabla_{23}G|^2
 \lesssim
 K^2L^{2/3}R^2\omega^{1/3}(P_R^M)^{2/3},
\]

so the coefficient is uniformly bounded precisely at

\[
 K\lesssim R^{-1}L^{-1/3}\omega^{-1/6}=K_{\rm low}.
\]

With

\[
 R=\exp[-(\rho/4)L^2],\qquad
 \omega=\exp[-(c_\gamma/4)L^2],
\]

the exponential rate is

\[
 L^{-2}\log K_{\rm low}
 =\frac{\rho}{4}+\frac{c_\gamma}{24}+o(1)
 =\frac{147163}{476280000}+o(1).
\]

Thus every \(R,L,\omega,K\) power in D.4--D.7 passes. D.3 must be read over
the same spacetime collar as D.4--D.5, or pointwise in time and then
integrated; either interpretation gives the displayed calculation. The
main note correctly warns that \(\int|F|^3\) does not control
\(\int|P_{\leq K}F|^3\) componentwise. Accordingly, it does not promote
this algebra to an unconditional decomposition lemma.

## 2. Horizontal modes and the vertical-frequency obstruction

For

\[
 F(t,x_2,x_3)=\sum_{n\in\mathbb Z}f_n(t,x_3)e^{inx_2},
\]

the passive equation
\(\partial_tF+b(t,x_3)\partial_2F-\Delta_{23}F=0\) gives exactly

\[
 \partial_tf_n-\partial_3^2f_n+(n^2+inb)f_n=0.
\]

Taking the real part of the \(L^2_{x_3}\) pairing with \(f_n\) removes the
purely imaginary potential and yields

\[
 \frac12\frac d{dt}\|f_n\|_2^2
 +\|\partial_3f_n\|_2^2+n^2\|f_n\|_2^2=0.
\]

Hence
\(\|f_n(t)\|_2\leq e^{-n^2(t-s)}\|f_n(s)\|_2\); equivalently, the squared
norm has factor \(e^{-2n^2(t-s)}\). D.8's damping statement is therefore
correct when read as a norm bound.

The horizontal zero mode
\(F_m=e^{-m^2t}\sin(mx_3)\) solves the passive equation for every frozen
shear \(b(t,x_3)\), while its vertical gradient grows like \(m\) relative
to its amplitude. It rigorously shows that horizontal frequency alone
cannot imply the full \(\nabla_{23}\) Rayleigh bound. The note also
correctly observes that a full spatial projection loses invariance under
multiplication by \(b(x_3)\).

## 3. Gradient identities D.10--D.11

Differentiating the passive equation in \(x_3\) gives

\[
 (\partial_t+b\partial_2-\Delta_{23})F_3=-b_3F_2,
\]

so the sign in D.10 is correct. Pairing the original equation with
\(-\Delta_{23}F\), integrating on the periodic \((x_2,x_3)\)-torus, and
using \(b_2=0\) gives

\[
 \frac12\frac d{dt}\|\nabla_{23}F\|_2^2
 +\|\Delta_{23}F\|_2^2
 =-\int b_3F_2F_3.
\]

In particular, the dissipative term is exactly
\(\|\Delta_{23}F\|_2^2\), and the shear term has no sign. Both features in
D.11 pass. The crude frozen bound
\(\|b_3\|_\infty\lesssim B/R=O(R^{-3})\) is also at the stated scale and
is too costly by itself.

For the transition geometry, a fixed \(x_3\)-slice of the radial collar
has area \(O(rR)=O(LR^2)\). Multiplying by an \(O(R)\)-thick transition
band gives

\[
 \lvert{\rm transition}\cap{\rm collar}\rvert=O(LR^3),
\]

whereas the full collar has volume \(O(L^2R^3)\). This verifies the
claimed factor \(L^{-1}\). At positive heat times \(b_3\) is not literally
compactly supported: the statement that its large part is confined to the
bands must be interpreted as a thresholded/core localization with
periodic heat-kernel tails. The note does not use compact support as a
theorem; it explicitly leaves the mixed \(b_3F_2F_3\) estimate OPEN. This
precision issue is thus nonblocking.

## 4. Short blocks and the exact intermediate-band gap

The \(O(R^2)\) clock window contains \(O(R^{-1})\) blocks of duration
\(O(R^3)\). Heat damping on one block becomes strong when

\[
 K^2R^3\gg1\quad\Longleftrightarrow\quad K\gg R^{-3/2}.
\]

The exponential rate of this threshold is \(3\rho/8\), while that of
\(K_{\rm low}\) is \(\rho/4+c_\gamma/24\). With the frozen values
\(\rho=9/10000\) and \(c_\gamma=8/3969\), exact arithmetic gives

\[
 \frac{3\rho}{8}=\frac{27}{80000},\qquad
 \frac{\rho}{4}+\frac{c_\gamma}{24}
 =\frac{147163}{476280000},
\]

and

\[
 \frac{\rho}{8}-\frac{c_\gamma}{24}
 =\boxed{\frac{27163}{952560000}}>0.
\]

This is one half of the B.39 rate
\(\rho/4-c_\gamma/12=27163/476280000\), as it should be. Thus D.12--D.14
correctly identify a genuine nonempty exponential intermediate band
\(K_{\rm low}\ll K\lesssim R^{-3/2}\); no endpoint convention or reversed
inequality is hidden here.

## 5. Exact mixed-cubic fallback, D.16--D.23

Starting from the exact passive energy identity B.14 with
\(\chi=\xi_k^R\), discarding the nonnegative endpoint term and using
\(|\eta_R'|+|\Delta\xi_k^R|\lesssim R^{-2}\) and
\(|\partial_2\xi_k^R|\lesssim R^{-1}\) gives

\[
 D_{k,R}^{{\rm out},F}
 \lesssim \omega R^{-3}\int_{I_{2R}}\int_{\rm out}|F|^2
 +\omega R^{-2}\int_{I_{2R}}\int_{\rm out}|b||F|^2.
\]

For \(p_F,p_b\) as in D.16, the scale-\(2R\) exterior velocity row
indeed gives \(p_F+p_b\lesssim P_R^M\): on the same support
\(W_{2R}\ge\omega\), and
\((F^2+b^2)^{3/2}\ge\max\{|F|^3,|b|^3\}\).

The collar spacetime volume is \(O(L^2R^5)\), so the first right-hand
term is

\[
 \begin{aligned}
 \omega R^{-3}(L^2R^5)^{1/3}
 (R^2\omega^{-1}p_F)^{2/3}
 =L^{2/3}\omega^{1/3}p_F^{2/3}.
 \end{aligned}
\]

For the second, Hölder gives with no residual power of \(R\) or \(\omega\)

\[
 \omega R^{-2}
 (R^2\omega^{-1}p_b)^{1/3}
 (R^2\omega^{-1}p_F)^{2/3}
 =p_b^{1/3}p_F^{2/3}.
\]

This proves D.20. Its \(P_R^M\le1\) corollary is valid because
\(L^{2/3}\omega^{1/3}\) is uniformly bounded on the frozen large-\(L\)
sequence and \(P_R^M\le(P_R^M)^{2/3}\).

The large-payment warning also passes. The upper support-volume bound,
the fixed cap lower bound from R0.75C, \(B\asymp R^{-2}\), and the
\(O(R^2)\) window imply

\[
 p_b\asymp L^2\omega R^{-3}.
\]

Since \(R=e^{-(\rho/4)L^2}\) and
\(\omega=e^{-(c_\gamma/4)L^2}\),

\[
 \lim_{L\to\infty}L^{-2}\log p_b
 =\frac{3\rho-c_\gamma}{4}
 =\boxed{\frac{27163}{158760000}}>0.
\]

Thus \(P_R^M\ge cp_b\to\infty\), so D.21 cannot be invoked on this
branch. Finally,

\[
 p_b^{1/3}p_F^{2/3}\lesssim(P_R^M)^{2/3}
 \quad\Longleftrightarrow\quad
 p_bp_F^2\lesssim(P_R^M)^2,
\]

up to the same absolute constants. D.23 is therefore the exact additional
mixed-payment condition for this absolute-value estimate, and the main
note correctly leaves it OPEN rather than treating the linear fallback as
a proof of B.45.

## 6. Localization, periodization, and claim boundary

The two displayed commutators

\[
 [P_{\leq K},b]\partial_2F,
 \qquad [P_{\leq K},\xi_k^R]F
\]

are the correct obstructions. Bounds for the cutoff commutator involve the
dimensionless gain \((KR)^{-1}\) only in the regime \(KR\gg1\). A global
Fourier projection is nonlocal, so its tails need not remain inside the
outer shell where \(W_{2R}\geq\omega\). On the torus, the projection kernel
and shell cutoff must both retain all periodic copies before any such
lower weight is invoked. The main note states all of these as analytic
blockers and does not silently discard a winding or substitute an
unweighted global energy for the Version-M payment.

The final boundary is accurate:

- D.4--D.7 are scale calculations conditional on a localized Rayleigh
  bound and cubic separation, not an unconditional Littlewood--Paley
  theorem;
- D.8 and D.10--D.13 are exact global identities/calculations;
- D.16--D.22 give an unconditional two-regime fallback, while D.23 is an
  explicitly open interaction gate on the frozen large-payment branch;
- the transition-band mixed estimate, intermediate band,
  cutoff/projection leakage, periodic weights, and any exact counterexample
  remain OPEN;
- failure of the present method is not asserted to be a counterexample;
- no complete-clock, fixed-deletion, suitable-weak, regularity, or
  singularity conclusion is drawn.

Mechanical checks also pass: tags D.1--D.23 are unique and consecutive,
display environments and delimiters balance, references resolve, and the
UTF-8 file contains no CR, NUL, or other nonprinting control character.

**Final verdict: PASS; blocker count: 0.** This audit makes no novelty or
priority claim. \(\mathbf{NOT\ CLAY}\).
