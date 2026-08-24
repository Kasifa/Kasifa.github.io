# R0.70Q exact certificate

This directory locks the finite exact payload for the covariance-evolution
and projector-gradient gate.

The producer verifies four groups.

1. With the row-gradient convention
   \(B_{ij}=\partial_i u_j\), vorticity stretching is \(B^{\mathsf T}\omega\).
   If a filtered block satisfies

   \[
   \mathcal D_\nu\Omega=B^{\mathsf T}\Omega+G,
   \qquad
   \mathcal D_\nu=\partial_t+u\cdot\nabla-\nu\Delta,
   \]

   then direct product differentiation gives

   \[
   \mathcal D_\nu(\Omega\otimes\Omega)
   =B^{\mathsf T}Q_\Omega+Q_\Omega B
    +G\otimes\Omega+\Omega\otimes G
    -2\nu\sum_k\partial_k\Omega\otimes\partial_k\Omega.
   \]

   Both a general algebraic jet and a direct polynomial differential sample
   verify the negative viscous-gradient-square sign.
2. At a simple largest eigenvalue \(\lambda_1\), with
   \(L=v_1\otimes v_1\), \(P=I-L\), and
   \(r=\operatorname{tr}(PQ)\), the producer verifies

   \[
   \partial\lambda_1=\operatorname{tr}(L\,\partial Q),
   \qquad
   \partial r=\operatorname{tr}(P\,\partial Q),
   \]

   and, for

   \[
   K_Q=\sum_{k,b>1}
   \frac{|v_b^{\mathsf T}(\partial_kQ)v_1|^2}
        {\lambda_1-\lambda_b}\ge0,
   \qquad K:=2K_Q,
   \]

   the curvature identities

   \[
   \Delta\lambda_1=\operatorname{tr}(L\Delta Q)+K,
   \qquad
   \Delta r=\operatorname{tr}(P\Delta Q)-K.
   \]

   Consequently the curvature sign is negative in the
   \(\mathcal D_\nu\lambda_1\) equation and positive in the
   \(\mathcal D_\nu r\) equation. A three-coordinate rational sample checks
   these signs independently through the characteristic polynomial.

   This certificate therefore uses \(K=2K_Q\). The canonical report's
   \(K_Q\) is the half-curvature sum without the leading factor two.
3. On normalized \(\mathbb T^3=(\mathbb R/2\pi\mathbb Z)^3\), the mode

   \[
   u_N=-e^{-\nu N^2t}(0,\cos Nx_1,\sin Nx_1)
   \]

   is divergence-free, has zero nonlinearity, satisfies the heat equation,
   and obeys \(\omega_N=-Nu_N\). A two-block scalar tight frame on its
   Fourier support gives

   \[
   Q=\omega_N\otimes\omega_N=E L,
   \qquad r=0,\qquad \lambda_1-\lambda_2=E,
   \]

   while

   \[
   |\nabla P|_F=\frac{|\nabla Q|_F}{E}=\sqrt2\,N.
   \]

   The covariance product equation and the exact cancellation in the
   residual curvature equation are also checked.
4. The amplitude-one family has normalized initial \(L^2\) energy and an
   exact energy identity. The rescaled family with
   \(a_N=(1+N^2)^{-1/2}\) satisfies

   \[
   \|a_Nu_N(0)\|_{H^1}^2
   =\|a_Nu_N(0)\|_2^2+\|\nabla(a_Nu_N)(0)\|_2^2=1,
   \]

   retains \(r=0\), relative gap one, and covariance energy at least
   \(1/2\), but has \(|\nabla P|_F=\sqrt2N\). This rules out only a bound
   for this explicit norm map: uniform initial \(H^1\) control together with
   zero residual and a unit relative gap cannot uniformly control the
   projector gradient.

Run the command in `command.txt` from the repository root. The regenerated
file must be byte-identical to `result.json` before checking `SHA256SUMS`.

## Scope boundary

The support-restricted two-block calculation is not a computer proof of an
infinite Littlewood--Paley theorem. The finite certificate does not prove
propagation for a covariance PDE or an analytic no-go statement beyond the
displayed energy/H1-to-projector-gradient norm maps. The normalized family
has unbounded higher Sobolev data, so it does not rule out estimates that use
such norms.

Nothing here proves a Navier--Stokes continuation criterion, finite-time
blow-up, global smoothness, or the Millennium problem.
