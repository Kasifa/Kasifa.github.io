# R0.71Q bounded primary-source audit

**Search date:** 2026-08-26  
**Question:** can quantitative complex-time analyticity pay the distinct
positive-entry times left by R0.71P, uniformly over localized observables,
truncations, and intervals approaching a possible singular endpoint?

## 1. Claim filters

A source was relevant only if it addressed at least one of these inputs:

1. an explicit complex-time radius for a three-dimensional NSE strong or
   mild solution;
2. an upper solution norm on the same complex domain;
3. a lower bound for a localized filtered observable at a real base point;
4. a temporal zero count, crossing count, or zero-set union estimate;
5. a cover uniform in the truncation or near a possible maximal endpoint.

Spatial analyticity alone, qualitative unique continuation for the complete
velocity field, and fixed-observable qualitative finiteness were not treated
as temporal packing results.

## 2. Wave one: direct quantitative sources

### Roger Temam, Chapter 7

- Source: [*Navier--Stokes Equations and Nonlinear Functional Analysis*,
  Chapter 7](https://epubs.siam.org/doi/10.1137/1.9781611970050.ch7).
- Theorem 7.1, pp. 51--56: a three-dimensional strong solution is
  (D(A))-valued analytic in a complex neighborhood of its classical
  interval.
- Formulas (7.8)--(7.12): from initial (V)-norm (R), the Galerkin
  complexification is bounded in the lobe
  
  \[
  0<s<|\cos\theta|^3T_1(R),
  \qquad T_1(R)=K_\nu(1+R^2)^{-2},
  \]
  
  with (sup\|u(z)\|_V^2\le2(1+R^2)).
- Formula (7.17): (Au) is bounded on compact subsets, with explicit
  dependence on viscosity, (R), and inverse distance to the lobe boundary.
- Formulas (7.24)--(7.25): the construction restarts at every classical
  time; a uniform real (V)-bound yields a uniform complex neighborhood.

**Ledger:** pays a radius and an upper complex norm on a classical window.
The radius is controlled by a strong (H^1) bound.  It gives no lower
filtered-observable anchor and no zero count by itself.

### Giga--Jo--Mahalov--Yoneda (2008)

- Source: [author-repository PDF](https://eprints.lib.hokudai.ac.jp/repo/huscap/all/69669/re860.pdf),
  [DOI 10.1016/j.physd.2008.03.007](https://doi.org/10.1016/j.physd.2008.03.007).
- Theorems 1.1--1.2 and the proof on pp. 12--13 construct a holomorphic
  solution in a complex sector (S(T_0,\sigma)), with
  (sup_S\|u(z)\|_X\le3\|u_0\|_X) under an explicit contraction condition
  proportional to (T_0^{1/2}\|u_0\|_X).
- Theorems 1.3--1.4: an almost-periodic Fourier amplitude is analytic, so a
  mode cannot be suddenly created after being identically absent.

**Ledger:** explicit domain and upper norm.  “No sudden creation” is an
identity-theorem statement; it does not bound repeated isolated zeros,
their spacing, or their union over modes.

### Dong--Zhang (2020)

- Source: [arXiv:1907.01687](https://arxiv.org/abs/1907.01687),
  [JFA DOI 10.1016/j.jfa.2020.108563](https://doi.org/10.1016/j.jfa.2020.108563).
- Theorem 3.1: for a bounded mild solution on
  ([0,1]\times\mathbb R^d),
  
  \[
  \sup_{0<t\le1}t^n\|\partial_t^nu(t)\|_\infty
  \le N^{n+1}n^n,
  \]
  
  with (N) depending on dimension and the assumed (L^\infty) bound.

**Ledger:** Cauchy--Hadamard gives a radius comparable to (t/N) and a
complex upper norm.  The assumed (L^\infty) control is already a strong
classical input; no observable anchor or temporal zero count is supplied.

### Wang--Gao--Xue (2022)

- Source: [author-repository PDF](https://ira.lib.polyu.edu.hk/bitstream/10397/94106/1/NS_Space_Time_Analyticity.pdf),
  [JMAA DOI 10.1016/j.jmaa.2022.126428](https://doi.org/10.1016/j.jmaa.2022.126428).
- Theorems 1.1 and 3.1 give joint derivative estimates of the form
  
  \[
  \|D_x^\beta\partial_t^ku(t)\|_{L^q}
  \le M^m m^m t^{-|\beta|/2-k-\mu_q}.
  \]
- Uniform-in-time constants occur in the already global small-(L^3)-data
  class; arbitrary data use a local existence interval.

**Ledger:** quantitative radius/growth for mild solutions.  No lower
projection anchor and no union-of-zero-sets theorem.

### Cong Wang (2026)

- Source: [arXiv:2503.03658](https://arxiv.org/abs/2503.03658),
  [JMP DOI 10.1063/5.0297339](https://doi.org/10.1063/5.0297339).
- Theorem 1.1 and Corollary 1.1 sharpen joint space--time analyticity for
  small critical Besov data, with a global relative time radius.

**Ledger:** marked as a 2026 small-data result.  It confirms that uniform
radius estimates are available in a class already known to be global; it
does not provide event packing for arbitrary large data.

## 3. Wave two: disconfirming and substitute searches

The second wave used combinations of:

- “Navier--Stokes temporal zeros quantitative count Fourier amplitude”;
- “filtered observable quantitative unique continuation time”;
- “Cartan lemma anchor-free zero count bounded analytic function”;
- “parabolic window zero packing Navier--Stokes”;
- “no sudden creation repeated zeros mode amplitude”;
- “complex-time analyticity singular endpoint uniform radius”.

### Masuda (1967)

- Source: [J-STAGE PDF](https://www.jstage.jst.go.jp/article/pjab1945/43/9/43_9_827/_pdf),
  [DOI 10.3792/pja/1195521421](https://doi.org/10.3792/pja/1195521421).
- Theorem 1 gives time analyticity; Theorem 2 gives unique continuation if
  the complete velocity field vanishes on a spatial open set at one time.

**Why it does not substitute:** (C_{j,Q}(t)=0) means that one localized
filtered image lies in an operator kernel.  It does not say that the full
velocity vanishes on any spatial open set.

### Jensen (1899) and Blaschke (1915)

- Sources: [Jensen, DOI 10.1007/BF02417878](https://doi.org/10.1007/BF02417878);
  [Blaschke archive](https://archiv.saw-leipzig.de/saw-archive/publikationen-quellen/publikationen/berichte-ueber-die-verhandlungen-der-koeniglich-saechsischen-gesellschaft-der-wissenschaften-zu-leipzig-mathematisch-physische-klasse-bd-1/berichte-ueber-die-verhandlungen-der-koeniglich-saechsischen-gesellschaft-der-wissenschaften-zu-leipzig-mathematisch-physische-klasse-bd-67/eine-erweiterung-des-satzes-von-vitali-ueber-folgen-analytischer-funktionen).
- Jensen's formula pays the center value explicitly.
- Finite Blaschke products have fixed unit-disk norm and arbitrarily
  prescribed finite zero sets.

**Why Cartan or recentering does not substitute:** moving the base point
changes the anchor; it does not remove the small-value ledger.  Blaschke
products supply an exact family with arbitrarily many clustered real zeros
and exponentially small center anchor.

### Foias--Temam spatial Gevrey regularity

- Source: [DOI 10.1016/0022-1236(89)90015-3](https://doi.org/10.1016/0022-1236(89)90015-3).

**Why it does not substitute:** spatial Fourier decay does not count time
zeros of localized physical-space observables and supplies no lower
projection value.

## 4. Source comparison matrix

| Source | Complex radius | Complex upper norm | Lower anchor | Zero count | All-filter union | Endpoint-uniform arbitrary data |
|---|---:|---:|---:|---:|---:|---:|
| Temam Ch. 7 | yes, strong-window | yes | no | no | no | no |
| Giga et al. 2008 | yes, local sector | yes | no | qualitative identity theorem only | no | no |
| Dong--Zhang 2020 | yes, from derivative bounds | yes | no | no | no | no |
| Wang--Gao--Xue 2022 | yes | yes | no | no | no | small data only |
| Cong Wang 2026 | yes | yes | no | no | no | small data only |
| Masuda 1967 | qualitative | qualitative | no | no | no | no |
| Jensen/Blaschke | assumed/given | assumed/given | required | conditional | pays component sum | not a PDE theorem |

## 5. Bounded conclusion

The checked literature pays the first two Jensen inputs on fixed classical
windows: a complex radius and a complex upper norm.  It does not pay:

1. a quantitative lower anchor for every localized filtered observable;
2. a summable union bound over shell--cell truncations;
3. the number of parabolic windows near a possible singular endpoint;
4. the pointwise R0.71P batch weight at the event set.

No primary theorem found in the two bounded waves directly controls the full
distinct entry-time counting measure from Leray energy.  This is a bounded
negative finding only.  It is not a claim that no such theorem exists, and it
is not a novelty or priority claim for R0.71Q.
