# R0.75F -- modal phase-integration identity and diagonal-control no-go

## 0. Result and exact boundary

R0.75E identifies the remaining passive outer-collar term as a signed
off-diagonal horizontal Fourier flux. The first natural attempt is to use
the oscillatory factor \(i(m-n)b\) and the modal evolution to integrate
that flux by parts in time.

The attempt has an exact outcome:

\[
 \boxed{
 \mathcal T_\xi
 =\mathcal E_{\rm off}
  -\mathcal A_{\rm off}
  +\mathcal D_{\rm off}.}
 \tag{F.1}
\]

These are precisely the off-diagonal endpoint, cutoff, and dissipation
parts of the original local energy identity. Substitution of (F.1) into
that identity cancels every off-diagonal term and leaves only the already
known diagonal modal energy identity. Hence:

\[
 \boxed{\text{direct modal phase integration without an additional
 coercive estimate gives no new bound.}}
 \tag{F.2}
\]

There is also no uniform comparison between a localized quadratic form and
its Fourier-diagonal part based only on nonnegativity and boundedness of the
cutoff. A finite real Fejér-type family gives an exact ratio

\[
 \frac{2N+N^{-1}}3\longrightarrow\infty.
 \tag{F.3}
\]

This is a proof-route no-go, not a counterexample to the R0.75E target.
It does not rule out enhanced-dissipation, resolvent, pathwise, uncertainty,
or payment-sensitive estimates that add genuine information.

## 1. Frozen inputs

| input | SHA-256 | role |
|---|---|---|
| research/r075b_bulk_clock_outer_padding_gate.md | 430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a | localized Caccioppoli identity |
| research/r075e_horizontal_cross_mode_flux_reduction.md | 99529b8934412775e19a1b70784cddf3e62190b50c42669ccd34135a134c5049 | horizontal coefficients and signed flux |

Retain the R0.75E notation

\[
 \ell=m-n,\qquad
 g_{nm}:=f_n\overline{f_m},\qquad
 \Xi_\ell(x_3)
 =\int_{\mathbb T_{x_1}}\widehat\xi_\ell(x_1,x_3)\,dx_1.
 \tag{F.4}
\]

All sums below are justified for the frozen smooth periodic fields. The
time interval is \([s_R,t_2]\), the cutoff \(\eta_R\) vanishes at \(s_R\)
and equals one at \(t_2\), and primes on \(f_n,\Xi_\ell\) mean
\(\partial_3\).

## 2. Exact modal-product equation

The mode equation and its conjugate are

\[
 \begin{aligned}
 \partial_tf_n
 &=f_n''-n^2f_n-inbf_n,\\
 \partial_t\overline{f_m}
 &=\overline{f_m}''-m^2\overline{f_m}
   +imb\overline{f_m}.
 \end{aligned}
 \tag{F.5}
\]

Therefore

\[
 \partial_tg_{nm}
 =f_n''\overline{f_m}+f_n\overline{f_m}''
 -(n^2+m^2)g_{nm}
 +i(m-n)bg_{nm}.
 \tag{F.6}
\]

Since

\[
 g_{nm}''
 =f_n''\overline{f_m}
  +2f_n'\overline{f_m}'
  +f_n\overline{f_m}'',
 \tag{F.7}
\]

the shear phase satisfies the exact identity

\[
 \boxed{
 i\ell b g_{nm}
 =\partial_tg_{nm}-g_{nm}''
  +2f_n'\overline{f_m}'
  +(n^2+m^2)g_{nm}.}
 \tag{F.8}
\]

No division by \(b\) or \(\ell\) occurs. In particular, (F.8) remains a
valid algebraic identity at shear zeros and is not yet an oscillatory
estimate.

## 3. Diagonal and off-diagonal quadratic forms

Define the terminal endpoint forms

\[
 \begin{aligned}
 \mathcal E_{\rm diag}
 &:=\pi\sum_n\int_{\mathbb T_{x_3}}
 \Xi_0|f_n(t_2)|^2\,dx_3,\\
 \mathcal E_{\rm off}
 &:=\pi\operatorname {Re}\sum_{n\ne m}
 \int_{\mathbb T_{x_3}}
 \Xi_\ell g_{nm}(t_2)\,dx_3.
 \end{aligned}
 \tag{F.9}
\]

The cutoff rows are

\[
 \begin{aligned}
 \mathcal A_{\rm diag}
 &:=\pi\sum_n\int_{s_R}^{t_2}\!\int
 [\eta_R'\Xi_0+\eta_R\Xi_0'']|f_n|^2\,dx_3dt,\\
 \mathcal A_{\rm off}
 &:=\pi\operatorname {Re}\sum_{n\ne m}
 \int_{s_R}^{t_2}\!\int
 [\eta_R'\Xi_\ell
  +\eta_R(\Xi_\ell''-\ell^2\Xi_\ell)]g_{nm}\,dx_3dt.
 \end{aligned}
 \tag{F.10}
\]

The dissipation forms are

\[
 \begin{aligned}
 \mathcal D_{\rm diag}
 &:=2\pi\sum_n\int_{s_R}^{t_2}\!\int
 \eta_R\Xi_0
 (|f_n'|^2+n^2|f_n|^2)\,dx_3dt,\\
 \mathcal D_{\rm off}
 &:=2\pi\operatorname {Re}\sum_{n\ne m}
 \int_{s_R}^{t_2}\!\int
 \eta_R\Xi_\ell
 (f_n'\overline{f_m}'+nm\,g_{nm})\,dx_3dt.
 \end{aligned}
 \tag{F.11}
\]

The factors are forced by the \(1/(2\pi)\) Fourier convention:
the endpoint and cutoff rows carry the local-energy factor \(1/2\), hence
\(\pi\), whereas the dissipation row carries the full period factor
\(2\pi\). The horizontal-gradient product is
\((in)(-im)=nm\).

With this notation, the full localized identity is exactly

\[
 \mathcal E_{\rm diag}+\mathcal E_{\rm off}
 +\mathcal D_{\rm diag}+\mathcal D_{\rm off}
 =
 \mathcal A_{\rm diag}+\mathcal A_{\rm off}
 +\mathcal T_\xi.
 \tag{F.12}
\]

## 4. Phase integration reconstructs the off-diagonal identity

Insert (F.8) into the R0.75E formula

\[
 \mathcal T_\xi
 =\pi\operatorname {Re}\sum_{n\ne m}
 \int_{s_R}^{t_2}\!\int
 \eta_R\Xi_\ell\,i\ell b g_{nm}\,dx_3dt.
 \tag{F.13}
\]

The time derivative gives

\[
 \int_{s_R}^{t_2}\eta_R\Xi_\ell\partial_tg_{nm}
 =\int\Xi_\ell g_{nm}(t_2)
  -\int_{s_R}^{t_2}\eta_R'\Xi_\ell g_{nm},
 \tag{F.14}
\]

because \(\eta_R(s_R)=0\). Periodic integration by parts in \(x_3\)
gives

\[
 -\int\eta_R\Xi_\ell g_{nm}''
 =-\int\eta_R\Xi_\ell''g_{nm}.
 \tag{F.15}
\]

Finally,

\[
 n^2+m^2=(m-n)^2+2nm=\ell^2+2nm.
 \tag{F.16}
\]

Combining (F.14)--(F.16) with the \(2f_n'\overline{f_m}'\) row yields
precisely (F.1):

\[
 \mathcal T_\xi
 =\mathcal E_{\rm off}
  -\mathcal A_{\rm off}
  +\mathcal D_{\rm off}.
 \tag{F.17}
\]

Substitution in (F.12) cancels
\(\mathcal E_{\rm off}\), \(\mathcal A_{\rm off}\), and
\(\mathcal D_{\rm off}\) on their two sides, leaving

\[
 \boxed{
 \mathcal E_{\rm diag}+\mathcal D_{\rm diag}
 =\mathcal A_{\rm diag}.}
 \tag{F.18}
\]

Equation (F.18) is also obtained directly by taking the real part of each
mode equation against \(\eta_R\Xi_0\overline{f_n}\). Thus the proposed
phase substitution is exactly the off-diagonal projection of the original
energy identity; it supplies no independent sign, small factor, or
observability estimate.

## 5. Positivity alone cannot recover the localized form

The remaining temptation is to compare the full nonnegative weighted
quadratic form with its diagonal Fourier average. Such a comparison is
false with a scale-independent constant even for smooth real trigonometric
polynomials.

Use normalized measure

\[
 \langle h\rangle:=\frac1{2\pi}\int_{-\pi}^{\pi}h(x)\,dx.
 \tag{F.19}
\]

For odd \(N=2M+1\), let

\[
 D_N(x):=\sum_{k=-M}^{M}e^{ikx},\qquad
 a_N:=\frac{D_N}{\sqrt N},\qquad
 X_N:=\frac{|D_N|^2}{N^2}.
 \tag{F.20}
\]

Both \(D_N\) and \(a_N\) are real, while \(X_N\) is a smooth nonnegative
trigonometric polynomial satisfying

\[
 0\le X_N\le1,\qquad
 \langle X_N\rangle=\frac1N,\qquad
 \langle|a_N|^2\rangle=1.
 \tag{F.21}
\]

The difference \(s=k-j\) occurs \(N-|s|\) times, so

\[
 \begin{aligned}
 \langle|D_N|^4\rangle
 &=N^2+2\sum_{q=1}^{N-1}q^2\\
 &=\frac{2N^3+N}{3}.
 \end{aligned}
 \tag{F.22}
\]

Consequently

\[
 \begin{aligned}
 \langle X_N|a_N|^2\rangle
 &=\frac{2+N^{-2}}3,\\
 \frac{\langle X_N|a_N|^2\rangle}
 {\langle X_N\rangle\langle|a_N|^2\rangle}
 &=\frac{2N+N^{-1}}3\longrightarrow\infty.
 \end{aligned}
 \tag{F.23}
\]

This finite exact family proves that \(0\le X\le1\) and Fourier
diagonalization alone cannot bound a localized quadratic form by a uniform
multiple of its diagonal average. It is not the frozen geometric collar
and is not an E.24 counterexample; it isolates the missing information.

## 6. What a successful next estimate must add

Equations (F.17)--(F.18) rule out only the circular proof that substitutes
the modal product equation without adding an estimate. Equation (F.23)
rules out only a cutoff-positivity/diagonal-average comparison with no
dynamic or payment input.

A viable continuation must add at least one genuinely new ingredient:

1. a quantitative uncertainty principle coupling concentration in the
   \(x_2\)-thin collar to horizontal frequencies and heat damping;
2. a resolvent or hypocoercive estimate that exploits shear phase over the
   full time window rather than algebraically replacing it;
3. a pathwise residence-time bound through the fixed collar;
4. a payment-sensitive bound on the positive off-diagonal Toeplitz form.

None of these is proved here. In particular, this note does not prove or
disprove the arbitrary-real cross-mode estimate E.24, complete-clock
extraction, fixed deletion, suitable-weak transfer, regularity, or
singularity. It is an exact route-pruning lemma inside the smooth frozen
family. \(\mathbf{NOT\ CLAY}.\)
