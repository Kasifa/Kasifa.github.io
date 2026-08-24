# R0.70K independent mathematical audit

**Audit status:** PASS
**Date:** 2026-08-24
**Scope:** independent re-derivation of the normalized covariance equation,
the frozen-source variance law, and the periodic diffusion sign witness
**Boundary:** this is an internal independent agent audit, not external peer
review and not a formal proof-assistant verification

## 1. Objects and assumptions

The audit used a smooth Navier--Stokes solution, a fixed translation-invariant
filter commuting with spatial derivatives, a smooth cutoff \(\chi\), and

\[
 Q=\int\chi\,W\otimes W,
 \qquad E=\operatorname{tr}Q>0,
 \qquad B=\frac{\operatorname{dev}Q}{E}.
 \tag{I.1}
\]

It did not assume a time-varying filter scale, a sharp cutoff, or an
unjustified Leray weak-solution passage.

## 2. Independent covariance calculation

Writing the raw covariance flux as a sum of transport/cutoff, stretching,
diffusion, and commutator pieces,

\[
 \dot Q=\sum_X X,
 \tag{I.2}
\]

direct differentiation gives

\[
 \boxed{
 \dot B=\frac1E\sum_X
 \left[\operatorname{dev}X-(\operatorname{tr}X)B\right].}
 \tag{I.3}
\]

The denominator correction is required separately for every raw flux. The
report retains it.

For

\[
 \alpha=|B|_F^2
 =\frac{\operatorname{tr}(Q^2)}{E^2}-\frac13,
 \tag{I.4}
\]

the independent scalar check is

\[
 \boxed{
 \frac12\dot\alpha
 =\frac1E\sum_X
 \left[B:X-(\operatorname{tr}X)\alpha\right].}
 \tag{I.5}
\]

This agrees with differentiating the quotient in (I.4) directly.

## 3. Frozen-source variance law

For a constant symmetric trace-free source \(\Sigma\), the independently
computed flux is

\[
 X_\Sigma=\Sigma Q+Q\Sigma.
 \tag{I.6}
\]

With \(R=Q/E\) and \(q=\Sigma:B=\Sigma:R\), (I.3) yields

\[
 \dot R\big|_\Sigma
 =\Sigma R+R\Sigma-2qR,
 \tag{I.7}
\]

and

\[
 \boxed{
 \dot q\big|_\Sigma
 =2\operatorname{tr}\left[R(\Sigma-qI)^2\right]\ge0.}
 \tag{I.8}
\]

The factor two, trace subtraction, and equality condition all agree with the
canonical report and exact producer.

## 4. Periodic Navier--Stokes diffusion sign witness

The audit rechecked

\[
 u(t,z)=\left(
 \frac b2e^{-4\nu t}\sin2z,
 -ae^{-\nu t}\sin z,
 0\right).
 \tag{I.9}
\]

It satisfies

\[
 \nabla\cdot u=0,
 \qquad
 (u\cdot\nabla)u=0,
 \qquad
 (W\cdot\nabla)u=0,
 \tag{I.10}
\]

and each component solves the heat equation. For \(\chi=1\) and the identity
filter, only diffusion remains in the covariance equation. Orthogonality on
the torus gives

\[
 Q=\frac12\operatorname{diag}
 \left(a^2e^{-2\nu t},b^2e^{-8\nu t},0\right).
 \tag{I.11}
\]

With

\[
 p=\frac{a^2e^{-2\nu t}}
        {a^2e^{-2\nu t}+b^2e^{-8\nu t}},
 \tag{I.12}
\]

the audit obtains

\[
 p'=6\nu p(1-p),
 \qquad
 \frac d{dt}|B|_F^2
 =12\nu p(1-p)(2p-1).
 \tag{I.13}
\]

Consequently

\[
 p=\frac45\Longrightarrow
 \frac d{dt}|B|_F^2=\frac{144}{125}\nu,
 \qquad
 p=\frac15\Longrightarrow
 \frac d{dt}|B|_F^2=-\frac{144}{125}\nu.
 \tag{I.14}
\]

The raw diffusion matrix is negative semidefinite in both cases. The sign
change appears only after normalization and is therefore a clean exact
obstruction to universal normalized-anisotropy monotonicity.

## 5. Claim audit

The following claims are supported:

- the exact smooth filtered covariance and normalized-shape ledgers;
- the nonnegative frozen-source variance law;
- the sharp boundedness, but not smallness, of \(B\);
- the exact periodic Navier--Stokes diffusion sign pair;
- closure of a universal normalization-only monotonicity branch.

The following claims are deliberately absent:

- a term-by-term sign theorem for the cutoff or commutator contribution;
- a weak-solution endpoint theorem;
- control through times with \(E=0\) or a lower bound \(E\ge e_*>0\);
- a finite-energy \(\mathbb R^3\) cascade at one fixed positive terminal time;
- a singularity, global-regularity, or Millennium-problem result.

A separate three-mode commutator counterexample is unnecessary for the stated
route decision. The two-mode shear already disproves the universal
normalization/diffusion monotonicity in a stronger setting where transport,
stretching, and commutator contributions vanish.

## Final status: PASS

The report's algebra, factors, normalization corrections, and exact shear
witness are internally consistent. The PASS applies only to the bounded
R0.70K gate above. It is not external peer review and does not certify a
Navier--Stokes regularity theorem.
