# R0.70G — Adjacent-source affine jets: critical dilation defect and the missing dual estimate

> **Status:** internal canonical research report; not a public theorem chapter.
> **Date:** 2026-08-24.
> **Scope:** fixed-source annular differences, critically normalized harmonic
> jets, a dissipation-level spacetime source coefficient estimate, exact
> initial-face pressure
> tests, and the remaining core-moment gap.

## 1. Result in one page

R0.70F left one concrete possibility open: perhaps adjacent fixed annuli behave
like martingale differences and remove the recurrent constant and linear
harmonic jets. R0.70G tests that possibility without identifying a physical
annular partition with a frequency Littlewood--Paley decomposition.

Let $r_j=2^{-j}$. For one fixed center $x_0$, one fixed source
$\Omega$, and cumulative exterior cutoffs $\Theta_j$, put

\[
 E_j=K*(\Theta_j\Omega),\qquad
 \psi_j=\Theta_j-\Theta_{j-1},\qquad
 H_j=K*(\psi_j\Omega)=E_j-E_{j-1}.
 \tag{1.1}
\]

If $P_j^{(n)}$ is the degree-$n$ Taylor coefficient of $E_j$ at
$x_0$, then the annular coefficient is

\[
 J_j^{(n)}=P_j^{(n)}-P_{j-1}^{(n)}.
 \tag{1.2}
\]

The Navier--Stokes critical coordinates are

\[
 c_j^{(n)}=r_j^{n+2}P_j^{(n)},\qquad
 h_j^{(n)}=r_j^{n+2}J_j^{(n)}.
 \tag{1.3}
\]

They obey the exact transport law

\[
 \boxed{
 h_j^{(n)}=c_j^{(n)}-2^{-(n+2)}c_{j-1}^{(n)}.}
 \tag{1.4}
\]

The coefficients for the constant, linear, and quadratic jets are therefore
$1/4,1/8,1/16$, not $1$. Equivalently,

\[
 h_j^{(n)}
 =\bigl(c_j^{(n)}-c_{j-1}^{(n)}\bigr)
  +\bigl(1-2^{-(n+2)}\bigr)c_{j-1}^{(n)}.
 \tag{1.5}
\]

The second term is the **critical dilation defect**. Exact source telescoping
and critical normalization cannot both use an ordinary coefficient-one
difference.

This is not a semantic issue. If
$h_m=1$, $c_0=0$, and
$\lambda=2^{-(n+2)}$, then

\[
 c_m=\frac{1-\lambda^m}{1-\lambda},\qquad
 c_m-\lambda c_{m-1}=1,\qquad
 c_m-c_{m-1}=\lambda^{m-1}.
 \tag{1.6}
\]

The raw increment has $\ell^1$ norm and square mass equal to $N$ through
level $N$, while the ordinary differences of the cumulative coordinates
have bounded total mass. Ordinary differences have hidden the recurrent
baseline; they have not bounded its positive work.

There is nevertheless a useful deterministic source estimate. If
$\Omega\in L^2$ at the time under consideration and the physical annuli have
bounded overlap, kernel homogeneity and Cauchy--Schwarz give

\[
 \boxed{
 \sum_j r_j^{2n+3}|J_j^{(n)}(x_0)|^2
 \le C_n\|\Omega\|_2^2.}
 \tag{1.7}
\]

In critical coordinates this is

\[
 \sum_j r_j^{-1}|h_j^{(n)}|^2\le C_n\|\Omega\|_2^2.
 \tag{1.8}
\]

After time integration, Leray dissipation controls the corresponding
spacetime weighted coefficient square estimate. This is not an unweighted
Littlewood--Paley square function and is not a pointwise-in-time consequence
of $\sup_t\|u(t)\|_2$ alone. The missing estimate is on the core enstrophy
moments paired with those jets. For the affine terms, a sufficient dual
condition is

\[
 \sum_j\left(
 r_j^{-3}|M_j^{(0)}|^2+r_j^{-5}|M_j^{(1)}|^2
 \right)<\infty.
 \tag{1.9}
\]

Finite energy does not provide (1.9), and the audited harmonic-analysis
theorems do not turn (1.7) into the fixed-center, positive-part, double-scale
packing required by the Navier--Stokes argument.

Exact compact pressure tests sharpen the boundary:

1. on the complete dyadic grid, separated annular jets form exact spikes, so
   both adjacent variation and square mass grow linearly;
2. after retaining only active scales, alternating full tensor profiles still
   have linearly growing adjacent square mass;
3. after projecting to the scalar actually paired with a fixed $e_1$-core,
   adjacent differences vanish, but the positive baseline work still grows
   linearly.

This eliminates one proposed shortcut: **replace the low-order fixed-source
jets by ordinary adjacent differences and expect energy or martingale
orthogonality to close the positive work automatically**. It does not exclude
a hybrid theorem that controls the mean mode by a new core-moment Carleson or
variation estimate.

All pressure tests are initial-face statements. Nothing here constructs a
common positive terminal time, a singular solution, a large-data regularity
theorem, or a solution of the Millennium problem.

## 2. Source boundary and three different notions of difference

The source problem is [Yu v1, Section 8.3](https://arxiv.org/html/2606.27560v1#S8.SS3).
That section requires a fixed smooth annular partition before applying a
harmonic Taylor expansion. It also states that the fixed-source route is a
separate conditional module and is not identified with the moving-shell
positive estimate.

Three constructions must remain distinct.

### 2.1 Fixed-source cumulative difference

For fixed $k$, fixed time, fixed filter, and fixed center, define

\[
 E_{J,k}=K*(\Theta_J\Omega_k),\qquad
 \Theta_J=\sum_{i\le J}\psi_i.
 \tag{2.1}
\]

Linearity gives the exact identity

\[
 E_{J,k}-E_{J-1,k}=K*(\psi_J\Omega_k).
 \tag{2.2}
\]

This is the algebra used in R0.70G.

### 2.2 Changing-filter difference

The expression

\[
 K*(\Theta_J\Omega_J)-K*(\Theta_{J-1}\Omega_{J-1})
 \tag{2.3}
\]

is not a single-annulus source. It contains both a cutoff difference and a
filter/target difference. Formula (2.2) is invalid if the same $k$ is not
held fixed.

### 2.3 Moving-center convolution difference

If the annular kernel is instead centered at the evaluation point,

\[
 D_jf(x)=\int K(x-y)\eta_j(y-x)f(y)\,dy,
 \tag{2.4}
\]

then $D_j$ is a convolution-type singular integral. Classical square,
jump, and variation estimates can apply after the required cancellation,
Fourier decay, and regularity hypotheses are verified. But the source annulus
now moves with $x$, so (2.4) is not one fixed exterior source producing a
harmonic field throughout the core ball.

R0.70G never substitutes (2.3) or (2.4) for (2.2).

## 3. Why this is not a martingale or frequency Littlewood--Paley decomposition

The label “martingale-style” refers only to the algebraic identity (2.2).
These multiplication operators are not conditional expectations relative to
nested sigma-algebras, and the annular pieces have no conditional-zero-mean
property or automatic martingale orthogonality.

It is also not a frequency projection. Physical multiplication gives

\[
 \widehat{\psi_j\Omega}=\widehat{\psi_j}*\widehat\Omega,
 \tag{3.1}
\]

which is generally full-frequency. The partition identity
$\sum_j\psi_j=1$ does not impose zero mean, zero first moment, or Fourier
annular support on each $\psi_j\Omega$.

The discrete transforms of
[Frazier--Jawerth](https://doi.org/10.1016/0022-1236(90)90137-A)
build cancellation and frequency localization into the analyzing and
synthesis functions. The tent spaces of
[Coifman--Meyer--Stein](https://doi.org/10.1016/0022-1236(85)90007-2)
and the BMO Carleson characterization of
[Fefferman--Stein](https://doi.org/10.1007/BF02392215)
provide the correct abstract language once an appropriate square function or
Carleson measure is already available. Bounded physical overlap does give the
elementary quadratic estimate
$\sum_j\|\psi_j\Omega\|_2^2\lesssim\|\Omega\|_2^2$; what is absent is the
martingale or frequency-cancellation structure. None of these facts makes a
positive physical annular partition into a martingale difference sequence.

## 4. Critical transport theorem

Let the degree-$n$ Taylor coefficient use the convention

\[
 P_j^{(n)}=\frac1{n!}D^nE_j(x_0),\qquad
 J_j^{(n)}=\frac1{n!}D^nH_j(x_0).
 \tag{4.1}
\]

Then (2.2) gives

\[
 J_j^{(n)}=P_j^{(n)}-P_{j-1}^{(n)}.
 \tag{4.2}
\]

A strain jet of degree $n$ scales as length to the power $-(n+2)$.
With

\[
 c_j^{(n)}=r_j^{n+2}P_j^{(n)},\qquad
 h_j^{(n)}=r_j^{n+2}J_j^{(n)},
 \tag{4.3}
\]

and $\rho_j=r_j/r_{j-1}$, direct substitution gives

\[
 \boxed{
 h_j^{(n)}=c_j^{(n)}-\rho_j^{\,n+2}c_{j-1}^{(n)}.}
 \tag{4.4}
\]

On the dyadic grid, $\rho_j=1/2$, which proves (1.4).
For a general gap, the ordinary-difference decomposition is

\[
 h_j^{(n)}
 =\bigl(c_j^{(n)}-c_{j-1}^{(n)}\bigr)
  +\bigl(1-\rho_j^{\,n+2}\bigr)c_{j-1}^{(n)}.
 \tag{4.5}
\]

No estimate has been used in (4.4)--(4.5); these are exact identities.

### 4.1 Fixed-grid sequence equivalence

Put $\lambda_n=2^{-(n+2)}<1$, extend a finite sequence by zero, and write

\[
 h=(I-\lambda_n S)c,
 \tag{4.6}
\]

where $S$ is the backward shift. For every $1\le p\le\infty$,

\[
 (1-\lambda_n)\|c\|_{\ell^p}
 \le\|h\|_{\ell^p}
 \le(1+\lambda_n)\|c\|_{\ell^p}.
 \tag{4.7}
\]

The upper and lower bounds follow from the triangle and reverse-triangle
inequalities and $\|S\|_{\ell^p\to\ell^p}\le1$. Consequently, on one fixed
grid, source increments and critically normalized cumulative jets have
equivalent $\ell^p$ summability. Adjacent source differencing does not
manufacture summability absent from the cumulative sequence.

### 4.2 Constant recurrence

The recurrence (1.6) gives the finite identities

\[
 \sum_{m=1}^N|h_m|=N,\qquad
 \sum_{m=1}^N|h_m|^2=N,
 \tag{4.8}
\]

while

\[
 \sum_{m=1}^N|c_m-c_{m-1}|
 =\frac{1-\lambda^N}{1-\lambda},
 \qquad
 \sum_{m=1}^N|c_m-c_{m-1}|^2
 =\frac{1-\lambda^{2N}}{1-\lambda^2}.
 \tag{4.9}
\]

Both quantities in (4.9) remain bounded as $N\to\infty$. Therefore an
ordinary adjacent difference can be small precisely while the covariant
source increment and its positive baseline remain recurrent.

## 5. Signed telescoping and the core-variation defect

For arbitrary tensor sequences $P_j$ and $M_j$, finite summation by parts
gives

\[
 \boxed{
 \sum_{j=a}^b(P_j-P_{j-1}):M_j
 =P_b:M_b-P_{a-1}:M_a
  +\sum_{j=a}^{b-1}P_j:(M_j-M_{j+1}).}
 \tag{5.1}
\]

If one target/filter $k$ is fixed and the same signed core moment is paired
with every source annulus, the interior term vanishes and the source row
telescopes to endpoints. R0.70G does not contradict that identity.

The intended Navier--Stokes sum changes the core scale, filter, cutoff, time
window, and normalized moment with $k$. Formula (5.1) then exposes the
remaining term: a cumulative source jet paired with the variation of the core
moment. The map $s\mapsto s_+$ and termwise absolute values also destroy
signed telescoping.

This separates two questions:

- **source cancellation:** exact for a fixed signed row;
- **positive double-scale packing:** requires control of changing core
  moments and cannot be inferred from the source telescope alone.

## 6. An unconditional source-side square function

Assume

\[
 \operatorname{supp}\psi_j
 \subset A_j:=\{c_0r_j\le |y-x_0|\le C_0r_j\},
 \tag{6.1}
\]

the annuli $A_j$ have uniformly bounded overlap, and
$|\psi_j|_\infty\le C_\psi$. The strain kernel satisfies

\[
 |D^nK(x_0-y)|\le C_n r_j^{-3-n}
 \quad\hbox{on }A_j.
 \tag{6.2}
\]

Cauchy--Schwarz on $A_j$ yields

\[
 |J_j^{(n)}(x_0)|
 \le C_n r_j^{-n-3/2}\|\psi_j\Omega\|_2.
 \tag{6.3}
\]

After squaring, multiplying by $r_j^{2n+3}$, and summing,

\[
 \sum_jr_j^{2n+3}|J_j^{(n)}(x_0)|^2
 \le C_n\sum_j\|\psi_j\Omega\|_2^2
 \le C_n'\|\Omega\|_2^2.
 \tag{6.4}
\]

This proves (1.7). For a fixed filtered source over time,

\[
 \sum_jr_j^{2n+3}\int_0^T|J_j^{(n)}(x_0,t)|^2\,dt
 \le C_n\int_0^T\|\Omega(t)\|_2^2\,dt.
 \tag{6.5}
\]

For Leray solutions and an $L^1$-contractive spatial filter, viscous energy
dissipation controls the right side after integration over almost every time
slice:

\[
 \int_0^T\|\Omega(t)\|_2^2\,dt
 \le \int_0^T\|\omega(t)\|_2^2\,dt
 \lesssim E_0/\nu.
 \tag{6.5a}
\]

This does not follow pointwise in time from
$\sup_t\|u(t)\|_2$ alone. Estimating a filtered vorticity only from velocity
energy gives
$\|\Omega_\ell(t)\|_2\lesssim\ell^{-1}\|u(t)\|_2$, with an additional
filter-scale loss. Formula (6.5) is for one fixed source/filter family and
does not sum freely over another changing filter index. For this reason,
(6.5) is called a **Leray dissipation-level spacetime weighted coefficient
estimate**, not a classical Littlewood--Paley square function.

There are two related but weaker classical $L^2$ facts:

\[
 \sum_j\|T(\psi_j\Omega)\|_2^2\lesssim\|\Omega\|_2^2,
 \tag{6.6}
\]

by bounded annular overlap and Calderón--Zygmund $L^2$ boundedness, and a
moving-center convolution square function averaged over all $x$. Neither
permits evaluation at one prescribed point merely from an output $L^2$
bound; point evaluation is not a bounded functional on $L^2$.

## 7. The exact dual gap for affine work

Let the spatial core moments be

\[
 M_j^{(0)}=\int\chi_j\Omega_j\otimes\Omega_j\,dx,
 \qquad
 M_j^{(1)}=\int\chi_j(x-x_0)\otimes
                  \Omega_j\otimes\Omega_j\,dx.
 \tag{7.1}
\]

The tensor contractions use the natural index pairing. From (6.4),

\[
 \sum_j\left(r_j^3|J_j^{(0)}|^2+r_j^5|J_j^{(1)}|^2\right)
 \lesssim\|\Omega\|_2^2.
 \tag{7.2}
\]

Therefore Cauchy--Schwarz would close the absolute affine pairing if

\[
 \boxed{
 \sum_j\left(r_j^{-3}|M_j^{(0)}|^2
             +r_j^{-5}|M_j^{(1)}|^2\right)<\infty.}
 \tag{7.3}
\]

Equation (7.3) is a sufficient condition, not a conclusion of R0.70G.
It is also not asserted to be the only possible closure norm. Its value is
diagnostic: the source estimate and the missing core estimate now carry
exactly dual scale weights.

Finite energy controls a global quadratic quantity. The target work is a
fixed-center, two-scale, positive cubic pairing. No algebra turns the former
into (7.3). A possible surviving route must add one of the following:

- a local or parabolic Carleson estimate for the transported core moments;
- summable variation of those moments, compatible with (5.1);
- a sign or rigidity mechanism surviving the positive-part operation;
- a different paired norm that controls the mean mode as well as differences.

## 8. Exact compact pressure tests

This section reuses the compact, smooth, divergence-free interlaced family
proved in R0.70F. Fix $\Lambda=2^M$,

\[
 R_n=\Lambda^{-2n},\qquad r_n=R_n/\Lambda,
 \qquad j_n=2Mn,\qquad k_n=(2n+1)M.
 \tag{8.1}
\]

One radial annular partition, one even compact filter, and all support
buffers are independent of $N$. The core-vorticity factor is

\[
 b_n=\sum_{a=0}^{n-1}\Lambda^{-4a}
 =\frac{1-\Lambda^{-4n}}{1-\Lambda^{-4}}.
 \tag{8.2}
\]

### 8.1 Complete-grid spikes

At each active source index $j_n$, evaluate the annular jet with its
associated target/filter $k_n$. At every unused source index, use the same
fixed partition and the corresponding annular coefficient. The zero claims
at carrier-transition and unused indices use the explicit plateau condition
in Section 8.4, not support separation alone. Put
$k(j)=j+M$, so that $r_{k(j)}=r_j/\Lambda$, and set
$\ell_{k(j)}=\sigma r_{k(j)}$. Let
$J_{j,k(j)}^{(n)}(x_0)$ denote the degree-$n$ coefficient at $x_0$ generated
by $\psi_j\Omega_{\ell_{k(j)}}$. Define the **target-normalized diagonal
observables**

\[
 T_j^{(0)}=r_{k(j)}^2J_{j,k(j)}^{(0)}(x_0),\qquad
 B_j^{(1)}=r_{k(j)}^3J_{j,k(j)}^{(1)}(x_0).
 \tag{8.2a}
\]

Thus $T_j^{(0)}$ and $B_j^{(1)}$ are respectively
$\Lambda^{-2}$ and $\Lambda^{-3}$ times the source-radius normalized
coefficients from Section 4. They change the filter index with $j$ and are
not one fixed-$k$ cumulative sequence.

The selected components are exactly

\[
 (T_j^{(0)})_{11}
 =\Lambda^{-2}\mathbf 1_{\{j_1,\ldots,j_N\}}(j),
 \qquad
 (B_j^{(1)})_{111}
 =6\Lambda^{-3}\mathbf 1_{\{j_1,\ldots,j_N\}}(j).
 \tag{8.3}
\]

The zero bands separate all active indices. Hence, for
$\Delta X_j=X_j-X_{j-1}$, every spike has one entry and one exit:

\[
 \sum_j|\Delta(T_j^{(0)})_{11}|=2N\Lambda^{-2},
 \qquad
 \sum_j|\Delta(T_j^{(0)})_{11}|^2=2N\Lambda^{-4},
 \tag{8.4}
\]

and

\[
 \sum_j|\Delta(B_j^{(1)})_{111}|=12N\Lambda^{-3},
 \qquad
 \sum_j|\Delta(B_j^{(1)})_{111}|^2=72N\Lambda^{-6}.
 \tag{8.5}
\]

Thus full-grid ordinary adjacent differences do not gain summability.
These spikes occur along the changing diagonal $k=j+M$; they do not break
the fixed-$k$ signed telescope in Section 5.

### 8.2 Active-only full-tensor differences

Skipping the zero bands makes the original same-shape R0.70F profiles
identical after critical transport. To pressure-test that reindexing, alternate
two constant profiles

\[
 A_0=\operatorname{diag}(1,-1/2,-1/2),\qquad
 A_1=\operatorname{diag}(1,-1/4,-3/4).
 \tag{8.6}
\]

Both are symmetric and trace-free, both satisfy
$e_1\cdot A_\nu e_1=1$, and their spectra differ. Moreover,

\[
 \|A_1-A_0\|_F^2=\frac18.
 \tag{8.7}
\]

For $\widehat A_n=\Lambda^{-2}A_{n\bmod2}$,

\[
 \sum_{n=1}^{N-1}\|\widehat A_{n+1}-\widehat A_n\|_F^2
 =\frac{N-1}{8}\Lambda^{-4}.
 \tag{8.8}
\]

The different spectra prevent removal by orthogonal frame alignment.

For the linear strain use the harmonic cubics

\[
 \Phi_0=x_1^3-3x_1x_2^2,
 \qquad
 \Phi_1=x_1^3-\frac32x_1(x_2^2+x_3^2),
 \tag{8.9}
\]

and $B_\nu=\nabla^3\Phi_\nu$. Both have the same positive lobe value

\[
 e_1\cdot\nabla^2\Phi_\nu(ce_1)e_1=6c,
 \tag{8.10}
\]

but

\[
 \|B_0\|_F^2=144,\qquad
 \|B_1\|_F^2=90,\qquad
 \|B_1-B_0\|_F^2=54.
 \tag{8.11}
\]

Their unequal norms exclude orthogonal equivalence. For
$\widehat B_n=\Lambda^{-3}B_{n\bmod2}$,

\[
 \sum_{n=1}^{N-1}\|\widehat B_{n+1}-\widehat B_n\|_F^2
 =54(N-1)\Lambda^{-6}.
 \tag{8.12}
\]

The same radial cutoff homotopy used in R0.70F makes these profiles smooth,
compact, and divergence-free without changing their exact core jets.

### 8.3 Scalar projection sees no difference but misses the baseline

The scalar components actually paired with the chosen $e_1$-core are

\[
 s_n^{(0)}=\Lambda^{-2},\qquad
 s_n^{(1)}=6c\Lambda^{-3}.
 \tag{8.13}
\]

Therefore

\[
 s_{n+1}^{(q)}-s_n^{(q)}=0.
 \tag{8.14}
\]

The exact positive works are nevertheless

\[
 w_n^{(0)}=c_\chi\eta^3\Lambda^{-2}b_n^2,
 \qquad
 w_n^{(1)}=6c\,c_\chi\eta^3\Lambda^{-3}b_n^2.
 \tag{8.15}
\]

Since $b_n\ge1$,

\[
 \sum_{n=1}^Nw_n^{(q)}\ge C_qN.
 \tag{8.16}
\]

At the same time, the adjacent work variation is bounded:

\[
 \sum_{n=1}^{N-1}|w_{n+1}^{(q)}-w_n^{(q)}|
 =C_q(b_N^2-1)
 \le C_q\left((1-\Lambda^{-4})^{-2}-1\right).
 \tag{8.17}
\]

For these two specified observables there is an exact dichotomy:

- keep the full tensor, and active-adjacent variation and square mass can grow
  linearly;
- keep only the paired scalar, and adjacent variation can vanish while the
  positive mean work grows linearly.

This is not a universal no-go theorem for every source-adaptive algorithm.
A hybrid construction could quotient tensor frames while separately
controlling a mean mode. Such a mean-mode estimate is precisely an additional
input, not a consequence of differencing.

### 8.4 Radial constant-core correction

The partition proof retains coarser carrier sources. Its fixed radial
partition, independent of $N$, is chosen with two families of plateaus:

\[
 \begin{aligned}
 \psi_{j_n}&=1
 &&\text{on the }\ell_{j_n+M}\text{-expanded generator return transition},\\
 \psi_{k_m}&=1
 &&\text{on the }\ell_{k_m+M}\text{-expanded nonconstant transition of }
 V_{r_m}.
 \end{aligned}
 \tag{8.17a}
\]

Here $j_n$ and $k_m$ are the generator and carrier scale indices from
(8.1). Taking $M$ sufficiently large leaves disjoint buffers, so both
plateau families and the intervening zero bands belong to one fixed smooth
partition.

For a carrier transition, every other partition piece vanishes on the
nonconstant transition. Moreover,

\[
 (1-\psi_{k_m})
 \Omega_{\ell_{k_m+M}}[V_{r_m}]
 =a(|x|)e_1,
 \tag{8.17b}
\]

where $a$ is constant on the inner core. The needed local fact is slightly
stronger than the radial-shell lemma in R0.70F. If
$a(|x|)=a_0$ on a center ball and

\[
 -\Delta F=a(|x|),
 \tag{8.18}
\]

then the regular radial solution has

\[
 F(x)=-\frac{a_0}{6}|x|^2+C
 \tag{8.19}
\]

there. Consequently

\[
 \nabla F\times e_1
 =\left(0,-\frac{a_0x_3}{3},\frac{a_0x_2}{3}\right)
 \tag{8.20}
\]

is a solid rotation and has zero strain. The full carrier already has zero
core strain, while its complement in (8.17b) also has zero strain by
(8.18)--(8.20). Therefore the selected carrier-transition annular source has
exactly zero core strain. The generator plateaus capture their complete
filter-expanded return transitions. This is the reason the unused
coefficients in (8.3) vanish; support buffers alone would not be sufficient.
No source is silently deleted.

## 9. Energy, small-data NSE, and the time boundary

The alternating family uses only finitely many compact base profiles. The
R0.70F estimates therefore remain uniform:

\[
 \sup_N\left(\|f_N\|_2+\|f_N\|_{BMO^{-1}}\right)<\infty.
 \tag{9.1}
\]

After multiplication by one sufficiently small
$\varepsilon>0$, independent of $N$,
[Koch--Tataru](https://math.berkeley.edu/~tataru/papers/nas.pdf)
gives a unique small global solution in its $X$ class. On the initial face,
the tensor jets scale exactly by $\varepsilon$ and the cubic works exactly by
$\varepsilon^3$. No such exact amplitude homogeneity is asserted for the
nonlinear solution at $t>0$.

This transfer says only that globally regular small-data initial states can
carry arbitrarily long finite initial-face recurrence patterns. For every
fixed smooth initial datum, standard classical local theory, agreeing with
the Koch--Tataru mild solution, preserves finitely many strict signs for a
possibly $N$-dependent short positive time. It does not give an $N$-uniform
persistence interval or place every scale on backward cylinders with one
common interior top time. The linear caloric component suppresses preloaded
fine scales at a fixed positive time. Whether the nonlinear term can
regenerate them is not proved or disproved here.

## 10. Primary-literature audit and theorem mismatch

The search covered physical annular decompositions, discrete
Littlewood--Paley analysis, tent/Carleson spaces, strong variation and jump
inequalities, polynomial approximation, critical NSE tent norms, and local
strain decompositions. The search stopped after new primary sources repeated
one of the already audited structural classes and no source matched all four
features of the target: fixed center, physical source annuli, pointwise
affine jets, and an energy-only positive double-scale packing.

| primary source | theorem or framework actually available | mismatch with the R0.70G target |
|---|---|---|
| [Yu, 2026, Section 8.3](https://arxiv.org/html/2606.27560v1#S8.SS3) | fixed-source harmonic affine-jet route; conditional annular closure elsewhere under explicit sequence summability | explicitly leaves the fixed-source route conditional and does not identify it with the moving-shell positive quantity |
| [Frazier--Jawerth, 1990](https://doi.org/10.1016/0022-1236(90)90137-A) | discrete Calderón reproducing formulas and sequence spaces with built-in frequency localization and cancellation | physical multiplication by $\psi_j$ is not such a transform |
| [Coifman--Meyer--Stein, 1985](https://doi.org/10.1016/0022-1236(85)90007-2) and [Fefferman--Stein, 1972](https://doi.org/10.1007/BF02392215) | tent-space framework and BMO--Carleson characterization | the desired endpoint closure would require a uniformly normalized local Carleson norm; global energy supplies only total mass |
| [Jones--Seeger--Wright, 2008](https://people.math.wisc.edu/~seeger/papers/jsw.pdf) | the introduction records the annular convolution square estimate; Theorem 1.2 gives jump and $q>2$ variation bounds under its kernel hypotheses | center moves with the evaluation point; no fixed exterior harmonic field on a core ball |
| [Dorronsoro, 1985](https://doi.org/10.1090/S0002-9939-1985-0796440-3) | Sobolev/potential-space characterization by deviation from the best low-degree polynomial | the deviation vanishes on the whole affine polynomial class and is blind to the surviving affine coefficients themselves |
| [Koch--Tataru, 2001](https://math.berkeley.edu/~tataru/papers/nas.pdf) | small-data global well-posedness in $BMO^{-1}$ using caloric and solution tent norms | the small critical norm is extra input and is not a fixed physical-annulus jet Carleson theorem |
| [Eyink--Aluie, 2009](https://arxiv.org/pdf/0909.2386) | scale locality of smooth coarse-grained energy flux under Besov/structure-function hypotheses | adds regularity/scaling assumptions and concerns convolution energy flux, not fixed-source affine strain work |
| [Hamlington--Schumacher--Dahm, 2008](https://arxiv.org/pdf/0801.1248) | local/nonlocal strain decomposition with balls centered at the evaluation point | moving centers and model/DNS illustrations do not give an energy-class fixed-center packing theorem |

The literature finding is deliberately narrow: **no theorem matching the
target was found in the audited primary sources**. It is not a proof that no
such theorem exists anywhere.

## 11. Claim-to-source ledger

| report claim | support | status |
|---|---|---|
| fixed-source harmonic expansion is separate from moving-shell reassignment | Yu Section 8.3 | directly stated by source |
| small $BMO^{-1}$ data give a unique small global $X$-solution | Koch--Tataru Theorem 2 | directly stated by source |
| frequency/localized transform results require cancellation absent from a generic physical cutoff product | Frazier--Jawerth plus Fourier identity (3.1) | source framework plus elementary inference |
| moving-center variation theory does not yield one prescribed fixed-source harmonic jet | Jones--Seeger--Wright compared with (2.4) | structural inference |
| BMO is characterized by a Carleson measure of its extension | Fefferman--Stein Theorem 3 | directly stated by source |
| global $L^2$ mass does not control a uniformly normalized local Carleson supremum | concentration at decreasing scales | elementary norm comparison, not a quoted theorem |
| exact critical factors, Abel identity, recurrences, tensor norms, and radial-core formula | Sections 4, 5, and 8; exact symbolic certificate | proved in this report and certificate |
| deterministic weighted source coefficient estimate and its Leray spacetime version | kernel homogeneity, Cauchy--Schwarz, bounded overlap, and dissipation | proved in Section 6 |
| energy does not automatically provide the dual moment norm (7.3) | norm mismatch plus exact pressure tests | proved only as failure of the tested automatic route; no universal impossibility claim |
| no matching energy-only theorem was found | bounded primary-source audit in Section 10 | search finding, not theorem |

## 12. Closed question, open question, and next gate

### Closed in R0.70G

- The fixed-source cumulative identity is exact only with one source/filter
  held fixed.
- Critical normalization changes the adjacent coefficient to
  $2^{-(n+2)}$.
- Physical annular pieces have no automatic martingale or frequency
  orthogonality.
- Energy supplies the weighted source square function (6.4), but not the
  required dual core-moment estimate.
- Full-grid, active full-tensor, and paired-scalar pressure tests jointly show
  why ordinary differencing alone cannot close the positive work.

### Still open

- A local/parabolic Carleson or variation estimate for the transported core
  moments.
- A signed rigidity mechanism that survives the positive part.
- An estimate coupling the source square function to filter-scale and
  time-scale changes of the core profile.
- Any common-positive-time version of the initial-face recurrence test.

### R0.70H success criterion

The next gate is the **core-moment filter/time variation problem**. Define the
critically transported zeroth and first core moments at consecutive filter
and cylinder scales, derive their exact difference identities from the
filtered vorticity equation, and test whether energy plus dissipation controls
either

\[
 \sum_k\|\Delta_k\widetilde M_k\|^2
 \quad\hbox{or}\quad
 \sum_k\|\Delta_k\widetilde M_k\|.
 \tag{12.1}
\]

R0.70H succeeds in one of two ways:

1. it proves a scale-correct dual bound strong enough to pair with (6.4); or
2. it gives an exact energy-bounded family showing which term in the moment
   difference identity prevents such a bound.

That is the next smallest auditable question. A positive result would supply
the first missing bridge from the source square function to the nonlinear
core work. A negative result would remove another proof architecture without
being misreported as evidence for singularity.

## 13. Reproduction and figure

The exact symbolic producer is
`research/r070g_adjacent_jet_audit.py`. It checks the transport factors,
finite Abel identity, constant recurrence, alternating constant and linear
profiles, radial constant-core lemma, source square-function exponents, and
the inherited initial-face work factors.

The explanatory journal figure is archived under
`figures/r070g-critical-transport/fig-r070g-critical-transport/` with source
data, plotting code, manifest, validation, caption, PDF, SVG, and 600 dpi PNG.
It is an analytic diagram, not a numerical Navier--Stokes simulation.
