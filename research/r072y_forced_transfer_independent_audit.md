# R0.72Y independent forced-transfer audit

**Date:** 2026-08-28

**Audit outcome:** **PASS** for the causal kernel calculation, the
strong-row \(L_d^2L_x^2\) forcing estimate at scale \(\alpha^2\), the
standard \(L_d^2H^{-1}_{\beta,x}\) forcing estimate at scale \(\alpha\),
the semiclassical \(L_d^2\mathcal H^{-1}_{\alpha,\beta,x}\) estimate at
scale \(\alpha^2\), their energy-space endpoint bounds, and the orthogonal
strong-row direct sum. **PASS** for an \(O_K(1)\) finite-history estimate
on weak and zero-coupling rows. **PASS as negative results** for a standard
\(H^{-1}\) estimate with coefficient \(O(\alpha^2)\), for any vanishing
\(\alpha\)-gain at the \(L_d^\infty L_x^2\) endpoint, and for a uniform
time-global estimate over undamped zero-coupling rows. The pressure-coupled
or triangular linearized subsystem, nonlinear Navier--Stokes closure, and
the Clay problem remain open.

The positive results below concern scalar invariant rows. They do not infer
a bound for an off-diagonal pressure or row-coupling operator that has not
been written and estimated.

---

## 0. Statement and norms under audit

On a compact physical-time interval \(K=[d_-,d_+]\), consider

\[
 \partial_dG
 =\bigl(D_\beta^2-\mu\bigr)G
 -i\sigma\varepsilon W(d,x)G+F,
 \qquad D_\beta=\partial_x+i\beta,
 \tag{0.1}
\]

on the physical \(2\pi\)-circle. Here
\(\sigma\in\{-1,1\}\), \(\mu\ge0\), and a strong row means

\[
 \varepsilon\ge4,
 \qquad
 \alpha=(\varepsilon/4)^{-1/5}\in(0,1].
 \tag{0.2}
\]

The natural covariant negative norm and its semiclassical refinement are

\[
 \|F\|_{H^{-1}_\beta}^2
 =\sum_{n\in\mathbb Z}
 \frac{|F_n|^2}{1+(n+\beta)^2},
 \tag{0.3}
\]

\[
 \|F\|_{\mathcal H^{-1}_{\alpha,\beta}}^2
 =\sum_{n\in\mathbb Z}
 \frac{|F_n|^2}{1+\alpha^2(n+\beta)^2}.
 \tag{0.4}
\]

Their dual positive norms are obtained by replacing the denominators by the
corresponding numerators. If the residue representatives are chosen in a
fixed interval, for example \(|\beta|\le1/2\), then \(H^{-1}_\beta\) and
the ordinary periodic \(H^{-1}\) norm are uniformly equivalent. Keeping
\(\beta\) in the notation avoids an unnecessary equivalence constant.

R0.72X supplies, for fixed \(T>0\), one \(q=q_{K,T}\in(0,1)\) such that
the homogeneous evolution satisfies

\[
 \|U_\alpha(d,s)\|_{2\to2}
 \le e^{-\mu(d-s)}
 q^{\lfloor(d-s)/(2T\alpha^2)\rfloor},
 \qquad d\ge s,\quad d,s\in K.
 \tag{0.5}
\]

All estimates audited below are consequences of (0.5), the scalar energy
identity, and Hilbert-space duality. They do not replace the analytic proof
of (0.5).

---

## 1. Causal kernel and \(L_x^2\)-valued forcing

Put

\[
 h=2T\alpha^2,
 \qquad
 k_\mu(r)=\mathbf1_{r\ge0}e^{-\mu r}q^{\lfloor r/h\rfloor}.
 \tag{1.1}
\]

At zero damping,

\[
 \|k_0\|_{L^1(0,\infty)}
 =\frac{2T\alpha^2}{1-q},
 \qquad
 \|k_0\|_{L^2(0,\infty)}^2
 =\frac{2T\alpha^2}{1-q^2}.
 \tag{1.2}
\]

For \(\mu>0\) and \(p\in[1,\infty)\), the exact damped arithmetic is

\[
 \|k_\mu\|_{L^p}^p
 =\frac{1-e^{-p\mu h}}
 {p\mu\left(1-q^pe^{-p\mu h}\right)}
 \le\frac{h}{1-q^p}.
 \tag{1.3}
\]

The right side of (1.3) is also the \(\mu\downarrow0\) limit. Thus scalar
damping never worsens any kernel estimate.

Let

\[
 A_q=\frac{2T}{1-q},
 \qquad
 B_q=\frac{2T}{1-q^2}.
 \tag{1.4}
\]

For the causal response

\[
 (\mathcal DF)(d)=\int_{d_-}^{d}U_\alpha(d,s)F(s)\,ds,
 \tag{1.5}
\]

Minkowski, Cauchy--Schwarz, and scalar Young convolution give

\[
 \|\mathcal DF\|_{L_d^2L_x^2}
 \le \sqrt{B_q}\,\alpha\|F\|_{L_d^1L_x^2},
 \tag{1.6}
\]

\[
 \|\mathcal DF\|_{L_d^\infty L_x^2}
 \le \|F\|_{L_d^1L_x^2},
 \tag{1.7}
\]

and

\[
 \boxed{
 \|\mathcal DF\|_{L_d^2L_x^2}
 \le A_q\alpha^2\|F\|_{L_d^2L_x^2},}
 \tag{1.8}
\]

\[
 \|\mathcal DF\|_{L_d^\infty L_x^2}
 \le \sqrt{B_q}\,\alpha\|F\|_{L_d^2L_x^2}.
 \tag{1.9}
\]

The estimates remain valid on finite \(K\): extending the scalar majorant
past \(|K|\) only enlarges its \(L^p\) norm and does not assume that the
evolution itself exists with the same constant beyond \(K\).

**Verdict:** PASS. The \(O(\alpha^2)\) spacetime Duhamel statement is an
\(L_x^2\)-forcing statement. Endpoint-concentrated \(L_d^1L_x^2\) forcing
does not inherit that gain.

---

## 2. Adjoint transfer from standard and semiclassical \(H^{-1}\)

Take \(g\in L^2(K;L_x^2)\) and define the backward adjoint response

\[
 z(s)=\int_s^{d_+}U_\alpha(d,s)^*g(d)\,dd.
 \tag{2.1}
\]

Since
\(\|U_\alpha(d,s)^*\|=\|U_\alpha(d,s)\|\), (1.8) applied backward gives

\[
 \|z\|_{L_d^2L_x^2}
 \le A_q\alpha^2\|g\|_{L_d^2L_x^2}.
 \tag{2.2}
\]

The backward energy identity is

\[
 \frac12\|z(d_-)\|_2^2
 +\|D_\beta z\|_{L_d^2L_x^2}^2
 +\mu\|z\|_{L_d^2L_x^2}^2
 =\operatorname{Re}\int_K(g,z)\,dd.
 \tag{2.3}
\]

Consequently

\[
 \|D_\beta z\|_{L_d^2L_x^2}
 \le\sqrt{A_q}\,\alpha\|g\|_{L_d^2L_x^2}.
 \tag{2.4}
\]

With

\[
 C_q=\sqrt{A_q^2+A_q},
 \tag{2.5}
\]

(2.2)--(2.4) yield the two distinct positive-norm estimates

\[
 \|z\|_{L_d^2H^1_\beta}
 \le C_q\alpha\|g\|_{L_d^2L_x^2},
 \tag{2.6}
\]

\[
 \|z\|_{L_d^2\mathcal H^1_{\alpha,\beta}}
 \le C_q\alpha^2\|g\|_{L_d^2L_x^2}.
 \tag{2.7}
\]

For the zero-initial forward variational solution, integration of
\((G,z)\) gives the exact transposition identity

\[
 \int_K(G,g)\,dd
 =\int_K\langle F,z\rangle\,dd.
 \tag{2.8}
\]

Dualizing (2.6) and (2.7) proves

\[
 \boxed{
 \|G\|_{L_d^2L_x^2}
 \le C_q\alpha
 \|F\|_{L_d^2H^{-1}_\beta},}
 \tag{2.9}
\]

\[
 \boxed{
 \|G\|_{L_d^2L_x^2}
 \le C_q\alpha^2
 \|F\|_{L_d^2\mathcal H^{-1}_{\alpha,\beta}}.}
 \tag{2.10}
\]

The elementary weight comparison

\[
 \frac1{1+\alpha^2\xi^2}
 \le\frac{\alpha^{-2}}{1+\xi^2},
 \qquad
 \alpha^2(1+\xi^2)\le1+\alpha^2\xi^2,
 \tag{2.11}
\]

shows directly that (2.10) implies (2.9), but the adjoint calculation also
exhibits where the lost factor occurs: the adjoint derivative costs one
power of \(\alpha^{-1}\) relative to its \(L^2\) norm.

No Christ--Kiselev lemma is used. No pointwise extension
\(U(d,s):H^{-1}\to L^2\) is assumed. The retarded operator is defined first
for smooth \(L_x^2\)-valued forcing and then extended by (2.9) or (2.10).

**Verdict:** PASS. The standard negative norm has coefficient
\(O(\alpha)\); the semiclassical negative norm has coefficient
\(O(\alpha^2)\).

---

## 3. Functional-analytic trace and approximation audit

For each fixed row and fixed \(\alpha>0\), multiplication by the real smooth
function \(\varepsilon W(d,\cdot)\) is a bounded skew perturbation on
\(L_x^2\), continuous in \(d\in K\). The covariant diffusion form is
coercive in real part. Standard Galerkin or Lions variational theory
therefore gives, for \(F\in L^2(K;H^{-1}_\beta)\),

\[
 G\in L^2(K;H^1_\beta),
 \qquad
 \partial_dG\in L^2(K;H^{-1}_\beta),
 \qquad
 G\in C(K;L_x^2).
 \tag{3.1}
\]

The last inclusion is the Hilbert-triple trace theorem. It is not a
consequence of maximal graph membership alone. Steklov averaging or
Galerkin limits justify the forward and backward energy identities and
(2.8).

An explicit density route is also available. Approximate \(F\) in
\(L^2H^{-1}_\beta\) by smooth \(F_m\). Apply (2.9) and the forced energy
estimate to differences of the corresponding smooth solutions. This makes
the solutions Cauchy in \(L^2H^1_\beta\cap C L^2\); the limit satisfies
(0.1) distributionally and preserves the energy identity. For fixed
\(\alpha\), the semiclassical and standard negative norms are equivalent,
so the same construction applies to (2.10).

The coefficient of the potential is not uniform as \(\alpha\downarrow0\),
but existence is rowwise for every fixed \(\alpha\). Uniformity of the final
estimates comes from (0.5) and the skew energy identity, not from a uniform
bounded-perturbation constant.

**Verdict:** PASS analytically. Time traces, variational existence, and the
adjoint integration-by-parts step are not finite-arithmetic claims.

---

## 4. Endpoint and energy-space bounds

Apply (2.9) on every prefix \([d_-,t]\subset K\). If

\[
 Y=\|G\|_{L_d^2L_x^2},
 \quad
 D=\|D_\beta G\|_{L_d^2L_x^2},
 \quad
 \mathcal F=\|F\|_{L_d^2H^{-1}_\beta},
 \tag{4.1}
\]

the forward zero-initial energy identity and (2.9) give

\[
 D^2
 \le \mathcal F\sqrt{Y^2+D^2}
 \le \mathcal F(Y+D)
 \le C_q\alpha\mathcal F^2+\mathcal F D.
 \tag{4.2}
\]

Put

\[
 r_q=\frac{1+\sqrt{1+4C_q}}2.
 \tag{4.3}
\]

and define

\[
 C_q'=\max\left\{
 r_q,\sqrt{2(C_q+r_q)}
 \right\}.
 \tag{4.4}
\]

Since \(0<\alpha\le1\), (4.2) implies the joint estimate

\[
 \max\left\{
 \|D_\beta G\|_{L_d^2L_x^2},
 \|G\|_{L_d^\infty L_x^2}
 \right\}
 \le C_q'\mathcal F.
 \tag{4.5}
\]

Pairing instead in
\(\mathcal H^{-1}_{\alpha,\beta}\)--\(\mathcal H^1_{\alpha,\beta}\)
and using (2.10) gives

\[
 \max\left\{
 \|D_\beta G\|_{L_d^2L_x^2},
 \|G\|_{L_d^\infty L_x^2}
 \right\}
 \le C_q'\alpha
 \|F\|_{L_d^2\mathcal H^{-1}_{\alpha,\beta}}.
 \tag{4.6}
\]

The positive damping term was discarded, so the constants are uniform for
all \(\mu\ge0\). For nonzero initial data, linear superposition and the
R0.72X homogeneous integrated bound give

\[
 \|G\|_{L_d^2L_x^2}
 \le\sqrt{B_q}\,\alpha\|G(d_-)\|_2
 +C_q\alpha\|F\|_{L_d^2H^{-1}_\beta},
 \tag{4.7}
\]

or the \(C_q\alpha^2\mathcal H^{-1}_{\alpha,\beta}\) forced term.

**Verdict:** PASS. Standard \(H^{-1}\) forcing has an \(O(1)\) endpoint
bound, not an \(O(\alpha)\) endpoint bound. The semiclassical norm carries
one endpoint power of \(\alpha\), not two.

---

## 5. Sharpness of the two spacetime exponents

The distinction between (2.9) and (2.10) is not an artifact of (2.11).
It can be realized inside the exact collision family.

Choose a nonzero even
\(\eta\in C_c^\infty(\mathbb R)\), put \(\psi=\eta''\), and choose a
nonzero \(\chi\in C_c^\infty((-T,T))\). Then \(\psi\) is even and
\(\int\psi=0\). For sufficiently small \(\alpha\), periodize the compactly
supported function on \(\mathbb T_\alpha\) and define

\[
 w_\alpha(S,X)=\chi(S)\psi(X),
 \tag{5.1}
\]

\[
 f_\alpha
 =(\partial_S-i\sigma V_\alpha)w_\alpha
 -\partial_X^2w_\alpha.
 \tag{5.2}
\]

The exact potential is odd in \(X\). Hence every term in (5.2) has zero
spatial mean: the derivative terms do so by construction, and
\(V_\alpha\psi\) is odd. On the fixed support,
\(V_\alpha\to H_3=X^3+6SX\) smoothly. Thus \(w_\alpha\) converges to a
nonzero fixed profile and \(f_\alpha\) converges in \(L^2_SH^{-1}_X\) to
a finite nonzero mean-zero profile. The limit forcing cannot vanish: that
would make the compact-time, zero-initial \(w_0\) a nonzero homogeneous
parabolic solution, contradicting uniqueness.

Return to physical variables with \(\varepsilon=4\alpha^{-5}\):

\[
 G_\alpha(d,x)=w_\alpha(d/\alpha^2,x/\alpha),
 \qquad
 F_\alpha(d,x)=\alpha^{-2}
 f_\alpha(d/\alpha^2,x/\alpha).
 \tag{5.3}
\]

The state scaling is exact:

\[
 \|G_\alpha\|_{L_d^2L_x^2}^2
 =\alpha^3\|w_\alpha\|_{L_S^2L_X^2}^2.
 \tag{5.4}
\]

The scaled and physical semiclassical Fourier coefficients give the exact
norm relation

\[
 \|F_\alpha\|_{L_d^2\mathcal H^{-1}_{\alpha,0}}^2
 =\alpha^{-1}
 \|f_\alpha\|_{L_S^2H^{-1}(\mathbb T_\alpha)}^2.
 \tag{5.5}
\]

Therefore

\[
 \frac{\|G_\alpha\|_{L_d^2L_x^2}}
 {\|F_\alpha\|_{L_d^2\mathcal H^{-1}_{\alpha,0}}}
 \sim c_{\rm sc}\alpha^2,
 \qquad c_{\rm sc}>0.
 \tag{5.6}
\]

Because \(f_\alpha\) is mean-zero and compactly supported in the scaled
coordinate, Fourier Riemann-sum convergence also gives

\[
 \|F_\alpha\|_{L_d^2H^{-1}}^2
 \sim\alpha
 \|f_0\|_{L_S^2\dot H^{-1}(\mathbb R)}^2,
 \tag{5.7}
\]

and hence

\[
 \frac{\|G_\alpha\|_{L_d^2L_x^2}}
 {\|F_\alpha\|_{L_d^2H^{-1}}}
 \sim c_{\rm std}\alpha,
 \qquad c_{\rm std}>0.
 \tag{5.8}
\]

This witness is zero-initial and mean-zero. It proves that neither an extra
mean-zero hypothesis nor a different use of the energy identity can improve
the standard \(H^{-1}\) coefficient from \(\alpha\) to \(\alpha^2\).
Recovering \(\alpha^2\) requires \(L_x^2\) forcing, an equivalent extra
spatial regularity assumption, or the explicit semiclassical weight (0.4).

**Verdict:** standardHMinusOneTransferAlpha2 is FALSE. The powers in
(2.9) and (2.10) are sharp for the exact collision family.

---

## 6. Endpoint counterexample

Fix any strong row, take \(\beta=\mu=0\), and let
\(e_N(x)=(2\pi)^{-1/2}e^{iNx}\). On the terminal interval of length
\(N^{-2}\), set

\[
 F_N(d,x)=N^2\mathbf1_{[d_+-N^{-2},d_+]}(d)e_N(x).
 \tag{6.1}
\]

Then

\[
 \|F_N\|_{L_d^2H_x^{-1}}
 =\frac{N}{\sqrt{1+N^2}}\longrightarrow1.
 \tag{6.2}
\]

For the heat equation, the endpoint response is exactly

\[
 \left(1-e^{-1}\right)e_N.
 \tag{6.3}
\]

For the full row, let
\(M_\alpha=\varepsilon\sup_K\|W(d,\cdot)\|_\infty\). Duhamel comparison
between the full homogeneous propagator and the heat propagator gives

\[
 \|U_\alpha(d,s)-e^{(d-s)\partial_x^2}\|_{2\to2}
 \le M_\alpha(d-s),
 \tag{6.4}
\]

because both outer propagators are \(L^2\) contractions and the potential is
a bounded skew multiplier. Integrating (6.4) against (6.1) bounds the
endpoint error by

\[
 \frac{M_\alpha}{2N^2}.
 \tag{6.5}
\]

For each \(\alpha\), choose \(N^2\gg M_\alpha\). The endpoint response then
has a positive lower bound independent of \(\alpha\). Thus no estimate of
the form

\[
 \|G(d_+)\|_2\le o_{\alpha\downarrow0}(1)
 \|F\|_{L_d^2H_x^{-1}}
 \tag{6.6}
\]

can hold. The same conclusion for
\(L_d^1L_x^2\to L_d^\infty L_x^2\) follows directly from strong continuity
and a normalized approximate time delta.

**Verdict:** HMinusOneEndpointAlphaGain is FALSE. The \(O(1)\) standard
\(H^{-1}\) endpoint bound in Section 4 has the correct uniform scale.

---

## 7. Orthogonal strong-row direct sum

For invariant orthogonal rows, let

\[
 \varepsilon_j\ge4,
 \qquad
 \alpha_j=(\varepsilon_j/4)^{-1/5}.
 \tag{7.1}
\]

Squaring (2.9), summing, and using Tonelli gives

\[
 \boxed{
 \sum_j\|G_j\|_{L_d^2L_x^2}^2
 \le C_q^2\sum_j\alpha_j^2
 \|F_j\|_{L_d^2H^{-1}_{\beta_j}}^2.}
 \tag{7.2}
\]

The semiclassical version is

\[
 \sum_j\|G_j\|_{L_d^2L_x^2}^2
 \le C_q^2\sum_j\alpha_j^4
 \|F_j\|_{L_d^2\mathcal H^{-1}_{\alpha_j,\beta_j}}^2.
 \tag{7.3}
\]

If \(\varepsilon_j\ge\varepsilon_{\min}\ge4\), then

\[
 \alpha_j\le\alpha_{\max}
 =(\varepsilon_{\min}/4)^{-1/5},
 \tag{7.4}
\]

so (7.2) has the common factor \(C_q\alpha_{\max}\) and no row-count
loss. Endpoint estimates also sum without a row-count factor by first
proving them for finite truncations and passing to the monotone limit.

For an infinite family, rowwise existence plus (7.2) makes the finite
truncations Cauchy. This establishes an orthogonal direct-sum solution in
the energy topology. It does not establish that an unbounded off-diagonal
pressure operator is defined on that topology.

If a coupled system has \(F=\mathcal BG+H\), a sufficient absorption gate in
the standard norm would be an actual proof of

\[
 C_q\left\|\operatorname{diag}(\alpha_j)\mathcal B\right\|
 _{L_d^2\ell^2L_x^2\to L_d^2\ell^2H^{-1}_{\beta,x}}<1.
 \tag{7.5}
\]

A finite nilpotent triangular system could instead be iterated with explicit
product constants. Neither property follows from the scalar estimates, and
the full physical coefficients have not been audited here.

**Verdict:** strongForcedDirectSumNoCountLoss is CLOSED for decoupled
invariant rows. completeLinearizedShearSubsystem remains OPEN.

---

## 8. Weak and zero-coupling rows

When \(0\le\varepsilon<4\), the R0.72X strong-family theorem is not invoked.
The skew potential nevertheless drops out of the scalar energy identity.
For a zero-initial variational solution, write

\[
 E(d)=\|G(d)\|_2^2,
 \qquad
 D(d)=\|D_\beta G(d)\|_2.
 \tag{8.1}
\]

The pointwise dual estimate

\[
 2|\langle F,G\rangle|
 \le\|F\|_{H^{-1}_\beta}^2
 +\|G\|_{H^1_\beta}^2
 \tag{8.2}
\]

gives

\[
 E'(d)+D(d)^2
 \le\|F(d)\|_{H^{-1}_\beta}^2+E(d).
 \tag{8.3}
\]

If \(L=|K|\), Gronwall and integration of (8.3) yield

\[
 \sup_{d\in K}E(d)
 \le e^L\|F\|_{L_d^2H^{-1}_\beta}^2,
 \tag{8.4}
\]

\[
 \|G\|_{L_d^2L_x^2}
 \le\sqrt{Le^L}\|F\|_{L_d^2H^{-1}_\beta},
 \tag{8.5}
\]

\[
 \|D_\beta G\|_{L_d^2L_x^2}^2
 \le(1+Le^L)\|F\|_{L_d^2H^{-1}_\beta}^2.
 \tag{8.6}
\]

These are finite-history bounds. They contain no enhanced-dissipation
gain and remain valid for every coupling size because only skewness was
used.

There is a time-global alternative when diffusion or damping has a genuine
gap. Put

\[
 \rho=\operatorname{dist}(\beta,\mathbb Z),
 \qquad
 \gamma_{\rho,\mu}
 =\min\left\{1,\frac{\rho^2+\mu}{1+\rho^2}\right\}.
 \tag{8.7}
\]

Poincare's inequality gives

\[
 \|D_\beta G\|_{L_d^2L_x^2}^2
 +\mu\|G\|_{L_d^2L_x^2}^2
 \ge\gamma_{\rho,\mu}\|G\|_{L_d^2H^1_\beta}^2.
 \tag{8.8}
\]

Hence, if \(\rho^2+\mu>0\),

\[
 \|G\|_{L_d^2H^1_\beta}
 \le\gamma_{\rho,\mu}^{-1}
 \|F\|_{L_d^2H^{-1}_\beta}.
 \tag{8.9}
\]

At \(\varepsilon=\beta=\mu=0\), the normalized spatial constant reduces
the equation to \(a'=f\). On \([0,L]\), take
\(f=L^{-1/2}\). The input \(L_d^2H_x^{-1}\) norm is one, while

\[
 \|a\|_{L^2(0,L)}=\frac{L}{\sqrt3}.
 \tag{8.10}
\]

Thus no time-uniform zero-row estimate exists, and the homogeneous spatial
constant is an exact nondecaying mode.

A mean-zero hypothesis at \(\beta=0\) is not by itself an invariant
restriction when \(\varepsilon W\ne0\): multiplication by \(W\) generally
creates a nonzero mean. Mean-zero Poincare may be used only for the heat
row or for an equation whose projection onto the mean-zero subspace is
explicitly part of the operator.

For a decoupled finite-history ledger one may set

\[
 \omega_j=
 \begin{cases}
  \alpha_j,&\varepsilon_j\ge4,\\
  1,&0\le\varepsilon_j<4,
 \end{cases}
 \tag{8.11}
\]

and combine (2.9) with (8.5) in \(\ell^2\), with a constant depending on
\(K,T,q\) but not on the row count.

**Verdict:** weakZeroFiniteHistoryEnergyLedger is CLOSED.
allRowsStrongScaleForcedGain is FALSE. A sharper weak nonzero-coupling
enhanced-dissipation rate at \(\beta=\mu=0\) remains OPEN.

---

## 9. Finite-certificate and analytic boundaries

The following parts reduce to finite algebra and are suitable for a
deterministic certificate:

1. the geometric sums in (1.2) and the damped identity (1.3);
2. the powers
   \(\alpha=(\varepsilon/4)^{-1/5}\) and
   \(\alpha^2=(\varepsilon/4)^{-2/5}\);
3. the weight inequality (2.11);
4. positivity and substitution checks for
   \(A_q,B_q,C_q,r_q\);
5. the row weights in (7.2), (7.3), and (8.11);
6. the exact zero-coupling constant-mode calculation (8.10);
7. finite-\(\alpha\), finite-Fourier evaluations of the two sharpness
   witnesses, as diagnostics rather than proofs of their limits.

The following steps remain analytic and must not be represented as
finite-certified:

1. construction of the nonautonomous variational evolution and its backward
   adjoint;
2. the Hilbert-triple endpoint trace in (3.1), Steklov/Galerkin energy
   identities, and the transposition identity (2.8);
3. density passage from smooth forcing to \(L^2H^{-1}\);
4. finite-truncation convergence for an infinite orthogonal row sum;
5. smooth local convergence \(V_\alpha\to H_3\) and the Fourier
   Riemann-sum limit (5.7);
6. the already established compactness proof behind the all-start
   semigroup (0.5).

The endpoint counterexample (6.1)--(6.5) has a finite Fourier core, but its
uniform conclusion still uses the analytic contraction/Duhamel comparison.

---

## 10. Final claim ledger

| Claim | Audit status | Exact scope |
|---|---|---|
| strongRowL2ForcingDuhamelAlpha2 | **CLOSED** | Scalar invariant strong rows; \(L_d^2L_x^2\) forcing |
| strongRowStandardHMinusOneTransferAlpha | **CLOSED** | Zero-initial scalar strong rows; standard covariant \(H^{-1}\) |
| strongRowSemiclassicalHMinusOneTransferAlpha2 | **CLOSED** | Zero-initial scalar strong rows; norm (0.4) |
| strongRowForcedEndpointStandardScaleOne | **CLOSED** | \(L_d^\infty L_x^2\) and energy-space bound |
| strongForcedDirectSumNoCountLoss | **CLOSED** | Decoupled invariant strong rows only |
| weakZeroFiniteHistoryEnergyLedger | **CLOSED** | \(O_K(1)\), without an ED gain |
| standardHMinusOneTransferAlpha2 | **FALSE** | Refuted even by zero-initial mean-zero forcing |
| HMinusOneEndpointAlphaGain | **FALSE** | High-frequency terminal pulse |
| allRowsStrongScaleForcedGain | **FALSE** | Zero/weak rows have no common strong scale |
| allPhysicalRowsUniformContraction | **FALSE** | Undamped zero-coupling constant mode |
| weakNonzeroUniformEnhancedDissipation | **OPEN** | Especially \(\beta=\mu=0\) below the strong threshold |
| completeLinearizedShearSubsystem | **OPEN** | Pressure/off-diagonal operator not controlled |
| nonlinearNavierStokes | **OPEN** | No nonlinear convolution or vortex-stretching bootstrap |
| Clay regularity problem | **OPEN** | No global regularity or blow-up theorem follows |

The generic label **forcedHMinusOneTransfer** is too ambiguous to freeze by
itself. It should be split by spatial norm and target topology: standard
\(H^{-1}\to L_d^2L_x^2\) closes at \(\alpha\), semiclassical
\(\mathcal H^{-1}_\alpha\to L_d^2L_x^2\) closes at \(\alpha^2\), and the
standard endpoint closes only at scale one. These scalar results are a
linear input for the next row-coupling audit, not a Navier--Stokes
regularity result.
