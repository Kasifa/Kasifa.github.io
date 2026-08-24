# R0.70J bounded primary-literature audit

**Release:** R0.70J
**Date:** 2026-08-24
**Question:** Does incompressibility, a trace-free exterior harmonic strain,
angular averaging, or helical polarization force the deviatoric diagonal
pairing to vanish?

## 1. Search protocol and stopping rule

The audit was deliberately bounded. A first wave covered four mechanisms:

1. symmetric trace-free tensors and spherical harmonics;
2. helical Fourier representations and helical triads;
3. vorticity-direction depletion and strain eigenvalue criteria;
4. nonlocal strain and the pressure-Hessian boundary.

A second wave searched only for a theorem annihilating an arbitrary external
harmonic STF tensor against a pure-helicity or angularly averaged vorticity
square. The search stopped after ten high-signal primary sources. Repeated
reviews, derivative expositions, and unverified new preprints were excluded.
The resulting statement is a bounded search finding, not a theorem that no
matching result exists anywhere in the literature.

## 2. Primary-source evidence matrix

| Source | Exact object relevant here | What it supports | What it does not supply |
|---|---|---|---|
| [Applequist, *Traceless Cartesian tensor forms for spherical harmonic functions* (1989)](https://doi.org/10.1088/0305-4470/22/20/011) | Cartesian STF representation of spherical harmonics | A rank-two STF tensor is the coefficient of a harmonic quadratic; the R0.70J source sector is the five-dimensional \(\ell=2\) representation | No time, frequency, or NSE cancellation |
| [Ledesma--Mewes, *Spherical-harmonic tensors* (2020)](https://journals.aps.org/prresearch/pdf/10.1103/PhysRevResearch.2.043061) | Orthonormal STF tensor basis equivalent to scalar spherical harmonics | Makes the source-response contraction an ordinary pairing in the \(\ell=2\) sector | Orthogonality of different irreducible sectors does not annihilate two nonzero vectors in the same \(\ell=2\) sector |
| [Waleffe, *The nature of triad interactions in homogeneous turbulence* (1992)](https://doi.org/10.1063/1.858309) | Helical eigenvectors and eight helicity combinations for a Fourier triad | Supplies the correct helical basis and shows that helicity labels reorganize nonlinear interactions | Triad energy/helicity conservation is not a null identity for one arbitrary external STF contraction; phase and amplitude data remain essential |
| [Biferale--Musacchio--Toschi, *Inverse energy cascade in three-dimensional isotropic turbulence* (2012)](https://arxiv.org/abs/1111.1412) | NSE dynamics projected to one helicity sign | A homochiral sector still has nontrivial nonlinear dynamics | The decimated periodic system is neither the full NSE nor a regularity theorem and gives no arbitrary-STF cancellation |
| [Constantin--Fefferman, *Direction of Vorticity and the Problem of Global Regularity for the Navier--Stokes Equations* (1993)](https://iumj.org/article/3627/) | Conditional regularity from coherence of vorticity direction in high-vorticity regions | Their conditional depletion/regularity mechanism assumes quantitative spatial coherence of the vorticity direction | Finite energy and a helicity label do not automatically provide that coherence; the theorem is not about an independent external STF source |
| [Beirão da Veiga--Berselli, *On the regularizing effect of the vorticity direction in incompressible viscous flows* (2002)](https://projecteuclid.org/journals/differential-and-integral-equations/volume-15/issue-3/On-the-regularizing-effect-of-the-vorticity-direction-in-incompressible/10.57262/die/1356060864.full) | Exact Biot--Savart stretching-rate kernel with an angular determinant and conditional direction-coherence criteria | Exhibits a real angular null factor when the strain and the vorticity come from the same Biot--Savart field | The paper supplies no transfer of that determinant cancellation to an independent arbitrary harmonic STF tensor |
| [Galanti--Gibbon--Heritage, *Vorticity alignment results for the three-dimensional Euler and Navier--Stokes equations* (1997)](https://arxiv.org/abs/chao-dyn/9709003) | Local evolution of stretching and rotation variables, including pressure-Hessian projections | Pressure-Hessian projections enter as additional, unclosed geometric quantities in the local alignment equations | Model fixed points and special flows do not prove universal alignment for NSE solutions |
| [Hamlington--Schumacher--Dahm, *Direct assessment of vorticity alignment with local and nonlocal strain rates in turbulent flows* (2008)](https://arxiv.org/pdf/0810.3439) | Direct Biot--Savart split of local and nonlocal strain in DNS | Empirical evidence that nonlocal/background strain can align with an extensional direction | DNS alignment statistics are not an a priori theorem and do not establish a sign at every scale or time |
| [Neustupa--Penel, *The role of eigenvalues and eigenvectors of the symmetrized gradient of velocity in the theory of the Navier--Stokes equations* (2003)](https://comptes-rendus.academie-sciences.fr/mathematique/item/10.1016/S1631-073X%2803%2900174-2.pdf) | Conditional regularity criteria involving strain eigenvalues, including the positive middle eigenvalue | Confirms that extensional strain geometry is regularity-relevant rather than algebraically absent | Requires additional spacetime integrability; it does not close the R0.70I high--high norm from Leray control |
| [Miller, *A regularity criterion involving only the middle eigenvalue of the strain tensor* (2020)](https://arxiv.org/abs/1710.05569) | Exact strain evolution and a middle-eigenvalue conditional criterion | Displays the trace-free projection of the vorticity-square forcing and the role of the pressure Hessian | Global pressure orthogonality does not survive arbitrary localization without cutoff and harmonic terms; the criterion is conditional |

The priority boundary on the middle-eigenvalue criterion is explicit: the
earlier Neustupa--Penel theorem must be cited, and no novelty attribution is
made to the later rediscovery.

## 3. Evidence synthesis

The sources separate three distinct cancellations that are easy to conflate.

### 3.1 Irreducible-tensor cancellation

The trace-free source is orthogonal to the scalar \(\ell=0\) component of
\(\omega\otimes\omega\). The deviatoric response belongs to the same
\(\ell=2\) representation as the source. STF harmonic theory therefore
predicts an allowed five-dimensional pairing, not an automatic zero.

### 3.2 Helical-triad cancellation

Waleffe's helical basis diagonalizes curl and exposes antisymmetric
conservation inside a full triad. R0.70J instead contracts the symmetric
zero-frequency covariance of a real conjugate pair with an external
symmetric tensor. The helicity-odd antisymmetric projector disappears, but
the helicity-even transverse projector remains. These are different
algebraic questions.

### 3.3 Vorticity-direction depletion

The cited Constantin--Fefferman and Beirão da Veiga--Berselli criteria obtain
conditional depletion/regularity under quantitative direction coherence for
the vorticity whose singular integral supplies the strain. The papers supply
no corresponding result for an independent arbitrary external harmonic
source coefficient. Their mechanisms remain a plausible conditional route
after R0.70J, but they do not furnish the missing energy-level estimate.

## 4. Precise literature finding

No source in this bounded audit proves that

\[
 S:\left(\omega\otimes\omega-
 \frac{|\omega|^2}{3}I\right)=0
\]

for every trace-free harmonic source \(S\), every divergence-free mode, or
every fixed helicity sign. The explicit symbol and witnesses in the canonical
R0.70J report rule out such a universal algebraic theorem.

The audit does identify viable *conditional* mechanisms:

- exact second-order isotropy of the directional covariance;
- a spherical 2-design before applying an absolute value or positive part;
- quantitative coherence of the direction of the actual vorticity whose
  Biot--Savart field supplies the strain;
- an equation-specific correlation between the external source coefficient
  and the core response.

None of these follows from the Leray energy inequality alone in the cited
sources.

## 5. Claim boundary

- In the literature matrix, “Exact object” summarizes the cited source's
  direct result. “What it supports” records the R0.70J inference supported by
  that result. “What it does not supply” is the R0.70J applicability boundary
  and is not necessarily a statement made by the cited authors.
- DNS observations are not elevated to theorems.
- The phrase “no matching theorem found” is restricted to the stated search
  protocol and source set.
- The explicit counterexamples disprove only a universal algebraic null
  structure based on STF, incompressibility, angular labels, and helicity.
  They do not disprove a deeper cancellation tied to one self-consistent NSE
  trajectory.
- No priority claim is made for the R0.70J tensor calculation without
  external journal-level review.
