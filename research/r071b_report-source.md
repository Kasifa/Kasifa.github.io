# R0.71B — Common-response packing no-go and a sign-sensitive output coefficient

**Date:** 2026-08-25

**Audience:** analysts working on three-dimensional incompressible
Navier--Stokes regularity, Littlewood--Paley formulations, and vortex
stretching

**Status:** exact analytic families plus finite Fourier certificates; no new
continuation criterion and no regularity claim

## 1. Direct decision

R0.71A left one static possibility open.  The exact response lift from
R0.70Z contains a common-response channel that remains order one in a
high--high--low interaction.  Perhaps its sign, when retained across scales,
could still force telescoping or a Carleson gain.

R0.71B gives a two-part answer.

### 1.1 Static common response has no automatic scale compensation

There is an explicit HHL family with shell parameter (Mge4) for which the
common and chord symbols are

\[
 \mathcal U_M
 =\frac{\sqrt2M(M+1)(2M+1)}
 {(2M^2+2M+1)^{3/2}},
 \tag{1.1}
\]

\[
 \mathcal C_M
 =-\frac{\sqrt2(2M+1)}
 {2(2M^2+2M+1)^{3/2}}.
 \tag{1.2}
\]

They obey

\[
 \mathcal U_M\nearrow1,
 \qquad
 M^2\mathcal C_M\longrightarrow-\frac12.
 \tag{1.3}
\]

Thus the response chord has the expected quadratic smallness, while the
common channel does not acquire any decaying shell-gap envelope.

Two exact fans sharpen this one-triad statement.

1. A same-low-mode fan has fixed total (L^2) mass, positive total common
   work tending to (1/4), and shell-work (ell^2) norm tending to zero like
   (1/(4\sqrt N)).  No shell-count-independent
   (ell^2\)-to-(ell^1) upgrade follows from sign and common response alone.
2. A shared-high equal-radius fan gives divergence-free fields (A_N,B_N,C_N)
   with

   \[
    \sup_\alpha\|T_\alpha A_N\|_\infty\le1,
    \qquad
    \|B_N\|_2=\|C_N\|_2=\frac1{\sqrt2},
    \tag{1.4}
   \]

   but

   \[
    \left|
    \int_{\mathbb T^3}S(A_N):
    \mathcal Q_{\mathscr T}(B_N,C_N)\,dx
    \right|
    \sim\frac{\sqrt N}{8}.
    \tag{1.5}
   \]

   Hence no uniform direct estimate of this polarized common-response form by
   the three quantities in (1.4) exists.

The second result does **not** disprove the known nonlinear continuation
criterion in (L_t^1\dot B^0_{\infty,\infty}).  It rejects a particular
energy-level polarized trilinear estimate.  The established Besov criterion
uses a logarithmic higher-norm argument instead.

### 1.2 A sign-sensitive coefficient exists, but its propagation is open

Let (K_+) contain one representative of each Fourier pair
({k,-k}), and define

\[
 w_k
 =2\operatorname{Re}
 \left(\overline{\widehat S(k)}:\widehat Q(k)\right),
 \qquad
 \mathfrak P_Q=\sum_{k\in K_+}w_k.
 \tag{1.6}
\]

Put

\[
 \mathcal T_+^2
 =\sum_{\substack{k\in K_+\\\widehat S(k)\ne0}}
 \frac{(w_k^+)^2}
 {4|k|^2|\widehat S(k)|_F^2},
 \qquad
 a_+=\frac{\mathcal T_+^2}{\|\omega\|_2^2},
 \tag{1.7}
\]

with a zero quotient when (widehat S(k)=0).  Then

\[
 \boxed{
 (\mathfrak P_Q)_+
 \le\|\nabla\omega\|_2\mathcal T_+
 \le\frac\nu4\|\nabla\omega\|_2^2
 +\nu^{-1}a_+\|\omega\|_2^2.}
 \tag{1.8}
\]

This coefficient passes the R0.71A sign test.  For the two fields with the
same pointwise covariance,

\[
 \mathcal T_+^2(\omega_{\Lambda,+})
 =\frac9{800}\Lambda^4,
 \qquad
 a_+(\omega_{\Lambda,+})
 =\frac3{39940400}\Lambda^2,
 \tag{1.9}
\]

whereas

\[
 \mathcal T_+(\omega_{\Lambda,-})=a_+(\omega_{\Lambda,-})=0.
 \tag{1.10}
\]

Thus (a_+) is not a function of (Q) alone.  It retains the phase of the
strain output.  It is also not equivalent to BMO: a nonzero divergence-free
single plane wave has positive square amplitude and nonzero BMO norm but
(a_+=0).

Equation (1.8) is a deterministic consumer inequality, not a closure.  No
bound placing (a_+) in (L_t^1) follows here from Leray energy, the
covariance projector, or Navier--Stokes dynamics.  An ordinary positive
Littlewood--Paley tent square does not repair this: under standard
hypotheses it is a BMO characterization, and it is sign blind on the
R0.71A pair.

No DNS, stochastic search, GPU run, or DGX computation is justified.  The
gate is exact and analytic.

## 2. Setting and exact channel algebra

Work on the normalized torus
(mathbb T^3=(\mathbb R/2\pi\mathbb Z)^3).  Let (omega) be smooth,
real, mean-zero, and divergence-free, with

\[
 \widehat u(k)=\frac{i,k\times\widehat\omega(k)}{|k|^2},
 \qquad
 S=\frac12(\nabla u+\nabla u^{\mathsf T}).
 \tag{2.1}
\]

Use the fixed real-even radial smooth scalar Parseval frame from
R0.70P--R0.71A:

\[
 T_\alpha f\,\widehat{}\,(k)=m_\alpha(k)\widehat f(k),
 \qquad
 \sum_\alpha m_\alpha(k)^2=1.
 \tag{2.2}
\]

Its response vector and correlation are

\[
 V(k)=(m_\alpha(k))_\alpha,
 \qquad
 \Gamma(p,q)=\langle V(p),V(q)\rangle.
 \tag{2.3}
\]

Equal radii have identical responses because the frame is radial.  Radii
separated by a strict factor greater than four have orthogonal responses
because each multiplier is supported in (1/2<2^{-j}|k|<2).

The frame covariance and its polarization are

\[
 Q(\omega)=\sum_\alpha T_\alpha\omega\otimes T_\alpha\omega,
 \tag{2.4}
\]

\[
 \mathcal Q_{\mathscr T}(f,g)
 =\sum_\alpha T_\alpha f\odot T_\alpha g,
 \qquad
 a\odot b=\frac{a\otimes b+b\otimes a}{2}.
 \tag{2.5}
\]

For a resonant triad (n+p+q=0), let (A_n,A_p,A_q) be the three
symmetrized strain placements from R0.70X.  They obey

\[
 |n|^2A_n+|p|^2A_p+|q|^2A_q=0.
 \tag{2.6}
\]

Define

\[
 \mathcal F=A_n+A_p+A_q,
 \tag{2.7}
\]

\[
 \mathcal P
 =\Gamma(p,q)A_n+
  \Gamma(q,n)A_p+
  \Gamma(n,p)A_q,
 \tag{2.8}
\]

and

\[
 \boxed{
 \mathcal U=\frac{\mathcal F+\mathcal P}{2},
 \qquad
 \mathcal C=\frac{\mathcal F-\mathcal P}{2}.}
 \tag{2.9}
\]

Then

\[
 \mathcal F=\mathcal U+\mathcal C,
 \qquad
 \mathcal P=\mathcal U-\mathcal C.
 \tag{2.10}
\]

This is the trace-level form of the (H^+,H^-,H^\Delta) response lift in
R0.70Z.  The names “common” and “chord” refer to (2.9), not to a new
published function space.

## 3. One HHL atom: the common channel remains order one

For (M\ge4), put

\[
 \begin{aligned}
 n&=(1,1,0),\\
 p_M&=(M,-M-1,0),\\
 q_M&=(-M-1,M,0),
 \end{aligned}
 \qquad
 R_M^2=2M^2+2M+1,
 \tag{3.1}
\]

and choose unit polarizations

\[
 c=\frac{(1,-1,0)}{\sqrt2},
 \qquad
 a=e_3,
 \qquad
 b_M=\frac{(M,M+1,0)}{R_M}.
 \tag{3.2}
\]

Direct arithmetic gives

\[
 n+p_M+q_M=0,
 \qquad
 n\cdot c=p_M\cdot a=q_M\cdot b_M=0,
 \tag{3.3}
\]

and

\[
 |p_M|=|q_M|=R_M>4|n|.
 \tag{3.4}
\]

Therefore

\[
 \Gamma(p_M,q_M)=1,
 \qquad
 \Gamma(n,p_M)=\Gamma(n,q_M)=0.
 \tag{3.5}
\]

The exact strain legs are

\[
 A_n=\frac{2M+1}{\sqrt2R_M},
 \tag{3.6}
\]

\[
 A_p=\frac{2M+1}{\sqrt2R_M}
 \left(1-\frac2{R_M^2}\right),
 \qquad
 A_q=-\frac{2M+1}{\sqrt2R_M}.
 \tag{3.7}
\]

They satisfy (2.6) exactly.  Substitution into (2.7)--(2.9) gives
(1.1)--(1.2).  Moreover,

\[
 \frac{d\mathcal U_M}{dM}
 =\frac{\sqrt2(5M^2+5M+1)}
 {(2M^2+2M+1)^{5/2}}>0.
 \tag{3.8}
\]

Hence

\[
 \mathcal U_M\ge\mathcal U_4
 =\frac{180\sqrt{82}}{1681}>0.969.
 \tag{3.9}
\]

### Theorem 3.1 — no decaying common-response shell envelope

There is no sequence (h_m\to0) and constant independent of the shell gap
such that every strictly separated HHL triad satisfies

\[
 |\mathcal U_{kJJ}|
 \le C h_{J-k}\times
 \text{the product of its three Fourier amplitudes}.
 \tag{3.10}
\]

The family (3.1)--(3.2) has (J-k\to\infty), but its normalized common
symbol tends to one.  The same family is consistent with the R0.70Y chord
gain because (mathcal C_M=O(M^{-2})).

## 4. Same-low fan: no automatic ℓ2-to-ℓ1 scale upgrade

Let

\[
 M_j=8^j,
 \qquad j=1,\ldots,N,
 \tag{4.1}
\]

and retain the same low mode (n,c) from (3.1)--(3.2).  Define

\[
 \omega_N
 =c\cos(n\cdot x)
 +\frac1{\sqrt N}\sum_{j=1}^N
 \left[
 a\cos(p_{M_j}\cdot x)
 +b_{M_j}\cos(q_{M_j}\cdot x)
 \right].
 \tag{4.2}
\]

### 4.1 Exact response and resonance separation

The high radii are pairwise separated by more than four.  Indeed,

\[
 R_{8M}^2-16R_M^2
 =96M^2-16M-15>0
 \qquad(M\ge8).
 \tag{4.3}
\]

Also (R_8^2=145>16|n|^2=32).  Thus each high pair has one common response,
different high pairs have orthogonal responses, and every high response is
orthogonal to the low response.

The zero-sum triple classification is exact.  The coordinate sum (x_1+x_2)
equals (2) on (n), (-1) on every (p_M,q_M), and changes sign under
frequency negation.  A resonant triple must therefore contain (n) and two
positive high modes, or its full negative.  Finally,

\[
 p_M+q_L=-n
 \quad\Longleftrightarrow\quad M=L.
 \tag{4.4}
\]

Hence the only resonances are the intended
(pm(n,p_{M_j},q_{M_j})), with their six permutations.  There are exactly
(12N) ordered resonances.

### 4.2 Fixed energy and the packing gap

Orthogonality and normalized torus integration give

\[
 \|\omega_N\|_2^2
 =\frac12+2N\frac1{2N}
 =\frac32.
 \tag{4.5}
\]

The common work from shell (j) is

\[
 w_j=\frac{\mathcal U_{M_j}}{4N}>0.
 \tag{4.6}
\]

Therefore

\[
 \mathfrak U_N
 =\sum_{j=1}^Nw_j
 =\frac1{4N}\sum_{j=1}^N\mathcal U_{8^j}
 \longrightarrow\frac14,
 \tag{4.7}
\]

while

\[
 \left(\sum_{j=1}^N|w_j|^2\right)^{1/2}
 =\frac1{4N}
 \left(\sum_{j=1}^N\mathcal U_{8^j}^2\right)^{1/2}
 \sim\frac1{4\sqrt N}.
 \tag{4.8}
\]

For the certified (N=8) instance, the exact producer and an independent
Fourier reconstruction both find 34 signed modes, 96 ordered resonances,

\[
 \mathfrak U_8=0.2497261589\ldots,
 \qquad
 \|w\|_{\ell^2}=0.08829188725\ldots.
 \tag{4.9}
\]

### Theorem 4.1 — same sign is not a packing theorem

There is no constant independent of (N) such that the same-low fan obeys

\[
 \left(\sum_{j=1}^Nw_j\right)_+
 \le C\left(\sum_{j=1}^N|w_j|^2\right)^{1/2}.
 \tag{4.10}
\]

The result does not rule out a Carleson norm that records all (N) units of
packing mass.  It rules out manufacturing that mass from sign or common
response alone.

## 5. Shared-high fan: the direct shell-supremum estimate fails

The preceding fan holds the low mode fixed.  A complementary construction
holds one high mode fixed and puts the coefficient across separated low
scales.

Let

\[
 M_j=16^j,
 \qquad
 d_j=1+M_j^2,
 \qquad
 Q_N=\prod_{j=1}^Nd_j.
 \tag{5.1}
\]

Set

\[
 q=(Q_N,0,0),
 \tag{5.2}
\]

\[
 p_j=\frac{Q_N}{d_j}
 (1-M_j^2,,2M_j,,0),
 \tag{5.3}
\]

\[
 n_j=-q-p_j
 =-\frac{2Q_N}{d_j}(1,M_j,0).
 \tag{5.4}
\]

Every frequency is integral.  They obey

\[
 |p_j|=|q|=Q_N,
 \qquad
 |n_j|=\frac{2Q_N}{\sqrt{d_j}}.
 \tag{5.5}
\]

Choose unit polarizations

\[
 c_j=\frac{(M_j,-1,0)}{\sqrt{d_j}},
 \qquad
 a_j=\frac{(-2M_j,1-M_j^2,0)}{d_j},
 \qquad
 b=e_3.
 \tag{5.6}
\]

Then

\[
 n_j\cdot c_j=p_j\cdot a_j=q\cdot b=0.
 \tag{5.7}
\]

Define

\[
 A_N=\sum_{j=1}^Nc_j\cos(n_j\cdot x),
 \tag{5.8}
\]

\[
 B_N=\frac1{\sqrt N}\sum_{j=1}^Na_j\cos(p_j\cdot x),
 \qquad
 C_N=b\cos(q\cdot x).
 \tag{5.9}
\]

### 5.1 Why every intended response is exactly common

All (p_j) and (q) have the same radius.  Therefore

\[
 V(p_j)=V(q),
 \qquad
 \Gamma(p_j,q)=1
 \tag{5.10}
\]

for the actual fixed radial frame, not merely for a sharp dyadic model.

Since (M_1=16), every high/low radius ratio is greater than eight.  Also

\[
 \frac{|n_j|}{|n_{j+1}|}
 =\sqrt{\frac{1+M_{j+1}^2}{1+M_j^2}}>4.
 \tag{5.11}
\]

Thus distinct low responses and every low/high response are orthogonal.

The support has no unintended resonant triple.  Every high mode is a vector
of the form (pm q) plus either zero or one low shift.  Three high modes
cannot sum to zero because their (q)-coefficient is odd and the low shifts
have total magnitude less than (Q_N/2).  One high mode cannot be canceled
by two lows.  With two high modes, cancellation of the (q)-coefficient
reduces the problem to a relation among at most three low vectors.  Their
strict factor-four lacunarity makes the largest magnitude greater than the
sum of the other two, except for the intended
(n_j+p_j+q=0).  Repeated-index cases are immediate from their different
directions.  Therefore there are exactly (12N) ordered resonances.

### 5.2 Exact polarized common work

Define the polarized covariance form (2.5).  Equal response gives

\[
 \mathcal Q_{\mathscr T}(B_N,C_N)=B_N\odot C_N.
 \tag{5.12}
\]

For the (j)-th triad, direct contraction gives

\[
 A_{n_j}=-\frac{M_j}{\sqrt{1+M_j^2}}.
 \tag{5.13}
\]

The normalized real-cosine integral is therefore

\[
 \boxed{
 \mathfrak P_{\rm cr}(A_N;B_N,C_N)
 :=\int S(A_N):\mathcal Q_{\mathscr T}(B_N,C_N)\,dx
 =-\frac1{8\sqrt N}
 \sum_{j=1}^N\frac{M_j}{\sqrt{1+M_j^2}}.}
 \tag{5.14}
\]

In particular,

\[
 |\mathfrak P_{\rm cr}|
 \sim\frac{\sqrt N}{8}.
 \tag{5.15}
\]

At the same time,

\[
 \|B_N\|_2^2=\|C_N\|_2^2=\frac12.
 \tag{5.16}
\]

Every frame block (T_\alpha) sees at most one low cosine because of
(5.11).  Parseval gives (|m_\alpha(k)|\le1), so

\[
 \mathcal B_{\mathscr T}(A_N)
 :=\sup_\alpha\|T_\alpha A_N\|_\infty\le1.
 \tag{5.17}
\]

### Theorem 5.1 — polarized shell-supremum no-go

There is no universal (C) such that all real smooth divergence-free
triples satisfy

\[
 |\mathfrak P_{\rm cr}(A;B,C)|
 \le C\mathcal B_{\mathscr T}(A)
 \|B\|_2\|C\|_2.
 \tag{5.18}
\]

Indeed the ratio in (5.18) for (5.8)--(5.9) is

\[
 \frac1{4\sqrt N}
 \sum_{j=1}^N\frac{M_j}{\sqrt{1+M_j^2}}
 \sim\frac{\sqrt N}{4}.
 \tag{5.19}
\]

For (N=8), both exact reconstructions give

\[
 \mathfrak P_{\rm cr}=-0.3534669874\ldots,
 \qquad
 \text{ratio}=0.7069339748\ldots.
 \tag{5.20}
\]

The theorem concerns the **polarized** three-field form.  It does not assert
failure of the known one-field estimate or continuation theorem involving
(|\omega\|_{\dot B^0_{\infty,\infty}}\|\omega\|_2^2).  In the full
one-field norm, the complete high block and the low field must be counted
together.

## 6. Why the canonical positive tent is the BMO boundary

For an admissible inhomogeneous periodic Littlewood--Paley resolution, the
standard square tent functional is

\[
 \mathcal C_\Delta(f)
 =\sup_{R\in\mathcal D(\mathbb T^3)}
 \left[
 \frac1{|R|}\int_R
 \sum_{j\ge j(R)-O(1)}|\Delta_jf(x)|^2\,dx
 \right]^{1/2}.
 \tag{6.1}
\]

The standard Littlewood--Paley/Carleson characterization gives

\[
 \mathcal C_\Delta(f)\simeq\|f\|_{\mathrm{BMO}}
 \tag{6.2}
\]

modulo constants.  In Triebel--Lizorkin notation this is
(F^0_{\infty,2}=\mathrm{BMO}).  This is established harmonic analysis, not
an R0.71B theorem.

For the shared-high fan, the root tent already records

\[
 \int_{\mathbb T^3}\sum_j|\Delta_jA_N|^2\,dx
 =\|A_N\|_2^2=\frac N2.
 \tag{6.3}
\]

Thus the positive tent norm grows like (sqrt N), exactly the scale needed
to absorb (5.15).  It does not produce a weaker coefficient.

It also loses the sign information needed here.  The R0.71A fields satisfy

\[
 Q(\omega_{\Lambda,+})(x)
 =Q(\omega_{\Lambda,-})(x)
 \tag{6.4}
\]

at every point.  Because the sign-flipped base responses are strictly
separated from the unchanged filler responses, every scale-resolved square
mass is also identical.  Nevertheless their covariance works have opposite
sign.  Any candidate depending only on nonnegative frame square mass cannot
distinguish the pair.

Classical Carleson embedding uses a positive measure or its total variation.
Controlling only the signed mass of a tent box permits arbitrary internal
cancellation and does not invoke that theorem.  A useful signed replacement
would need a proved partial-sum, paraproduct, or dynamical telescoping
estimate.

## 7. The positive-output coefficient

Let (K_+) contain exactly one representative of each nonzero pair
({k,-k}).  Since the field is real,

\[
 \mathfrak P_Q
 =\sum_{k\in K_+}
 2\operatorname{Re}
 \left(\overline{\widehat S(k)}:\widehat Q(k)\right)
 =\sum_{k\in K_+}w_k.
 \tag{7.1}
\]

For a divergence-free Fourier coefficient,

\[
 |\widehat S(k)|_F^2
 =\frac12|\widehat\omega(k)|^2.
 \tag{7.2}
\]

Consequently,

\[
 4\sum_{k\in K_+}|k|^2|\widehat S(k)|_F^2
 =\|\nabla\omega\|_2^2.
 \tag{7.3}
\]

### Theorem 7.1 — exact positive-output Cauchy--Young reduction

For (mathcal T_+) defined in (1.7),

\[
 \begin{aligned}
 (\mathfrak P_Q)_+
 &\le\sum_{k\in K_+}w_k^+\\
 &=\sum_{k\in K_+}
 2|k||\widehat S(k)|_F
 \frac{w_k^+}{2|k||\widehat S(k)|_F}\\
 &\le\|\nabla\omega\|_2\mathcal T_+.
 \end{aligned}
 \tag{7.4}
\]

Young's inequality is exact in the form

\[
 \frac\nu4D+\frac1\nu\mathcal T_+^2
 -\sqrt D\mathcal T_+
 =\left(
 \frac{\sqrt{\nu D}}2-
 \frac{\mathcal T_+}{\sqrt\nu}
 \right)^2\ge0.
 \tag{7.5}
\]

This proves (1.8).  The coefficient (a_+) has the critical time scaling:
dimensionally it scales like inverse time, so an (L_t^1) bound would match
the enstrophy consumer.  The theorem does not supply that bound.

### 7.1 Exact R0.71A test

For the R0.71A positive field, the only nonzero signed output is

\[
 w_{(1,0,1)}=\frac{3\sqrt2}{40}\Lambda^3.
 \tag{7.6}
\]

Since

\[
 \|\omega_{\Lambda,\pm}\|_2^2
 =\frac{299553}{2}\Lambda^2,
 \tag{7.7}
\]

formulas (1.9)--(1.10) follow.  The negative field has the same covariance
but the sole output is negative.  Hence its positive-output square vanishes.

### 7.2 It is not a BMO norm

Let

\[
 \omega_N=e_2\cos(Nx_1).
 \tag{7.8}
\]

This is nonzero and divergence-free.  Its square-function/BMO amplitude is
nonzero, but the strain polarization is orthogonal to its covariance.  The
exact Fourier calculation gives

\[
 \mathfrak P_Q(\omega_N)=0,
 \qquad
 \mathcal T_+(\omega_N)=a_+(\omega_N)=0.
 \tag{7.9}
\]

Thus (a_+) is a sign-sensitive nonlinear coefficient, not a norm and not a
BMO-equivalent positive tent quantity.

## 8. What the enstrophy consumer would require

Let

\[
 Y(t)=\|\omega(t)\|_2^2,
 \qquad
 D(t)=\|\nabla\omega(t)\|_2^2.
 \tag{8.1}
\]

The exact split is

\[
 \frac12Y'+\nu D
 =\mathfrak P_Q+\mathfrak E_S.
 \tag{8.2}
\]

R0.70Y proved the mixed defect bound

\[
 |\mathfrak E_S|
 \le C_{\mathscr T}
 \|\omega\|_{B^0_{\infty,\infty}}Y.
 \tag{8.3}
\]

Combining (1.8) and (8.3) gives

\[
 \frac12Y'+\frac{3\nu}{4}D
 \le
 \left[
 \nu^{-1}a_+
 +C_{\mathscr T}
 \|\omega\|_{B^0_{\infty,\infty}}
 \right]Y.
 \tag{8.4}
\]

Thus integrability of the bracket is sufficient for the existing enstrophy
argument.  This statement is not a new continuation criterion: the
(L_t^1\dot B^0_{\infty,\infty}) vorticity condition is already known, and
it alone is sufficient in the established theorem of
Kozono--Ogawa--Taniuchi.  Equation (8.4) only verifies that (a_+) has the
correct consumer and sign sensitivity.

A nonredundant next step must do at least one of the following:

1. derive (a_+\in L_t^1) and control the defect without assuming an already
   sufficient Besov coefficient;
2. localize (mathcal T_+) into a genuine signed tent quantity and prove a
   Navier--Stokes partial-sum estimate;
3. connect (a_+) quantitatively to the transverse residual or another
   independently propagated critical quantity.

## 9. Literature boundary

The source audit gives the following classifications.

- Bony's paraproduct decomposition separates low--high, high--low, and
  resonant frequency interactions.  It is a bookkeeping identity and does
  not itself provide sign cancellation.
- Coifman--Meyer--Stein tent spaces and the Fefferman--Stein/Frazier--Jawerth
  Littlewood--Paley theory place the ordinary positive square tent at the
  BMO boundary.
- CLMS compensated compactness followed by Hardy--BMO duality supplies the
  established signed endpoint

  \[
   |\mathfrak I|
   \lesssim\|\omega\|_{\mathrm{BMO}}\|\omega\|_2^2.
   \tag{9.1}
  \]

  It does not derive the BMO coefficient from Leray energy or covariance
  geometry.
- Kozono--Taniuchi and Kozono--Ogawa--Taniuchi already give BMO and
  (dot B^0_{\infty,\infty}) continuation criteria.  R0.71B therefore does
  not claim that BMO is the weakest known criterion, nor that a shell
  supremum can never be used by a different method.
- Koch--Tataru's (BMO^{-1}) tent norm is a positive critical small-data
  space.  It does not provide a signed large-data common-response
  cancellation.

The bounded search did not locate the exact fans (4.2) or (5.8)--(5.9), or
the coefficient (1.7), in the checked sources.  This is not a priority or
novelty claim.  A publication-level novelty statement would require a wider
specialist search and external review.

## 10. Research value and stopping decision

R0.71B closes three tempting shortcuts.

1. **Chord transfer:** the small response chord does not transfer to the
   common channel.
2. **Same-sign packing:** retaining the signs does not by itself upgrade
   shell (ell^2) control to an unweighted positive sum.
3. **Shell supremum:** a direct polarized
   (B^0_{\infty,\infty}\)-type shell supremum with two (L^2) factors
   cannot control the common form.

It also records one viable reduction variable.  The positive-output
coefficient (a_+) sees the missing phase and has the exact dissipation
consumer (1.8).  Its usefulness now depends entirely on a noncircular
Navier--Stokes propagation or localization theorem.  Calling (1.7) a
solution without that theorem would only rename the unresolved work.

This stage does not improve the known unconditional theory, prove a
singularity, prove global regularity, or solve any part of the Clay problem
in the theorem-reduction sense.  Its value is a precise route classification
and a reproducible signed target for the next stage.

## 11. Next justified gate: R0.71C

R0.71C should test a **signed-before-square localization** of (1.7).
The preassigned target is not an ordinary positive LP Carleson measure.
It should retain the strain phase in local packets and seek one of:

1. a uniform bound for signed partial sums over nested tents;
2. a Navier--Stokes flux identity that telescopes between adjacent time--scale
   boxes; or
3. a quantitative estimate of the local positive-output coefficient by the
   transverse residual and a genuinely propagated critical norm.

The acceptance test must include both fans in Sections 4--5, the R0.71A
same-covariance sign pair, and comparison with existing BMO, dyadic-BMO, and
(dot B^0_{\infty,\infty}) criteria.  If the localization reduces exactly to
the positive tent in (6.1), the route stops as a BMO restatement.

No large computation is justified before this analytic localization is
defined.

## 12. Reproduction boundary

Run the exact producer:

~~~bash
tmp/r068b-venv/bin/python research/r071b_exact_audit.py
~~~

Run the independent checker:

~~~bash
tmp/r068b-venv/bin/python research/r071b_independent_audit.py
~~~

The producer checks ten groups, including:

1. the exact HHL strain legs, weighted cyclic null, common/chord formulas,
   derivative, and limits;
2. all (N=8) same-low fan modes and 96 ordered resonances;
3. the fixed energy, total common work, and shell (ell^2) sequence for
   (N=1,2,4,8);
4. the integer rational-circle construction for the shared-high fan;
5. all strict response separations and 96 shared-high resonances;
6. the full Fourier reconstruction of the polarized common work;
7. the frame shell-supremum, root tent mass, and normalized ratio;
8. the exact R0.71A positive and negative output ledgers;
9. the strain-gradient Parseval identity and Young square; and
10. the plane-wave non-equivalence test.

The independent checker reimplements the Fourier strain, convolution, and
work calculation without importing the R0.71B producer.  It reproduces the
two (N=8) fan values and the R0.71A output constants.

The finite checks do not prove the arbitrary-(N) resonance lemmas, the
standard BMO Carleson characterization, the cited continuation theorems, a
time-integrability estimate for (a_+), or any Navier--Stokes regularity
conclusion.  Those analytic dependencies and boundaries are stated above.
