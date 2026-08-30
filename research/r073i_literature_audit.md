# R0.73I primary-literature boundary audit: selected gain for a slowly varying shear

**Search date:** 2026-08-30  
**Audit type:** independent source-stage literature audit  
**Frozen target:** research/r073i_problem_freeze.md  
**Public status:** not released  
**Claim status:** literature boundary only; no R0.73I spectral or adiabatic contract is closed here

## 1. Direct decision

The primary literature located in this audit does **not** contain a theorem
for the exact R0.73I family

\[
 W(d,x)=-\frac12e^{-d}\sin x+\frac14e^{-4d}\sin 2x,
 \qquad
 B_\varepsilon(d)=\widetilde A(d)-\varepsilon L,
 \qquad L=-\partial_x^2+\frac14,
\]

which proves, for a canonically anchored rightmost rank-one branch,

\[
 \log G_\varepsilon(D)
 =\frac1\varepsilon\int_0^D\operatorname{Re}\lambda_0(s)\,\mathrm ds
 +O_D(1).
 \tag{1.1}
\]

Nor did the search locate a theorem for this family giving the stronger
two-term law

\[
 \log G_\varepsilon(D)
 =\frac1\varepsilon\int_0^D\operatorname{Re}\lambda_0(s)\,\mathrm ds
 +\mathcal C_D+O_D(\varepsilon).
 \tag{1.2}
\]

No located result rules out (1.1) or (1.2) once a simple uniformly rightmost
branch and a uniform relative complement estimate have been proved. What the
literature does rule out is the shortcut from an instantaneous spectral
abscissa or a finite-dimensional eigensolver to either formula. Nonnormal
transient growth, defective spectral clusters, embedded eigenvalues, and
nonuniform evolution constants can all add polynomial or
\(\exp(o(\varepsilon^{-1}))\) factors.

The exact boundary is therefore:

| Question | Literature decision |
|---|---|
| Exact decaying two-harmonic periodic shear already treated? | **No located collision.** |
| Moving shear with rigorously selected transient exponential growth? | **Yes, but only coarse two-sided rates in a different near-Couette problem.** |
| Frozen Rayleigh/Orr--Sommerfeld simple unstable modes and complementary decay? | **Yes, for other stationary profiles, domains, and scalings.** |
| Abstract nonselfadjoint adiabatic tracking for unbounded closed generators? | **Yes, conditionally.** The hypotheses include the branch, gap, regular projection, and bounded/contractive shifted evolution that R0.73I still has to prove. |
| A black-box theorem yielding (1.2) for the singular family \(B_\varepsilon=B_0-\varepsilon L\)? | **No located theorem.** |
| A literature obstruction to a rank-one matching action after all contracts pass? | **None located.** |

## 2. What is being compared

R0.73H uses

\[
 G_\Lambda(D)=\|S_{1,\Lambda}(D,0)\phi_\Lambda\|_2,
 \qquad D=d_0<1/450,
 \tag{2.1}
\]

where the current record chooses a unit vector in a frozen top spectral
subspace but does not yet prove that this subspace is rank one. The inherited
endpoint \(d_0\) is also shrinkable rather than canonical. In contrast, the
R0.73I target sets \(\varepsilon=\Lambda^{-1}\), proves a unique simple
rightmost branch \(P_\varepsilon(d)\), fixes the phase by an explicit anchor,
and defines

\[
 G_\varepsilon(D)
 =\|U_\varepsilon(D/\varepsilon,0)h_\varepsilon(0)\|_2.
 \tag{2.2}
\]

Consequently, a paper about a propagator norm, a specially constructed datum,
or a frozen unstable eigenmode is relevant precedent but is not automatically
a theorem about either (2.1) or (2.2).

Three accuracy levels must also remain separate:

1. **Normalized action only:**
   \(\varepsilon\log G_\varepsilon(D)\to\mathcal A(D)\). Polynomial
   prefactors and every \(\exp(o(\varepsilon^{-1}))\) factor disappear here.
2. **Matching bounded prefactor:**
   \(\log G_\varepsilon=\mathcal A/\varepsilon+O(1)\). Polynomial and
   stretched-exponential factors are forbidden.
3. **Two-term expansion:**
   \(\log G_\varepsilon=\mathcal A/\varepsilon+\mathcal C_D+O(\varepsilon)\).
   This additionally identifies the first viscous and geometric corrections.

The present R0.73I Contracts I1--I3 target level 2. Level 3 is a later,
strictly stronger target.

## 3. Direct time-dependent and heat-evolving shear results

### 3.1 Li--Masmoudi--Zhao: the closest moving-shear lower/upper growth theorem

Hui Li, Nader Masmoudi, and Weiren Zhao, *A dynamical approach to the study
of instability near Couette flow*, Communications on Pure and Applied
Mathematics 77 (2024), 2863--2946;
[journal DOI](https://doi.org/10.1002/cpa.22183),
[author preprint](https://arxiv.org/abs/2203.10894).

Theorem 1.1 treats the two-dimensional domain \(\mathbb T\times\mathbb R\).
It constructs heat-evolving shears \(b_\nu(t,y)\) at distance comparable to
\(\nu^{1/2-\delta_0}\) from Couette flow and a selected initial perturbation.
For

\[
 0\le t\le T,
 \qquad
 T=\varepsilon_1\nu^{-1/3+(2/3)\delta_0}\log(\nu^{-1}),
\]

the \(k=\pm1\) modes satisfy two-sided bounds of the form

\[
 c\|\omega_{\rm in}\|e^{c\nu^{1/3-(2/3)\delta_0}t}
 \le \|\omega_{\pm1}(t)\|_2
 \le
 C\|\omega_{\rm in}\|e^{C\nu^{1/3-(2/3)\delta_0}t}.
 \tag{3.1}
\]

At the endpoint this is polynomial amplification in \(\nu^{-1}\). The paper
deliberately obtains the growth dynamically, without using an eigenvalue or
pseudospectrum calculation.

**Usable for R0.73I:** it is the strongest located primary precedent that a
genuinely time-dependent viscous shear can support a rigorously selected
transient exponential growth law.

**Not supplied:** the constants in the upper and lower exponents are
different; there is no integrated frozen rightmost eigenvalue, no canonical
rank-one Riesz branch, no fixed slow interval of the R0.73I type, and no
bounded compensated prefactor. Its profile, domain, norm, and viscosity/time
scaling all differ from R0.73I. Thus (3.1) neither proves nor conflicts with
(1.1).

### 3.2 Li--Zhao: a heat-evolving stable-to-unstable frozen spectrum

Hui Li and Weiren Zhao, *Viscosity driven instability of shear flows without
boundaries*, Journal de Mathématiques Pures et Appliquées 200 (2025), 103724;
[journal DOI](https://doi.org/10.1016/j.matpur.2025.103724),
[author preprint](https://arxiv.org/abs/2410.23798).

Theorem 1.1 constructs, for every \(\nu>0\), a monotone shear on
\(\mathbb T\times\mathbb R\) satisfying the heat equation. Initially every
nonzero-wave-number frozen Rayleigh operator has no point spectrum. At
\(\widetilde T=\widetilde C(\gamma)\nu^{-1}\), the \(k=\pm1\) operator has an
embedded neutral eigenvalue; on
\((\widetilde T,T]\), with \(T=C(\gamma)\nu^{-1}\), it has a unique unstable
frozen eigenvalue \(c=ic_i(t)\), and \(c_i(T)=\gamma\). The authors explicitly
leave the corresponding unforced nonlinear evolution instability for future
work.

**Usable for R0.73I:** it proves that heat evolution can change the Rayleigh
spectral type and can create a unique frozen unstable branch. It is a strong
warning that a spectral hypothesis must hold on the whole interval, not only
at \(d=0\).

**Not supplied:** no selected Orr--Sommerfeld propagator estimate and no
integrated action. It is a frozen-time spectral transition theorem, not an
adiabatic evolution theorem.

### 3.3 Li--Zhao: stable moving shear and a time-dependent wave operator

Hui Li and Weiren Zhao, *Asymptotic stability in the critical space of 2D
monotone shear flow in the viscous fluid*, Communications in Mathematical
Physics 405 (2024), article 267;
[journal DOI](https://doi.org/10.1007/s00220-024-05155-8),
[author preprint](https://arxiv.org/abs/2306.03555).

The main assumption requires, for every \(t\ge0\), that the frozen Rayleigh
operator of the heat-evolving monotone shear have neither eigenvalues nor
embedded eigenvalues. The main theorem gives nonlinear stability at the
\(\nu^{1/2}\) critical size, enhanced dissipation
\(e^{-c\nu^{1/3}t}\) of nonzero vorticity modes, and inviscid-damping
estimates with constants uniform in \(\nu\). Its proof constructs a
time-dependent wave operator for the moving Rayleigh operator.

**Usable for R0.73I:** this is direct evidence that an interval-uniform
operator conjugation can control a heat-evolving nonlocal shear problem.

**Not supplied:** it assumes the stable spectral regime and proves decay,
not tracking of an isolated unstable eigenline relative to its complement.
The wave operator does not replace the R0.73I branch, projection, or relative
dichotomy proof.

### 3.4 Lin--Xu: the closest unforced periodic heat-decaying geometry

Zhiwu Lin and Ming Xu, *Metastability of Kolmogorov flows and inviscid damping
of shear flows*, Archive for Rational Mechanics and Analysis 231 (2019),
1811--1852;
[journal DOI](https://doi.org/10.1007/s00205-018-1311-8),
[author preprint](https://arxiv.org/abs/1707.00278).

The exact linearized periodic equation includes

\[
 \partial_t\omega
 =\nu\Delta\omega-e^{-\nu t}\sin y\,\partial_x(1+\Delta^{-1})\omega.
 \tag{3.2}
\]

For \(\mathbb T_\alpha\), \(\alpha>1\), their first linear theorem states
that for any fixed \(\tau,\delta>0\), sufficiently small \(\nu\) reduces the
non-shear \(L^2\) norm by the factor \(\delta\) at time \(\tau/\nu\). At
\(\alpha=1\), the same conclusion holds after removing the anomalous
\(\{\cos x,\sin x\}\) modes.

**Usable for R0.73I:** (3.2) is the closest located theorem in periodic,
unforced, heat-decaying shear geometry.

**Not supplied:** the result is stable/metastable and treats a single
harmonic. It has no selected unstable eigenbranch and no matching positive
action.

## 4. Abstract adiabatic theory: what can and cannot be imported

### 4.1 Nenciu--Rasche is a finite-dimensional precedent, not the PDE theorem

Gheorghe Nenciu and Günter Rasche, *On the adiabatic theorem for
nonself-adjoint Hamiltonians*, Journal of Physics A 25 (1992), 5741--5751;
[journal DOI](https://doi.org/10.1088/0305-4470/25/21/027),
[author publication record](https://www.imar.ro/~ghnenciu/).

The paper treats a slowly driven **two-level** nonselfadjoint Hamiltonian.
Its abstract states that general adiabatic following can fail, but survives
for the subspace corresponding to the eigenvalue with largest imaginary part
(the least dissipative eigenvalue); the restricted evolution has a full
asymptotic expansion, including an explicit first correction beyond Berry's
phase.

This is the closest located finite-dimensional precedent for the logic
“isolated dominant branch + dynamic phase + geometric/first correction.” It
does **not** treat an unbounded Orr--Sommerfeld generator, a continuous
spectral complement, a viscosity-dependent domain, or the singular limit
\(B_\varepsilon=B_0-\varepsilon L\). It therefore cannot be cited as the
proof of (1.1) or (1.2).

### 4.2 Abou Salem--Fröhlich: unbounded closed, nonnormal generators

Walid K. Abou Salem and Jürg Fröhlich, *Adiabatic Theorems for Quantum
Resonances*, Communications in Mathematical Physics 273 (2007), 651--675;
[journal DOI](https://doi.org/10.1007/s00220-007-0198-2),
[author preprint](https://arxiv.org/abs/math-ph/0607054).

Section 3.2, Theorem 3.2, is the closest directly usable unbounded-operator
black box found in this audit. It assumes:

- closed operators \(A(s)\) with a common dense domain;
- a uniformly bounded generated evolution;
- differentiability of a reference resolvent and boundedness of
  \(A(s)\dot R(-1,s)\);
- a simple isolated eigenvalue with a uniform spectral gap;
- a twice differentiable Riesz projection.

The adiabatic generator adds \(-\tau^{-1}[\dot P,P]\), intertwines the
spectral subspaces exactly, and the exact and adiabatic propagators differ by
\(O(\tau^{-1})\) uniformly on the slow interval. The paper also states that
if the evolution is only quasi-bounded by \(Me^{\gamma t}\), the error becomes
\(Ce^{\tau\gamma}/\tau\), useful only on the limited regime
\(1\ll\tau\ll\gamma^{-1}\).

**Conditional import:** after shifting by the selected scalar growth and
proving a uniformly bounded relative evolution, this theorem supplies the
correct rank-one intertwining mechanism with \(\tau=\varepsilon^{-1}\).

**Unclosed R0.73I hypotheses:** the theorem assumes rather than proves the
continuum simple branch, uniform isolation, \(C^2\) projection, and bounded
shifted evolution. Its generator family is fixed while the adiabatic
parameter tends to zero. R0.73I instead has an additional singular
dependence \(B_\varepsilon=B_0-\varepsilon L\); applying the theorem to each
\(\varepsilon\) requires every constant to be uniform in that second role of
\(\varepsilon\).

### 4.3 Joye: analytic-in-time closed generators and the nilpotent warning

Alain Joye, *General Adiabatic Evolution with a Gap Condition*,
Communications in Mathematical Physics 275 (2007), 139--162;
[journal DOI](https://doi.org/10.1007/s00220-007-0299-y),
[author preprint](https://arxiv.org/abs/math-ph/0608059),
[author PDF](https://www-fourier.univ-grenoble-alpes.fr/~joye/genadiabcmp.pdf).

Hypotheses H1--H3 treat a family of closed operators on a common domain in a
Banach space, analytic in the **slow parameter**, with finitely many isolated
eigenvalues of constant finite algebraic multiplicity and a uniform gap.
For the infinite-dimensional complement, H3 requires a shifted contraction
semigroup and a resolvent condition. Theorem 2.1 constructs
superadiabatic projections \(P^*=P+O(\varepsilon)\), exact intertwining, and
an exponentially accurate approximation relative to the dominant dynamic
phase.

For a finite spectral block the theorem permits the factor

\[
 \exp(d_j/\varepsilon^{\beta_j}),
 \qquad 0\le\beta_j<1.
 \tag{4.1}
\]

It states that \(d_j=0\) exactly when the eigen-nilpotent on that block
vanishes. The paper also gives a finite-dimensional example with
\(\exp(c/\sqrt\varepsilon)\) growth caused by nilpotent structure.

**Consequence:** (4.1) preserves a normalized action but destroys the
bounded-prefactor conclusion. A simple rank-one R0.73I branch has no
nilpotent, so Joye's result supports the proposed route **provided H3 is
proved**. A non-simple top cluster does not.

“Analytic in the slow parameter” here must not be confused with “each frozen
operator generates an analytic semigroup.” The theorem's complement
contraction/resolvent hypothesis is substantive; sectoriality or a real
spectral gap has not been obtained for R0.73I merely by citing this paper.

### 4.4 Schmid: Kato-stable closed operators on a common domain

Jochen Schmid, *Adiabatic theorems for general linear operators with
time-independent domains*, Reviews in Mathematical Physics 31 (2019),
1950014;
[journal DOI](https://doi.org/10.1142/S0129055X19500144),
[author preprint](https://arxiv.org/abs/1804.11213).

Condition 2.9 assumes densely defined closed operators on a common domain,
Kato \((M,\omega)\)-stability, and
\(A\in W_*^{1,1}(I,\mathcal L(Y,X))\), where \(Y\) carries a reference graph
norm. Theorem 3.1, with \(\omega=0\), a continuously varying compact
uniformly isolated spectral subset, and
\(P\in W_*^{2,1}(I,\mathcal L(X))\), compares the evolution of
\(A/\varepsilon\) with that of
\(A/\varepsilon+[P',P]\): the latter intertwines exactly and the operator-norm
difference is \(O(\varepsilon)\).

**Conditional import:** this is an appropriate general framework after a
scalar shift if one proves uniform Kato stability of the shifted full and
complement evolution.

**Unclosed R0.73I hypotheses:** a real spectral gap does not imply this Kato
stability for a nonnormal generator. In addition, the reference graph norm
for \(B_\varepsilon\) can become singular as \(\varepsilon\downarrow0\).
Schmid's theorem is not itself a uniform double-parameter theorem for that
loss of domain at \(\varepsilon=0\).

### 4.5 Avron--Fraas--Graf--Grech: contraction generators and prepared slow manifolds

J. E. Avron, M. Fraas, G. M. Graf, and P. Grech, *Adiabatic Theorems for
Generators of Contracting Evolutions*, Communications in Mathematical
Physics 314 (2012), 163--191;
[journal DOI](https://doi.org/10.1007/s00220-012-1504-1),
[author preprint](https://arxiv.org/abs/1106.4661).

In the gapped setting the paper assumes that every \(L(s)\) generates a
contraction, that its range is closed with
\(\mathcal B=\ker L\oplus\operatorname{ran}L\), and that zero remains
uniformly isolated. Theorem 6 gives an arbitrary-order slow-manifold
expansion, with a uniformly bounded remainder, for specially prepared
initial data. Theorem 9 shows that the projected slow component follows
parallel transport up to \(O(\varepsilon)\), while explicitly making no
claim about the fast component.

**Conditional import:** after shifting the rightmost eigenvalue to zero,
this supplies a model for a power expansion and parallel transport.

**Not supplied:** the needed contraction property, direct-sum decomposition,
and control of the fast complement. The exact R0.73I launch also has to be
shown to lie on the required slow manifold to the needed order.

### 4.6 Joye 1995: a genuinely singular perturbation, but selfadjoint

Alain Joye, *An Adiabatic Theorem for Singularly Perturbed Hamiltonians*,
Annales de l'I.H.P. Physique théorique 63 (1995), 231--250;
[primary archive PDF](https://www.numdam.org/item/AIHPA_1995__63_2_231_0.pdf),
[author preprint](https://arxiv.org/abs/funct-an/9411001).

The paper considers a selfadjoint \(H_0(t)\) with a gap perturbed by
\(\varepsilon H_1(t)\), where \(H_1\) may have a smaller domain and the full
operator need not retain the gap. Its adiabatic proposition constructs an
intertwining comparison evolution with an \(O(\varepsilon)\) error.

This is structurally close to the singular term \(-\varepsilon L\), but the
proof relies on selfadjoint/unitary structure. It does not supply a
nonnormal Orr--Sommerfeld theorem.

### 4.7 Evolution dichotomy is an additional theorem, not a consequence of a gap

Yuri Latushkin and Roland Schnaubelt, *Evolution Semigroups, Translation
Algebras, and Exponential Dichotomy of Cocycles*, Journal of Differential
Equations 159 (1999), 321--369;
[journal DOI](https://doi.org/10.1006/jdeq.1999.3668),
[author PDF](https://www.math.kit.edu/iana3/~schnaubelt/media/aht.pdf).

For an exponentially bounded strongly continuous cocycle on a Banach space,
the paper proves equivalences between exponential dichotomy, hyperbolicity of
the associated evolution semigroup, and an imaginary-axis resolvent
condition for its generator. It also proves perturbative robustness and a
Perron-type characterization.

This gives an appropriate language and possible proof route for the R0.73I
relative complement. It is not a sharp action theorem and does not infer a
nonautonomous dichotomy from the instantaneous spectra alone.

### 4.8 Specific outcome of the analytic-semigroup search

No located primary theorem starts only from “a slowly varying family of
sectorial/nonselfadjoint parabolic generators with an isolated rightmost
eigenvalue” and concludes the two-term norm law (1.2). Analytic-semigroup
generation can provide well-posedness, smoothing, and frozen resolvent
estimates, but it does not identify the growth bound of a nonnormal
nonautonomous complement with its spectral bound.

The applicable primary results found here use stronger evolution hypotheses:
bounded shifted evolution in Abou Salem--Fröhlich, the explicit H3
contraction/resolvent condition in Joye, Kato stability in Schmid, or
contraction generation plus a direct-sum condition in Avron et al. Thus a
future R0.73I proof may use sectorial/analytic-semigroup estimates to verify
one of those hypotheses, but “analytic parabolic” is not by itself the
missing adiabatic certificate.

## 5. Autonomous Orr--Sommerfeld/Rayleigh precedents and nonnormal warnings

### 5.1 Colombo--Dolce--Montalto--Ventura: stationary periodic rank-one mode

Maria Colombo, Michele Dolce, Riccardo Montalto, and Paolo Ventura,
*Long-wave instability of periodic shear flows for the 2D Navier--Stokes
equations* (2025 preprint);
[author preprint](https://arxiv.org/abs/2509.18070).

Theorem 1.1 treats a forced stationary zero-average
\(U\in H^3(\mathbb T)\) on an elongated torus. If
\(\|\partial_y^{-1}U\|_2>\nu\) and \(\alpha|k|\le\delta_0\nu\), then the
given Fourier row has exactly one simple unstable eigenfunction, all
remaining spectrum is pure point in \(\{\operatorname{Re}z\le-\nu/2\}\),
and

\[
 \left|\lambda_{\nu,\alpha k}
 -\frac{(\alpha k)^2}{\nu}
   (\|\partial_y^{-1}U\|_2^2-\nu^2)\right|
 \le C\frac{(\alpha|k|)^3}{\nu^2}.
 \tag{5.1}
\]

The eigenfunction is \(O(\alpha|k|/\nu)\)-close to \(U\) in \(L^2\).

**Usable for R0.73I:** a strong periodic, infinite-dimensional precedent for
simple-mode counting and an explicit spectral separation.

**Not supplied:** it is stationary and forced, in the long-wave regime
\(\alpha\ll\nu\); R0.73I is a heat-evolving fixed row with
\(\Lambda\to\infty\). It gives no moving-branch propagator action.

### 5.2 Bian--Grenier: autonomous adjoint-selected mode plus Green remainder

Dongfen Bian and Emmanuel Grenier, *Asymptotic behaviour of solutions of
linearized Navier Stokes equations in the long waves regime* (2023
preprint); [author preprint](https://arxiv.org/abs/2312.16938).

For an analytic concave half-plane shear with no-slip boundary, Theorem 1.1
constructs a rank-one contribution selected by an adjoint eigenvector and an
exponentially decaying Green remainder. The unstable window lies between
scales comparable to \(\nu^{1/4}\) and \(\nu^{1/6}\). The stable remainder
has a nonnormal amplification factor \(\eta(\alpha,\nu)\), as large as a
constant times \(\nu^{-1/4}\) in one stated regime.

**Usable for R0.73I:** this is an autonomous PDE analogue of “left/right
selected rank-one growth + controlled complement.”

**Boundary:** the polynomial factor is invisible to
\(\varepsilon\log G\) but is incompatible with an \(\varepsilon\)-uniform
bounded prefactor when the parameters are identified. The geometry,
boundary layer, long-wave scaling, and stationary generator are different.
The paper's abstract and displayed theorem use different powers for one
growth-rate description, so this audit relies only on the unambiguous
rank-one/Green-remainder and amplification statements above.

### 5.3 Grenier--Nguyen: stationary semigroup exponent with an arbitrary margin

Emmanuel Grenier and Toan T. Nguyen, *Sharp bounds for the resolvent of
linearized Navier Stokes equations in the half space around a shear profile*,
Journal of Differential Equations 269 (2020), 9384--9403;
[journal DOI](https://doi.org/10.1016/j.jde.2020.06.046),
[author preprint](https://arxiv.org/abs/1703.00881).

Theorem 1.1 assumes a smooth stationary half-space boundary-layer profile
with a maximal unstable Euler eigenvalue \(\lambda_0\). For fixed Fourier
frequency and every \(\tau>0\), it proves, uniformly for \(\nu\le1\),

\[
 \|e^{L_\alpha t}\omega\|_{\beta,\gamma}
 \le C_\tau e^{(\operatorname{Re}\lambda_0+\tau)t}
 \|\omega\|_{\beta,\gamma}.
 \tag{5.2}
\]

This is a sharp autonomous exponential upper estimate in a boundary-layer
vorticity norm. The arbitrary \(\tau\) margin is not a bounded prefactor at
the exact exponent, and no moving action is present.

### 5.4 Li--Ren--Wang--Zhang: embedded spectrum can create large growth

Hui Li, Siqi Ren, Yuxi Wang, and Guoqing Zhang, *Instability of shear flows
with neutral embedded eigenvalues* (2026 preprint);
[author preprint](https://arxiv.org/abs/2602.07807).

Theorem 1.2 assumes a monotone shear on \(\mathbb T\times\mathbb R\) whose
Rayleigh operator has one embedded eigenvalue and no other eigenvalues. For
every \(M\), it constructs unit \(L^\infty+L^2\) initial data and a time at
which both norms are at least \(M\). Theorem 1.3 gives at least linear growth
when the embedded eigenvalue is multiple. Corollary 1.6 shows that any
prescribed finite amount of this \(L^2\) growth persists for sufficiently
small viscosity in the Orr--Sommerfeld evolution.

This is a rigorous, current nonnormal warning. It does not obstruct the
R0.73I route if Contract I1 gives an isolated simple eigenvalue with a
uniform gap; its assumptions deliberately violate that contract.

### 5.5 Trefethen--Trefethen--Reddy--Driscoll: spectrum alone is insufficient

Lloyd N. Trefethen, Anne E. Trefethen, Satish C. Reddy, and Tobin A.
Driscoll, *Hydrodynamic Stability Without Eigenvalues*, Science 261 (1993),
578--584;
[journal DOI](https://doi.org/10.1126/science.261.5121.578),
[author PDF](https://people.maths.ox.ac.uk/trefethen/publication/PDF/1993_57.pdf).

The paper gives the classic pseudospectral/numerical demonstration that
spectrally stable Couette and Poiseuille linearizations can exhibit very
large transient amplification because their eigenvectors are nonorthogonal.
It is not a theorem for the R0.73I family, but it is decisive evidence against
replacing an evolution estimate by instantaneous eigenvalue plots.

## 6. Audit of the proposed two-term law

This section is an inference from the cited adiabatic machinery, not a claim
proved by any one cited paper.

Write the slow equation as

\[
 \varepsilon\partial_d v=B_\varepsilon(d)v.
 \tag{6.1}
\]

Let \(q_\varepsilon(d)\) and \(\ell_\varepsilon(d)\) be right and left
eigenvectors of a simple branch, normalized by
\(\langle\ell_\varepsilon,q_\varepsilon\rangle=1\). On the exact rank-one
adiabatic equation, the scalar amplitude satisfies

\[
 a'(d)=\left[
 \frac{\lambda_\varepsilon(d)}{\varepsilon}
 -\langle\ell_\varepsilon(d),q_\varepsilon'(d)\rangle
 \right]a(d).
 \tag{6.2}
\]

Suppose, uniformly on \([0,D]\), one proves

\[
 \lambda_\varepsilon
 =\lambda_0+\varepsilon\mu+O(\varepsilon^2),
 \tag{6.3}
\]

together with a sufficiently regular expansion of the left/right branch and
a relative \(O(\varepsilon)\) comparison between the exact selected orbit and
(6.2). Then (6.2) formally yields

\[
 \begin{aligned}
 \mathcal C_D={}&
 \int_0^D\operatorname{Re}\mu(s)\,\mathrm ds
 -\operatorname{Re}\int_0^D
   \langle\ell_0(s),q_0'(s)\rangle\,\mathrm ds\\
 &+\log\|q_0(D)\|_2-\log\|q_0(0)\|_2.
 \end{aligned}
 \tag{6.4}
\]

The whole expression is invariant under a nonzero change of eigenvector
gauge. If \(q_0(d)\) is \(L^2\)-normalized for every \(d\), the endpoint
norm terms vanish.

For \(B_\varepsilon=B_0-\varepsilon L\), standard first-order eigenvalue
perturbation suggests

\[
 \mu(d)=-\langle\ell_0(d),Lq_0(d)\rangle.
 \tag{6.5}
\]

Equation (6.5) is **formal here** because \(L\) is unbounded and the
\(\varepsilon\downarrow0\) limit is singular. It becomes a theorem only
after proving the necessary domain/adjoint regularity and a uniform
first-order branch expansion. Under those conditions, (6.4) reduces to the
continuum counterpart of the finite R0.73I diagnostic

\[
 -\int_0^D\operatorname{Re}\left[
 \langle\ell_0,q_0'\rangle+\langle\ell_0,Lq_0\rangle
 \right]\,\mathrm dd.
\]

The current Contract I2 estimate
\(|\lambda_\varepsilon-\lambda_0|\le C\varepsilon\) is enough to keep the
eigenvalue contribution at \(O(1)\), but it does not identify a fixed
\(\mathcal C_D\) with \(O(\varepsilon)\) remainder. For (1.2), the minimum
additional package is:

1. the uniform second-order expansion (6.3), not merely an
   \(O(\varepsilon)\) bound;
2. uniform \(C^2\) left/right eigenvectors or equivalent Riesz-projection
   expansions in an appropriate operator topology;
3. a scalar-shifted full/complement evolution estimate giving a **relative**
   \(O(\varepsilon)\) adiabatic remainder;
4. a canonical initial anchor and controlled endpoint normalization.

Nenciu--Rasche demonstrates this kind of expansion in a two-level matrix
setting. Abou Salem--Fröhlich, Joye, Schmid, and
Avron--Fraas--Graf--Grech provide ingredients for unbounded closed
generators under strong hypotheses. None of them verifies this four-part
package for the R0.73I Orr--Sommerfeld family.

## 7. Exact consequences for Contracts I1--I4

### I1: unique simple rightmost inviscid branch

This remains a bespoke continuum spectral theorem. The stationary periodic
result of Colombo et al. demonstrates that exact mode counting and separation
are achievable, but in a different long-wave viscous regime. The Li--Zhao
stable-to-unstable construction shows why the contour, simplicity, and gap
must be interval-uniform. No cited paper proves them for the frozen R0.73I
two-harmonic Rayleigh operator.

### I2: uniform viscous continuation

The cited abstract theorems begin after a regular isolated branch exists.
They do not prove convergence from the viscous unbounded family to the
inviscid operator. R0.73I must prove the uniform contour, rank one,
projection convergence, branch regularity, and at least
\(\lambda_\varepsilon-\lambda_0=O(\varepsilon)\). The two-term target needs
(6.3).

### I3: matching selected gain

A uniform real-part gap is necessary but not sufficient. What is still
needed is a scalar-shifted full or complementary evolution estimate with
constants uniform in \(\varepsilon\). This is the role played by bounded
evolution in Abou Salem--Fröhlich, H3 in Joye, Kato stability in Schmid, or
contraction generation in Avron et al. One of these hypotheses must be
proved for the actual operator; it cannot be inferred from the spectrum of a
nonnormal generator.

If the branch is rank one and this relative evolution estimate passes, the
primary literature is consistent with
\(G_\varepsilon\asymp e^{\mathcal A/\varepsilon}\). If the selected block is
defective or genuinely multidimensional, the natural leading object is a
finite-dimensional cocycle/Lyapunov exponent, which need not equal the
integral of the pointwise maximal real eigenvalue.

### I4: backward action localization

An endpoint estimate alone is insufficient. The adiabatic/dichotomy bounds
must hold uniformly on every subinterval \([s,D]\), with the same phase
anchor and controlled constants. Latushkin--Schnaubelt supplies an abstract
dichotomy characterization, but the required interval-uniform estimates for
this PDE remain open.

## 8. Collision and obstruction conclusion

The literature search found no result that makes R0.73I redundant and no
result that forbids its matching action under the frozen contracts.

The nearest direct moving-shear theorem, Li--Masmoudi--Zhao, proves genuine
selected transient exponential growth but only between unequal coarse rates.
The nearest moving spectral theorem, Li--Zhao 2025, proves a frozen unique
unstable branch but explicitly stops before the evolving instability
problem. The nearest autonomous PDE decompositions, Colombo et al. and
Bian--Grenier, show that simple-mode counting and adjoint-selected
rank-one/complement formulas are possible in other regimes. The abstract
adiabatic papers show that (1.1), and conditionally (1.2), have a legitimate
operator-theoretic route.

They also identify the exact point where the new work lies:

\[
 \boxed{
 \text{continuum branch/gap}
 +\text{uniform singular viscous continuation}
 +\text{relative complement evolution}
 \Longrightarrow\text{matching action}.}
\]

No citation can replace those three proofs. Until they pass, the exact
R0.73I continuum upper action already proved from the numerical form remains
one-sided, the finite WKB residual remains diagnostic, and the site must keep
“canonicalSelectedBranch”, “matchingSelectedGainAction”, and
“twoTermSelectedGainAsymptotic” **OPEN**.

## 9. Search boundary

The audit searched the current primary-source literature through journal
pages, DOI records, author-hosted manuscripts, and author preprints, with
special attention to time-dependent/heat-evolving shears, Rayleigh and
Orr--Sommerfeld modes, nonselfadjoint adiabatic theorems for unbounded closed
generators, contraction/analytic evolution, exponential dichotomy, and
nonnormal transient growth. “No located theorem” is a documented
non-collision result for this search, not a claim that no related theorem can
exist anywhere. Any later collision check should search by the exact
operator family and by the three missing mechanisms in the boxed implication
above.
