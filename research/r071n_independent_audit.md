# R0.71N standalone finite Fourier audit

## Purpose

The file research/r071n_independent_audit.py checks the full fixed-cell scalar
with a Fourier implementation that imports neither the exact symbolic
producer nor an earlier release checker. It constructs two explicit smooth,
divergence-free periodic velocity fields and evaluates their Navier--Stokes
time jets at \(t=0\).

The calculation is not DNS and performs no time stepping. Its sign output is
a deterministic high-margin binary64 diagnostic, not an interval-certified
sign theorem.

## Command

    PYTHONDONTWRITEBYTECODE=1 tmp/r068b-venv/bin/python \
      research/r071n_independent_audit.py \
      --output /tmp/r071n-independent-result.json

The checker runs orders \(48^3\), \(64^3\), and \(80^3\).

## Construction

For each witness the script declares five positive Fourier frequencies and
explicit complex polarization vectors. Each vector is projected onto the
plane perpendicular to its frequency, and its conjugate is placed at the
negative frequency. No random-number generator is called.

The fixed annular multiplier has \(\kappa=4\), and the viscosity is
\(\nu=0.2\). A positive nonconstant trigonometric cutoff is shared by both
witnesses.

The checker evaluates

\[
 L=\mathbb P(u\times\omega),\qquad
 u_t=L+\nu\Delta u,
\]

\[
 \omega_t=\operatorname{curl}L+\nu\Delta\omega,
 \qquad
 L_t=\mathbb P(u_t\times\omega+u\times\omega_t).
\]

It also differentiates once more where the local second-jet representation
requires \(e_{tt}\) and \((D_Q^\chi)_t\). Every time derivative is therefore
the instantaneous derivative forced by the NSE, not a finite difference.

## Alias safety

The quadratic NSE jet is represented strictly below Nyquist. Cubic
frequencies that wrap on the \(48^3\) grid are enumerated, and the checker
requires that none can alias into the selected annulus. It separately checks
that every cutoff-weighted zero-mode quadrature is below the grid order.

The final scalar values at orders 48 and 64 are compared with order 80. The
largest relative difference over all recorded state variables is
\(1.26\times10^{-14}\), below the declared \(5\times10^{-11}\) threshold.

## Independent identities

For each witness and resolution the script checks:

1. \(B_t=\langle F_t,C\rangle+\langle F,C_t\rangle\);
2. the \(N,M\) product-rule reconstruction of \(B_t\);
3. the radial/projective reconstruction;
4. the direct quotient formula for
   \(\mathcal J=z_t+\nu\kappa^2z\);
5. the R0.71L normalized field--tangent formula;
6. the R0.71M radial-\(N\) formula;
7. the R0.71N square--residual formula;
8. the local filtered-enstrophy balance
   \(B=e_t+\nu D_Q^\chi\);
9. the local second-jet formula after the apparent square cancels.

The five independently assembled values of \(\mathcal J\) agree with maximum
relative residual \(4.82\times10^{-16}\). The largest local-enstrophy
balance residual is \(4.36\times10^{-14}\), and the largest recorded
square-cancellation residual is \(2.58\times10^{-15}\).

## Sign diagnostic

At order 64:

| witness | \(z_Q\) | \(\mathcal P_Q^\square\) | \(\mathfrak R_Q\) | \(\mathcal J_Q\) |
|---|---:|---:|---:|---:|
| positiveJ_seed49 | \(0.0037338305\) | \(5023.6425100\) | \(749.9219443\) | \(1.3523543\) |
| negativeJ_seed5 | \(0.0019598744\) | \(5167.6945795\) | \(-25941.2940133\) | \(-7.3713441\) |

Both normalized pairings are positive. The complete signed source has
opposite signs, and in the second witness the residual overwhelms the
positive square.

These fields are smooth trigonometric-polynomial initial data, so they start
local classical NSE trajectories. The sign table remains a diagnostic
because the current checker uses ordinary floating arithmetic rather than
exact convolution or outward-rounded intervals. No theorem in the report
depends on this table.

## Claim boundary

The checker proves no sign statement on a time interval, no control of
denominator-zero faces, no continuation criterion, no weak-solution limit,
no regularity or singularity result, no originality claim, and no conclusion
about the Millennium problem.
