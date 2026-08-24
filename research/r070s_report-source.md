# R0.70S — An energy-level no-go for the near-rank palinstrophy majorant

**Status:** internal canonical candidate; not a public theorem chapter

**Release:** R0.70S

**Date:** 2026-08-25

## 1. Decision

R0.70R proved

\[
 (\mathcal K_Q-\mathcal D_P)_+
 \leq c_{r/E}\mathcal G,
 \qquad
 \mathcal G=\sum_{\alpha,k}|\partial_kT_\alpha\omega|^2.
 \tag{1.1}
\]

Thus \(c_{r/E}\mathcal G\) is the coefficient-level majorant for the possible
positive diffusion deficit; the residual equation carries the fixed factor
\(2\nu\).

R0.70S asks whether the energy-level quantities already isolated in R0.70Q
can control the spacetime integral of the right-side majorant in (1.1).

The answer is no.  For every fixed \(T>0\) and \(\nu>0\), there is a sequence of smooth
global periodic Navier--Stokes shear heat flows with a uniform pointwise
near-rank-one ratio such that

\[
 \|u_{N,*}(0)\|_2^2\longrightarrow0,
 \tag{1.2}
\]

\[
 \|R_N\|_{L^2(0,T)}
 +\|\mathfrak C_{P_N}\|_{L^2(0,T)}
 +\mathfrak W_{L_N}(0,T)
 \longrightarrow0,
 \tag{1.3}
\]

but

\[
 \boxed{
 \int_0^T\!\!\int_{\mathbb T^3}
 c_{r_N/E_N}\mathcal G_N\,dx\,dt
 \longrightarrow+\infty.}
 \tag{1.4}
\]

Consequently, no right-hand side that is locally bounded in the four inputs
in (1.2)--(1.3), together with a fixed upper bound for \(r/E\), can control
the R0.70R palinstrophy majorant.

This is a scale-separation no-go, not a singularity result.  The initial
enstrophy in the sequence diverges.  The theorem therefore does not exclude
an estimate depending on \(\|\omega_N(0)\|_2\), an initial \(H^1\) or higher
norm, a frequency moment, or another quantity that sees the rising
palinstrophy scale.

The route implication is:

1. a closure of this majorant using only kinetic energy, \(R\), the exact
   commutator square, the weighted direction cost, and a pointwise near-rank
   ratio is impossible;
2. any closure that remains locally bounded in scalar inputs must include
   information not confined to a compact set along the explicit sequence.
   An initial derivative-sensitive quantity such as enstrophy is one natural
   candidate;
3. a separate route may instead retain cancellation in the signed diffusion
   deficit.  The selected next route tests the enstrophy branch, but R0.70S
   neither proves it unique nor decides whether it closes.

No public-page update or GitHub publication is authorized by this report.

## 2. The fixed two-frequency base flow

Work on

\[
 \mathbb T^3=(\mathbb R/2\pi\mathbb Z)^3.
 \tag{2.1}
\]

All spatial integrals and norms below use normalized Haar measure.

Fix an integer

\[
 M=16
 \tag{2.2}
\]

and the transverse unit fields

\[
 v_n(x_1)
 =(0,\cos(nx_1),\sin(nx_1)),
 \tag{2.3}
\]

\[
 w_m(x_1)
 =(0,\sin(mx_1),\cos(mx_1)).
 \tag{2.4}
\]

For \(s\geq0\), define the base vorticity

\[
 \omega_1(x,s)
 =e^{-\nu s}v_1(x_1)
 +M^{-1}e^{-\nu M^2s}w_M(x_1).
 \tag{2.5}
\]

It is smooth, mean zero, divergence free, transverse to \(e_1\), and depends
only on \(x_1\).  Its Biot--Savart velocity

\[
 u_1=\nabla\times(-\Delta)^{-1}\omega_1
 \tag{2.6}
\]

is explicitly

\[
 u_1(x,s)
 =-e^{-\nu s}v_1(x_1)
  +M^{-2}e^{-\nu M^2s}w_M(x_1).
 \tag{2.7}
\]

It has the same shear geometry.  Hence

\[
 (u_1\cdot\nabla)u_1=0,
 \qquad
 \partial_su_1=\nu\Delta u_1.
 \tag{2.8}
\]

Thus \(u_1\) is a smooth global unforced Navier--Stokes solution.

Use the pinned complete periodic frame

\[
 \mathscr T=\{T_\star=\Pi_0\}\cup\{T_j:j\in\mathbb Z\},
 \qquad
 \widehat{T_jf}(k)=\varphi(2^{-j}k)\widehat f(k)
 \quad(k\ne0).
 \tag{2.9a}
\]

Here \(\varphi\) is real, even, radial, and smooth, with

\[
 \operatorname{supp}\varphi
 \subset\{\tfrac12<|\xi|<2\},
 \qquad
 \sum_{j\in\mathbb Z}|\varphi(2^{-j}\xi)|^2=1
 \quad(\xi\ne0).
 \tag{2.9b}
\]

For any mean-zero vorticity \(\omega\), write

\[
 \Omega_\alpha=T_\alpha\omega,
 \qquad
 Q[\omega]=\sum_{\alpha\in\{\star\}\cup\mathbb Z}
 \Omega_\alpha\otimes\Omega_\alpha.
 \tag{2.9c}
\]

At a simple top eigenvalue, \(L\) denotes its rank-one spectral projector,
\(P=I-L\), \(E=\operatorname{tr}Q\), and \(r=\operatorname{tr}(PQ)\).

The frequency \(1\) activates only \(T_0\), while \(M=16=2^4\) activates
only \(T_4\); exact tightness gives multiplier modulus one at each active
frequency, and real-evenness gives the same real scalar on the two signs.
The zero block vanishes because \(\omega_1\) is mean zero.
Thus the active index sets are disjoint, and the covariance contains no
cross-frequency block term:

\[
 \boxed{
 Q_1
 =a(s)^2v_1\otimes v_1
 +b(s)^2w_M\otimes w_M,}
 \tag{2.10}
\]

where

\[
 a(s)=e^{-\nu s},
 \qquad
 b(s)=M^{-1}e^{-\nu M^2s}.
 \tag{2.11}
\]

## 3. Gap, residual ratio, and positivity of the target

Let \(\theta(x,s)\) be the angle between \(v_1(x_1)\) and \(w_M(x_1)\).
The nonzero eigenvalues of (2.10) are

\[
 \lambda_{1,2}
 =\frac12
 \left[
  a^2+b^2
  \pm
  \sqrt{(a^2-b^2)^2+4a^2b^2\cos^2\theta}
 \right],
 \tag{3.1}
\]

and \(\lambda_3=0\).  Since

\[
 \frac{b(s)}{a(s)}
 =M^{-1}e^{-\nu(M^2-1)s}
 \leq\frac1M,
 \tag{3.2}
\]

the top eigenvalue is simple for every finite \(s\), with

\[
 \lambda_1-\lambda_2
 \geq a^2-b^2>0.
 \tag{3.3}
\]

Set

\[
 E_1=\operatorname{tr}Q_1=a^2+b^2,
 \qquad
 r_1=\lambda_2.
 \tag{3.4}
\]

The relative gap is uniform even though the absolute covariance decays:

\[
 \frac{\lambda_1-\lambda_2}{E_1}
 \geq\frac{a^2-b^2}{a^2+b^2}
 \geq\frac{M^2-1}{M^2+1}
 =\frac{255}{257}.
 \tag{3.5}
\]

Because \(\lambda_1\geq a^2\),

\[
 0\leq\eta_1:=\frac{r_1}{E_1}
 \leq\frac{b^2}{a^2+b^2}
 \leq\frac1{M^2+1}
 =\frac1{257}<\frac15.
 \tag{3.6}
\]

The R0.70R coefficient is

\[
 c_{\eta}
 =\frac{\sqrt\eta}
        {\sqrt{1-\eta}-\sqrt\eta}.
 \tag{3.7}
\]

It is increasing on \([0,1/2)\), so (3.6) yields

\[
 0\leq c_{\eta_1(x,s)}\leq c_{1/(M^2+1)}=\frac1{M-1}.
 \tag{3.8}
\]

For the base flow, tightness also gives the pointwise block-gradient density

\[
 \boxed{
 \mathcal G_1(s)
 =e^{-2\nu s}+e^{-2\nu M^2s}.}
 \tag{3.9}
\]

It is independent of \(x\).  At \((x_1,s)=(0,0)\), the two vectors in (2.10)
are orthogonal, so

\[
 \eta_1(0,0)=\frac1{M^2+1},
 \qquad
 c_{\eta_1(0,0)}=\frac1{M-1}>0.
 \tag{3.10}
\]

The gap in (3.3) makes \(\eta_1\) continuous.  Hence the nonnegative number

\[
 I_1(S)
 =\int_0^S\!\!\int_{\mathbb T^3}
 c_{\eta_1}\mathcal G_1\,dx\,ds
 \tag{3.11}
\]

is strictly positive for every \(S>0\).  It has a finite positive limit:

\[
 0<I_1(\infty)
 \leq
 \frac1{M-1}
 \left(
  \frac1{2\nu}+\frac1{2\nu M^2}
 \right)
 <\infty.
 \tag{3.12}
\]

The strict lower bound uses only continuity near \((0,0)\); no numerical
quadrature is involved.

## 4. Exact dyadic scaling of the frame

Let

\[
 N=2^J,
 \qquad J\in\mathbb N,
 \tag{4.1}
\]

and let

\[
 (\mathcal S_Nf)(x)=f(Nx)
 \tag{4.2}
\]

be the integer covering pullback on the torus.  Normalized Haar measure gives

\[
 \|\mathcal S_Nf\|_2=\|f\|_2.
 \tag{4.3}
\]

The dyadic multipliers obey the exact index-shift identity

\[
 \boxed{
 T_j\mathcal S_N
 =\mathcal S_NT_{j-J}.}
 \tag{4.4}
\]

For every spatial function \(f\), the constant block satisfies

\[
 \Pi_0(\mathcal S_Nf)=\Pi_0f.
 \tag{4.5}
\]

For amplitudes \(A_N>0\), define

\[
 \omega_N(x,t)
 =A_N\bigl(\mathcal S_N[\omega_1(\cdot,N^2t)]\bigr)(x).
 \tag{4.6}
\]

Its velocity is

\[
 u_N(x,t)
 =\frac{A_N}{N}
  \bigl(\mathcal S_N[u_1(\cdot,N^2t)]\bigr)(x).
 \tag{4.7}
\]

It is again a smooth global mean-zero shear heat solution, so
\(u_{N,*}=u_N\).  Equations (4.3)--(4.5)
give

\[
 Q_N(x,t)
 =A_N^2Q_1(Nx,N^2t),
 \tag{4.8}
\]

\[
 E_N(x,t)=A_N^2E_1(Nx,N^2t),
 \qquad
 r_N(x,t)=A_N^2r_1(Nx,N^2t),
 \qquad
 \eta_N(x,t)=\eta_1(Nx,N^2t),
 \tag{4.9}
\]

\[
 L_N(x,t)=L_1(Nx,N^2t),
 \qquad
 P_N(x,t)=P_1(Nx,N^2t),
 \tag{4.10}
\]

and

\[
 \mathcal G_N(x,t)
 =A_N^2N^2\mathcal G_1(N^2t).
 \tag{4.11}
\]

The pointwise ratio remains uniformly bounded by \(1/257\), and the relative
gap remains at least \(255/257\).

## 5. Scaling of the four proposed inputs

Define

\[
 R_N(t)=\int_{\mathbb T^3}r_N(x,t)\,dx
 \tag{5.1}
\]

and

\[
 \mathfrak C_{P_N}(t)
 =\sum_\alpha
  \|[T_\alpha,P_N]\omega_N(t)\|_2^2.
 \tag{5.2}
\]

The zero-mode commutator is included in the sum.  The covering pullback
preserves its spatial mean, while (4.4) shifts the annular indices.
Therefore

\[
 R_N(t)=A_N^2R_1(N^2t),
 \tag{5.3}
\]

\[
 \boxed{
 \mathfrak C_{P_N}(t)
 =A_N^2\mathfrak C_{P_1}(N^2t).}
 \tag{5.4}
\]

For every fixed \(T>0\),

\[
 \|R_N\|_{L^2(0,T)}
 =\frac{A_N^2}{N}
  \|R_1\|_{L^2(0,N^2T)},
 \tag{5.5}
\]

\[
 \|\mathfrak C_{P_N}\|_{L^2(0,T)}
 =\frac{A_N^2}{N}
  \|\mathfrak C_{P_1}\|_{L^2(0,N^2T)}.
 \tag{5.6}
\]

Both base functions belong to \(L^2(0,\infty)\).  For \(R_1\), this follows
from

\[
 0\leq R_1(s)\leq b(s)^2
 =M^{-2}e^{-2\nu M^2s}.
 \tag{5.7}
\]

For the exact commutator square, orthogonality of \(P_1\), the triangle
inequality, and complete-frame tightness give the direct bound

\[
 \begin{aligned}
 \mathfrak C_{P_1}(s)
 &\leq
 2\sum_\alpha\|T_\alpha(P_1\omega_1)\|_2^2
 +2\sum_\alpha\|P_1T_\alpha\omega_1\|_2^2\\
 &\leq4\|\omega_1(s)\|_2^2.
 \end{aligned}
 \tag{5.8}
\]

The right side decays exponentially.  This argument includes the constant
block and avoids replacing the exact commutator by a Lipschitz majorant.

The energy-weighted direction cost is

\[
 \mathfrak W_{L_N}(0,T)
 =\int_0^T
  \|u_{N,*}(t)\|_2^2
  \|\nabla u_N(t)\|_2^2
  \|\nabla L_N(t)\|_\infty^2\,dt.
 \tag{5.9}
\]

Since

\[
 \|u_{N,*}(t)\|_2^2
 =\frac{A_N^2}{N^2}\|u_1(N^2t)\|_2^2,
 \tag{5.10}
\]

\[
 \|\nabla u_N(t)\|_2^2
 =A_N^2\|\nabla u_1(N^2t)\|_2^2,
 \tag{5.11}
\]

\[
 \|\nabla L_N(t)\|_\infty^2
 =N^2\|\nabla L_1(N^2t)\|_\infty^2,
 \tag{5.12}
\]

one obtains

\[
 \boxed{
 \mathfrak W_{L_N}(0,T)
 =\frac{A_N^4}{N^2}
  \mathfrak W_{L_1}(0,N^2T).}
 \tag{5.13}
\]

Indeed, after removing the positive scalar \(a(s)^2\), the covariance is
\(v_1\otimes v_1+\varepsilon(s)^2w_M\otimes w_M\), where
\(0\leq\varepsilon\leq M^{-1}\).  Its gap is at least
\(1-\varepsilon^2\), while the norm of its spatial derivative is at most
\(2+2M\varepsilon^2\).  The spectral-projector derivative formula therefore
gives a uniform bound for \(\|\nabla L_1\|_\infty\).  The two velocity
factors decay exponentially, so the base cost over \((0,\infty)\) is finite.

Finally, the initial kinetic energy scales as

\[
 \boxed{
 \|u_{N,*}(0)\|_2^2
 =\frac{A_N^2}{N^2}\|u_1(0)\|_2^2.}
 \tag{5.14}
\]

## 6. Scaling of the palinstrophy majorant

Let

\[
 I_N(T)
 =\int_0^T\!\!\int_{\mathbb T^3}
 c_{\eta_N}\mathcal G_N\,dx\,dt.
 \tag{6.1}
\]

Equations (4.5), (4.9), and (4.11), followed by \(s=N^2t\), give the exact
identity

\[
 \boxed{
 I_N(T)=A_N^2I_1(N^2T).}
 \tag{6.2}
\]

This identity exposes the derivative mismatch.  The two powers of \(N\) in
\(\mathcal G_N\) cancel only the parabolic time change; they do not produce
the inverse \(N^2\) present in the kinetic energy.

## 7. Energy-level no-go theorem

### Theorem 7.1 — Vanishing structural inputs and divergent palinstrophy majorant

Fix \(T>0\), \(\nu>0\), \(\eta_0=1/257\), and the frame \(\mathscr T\) in
(2.9a)--(2.9c).  Set \(M=16\), take \(N=2^J\to\infty\), and choose

\[
 A_N=N^{1/4}.
 \tag{7.1}
\]

Then

\[
 \|u_{N,*}(0)\|_2^2
 =N^{-3/2}\|u_1(0)\|_2^2
 \longrightarrow0,
 \tag{7.2}
\]

\[
 \|R_N\|_{L^2(0,T)}
 \leq
 N^{-1/2}\|R_1\|_{L^2(0,\infty)}
 \longrightarrow0,
 \tag{7.3}
\]

\[
 \|\mathfrak C_{P_N}\|_{L^2(0,T)}
 \leq
 N^{-1/2}
 \|\mathfrak C_{P_1}\|_{L^2(0,\infty)}
 \longrightarrow0,
 \tag{7.4}
\]

and

\[
 \mathfrak W_{L_N}(0,T)
 \leq
 N^{-1}\mathfrak W_{L_1}(0,\infty)
 \longrightarrow0.
 \tag{7.5}
\]

On the other hand, (3.12) and (6.2) give

\[
 I_N(T)
 =N^{1/2}I_1(N^2T)
 \longrightarrow+\infty.
 \tag{7.6}
\]

All members of the sequence obey

\[
 0\leq\frac{r_N}{E_N}\leq\frac1{257}.
 \tag{7.7}
\]

Here \(E_N>0\) at every finite time, so the ratio is defined everywhere.

There is no function
\(F_{T,\nu,\eta_0,\mathscr T}:[0,\infty)^4\to[0,\infty)\) for which there
exist \(\delta,C>0\) satisfying

\[
 \sup_{z\in[0,\delta]^4}F_{T,\nu,\eta_0,\mathscr T}(z)\leq C
 \tag{7.8}
\]

and, for every dyadic \(N\) in the explicit shear family,

\[
 \begin{aligned}
 I_N(T)\leq F_{T,\nu,\eta_0,\mathscr T}\Big(
 &\|u_{N,*}(0)\|_2^2,
 \|R_N\|_{L^2(0,T)},
 \|\mathfrak C_{P_N}\|_{L^2(0,T)},\\
 &\mathfrak W_{L_N}(0,T)
 \Big)
 \end{aligned}
 \tag{7.9}
\]

Indeed, (7.2)--(7.5) eventually place the input in \([0,\delta]^4\), whereas
(7.6) exceeds \(C\).  Therefore
the same estimate is impossible on any smooth-solution class containing this
family and using only these four inputs plus the fixed parameters.

### Proof boundary

Every field used above is a global smooth solution with zero nonlinearity.
The contradiction in (7.9) is a high-frequency scaling contradiction, not a
blow-up mechanism.  It concerns the positive majorant \(c_\eta\mathcal G\);
it does not assert that the signed deficit \(\mathcal K_Q-\mathcal D_P\)
is large on this family.

The initial enstrophy is

\[
 \|\omega_N(0)\|_2^2
 =A_N^2\|\omega_1(0)\|_2^2
 =N^{1/2}\|\omega_1(0)\|_2^2
 \longrightarrow+\infty.
 \tag{7.10}
\]

Thus Theorem 7.1 does not exclude a bound whose right side depends on initial
\(H^1\), enstrophy, palinstrophy, a frequency moment,
or another derivative-sensitive datum.  Such a dependence is not
automatically circular: initial enstrophy is part of smooth initial data.
What would be circular is assuming its uniform-in-time continuation bound.

## 8. What remains

The R0.70Q conditional continuation theorem itself survives this test.  It
requires \(R,\mathfrak C_P\in L_t^2\) and finite \(\mathfrak W_L\); every
member of the present global family satisfies those conditions.  That
theorem never claimed to control \(I(T)\).

R0.70S instead closes one proposed producer route: the R0.70R palinstrophy
majorant cannot be bounded from the R0.70Q structural inputs at the kinetic
energy level.

The selected next target is an enstrophy-dependent structural inequality.
Starting from

\[
 \frac12\frac d{dt}\|\omega\|_2^2
 +\nu\|\nabla\omega\|_2^2
 =\int_{\mathbb T^3}\omega\cdot S\omega\,dx,
 \tag{8.1}
\]

the proposed experiment tests whether the covariance residual, exact
commutator, or line geometry can control the stretching source on the right
without assuming the desired uniform enstrophy bound.  A successful estimate
may depend on \(\|\omega(0)\|_2\); it may not insert
\(\sup_{t<T}\|\omega(t)\|_2\) as an unexplained hypothesis.

## 9. Claim boundary

What is proved:

- the exact dyadic frame-index shift and torus pullback identities;
- a uniform simple gap and pointwise near-rank ratio for the base flow;
- the exact scaling of \(R\), \(\mathfrak C_P\), \(\mathfrak W_L\), kinetic
  energy, and the weighted palinstrophy majorant;
- the locally bounded energy-level no-go in Theorem 7.1.

What is not proved:

- failure of estimates using initial enstrophy or higher initial norms;
- failure of estimates that retain additional cancellation in the signed
  diffusion deficit rather than estimating it by \(c_\eta\mathcal G\);
- failure of all possible covariance or line-field producer mechanisms;
- exclusion of a right-hand side deliberately singular at the zero input;
- propagation of a near-rank-one condition for general solutions;
- any finite-time singularity or global-regularity theorem.

The exact certificate for this release checks the finite Fourier, covariance,
gap, scaling-weight, and exponent arithmetic.  The full dyadic operator and
covering identities are analytic lemmas in Sections 4--6 and are locked
semantically rather than inferred from finite samples.  Positivity of \(I_1\)
follows analytically from the certified positive point and continuity; it is
not a numerical-integration claim.
