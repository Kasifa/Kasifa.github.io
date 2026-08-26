# R0.72B bounded literature audit

**Checked:** 2026-08-27
**Question:** Does an existing enhanced-dissipation theorem uniformly control
the heat-decaying, many-frequency profile used in R0.72B, or the accumulated
complete target-root ledger?

## Direct answer

No checked source proves that statement. The closest papers control terminal
semigroup decay for fixed stationary profiles, slowly varying profiles with
uniform structure, scalar time modulation of one fixed profile, or a rigidly
translating sine profile. None controls a coordinate-zero derivative ledger
accumulated before the decay time. None supplies constants uniform for the
R0.72B trigonometric polynomials when the number of carriers, critical points,
and heat-decay rates all vary with \(M\).

This is a bounded claim about the sources listed below, not a claim that no
other relevant paper exists.

## Source matrix

| Primary source | Proved scope used here | Why it does not close R0.72B |
|---|---|---|
| Constantin--Kiselev--Ryzhik--Zlatoš, [Annals 2008](https://doi.org/10.4007/annals.2008.168.643) | Qualitative relation between relaxation enhancement and mixing for incompressible flows. | Does not provide the present nonautonomous many-carrier constants or a root-slope ledger. |
| Bedrossian--Coti Zelati, [Arch. Rational Mech. Anal.](https://doi.org/10.1007/s00205-017-1099-y) | Quantitative enhanced dissipation for stationary shear flows with finite-order critical points, including the viscosity/degeneracy scale used as a frozen comparison. | The profile is autonomous. Uniformity under an \(M\)-dependent heat-evolving trigonometric polynomial is not supplied. |
| Albritton--Beekie--Novack, [arXiv:2105.12308](https://arxiv.org/abs/2105.12308) | Enhanced dissipation through Hörmander-type hypoellipticity for fixed vector fields under finite-order bracket conditions. | Does not track changing critical geometry or accumulated exact coordinate zeros. |
| Coti Zelati--Gallay, [JLMS](https://doi.org/10.1112/jlms.12782) | Sharp enhanced-dissipation and Taylor-dispersion estimates for higher-dimensional parallel stationary shears. | Stationary profile and terminal norm estimates; no complete target-row slope measure. |
| Coble--He, [arXiv:2309.15738](https://arxiv.org/abs/2309.15738), [published version](https://doi.org/10.4310/CMS.2024.v22.n6.a10) | Sharp decay for time-dependent shears whose critical points vary slowly relative to a reference profile, with uniform profile regularity, finite critical structure, and a small time derivative. | An \(M\)-growing heat sum need not have uniform critical count, shape constants, \(W^{2,\infty}\) bounds, or slow variation. The theorem does not pay past root slopes. |
| Gardner--Liss--Mattingly, [arXiv:2410.05657](https://arxiv.org/abs/2410.05657) | Pathwise enhanced dissipation for smooth fixed shears, including local dependence on streamline geometry and finite/infinite-order critical behavior. | The checked results are not a uniform theorem for the present changing heat profile and do not estimate the target-root ledger. |
| Benthaus--Nobili, [arXiv:2501.16905](https://arxiv.org/abs/2501.16905) | Nonautonomous enhanced dissipation for \(v(y,t)=\xi(t)w(y)\), including accelerating and intermittent scalar modulation. | All spatial critical points belong to one fixed profile \(w\). R0.72B changes the relative Fourier amplitudes, so it is not scalar modulation. |
| Benthaus--Coclite--Nobili, [arXiv:2603.14624](https://arxiv.org/abs/2603.14624) | For \(v(y,t)=\sin(y-ct)\), proves time-averaged mixing, enhanced dissipation for \(c=c_0\nu^\ell\), \(\ell\in(1/3,3/4)\), and heat-like behavior for large translation speed. | It treats a rigidly translating single sine with a specialized extended functional. It does not cover an \(M\)-frequency heat-decaying sum or a launch-inclusive root ledger. |

## Exact comparison boundary

The R0.72B frozen comparison records four quantities separately:

\[
 n_M,\qquad c_{{\rm sub},M},\qquad
 \Theta_M=L_M\Gamma_M^{\rm fr},\qquad
 \Xi_M=|\delta_M|\int\|b_M(x)-b_M(A)\|_\infty\,dx.
\]

The first two encode critical geometry. The third measures whether the
observation window reaches the adjacent frozen decay time. The fourth is the
coupling-weighted Duhamel error. The weaker condition
\(L_M\kappa r_{\max,M}^2\ll1\) does not imply \(\Xi_M\ll1\).

Even a valid nonautonomous semigroup estimate can only enter a restarted tail
bound through the remaining energy. The nonnegative complete ledger splits as

\[
G_{\rm all}^{\rm ex}([0,a+L])
=G_{\rm pre}^{\rm ex}([0,a])
+G_{\rm tail}^{\rm ex}((a,a+L]),
\]

so terminal decay cannot cancel the first term.

## What was searched

The audit checked the cited primary papers and targeted searches for:

- time-dependent shear enhanced dissipation;
- moving critical points;
- scalar time modulation and intermittent shear;
- heat-evolving or heat-decaying shear profiles;
- many-frequency uniform enhanced dissipation;
- pathwise and Hörmander approaches.

Search results unrelated to incompressible shear advection--diffusion were
discarded. No secondary survey is used to support a theorem statement.

## Consequence for R0.72B

The target-row participation theorem is independent of an enhanced-dissipation
theorem. It controls the complete ledger directly and is valid before the
adjacent frozen decay time. Enhanced dissipation remains an optional tail
improvement, subject to its own uniform hypotheses and the freezing error.
