# R0.73P bounded primary-source audit

**Status:** primary texts for the critical robustness and eventual-regularity
claims have been read theorem-by-theorem; the exact theorem text of Mucha
2001 remains unavailable in this environment and is deliberately not used to
close any release claim

**Audit question:** which parts of the R0.73P topology ladder are already
published, and does any verified theorem remove all higher-frequency
dependence from the initial \(L^2\) threshold?

## 1. Direct answer

The global \(H^{1/2}\) stability tube is a classical corollary, not a new
robustness theorem.  The decisive source is Burczak--Zaj\k{a}czkowski 2016,
which gives a quantitative periodic \(\dot H^\alpha\) robustness condition
for every \(\alpha\in[1/2,1]\).  At \(\alpha=1/2\), its exponent contains
\(\int\|\nabla u\|_2^4\), which is finite for every R0.73O reference orbit.

Mar\'in-Rubio--Robinson--Sadowski 2013 gives the earlier periodic
\(\dot H^{1/2}\) finite-time robustness theorem and the exact critical
energy inequality used for exponential synchronization.  Hoang--Martinez
2017 proves explicit eventual Gevrey regularity for every periodic
Leray--Hopf solution, with a starting time depending only on the initial
\(L^2\) norm and the Gevrey radius.

No verified source in this audit supplies a frequency-independent
\(L^2\)-only strong-regularity threshold from the initial time.  Mucha 2008
explicitly requires the \(L^2\) norm to be sufficiently small **compared to**
a higher Besov trace norm.  Mucha 2001 has the closest abstract-level claim,
but its complete theorem quantifiers were not accessible and are not
inferred from the abstract or from the 2008 paper.

## 2. Burczak--Zaj\k{a}czkowski 2016: quantitative critical robustness

**Source:** Jan Burczak and Wojciech M. Zaj\k{a}czkowski,
"Quantitative robustness of regularity for 3D Navier--Stokes system in
\(\dot H^\alpha\)-spaces," *Nonlinear Analysis: Real World Applications*
31 (2016), 513--532.

- [arXiv primary manuscript](https://arxiv.org/abs/1409.3485)
- [journal DOI](https://doi.org/10.1016/j.nonrwa.2016.03.001)

Theorem 1 works in the periodic cube \(Q_L=[0,L]^3\), with viscosity
\(\nu>0\), \(\alpha\in[1/2,1]\), and explicitly defined constants
\(K_2,K_3,K_4\).  If \(u\) is an \(\alpha\)-strong solution on
\([0,T_*]\), then for every \(T<T_*\) the proximity condition

\[
 \left(
 |u_0-v_0|_{\alpha,L}^2
 +K_4\int_0^T|f-g|_{\alpha-1,L}^2dt
 \right)
 \exp\!\left[
 K_3\int_0^T
 \|\nabla u(t)\|_{L^{3/(2-\alpha)}}^4dt
 \right]
 <\left({\bar\nu\over K_2}\right)^2
 \tag{2.1}
\]

makes every Leray--Hopf comparison solution \(\alpha\)-strong up to
\(T\).  The theorem also bounds

\[
 \sup_{0\le t\le T}|u-v|_{\alpha,L}^2
 +(\nu-\bar\nu-\varepsilon_1-\varepsilon_2)
 \int_0^T|u-v|_{\alpha+1,L}^2dt.
 \tag{2.2}
\]

At \(\alpha=1/2\), the integral in (2.1) is
\(\int\|\nabla u\|_2^4\).  Its finiteness on \([0,\infty)\) produces a
single positive radius valid for every finite \(T\) and every starting time
along the R0.73O orbit.  This is the primary published input for the
R0.73P critical tube.

The normalization transfer was checked explicitly rather than hidden in a
generic constant.  R0.73P uses \([0,2\pi]^3\) with normalized Haar measure.
At \(L=2\pi\), the paper's coefficient norm \(|\cdot|_{s,2\pi}\) equals the
released Stokes norm, while its physical Lebesgue gradient satisfies

\[
 \|\nabla z\|_{L^2(dx)}^4=(2\pi)^6|z|_1^4.
\]

Thus the exponential constant in the released action is precisely
\(K_3'=(2\pi)^6K_3^c\), with \(K_2^c,K_3^c,K_4^c\) copied and specialized
in `r073p_critical_frequency_proof.md` Section 4.

The paper itself says that its Theorem 1 refines and generalizes the earlier
Mar\'in-Rubio--Robinson--Sadowski result.  It also identifies numerical
verification in critical spaces as an open program.  R0.73P therefore makes
no novelty claim for the robustness theorem.

## 3. Mar\'in-Rubio--Robinson--Sadowski 2013: the critical difference inequality

**Source:** Pedro Mar\'in-Rubio, James C. Robinson, and Witold Sadowski,
"Solutions of the 3D Navier--Stokes equations for initial data in
\(\dot H^{1/2}\): robustness of regularity and numerical verification of
regularity for bounded sets of initial data in \(\dot H^1\)," *Journal of
Mathematical Analysis and Applications* 400 (2013), 76--85.

- [institutional full text](https://idus.us.es/server/api/core/bitstreams/b0e9a174-2dd3-484d-9a9d-39ec5ee1323c/content)
- [journal DOI](https://doi.org/10.1016/j.jmaa.2012.10.064)

The paper uses the periodic cube \([0,2\pi]^3\), zero mean, and divergence-
free homogeneous Sobolev spaces.

- Theorem 1 gives local critical existence through a heat-flow condition.
- Theorem 2 upgrades a critical solution with \(H^1\) initial data to
  \(L^\infty H^1\cap L^2H^2\).
- Theorem 3 proves finite-time robustness in \(\dot H^{1/2}\).

For equal forcing, the proof of Theorem 3 derives

\[
 {d\over dt}|w|_{1/2}^2+{1\over2}|w|_{3/2}^2
 \le C|u|_1^4|w|_{1/2}^2
 +C|w|_{1/2}^2|w|_{3/2}^2.
 \tag{3.1}
\]

This is the exact bootstrap form used in the R0.73P exponential critical
synchronization proof.  The theorem statement writes the initial
\(H^{1/2}\) distance without a square, whereas the proof closes a squared
energy condition; after changing universal constants both give a positive
radius of the same exponential form.  R0.73P therefore states generic or
computable constants and does not identify the two literal prefactors.

Equation (9) of the paper gives

\[
 \|z\|_{H^1}^4
 \le \|z\|_{H^{1/2}}^2\|z\|_{H^{3/2}}^2,
 \tag{3.2}
\]

which places every critical solution in \(L^4_tH^1_x\hookrightarrow
L^4_tL^6_x\), a Serrin class.  This supports the persistence of an initial
\(H^3\) solution inside the global critical solution.

The paper's Theorem 12 does not supply an unconditional finite covering of
an \(\dot H^1\) ball.  Under its Definition 4, “numerically verifiable” is
conditional: if the ball-wide regularity statement is true, the algorithm
terminates after finitely many checks.  R0.73P therefore uses no numerical
ball-coverage claim from that theorem.

## 4. Hoang--Martinez 2017: explicit eventual Gevrey regularity

**Source:** Luan T. Hoang and Vincent R. Martinez, "Asymptotic expansion in
Gevrey spaces for solutions of Navier--Stokes equations," *Asymptotic
Analysis* 104 (2017), 167--190.

- [arXiv primary manuscript](https://arxiv.org/abs/1511.03523)
- [journal DOI](https://doi.org/10.3233/ASY-171429)

Theorem 2.4 applies to every periodic Leray--Hopf weak solution.  For every
\(\sigma>0\), it gives

\[
 |v(t)|_{\alpha+1/2,\sigma}
 \le D_{\alpha,\sigma}e^{-t},
 \qquad \alpha\ge0,
 \quad t\ge T,
 \tag{4.1}
\]

with the explicit choice

\[
 T=24\sigma+34+
 \bigl(\log(12C_1\|v_0\|_2)\bigr)_+.
 \tag{4.2}
\]

The time is independent of \(\alpha\).  Replacing \(\|v_0\|_2\) by an
energy-ball radius \(M\) gives a common upper time for every initial datum in
that ball and every Leray--Hopf selection.  This verifies the quantifier
structure of the self-contained R0.73P eventual-regularity proof.

The source does not say that the weak solution was regular before \(T\), and
eventual Gevrey regularity does not propagate backward.  It therefore
supports the delayed theorem and simultaneously preserves the early-time
Clay gap.

## 5. Mucha 2008: high-norm dependence is explicit

**Source:** Piotr B. Mucha, "Global solutions, structure of initial data and
the Navier--Stokes equations," *Banach Center Publications* 81 (2008),
277--286.

- [official full text](https://www.impan.pl/shop/en/publication/transaction/download/product/86758)
- [DOI](https://doi.org/10.4064/bc81-0-18)

Theorem 1.2 assumes

\[
 v_0\in B^{2-2/q}_{p,q}(\Omega)\cap L^2(\Omega),
 \qquad {3\over p}+{2\over q}<3,
 \tag{5.1}
\]

and states that \(\|v_0\|_2\) is sufficiently small **compared to**
\(\|v_0\|_{B^{2-2/q}_{p,q}}\).  The proof first chooses an interpolation
parameter depending on the higher trace bound and only then imposes the
\(L^2\) restriction.  Thus this theorem allows a large higher norm in the
sense that no fixed universal upper bound is imposed, but its admissible
\(L^2\) size still depends on that norm.

It cannot be cited as a frequency-independent \(L^2\)-only threshold.

## 6. Mucha 2001: closest collision, incomplete theorem access

**Source:** Piotr B. Mucha, "Stability of Nontrivial Solutions of the
Navier--Stokes System on the Three Dimensional Torus," *Journal of
Differential Equations* 172 (2001), 359--375.

- [journal DOI and abstract](https://doi.org/10.1006/jdeq.2000.3863)

The verified abstract says that a \(W^{2,1}_r\) perturbation norm can be
controlled when the perturbing initial data are sufficiently small in
\(L^2\), and that unforced two-dimensional flows are stable.  The abstract
does not expose whether the \(L^2\) threshold depends on a higher trace norm,
on the reference solution, or on a local-existence bound.

The full theorem was not obtainable from the publisher in this environment:
the text-mining endpoint returned metadata only, the article page returned a
robot challenge, and no author-repository copy was located in the bounded
search.  R0.73P therefore records the source as collision-sensitive and uses
none of its unverified quantifiers.  In particular, the dependence in Mucha
2008 is not retroactively imposed on the 2001 theorem, and the 2001 abstract
is not promoted to a uniform \(L^2\)-only theorem.

## 7. Classical critical theory and the topology boundary

[Fujita--Kato](https://doi.org/10.1007/BF00276188) supplies the classical
critical local theory behind the \(H^{1/2}\) solution class.  Standard
Serrin regularity and weak--strong uniqueness allow an \(H^3\) local
solution to persist whenever it belongs globally to the critical class.

The following implications are therefore literature-established or direct
corollaries:

\[
 \text{finite critical orbit action}
 \Longrightarrow
 \text{positive global }H^{1/2}\text{ radius},
 \tag{7.1}
\]

and

\[
 \operatorname{supp}\widehat w_0\subset\{|k|\le N\},
 \quad \|w_0\|_2<R_{1/2}N^{-1/2}
 \Longrightarrow
 \text{global strong continuation}.
 \tag{7.2}
\]

The following implication is not supplied by any verified source:

\[
 \|w_0\|_2<\delta[u]
 \quad\Longrightarrow\quad
 \text{strong continuation from the initial time},
 \tag{7.3}
\]

uniformly over arbitrarily high frequencies.

## 8. Novelty and value decision

The R0.73P main theorem is best classified as a rigorous, topology-matched
synthesis of published robustness theory, the R0.73O orbit actions, and a
newly explicit comparison of frequency-transfer gates inside this research
program.  Its value is that it replaces the crude \(N^{-3}\) entry by the
critical \(N^{-1/2}\) entry and isolates the unknown early weak window.

It is not a new Fujita--Kato theorem, not a new eventual-regularity theorem,
and not evidence that the Clay problem is solved.  A genuinely stronger
future direction would need a relative heat-flow or critical Besov envelope
strictly larger than the \(H^{1/2}\) ball, followed by a fresh collision
audit.

```text
criticalH12Robustness=LITERATURE_ESTABLISHED
explicitPeriodicCriticalConstants=LITERATURE_ESTABLISHED
eventualGevreyForEveryLerayHopf=LITERATURE_ESTABLISHED
Mucha2008L2ThresholdIndependentOfHighTraceNorm=FALSE
Mucha2001ExactThresholdDependence=UNVERIFIED_COLLISION_SENSITIVE
uniformL2OnlyStrongThreshold=OPEN
noveltyOrPriorityClaim=FORBIDDEN
clayConclusion=OPEN
```
