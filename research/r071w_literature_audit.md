# R0.71W bounded primary-source audit: complete Leray ledger, projected rotational charge, and fixed-zero trace

**Search date:** 2026-08-26

**Question:** which established results license the Leray energy/enstrophy
ledger, rotational/Lamb formulation, Fourier \(\dot H^{-1}\) square
budget, 2D3C reduction, and level-crossing interfaces used around R0.71W;
and does a checked source already give the deterministic, data-uniform,
fixed-zero quadratic trace that the report disproves for the complete first
row?

## 1. Bounded answer

The checked sources license the surrounding interfaces, not the R0.71W
theorem.

Leray and Temam provide the energy class and the standard trilinear estimates.
The rotational identity fixes the sign convention

\[
 u_t=\nu\Delta u+\mathbb P(u\times\omega),\qquad
 L:=\mathbb P(u\times\omega),
\]

while the classical enstrophy equation remains a strong-solution identity.
Littlewood--Paley theory supplies the Fourier background for the elementary
finite-overlap estimate

\[
 \sum_j \kappa_j^{-2}\|T_jL\|_2^2
 \lesssim \|L\|_{\dot H^{-1}}^2.
\]

The exact constant and the particular multiplier family used in R0.71W are
checked directly by Plancherel; they are not quoted as a theorem from the
monograph.

The 2D3C literature verifies that the ambient invariant reduction is
standard. It does not contain the narrower triangular identity
\(L=(-vf_z,0,0)\), amplitude doping, modular target isolation, uniformly
rescaled implicit-function construction, prescribed simple roots, or the
complete-ledger no-go sequence. Those are internal arguments in the report.

Area, indicatrix, deterministic local-time, and truncated-variation results
pay crossings only after integration over the level variable (or identify a
density only almost everywhere). They do not imply a uniform bound at the
distinguished level \(z=0\). Stochastic Kac--Rice formulas can evaluate a
fixed level in expectation under smoothness and nondegeneracy hypotheses, but
that is a different theorem and does not apply to a deterministic single NSE
trajectory from Leray data.

Within the bounded search described in Section 6, I did **not locate** a
deterministic theorem converting the complete normalized first Leray row into
a data-uniform sum of fixed-zero quadratic atoms. This is a bounded-search
negative result only. It is **not** a statement that such a theorem does not
exist, and it is **not** a claim of novelty, originality, or priority for
R0.71W.

## 2. Source-to-claim ledger

| ID | Primary or authoritative source, date, and visible evidence | Claim licensed for R0.71W | Applicability, conflict, or gap | Confidence |
|---|---|---|---|---|
| S1 | Jean Leray, *Sur le mouvement d'un liquide visqueux emplissant l'espace*, *Acta Mathematica* 63 (1934), pp.193--248, [DOI](https://doi.org/10.1007/BF02547354), [scan](https://archive.ymsc.tsinghua.edu.cn/pacm_download/117/5537-11511_2006_Article_BF02547354.pdf), p.235 equation (5.9) and p.241 | The foundational weak-solution energy inequality and the energy-class control behind the first-row ledger. | It does not control a prescribed zero-level trace, \(\omega_t\), or a sum of quadratic root slopes. | high |
| S2 | Roger Temam, *Navier--Stokes Equations and Nonlinear Functional Analysis*, 2nd ed., SIAM (1995), [DOI](https://doi.org/10.1137/1.9781611970050), §2.3 pp.11--13, equation (3.2) p.17, Theorem 3.1 p.21, Remark 3.2 and Theorem 3.2 pp.21--22 | Standard Sobolev interpolation, trilinear estimates, energy identity/inequality, and global two-dimensional strong theory. In particular they justify the finite-time integrability of the normalized projected rotational row. | Combining the cited estimates to obtain \(\|L\|_{\dot H^{-1}}\lesssim\|u\|_4^2\) is a direct deduction, not a theorem stated in the source. No fixed-zero atom estimate follows. | high |
| S3 | Charles R. Doering and J. D. Gibbon, *Applied Analysis of the Navier--Stokes Equations*, Cambridge University Press (1995), [DOI](https://doi.org/10.1017/CBO9780511608803), p.129 equations (6.5.1)--(6.5.3), p.131 equation (6.5.13) | Rotational/Lamb-vector formulation and the classical three-dimensional enstrophy identity, including vortex stretching. | Many sources call \(\omega\times u\) the Lamb vector. R0.71W uses the opposite projected sign \(L=\mathbb P(u\times\omega)\); the report's convention is algebraically consistent but should be named explicitly. The enstrophy equality requires smoothness. | high |
| S4 | Luca Biferale, Michele Buzzicotti, and Moritz Linkmann, *From two-dimensional to three-dimensional turbulence through two-dimensional three-component flows*, *Physics of Fluids* 29, 111101 (2017), [DOI](https://doi.org/10.1063/1.4990082), [arXiv](https://arxiv.org/abs/1706.02371), §II equations (1)--(2), manuscript p.2 | A three-component velocity depending on two coordinates is an exact invariant reduction: the in-plane velocity follows 2D NSE and the remaining component follows advection--diffusion. | It licenses only the ambient 2D3C class. The triangular ansatz \(u=(f(y,z,t),0,v(y,t))\), its global linear dynamics, and the exact formula for projected \(L\) are verified by substitution in R0.71W. | high |
| S5 | Hajer Bahouri, Jean-Yves Chemin, and Raphaël Danchin, *Fourier Analysis and Nonlinear Partial Differential Equations*, Springer (2011), [DOI](https://doi.org/10.1007/978-3-642-16830-7), Littlewood--Paley theory pp.51--121 and incompressible NSE pp.203--243 | Standard dyadic multipliers, Bernstein estimates, homogeneous Sobolev norms, and finite-overlap square-function bookkeeping. | The exact compact annular projector and \(\dot H^{-1}\) square budget in R0.71W are a direct torus Plancherel calculation. The book does not state the report's no-go theorem. | high for background; high for the direct finite-overlap deduction |
| S6 | Samuel Karlin and William J. Studden, *Tchebycheff Systems: With Applications in Analysis and Statistics*, Interscience (1966), [catalogue record](https://books.google.com/books?id=P7Y-AAAAIAAJ), Chapters I and XI, especially Chapter XI, Theorem 1.1 | Wronskian criteria, zero-counting, nonsingular interpolation matrices, and the standard ECT-system mechanism used for the limiting exponential response family. | The source does not verify this particular response family, the uniform inverse Jacobian for large \(q\), the divided target map, or an NSE implicit curve. Those estimates are proved in R0.71W §4. | high for ECT theory; internal verification still required |
| S7 | Herbert Federer, *Geometric Measure Theory*, Springer (1969), [DOI](https://doi.org/10.1007/978-3-642-62010-2), §3.2.3 p.243 | The weighted area formula. In one dimension it yields \(\int \sum_{r(t)=z}g(t)\, dz=\int g(t)|r'(t)|\,dt\) for the appropriate representative and hypotheses. | It integrates over \(z\). It does not evaluate the crossing density at \(z=0\), and its Lipschitz statement is not applied verbatim to every weak coefficient without the one-dimensional AC extension. | high |
| S8 | Jean Bertoin and Marc Yor, *Local times for functions with finite variation: two versions of Stieltjes change of variables formula*, *Bulletin of the London Mathematical Society* 46 (2014), 553--560, [DOI](https://doi.org/10.1112/blms/bdu014), [arXiv](https://arxiv.org/abs/1307.1288), Theorem 1 p.555 and proof pp.559--560 | Signed and positive occupation measures of a finite-variation path have crossing-number densities in \(L^1(dz)\). | The density is a level-integrated/almost-everywhere object. Absolute continuity of the occupation measure gives no uniform point evaluation at a prescribed level. | high |
| S9 | Rafał M. Łochowski, *On a generalisation of the Banach indicatrix theorem*, *Colloquium Mathematicum* 148 (2017), 301--313, [DOI](https://doi.org/10.4064/cm6583-3-2017), [arXiv](https://arxiv.org/abs/1503.01746), Theorem 1 pp.304--305 | Upcrossing, downcrossing, and total crossing counts of positive-height bands integrate to the corresponding truncated variations. | A positive band can miss excursions whose heights collapse with the data. The theorem does not survive \(c\downarrow0\) as a uniform fixed-zero quadratic trace. | high |
| S10 | Darlington Hove, Farai J. Mhlanga, Rafał M. Łochowski, and Phumlani L. Zondi, *Local times of deterministic paths with finite variation*, first posted 2024 and journal version 2026, [DOI](https://doi.org/10.4064/cm9372-11-2025), [arXiv](https://arxiv.org/abs/2405.13174), Theorem 2.8, Remark 2.9 pp.5--6, formula (16) p.8 | Modern deterministic crossing densities and change-of-variable identities, including pointwise formulations at simple levels under the stated path hypotheses. | Choosing an everywhere-defined representative is not a norm estimate for its value at zero. The source contains no Leray-to-fixed-zero trace inequality. | high for the stated deterministic local-time theorem |
| S11 | Richard B. Melrose, *Differential Analysis: 18.155 lecture notes*, MIT OpenCourseWare (2004), [official PDF](https://ocw.mit.edu/courses/18-155-differential-analysis-fall-2004/d7569c76af5fd5132b03d34b4db590e0_lecture_notes.pdf), Theorem 10.1 | The familiar one-dimensional Sobolev trace threshold: continuous point evaluation is available above one-half derivative, whereas an \(L^2\) class alone has no canonical value on a measure-zero set. | This is an explanatory functional-analytic obstruction, not an NSE counterexample and not a proof that every possible nonlinear fixed-level trace must fail. | high for the trace threshold; limited applicability to nonlinear crossing densities |
| S12 | Corinne Berzin, Alain Latour, and José R. León, *Kac--Rice formula: a contemporary overview of the main results and applications* (2022), [arXiv](https://arxiv.org/abs/2205.08742), chapters on one-dimensional level sets and nondegeneracy conditions | Under probabilistic smoothness and nondegeneracy assumptions, Kac--Rice formulas can treat a specified level in expectation. This is the closest checked positive fixed-level interface. | It averages over randomness, requires density/nondegeneracy hypotheses, and does not furnish a deterministic pathwise bound for a single NSE solution. It therefore neither conflicts with nor closes R0.71W. | high for the distinction; not a source for the R0.71W claim |

## 3. R0.71W internal claim ledger

The following table separates what the sources above supply from what must be
proved in the report itself.

| Claim | External interface | Exact R0.71W evidence | Scope retained after audit |
|---|---|---|---|
| Exact globally smooth triangular 2.5D sequence | S2 and S4 license global 2D/2D3C dynamics | §2 substitutes \(u=(f,0,v)\) into unforced periodic NSE; §3 isolates the fixed target shell | Exact smooth solutions, but a special invariant class and a different datum for every \(q\) |
| Uniform rescaled IFT | S6 licenses only the limiting ECT interpolation mechanism | §4 proves uniform Dyson bounds through two parameter derivatives, convergence of the divided target map and Jacobian, a fixed inverse bound, and contraction on a \(q\)-independent ball | Fixed finite number of prescribed rescaled roots and the chosen phase family; no arbitrary node set or \(N\to\infty\) statement |
| Exact roots and slopes | No checked source states the NSE result | §4.2 gives exact simple roots; §5 proves \(\partial_ta_q(t_{m,q})=\mathscr A_q^2[\Gamma'(\tau_m)+o(1)]\) | Root times lie in an \(O(q^{-2})\) cluster inside a fixed macroscopic interval; this is not fixed-distance interior recurrence |
| \(Y\) and \(\mathcal R_Y\) | S1--S2 license energy estimates, not the amplitude-doped asymptotic | §6 uses the \(z\)-independent background and direct \(f_z,f_y,v_y\) estimates to prove \(c\mathscr A_q^2q^2\le Y_q\le C\mathscr A_q^2q^2\) and \(\mathcal R_{Y_q}(I)\le C\) | The initial energy/enstrophy grow with \(q\); no bounded-data conclusion |
| Projected rotational charge | S3 fixes the rotational convention; S5 supplies Fourier bookkeeping | §2 proves exactly \(L_q=(-v_qf_{q,z}^{act},0,0)\); §7 proves the full-frequency bound \(\ell^{-1}\int_I\|L_q\|_{\dot H^{-1}}^2/Y_q\le C\mathscr A_q^2/q^4\) | This is the whole projected \(L\), not a selected-shell surrogate; the decoupled background does not enter \(L\) |
| Complete first-row no-go | No external theorem is used for the counterexample | §5 gives \(J_{*,2,q}\asymp\mathscr A_q^2/q^2\); §§6--7 bound the complete denominator; Theorem 8.1 takes \(\mathscr A_q=q^\alpha\), \(1<\alpha<2\) | Rejects a data-independent constant for the stated complete first-row ledger on fixed \(I\); it does not reject arbitrary data dependence or other payments |
| Data-dependent boundary | No checked source resolves the endpoint | §8.1 proves \(D_q\asymp q^{2\alpha+2}\) and \(J\asymp D_q^{(\alpha-1)/(\alpha+1)}\), defeating every fixed \(D^\beta\) with \(\beta<1/3\) after choosing \(\alpha\) | \(D^{1/3}\), larger data factors, bounded-data variants, and differently normalized ledgers remain open |
| Computation | No external numerical result is needed | §11 reconstructs the finite Chebyshev problem at high precision and independently in binary64, checking constants and predicted powers | Corroboration only; the continuum Dyson estimate, IFT, exact roots, slopes, \(Y\), and full \(L\) bounds are analytic claims |

## 4. Why level integration does not pay the fixed-zero quadratic atom

For an absolutely continuous scalar path \(r\), the weighted area formula
has the exponent ledger

\[
 \int_{\mathbb R}
 \sum_{t:r(t)=z}|r'(t)|^{p-1}\,dz
 =\int_I |r'(t)|^p\,dt.
\]

Thus an \(L_t^2\) payment controls the **level-integrated linear-slope**
density. A level-integrated quadratic slope corresponds instead to a cubic
time payment. Evaluating the quadratic density at the single level \(z=0\)
adds a second, independent trace problem.

Neither difficulty is resolved by declaring a preferred representative of an
\(L^1(dz)\) crossing density. For example,

\[
 \Phi_n(z)=n(1-nz)_+,\qquad
 \int_0^\infty \Phi_n(z)\,dz=\tfrac12,\qquad
 \Phi_n(0)=n.
\]

This scalar family is only an interface test; it is not an NSE trajectory.
The NSE-specific statement comes instead from the exact R0.71W family, where

\[
 J_{*,2,q}\asymp q^{2\alpha-2}\to\infty,\qquad
 \mathcal R_{Y_q}(I)\le C,\qquad
 \ell^{-1}\int_I
 \frac{\|L_q\|_{\dot H^{-1}}^2}{Y_q}\,dt
 \le Cq^{2\alpha-4}\to0.
\]

The fixed \(\nu^2\) baseline remains bounded, so the atom-to-complete-ledger
ratio diverges. This is a data-uniform no-go, not a global regularity result.

## 5. Attribution and computation boundary

- The external sources establish energy, rotational, 2D3C, Fourier, ECT, and
  area/occupation interfaces only.
- The triangular projection identity, modular isolation, amplitude-doped
  scaling, uniform rescaled IFT, exact roots and slopes, nonlinear enstrophy
  bounds, full-frequency projected-\(L\) estimate, and Theorem 8.1 belong to
  the internal argument in `r071w_report-source.md`.
- The producer and independent calculations check finite formulas, leading
  constants, and powers. They do not replace any continuum estimate or prove
  exact zeros.
- The report does not prove a continuation criterion, finite-time
  singularity, global regularity of general 3D NSE, failure of every
  data-dependent estimate, sharpness at exponent \(1/3\), or a priority
  claim.

## 6. Search boundary and stopping reason

The bounded search covered: Leray/Temam energy theory; rotational and
enstrophy identities; exact 2D3C reductions; Fourier/Littlewood--Paley
\(\dot H^{-1}\) bookkeeping; ECT interpolation; one-dimensional
area/coarea and finite-variation occupation identities; truncated crossings;
deterministic local times; Sobolev point traces; and stochastic Kac--Rice as
the closest positive fixed-level analogue.

Targeted title, DOI, arXiv, and reverse-keyword searches repeatedly returned
one of four interfaces: a level integral, an almost-every-level density, a
positive-height band, or a stochastic expectation with nondegeneracy. I
stopped after these categories stabilized and after the primary/authoritative
sources above exposed the precise remaining deterministic trace gap. The
search was not exhaustive across every language, monograph, or unpublished
manuscript.

Accordingly, “not located” is the only warranted literature statement. It
must not be rewritten as “does not exist,” “is new,” or “has priority.”
