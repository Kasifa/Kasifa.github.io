# R0.73P claim--source ledger

**Status:** source topology fixed; independent analytic verdict passed

| ID | Claim | Evidence class | Exact source or proof | Release use |
| --- | --- | --- | --- | --- |
| C1 | \(\int_0^\infty |u|_1^4<\infty\) and \(\int_0^\infty\|\nabla u\|_\infty<\infty\) for an R0.73O orbit | Internal analytic corollary | R0.73O decay ladder plus energy equality; `r073p_critical_frequency_proof.md` Section 2 | Closes finite orbit actions only |
| C2 | Relative weak \(L^2\) energy and exponential decay | Classical/internal derivation | Weak--strong relative energy; `r073p_critical_frequency_proof.md` Section 3 | Applies to every Leray--Hopf comparison selection |
| C3 | Quantitative periodic \(\dot H^{1/2}\) robustness | Published primary theorem | Burczak--Zaj\k{a}czkowski 2016, Theorem 1, DOI 10.1016/j.nonrwa.2016.03.001 | Primary existence gate for the global critical tube |
| C4 | Critical difference inequality and finite-time robustness | Published primary theorem | Mar\'in-Rubio--Robinson--Sadowski 2013, Theorem 3 and proof, DOI 10.1016/j.jmaa.2012.10.064 | Supports bootstrap and exponential synchronization |
| C5 | \(H^{1/2}\) class lies in Serrin \(L^4_tL^6_x\) | Published identity plus standard theory | Mar\'in-Rubio--Robinson--Sadowski equation (9); Serrin regularity | Propagates initial \(H^3\) regularity globally |
| C6 | Band-limited \(N^{-1/2}\) threshold | Exact analytic corollary | Parseval/Bernstein inequality in `r073p_critical_frequency_proof.md` Section 7 | Sufficient frequency-localized \(L^2\) gate |
| C7 | Mixed \(L^2+H^s\) and low/high-tail gates | Exact analytic corollary | Fourier log convexity and orthogonal split in Section 8 | Sufficient, not necessary |
| C8 | Norm-transfer exponent \(1/2\) is attained | Exact analytic witness | One normalized divergence-free Fourier shear mode | Sharp only for the embedding |
| C9 | Every periodic Leray--Hopf solution is eventually Gevrey | Published primary theorem | Hoang--Martinez 2017, Theorem 2.4, DOI 10.3233/ASY-171429 | Verifies uniform eventual-regularity quantifiers |
| C10 | Uniform eventual \(H^3\) entry on an \(L^2\) ball | Internal analytic proof | `r073p_delayed_synchronization_proof.md` Sections 1--2 | Common upper time; selection-dependent internal entry time allowed |
| C11 | One-sided delayed \(L^2\to H^3\) Lipschitz synchronization | Internal analytic proof | `r073p_delayed_synchronization_proof.md` Sections 3--4 | Only against a fixed global strong reference |
| C12 | Mucha 2008 threshold depends on high trace norm | Published primary theorem | Mucha 2008, Theorem 1.2, DOI 10.4064/bc81-0-18 | Excludes promotion to a uniform \(L^2\)-only theorem |
| C13 | Mucha 2001 exact \(L^2\) threshold dependence | Unresolved collision | DOI 10.1006/jdeq.2000.3863; full theorem unavailable in bounded audit | No release theorem relies on it |
| C14 | Uniform \(L^2\)-only strong threshold | Open claim | No verified source or internal proof | Must remain `OPEN_COLLISION_SENSITIVE` |
| C15 | Arbitrary-data Clay conclusion | Open problem | Outside all proved interfaces | Must remain `OPEN` and `NOT CLAY` |
| C16 | Broader collision audit: anisotropic, almost-two-dimensional, and critical small-data routes | Published primary sources | `r073p_primary_literature_addendum.md`: Iftimie 1999, Gallagher 1997, Kato 1984, Koch--Tataru 2001, and two Mucha 2008 papers | Confirms that verified strong results retain a critical or higher-trace smallness condition |

## Evidence rules

1. Published theorems are cited only with their verified equation, domain,
   topology, and time quantifiers.
2. Internal analytic corollaries may combine published theorems with the
   finite actions proved in R0.73O, but do not acquire novelty by
   combination.
3. Finite plotted values of exact powers are diagnostics and presentation
   assets only.
4. An inaccessible full theorem is not reconstructed from an abstract.
5. No result in this ledger supports finite-time blow-up, nonuniqueness, or
   arbitrary-data global regularity.
