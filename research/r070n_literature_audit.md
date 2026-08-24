# R0.70N bounded primary-literature audit

**Audit date:** 2026-08-25

## 1. Question, corpus, and stopping rule

The proposed statement under audit is

\[
 \mathcal Q_k
 =\sum_{j=k-m}^{k+m}w_{k,j}Q_j,
 \qquad
 Q_j=\int\chi_j\Omega_j\otimes\Omega_j\,dx,
 \tag{1.1}
\]

followed by a solution-independent lower-frame estimate

\[
 \mathcal Q_k
 \succeq c\,\operatorname{tr}(\mathcal Q_k)I,
 \qquad c>0.
 \tag{1.2}
\]

The audit used arXiv, journal or publisher pages, DOI-resolved records, and
author-hosted manuscripts.  Technical conclusions were taken only from
primary papers or their official abstracts.  Search families covered:

- filtered vorticity, subgrid defects, and multi-scale stress identities;
- vorticity covariance, realizability, and structure tensors;
- Littlewood--Paley and wavelet multi-resolution decompositions;
- finite frames, lower-frame bounds, persistent excitation, and
  observability Gramians;
- affine-invariant SPD and fixed-rank PSD geometry;
- shear, Beltrami, and helical Fourier structures;
- vorticity-direction and component-reduction regularity criteria;
- 2025--2026 uses of “filtered vortex stretching” and “coercivity” in
  Navier--Stokes research.

The search stopped after every theme had at least one canonical primary
source, the two newest close lexical matches had been checked, and two
targeted passes over covariance/frame/Gramian synonyms returned no exact
match to (1.2).  The exact shear counterexample had also made further
bibliographic expansion irrelevant to the truth value of the universal
claim.

This was not an exhaustive MathSciNet, zbMATH, or all-language systematic
review.  “No exact match was found” is therefore a bounded-search statement,
not proof of absence from all literature.

## 2. Direct collision decision

No audited source proves that scalar/componentwise filtering plus
nonnegative summation automatically gives (1.2) for every smooth
Navier--Stokes solution.

More decisively, the proposed universal statement is false.  The exact
periodic shear

\[
 u=Ae^{-\nu N^2t}\sin(Ny)e_1
 \tag{2.1}
\]

has filtered vorticity parallel to \(e_3\) at every scalar filter scale.
Every \(Q_j\) and every nonnegative scale, center, or time sum therefore has
rank at most one.  A single real helical wave similarly leaves one common
null direction and gives rank at most two.

The literature is still essential for the claim boundary:

- covariance and multi-scale filtering are prior objects;
- a lower-frame or persistent-excitation bound is normally an extra
  directional-richness property;
- low-rank covariance is not automatically a regularity criterion;
- affine SPD geometry cannot cross rank loss without changing geometry;
- a single helical mode is rank deficient, but a multi-axis Beltrami field
  need not be.

## 3. Filtered and multi-scale fluid identities

### 3.1 Yu (2026)

- Source: Runlong Yu, “Filtered Vortex Stretching and Subgrid Defects for the
  Three-Dimensional Navier--Stokes Equations,”
  [arXiv:2606.27560](https://arxiv.org/abs/2606.27560), submitted
  25 June 2026.
- Exact support: a finite-scale filtered-vorticity stretching estimate,
  angular defects, diffusion absorption, differentiated commutator stress,
  and explicit far-field/localization residuals.
- It cannot support: a covariance Gramian, strict positive definiteness, or
  a lower bound for \(\lambda_{\min}(\mathcal Q_k)\).
- Collision/gap: this is the closest 2026 filtered-vorticity paper found.
  Its direction defect and residual structure reinforce the need to keep
  commutator and localization terms, but it does not supply (1.2).
- Confidence: high; arXiv title, date, author, and abstract verified.

### 3.2 Germano (1992)

- Source: Massimo Germano, “Turbulence: the filtering approach,”
  *Journal of Fluid Mechanics* 238 (1992), 325--336,
  [DOI 10.1017/S0022112092001733](https://doi.org/10.1017/S0022112092001733).
- Exact support: exact algebraic relations among generalized central moments
  and stresses at different filtering levels.
- It cannot support: angular spanning of filtered vorticity or strict
  covariance positivity.
- Collision/gap: scale ledgers are classical; the R0.70N issue is a target
  space lower-frame bound, not the existence of a scale identity.
- Confidence: high.

### 3.3 Eyink (2006)

- Source: Gregory L. Eyink, “Multi-scale gradient expansion of the turbulent
  stress tensor,” *Journal of Fluid Mechanics* 549 (2006), 159--190,
  [arXiv:nlin/0512022](https://arxiv.org/abs/nlin/0512022),
  [DOI 10.1017/S0022112005007895](https://doi.org/10.1017/S0022112005007895).
- Exact support: a convergent multi-scale expansion of turbulent stress and
  precise scale/space locality statements under the paper's hypotheses.
- It cannot support: scalar energy locality implying a three-dimensional
  angular lower frame.
- Collision/gap: multi-scale completeness in function space does not mix a
  fixed vector direction across components.
- Confidence: high.

### 3.4 Johnson (2020)

- Source: Perry L. Johnson, “Energy Transfer from Large to Small Scales in
  Turbulence by Multiscale Nonlinear Strain and Vorticity Interactions,”
  *Physical Review Letters* 124 (2020), 104501,
  [DOI 10.1103/PhysRevLett.124.104501](https://doi.org/10.1103/PhysRevLett.124.104501);
  erratum 126 (2021), 029901,
  [DOI 10.1103/PhysRevLett.126.029901](https://doi.org/10.1103/PhysRevLett.126.029901).
- Exact support: multi-scale decomposition of energy transfer into strain
  self-amplification and vorticity-stretching contributions.
- It cannot support: a smallest-eigenvalue estimate for the directional
  covariance in (1.1).
- Collision/gap: scalar transfer identities and matrix frame coercivity are
  distinct assertions.
- Confidence: high.

## 4. Covariance realizability and multi-resolution structure

### 4.1 Schumann (1977) and Vreman--Geurts--Kuerten (1994)

- Sources:
  [Schumann, DOI 10.1063/1.861942](https://doi.org/10.1063/1.861942);
  [Vreman--Geurts--Kuerten, DOI 10.1017/S0022112094003745](https://doi.org/10.1017/S0022112094003745).
- Exact support: realizability constraints for Reynolds or LES stress
  tensors, including the natural role of positive semidefiniteness.
- They cannot support: replacing semidefinite realizability by uniform
  positive definiteness.
- Collision/gap: one- and two-component boundary states are allowed by PSD
  realizability.  Moreover, those stress tensors are not identical to the
  localized vorticity second moment in (1.1).
- Confidence: high.

### 4.2 Daubechies (1988) and Mallat (1989)

- Sources:
  [Daubechies, DOI 10.1002/cpa.3160410705](https://doi.org/10.1002/cpa.3160410705);
  [Mallat, DOI 10.1109/34.192463](https://doi.org/10.1109/34.192463).
- Exact support: orthonormal wavelets and multi-resolution decompositions
  with scalar \(L^2\) energy identities.
- They cannot support: directional mixing.  If
  \(\omega(x)=a f(x)\), then every componentwise scalar wavelet piece is
  \(a\,T_jf\), and the sum of outer products remains rank one.
- Collision/gap: Parseval completeness controls total energy, not the lower
  eigenvalue of a three-dimensional target-space Gramian.
- Confidence: high.

### 4.3 Structure-tensor literature

- Sources:
  Josef Bigün and Gösta H. Granlund, “Optimal Orientation Detection of Linear
  Symmetry,” ICCV 1987, pp. 433--438,
  [author bibliography](https://www2.hh.se/staff/josef/public/publications/node2.html);
  Joachim Weickert, “Coherence-Enhancing Diffusion Filtering,”
  *International Journal of Computer Vision* 31 (1999), 111--127,
  [DOI 10.1023/A:1008009714131](https://doi.org/10.1023/A:1008009714131).
- Exact support: local averages of gradient outer products form structure
  tensors whose eigenvalues diagnose direction and coherence.
- They cannot support: automatic isotropy of an outer-product average.
- Collision/gap: small eigenvalues and rank deficiency are meaningful
  structures in this literature, not states ruled out by averaging.
- Confidence: medium-high; the analogy is exact at the matrix level but the
  observables differ.

## 5. Frames, observability, and persistent excitation

### 5.1 Duffin--Schaeffer and finite-frame theory

- Sources:
  [Duffin--Schaeffer, DOI 10.1090/S0002-9947-1952-0047179-6](https://doi.org/10.1090/S0002-9947-1952-0047179-6);
  [Benedetto--Fickus, DOI 10.1023/A:1021323312367](https://doi.org/10.1023/A:1021323312367);
  [Cahill et al., arXiv:1106.0921](https://arxiv.org/abs/1106.0921).
- Exact support: the minimum and maximum eigenvalues of a finite frame
  operator are its optimal frame bounds; tightness and prescribed spectra
  are properties of the vector family.
- It cannot support: deriving spanning or a positive lower-frame bound from
  the total squared length alone.
- Collision/gap: with
  \(g_{j,x}=\sqrt{w_j\chi_j(x)}\,\Omega_j(x)\), the matrix
  \(\mathcal Q_k\) is precisely the continuous finite-dimensional frame
  operator.  Formula (1.2) is an extra uniform frame condition.
- Confidence: high.

### 5.2 Boyd--Sastry and Narendra--Annaswamy

- Sources:
  [Boyd--Sastry, DOI 10.1016/0005-1098(86)90002-6](https://doi.org/10.1016/0005-1098(86)90002-6);
  [Narendra--Annaswamy, DOI 10.1080/00207178708933715](https://doi.org/10.1080/00207178708933715).
- Exact support: parameter convergence and persistent excitation are tied to
  positive lower bounds on time-window Gramians of regressor signals.
- They cannot support: deriving persistent excitation from signal energy.
- Collision/gap: R0.70N replaces a time signal by a scale/space observation
  family, but the same algebra remains.  Missing directions yield only
  subspace observability.
- Confidence: high.

## 6. SPD and fixed-rank PSD geometry

### 6.1 Pennec--Fillard--Ayache (2006)

- Source: “A Riemannian Framework for Tensor Computing,”
  *International Journal of Computer Vision* 66 (2006), 41--66,
  [DOI 10.1007/s11263-005-3222-z](https://doi.org/10.1007/s11263-005-3222-z).
- Exact support: affine-invariant geometry on the SPD cone, congruence
  invariance, and the metric's rank boundary.
- It cannot support: turning a PSD covariance into an SPD covariance or
  controlling an inverse at rank loss.
- Collision/gap: the R0.70M affine metric remains conditional on
  \(\mathcal Q_k\succ0\).
- Confidence: high.

### 6.2 Bonnabel--Sepulchre (2009)

- Source: “Riemannian Metric and Geometric Mean for Positive Semidefinite
  Matrices of Fixed Rank,” *SIAM Journal on Matrix Analysis and Applications*
  31 (2009), 1055--1070,
  [arXiv:0807.4462](https://arxiv.org/abs/0807.4462),
  [DOI 10.1137/080731347](https://doi.org/10.1137/080731347).
- Exact support: a quotient geometry for fixed-rank PSD matrices compatible
  with rank-preserving transformations and pseudoinverses.
- It cannot support: creation of missing directions, a full-space inverse, or
  a rank-uniform coercivity constant.
- Collision/gap: fixed-rank geometry is a legitimate language for a
  degenerate branch, but the evolving range projector and its NSE source must
  still be controlled.
- Confidence: high.

## 7. Beltrami and helical boundaries

### 7.1 Constantin--Majda (1988) and Waleffe (1992)

- Sources:
  [Constantin--Majda, DOI 10.1007/BF01218019](https://doi.org/10.1007/BF01218019);
  [Waleffe, DOI 10.1063/1.858309](https://doi.org/10.1063/1.858309).
- Exact support: Beltrami spectral structure, helical Fourier modes, and
  helical triad interactions are classical.
- They cannot support: the assertion that every Beltrami covariance is
  singular.
- Collision/gap: R0.70N uses one real helical axis as a rank-two witness and
  separately records a two-axis positive control.  The no-go is not a claim
  about all Beltrami fields.
- Confidence: high.

### 7.2 Inage (2026): lexical, not mathematical, collision

- Source: Shin-ichi Inage, “Structural Reduction Framework and Residence-Time
  Compression of Coherent Same-Scale Triadic Interactions in the 3D
  Navier--Stokes Equations,” *Mathematics* 14 (2026), 1410,
  [DOI 10.3390/math14091410](https://doi.org/10.3390/math14091410).
- Exact support: within the paper's dyadic--triadic structural framework,
  “curvature coercivity” concerns amplitude-active, geometrically
  nondegenerate, low-phase-drift coherent interactions and residence-time
  compression.
- It cannot support: a covariance matrix lower bound or inclusion of
  degenerate shear/one-axis states in its coercive set.
- Collision/gap: the word “coercivity” refers to a different object.  The
  article's own scope statement does not claim a general solution of global
  regularity.
- Confidence: high; publisher page, abstract, theorem framing, and scope
  statement checked on 2026-08-25.

## 8. Geometric and anisotropic regularity criteria

### 8.1 Constantin--Fefferman (1993)

- Source: “Direction of Vorticity and the Problem of Global Regularity for
  the Navier--Stokes Equations,” *Indiana University Mathematics Journal* 42
  (1993), 775--789,
  [journal page](https://iumj.org/article/3627/),
  [DOI 10.1512/iumj.1993.42.42034](https://doi.org/10.1512/iumj.1993.42.42034).
- Exact support: sufficient coherence of vorticity direction in high-vorticity
  regions depletes stretching and yields regularity under the paper's
  quantitative hypotheses.
- It cannot support: covariance rank deficiency alone as a regularity
  condition.
- Collision/gap: directional alignment may be benign, but a spatially
  averaged spectral ratio does not supply the pointwise direction regularity
  used in the theorem.
- Confidence: high.

### 8.2 Beirão da Veiga--Berselli (2002)

- Source: “On the regularizing effect of the vorticity direction in
  incompressible viscous flows,” *Differential and Integral Equations* 15
  (2002), 345--356,
  [DOI 10.57262/die/1356060864](https://doi.org/10.57262/die/1356060864),
  [author PDF](https://people.dm.unipi.it/beiraodaveiga/pdf/hbv-79.pdf).
- Exact support: a regularizing criterion formulated through quantitative
  control of the vorticity direction.
- It cannot support: a lower covariance eigenvalue or a bridge from
  scale-averaged \(L^2\) planarity to its direction hypothesis.
- Confidence: high.

### 8.3 Chae--Choe (1999)

- Source: “Regularity of solutions to the Navier--Stokes equation,”
  *Electronic Journal of Differential Equations* 1999(05), 1--7,
  [journal page](https://ejde.math.txstate.edu/Volumes/1999/05/abstr.html),
  [primary PDF](https://www.kurims.kyoto-u.ac.jp/EMIS/journals/EJDE/Volumes/1999/05/chae.pdf).
- Exact support: regularity criteria involving only two fixed components of
  the vorticity.
- It cannot support: smallness of only one covariance eigenvalue.  Small
  \(\lambda_3\) says the vorticity is near a plane; controlling two vorticity
  components is geometrically closer to concentration near a line.
- Collision/gap: a usable degenerate branch must distinguish rank two from
  rank one and must reach the paper's scale-critical mixed norms.
- Confidence: high; official abstract explicitly states “only two
  components.”

### 8.4 Miller (2021)

- Source: Evan Miller, “A locally anisotropic regularity criterion for the
  Navier--Stokes equation in terms of vorticity,” *Proceedings of the
  American Mathematical Society, Series B* 8 (2021), 60--74,
  [arXiv:2002.02152](https://arxiv.org/abs/2002.02152),
  [DOI 10.1090/bproc/74](https://doi.org/10.1090/bproc/74).
- Exact support: smoothness persists when vorticity projected onto a plane is
  controlled in the scale-critical \(L_t^4L_x^2\) space, with a variable
  plane permitted under a bound on the gradient of its unit normal.
- It cannot support: replacing that critical norm and normal-field
  regularity by the relative, localized, filtered \(L^2\) eigenvalue ratio
  \(c_*\).
- Collision/gap: the theorem motivates a rank-stratified branch, but no
  audited source supplies the required filtered-to-unfiltered critical
  bridge.
- Confidence: high; arXiv abstract and journal DOI verified.

### 8.5 Serrin (1962) and Escauriaza--Seregin--Šverák (2003)

- Sources:
  [Serrin, DOI 10.1007/BF00253344](https://doi.org/10.1007/BF00253344);
  [Escauriaza--Seregin--Šverák, DOI 10.1070/RM2003v058n02ABEH000609](https://doi.org/10.1070/RM2003v058n02ABEH000609).
- Exact support: critical or endpoint velocity control yields regularity or
  continuation in the stated settings.
- They cannot support: deriving those spaces from a finite-scale covariance
  spectrum.
- Collision/gap: any successful covariance route still needs a theorem
  connecting its spectral diagnostic to a recognized critical quantity.
- Confidence: high.

## 9. Novelty boundary

The following claims are not defensible:

- first use of a vorticity covariance or outer-product tensor;
- first summation across filter scales;
- first structure tensor, frame operator, persistent-excitation Gramian, or
  observability lower bound;
- first affine-invariant SPD or fixed-rank PSD geometry;
- first rank deficiency of shear or one helical mode;
- wavelet/LP energy completeness implies directional frame coercivity;
- small \(\lambda_{\min}\) itself implies a known regularity criterion.

After the exact derivation and certificate, the defensible bounded statement
is:

> Within the primary sources audited through 2026-08-25, no exact theorem was
> found that gives a universal positive lower frame for a finite adjacent-scale
> scalar-filtered vorticity covariance.  R0.70N gives an exact no-go for that
> statement on smooth periodic NSE solutions, retains the complete aggregate
> source ledger, and shows that merely excluding exactly two-dimensional data
> still gives no solution-independent constant.

The shear observation alone is a decisive route-closing lemma, not by itself
a complete high-level paper.  A substantial next contribution would require
one of:

\[
 \text{a critical residual theorem on a quantitatively coercive branch},
 \tag{9.1}
\]

or

\[
 \text{a rigorous rank-stratified bridge from near-one-dimensional
 vorticity to a known anisotropic continuation criterion}.
 \tag{9.2}
\]

Neither bridge is supplied by the audited literature.
