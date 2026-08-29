# R0.73A problem freeze: the physical long-wave OS variable and the hidden mean mode

**Frozen:** 2026-08-29

**Status:** source-stage only.  Nothing in this file is public, certified, or
counted as a closed section.  Candidate statements marked `TO_PROVE` must pass
an analytic derivation, a deterministic certificate, an independent audit,
and the release gate before their status can change.

## 1. Inherited operator and exact scope

R0.73A starts from the unforced Orr--Sommerfeld row proved in R0.72Y--Z,

\[
 q_d=-\mathcal L q-icB_\mu(d)q,
 \qquad
 B_\mu(d)=W(d)+W_{xx}(d)\mathcal L^{-1},
 \tag{1.1}
\]

\[
 \mathcal L=-\partial_x^2+\mu,
 \qquad
 W(d,x)=-\frac12e^{-d}\sin x+\frac14e^{-4d}\sin 2x.
 \tag{1.2}
\]

The first theorem candidate is restricted to the physical two-dimensional
long-wave family

\[
 \beta=0,\qquad \xi=0,\qquad \gamma\ne0,\qquad
 \mu=\gamma^2,\qquad c=\gamma\Lambda,
 \tag{1.3}
\]

with \(0<\mu\le1\).  It is not a theorem for arbitrary independent triples
\((\mu,c,\Lambda)\), not a Squire estimate, and not a Bloch direct sum.

Let

\[
 \Pi_0 f=\frac1{2\pi}\int_{0}^{2\pi}f(x)\,dx,
 \qquad Q_0=I-\Pi_0.
 \tag{1.4}
\]

The raw decomposition \(q=a+r\), \(a=\Pi_0q\), \(r=Q_0q\), is singular as
\(\mu\downarrow0\), because \(\mathcal L^{-1}a=a/\mu\).  The physical
renormalization is instead

\[
 h=\frac{\Pi_0q}{\mu}=\Pi_0(\mathcal L^{-1}q),
 \qquad r=Q_0q,
 \qquad q=\mu h+r.
 \tag{1.5}
\]

Thus \(h\) is the mean wall-normal velocity, not an artificial spectral
coefficient.

## 2. Exact cancellation to be certified

For every mean-zero \(r\), put \(s=\mathcal L^{-1}r\).  Since
\(r=-s_{xx}+\mu s\), periodic integration by parts gives

\[
 \boxed{
 \Pi_0\!\left(Wr+W_{xx}\mathcal L^{-1}r\right)
 =\mu\Pi_0\!\left(W\mathcal L^{-1}r\right).}
 \tag{2.1}
\]

Also

\[
 B_\mu(\mu h)=h(W_{xx}+\mu W),
 \qquad \Pi_0(W_{xx}+\mu W)=0.
 \tag{2.2}
\]

Consequently (1.1) is exactly equivalent to

\[
 \boxed{
 \begin{aligned}
 h_d&=-\mu h-ic\,\Pi_0\!\left(W\mathcal L^{-1}r\right),\\
 r_d&=-\mathcal Lr-icQ_0B_\mu r
      -ic\,h(W_{xx}+\mu W).
 \end{aligned}}
 \tag{2.3}
\]

No coefficient in (2.3) contains \(1/\mu\).  Equation (2.1), rather than a
rank-one projection onto \(W_{xx}\), is the candidate low-gap regularizer.

## 3. Candidate all-start transient theorem

Use the normalized \(L^2\) norm and define

\[
 \|(h,r)\|_{X_\mu}^2=|h|^2+\|r\|_2^2.
 \tag{3.1}
\]

For \(0<\mu\le1\), the elementary profile bounds are

\[
 \|W(d)\|_\infty
 \le \frac12e^{-d}+\frac14e^{-4d},
 \qquad
 \|W_{xx}(d)\|_\infty
 \le \frac12e^{-d}+e^{-4d}.
 \tag{3.2}
\]

The proposed logarithmic-norm majorant is

\[
 C_W(d)=\frac74e^{-d}+2e^{-4d},
 \tag{3.3}
\]

and

\[
 J(s,d)=\int_s^d C_W(\tau)\,d\tau
 =\frac74(e^{-s}-e^{-d})
  +\frac12(e^{-4s}-e^{-4d})
 \le\frac94e^{-s}.
 \tag{3.4}
\]

The theorem candidate is

\[
 \boxed{
 \|(h(d),r(d))\|_{X_\mu}
 \le
 \exp\!\left[-\mu(d-s)+|c|J(s,d)\right]
 \|(h(s),r(s))\|_{X_\mu}.}
 \tag{3.5}
\]

In particular, on the low-coupling class \(|c|\le4\),

\[
 \|(h(d),r(d))\|_{X_\mu}
 \le e^9e^{-\mu(d-s)}
 \|(h(s),r(s))\|_{X_\mu}.
 \tag{3.6}
\]

`renormalizedPhysicalLongWaveOSTransientPropagator=TO_PROVE`.

The norm in (3.1) is a hybrid mean-velocity/mean-zero-vorticity norm.  It is
not uniformly equivalent to raw \(L^2_q\) or to the complete kinetic-energy
norm as \(\mu\downarrow0\).  No such equivalence may be claimed.

## 4. Tangent mismatch to be proved

R0.72Z found the abstract mean-zero \(\mu=0\) solution

\[
 q_*(d)=W_{xx}(d),\qquad
 (-\partial_x^2)^{-1}q_*=-W.
 \tag{4.1}
\]

The physical lift of (2.3) retains the hidden variable \(h\).  If
\(r=W_{xx}\), \(h=0\), and
\(c=c_\mu=\gamma\Lambda_\mu\), then along a specified path with
\(c_\mu\to c_0\),

\[
 h_d
 \longrightarrow
 ic_0\,\Pi_0(W^2)
 =ic_0\left(\frac18e^{-2d}+\frac1{32}e^{-8d}\right).
 \tag{4.2}
\]

This limit is nonzero when \(c_0\ne0\), which requires
\(|\Lambda_\mu|\sim|c_0|/|\gamma|\).  If \(\Lambda\) is held fixed, then
\(c_\mu\to0\) and this instantaneous derivative tends to zero; that path is
not decided here.  For every fixed positive gap with \(c_\mu\ne0\), the
lifted line \(h=0\),
\(r\in\operatorname{span}\{W_{xx}(d)\}\) is not invariant.  A
\(W_{xx}\)-amplitude alone is therefore not a sufficient physical state
variable.

`rankOneAbstractTangentClosesPhysicalLongWaveLimit=TO_DISPROVE`, where
`closes` means an invariant lifted one-dimensional physical state.

This does not invalidate the exact abstract solution (4.1); it identifies a
singular-limit mismatch between two different phase spaces.

## 5. Frozen-time spectral audit required before publication

For the stationary two-dimensional periodic OS operator, the long-wave
expansion of Colombo--Dolce--Montalto--Ventura (arXiv:2509.18070) applies
after the identification

\[
 \nu_{\rm lit}=|\Lambda|^{-1},\qquad
 \varepsilon_{\rm lit}=|\gamma|,
 \qquad U_{\rm lit}=\operatorname{sgn}(\Lambda)W(d,\cdot),
 \tag{5.1}
\]

and multiplication of their generator by \(|\Lambda|\).  In the normalized
\(L^2\) convention,

\[
 H(d):=\|\partial_x^{-1}W(d)\|_2^2
 =\frac18e^{-2d}+\frac1{128}e^{-8d}.
 \tag{5.2}
\]

The leading frozen eigenvalue is therefore expected to satisfy

\[
 \operatorname{Re}\lambda_0(d)
 =c^2H(d)-\gamma^2
  +O_W\!\left(|c|^3+|c|\mu\right)
 \tag{5.3}
\]

under the source theorem's smallness condition
\(|c|\le\delta_0(\|W(d)\|_{C^2})\).  When \(|\Lambda|\ge1\), the remainder
reduces to \(O_W(|c|^3)\).  The source theorem gives instability when

\[
 |\Lambda|^2H(d)>1.
 \tag{5.4}
\]

This is a literature specialization, not a new theorem.  It prohibits any
claim that all frozen low-gap rows are spectrally stable.  It does not by
itself decide the nonautonomous propagator, because \(W\) evolves by heat.

## 6. Falsification gates

R0.73A stops or changes direction if any of the following occurs:

1. direct Fourier algebra contradicts (2.1)--(2.3);
2. the energy calculation cannot yield (3.5) with constants independent of
   \(\mu\in(0,1]\);
3. Galerkin truncations fail to converge under both mode and time-step
   refinement;
4. the literature theorem cannot be mapped to (1.1) with signs, time scale,
   and norm convention made explicit;
5. the claimed tangent mismatch disappears after the physical row and
   inverse-coordinate constraints are imposed;
6. an independent auditor finds an untracked payment in \(\Lambda\),
   \(\gamma\), \(\mu\), or the complete kinetic norm.

## 7. Publication boundary

Even if (2.3)--(3.6) close, the following remain open unless separately
proved:

- a scalar-\(A_2\)-rate low-gap OS estimate;
- a uniformly equivalent physical kinetic-energy propagator without
  \(|\Lambda|\) payment;
- Squire/lift-up transfer on the low-gap family;
- Bloch-uniform direct summation;
- nonlinear row convolution, vortex stretching, and the Clay problem.
