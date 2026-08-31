# R0.73R independent literature readback

**Read back against:** `research/r073r_primary_literature_audit.md` and
`research/r073r_claim_source_ledger.md`

**Date:** 2026-08-31

**Verdict:** `PASS_WITH_CLASSICAL_COLLISION_AND_NO_PRIORITY_LANGUAGE`

## 1. What was rechecked

The readback did not search for a favorable novelty statement.  It checked
whether the release's strongest public phrases remain inside the domains and
indices of the cited sources.

| Slot | Readback | Verdict |
| --- | --- | --- |
| periodic caloric Besov norm | Chemin--Gallagher work on mean-free \(\mathbb T^3\); Definition 1.1 with \((s,p,q)=(1/2,6,4)\) gives the exact \(dt\) heat integral | `DIRECT_COLLISION` |
| periodic dyadic norm | the same paper's Definitions 2.1--2.2 give the LP version, and Lemma 4.2 supplies annular heat decay | `DIRECT_COLLISION` |
| critical-space stability | Gallagher--Iftimie--Planchon Theorem 3.1 is a whole-space openness/stability theorem in critical Besov classes, including \((p,q)=(6,4)\) | `CLASSICAL_MECHANISM_DOMAIN_DIFFERS` |
| sixth-moment phase majorant | Green--Ruzsa state the even-integer majorant principle; \(p=6\) is included | `DIRECT_COLLISION` |
| Rudin--Shapiro flatness | the historical record and Balister's accessible Proposition 4 support the complementary identity and \(O(\sqrt m)\) bound | `CLASSICAL_INPUT` |
| exact divergence-free matched pair | no exact collision was located in the bounded search | `NO_PRIORITY_INFERENCE` |
| arbitrary \(L^2\)-only strong entrance | none of the sources proves it | `OPEN` |

## 2. Notation correction

The local LP decomposition has indices \(j\ge0\) and one low-frequency block.
The inspected periodic source writes \(B^{-1/2}_{6,4}\), not a separate
homogeneous-space theorem.  Public text should therefore use “mean-zero
periodic \(B^{-1/2}_{6,4}\)” or explain that a dot only records removal of the
zero mode.

This correction does not change the norm because all data in the release are
mean zero and the torus has a spectral gap.  It does prevent an avoidable
homogeneous/inhomogeneous notation overclaim.

## 3. Source-scope boundaries

1. The Gallagher--Iftimie--Planchon theorem is on \(\mathbb R^3\).  It may
   establish that critical-Besov orbit openness is classical in principle,
   but it is not cited as the proof of the periodic all-restart radius.
2. The Green--Ruzsa/Hardy--Littlewood majorant statement authorizes only the
   even-exponent phase comparison.  It does not supply the R0.73R vector
   normalization, carrier factor, or heat trace.
3. Rudin--Shapiro sources authorize the recursion and flatness estimate.  The
   three-dimensional divergence-free tensor embedding remains an internal
   exact construction.
4. Randomized-data and spectral-projector sources are collision context.
   They are not dependencies of the deterministic proof.
5. Failure to find the exact matched pair is not evidence that it is new.

## 4. Authorized public boundary

The literature supports this wording:

> The caloric Besov equivalence and the surrounding phase/sparse-frequency
> mechanisms are classical.  R0.73R supplies a self-contained deterministic
> shell interface and one exact matched divergence-free example.  It makes no
> novelty or priority claim.

The literature does not support wording that calls the release a new Besov
space, the first phase-sensitive entrance, a new oscillatory-data regularity
theorem, or progress from arbitrary \(L^2\) data to the Clay conclusion.

## 5. Readback ledger

```text
periodicHeatBesovClaim=VERIFIED_CLASSICAL
wholeSpaceCriticalOpennessDomainPreserved=PASS
evenP6MajorantClaim=VERIFIED_CLASSICAL
rudinShapiroHistoricalScopePreserved=PASS
matchedPairNoveltyEstablished=FALSE
absenceFromBoundedSearchImpliesPriority=FALSE
uniformL2OnlyStrongEntrance=OPEN
clayConclusion=OPEN
noveltyOrPriorityClaim=FORBIDDEN
```
