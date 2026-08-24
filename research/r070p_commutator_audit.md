# R0.70P endpoint square-commutator audit

**Audit status:** PASS for the canonical unweighted smooth annular
Littlewood--Paley frame; FAIL for arbitrary weights

**Audit date:** 2026-08-25

**Object audited:** the energy-endpoint estimate

\[
 \left(\sum_j w_j\|[T_j,A]f\|_2^2\right)^{1/2}
 \stackrel{?}{\leq}
 C\|\nabla A\|_{L^\infty}\|f\|_{H^{-1}}.
 \tag{0.1}
\]

Here and below

\[
 [T,A]f:=T(Af)-A(Tf).
 \tag{0.2}
\]

The coefficient may be scalar or matrix-valued.  The application intended in
R0.70P is a common orthogonal projector \(A=P(x,t)\) acting on vorticity.
This audit is spatial: time is a parameter throughout.

## 1. Exact decision

The following statements survive the audit.

1. For a standard complete **smooth annular** Littlewood--Paley frame and
   \(w_j=1\), (0.1) is true on \(\mathbb R^3\) with the homogeneous
   \(\dot H^{-1}\) norm.
2. The analogous periodic statement is true on \(\mathbb T^3\) for the
   homogeneous annular blocks augmented by the exact constant-mode projector
   \(\Pi_0\), with zero-mean \(f\).  On that subspace, \(H^{-1}\) and
   \(\dot H^{-1}\) are equivalent.
3. If \(0\leq w_j\leq W<\infty\), the Euclidean annular estimate remains
   true with the additional factor \(W^{1/2}\).  For the full periodic frame,
   where \(\Pi_0\) retains unit weight, the factor is
   \(\max\{1,W^{1/2}\}\).
4. There is no constant independent of an arbitrary nonnegative weight
   sequence.  An explicit one-mode torus test makes the left side at least
   \(c\sqrt{w_J}\) while both norms on the right remain one.

The proof is not a consequence of the elementary one-block bound alone.  Its
nontrivial ingredient is the first-order Calderón--Coifman--Meyer commutator
theorem, applied uniformly to finite Rademacher sums of the dyadic symbols.

## 2. Pinned Littlewood--Paley convention

Fix

\[
 \varphi\in C_c^\infty(\mathbb R^3\setminus\{0\}),
 \qquad
 \operatorname{supp}\varphi
 \subset\{\xi:c_0\leq|\xi|\leq c_1\},
 \tag{2.1}
\]

where \(0<c_0<c_1<\infty\), and put

\[
 \varphi_j(\xi)=\varphi(2^{-j}\xi),
 \qquad
 T_j=\varphi_j(D),
 \qquad j\in\mathbb Z.
 \tag{2.2}
\]

Assume the exact standard square partition

\[
 \sum_{j\in\mathbb Z}|\varphi_j(\xi)|^2=1
 \qquad(\xi\neq0).
 \tag{2.3}
\]

Annular support implies that at each nonzero frequency only a fixed number
\(N_0=N_0(c_0,c_1)\) of the symbols are active.  The upper estimate below
uses finite overlap and smoothness.  Exact equality in (2.3) is not needed
for the commutator upper bound, but it is the canonical reconstruction
normalization used in the main R0.70P report.

On \(\mathbb T^3=(\mathbb R/2\pi\mathbb Z)^3\), equipped with normalized
Haar measure, let

\[
 (\Pi_0h)(x):=\int_{\mathbb T^3}h(y)\,dy
 \tag{2.4}
\]

be the constant-mode projector, and restrict the same annular symbols to
\(\mathbb Z^3\setminus\{0\}\), still indexed by \(j\in\mathbb Z\).  The
canonical periodic frame is

\[
 \{\Pi_0\}\cup\{T_j:j\in\mathbb Z\},
 \qquad
 |\mathbf1_{\{0\}}(k)|^2
 +\sum_{j\in\mathbb Z}|\varphi_j(k)|^2=1
 \quad(k\in\mathbb Z^3).
 \tag{2.5}
\]

Although the input \(f\) will have zero mean, \(Af\) need not.  Therefore
\(\Pi_0\) cannot be deleted from the square function applied to \(Af\) or
from the commutator ledger.  Because \(|k|\geq1\) on the nonzero lattice,
sufficiently negative annular blocks vanish there.  An inhomogeneous torus
resolution gives an equivalent norm, but it is not the canonical convention
audited here.  Changing the measure normalization changes only the explicit
duality constant below.

Sharp Fourier shells, cumulative low-pass families with infinite overlap,
and a scale-dependent family of coefficients \(A_j\) are not covered by this
convention.

## 3. Canonical Euclidean theorem

### Theorem 3.1 -- homogeneous endpoint square commutator

Let the operators \(T_j\) satisfy Section 2.  If

\[
 A\in W^{1,\infty}(\mathbb R^3;\mathbb C^{m\times m})
 \tag{3.1}
\]

and \(f\in\dot H^{-1}(\mathbb R^3;\mathbb C^m)\), then

\[
 \boxed{
 \left(\sum_{j\in\mathbb Z}\|[T_j,A]f\|_2^2\right)^{1/2}
 \leq C_{\varphi,m}\|\nabla A\|_\infty
 \|f\|_{\dot H^{-1}}.}
 \tag{3.2}
\]

It is enough to prove (3.2) for smooth \(A\) and Schwartz \(f\) whose Fourier
support stays away from zero.  The general statement follows by
regularization and completion.  Since constants commute with every \(T_j\),
the right side uses the Lipschitz seminorm, not \(\|A\|_\infty\).

### 3.1 The external theorem actually used

The proof depends on the following first-order commutator theorem.

> **Calderón--Coifman--Meyer dependency.**  If \(p(D)\) is a translation
> invariant order-one operator whose smooth symbol satisfies the homogeneous
> estimates
> \[
>  |\partial_\xi^\alpha p(\xi)|
>  \leq C_\alpha|\xi|^{1-|\alpha|},
>  \qquad \xi\neq0,
>  \tag{3.3}
> \]
> for sufficiently many multiindices, then
> \[
>  \|[p(D),A]g\|_2
>  \leq C_p\|\nabla A\|_\infty\|g\|_2.
>  \tag{3.4}
> \]
> The constant is controlled by finitely many symbol seminorms in (3.3).

The homogeneous first-commutator mechanism originates in A. P. Calderón,
“Commutators of Singular Integral Operators,” *PNAS* 53 (1965), 1092--1099,
[DOI 10.1073/pnas.53.5.1092](https://doi.org/10.1073/pnas.53.5.1092).
The order-one pseudodifferential form used here is the theorem of R. R.
Coifman and Y. Meyer, “Commutateurs d'intégrales singulières et opérateurs
multilinéaires,” *Annales de l'Institut Fourier* 28 (1978), 177--202,
[DOI 10.5802/aif.708](https://doi.org/10.5802/aif.708).  Their earlier bilinear
commutator paper is R. R. Coifman and Y. Meyer, *Transactions of the AMS* 212
(1975), 315--331,
[DOI 10.1090/S0002-9947-1975-0380244-8](https://doi.org/10.1090/S0002-9947-1975-0380244-8).

This audit does not reprove the Calderón--Coifman--Meyer theorem.  It checks
that the complete randomized LP symbol family satisfies its hypotheses with
a constant independent of signs and truncation endpoints.

**Publication blocker -- exact theorem/page citation.**  The external form
needed here is the seminorm-uniform \(\dot S^1\) version (3.3), not merely a
statement for one fixed homogeneous symbol.  The candidate locations in the
1978 primary paper are Theorem 2 on pp. 179--180, whose constant is stated in
terms of the symbol bounds, the compact-manifold discussion on pp. 177--178,
and the Lipschitz endpoint argument in Section 5.  Before this result is
submitted or advertised as a formally sourced lemma, the report must pin the
exact page-level implication for the scale-normalized homogeneous randomized
family, or append its standard paraproduct proof.  The short abstract of the
1978 paper is not sufficient evidence for that uniformity.  The passage from
smooth compactly supported coefficients to bounded \(W^{1,\infty}\)
coefficients is by mollification and expanding cutoffs in the commutator
kernel.  Constants in \(A\) commute, and the Calderón estimate depends on the
Lipschitz seminorm.  This extension is also part of the named external
dependency rather than a new claim of R0.70P.

### 3.2 Finite Rademacher truncation

Let \(F\subset\mathbb Z\) be finite and let
\(\varepsilon_j\in\{-1,1\}\).  Define

\[
 M_{\varepsilon,F}
 :=\sum_{j\in F}\varepsilon_jT_j,
 \qquad
 m_{\varepsilon,F}(\xi)
 :=\sum_{j\in F}\varepsilon_j\varphi_j(\xi).
 \tag{3.5}
\]

Finite overlap gives, for every multiindex \(\alpha\),

\[
 \sup_{F,\varepsilon}\sup_{\xi\neq0}
 |\xi|^{|\alpha|}
 |\partial_\xi^\alpha m_{\varepsilon,F}(\xi)|
 \leq C_{\alpha,\varphi}.
 \tag{3.6}
\]

In particular, \(M_{\varepsilon,F}\) is uniformly bounded on \(L^2\), and

\[
 q_{\varepsilon,F}(\xi)
 :=|\xi|m_{\varepsilon,F}(\xi)
 \tag{3.7}
\]

satisfies the order-one bounds (3.3), uniformly in \(F\) and the signs.

This uniformity is homogeneous.  If the cited external theorem is stated
only with inhomogeneous \(S^1\) seminorms, those seminorms are not uniform as
\(\min F\to-\infty\).  One must first dilate the lowest active Euclidean
annulus to unit scale and use scale invariance of the commutator estimate.
This normalization step is part of the page-level dependency flagged in
Section 3.1; it cannot be hidden inside an inhomogeneous symbol constant.

For \(C_j=[T_j,A]f\), exact orthogonality of the independent signs gives

\[
 \mathbb E_\varepsilon
 \left\|\sum_{j\in F}\varepsilon_jC_j\right\|_2^2
 =\sum_{j\in F}\|C_j\|_2^2.
 \tag{3.8}
\]

This is an exact \(L^2\) identity, not merely a Khintchine inequality.
Moreover,

\[
 \sum_{j\in F}\varepsilon_j[T_j,A]
 =[M_{\varepsilon,F},A]
 \tag{3.9}
\]

because the same coefficient \(A\) is used at every scale.

### 3.3 First-order decomposition

Let \(\Lambda=|D|\) and put

\[
 g=\Lambda^{-1}f,
 \qquad
 \|g\|_2=\|f\|_{\dot H^{-1}}.
 \tag{3.10}
\]

The exact operator identity is

\[
 [M_{\varepsilon,F},A]\Lambda
 =[M_{\varepsilon,F}\Lambda,A]
 +M_{\varepsilon,F}[A,\Lambda].
 \tag{3.11}
\]

The first term in (3.11) is the commutator of \(A\) with the order-one
symbol \(q_{\varepsilon,F}\).  The second uses the order-one symbol
\(|\xi|\), followed by a uniformly \(L^2\)-bounded zero-order multiplier.
The dependency (3.4) therefore gives

\[
 \begin{aligned}
 \|[M_{\varepsilon,F},A]f\|_2
 &\leq
 \|[M_{\varepsilon,F}\Lambda,A]g\|_2
 +\|M_{\varepsilon,F}[A,\Lambda]g\|_2\\
 &\leq C_{\varphi,m}\|\nabla A\|_\infty\|g\|_2\\
 &=C_{\varphi,m}\|\nabla A\|_\infty
 \|f\|_{\dot H^{-1}},
 \end{aligned}
 \tag{3.12}
\]

uniformly in \(F\) and \(\varepsilon\).  Combining (3.8)--(3.12) gives the
same bound for every finite square sum.  Increasing \(F\) to all integers
and using monotone convergence proves (3.2).

The finite-truncation step is essential.  No convergence of an infinite
random multiplier is assumed before the uniform estimate is obtained.

## 4. Frequency and scale audit

For scalar notation, the exact Fourier formula is

\[
 \widehat{[T_j,A]f}(n)
 =\int_{k+q=n}
 \bigl(\varphi_j(n)-\varphi_j(k)\bigr)
 \widehat A(q)\widehat f(k)\,dk.
 \tag{4.1}
\]

On the torus the integral is replaced by a sum.  Formula (4.1) separates
three mechanisms.

### 4.1 Low coefficient frequency, high input frequency

If \(|q|\ll|k|\simeq2^j\), the mean-value theorem gives

\[
 |\varphi_j(k+q)-\varphi_j(k)|
 \leq C2^{-j}|q|.
 \tag{4.2}
\]

The factor \(|q|\widehat A(q)\) corresponds to one derivative of \(A\),
while \(2^{-j}\simeq|k|^{-1}\) supplies the \(H^{-1}\) input weight.

### 4.2 High coefficient frequency, low input frequency

If \(|k|\ll|q|\simeq|n|\simeq2^j\), then the Lipschitz scaling of the
coefficient supplies one inverse high frequency.  At the one-mode level,

\[
 |\widehat A(q)|\,|\widehat f(k)|
 \lesssim
 \|\nabla A\|_\infty
 {|\widehat f(k)|\over|q|}
 \leq
 \|\nabla A\|_\infty
 {|\widehat f(k)|\over|k|}.
 \tag{4.3}
\]

For a general \(A\), (4.3) is a scaling explanation, not a legitimate
\(\ell^1\) Fourier-coefficient proof: \(L^\infty\) does not control the
absolute sum of Fourier coefficients.

### 4.3 Comparable high frequencies and low output

The delicate face is

\[
 |q|\simeq|k|\gg|n|=|k+q|.
 \tag{4.4}
\]

There is no small symbol difference in (4.1).  A blockwise absolute estimate
produces a downward high--high-to-low tail and can falsely suggest a
logarithmic loss.  The first-order commutator theorem controls precisely this
resonant interaction.  Algebraically, (3.11) converts it into two order-one
commutators acting on \(g=\Lambda^{-1}f\).  Therefore the proof must not be
replaced by independent estimates of all Fourier pairs.

## 5. Periodic theorem and the transference dependency

### Theorem 5.1 -- zero-mean torus endpoint

Let \(\{\Pi_0\}\cup\{T_j:j\in\mathbb Z\}\) be the exact periodic frame in
Section 2.  If

\[
 A\in W^{1,\infty}(\mathbb T^3;\mathbb C^{m\times m}),
 \qquad
 \int_{\mathbb T^3}f\,dx=0,
 \tag{5.1}
\]

then

\[
 \boxed{
 \left(
 \|[\Pi_0,A]f\|_{L^2(\mathbb T^3)}^2
 +\sum_{j\in\mathbb Z}\|[T_j,A]f\|_{L^2(\mathbb T^3)}^2
 \right)^{1/2}
 \leq C_{\mathbb T,\varphi,m}\|\nabla A\|_{L^\infty(\mathbb T^3)}
 \|f\|_{\dot H^{-1}_\#(\mathbb T^3)}.}
 \tag{5.2}
\]

The zero-mean hypothesis is needed for the homogeneous definition of
\(\Lambda^{-1}f\).  It does not justify deleting \(\Pi_0\), because the
product \(Af\) may have a nonzero mean.  An inhomogeneous \(H^{-1}\)
formulation is equivalent after the zero mode is handled separately, but it
is not the convention in (5.2).

### 5.1 Exact constant-mode term

Since \(\Pi_0f=0\),

\[
 [\Pi_0,A]f=\Pi_0(Af).
 \tag{5.3}
\]

For a constant unit vector \(c\in\mathbb C^m\), homogeneous
\(H^{-1}\)--\(H^1\) duality on the zero-mean torus gives

\[
 \begin{aligned}
 |c^*\Pi_0(Af)|
 &=|\langle f,A^*c\rangle|\\
 &=|\langle f,(A-\Pi_0A)^*c\rangle|\\
 &\leq
 \|f\|_{\dot H^{-1}_\#}
 \|\nabla(A^*c)\|_2\\
 &\leq
 |\mathbb T^3|^{1/2}\|\nabla A\|_\infty
 \|f\|_{\dot H^{-1}_\#}.
 \end{aligned}
 \tag{5.4}
\]

Here the subscript \(\#\) denotes zero mean.  With normalized measure,
\(|\mathbb T^3|=1\).  Taking the supremum over \(c\) proves

\[
 \|[\Pi_0,A]f\|_2
 \leq C_{\mathbb T,m}\|\nabla A\|_\infty
 \|f\|_{\dot H^{-1}_\#}.
 \tag{5.5}
\]

This finite-dimensional estimate is proved directly and is not part of the
Calderón--Coifman--Meyer dependency.

### 5.2 Periodic first-order commutator lemma

The periodic proof requires the following lemma, rather than an unsupported
claim that Euclidean transference is automatic.

> **Lemma P.**  Let \(p(\xi)\) satisfy the Euclidean order-one hypotheses in
> (3.3), be continuous at zero with \(p(0)=0\), and let \(p(D_{\mathbb T})\)
> be the Fourier-series multiplier with symbol \(p(k)\),
> \(k\in\mathbb Z^3\).  Then
> \[
>  \|[p(D_{\mathbb T}),A]g\|_{L^2(\mathbb T^3)}
>  \leq C_p\|\nabla A\|_\infty\|g\|_2.
>  \tag{5.6}
> \]

Coifman--Meyer (1978) formulate their order-one commutator result on a
compact smooth manifold \(V\), so \(V=\mathbb T^3\) is directly within the
primary paper's geometric setting.  For the present family one additionally
needs the constant to be uniform under the finite randomized symbols; this
is supplied by the uniform symbol bounds (3.6)--(3.7).  Thus Lemma P may be
quoted as the periodic instance of that primary theorem.  The lifting
argument below records an independent route and makes clear why ordinary
linear multiplier transference alone would not suffice.

Here is a direct lifting argument for Lemma P.  First take periodic
trigonometric polynomials \(A,g\).  Extend them periodically to
\(\mathbb R^3\), choose a fixed \(\eta\in C_c^\infty(\mathbb R^3)\), and
write \(\eta_R(x)=\eta(x/R)\).  For every fixed trigonometric polynomial
\(h\), Fourier concentration of \(\widehat{\eta_R}\) at zero gives

\[
 R^{-3/2}
 \left\|
 p(D)(\eta_Rh_{\mathrm{per}})
 -\eta_R\bigl(p(D_{\mathbb T})h\bigr)_{\mathrm{per}}
 \right\|_{L^2(\mathbb R^3)}
 \longrightarrow0.
 \tag{5.7}
\]

For a nonzero Fourier mode this follows from continuity of \(p\) near that
lattice point and the concentration of
\(R^3\widehat\eta(R(\xi-k))\).  For the zero mode, \(p(0)=0\) and the
order-one bound imply an extra factor \(R^{-1}\).  Since only finitely many
modes are present, the limit may be summed.  Also

\[
 R^{-3}\|\eta_Rh_{\mathrm{per}}\|_2^2
 \longrightarrow
 c_\eta\|h\|_{L^2(\mathbb T^3)}^2.
 \tag{5.8}
\]

Apply the Euclidean bound (3.4) to
\([p(D),A_{\mathrm{per}}](\eta_Rg_{\mathrm{per}})\), divide by \(R^{3/2}\),
and use (5.7)--(5.8) for \(g\) and \(Ag\).  Letting \(R\to\infty\) proves
(5.6) for trigonometric polynomials.  Periodic mollification of \(A\)
preserves its Lipschitz seminorm; density of trigonometric polynomials in
\(L^2\), followed by the uniform estimate, gives the stated lemma.

This is a commutator lifting argument, not an application of the linear
multiplier theorem alone.  K. de Leeuw's primary linear transference paper is
“On \(L^p\) Multipliers,” *Annals of Mathematics* 81 (1965), 364--379,
[DOI 10.2307/1970621](https://doi.org/10.2307/1970621).  That theorem by
itself does not transfer the bilinear expression \([p(D),A]g\); the cutoff
argument above supplies the missing step.

### 5.3 Completion of the torus proof

For a finite Rademacher truncation of the homogeneous torus blocks, the
restricted random symbol is uniformly order zero, and its product with
\(|k|\) satisfies Lemma P uniformly.  On the zero-mean subspace let

\[
 g=\Lambda^{-1}f,
 \qquad \Lambda e^{ik\cdot x}=|k|e^{ik\cdot x},\quad k\neq0.
 \tag{5.9}
\]

The identity (3.11), Lemma P for \(M_{\varepsilon,F}\Lambda\) and
\(\Lambda\), and the exact Rademacher identity prove every finite square
sum of annular commutators.  Monotone convergence handles all annular
scales.  Combining that estimate with the separately proved constant-mode
bound (5.5) proves (5.2).  No smooth low block is inserted: the periodic
frame consists of the same exact annular square partition on nonzero lattice
modes plus the exact projector \(\Pi_0\).

## 6. Matrix coefficients and the vorticity specialization

For

\[
 A=(A_{ab})_{a,b=1}^m,
 \qquad f=(f_b)_{b=1}^m,
 \tag{6.1}
\]

one has

\[
 ([T_j,A]f)_a
 =\sum_{b=1}^m[T_j,A_{ab}]f_b,
 \qquad
 ([\Pi_0,A]f)_a
 =\sum_{b=1}^m[\Pi_0,A_{ab}]f_b.
 \tag{6.2}
\]

Applying the scalar result to each entry and using finite-dimensional norm
equivalence proves Theorem 3.1 with \(C_{\varphi,m}\) and Theorem 5.1 with
\(C_{\mathbb T,\varphi,m}\).  For a fixed matrix size \(m=3\), this
dependence is harmless.  No symmetry, positivity, or projection identity is
needed for the estimate.

If \(f=\omega=\nabla\times u\) and \(u\) is divergence-free, then on
\(\mathbb R^3\)

\[
 \|\omega\|_{\dot H^{-1}}=\|u\|_2.
 \tag{6.3}
\]

Consequently a common spatial projector \(P\) satisfies, on \(\mathbb R^3\),

\[
 \left(
 \sum_j\|[T_j,P]\omega\|_2^2
 \right)^{1/2}
 \leq C\|\nabla P\|_\infty\|u\|_2.
 \tag{6.4R}
\]

On \(\mathbb T^3\), put \(u_*=u-\Pi_0u\).  Then
\(\|\omega\|_{\dot H^{-1}_\#}=\|u_*\|_2\), and the corresponding bound is

\[
 \left(
 \|[\Pi_0,P]\omega\|_2^2
 +\sum_j\|[T_j,P]\omega\|_2^2
 \right)^{1/2}
 \leq C\|\nabla P\|_\infty\|u_*\|_2.
 \tag{6.4T}
\]

Periodic vorticity has \(\Pi_0\omega=0\), so adding \(\Pi_0\) does not alter
the observed covariance or residual built from \(P T_j\omega\).  It is still
needed on the reconstruction side because

\[
 \Pi_0(P\omega)=[\Pi_0,P]\omega
 \tag{6.5}
\]

may be nonzero.  Equations (6.4R), (6.4T), and (6.5) are the positive
endpoint produced by this audit.

## 7. Bounded weights and the arbitrary-weight obstruction

For nonnegative weights, the correct random multiplier is

\[
 M_{\varepsilon,F,w}
 =\sum_{j\in F}\varepsilon_j\sqrt{w_j}\,T_j.
 \tag{7.1}
\]

In the canonical torus frame, these weights apply to the annular blocks;
the exact constant projector \(\Pi_0\) keeps unit weight and is estimated
separately by (5.5).

### Proposition 7.1 -- bounded-weight variant

If

\[
 W:=\sup_jw_j<\infty,
 \tag{7.2}
\]

then

\[
 \left(\sum_jw_j\|[T_j,A]f\|_2^2\right)^{1/2}
 \leq C_{\varphi,m}W^{1/2}
 \|\nabla A\|_\infty\|f\|_{\dot H^{-1}}.
 \tag{7.3}
\]

Indeed, finite overlap changes (3.6) only by the factor \(W^{1/2}\).  A
positive lower bound for the weights is irrelevant to the commutator upper
estimate, although it may be required by a separate lower-frame
reconstruction theorem.

For the canonical periodic frame, combining (7.3) with (5.5) gives

\[
 \left(
 \|[\Pi_0,A]f\|_2^2
 +\sum_jw_j\|[T_j,A]f\|_2^2
 \right)^{1/2}
 \leq C_{\mathbb T,\varphi,m}\max\{1,W^{1/2}\}
 \|\nabla A\|_\infty\|f\|_{\dot H^{-1}_\#}.
 \tag{7.3T}
\]

More generally, (7.3) holds if the randomized weighted symbols satisfy a
uniform order-zero family bound

\[
 \sup_{F,\varepsilon}\sup_{\xi\neq0}
 |\xi|^{|\alpha|}
 \left|
 \partial_\xi^\alpha
 \sum_{j\in F}\varepsilon_j\sqrt{w_j}\varphi_j(\xi)
 \right|<\infty
 \tag{7.4}
\]

for the finite set of derivatives required by the commutator theorem.  For a
nondegenerate fixed annular profile with finite overlap, boundedness of the
weights is the transparent sufficient condition and is essentially forced
by a one-block test.

### Theorem 7.2 -- arbitrary weights fail

Because a nonzero compactly supported annular profile must vary along some
ray, and rational directions are dense, one can choose a primitive
\(\ell\in\mathbb Z^3\setminus\{0\}\), write
\(\widehat\ell=\ell/|\ell|\), and choose \(\rho\in(c_0,c_1)\) such that

\[
 {d\over dr}\varphi(r\widehat\ell)\big|_{r=\rho}\neq0.
 \tag{7.5}
\]

Choose positive integers \(n_J\) so that
\(2^{-J}n_J|\ell|\to\rho\), put \(k_J=n_J\ell\), and fix a unit vector
\(b\perp\ell\).  On the normalized torus set

\[
 A(x)=|\ell|^{-1}\cos(\ell\cdot x),
 \qquad
 f_J(x)=|k_J|e^{ik_J\cdot x}b.
 \tag{7.6}
\]

Then \(f_J\) is zero mean and divergence-free, and

\[
 \|\nabla A\|_\infty=1,
 \qquad
 \|f_J\|_{\dot H^{-1}}=1.
 \tag{7.7}
\]

Directly,

\[
 \begin{aligned}
 [T_J,A]f_J
 ={|k_J|\over2|\ell|}\sum_{\sigma=\pm1}
 &\left[
 \varphi\!\left(2^{-J}(k_J+\sigma\ell)\right)
 -\varphi\!\left(2^{-J}k_J\right)
 \right]\\
 &\times e^{i(k_J+\sigma\ell)\cdot x}b.
 \end{aligned}
 \tag{7.8}
\]

The two output modes are orthogonal, and Taylor expansion yields

\[
 \|[T_J,A]f_J\|_2
 \longrightarrow
 {\rho\over\sqrt2}
 \left|{d\over dr}\varphi(r\widehat\ell)\big|_{r=\rho}\right|
 =:c_\varphi>0.
 \tag{7.9}
\]

Hence

\[
 \left(\sum_jw_j\|[T_j,A]f_J\|_2^2\right)^{1/2}
 \geq c_\varphi\sqrt{w_J}+o(\sqrt{w_J}).
 \tag{7.10}
\]

If \(w_J\to\infty\) along active annular scales, (0.1) cannot hold with a
weight-independent constant.  The same construction can be kept inside the
projector class.  Choose orthonormal \(b,c\perp\ell\), and take

\[
 v(x)=b\cos(\ell\cdot x)+c\sin(\ell\cdot x),
 \qquad
 A=I-v\otimes v,
 \tag{7.11}
\]

while testing \(|k_J|e^{ik_J\cdot x}b\).  The nonconstant matrix entries
shift the frequency by \(\pm2\ell\); the same Taylor calculation gives a
fixed positive limit proportional to the derivative in (7.5).  Here
\(\|\nabla A\|_\infty\) is fixed independently of \(J\), which is all the
weight obstruction requires.

On \(\mathbb R^3\), a compactly supported wave-packet version gives the same
obstruction.  Dyadic dilation also covers unbounded weights occurring toward
low homogeneous scales.

## 8. Where a Rademacher--Calderón proof can fail

The canonical proof above does not fail.  The following superficially
similar arguments do.

1. **Arbitrary weights.**  If \(w_J\) is large, the order-zero seminorm of
   the randomized symbol in (7.1) is at least \(c\sqrt{w_J}\).  Uniformity is
   lost exactly at (3.6), and (7.10) shows this is a true obstruction rather
   than only a proof defect.
2. **Only a zero-order CZ theorem.**  Ordinary \(L^2\) boundedness of a
   Calderón--Zygmund operator, or the BMO commutator theorem, does not provide
   the derivative gain from \(H^{-1}\) to \(L^2\).  The order-one
   Calderón--Coifman--Meyer theorem is indispensable.
3. **Infinite randomization before truncation.**  The exact expectation is
   first applied to a finite set \(F\).  The full result follows only after a
   uniform bound and monotone convergence.
4. **A direction depending on scale.**  In general
   \[
    \sum_j\varepsilon_j[T_j,A_j]
    \neq [\sum_j\varepsilon_jT_j,A]
    \tag{8.1}
   \]
   for any single \(A\).  R0.70P therefore needs a common projector across
   all scales participating in the square function.
5. **Nonsmooth or infinitely overlapping filters.**  Sharp shells and
   cumulative low-pass families need not satisfy the uniform symbol bounds
   (3.6).  The theorem audited here makes no claim for them.
6. **The torus zero mode.**  The homogeneous factorization
   \(g=\Lambda^{-1}f\) is unavailable unless \(f\) has zero mean.  For
   vorticity this is automatic on the periodic box, but it must remain in the
   formal statement.  Even then, \(Af\) may have nonzero mean, so the exact
   projector \(\Pi_0\) and estimate (5.5) cannot be omitted.

## 9. Exact downstream boundary for R0.70P

The Littlewood--Paley square-function identity gives, schematically,

\[
 \|P\omega\|_2
 \lesssim
 \left(\sum_j\|P T_j\omega\|_2^2\right)^{1/2}
 +\left(
 \|[\Pi_0,P]\omega\|_2^2
 +\sum_j\|[T_j,P]\omega\|_2^2
 \right)^{1/2}.
 \tag{9.1}
\]

Here \(P\Pi_0\omega=0\), so no constant-mode term is added to the observed
residual.  The term \([\Pi_0,P]\omega=\Pi_0(P\omega)\) restores the constant
mode of the reconstructed field.

Using (6.4T), a valid conditional periodic bridge is therefore

\[
 \|P\omega\|_2
 \lesssim R_P^{1/2}
 +\|\nabla P\|_\infty\|u_*\|_2,
 \qquad
 R_P:=\sum_j\|P T_j\omega\|_2^2.
 \tag{9.2}
\]

This does **not** yet produce the Miller-critical spacetime bound.  To infer

\[
 P\omega\in L_t^4L_x^2,
 \tag{9.3}
\]

one still needs

\[
 R_P\in L_t^2,
 \qquad
 \|\nabla P\|_\infty\|u_*\|_2\in L_t^4.
 \tag{9.4}
\]

The Leray energy bound gives \(u_*\in L_t^\infty L_x^2\), but it does not give
\(\nabla P\in L_t^4L_x^\infty\).  The following remain separate unresolved
PDE requirements:

- propagation of a common projector across scales and spatial windows;
- a uniform principal spectral gap;
- control of \(\nabla Q/E\), hence of \(\nabla P\);
- orientation, or a regularity criterion formulated directly for the
  projector;
- absolute \(L_t^2\) control of the observed residual;
- a periodic downstream regularity theorem if the argument remains on
  \(\mathbb T^3\).

Thus the endpoint square commutator is a genuine positive harmonic-analysis
lemma.  It closes one spatial energy-level gate, but it is neither a
Navier--Stokes continuation criterion nor a propagation theorem for its own
hypotheses.

## 10. Publication-safe statement

> For a fixed standard smooth annular Littlewood--Paley resolution and one
> common Lipschitz matrix coefficient \(A\), the unweighted square sequence
> of commutators gains exactly one derivative:
> \[
>  \|([T_j,A]f)_j\|_{L_x^2\ell_j^2}
>  \lesssim
>  \|\nabla A\|_\infty\|f\|_{\dot H^{-1}}.
> \]
> The result holds on \(\mathbb R^3\).  On the zero-mean periodic box, the
> same annular family must be augmented by the exact constant-mode projector
> \(\Pi_0\); its commutator is controlled directly by
> \(H^{-1}\)--\(H^1\) duality, while the annular part uses Lemma P.
> Uniformly bounded nonnegative annular weights are allowed with a
> \(\sqrt{\sup_jw_j}\) loss; arbitrary weights are excluded by the explicit
> frequency-shift test (7.6)--(7.10).  The theorem is spatial and assumes the
> common Lipschitz coefficient; it does not propagate that coefficient from
> the Navier--Stokes covariance equation.
