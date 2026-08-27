# Figure contract

## Analytical question and takeaway

**Question.** Can one verify the R0.72O full-superposition
enhanced-dissipation gate for a genuine two-carrier physical class, and where
does that verification lose Morse geometry?

**Supported takeaway.** Yes, for the declared `(R, 2R)` affine-row family
with `B=2`, `0 < lambda_- <= |lambda| <= 1/8`, and uniform certificate
lineage. The full shear has two fixed nondegenerate critical points and meets
the shape gate uniformly. The exact first Morse wall is `|lambda|=1/4` at
`y=0`, with the time-slice wall `|lambda|=exp(3y)/4`. This is a restricted
positive class, not a theorem for arbitrary `N`, `p`, phases, or geometries.
In the exact cell reduction, the paired positive/negative shifts contribute
the factor `2 cos(m phi)` and the definition of `epsilon` absorbs that factor;
`B=2` is not a cancellation of the signed-shift factor.

## Chart map

| Panel | Analytical comparison | Form | Claim status |
|---|---|---|---|
| A | exact affine-cell reduction and full two-carrier profile | three direct formula slices plus the exact reduction annotation | proved identity in the declared class |
| B | uniform bracket and fixed critical set | exact envelope with critical-point guides | proved shape inequalities; no sampling inference |
| C | time-slice Morse wall versus the safe cone | exact boundary curves and shaded cone | exact applicability boundary, not an ED counterexample |
| D | R0.72O conditional ledger versus R0.72P proved class | fixed-polynomial-coupling asymptotic representative with open conditional and filled proved status marks | proved only for the declared two-carrier family; the exact ledger retains `L_(R,epsilon)` and constants are suppressed |

## Runtime lineage

The formal plot command must receive six paths:

- the frozen R0.72P analytic report;
- the producer configuration from the certified run;
- the passed producer result;
- the independent configuration from the certified run;
- the passed independent result;
- the passed producer-independent crosscheck.

Those paths do not replace the certificate bundle ledger. All five JSON
inputs must be the canonical files in `research/certificates/r072p`, and the
derived `SHA256SUMS` lineage must be valid UTF-8/LF, uniquely byte-sorted,
free of symlinks and nested entries, digest-correct, and an exact cover of the
flat directory except for the ledger itself and a regular `.DS_Store`.

The plotting code hashes all six explicit inputs plus the derived certificate
ledger and stores their resolved paths and hashes in `results.json`. It accepts
no implicit fallback and does not infer a
certificate location from a working tree. The crosscheck must declare
`checks.formalSourceReady=true`, `temporaryUnsealedSourceAllowed=false`, and a
full source commit shared by both clean, tracked route configurations.
Certificate content is not plotted as empirical data; it gates lineage and
corroborates the exact formulas.

At formal sealing, the source commit must contain byte-identical Git blobs
for the report and all three audit programs. The certificate commit must
contain byte-identical blobs for the two configurations, two results, and the
crosscheck supplied at runtime. `results.repositoryCommitAtBuild` must equal
the certificate commit, and the source commit must be its ancestor. The
certificate commit also binds the `SHA256SUMS` blob itself.

Formal plot and builder runs execute both tracked and staged `git diff`
quiet checks. Untracked outputs are allowed, but any tracked/staged drift is
fatal. Every figure source must already be a blob at the plot HEAD; results
record those blob ids and `verifiedTrackedTreeClean=true`, and the formal
manifest checks them against the certificate commit.

## Theorem, boundary, and finite-only distinction

- Blue solid lines and filled circles denote proved statements in the
  declared R0.72P class.
- Ochre open markers retain the earlier R0.72O conditional status at exactly
  the same algebraic values.
- Dark dash-dot lines are analytic components or neutral references.
- The Morse wall is an exact analytic boundary. It is not a failed simulation
  and is not evidence that enhanced dissipation itself fails.
- No regression, fitted exponent, interpolated certificate curve, or PDE
  evolution is allowed.
- Any future finite diagnostic must be added with a separate `finite-only`
  status and may not alter a theorem curve or theorem constant.

## Surface and QA

The static Matplotlib figure uses the R0.72O journal footprint, 177.8 x
132.08 mm, and exports editable-text SVG, one-page PDF, and 600 dpi PNG. The
palette is capped at blue and ochre plus warm neutrals, with line style and
marker fill carrying status in grayscale. A research blossom is locked to
the top-right header corner.

Formal QA requires final-size, grayscale, and PDF-raster inspection at 180
dpi; formula checks for all four panels; passed certificate lineage; source
and output hashes; public/master byte identity; and explicit inspection of
the proved/boundary/conditional distinctions.

Automatic validation precedes a mandatory human stop on the three QA
surfaces. Only the human inspection authorizes
`R072P_VISUAL_QA_INSPECTED=true`. The builder reruns custom validation before
hashing, rejects extra files or post-validation changes, and the sealed
package must then pass both the repository-generic validator and the flat
checksum ledger.

## Claim boundary

The theorem represented by this figure concerns only two collinear carriers
`(R, 2R)`, declared coherence `B=2`, a fixed nonzero coefficient cone inside
`|lambda| <= 1/8`, one orthogonal affine residue row, and the inherited
exact-root-corrected triangular 2.5D family. The extra affine-residue damping
is beneficial. The compact-ε completion packages bounded coupling with the
same displayed semigroup constants but is not a new asymptotic
enhanced-dissipation theorem. The figure does not establish a common-band
theorem for arbitrary coefficients, arbitrary `N` or `p`, moving or
degenerate critical points, multiscale physical absorption, a general 3D
continuation criterion, finite-time singularity, or global Navier--Stokes
regularity.
