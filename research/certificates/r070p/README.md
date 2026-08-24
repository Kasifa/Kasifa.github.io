# R0.70P exact certificate

This directory locks the finite exact payload for the periodic
projector/harmonic bridge gate.

The producer verifies five groups:

1. for the convention (B_{ij}=\partial_i u_j), the orientation-free
   identity

   \[
   \operatorname{tr}(LS^2)-\frac14|P\omega|^2
   =B_{ij}B_{ki}L_{jk},
   \qquad L^2=L=L^{\mathsf T},\quad \operatorname{tr}L=1,\quad P=I-L,
   \]

   on an eight-parameter trace-free symbolic gradient family and rational
   samples;
2. constant- and variable-projector periodic trigonometric examples,
   including a sign-changing local lift, for the integration-by-parts
   identity;
3. the complete sixteen-sign, four-vector Rademacher orthogonality identity;
4. the exact \(\sqrt W\) loss for bounded square-function weights and a
   projector-valued, near-single-frequency commutator family showing why an
   unbounded sequence of weights has no uniform constant (the exact
   subsequence \(n_J=2^{J-1}\) makes the audited scale \(2n_J=2^J\)
   dyadic, while the selected profile satisfies
   \(\phi'(1/2)=24/25\ne0\)); and
5. the torus completion \(T_\star=\Pi_0\), including the exact finite-Fourier
   identity \([\Pi_0,P]f=\Pi_0(Pf)\) for mean-zero \(f\), an equality case of
   homogeneous \(H^{-1}\)--\(H^1\) duality, the vanishing direct covariance
   \(Q_\star\) and residual \(R_\star\) contributions, and a
   finite-dimensional analysis/synthesis bridge with explicit commutator,
   blind-frame, equality, and deterministic pseudorandom rational cases.

The constant block is not an observed residual term: periodic vorticity has
\(\Pi_0\omega=0\), so \(P\Pi_0\omega=0\). It is nevertheless required on
the reconstruction side because \(P\omega\) can have nonzero mean and

\[
 \Pi_0(P\omega)=[\Pi_0,P]\omega.
\]

Thus the canonical periodic bridge has the finite-audit target form

\[
 \|P\omega\|_2\le C_{\rm LP}\left[
 \left(\sum_j\|PT_j\omega\|_2^2\right)^{1/2}
 +\left(\|[\Pi_0,P]\omega\|_2^2
 +\sum_j\|[T_j,P]\omega\|_2^2\right)^{1/2}\right].
\]

The certificate verifies one exact finite Fourier instance of the constant
block and finite matrix instances of the bridge; it does not certify the
infinite-dimensional estimate displayed above.

All periodic values use
\(\mathbb T^3=(\mathbb R/2\pi\mathbb Z)^3\) with normalized Haar measure,
Fourier modes \(e^{ik\cdot x}\), and
\(|D|e^{ik\cdot x}=|k|e^{ik\cdot x}\). In particular,
\(\|f\|_{\dot H^{-1}_\#}^2=\sum_{k\ne0}|\widehat f(k)|^2/|k|^2\).

Run the command in `command.txt` from the repository root. The regenerated
file must be byte-identical to `result.json` before checking `SHA256SUMS`.

## Scope boundary

The producer checks finite symbolic, rational, trigonometric,
Fourier-coefficient, Rademacher, matrix, and limit identities. It does **not** prove a Calderón reproducing theorem,
Littlewood--Paley boundedness on an infinite-dimensional function space, the
variable-projector commutator estimate required by Navier--Stokes, or a PDE
continuation theorem. The
finite-dimensional bridge records exactly which reconstruction and
commutator hypotheses such an analytic theorem would still need.

The periodic projector argument also distinguishes

\[
 \operatorname*{ess\,sup}_{0<t<T_{\max}}
 \|\nabla L(t)\|_{\infty}<\infty
\]

from mere local boundedness on compact subintervals of
\([0,T_{\max})\). The latter does not imply the former. This certificate
does not package that logical distinction as a counterexample or claim that
either condition follows from a covariance ledger.

Nothing here proves finite-time blow-up, global smoothness, or the
Navier--Stokes Millennium problem.
