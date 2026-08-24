# R0.70S exact certificate

This directory locks the exact finite/symbolic payload for the R0.70S
energy-level no-go for the near-rank palinstrophy **majorant**.

Work on \(\mathbb T^3=(\mathbb R/2\pi\mathbb Z)^3\) with normalized Haar
measure. Fix \(M=16=2^4\), \(N=2^J\), and

\[
 v_N=(0,\cos Nx_1,\sin Nx_1),\qquad
 w_{MN}=(0,\sin MNx_1,\cos MNx_1).
\]

For \(A_N>0\), the producer checks

\[
 \omega_N=A_N\left[
 e^{-\nu N^2t}v_N+M^{-1}e^{-\nu M^2N^2t}w_{MN}
 \right],
\]

\[
 u_N=\frac{A_N}{N}\left[
 -e^{-\nu N^2t}v_N+M^{-2}e^{-\nu M^2N^2t}w_{MN}
 \right].
\]

It verifies \(\nabla\cdot u_N=0\), \(\nabla\times u_N=\omega_N\), zero
advective nonlinearity, and \(\partial_tu_N=\nu\Delta u_N\). Thus every
finite member is a smooth global mean-zero unforced Navier--Stokes shear
heat flow; no existence theorem is inferred from a finite computation.

The producer verifies four groups.

1. **Disjoint exact frame blocks.** For the pinned complete periodic frame

   \[
    \mathscr T=\{T_\star=\Pi_0\}\cup\{T_j:j\in\mathbb Z\},
   \]

   whose annular symbol has strict support \(1/2<|\xi|/2^j<2\), frequency
   \(N\) activates only \(j=J\), while \(MN\) activates only \(j=J+4\).
   Tightness gives response square one at both frequencies. This is an
   analytic consequence of the pinned strict support and exact tightness;
   the producer does not numerically evaluate the multiplier profile.
   Consequently

   \[
    Q_N=\alpha^2v_N\otimes v_N+\beta^2w_{MN}\otimes w_{MN},
   \]

   where \(\alpha=A_Ne^{-\nu N^2t}\) and
   \(\beta=A_NM^{-1}e^{-\nu M^2N^2t}\). Although
   \(\Pi_0\omega_N=0\), the zero-mode commutator
   \([\Pi_0,P_N]\omega_N\) is retained in the complete commutator square.

2. **Spectrum, gap, and positive majorant point.** Since

   \[
    d=v_N\cdot w_{MN}=\sin(17Nx_1),
   \]

   the exact characteristic polynomial is

   \[
    \mu[\mu^2-E\mu+\alpha^2\beta^2(1-d^2)].
   \]

   The nonzero eigenvalues have gap

   \[
    \lambda_1-\lambda_2
    =\sqrt{(\alpha^2-\beta^2)^2+4\alpha^2\beta^2d^2}
    \geq\alpha^2-\beta^2>0.
   \]

   With

   \[
    q=\frac{\beta^2}{\alpha^2}
     =\frac1{256}e^{-510\nu N^2t},
   \]

   the exact endpoint slacks give

   \[
    \frac{\lambda_1-\lambda_2}{E}\geq\frac{255}{257},
    \qquad 0\leq\eta:=\frac rE\leq\frac1{257}.
   \]

   Hence

   \[
    0\leq c_\eta
    =\frac{\sqrt\eta}{\sqrt{1-\eta}-\sqrt\eta}
    \leq\frac1{15}.
   \]

   Tightness gives

   \[
    \mathcal G_N=A_N^2N^2
    (e^{-2\nu N^2t}+e^{-2\nu M^2N^2t}).
   \]

   At \(t=0,x_1=0\), the directions are orthogonal,
   \(\eta=1/257\), \(c_\eta=1/15\), and
   \(\mathcal G_N/(A_N^2N^2)=2\). Thus the normalized integrand is
   \(2/15>0\). The finite-time gap makes it continuous, so it stays
   positive on a one-sided positive-measure neighbourhood in \(t\geq0\).
   This proves \(I_1(S)>0\) for every \(S>0\), without quadrature. Also

   \[
    0<I_1(\infty)\leq\frac{257}{7680\nu}<\infty.
   \]

3. **Analytic scaling lemmas and conditional exact arithmetic.** For
   \((\mathcal S_Nf)(x)=f(Nx)\), normalized Haar measure and the Fourier
   symbols give

   \[
    \|\mathcal S_Nf\|_p=\|f\|_p,\quad
    \Pi_0(\mathcal S_Nf)=\Pi_0f,\quad
    T_j\mathcal S_N=\mathcal S_NT_{j-J}.
   \]

   In particular, including the star block,

   \[
    [T_j,P_N]\omega_N
    =A_N\mathcal S_N([T_{j-J},P_1]\omega_1),
   \]

   \[
    [\Pi_0,P_N]\omega_N
    =A_N\mathcal S_N([\Pi_0,P_1]\omega_1).
   \]

   For every fixed \(T>0\),

   \[
    \|R_N\|_{L^2(0,T)}
    =\frac{A_N^2}{N}\|R_1\|_{L^2(0,N^2T)},
   \]

   \[
    \|\mathfrak C_{P_N}\|_{L^2(0,T)}
    =\frac{A_N^2}{N}
      \|\mathfrak C_{P_1}\|_{L^2(0,N^2T)},
   \]

   \[
    \mathfrak W_{L_N}(0,T)
    =\frac{A_N^4}{N^2}\mathfrak W_{L_1}(0,N^2T),
    \qquad I_N(T)=A_N^2I_1(N^2T).
   \]

   The universal Haar, spectral-projector, complete-frame, and commutator
   lifting statements in this display are analytic lemmas in the report.
   The producer independently checks the displayed fields against their
   (N=1) pullbacks, the Fourier multiplier-argument shift, one finite Haar
   sample, and the conditional factor arithmetic once the analytic
   pointwise scaling weights are supplied. It does not infer the general
   lemmas from that sample.

   The multiplier-dependent base commutator norm is not evaluated in closed
   form. Its finiteness follows analytically from complete-frame tightness:

   \[
    \mathfrak C_{P_1}(s)\leq4\|\omega_1(s)\|_2^2.
   \]

4. **Conditional exponent contradiction and boundary.** With
   \(A_N=N^{1/4}\),

   \[
    \|u_N(0)\|_2^2
    =\frac{65537}{65536}N^{-3/2},
   \]

   while the residual and complete commutator \(L_t^2\) identities carry
   the factor \(N^{-1/2}\), and \(\mathfrak W_{L_N}\) carries \(N^{-1}\).
   In contrast,

   \[
    I_N(T)=N^{1/2}I_1(N^2T)\longrightarrow\infty.
   \]

   This uses \(I_1(N^2T)\geq I_1(T)>0\), not numerical sampling. Meanwhile

   \[
    \|\omega_N(0)\|_2^2=\frac{257}{256}N^{1/2}\longrightarrow\infty.
   \]

## Claim boundary

Together with the report's named analytic lemmas, this exact payload rules
out only one right-hand side fixed uniformly across all dyadic \(N\) and
locally bounded near the zero four-tuple of kinetic energy, residual
\(L_t^2\) norm, exact
complete-frame commutator \(L_t^2\) norm, and weighted direction cost, with
\(T,\nu,\eta_0=1/257\), and the frame fixed. It concerns the positive
coefficient-level majorant \(c_\eta\mathcal G\).

It does **not** assert that the signed deficit
\(\mathcal K_Q-\mathcal D_P\) is large on this family. It does not exclude
estimates depending on initial \(H^1\), enstrophy, palinstrophy, higher
Sobolev norms, frequency moments, absolute covariance, or another
derivative-sensitive datum. It also does not prove a singularity, a PDE
closure, a continuation theorem, global regularity, or the Millennium
problem.

Run `command.txt` from the repository root. The regenerated JSON must be
byte-identical to `result.json` before checking `SHA256SUMS`.
