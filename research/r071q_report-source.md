# R0.71Q -- Quantitative complex-time windows give only an anchor- and truncation-taxed entry bound

**Date:** 2026-08-26

**Audience:** analysts working on three-dimensional incompressible
Navier--Stokes regularity, complex-time analyticity, localized
Littlewood--Paley observables, Jensen zero counts, and temporal packing

**Status:** release source.  This report proves a finite conditional
parabolic-window Jensen theorem, extracts an explicit two-sided disk from
Temam's complex-time lobe, proves two exact analytic counterfamilies, and
classifies the direct zero-count route.  It proves no uniform Navier--Stokes
zero count, infinite-frame estimate, continuation criterion, singularity,
global regularity, novelty, priority, or Millennium-problem result.

## 0. Direct decision

R0.71P reduced the fixed-partition positive-entry target to

\[
 \mathsf S_{\Lambda,+}(K)
 \le \int_K \mathcal H(t)\,d\mathfrak n_\Lambda(t),
 \qquad
 \mathcal H(t)=M_\chi C_T
 \frac{\|L(t)\|_{\dot H^{-1}}^2}{Y(t)},
 \tag{0.1}
\]

where \(\mathfrak n_\Lambda\) counts distinct entry times and already groups
all simultaneous shell--cell entries into one spatial batch.  R0.71Q asks
whether complex-time analyticity can pay this remaining temporal measure.

The exact decision is:

1. on a fixed compact classical interval and for a fixed finite truncation,
   Temam's construction gives a quantitative complex-time disk and an upper
   complex norm;
2. a finite ownership cover and Jensen's formula then give a rigorous bound
   for \(\mathsf S_{\Lambda,+}(K)\);
3. the bound necessarily contains four ledgers: analytic radius, complex
   growth, a nonzero observable anchor, and the cover;
4. taking the union over shell--cell observables adds a fifth ledger: the
   component/truncation sum;
5. the weighted target also needs a windowwise pointwise envelope for
   \(\mathcal H\); a zero count alone does not convert counting measure to
   Leray-time measure;
6. Temam's radius is proportional to
   \((1+\sup\|u\|_{H^1}^2)^{-2}\), so endpoint-uniform coverage already asks
   for a three-dimensional strong continuation norm;
7. finite Blaschke products prove that radius and complex upper norm alone
   cannot control even the distinct real zero count or the upward-crossing
   count: the anchor decays exponentially and its Jensen logarithm is sharp;
8. a second analytic family proves that uniformly controlled individual
   observables can have a zero-set union growing linearly with the number of
   observables.

Therefore the direct complex-time zero-count branch remains a **conditional
finite theorem** and stops here.  A useful next step must introduce genuinely
Navier--Stokes-specific coupling between entry events, not another use of
qualitative analyticity.

## 1. Interface inherited from R0.71P

On the normalized periodic torus, let \(u\) be a nontrivial zero-mean
classical solution, let \(\omega=\operatorname{curl}u\), and put

\[
 Y=\|\omega\|_2^2,
 \qquad L=\mathbb P(u\times\omega),
 \qquad F_j=T_jL,
 \tag{1.1}
\]

\[
 C_\alpha(t)
 =C_{j,Q}(t)
 =\operatorname{curl}(\chi_QT_j\omega(t)),
 \qquad \alpha=(j,Q).
 \tag{1.2}
\]

For a finite truncation \(\Lambda\), let \(\mathcal T_\Lambda(K)\) be the
distinct times at which at least one component has a positive right-entry
atom.  R0.71P proved

\[
 \mathsf e_\Lambda(t)
 =\sum_{\alpha\text{ entering at }t}
 \kappa_j^{-2}A_{\alpha,+}(t)
 \le \mathcal H(t),
 \tag{1.3}
\]

and hence (0.1).  Every positive entry is a vector zero of at least one
\(C_\alpha\), but not every vector zero is a positive entry.  Counting all
component zeros is therefore a valid upper bound.

The half-open convention \(K=[a,b)\) remains fixed: a zero at \(a\) may be
owned by the cover, while \(b\) is excluded.

## 2. The scalar and Hilbert-valued Jensen gate

Let \(C:D(t_*,R)\to H_{\mathbb C}\) be strongly holomorphic, with

\[
 \sup_{D(t_*,R)}\|C(z)\|_H\le M,
 \qquad C(t_*)\ne0.
 \tag{2.1}
\]

Complex Hahn--Banach supplies a norm-one functional \(\ell\) with
\(\ell(C(t_*))=\|C(t_*)\|\).  The scalar function \(f=\ell\circ C\) has
every vector zero of \(C\) as a scalar zero, while
\(|f(t_*)|=\|C(t_*)\|\).  Jensen's formula therefore gives, for
\(0<r<R\),

\[
 \boxed{
 N_C(D(t_*,r))
 \le
 \frac{\log\!\left(M/\|C(t_*)\|_H\right)}
 {\log(R/r)}.}
 \tag{2.2}
\]

The left side counts distinct vector zeros.  The scalar Jensen count uses
multiplicity and is at least as large.  Since that scalar count is an integer,
(2.2) also gives the integer capacity

\[
 N_C(D(t_*,r))
 \le
 \left\lfloor
 \frac{\log(M/\|C(t_*)\|_H)}{\log(R/r)}
 \right\rfloor.
 \tag{2.2a}
\]

A strict inner--outer radius margin is essential: the denominator degenerates
as \(r\uparrow R\).  Formula (2.2) counts the open inner disk.  If a later
ownership convention permits a zero on its inner boundary, one must enlarge
the counting radius to some \(r'<R\), or use the corresponding closed-disk
limit; a counting-measure atom cannot be discarded as a Lebesgue-null
boundary point.

Moving the base point by a disk automorphism changes the anchor but does not
remove it.  Poisson--Jensen instead gives a sum of Green weights

\[
 \sum_{f(a)=0}\log\frac1{|\phi_{t_*}(a)|}
 \le \log\frac{M}{|f(t_*)|}.
 \tag{2.3}
\]

Thus Cartan estimates, disk automorphisms, and Blaschke factorization cannot
create an anchor-free zero count.

## 3. A quantitative disk from Temam's complex-time lobe

For the unforced periodic equation, Temam's Chapter 7 construction starts at
a real time \(\tau\) with \(u(\tau)\in V\) and gives the lobe

\[
 \Delta(u(\tau))
 =\left\{se^{i\theta}:
 0<s<|\cos\theta|^3T_1(\|u(\tau)\|_V),\ |θ|<\frac\pi2\right\},
 \tag{3.1}
\]

\[
 T_1(R)=\frac{K_\nu}{(1+R^2)^2},
 \tag{3.2}
\]

and on that lobe

\[
 \sup_{z\in\tau+\Delta(u(\tau))}\|u(z)\|_V^2
 \le 2(1+\|u(\tau)\|_V^2).
 \tag{3.3}
\]

The constants depend on viscosity and the periodic domain.  These formulas
are Temam's (7.8)--(7.12), restarted at \(\tau\).

Set \(T=T_1(R)\).  Writing \(se^{i\theta}=x+iy\), the lobe condition is

\[
 (x^2+y^2)^2<x^3T,\qquad x>0.
 \tag{3.4}
\]

The exact rational audit proves

\[
 \boxed{D(T/4,T/64)\subset\Delta_R.}
 \tag{3.5}
\]

Indeed, after setting \(T=1\), every point of that disk satisfies

\[
 x\ge\frac{15}{64},\quad
 x^2+y^2\le\frac{290}{4096},
 \tag{3.6}
\]

and

\[
 \left(\frac{290}{4096}\right)^2
 <\left(\frac{15}{64}\right)^3.
 \tag{3.7}
\]

Consequently, starting at \(\tau=t_*-T/4\) gives a genuine two-sided disk
\(D(t_*,T/64)\) around the real center \(t_*\).

### 3.1 Strong-space upper bound for the filtered observable

Temam's (7.17) also bounds \(Au\) on compact subsets of the lobe.  The
smaller disk \(D(t_*,T/128)\) has distance at least \(T/128\) from the
boundary of the certified disk (3.5), so in the unforced case

\[
 \sup_{D(t_*,T/128)}\|Au(z)\|_2
 \le
 C_\nu(1+R^2)^{3/2}
 +\frac{1024}{\sqrt{\lambda_1}T}(1+R^2)^{1/2}
 =:\mathcal D(R,T).
 \tag{3.8}
\]

For each fixed shell--cell index, the map

\[
 \mathcal O_\alpha u
 =\operatorname{curl}(\chi_QT_j\operatorname{curl}u)
 \tag{3.9}
\]

is bounded from \(D(A)\) to \(L^2\).  Hence

\[
 M_\alpha
 :=\|\mathcal O_\alpha\|_{D(A)\to L^2}\mathcal D(R,T)
 \tag{3.10}
\]

is a valid complex-disk upper bound for \(C_\alpha\).  This is finite for
every fixed \(\alpha\), but its operator factor need not be uniform over all
shells and cells.

## 4. Conditional parabolic-window packing theorem

Let \(K=[a,b)\Subset I_{\rm strong}\), choose \(\delta>0\) with

\[
 K^\sharp=[a-\delta,b+\delta]\Subset I_{\rm strong},
 \qquad
 R_\sharp=\sup_{t\in K^\sharp}\|u(t)\|_V,
 \tag{4.1}
\]

and define

\[
 T_\sharp
 =\min\left\{\delta,
 \frac{K_\nu}{(1+R_\sharp^2)^2}\right\},
 \quad
 R_o=\frac{T_\sharp}{128},
 \quad r_i=\frac{T_\sharp}{256}.
 \tag{4.2}
\]

Remove every \(C_\alpha\) that is identically zero on the connected strong
interval; it has no entry.  For finite \(\Lambda\), the union of the zero
sets of the remaining components is finite on \(K^\sharp\).  One may
therefore choose real centers \(t_m\), avoiding that union, whose inner
intervals \((t_m-r_i,t_m+r_i)\) cover \(K\).  Concretely, place the first
and last grid centers \(r_i/4\) beyond the two endpoints of \(K\), and use
equally spaced intermediate centers with spacing at most \(r_i/2\).  Perturb
each center by less
than \(r_i/8\) to avoid the finite forbidden zero set.  Consecutive centers
remain less than \(3r_i/4\) apart, the endpoint margins remain positive, and
the open inner intervals still cover the whole closure \([a,b]\).  This
construction gives

\[
 J\le 2+\left\lceil\frac{512|K|}{T_\sharp}\right\rceil.
 \tag{4.3}
\]

Let \(K_m\) be an exact pointwise ownership partition subordinate to these
intervals: explicitly,

\[
 K=\mathop{\dot\bigcup}_{m=1}^{J}K_m,
 \qquad
 K_m\subset(t_m-r_i,t_m+r_i),
 \tag{4.3a}
\]

with each \(K_m\) Borel.  This is not merely an almost-everywhere partition.
Thus a possible atom at \(a\) is assigned once, \(b\) remains excluded by the
half-open convention, every internal ownership boundary is assigned to one
set, and every owned zero lies strictly inside its Jensen inner disk.  Put

\[
 H_m=
 \begin{cases}
 \sup_{t\in K_m}\mathcal H(t),&K_m\ne\varnothing,\\
 0,&K_m=\varnothing,
 \end{cases}
 \qquad
 a_{\alpha m}=\|C_\alpha(t_m)\|_2>0.
 \tag{4.4}
\]

The empty-set convention is needed because an arbitrary subordinate
ownership partition may contain unused windows.  For nonempty \(K_m\), the
quantity \(H_m\) is finite on the declared compact classical neighborhood:
the nontrivial solution has \(Y>0\), and \(\mathcal H\) is continuous there.

For every pair \((\alpha,m)\), define the integer Jensen capacity

\[
 J_{\alpha m}
 =\left\lfloor
 \frac{\log(M_\alpha/a_{\alpha m})}{\log2}
 \right\rfloor.
 \tag{4.5}
\]

At each distinct entry time, choose one entering component as its witness in
addition to its unique owned window.  This produces disjoint sets of times
indexed by \((\alpha,m)\).

### Theorem 4.1 -- finite anchor-taxed entry packing

With the preceding definitions,

\[
 \boxed{
 \mathsf S_{\Lambda,+}(K)
 \le
 \sum_{m=1}^{J}H_m
 \sum_{\alpha\in\Lambda^*}J_{\alpha m}
 \le
 \frac1{\log2}\sum_{m=1}^{J}H_m
 \sum_{\alpha\in\Lambda^*}
 \log\frac{M_\alpha}{a_{\alpha m}}.}
 \tag{4.6}
\]

Here \(\Lambda^*\) contains the non-identically-zero components.

#### Proof

Every entry time owned by \(K_m\) is a zero of at least one component in
\(D(t_m,r_i)\).  After choosing one entering witness component, let
\(\mathcal T_{\alpha m}\) contain the times assigned to \((\alpha,m)\).
Then

\[
 \mathcal T_\Lambda(K)\cap K_m
 =\mathop{\dot\bigcup}_{\alpha\in\Lambda^*}
 \mathcal T_{\alpha m},
 \tag{4.7a}
\]

and each \(\mathcal T_{\alpha m}\) is a set of distinct vector zeros of
\(C_\alpha\) in the open inner disk.  Formula (2.2a), with
\(R_o/r_i=2\), gives

\[
 \#(\mathcal T_\Lambda(K)\cap K_m)
 \le\sum_{\alpha\in\Lambda^*}J_{\alpha m}.
 \tag{4.7}
\]

At each owned time, R0.71P gives \(\mathsf e_\Lambda(t)\le H_m\).  Therefore

\[
 \begin{aligned}
 \mathsf S_{\Lambda,+}(K)
 &=\sum_{m=1}^{J}
   \sum_{t\in\mathcal T_\Lambda(K)\cap K_m}
   \mathsf e_\Lambda(t)\\
 &\le\sum_{m=1}^{J}H_m
   \#(\mathcal T_\Lambda(K)\cap K_m)\\
 &\le\sum_{m=1}^{J}H_m
   \sum_{\alpha\in\Lambda^*}J_{\alpha m}.
 \end{aligned}
 \tag{4.8}
\]

Finally, \(J_{\alpha m}\le
\log(M_\alpha/a_{\alpha m})/\log2\), and all \(H_m\) are nonnegative,
which proves the second inequality in (4.6). \(\square\)

A direct sum \(\bigoplus_\alpha C_\alpha\) cannot replace the witness
construction: it vanishes at the intersection, not the union, of component
zero sets.  A product of windowwise norming scalarizations has a zero set
that contains the component union and may contain additional projection
zeros.  The finite tensor product \(\bigotimes_\alpha C_\alpha\) has exactly
the component union as its vector zero set.  Neither construction removes
the loss: its center anchor is the product of the component anchors, the
available product upper bound gives exactly the sum of logarithmic taxes in
(4.6), and simultaneous component zeros acquire summed order.

The theorem is quantitative and finite.  It does not say that its right-hand
side is controlled by Leray data.

## 5. Exact anchor obstruction: a rational Blaschke family

For \(N\ge1\), define the distinct rational zeros

\[
 a_{N,k}=\frac{2N^2-k}{4N^2},
 \qquad k=1,\ldots,N,
 \tag{5.1}
\]

and

\[
 B_N(z)=\prod_{k=1}^N\frac{z-a_{N,k}}{1-a_{N,k}z}.
 \tag{5.2}
\]

All zeros lie in \([1/4,1/2)\), with the endpoint \(1/4\) occurring only
when \(N=1\).  Every factor maps the
unit disk into itself and has unit modulus on the boundary, so

\[
 \|B_N\|_{H^\infty(\mathbb D)}=1.
 \tag{5.3}
\]

The center anchor is

\[
 |B_N(0)|=\prod_{k=1}^Na_{N,k}.
 \tag{5.4}
\]

Since \(a_{N,k}=\frac12(1-k/(2N^2))\),

\[
 N
 \le \frac{\log(1/|B_N(0)|)}{\log2}
 \le N+\frac1{\log2}.
 \tag{5.5}
\]

The left side is exactly the number of distinct real zeros in
\(D(0,1/2)\); thus the Jensen anchor logarithm is sharp up to an additive
constant independent of \(N\).

Along the real axis, derivative signs alternate.  Exactly
\(\lceil N/2\rceil\) zeros have positive derivative.  Therefore, for a unit
Hilbert vector \(e\), \(C_N(z)=B_N(z)e\) has a fixed analytic radius, fixed
complex norm, and an unbounded number of simple real zeros and upward
crossings.

For direct compatibility with the R0.71P positive-entry definition, take

\[
 \widetilde C_N(z)=B_N(z)^2e,
 \qquad F=e,\qquad Y=1.
 \tag{5.6}
\]

Every zero is now even order, its leading direction is a positive multiple
of \(e\), and all \(N\) zeros have \(A_+=1\).  The complex norm remains one;
the center anchor is merely squared.  Hence analytic radius and upper growth
alone allow arbitrarily many abstract positive entries, not only unsigned
zeros.  This remains an analytic Hilbert path, not an NSE repeated-face
construction.

This proves a method impossibility:

> No zero-count or upward-crossing bound can depend only on a common complex
> radius and a common complex upper norm.  A quantitative lower anchor, or a
> genuinely stronger dynamical input, is necessary.

The family is analytic, not a Navier--Stokes solution trajectory.

## 6. Exact component-union obstruction

The anchor obstruction is not the only loss.  For \(q=1,\ldots,Q\), take

\[
 g_q(z)=z-b_q,
 \qquad b_q\in(1/4,1/2)
 \tag{6.1}
\]

with distinct \(b_q\).  On \(D(0,1)\),

\[
 \sup|g_q|<\frac32,
 \qquad |g_q(0)|>\frac14,
 \tag{6.2}
\]

uniformly in \(q\).  Each component has one simple positive-derivative real
zero in \(D(0,3/4)\), but the union has exactly \(Q\) distinct zeros.

Thus even uniform per-component radius, norm, and anchor bounds do not
control the union independently of \(|\Lambda|\).  Summing component Jensen
bounds pays \(|\Lambda|\).  Replacing the sum by the product
\(\prod_\alpha f_\alpha\) pays the same tax through a product anchor, whose
logarithm is the sum of the component logarithms.  A direct-sum vector does
not help: a component zero is generally not a zero of the full direct-sum
vector.

This is precisely the union operation required by distinct entry times.
R0.71P removed simultaneous spatial multiplicity only after an entry time was
given; it did not couple the zero sets at different times.

### 6.1 A separate window-cover obstruction

On \(K=[0,1)\), set

\[
 C_N(z)=\left(\frac{\sin(\pi Nz)}{\pi N}\right)^2e,
 \qquad F=e,\qquad Y=1.
 \tag{6.3}
\]

The \(N\) points \(k/N\), \(k=0,\ldots,N-1\), are even-order positive
entries with \(A_+=1\).  Give the \(m\)-th entry the owned cell
\(E_m=[m/N,(m+1)/N)\), center
\(c_m=(m+1/2)/N\), outer radius \(3/(4N)\), and inner radius
\(5/(8N)\).  Then the radius ratio is \(6/5\), and

\[
 \frac{M_m}{\|C_N(c_m)\|}
 \le\cosh^2(3\pi/4)
 \tag{6.4}
\]

uniformly in \(m\) and \(N\).  Nevertheless, the exact ownership cover has
\(N\) windows.  Thus locally uniform radius ratio, relative growth, and
anchor do not pay the global count; the cover cardinality is an independent
ledger.  Merging the windows transfers the same cost into global complex
growth.

## 7. Why the four NSE ledgers are not paid

### 7.1 Radius and cover

The inverse Temam scale is

\[
 T_\sharp^{-1}
 \gtrsim K_\nu^{-1}(1+R_\sharp^2)^2.
 \tag{7.1}
\]

Since \(R_\sharp^2=\sup Y\) up to the periodic norm equivalence, the finite
cover (4.3) uses a strong \(L_t^\infty H_x^1\) continuation-scale quantity.
Leray controls \(\int Y\,dt\), not \(\sup Y\) or
\(\int(1+Y)^2dt\).  The exact pulse

\[
 Y_N(t)=N(1-Nt)_+
 \tag{7.2}
\]

has \(\int_0^1Y_Ndt=1/2\) while
\(\int_0^1Y_N^2dt=N/3\).  This is an abstract budget separation, not an NSE
trajectory, but it proves that an \(L^1\) enstrophy bound cannot by itself pay
the generic inverse-window density.

If a common complex radius and corresponding strong bound remained uniform
as \(K\uparrow T^*\), the local strong theory would continue the solution
past \(T^*\).  Endpoint-uniform radius control is therefore already a
continuation result.

### 7.2 Complex growth

Formula (3.10) pays the upper complex norm only after fixing a strong window
and one operator \(\mathcal O_\alpha\).  It contains both \(T_\sharp^{-1}\)
and the shell--cell operator norm.  This is valid finite data, not a uniform
all-frame estimate.

### 7.3 Projection anchor

Energy and enstrophy are upper norms of the full field.  The localized
filtered map \(\mathcal O_\alpha\) has a nontrivial kernel and admits
cancellation.  R0.71P already contains a smooth NSE initial jet with

\[
 Y(0)=1,
 \qquad C_\alpha(0)=0,
 \qquad C_{\alpha,t}(0)\ne0.
 \tag{7.3}
\]

Thus no positive lower bound for \(\|C_\alpha(t)\|\) can follow from the
total enstrophy at a prescribed time.  Choosing cover centers away from zeros
makes every finite anchor positive, but gives no uniform quantitative lower
bound as the truncation, solution, or endpoint varies.

### 7.4 Component union

The sum over \(\alpha\) in (4.6) is not a proof artifact removable by one
norming functional.  Section 6 proves an exact analytic union obstruction.
Removing it would require a new PDE statement coupling the zero sets of all
localized observables.

### 7.5 Pointwise batch envelope

Even a closed zero count controls only \(\#\mathcal T_\Lambda\).  The target
is weighted by \(\mathcal H(t)\), so (4.6) additionally pays
\(H_m=\sup_{K_m}\mathcal H\).  Leray estimates ordinary time integrals of
related quantities, not their supremum at an atomic event set.  Uniform
control of this envelope near a potential singular endpoint is another
strong, presently unpaid input.

## 8. Primary-source boundary

1. [Temam, Chapter 7](https://epubs.siam.org/doi/10.1137/1.9781611970050.ch7),
   especially (7.8)--(7.12), (7.17), and (7.24)--(7.25), gives the
   complex-time lobe, its strong-space bound, and restart on classical
   intervals.  Its scale depends on a strong \(V\)-norm.
2. [Jensen's 1899 paper](https://doi.org/10.1007/BF02417878) supplies the
   disk zero formula.  It contains the center value rather than eliminating
   it.
3. [Blaschke's 1915 paper](https://archiv.saw-leipzig.de/saw-archive/publikationen-quellen/publikationen/berichte-ueber-die-verhandlungen-der-koeniglich-saechsischen-gesellschaft-der-wissenschaften-zu-leipzig-mathematisch-physische-klasse-bd-1/berichte-ueber-die-verhandlungen-der-koeniglich-saechsischen-gesellschaft-der-wissenschaften-zu-leipzig-mathematisch-physische-klasse-bd-67/eine-erweiterung-des-satzes-von-vitali-ueber-folgen-analytischer-funktionen)
   and the modern [finite-product survey](https://arxiv.org/abs/1512.05444)
   give the bounded analytic zero factors used in Section 5.
4. [Giga--Jo--Mahalov--Yoneda](https://doi.org/10.1016/j.physd.2008.03.007)
   construct explicit complex-time sectors for almost-periodic data and prove
   that a Fourier mode cannot be suddenly created.  They do not bound
   repeated zeros or the union over modes.
5. [Dong--Zhang](https://doi.org/10.1016/j.jfa.2020.108563) prove
   \(t^n\|\partial_t^nu\|_\infty\le N^{n+1}n^n\) for bounded mild
   solutions.  The resulting radius depends on the assumed strong
   \(L^\infty\) bound and supplies no filtered-observable anchor.
6. [Wang--Gao--Xue](https://doi.org/10.1016/j.jmaa.2022.126428) prove joint
   space--time derivative estimates for \(L^3\) mild solutions; time-uniform
   constants occur in the already global small-data class.
7. [Masuda](https://doi.org/10.3792/pja/1195521421) proves analyticity and
   unique continuation when the complete velocity field vanishes on a
   spatial open set.  A localized filtered observable lying in an operator
   kernel is outside that hypothesis.

Two bounded, disconfirming primary-source searches through 2026-08-26 found
no theorem paying the lower anchor, the component-union tax, or the full
R0.71P entry-time measure from Leray data.  This is a bounded negative
finding, not a claim of nonexistence, originality, or priority.

## 9. Exact and independent audits

The exact producer certifies:

1. the rational inclusion (3.5)--(3.7);
2. seven Blaschke cases \(N=1,2,4,8,16,32,64\), including exact rational
   anchors, derivative-sign counts, and the squared positive-entry variant;
3. seven component-union cases with uniform individual data;
4. the locally uniform sine-square cover family;
5. the exact \(L^1\)-versus-inverse-window pulse ledger.

The independent checker uses 8,192 boundary samples for every Blaschke
product, verifies the prescribed zeros and anchor product, tests 200,000
random points in the extracted lobe disk, and reconstructs the component and
covering costs without importing the exact producer.  No PDE time evolution
is performed.

## 10. Research value and next interface

R0.71Q does not close temporal packing.  Its value is a sharp method
classification:

\[
 \boxed{
 \text{complex-time analyticity}
 +\text{upper growth}
 \not\Rightarrow
 \text{uniform entry-time packing}.}
 \tag{10.1}
\]

The missing information is not one vague constant.  It consists of a
continuation-scale cover, a lower observable anchor, a coupling law for the
union of zero sets, and a pointwise bound for the entry-batch weight.  The
Blaschke, sine-square, and linear-observable families prove that the anchor,
cover, and union taxes cannot be removed within abstract holomorphic function
theory.

The next finite gate is R0.71R: test an NSE-specific parabolic incidence or
Carleson packing law for entry events, using the signed precursor/source
before componentwise positive parts are selected.  Any candidate must be
checked against the R0.71P sequential path, the R0.71Q anchor family, and the
all-observable union tax.

## 11. Claim boundary

**Proved:** the finite conditional theorem (4.6), an explicit Temam-lobe
disk, an asymptotically sharp anchor obstruction, a uniform-data
component-union obstruction, and an independent numerical audit.

**Not proved:** a uniform NSE temporal zero count, a quantitative lower
anchor, all-frame packing, an infinite-frame limit, a Leray-level source
bound, continuation, finite-time singularity, three-dimensional global
regularity, or any conclusion on the Millennium Problem.

The analytic counterfamilies are not NSE trajectories.  The use of Temam,
Jensen, and Blaschke is classical; no novelty or priority claim is made for
those ingredients.
