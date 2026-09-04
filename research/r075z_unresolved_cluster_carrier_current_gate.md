# R0.75Z -- unresolved-cluster normal form and the carrier-current gate

## 0. Result and exact boundary

R0.75X pays every fixed finite family in the low-carrier sector.  R0.75Y
pays every strongly separated family in the high-carrier sector.  This note
identifies the exact part of parameter space left between them and tests the
most immediate proposed recursion: demodulate each unresolved cluster and
apply the low-carrier theorem to its envelope.

Fix an integer `q>=1`, let

\[
 1\le n_1<n_2<\cdots<n_q\le2n_1,
 \qquad \ell=aR,
 \tag{Z.1}
\]

and retain the exact diffusive shear

\[
 F(t,y)=\sum_{j=1}^q A_je^{-n_j^2t}
 \cos\bigl(n_j(y-Bt)-\phi_j\bigr).
 \tag{Z.2}
\]

For fixed `q`, choose the R0.75X threshold `C_0=8q`.  Then every family
falls into exactly one of the following three sectors:

\[
 \begin{array}{ll}
 \text{X-sector:}&n_1\ell<8q,\\
 \text{Y-sector:}&n_1\ell\ge8q\ \text{and}\
   (n_{j+1}-n_j)\ell\ge8q\quad(1\le j<q),\\
 \text{Z-sector:}&n_1\ell\ge8q\ \text{and at least one}\
   (n_{j+1}-n_j)\ell<8q.
 \end{array}
 \tag{Z.3}
\]

The X-sector is paid by R0.75X.  The Y-sector satisfies the signed-spectrum
condition of R0.75Y and is paid there.  Thus the Z-sector is the complete
remaining high-carrier region for this fixed-`q` family, rather than a
selected example of it.

Cut the ordered frequencies at every adjacent gap at least `8q/ell`.
This gives a unique partition into maximal consecutive clusters.  Each
non-singleton cluster `C={r,...,s}` has carrier `N=n_r` and offsets
`d_j=n_j-N` satisfying

\[
 0=d_r<d_{r+1}<\cdots<d_s,
 \qquad
 d_s\ell<8q(s-r)\le8q(q-1),
 \qquad d_s\le N.
 \tag{Z.4}
\]

Its analytic signal has the exact carrier-envelope representation

\[
 \begin{aligned}
 H_C(t,y)&:=\sum_{j=r}^s A_je^{-n_j^2t}
 e^{i(n_j(y-Bt)-\phi_j)}\\
 &=e^{-N^2t}e^{iN(y-Bt)}Z_C(t,y),\\
 Z_C(t,y)&:=\sum_{j=r}^s A_j
 e^{-(2Nd_j+d_j^2)t}e^{i(d_j(y-Bt)-\phi_j)},
 \qquad F_C=\operatorname {Re}H_C.
 \end{aligned}
 \tag{Z.5}
\]

The envelope is spatially low-band for fixed `q`, by Z.4, but it does not
satisfy the low-carrier equation used in R0.75X.  Instead,

\[
 \boxed{
 \partial_tZ_C+B\partial_yZ_C-\partial_y^2Z_C
 -2iN\partial_yZ_C=0.}
 \tag{Z.6}
\]

If `Q_C=|Z_C|^2` and
`J_C=\operatorname {Im}(\overline{Z_C}\partial_yZ_C)`, then

\[
 \boxed{
 \partial_tQ_C+B\partial_yQ_C-\partial_y^2Q_C
 =-2|\partial_yZ_C|^2-4NJ_C.}
 \tag{Z.7}
\]

The carrier current is globally favorable because the offsets are
nonnegative, but it has no fixed sign locally.  Moreover no constant
independent of `N` can control `N|J_C|` pointwise by
`Q_C+|\partial_yZ_C|^2`, even for a two-term envelope.  Consequently the
R0.75X local-energy argument cannot be recursively applied to `Z_C` after
taking the new current term in absolute value.  This is a no-go result for
that proof strategy, not a counterexample to the desired cluster flux
estimate.

The next admissible route must keep the one-sided offset spectrum and the
sign of the current, or estimate the density and carrier blocks jointly
before local absolute values are taken.  No full Z-sector flux payment is
claimed here.

## 1. Frozen inputs

The immediately used inputs are

| input | SHA-256 | role |
|---|---|---|
| `research/r075b_bulk_clock_outer_padding_gate.md` | `430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a` | frozen complete clock and cutoff |
| `research/r075r_outer_cap_spectral_concentration_obstruction.md` | `e5eba5b262a8e140eaa149b6d914f355f2f3c636ec1e74cf85515f1c38fd32f3` | unresolved packet boundary |
| `research/r075x_fixed_finite_mode_low_carrier_payment.md` | `8e0c412528578c15d807b33b64f0996e62a2dabe2ebd58fa297f67c093929763` | every fixed-`q` low-carrier family |
| `research/r075y_strongly_separated_multimode_flux_payment.md` | `74790f910b596c86b204291d997ef723cabbc85d14a89e3fe900814fcd88b0a6` | strongly separated high-carrier family |

The frozen geometric and temporal assumptions remain

\[
 a=pL,
 \qquad R=e^{-\rho L^2/4},
 \qquad \omega=e^{-c_\gamma L^2/4},
 \qquad T_R=4R^2,
 \qquad \ell=aR.
 \tag{Z.8}
\]

This note uses only exact finite Fourier algebra.  It imports no external
observability, unique-continuation, or cluster theorem.

## 2. Exhaustive fixed-`q` parameter partition

R0.75X allows any fixed low-carrier threshold `C_0`.  Taking `C_0=8q`
for the present fixed `q` proves the X-sector row of Z.3.

Suppose now that `n_1 ell>=8q`.  The minimum gap of the signed spectrum is

\[
 \delta_{\boldsymbol n}
 =\min\!\left(2n_1,\min_{1\le j<q}(n_{j+1}-n_j)\right).
 \tag{Z.9}
\]

Indeed the smallest positive-positive gap is adjacent, the smallest
negative-negative gap is the same, and the smallest positive-negative gap
is `2n_1`.  If every adjacent gap obeys the Y-sector row of Z.3, then

\[
 2n_1\ell\ge16q,
 \qquad
 \ell\min_{1\le j<q}(n_{j+1}-n_j)\ge8q,
 \qquad
 \ell\delta_{\boldsymbol n}\ge8q.
 \tag{Z.10}
\]

This is exactly the hypothesis Y.3.  If an adjacent gap fails it, the
family lies in the Z-sector.  The three rows of Z.3 are disjoint and cover
all possibilities, so the partition is exhaustive.

For the cluster partition, place a cut between `n_j` and `n_{j+1}` exactly
when

\[
 (n_{j+1}-n_j)\ell\ge8q.
 \tag{Z.11}
\]

Maximality makes the consecutive blocks unique.  In a block
`C={r,...,s}`, every internal gap is strictly less than `8q/ell`; hence

\[
 (n_s-n_r)\ell
 =\sum_{j=r}^{s-1}(n_{j+1}-n_j)\ell
 <8q(s-r).
 \tag{Z.12}
\]

The dyadic band in Z.1 also gives

\[
 n_s-N\le2n_1-N\le n_1\le N,
 \tag{Z.13}
\]

which completes Z.4.  A Z-sector family has at least one non-singleton
cluster, while the all-singleton partition is exactly the Y-sector within
`n_1 ell>=8q`.

## 3. Exact carrier-envelope equation

Fix one non-singleton cluster and abbreviate `Z=Z_C`, `H=H_C`.  The `j`th
envelope mode is

\[
 Z_j(t,y)=A_je^{-(2Nd_j+d_j^2)t}
 e^{i(d_j(y-Bt)-\phi_j)}.
 \tag{Z.14}
\]

Direct differentiation gives

\[
 \begin{aligned}
 \partial_tZ_j&=(-2Nd_j-d_j^2-iBd_j)Z_j,\\
 B\partial_yZ_j&=iBd_jZ_j,\\
 -\partial_y^2Z_j&=d_j^2Z_j,\\
 -2iN\partial_yZ_j&=2Nd_jZ_j.
 \end{aligned}
 \tag{Z.15}
\]

The four rows sum to zero term by term, proving Z.6.  Conversely,
multiplication by `e^{-N^2t}e^{iN(y-Bt)}` restores

\[
 \partial_tH+B\partial_yH-\partial_y^2H=0.
 \tag{Z.16}
\]

Thus demodulation has not produced the real advection-diffusion equation
X.13.  It has produced a complex equation with an `N`-dependent imaginary
first derivative.  The real decay rates

\[
 \lambda_j=2Nd_j+d_j^2
 \tag{Z.17}
\]

also remain unbounded as the carrier tends to infinity whenever
`d_j>0`.  Spatial boundedness of the offsets alone therefore does not put
the envelope into the compact coefficient family used by R0.75X.

## 4. Exact square and flux split for one cluster

The real cluster component is `F_C=(H_C+\overline{H_C})/2`.  Therefore

\[
 \boxed{
 F_C^2
 =\frac12e^{-2N^2t}|Z_C|^2
 +\frac12e^{-2N^2t}
 \operatorname {Re}\!\left(e^{2iN(y-Bt)}Z_C^2\right).}
 \tag{Z.18}
\]

Use the frozen odd radial kernel

\[
 D_R(y)=-2\pi y\vartheta(|y|/R-a),
 \qquad
 \mathcal T_C:=\frac12\int_0^{T_R}\eta_R(t)B
 \int_{-\pi}^{\pi}D_R(y)F_C(t,y)^2\,dydt.
 \tag{Z.19}
\]

Substitution of Z.18 gives the exact decomposition

\[
 \boxed{\mathcal T_C=\mathcal T_C^{\rm den}
 +\mathcal T_C^{\rm car},}
 \tag{Z.20}
\]

where

\[
 \begin{aligned}
 \mathcal T_C^{\rm den}
 &:=\frac14\int_0^{T_R}\eta_RB e^{-2N^2t}
 \int_{-\pi}^{\pi}D_R|Z_C|^2\,dydt,\\
 \mathcal T_C^{\rm car}
 &:=\frac14\operatorname {Re}\int_0^{T_R}\eta_RB e^{-2N^2t}
 \int_{-\pi}^{\pi}D_Re^{2iN(y-Bt)}Z_C^2\,dydt.
 \end{aligned}
 \tag{Z.21}
\]

The density block contains only offset differences.  The carrier block
contains the self and offset-sum rows translated by `2N`.  This split is
exact for the square of one cluster.  For the square of the full family,
cross-cluster products must still be added; Z.20 does not pay or discard
them.

## 5. Local carrier current

Set

\[
 Q=|Z|^2,
 \qquad J=\operatorname {Im}(\overline Z\,\partial_yZ).
 \tag{Z.22}
\]

From Z.6,

\[
 \partial_tZ=-B\partial_yZ+\partial_y^2Z+2iN\partial_yZ.
 \tag{Z.23}
\]

Taking twice the real part after multiplication by `overline Z`, and
using

\[
 2\operatorname {Re}(\overline Z\,\partial_y^2Z)
 =\partial_y^2|Z|^2-2|\partial_yZ|^2,
 \qquad
 4N\operatorname {Re}(i\overline Z\,\partial_yZ)=-4NJ,
 \tag{Z.24}
\]

proves Z.7.

The same term is visible in the unmodulated gradient:

\[
 |\partial_yH|^2=e^{-2N^2t}
 \left(N^2Q+|\partial_yZ|^2+2NJ\right).
 \tag{Z.25}
\]

There is no contradiction with the ordinary energy identity for `H`;
Z.7 and Z.25 are the same dissipation written in modulated variables.

The current is favorable only after full-period integration.  Orthogonality
of the distinct nonnegative integer offsets yields

\[
 \boxed{
 \int_{-\pi}^{\pi}J(t,y)\,dy
 =2\pi\sum_{j=r}^s d_jA_j^2
 e^{-2(2Nd_j+d_j^2)t}\ge0.}
 \tag{Z.26}
\]

Consequently,

\[
 \frac d{dt}\int_{-\pi}^{\pi}Q\,dy
 =-2\int_{-\pi}^{\pi}|\partial_yZ|^2\,dy
 -4N\int_{-\pi}^{\pi}J\,dy\le0.
 \tag{Z.27}
\]

The collar argument is local in `y`, so Z.26 cannot simply be substituted
for the current inside a weighted interval.

## 6. Exact failure of carrier-uniform pointwise absolute payment

Consider the two-term envelope

\[
 Z^{(N)}(y)=2-e^{iy},
 \tag{Z.28}
\]

which is the time-zero envelope of frequencies `N` and `N+1`, with a
phase change on the second mode.  At the centre of the frozen interval,
`y=0`,

\[
 Z^{(N)}(0)=1,
 \qquad \partial_yZ^{(N)}(0)=-i,
 \qquad Q(0)=1,
 \qquad J(0)=-1.
 \tag{Z.29}
\]

If a constant `C` independent of `N` satisfied

\[
 2N|J(y)|\le C\bigl(Q(y)+|\partial_yZ(y)|^2\bigr)
 \tag{Z.30}
\]

for every admissible carrier-envelope pair, Z.29 would imply `N<=C`
for every positive integer `N`, which is impossible.  More sharply, the
modulated dissipation density at this point is

\[
 |\partial_yZ^{(N)}(0)|^2+2NJ(0)=1-2N<0.
 \tag{Z.31}
\]

For example, with `q=2` and `ell=1`, the frequencies `(N,N+1)` lie in an
unresolved high-carrier cluster for every `N>=16`.

This calculation rules out only a carrier-uniform pointwise estimate of
the absolute current.  It does not rule out a signed weighted estimate, a
Hardy-space argument using the nonnegative offset spectrum, a cancellation
between Z.21's two blocks, or the final desired collar-flux inequality.

## 7. Route decision and open obligations

The exhaustive reduction Z.3 changes the next question.  There is no
longer an unspecified `q>=3` high-carrier region: after X and Y, it is
precisely the high-carrier family containing at least one maximal block of
nearby modes.  Z.5--Z.7 show that this block is a low-band complex envelope
with a large carrier current, not another instance of the real low-carrier
equation.

The next proof attempt must establish at least one of the following before
claiming cluster payment:

1. a localized signed-current inequality that exploits the one-sided
   offset spectrum without an `N` loss;
2. a joint multiplier identity for `\mathcal T_C^{\rm den}+\mathcal T_C^{\rm car}`
   in which the large current is never estimated separately; or
3. a finite-dimensional cluster observable that controls cross-cluster
   products and remains uniform in the carrier.

**Closed here:** an exhaustive fixed-`q` X/Y/Z parameter partition; the
unique maximal cluster decomposition; the exact carrier-envelope equation;
the exact density/carrier split of one cluster square; the local and global
carrier-current identities; and a concrete carrier-uniform pointwise
no-go example.

**Open:** every full Z-sector collar-flux estimate; a localized signed
current estimate; joint density/carrier cancellation; cross-cluster
aggregation; arbitrary growing packets; nonconstant or vertically
dependent shear; projection from a larger velocity; arbitrary-field E.24;
complete Version-M extraction; fixed deletion; suitable-weak transfer;
regularity; and singularity.

The field Z.2 remains an exact smooth unforced shear component, subject to
the same constant-background and Version-M boundary recorded in R0.75Y.
No simulation or formal scientific figure is needed for these exact
identities.  No completeness, novelty, or priority claim is made.
**NOT CLAY.**
