# Independent primary audit of R0.75F

## 0. Frozen object and verdict

Audited file:
`research/r075f_modal_phase_integration_identity.md`.

Frozen SHA-256:
`f7a72ebfe0471e18c0d5d44bd3123491d7cd47a79293d1860c5d023c13acf440`.

**Verdict: PASS. Mathematical blocker count: 0. Release blocker count: 0.**

The note proves two route-pruning statements. First, substituting the exact
modal-product equation into the signed off-diagonal flux reconstructs the
off-diagonal part of the same localized energy identity and therefore adds
no estimate. Second, a finite real Fejer-type family rules out a uniform
localized-form/diagonal-average comparison based only on
`0 <= X <= 1`. Neither statement is promoted to a counterexample to E.24
or to an obstruction to methods that add coercive information.

The two frozen inputs recompute as

| input | SHA-256 |
|---|---|
| `research/r075b_bulk_clock_outer_padding_gate.md` | `430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a` |
| `research/r075e_horizontal_cross_mode_flux_reduction.md` | `99529b8934412775e19a1b70784cddf3e62190b50c42669ccd34135a134c5049` |

## 1. Modal-product equation, F.4--F.8

For

\[
 g_{nm}=f_n\overline{f_m},\qquad \ell=m-n,
\]

the two modal equations have shear rows `-inbf_n` and
`+imb overline(f_m)`. Their product therefore contributes

\[
 i(m-n)b g_{nm}=i\ell b g_{nm}.
\]

The vertical product rule is

\[
 g_{nm}''=f_n''\overline{f_m}
 +2f_n'\overline{f_m}'
 +f_n\overline{f_m}'',
\]

so solving the product equation for the shear row gives exactly

\[
 i\ell b g_{nm}
 =\partial_tg_{nm}-g_{nm}''
 +2f_n'\overline{f_m}'
 +(n^2+m^2)g_{nm}.
\]

The signs and the coefficient two are correct. No division by `b` or
`ell` is used, so this is an identity at shear zeros rather than a hidden
nondegeneracy estimate.

## 2. Quadratic forms and normalization, F.9--F.13

Under the frozen `1/(2 pi)` Fourier convention, integrating a surviving
horizontal mode over one period contributes `2 pi`. The endpoint and
cutoff rows originate from the half-energy identity and therefore carry
`pi`; the dissipation row carries `2 pi`.

The horizontal gradient product is

\[
 (in f_n)\overline{(im f_m)}=(in)(-im)g_{nm}=nm g_{nm},
\]

which confirms the `nm` term in F.11. The cutoff Laplacian acting on the
difference mode contributes `-ell^2 Xi_ell`, so the off-diagonal cutoff
coefficient is exactly

\[
 \eta_R'\Xi_\ell+\eta_R(\Xi_\ell''-\ell^2\Xi_\ell).
\]

These rows reproduce the diagonal/off-diagonal decomposition of the
R0.75B localized identity without omitting the endpoint or changing the
signed transport flux.

## 3. Exact cancellation, F.14--F.18

Because `eta_R(s_R)=0` and `eta_R(t_2)=1`, time integration gives the
terminal off-diagonal form minus the `eta_R'` cutoff form. Periodic
integration in `x_3` gives

\[
 -\int\eta_R\Xi_\ell g_{nm}''
 =-\int\eta_R\Xi_\ell''g_{nm}.
\]

Finally,

\[
 n^2+m^2=(m-n)^2+2nm=\ell^2+2nm.
\]

After multiplication by `pi` and taking the real part, the terms assemble
without a remainder as

\[
 \mathcal T_\xi
 =\mathcal E_{\rm off}-\mathcal A_{\rm off}
 +\mathcal D_{\rm off}.
\]

Substitution into F.12 cancels those same three off-diagonal forms and
leaves

\[
 \mathcal E_{\rm diag}+\mathcal D_{\rm diag}
 =\mathcal A_{\rm diag}.
\]

This is independently obtainable from the real part of each single-mode
equation tested against `eta_R Xi_0 overline(f_n)`. The phase substitution
therefore has no independent sign, small factor, or observability content.

## 4. Finite Fejer-family audit, F.19--F.23

For odd `N=2M+1`, the symmetric Dirichlet polynomial `D_N` has exactly
`N` unit Fourier coefficients and is real. Thus

\[
 |D_N|\le N,\qquad
 0\le X_N=|D_N|^2/N^2\le1,
\]

and Parseval gives

\[
 \langle X_N\rangle=1/N,
 \qquad \langle|a_N|^2\rangle=1.
\]

The difference frequency `s` occurs `N-|s|` times. Hence

\[
 \langle|D_N|^4\rangle
 =\sum_{s=-(N-1)}^{N-1}(N-|s|)^2
 =N^2+2\sum_{q=1}^{N-1}q^2
 =\frac{2N^3+N}{3}.
\]

It follows exactly that

\[
 \langle X_N|a_N|^2\rangle=\frac{2+N^{-2}}3,
 \qquad
 \frac{\langle X_N|a_N|^2\rangle}
 {\langle X_N\rangle\langle|a_N|^2\rangle}
 =\frac{2N+N^{-1}}3.
\]

Direct finite checks give `19/9`, `17/5`, and `33/7` for
`N=3,5,7`, respectively. The ratio diverges, while every member remains a
smooth real trigonometric polynomial with a smooth nonnegative weight.

## 5. Structural and claim audit

- Equation tags F.1--F.23 are unique and consecutive.
- Every internal F-reference resolves to one of those tags.
- The endpoint, time-cutoff, vertical-cutoff, horizontal-frequency, and
  dissipation terms are all retained with the correct measure factors.
- The finite family is not identified with the frozen spherical collar and
  is not called an E.24 counterexample.
- The note rules out only a circular phase substitution and a positivity-only
  diagonal comparison.
- Enhanced dissipation, resolvent, hypocoercive, pathwise, uncertainty, and
  payment-sensitive routes remain open.
- No simulation, DNS, regularity theorem, singularity theorem, novelty, or
  priority claim is made.

The frozen R0.75F claims are mathematically consistent and ready for a
dual finite certificate. **NOT CLAY.**
