# R0.74L — independent figure audit

## Final verdict and scope

**PASS after fail-closed repair and complete reseal.**  This audit covers the
formal figure package only.  It does not supply a new analytic proof, a
novelty claim, or any Navier--Stokes regularity conclusion.

The audited package is

    research/figures/r074l/fig-r074l-forward-clock-bv/

and the final resealed `SHA256SUMS` hash is

    4e2df61354222bc74cc343315e98397c0a9bad05289097ac8fcc9006eeb1215d.

## Fail-closed repair ledger

The first independent pass returned **FAIL-CLOSE** at the former
`SHA256SUMS` hash

    499886ccb7eeec8fdf8cf3f1b1e984cca7442fa2069b95ddd947ebc53e9fbd04.

It found one decimal transcription error and four displayed-label
ambiguities even though the original validator reported 43/43.  All five
were corrected before release:

1. the decimal column for `189/68157440` is now
   `0.000002772991473858173`;
2. the initial law reads `X0 ~ K_T, T=R^2`, not the ambiguous `K_R^2`;
3. the proved target is the script majorant `ℬ_j(tau)`, not the amplitude
   `B_j`;
4. the `R^-3` factor is labelled `∫ H_R du`, rather than as a bare
   kernel derivative; and
5. the bad-path ledger writes the separate crude-slice factor `L` and
   probability factor `R`, so it does not suggest
   `P(bad) = O(LR)`.

The validator was strengthened to compare every decimal field with its
exact rational value and to bind the displayed mathematical labels.  The
package was then regenerated and resealed from source.

## Independent structural and numerical reconstruction

An isolated temporary-copy run returned 45/45.  Regenerated
`validation.json`, `layout-bounds.json`, `manifest.json`, and `SHA256SUMS`
were byte-identical to the resealed originals.  All 22 entries in
`SHA256SUMS` passed.

The independent data reconstruction found:

| Check | Result |
|---|---|
| CSV exact keys | PASS, 20/20 |
| decimal-to-exact agreement | PASS, 20/20 at relative/absolute tolerance `5e-15` |
| good-path `R`-exponent sum | PASS, `5` |
| bad-path `R`-exponent sum | PASS, `5` |
| independent Ruby finite certificate | PASS, 24/24 |

## Visual and vector inspection

The 600-dpi PNG, final-size surface, grayscale surface, and independently
rasterized PDF all pass: no clipping, overlap, missing glyph, broken arrow,
or unreadable final-size label was found.  The symbols `ℬ`, `∫`, `θ`, and
the exact reserve fraction survive rendering.  Grayscale distinction is
retained through position, borders, and direct labels.

The PDF is one unencrypted vector page of approximately 178 mm by 92 mm,
with zero image XObjects.  The SVG contains no embedded raster image and
retains all corrected labels as text.  Blank PDF metadata and one unused
font setup resource are nonblocking hygiene observations; neither changes
the mathematical content or the vector status.

## Final bound hashes

| Object | SHA-256 |
|---|---|
| `SHA256SUMS` | `4e2df61354222bc74cc343315e98397c0a9bad05289097ac8fcc9006eeb1215d` |
| `manifest.json` | `4ad82fb1cfd7f9d1aea43ea5378bd1a626bc80933e94c26e8f3008f7dad83c42` |
| `validation.json` | `390d8ef9f66e115f4c4c4a914270824f9ecaea3462e39b8a6573977d84ba6ab0` |
| `source-data.csv` | `1f57ff93fb730c630e756f858e6794942045ce4eecd4a7032888519548ce755a` |
| `plot.py` | `0ed7671c2714018143dbaf93f352e0bb3c16c50bd96e602b1821534f58d20a85` |
| `validate.py` | `b69b04c522cdaf8ed63ef6a30dae25d095665b5a01f79d355f2cea02c25d1126` |
| `figure.svg` | `1984bfc1aa6485601955caf1cdf7f728941429b28dfee1ae4db39f213ebb21fa` |
| `figure.pdf` | `6d714dab40747125f1b6587342c6fa559d5eaf26e8690a3e9de33770b75d3fb1` |
| `figure.png` | `8fa2e33db7f7713e0c54e924468b3135a94b10812cafb0c2f3d1429ca1e0026d` |
| `qa-final-size.png` | `ffeb8c68a6dd8928ee7757daf9aaa8538226febffc14d5f5183db9f3b187a38d` |
| `qa-grayscale.png` | `5a20fb41f04fc99e82527ac1859667839edc12f16891dccd2e28b705b973c5bd` |
| `qa-pdf.png` | `5d15608e7d443d125396023bc96c77a47843bf71de0f84b2c8604adad813f905` |
| `results.json` | `92c1151c44d8c740554f3985b31cef489dbde82878b514fc59ec701c7662b6c2` |

The external analytic bindings in the package manifest also match the
current proof, finite certificate, analytic audit, Python producer, and
independent Ruby verifier.  No correction remains open within figure-QA
scope.

The figure states the exact boundary: main target collar proved, nearest
inward collar open, no DNS or simulation, and **NOT CLAY**.
