# R0.70T exact certificate

This directory locks the exact finite/symbolic payload for the R0.70T frame
stretching identity, divergence-free amplitude cancellation, and sharp
fixed-frame divergence defect.

Work on normalized

\[
 \mathbb T^3=(\mathbb R/2\pi\mathbb Z)^3,
 \qquad B_{ij}=\partial_i u_j,
 \qquad S=\tfrac12(B+B^{\mathsf T}).
\]

For the pinned complete scalar frame

\[
 \mathscr T=\{T_\star=\Pi_0\}\cup\{T_j:j\in\mathbb Z\},
 \qquad \sum_\alpha T_\alpha^2=I,
\]

put \(\Omega_\alpha=T_\alpha\omega\) and
\(Q=\sum_\alpha\Omega_\alpha\otimes\Omega_\alpha\).  At a simple top
eigenvalue write

\[
 Q=\lambda L+H,
 \qquad L=\ell\otimes\ell,
 \qquad P=I-L.
\]

The two central identities are

\[
 \int\omega\cdot S\omega
 =\int S:Q
  +\sum_\alpha\langle\Omega_\alpha,[T_\alpha,S]\omega\rangle,
 \qquad [T,S]=T(S\,\cdot)-ST,
\]

and

\[
 \mathcal A_L
 =L(\nabla\lambda+2\lambda\operatorname{div}L)
 =-2\ell\sum_\alpha
   a_\alpha\operatorname{div}b_\alpha,
\]

where \(a_\alpha=\ell\cdot\Omega_\alpha\) and
\(b_\alpha=P\Omega_\alpha\).  Thus

\[
 |\mathcal A_L|\leq2\sqrt{\lambda\mathcal J_P},
 \qquad
 \mathcal J_P=\sum_\alpha
 |\operatorname{div}(P\Omega_\alpha)|^2.
\]

## Direct machine checks

The producer performs five groups of exact checks.

### 1. Noncommuting finite Parseval ledger

It uses

\[
 T_1=\operatorname{diag}(3/5,5/13),\qquad
 T_2=\operatorname{diag}(4/5,12/13),
\]

\[
 S=\begin{pmatrix}2&3\\3&-1\end{pmatrix},
 \qquad w=(1,2)^{\mathsf T}.
\]

The producer calculates, rather than preassigns,

\[
 T_1^2+T_2^2=I,
 \qquad w^{\mathsf T}Sw=10,
\]

\[
 \sum_i(T_iw)^{\mathsf T}S(T_iw)=\frac{626}{65},
 \qquad
 \sum_i(T_iw)^{\mathsf T}[T_i,S]w=\frac{24}{65}.
\]

The nonzero commutator fixes the plus sign in the finite Parseval split.  This
finite Hilbert-space calculation does not prove the countable Fourier-frame
identity.

### 2. Nonzero periodic product-rule sample

For

\[
 u=(2\cos x_2,0,2\cos x_1+2\sin(x_1+x_2)),
\]

the producer forms \(B,S,\omega=\nabla\times u\),
\(Q=\omega\otimes\omega\), and \(\operatorname{div}Q\) from the displayed
field.  It verifies both divergences vanish and obtains the nonzero exact
averages

\[
 \int S:Q=\int B:Q
 =-\int u\cdot\operatorname{div}Q=2.
\]

This sample fixes the row-gradient and tensor-divergence signs.  General
periodic integration by parts at Sobolev regularity remains analytic.

### 3. Cancellation polynomial and sharp SOS

In the coordinate gauge \(\ell=e_1\), let

\[
 p_\alpha=\ell\cdot\nabla a_\alpha,
 \qquad d_\alpha=\operatorname{div}b_\alpha,
 \qquad \delta=\operatorname{div}\ell.
\]

The producer retains the actual block-divergence residuals

\[
 c_\alpha=p_\alpha+a_\alpha\delta+d_\alpha
\]

and proves the polynomial certificate

\[
 \mathcal A_{\parallel}
 +2\sum_\alpha a_\alpha d_\alpha
 =2\sum_\alpha a_\alpha c_\alpha.
\]

Only after the divergence-free premises \(c_\alpha=0\) does this yield the
amplitude cancellation.  The producer also expands the covariance from
finite blocks and checks

\[
 Q-\lambda L-H
 =\ell C^{\mathsf T}+C\ell^{\mathsf T},
 \qquad C=PQ\ell=\sum_\alpha a_\alpha b_\alpha.
\]

The eigenline premise is \(C=0\); it is not inserted by defining both sides
to be equal.

For three finite blocks it checks the exact Lagrange identity

\[
 \lambda\mathcal J_P-(a\cdot d)^2
 =\sum_{i<j}(a_id_j-a_jd_i)^2,
\]

which proves the coefficient \(2\) and includes an equality witness.

### 4. Fixed-frame global vertical shear

Set \(M=16\) and

\[
 \psi_L=\frac M5\sin(5x_2)
 +\frac M{24}
 [\cos(3x_1+4x_2)-\cos(3x_1-4x_2)],
\]

\[
 \psi_H=-\frac1{5M}\sin(5Mx_1)+\frac1{25}\cos(5Mx_2),
\]

\[
 u_M^0=M^{-1}(0,0,\psi_L+\psi_H),
 \qquad \omega_M=\nabla\times u_M^0=\omega_L+\omega_H.
\]

The producer differentiates these fields and verifies:

- zero velocity and vorticity divergence and zero vorticity mean;
- \((\Delta+25)\omega_L=0\) and
  \((\Delta+6400)\omega_H=0\);
- the full curl identity;
- the time-dependent heat-equation residuals;
- zero advective nonlinearity and \(S\omega=0\).

Thus the displayed finite Fourier field itself is an exact smooth global
unforced vertical-shear heat solution.

The multiplier profile is not evaluated numerically.  Strict annular support
implies only

\[
 \varnothing\ne I_5\subseteq\{2,3\},
 \qquad I_{80}=I_5+4\subseteq\{6,7\}.
\]

It does not imply that both possible indices are active.  Put

\[
 \rho=\varphi(5/4),\qquad
 \sigma=\varphi(5/8).
\]

Real-even radiality and exact tightness give the analytic premise

\[
 \rho^2+\sigma^2=1.
\]

The producer retains \(\rho,\sigma\) symbolically and proves the factor
identity

\[
 Q_{\rm frame}-Q_{\rm target}
 =(\rho^2+\sigma^2-1)Q_{\rm target}.
\]

At \(x=t=0\), it computes

\[
 Q=\operatorname{diag}(1,1/256,0),
 \qquad \partial_1Q=\operatorname{diag}(-2,0,0),
 \qquad \partial_2Q=\partial_3Q=0.
\]

Using the full first-order spectral-projector and projected-block product
rules, including \(\partial_iP\), it obtains

\[
 \nabla L=0,
 \qquad \mathcal J_P=1,
 \qquad \mathcal A_L=-2e_1,
 \qquad \frac rE=\frac1{257}.
\]

The same derivative ledger is computed from the four symbolic response
blocks, giving

\[
 \lambda_1-\lambda_2=\frac{255}{256},
 \qquad
 \frac{\lambda_1-\lambda_2}{E}=\frac{255}{257},
 \qquad
 \mathcal G=258.
\]

Hence equality in the coefficient-2 bound is attained inside the pinned-frame
class.  This statement is pointwise at the initial time.  It neither asserts
uniform near rank on the torus nor propagation of the equality.

The direct machine anchor in this archive is \(M=16\).  The parameter family
\(M=2^m\) and the limit \(r/E=1/(M^2+1)\to0\) are proved by the report's
general symbolic formulas, not by pretending that one finite machine run
certifies every \(M\).

### 5. Isolated exact-rank boundary

For the local block jets

\[
 \Omega_1=(1-x_1,x_2,0),
 \qquad \Omega_2=(1+x_1,-x_2,0),
\]

the producer computes at the origin

\[
 Q=2e_1\otimes e_1,
 \qquad \nabla Q=\nabla L=0,
\]

\[
 \operatorname{div}(P\Omega_1)=1,
 \qquad \operatorname{div}(P\Omega_2)=-1.
\]

Thus \(\mathcal A_L=0\) but \(\mathcal J_P=2\).  An isolated smooth
rank-one point does not force \(\mathcal J_P=0\); the latter follows when
rank one holds on an open neighborhood.

## Analytic dependencies

The certificate does not claim to machine-prove:

- the countable Parseval identity, convergence, or sum/integral exchange;
- the general pinned cutoff support, real-even radiality, tight partition, or
  commutation with derivatives;
- general smooth simple-eigenvalue projector calculus or orientation
  patching;
- the whole-torus Section 5 ledger without its global simple-top hypothesis;
- the report's reduced inverse \(\mathcal R_Q\), half-curvature convention
  for \(\mathcal K_Q\), or the general derivative upper ledger (6.7);
- the report's general \(M=2^m\) extension and its \(M\to\infty\) near-rank
  limit; this archive directly computes the \(M=16\) anchor;
- the periodic \(H^1\) blow-up alternative.

The Section 8 continuation reading assumes both \(T_{\max}<\infty\) and a
global simple top eigenvalue on
\(\mathbb T^3\times[0,T_{\max})\).  The certificate does not verify those
hypotheses from initial data.

## Claim boundary

Together with the named analytic frame lemmas, the exact payload proves that
common block origin and a pointwise residual ratio \(1/(M^2+1)\) neither
improve the coefficient \(2\) nor make
\(\mathcal A_L/\sqrt{\lambda\mathcal J_P}\) small.  The sample has identically
zero vortex stretching, so it is not a stretching-production counterexample.

The certificate does not control \(\mathcal J_P\), the stretching commutator,
or enstrophy by energy-level inputs.  It does not establish a signed estimate,
propagate near rank, close a PDE inequality, prove a singularity, verify the
continuation hypotheses, prove unconditional global regularity, or solve the
Millennium problem.

Run `command.txt` from the repository root.  The regenerated JSON must be
byte-identical to `result.json` before checking `SHA256SUMS`.
