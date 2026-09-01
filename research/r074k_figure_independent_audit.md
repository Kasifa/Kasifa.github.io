# R0.74K independent formal-figure audit

**Audit date:** 2026-09-02
**Verdict:** `R074K_FIGURE_INDEPENDENT_AUDIT_PASS`
**Claim boundary:** `FINITE EXACT + CONDITIONAL ROUTE; NOT CLAY`

## 1. Bound artifacts

This verdict is bound to the following bytes. Any change requires a fresh
render, seal, and visual audit.

| Artifact | SHA-256 |
|---|---|
| `research/figures/r074k/fig-r074k-single-inward-collar/figure.pdf` | `826fb9441fbdfa699f39bd528314529a734bf9f371e009aa60d86c6e9046c3bc` |
| `research/figures/r074k/fig-r074k-single-inward-collar/figure.png` | `d0644e4d3b98c73ed53151e9816f7d3ce68028150ede9d939c13eab173a624b5` |
| `research/figures/r074k/fig-r074k-single-inward-collar/plot.py` | `1a8c06fa347693592efb824792fadc1fe673c0d5406c2ec5a8defca37beb79fd` |
| `research/figures/r074k/fig-r074k-single-inward-collar/validate.py` | `7525e697b013a65bcb4031c890ed60dd27870b02f0446d8cede3bdae99f3fd0d` |
| `research/figures/r074k/fig-r074k-single-inward-collar/qa-report.md` | `4275168a47eac1a98bf88b437446b914e5661744355d226d8438cf7a4e446e8a` |
| `research/figures/r074k/fig-r074k-single-inward-collar/SHA256SUMS` | `59ad9518f0525e6fb9234aa4660511ab78bbda14eccf94c1bd5ed680f070753c` |
| `research/r074k_single_collar_exponent_certificate.json` | `67e4ab156d7d5a73fd07e584f3f87f7c9287591856b285bd9a747d00f85de41f` |

## 2. Structural and seal checks

The package validator returned

```text
verify-only PASS 41/41; 25 files; seals PASS
```

An independent `shasum -a 256 -c SHA256SUMS` run returned `OK` for every
listed package file. A byte-level scan found no forbidden C0 or DEL control
characters. The PDF is one unencrypted 178 mm by 92 mm page. The publication
PNG is RGB, 4205 by 2174 pixels, with approximately 600-dpi metadata.

The validator no longer self-certifies visual QA. It reads the explicit
`Manual status: PASS` gate in `qa-report.md`; removing that gate makes the
overall validation status fail.

## 3. Independent visual inspection

The following four post-render surfaces were each inspected:

1. the 600-dpi color master `figure.png`;
2. the 1402 by 724 final-size raster `qa-final-size.png`;
3. the corresponding grayscale raster `qa-grayscale.png`; and
4. the independent 300-dpi PDF raster `qa-pdf.png`.

The current render has no clipping, overpainting, hard overlap, missing glyph,
or unreadable final-size label. The minimum declared font is 5 pt. Panel and
page titles, axes, legends, arrows, formula boxes, and the claim-boundary
footer remain legible at final size. The two quantitative curves remain
distinguishable in grayscale by luminance as well as position.

## 4. Mathematical-label audit

Panel A agrees with the frozen exact table:

- the sharp squared-tail margin is adverse at `m=1` and positive for every
  displayed `m>=2`;
- the inherited denominator-262 margin is adverse at `m=1,2` and positive
  from `m=3` onward; and
- the separate diamond identifies the negative positive-volume-slab margin
  without being confused with either curve.

The legends now state `d_m^2 / 132` and `d_m^2 / 262`, so the denominators
cannot be misread as part of the symbol `p`.

Panel B now draws the exact nested geometry:

- blue `A_j`: `32/63 < |x|/r_j < 64/63`;
- red `A_{j-1}`: `16/63 < |x|/r_j < 32/63`;
- packet center: `15/16`; and
- positive-volume reference height: `4033/8064`.

Both annular labels lie in their corresponding regions, and both `x_2` and
`x_3` labels are visible. The reference-packet scale is marked `PROVED`, while
the true-packet bridge--BV estimate and the `j-1` shear-expulsion estimate are
separately marked `OPEN`. The compact conditional box displays
`sup_tau [I_j(tau)]_+ <= C Gamma_j L_j R_j^5`, explicitly binds it to open
hypothesis (4.3), and makes the familywise conclusion conditional on that
hypothesis.

## 5. Audit limit

This PASS certifies the figure package's byte integrity, visual quality,
mathematical labeling, and conservative claim boundary. It does not prove the
true-packet bridge--BV estimate, nearest-inner shear expulsion, hypothesis
(4.3), a matching collar upper, a universal endpoint result, regularity,
singularity formation, novelty, or priority. The figure contains exact finite
bookkeeping and an analytic dependency diagram, not DNS or simulation.

**NOT CLAY.**
