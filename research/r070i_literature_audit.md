# R0.70I primary-source literature audit

> **Audit date:** 2026-08-24
>
> **Disposition:** bounded search completed; no full-match theorem found
>
> **Scope:** parabolic tent/Carleson embeddings, Navier--Stokes bilinear
> estimates, local energy and scale flux, and bilinear variational or
> Littlewood--Paley square-function estimates that might control the
> fixed-center, changing-cutoff quadratic vorticity-moment pairing below.
> This is a source-and-norm audit, not external peer review and not a proof
> that no matching theorem exists.

## 1. Audit conclusion

The audit stopped after eight new high-signal primary sources, in addition to
the eight-source R0.70H baseline. No theorem in this bounded search controls,
from the Leray energy inequality and dissipation alone, the complete quantity

\[
 \boxed{
 \begin{aligned}
 \mathcal Q_{\rm core}(x_0)
 :=\int\sum_k r_k^{-3}\bigg[&
  \mathbf1_{I_{k+1}}(t)
  \left|m_k^{(n)}(t)-\rho_k^n m_{k+1}^{(n)}(t)\right|^2\\
 &+\mathbf1_{I_k\setminus I_{k+1}}(t)
  \left|m_k^{(n)}(t)\right|^2
 \bigg]dt,
 \qquad n=0,1 .
 \end{aligned}}
 \tag{1.1}
\]

Here the center is fixed, $r_{k+1}=\rho_k r_k$, the time windows share a
common top,

\[
 I_k=(t_0-r_k^2,t_0),
\]

and, for one fixed filter and cutoff family,

\[
 \begin{aligned}
 \Omega_k&=\varphi_{\sigma r_k}*\omega,
 &\chi_k(x)&=\chi\!\left(\frac{x-x_0}{r_k}\right),\\
 M_k^{(n)}(t)
 &=\int\chi_k(x)(x-x_0)^{\otimes n}\otimes
       \Omega_k(x,t)\otimes\Omega_k(x,t)\,dx,
 &m_k^{(n)}&=r_k^{1-n}M_k^{(n)}.
 \end{aligned}
 \tag{1.2}
\]

A full match would have to retain all five features simultaneously:

1. a quadratic vorticity moment, rather than a velocity field or velocity
   energy flux;
2. one fixed spatial center with changing physical cutoffs and filters;
3. the common-top nested windows, including the discarded-slab term;
4. the negative scale weight $r_k^{-3}$ after squaring; and
5. hypotheses no stronger than the Leray energy and dissipation bounds.

Every source below misses at least one structural feature and, in most cases,
several of them.

## 2. Non-duplicated search boundary

Before adding sources, the audit checked the eight primary sources already
used in R0.70H: Caffarelli--Kohn--Nirenberg; Duchon--Robert;
Dascaliuc--Grujić 2011 and 2013; Fefferman--Stein; Koch--Tataru;
Jones--Seeger--Wright; and Do--Muscalu--Thiele. Those sources were treated as
the baseline and are not counted again below.

The eight additions were selected to test four possible bridges that the
baseline left open:

- maximal regularity and Carleson embeddings in parabolic tent spaces;
- a direct Navier--Stokes Duhamel bilinear estimate;
- local-in-space energy control and smooth physical coarse-graining; and
- a bilinear variation theorem beyond the dyadic/LP formulation of
  Do--Muscalu--Thiele.

## 3. Primary-source matrix

### 3.1 Auscher--Monniaux--Portal: maximal regularity on tent spaces

**Source.** Pascal Auscher, Sylvie Monniaux, and Pierre Portal,
[The maximal regularity operator on tent spaces](https://arxiv.org/pdf/1011.1748),
2010, especially the tent-space definition on pp. 1--2, Definition 2.3, and
Theorems 3.1--3.2.

**Exact hypotheses and object.** Let $-L$ generate a bounded analytic
semigroup on $L^2(\mathbb R^d)$, and set

\[
 M_Lf(t)=\int_0^t Le^{-(t-s)L}f(s)\,ds.
\]

Theorem 3.1 assumes $L^2$ off-diagonal estimates of sufficient order for
$(tLe^{-tL})_{t>0}$ and proves boundedness of $M_L$ on weighted
$T^{p,2,m}(t^\beta\,dt\,dx)$ in its stated $p,\beta,m$ range. Theorem 3.2 is
the endpoint result on $T^{\infty,2,m}(t^\beta\,dt\,dx)$ for $\beta<1$ and
off-diagonal order $M>d/(2m)$. The input is already assumed to lie in the
same tent space whose norm is propagated to the linear output.

**Match and gap.** This is a genuine parabolic maximal-regularity theorem and
applies to the heat operator with $m=2$. It acts linearly on a spacetime
field and integrates $|f(t,x)|^2$ in $x$ before taking the center/radius
supremum. It neither forms a scalar/tensor quadratic moment and then squares
it, nor compares changing compact cutoffs, nor supplies a discrete
$r_k^{-3}$ scale variation. Applying it to a vorticity equation would first
require a tent-space bound for the nonlinear source, which is not supplied by
Leray dissipation.

### 3.2 Auscher--Frey: the Navier--Stokes tent-space bilinear map

**Source.** Pascal Auscher and Dorothee Frey,
[On well-posedness of parabolic equations of Navier--Stokes type with
$BMO^{-1}(\mathbb R^n)$ data](https://arxiv.org/pdf/1412.8407v3), 2015,
Definition 2.2, Theorem 2.4, equations (2.3)--(2.6), and Proposition 4.1.

**Exact hypotheses and object.** The admissible velocity path space is

\[
 \|u\|_{E_T}
 =\|t^{1/2}u\|_{L^\infty((0,T)\times\mathbb R^n)}
 +\sup_{x,0<t<T}
 \left(t^{-n/2}\int_0^t\int_{B(x,\sqrt t)}|u(s,y)|^2\,dy\,ds\right)^{1/2}.
\]

For

\[
 B(u,v)(t)=\int_0^t e^{(t-s)\Delta}\mathbb P\operatorname{div}
 (u\otimes v)(s)\,ds,
\]

Theorem 2.4 proves $B:E_T\times E_T\to E_T$. In the proof,
$\alpha=u\otimes v$ satisfies

\[
 \alpha\in T^{\infty,1},\qquad
 s^{1/2}\alpha\in T^{\infty,2},\qquad
 s\alpha\in L^\infty.
 \tag{3.1}
\]

The fixed-point well-posedness application requires small initial data in
$BMO^{-1}$. Proposition 4.1 shows that the relevant $A_2$ term is not
bounded from the weighted $T^{\infty,2}$ input to $T^{\infty,2}$; the
$T^{\infty,1}$ contribution cannot simply be discarded in this proof.

**Match and gap.** This is the closest direct NSE tent-space bilinear result.
However, taking $\alpha=\omega\otimes\omega$ would make
$T^{\infty,1}$ a parabolic local-enstrophy concentration condition and the
weighted $T^{\infty,2}$ condition a fourth-order vorticity requirement.
Neither follows from $\omega\in L^2_{t,x}$. The output is a Duhamel velocity
field, not the changing-cutoff moment increment in (1.1).

### 3.3 Germain--Pavlović--Staffilani: higher regularity in the
$BMO^{-1}$ solution class

**Source.** Pierre Germain, Nataša Pavlović, and Gigliola Staffilani,
[Regularity of solutions to the Navier--Stokes equations evolving from small
data in $BMO^{-1}$](https://arxiv.org/pdf/math/0609781v2), 2007, equation
(2.1), Theorem 2.2, Corollary 2.3, and Lemma 3.1.

**Exact hypotheses and object.** If
$\|u_0\|_{BMO^{-1}}<\varepsilon(d)$, Theorem 2.2 gives, for the
Koch--Tataru solution,

\[
 t^{k/2}\nabla^k u\in X^0,
 \qquad k\ge0,
\]

and Corollary 2.3 gives the corresponding $t^{-k/2}$ derivative decay in
$BMO^{-1}$. Lemma 3.1 defines

\[
 A(N)=\sup_{x_0,0<t<1}t^{-d/2}
 \int_0^t\int_{|x-x_0|<\sqrt t}|N(x,s)|\,dx\,ds
\]

and bounds a heat-regularized time integral $\beta_k$ by

\[
 \int_0^1\int_{\mathbb R^d}|\beta_k|^2
 \lesssim b(k)A(N)
 \int_0^1\int_{\mathbb R^d}|N|.
 \tag{3.2}
\]

**Match and gap.** For $N=\omega\otimes\omega$, Leray dissipation can
control the final total $L^1$ factor in (3.2), but not the normalized
Carleson factor $A(N)$. Thus this lemma identifies a precise missing input
rather than deriving it from energy. Its output is a heat-regularized source
field. The theorem also starts in a small-$BMO^{-1}$ class whose positive-time
regularity is already known, so it cannot serve as an energy-only route to
(1.1).

### 3.4 Jia--Šverák: local-in-space estimates near the initial time

**Source.** Hao Jia and Vladimír Šverák,
[Local-in-space estimates near initial time for weak solutions of the
Navier--Stokes equations and forward self-similar solutions](https://arxiv.org/pdf/1204.0529),
2012, Definition 3.1, Lemma 3.1, and Theorem 3.1.

**Exact hypotheses and object.** Their Leray solution class has uniformly
local velocity energy and dissipation and satisfies a local energy
inequality. Lemma 3.1 assumes a finite uniformly local initial $L^2$ bound at
one radius $R$ and obtains, for a short interval of length comparable to
$R^2$, a bound on

\[
 \operatorname*{ess\,sup}_t\sup_{x_0}\int_{B_R(x_0)}|u(t)|^2
 +\sup_{x_0}\int\!\!\int_{B_R(x_0)}|\nabla u|^2.
 \tag{3.3}
\]

Theorem 3.1 additionally assumes $u_0\in L^m(B_2)$ with $m>3$ and bounded
local $L^m$ norm. After splitting off a compactly supported $L^m$ mild
solution $a$, it proves short-time Hölder control of $u-a$ in a smaller
cylinder.

**Match and gap.** These are genuinely local-in-space estimates and can be
translated to a chosen good center. Their controlled quantities are velocity
energy and dissipation at a selected radius, not a square sum over a nested
fine-scale chain of filtered vorticity moments. The regularity theorem also
uses the additional subcritical local $L^m$ hypothesis.

### 3.5 Bradshaw--Tsai: local energy in Wiener amalgam spaces

**Source.** Zachary Bradshaw and Tai-Peng Tsai,
[Local energy solutions to the Navier--Stokes equations in Wiener amalgam
spaces](https://arxiv.org/pdf/2008.09204), 2020, Definition 1.1 and Theorem
1.4.

**Exact hypotheses and object.** Theorem 1.4 assumes divergence-free
$u_0\in E_q^2$, $2\le q<\infty$, and a local energy solution in the stated
$LE_q$ class. At each $R\ge1$ it bounds the $\ell^{q/2}$ norm over lattice
centers $k\in\mathbb Z^3$ of

\[
 \sup_{0\le t\le T}\int_{B_R(Rk)}|u(x,t)|^2\,dx
 +\int_0^T\int_{B_R(Rk)}|\nabla u|^2\,dx\,dt,
 \tag{3.4}
\]

with the explicit $R^{3-6/q}$ growth and the time range stated in the
theorem.

**Match and gap.** The discrete index in (3.4) labels different spatial
centers at one scale. In (1.1), it labels different fine scales at one fixed
center. The theorem is therefore an amalgam estimate in the wrong discrete
direction; it also controls velocity energy once, not a squared quadratic
vorticity moment with nested time windows.

### 3.6 Eyink--Aluie: smooth coarse-graining and band-energy budgets

**Source.** Gregory L. Eyink and Hussein Aluie,
[Localness of energy cascade in hydrodynamic turbulence, I. Smooth
coarse-graining](https://arxiv.org/pdf/0909.2386), 2009, equations (1)--(11)
and (20)--(24).

**Exact hypotheses and object.** For a smooth, normalized, sufficiently
decaying convolution kernel $G$, the paper defines

\[
 u_\ell=G_\ell*u,
 \qquad
 \tau_\ell(u,u)=(u\otimes u)_\ell-u_\ell\otimes u_\ell,
 \qquad
 \Pi_\ell=-\nabla u_\ell:\tau_\ell(u,u).
\]

Equations (4), (7), and (9) are the corresponding large-scale,
small-scale, and band-energy budgets. For a geometric sequence and an
S-type smooth filter, equation (11) gives a positive global band-energy
decomposition that converges for finite total $L^2$ energy. The scale-locality
bounds (23)--(24) additionally use inertial-range velocity-increment/Besov
scaling with $0<\sigma_p<1$; comparison to the total mean flux also assumes
that mean flux is nonzero.

**Match and gap.** Equation (11) is a real positive, global, first-power
$\ell^1$ band-energy statement available from $L^2$ data. It does not
localize at a fixed center by compact cutoffs, does not include common-top
time windows, and does not give the negative-weight $\ell^2$ expression in
(1.1). Applying the algebra to vorticity at almost every time would still
provide only a quantity linear in enstrophy; squaring it requires additional
time or spatial integrability.

### 3.7 Cheskidov--Constantin--Friedlander--Shvydkoy: LP flux locality

**Source.** Alexey Cheskidov, Peter Constantin, Susan Friedlander, and Roman
Shvydkoy,
[Energy conservation and Onsager's conjecture for the Euler equations](https://arxiv.org/pdf/0704.0759),
2007, equation (10), Proposition 3.2, Theorem 3.3, and Proposition 4.3.

**Exact hypotheses and object.** The global Fourier Littlewood--Paley energy
flux is

\[
 \Pi_Q=\int_{\mathbb R^3}
 \operatorname{Tr}\!\left[S_Q(u\otimes u)\cdot\nabla S_Qu\right]dx.
\]

Proposition 3.2 bounds it by

\[
 |\Pi_Q|\lesssim (K*d^2)^{3/2}(Q),
 \qquad
 d_q=2^{q/3}\|\Delta_qu\|_3.
 \tag{3.5}
\]

Theorem 3.3 obtains energy conservation for weak Euler solutions in
$L_t^3B^{1/3}_{3,c(\mathbb N)}\cap C_wL_x^2$. Proposition 4.3 treats
enstrophy flux in two space dimensions and again uses $L^3$-based
Littlewood--Paley vorticity coefficients.

**Match and gap.** The estimate is global in space, localized in frequency,
and based on $L^3$/Besov information. Leray energy and dissipation do not
directly give the endpoint coefficient sequence in (3.5). The enstrophy
statement is two-dimensional, not a three-dimensional fixed-center
vorticity-moment theorem.

### 3.8 Kovač--Zorin-Kranich: variation of martingale paraproducts

**Source.** Vjekoslav Kovač and Pavel Zorin-Kranich,
[Variational estimates for martingale paraproducts](https://arxiv.org/pdf/1812.09763),
2019, equation (1.4) and Theorem 1.1.

**Exact hypotheses and object.** Let $f$ and $g$ be martingales with respect
to the same filtration. For $p,q\in(1,\infty)$,
$r\in(1/2,\infty)$, and $1/p+1/q=1/r$, the truncated paraproduct is

\[
 \Pi_{n,n'}(f,g)=\sum_{n<i<j\le n'}df_i\,dg_j.
\]

Theorem 1.1 bounds its strong $\varrho$-variation for every
$\varrho\in(1,\infty)$, as well as its jump-counting function, in $L^r$ by
$\|f\|_{L^p}\|g\|_{L^q}$.

**Match and gap.** This extends the bilinear variation mechanism beyond the
dyadic/LP setting in the R0.70H baseline, but it still requires genuine
conditional expectations for one common filtration. Smooth dilated physical
cutoffs and filters are not conditional expectations. Moreover,
$\Pi_{n,n'}$ is an off-diagonal paraproduct; it omits the diagonal quadratic
term, the changing spatial cutoff, the discarded time slab, and the
$r_k^{-3}$ weight in (1.1).

## 4. Why the two occurrences of $r^{-3}$ are not the same norm

In three spatial dimensions, the parabolic $T^{\infty,2}$ norm has the
schematic form

\[
 \|F\|_{T^{\infty,2}}^2
 =\sup_{x_0,r>0}r^{-3}
 \int_{t_0-r^2}^{t_0}\int_{B_r(x_0)}|F(x,t)|^2\,dx\,dt,
 \tag{4.1}
\]

after an inessential time translation. The $r^{-3}$ factor normalizes the
volume of the spatial ball. Crucially, (4.1) squares the field first and then
integrates it in space.

The target (1.1) instead contains terms of the form

\[
 \int r_k^{-3}
 \left|\int \chi_k(x)(x-x_0)^{\otimes n}
 \otimes\Omega_k(x,t)\otimes\Omega_k(x,t)\,dx\right|^2dt,
 \tag{4.2}
\]

up to the critical factor $r_k^{1-n}$ and the exact adjacent-scale
combination. It integrates a quadratic field in space first and then squares
the resulting tensor.

For $n=0,1$, compact support and the critical normalization give the direct
size estimate

\[
 |m_k^{(n)}(t)|
 \lesssim r_k E_k(t),
 \qquad
 E_k(t):=\int_{B_{Cr_k}(x_0)}|\Omega_k(x,t)|^2\,dx.
 \tag{4.3}
\]

Consequently, a direct absolute-value estimate for a slab term in (1.1)
encounters

\[
 r_k^{-3}|m_k^{(n)}|^2
 \lesssim r_k^{-1}E_k(t)^2
 \lesssim r_k^2
 \int_{B_{Cr_k}(x_0)}|\Omega_k(x,t)|^4\,dx.
 \tag{4.4}
\]

Thus the apparent equality of the exponent $-3$ in (4.1) and (4.2) is only
notational. The direct route to (4.2) is fourth order in vorticity and also
retains a scale sum. Standard tent control is second order in the spacetime
field.

For a Leray solution,

\[
 u\in L_t^\infty L_x^2\cap L_t^2\dot H_x^1,
 \qquad
 \omega\in L^2_{t,x},
\]

so the enstrophy density is only globally $L^1$ in spacetime. This does not
give an $L_t^2$ bound for $E_k(t)$, a normalized local-enstrophy Carleson
bound, or a generic $L^4$ vorticity estimate. Possible signed cancellation
in the fine-window difference must therefore be proved before squaring; it
cannot be replaced by (4.4) without adding stronger hypotheses.

## 5. Closest partial bridges and their exact boundary

The audit identifies three legitimate partial tools, but none closes
$\mathcal Q_{\rm core}$.

1. **Heat/tent propagation.** Auscher--Monniaux--Portal can propagate an
   already available tent norm through a linear maximal-regularity operator.
   Auscher--Frey can propagate the stronger collection (3.1) through the NSE
   Duhamel bilinear map. Neither paper derives those nonlinear source norms
   from Leray energy.
2. **Carleson times total mass.** Germain--Pavlović--Staffilani Lemma 3.1
   would use the globally available $\int|\omega\otimes\omega|$, but it also
   requires the unavailable local Carleson factor $A(\omega\otimes\omega)$.
   This is a precise restatement of the local-concentration gap, not a
   closure.
3. **Scale decomposition.** Eyink--Aluie gives a positive global
   band-energy decomposition, while Do--Muscalu--Thiele from the R0.70H
   baseline and Kovač--Zorin-Kranich give bilinear variation for genuine
   frequency or martingale paraproduct blocks. These mechanisms may address
   an exactly isolated off-diagonal LP component. They do not cover the
   diagonal vorticity square, physical-cutoff commutator, common-top slab, or
   negative scale weight.

It would therefore be inaccurate to cite any of these results as an
energy-only theorem for (1.1). At most they justify a future conditional
lemma or one rigorously isolated component of the R0.70I decomposition.

## 6. Stop rule and absence-claim boundary

The search used the following stopping rule.

- First, inspect the R0.70H eight-source baseline and do not count it again.
- Then cover each remaining mechanism by a primary theorem or exact
  definition: parabolic maximal regularity, NSE bilinear tent estimates,
  local energy/physical-scale flux, and bilinear variation.
- Stop after eight new high-signal sources once every subsequent candidate
  repeats an already documented mismatch: wrong field, wrong integration
  order, wrong discrete index, extra critical/Besov/Carleson hypothesis, or
  absence of the physical cutoff and nested-window ledger.

Accordingly, the defensible conclusion is:

> **No theorem matching the complete fixed-center $r_k^{-3}$
> changing-cutoff quadratic vorticity-moment pairing was found in this
> bounded primary-source audit.**

This sentence records the outcome of a deliberately finite search. It does
not prove that no such theorem appears elsewhere, that no equivalent theorem
can be reformulated to apply, or that an energy-only estimate is impossible.
Any stronger absence claim would require a substantially broader systematic
review or an independent mathematical obstruction.
