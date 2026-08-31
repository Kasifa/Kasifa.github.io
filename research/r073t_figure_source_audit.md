# R0.73T formal-figure source audit

**Audited directory:**
`research/figures/r073t/fig-r073t-dynamic-autocorrelation/`

**Audit mode:** independent, source-only review of the ten declared source
files; exact row reconstruction; local temporary render; no source edits, no
Git commit, no network, GPU, or DGX

**Verdict:** `BLOCKED_BEFORE_VISUAL_AND_PROVENANCE_SEAL`

The mathematical constants and signs are correct, and the generator rebuilds
the intended 28 rows.  The present source is not yet safe to seal.  There are
three release-blocking defects: Panel C text is visibly clipped, the four
Panel A rows are attributed to a certificate which does not contain their
analytic proof, and the validator trusts two booleans in the certificate
manifest instead of verifying its fail-closed seal.  Several secondary
inventory, wording, and QA gaps are listed below.

## 1. Frozen ten-file source inventory

The directory contains exactly these ten source files before generation:

1. `README.md`
2. `caption.md`
3. `chart-contract-and-source-data.md`
4. `command.txt`
5. `config.json`
6. `contract.json`
7. `plot.py`
8. `qa-protocol.md`
9. `requirements.txt`
10. `validate.py`

The declared generated inventory is internally arithmetically consistent:

| Class | Declared count | Reconstruction |
| --- | ---: | --- |
| source | 10 | the list above |
| raw | 11 | CSV, three figure formats, three QA rasters, environment, results, progress, resource log |
| metadata | 4 | validation, manifest, QA report, SHA sums |
| package | 25 | \(10+11+4\) |
| manifest-bound | 23 | source + raw + validation + QA report |
| expected SHA lines | 24 | 23 bound files + manifest |

The source and JSON syntax checks passed.  No unexpected source file was
present during this audit.

## 2. Independent mathematical reconstruction

### 2.1 Panel A

With

\[
 Q=\|u\|_4^4,\qquad
 X^2=\|\nabla|u|^2\|_2^2,\qquad
 Y=\int |u|^2|\nabla u|^2,
\]

the plotted balance

\[
 Q'+4\nu Y+2\nu X^2
 =4\int p\,u\cdot\nabla |u|^2
\]

has the correct sign and viscous factors.  The pressure estimate

\[
 4\left|\int p\,u\cdot\nabla |u|^2\right|
 \le \nu X^2+{4C_R^2\over\nu}\|u\|_6^6
\]

has the correct Young constant.  Combining it with the R0.73S classical
bound \(\|u\|_6^6\le AQ\) correctly leaves

\[
 Q'+4\nu Y+\nu X^2
 \le {4C_R^2\over\nu}AQ.
\]

Panel A is therefore mathematically correct as a **one-sided estimate**.  It
is not an autonomous closure because \(A(t)\) remains unclosed.

### 2.2 Panel B

For

\[
 v_N=(0,\cos Nx_1,\sin Nx_1),
\]

one has at the displayed initial time

\[
 |v_N|^2=1,\qquad C(h)=\delta_{h0},\qquad
 \dot C_0(0)=-2\nu N^2.
\]

Thus the eight plotted values \(N=1,\ldots,8\) are exactly

\[
 { |\dot C_0(0)|\over2\nu}=N^2
 =1,4,9,16,25,36,49,64.
\]

The constant and normalization pass.  The time \(t=0\) must be displayed;
away from zero the ratio is
\(N^2e^{-2\nu N^2t}\), not \(N^2\).

### 2.3 Panel C

The R0.73T exact certificate gives

\[
 Q'(u_L;0)=-16536\nu L^2-384L,
 \qquad
 Q'(-u_L;0)=-16536\nu L^2+384L.
\]

Therefore the sixteen values at \(L=1,\ldots,8\), after subtracting the
common viscous term, are exactly \(-384L\) and \(+384L\).  The series signs,
legend labels, centering, and vertical-axis formula are correct.

The statement that the full derivative is “dominated” by the quadratic
negative term is true for fixed \(\nu>0\) as \(L\to\infty\), and throughout
the displayed grid when the project normalization \(\nu=1\) is used.  It is
not uniform over arbitrarily small symbolic \(\nu\) and all displayed \(L\).

## 3. Exact 28-row source reconstruction

The generator and independent validator agree row by row on

\[
 4\ \text{Panel A analytic nodes}
 +8\ \text{Panel B points}
 +16\ \text{Panel C points}
 =28\ \text{rows}.
\]

A local `--data-only` reconstruction produced 28 data rows plus the CSV
header.  Every plotted coordinate is an integer, so the intermediate
`float` plus `.17g` serialization introduces no numerical loss on this grid.

The provenance statement does **not** pass:

- Panel B and Panel C, 24 rows in total, are reconstructed from
  `research/certificates/r073t/results.json`.
- Panel A's four analytic identities are not present or proved in that
  finite witness certificate.  They come from the R0.73T continuum analytic
  derivation and R0.73S.
- Nevertheless `row()` assigns every row
  `source_origin=sealed-r073t-fraction-certificate`, and
  `chart-contract-and-source-data.md` says the only data source is
  `results.json`.

This is a release blocker.  The four analytic rows need a distinct analytic
source binding, or the certificate must be extended to bind the exact
analytic claim ledger.  Merely duplicating the same hard-coded formulas in
`plot.py` and `validate.py` is not independent source verification.

## 4. Generator runtime audit

With the actual cached figure dependency directory
`/Users/kasifa/.cache/codex-runtimes/r073s-figure-python`, the generator ran
successfully in a temporary directory and produced:

| Artifact | Observed result |
| --- | --- |
| CSV | 28 data rows |
| PNG | 4204 x 2362 px; configured 600 dpi dimensions pass the validator's two-pixel tolerance |
| final-size QA | 1800 x 1011 px |
| grayscale QA | 1800 x 1011 px |
| PDF QA raster | 1262 x 709 px |
| PDF | one generated page |
| dependency versions | all five pinned versions matched |

Following the README literally with the Codex workspace dependency path
reported for this thread failed at the first render import with
`ModuleNotFoundError: No module named 'matplotlib'`.  The command files leave
`<python-packages>` unresolved.  This is a reproducibility defect rather
than a mathematical error: the README should identify a tested environment
or give an installation/bootstrap command from `requirements.txt`.

The generator fails nonzero when its certificate check fails, and it pins
all constants used by Panels B/C.  Two smaller fail-closed issues remain:

1. neither `--data-only` nor `--render-preseal` is required; invoking the
   script with no mode silently renders;
2. `source_origin` says `sealed` during pre-seal generation, before the
   certificate or figure source commit has necessarily been sealed.

## 5. Validator and seal audit

### 5.1 What already fails closed

- a full lowercase 40-hex source commit is required;
- all ten declared source blobs must equal the working-tree bytes;
- unexpected top-level files fail;
- all source/raw files are required before validation;
- the CSV schema, 28 rows, and every field are rebuilt independently;
- dependency versions, PNG dimensions, PDF page/media box, basic SVG
  markers, configured palette roots, minimum artifact sizes, and the main
  claim boundary are checked;
- any failed `add()` check raises and exits nonzero;
- `--verify-only` requires byte-identical validation, QA report, manifest,
  and SHA sums.

The source-only failure probe exited nonzero on the missing raw inventory,
as intended.

### 5.2 Release-blocking seal weakness

The figure validator runs the exact certificate producer in `--check-only`
mode, but for the certificate seal it only loads
`research/certificates/r073t/manifest.json` and tests

```text
finalSeal == true
sourceCommitAssigned == true
```

It does not run the certificate `seal_package.py --check-only`, verify the
certificate `SHA256SUMS`, or reconstruct the manifest's Git blob bindings.
A stale or manually altered manifest with those two booleans can therefore
cross the figure gate while `results.json` remains computationally valid but
uncommitted.  The figure validator must invoke the fail-closed certificate
seal against its recorded full source commit, or independently recheck the
same blob bindings and sums.

### 5.3 Unpinned validation inventory

The current source produces 89 validation checks:

\[
 17\ \text{fixed pre-row checks}
 +56\ \text{row checks}
 +16\ \text{artifact/visual checks}=89.
\]

No assertion requires `len(checks)==89`.  Removing a check can therefore
lower the reported count while still writing `allChecksPass=true`.  Likewise
the manifest reports 23 bound files and SHA sums should contain 24 lines,
but neither number is explicitly pinned.  These counts should be fixed
before sealing.

### 5.4 QA protocol is stronger than its implementation

The protocol and generated QA report claim an independent PDF raster
comparison and grayscale inspection.  The validator only opens the three QA
PNGs and checks minimum dimensions; it neither regenerates the PDF raster
nor compares it with the PNG, and it does not verify grayscale image mode or
pixel equivalence.  A valid unrelated image could satisfy these automated
checks.  Either implement the comparisons or narrow the QA report to an
explicitly human-confirmed statement.

Additional hardening gaps, not individually release-blocking after the three
issues above are fixed:

- JSON loading does not reject duplicate keys;
- source/raw paths are not required to be nonsymlink regular files;
- `environment.json` package versions and `network=not used` are not checked
  against the sealing runtime;
- the validator does not check the full generated `results.json` inventory
  (`allSourceChecksPass`, row/series counts, certificate count, figure ID);
- config, contract, and output identifiers are only partially cross-bound;
- unexpected subdirectories are ignored.

## 6. Visual and TeX audit

The temporary 178 mm x 100 mm render is not visually sealable.

1. **Panel C title is clipped at the right figure edge.**  “Pressure
   polarization loss” loses its final characters.
2. **Panel C subtitle is more seriously clipped.**  The statement that the
   common \(-16536\nu L^2\) term was removed is truncated, even though this
   distinction is the central anti-misreading safeguard in the QA protocol.
3. The label “static autocorrelation certificate” extends beyond the gold
   Panel A box.
4. The main title says “one upper closure,” while the mathematical result is
   explicitly an unclosed one-sided estimate.  “One upper estimate” or “one
   one-sided budget” would respect the claim boundary.
5. Panels B and C and the caption should state `at t=0`.
6. “Pressure-tensor polarization” is not quite what the sign pair alone
   proves: \(u_L\) and \(-u_L\) have the same \(u\otimes u\) and the same
   pressure.  What changes is the odd velocity phase/sign in the pressure
   work.  “Velocity polarization/phase in the pressure pairing” is the
   exact information loss certified by this pair.

The grayscale encoding itself passes visual inspection: square filled gold
markers remain distinguishable from dashed hollow blue circles.  Axes,
zero line, main equations, and the two plotted laws are otherwise legible.

Because visual confirmation is currently only a command-line boolean, the
validator could still seal this visibly clipped render if the flag were
supplied.  Human QA must refuse confirmation until the clipping and source
language are repaired.

## 7. Final claim boundary and required gate

The following statements are supported after the source defects are fixed:

- the one-sided \(AQ\) differential inequality;
- carrier-scale non-autonomy of complete unweighted scalar autocorrelation;
- signed pressure-work non-identifiability for the exact sign pair;
- exact 24-point witness data and four analytic diagram nodes;
- no simulation, fit, singular solution, new regularity criterion, global
  regularity theorem, or Clay conclusion.

The figure should not be source-sealed or published until all three blocking
items pass a new independent readback:

1. repair visible title/subtitle/box-label clipping and replace “closure”;
2. correct and bind the four Panel A source origins;
3. verify the certificate's actual fail-closed seal rather than two manifest
   booleans.

After those repairs, pin the 89-check and 23/24-file inventories, implement
or narrow the claimed raster comparison, rerender in the tested dependency
environment, and repeat color/grayscale/PDF visual QA.
