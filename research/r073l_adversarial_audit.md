# R0.73L adversarial audit

**Status:** PASS; no surviving counterexample under the sealed hypotheses

## 1. Counterexample target

The audit attempted to preserve all R0.73K inputs while producing an
unbounded prefactor on \([0,D_*/\varepsilon]\).  The relevant attack classes
were:

1. a Jordan nilpotent on the selected block;
2. a second branch with equal or larger real action;
3. nonnormal switching growth in the complement;
4. loss through a badly conditioned moving projection;
5. an illegal backward use of the parabolic complement;
6. a hidden \(H^2\) graph-norm blow-up;
7. cancellation between nonorthogonal selected and complementary pieces.

## 2. Why the attacks fail here

The first two are excluded by the algebraically simple rank-one branch and
the fixed right-half-plane isolation proved in R0.73K.  The fourth is excluded
by \(\|P_\varepsilon\|<9/5\) and the uniform \(P_\varepsilon'\) bound.

The third attack is genuine in abstract nonnormal systems: frozen spectral
gaps do not control arbitrary switched products.  The R0.73L proof does not
deny this.  Instead, it uses the special slow drift
\(B(d+\varepsilon\tau)-B(d)=O(\varepsilon)\) on each fixed fast block and
the exact Kato fiber map.  Once the per-block relative norm is strictly below
one, switched-growth counterexamples cannot satisfy the displayed Duhamel
bound and all the inherited constants simultaneously.

The proof contains no backward complement evolution and no global
\(W^{-1}BW\) conjugation.  Thus attacks five and six do not apply.  Attack
seven is blocked by the projection inequality
\(\|u\|\ge\|Pu\|/\|P\|\), not by a false Pythagorean identity.

## 3. Parameter-separation stress test

If viscosity \(\nu\) and the adiabatic parameter \(\varepsilon\) were
independent, an eigenvalue estimate
\(|\lambda_\nu-\lambda_0|=O(\nu)\) would insert the factor

\[
 \exp[O(\nu/\varepsilon)].
\]

The bounded-prefactor conclusion could then fail when
\(\nu/\varepsilon\to\infty\).  R0.73L is valid because the reduced equation
uses the same \(\varepsilon\) in viscosity and slow time.  This dependency is
now stated explicitly and is part of the theorem, not an incidental notation.

## 4. Backward-localization stress test

The legal statement normalizes one forward selected orbit at its terminal
time and compares two forward-time estimates.  The exact terminal vector is
only relatively \(O(\varepsilon)\) close to \(P(D)H\); it need not lie in that
line.  The proof makes neither a backward solvability claim nor an assertion
for arbitrary terminal spectral data.

## 5. Final adversarial verdict

No counterexample was found that satisfies the rank-one branch, uniform
projection motion, bounded profile drift, frozen relative semigroup decay,
and the corrected block-Duhamel inequalities.  The theorem is therefore
accepted with the following retained open boundary:

```text
exactInstantaneousSelectedInvarianceForTrueOrbit=OPEN
backwardParabolicEvolutionFromTerminalEigenvector=OPEN
explicitEpsilonL=OPEN
limitingPrefactor=OPEN
twoTermWKB=OPEN
nonlinearAndThreeDimensionalClosure=OPEN
Clay=OPEN
```

