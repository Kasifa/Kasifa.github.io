# R0.72E independent analytic audit

**Date:** 2026-08-27
**Disposition:** pass after four required repairs: use a fixed
\(q_0>R_*\) for target-shell isolation; transfer the Bessel family through
the exact constant-diagonal conjugacy; cite the drift-bracket density theorem
from Kusuoka--Stroock Part II rather than Part III; and retain the strong
\((1+\log\delta)/\delta\) action bound.  The weaker
\(O(\delta^{-2/3})\) bound does not pay the final amplitude choice.

## 1. Scope of the audit

The audit reconstructed the following chain without using the producer
certificate:

\[
 \text{triangular NSE}
 \to\text{fixed-}q_0\text{ lattice}
 \to\text{Bessel roots}
 \to Q_{\delta,q_0}
 \to\text{full }\dot H^{-1}\text{ charge}
 \to\frac{\mathcal J_{\rm all}}{D^{1/3}\Lambda_1}.
 \tag{1.1}
\]

The purpose was to identify a missing factor or quantifier before the result
entered the public route.  No step below treats a numerical fit as a proof.

## 2. Exact PDE and projection

For

\[
 u=(f(y,z,t),0,v(y,t)),
 \tag{2.1}
\]

direct differentiation gives

\[
 \operatorname{div}u=0,
 \qquad
 (u\cdot\nabla)u=(vf_z,0,0).
 \tag{2.2}
\]

The pressure may be chosen constant after the gradient part of the quadratic
term is removed.  Equivalently,

\[
 \mathbb P(u\times\omega)=(-vf_z,0,0).
 \tag{2.3}
\]

This verifies that the action in the report is the complete projected Lamb
field of an exact unforced three-dimensional solution.

## 3. Fixed-\(q_0\) Fourier dictionary

Take

\[
 v=P e^{-q_0^2t}(e^{iq_0y}+e^{-iq_0y}),
 \qquad
 f^+=S\sum_rF_r(q_0^2t)e^{i(q_0ry+z)}.
 \tag{3.1}
\]

Then

\[
 F_x=D_\mu F+\delta V(x)F,
 \qquad
 \mu=q_0^{-2},
 \qquad
 \delta=P/q_0^2,
 \tag{3.2}
\]

with

\[
 (D_\mu F)_r=-(r^2+\mu)F_r,
 \qquad
 (VF)_r=-ie^{-x}(F_{r-1}+F_{r+1}).
 \tag{3.3}
\]

Thus the physical amplitude in the release must be

\[
 P_R=q_0^2\delta_R.
 \tag{3.4}
\]

The first rejected draft used \(q_0=1\).  A radial target annulus around
\(|k_*|=1\) would then also see the shear frequency.  Fixing any integer
\(q_0>R_*\) puts the shear and every non-target active mode outside the
multiplier support.  This is not a cosmetic change; it is needed for a
complete-shell root.

## 4. Exact transfer of the Bessel family

The fixed-\(q_0\) extension can be checked without repeating the growing
window proof.  Since

\[
 D_\mu=D_1+(1-\mu)I,
 \tag{4.1}
\]

the solutions satisfy the exact conjugacy

\[
 F_\mu(x)=e^{(1-\mu)x}F_1(x).
 \tag{4.2}
\]

Therefore their target zeros coincide exactly.  At a root,

\[
 P_0VF_\mu=e^{(1-\mu)x}P_0VF_1.
 \tag{4.3}
\]

The selected roots lie at \(x=O(R^{-3})\), so the factor in (4.3) is
\(1+O_{q_0}(R^{-3})\).  R0.72A's asymptotic remains

\[
 \sum_{k=1}^R|P_0VF_\mu(x_{k,R})|^2
 =\frac8{\pi^2}\log R+O_{q_0}(1).
 \tag{4.4}
\]

At a complete-shell root,

\[
 C_{*,t}=-\Delta F_*,
 \qquad
 \langle F_*,C_{*,t}\rangle=\|\nabla F_*\|_2^2>0.
 \tag{4.5}
\]

Hence every selected simple root is a positive right entry.  Alternating
scalar crossing signs do not remove half the roots.

## 5. Audit of the action theorem

### 5.1 Feynman--Kac time ordering

The initial-value formula runs the potential backward along the Brownian
path.  For

\[
 Z_t=\int_0^t e^{-(t-s)}e^{iB_s}\,ds,
 \qquad B_t=\sqrt2W_t,
 \tag{5.1}
\]

the exact representation is

\[
 \phi(t,\theta)
 =ie^{-\mu t}e^{-i\theta}
 \mathbb E\left[
 e^{-iB_t}
 e^{-2i\delta\operatorname{Re}(e^{i\theta}Z_t)}
 \right].
 \tag{5.2}
\]

Both the negative sign and the weight \(e^{-(t-s)}\) agree with the first
Duhamel derivative at \(\delta=0\).

### 5.2 Oscillatory negative norm

For \(A_\mu=\mu-\partial_\theta^2\), low Fourier modes of

\[
 \cos\theta e^{-i\theta}e^{-i\kappa\cos(\theta+\beta)}
 \tag{5.3}
\]

are \(O(\kappa^{-1/2})\) by uniform nondegenerate stationary phase.  The
sum of their \(A_\mu^{-1}\) weights is finite:

\[
 \sum_n\frac1{\mu+n^2}
 =\pi q_0\coth(\pi/q_0).
 \tag{5.4}
\]

The high-frequency Parseval tail is \(O(\kappa^{-2})\).  Thus the squared
norm is \(O_{q_0}((1+\kappa)^{-1})\).  The audit rejects any claim that the
constant is uniform when \(q_0\to\infty\).

### 5.3 Quantitative weak Hörmander input

The kinetic diffusion is

\[
 dB_t=\sqrt2dW_t,
 \qquad dZ_t=(-Z_t+e^{iB_t})dt.
 \tag{5.5}
\]

The noise field and two drift brackets are mutually transverse everywhere;
their absolute determinant in \((B,\operatorname{Re}Z,\operatorname{Im}Z)\)
coordinates is exactly \(4\).
This is a parabolic/weak Hörmander condition, not a strong-noise-bracket
condition.  Kusuoka--Stroock Part II, Corollary (3.25) and inequality
(3.27), pp. 22--23, permit these drift brackets and give a polynomial
small-time joint-density bound.  Choosing the off-diagonal order above one
makes the terminal-angle weight integrable, so the marginal satisfies

\[
 \|\rho_t^Z\|_\infty\le C_Tt^{-N}.
 \tag{5.6}
\]

Part III was inspected and rejected as the citation for this step.

### 5.4 Negative moment and integration

On the Brownian event \(\sup_{s\le t}|B_s|\le\pi/3\),

\[
 |Z_t|\ge\tfrac12(1-e^{-t})\gtrsim_Tt.
 \tag{5.7}
\]

The complement has probability \(O(e^{-c/t})\).  The two-dimensional
density makes \(|z|^{-3/2}\) integrable, and Hölder's inequality absorbs
every polynomial density loss into the exponential complement.  Therefore

\[
 \mathbb E|Z_t|^{-1}\le C_T/t.
 \tag{5.8}
\]

Jensen and (5.8) give

\[
 Q_{\delta,q_0}(T)
 \lesssim_{T,q_0}
 \int_0^T\min\{1,(\delta t)^{-1}\}\,dt
 \lesssim_{T,q_0}\frac{1+\log(2+\delta)}\delta.
 \tag{5.9}
\]

This strong form is necessary.  If one retained only
\(Q=O(\delta^{-2/3})\), then the chosen
\(S^2=\delta/\log(2+\delta)\) would make the normalized rotational action
grow.  The weaker estimate is sufficient for other amplitudes, but not for
the theorem as stated.

## 6. Exact physical powers

Under normalized Fourier Parseval,

\[
 D_R
 =2P_R^2(1+q_0^2)+2S_R^2(q_0^2+2).
 \tag{6.1}
\]

With \(P_R=q_0^2\delta_R\) and
\(S_R^2=\delta_R/\log(2+\delta_R)\),

\[
 D_R\asymp_{q_0}\delta_R^2.
 \tag{6.2}
\]

The exact enstrophy is

\[
 Y_R(t)=2q_0^2P_R^2e^{-2x}
 +2S_R^2\left(\|F_R(x)\|_2^2
 +q_0^2\|\partial_\theta\phi_R(x)\|_2^2\right),
 \quad x=q_0^2t.
 \tag{6.3}
\]

The first-moment barrier

\[
 \|\partial_\theta\phi_R\|_2^2
 \le\max\{1,(2\delta_R)^{2/3}\}
 \tag{6.4}
\]

makes the active-to-shear enstrophy ratio
\(O_{T,q_0}(\delta_R^{-1/3}/\log\delta_R)\).  Hence
\(\mathcal R_Y=O_{T,q_0}(1)\).

## 7. Full rotational charge and the three \(q_0^{-2}\) factors

Every positive-sector Lamb mode has frequency \((q_0r,1)\).  Consequently

\[
 \|\mathbb P(u\times\omega)\|_{\dot H^{-1}}^2
 =2S_R^2P_R^2q_0^{-2}
 \|VF_R\|_{A_q^{-1}}^2.
 \tag{7.1}
\]

Changing variables contributes a second \(q_0^{-2}\), and division by the
shear-enstrophy floor contributes a third.  Explicitly,

\[
 \frac1T\int_0^T
 \frac{\|\mathbb P(u\times\omega)\|_{\dot H^{-1}}^2}{Y_R}\,dt
 \le\frac{e^{2q_0^2T}S_R^2}{Tq_0^6}
 Q_{\delta_R,q_0}(q_0^2T)
 =O_{T,q_0}(1).
 \tag{7.2}
\]

The expression sums every lattice coefficient.  It is not a target-shell
estimate.

## 8. Final exponent ledger

The root atom is

\[
 J_*(t_{k,R})
 =c_*\frac{S_R^2P_R^2|h_{k,R}|^2}{Y_R(t_{k,R})},
 \qquad c_*>0.
 \tag{8.1}
\]

Thus

\[
 \mathcal J_{{\rm all},R}
 \gtrsim_{q_0}
 \frac{\delta_R}{\log(2+\delta_R)}\log R
 \asymp_{q_0}\delta_R.
 \tag{8.2}
\]

Together with \(D_R^{1/3}\asymp\delta_R^{2/3}\) and
\(\Lambda_1=O(1)\),

\[
 \frac{\mathcal J_{{\rm all},R}}
 {D_R^{1/3}\Lambda_1}
 \gtrsim_{T,q_0}\delta_R^{1/3}=R^{4/3}.
 \tag{8.3}
\]

The exponent arithmetic is exact.  Unknown fixed target, torus, and
\(q_0\) constants cannot change divergence.

## 9. Independent computation boundary

The independent program uses a real invariant lattice and a fixed-step root
scan, while the producer uses a complex spectral action solver and separate
Bessel brackets.  It checks root count, root shifts, selected mass, action
trend, data identities, and the exponent ledger.  It imports neither the
producer code nor its result.

The numerical calculations are finite truncations in binary64 arithmetic.
They are not interval certificates and do not prove the infinite-lattice
limit or the cited density theorem.  Their purpose is to catch sign,
normalization, and implementation errors.

## 10. Final disposition

The fixed-\(q_0\) theorem is internally consistent and the physical
normalization closes.  No fatal gap remains in the stated triangular-class
negative result.  The following statements remain outside the evidence:

1. a \(q_0=q_0(R)\) limit;
2. a nontriangular full-feedback construction;
3. failure of every possible data-dependent payment;
4. a continuation criterion, finite-time singularity, or global regularity
   theorem for general three-dimensional Navier--Stokes solutions.
