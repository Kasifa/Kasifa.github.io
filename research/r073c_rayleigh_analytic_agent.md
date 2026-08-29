# R0.73C independent analytic audit: the cubic neutral level and the frozen Rayleigh branch

> **Working-note status (2026-08-30):** this is the pre-certificate branch
> audit.  The later validated monodromy proof closes C4 at \(\gamma=1/2\);
> see `r073c_monodromy_proof.md` and `r073c_report-source.md`.  Root
> uniqueness and C5 remain open.

**Date:** 2026-08-30  
**Scope:** C3--C4 of `research/r073c_problem_freeze.md` only  
**Public status:** no public-release authorization is supplied by this note

## 0. Decision

The exact collision neutral mode can be closed analytically, including its
periodic Sobolev domain.  The strongest conclusion established here is

\[
 \boxed{
  \gamma_0=\frac{\sqrt7}{2},\qquad
  0\in\sigma_p(A_{\gamma_0}(0)).
 }
 \tag{0.1}
\]

The singular Sturm--Liouville operator at this neutral level has exactly one
negative eigenvalue, namely \(-7/4\), and its next eigenvalue is zero.

This fact alone does **not** prove an unstable Rayleigh eigenvalue.  The
standard Lin/Tollmien theorems located in the primary literature cannot be
quoted for the present profile: their boundedness, sign, integrability,
critical-level, and/or boundary hypotheses fail.  In particular,

\[
 -\frac{W_0''}{W_0}
 =4-\frac{3}{1-\cos x}
 =-\frac6{x^2}+\frac72+O(x^2)
 \tag{0.2}
\]

is neither bounded nor locally integrable at the cubic zero.

There is nevertheless a sharp conditional direction calculation.  If a
PT-symmetric purely growing branch \(c=i\eta\), \(\eta>0\), converges to the
neutral mode, then necessarily

\[
 \boxed{
  \eta=\frac{7/4-\gamma^2}{4}
       +o\!\left(7/4-\gamma^2\right),
  \qquad
  \sigma=\gamma\eta>0.
 }
 \tag{0.3}
\]

Thus the unstable side, **conditional on branch existence**, is
\(0<\gamma<\sqrt7/2\).  Finite Fourier calculations reproduce the coefficient
\(1/4\) to high accuracy, but cutoff convergence is not an
infinite-dimensional existence proof.  Consequently the ledger supported by
this analytic audit is

| item | state after this audit | reason |
|---|---|---|
| C3: exact neutral mode | **THEOREM / CLOSED** | Sections 2--3 below |
| uniqueness of the negative neutral threshold | **THEOREM / CLOSED** | exact Pöschl--Teller spectrum |
| side and first slope of a convergent pure-growth branch | **CONDITIONAL THEOREM** | Section 5 |
| C4: existence of \(\operatorname{Re}\sigma>0\) point spectrum | **NOT CLOSED ANALYTICALLY HERE** | requires the missing singular continuation lemma or a rigorous infinite-dimensional enclosure |
| instability for every \(0<\gamma<\sqrt7/2\) | **OPEN** | stronger than C4 and not implied by the neutral identity |

## 1. Operator and phase-speed convention

Work on \(\mathbb T_{2\pi}=\mathbb R/(2\pi\mathbb Z)\), with

\[
 W_0(x)=-\frac12\sin x+\frac14\sin2x,
 \qquad
 L_\mu=-\partial_x^2+\mu,
 \qquad \mu=\gamma^2>0.
 \tag{1.1}
\]

If \(q=L_\mu\phi\), the eigenvalue equation

\[
 A_\gamma q=\sigma q,
 \qquad
 A_\gamma=-i\gamma\left(W_0+W_0''L_\mu^{-1}\right),
 \tag{1.2}
\]

is equivalent, with \(\sigma=-i\gamma c\), to

\[
 (W_0-c)(\phi''-\mu\phi)-W_0''\phi=0.
 \tag{1.3}
\]

Hence \(c=i\eta\), \(\eta>0\), gives the real growing eigenvalue
\(\sigma=\gamma\eta>0\).

The essential spectrum must be kept in view.  Since
\(W_0''L_\mu^{-1}\) is compact on \(L^2(\mathbb T_{2\pi})\),

\[
 \sigma_{\rm ess}(A_\gamma)
 =-i\gamma\,\operatorname{Ran}(W_0),
 \tag{1.4}
\]

which contains zero.  The neutral eigenvalue in (0.1) is therefore embedded;
ordinary isolated-eigenvalue Kato perturbation does not apply.

## 2. The periodic neutral mode is legitimate

On the fundamental interval \(0<x<2\pi\), set

\[
 s=\sin\frac x2,
 \qquad
 \phi_0(x)=s^3.
 \tag{2.1}
\]

At the two endpoints, \(\phi_0=\phi_0'=0\).  Its periodic extension is
\(|\sin(x/2)|^3\) when represented on \((-\pi,\pi)\).  It is \(C^2\) and
belongs to \(H^2_{\rm per}\), although it is not \(C^3\) at the joined cubic
level.  This distinction matters: calling the raw formula
"anti-periodic" and discarding it would be incorrect in the periodic Sobolev
domain.

An independent Fourier check is

\[
 \phi_0(x)=\frac4{3\pi}
 +\sum_{n=1}^{\infty}
 \frac{24}{\pi(1-4n^2)(9-4n^2)}\cos(nx).
 \tag{2.2}
\]

The coefficients are \(O(n^{-4})\), proving \(H^2_{\rm per}\) regularity
directly.  In particular,

\[
 q_0=L_{7/4}\phi_0
 =4\sin^3\frac x2-\frac32\sin\frac x2
 \quad (0<x<2\pi)
 \tag{2.3}
\]

defines a nonzero element of \(L^2(\mathbb T_{2\pi})\).

## 3. Exact identity and the complete singular threshold spectrum

Factorization of the profile gives

\[
 W_0=-2\sin^3\frac x2\cos\frac x2,
 \qquad
 \frac{W_0''}{W_0}
 =-4+\frac{3}{1-\cos x}
 =-4+\frac{3}{2\sin^2(x/2)}.
 \tag{3.1}
\]

Direct differentiation yields

\[
 \phi_0''=\frac32\sin\frac x2
             -\frac94\sin^3\frac x2,
 \tag{3.2}
\]

and therefore, almost everywhere and distributionally on the torus,

\[
 \left(-\partial_x^2+\frac{W_0''}{W_0}\right)\phi_0
 =-\frac74\phi_0.
 \tag{3.3}
\]

There is no delta mass at the joined endpoint because \(\phi_0'\) matches
there.  Equation (3.3) also gives

\[
 q_0=-\frac{W_0''}{W_0}\phi_0,
 \qquad
 W_0q_0+W_0''\phi_0=0,
 \tag{3.4}
\]

so (1.2) proves \(A_{\sqrt7/2}q_0=0\).  This closes C3.

The negative-threshold count is also exact.  Put \(t=x/2\).  On
\((0,\pi)\), the singular point is represented by the two endpoints and

\[
 4H_0=-\partial_t^2+6\csc^2t-16.
 \tag{3.5}
\]

The coefficient \(6>3/4\) makes both endpoints limit point.  For
\(Q_3=\partial_t-3\cot t\),

\[
 -\partial_t^2+6\csc^2t=Q_3^*Q_3+9.
 \tag{3.6}
\]

Thus the ground value is 9, with ground state \(\sin^3t\).  More
generally the Friedrichs spectrum is

\[
 \lambda_n\!\left(-\partial_t^2+6\csc^2t\right)=(n+3)^2,
 \qquad
 \psi_n(t)=\sin^3t\,C_n^3(\cos t),
 \qquad n=0,1,\ldots,
 \tag{3.7}
\]

where \(C_n^3\) is a Gegenbauer polynomial.  Consequently

\[
 \sigma(H_0)
 =\left\{\frac{(n+3)^2-16}{4}:n=0,1,\ldots\right\}
 =\left\{-\frac74,0,\frac94,5,\ldots\right\}.
 \tag{3.8}
\]

The zero state is proportional to
\(\sin^3t\cos t=-W_0/2\).  Hence \(-7/4\) is the unique negative
eigenvalue of this singular neutral operator.

At fixed positive \(\gamma\), zero is one embedded neutral eigenvalue, not
two distinct conjugate eigenvalues.  The word "pair" is safe only if it means
the pair \((c,\gamma)=(0,\sqrt7/2)\), or if the two rows \(\pm\gamma\) are
being counted explicitly.

## 4. What the cubic critical level changes

Near the joined point \(x=0\),

\[
 W_0(x)=-\frac{x^3}{4}+\frac{x^5}{16}+O(x^7),
 \qquad
 W_0''(x)=-\frac32x+\frac54x^3+O(x^5),
 \tag{4.1}
\]

and

\[
 \frac{W_0''}{W_0}
 =\frac6{x^2}-\frac72+O(x^2).
 \tag{4.2}
\]

The indicial equation for the neutral Sturm--Liouville problem is
\(r(r-1)=6\), giving \(r=3\) and \(r=-2\).  The \(H^1\) branch is the
cubic one; the \(x^{-2}\) branch is excluded.  This proves why the neutral
state lies in the Friedrichs domain, but it also shows why the coefficient
cannot be treated as a regular bounded potential.

For nonzero phase speed near zero, a critical point of order three has a
different connection problem from a simple critical level.  Local Rayleigh
analysis at a degeneracy of order \(n\) produces the scale
\(|c|^{2-1/n}\); here this is \(|c|^{5/3}\).  Thus ordinary holomorphic
dependence through \(c=0\) is not available without a weighted singular
analysis.  This is consistent with the direct power count in Section 5:
the cubic point contributes \(O(\eta^{5/3})\), while the simple zero at
\(x=\pi\) contributes the leading \(O(\eta)\) term.

## 5. Exact branch-side calculation

This section separates an exact identity from its missing existence premise.
Suppose that for \(\eta\downarrow0\) there is a PT-symmetric periodic branch

\[
 c=i\eta,\qquad
 \mu=\mu(\eta),\qquad
 \phi_\eta\longrightarrow\phi_0,
 \tag{5.1}
\]

with normalization \(\phi_\eta(\pi)\to1\), and with convergence strong
enough to pass the two critical layers in the weighted pairing below.  This
is the premise that remains to be proved by a singular Evans or weighted
Lyapunov--Schmidt lemma.

Away from the zeros of \(W_0\), (1.3) can be written

\[
 (H_0+\mu)\phi_\eta
 +c\frac{W_0''}{W_0(W_0-c)}\phi_\eta=0.
 \tag{5.2}
\]

Pairing with \(\phi_0\) and using (3.3) gives the exact solvability identity

\[
 (\mu-\mu_0)\langle\phi_0,\phi_\eta\rangle
 +c\int_{0}^{2\pi}
 \frac{W_0''\phi_0\phi_\eta}{W_0(W_0-c)}\,dx=0,
 \qquad \mu_0=\frac74.
 \tag{5.3}
\]

The neutral mass is

\[
 N_0=\|\phi_0\|_2^2
 =2\int_0^\pi\sin^6t\,dt
 =\frac{5\pi}{8}.
 \tag{5.4}
\]

At the simple critical level \(x=\pi\),

\[
 W_0'(\pi)=1,
 \qquad
 \left.\frac{W_0''}{W_0}\right|_{x=\pi}
 =\frac{W_0'''(\pi)}{W_0'(\pi)}=-\frac52,
 \qquad
 \phi_0(\pi)=1.
 \tag{5.5}
\]

The elementary Poisson-kernel limit therefore gives

\[
 \frac1\eta\,i\eta\int_{0}^{2\pi}
 \frac{W_0''\phi_0\phi_\eta}{W_0(W_0-i\eta)}\,dx
 \longrightarrow \frac{5\pi}{2}.
 \tag{5.6}
\]

PT symmetry cancels the nonsingular imaginary principal-value part.  Near
the cubic point, \(W_0\sim-x^3/4\),
\(W_0''/W_0\sim6/x^2\), and
\(\phi_0\sim |x|^3/8\); its real contribution is
\(O(\eta^{5/3})=o(\eta)\).  Substitution of (5.4)--(5.6) into (5.3) yields

\[
 (\mu-\mu_0)\frac{5\pi}{8}
 +\frac{5\pi}{2}\eta+o(\eta)=0,
 \tag{5.7}
\]

which is exactly

\[
 \mu-\frac74=-4\eta+o(\eta).
 \tag{5.8}
\]

This proves (0.3) **once the branch premise (5.1) is supplied**.  It does not
prove that such a branch exists.

## 6. Why the standard criteria are unavailable

### 6.1 Lin 2003, class \(K\) / odd-flow arguments

Lin's class \(K\) assumes
\(-U''/(U-U_s)\) nonnegative and bounded; class \(K_+\) assumes it is
positive.  Here, for \(U_s=0\), (0.2) is unbounded and changes sign.  The
odd-flow theorem still assumes bounded \(K\), and its displayed problem has
Dirichlet channel boundary conditions rather than the present periodic
fiber.  Neither theorem can be quoted unchanged.

There is a second caution: the later 2014 correction of the odd-flow count
adds the interval below the smallest neutral wave number when the number of
negative Sturm--Liouville eigenvalues is odd.  Therefore the older interval
formula should not be imported without that correction even in a regular
problem.

### 6.2 The 2014 unbounded-\(K\) extension

Qi--Chen--Xie's smooth theorem allows \(K\in L^1\).  The present
\(K\sim-6/x^2\) is not in \(L^1_{\rm loc}\).  Their separate piecewise-smooth
framework has additional junction hypotheses; smoothness of \(W_0\) by
itself does not verify those hypotheses.  No theorem from that paper is used
here.

### 6.3 Class \(F\)

Lin's class \(F\) requires \(U''\) to have the same sign at all preimages of
every non-inflection value.  The present profile fails this condition.  For a
small negative value of \(U\), one preimage is near \(0^+\), where
\(U''<0\), and another is near \(\pi^-\), where \(U''>0\).

### 6.4 Regular Tollmien derivative

The regular Tollmien formula assumes, among other things, a bounded regular
quotient and nonzero \(U'\) at the relevant critical points.  Although the
zero at \(x=\pi\) is simple, the same phase speed also meets the cubic zero
at \(x=0\), where

\[
 W_0(0)=W_0'(0)=W_0''(0)=0,
 \qquad W_0'''(0)=-\frac32.
 \tag{6.1}
\]

One may not delete that critical point from the hypothesis check merely
because \(\phi_0\) vanishes there.  Its cancellation must instead be proved in
a weighted continuation lemma, as isolated in (5.1)--(5.6).

## 7. Finite diagnostics, explicitly non-formal

Fourier matrices for the periodic \(q\)-operator give a real positive branch.
The following values use cutoffs for which the displayed digits were stable
between the two tested truncations; they are diagnostics, not a tail
enclosure.

| \(\gamma\) | \(7/4-\gamma^2\) | finite \(\eta=\sigma/\gamma\) | \(\eta/[(7/4-\gamma^2)/4]\) |
|---:|---:|---:|---:|
| 1.300 | 0.060000 | 0.014893190115 | 0.992879 |
| 1.320 | 0.007600 | 0.001899046981 | 0.999498 |
| 1.321 | 0.004959 | 0.001239453 | 0.999761 |
| 1.322 | 0.002316 | 0.000578987304 | 0.999978 |

At \(\gamma=1/2\), the converged finite candidate is

\[
 \sigma_{\rm fin}=0.170407976920\ldots>0.
 \tag{7.1}
\]

This is well inside the open right half-plane and is a good target for a
Riesz-projection/Fredholm tail enclosure.  Ordinary Galerkin rightmost-real
parts at \(\gamma=\gamma_0\) are polluted by the discretized essential
spectrum and must not be used to identify (0.1).

## 8. Exact next gate for C4

There are two honest routes.

1. **Analytic route.**  Prove the missing periodic singular-continuation
   lemma (5.1), preferably as a PT-symmetric Evans-function statement.  The
   proof must control the order-three layer on scale \(\eta^{1/3}\), show no
   loss of the neutral Riesz count into the essential spectrum, and justify
   (5.6).  Equations (5.4)--(5.8) then fix the branch direction and slope.

2. **Infinite-dimensional enclosure.**  At a fixed row such as
   \(\gamma=1/2\), split the bounded operator into multiplication plus a
   compact smoothing term, enclose a Riesz contour for the finite-rank
   approximation, and prove that the Fourier tail cannot change its rank.
   This closes the existential C4 without claiming the full interval
   \((0,\sqrt7/2)\).

The second route is shorter for C4.  The first route is mathematically more
valuable because it explains the collision threshold and could eventually
prove a whole one-sided interval.

## 9. Primary-source boundary

- Z. Lin, *Instability of Some Ideal Plane Flows*, SIAM J. Math. Anal. 35
  (2003), 318--356, DOI
  [10.1137/S0036141002406266](https://doi.org/10.1137/S0036141002406266).
  Checked use: definitions of class \(K/K_+\), odd-flow theorem, neutral
  limiting modes, and the regular Tollmien bifurcation hypotheses.
- J. Qi, S. Chen, and B. Xie, *Instability of plane shear flows*, Nonlinear
  Analysis 109 (2014), 23--32, DOI
  [10.1016/j.na.2014.06.010](https://doi.org/10.1016/j.na.2014.06.010).
  Checked use: the corrected odd-negative-index interval and the
  \(K\in L^1\) extension.  The present inverse-square quotient lies outside
  that smooth theorem.
- E. Bian and E. Grenier, *Singularities of Rayleigh equation*,
  [arXiv:2408.00977](https://arxiv.org/abs/2408.00977).
  Checked use: local structure at critical points of arbitrary order and the
  \(|c|^{2-1/n}\) localization scale.  It is not used as a global periodic
  instability theorem.

## 10. Final claim boundary

This note proves the exact embedded neutral eigenvalue and the complete
negative spectrum of its singular Sturm--Liouville operator.  It also proves
the direction and coefficient of any pure-growth branch satisfying the
explicit convergence premise (5.1).  It does **not** convert finite Fourier
convergence into point spectrum, does **not** establish instability for every
\(0<\gamma<\sqrt7/2\), and has no nonlinear or Clay implication.
