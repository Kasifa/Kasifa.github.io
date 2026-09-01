# R0.73X finite diagnostic design: cutoff commutators, concentration, and tent candidates

**Design date:** 2026-09-01

**Status:** exact-algebra design; no sealed two-producer package has been run
and no candidate inequality is certified or refuted by this file alone

**Arithmetic policy:** finite Fourier dictionaries with Gaussian heat
multipliers retained symbolically; rational coefficients and exact integer
wavevectors first, interval arithmetic only for a separately declared sign
isolation step

**Ordinary translation path:** LOCAL_DIRECT_NO_DGX

**DGX used:** false

**Network used:** false

## 1. What the diagnostic is allowed to decide

The finite package is designed to do three things:

1. verify the exact Fourier and cutoff algebra behind
   \[
   \Pi_s=\nabla\cdot K_s+{\mathscr S}_s,\qquad
   \int\eta\Pi_s=-\int\nabla\eta\cdot K_s+\int\eta{\mathscr S}_s;
   \tag{1.1}
   \]
2. refute a precisely stated universal inequality when an exact ratio is
   proved unbounded within its quantifiers;
3. test the scaling and normalization of proposed tent quantities on a
   finite, increasingly concentrated family.

It is not designed to prove a PDE estimate from bounded examples.  In
particular, it cannot certify a suitable weak solution, a nonzero defect
measure, a full-time trajectory, epsilon regularity, or global regularity.

## 2. Exact Fourier ledger

Write a real mean-zero divergence-free trigonometric polynomial as

\[
 u(x)=\sum_{k\in{\cal K}}a(k)e^{ik\cdot x},\qquad
 a(-k)=\overline{a(k)},\qquad k\cdot a(k)=0.
\tag{2.1}
\]

For \(m\in\mathbb Z^3\),

\[
 \widehat{\tau}_{ij,s}(m)
 =\sum_{k+\ell=m}
 \left(e^{-s|m|^2}-e^{-s(|k|^2+|\ell|^2)}\right)
 a_i(k)a_j(\ell).
\tag{2.2}
\]

The signed production coefficient is

\[
 \widehat\Pi_s(n)
 =-\sum_{m+r=n}\widehat\tau_{ij,s}(m)\,
 (ir_j)e^{-s|r|^2}a_i(r).
\tag{2.3}
\]

For ordered \(k+\ell+r=n\), the third central multiplier is

\[
 \begin{aligned}
 c_s(k,\ell,r)={}&e^{-s|n|^2}
 -e^{-s|k|^2}e^{-s|\ell+r|^2}
 -e^{-s|\ell|^2}e^{-s|k+r|^2}\\
 &-e^{-s|r|^2}e^{-s|k+\ell|^2}
 +2e^{-s(|k|^2+|\ell|^2+|r|^2)}.
 \end{aligned}
\tag{2.4}
\]

Thus

\[
 \widehat K_{j,s}(n)
 ={1\over2}\sum_{\substack{k+\ell+r=n\\i}}
 c_s(k,\ell,r)a_i(k)a_i(\ell)a_j(r).
\tag{2.5}
\]

The first producer defines

\[
 \widehat{\mathscr S}^{\,A}_s(n)
 =\widehat\Pi_s(n)-in_j\widehat K_{j,s}(n).
\tag{2.6}
\]

The independent producer must instead expand

\[
 {\mathscr S}_s={1\over4s}\int
 y\cdot a_s(x,y)|a_s(x,y)|^2g_s(y)\,dy
\tag{2.7}
\]

using

\[
 \int_{\mathbb R^3}y_\alpha g_s(y)e^{-iq\cdot y}\,dy
 =-2isq_\alpha e^{-s|q|^2}.
\tag{2.8}
\]

Agreement of (2.6) and (2.7) coefficient by coefficient is mandatory.
Using (2.6) in both producers would only recheck the same subtraction and
would not independently audit the \(1/(4s)\) coefficient.

The gradient covariance is computed as

\[
 D_{ii,s}=P_s(|\nabla u|^2)-|\nabla v_s|^2,
\tag{2.9}
\]

both by direct convolution and by the independent identity

\[
 D_{ii,s}=2\int_0^sP_{s-r}\!\left(
 \partial_\ell\partial_m v_{r,i}\,
 \partial_\ell\partial_m v_{r,i}\right)\,dr.
\tag{2.9a}
\]

The two constructions must agree coefficient by coefficient, including the
factor \(2\).  Pressure is fixed by

\[
 \widehat p(n)
 =-{n_i n_j\over|n|^2}\widehat{u_i u_j}(n),
 \quad n\ne0,\qquad \widehat p(0)=0,
\tag{2.10}
\]

so the pressure covariance \(Q_s=P_s(pu)-p_sv_s\) is not omitted from the
localized trace ledger.

## 3. Track A: sparse resonant witness and harmonic cutoff

The guaranteed sparse starting support is the three-conjugate-pair 2D3C
triad already available from R0.73W:

\[
 \begin{aligned}
 W(x,y,z)=\big(&-2\cos y-2\sin(x+y),\\
               &-2\cos x+2\sin(x+y),\\
               &-\cos x-\cos y-\sin(x+y)\big).
 \end{aligned}
\tag{3.1}
\]

Its positive wavevectors are

\[
 k_1=(1,0,0),\qquad k_2=(0,1,0),\qquad
 k_3=k_1+k_2,
\tag{3.2}
\]

and \(u_A=AW\).  This is an upper bound on support complexity, not yet a
minimality theorem.

For an exact nonnegative mode probe use

\[
 \eta_{\varepsilon,\ell,x_0}(x)
 =1+\varepsilon\cos(\ell\cdot(x-x_0)),
 \qquad 0<|\varepsilon|\le{1\over2}.
\tag{3.3}
\]

Although (3.3) is not compactly supported, it isolates one Fourier
coefficient without numerical quadrature:

\[
 \langle f\rangle:=(2\pi)^{-3}\int_{\mathbb T^3}f(x)\,dx,
 \qquad
 \langle\eta f\rangle
 =\widehat f(0)+\varepsilon
 \operatorname{Re}\!\left(e^{i\ell\cdot x_0}\widehat f(\ell)\right).
\tag{3.4}
\]

The probe frequencies \(\ell\) are enumerated over the complete nonzero
support of \(\Pi_s\), \(K_s\), and \({\mathscr S}_s\).  The package must find
and freeze the lexicographically first row for which

\[
 \langle\eta\Pi_s\rangle,\qquad
 -\langle\nabla\eta\cdot K_s\rangle,\qquad
 \langle\eta{\mathscr S}_s\rangle
\tag{3.5}
\]

are all individually nonzero and satisfy (1.1) exactly.  If the field (3.1)
does not supply such a row, the declared fallback is the rank-three R0.73W
extension; no ad hoc dense random field may silently replace it.

An unsealed standard-library rational scratch check already supplies a
deterministic seed.  At \(q=e^{-s}=1/2\),
\(\ell=(1,1,0)\), \(x_0=0\), and \(\varepsilon=1/2\), it gives

\[
 \widehat\Pi_s(0)=-{3\over16},\quad
 \widehat\Pi_s(\ell)={3\over16},\quad
 \widehat{\nabla\cdot K_s}(\ell)={9\over64},\quad
 \widehat{\mathscr S}_s(\ell)={3\over64}.
\tag{3.6}
\]

Consequently, the proposed probe row is

\[
 \langle\eta\Pi_s\rangle=-{3\over32},\qquad
 -\langle\nabla\eta\cdot K_s\rangle={9\over128},\qquad
 \langle\eta{\mathscr S}_s\rangle=-{21\over128}.
\tag{3.7}
\]

The last two values add to the first.  These numbers are a design anchor,
not a sealed result: both independent producers must reconstruct them, and
one producer must obtain \({\mathscr S}_s\) directly from (2.7).

### 3.1 Bounded minimal-support search

One conjugate pair is excluded analytically.  Such a field depends only on
\(k\cdot x\) and takes values in \(k^\perp\); hence
\(\tau_s k=0\), \(K_s\cdot k=0\), and
\(\Pi_s=\nabla\cdot K_s={\mathscr S}_s=0\).  Two conjugate pairs are
therefore the first support size worth searching.  The remainder vanishes
directly as well: the increment lies in \(k^\perp\), depends on \(y\) only
through \(k\cdot y\), and the perpendicular Gaussian first moments in
\(y\cdot a_s\) are zero.

Minimality beyond that observation is a separate finite question.  Make the
enumeration genuinely finite as follows.  Choose one representative of each
pair \(\{k,-k\}\)
by lexicographic sign.  For each such \(k\), let \(j(k)\) be the least
coordinate index for which \(k\) is not parallel to \(e_{j(k)}\), and set

\[
 b_1(k)=\operatorname{prim}\big(k\times e_{j(k)}\big),\qquad
 b_2(k)=\operatorname{prim}\big(k\times b_1(k)\big),
 \tag{3.8}
\]

where \(\operatorname{prim}\) divides by the gcd of the nonzero integer
components and fixes the first nonzero component positive.  Represent the
real field at a positive wavevector by

\[
 c(k)\cos(k\cdot x)+d(k)\sin(k\cdot x),\qquad
 c(k),d(k)\in\operatorname{span}_{\mathbb Z}\{b_1(k),b_2(k)\}.
 \tag{3.9}
\]

Enumerate:

- two and then three conjugate wavevector pairs in
  \([-2,2]^3\setminus\{0\}\);
- the four integer coefficients of \(c(k)\) and \(d(k)\) in the basis
  \((b_1(k),b_2(k))\), each in \(\{-2,-1,0,1,2\}\), excluding a zero
  wavevector pair;
- probe frequencies in the exact cubic output support.

For the finite probe stage it is enough to use
\(\varepsilon\in\{-1/2,1/2\}\) and the two phases
\(\cos(\ell\cdot x)\), \(\sin(\ell\cdot x)\).  This detects the real and
imaginary parts without a continuous search over \(x_0\).

Candidates are ordered by

\[
 \left(\#\hbox{ conjugate pairs},\,
 \max|k|_\infty,\,
 \sum_{k>0}\big(\|c(k)\|_1+\|d(k)\|_1\big),\,
 \ell,\,\hbox{probe phase},\,\varepsilon\right).
\tag{3.10}
\]

An exhaustive zero result proves minimality only within this box,
polarization basis, and coefficient alphabet.  The public phrase
“minimal sparse witness” is forbidden unless the search domain is appended.

## 4. Smooth NSE tangent check

A finite trigonometric polynomial is admissible as smooth initial data.
At \(t=0\), compute the exact Navier--Stokes tangent

\[
 \dot u=-\mathbb P\nabla\cdot(u\otimes u)+\nu\Delta u.
\tag{4.1}
\]

Differentiate

\[
 k_s={1\over2}\left(P_s|u|^2-|P_su|^2\right)
\tag{4.2}
\]

with (4.1), and independently construct

\[
 G_s=v_sk_s+Q_s-\nu\nabla k_s.
\tag{4.3}
\]

The exact mode table must verify

\[
 \partial_tk_s+\nabla\cdot G_s
 =-\nu D_{ii,s}+{\mathscr S}_s
\tag{4.4}
\]

and its harmonic-cutoff integral.  This checks the smooth, zero-defect
PDE tangent at one time.  It is stronger than a static identity check but
still does not integrate a Navier--Stokes trajectory.

Amplitude degrees must be recorded explicitly:

\[
 k_s,D_{ii,s}\sim A^2,\qquad
 K_s,Q_s,\Pi_s,{\mathscr S}_s\sim A^3.
\tag{4.5}
\]

Therefore, if either numerator in (5.1)--(5.2) of the problem freeze is
nonzero for an admissible cutoff, its ratio to the complete displayed
quadratic denominator grows linearly in \(|A|\).  The harmonic row (3.7)
proves that the relevant functions are not identically zero.  Transfer to a
compact local cutoff uses a separate continuity argument: choose a
nonnegative bump in a neighborhood where the cubic coefficient has fixed
sign.  To meet a prescribed relation \(s=\theta R^2\), use the integer
rescaling \(W_N(x)=W(Nx)\), for which the anchor heat factor is attained at
\(s=(\log2)/N^2\), and choose
\(R=N^{-1}\sqrt{(\log2)/\theta}\); taking \(N\) large places the bump inside
the frozen torus chart.  This scale match alone does not prove that a
standard radius-\(R\) cutoff has a nonzero numerator: that fact must be
checked exactly (or by a rigorous fixed-sign neighborhood estimate) for the
chosen \(\theta\).  Only after that cutoff-quantifier check does amplitude
scaling refute the local candidates.  It does not refute a ledger containing
the cubic cutoff and pressure rows.

## 5. Track B: exact finite Fourier concentration

To test spatial concentration without leaving finite Fourier algebra, use
the one-dimensional Fejér kernel

\[
 F_M(x)=\sum_{|j|<M}\left(1-{|j|\over M}\right)e^{ijx}
 ={1\over M}\left({\sin(Mx/2)\over\sin(x/2)}\right)^2
\tag{5.1}
\]

and the bounded three-dimensional cutoff

\[
 \eta_M(x)=M^{-3}F_M(x_1)F_M(x_2)F_M(x_3),
\qquad 0\le\eta_M\le1.
\tag{5.2}
\]

It has width \(M^{-1}\), rational Fourier coefficients, and no quadrature
error.  It is not a compactly supported cutoff: it is an exact concentration
and mode-probe surrogate.  A statement quantified only over compactly
supported cutoffs is not refuted until an analytic approximation or tail
argument transfers the finite result.  Let \(W_N(x)=W(Nx)\), choose
\(N=8M\), and define

\[
 U_{N,M}=\mathbb P_0(\eta_M W_N),\qquad
 u_{A,N,M}=AN\,U_{N,M},
\tag{5.3}
\]

where \(\mathbb P_0\) is the periodic Leray projection followed by removal
of the zero mode.  The separation \(N=8M\) prevents the carrier from being
mistaken for a zero mode while keeping the heat and localization scales
comparable.  Every coefficient in (5.3) is rational before applying the
heat multiplier.

For a carrier-scale parameter \(\vartheta>0\), set

\[
 R=M^{-1},\qquad s=\vartheta N^{-2}
 ={\vartheta\over64}R^2.
\tag{5.4}
\]

The heat factors are retained as powers of
\(q_{N,\vartheta}=e^{-\vartheta/N^2}\).  To test the problem-freeze slice
\(s=\theta R^2\), take \(\vartheta=64\theta\).  No floating-point value of
\(q\) is needed for the polynomial identity checks.

The sequence

\[
 M=3,4,5,\ldots,\qquad N=8M
\tag{5.5}
\]

is the proposed increasingly concentrated exact family; \(M\ge3\) ensures
\(R=M^{-1}<\pi/8\), as required by the problem freeze.  The cases
\(M=1,2\) may be retained only as algebraic implementation tests, not as
admissible local-cylinder rows.  The package must measure concentration
after the nonlocal Leray projection rather than assume that the Fejér
envelope survives unchanged.  Two amplitude regimes are reported:

1. \(A=1\), to audit the Navier--Stokes scaling powers;
2. \(A=A_M\) chosen by an exact normalization of
   \(\|u_{A,N,M}\|_2\), to test whether fixed global energy can coexist with
   growth of a local dimensionless row.

The normalization itself is part of the exact output.  No asymptotic power
is to be inserted before the finite sums establish it.

The concentrated family does not license a ratio test for problem-freeze
(5.3) until the exterior functional \({\cal A}_{\rm ext}\) is frozen and is
either evaluated on the family or bounded by a proved hypothesis.  Omitting
that nonlocal row would test a different, incomplete inequality.

## 6. Tent-slice diagnostics

A static finite field cannot supply the full time integral over
\({\cal T}_R\).  It can supply the exact spatial--heat-scale slice

\[
 {\cal T}^{\rm sgn}_{\Pi}(R)
 ={1\over R}\left|
 \int_0^{R^2}\int_{\mathbb T^3}\eta_M\Pi_s\,dx\,ds\right|,
\tag{6.1}
\]

and similarly for \({\mathscr S}_s\),
\(\nabla\eta_M\cdot K_s\), and \(D_{ii,s}\).  The \(R^{-1}\)
normalization is scale invariant for one spatial--scale slice.

The \(s\)-integral is exact term by term:

\[
 \int_0^{R^2}e^{-\alpha s}\,ds
 =\begin{cases}
 (1-e^{-\alpha R^2})/\alpha,&\alpha>0,\\
 R^2,&\alpha=0.
 \end{cases}
\tag{6.2}
\]

The signed slice gives a rigorous lower bound for the corresponding
absolute spatial--scale integral,

\[
 \int_0^{R^2}\!\!\int\eta_M|\Pi_s|\,dx\,ds
 \ge
 \left|\int_0^{R^2}\!\!\int\eta_M\Pi_s\,dx\,ds\right|.
\tag{6.3}
\]

Thus an unbounded ratio based on (6.1) can refute an absolute candidate with
the same denominator.  A bounded signed ratio says nothing about the
absolute quantity.

The half-weighted slice

\[
 {\cal T}^{\rm sgn}_{\Pi,1/2}(R)
 =\left|
 \int_0^{R^2}s^{-1/2}
 \int\eta_M\Pi_s\,dx\,ds\right|
\tag{6.4}
\]

is also dimensionless at one fixed time.  Its exponential integrals involve
the exact error-function expression.  This row belongs in a separate
symbolic/interval certificate and must not be mixed with the rational
polynomial checks.

Neither (6.1) nor (6.4) is a full parabolic Carleson norm.  Promotion to a
time-integrated counterexample requires an actual smooth Navier--Stokes
solution on the claimed interval with rigorous lower and upper bounds.

## 7. Defect-channel unit test

For smooth Fourier data, \(\mu=0\).  A synthetic nonnegative measure

\[
 \mu_{\rm test}=m\,\delta_{(t_*,x_*)},\qquad m>0,
\tag{7.1}
\]

may be inserted only as a bookkeeping unit test.  It must produce

\[
 P_s\mu_{\rm test}=m\,g_s^{\rm per}(x-x_*)\delta_{t_*}\ge0
\tag{7.2}
\]

and enter (3.8) of the problem freeze with a positive sign on the payment
side.  The output must be labeled SYNTHETIC_SIGN_TEST_ONLY.
It is not evidence that (7.1) is generated by a suitable weak
Navier--Stokes solution.

## 8. Required exact output rows

Each producer must emit the following rows.

1. Reality, mean-zero, and divergence-free checks.
2. Complete mode inventories for \(v_s,\tau_s,\Pi_s,K_s,{\mathscr S}_s\),
   \(D_{ii,s},p_s,Q_s\).
3. Coefficientwise equality of the direct production formula and the
   centered-increment split.
4. Equality of the direct Gaussian-moment and subtraction constructions of
   \({\mathscr S}_s\).
5. The integrated cutoff identity with the sign
   \(-\nabla\eta\cdot K_s\).
6. The smooth Navier--Stokes tangent identity (4.4), including pressure.
7. Exact amplitude degrees and parity under \(u\mapsto-u\).
8. Numerator, every denominator term, and the simplified ratio for each
   declared absorption candidate.
9. The \(M,N,R,s\) normalization and complete table for the concentrated
   family.
10. Signed and absolute quantities kept in distinct fields.
11. A scope flag distinguishing an instantaneous counterexample, a
    tent-slice diagnostic, and a true time-integrated PDE statement.
12. navierStokesSimulation=false, nonzeroPdeDefectConstructed=false,
    carlesonEstimateProved=false, epsilonRegularityProved=false,
    clayConclusion=OPEN, and dgxUsed=false.

Two independent producers must use different constructions for
\({\mathscr S}_s\) and for the smooth tangent.  Byte equality of a common
normalized result object is required before any finite claim is sealed.

## 9. Decision table

| Observation | Licensed conclusion | Forbidden upgrade |
|---|---|---|
| Exact equality in (1.1) for every stored mode | cutoff/sign/index implementation is correct on the declared field | localized PDE estimate |
| Nonzero cubic numerator and quadratic denominator with ratio \(\to\infty\) as \(|A|\to\infty\) | the exact amplitude-independent candidate is false for all smooth data | failure of every nonlinear or ledger-complete estimate |
| Ratio grows along the exact Fejér--Leray family | the declared scale-uniform candidate is false, if all of its terms were included | blow-up, singularity, or generic turbulence |
| Ratio stays bounded for all computed \(M\) | bounded-search result | proof of a Carleson inequality |
| Smooth tangent identity passes | one-time Navier--Stokes compatibility | control over a time interval |
| Synthetic defect sign test passes | defect sign and convolution bookkeeping pass | existence of a PDE defect |
| Signed tent slice is small | signed cancellation on the family | absolute tent or Carleson control |

## 10. Stop conditions

The finite line stops and reports OPEN if:

- the only apparent obstruction disappears after restoring \(Q_s\), the
  endpoint term, or a cutoff derivative;
- the desired lower bound requires replacing a signed integral by an
  absolute integral without proof;
- the argument needs a time interval but only a static field or one time
  derivative has been computed;
- a weak defect is required but all fields are smooth;
- interval arithmetic cannot isolate the sign uniformly in the declared
  parameter range;
- the proposed conclusion exceeds the explicit quantifiers of the family.

This package is an exact falsification and normalization device.  It is not
a PDE certificate and is NOT CLAY.
