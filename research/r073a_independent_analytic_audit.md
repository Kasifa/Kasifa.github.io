# R0.73A independent analytic audit: physical long-wave transient theorem

**Date:** 2026-08-29

**Role:** independent re-derivation of
`research/r073a_transient_proof.md`, followed by a compatibility audit against
`research/r073a_projection_derivation_agent.md`.

**Decision:** **ANALYTIC PASS WITH REQUIRED PUBLICATION-SCOPE EDITS.**  No
equation, sign, energy constant, Gronwall factor, or norm identity in the
physical theorem failed.  Two narrative statements about the singular limit
and “rank-one closure” must be narrowed before publication, and the source has
one harmless TeX typo.  This audit is not a deterministic certificate or a
release authorization.

No literature assertion is used in this audit.

---

## 0. Decision ledger

| Item audited | Decision | Independent conclusion |
|---|---|---|
| inherited physical row and parameter scope | **PASS** | valid only for \(\beta=\xi=0\), \(\mu=\gamma^2\in(0,1]\), \(c=\gamma\Lambda\in\mathbb R\) |
| \(q\leftrightarrow(h,r)\) transformation | **PASS** | exact bijection for each fixed \(\mu>0\) |
| periodic mean cancellation and signs | **PASS** | (2.3) follows with the displayed positive \(\mu\Pi_0(W\mathcal L_\mu^{-1}r)\) remainder |
| regular homogeneous \((h,r)\) system | **PASS** | no \(\mu^{-1}\) coefficient remains in its homogeneous generator |
| dissipative and coupling energy bounds | **PASS** | all three constants \(b_\mu,p_\mu,k_\mu\) have the stated bounds |
| profile majorant \(C_W\) and \(J(s,d)\) | **PASS** | \(C_W=\frac74e^{-d}+2e^{-4d}\), \(J\le\frac94e^{-s}\) |
| Gronwall and square root | **PASS** | there is no missing factor of two |
| forced Duhamel estimate | **PASS WITH HYPOTHESIS** | require \(\mathfrak F_\mu\in L^1_{\rm loc}(X_\mu)\); the \(\mu^{-1}\) mean payment is exact |
| hidden-mean derivative | **PASS WITH SCOPE** | positive-gap non-invariance is exact; a nonzero \(\mu\downarrow0\) derivative additionally requires \(c_\mu\to c_0\ne0\) |
| raw, hybrid, and OS kinetic norms | **PASS** | identities are exact; none gives a uniform two-sided replacement for \(X_\mu\) |
| compatibility with the moving-projection note | **PASS WITH SCOPE** | the two results concern different phase spaces and are complementary |
| categorical phrase “rank-one cannot close” | **FAIL AS WRITTEN** | replace by the precise non-invariance / insufficient-state statement in Sec. 9 below |
| source TeX at transient proof (1.3) | **FAIL, TYPESETTING ONLY** | `0,qquad` must be `0,\qquad`; it does not affect the mathematics |

---

## 1. Conventions and the fixed positive-gap phase space

Use the normalized inner product

\[
 \langle f,g\rangle_0
 =\frac1{2\pi}\int_0^{2\pi}\overline f g\,dx,
 \qquad \|1\|_2=1,
 \tag{1.1}
\]

and let \(\Pi_0 f=\widehat f(0)\), regarded as the corresponding constant
function when it is subtracted from \(f\).  Put \(Q_0=I-\Pi_0\).  For every
fixed \(\mu>0\),

\[
 T_\mu q
 :=(h,r)
 =\left(\mu^{-1}\Pi_0q,Q_0q\right),
 \qquad
 T_\mu^{-1}(h,r)=\mu h+r
 \tag{1.2}
\]

is an exact bijection between \(L^2(\mathbb T)\) and
\(\mathbb C\oplus Q_0L^2\).  The map is singular as \(\mu\downarrow0\),
which is a feature of the theorem rather than an omitted estimate.

The audited equation is

\[
 q_d=-\mathcal L_\mu q
 -ic\left(Wq+W_{xx}\mathcal L_\mu^{-1}q\right),
 \qquad
 \mathcal L_\mu=-\partial_x^2+\mu.
 \tag{1.3}
\]

Nothing below applies directly to \(\beta\ne0\), \(\xi\ne0\),
\(\mu=0\), the Squire row, or a Bloch direct sum.

---

## 2. Mean cancellation and transformed system

**Decision: PASS.**

Let \(r=Q_0r\) and \(s_r=\mathcal L_\mu^{-1}r\).  Then
\(\Pi_0s_r=0\) and

\[
 r=-s_{r,xx}+\mu s_r.
 \tag{2.1}
\]

Two periodic integrations by parts give

\[
 \begin{aligned}
 \Pi_0(Wr)
 &=-\Pi_0(Ws_{r,xx})+\mu\Pi_0(Ws_r)\\
 &=-\Pi_0(W_{xx}s_r)+\mu\Pi_0(Ws_r).
 \end{aligned}
 \tag{2.2}
\]

The sign in front of \(W_{xx}s_r\) is negative.  Hence

\[
 \Pi_0\left(Wr+W_{xx}\mathcal L_\mu^{-1}r\right)
 =\mu\Pi_0\left(W\mathcal L_\mu^{-1}r\right).
 \tag{2.3}
\]

For the constant component,

\[
 \mathcal L_\mu^{-1}(\mu h)=h,
 \qquad
 B_\mu(\mu h)=h(W_{xx}+\mu W),
 \tag{2.4}
\]

whose mean is zero because both \(W\) and \(W_{xx}\) are mean-zero.
Taking the mean of (1.3) first gives

\[
 \mu h_d=-\mu^2h
 -ic\,\mu\Pi_0(W\mathcal L_\mu^{-1}r).
 \tag{2.5}
\]

Dividing by \(\mu>0\), and separately applying \(Q_0\), yields

\[
 \boxed{
 \begin{aligned}
 h_d&=-\mu h-ic\,\Pi_0(W\mathcal L_\mu^{-1}r),\\
 r_d&=-\mathcal L_\mu r
 -icQ_0\left(Wr+W_{xx}\mathcal L_\mu^{-1}r\right)\\
 &\qquad-ic\,h(W_{xx}+\mu W).
 \end{aligned}}
 \tag{2.6}
\]

Thus the homogeneous generator on
\(\mathbb C\oplus Q_0L^2\) has no negative power of \(\mu\).  This does
not say that the coordinate map \(T_\mu\), a transformed forcing, or a
comparison with raw \(L^2_q\) is nonsingular.

For fixed \(\mu>0\), all non-heat terms in (2.6) are bounded operators and
depend continuously on \(d\).  A standard bounded-perturbation construction
therefore produces the claimed evolution family.  In a formal proof, the
energy calculation can first be made on the heat-generator domain and then
passed to mild solutions by density.

---

## 3. Energy ledger

**Decision: PASS.**

Write

\[
 E(d)=|h(d)|^2+\|r(d)\|_2^2.
 \tag{3.1}
\]

On \(Q_0L^2\), the Fourier eigenvalues of \(\mathcal L_\mu\) are
\(k^2+\mu\), \(k\ne0\), so

\[
 \|\mathcal L_\mu^{-1}r\|_2
 \le\frac1{1+\mu}\|r\|_2,
 \qquad
 \langle r,\mathcal L_\mu r\rangle_0
 \ge(1+\mu)\|r\|_2^2.
 \tag{3.2}
\]

Define, as in the proof draft,

\[
 \begin{aligned}
 b_\mu&=\|W\|_\infty
 +\frac{\|W_{xx}\|_\infty}{1+\mu},\\
 p_\mu&=\frac{\|W\|_2}{1+\mu},\\
 k_\mu&=\|W_{xx}+\mu W\|_2.
 \end{aligned}
 \tag{3.3}
\]

The three required estimates are

\[
 \left|\left\langle
 r,Q_0(Wr+W_{xx}\mathcal L_\mu^{-1}r)
 \right\rangle_0\right|
 \le b_\mu\|r\|_2^2,
 \tag{3.4}
\]

\[
 \left|\Pi_0(W\mathcal L_\mu^{-1}r)\right|
 \le p_\mu\|r\|_2,
 \qquad
 \|h(W_{xx}+\mu W)\|_2
 \le k_\mu|h|.
 \tag{3.5}
\]

The placement of \(Q_0\) causes no cost because it is an orthogonal
projection and \(r\in Q_0L^2\).  Taking
\(\operatorname{Re}(\overline h h_d+\langle r,r_d\rangle_0)\) in (2.6)
gives

\[
 \begin{aligned}
 \frac12E'
 &\le-\mu|h|^2-(1+\mu)\|r\|_2^2
 +|c|b_\mu\|r\|_2^2\\
 &\qquad+|c|(p_\mu+k_\mu)|h|\|r\|_2\\
 &\le-\mu E
 +|c|\left[b_\mu+\frac12(p_\mu+k_\mu)\right]E.
 \end{aligned}
 \tag{3.6}
\]

The proof deliberately discards the additional \(-\|r\|_2^2\).  It also
bounds the skew multiplication contribution from real \(W\) instead of
using its exact zero real part.  These choices make the estimate
conservative, not invalid.

---

## 4. Constant audit and Gronwall square root

**Decision: PASS.**

For \(0<\mu\le1\), normalized measure gives
\(\|f\|_2\le\|f\|_\infty\), and therefore

\[
 \begin{aligned}
 b_\mu+\frac12(p_\mu+k_\mu)
 &\le \|W\|_\infty+\|W_{xx}\|_\infty
 +\frac12\|W\|_\infty\\
 &\quad+\frac12(\|W_{xx}\|_\infty+\|W\|_\infty)\\
 &=2\|W\|_\infty+\frac32\|W_{xx}\|_\infty.
 \end{aligned}
 \tag{4.1}
\]

With \(a=e^{-d}\), \(b=e^{-4d}\),

\[
 \|W\|_\infty\le\frac a2+\frac b4,
 \qquad
 \|W_{xx}\|_\infty\le\frac a2+b,
 \tag{4.2}
\]

so the right side of (4.1) is

\[
 C_W(d)=\frac74e^{-d}+2e^{-4d}.
 \tag{4.3}
\]

Equation (3.6) is

\[
 E'\le2[-\mu+|c|C_W(d)]E.
 \tag{4.4}
\]

Consequently

\[
 E(d)\le
 e^{-2\mu(d-s)+2|c|J(s,d)}E(s),
 \tag{4.5}
\]

and taking the square root produces exactly one copy of each exponent:

\[
 \|(h(d),r(d))\|_{X_\mu}
 \le e^{-\mu(d-s)+|c|J(s,d)}
 \|(h(s),r(s))\|_{X_\mu}.
 \tag{4.6}
\]

There is no factor-of-two error.  Direct integration gives

\[
 J(s,d)=\frac74(e^{-s}-e^{-d})
 +\frac12(e^{-4s}-e^{-4d})
 \le\frac94e^{-s}\le\frac94.
 \tag{4.7}
\]

Thus \(|c|\le4\) implies the stated \(e^9e^{-\mu(d-s)}\) bound.  The
constant \(e^9\) is a sufficient, deliberately nonsharp transient
prefactor; the proof makes no optimality claim.

---

## 5. Forced Duhamel formula

**Decision: PASS WITH AN EXPLICIT REGULARITY HYPOTHESIS.**

For

\[
 q_d=A_\mu(d)q+F_q,
 \tag{5.1}
\]

the transformed forcing is exactly

\[
 T_\mu F_q
 =\mathfrak F_\mu
 =\left(\mu^{-1}\Pi_0F_q,Q_0F_q\right).
 \tag{5.2}
\]

Assuming \(\mathfrak F_\mu\in
L^1_{\rm loc}([s,d];\mathbb C\oplus Q_0L^2)\), variation of constants and
(4.6) give

\[
 \begin{aligned}
 \|(h(d),r(d))\|_{X_\mu}
 &\le e^{-\mu(d-s)+|c|J(s,d)}
 \|(h(s),r(s))\|_{X_\mu}\\
 &\quad+\int_s^d
 e^{-\mu(d-\tau)+|c|J(\tau,d)}
 \|\mathfrak F_\mu(\tau)\|_{X_\mu}\,d\tau.
 \end{aligned}
 \tag{5.3}
\]

The mean factor \(\mu^{-1}\) cannot be removed while retaining this
coordinate norm for arbitrary forcing.  A spatially constant forcing
\(F_q=f(d)\) already gives \(h_d\supset f(d)/\mu\), so the payment is
sharp at the coordinate-map level.

For publication, define \(B_\mu(d)=M_W+M_{W_{xx}}\mathcal L_\mu^{-1}\)
again in the forced section or refer explicitly to its earlier definition.

---

## 6. Hidden-mean derivative

**Decision: PASS WITH REQUIRED PARAMETER-PATH AND TOPOLOGY QUALIFIERS.**

Let

\[
 \phi=W_{xx}=\frac a2\sin x-b\sin2x,
 \qquad a=e^{-s},\quad b=e^{-4s}.
 \tag{6.1}
\]

For \(h(s)=0\), \(r(s)=\phi(s)\), allow the physically linked coupling
\(c=c_\mu=\gamma\Lambda_\mu\) to depend on \(\mu=\gamma^2\).  Then

\[
 \mathcal L_\mu^{-1}\phi
 =\frac{a}{2(1+\mu)}\sin x
 -\frac{b}{4+\mu}\sin2x.
 \tag{6.2}
\]

Since \(\Pi_0(\sin^2kx)=1/2\) and distinct sine modes are orthogonal,

\[
 \Pi_0(W\mathcal L_\mu^{-1}\phi)
 =-\frac{a^2}{8(1+\mu)}
 -\frac{b^2}{8(4+\mu)}.
 \tag{6.3}
\]

The sign in the first equation of (2.6) therefore gives

\[
 \boxed{
 h_d(s)=ic_\mu\left[
 \frac{e^{-2s}}{8(1+\mu)}
 +\frac{e^{-8s}}{8(4+\mu)}
 \right].}
 \tag{6.4}
\]

The bracket has a nonzero finite limit.  Therefore, along a specified
parameter sequence for which \(c_\mu\to c_0\),

\[
 h_d(s)\longrightarrow
 ic_0\left(\frac18e^{-2s}+\frac1{32}e^{-8s}\right)
 =ic_0\,\Pi_0(W(s)^2).
 \tag{6.5}
\]

For every fixed positive gap with \(c_\mu\ne0\), the lifted line

\[
 \{(h,r):h=0,\ r=A\phi(d)\}
 \tag{6.6}
\]

is not invariant under the physical dynamics.  A state variable recording
only the coefficient of \(\phi\) cannot reconstruct the hidden mean velocity.

There is an additional parameter-path boundary.  A **nonzero limiting**
derivative in (6.5) requires \(c_0\ne0\).  Since
\(c_\mu=\gamma\Lambda_\mu\), holding \(c_\mu\to c_0\ne0\) forces
\(|\Lambda_\mu|\sim |c_0|/|\gamma|\).  If instead the background amplitude
\(\Lambda\) is held fixed, then \(c_\mu=\gamma\Lambda\to0\), and (6.4)
gives \(h_d(s)\to0\).  The instantaneous calculation does not disprove a
fixed-\(\Lambda\) singular limit.

Even on a path with \(c_0\ne0\), what (6.4) does **not** prove by itself is
failure of convergence in every
topology applied only to raw \(q=\mu h+r\): a bounded nonzero \(h\) is
invisible in the raw mean \(\mu h\) as \(\mu\downarrow0\).  The safe result
is a mismatch in the lifted \(X_\mu\)-type phase space, with the initial
condition \(h(s)=0\).  Any stronger raw-\(q\) singular-limit statement would
need a separately stated topology and an evolution-level convergence or
counterexample argument.

---

## 7. The three norm identities

**Decision: PASS.**

Orthogonality of constants and mean-zero functions gives

\[
 \|q\|_2^2=\mu^2|h|^2+\|r\|_2^2.
 \tag{7.1}
\]

For \(0<\mu\le1\), the exact comparison is

\[
 \mu\|(h,r)\|_{X_\mu}
 \le\|q\|_2
 \le\|(h,r)\|_{X_\mu}.
 \tag{7.2}
\]

The inverse loss \(\mu^{-1}\) is sharp on the constant mode.

For the OS contribution to physical kinetic energy,

\[
 Q_{\rm kin}^2
 =\mu^{-1}\|\mathcal L_\mu^{-1/2}q\|_2^2
 =|h|^2+
 \sum_{k\ne0}\frac{|\widehat r(k)|^2}{\mu(k^2+\mu)}.
 \tag{7.3}
\]

This confirms the draft's formula.  It also makes both failures of uniform
equivalence explicit:

1. the \(k=1\) weight is \(1/[\mu(1+\mu)]\), which diverges as
   \(\mu\downarrow0\), so \(Q_{\rm kin}\) is not uniformly bounded by
   \(X_\mu\);
2. the weight tends to zero as \(|k|\to\infty\), so on the full
   infinite-dimensional space no bound
   \(\|r\|_2\le C Q_{\rm kin}\) exists even for a fixed \(\mu\).

The transient estimate is therefore a theorem in a stronger hybrid
mean-velocity/mean-zero-vorticity graph norm.  It is not a propagator theorem
for all finite-kinetic-energy OS data, and (7.3) is only the OS contribution,
not the complete OS--Squire kinetic norm.

---

## 8. Compatibility with the moving-projection derivation

**Decision: PASS WITH EXPLICIT SEPARATION.**

The two notes can be presented together, but only if the following ledger is
kept visible.

| Feature | Moving-projection note | Physical transient theorem |
|---|---|---|
| phase space | \(H_0=L^2_0\) at exactly \(\beta=\mu=0\) for the tangent theorem | full periodic \(L^2\), lifted to \(\mathbb C\oplus Q_0L^2\), with \(\mu>0\) |
| exact object | \(\phi=W_{xx}\) solves \(\phi_d=\mathscr A_0\phi\) | \((h,r)=(0,\phi)\) generates nonzero \(h_d\) when \(c_\mu\ne0\) |
| mechanism | time-dependent rank-one quotient algebra | exact mean cancellation after \(h=\Pi_0q/\mu\) renormalization |
| low-gap cost | a normalized dual has a \(g^{-1}\) adjoint constant-mode obstruction | the norm explicitly assigns the constant component the \(\mu^{-1}\) coordinate weight |
| conclusion | exact abstract quotient closure; no uniform unweighted rank-one block through \(g=0\) | uniform-in-\(\mu\) viscous-rate bound in the singular hybrid norm \(X_\mu\) |

At \(\beta=0\), the projection note's gap is \(g=\mu\).  Its
\(g^{-1}\) obstruction is therefore not contradicted by (4.6): the physical
proof does not produce an unweighted rank-one splitting.  It changes
coordinates by

\[
 q\mapsto(\mu^{-1}\Pi_0q,Q_0q),
 \tag{8.1}
\]

and pays exactly the singular constant-mode weight detected by the dual
calculation.  The cancellation then makes the generator regular in that
singular norm.

Likewise, the projection note proves that a time-dependent rank-one
**quotient/complement system** is algebraically closed.  The physical note
proves that the one-dimensional lifted line with \(h=0\) is not
**invariant**.  These statements are compatible.  “Closed quotient” and
“invariant one-dimensional physical dynamics” must not be used as synonyms.

The non-invariance of the fixed
\(\operatorname{span}\{\sin x,\sin2x\}\) carrier under the full OS operator
is also consistent with (2.6), whose variable \(r\) retains all mean-zero
Fourier modes.

---

## 9. Required wording corrections before publication

### 9.1 Singular-limit sentence

The heading “the abstract tangent is not the physical long-wave limit” is
too broad unless the parameter path, topology, and lifted state are stated
in the heading or first sentence.  The audited calculation supports:

> For every \(\mu>0\) with \(c_\mu\ne0\), the lifted physical trajectory
> initialized by \(h(s)=0\), \(r(s)=W_{xx}(s)\) immediately generates a
> hidden mean.  Along collision sequences with \(c_\mu\to c_0\ne0\), this
> derivative has the nonzero limit (6.5).

It does not, without another argument, decide every raw-\(L^2_q\) limit or
the fixed-\(\Lambda\) path, for which \(c_\mu\to0\).

### 9.2 Rank-one sentence

The sentence claiming categorically that a rank-one projection onto
\(W_{xx}\) “cannot close the physical long-wave dynamics” conflicts in
terminology with the exact quotient closure proved in the projection note.
Replace it by:

> The lifted line \(h=0\), \(r\in\operatorname{span}\{W_{xx}(d)\}\) is
> not invariant for \(c_\mu\ne0\).  Consequently a \(W_{xx}\)-amplitude alone
> is not a sufficient state variable for the physical positive-gap
> long-wave evolution.

The machine-readable claim
`rankOneAbstractTangentClosesPhysicalLongWaveLimit=FALSE` is safe only if
“closes” is defined to mean this invariant lifted one-dimensional state, not
the general moving quotient identity.

### 9.3 Status and small source corrections

1. In transient proof (1.3), change `0,qquad` to `0,\qquad`.
2. Add \(\mathfrak F_\mu\in L^1_{\rm loc}(X_\mu)\) to the forced corollary.
3. Qualify “uniform low-coupling estimate” as uniform for
   \(0<\mu\le1\), \(d\ge s\ge0\), \(|c|\le4\), **in \(X_\mu\)**.
4. Do not label the analytic claims formally `CLOSED` until the announced
   deterministic certificate and release binding pass.  This document
   supports `ANALYTIC_PASS`.

---

## 10. Reproducibility checks

An independent finite Fourier calculation, using only the displayed
coefficients of \(W\), tested multiple
\((d,\mu,c)\) values and random complex mean-zero states.  It returned

\[
 \begin{array}{ll}
 \text{maximum error in the mean cancellation} & 1.36\times10^{-16},\\
 \text{maximum error in the hidden-mean formula} & 5.55\times10^{-17},\\
 \text{minimum sampled margin in the energy majorant} & 8.24\times10^2>0.
 \end{array}
 \tag{10.1}
\]

These computations are supplemental checks, not substitutes for Secs. 2--7.

---

## 11. Publishable conclusion boundary

Subject to the wording corrections in Sec. 9 and the separate certificate
gate, the following is analytically publishable:

1. for the physical row \(\beta=\xi=0\),
   \(\mu=\gamma^2\in(0,1]\), the transformation
   \(h=\Pi_0q/\mu\), \(r=Q_0q\) yields the exact regular system (2.6);
2. its evolution family obeys the viscous-rate, finite-transient estimate
   (4.6), and \(|c|\le4\) gives the sufficient prefactor \(e^9\);
3. transformed forcing obeys (5.3) with the explicit \(\mu^{-1}\) mean
   payment;
4. for each positive gap with \(c_\mu\ne0\), the lifted tangent line with
   zero hidden mean is not invariant; its derivative has a nonzero
   \(\mu\downarrow0\) limit only along paths with
   \(c_\mu\to c_0\ne0\), as witnessed by (6.4)--(6.5);
5. the raw, hybrid, and OS kinetic norms obey (7.1)--(7.3), so the theorem
   cannot be exported to an unweighted or complete physical kinetic norm;
6. the physical theorem and the abstract moving-projection theorem are
   complementary and may be published side by side with their phase spaces
   explicitly separated.

The audit does **not** establish an \(A_2\)-rate estimate, optimality of
\(C_W\) or \(e^9\), failure or validity of the fixed-\(\Lambda\) raw-\(q\)
limit through \(\mu=0\), a complete physical kinetic propagator,
Squire/lift-up control, Bloch-uniform summation, a nonlinear estimate, or any
part of the Clay regularity theorem.
