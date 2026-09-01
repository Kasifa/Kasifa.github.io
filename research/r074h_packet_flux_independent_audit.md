# R0.74H — independent audit of the explicit-family collar flux

## Verdict

**INDEPENDENT ANALYTIC PASS AFTER ONE REQUIRED NOTATION FIX.**

The original Section 7 candidate was audited read-only at SHA-256

    8595b1b1d48d0f2024c6a5169982cb92cd7deb6685a9489ebcdbbf41206a1f67.

Its analytic signs and scales were correct, but equation (7.2) used a
periodic torus weight inside an \(\mathbb R^3\) integral.  The repaired
source introduced the nonperiodized lift-side weight

\[
 \vartheta_R^{\rm ann}=\sum_{k\ge1}\gamma_k\psi_k^R
\]

and passed a second read-only audit at SHA-256

    f43669dd7d06d3faacf9b111b939583096c253a262868accc575b4d256ab0613.

The subsequent declaration-only patch is separately covered by the scaling
and claim audit.

## 1. Exact flux reduction

On the R0.74F--G family,

\[
 u=(\mathfrak aF,B\theta,0),\qquad p=0,
 \qquad X_R=a_R=a_R'=0.
\]

Substitution into the Version-M flux gives

\[
 \frac1{2R}\int\eta
 (\mathfrak a^2F^2+B^2\theta^2)
 (\mathfrak aF\partial_1\vartheta_R^{\rm ann}
  +B\theta\partial_2\vartheta_R^{\rm ann}).
\]

All \(\partial_1\) terms integrate to zero because their coefficients are
independent of \(x_1\).  The pure-shear term integrates to zero in \(x_2\).
The remaining exact term is

\[
 \mathfrak F_R(\tau)
 =\frac{\mathfrak a^2B}{2R}
 \int_{s_R}^{\tau}\eta_R
 \int_{\mathbb R^3}\theta F^2
 \partial_2\vartheta_R^{\rm ann}.
\]

The sign, factor \(1/2\), and power \(R^{-1}\) are correct.  Periodic
unfolding justifies the \(\mathbb R^3\) form, and the super-Gaussian shell
weights give absolute convergence.

## 2. Terminal lobe to positive flux

For every \(\tau\) in the terminal interval

\[
 J_j=(t_{0,j}-R_j^3,t_{0,j})\subset I_{R_j},
\]

the R0.74F lobe and \(\Theta_R\ge\gamma_j\) on the selected annulus give,
at \(\mathfrak a_j=B_j\gamma_j^{-1/2}\),

\[
 \frac1R\int\Theta_R|u_j(\tau)|^2
 \ge cB_j^2L_jR_j^2.
\]

The quadratic-cutoff row satisfies

\[
 \mathfrak Q_{R_j}
 \le C(P_{R_j})^{2/3}
 \le CB_j^2R_j^2.
\]

The exact energy identity and nonnegative dissipation therefore imply, for
large \(j\),

\[
 \mathfrak C_{R_j}
 \ge cB_j^2L_jR_j^2,
\qquad
 (\mathfrak C_{R_j})^{3/2}
 \ge cB_j^3L_j^{3/2}R_j^3.
\]

This is a lower bound only.  It does not establish a reverse comparison or
an asymptotic equivalence.

## 3. Version-M/Version-F identity

Because the trajectory, velocity subtraction, and acceleration all vanish,

\[
 v_R=w_R=u,
\]

the two pressure gauges agree and the acceleration moment is zero.  Hence
the two fluxes and their positive cumulative parts coincide exactly.

## Required repair and recheck

The pre-repair notation used the periodic \(\Theta_R\) in an
\(\mathbb R^3\) integral, which would be ill-defined if read literally.
Replacing it with \(\vartheta_R^{\rm ann}\) repaired the only blocking
issue.  The terminal statement was also sharpened from a Lebesgue-time
sequence to every \(\tau\in J_j\), and the conclusion now explicitly says
that no reverse flux comparison is claimed.

## Boundary

This audit concerns one explicit smooth solution family.  It does not make
the collar flux an independently controllable regularity quantity, extend
the estimate to weak solutions, or prove epsilon regularity, continuation,
global regularity, novelty, or priority.  **NOT CLAY.**
