# R0.71K independent mathematical audit

## 1. Audit question

The audit checks the narrow R0.71K claim:

> For one fixed aligned, scale-covariant matched partition, the R0.71J
> selected parent has zero work in every cell at the initial trace, develops a
> positive localized aggregate endpoint on the parabolic window, and therefore
> has \(K^{-2}\) positive joint creation.  The same bounded-overlap local
> heat/support payment is only \(O((\nu K^4)^{-1})\).

The checker does not import the exact SymPy producer or the repository's
Fourier helper.  It independently reconstructs curl, convolution, Leray
projection, parent restriction, the translated partition, and a complete
cutoff--curl denominator quadrature.

## 2. Explicit partition used by the checker

Let \(R=3\pi/2\) and

\[
 g(s)=
 \begin{cases}
 \exp\!\left[-(1-(s/R)^2)^{-1}\right],&|s|<R,\\
 0,&|s|\ge R.
 \end{cases}
\]

Define

\[
 h(s)=\frac{g(s)}{\sum_{n\in\mathbb Z}g(s-2\pi n)}.
\]

Then \(h\in C_c^\infty(\mathbb R)\), \(h\ge0\), and

\[
 \sum_{n\in\mathbb Z}h(s-2\pi n)=1.
\]

The three-dimensional atom is the tensor product
\(\eta(y)=h(y_1)h(y_2)h(y_3)\).  At the selected parent
\(\kappa=4K\), the torus partition uses translates of \(\eta(Kx)\).
It has at most \(2^3=8\) overlaps and support radius comparable to
\(K^{-1}=4\kappa^{-1}\).  The construction rule is fixed before the NSE
datum.

On 8193 deterministic points in one period, the independent checker found

\[
 \max\left|\sum_nh(s-2\pi n)-1\right|
 =2.22\times10^{-16},
\]

and the corresponding derivative-sum residual was also
\(2.22\times10^{-16}\).  These samples validate the implementation.  The
proof that the translates form a partition follows directly from the
definition and does not rely on the samples.

## 3. Independent Fourier reconstruction

The checker starts from the R0.71J velocity coefficients at normalized
frequency \(K=1\), applies the pure heat factor
\(e^{-|k|^2\theta}\), and rebuilds

\[
 \omega=\nabla\times u,
 \qquad
 F=A_\kappa\mathbb P(u\times\omega),
 \qquad
 W=A_\kappa\omega,
 \qquad
 C=\nabla\times W.
\]

It independently recovers at \(\theta=0\)

\[
 B=0,\qquad D=3942,\qquad Y=178,
\]

and at \(\theta_*=(\log2)/18\)

\[
 B=0.5400298694461556,
\]

\[
 D=693.8204950994357,
 \qquad
 Y=35.12843837102585,
\]

so that

\[
 \frac{B^2}{DY}=1.1965465392386885\times10^{-5}.
\]

The last number agrees with the closed R0.71J value to floating-point
precision, but it was obtained from a separate direct convolution path.

## 4. Complete one-cell denominator quadrature

For the selected parent, \(W=(W_1,W_2,0)\) and is independent of \(y_3\).
Writing \(\eta=h_1h_2h_3\), the local curl is

\[
 \nabla\times(\eta W)=
 \begin{pmatrix}
 -h_1h_2h_3'W_2\\
 h_1h_2h_3'W_1\\
 h_1h_2h_3C_3+h_1'h_2h_3W_2-h_1h_2'h_3W_1
 \end{pmatrix}.
\]

Thus the quadrature retains the interior term, both cutoff--curl terms, their
cross terms, and the \(y_3\)-collar components.  No collar is deleted.

A tensor 360-point Gauss--Legendre rule gives

| time | normalized one-cell \(d\) at \(K=1\) | \(D_{\rm loc}/D\) | work residual |
|---:|---:|---:|---:|
| \(0\) | 2831.4164745060 | 0.7182690194 | \(-1.20\times10^{-9}\) |
| \(\theta_*\) | 502.7892233752 | 0.7246675861 | \(-2.26\times10^{-10}\) |

The work residual is the quadrature value of the one-cell work minus the
normalized global work.  Translation invariance proves exact equality; the
small residual measures quadrature error.  At \(\theta_*\), the concrete
partition gives localized aggregate amplitude

\[
 1.6511660824611684\times10^{-5},
\]

which is positive and, for this template, larger than the global amplitude.
This numerical value is diagnostic only.  The theorem uses the analytic bound
\(D_{\rm loc}\le C_{\rm part}D\), not the quadrature value.

## 5. Equal-cell algebra

Every selected field has Fourier frequency in
\(K\mathbb Z\times K\mathbb Z\times\{0\}\).  Translation by
\(2\pi q/K\) leaves \(F\) and \(W\) unchanged and carries one partition atom
to another.  Therefore all \(B_Q\) and all \(d_Q\) are equal.  Since
\(\sum_Q\chi_Q=1\),

\[
 B_Q=\frac{B_\kappa}{K^3},
 \qquad
 d_Q=\frac{D_{\rm loc}}{K^3},
\]

and hence

\[
 \sum_Qq_Q
 =K^3\frac{(B_\kappa^+/K^3)^2}{D_{\rm loc}/K^3}
 =\frac{(B_\kappa^+)^2}{D_{\rm loc}}.
\]

At \(t=0\), this gives \(B_Q=q_Q=a_Q=0\) for every cell, not only after
summation.  The selected parent denominator is positive on the R0.71J fixed
window.  If one local denominator vanished, translation symmetry would make
all of them vanish, contradicting

\[
 \sum_Q\nabla\times(\chi_QW)=\nabla\times W\ne0.
\]

Thus there is no denominator face in the selected finite family.

## 6. Independent scale ledger

Each cell has volume \(K^{-3}\).  On the selected family,

| quantity | per cell | sum over \(K^3\) cells |
|---|---:|---:|
| \(B_Q\) | \(K^0\) | \(K^3\) |
| \(d_Q\) | \(K^1\) | \(K^4\) |
| \(q_Q\) | \(K^{-1}\) | \(K^2\) |
| \(a_Q=q_Q/Y\) | \(K^{-3}\) | \(K^0\) |
| \(z_Q\) | \(K^{-3/2}\) | — |
| \(\mathcal J_Q\) | \(\nu K^{1/2}\) | — |
| weighted, time-integrated positive creation | \(K^{-5}\) | \(K^{-2}\) |
| weighted, time-integrated support heat payment | \((\nu K^7)^{-1}\) | \((\nu K^4)^{-1}\) |

For \(K=8,16,32,64,128\), the independently evaluated lower-bound ratio has
successive factors

\[
 4, 4, 4, 4,
\]

which is the exact \(K^2\) law.

## 7. Collar audit

At matched radius, \(\nabla\chi=O(K)\) and
\(\Delta\chi=O(K^2)\).  Consequently

\[
 \nabla\chi\times W
\]

has the same pointwise size as \(\nabla\times W\), while

\[
 -\nu\nabla\times\!left(
 2\nabla\chi\cdot\nabla W+(\Delta\chi)W
 \right)
\]

has the same scale as the main part of \(M_Q=C_{Q,t}+\nu\kappa^2C_Q\).
After cell summation, physical-time integration, and the outer
\(\kappa^{-2}\) weight, the viscous collar can contribute at order
\(K^{-2}\).  It is therefore not lower order and is large enough in scale to
pay the positive creation if an independent estimate existed.

The fixed partition makes only the cutoff-motion row zero.  The projective
tangent row \(\langle P_Qx,E_{Q,t}\rangle\) remains present and leading.  No
part of the audit takes the positive parts of radial and tangent rows
separately.

## 8. Audit verdict

**PASS within the declared scope.**  The exact translated-cell algebra, the
independent Fourier reconstruction, the complete one-cell denominator
quadrature, and the scale ledger agree:

\[
 \mathcal Z_K^{\mathrm{sel,loc}}\gtrsim K^{-2},
 \qquad
 \mathcal H_K^{\mathrm{loc}}\lesssim(\nu K^4)^{-1}.
\]

This rejects only the same local heat/support endpoint as a uniform payment.
It does not reject a separate collar/shape/face budget, arbitrary or moving
partitions, an infinite frame--cell evolution identity, a Leray-limit
statement, a continuation criterion, or Navier--Stokes regularity.
