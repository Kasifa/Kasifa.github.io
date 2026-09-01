# R0.74H — independent audit of the two-frame weighted energy closure

## Verdict

**INDEPENDENT ANALYTIC PASS.**  No blocking error was found in the
finite-shell limit, either weighted energy identity, the quadratic-cutoff
row, the acceleration payment, or the two-regime closure.

The first full candidate audited read-only had SHA-256

    8595b1b1d48d0f2024c6a5169982cb92cd7deb6685a9489ebcdbbf41206a1f67.

The audit required six correctable changes.  They were applied and the
repaired analytic source passed a second read-only audit at SHA-256

    f43669dd7d06d3faacf9b111b939583096c253a262868accc575b4d256ab0613.

The later claim-boundary patch did not alter Sections 2--6.  In the current
analytic source

    c5cada2e8698c12154b6ee9c2c49ce1c7e5f23fc99c50558937a31209bb8c968

the exact byte slice from `## 2.` up to, but not including, `## 7.` has
SHA-256

    b355b7c59c27e0d94e01c59f1d0cdae55052f5ec9ae57cb6f2859370bc7317df.

## 1. Finite-shell limit

For \(0\le k\le2\), lattice-point counting gives

\[
 \|D^k\Psi_j^R\|_\infty
 \le CR^{-k}(1+2^{3j}R^3).
\]

The super-Gaussian \(\gamma_j\) makes this summable.  Hence
\(\Theta_{R,N}\to\Theta_R\) in \(C^2(\mathbb T^3)\), and every term in the
smooth finite-shell identities has a licensed limit.  No infinite test is
inserted before this limit is established.

## 2. Version M identity

For

\[
 \partial_tv_R-\Delta v_R+(v_R-a_R)\cdot\nabla v_R+\nabla\pi_R=0,
\]

the diffusion, transport, and pressure integrations by parts give exactly

\[
 \frac1{2R}\int\Theta|v_R(\tau)|^2
 +\frac1R\int\eta\Theta|\nabla v_R|^2
 =\text{quadratic cutoff}+\mathfrak F_R^M(\tau).
\]

The sign of the incoming flux, its \(1/R\) normalization, and the kinetic
factor \(1/2\) are correct.  The spatially constant \(a_R\) remains inside
the residual transport; it creates no body force.

The scalar pressure gauge is harmless:

\[
 \int c_{2R}v_R\cdot\nabla\Theta
 =-c_{2R}\int\Theta\nabla\cdot v_R=0.
\]

## 3. Version F identity and acceleration

For

\[
 \partial_tw_R-\Delta w_R+w_R\cdot\nabla w_R+\nabla\pi_R=-a_R',
\]

the body-force contribution has the sign

\[
 -\frac1R\int\eta a_R'\cdot\int\Theta w_R.
\]

Expanding the shell sum gives

\[
 \sup_\tau|\mathfrak B_R^F(\tau)|
 \le\frac12\mathcal J_{\rm acc,sh}^{F,R}
 \le\frac12\mathcal J_{\rm acc}^{F,R}.
\]

The factor \(1/2\) is exactly the reciprocal of the \(2/R\) normalization
in the frozen shell acceleration moment.  Since

\[
 P_R^F\ge(\mathcal J_{\rm acc}^{F,R})^{3/2},
\]

monotonicity yields
\(\mathcal J_{\rm acc}^{F,R}\le(P_R^F)^{2/3}\).  No second enlargement of
the acceleration row occurs.

## 4. Pressure transfer

Taking divergence in both local frames gives

\[
 -\Delta\pi_R
 =\partial_i\partial_j(v_{R,i}v_{R,j})
 =\partial_i\partial_j(w_{R,i}w_{R,j}).
\]

The constant drift and constant body force vanish under the relevant
divergences.  Therefore the frozen local Riesz/harmonic pressure ledger
applies in both frames.

## 5. Quadratic-cutoff row

Weighted Hölder and the parabolic shell volume give

\[
 S_2\le CR^{5/3}S_3^{2/3},
\qquad
 R^{-3}S_2\le C(R^{-2}S_3)^{2/3}.
\]

The doubled-radius support identity and the core/exterior split pay
\(R^{-2}S_3\) by \(P_{0,R}^\alpha\).  Thus every \(R\) power in

\[
 \mathfrak Q_R^\alpha
 \le C(P_{0,R}^\alpha)^{2/3}
 \le C(P_R^\alpha)^{2/3}
\]

is correct.

## 6. Control of both parts of the endpoint

At each \(\tau\in I_R\), the weighted identity controls the terminal
exterior energy after dropping nonnegative dissipation.  Letting
\(\tau\uparrow t_0\) separately controls the full \(I_R\) dissipation after
dropping nonnegative terminal energy.  Taking the essential supremum and
adding the two inequalities therefore controls

\[
 X_R^\alpha
 =\mathcal U_{\rm ext}^{\infty,\alpha,R}
 +\mathcal D_{\rm ext}^{\alpha,R}.
\]

The positive part of the signed flux is the only remaining identity-level
row that can enlarge the left side.  The direct absolute flux bound is
linear in the frozen pre-acceleration ledger.  Consequently Theorem 5.1,
Theorem 6.2, and Corollary 6.3 follow with the stated powers.

## Correction ledger

The audit required and then verified these changes:

1. replace a set-distance infimum by the correct cutoff-support inclusion;
2. treat the pressure gauge as a scalar;
3. display the \(C^2\) lattice-counting majorant;
4. state the common pressure Poisson identity;
5. state \(\eta_R(s_R)=0\) and \(\eta_R(\tau)=1\); and
6. display separate endpoint-energy and full-dissipation bounds.

The repaired source passed all six checks.

## Boundary

This audit proves no weak-solution extension, epsilon regularity,
continuation, singularity exclusion, global regularity, novelty, or priority.
It audits the displayed smooth-solution size theorem only.  **NOT CLAY.**
