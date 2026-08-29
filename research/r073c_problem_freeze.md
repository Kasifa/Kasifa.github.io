# R0.73C problem freeze: large-coupling transient growth at the collision profile

**Date:** 2026-08-30  
**Status:** result freeze after analytic and interval proof; public release
still requires the formal certificate, independent arithmetic recomputation,
figure, PDF, and publication gates.

## 0. Why the next question must be refrozen

R0.73B proved the complete physical-kinetic estimate

\[
 \|U(d,s)\|_{L^2_\sigma\to L^2_\sigma}
 \le \exp\!\left(\frac{|\Lambda|}{2}K(s,d)\right)
 \le e^{5|\Lambda|e^{-s}/16},
 \tag{0.1}
\]

and the exact lift-up row gives a lower bound of order \(|\Lambda|\).
Those two facts do not determine the sharp large-\(|\Lambda|\) law.  A
polynomial upper bound is only a candidate.  It must first survive the
frozen Rayleigh spectrum of the two-harmonic collision profile.

I therefore freeze R0.73C as a stability-boundary question, not as a request
to prove a polynomial estimate chosen in advance.

## 1. Exact row and norm

Use the two-dimensional row

\[
 \beta=\xi=0,\qquad \mu=\gamma^2>0,
 \qquad \mathcal L_\mu=-\partial_x^2+\mu,
 \tag{1.1}
\]

with

\[
 W(d,x)=-\frac12e^{-d}\sin x+\frac14e^{-4d}\sin2x.
 \tag{1.2}
\]

The exact Orr--Sommerfeld equation is

\[
 q_d=-\mathcal L_\mu q
 -i\gamma\Lambda\left(
 Wq+W_{xx}\mathcal L_\mu^{-1}q\right).
 \tag{1.3}
\]

Equivalently,

\[
 q_d=\bigl(\Lambda A_\gamma(d)-\mathcal L_\mu\bigr)q,
 \qquad
 A_\gamma(d)=-i\gamma\left(
 W(d)+W_{xx}(d)\mathcal L_\mu^{-1}\right).
 \tag{1.4}
\]

The physical OS kinetic norm is

\[
 \|q\|_{\mathcal K_\mu}^2
 =\mu^{-1}\|\mathcal L_\mu^{-1/2}q\|_2^2.
 \tag{1.5}
\]

For fixed \(\gamma>0\), (1.5) is equivalent to the ordinary row norms.
No equivalence constant may be used uniformly as \(\gamma\downarrow0\).

For a fixed small observation window \(d_*>0\), define

\[
 G_\gamma(\Lambda;d_*)
 =\sup_{0\le d\le d_*}
 \|U_{\gamma,\Lambda}(d,0)\|_{\mathcal K_\mu\to\mathcal K_\mu}.
 \tag{1.6}
\]

The sign of \(\Lambda\) is related by complex conjugation, so asymptotic
claims will be stated in \(|\Lambda|\).

## 2. Exact frozen neutral calculation

At the collision time,

\[
 W_0(x)=W(0,x)
 =-\frac12\sin x+\frac14\sin2x
 =-2\sin^3(x/2)\cos(x/2).
 \tag{2.1}
\]

Away from its zeros,

\[
 \frac{W_0''}{W_0}
 =-4+\frac{3}{1-\cos x}
 =-4+\frac{3}{2\sin^2(x/2)}.
 \tag{2.2}
\]

Let

\[
 H_0=-\partial_x^2+\frac{W_0''}{W_0},
 \qquad \phi_0(x)=\sin^3(x/2)\quad(0<x<2\pi),
 \tag{2.3}
\]

where \(\phi_0\) is extended periodically, equivalently as
\(|\sin(x/2)|^3\) at the joined cubic level.  This extension belongs to
\(C^2\cap H^2_{\rm per}\), although it is not \(C^3\).  Direct
differentiation gives the exact singular Sturm--Liouville identity

\[
 \boxed{H_0\phi_0=-\frac74\phi_0.}
 \tag{2.4}
\]

Thus the frozen Rayleigh equation has the explicit neutral mode

\[
 c_{\rm ph}=0,qquad
 \gamma_0=\frac{\sqrt7}{2},qquad
 \phi=\phi_0.
 \tag{2.5}
\]

The Pöschl--Teller transform also gives the complete Friedrichs spectrum

\[
 \sigma(H_0)=\left\{\frac{(n+3)^2-16}{4}:n=0,1,\ldots\right\},
 \tag{2.6}
\]

so \(-7/4\) is the unique negative threshold.  Equation (2.4) is an exact
fact.  It does **not** by itself prove
which side of \(\gamma_0\) contains an unstable eigenvalue, because the
coefficient (2.2) is singular at the cubic zero of \(W_0\).  Any use of a
regular Tollmien--Lin criterion must verify its hypotheses rather than cite
the neutral mode alone.

## 3. Certified instability row

At

\[
 \gamma_*=\frac12,\qquad \mu_*=\frac14,
 \tag{3.1}
\]

the periodic Rayleigh ODE for \(c=i\eta\) has a determinant-one monodromy
matrix \(M(\eta)\) with real trace.  Validated interval integration proves

\[
 \operatorname{tr}M(0.3407)-2<0,
 \qquad
 \operatorname{tr}M(0.3410)-2>0.
 \tag{3.2}
\]

Continuity therefore gives \(\eta_*\in(0.3407,0.3410)\) with a nonzero
periodic Rayleigh solution.  Since \(\sigma=-i\gamma c=\gamma\eta\),

\[
 \boxed{
 \gamma_*=\frac12,\qquad
 \exists\,\sigma_*\in(0.17035,0.17050):
 \quad \sigma_*\in\sigma_p(A_{1/2}(0)).}
 \tag{3.3}
\]

This is an infinite-dimensional periodic-ODE certificate, not a Fourier
cutoff extrapolation.  The finite value
\(0.170407976920434\ldots\) is retained only as an independent diagnostic.
Root uniqueness, algebraic simplicity, and instability of every
\(0<\gamma<\sqrt7/2\) remain OPEN.

## 4. Fast-time transfer gate

The inviscid eigenvalue in (3.3) is outside the imaginary essential spectrum
and hence isolated with finite multiplicity.  This fact alone is not enough
to transfer it through the singular viscous limit.  Rescale

\[
 \theta=|\Lambda|d.
 \tag{4.1}
\]

Then (1.4) becomes

\[
 \partial_\theta q
 =\operatorname{sgn}(\Lambda)A_{\gamma_*}
   (\theta/|\Lambda|)q
 -|\Lambda|^{-1}\mathcal L_{\mu_*}q.
 \tag{4.2}
\]

On a logarithmic fast interval

\[
 0\le\theta\le M\log|\Lambda|,
 \qquad
 0\le d\le M\frac{\log|\Lambda|}{|\Lambda|},
 \tag{4.3}
\]

the heat profile moves slowly, but
\(-|\Lambda|^{-1}\mathcal L_{\mu_*}\) remains an unbounded operator in the
physical kinetic space.  It may not be treated as a small bounded
perturbation.  The required transfer theorem must first establish for the
complete viscous generator: eigenvalue persistence, a uniform Riesz contour,
a complementary dichotomy, and graph-domain-compatible Kato transport.
Under precisely that package, the quantified conditional output is

\[
 \|U_{\gamma_*,\Lambda}(d_\Lambda,0)q_*\|_{\mathcal K_{\mu_*}}
 \ge C_M|\Lambda|^{M\sigma_*-o(1)}
 \|q_*\|_{\mathcal K_{\mu_*}},
 \tag{4.4}
\]

for a specified \(d_\Lambda\) in (4.3).  Formula (4.4) may not be inferred
from an instantaneous numerical abscissa.

If (4.4) holds for every fixed \(M\), then

\[
 \boxed{
 \forall p>0:\quad
 \limsup_{|\Lambda|\to\infty}
 \frac{G_{\gamma_*}(\Lambda;d_*)}{|\Lambda|^p}=\infty.}
 \tag{4.5}
\]

This would make every fixed-degree global polynomial upper bound false.
It would still fall short of a sharp fixed-window law
\(G=e^{\Theta(|\Lambda|)}\).

## 5. Decision ledger

| ID | Statement | Initial state | Required evidence |
|---|---|---|---|
| C1 | exact lift-up lower bound is linear in \(|\Lambda|\) | inherited CLOSED | R0.73B exact component solution |
| C2 | global complete-row upper is at most \(e^{5|\Lambda|/16}\) at \(s=0\) | inherited CLOSED | R0.73B kinetic identity |
| C3 | collision profile has the exact neutral mode and singular spectrum (2.4)--(2.6) | CLOSED | exact Sobolev-domain proof and Pöschl--Teller spectrum |
| C4 | \(\gamma=1/2\) has a frozen unstable Rayleigh eigenvalue in \((0.17035,0.17050)\) | CLOSED subject to formal source sealing | validated infinite-dimensional monodromy sign change plus independent arithmetic recomputation |
| C5 | frozen instability transfers through (4.2) on logarithmic fast time | OPEN | vanishing-viscosity eigenvalue/Riesz/dichotomy/domain package |
| C6 | every fixed-degree polynomial global upper is false | CONDITIONAL on C4--C5 | exact implication (4.4)--(4.5) |
| C7 | \(G=e^{\Theta(|\Lambda|)}\) on a fixed window | OPEN | adiabatic/dichotomy theorem and matching rate |
| C8 | spectrally stable projected class admits a polynomial bound | OPEN | a separately stated projection and uniform resolvent |
| C9 | complete OS--Squire \(A_2\) direct sum | OPEN | collision-scale pressure and Squire closure |
| C10 | nonlinear Navier--Stokes or Clay implication | OPEN | not supplied by this linear gate |

## 6. Falsification and certificate requirements

The first finite screen will compare at least:

- \(\gamma\in\{1/4,1/2,3/4,1,\sqrt7/2,3/2\}\);
- positive and negative \(\Lambda\);
- Fourier cutoffs and time steps with independent convergence checks;
- frozen eigenvalues, nonautonomous gains, exact lift-up, and the R0.73B
  exponential envelope;
- short-time windows \(d=M\log|\Lambda|/|\Lambda|\) and fixed windows.

Every plotted finite matrix must remain labelled finite dimensional.  A
formal spectral claim requires a separate tail enclosure; ordinary cutoff
convergence is not such an enclosure.

R0.73C can be marked complete only after the analytic result,
independent audit, deterministic certificate, formal figure package,
synchronized HTML/PDF, cumulative recap, literature boundary, bilingual
dictionary, and publication tests all pass.  Public counters do not move at
this source-freeze stage.
