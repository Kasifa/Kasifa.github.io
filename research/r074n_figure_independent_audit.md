# R0.74N independent figure-package audit

## Result

I audited the sealed package at
`research/figures/r074n/fig-r074n-all-shell-synthesis/` from a stable
snapshot.  I did not accept the package's recorded validation result as
evidence.  The result is

\[
 \boxed{\text{INDEPENDENT FIGURE-PACKAGE AUDIT: PASS; NOT CLAY.}}
\]

This verdict concerns reproducibility, exact-data binding, rendering,
typography, visual legibility, and the stated claim boundary of one formal
figure.  It does not enlarge the R0.74N theorem.  In particular, it proves no
universal endpoint estimate, singularity statement, or Navier--Stokes
regularity result.

## 1. Stable snapshot and seal

The publication masters and package seals are:

| file | SHA-256 |
|---|---|
| `figure.svg` | `830c091a6b55abf8c4e1a737e595d0ada9a7a088d4b77b9a0678c22ee35590f8` |
| `figure.pdf` | `cbc1de4ea76e201d921fab1b4cbb50913838106c2814cc9a460ce390cc4c3878` |
| `figure.png` | `809a0c89e94494d562c35baecb993f8674b1539436710775484374216909bad4` |
| `manifest.json` | `fc5d6f5a9fe861068ffc4014f42d7eecd7261dbd41fd4d6b0f7f29c55458cea9` |
| `validation.json` | `f28e2c40eb58a8f284a8e1b681c3bf0561c6aa26cc805076bd438d9cc58d1bad` |
| `SHA256SUMS` | `4cd2b72d53f8ebcf02b403c3f5497ac159a85d49bfe87b9f944be1a95605fa3f` |

The directory contains 26 physical files.  The manifest contains 24 package
entries and 21 external bindings.  `SHA256SUMS` contains 25 lines, one for
every package file except the checksum file itself.  I independently
recomputed every byte count and SHA-256 value; all entries and all 25
checksum lines matched.

The external chain includes the final problem freeze, theorem source,
independent analytic audit, cross-note implication audit, final source
rebind, gap matrix, reader source, dictionary, reader audit, Python
certificate, Ruby reconstruction, certificate report, two independent
finite audits, bounded literature note and its independent audit, and the
inherited audited R0.74L/R0.74M mechanisms.  The principal final bindings
are:

| external object | SHA-256 |
|---|---|
| `research/r074n_problem_freeze.md` | `4b2df724cf81cf28d0c9b89636ae166ade11746f623ca2a3466f08e4e1adfacc` |
| `research/r074n_all_shell_synthesis.md` | `ca1ddabb6ea931b2f1a96b5cb000e955492c6852b0ea3b2aaa6148c6f3fa9e1e` |
| `research/r074n_all_shell_independent_audit.md` | `5173ac954ca82e2abc0371258527ddd8b6bc372e43de6c3a2aeea2a9f2b187e9` |
| `research/r074n_crossnote_implication_independent_audit.md` | `7c289055939cdbf21780337e7da2a1d91109172d89a6c168258703124b50be8a` |
| `research/r074n_final_source_rebind_audit.md` | `ea51805047a8dbb3e914f4f29c8f93fd117ff1a22d8320f832af1cab7002042c` |
| `research/r074n_gap_matrix.md` | `986a2ddc20318f6f70a968f80fd972c671e7ae43fe769e2acd00d4230d08fb06` |
| `research/r074n_report-source.md` | `b3a50fe4aaf9ca1b98d92fa4df3ab3ff3a461163fc9d857c0219cea3a29272c1` |
| `research/r074n_bilingual_dictionary.md` | `d1418d676333293fab29c11d21da053e60f61241068d4b8aaf2565636c270755` |
| `research/r074n_reader_source_independent_audit.md` | `ab63f12d729d60012e68205015dc4e6a6a93896d0b484bbb60c7e6dbaedbd00e` |
| `research/r074n_all_shell_certificate.json` | `53481cf393308a786c3a414da6238faaa9b8a15dac0017638c47584615bbecc2` |
| `research/r074n_certificate_independent_audit.md` | `53a8d9c71955070c56587c2370cc5a45388084c1dcd16bac366f34e4e73e20d2` |
| `research/r074n_certificate_adversarial_audit.md` | `0c251b5ba3f30fae668aaa9ca1504ee4f713feb26e60aeb674a02f9b77064448` |
| `scripts/r074n_all_shell_certificate.py` | `1174dfba5484fa53f4022ed5725bbd511cf4596f5b133997262844c439857e8c` |
| `scripts/r074n_all_shell_certificate_independent.rb` | `32621a28ca2312fcddea83135309ecd7cd3cc3d2515f929b401d04b9d221f744` |

The adversarial certificate audit is therefore not merely mentioned in
prose: its exact final hash is part of the figure manifest.

## 2. Isolated deterministic reconstruction

I copied the package and all 21 manifest-selected external inputs into a new
repository-shaped temporary directory.  No `.git` state or unlisted research
file was copied.

First, I ran the copied `plot.py`.  The regenerated SVG, vector PDF, 600-dpi
PNG, final-size raster, grayscale raster, independent PDF raster, SVG Quick
Look raster, `results.json`, `environment.json`, `progress.ndjson`, and
`command.txt` were byte-identical to the sealed originals.

Second, I ran the copied `validate.py`.  It returned

```text
verify-only PASS 67/67; 24 package entries
```

Its regenerated `manifest.json`, `validation.json`, `SHA256SUMS`, and
`layout-bounds.json` were byte-identical to the sealed originals.  The
validator also reran the Python exact certificate and the independent Ruby
`Rational` reconstruction from inside the temporary repository.  Both passed.

This establishes deterministic reconstruction of both the visual outputs
and the seal, rather than only a successful read of previously generated
files.

The post-correction reconstruction left the SVG, PDF, PNG, and all four QA
rasters byte-identical to the prior figure.  Only the validator and generated
binding/seal files changed.

## 3. Independent exact-data reconstruction

I parsed all 20 rows of `source-data.csv` with a separate exact-rational
program which did not import `plot.py` or `validate.py`.  Every decimal field
agreed with its canonical rational field.  The reconstructed identities
include

\[
 \frac35-\frac{32}{63}-\frac1{16}=\frac{149}{5040},
\]

\[
 \frac1{16}-\frac1{320}-\frac8{3969}
 =\frac{72851}{1270080}>0,
\]

and

\[
 3\frac8{3969}-\frac1{320}
 =\frac{1237}{423360}>0.
\]

The table also agrees with the source proof's final-segment length (1/64),
displacement prefactor (1/32768), tail denominator (1056), outer
collar-volume factor (4^k), eventual ratio (1/2), and identity
(4^{j+1}=(4096/3969)L_j^2).

The data contract explicitly says that the outer bars are ordinal shell
symbols and not quantitative observations.  No plotted height is used as
mathematical evidence.

## 4. Semantic correspondence to the proof

The figure preserves the exact disjoint decomposition

\[
 \{k\ge1\}
 =\{1\le k\le j-1\}\,\dot\cup\,\{j\}\,\dot\cup\,\{k\ge j+1\}.
\]

The three lower panels then record the correct, distinct obligations.

1. **Combined inward range.**  The figure states the uniform positive-chord
   bound
   \(\overline D_<\le C\sum_{k\ge1}2^k\Gamma_k<\infty\), support in the
   common padded \(r_-\) tube, the inherited R0.74M expulsion, and the separate
   good/bad payments.  It explicitly says that no shell or packet
   cancellation is used.
2. **Target shell.**  The figure labels the R0.74L true-packet estimate as an
   absolute estimate including both radial faces and sends it to
   \(C\Gamma_jLR^5\).
3. **Outer range.**  The figure states
   \(|\mathcal J_{j,k}|\le C\Gamma_k4^kR^4\), the infinite geometric majorant,
   the eventual ratio \(1/2\), and the positive reserve
   \(3c_\gamma-\rho=1237/423360\).  The panel title explicitly identifies the
   super-Gaussian outer tail.

All three branches visibly terminate at the same target
\(C\Gamma_jLR^5\).  The header says that the ranges have no missing or
overlapping row.

The graphic itself is a shell-synthesis figure, so it does not draw the later
cross-note energy consequence.  The final bound corpus now proves, on this
same exact family,

\[
 X_j\asymp\mathfrak C_j\asymp B_j^2L_jR_j^2
 \asymp P_j^{2/3}\sqrt{1+\log_+P_j},
\]

with component bounds

\[
 cT_j\le\mathcal U_j\le X_j\le CT_j,
 \qquad 0\le\mathcal D_j\le CT_j.
\]

This is a separately audited, non-circular cross-note consequence.  It does
not give a matching lower bound for \(\mathcal D_j\), and it does not prove a
universal endpoint inequality for arbitrary smooth flows.

## 5. Vector, font, and physical-size checks

The SVG contains 50 text nodes and 31 path/rectangle/circle/polygon vector
nodes, with no raster image node.  It embeds two complete TTF payloads:

| embedded font | decoded bytes | decoded SHA-256 |
|---|---:|---|
| DejaVu Sans regular | 757076 | `7da195a74c55bef988d0d48f9508bd5d849425c1770dba5d7bfc6ce9ed848954` |
| DejaVu Sans bold | 705684 | `e6476c1b80502924294eed40894c5b18e06c181444ca953e5334262df9c27724` |

Those bytes exactly equal the pinned fonts used by the generator.  The SVG
is therefore self-contained and does not depend on an installed-font name.

The PDF is one unencrypted vector page.  Its measured media box is
(177.9999897\,\mathrm{mm}\times100.0000117\,\mathrm{mm}), consistent with
the declared (178\,\mathrm{mm}\times100\,\mathrm{mm}) double-column size.
It has no image XObject and carries embedded subset DejaVu Sans regular and
bold TrueType fonts.

The publication raster is (4205\times2363) RGB pixels with 600-dpi
metadata.  The final-size and grayscale checks are (1402\times788) at
200 dpi, and the independent PDF raster is (2103\times1182) at 300 dpi.

## 6. Visual inspection

I inspected these five surfaces at their native resolution:

1. `figure.png`;
2. `qa-final-size.png`;
3. `qa-grayscale.png`;
4. `qa-pdf.png`; and
5. `qa-svg-quicklook.png`.

I also regenerated the Quick Look raster in the isolated reconstruction; it
was byte-identical to the archived QA surface.  There is no clipping,
overlap, detached label, broken outline, serif substitution, or missing
glyph.  The combined inward rings, target annulus, and outer ordinal bars
remain distinct in grayscale through geometry, position, and dash pattern.
The four-line outer summation remains readable at final size, and its bars
are visibly labeled as non-quantitative symbols.

## 7. Fail-closed history

The package did not pass prematurely.  The first validator run stopped at
59/62 because the external analytic audit had not yet been promoted to
`PASS`, manual visual QA was still pending, and the vector-node predicate
failed to count SVG circles.  The first two states were resolved only after
the external audit and five-surface inspection; the predicate was repaired
to count the actual vector primitives.

After the adversarial finite audit was added, validation again stopped at
63/64 because a literal sentence matcher crossed a Markdown line break.  The
matcher was narrowed to the same explicit anti-self-certification clause;
the bound external file and its hash did not change.  Before the final seal,
the dense outer summation was also split over two lines and the panel was
explicitly titled `super-Gaussian outer tail` for final-size readability.

No mathematical source file was changed during figure construction or this
audit.

After the post-correction freeze, this audit failed the old source hashes
closed, rebound 21 final source/audit inputs including the new cross-note
audit, and reran the isolated reconstruction.  The expanded validator passed
67/67 while all publication-master bytes remained unchanged.

## 8. Claim and simulation boundary

The generator contains no random-number generator, numerical trajectory, or
DNS code.  The package consistently records `simulation: false` and says
`schematic`, `not to scale`, `no DNS`, and `no sampled path`.

The exact status is:

- the R0.74N all-shell source theorem has independent analytic audit result
  PASS and a final source rebind;
- the finite arithmetic has independent Python/Ruby and adversarial audits;
- this note independently passes the sealed formal figure package;
- the shell theorem concerns one frozen exact smooth family and one local
  collar observable;
- the same exact family now has the separately audited matching
  \(X_j\) and \(\mathfrak C_j\) laws;
- only an upper bound, not a matching lower bound, is proved for the
  dissipation component \(\mathcal D_j\) alone;
- the universal square-root-log endpoint inequality for arbitrary smooth
  solutions, arbitrary-flow collar control, and every universal regularity
  implication remain OPEN; and
- no Clay problem claim is made.

\[
 \boxed{\text{R0.74N FIGURE PACKAGE: PASS; FAMILYWISE ONLY; NOT CLAY.}}
\]
