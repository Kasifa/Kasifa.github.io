# R0.73I source note: fixed-window action no-go from the present inputs

**Date:** 2026-08-30  
**Parent inputs audited:** R0.73F moving dichotomy, R0.73G selected launch,
and R0.73H gain-normalized departure  
**Evidence class:** exact logical non-implication and finite-dimensional
counterexamples; source stage  
**Public status:** not released

## 1. Exact decision

The presently proved R0.73F--H inputs do **not** imply any of the following
at a fixed positive slow window \(D\):

1. that the inherited endpoint \(D\) is a canonical numerical constant;
2. that the launch \(\phi_\Lambda\) is canonically determined;
3. that
   \[
   \lim_{\Lambda\to\infty}
   \frac1\Lambda\log G_\Lambda(D)
   \tag{1.1}
   \]
   exists for every admissible choice of the inherited launch;
4. that a limit in (1.1), if it exists, equals an integral of instantaneous
   rightmost eigenvalues;
5. that removal of the leading exponential leaves a bounded prefactor;
6. that the lower dichotomy exponent \(rD\) is the sharp action;
7. that the gain-normalized seed in R0.73H can be replaced by a pure
   prescribed exponential seed.

This is a statement about the logical strength of the **current proved
inputs**.  It does not assert that the actual periodic Navier--Stokes row
lacks a simple rightmost branch, a matching fixed-window action, or a
bounded asymptotic prefactor.  Any of those properties may be true, but each
requires an additional theorem.

## 2. The endpoint inherited from R0.73F is shrinkable

R0.73F first chooses

\[
 0<b<\alpha<c<a,
 \qquad
 \nu=\min\{\alpha-b,c-\alpha\},
 \qquad
 K\ge1,
 \tag{2.1}
\]

and then says to choose \(d_0>0\) sufficiently small that

\[
 C_A d_0<\frac{\nu}{16K^2},
 \qquad C_A=\frac{49}{4},
 \tag{2.2}
\]

together with a further harmless shrinking condition.  No maximal choice
or canonical selection rule for \(d_0\) is part of the theorem.

The R0.73H certificate and the \(\gamma=1/2\) numerical-form transfer imply
the rigorous upper bound

\[
 d_0<\frac{\sqrt{19/180}}{392}<\frac1{450}.
 \tag{2.3}
\]

Hence R0.73H's endpoint

\[
 D=\min\{d_0,1/450\}
 \tag{2.4}
\]

is exactly \(D=d_0\).  Equation (2.3) is only an upper bound: it does not
select a positive value of \(d_0\).  If one admissible value is chosen, any
smaller positive value is also admissible.  Therefore a theorem whose
claimed action depends on this inherited \(D\) is not reproducible until a
specific endpoint is separately frozen.

## 3. The inherited launch is not canonical

R0.73G instructs the reader to choose an \(L^2\)-unit eigenvector
\(h_\varepsilon\) in the finite nonzero frozen top spectral block.  The
analytic record currently proves neither

- that the top Riesz projection has rank one;
- that its eigenvalue is simple;
- that the certified eigenvalue is the unique rightmost spectral point;
- nor a deterministic continuum rule for selecting a line when the block
  has dimension greater than one.

A phase convention would only select a representative after an eigenline
has been selected.  Phase does not change the norm \(G_\Lambda\), whereas
the choice of eigenline can.

The finite diagnostic's rule “largest real part, then largest imaginary
part, then phase anchor” is a binary64 matrix convention.  It is not a
continuum rank-one or selection theorem and cannot repair this gap.

R0.73F's every-vector lower bound is sufficient for the coarse lower law:
every unit vector in the top block grows at least at the declared
dichotomy rate.  That fact does not force all vectors in the block to have
the same sharp action.

## 4. Two-dimensional top-block counterexample: nonunique selected action

Let the active top space be \(\mathbb C^2\), let \(L=I\), and define

\[
 A(d)=
 \begin{pmatrix}
 a+\kappa d&0\\
 0&a-\kappa d
 \end{pmatrix},
 \qquad a>0,\quad\kappa>0.
 \tag{4.1}
\]

If a stable complement is desired, take the direct sum with the scalar
operator \(-1\).  Put

\[
 B_\varepsilon(d)=A(d)-\varepsilon I
 \tag{4.2}
\]

and consider the same fast-time scaling as in R0.73F,

\[
 u_\theta=B_\varepsilon(\varepsilon\theta)u,
 \qquad 0\le\theta\le D/\varepsilon.
 \tag{4.3}
\]

This family is normal and smooth, has common domain, obeys

\[
 \|A(d)-A(0)\|=\kappa d,
 \tag{4.4}
\]

and has a fixed two-dimensional top cluster separated from the optional
stable complement.  At \(d=0\), both \(e_1\) and \(e_2\) are normalized
eigenvectors with the same top eigenvalue \(a-\varepsilon\).  They are both
allowed by the inherited instruction “choose a normalized eigenvector in
the top block.”

The two exact endpoint gains are

\[
 G_{\varepsilon,+}(D)
 =
 \exp\left[
 \frac{aD+\frac12\kappa D^2}{\varepsilon}-D
 \right],
 \tag{4.5}
\]

and

\[
 G_{\varepsilon,-}(D)
 =
 \exp\left[
 \frac{aD-\frac12\kappa D^2}{\varepsilon}-D
 \right].
 \tag{4.6}
\]

Consequently,

\[
 \lim_{\varepsilon\downarrow0}
 \varepsilon\log G_{\varepsilon,\pm}(D)
 =aD\pm\frac12\kappa D^2.
 \tag{4.7}
\]

For a sufficiently small \(D\), the entire top block remains uniformly to
the right of any fixed rate below \(a-\kappa D\), so a coarse moving
dichotomy lower law coexists with both different sharp actions.

Now choose \(h_\varepsilon=e_1\) on one sequence of
\(\varepsilon\downarrow0\) and \(h_\varepsilon=e_2\) on an interlaced
sequence.  Both choices satisfy the stated frozen selection rule, but
\(\varepsilon\log G_\varepsilon(D)\) has the two distinct subsequential
limits in (4.7).  Thus the current noncanonical selection rule cannot imply
existence of “the” selected fixed-window action.

This counterexample does not model the detailed coefficients of the
periodic Navier--Stokes operator.  Its role is narrower and exact: it proves
that the abstract properties currently invoked from R0.73F--G are
insufficient for the claimed inference.

## 5. Jordan counterexample: an action limit does not control the prefactor

Again take the active space \(\mathbb C^2\), \(L=I\), and now define

\[
 A(d)=
 \begin{pmatrix}
 a&0\\
 d&a
 \end{pmatrix}.
 \tag{5.1}
\]

An optional stable direct summand \(-1\) may again be added.  Starting from
the frozen top eigenvector \(e_1\), the exact fast-time system is

\[
 \begin{aligned}
 x_\theta&=(a-\varepsilon)x,\\
 y_\theta&=\varepsilon\theta\,x+(a-\varepsilon)y,
 \end{aligned}
 \qquad
 x(0)=1,\quad y(0)=0.
 \tag{5.2}
\]

At \(\theta=D/\varepsilon\),

\[
 U_\varepsilon(D/\varepsilon,0)e_1
 =
 e^{aD/\varepsilon-D}
 \left(e_1+\frac{D^2}{2\varepsilon}e_2\right).
 \tag{5.3}
\]

Therefore

\[
 G_\varepsilon(D)
 =
 e^{aD/\varepsilon-D}
 \sqrt{1+\frac{D^4}{4\varepsilon^2}}
 \sim
 \frac{D^2}{2}\varepsilon^{-1}e^{-D}e^{aD/\varepsilon}.
 \tag{5.4}
\]

The logarithmic action exists:

\[
 \lim_{\varepsilon\downarrow0}
 \varepsilon\log G_\varepsilon(D)=aD,
 \tag{5.5}
\]

but the compensated gain

\[
 G_\varepsilon(D)e^{-aD/\varepsilon}
 \tag{5.6}
\]

grows like \(\varepsilon^{-1}\).  Hence an action limit alone does not
produce a two-sided constant-prefactor estimate.

The same example remains compatible with a coarse dichotomy at every
strictly smaller exponential rate \(r<a\).  Indeed, for
\(0\le s\le t\le D/\varepsilon\), its top-block transition matrix is

\[
 e^{(a-\varepsilon)(t-s)}
 \begin{pmatrix}
 1&0\\
 \frac{\varepsilon}{2}(t^2-s^2)&1
 \end{pmatrix}.
 \tag{5.7}
\]

Writing \(\tau=t-s\) gives

\[
 \frac{\varepsilon}{2}(t^2-s^2)
 =\frac{\varepsilon}{2}\tau(t+s)
 \le D\tau.
 \tag{5.8}
\]

For \(\varepsilon<(a-r)/2\), the norm of the inverse of (5.7) is bounded by

\[
 e^{-r\tau}
 (1+D\tau)e^{-(a-r)\tau/2}.
 \tag{5.9}
\]

The last factor has a finite supremum independent of \(\varepsilon,s,t\).
Thus a uniform inverse dichotomy at rate \(r\) coexists with the
\(\varepsilon^{-1}\) endpoint prefactor.  Polynomial factors are absorbed
by the positive exponential margin \(a-r\), and the R0.73F estimates do not
exclude them.

## 6. The lower dichotomy rate is not the sharp action

The issue already appears in one dimension.  For

\[
 A(d)=a,\qquad L=I,
 \tag{6.1}
\]

the exact gain is

\[
 G_\varepsilon(D)=e^{aD/\varepsilon-D}.
 \tag{6.2}
\]

Every \(r<a\) can serve as a valid coarse lower exponential rate after
adjusting a uniform prefactor, while the sharp action remains \(aD\).
Therefore the R0.73F number

\[
 r=\alpha+\eta
 \tag{6.3}
\]

is a proof-dependent dichotomy rate.  No present argument identifies
\(rD\) with the true selected action.

## 7. Consequence for prescribed seeds

Suppose a future theorem proves only

\[
 \frac1\Lambda\log G_\Lambda(D)\longrightarrow\mathcal A(D).
 \tag{7.1}
\]

This is equivalent to

\[
 G_\Lambda(D)=e^{\mathcal A(D)\Lambda+o(\Lambda)}.
 \tag{7.2}
\]

For the pure exponential seed

\[
 s_\Lambda=\delta e^{-\mathcal A(D)\Lambda},
 \tag{7.3}
\]

the effective linear endpoint amplitude in the R0.73H Taylor scheme is

\[
 s_\Lambda G_\Lambda(D)
 =\delta e^{o(\Lambda)}.
 \tag{7.4}
\]

Expression (7.4) need not remain uniformly small and need not remain
bounded away from zero.  The Jordan example makes it grow like
\(\delta\Lambda\).

The previously tempting lower-law seed

\[
 \delta e^{-rD\Lambda}
 \tag{7.5}
\]

is even less controlled.  R0.73F gives a positive lower bound for its
effective linear endpoint amplitude but no uniform upper bound.  In the
scalar example (6.1)--(6.2), that amplitude is

\[
 \delta e^{(a-r)D\Lambda-D},
 \tag{7.6}
\]

which is exponentially outside the fixed perturbative Taylor radius when
\(a>r\).

To replace the exact gain-normalized seed \(\delta/G_\Lambda(D)\) by the
pure seed in (7.3), one needs at least

\[
 0<c_D
 \le G_\Lambda(D)e^{-\mathcal A(D)\Lambda}
 \le C_D<\infty
 \tag{7.7}
\]

for all sufficiently large \(\Lambda\).  If instead the true asymptotic is

\[
 G_\Lambda(D)\asymp
 \Lambda^p e^{\mathcal A(D)\Lambda},
 \tag{7.8}
\]

then the matched prescribed seed must contain the compensating factor

\[
 \delta\Lambda^{-p}e^{-\mathcal A(D)\Lambda}.
 \tag{7.9}
\]

The R0.73G bound
\(\|\phi_\Lambda\|_{H^3}\lesssim\Lambda^2\) is a separate initial-vector
regularity cost.  It neither proves nor rules out the propagation prefactor
in (7.7)--(7.8).

## 8. Additional theorems that would remove the no-go

A fixed-window matching-action theorem for the actual periodic operator
would require, at minimum:

1. a separately frozen positive endpoint \(D_*\), not the shrinkable
   instruction “take \(d_0\) sufficiently small”;
2. a rank-one simple branch that is uniquely rightmost on
   \([0,D_*]\), or a canonical block-level replacement;
3. normalized left and right eigenvectors with a uniform condition-number
   bound;
4. a uniform viscous branch and an error strong enough to control the
   exponent, typically
   \[
   \lambda_\varepsilon(d)
   =\lambda_0(d)+O(\varepsilon)
   \quad\hbox{uniformly on }[0,D_*];
   \tag{8.1}
   \]
5. non-selfadjoint adiabatic tracking with the unbounded
   \(-\varepsilon L\) handled on its common domain, including control of the
   geometric transport factor;
6. a two-sided prefactor theorem if the goal is prescribed-seed nonlinear
   departure rather than only a logarithmic action.

The current norm-\(C^1\) instantaneous Riesz projection and moving
dynamical dichotomy do not by themselves supply items 2--6.  In particular,
the unbounded viscous term cannot be reclassified as a bounded
\(O(\varepsilon)\) perturbation.

## 9. Exact boundary of this source note

The diagonal and Jordan systems are counterexamples to an inference from a
set of abstract inputs.  They are not counterexamples to a theorem already
proved for the exact Navier--Stokes row, and they are not numerical evidence
about that row.

Accordingly, the correct source-stage conclusion is:

> The present R0.73F--H record proves a coarse fixed-window exponential
> sandwich and a gain-normalized nonlinear departure.  It does not yet
> determine a canonical fixed-window selected action or its prefactor.
> The actual operator may possess both; proving them remains an open
> R0.73I contract.

Nothing in this note implies fixed-background Lyapunov instability,
three-dimensional vortex-stretching closure, finite-time singularity, or a
resolution of the Clay problem.
