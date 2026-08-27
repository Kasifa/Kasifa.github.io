# R0.72E bounded primary-source literature audit

**Search date:** 2026-08-27
**Question:** Which primary results justify the kinetic-density input and
which neighboring shear-flow theorems could, or could not, replace the direct
negative Sobolev action proof?

## Direct conclusion

The new external input is narrow.  Kusuoka--Stroock Part II gives the
quantitative transition-density estimate for a diffusion whose missing
directions are created by brackets with the drift.  After verifying a
uniform three-vector frame and integrating the lifted terminal angle, it
supplies the polynomial marginal density bound used in R0.72E.

The bounded search did not find a deterministic enhanced-dissipation theorem
that directly states

\[
 \int_0^T\|V(t)\phi(t)\|_{A_q^{-1}}^2dt
 \lesssim\frac{1+\log\delta}{\delta}
 \tag{0.1}
\]

for the heat-decaying potential in the report.  Existing neighboring results
control terminal norms, fixed-profile mixing, or different observations.
They are comparisons, not substitutes for the Feynman--Kac proof.

## Claim-to-source ledger

| primary source | checked result | use in R0.72E | does not provide |
|---|---|---|---|
| S. Kusuoka and D. Stroock, *Applications of the Malliavin calculus, Part II* (1985), Corollary (3.25) and inequality (3.27), pp. 22--23, [repository record](https://repository.dl.itc.u-tokyo.ac.jp/records/39529), [DOI](https://doi.org/10.15083/00039520) | Global quantitative density and derivative bounds under a uniform condition that includes drift-generated brackets; the introduction explicitly notes inclusion of Hörmander's drift term. | With \(X_1=\sqrt2\partial_\theta\) and the first two drift brackets, gives a polynomial joint-density bound.  Choosing the off-diagonal order above one makes the lifted terminal-angle weight integrable and gives the \(Z_t\) marginal bound. | The oscillatory \(A_q^{-1}\) estimate, the negative-moment return event, or the NSE ledger. |
| NIST DLMF [10.12](https://dlmf.nist.gov/10.12) | Jacobi--Anger expansions. | Identifies the frozen target as \(J_1(2\tau)\). | Persistence under exact dissipation. |
| NIST DLMF [10.21](https://dlmf.nist.gov/10.21), [10.17](https://dlmf.nist.gov/10.17), and [10.6](https://dlmf.nist.gov/10.6) | Simplicity, spacing, zero asymptotics, derivative asymptotics, and recurrence identities for Bessel functions. | Gives the separated roots and the coefficient \(8/\pi^2\) in the selected slope mass. | The growing-window \(C^1\) comparison. |
| C. Coble and S. He, *A Note on Enhanced Dissipation and Taylor Dispersion of Time-dependent Shear Flows* (2024), [arXiv:2309.15738](https://arxiv.org/abs/2309.15738) | Quantitative enhanced dissipation for time-dependent shears with controlled critical-point structure. | A deterministic comparison after rescaling the decaying cosine profile. | The \(A_q^{-1}\) action (0.1) or temporal coordinate roots. |
| M. Beck and C. E. Wayne, *Metastability and rapid convergence to quasi-stationary bar states for the two-dimensional Navier--Stokes equations* (2013), [arXiv:1108.3416](https://arxiv.org/abs/1108.3416) | Rapid decay for an approximate nonautonomous operator around a viscously decaying bar state. | Close heat-decaying-shear comparison. | The exact operator here, an unweighted initial norm, or the required action. |
| J. Bedrossian and M. Coti Zelati, *Enhanced dissipation, hypoellipticity, and anomalous small noise inviscid limits in shear flows* (2017), [arXiv:1510.08098](https://arxiv.org/abs/1510.08098) | Fixed-profile enhanced-dissipation and inviscid negative-Sobolev mixing estimates with rates depending on critical-point degeneracy. | Confirms the \(\sqrt\delta\) comparison scale for a cosine profile. | A stable nonautonomous action estimate with no derivative loss. |
| M. Coti Zelati, *Stable mixing estimates in the infinite Péclet number limit* (2019), [arXiv:1909.01310](https://arxiv.org/abs/1909.01310) | Stable \(H^{-1}\) mixing for strictly monotone shears under quantitative derivative ratios. | Shows the hypotheses needed for a direct stable negative-norm transfer. | Cosine has critical points and violates strict monotonicity. |
| G. Iyer, X. Maekawa, and N. Masmoudi, *On pseudospectral bounds for non-selfadjoint operators and their applications to stability of Kolmogorov flows* (2019), [arXiv:1710.05132](https://arxiv.org/abs/1710.05132) | Sharp resolvent and semigroup estimates for Kolmogorov-type operators. | A spectral-scale comparison for a sinusoidal profile. | The integrated Kato observation needed in (0.1), and its operator contains a different nonlocal term. |
| O. Perruchaud, *Small time expansion for a strictly hypoelliptic kernel* (2023), [arXiv:2301.06904](https://arxiv.org/abs/2301.06904) | Sharp small-time density scales for kinetic Brownian motion without the damping \(-Z\). | Corroborates the polynomial hypoelliptic density mechanism. | Literal coverage of \(dZ=(-Z+e^{i\Theta})dt\). |

## Exact citation boundary

Part III of Kusuoka--Stroock is not cited for the decisive density step.  Its
relevant density section imposes a zero-drift restriction.  The present
diffusion is parabolic/weak Hörmander: the two planar directions appear only
after commuting the noise field with the drift.  Part II, Corollary (3.25)
and inequality (3.27), pp. 22--23, are the verified source statements that
permit this structure and expose the required polynomial small-time and
off-diagonal weights.

The report uses the source as follows:

1. lift the angular Brownian motion to \(\mathbb R\);
2. verify the uniform frame from \(X_1\), \([X_1,X_0]\), and
   \([X_1,[X_1,X_0]]\);
3. choose the polynomial off-diagonal order above one; and
4. integrate the terminal angle to obtain
   \(\|\rho_t^Z\|_\infty\le C_Tt^{-N}\).

No compact-manifold extension or unproved periodization is used.

## Negative search result

The deterministic sources above do not close the chain

\[
 \text{terminal enhanced dissipation}
 \Longrightarrow
 \text{integrated }A_q^{-1}\text{ observation}
 \Longrightarrow
 \text{bounded full NSE rotational charge}
 \Longrightarrow
 \text{supercritical temporal-root ledger}.
 \tag{4.1}
\]

R0.72E proves the first missing implication directly by a random-phase
representation, stationary phase, and a return-event estimate.  The later
implications use the exact triangular Fourier dictionary.  The bounded
search found no primary paper stating the combined result.  This is not an
originality, priority, or exhaustive nonexistence claim.
