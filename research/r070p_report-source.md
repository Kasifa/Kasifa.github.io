# R0.70P — An energy-level Littlewood–Paley commutator bridge and a periodic projector criterion

**Status:** internal canonical candidate; not a public theorem chapter

**Release:** R0.70P

**Date:** 2026-08-25

## 1. Decision in one page

R0.70O proved that finite high-frequency-blind scalar observations cannot
uniformly reconstruct the unfiltered transverse-vorticity norm.  R0.70P asks
whether a **complete** smooth Littlewood--Paley frame repairs that loss when
the target plane varies with space and time.

Three analytic gates are separated.

1. **Frame-to-vorticity gate: PASS.**  For a complete scalar frame and a
   rank-two orthogonal projector \(P(x,t)\), the only new term is the square
   commutator
   \[
     \mathcal C(t)=\sum_\alpha\|[T_\alpha,P]\omega(t)\|_2^2.
     \tag{1.1}
   \]

2. **Energy-level commutator gate: PASS for a fixed standard smooth frame.**
   If \(T_j=\varphi(2^{-j}D)\) is a smooth annular
   Littlewood--Paley family, then
   \[
    \boxed{
    \left(\sum_\alpha\|[T_\alpha,A]f\|_2^2\right)^{1/2}
    \leq C_\varphi\|\nabla A\|_\infty\|f\|_{\dot H^{-1}}.}
    \tag{1.2}
   \]
   On \(\mathbb T^3\), \(f\) is required to have zero mean and the square
   sum also contains the constant-mode block \(T_\star=\Pi_0\).  The proof uses
   finite Rademacher randomization and a separate zero-mode estimate, plus the first-order
   Calderón--Coifman--Meyer commutator theorem.  It is not a consequence of
   an arbitrary frame lower bound.

3. **Continuation-consumer gate: PASS on \(\mathbb T^3\).**  Miller's
   variable-direction argument has an orientation-free projector form.  For
   a maximal unforced periodic \(H^1\) mild solution, if
   \[
    \operatorname*{ess\,sup}_{0<t<T_{\max}}
       \|\nabla L(t)\|_\infty<\infty,
    \qquad
    (I-L)\omega\in L^4(0,T_{\max};L^2),
    \tag{1.3}
   \]
   where \(L\) is a measurable rank-one orthogonal projector, then the
   solution extends past \(T_{\max}\).  No global choice of a unit
   eigenvector and no time derivative of \(L\) are needed.

These three facts give the conditional bridge

\[
 \boxed{
 \|P\omega\|_{L_t^4L_x^2}
 \leq a_0^{-1/2}
 \left(
  \|R\|_{L_t^2}^{1/2}
  +C_{\mathcal T}\|u-\bar u\|_{L_t^\infty L_x^2}
       \|\nabla P\|_{L_t^4L_x^\infty}
 \right),}
 \tag{1.4}
\]

where

\[
 R(t)=\sum_\alpha\|P T_\alpha\omega(t)\|_2^2.
 \tag{1.5}
\]

The result closes the harmonic-analysis reconstruction step.  It does
**not** prove that a Navier--Stokes covariance principal projector satisfies
the assumptions in (1.4).  The remaining hard gate is to propagate, without
circular use of the target critical norm,

\[
 R\in L_t^2,
 \qquad
 \lambda_1-\lambda_2\geq\gamma\operatorname{tr}Q,
 \qquad
 \frac{|\nabla Q|}{\operatorname{tr}Q}
   \in L_t^4L_x^\infty
 \quad\hbox{or stronger}.
 \tag{1.6}
\]

R0.70P is therefore a genuine conditional bridge, not a regularity proof and
not a solution of the Navier--Stokes Millennium problem.  No DNS or DGX run
is justified before the propagation gate in (1.6) has its own non-circular
ledger.

## 2. Explicit complete scalar frame

The theorem is deliberately stated for one fixed smooth frame, not for an
arbitrary collection of multipliers.

Choose a real, even, radial, smooth annular function
\(\eta\in C_c^\infty(\mathbb R^3\setminus\{0\})\) such that

\[
 \operatorname{supp}\eta
 \subset\{\tfrac12<|\xi|<2\},
 \qquad
 \sum_{j\in\mathbb Z}|\eta(2^{-j}\xi)|^2>0
 \quad(\xi\neq0).
 \tag{2.1}
\]

Define

\[
 d(\xi)=
 \left(\sum_{j\in\mathbb Z}|\eta(2^{-j}\xi)|^2\right)^{1/2},
 \qquad
 \varphi(\xi)=\frac{\eta(\xi)}{d(\xi)}.
 \tag{2.2}
\]

The sum has uniformly finite overlap, \(d(2^k\xi)=d(\xi)\), and

\[
 \sum_{j\in\mathbb Z}|\varphi(2^{-j}\xi)|^2=1
 \qquad(\xi\neq0).
 \tag{2.3}
\]

Let

\[
 T_j=\varphi(2^{-j}D).
 \tag{2.4}
\]

All torus norms below use normalized Haar measure.  On \(\mathbb R^3\),
the frame is homogeneous and is first defined on
Schwartz functions with Fourier support away from zero.  On
\(\mathbb T^3=(\mathbb R/2\pi\mathbb Z)^3\), the annular blocks act on
nonzero Fourier modes.  Adjoin the exact constant-mode projector

\[
 T_\star=\Pi_0,
 \qquad
 \Pi_0f=\int_{\mathbb T^3}f(x)\,dx.
 \tag{2.5a}
\]

Write \(\mathcal I_{\mathbb R}=\mathbb Z\) and
\(\mathcal I_{\mathbb T}=\{\star\}\cup\mathbb Z\).  Parseval gives

\[
 \sum_{\alpha\in\mathcal I_{\mathbb D}}\|T_\alpha f\|_2^2=\|f\|_2^2.
 \tag{2.5}
\]

More generally, the arguments below only use an explicit complete smooth
frame with

 \[
 a_0\|f\|_2^2
 \leq\sum_\alpha\|T_\alpha f\|_2^2
 \leq a_1\|f\|_2^2,
 \tag{2.6}
\]

finite annular overlap and uniform symbol seminorms for the nonzero-mode
blocks, together with the isolated \(\Pi_0\) block on the torus.  A bare lower-frame
inequality without these symbol conditions is insufficient for the
commutator theorem.

For vorticity \(\omega\in L^2\), put

\[
 \Omega_\alpha=T_\alpha\omega,
 \qquad
 Q(x,t)=\sum_\alpha\Omega_\alpha(x,t)\otimes\Omega_\alpha(x,t).
 \tag{2.7}
\]

On the torus \(\Pi_0\omega=0\), so the adjoined block contributes neither
to \(Q\) nor to the residual below.  It is nevertheless indispensable when
the lower frame is applied to \(P\omega\), whose mean need not vanish.

By Tonelli and (2.6), the nonnegative series
\(\sum_\alpha|\Omega_\alpha(x,t)|^2\) is finite for almost every \(x\), so \(Q\) is
well defined almost everywhere.  If \(L(x,t)\) is a rank-one orthogonal
projector and \(P=I-L\), define

 \[
 R(t)=\int_{\mathbb D}\operatorname{tr}(P Q)\,dx
 =\sum_\alpha\|P T_\alpha\omega\|_2^2,
 \tag{2.8}
\]

where \(\mathbb D\) is \(\mathbb R^3\) or \(\mathbb T^3\).

## 3. The exact frame--commutator bridge

### Theorem 3.1 — Abstract variable-projector bridge

Let \(\{T_\alpha\}\) satisfy the lower frame in (2.6), let \(P(x)\) be an
orthogonal projector, and let

\[
 \mathcal C(f,P)=\sum_\alpha\|[T_\alpha,P]f\|_2^2,
 \qquad
 [T_\alpha,P]=T_\alpha P-PT_\alpha.
 \tag{3.1}
\]

Then

\[
 \boxed{
 \sqrt{a_0}\|Pf\|_2
 \leq R_P(f)^{1/2}+\mathcal C(f,P)^{1/2},}
 \tag{3.2}
\]

where

\[
 R_P(f)=\sum_\alpha\|P T_\alpha f\|_2^2.
 \tag{3.3}
\]

#### Proof

For each \(\alpha\),

\[
 T_\alpha(Pf)=P T_\alpha f+[T_\alpha,P]f.
 \tag{3.4}
\]

Apply the lower frame to \(Pf\), then use the triangle inequality in the
Hilbert space \(\ell^2_\alpha(L_x^2)\):

\[
 \sqrt{a_0}\|Pf\|_2
 \leq
 \left(\sum_\alpha\|T_\alpha(Pf)\|_2^2\right)^{1/2}
 \leq R_P(f)^{1/2}+\mathcal C(f,P)^{1/2}.
 \tag{3.5}
\]

No Navier--Stokes equation, spectral gap, or direction orientation is used.
The theorem is exact but has content only after \(\mathcal C\) is bounded by
quantities below the target regularity level.

### Corollary 3.2 — Time-critical form

If \(R,\mathcal C\in L^2(0,T)\), then

\[
 \boxed{
 \|P f\|_{L^4(0,T;L^2)}
 \leq a_0^{-1/2}
 \left(
  \|R\|_{L^2(0,T)}^{1/2}
  +\|\mathcal C\|_{L^2(0,T)}^{1/2}
 \right).}
 \tag{3.6}
\]

This follows by taking the \(L_t^4\) norm of (3.2) and observing that
\(\|R^{1/2}\|_{L_t^4}=\|R\|_{L_t^2}^{1/2}\).

## 4. The endpoint square commutator

### Theorem 4.1 — Energy-level square commutator on \(\mathbb R^3\)

Let \(T_j\) be the frame in Section 2.  If
\(A\in W^{1,\infty}(\mathbb R^3;\mathbb C^{m\times m})\), then

\[
 \boxed{
 \left(\sum_{j\in\mathbb Z}
  \|[T_j,A]f\|_2^2\right)^{1/2}
 \leq C_\varphi\|\nabla A\|_\infty
       \|f\|_{\dot H^{-1}(\mathbb R^3)}.}
 \tag{4.1}
\]

It is enough first to take \(f\in\mathcal S\) with Fourier support separated
from zero; the result then extends by density in \(\dot H^{-1}\).

### Theorem 4.2 — Zero-mean periodic version

For \(A\in W^{1,\infty}(\mathbb T^3;\mathbb C^{m\times m})\) and zero-mean
\(f\),

\[
 \boxed{
 \left(\sum_{\alpha\in\mathcal I_{\mathbb T}}
  \|[T_\alpha,A]f\|_2^2\right)^{1/2}
 \leq C_{\varphi,\mathbb T^3}\|\nabla A\|_\infty
       \|f\|_{\dot H^{-1}_\#(\mathbb T^3)}.}
 \tag{4.2}
\]

Here \(|D|^{-1}\) is defined on the nonzero Fourier modes.  The constant
depends on the fixed torus normalization and frame, not on \(A\), \(f\), or
the number of active scales.

### Proof of Theorems 4.1--4.2

The proof must be done with finite random sums before taking any limit.  Let
\(F\subset\mathbb Z\) be finite and let \(\varepsilon_j\in\{-1,1\}\) be
independent Rademacher signs.  Define

\[
 M_{\varepsilon,F}=\sum_{j\in F}\varepsilon_jT_j.
 \tag{4.3}
\]

Exact orthogonality of the signs gives

\[
 \mathbb E_\varepsilon
 \|[M_{\varepsilon,F},A]f\|_2^2
 =\sum_{j\in F}\|[T_j,A]f\|_2^2.
 \tag{4.4}
\]

The symbol

\[
 m_{\varepsilon,F}(\xi)
 =\sum_{j\in F}\varepsilon_j\varphi(2^{-j}\xi)
 \tag{4.5}
\]

satisfies, uniformly in \(F\) and \(\varepsilon\),

\[
 |\partial_\xi^\alpha m_{\varepsilon,F}(\xi)|
 \leq C_{\alpha,\varphi}|\xi|^{-|\alpha|}.
 \tag{4.6}
\]

This is where smooth annular support and finite overlap are used.  Let
\(\Lambda=|D|\), put \(g=\Lambda^{-1}f\), and note the exact operator
identity

\[
 [M_{\varepsilon,F},A]\Lambda
 =[M_{\varepsilon,F}\Lambda,A]
  +M_{\varepsilon,F}[A,\Lambda].
 \tag{4.7}
\]

The multiplier \(M_{\varepsilon,F}\Lambda\) has a uniformly bounded
homogeneous order-one symbol.  The scale-invariant first-order commutator
theorem gives

\[
 \|[M_{\varepsilon,F}\Lambda,A]g\|_2
 \leq C_\varphi\|\nabla A\|_\infty\|g\|_2,
 \tag{4.8}
\]

and the Calderón commutator for \(\Lambda\) gives

\[
 \|[A,\Lambda]g\|_2
 \leq C\|\nabla A\|_\infty\|g\|_2.
 \tag{4.9}
\]

Since \(M_{\varepsilon,F}\) is uniformly bounded on \(L^2\), (4.7)--(4.9)
imply

\[
 \|[M_{\varepsilon,F},A]f\|_2
 \leq C_\varphi\|\nabla A\|_\infty
       \|f\|_{\dot H^{-1}}.
 \tag{4.10}
\]

Insert this in (4.4) and let \(F\uparrow\mathbb Z\).  Monotone convergence
of the nonnegative partial square sums proves (4.1).

For \(\mathbb T^3\), the same randomization proof is first performed on
the annular nonzero-mode blocks.
The finite randomized symbols periodize to a uniformly bounded family of
order-zero toroidal multipliers, and their products with \(|D|\) form a
uniform first-order family.  The periodic first-order commutator estimate is
obtained by periodizing the Calderón kernel, or equivalently by applying the
order-one Coifman--Meyer theorem in finitely many coordinate charts of the
compact torus.  The zero Fourier mode is excluded before \(\Lambda^{-1}\) is
introduced.

The adjoined constant block is estimated separately.  Since \(\Pi_0f=0\),

\[
 [\Pi_0,A]f=\Pi_0(Af).
 \tag{4.10a}
\]

For each matrix component, homogeneous \(H^{-1}\)--\(H^1\) duality on the
normalized torus gives

\[
 \|\Pi_0(Af)\|_2
 \leq C_m\|f\|_{\dot H^{-1}_\#}
        \|\nabla A\|_{L^2}
 \leq C_m\|\nabla A\|_\infty
        \|f\|_{\dot H^{-1}_\#}.
 \tag{4.10b}
\]

Constants in \(A\) disappear because \(f\) has zero mean.  Combining
(4.10b) with the annular square estimate proves the full
\(\mathcal I_{\mathbb T}\)-sum in (4.2).  This zero-mode step is necessary:
although vorticity has zero mean, \(P\omega\) generally does not.

The published analytic inputs are A. P. Calderón,
“Commutators of Singular Integral Operators,” *PNAS* 53 (1965), 1092--1099,
[DOI 10.1073/pnas.53.5.1092](https://doi.org/10.1073/pnas.53.5.1092), and
R. R. Coifman--Y. Meyer, “Commutateurs d'intégrales singulières et opérateurs
multilinéaires,” *Annales de l'Institut Fourier* 28 (1978), 177--202,
[DOI 10.5802/aif.708](https://doi.org/10.5802/aif.708).  Coifman--Meyer's
Theorem 2 on pp. 179--180 gives the order-one commutator estimate with the
constant controlled by the symbol bounds; the introduction on pp. 177--178
states the compact-manifold version, and Section 5 supplies the Lipschitz
endpoint.  For Euclidean truncations reaching arbitrarily low homogeneous
scales, first dilate the lowest active scale to unit size; the estimate is
scale invariant.  On the torus, nonzero lattice frequencies give a fixed
lowest active scale.  The square-function form (4.1) is the
finite-randomization consequence above; it is not quoted as a verbatim
theorem from either paper.

### Why a blockwise Taylor estimate is not a proof

On the Fourier side,

\[
 \widehat{[T_j,A]f}(n)
 =\sum_{k+q=n}
 \bigl(\varphi_j(n)-\varphi_j(k)\bigr)
 \widehat A(q)\widehat f(k).
 \tag{4.11}
\]

Low--high interactions expose the expected factor \(2^{-j}|q|\), but
high--high-to-low interactions can create a misleading logarithmic loss if
absolute values are summed coefficient by coefficient.  The first-order
commutator theorem in (4.8)--(4.9) supplies the cancellation on that resonant
set.  Replacing it by a generic zeroth-order Calderón--Zygmund estimate does
not prove (4.1).

## 5. Weight boundary and an explicit obstruction

### Corollary 5.1 — Bounded weights

If \(0\leq w_j\leq W<\infty\), then

\[
 \left(\sum_jw_j\|[T_j,A]f\|_2^2\right)^{1/2}
 \leq C_\varphi\sqrt W\|\nabla A\|_\infty
       \|f\|_{\dot H^{-1}}.
 \tag{5.1}
\]

Indeed, the weighted left side is at most \(\sqrt W\) times the unweighted
left side in Theorem 4.1 or 4.2.

### Proposition 5.2 — Arbitrary weights fail

There is no constant independent of an arbitrary nonnegative weight
sequence.  Choose \(\rho\) with
\(\frac{d}{dr}\varphi(re_1)|_{r=\rho}\neq0\), and choose integers
\(n_J\) such that \(2^{-J}n_J\to\rho\) as \(J\to\infty\).  On the
normalized torus set

\[
 A(x)=\cos x_1,
 \qquad
 f_J(x)=n_Je^{in_Jx_1}e_2.
 \tag{5.2}
\]

Then

\[
 \|\nabla A\|_\infty=1,
 \qquad
 \|f_J\|_{\dot H^{-1}_\#}=1.
 \tag{5.3}
\]

Direct Fourier calculation gives

\[
 \begin{aligned}
 [T_J,A]f_J
 =\frac{n_J}{2}\bigl(&
 [\varphi(2^{-J}(n_J+1)e_1)-\varphi(2^{-J}n_Je_1)]
       e^{i(n_J+1)x_1}\\
 &+[\varphi(2^{-J}(n_J-1)e_1)-\varphi(2^{-J}n_Je_1)]
       e^{i(n_J-1)x_1}\bigr)e_2,
 \end{aligned}
 \tag{5.4}
\]

and therefore

\[
 \|[T_J,A]f_J\|_2
 \longrightarrow
 \frac{\rho}{\sqrt2}
 \left|\frac{d}{dr}\varphi(re_1)\big|_{r=\rho}\right|>0.
 \tag{5.5}
\]

The weighted square sum is at least \(c\sqrt{w_J}\).  Taking
\(w_J\to\infty\) disproves a weight-independent estimate.  Thus R0.70P must
fix \(w_j=1\), or retain \(\sup_jw_j\) explicitly.  It cannot inherit
arbitrary weights merely because an abstract frame inequality happens to
hold.

## 6. The non-circular Navier--Stokes bridge

Let \(u\) be divergence free and let \(\omega=\nabla\times u\).  Write
\(u_*=u\) on \(\mathbb R^3\) and \(u_*=u-\bar u\) on \(\mathbb T^3\).  On
\(\mathbb R^3\),

\[
 \|\omega\|_{\dot H^{-1}}=\|u\|_2
 \tag{6.1}
\]

for the solenoidal Fourier modes.  On \(\mathbb T^3\),

\[
 \|\omega\|_{\dot H^{-1}_\#}=\|u_*\|_2.
 \tag{6.2}
\]

Taking \(A=P\) and \(f=\omega\) in Theorem 4.1 or 4.2 gives

\[
 \mathcal C(t)^{1/2}
 \leq C_{\mathcal T}\|\nabla P(t)\|_\infty
       \|u_*(t)\|_2.
 \tag{6.3}
\]

Combining (6.3) with Corollary 3.2 proves:

### Theorem 6.1 — Energy-level variable-projector reconstruction

If \(R\in L^2(0,T)\), \(u_*\in L^\infty(0,T;L^2)\), and
\(\nabla P\in L^4(0,T;L^\infty)\), then

\[
 \boxed{
 \|P\omega\|_{L^4(0,T;L^2)}
 \leq a_0^{-1/2}
 \left[
  \|R\|_{L^2(0,T)}^{1/2}
  +C_{\mathcal T}\|u_*\|_{L^\infty(0,T;L^2)}
       \|\nabla P\|_{L^4(0,T;L^\infty)}
 \right].}
 \tag{6.4}
\]

For an unforced Navier--Stokes solution, the energy inequality bounds the
velocity factor by \(\|u_*(0)\|_2\).  No \(L^2\) vorticity norm occurs on the
right side.  This is the precise sense in which the commutator is reduced to
the energy level.

The theorem would become circular if (6.3) were replaced by
\(\|\nabla P\|_\infty\|\omega\|_2\), because the time estimate would then
ask for the very vorticity regularity being reconstructed.

## 7. Spectral geometry enters only through \(\nabla P\)

Suppose the pointwise covariance \(Q\) in (2.7) is weakly differentiable in
space and has eigenvalues
\(\lambda_1\geq\lambda_2\geq\lambda_3\geq0\), with

\[
 E=\operatorname{tr}Q>0,
 \qquad
 \lambda_1-\lambda_2\geq\gamma E,
 \qquad \gamma>0.
 \tag{7.1}
\]

Let \(L\) be the principal rank-one spectral projector and \(P=I-L\).
The exact projector perturbation formula from R0.70O gives

\[
 |\partial_iP|_F
 \leq\frac{|\partial_iQ|_F}{\lambda_1-\lambda_2}
 \leq\gamma^{-1}\frac{|\partial_iQ|_F}{E}.
 \tag{7.2}
\]

Define

\[
 G(t)=\operatorname*{ess\,sup}_{x:E(x,t)>0}
       \frac{|\nabla Q(x,t)|_F}{E(x,t)}.
 \tag{7.3}
\]

Then Theorem 6.1 yields

\[
 \boxed{
 \|P\omega\|_{L^4(0,T;L^2)}
 \leq a_0^{-1/2}
 \left[
  \|R\|_{L^2(0,T)}^{1/2}
  +C_{\mathcal T}\gamma^{-1}
       \|u_*(0)\|_2\|G\|_{L^4(0,T)}
 \right].}
 \tag{7.4}
\]

In the near-line branch of R0.70O,

\[
 \frac{\lambda_2+\lambda_3}{E}\leq\eta<\frac12
 \quad\Longrightarrow\quad
 \gamma=1-2\eta.
 \tag{7.5}
\]

The spectral gap therefore supplies a stable algebraic denominator.  It does
not supply \(G\), nor does a small normalized ratio imply the absolute
condition \(R\in L_t^2\).

At zeros of \(E\), the principal projector is not uniquely determined.  A usable
continuation theorem must either work on a region where \(E>0\), prescribe a
measurable projector extension with the stated Sobolev bound, or prove a
zero-set lemma from the covariance PDE.  A spectral gap alone does not solve
this issue.

## 8. Periodic projector form of the Miller consumer

### Theorem 8.1 — Orientation-free periodic continuation criterion

Let \(\nu>0\), and let

\[
 u\in C([0,T_{\max});H^1_\sigma(\mathbb T^3))
 \cap L^2_{\mathrm{loc}}([0,T_{\max});H^2(\mathbb T^3))
 \tag{8.1}
\]

be the maximal unforced periodic mild/strong Navier--Stokes solution.  Put

\[
 \omega=\nabla\times u,
 \qquad
 S=\frac12(\nabla u+\nabla u^{\mathsf T}).
 \tag{8.2}
\]

Let \(L(x,t)\) be jointly measurable and satisfy almost everywhere

\[
 L=L^{\mathsf T},
 \qquad L^2=L,
 \qquad\operatorname{tr}L=1,
 \tag{8.3}
\]

and put \(P=I-L\).  If \(T_{\max}<\infty\) and

\[
 M:=\operatorname*{ess\,sup}_{0<t<T_{\max}}
       \|\nabla_xL(t)\|_{L^\infty}<\infty,
 \tag{8.4}
\]

\[
 P\omega\in L^4(0,T_{\max};L^2),
 \tag{8.5}
\]

then \(u\) extends past \(T_{\max}\).

The endpoint-uniform condition (8.4) is essential to this statement.
Merely assuming \(L\in L^\infty_{\mathrm{loc}}([0,T_{\max});W^{1,\infty})\)
allows \(\|\nabla L(t)\|_\infty\to\infty\) as
\(t\uparrow T_{\max}\) and does not close the proof.  Miller's published
whole-space theorem assumes
\(\nabla_xv\in L^\infty_{\mathrm{loc}}([0,\infty);L^\infty_x)\), which is
uniform on every finite candidate interval.

### Proof

The spatial mean \(\bar u(t)=\bar u_0\) is conserved.  Let
\(\widetilde u=u-\bar u_0\).  Then \(S\) and \(\omega\) are unchanged, and

\[
 \frac12\|\widetilde u(t)\|_2^2
 +\nu\int_0^t\|\nabla u(s)\|_2^2\,ds
 =\frac12\|\widetilde u_0\|_2^2.
 \tag{8.6}
\]

Define

\[
 Z_L(t)=\int_{\mathbb T^3}\operatorname{tr}(L S^2)\,dx.
 \tag{8.7}
\]

Let \(B_{ij}=\partial_i u_j\).  The pointwise algebraic identity is

\[
 \boxed{
 \operatorname{tr}(LS^2)-\frac14|P\omega|^2
 =B_{ij}B_{ki}L_{jk}.}
 \tag{8.8}
\]

Locally writing \(L=v\otimes v\) verifies (8.8) from

\[
 |Sv|^2-\frac14|v\times\omega|^2
 =(Bv)\cdot(B^{\mathsf T}v).
 \tag{8.9}
\]

Both sides of (8.8) depend only on \(L\), so no global orientation of the
line field is used.  Periodic integration by parts and
\(\partial_i u_i=0\) give

\[
 \int_{\mathbb T^3}B_{ij}B_{ki}L_{jk}\,dx
 =-\int_{\mathbb T^3}
   \widetilde u_j\,\partial_k u_i\,\partial_iL_{jk}\,dx.
 \tag{8.10}
\]

Consequently,

\[
 Z_L(t)
 \leq\frac14\|P\omega(t)\|_2^2
 +C\|\widetilde u(t)\|_2
     \|\nabla u(t)\|_2\|\nabla L(t)\|_\infty.
 \tag{8.11}
\]

Squaring, integrating, and using (8.4)--(8.6) yields

\[
 \int_0^{T_{\max}}Z_L(t)^2\,dt
 \leq
 \frac18\int_0^{T_{\max}}\|P\omega(t)\|_2^4\,dt
 +C_\nu\|\widetilde u_0\|_2^4M^2<\infty.
 \tag{8.12}
\]

Let \(\mu_1\leq\mu_2\leq\mu_3\) be the eigenvalues of the trace-free
symmetric matrix \(S\).  Since
\(|\mu_2|=\min_i|\mu_i|\), every rank-one projector satisfies

\[
 (\mu_2^+)^2\leq\operatorname{tr}(LS^2).
 \tag{8.13}
\]

Thus \(\mu_2^+\in L^4(0,T_{\max};L^2)\).  For completeness, the periodic
strain identity is

\[
 \frac{d}{dt}\|S\|_2^2
 +2\nu\|\nabla S\|_2^2
 =-4\int_{\mathbb T^3}\det S\,dx.
 \tag{8.14}
\]

The pointwise determinant bound

\[
 -\det S\leq\frac12\mu_2^+|S|^2
 \tag{8.15}
\]

and the zero-mean periodic Gagliardo--Nirenberg inequality

\[
 \|S\|_4^2
 \leq C_{\mathbb T^3}\|S\|_2^{1/2}
       \|\nabla S\|_2^{3/2}
 \tag{8.16}
\]

give, by Young's inequality,

\[
 \frac{d}{dt}\|S\|_2^2
 \leq C_{\mathbb T^3}\nu^{-3}
       \|\mu_2^+(t)\|_2^4\|S(t)\|_2^2.
 \tag{8.17}
\]

Gronwall and (8.12)--(8.13) imply

\[
 \sup_{t<T_{\max}}\|S(t)\|_2<\infty.
 \tag{8.18}
\]

Finally,

\[
 \|\nabla u\|_2^2=2\|S\|_2^2
 \tag{8.19}
\]

for periodic divergence-free fields.  Together with the conserved mean,
(8.18) bounds \(\|u(t)\|_{H^1}\) up to \(T_{\max}\), contradicting the
periodic \(H^1\) blow-up alternative.  This proves the extension.

The proof is the projector rewriting of the mechanism in Evan Miller,
“A Locally Anisotropic Regularity Criterion for the Navier--Stokes Equation
in Terms of Vorticity,” *Proc. Amer. Math. Soc. Ser. B* 8 (2021), 60--74,
[DOI 10.1090/bproc/74](https://doi.org/10.1090/bproc/74).  Miller's Theorem
1.6 is on \(\mathbb R^3\) and uses a unit vector.  The strain criterion used
in (8.13)--(8.17) is developed in Evan Miller, “A Regularity Criterion for
the Navier--Stokes Equation Involving Only the Middle Eigenvalue of the
Strain Tensor,” *Arch. Rational Mech. Anal.* 235 (2020),
[DOI 10.1007/s00205-019-01419-z](https://doi.org/10.1007/s00205-019-01419-z);
that paper explicitly notes that the argument applies equally on the torus,
with domain-dependent constants.

## 9. Combined conditional continuation theorem

### Theorem 9.1 — Complete-frame covariance criterion on \(\mathbb T^3\)

Let \(u\) be as in Theorem 8.1 and use the explicit complete frame from
Section 2.  Suppose \(T_{\max}<\infty\).  Define \(Q\) by (2.7), and suppose that there is a jointly
measurable rank-one principal eigendirection selection \(L\), with a legal
extension across non-simple points and with \(P=I-L\),
such that

\[
 R(t)=\int_{\mathbb T^3}\operatorname{tr}(P Q)\,dx
 \in L^2(0,T_{\max}),
 \tag{9.1}
\]

\[
 \operatorname*{ess\,sup}_{0<t<T_{\max}}
 \|\nabla P(t)\|_\infty<\infty.
 \tag{9.2}
\]

Then \(u\) extends past \(T_{\max}\).

#### Proof

The energy equality and Theorems 4.2 and 6.1 imply

\[
 P\omega\in L^4(0,T_{\max};L^2).
 \tag{9.3}
\]

Condition (9.2) is stronger than the \(L_t^4\) assumption needed for the
bridge and is exactly the endpoint-uniform spatial regularity required by
Theorem 8.1.  Apply that theorem.

Theorem 9.1 is logically valid but not yet an a priori Navier--Stokes
regularity criterion: its two hypotheses are properties of a solution-
dependent covariance projector and have not been derived from initial data
or a subcritical spacetime norm.  In particular, merely naming
\(R\) and \(\nabla P\) does not close the Millennium problem.

## 10. Spatial averaging windows add a separate defect

If the covariance is spatially averaged on
\(\mathbb D\in\{\mathbb R^3,\mathbb T^3\}\),

\[
 Q_K(x)=\sum_j\int K_j(x-y)
       \Omega_j(y)\otimes\Omega_j(y)\,dy,
 \tag{10.1}
\]

write

\[
 R_K(t)=\int_{\mathbb D}\operatorname{tr}(P(x)Q_K(x))\,dx.
 \tag{10.1a}
\]

In general, \(R_K\) is not equal to
\(\sum_j\|P\Omega_j\|_2^2\).  One must retain

\[
 D(t)=\sum_j\iint K_j(x-y)
 |(P(x)-P(y))\Omega_j(y)|^2\,dx\,dy.
 \tag{10.2}
\]

Assume each \(K_j\) is nonnegative and normalized on the chosen domain.  On
the torus, convolution is periodic and \(|z|\) below denotes geodesic
distance represented in a fixed fundamental cell.  Then

\[
 \sum_j\|P\Omega_j\|_2^2\leq2R_K+2D.
 \tag{10.3}
\]

If the kernel moments match the dyadic scales,

\[
 \int|z|^2K_j(z)\,dz\lesssim2^{-2j},
 \tag{10.4}
\]

then

\[
 D(t)\lesssim\|\nabla P(t)\|_\infty^2
 \sum_j2^{-2j}\|\Omega_j(t)\|_2^2
 \lesssim\|\nabla P(t)\|_\infty^2\|u_*(t)\|_2^2.
 \tag{10.5}
\]

R0.70P uses the same-point covariance (2.7), so \(D=0\).  Formula
(10.2) is recorded to prevent a later local-window model from silently
identifying \(P(x)\) with \(P(y)\).

## 11. Remaining Navier--Stokes propagation gate

The following items are not supplied by harmonic analysis:

1. \(R\in L_t^2\) for the solution-selected principal projector;
2. persistence of a near-line gap
   \(\lambda_1-\lambda_2\geq\gamma E\);
3. non-circular control of \(G=|\nabla Q|/E\);
4. a legal extension of the projector across \(E=0\);
5. endpoint-uniform, not merely pre-endpoint-local, control of
   \(\|\nabla P(t)\|_\infty\);
6. the window defect (10.2), if spatial averaging is introduced.

The next analytic ledger should derive the evolution of the pointwise frame
covariance from

\[
 \partial_t\omega+(u\cdot\nabla)\omega
 -\nu\Delta\omega=(\omega\cdot\nabla)u,
 \tag{11.1}
\]

including all filter commutators with transport, stretching, and diffusion.
It must then test whether \(R\), the gap, and \(G\) can be propagated using
energy-level or otherwise genuinely weaker data.

The route stops if every estimate for \(G\) requires
\(\|\omega\|_{L_t^4L_x^2}\), \(\|\nabla\omega\|_\infty\), or an equivalent
regularity norm.  Such an estimate would only rewrite the desired conclusion
as a hypothesis.

## 12. Claim boundary and reproducibility

What is proved in R0.70P:

- the exact frame--commutator bridge (Theorem 3.1);
- the negative-one-order square commutator for a fixed standard smooth
  complete LP frame (Theorems 4.1--4.2), conditional only on the cited
  classical first-order commutator theorem;
- the bounded-weight extension and explicit arbitrary-weight obstruction;
- the non-circular energy-level vorticity bridge (Theorem 6.1);
- the orientation-free periodic projector continuation theorem
  (Theorem 8.1);
- the combined conditional criterion (Theorem 9.1).

What is not proved:

- propagation of \(R\), the spectral gap, or \(G\) by Navier--Stokes;
- a criterion stated purely in initial data or a known subcritical norm;
- a fixed-positive-delay analogue of the R0.70O obstruction;
- regularity of arbitrary Leray--Hopf solutions;
- global regularity or finite-time singularity for three-dimensional
  Navier--Stokes.

The exact producer in `research/r070p_exact_audit.py` checks the finite
algebraic identities, the projector identity, representative periodic
integration by parts, the finite Rademacher identity, and the explicit weight
scaling.  It does not numerically prove the Calderón--Coifman--Meyer theorem
or the PDE continuation argument.  Those parts are analytic and are audited
separately in:

- `research/r070p_commutator_audit.md`;
- `research/r070p_projector_miller_audit.md`;
- `research/r070p_literature_audit.md`.

The archived payload, command, environment, and hashes are in
[`research/certificates/r070p/`](certificates/r070p/).

No public-page update or GitHub publication is authorized by this report.
