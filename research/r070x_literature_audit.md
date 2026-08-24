# R0.70X bounded literature audit

**Scope:** primary-source boundary for the cyclic triad identity, the
high--high--low \(t/R\) factor, and the complete-frame rank-at-most-one signed
obstruction

**Date:** 2026-08-25

## Decision

The R0.70X calculations should not be described as the first triadic
conservation law or the first cancellation-based scale-locality factor.
Both phenomena have classical precedents in different observables.

The report makes a narrower claim:

1. the Laplacian-weighted cyclic identity is derived for the present
   strain--vorticity amplitudes;
2. that identity is combined with the unequal response kernel of the pinned
   complete radial frame;
3. the resulting frame-defect cyclic block has a deterministic orbitwise
   \(t/R\) bound with a matching sharp family; and
4. an explicit complete-frame finite Fourier field separates covariance
   rank depletion from signed-work depletion.

The bounded search found no primary-source statement matching item 4. This
is not a novelty or priority claim.

## Primary sources and exact boundaries

### Waleffe: helical triad conservation and cancellation

Fabian Waleffe, *The nature of triad interactions in homogeneous
turbulence*, Physics of Fluids A 4 (1992), 350--363,
[DOI 10.1063/1.858309](https://doi.org/10.1063/1.858309).

Waleffe's helical formulation uses exact energy and helicity conservation
inside each inviscid triad. It also identifies large opposite-signed
contributions in elongated triads whose net transfer can be smaller.

Boundary for R0.70X: the identity

\[
 |n|^2A_n+|p|^2A_p+|q|^2A_q=0
\]

is not advertised as a new universal triad-conservation principle. Its
role here is the exact adaptation to the frame-defect strain amplitudes and
the response-slope difference formula.

### L'vov--Falkovich: counterbalanced nonlocal interaction

Victor L'vov and Gregory Falkovich, *Counterbalanced interaction locality
of developed hydrodynamic turbulence*, Physical Review A 46 (1992),
4762--4772,
[DOI 10.1103/PhysRevA.46.4762](https://doi.org/10.1103/PhysRevA.46.4762).

This work obtains an explicit scale-ratio factor in a statistical
triple-correlation asymptotic for nonlocal turbulence interactions.

Boundary for R0.70X: the factor in that paper concerns a quasi-Lagrangian
statistical observable, not the deterministic radial-frame defect
\(\mathcal G(n,p,q)\). The present \(t/R\) estimate is therefore not
claimed as the first nonlocal cancellation factor.

### Eyink--Aluie: conditional scale locality

Gregory Eyink and Hussein Aluie, *Localness of energy cascade in
hydrodynamic turbulence. I. Smooth coarse graining*, Physics of Fluids 21
(2009), 115107,
[arXiv:0909.2386](https://arxiv.org/abs/0909.2386),
[DOI 10.1063/1.3266883](https://doi.org/10.1063/1.3266883).

Hussein Aluie and Gregory Eyink, *Localness of energy cascade in
hydrodynamic turbulence. II. Sharp spectral filter*, Physics of Fluids 21
(2009), 115108,
[arXiv:0909.2451](https://arxiv.org/abs/0909.2451),
[DOI 10.1063/1.3266948](https://doi.org/10.1063/1.3266948).

These papers prove scale-locality estimates for kinetic-energy flux under
inertial-range regularity/scaling assumptions and discuss cancellation in
signed nonlocal contributions.

Boundary for R0.70X: their flux, filtering, and hypotheses differ from the
vorticity covariance observable. Their results motivate retaining the
signed cyclic sum but do not prove the orbitwise formula or a global
critical bound here.

### Bony--Coifman--Meyer: summation framework

Jean-Michel Bony, *Calcul symbolique et propagation des singularités pour
les équations aux dérivées partielles non linéaires*, Annales scientifiques
de l'École Normale Supérieure 14 (1981), 209--246,
[DOI 10.24033/asens.1404](https://doi.org/10.24033/asens.1404).

Ronald Coifman and Yves Meyer, *On commutators of singular integrals and
bilinear singular integrals*, Transactions of the AMS 212 (1975), 315--331,
[DOI 10.1090/S0002-9947-1975-0380244-8](https://doi.org/10.1090/S0002-9947-1975-0380244-8).

These are the appropriate classical references for comparable-frequency
multiplier estimates and dyadic paraproduct summation.

Boundary for R0.70X: applicability to a final vector-valued cyclic operator
still requires explicit uniform symbol-derivative estimates, treatment of
zero and diagonal sets, periodic transference, and shell summation. The
orbitwise \(t/R\) calculation alone is not such a theorem.

Camil Muscalu, *Paraproducts with flag singularities I*, Revista Matemática
Iberoamericana 23 (2007), 705--742,
[DOI 10.4171/RMI/510](https://doi.org/10.4171/RMI/510), is a possible later
tool only if the final multiplier develops genuinely nested singular
subspaces. The current response kernel does not establish a flag structure.

## Claim controls used in the report

- The cyclic identity is called an exact identity for this observable, not
  a new general conservation law.
- The \(t/R\) result is called deterministic and orbitwise, not a completed
  global scale-locality theorem.
- The sharp family proves only the exponent boundary for that orbitwise
  estimate.
- The rank-at-most-one field is used as a separation/counterexample result, not as
  a Navier--Stokes evolution or regularity theorem.
- No source above is presented as proving the R0.70X covariance statement.
- No priority, singularity, global-regularity, or Millennium claim is made.
