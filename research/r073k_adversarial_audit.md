# R0.73K adversarial audit

**Final decision:** PASS
**Purpose:** attempt to break the theorem by domain jumps, parameter loss,
nonnormality, or an invalid semigroup shortcut

## 1. Attacks attempted

The audit tested five possible failure mechanisms.

1. **Parameter degeneration:** pointwise viscous persistence might fail to
   admit one common threshold on \([0,1/450]\).
2. **Multiplicity or symmetry failure:** a rank-one inviscid branch might
   split into a complex-conjugate viscous pair.
3. **Condition-number blow-up:** projection convergence might be too weak to
   preserve a useful left--right overlap.
4. **Unbounded perturbation misuse:** the formal first-order eigenvalue
   correction might illegally apply \(L\) to an uncontrolled vector.
5. **Spectral-bound fallacy:** a fixed real-part gap might be used as if it
   automatically bounded a nonnormal complementary semigroup.

No attack produced a counterexample to the final theorem.

## 2. Parameter-uniformity attack

**Defeated.**  Uniformity is not inferred from a collection of pointwise
theorems.  It comes from a common dense core, joint strong convergence, the
norm-compact family \(d\mapsto K_d\), the corresponding adjoint family, and
one compact product parameter set.  These inputs produce a single Fredholm
inverse bound and a single small-viscosity threshold.

The proof also explicitly rejects full Kato norm-resolvent convergence, so
there is no hidden compact-resolvent contradiction at \(\varepsilon=0\).

## 3. Rank-one and reality attack

**Defeated.**  Operator-norm projection convergence below one preserves rank.
The total algebraic multiplicity in the selected disk is therefore exactly
one.  The antiunitary reflection--conjugation symmetry preserves the viscous
domain and maps \(\lambda\) to \(\bar\lambda\).  A nonreal point would force
two points counted with multiplicity, contradicting rank one.

## 4. Conditioning attack

**Defeated.**  R0.73J gives

\[
 \sup_d\|P_0(d)\|<{1\over0.5853}=1.7085255\ldots .
 \tag{4.1}
\]

After choosing the common viscosity threshold so that the uniform projection
difference is below \(0.08\),

\[
 \sup_d\|P_\varepsilon(d)\|<1.7885256<{9\over5}.
 \tag{4.2}
\]

For rank-one projections this is exactly the reciprocal left--right overlap
bound, giving a viscous overlap greater than \(5/9\).

## 5. Unbounded-domain attack

**Defeated after repair.**  The first draft stated the smoothness input too
briefly.  The final version includes a uniform denominator bound for the
explicit adjoint potential, parameter-dependent ODE regularity, compact-
interval control of the normalization, and

\[
 \ell_0(d)\in D(L),\qquad
 \sup_d\|L\ell_0(d)\|<\infty.
 \tag{5.1}
\]

It separately proves
\(P_\varepsilon H\subset D(B_\varepsilon)=D(L)\).  The exact pairing identity
therefore moves \(L\) onto a controlled inviscid vector and never estimates
\(L(h_\varepsilon-h_0)\).

## 6. Nonnormal semigroup attack

**Defeated after repair.**  The final proof does not infer a semigroup bound
from the spectral gap.  It proves a reduced-resolvent bound on the full
vertical line, including high-frequency decay.  The Bromwich argument first
integrates by parts, then moves the square-resolvent integral through the
reduced pole-free strip.  Uniform \(O(|\tau|^{-2})\) control makes the
horizontal sides vanish.  The argument does not require an analytic-sector
angle uniform in viscosity.

## 7. Remaining open attack surfaces

The following claims are not present and were not audited as if they were:

- an explicit numerical value of the viscosity threshold;
- analyticity in viscosity through \(\varepsilon=0\);
- nonselfadjoint adiabatic tracking for time \(D_*/\varepsilon\);
- a matching two-sided action with bounded prefactor;
- nonlinear or three-dimensional Navier--Stokes instability;
- finite-time singularity or the Clay problem.

```text
adversarialAudit=PASS
structuralCounterexampleFound=false
localRepairsCompleted=true
continuumClaimsK1ThroughK7Survive=true
```
