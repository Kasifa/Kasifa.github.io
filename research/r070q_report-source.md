# R0.70Q — Exact covariance evolution, a raw-projector no-go, and a structure-adapted continuation target

**Status:** internal canonical candidate; not a public theorem chapter

**Release:** R0.70Q

**Date:** 2026-08-25

## 1. Decision in one page

R0.70P closed a conditional harmonic-analysis bridge.  R0.70Q asks whether
the Navier--Stokes equation itself propagates its covariance residual,
principal gap, and projector regularity.

Five decisions are now exact.

1. **Filtered covariance evolution: PASS.**  For the fixed scalar Fourier
   frame, the block vorticities and their pointwise covariance satisfy an
   exact material--diffusion equation.  Its source ledger contains
   stretching, transport and stretching commutators, a negative projected
   gradient-covariance term, and a positive spectral-curvature term.

2. **Aligned-state diffusion balance: PASS.**  At every point where
   \(Q=EL\) has rank one and \(E>0\), the spectral curvature is absorbed by
   the projected gradient covariance:

   \[
    \mathcal K_Q
    \leq\sum_{\alpha,k}|P\partial_k\Omega_\alpha|^2.
    \tag{1.1}
   \]

   Hence the net diffusion contribution to the residual equation is
   nonpositive.  The rotating Beltrami family below attains equality, so the
   coefficient is sharp.

3. **Direct Leray-energy closure of this covariance ledger: FAIL.**  Leray
   energy gives

   \[
    R\in L_t^1,
    \tag{1.2}
   \]

   while the R0.70P bridge requires \(R\in L_t^2\).  The estimates recorded
   below do not by themselves close the stretching, filter-defect, curvature,
   pointwise-gap, and normalized-projector terms at the energy level.

4. **Raw projector production from energy, residual, and relative gap:
   FAIL.**  An exact global Beltrami heat mode has

   \[
    R=0,\qquad
    \frac{\lambda_1-\lambda_2}{\operatorname{tr}Q}=1,
    \qquad
    \|\nabla P\|_F
    =\frac{\|\nabla Q\|_F}{\operatorname{tr}Q}
    =\sqrt2\,N.
    \tag{1.3}
   \]

   The velocity amplitude can be chosen so that any prescribed finite
   Sobolev norm is uniformly bounded, or even so that the initial data tend
   to zero in \(C^\infty\), while the projector gradient diverges.  A
   relative gap does not stabilize an eigendirection near \(Q=0\).

5. **A structure-adapted conditional target: PASS.**  The raw
   \(\|\nabla P\|_\infty\) bound is sufficient but not necessary.  Define

   \[
    \mathfrak C_P(t)
    =\sum_\alpha\|[T_\alpha,P]\omega(t)\|_2^2
    \tag{1.4}
   \]

   and the energy-weighted direction cost

   \[
    \mathfrak W_L
    =\int_0^{T_{\max}}
      \|u_*(t)\|_2^2\|\nabla u(t)\|_2^2
      \|\nabla L(t)\|_\infty^2\,dt.
    \tag{1.5}
   \]

   If \(R,\mathfrak C_P\in L_t^2\) and
   \(\mathfrak W_L<\infty\), the periodic \(H^1\) solution extends.  This
   criterion needs neither an endpoint-uniform projector gradient nor a
   spectral gap in its statement.

The remaining problem is therefore narrower.  It is not to propagate the
rough quantity

\[
 G=\frac{|\nabla Q|}{\operatorname{tr}Q}
\tag{1.6}
\]

for every coherent flow.  It is to propagate the three
structure-sensitive quantities in (1.4)--(1.5), together with \(R\), without
using an equivalent of the desired critical vorticity norm.

R0.70Q is not a regularity proof and not a solution of the Navier--Stokes
Millennium problem.  The exact obstruction is analytic; no DNS or DGX run
is needed for this gate.

## 2. Conventions and solution class

Work first with a smooth unforced solution on
\(\mathbb D=\mathbb R^3\) or \(\mathbb T^3\).  On the torus all integrals use
normalized Haar measure and the mean-zero velocity is

\[
 u_*=u-\bar u.
\tag{2.1}
\]

Use the row-gradient convention

\[
 B_{ij}=\partial_i u_j,
 \qquad
 S=\frac12(B+B^{\mathsf T}),
 \tag{2.2}
\]

Matrix and matrix-gradient pointwise norms are Frobenius norms.  Thus, for
example, \(\|\nabla P\|_\infty\) means the spatial essential supremum of
\(|\nabla P|_F\).

and define

\[
 \mathscr L_\nu
 =\partial_t+u\cdot\nabla-\nu\Delta.
 \tag{2.3}
\]

The vorticity equation is

\[
 \boxed{\mathscr L_\nu\omega=B^{\mathsf T}\omega,}
 \qquad
 (B^{\mathsf T}\omega)_j=B_{ij}\omega_i.
 \tag{2.4}
\]

The transpose in (2.4) is fixed by (2.2); changing gradient convention
without changing this term reverses indices and invalidates the later
matrix equation.

Use the explicit tight frame from R0.70P.  Its nonzero-mode blocks are
real-even radial scalar multipliers

\[
 T_j=\varphi(2^{-j}D),
 \qquad
 \sum_j|\varphi(2^{-j}\xi)|^2=1
 \quad(\xi\ne0).
 \tag{2.5}
\]

On the torus, adjoin \(T_\star=\Pi_0\).  Since periodic vorticity has zero
mean, the star block is zero in the covariance evolution, although it
remains necessary in the R0.70P reconstruction commutator.

All termwise calculations below can first be made for a finite frame
truncation.  For a smooth solution, finite overlap and rapid Fourier decay
justify the limit.  For weak solutions, the displayed pointwise equations
are formal until the corresponding products and limits are justified.

## 3. Filtered vorticity and covariance equation

Put

\[
 \Omega_\alpha=T_\alpha\omega.
 \tag{3.1}
\]

For operators, use \([A,C]=AC-CA\).  Since \(T_\alpha\) commutes with
\(\partial_t\), spatial derivatives, and \(\Delta\),

\[
 \boxed{
 \mathscr L_\nu\Omega_\alpha
 =B^{\mathsf T}\Omega_\alpha+\mathcal E_\alpha,}
 \tag{3.2}
\]

where

\[
 \begin{aligned}
 \mathcal E_\alpha^{\mathrm{tr}}
   &=[u\cdot\nabla,T_\alpha]\omega,\\
 \mathcal E_\alpha^{\mathrm{str}}
   &=[T_\alpha,B^{\mathsf T}]\omega,\\
 \mathcal E_\alpha^{\mathrm{diff}}
   &=\nu[T_\alpha,\Delta]\omega=0,\\
 \mathcal E_\alpha
   &=\mathcal E_\alpha^{\mathrm{tr}}
     +\mathcal E_\alpha^{\mathrm{str}}.
 \end{aligned}
 \tag{3.3}
\]

Equivalently,

\[
 \mathcal E_\alpha
 =-[T_\alpha,u\cdot\nabla]\omega
  +[T_\alpha,B^{\mathsf T}]\omega.
 \tag{3.4}
\]

If a future filter depends on time or space, (3.3) acquires additional
commutators.  Those terms are absent for the fixed Fourier frame.

Define

\[
 Q=\sum_\alpha\Omega_\alpha\otimes\Omega_\alpha,
 \tag{3.5}
\]

\[
 \mathcal F_Q
 =\sum_\alpha
  \left(
   \mathcal E_\alpha\otimes\Omega_\alpha
   +\Omega_\alpha\otimes\mathcal E_\alpha
  \right),
 \tag{3.6}
\]

and the positive semidefinite gradient covariance

\[
 \mathcal H_Q
 =\sum_{\alpha,k}
   \partial_k\Omega_\alpha\otimes\partial_k\Omega_\alpha.
 \tag{3.7}
\]

The product Laplacian supplies a factor two:

\[
 \Delta(\Omega\otimes\Omega)
 =(\Delta\Omega)\otimes\Omega
  +\Omega\otimes(\Delta\Omega)
  +2\sum_k\partial_k\Omega\otimes\partial_k\Omega.
 \tag{3.8}
\]

Therefore

\[
 \boxed{
 \mathscr L_\nu Q
 =B^{\mathsf T}Q+QB+\mathcal F_Q-2\nu\mathcal H_Q.}
 \tag{3.9}
\]

For \(E=\operatorname{tr}Q\), symmetry of \(Q\) removes the antisymmetric
part of \(B\), and

\[
 \boxed{
 \mathscr L_\nu E
 =2S:Q
  +2\sum_\alpha\mathcal E_\alpha\cdot\Omega_\alpha
  -2\nu\sum_{\alpha,k}|\partial_k\Omega_\alpha|^2.}
 \tag{3.10}
\]

Equations (3.9)--(3.10) are exact.  They do not yet have a favorable sign.

## 4. Principal residual and spectral curvature

Assume

\[
 \lambda_1>\lambda_2\ge\lambda_3\ge0.
 \tag{4.1}
\]

Let

\[
 L=v_1\otimes v_1,
 \qquad
 P=I-L,
 \qquad
 r=\operatorname{tr}(PQ)=E-\lambda_1=\lambda_2+\lambda_3.
 \tag{4.2}
\]

The reduced resolvent on the complementary plane is

\[
 \mathcal R_Q
 =P(\lambda_1I-Q)^{-1}P
 =\sum_{b=2}^3\frac{L_b}{\lambda_1-\lambda_b}.
 \tag{4.3}
\]

For symmetric perturbations \(H,K\),

\[
 D\lambda_1[H]=L:H,
 \tag{4.4}
\]

\[
 DL[H]=\mathcal R_QHL+LH\mathcal R_Q,
 \tag{4.5}
\]

\[
 Dr[H]=P:H,
 \tag{4.6}
\]

and

\[
 \boxed{
 D^2r[H,K]
 =-\operatorname{tr}(LH\mathcal R_QK)
  -\operatorname{tr}(LK\mathcal R_QH).}
 \tag{4.7}
\]

In particular, \(r(Q)=\operatorname{tr}Q-\lambda_{\max}(Q)\) is concave on
the simple-top stratum:

\[
 D^2r[H,H]
 =-2\operatorname{tr}(LH\mathcal R_QH)\le0.
 \tag{4.8}
\]

Define the nonnegative spectral curvature

\[
 \mathcal K_Q
 =\sum_k
 \operatorname{tr}
 \left(
  L(\partial_kQ)\mathcal R_Q(\partial_kQ)
 \right)
 =\sum_{k,b=2}^3
 \frac{|v_b^{\mathsf T}(\partial_kQ)v_1|^2}
      {\lambda_1-\lambda_b}.
 \tag{4.9}
\]

The spatial chain rule gives

\[
 \Delta r=P:\Delta Q-2\mathcal K_Q.
 \tag{4.10}
\]

The first-order material derivative has no projector-derivative remainder.
Combining it with (4.10) yields the sign-critical identity

\[
 \boxed{
 \mathscr L_\nu r
 =P:\mathscr L_\nu Q+2\nu\mathcal K_Q.}
 \tag{4.11}
\]

Substituting (3.9) into (4.11), and using that \(P\) commutes with \(Q\),
gives

\[
 \boxed{
 \begin{aligned}
 \mathscr L_\nu r
 ={}&
 2\operatorname{tr}(BPQ)
 +2\sum_\alpha(P\Omega_\alpha)\cdot\mathcal E_\alpha\\
 &-2\nu\sum_{\alpha,k}|P\partial_k\Omega_\alpha|^2
 +2\nu\mathcal K_Q.
 \end{aligned}}
 \tag{4.12}
\]

The four terms have different signs:

- stretching has no fixed sign;
- the filter defect has no fixed sign;
- projected gradient covariance is nonpositive;
- spectral curvature is nonnegative.

The two diffusion contributions do not have a fixed net sign.

The projector derivative is

\[
 \partial_kP
 =-\mathcal R_Q(\partial_kQ)L
  -L(\partial_kQ)\mathcal R_Q.
 \tag{4.13}
\]

Consequently,

\[
 \mathcal K_Q
 =\sum_{k,b=2}^3
   (\lambda_1-\lambda_b)c_{kb}^2,
 \qquad
 \|\nabla P\|_F^2
 =2\sum_{k,b=2}^3c_{kb}^2,
 \tag{4.14}
\]

where

\[
 c_{kb}
 =\frac{v_b^{\mathsf T}(\partial_kQ)v_1}
        {\lambda_1-\lambda_b}.
 \tag{4.15}
\]

Thus

\[
 \frac{\lambda_1-\lambda_2}{2}\|\nabla P\|_F^2
 \le\mathcal K_Q
 \le
 \frac{\lambda_1-\lambda_3}{2}\|\nabla P\|_F^2.
 \tag{4.16}
\]

On the periodic box, integration removes transport and scalar diffusion.
With

\[
 R(t)=\int_{\mathbb T^3}r(x,t)\,dx,
 \tag{4.17}
\]

one obtains

\[
 \boxed{
 \begin{aligned}
 R'(t)=\int_{\mathbb T^3}\Big[
 &2\operatorname{tr}(BPQ)
 +2\sum_\alpha(P\Omega_\alpha)\cdot\mathcal E_\alpha\\
 &-2\nu\sum_{\alpha,k}|P\partial_k\Omega_\alpha|^2
 +2\nu\mathcal K_Q
 \Big]\,dx.
 \end{aligned}}
 \tag{4.18}
\]

This is the exact propagation ledger.  It is not a closed differential
inequality.

### Proposition 4.1 — Sharp rank-one diffusion absorption

Suppose at a point that \(Q=EL\), where \(E>0\) and
\(L=v_1\otimes v_1\).  Because \(Q\) is a sum of positive rank-one
matrices, there are real scalars \(a_\alpha\) such that

\[
 \Omega_\alpha=a_\alpha v_1,
 \qquad
 \sum_\alpha a_\alpha^2=E.
 \tag{4.19}
\]

Put \(h_{\alpha k}=P\partial_k\Omega_\alpha\).  Differentiating \(Q\) and
projecting its off-diagonal block gives

\[
 P(\partial_kQ)v_1
 =\sum_\alpha a_\alpha h_{\alpha k}.
 \tag{4.20}
\]

Since the two lower eigenvalues vanish, (4.9) and Cauchy--Schwarz yield

\[
 \begin{aligned}
 \mathcal K_Q
 &=\frac1E\sum_k
   \left|\sum_\alpha a_\alpha h_{\alpha k}\right|^2\\
 &\leq\sum_{\alpha,k}|h_{\alpha k}|^2
 =\sum_{\alpha,k}|P\partial_k\Omega_\alpha|^2.
 \end{aligned}
 \tag{4.21}
\]

Consequently the two diffusion terms in (4.12) obey the sharp aligned-state
sign condition

\[
 \boxed{
 -2\nu\sum_{\alpha,k}|P\partial_k\Omega_\alpha|^2
 +2\nu\mathcal K_Q\leq0.}
 \tag{4.22}
\]

No spectral denominator remains in (4.21).  This does not yet control the
near-rank-one case: the size and sign of the absorption deficit away from
\(r=0\) are a separate quantitative problem.

## 5. What the Leray energy ledger supplies

The tight frame and periodic div--curl identity give

\[
 \int_{\mathbb T^3}E(t)\,dx
 =\sum_\alpha\|T_\alpha\omega(t)\|_2^2
 =\|\omega(t)\|_2^2
 =\|\nabla u(t)\|_2^2.
 \tag{5.1}
\]

Since \(0\le r\le E\),

\[
 0\le R(t)\le\|\omega(t)\|_2^2.
 \tag{5.2}
\]

The energy equality therefore gives only

\[
 \boxed{
 \int_0^T R(t)\,dt
 \le
 \int_0^T\|\nabla u(t)\|_2^2\,dt
 \le\frac{\|u_*(0)\|_2^2}{2\nu}.}
 \tag{5.3}
\]

This is one time exponent short of \(R\in L_t^2\).

The remaining terms in (4.18) expose separate blockers.

1. Pointwise,

   \[
    |\operatorname{tr}(BPQ)|
    \le |B|\,r,
    \tag{5.4}
   \]

   but energy does not provide the spatial or temporal norms needed to
   integrate the product at the \(R^2\) level.

2. The stretching defect contains \(B^{\mathsf T}\omega\), and the transport
   commutator contains high--low velocity--vorticity interactions.  Their
   square sequence is not controlled by
   \(u\in L_t^\infty L_x^2\) and
   \(\omega\in L_t^2L_x^2\).

3. The negative term uses \(\nabla\Omega_\alpha\), hence one more vorticity
   derivative than Leray energy controls.

4. Spectral curvature obeys the rough bound

   \[
    \mathcal K_Q
    \le
    \frac{|\nabla Q|_F^2}{\lambda_1-\lambda_2}.
    \tag{5.5}
   \]

   If \(\lambda_1-\lambda_2\ge\gamma E\), then

   \[
    \mathcal K_Q
    \le\gamma^{-1}
      \left(\frac{|\nabla Q|_F}{E}\right)^2E.
    \tag{5.6}
   \]

   This reintroduces the unknown normalized gradient.
   Proposition 4.1 shows that estimating the positive curvature term alone
   is unnecessarily lossy at \(r=0\).  A viable estimate must retain its
   coupling to the negative projected-gradient term and quantify only the
   failure of (4.21) when \(r>0\).

5. The pointwise implication

   \[
    \frac rE\le\eta<\frac12
    \quad\Longrightarrow\quad
    \lambda_1-\lambda_2\ge(1-2\eta)E
    \tag{5.7}
   \]

   is exact, but the spatial integral \(R=\int r\) does not imply the
   pointwise premise.

6. A top gap makes \(L\) smooth even if
   \(\lambda_2=\lambda_3\).  It does not make the ordered lower eigenvalue
   \(\lambda_2\) differentiable through that collision.  Propagating the
   gap as a difference of two smooth scalar eigenvalues is therefore not a
   legal shortcut.

The exact equation passes the algebraic gate.  It fails the energy-level
closure gate.

## 6. Exact rotating Beltrami heat mode

Let \(N\ge1\) be an integer and let \(\varepsilon_N>0\).  Define

\[
 a_N(t)=\varepsilon_Ne^{-\nu N^2t},
 \qquad
 \theta=Nx_1,
 \tag{6.1}
\]

\[
 v_N=(0,\cos\theta,\sin\theta),
 \qquad
 w_N=(0,-\sin\theta,\cos\theta),
 \tag{6.2}
\]

and

\[
 u_N=-a_Nv_N.
 \tag{6.3}
\]

Then

\[
 \nabla\cdot u_N=0,
 \qquad
 (u_N\cdot\nabla)u_N=0,
 \qquad
 \partial_tu_N=\nu\Delta u_N.
 \tag{6.4}
\]

Thus \(u_N\) is a smooth global unforced Navier--Stokes solution.  Its
vorticity is

\[
 \omega_N=\nabla\times u_N
 =Na_Nv_N=-Nu_N,
 \tag{6.5}
\]

and

\[
 B^{\mathsf T}\omega_N=0.
 \tag{6.6}
\]

Because the pinned frame multipliers are real, even, and radial,

\[
 T_j\omega_N=c_{j,N}\omega_N,
 \qquad
 c_{j,N}=\varphi(2^{-j}Ne_1)\in\mathbb R,
 \tag{6.7}
\]

and

\[
 \sum_jc_{j,N}^2=1.
 \tag{6.8}
\]

Therefore

\[
 \boxed{Q_N=\omega_N\otimes\omega_N=E_NL_N,}
 \tag{6.9}
\]

where

\[
 E_N=N^2a_N^2,
 \qquad
 L_N=v_N\otimes v_N,
 \qquad
 P_N=I-L_N.
 \tag{6.10}
\]

The spectrum is

\[
 (\lambda_1,\lambda_2,\lambda_3)=(E_N,0,0).
 \tag{6.11}
\]

Hence, for every finite time,

\[
 r_N=R_N=0,
 \qquad
 \lambda_1-\lambda_2=E_N,
 \qquad
 \frac{\lambda_1-\lambda_2}{E_N}=1.
 \tag{6.12}
\]

The direction varies at frequency \(N\):

\[
 \boxed{
 \|\nabla P_N\|_F
 =\frac{|\nabla Q_N|_F}{E_N}
 =\sqrt2\,N.}
 \tag{6.13}
\]

The frame residual and the actual commutator both vanish:

\[
 P_NT_j\omega_N=0,
 \qquad
 [T_j,P_N]\omega_N
 =T_j(P_N\omega_N)-P_NT_j\omega_N=0.
 \tag{6.14}
\]

The star block also vanishes.

The covariance equation records an exact diffusion cancellation.  One has

\[
 \mathcal E_j=0,
 \qquad
 \mathcal H_{Q_N}
 =E_NN^2\,w_N\otimes w_N,
 \tag{6.15}
\]

\[
 \mathcal K_{Q_N}=E_NN^2,
 \tag{6.16}
\]

and

\[
 \mathscr L_\nu Q_N
 =-2\nu E_NN^2\,w_N\otimes w_N.
 \tag{6.17}
\]

Consequently,

\[
 -2\nu P_N:\mathcal H_{Q_N}
 +2\nu\mathcal K_{Q_N}=0,
 \tag{6.18}
\]

as required by \(r_N\equiv0\).  Dropping either diffusion term gives a
false residual evolution.

## 7. The raw-projector no-go

### Theorem 7.1 — No amplitude-level bound for the principal direction

For the family in Section 6, \(P_N\) is independent of
\(\varepsilon_N\).  Consequently:

1. with \(\varepsilon_N=1\),

   \[
    \|u_N(0)\|_2=1,
    \qquad
    R_N=0,
    \qquad
    \frac{\lambda_1-\lambda_2}{E_N}=1,
    \tag{7.1}
   \]

   but \(\|\nabla P_N\|_\infty=\sqrt2N\);

2. for any fixed \(m\ge0\), using the Bessel-potential Sobolev norm and
   choosing

   \[
    \varepsilon_N=(1+N^2)^{-m/2}
    \tag{7.2}
   \]

   gives the exact normalized value

   \[
    \|u_N(0)\|_{H^m}=1,
    \tag{7.3}
   \]

   while \(\|\nabla P_N\|_\infty=\sqrt2N\);

3. choosing \(\varepsilon_N=e^{-N}\) gives

   \[
    u_N(0)\longrightarrow0
    \quad\hbox{in }C^\infty(\mathbb T^3),
    \tag{7.4}
   \]

   while the projector gradients diverge.

Thus no estimate can bound the principal-projector gradient by a right-hand
side that is locally bounded in any fixed finite collection of
amplitude-sensitive Sobolev norms, \(R\), and the relative spectral gap near
this sequence approaching \(Q=0\).  An estimate of that type needs an
absolute nondegeneracy input, an amplitude cutoff, the initial direction
gradient itself, or additional structure.

For every fixed \(0\le\tau<T<\infty\),

\[
 \|\nabla P_N\|_{L^4(\tau,T;L^\infty)}
 =\sqrt2\,N(T-\tau)^{1/4},
 \tag{7.5}
\]

so a positive time delay does not repair the raw normalized-gradient
estimate.  The amplitude decay cancels in
\(|\nabla Q_N|/E_N\).

### Exact scope

The example proves no singularity and no dynamic growth of the projector:
the direction is highly oscillatory from the initial time and the solution
is global.  It does not show that \(R\) or the gap cannot propagate; both
are perfect in this family.  It does not exclude estimates depending on an
absolute gap, an energy floor, a frequency moment, the initial direction
gradient, or higher structure.

Most importantly, (6.14) shows that the generic estimate

\[
 \mathfrak C_P^{1/2}
 \lesssim\|\nabla P\|_\infty\|u_*\|_2
 \tag{7.6}
\]

can be arbitrarily non-sharp.  The no-go rejects the raw \(G\)-producer; it
does not reject the exact commutator bridge.

The real-even condition in (6.7) is essential.  If scalar multipliers carry
different phases on the two helical Fourier modes, the filtered vectors
need not remain collinear and \(Q_N\) can have rank two.  The R0.70P frame
was made real-even and radial, so the exact rank-one statement is legal for
the canonical route.

## 8. A structure-adapted conditional continuation theorem

The R0.70P frame theorem only needs the exact commutator square, not its
rough Lipschitz upper bound.  The periodic projector proof only needs an
energy-weighted direction integral, not endpoint-uniform
\(\|\nabla L\|_\infty\).

### Theorem 8.1 — Residual, exact commutator, and weighted direction cost

Let

\[
 u\in C([0,T_{\max});H^1_\sigma(\mathbb T^3))
 \cap L^2_{\mathrm{loc}}([0,T_{\max});H^2)
 \tag{8.1}
\]

be a maximal unforced mild/strong solution with
\(T_{\max}<\infty\).  Let \(L\) be a jointly measurable rank-one
orthogonal projector, put \(P=I-L\), and assume
\(L(t)\in W^{1,\infty}_x\) for almost every \(t\).  Define

\[
 R(t)=\sum_\alpha\|PT_\alpha\omega(t)\|_2^2,
 \tag{8.2}
\]

\[
 \mathfrak C_P(t)
 =\sum_\alpha\|[T_\alpha,P]\omega(t)\|_2^2.
 \tag{8.3}
\]

If

\[
 R,\mathfrak C_P\in L^2(0,T_{\max})
 \tag{8.4}
\]

and

\[
 \boxed{
 \mathfrak W_L
 =\int_0^{T_{\max}}
  \|u_*(t)\|_2^2
  \|\nabla u(t)\|_2^2
  \|\nabla L(t)\|_\infty^2\,dt
 <\infty,}
 \tag{8.5}
\]

then \(u\) extends past \(T_{\max}\).

#### Proof

The complete-frame bridge gives

\[
 \|P\omega\|_{L_t^4L_x^2}
 \le a_0^{-1/2}
 \left(
  \|R\|_{L_t^2}^{1/2}
  +\|\mathfrak C_P\|_{L_t^2}^{1/2}
 \right).
 \tag{8.6}
\]

For

\[
 Z_L(t)=\int_{\mathbb T^3}\operatorname{tr}(LS^2)\,dx,
 \tag{8.7}
\]

the orientation-free integration-by-parts estimate from R0.70P gives

\[
 Z_L(t)^2
 \le\frac18\|P\omega(t)\|_2^4
 +2\|u_*(t)\|_2^2
   \|\nabla u(t)\|_2^2
   \|\nabla L(t)\|_\infty^2.
 \tag{8.8}
\]

Equations (8.4)--(8.6) and (8.5) imply
\(Z_L\in L^2(0,T_{\max})\).  The middle-strain estimate and periodic
\(H^1\) blow-up alternative then give the extension.

The condition (8.5) is formally critical under the usual
\(\mathbb R^3\) Navier--Stokes scaling.
It is weaker than endpoint-uniform \(\|\nabla L\|_\infty\) combined with
energy, and it accommodates the exact cancellation in Section 6.

For the Beltrami family, using the Frobenius tensor norm and integrating to
any \(0<T\leq\infty\),

\[
 R_N=\mathfrak C_{P_N}=0,
 \tag{8.9}
\]

and

\[
 \mathfrak W_{L_N}
 =\frac{\varepsilon_N^4N^2}{2\nu}
   \left(1-e^{-4\nu N^2T}\right)<\infty.
 \tag{8.10}
\]

Thus the hypotheses in Theorem 8.1 are compatible with this harmless family
even when the raw projector gradient is large.

## 9. Revised propagation target

The covariance PDE (4.12) remains relevant to \(R\), but R0.70Q changes the
projector part of the route.

The next ledger should test:

1. whether the sharp rank-one absorption (4.21) has a quantitative
   near-rank-one extension whose error is controlled by \(r\), and whether
   this closes \(R\in L_t^2\) in (4.18);
2. whether the exact commutator square
   \(\mathfrak C_P\), rather than its raw Lipschitz majorant, has a
   covariance or paraproduct evolution with favorable aligned-state
   cancellation;
3. whether the weighted direction cost \(\mathfrak W_L\) can be controlled
   directly, possibly after splitting the low-\(E\) region where the
   principal direction is unstable;
4. whether an approximate or regularized line field gives a better balance
   between residual and direction cost than the exact principal projector.

A route stops if it replaces any of these quantities by
\(\|\omega\|_{L_t^4L_x^2}\),
\(\|\nabla\omega\|_\infty\), or an equivalent continuation norm.

The exact Beltrami family also sets an acceptance test for every future
estimate:

- it must allow \(R=\mathfrak C_P=0\);
- it must preserve the exact diffusion-curvature cancellation;
- it must not demand a uniform amplitude-independent bound on raw
  \(\nabla P\) or \(G\).

## 10. Claim boundary and reproducibility

What is proved in R0.70Q:

- the exact block-vorticity, covariance, trace, and principal-residual
  evolution identities;
- the positive sign and exact coefficient of spectral curvature;
- the sharp rank-one absorption of spectral curvature by projected gradient
  covariance;
- the \(R\in L_t^1\), not \(L_t^2\), energy baseline;
- the global rotating Beltrami family and its diffusion-curvature
  cancellation;
- the raw-projector no-go in Theorem 7.1;
- the structure-adapted conditional continuation theorem.

What is not proved:

- propagation of \(R\in L_t^2\);
- propagation of the exact commutator square or weighted direction cost;
- persistence of a covariance principal line for arbitrary data;
- regularity of arbitrary Leray--Hopf solutions;
- global regularity or finite-time singularity for three-dimensional
  Navier--Stokes.

The exact producer in research/r070q_exact_audit.py checks only the finite
matrix, trigonometric, spectral, and Beltrami identities.  It does not prove
an infinite-dimensional commutator theorem or a Navier--Stokes continuation
theorem.

No public-page update or GitHub publication is authorized by this report.
