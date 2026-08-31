# R0.73O bounded literature audit

**Search date:** 2026-08-31

**Status:** bounded primary-source audit complete.  The Mucha 2001 full
theorem text was not retrievable as machine-readable primary text, so its
exact constants remain an explicit release caveat rather than being inferred
from the abstract.

**Question:** Which parts of R0.73O are already classical, does any checked
source prove a uniform \(L^2\)-input stability threshold for arbitrary regular
perturbations on \(\mathbb T^3\), and can a forced nondecaying equilibrium give
a rigorous fixed-distance escape while every witnessing solution remains
smooth?

## 1. Search protocol and stop rule

The audit used two waves.

1. **Direct global-solution stability:** large strong solutions, openness of
   the global-data set, critical-space stability, and periodic-torus results.
2. **Collision and contrast:** \(L^2\)-small/high-norm-large perturbations,
   forced Kolmogorov spectral instability, and linear-to-nonlinear transfer.

Priority was given to original papers, author or journal PDFs, Numdam,
Centre Mersenne, arXiv versions of the published paper, and official journal
metadata. Search stopped after the exact theorem topologies and the principal
Mucha/Kolmogorov collisions had been identified. This is a bounded
non-collision audit, never an exhaustive novelty or priority search.

## 2. Direct global-orbit stability literature

### 2.1 Pizzocchero 2021: the closest direct periodic collision

Pizzocchero works on the mean-zero torus \(\mathbb T^d\), \(d\ge2\), with no
force. Proposition 4.2 identifies eventual Sobolev smallness, decay, time
integrability, and exponential decay for a global smooth solution. Theorem 5.1
then proves that if \(n>d/2+1\) and a smooth global decaying solution \(v\) is
perturbed by smooth data satisfying

\[
 \|u_0-v_0\|_{H^n}<\rho_n(v),
\]

the perturbed solution is global and decays, with an explicit
\(H^n\)-exponential difference estimate. In dimension three one may take
\(n=3\).

The printed theorem is formulated for \(H^\infty\) data, and Remark 5.2 states
openness in the \(H^\infty\) Frechet topology; it does not literally state
openness of the entire \(H^3\) global-data set. Nevertheless, it is a direct
collision with the conceptual content of R0.73O. Extending the result to the
standard \(H^3\) local theory by positive-time smoothing and continuation is a
narrow technical corollary, not a plausible headline novelty.

Primary source: L. Pizzocchero,
[*On the global stability of smooth solutions of the Navier--Stokes
equations*](https://doi.org/10.1016/j.aml.2020.106970), Applied Mathematics
Letters 115 (2021), 106970, Proposition 4.2, Theorem 5.1, Remark 5.2;
[author post-print](https://air.unimi.it/bitstream/2434/808431/3/global_definitivo.pdf).

### 2.2 Automatic periodic smoothing and decay

Hoang--Martinez prove that every Leray--Hopf solution of the mean-zero
three-dimensional periodic equation with potential body force (removed by the
Leray projection) is eventually Gevrey regular and exponentially decaying in
all Sobolev orders. Thus the late smooth exponential regime used by R0.73O is
itself classical and is not a new consequence of the explicit ladder.

Primary source: L. T. Hoang, V. R. Martinez,
[*Asymptotic expansion in Gevrey spaces for solutions of Navier--Stokes
equations*](https://arxiv.org/abs/1511.03523), Asymptotic Analysis 104 (2017),
167--190, DOI
[10.3233/ASY-171429](https://doi.org/10.3233/ASY-171429), Theorem 2.4.

### 2.3 Enciso--Lucà--Peralta-Salas 2017

Their periodic robustness theorem gives global exponential \(H^m\) control of
perturbations around a global base solution satisfying
\(L^2_tW^{r,\infty}_x\), for \(0\le m\le r\). Taking \(r=3\) directly supplies
an \(H^3\)-input/\(H^3\)-output theorem under a stronger base-orbit
integrability hypothesis.

Primary source: A. Enciso, R. Lucà, D. Peralta-Salas,
[*Vortex reconnection in the three dimensional Navier--Stokes
equations*](https://arxiv.org/abs/1606.06176), Advances in Mathematics 309
(2017), 452--486, DOI
[10.1016/j.aim.2017.01.025](https://doi.org/10.1016/j.aim.2017.01.025),
Theorem 3.1.

### 2.4 Ponce--Racke--Sideris--Titi 1994

Theorem 1 treats a global strong reference solution on a \(C^3\) domain and
assumes

\[
 \int_0^\infty\|\nabla v(t)\|_2^4\,dt<\infty.
\]

For Poincare domains, sufficiently small \(H^1\)-type initial perturbations
and \(L^2_tL^2_x\) force perturbations yield a global strong solution uniformly
close in \(H^1\). The paper includes stability applications to large symmetric
solutions and unforced two-dimensional flows under three-dimensional
perturbations. Its printed domain formulation is not the standard cubic torus,
although the energy mechanism is directly neighboring.

**Collision decision:** strong stability of large global solutions is
classical. R0.73O cannot claim novelty for openness or for the generic idea
that a sufficiently integrable global orbit has a stability neighborhood.

Primary source: G. Ponce, R. Racke, T. C. Sideris, E. S. Titi,
[*Global Stability of Large Solutions to the 3D Navier Stokes
Equations*](https://web.math.ucsb.edu/~sideris/pdffiles/CMP-1994.pdf),
Comm. Math. Phys. 159 (1994), 329--341, DOI
[10.1007/BF02102642](https://doi.org/10.1007/BF02102642), Theorems 1--4.

### 2.5 Gallagher--Iftimie--Planchon 2003

For the whole-space equation, an a priori global solution in the critical
\(L^3\)/Besov framework tends to zero at large time. The set of global data is
open in the corresponding critical topology, and nearby data give global
solutions. The domain and topology differ from R0.73O, but the openness and
late-smallness architecture is unmistakably prior art.

Primary source: I. Gallagher, D. Iftimie, F. Planchon,
[*Asymptotics and stability for global solutions to the Navier--Stokes
equations*](https://www.numdam.org/item/AIF_2003__53_5_1387_0/), Ann. Inst.
Fourier 53 (2003), 1387--1424, DOI
[10.5802/aif.1983](https://doi.org/10.5802/aif.1983).

### 2.6 Critical-space strong and weak stability

Bahouri--Chemin--Gallagher distinguish ordinary strong openness of the
global-data set in critical spaces from their stronger weak-convergence
stability theorem. Their result is on \(\mathbb R^3\), not the periodic \(H^3\)
phase space.

Primary source: H. Bahouri, J.-Y. Chemin, I. Gallagher,
[*On the stability of global solutions to the three-dimensional Navier--Stokes
equations*](https://jep.centre-mersenne.org/item/10.5802/jep.84.pdf),
Journal de l'Ecole polytechnique 5 (2018), 843--911, DOI
[10.5802/jep.84](https://doi.org/10.5802/jep.84).

Chemin--Gallagher construct large periodic global solutions under a nonlinear
smallness condition and explicitly place their construction inside the known
open global-data set. This is periodic prior art, but not an all-global-orbit
\(H^3\) finite-action theorem.

Primary source: J.-Y. Chemin, I. Gallagher,
[*Large, global solutions to the Navier--Stokes equations, slowly varying in
one direction*](https://arxiv.org/abs/math/0508374). The title/version and
domain metadata must be checked in the final bibliography before release; the
theorem content, rather than a title paraphrase, is the evidence.

## 3. The Mucha collision

### 3.1 Mucha 2001 torus paper

The publisher abstract says that on the three-dimensional torus the
\(W^{2,1}_r\) norm of a perturbation is controlled when its initial datum is
small enough in \(L^2\), and gives stability of unforced two-dimensional
flows. That wording is close to the R0.73N open cell called full FPS
\((H^3,L^2)\).

Primary metadata and abstract: P. B. Mucha,
[*Stability of Nontrivial Solutions of the Navier--Stokes System on the Three
Dimensional Torus*](https://doi.org/10.1006/jdeq.2000.3863), J. Differential
Equations 172 (2001), 359--375.

The accessible publisher page was protected by an interactive challenge, and
the retrieved object labeled as a PDF was HTML rather than the paper. The
audit therefore does **not** assert the exact theorem quantifiers from the
abstract alone. In particular, “small enough in \(L^2\)” does not tell us
whether the threshold is uniform over arbitrarily large regular norms.

### 3.2 Mucha 2008 resolves the relevant dependence pattern

Mucha's accessible later paper gives the dependence explicitly. Theorem 1.2
assumes regular data in a Besov trace space and says

\[
 \|v_0\|_{L^2}
 \quad\hbox{is sufficiently small compared with}\quad
 \|v_0\|_{B^{2-2/q}_{p,q}}.
\]

The paper states that analogous earlier work covered the torus and
\(\mathbb R^3\) in \(W^{2,1}_{p,p}\) spaces. This is direct evidence that the
small-\(L^2\) condition in this method is high-norm dependent, not a uniform
threshold over arbitrary regular data.

Primary source: P. B. Mucha,
[*Global solutions, structure of initial data and the Navier--Stokes
equations*](https://doi.org/10.4064/bc81-0-18), Banach Center Publ. 81 (2008),
277--286, Theorem 1.2 and the discussion following it.

**Collision decision:** R0.73O must cite Mucha 2001 as the closest torus
collision and must not advertise its \(H^3\)-small stability tube as a new
phenomenon. The checked evidence does not close a radius uniform over data
small only in \(L^2\) and arbitrarily large in \(H^3\). Because the exact 2001
theorem text was not directly inspected, the final wording is “not established
by the checked exact theorem statements,” not an absolute absence claim.

## 4. Forced autonomous instability

### 4.1 Kolmogorov spectral problem

Meshalkin--Sinai reduce the linear stability of the two-dimensional
Kolmogorov flow to a continued-fraction eigenvalue equation and prove the
exchange-of-stability property: an eigenvalue with nonnegative real part is
real. Nagatou formulates the eigenproblem

\[
 \sigma\Delta\phi-{1\over R}\Delta^2\phi
 +\sin y(\Delta+I)\partial_x\phi=0
\]

on a rectangular two-torus and gives a computer-assisted critical enclosure.
For \(\alpha=0.7\), the critical value is enclosed by

\[
R_c\in[3.011528364444,3.011528364446].
\]

The enclosure and exchange proposition alone do not select the supercritical
side.  R0.73O closes that edge by a composite primary-source certificate.
Matsuda--Miyatake Proposition 1 proves that the zero-eigenvalue recurrence has
a nonzero \(\ell^2\) solution only at the unique neutral parameter
\(\lambda(\beta)\) for \(0<\beta<1\), and none for \(\beta\ge1\).  Ilyin
Theorem 5.1 supplies positive real spectrum at a finite sufficiently large
Reynolds parameter.  Continuous spectral dependence plus Nagatou's exclusion
of nonzero imaginary crossings, the full-Fourier zero-mode exclusion, a
uniform compact-interval spectral rectangle, and Riesz-projection rank
continuation then propagate that positive spectrum down the entire interval
\((R_c,\infty)\).  Watanabe's primary-source account identifies
Nagatou's enclosed \(\alpha=0.7\) value as the point where the basic flow loses
stability.  This is an explicit theorem chain, not a claim that Nagatou alone
proves the one-sided direction.

Primary sources:

- L. D. Meshalkin, Ya. G. Sinai, official
  [1961 journal scan](https://pmm.ipmnet.ru/ru/Issues/1961/25-6/1140), English
  DOI [10.1016/0021-8928(62)90149-1](https://doi.org/10.1016/0021-8928(62)90149-1).
- K. Nagatou,
  [*A computer-assisted proof on the stability of the Kolmogorov
  flows*](https://doi.org/10.1016/j.cam.2003.10.016), J. Comput. Appl. Math.
  169 (2004), 33--44, especially the eigenproblem and verified examples.
- Y. Watanabe et al.,
  [*An efficient numerical verification method for the Kolmogorov
  problem*](https://doi.org/10.1016/j.cam.2016.01.055), J. Comput. Appl. Math.
  (2016), Section 6.1, used as a later exact restatement of the critical
  enclosure and loss-of-stability interpretation.
- M. Matsuda and S. Miyatake,
  [*Bifurcation analysis of Kolmogorov flows*](https://doi.org/10.2748/tmj/1113247600),
  Tohoku Math. J. 54 (2002), 329--365, Proposition 1.
- A. A. Ilyin,
  [*Lieb--Thirring integral inequalities and their applications to attractors
  of the Navier--Stokes equations*](https://doi.org/10.1070/SM2005v196n01ABEH000871),
  Sbornik Math. 196 (2005), 29--61, Theorem 5.1.
- T. Kato,
  [*Perturbation Theory for Linear Operators*](https://link.springer.com/book/10.1007/978-3-642-66282-9),
  Chapters III.6 and VII.1--2, used only for the standard compact-resolvent,
  type-(A), and Riesz-projection framework; the explicit uniform spectral
  rectangle is derived in the R0.73O proof.
- Y. Watanabe,
  [*A computer assisted proof of the Kolmogorov problem of incompressible
  viscous fluid*](https://www.kurims.kyoto-u.ac.jp/~kyodo/kokyuroku/contents/pdf/1905-11.pdf),
  RIMS Kôkyûroku 1905 (2014), Section 7.

The fixed-cube embedding is not copied from those papers. R0.73O derives it
directly with forcing wave number \(N=10\), physical \(x\)-wave number \(m=7\),
\(\alpha=m/N=0.7\), and \(R=A/(\nu N)=3.012\).

### 4.2 Linear spectrum to nonlinear escape

Friedlander--Pavlović--Shvydkoy Definition 2.1 uses \(X\) for the solution
space and \(Z\) for both the small initial metric and the observed metric.
Theorem 2.2 says that right-half-plane \(L^p\) spectrum implies nonlinear
\((L^q,L^p)\) instability for \(q>\max\{p,n\}\). On a finite domain the
unstable eigenfunction is smooth, and the proof remarks that the initial size
can be measured in a \(C^\infty\) metric while escape remains in \(L^p\).

Primary source: S. Friedlander, N. Pavlović, R. Shvydkoy,
[*Nonlinear instability for the Navier--Stokes
equations*](https://arxiv.org/abs/math/0508173), Comm. Math. Phys. 264 (2006),
335--347, Definition 2.1, Theorem 2.2, and the finite-domain remark after its
proof; DOI
[10.1007/s00220-006-1526-7](https://doi.org/10.1007/s00220-006-1526-7).

For R0.73O, the unstable eigenfunction and initial perturbations are planar.
Planar invariance and two-dimensional global regularity remove the
“nonexistence of a global solution” branch from the instability definition.
The output is an actual fixed \(L^2\) escape by globally smooth solutions.

## 5. Audit decisions

| Question | Decision | Evidence boundary |
|---|---|---|
| Is strong stability/openness around large global solutions new? | **No. Classical.** | Pizzocchero, PRST, GIP, BCG, Mucha |
| Is the direct periodic \(H^3\) finite-\(H^4\)-action derivation still useful? | **Yes, only as a self-contained scoped corollary and route closure.** | Pizzocchero is a direct smooth periodic collision; no priority language |
| Does Mucha 2001's abstract by itself close uniform FPS \((H^3,L^2)\)? | **No conclusion from abstract alone.** | exact threshold dependence unavailable there |
| Does the accessible Mucha method show high-norm dependence? | **Yes.** | Mucha 2008 Theorem 1.2 |
| Is the standard \(N=1\) cubic Kolmogorov flow covered by the \(\alpha<1\) instability? | **No.** | the cube has no longer integer \(x\)-mode; use \(N=10,m=7\) |
| Can a forced standard-cube equilibrium have smooth \(H^3\)-small/\(L^2\)-escaping data? | **Closed by a composite checked theorem chain and final independent audit.** | Nagatou + Matsuda--Miyatake + Ilyin + Kato framework + exact scaling + 2D FPS + planar globality |
| Does the forced example advance the Clay conclusion directly? | **No.** | different equation; all witness solutions are smooth |

## 6. Publication language

Safe wording:

> R0.73O gives a self-contained \(H^3\) derivation of a classical periodic
> stability phenomenon: every a priori global unforced orbit enters a smooth,
> exponentially decaying regime and has a positive synchronized stability
> tube. The finite accumulated \(H^4\) action is the route-specific bridge used
> here. A separate forced Kolmogorov equilibrium supplies a topology-matched
> instability contrast while all witnessing solutions remain globally smooth.

Forbidden wording includes “first,” “new global stability theorem,” “closes
the \(L^2\) threshold,” “turbulence proved,” “singularity mechanism,” or any
claim that the forced example is evidence of finite-time blow-up.
