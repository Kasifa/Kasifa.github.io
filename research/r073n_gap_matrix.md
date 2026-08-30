# R0.73N claim-evidence gap matrix

**Status:** literature, internal analytic, adversarial, symmetry, and
compactness audits PASS; finite and publication gates remain separately
tracked

| ID | Claim or question | Best evidence route | Current state | Residual boundary or required action |
|---|---|---|---|---|
| G1 | What does FPS \((X,Z)\) mean? | FPS Definition 2.1 | CLOSED | \(X\) is solution regularity; \(Z\) measures both input smallness and output distance |
| G2 | Does the draft's original \(H^3\)-small/\(L^2\)-output definition equal FPS \((H^3,L^2)\)? | direct comparison with FPS Definition 2.1 | NO | use \(H^3\)-in/\(L^2\)-out terminology instead |
| G3 | How is a nonstationary base connected to FPS? | explicit synchronized process definition | CLOSED AS DEFINITION | adaptation at \(t_0=0\), not a theorem of FPS; no orbital or all-start-time claim |
| G4 | Is fixed-distance escape the complete negation of FPS stability? | FPS remark after Definition 2.1 | NO | loss of the required global \(X\)-solution is the other branch |
| G5 | Are the R0.73M quantifiers family-level? | sealed R0.73M theorem | CLOSED | \(\Lambda\) changes the base; no exchange to one fixed member |
| G6 | Does every fixed member have finite relative \(L^2\) gain? | exact relative-energy identity and finite integrated strain | CLOSED on the common strong lifespan | call it all-time only for global comparison solutions |
| G7 | Does every fixed member have a positive full-three-dimensional \(H^3\) tube? | direct periodic \(H^3\) energy/bootstrap/continuation proof | CLOSED INTERNALLY; independent analytic audit PASS | synchronized \((H^3,H^3)\), not an external literature inference |
| G8 | Does full-three-dimensional \(H^3\)-small input imply \(L^2\)-small synchronized output? | G7 plus Sobolev norm domination | CLOSED INTERNALLY | custom mixed-topology corollary; avoid FPS pair notation |
| G9 | Is the planar subsystem FPS-style \((H^3_{\mathrm{pl}},L^2_{\mathrm{pl}})\) stable? | planar invariance, two-dimensional global regularity, and the relative \(L^2\) bound | CLOSED INTERNALLY | restrict both \(X\) and \(Z\) to the planar phase space |
| G10 | Is full-three-dimensional FPS \((H^3,L^2)\) stable? | no theorem in the source proof or checked literature | **OPEN** | must handle arbitrary \(H^3\)-regular data small only in \(L^2\), including global continuation |
| G11 | Can steady spectral-to-nonlinear transfer prove the trajectory claim? | FPS Theorem 2.2 versus the time-dependent base | NO | one autonomous steady generator is absent |
| G12 | Can a frozen unstable Rayleigh operator prove nonlinear instability of the complete orbit? | Li--Zhao 2024 and direct finite-action comparison | NO | a full non-autonomous nonlinear evolution theorem would be required |
| G13 | Does transient or threshold amplification contradict fixed-member stability? | Trefethen et al.; Li--Masmoudi--Zhao; direct quantifier comparison | NO | finite parameter-dependent gain is compatible with a smaller stability radius |
| G14 | Do Grenier-type family theorems establish a fixed-member result? | Desjardins--Grenier; Grenier; Grenier--Nguyen | NO | parameter family, boundary, approximate-solution, and forcing hypotheses differ |
| G15 | Does periodic decaying-shear literature prove or contradict the internal tube? | Lin--Xu | NO CONFLICT | stable-side precedent only; theorem-specific radius remains internal |
| G16 | What is the correct flow-map statement? | one autonomous map \(S(T_*)\) and pointed maps \(F_\Lambda\) | RESOLVED | say pointed family non-equicontinuity or failure of uniform continuity on the explicit planar data set |
| G17 | Is the amplification modulus genuinely local? | \(H^3\)-localized limsup over the explicit strong-solution domain \(\mathcal D_T\) | CLOSED | \(2\to2\) labels quotient norms; locality remains \(H^3\) |
| G18 | Is the \(H^3\) commutator presentation norm-consistent? | Bessel potential \(J^3\), Kato--Ponce, and equivalent integer-derivative presentation | CLOSED; independent audit PASS | all norm-equivalence constants are absorbed into \(C_3\) |
| G19 | What does Fujita--Kato support? | classical initial-value theory | RESOLVED | local strong theory/continuation background only; not the finite-strain stability theorem |
| G20 | Are the registered symmetry and compactness shortcuts excluded? | direct transformation and Sobolev/Fourier obstruction files | CLOSED; independent audit PASS | route-specific; unregistered alternative mechanisms are not classified |
| G21 | Does the bounded search prove novelty or priority? | two-wave search record and stop rule | NO | retain bounded-search, non-exhaustive, non-priority wording |
| G22 | Does R0.73N bear on arbitrary-background instability, singularity, or Clay? | theorem scope and official problem boundary | OPEN / OUT OF SCOPE | no extrapolation is licensed |

## Release blockers

The literature gate may remain PASS only if every downstream theorem,
ledger, recap, and public page preserves all of the following:

1. full-three-dimensional FPS \((H^3,L^2)\) is OPEN;
2. the proved full-three-dimensional result is FPS-style
   \((H^3,H^3)\);
3. \(H^3\)-in/\(L^2\)-out is labeled as a custom corollary;
4. the planar \((H^3_{\mathrm{pl}},L^2_{\mathrm{pl}})\) statement is
   explicitly restricted to the invariant planar phase space;
5. the fixed-\(\Lambda\) theorem is attributed to the internal energy and
   bootstrap proof, not to external literature;
6. family non-equicontinuity is not renamed fixed-member instability;
7. absence language stays bounded and carries no novelty or priority claim.

## Fail-closed rule

Any occurrence of “\((H^3,H^3)\), hence FPS \((H^3,L^2)\)” or any closure of
full-three-dimensional FPS \((H^3,L^2)\) reopens G1--G10 and fails the
claim-boundary gate.  Any public “first”, exhaustive, or priority statement
reopens G21.  Finite computation and literature analogy cannot close an
internal continuum-theorem row.
