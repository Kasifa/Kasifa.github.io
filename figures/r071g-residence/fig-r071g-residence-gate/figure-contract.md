# Figure contract — fig-r071g-residence-gate

## Analytical question

Can a signed projected-Lamb trace remain positive for longer than the viscous
time \(K^{-2}\), and if fixed positive relative levels do retain that scale,
is residence alone enough to turn the R0.71F heat bulk into an unweighted
bottom trace?

## Supported takeaway

The exact global-smooth 2D3C family separates three statements.

1. Sign-only residence has no universal \(CK^{-2}\) bound.
2. Fixed positive relative levels in this family exit on the critical
   \(K^{-2}\) scale.
3. Critical residence for every event still does not provide the missing
   unweighted summability.

The figure does not establish a general high-superlevel residence theorem for
arbitrary NSE solutions.

## Evidence classes

- **Finite exact-chain integrations:** fixed-step complex RK4 applied to the
  rigorously derived 2D3C sideband ODE at \(|m|\le24\).  These are reduced
  checks of a global-smooth NSE family, not a 3D PDE simulation.
- **Exact weak-coupling limits:** horizontal references from
  \(q/q(0)=e^{-6\theta}\) at the analytically extended value \(\mu=0\).
- **Exact functional partial sums:** closed-form values for the disjoint-event
  residence obstruction.
- **Illustrative asymptotic guide:** the dashed \(0.5\mu^{-1}\) line in Panel
  B is labeled as a guide and is not used as a theorem.

## Panel contract

- **A — signed low-shell work.** Plot \(e^{4\theta}H_\mu\) for
  \(\mu=0.5,0.2,0.1,0.05\) through the first crossing and a short negative
  continuation.  Retain line-style distinctions and the exact \(\mu=0\)
  horizontal coefficient reference.
- **B — first sign exits.** Plot the five finite exit checks against
  \(\mu^{-1}\), the \(0.5\mu^{-1}\) guide, and a one-viscous-time reference.
- **C — fixed relative \(q\) exits.** Plot first exits at
  \(\rho=0.5,0.1,0.01\), with exact
  \(\frac16\log(1/\rho)\) weak-coupling references.  The horizontal axis must
  visually approach \(\mu=0\) to the right.
- **D — summability obstruction.** Plot the unweighted partial sum \(n\) and
  the weighted partial sum \((4^n-1)/(3\cdot4^n)\), with separate labeled
  axes and the \(1/3\) limit.

## Data and numerical grain

- Chain radius: 24 on each side of the central mode.
- Fixed step: \(2.5\times10^{-4}\) in dimensionless time.
- Final time: \(10.5\); archived profiles every \(0.02\).
- Couplings: \(1,0.5,0.2,0.1,0.05\).
- Relative levels: \(0.5,0.1,0.01\).
- Independent adaptive DOP853 checks use radii 12 and 18 and agree on the
  displayed first sign exits to better than \(4\times10^{-14}\) between those
  two radii.  The fixed-step figure values agree with the adaptive values to
  better than \(5\times10^{-8}\).
- Random seed: none.

## Visual and archival rules

- Static double-column figure, exactly 178 by 108 millimetres.
- Vector PDF and SVG plus a 600 dpi PNG.
- Line style and marker shape must retain the claims in grayscale.
- Inspect the full-resolution PNG, grayscale preview, and independently
  rasterized PDF.
- Archive the CSV, generator, plotting source, validation, independent
  comparison, caption, environment, commands, manifest, and SHA-256 ledger.

## Claim boundary

The arbitrary-\(M\) sign-only no-go is proved analytically in the report; the
finite curves merely check the exact reduced chain.  The relative-level
curves concern this one true-solution family, not arbitrary NSE solutions.
Panel D is an abstract logical obstruction rather than an NSE trajectory.
Nothing here proves regularity, constructs a singularity, establishes
originality, or resolves the Millennium problem.
