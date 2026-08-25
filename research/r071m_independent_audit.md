# R0.71M standalone Fourier audit

## Purpose

research/r071m_independent_audit.py checks the R0.71M algebra through a
separate finite Fourier implementation. It imports neither
research/r071m_exact_audit.py nor any R0.71L producer.

The checker is an identity diagnostic. It is not a DNS, a time-stepping
scheme, a finite-\(K\) approximation to a singular solution, or a continuous
sign certificate.

## Default command

    PYTHONDONTWRITEBYTECODE=1 tmp/r068b-venv/bin/python \
      research/r071m_independent_audit.py \
      --order 48 \
      --output /tmp/r071m-independent-result.json

The formal certificate repeats the same calculation at order 64.

## Construction

The checker declares five real Fourier mode pairs on \(\mathbb T^3\). Each
coefficient is projected onto its frequency-orthogonal plane before the
conjugate mode is added, so the resulting field is exactly divergence free
up to binary64 roundoff.

It then builds:

1. a deterministic compact annular radial multiplier with \(\kappa=4\);
2. \(W_j=T_j\omega\);
3. \(F_j=\mathbb P T_j(u\times\omega)\);
4. the direct commutator
   \[
   \mathcal R_j=T_j(u\times\omega)-u\times W_j;
   \]
5. a second implementation obtained by expanding the quadratic-increment
   formula into filtered derivatives and products;
6. a fixed positive nonconstant trigonometric cutoff \(\chi_Q\);
7. \(C_Q=\operatorname{curl}(\chi_QW_j)\), the rank-one projector \(P_Q\),
   the viscous mismatch \(H_j\), and the localized source \(M_Q\).

All products are evaluated in physical space and all derivatives in Fourier
space. The 48-point default is alias-safe for the declared finite mode set
and cutoff frequencies. The 64-point formal run provides a second resolution
check.

## Checked identities

### 1. Increment commutator

The direct cross-product definition is compared against

\[
 \frac12\nabla T_j|u|^2
 -u_a\nabla T_ju_a
 -\operatorname{div}T_j(u\otimes u)
 +(u\cdot\nabla)T_ju.
\]

This is the convolution expansion of

\[
 \int\left[
 \frac12|\delta_hu|^2\nabla\phi_j
 -(\nabla\phi_j\cdot\delta_hu)\delta_hu
 \right]dh.
\]

### 2. Resolved/commutator fusion

The checker verifies

\[
 \operatorname{curl}F_j
 =
 \operatorname{curl}(u\times W_j)
 +\operatorname{curl}\mathcal R_j.
\]

It records both the fraction of \(\mathcal R_j\)'s Fourier energy outside the
declared annular multiplier support and the fraction strictly above its upper
edge \(1.45\kappa\). A strictly positive high off-band fraction is required,
so the witness directly exhibits the missing \(O(\kappa)\) upper-frequency
support needed for the displayed Bernstein step.

### 3. Projective cutoff pairing

With

\[
 \alpha_Q=B_Q/d_Q,
\]

the checker compares

\[
 \langle P_QF_j,P_QM_Q\rangle
\]

against

\[
 \int\chi_Q
 \left(G_j-\alpha_Q\operatorname{curl}C_Q\right)
 \cdot\left(G_j+\nu H_j\right).
\]

### 4. Radial form

It reconstructs

\[
 C_{Q,t}=M_Q-\nu\kappa^2C_Q
\]

and checks

\[
 \langle P_QF_j,P_QM_Q\rangle
 =
 \int\chi_QG_j\cdot(G_j+\nu H_j)
 -\frac{B_Q}{d_Q}
  \left(\frac12d_{Q,t}+\nu\kappa^2d_Q\right).
\]

### 5. Four-row upper bound

The exact positive-branch tangent envelope is compared with the declared
Cauchy upper bound using

\[
 A=\operatorname{curl}(u\times W_j),\quad
 D=\operatorname{curl}\mathcal R_j,\quad
 K=(B_Q/d_Q)\operatorname{curl}C_Q,\quad
 V=\nu H_j.
\]

## Acceptance thresholds

| Check | Threshold |
|---|---:|
| divergence residual | \(<10^{-12}\) |
| increment identity relative residual | \(<2\times10^{-11}\) |
| resolved/commutator fusion relative residual | \(<2\times10^{-11}\) |
| projective pairing relative residual | \(<3\times10^{-11}\) |
| radial pairing relative residual | \(<3\times10^{-11}\) |
| commutator off-band energy fraction | \(>10^{-4}\) |
| commutator high off-band energy fraction | \(>10^{-4}\) |
| exact tangent envelope versus upper bound | envelope \(\le\) bound |

The formal result JSON records the actual residuals and the full claim
boundary.

## Independence and limitations

The checker shares mathematical definitions with the report, as any
verification must, but it does not call or parse the exact producer. It uses
a Fourier-field path instead of the exact producer's symbolic integrand and
finite self-adjoint operator model.

The finite computation proves the displayed identities only for its declared
witness up to binary64 tolerance. Universal statements in the report are
proved analytically. The checker does not establish a sign over a time
interval, an estimate for arbitrary Leray solutions, an infinite
frame--cell passage, or a regularity theorem.
