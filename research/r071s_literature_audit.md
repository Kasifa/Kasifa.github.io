# R0.71S bounded primary-source audit: signed and bilinear parabolic packets

**Search date:** 2026-08-26
**Question:** is there an existing theorem that controls signed or bilinear
wavelet packets attached to temporal samples or zero-entry windows by an
\(L_t^2H_x^{-1}\) Lamb-vector budget, or directly by the Leray--Hopf
energy budget?

## 1. Bounded answer

No checked theorem supplies the full implication

\[
 \text{adaptive zero entry or temporal sample}
 \quad\longrightarrow\quad
 \text{uniform signed/bilinear packet charge}
 \quad\longrightarrow\quad
 \text{Leray-paid packet sum}.
\]

The primary sources do supply two useful but narrower mechanisms.

1. A fixed family of **space--time pairings** is controlled by an
   \(L_t^2H_x^{-1}\) source norm whenever the dual packets form a Bessel
   family in \(L_t^2H_x^1\).  This is frame/Hilbert-space duality, not a
   temporal point-sampling theorem.
2. For a forced heat state that vanishes at the left endpoint, a signed
   terminal coefficient has an exact backward-adjoint representation.  A
   family estimate follows if the corresponding backward heat packets have a
   uniform Bessel bound.

Two hard boundaries prevent these statements from being used as a completed
R0.71S certificate.

- A general element of \(L_t^2H_x^{-1}\) has no canonical value at one
  time.  Raw samples of the source cannot be bounded by its
  \(L_t^2H_x^{-1}\) norm.
- The ordinary three-dimensional Leray--Hopf budget directly places the Lamb
  vector in \(L_t^{4/3}H_x^{-1}\), not in
  \(L_t^2H_x^{-1}\).  An \(L_t^2H_x^{-1}\) Lamb budget is an extra
  hypothesis unless another estimate is proved.

This is a bounded negative finding from two search waves.  It is not a claim
that no more specialized theorem exists.

## 2. Two functional-analytic boundaries

### 2.1 An \(L_t^2\) equivalence class cannot be sampled at a time

Let \(X\) be any nonzero Hilbert or Banach space.  An element of
\(L^2(0,T;X)\) is an almost-everywhere equivalence class.  Given a
representative \(f\), a time \(t_0\), and any \(z\in X\), changing
only \(f(t_0)\) to \(z\) leaves the \(L^2\) element and its norm
unchanged.  Consequently, there is no well-defined bounded map

\[
 f\in L^2(0,T;X)\longmapsto f(t_0)\in X.
\]

The same obstruction applies to a countable set of sample times.  It is
therefore invalid to write an estimate for raw values \(L(t_\beta)\) using
only \(\|L\|_{L_t^2H_x^{-1}}\).

There are three legitimate replacements, and they must not be conflated.

1. Use a space--time pairing
   \(\int\langle L,\Psi\rangle\,dt\).
2. Smooth or band-limit in time before sampling.
3. Sample a **state** \(w(t)\) for which the evolution equation supplies a
   continuous time representative.  Lions--Magenes gives this trace for the
   forced heat class used below.

### 2.2 The Leray budget gives \(L_t^{4/3}H_x^{-1}\), not
\(L_t^2H_x^{-1}\)

Let \(u\) be a three-dimensional Leray--Hopf solution on a finite time
interval, on \(\mathbb R^3\) or on a periodic domain with the usual
adjustments.  The available bounds are

\[
 u\in L_t^\infty L_x^2\cap L_t^2H_x^1.
\]

For a divergence-free test field \(\varphi\in H^1\), the projected Lamb
vector

\[
 L=P(u\times\omega)=-P((u\cdot\nabla)u)
\]

satisfies

\[
\begin{aligned}
 |\langle L,\varphi\rangle|
 &=\left|\int (u\otimes u):\nabla\varphi\,dx\right| \\
 &\le \|u\|_4^2\|\nabla\varphi\|_2 \\
 &\lesssim
 \|u\|_2^{1/2}\|\nabla u\|_2^{3/2}
 \|\varphi\|_{H^1}.
\end{aligned}
\]

Thus

\[
 \|L(t)\|_{H^{-1}}
 \lesssim
 \|u(t)\|_2^{1/2}\|\nabla u(t)\|_2^{3/2}.
\]

Raising this inequality to the \(4/3\) power and integrating gives

\[
 \int_0^T\|L(t)\|_{H^{-1}}^{4/3}\,dt
 \lesssim
 \|u\|_{L_t^\infty L_x^2}^{2/3}
 \int_0^T\|\nabla u(t)\|_2^2\,dt.
\]

By contrast, squaring the pointwise estimate would require control of
\(\int\|\nabla u\|_2^3dt\), which is absent from the Leray
inequality.  On a finite interval, \(L^{4/3}_t\) does not embed into
\(L_t^2\).  Hence the implication

\[
 \text{Leray budget}\quad\Longrightarrow\quad
 L\in L_t^2H_x^{-1}
\]

is not available.  It can become true under additional regularity, in two
dimensions, or after a separately proved frequency/localization estimate;
none of those upgrades is part of the ordinary three-dimensional Leray
budget.

## 3. Search protocol

The search was deliberately stopped after two waves.

- **Wave one:** Koch--Tataru critical parabolic spaces,
  Coifman--Meyer--Stein tent spaces and Carleson duality, and
  Dascaliuc--Grujić signed physical-scale flux.
- **Wave two:** Frazier--Jawerth coefficient transforms, smoothed sampling and
  trace thresholds; Lions--Magenes evolution traces and backward adjoints; and
  Escauriaza--Seregin--Šverák backward uniqueness.

Exact DOI metadata and the accessible primary text were checked after the two
discovery waves.  No third broad search was made.  Each source below records
what was visible, what it supports, and the remaining gap.

## 4. Primary-source ledger

### 4.1 Koch--Tataru: a critical bilinear map in \(X\) and \(Y\)

**Source.** Herbert Koch and Daniel Tataru, *Well-posedness for the
Navier--Stokes Equations*, Advances in Mathematics **157** (2001), 22--35.
[Author PDF](https://math.berkeley.edu/~tataru/papers/nas.pdf),
[DOI 10.1006/aima.2000.1937](https://doi.org/10.1006/aima.2000.1937).

**Checked evidence.** The author PDF contains the definitions of
\(BMO^{-1}\), \(X\), and \(Y\) on pp. 1--2, Theorem 2 on p. 2,
and Lemmas 3.1--3.2 on pp. 5--6.

The solution norm is

\[
 \|u\|_X=
 \sup_{t>0}t^{1/2}\|u(t)\|_\infty
 +\sup_{x,R}\left(
 |B(x,R)|^{-1}\int_0^{R^2}\int_{B(x,R)}|u|^2\,dy\,dt
 \right)^{1/2},
\]

while \(Y\) has a \(\sup_t t\|f(t)\|_\infty\) term and a
local space--time \(L^1\) Carleson term.  Theorem 2 gives the unique
small global solution in \(X\) for small divergence-free
\(BMO^{-1}\) data.  Lemma 3.1 maps \(N(u)=u\otimes u\) from \(X\)
to \(Y\), and Lemma 3.2 maps the Duhamel operator
\(V\nabla P:Y\to X\).  Polarization yields the bilinear bound

\[
 \|V\nabla P(u\otimes v)\|_X
 \lesssim \|u\|_X\|v\|_X.
\]

**What it supports.** A scale-critical bilinear construction can be controlled
when the solution and source are placed in matched parabolic Carleson spaces.
The heat kernel, product structure, and local parabolic boxes are all part of
the estimate.

**What it does not support.** The Koch--Tataru source space \(Y\) is not
\(L_t^2H_x^{-1}\), and an arbitrary Leray--Hopf solution is not known to
belong to \(X\).  The result contains no zero-entry rule, no adaptive
temporal sample sum, and no lower charge per event.

**Confidence:** high.  The theorem and both mapping lemmas were read in the
primary PDF.

### 4.2 Coifman--Meyer--Stein: tent integrals and Carleson structure

**Source.** R. R. Coifman, Y. Meyer, and E. M. Stein, *Some New Function
Spaces and Their Applications to Harmonic Analysis*, Journal of Functional
Analysis **62** (1985), 304--335.
[DOI 10.1016/0022-1236(85)90007-2](https://doi.org/10.1016/0022-1236(85)90007-2).

**Checked evidence.** The publisher abstract states that the paper introduces
the tent spaces, identifies \(T_\infty^p\) with maximal-function
questions and \(T_2^p\) with square-function questions, and develops
connections with \(L^p\), Hardy spaces, atomic decomposition, and
multilinear analysis.  The complete theorem text was not openly retrievable in
this pass, so no theorem-number-specific claim is used here.

For a measurable function on the upper half-space, the basic tent quantity is
a cone or tent **integral**, schematically

\[
 A_qF(x)=\left(\int_{\Gamma(x)}|F(y,t)|^q
 \frac{dy\,dt}{t^{n+1}}\right)^{1/q},
\]

with dual/endpoint formulations expressed through integrated pairings and
Carleson measures.

**What it supports.** If event boxes satisfy a Carleson packing condition and
the observable is paired with atoms or is a canonical semigroup extension,
tent-space duality is an appropriate route to a packet-sum estimate.

**What it does not support.** A general tent-space element is still an
almost-everywhere equivalence class.  Changing its values at a discrete set of
space--time points does not change any tent norm.  Consequently, the theory
does not by itself imply

\[
 \sum_\beta |F(t_\beta,x_\beta)|^2
 \lesssim \|F\|_{T_q^p}^2.
\]

Such a sampled estimate needs a semigroup, analytic, band-limited, or other
regular representative, together with a discrete Carleson condition.

**Confidence:** high for the integrated/tent versus raw-point distinction;
medium for the precise endpoint duality details because the full primary text
was not visible in this pass.

### 4.3 Frazier--Jawerth: coefficient pairings, smoothed samples, and the
trace threshold

**Source.** Michael Frazier and Björn Jawerth, *A Discrete Transform and
Decompositions of Distribution Spaces*, Journal of Functional Analysis
**93** (1990), 34--170.
[Accessible primary PDF](https://www.nara-wu.ac.jp/math/personal/moritoh/wavelet/1211_frazier_jawerth.pdf),
[DOI 10.1016/0022-1236(90)90137-A](https://doi.org/10.1016/0022-1236(90)90137-A).

**Checked evidence.** Theorem 2.2 is on article p. 47, Lemma 2.5 and its use
are on pp. 50--51, and Theorem 11.1 is on p. 127.

Theorem 2.2 gives bounded analysis and synthesis maps

\[
 S_\varphi f=\{\langle f,\varphi_Q\rangle\}_Q,
 \qquad
 T_\psi s=\sum_Qs_Q\psi_Q,
 \qquad
 T_\psi S_\varphi f=f,
\]

between homogeneous Triebel--Lizorkin spaces and their sequence spaces.
These are distributional pairings, not values of \(f\) at cube centers.

Lemma 2.5 compares sequence norms formed from the supremum and infimum of
the frequency-localized function \(\tilde\varphi_\nu*f\) on sufficiently
small cubes.  The proof of Theorem 2.2 then samples

\[
 (\tilde\varphi_\nu*f)(2^{-\nu}k).
\]

Thus the apparently pointwise quantity is sampled **after** Littlewood--Paley
smoothing.  It is not \(f(2^{-\nu}k)\).

Theorem 11.1 treats the hyperplane trace
\(\operatorname{Tr}f(x')=f(x',0)\).  In particular, for \(p>1\):

- if \(\alpha>1/p\), the trace exists in the corresponding Besov
  space;
- at \(\alpha=1/p\), the trace does not exist in the stated distribution
  target;
- for \(\alpha<1/p\), the trace does not exist even in the weaker targets
  listed in the theorem.

For \(p=2\), zero time regularity is below the \(1/2\) trace threshold.
Applying the scalar theorem with time as one coordinate gives the correct
warning for point-time sampling.  The Hilbert-valued
\(H_x^{-1}\) formulation is a standard extension, but is not stated
verbatim in the paper.

**What it supports.** A valid R0.71S packet may use a genuine space--time
pairing or a time-smoothed/band-limited sample.  A fixed dyadic frame gives a
sequence-space upper bound.

**What it does not support.** The theorem does not show that an arbitrary
solution-dependent family of zero times, translations, and window lengths is
a Bessel family.  Nor does it turn one positive excursion into a uniform
lower coefficient.

**Confidence:** high.  All three relevant statements were checked in the
primary PDF.

### 4.4 Lions--Magenes: continuous state traces and the backward heat packet

**Source.** J. L. Lions and E. Magenes, *Non-Homogeneous Boundary Value
Problems and Applications*, Vol. I, Springer, 1972, chapter *Variational
Evolution Equations*, pp. 227--308.
[Official chapter](https://link.springer.com/chapter/10.1007/978-3-642-65161-8_3),
[book DOI 10.1007/978-3-642-65161-8](https://doi.org/10.1007/978-3-642-65161-8).

**Checked evidence.** The Springer page confirms the authors, year, chapter,
and page range.  The page exposes only a preview, so the exact proposition
number was not visible.  The standard Lions--Magenes evolution lemma used
here is stated explicitly to make the dependency auditable.

For a Gelfand triple \(V\subset H\subset V'\),

\[
 w\in L^2(a,b;V),\qquad w_t\in L^2(a,b;V')
\]

has an \(H\)-valued continuous representative and satisfies the endpoint
energy/pairing formula.  With \(V=H^1\), \(H=L^2\), and
\(V'=H^{-1}\), a solution of

\[
 w_t-\nu\Delta w=G,\qquad w(a)=0,
\]

therefore has a legitimate endpoint \(w(b)\).  Testing against the
backward heat solution gives the exact identity

\[
 \boxed{
 \langle w(b),\phi\rangle
 =\int_a^b
 \langle G(s),e^{\nu(b-s)\Delta}\phi\rangle_{H^{-1},H^1}\,ds
 }
\]

for suitable \(\phi\).  On \(\mathbb R^3\), or on the zero-mean
torus with homogeneous norms,

\[
\begin{aligned}
 \int_a^b
 \|\nabla e^{\nu(b-s)\Delta}\phi\|_2^2\,ds
 &=\frac{\|\phi\|_2^2-\|e^{\nu(b-a)\Delta}\phi\|_2^2}
 {2\nu} \\
 &\le \frac{\|\phi\|_2^2}{2\nu}.
\end{aligned}
\]

Consequently,

\[
 |\langle w(b),\phi\rangle|
 \le (2\nu)^{-1/2}
 \|G\|_{L^2(a,b;\dot H^{-1})}\|\phi\|_2.
\]

For an event family \(I_\beta=(a_\beta,b_\beta)\), define

\[
 \Psi_\beta(s)=
 \mathbf 1_{I_\beta}(s)
 e^{\nu(b_\beta-s)\Delta}\phi_\beta.
\]

If these packets satisfy the synthesis/Bessel estimate

\[
 \left\|\sum_\beta c_\beta\Psi_\beta
 \right\|_{L_t^2\dot H_x^1}^2
 \le B\sum_\beta|c_\beta|^2,
\]

then Hilbert-space duality gives

\[
 \sum_\beta
 |\langle w_\beta(b_\beta),\phi_\beta\rangle|^2
 \le B\|G\|_{L_t^2\dot H_x^{-1}}^2.
\]

**What it supports.** This is a rigorous source-side replacement for a raw
sample.  Zero entry removes the initial term, and derivatives can be shifted
onto the backward packet before estimating the source.

**What it does not support.** Lions--Magenes supplies the trace and one-packet
duality.  It does not prove the Bessel estimate for solution-dependent event
windows, and it gives no event-to-packet lower charge.

**Confidence:** high for the lemma and the displayed semigroup derivation;
medium for the exact book proposition number because the primary chapter text
was not visible in the Springer preview.

### 4.5 Dascaliuc--Grujić: signed flux only after time and cover averaging

**Source.** R. Dascaliuc and Z. Grujić, *Energy Cascades and Flux Locality in
Physical Scales of the 3D Navier--Stokes Equations*, Communications in
Mathematical Physics **305** (2011), 199--220.
[Primary arXiv text](https://arxiv.org/pdf/1101.2193),
[DOI 10.1007/s00220-011-1219-8](https://doi.org/10.1007/s00220-011-1219-8).

**Checked evidence.** The localized flux is defined on article pp. 2--3,
optimal coverings and modified fluxes on pp. 8--9, and Theorem 4.1 on
pp. 11--12.

The signed local energy-plus-pressure flux is

\[
 \Phi_{x_0,R}(t)=
 \int\left(\frac12|u|^2+p\right)u\cdot\nabla\phi\,dx.
\]

The weak-solution formulation introduces a nonnegative anomalous-flux defect
and the modified flux \(\Psi_R\).  Theorem 4.1 assumes a Taylor-scale
separation

\[
 \tau_0<c\gamma R_0
\]

and proves, for
\((c\gamma)^{-1}\tau_0\le R\le R_0\),

\[
 c_{0,\gamma}\nu E\le \Psi_R\le c_{1,\gamma}\nu E.
\]

Here \(\Psi_R\) is averaged over an optimal spatial covering and a time
interval \([0,2T]\) with \(T\ge R_0^2/\nu\).

**What it supports.** A signed NSE nonlinearity can retain a positive lower
bound after a carefully chosen space--time and cover average.  This is a
genuine example of sign surviving longer than a termwise absolute-value
estimate.

**What it does not support.** The sign is conditional on scale separation and
appears only after time and ensemble averaging.  The theorem does not attach
a positive amount of flux to every zero entry, does not control a discrete
time-sample family, and does not derive its hypothesis from the bare Leray
budget.

**Confidence:** high.  The definitions and Theorem 4.1 were read in the
primary text.

### 4.6 Escauriaza--Seregin--Šverák: qualitative backward uniqueness, not
zero counting

**Sources.** L. Escauriaza, G. A. Seregin, and V. Šverák,
*Backward Uniqueness for Parabolic Equations*, Archive for Rational Mechanics
and Analysis **169** (2003), 147--157,
[DOI 10.1007/s00205-003-0263-8](https://doi.org/10.1007/s00205-003-0263-8);
and *\(L_{3,\infty}\)-Solutions of the Navier--Stokes Equations and
Backward Uniqueness*, Russian Mathematical Surveys **58** (2003), 211--250,
[official MathNet page](https://www.mathnet.ru/eng/rm609),
[DOI 10.1070/RM2003v058n02ABEH000609](https://doi.org/10.1070/RM2003v058n02ABEH000609).

**Checked evidence.** The MathNet primary record states the conclusion that
the critical \(L_{3,\infty}\) Cauchy-problem solutions are smooth and
provides the full bibliographic record.  The companion backward-uniqueness
paper treats a closed parabolic differential inequality, full terminal-field
vanishing, an exterior-domain setting, and growth/coefficient hypotheses.

**Exact scope relevant here.** Backward uniqueness says, under those
hypotheses, that a field satisfying the closed parabolic inequality and
vanishing everywhere at the terminal time must vanish backward.  The NSE
paper uses this qualitative mechanism, after blow-up and vorticity arguments,
in the critical \(L_t^\infty L_x^3\) regularity theorem.

**What it supports.** It can rule out a nontrivial closed parabolic field that
vanishes as a whole at the terminal time, once the required coefficient,
growth, and regularity hypotheses have been verified.

**What it does not support.** A zero of one localized wavelet coefficient is
not full-field vanishing.  The localized R0.71S observable is forced, and the
localization/filter has a nontrivial kernel.  Backward uniqueness supplies no
spacing or cardinality theorem for coefficient zeros, no quantitative lower
charge near a zero, and no estimate paid by the Leray energy budget.

**Confidence:** high for the qualitative scope and the NSE regularity
conclusion; no quantitative zero-count consequence is present in the checked
statements.

## 5. Comparison with the R0.71S candidate

| Source or mechanism | Raw source sample | Integrated signed packet | Zero-entry state endpoint | Adaptive-family sum | Lower charge per event | Bare Leray payment |
|---|---:|---:|---:|---:|---:|---:|
| Koch--Tataru | no | bilinear in \(X,Y\) | not an entry theorem | no | no | no |
| Coifman--Meyer--Stein | no | yes, through tent pairings | only with extra semigroup structure | conditional on Carleson packing | no | no |
| Frazier--Jawerth | no | yes, fixed coefficient frame | smoothed samples only | fixed frame/subfamily | no | no |
| Lions--Magenes plus heat adjoint | source sample no | yes | yes | only if adjoint packets are Bessel | no | \(L_t^2H^{-1}\) is extra |
| Dascaliuc--Grujić | no | signed cover average | no | ensemble average | conditional averaged positivity | conditional, not bare |
| Escauriaza--Seregin--Šverák | no | no packet sum | full-field terminal zero only | no | no | criterion-level regularity |

## 6. Precise theorem still needed

The most defensible next target is a finite-family statement.  For event
windows \(I_\beta=(a_\beta,b_\beta)\), spatial analysis atoms
\(\phi_\beta\), and forced heat states satisfying

\[
 (w_\beta)_t-\nu\Delta w_\beta=G,\qquad
 w_\beta(a_\beta)=0,
\]

the source side reduces exactly to the backward packets

\[
 \Psi_\beta(s)=
 \mathbf 1_{I_\beta}(s)
 e^{\nu(b_\beta-s)\Delta}\phi_\beta.
\]

R0.71S would need to prove both of the following with constants uniform in
the finite event family.

1. **Bessel/Carleson upper bound**

   \[
   \left\|\sum_\beta c_\beta\Psi_\beta
   \right\|_{L_t^2\dot H_x^1}^2
   \le B\sum_\beta|c_\beta|^2.
   \]

2. **Event-to-packet lower comparison**, in a form that preserves sign or a
   controlled bilinear pairing and is strong enough to pay the positive
   excursion charge.

The first item may follow from a fixed spatial frame plus a proved parabolic
packing condition for the event intervals.  The second item is not provided
by any checked source.  If \(\phi_\beta\) is selected from
\(w_\beta(b_\beta)\) after observing the solution, that adaptive
selection must itself be audited: a lower coefficient obtained by choosing
the best atom does not automatically preserve the Bessel constant.

Finally, replacing \(G\) by the Lamb vector requires moving every curl,
cutoff derivative, and multiplier onto the adjoint packet and checking its
\(L_t^2H_x^1\) norm at the intended NSE scaling.  Even if that succeeds,
the resulting \(L_t^2H_x^{-1}\) Lamb norm is not automatically Leray-paid;
Section 2.2 remains an independent gate.

## 7. Bounded conclusion

The checked literature supports a rigorous change of object:

\[
 \text{raw temporal sample}
 \quad\rightsquigarrow\quad
 \text{space--time pairing or zero-entry state endpoint tested by a
 backward heat packet}.
\]

It does not complete the R0.71S incidence argument.  The missing work is a
uniform Bessel/Carleson theorem for the solution-dependent event packets and
an event-to-packet lower comparison that retains enough sign.  A separate
payment theorem would then be needed to replace an
\(L_t^2H_x^{-1}\) Lamb hypothesis by the ordinary Leray budget.  Without
that theorem, the directly paid exponent is \(4/3\), as derived above.
